# /// script
# requires-python = ">=3.11"
# dependencies = ["pydantic>=2"]
# ///
"""
Review report validator: validates candidate JSON artifacts against type-specific
pydantic models. The model is selected by report_type ("general" or "slop").

Exits 0 on valid, 1 on any validation failure with diagnostic messages.
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

INFRA_PREFIXES = [".github/", ".agents/", "quality-control/", "opencode/skills/"]

LOW_SIGNAL_CATEGORIES = frozenset(
    {
        "code-style",
        "style",
        "readability",
        "import-placement",
        "import-order",
        "file-length",
        "line-length",
        "naming",
        "naming-convention",
        "duplication",
        "duplicate-code",
        "comment-style",
        "formatting",
    }
)

_INVARIANT_REJECT = [
    re.compile(p, re.IGNORECASE)
    for p in [
        "-O",
        "optimized mode",
        "clean code",
        "no violation",
        r"nothing (?:to |)report",
        r"looks? (?:good|correct|fine|right|ok)",
        r"no issues? found",
        r"appears? correct",
        r"everything (?:looks|seems|is)",
        r"i (?:don't|do not|did not|didn't) find",
    ]
]


def _path_exists_in_git(path: Path, sha: str) -> bool:
    """True if *path* exists at *sha* in the repository at CWD."""
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{sha}:{path.as_posix()}"],
        capture_output=True,
    )
    if result.returncode >= 2:
        raise RuntimeError(
            f"git cat-file -e {sha}:{path} failed: {result.stderr.decode().strip()}"
        )
    return result.returncode == 0


def _is_infra_path(p: Path) -> bool:
    s = p.as_posix()
    return any(s.startswith(prefix) for prefix in INFRA_PREFIXES)


# ---------------------------------------------------------------------------
# Shared leaf types
# ---------------------------------------------------------------------------


class Location(BaseModel):
    path: Path
    start_line: int = Field(ge=1)
    end_line: int = Field(ge=1)


class Evidence(BaseModel):
    kind: str
    path: Path
    lines: list[Annotated[int, Field(ge=1)]] = Field(min_length=2, max_length=2)


class CheckedSurface(BaseModel):
    path: Path
    reason: str
    lines_read: list[Annotated[int, Field(ge=1)]] = Field(min_length=2, max_length=2)
    result: str


# ---------------------------------------------------------------------------
# General review
# ---------------------------------------------------------------------------


class GeneralFinding(BaseModel):
    tier: Literal["tier1", "tier2"]
    label: str
    category: str
    location: Location
    violated_invariant: str = Field(min_length=20)
    proof_command: str = Field(min_length=10)
    symptom: str
    source: str
    consequence: str
    remedy: str
    evidence: list[Evidence] = Field(min_length=1)

    @field_validator("category")
    @classmethod
    def _no_infra_categories(cls, v: str) -> str:
        v_lower = v.lower()
        for cat in ("infra", "infrastructure", "ci", "workflow", "config"):
            if cat in v_lower:
                raise ValueError(
                    f"REJECTED: forbidden category '{v}'. "
                    f"FIX: use a defect-type category like 'semantic-regression', "
                    f"'incorrect-output', 'test-quality', 'null-safety', etc. "
                    f"Category describes the defect, not the CI layer."
                )
        return v

    @model_validator(mode="after")
    def _tier_category_consistency(self) -> Self:
        if self.category.lower() in LOW_SIGNAL_CATEGORIES and self.tier == "tier1":
            raise ValueError(
                f"REJECTED: category '{self.category}' is low-signal, "
                f"must be tier2, not tier1. "
                f"FIX: change tier to 'tier2' or use a non-low-signal category "
                f"(e.g. 'semantic-regression', 'test-quality'). "
                f"Low-signal categories: {sorted(LOW_SIGNAL_CATEGORIES)}"
            )
        return self

    @field_validator("violated_invariant")
    @classmethod
    def _no_empty_invariant(cls, v: str) -> str:
        for pat in _INVARIANT_REJECT:
            if pat.search(v):
                raise ValueError(
                    f"REJECTED: violated_invariant contains prohibited pattern "
                    f"'{pat.pattern}'. "
                    f"FIX: violated_invariant must name a specific violated contract "
                    f"or behavior. Bad: 'clean code'. "
                    f"Good: 'The CI runner silently swallows diff-retrieval failures "
                    f"instead of aborting'."
                )
        return v


class GeneralReport(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schema_version: Annotated[int, Field(ge=1)] = 1
    report_type: Literal["general"] = "general"
    repo_sha: str = Field(min_length=40, max_length=40)
    review_scope: list[Path] = Field(min_length=1)
    findings: list[GeneralFinding] = Field(min_length=1)
    checked_surfaces: list[CheckedSurface]
    rejected_easy_wins: list[str]

    @model_validator(mode="after")
    def _check_git_paths(self) -> Self:
        sha = self.repo_sha
        for i, p in enumerate(self.review_scope):
            if not _path_exists_in_git(p, sha):
                raise ValueError(
                    f"REJECTED: review_scope[{i}] path '{p}' does not exist "
                    f"at commit {sha[:8]}. "
                    f"FIX: only list files that exist in git at repo_sha. "
                    f"Run 'git cat-file -e {sha}:{p}' to verify."
                )
        for i, finding in enumerate(self.findings):
            loc_path = finding.location.path
            if _is_infra_path(loc_path):
                raise ValueError(
                    f"REJECTED: findings[{i}] location is an infrastructure "
                    f"path: {loc_path}. "
                    f"FIX: findings must target source or test files in the PR diff, "
                    f"not CI/agent infrastructure files."
                )
            if not _path_exists_in_git(loc_path, sha):
                raise ValueError(
                    f"REJECTED: findings[{i}] location path '{loc_path}' "
                    f"does not exist at commit {sha[:8]}. "
                    f"FIX: every finding path must exist in git at repo_sha. "
                    f"Run 'git cat-file -e {sha}:{loc_path}' to verify."
                )
            for j, ev in enumerate(finding.evidence):
                if not _path_exists_in_git(ev.path, sha):
                    raise ValueError(
                        f"REJECTED: findings[{i}].evidence[{j}] path '{ev.path}' "
                        f"does not exist at commit {sha[:8]}. "
                        f"FIX: every evidence path must exist in git at repo_sha. "
                        f"Run 'git cat-file -e {sha}:{ev.path}' to verify."
                    )
        return self

    @model_validator(mode="after")
    def _require_substantive_finding(self) -> Self:
        if not any(
            f.tier == "tier1" or f.category.lower() not in LOW_SIGNAL_CATEGORIES
            for f in self.findings
        ):
            raise ValueError(
                "REJECTED: at least one finding must be substantive "
                "(Tier 1 or non-low-signal category). "
                f"FIX: all your findings are low-signal categories at tier2. "
                f"Add at least one Tier 1 finding or use a substantive category "
                f"(not one of {sorted(LOW_SIGNAL_CATEGORIES)}). "
                f"A substantive finding has a concrete 'violated_invariant' and "
                f"reproducible 'proof_command'."
            )
        return self


# ---------------------------------------------------------------------------
# Slop review
# ---------------------------------------------------------------------------


class SlopFinding(BaseModel):
    tier: Literal["tier1", "tier2"]
    label: str
    category: str
    location: Location
    violated_invariant: str = Field(min_length=20)
    proof_command: str = Field(min_length=10)
    pattern: str
    task_narrative: str
    slop_narrative: str
    why_it_matters: str
    user_surprise: str
    existential_justification: str
    failure_mode: str
    evidence: list[Evidence] = Field(min_length=1)

    @field_validator("category")
    @classmethod
    def _no_infra_categories(cls, v: str) -> str:
        v_lower = v.lower()
        for cat in ("infra", "infrastructure", "ci", "workflow", "config"):
            if cat in v_lower:
                raise ValueError(
                    f"REJECTED: forbidden category '{v}'. "
                    f"FIX: use a defect-type category like 'bridge-burning', "
                    f"'runtime-control-flow', 'validation-evasion', "
                    f"'defaults-and-fallbacks', etc. "
                    f"Category describes the slop pattern, not the CI layer."
                )
        return v

    @model_validator(mode="after")
    def _tier_category_consistency(self) -> Self:
        if self.category.lower() in LOW_SIGNAL_CATEGORIES and self.tier == "tier1":
            raise ValueError(
                f"REJECTED: category '{self.category}' is low-signal, "
                f"must be tier2, not tier1. "
                f"FIX: change tier to 'tier2' or use a non-low-signal category "
                f"(e.g. 'bridge-burning', 'validation-evasion'). "
                f"Low-signal categories: {sorted(LOW_SIGNAL_CATEGORIES)}"
            )
        return self

    @field_validator("violated_invariant")
    @classmethod
    def _no_empty_invariant(cls, v: str) -> str:
        for pat in _INVARIANT_REJECT:
            if pat.search(v):
                raise ValueError(
                    f"REJECTED: violated_invariant contains prohibited pattern "
                    f"'{pat.pattern}'. "
                    f"FIX: violated_invariant must name a specific violated contract "
                    f"or behavior. Bad: 'clean code'. "
                    f"Good: 'The agent suppresses stderr to construct synthetic "
                    f"fallback results instead of failing on missing files'."
                )
        return v


class SlopReport(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schema_version: Annotated[int, Field(ge=1)] = 1
    report_type: Literal["slop"] = "slop"
    repo_sha: str = Field(min_length=40, max_length=40)
    review_scope: list[Path] = Field(min_length=1)
    findings: list[SlopFinding] = Field(min_length=1)
    checked_surfaces: list[CheckedSurface]
    rejected_easy_wins: list[str]

    @model_validator(mode="after")
    def _check_git_paths(self) -> Self:
        sha = self.repo_sha
        for i, p in enumerate(self.review_scope):
            if not _path_exists_in_git(p, sha):
                raise ValueError(
                    f"REJECTED: review_scope[{i}] path '{p}' does not exist "
                    f"at commit {sha[:8]}. "
                    f"FIX: only list files that exist in git at repo_sha. "
                    f"Run 'git cat-file -e {sha}:{p}' to verify."
                )
        for i, finding in enumerate(self.findings):
            loc_path = finding.location.path
            if _is_infra_path(loc_path):
                raise ValueError(
                    f"REJECTED: findings[{i}] location is an infrastructure "
                    f"path: {loc_path}. "
                    f"FIX: findings must target source or test files in the PR diff, "
                    f"not CI/agent infrastructure files."
                )
            if not _path_exists_in_git(loc_path, sha):
                raise ValueError(
                    f"REJECTED: findings[{i}] location path '{loc_path}' "
                    f"does not exist at commit {sha[:8]}. "
                    f"FIX: every finding path must exist in git at repo_sha. "
                    f"Run 'git cat-file -e {sha}:{loc_path}' to verify."
                )
            for j, ev in enumerate(finding.evidence):
                if not _path_exists_in_git(ev.path, sha):
                    raise ValueError(
                        f"REJECTED: findings[{i}].evidence[{j}] path '{ev.path}' "
                        f"does not exist at commit {sha[:8]}. "
                        f"FIX: every evidence path must exist in git at repo_sha. "
                        f"Run 'git cat-file -e {sha}:{ev.path}' to verify."
                    )
        return self

    @model_validator(mode="after")
    def _require_substantive_finding(self) -> Self:
        if not any(
            f.tier == "tier1" or f.category.lower() not in LOW_SIGNAL_CATEGORIES
            for f in self.findings
        ):
            raise ValueError(
                "REJECTED: at least one finding must be substantive "
                "(Tier 1 or non-low-signal category). "
                f"FIX: all your findings are low-signal categories at tier2. "
                f"Add at least one Tier 1 finding or use a substantive category "
                f"(not one of {sorted(LOW_SIGNAL_CATEGORIES)}). "
                f"A substantive slop finding has a concrete 'violated_invariant' and "
                f"a reproducible 'proof_command' showing the bridge-burning pattern."
            )
        return self


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------

_MODEL_BY_TYPE: dict[str, type[GeneralReport | SlopReport]] = {
    "general": GeneralReport,
    "slop": SlopReport,
}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: uv run {sys.argv[0]} <report.json>")
        sys.exit(1)

    result_path = Path(sys.argv[1])
    if not result_path.is_file():
        print(f"Error: file not found: {result_path}", file=sys.stderr)
        sys.exit(1)

    with open(result_path) as f:
        data: dict = json.load(f)

    report_type = data.get("report_type", "")
    model_cls = _MODEL_BY_TYPE.get(report_type)
    if model_cls is None:
        print(f"Error: unknown report_type '{report_type}'", file=sys.stderr)
        sys.exit(1)

    try:
        model_cls(**data)
    except Exception as exc:
        msg = str(exc)
        # pydantic ValidationError has .errors() with structured messages
        # but str(exc) already renders them sanely.
        print(f"Report validation FAILED:\n  {msg}")
        sys.exit(1)

    print("Report validation PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
