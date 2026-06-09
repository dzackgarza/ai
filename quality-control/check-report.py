# /// script
# requires-python = ">=3.11"
# dependencies = ["pydantic>=2", "cyclopts"]
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

from cyclopts import App
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

app = App(
    name="check-report",
    help="Review report validator: validates candidate JSON artifacts against pydantic models.",
)

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
    path: Path = Field(
        description="File path relative to repo root. Must exist in git at repo_sha."
    )
    start_line: int = Field(ge=1, description="Finding start line (1-indexed).")
    end_line: int = Field(ge=1, description="Finding end line (1-indexed).")


class Evidence(BaseModel):
    kind: str = Field(
        description="Evidence type: file-read, diff-snippet, command-output."
    )
    path: Path = Field(
        description="Evidence file path relative to repo root. Must exist in git at repo_sha."
    )
    lines: list[Annotated[int, Field(ge=1)]] = Field(
        min_length=2,
        max_length=2,
        description="Line range [start, end] this evidence covers (1-indexed).",
    )


class CheckedSurface(BaseModel):
    path: Path = Field(description="File path examined during review.")
    reason: str = Field(
        description="Why this surface was selected: high-churn, diff-context, dependency-graph."
    )
    lines_read: list[Annotated[int, Field(ge=1)]] = Field(
        min_length=2,
        max_length=2,
        description="Line range [start, end] read during review (1-indexed).",
    )
    result: str = Field(description="Outcome: finding, clean, needs-attention.")


# ---------------------------------------------------------------------------
# General review
# ---------------------------------------------------------------------------


class GeneralFinding(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "x-custom-validation": {
                "_tier_category_consistency": {
                    "rule": "Low-signal categories (see LOW_SIGNAL_CATEGORIES) require tier2",
                    "validator": "_tier_category_consistency",
                }
            }
        },
    )
    tier: Literal["tier1", "tier2"] = Field(
        description="tier1: a real semantic regression, broken invariant, or "
        "incorrect behavior that changes program output or violates a correctness "
        "property. tier2: a minor concern, code quality observation, or low-risk "
        "issue. Low-signal categories (naming, formatting, etc.) are forced to "
        "tier2 by validation.",
        json_schema_extra={
            "x-custom-validation": {
                "rule": "Low-signal categories must be tier2. See category field and _tier_category_consistency",
                "validator": "_tier_category_consistency",
            }
        },
    )
    label: str = Field(
        description="Short label describing defect shape (not severity). "
        "Ground it in what the code actually does wrong — e.g. if a function "
        "returns wrong output: INCORRECT_OUTPUT; if stderr is silenced: "
        "SUPPRESSED_ERROR; if Optional is unwrapped without guard: NULL_UNSAFE. "
        "Look at the bridge-burning-red-flags.md and runtime-control-flow-red-flags.md "
        "inventories in reviewing-llm-code for grounded pattern names.",
    )
    category: str = Field(
        description="Defect type. Ground it in known categories from policy-index "
        "and the bridge-burning rules. "
        "Examples: semantic-regression, test-quality, null-safety, "
        "missing-error-handling, logic-error. "
        "Forbidden: infra, infrastructure, ci, workflow, config.",
        json_schema_extra={
            "x-custom-validation": {
                "rule": "Rejected if value contains: infra, infrastructure, ci, workflow, config",
                "validator": "_no_infra_categories",
            }
        },
    )
    location: Location = Field(
        description="File and line range where the finding occurs."
    )
    violated_invariant: str = Field(
        min_length=20,
        description="A specific, verifiable contract or behavior that is violated. "
        "Must name something falsifiable — provable or disprovable via a command or "
        "code inspection. Not a blanket judgment. "
        "Rejected patterns (blanket claims that name nothing specific): -O, "
        "optimized mode, clean code, no violation, nothing to report, "
        "looks (good|correct|fine|right|ok), no issues found, appears correct, "
        "everything (looks|seems|is).",
        json_schema_extra={
            "x-custom-validation": {
                "rule": "Must name a specific falsifiable contract. "
                "Rejected against patterns: -O, optimized mode, clean code, "
                "no violation, nothing to report, looks (good|correct|fine|right|ok), "
                "no issues found, appears correct, everything (looks|seems|is)",
                "validator": "_no_empty_invariant",
            }
        },
    )
    proof_command: str = Field(
        min_length=10,
        description="Shell command or code path that proves the invariant is "
        "violated. Must be reproducible by another agent. "
        "Example: 'grep -rn get_diff quality-control/run-review.py'",
    )
    symptom: str = Field(description="Observable symptom of the defect.")
    source: str = Field(
        description="Root cause: what code or pattern produces the symptom."
    )
    consequence: str = Field(description="What breaks or degrades due to this defect.")
    remedy: str = Field(description="How to fix the defect.")
    evidence: list[Evidence] = Field(
        min_length=1,
        description="Supporting evidence proving the finding. At least one item required.",
    )

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
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "x-custom-validation": {
                "_require_substantive_finding": {
                    "rule": "At least one finding must be Tier 1 or non-low-signal category",
                    "validator": "_require_substantive_finding",
                },
                "_check_git_paths": {
                    "rule": "Every path must exist in git at repo_sha and not be in INFRA_PREFIXES",
                    "validator": "_check_git_paths",
                },
            }
        },
    )
    schema_version: Annotated[int, Field(ge=1)] = Field(
        default=1,
        description="Report format version. Currently 1.",
    )
    report_type: Literal["general"] = Field(
        default="general",
        description="Must be 'general'. Selects the GeneralFinding model for validation.",
    )
    repo_sha: str = Field(
        min_length=40,
        max_length=40,
        description="Full git commit SHA being reviewed. Used to verify all paths "
        "exist in git; also recorded in PR comment metadata.",
    )
    review_scope: list[Path] = Field(
        min_length=1,
        description="Files examined during review, relative to repo root. "
        "All must exist in git at repo_sha. Typically drawn from the PR diff.",
    )
    findings: list[GeneralFinding] = Field(
        min_length=1,
        description="General review findings. At least one required; at least one "
        "must be substantive (Tier 1 or non-low-signal category).",
    )
    checked_surfaces: list[CheckedSurface] = Field(
        description="Surfaces inspected during review, whether findings were found "
        "or not. Documents review thoroughness.",
    )
    rejected_easy_wins: list[str] = Field(
        description="Low-signal observations the agent considered but declined to "
        "elevate to findings, with brief reason. Documents that non-trivial "
        "patterns were evaluated and dismissed, not missed.",
    )

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
    model_config = ConfigDict(
        json_schema_extra={
            "x-custom-validation": {
                "_tier_category_consistency": {
                    "rule": "Low-signal categories (see LOW_SIGNAL_CATEGORIES) require tier2",
                    "validator": "_tier_category_consistency",
                }
            }
        },
    )
    tier: Literal["tier1", "tier2"] = Field(
        description="tier1: a concrete bridge-burning pattern — runtime default, "
        "fallback, suppressed error, mock-pretending-as-proof, or similar "
        "validation-evasion construct. "
        "tier2: speculative over-engineering, minor style deviation, or a pattern "
        "that could become harmful under implausible conditions. "
        "Low-signal categories are forced to tier2 by validation.",
        json_schema_extra={
            "x-custom-validation": {
                "rule": "Low-signal categories require tier2. Cross-field with category.",
                "validator": "_tier_category_consistency",
            }
        },
    )
    label: str = Field(
        description="Short label grounded in the specific bridge-burning construct. "
        "Look at the actual code pattern: is it a runtime default, a suppressed "
        "error, a mock without assertion, a conditional import, a boolean mode "
        "flag? The label should name the construct, not grade it. "
        "See bridge-burning-red-flags.md for the inventory of recognized patterns.",
    )
    category: str = Field(
        description="Slop pattern category from the anti-slop skill taxonomy. "
        "Look at policy-index and the bridge-burning inventory for grounded "
        "categories like: bridge-burning, runtime-control-flow, "
        "validation-evasion, defaults-and-fallbacks, proof-laundering. "
        "Forbidden: infra, infrastructure, ci, workflow, config.",
        json_schema_extra={
            "x-custom-validation": {
                "rule": "Rejected if value contains: infra, infrastructure, ci, workflow, config",
                "validator": "_no_infra_categories",
            }
        },
    )
    location: Location = Field(
        description="File and line range where the slop pattern occurs."
    )
    violated_invariant: str = Field(
        min_length=20,
        description="A specific engineering invariant that is violated by the slop "
        "pattern. Must name a concrete contract (e.g., 'every error path fails "
        "loudly, but this code suppresses stderr'). Not a blanket judgment. "
        "Rejected patterns (blanket claims that name nothing specific): -O, "
        "optimized mode, clean code, no violation, nothing to report, "
        "looks (good|correct|fine|right|ok), no issues found, appears correct, "
        "everything (looks|seems|is).",
        json_schema_extra={
            "x-custom-validation": {
                "rule": "Must name a specific falsifiable contract. "
                "Rejected against patterns: -O, optimized mode, clean code, "
                "no violation, nothing to report, looks (good|correct|fine|right|ok), "
                "no issues found, appears correct, everything (looks|seems|is)",
                "validator": "_no_empty_invariant",
            }
        },
    )
    proof_command: str = Field(
        min_length=10,
        description="Shell command or code path that reproduces the slop pattern. "
        "Must be reproducible by another agent. "
        "Example: 'rg '2>/dev/null' quality-control/', "
        "'probe search 'Optional.*Field' -- src/db/service.py'",
    )
    pattern: str = Field(
        description="Structural pattern name. Ground it in the actual code construct "
        "(is there a 2>/dev/null it's runtime-default? a mock without assertion? "
        "a try/except ImportError? a boolean mode flag?). "
        "See bridge-burning-red-flags.md and runtime-control-flow-red-flags.md "
        "for the full pattern inventory.",
    )
    task_narrative: str = Field(
        description="What the agent was supposed to build — capsulizes the task "
        "context so the reader understands the assigned goal.",
    )
    slop_narrative: str = Field(
        description="What the agent actually produced — the bridge-burning "
        "substitution. Contrast with task_narrative.",
    )
    why_it_matters: str = Field(
        description="Concrete consequence of this slop pattern: silent data loss, "
        "masked failure, untestable branch, non-deterministic behavior, etc.",
    )
    user_surprise: str = Field(
        description="What the user would observe that would trigger a 'why did this "
        "happen' reaction. Epistemic: describe the observable surprise, not the "
        "hypothetical.",
    )
    existential_justification: str = Field(
        description="Why this finding exists. The agent's rationalization for the "
        "bridge-burning choice (e.g., 'defensive coding', 'graceful degradation', "
        "'backward compatibility', 'just in case').",
    )
    failure_mode: str = Field(
        description="Which LLM failure mode this slop exploits. "
        "See the llm-failure-modes skill for the full catalog. "
        "Use the documented numbered labels (e.g. asymmetric-risk-model (#20), "
        "false-binary (#7), reward-hacking (#13), epistemic-bottleneck (#4)), "
        "not invented names.",
    )
    evidence: list[Evidence] = Field(
        min_length=1,
        description="Supporting evidence proving the slop pattern. At least one "
        "item required. Should include file-read or diff-snippet showing the "
        "offending construct.",
    )

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
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "x-custom-validation": {
                "_require_substantive_finding": {
                    "rule": "At least one finding must be Tier 1 or non-low-signal category",
                    "validator": "_require_substantive_finding",
                },
                "_check_git_paths": {
                    "rule": "Every path must exist in git at repo_sha and not be in INFRA_PREFIXES",
                    "validator": "_check_git_paths",
                },
            }
        },
    )
    schema_version: Annotated[int, Field(ge=1)] = Field(
        default=1,
        description="Report format version. Currently 1.",
    )
    report_type: Literal["slop"] = Field(
        default="slop",
        description="Must be 'slop'. Selects the SlopFinding model for validation.",
    )
    repo_sha: str = Field(
        min_length=40,
        max_length=40,
        description="Full git commit SHA being reviewed. Used to verify all paths "
        "exist in git; also recorded in PR comment metadata.",
    )
    review_scope: list[Path] = Field(
        min_length=1,
        description="Files examined during review, relative to repo root. "
        "All must exist in git at repo_sha.",
    )
    findings: list[SlopFinding] = Field(
        min_length=1,
        description="Slop review findings. At least one required; at least one "
        "must be substantive (Tier 1 or non-low-signal category).",
    )
    checked_surfaces: list[CheckedSurface] = Field(
        description="Surfaces inspected during review, whether findings were found "
        "or not. Documents review thoroughness.",
    )
    rejected_easy_wins: list[str] = Field(
        description="Low-signal observations or potential slop patterns the agent "
        "considered but declined to elevate. Brief reason for each. Documents "
        "that non-trivial patterns were evaluated, not missed.",
    )

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


@app.command
def validate(path: Path, report_type: Literal["general", "slop"]):
    """Validate a candidate report JSON file.

    Args:
        path: Path to the report JSON file.
        report_type: Type of report — "general" or "slop".
    """
    if not path.is_file():
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    with open(path) as f:
        data: dict = json.load(f)

    model_cls = _MODEL_BY_TYPE.get(report_type)
    if model_cls is None:
        print(f"Error: unknown report_type '{report_type}'.", file=sys.stderr)
        sys.exit(1)

    try:
        model_cls(**data)
    except Exception as exc:
        msg = str(exc)
        print(f"Report validation FAILED:\n  {msg}")
        sys.exit(1)

    print("Report validation PASSED")
    sys.exit(0)


@app.command
def schema(type: Literal["general", "slop"] = None):
    """Dump JSON Schema for a report type.

    Args:
        type: Which report schema to dump — "general" or "slop". Required.
    """
    if type is None:
        print("Error: --type is required. Use 'general' or 'slop'.", file=sys.stderr)
        sys.exit(1)

    model_cls = _MODEL_BY_TYPE.get(type)
    if model_cls is None:
        print(
            f"Error: unknown type '{type}'. Use 'general' or 'slop'.", file=sys.stderr
        )
        sys.exit(1)

    print(json.dumps(model_cls.model_json_schema(), indent=2))
    sys.exit(0)


@app.command
def metadata(path: Path):
    """Print machine-parseable metadata from a validated artifact.

    Args:
        path: Path to the validated artifact JSON file.
    """
    if not path.is_file():
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    with open(path) as f:
        data = json.load(f)

    findings = data.get("findings", [])
    result = {
        "repo_sha": data.get("repo_sha", ""),
        "report_type": data.get("report_type", "unknown"),
        "finding_count": len(findings),
        "tier1_count": sum(1 for f in findings if f.get("tier") == "tier1"),
        "tier2_count": sum(1 for f in findings if f.get("tier") == "tier2"),
    }
    print(json.dumps(result))
    sys.exit(0)


@app.command
def finding_body(path: Path, index: int):
    """Render a single finding's markdown body for use as a review thread.

    Args:
        path: Path to the validated artifact JSON file.
        index: 0-based index of the finding to render.
    """
    if not path.is_file():
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    with open(path) as f:
        data = json.load(f)

    findings = data.get("findings", [])
    if index < 0 or index >= len(findings):
        print(
            f"Error: index {index} out of range (0-{len(findings) - 1})",
            file=sys.stderr,
        )
        sys.exit(1)

    report_type = data.get("report_type", "unknown")
    repo_sha = data.get("repo_sha", "unknown")[:8]
    finding = findings[index]
    body = _render_finding_thread_body(index, finding, report_type, repo_sha)
    print(body)
    sys.exit(0)


@app.command
def render(path: Path):
    """Render a validated review artifact into a uniform PR comment.

    Args:
        path: Path to the validated artifact JSON file.
    """
    if not path.is_file():
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    with open(path) as f:
        data = json.load(f)

    report_type = data.get("report_type", "unknown")
    findings = data.get("findings", [])
    checked_surfaces = data.get("checked_surfaces", [])
    rejected_easy_wins = data.get("rejected_easy_wins", [])

    score = _compute_score(findings)
    tier1_count = sum(1 for f in findings if f.get("tier") == "tier1")
    tier2_count = sum(1 for f in findings if f.get("tier") == "tier2")

    lines = [
        f"# Code Review: {report_type}",
        "",
        f"**Score: {score}/100**",
        "",
        "## Summary",
        "",
        f"- Tier 1 findings: {tier1_count}",
        f"- Tier 2 findings: {tier2_count}",
        f"- Score: {score}/100 (base 100, -20 per Tier 1, -5 per Tier 2, min 0)",
        "",
    ]

    if findings:
        lines.append("## Findings")
        lines.append("")
        for i, f in enumerate(findings, 1):
            lines.append(_render_finding(i, f))

    lines.append("## Checked Surfaces")
    lines.append("")
    lines.append(_render_checked_surfaces(checked_surfaces))
    lines.append("")

    if rejected_easy_wins:
        lines.append("## Rejected Easy Wins")
        lines.append("")
        for r in rejected_easy_wins:
            lines.append(f"- {r}")
        lines.append("")

    print("\n".join(lines))


def _compute_score(findings: list[dict]) -> int:
    tier1 = sum(1 for f in findings if f.get("tier") == "tier1")
    tier2 = sum(1 for f in findings if f.get("tier") == "tier2")
    raw = 100 - (tier1 * 20) - (tier2 * 5)
    return max(0, raw)


def _render_finding(n: int, f: dict) -> str:
    tier = f.get("tier", "?")
    label = f.get("label", "?")
    category = f.get("category", "?")
    loc = f.get("location", {})
    loc_path = loc.get("path", "?")
    start = loc.get("start_line", "?")
    end = loc.get("end_line", "?")
    violated = f.get("violated_invariant", "")
    proof = f.get("proof_command", "")

    lines = [
        f"### Finding {n}: {label} ({category}, {tier})",
        "",
        f"**Location:** `{loc_path}:{start}-{end}`",
    ]
    if violated:
        lines.append(f"**Violated invariant:** {violated}")
    if proof:
        lines.append(f"**Proof command:** `{proof}`")
    lines.append("")

    # General review fields
    if "symptom" in f:
        lines.append("| Field | Detail |")
        lines.append("|-------|--------|")
        for field in ["symptom", "source", "consequence", "remedy"]:
            lines.append(f"| **{field.capitalize()}** | {f.get(field, '')} |")
        lines.append("")

    # Slop review fields
    if "pattern" in f:
        slop_fields = [
            ("Pattern", "pattern"),
            ("Original task", "task_narrative"),
            ("Slop narrative", "slop_narrative"),
            ("Why this matters", "why_it_matters"),
            ("User surprise", "user_surprise"),
            ("Existential justification", "existential_justification"),
            ("Failure mode", "failure_mode"),
        ]
        lines.append("| Field | Detail |")
        lines.append("|-------|--------|")
        for label_k, key in slop_fields:
            lines.append(f"| **{label_k}** | {f.get(key, '')} |")
        lines.append("")

    evidence = f.get("evidence", [])
    if evidence:
        lines.append("**Evidence:**")
        for ev in evidence:
            p = ev.get("path", "?")
            lo, hi = (ev.get("lines") or ["?", "?"])[:2]
            lines.append(f"- `{p}:{lo}-{hi}` ({ev.get('kind', '?')})")
        lines.append("")

    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def _render_finding_thread_body(
    index: int,
    finding: dict,
    report_type: str,
    repo_sha_short: str,
) -> str:
    """Render a single finding as a compact markdown body for a review thread.

    This is the format posted as a GitHub PR review comment, not the full
    rendered report.  The body is self-contained: tier, label, violated invariant,
    proof command, evidence, and source attribution.
    """
    tier = finding.get("tier", "?")
    label = finding.get("label", "?")
    loc = finding.get("location", {})
    loc_path = loc.get("path", "?")
    start = loc.get("start_line", "?")
    end = loc.get("end_line", "?")
    violated = finding.get("violated_invariant", "")
    proof = finding.get("proof_command", "")

    report_label = "General Review" if report_type == "general" else "Slop Review"

    lines = [
        f"### [{report_label}][{tier}] {label}",
        "",
        f"**Location:** `{loc_path}:{start}-{end}`",
    ]
    if violated:
        lines.append(f"**Violated invariant:** {violated}")
    if proof:
        lines.append(f"**Proof command:** `{proof}`")
    lines.append("")

    evidence = finding.get("evidence", [])
    if evidence:
        lines.append("**Evidence:**")
        for ev in evidence:
            p = ev.get("path", "?")
            lo, hi = (ev.get("lines") or ["?", "?"])[:2]
            lines.append(f"- `{p}:{lo}-{hi}` ({ev.get('kind', '?')})")
        lines.append("")

    # General narrative fields
    if "symptom" in finding:
        lines.append(f"**Symptom:** {finding['symptom']}")
        lines.append("")
    if "consequence" in finding:
        lines.append(f"**Consequence:** {finding['consequence']}")
        lines.append("")
    if "remedy" in finding:
        lines.append(f"**Remedy:** {finding['remedy']}")
        lines.append("")

    # Slop narrative fields (compact)
    if "pattern" in finding:
        lines.append(f"**Pattern:** {finding['pattern']}")
        lines.append("")
        if "why_it_matters" in finding:
            lines.append(f"**Why this matters:** {finding['why_it_matters']}")
            lines.append("")

    lines.extend(
        [
            "---",
            "",
            f"Source: {report_label}, commit {repo_sha_short}.",
        ]
    )

    return "\n".join(lines)


def _render_checked_surfaces(surfaces: list[dict]) -> str:
    if not surfaces:
        return "_None._"
    rows = ["| Path | Reason | Lines | Result |", "|------|--------|-------|--------|"]
    for s in surfaces:
        lo, hi = (s.get("lines_read") or ["?", "?"])[:2]
        rows.append(
            f"| `{s['path']}` | {s.get('reason', '?')} | {lo}-{hi} | {s.get('result', '?')} |"
        )
    return "\n".join(rows)


if __name__ == "__main__":
    app()
