import pytest

from extract_unresolved_issues.cli import app


def test_resolve_missing_args():
    # Should fail if comment_id or justification are not provided
    with pytest.raises(SystemExit):
        app(["resolve"])


def test_resolve_invalid_justification(capsys):
    # Should fail due to validation error in logic if justification is invalid
    # It catches exception and calls sys.exit(1)
    with pytest.raises(SystemExit) as exc:
        app(["resolve", "123", "just fixed it", "--repo", "owner/repo"])
    assert exc.value.code == 1


def test_issues_invalid_pr_url():
    with pytest.raises(SystemExit) as exc:
        app(["issues", "invalid-url"])
    assert exc.value.code == 1
