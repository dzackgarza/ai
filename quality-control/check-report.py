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
from typing import Annotated, Literal

from pydantic import BaseModel, Field, field_validator, model_validator

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

INFRA_PREFIXES = [".github/", ".agents/", "quality-control/", "opencode/skills/"]

REPORT_MIN_LENGTH = 200


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

_GENERAL_MARKERS = [
    re.compile(r"Finding\s+\d+"),
    re.compile(r"Symptom:"),
    re.compile(r"Source:"),
    re.compile(r"Consequence:"),
]

_GENERAL_REJECT = [
    re.compile(p, re.IGNORECASE)
    for p in [
        "-O",
        "optimized mode",
        "passed without",
        "no violations",
        "clean code",
        r"all.*(?:other|remaining).*(?:passed|clean|fine|acceptable)",
        r"no.*(?:bridge.burning|runtime.control.flow).*violation",
        r"nothing (?:to |)report",
        "full repository sweep",
        r"full.*sweep.*(?:excluding|excluded)",
        "excluding forbidden",
        "excluded targets",
    ]
]


class GeneralFinding(BaseModel):
    tier: Literal["tier1", "tier2"]
    label: str
    category: str
    location: Location
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
                raise ValueError(f"forbidden category: {v}")
        return v


class GeneralReport(BaseModel):
    schema_version: Annotated[int, Field(ge=1)] = 1
    report_type: Literal["general"] = "general"
    repo_sha: str = Field(min_length=40, max_length=40)
    review_scope: list[Path] = Field(min_length=1)
    findings: list[GeneralFinding] = Field(min_length=1)
    checked_surfaces: list[CheckedSurface]
    rejected_easy_wins: list[str]
    score: Annotated[int, Field(ge=0, le=100)]
    report: str = Field(min_length=REPORT_MIN_LENGTH)

    @model_validator(mode="after")
    def _check_git_paths(self) -> GeneralReport:
        sha = self.repo_sha
        for i, p in enumerate(self.review_scope):
            if not _path_exists_in_git(p, sha):
                raise ValueError(f"review_scope[{i}] path does not exist at {sha}: {p}")
        for i, finding in enumerate(self.findings):
            loc_path = finding.location.path
            if _is_infra_path(loc_path):
                raise ValueError(
                    f"findings[{i}] location is an infrastructure path: {loc_path}"
                )
            if not _path_exists_in_git(loc_path, sha):
                raise ValueError(
                    f"findings[{i}] location path does not exist at {sha}: {loc_path}"
                )
            for j, ev in enumerate(finding.evidence):
                if not _path_exists_in_git(ev.path, sha):
                    raise ValueError(
                        f"findings[{i}].evidence[{j}] path does not exist "
                        f"at {sha}: {ev.path}"
                    )
        return self

    @field_validator("report")
    @classmethod
    def _check_report_markers(cls, v: str) -> str:
        for marker in _GENERAL_MARKERS:
            if not marker.search(v):
                raise ValueError(f"report missing required marker: {marker.pattern}")
        for pat in _GENERAL_REJECT:
            if pat.search(v):
                raise ValueError(f"report contains prohibited pattern: {pat.pattern}")
        return v


# ---------------------------------------------------------------------------
# Slop review
# ---------------------------------------------------------------------------

_SLOP_MARKERS = [
    re.compile(r"Finding\s+\d+"),
    re.compile(r"Pattern:"),
    re.compile(r"Concrete evidence:"),
    re.compile(r"Original requested task narrative:"),
    re.compile(r"Descent into slop narrative:"),
    re.compile(r"Why this matters:"),
    re.compile(r"User surprise analysis:"),
    re.compile(r"Existential justification:"),
    re.compile(r"Failure mode:"),
]

_SLOP_REJECT = [
    re.compile(p, re.IGNORECASE)
    for p in [
        "-O",
        "optimized mode",
        "passed without",
        "no violations",
        "clean code",
        r"all.*(?:other|remaining).*(?:passed|clean|fine|acceptable)",
        r"no.*(?:bridge.burning|runtime.control.flow).*violation",
        r"nothing (?:to |)report",
        "full repository sweep",
        r"full.*sweep.*(?:excluding|excluded)",
        "excluding forbidden",
        "excluded targets",
    ]
]


class SlopFinding(BaseModel):
    tier: Literal["tier1", "tier2"]
    label: str
    category: str
    location: Location
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
                raise ValueError(f"forbidden category: {v}")
        return v


class SlopReport(BaseModel):
    schema_version: Annotated[int, Field(ge=1)] = 1
    report_type: Literal["slop"] = "slop"
    repo_sha: str = Field(min_length=40, max_length=40)
    review_scope: list[Path] = Field(min_length=1)
    findings: list[SlopFinding] = Field(min_length=1)
    checked_surfaces: list[CheckedSurface]
    rejected_easy_wins: list[str]
    score: Annotated[int, Field(ge=0, le=100)]
    report: str = Field(min_length=REPORT_MIN_LENGTH)

    @model_validator(mode="after")
    def _check_git_paths(self) -> SlopReport:
        sha = self.repo_sha
        for i, p in enumerate(self.review_scope):
            if not _path_exists_in_git(p, sha):
                raise ValueError(f"review_scope[{i}] path does not exist at {sha}: {p}")
        for i, finding in enumerate(self.findings):
            loc_path = finding.location.path
            if _is_infra_path(loc_path):
                raise ValueError(
                    f"findings[{i}] location is an infrastructure path: {loc_path}"
                )
            if not _path_exists_in_git(loc_path, sha):
                raise ValueError(
                    f"findings[{i}] location path does not exist at {sha}: {loc_path}"
                )
            for j, ev in enumerate(finding.evidence):
                if not _path_exists_in_git(ev.path, sha):
                    raise ValueError(
                        f"findings[{i}].evidence[{j}] path does not exist "
                        f"at {sha}: {ev.path}"
                    )
        return self

    @field_validator("report")
    @classmethod
    def _check_report_markers(cls, v: str) -> str:
        for marker in _SLOP_MARKERS:
            if not marker.search(v):
                raise ValueError(f"report missing required marker: {marker.pattern}")
        for pat in _SLOP_REJECT:
            if pat.search(v):
                raise ValueError(f"report contains prohibited pattern: {pat.pattern}")
        return v


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
