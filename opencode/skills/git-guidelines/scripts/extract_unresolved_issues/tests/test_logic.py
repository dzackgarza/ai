import pytest
from pydantic import ValidationError

from extract_unresolved_issues.logic import (
    parse_pr_url,
    validate_justification,
)
from extract_unresolved_issues.models import (
    ResolveInput,
)


def test_parse_pr_url():
    pr = parse_pr_url("owner/repo#123")
    assert pr.repo == "owner/repo"
    assert pr.number == 123

    pr = parse_pr_url("https://github.com/owner/repo/pull/123")
    assert pr.repo == "owner/repo"
    assert pr.number == 123

    with pytest.raises(ValueError):
        parse_pr_url("invalid-format")


def test_validate_justification():
    assert validate_justification("Fixed in commit 1234567890")
    assert validate_justification("See issue #456")
    assert validate_justification("https://github.com/owner/repo/issues/789")
    assert validate_justification("/commit/abcdef1234")

    assert not validate_justification("I fixed it")
    assert not validate_justification("done")


def test_resolve_input_validation():
    # Should work
    ResolveInput(comment_id="123", justification="commit abcdef")

    # Missing fields should fail
    with pytest.raises(ValidationError):
        ResolveInput.model_validate({"comment_id": "123"})
