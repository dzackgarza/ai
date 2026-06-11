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


def _path_in_checkout(path: Path) -> bool:
    """True if *path* exists in the reviewed checkout (the CWD)."""
    return (Path.cwd() / path).is_file()


def _line_count(path: Path) -> int:
    """Number of lines in *path* within the reviewed checkout."""
    return len((Path.cwd() / path).read_text(errors="replace").splitlines())


def _is_infra_path(p: Path) -> bool:
    s = p.as_posix()
    return any(s.startswith(prefix) for prefix in INFRA_PREFIXES)


# ---------------------------------------------------------------------------
# Shared leaf types
# ---------------------------------------------------------------------------


class Location(BaseModel):
    path: Path = Field(
        description="File path relative to repo root. Must exist in the reviewed checkout."
    )
    start_line: int = Field(ge=1, description="Finding start line (1-indexed).")
    end_line: int = Field(ge=1, description="Finding end line (1-indexed).")

    @model_validator(mode="after")
    def _ordered_lines(self) -> Self:
        if self.start_line > self.end_line:
            raise ValueError(
                f"REJECTED: start_line {self.start_line} > end_line "
                f"{self.end_line}. FIX: start_line must not exceed end_line."
            )
        return self


class Evidence(BaseModel):
    kind: str = Field(
        description="Evidence type: file-read, diff-snippet, command-output."
    )
    path: Path = Field(
        description="Evidence file path relative to repo root. Must exist in the reviewed checkout."
    )
    lines: list[Annotated[int, Field(ge=1)]] = Field(
        min_length=2,
        max_length=2,
        description="Line range [start, end] this evidence covers (1-indexed).",
    )

    @model_validator(mode="after")
    def _ordered_lines(self) -> Self:
        if self.lines[0] > self.lines[1]:
            raise ValueError(
                f"REJECTED: evidence lines {self.lines} are not an ascending "
                f"[start, end] range. FIX: start must not exceed end."
            )
        return self


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
                "_check_paths": {
                    "rule": "Every path must exist in the reviewed checkout and not be in INFRA_PREFIXES",
                    "validator": "_check_paths",
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
    review_scope: list[Path] = Field(
        min_length=1,
        description="Files examined during review, relative to repo root. "
        "All must exist in the reviewed checkout. Typically drawn from the PR diff.",
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
    def _check_paths(self) -> Self:
        for i, p in enumerate(self.review_scope):
            if not _path_in_checkout(p):
                raise ValueError(
                    f"REJECTED: review_scope[{i}] path '{p}' does not exist "
                    f"in the reviewed checkout. "
                    f"FIX: only list files that exist in the repository, "
                    f"relative to the repo root."
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
            if not _path_in_checkout(loc_path):
                raise ValueError(
                    f"REJECTED: findings[{i}] location path '{loc_path}' "
                    f"does not exist in the reviewed checkout. "
                    f"FIX: every finding path must be a real file in the "
                    f"repository, relative to the repo root."
                )
            n_lines = _line_count(loc_path)
            if finding.location.end_line > n_lines:
                raise ValueError(
                    f"REJECTED: findings[{i}] location lines "
                    f"{finding.location.start_line}-{finding.location.end_line} "
                    f"exceed the length of '{loc_path}' ({n_lines} lines). "
                    f"FIX: use line numbers that exist in the file."
                )
            for j, ev in enumerate(finding.evidence):
                if not _path_in_checkout(ev.path):
                    raise ValueError(
                        f"REJECTED: findings[{i}].evidence[{j}] path '{ev.path}' "
                        f"does not exist in the reviewed checkout. "
                        f"FIX: every evidence path must be a real file in the "
                        f"repository, relative to the repo root."
                    )
                ev_lines = _line_count(ev.path)
                if ev.lines[1] > ev_lines:
                    raise ValueError(
                        f"REJECTED: findings[{i}].evidence[{j}] lines {ev.lines} "
                        f"exceed the length of '{ev.path}' ({ev_lines} lines). "
                        f"FIX: use line numbers that exist in the file."
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
                "_check_paths": {
                    "rule": "Every path must exist in the reviewed checkout and not be in INFRA_PREFIXES",
                    "validator": "_check_paths",
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
    review_scope: list[Path] = Field(
        min_length=1,
        description="Files examined during review, relative to repo root. "
        "All must exist in the reviewed checkout.",
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
    def _check_paths(self) -> Self:
        for i, p in enumerate(self.review_scope):
            if not _path_in_checkout(p):
                raise ValueError(
                    f"REJECTED: review_scope[{i}] path '{p}' does not exist "
                    f"in the reviewed checkout. "
                    f"FIX: only list files that exist in the repository, "
                    f"relative to the repo root."
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
            if not _path_in_checkout(loc_path):
                raise ValueError(
                    f"REJECTED: findings[{i}] location path '{loc_path}' "
                    f"does not exist in the reviewed checkout. "
                    f"FIX: every finding path must be a real file in the "
                    f"repository, relative to the repo root."
                )
            n_lines = _line_count(loc_path)
            if finding.location.end_line > n_lines:
                raise ValueError(
                    f"REJECTED: findings[{i}] location lines "
                    f"{finding.location.start_line}-{finding.location.end_line} "
                    f"exceed the length of '{loc_path}' ({n_lines} lines). "
                    f"FIX: use line numbers that exist in the file."
                )
            for j, ev in enumerate(finding.evidence):
                if not _path_in_checkout(ev.path):
                    raise ValueError(
                        f"REJECTED: findings[{i}].evidence[{j}] path '{ev.path}' "
                        f"does not exist in the reviewed checkout. "
                        f"FIX: every evidence path must be a real file in the "
                        f"repository, relative to the repo root."
                    )
                ev_lines = _line_count(ev.path)
                if ev.lines[1] > ev_lines:
                    raise ValueError(
                        f"REJECTED: findings[{i}].evidence[{j}] lines {ev.lines} "
                        f"exceed the length of '{ev.path}' ({ev_lines} lines). "
                        f"FIX: use line numbers that exist in the file."
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
def validate(
    path: Path,
    report_type: Literal["general", "slop"],
    output: Path,
):
    """Validate a candidate report and write the artifact.

    The report contains analysis only — findings, scope, surfaces. All
    run provenance (commit, ref, repo) is owned by the CI environment and
    attached at SARIF conversion/upload, never by the agent or this tool.

    Args:
        path: Path to the candidate report JSON file.
        report_type: Type of report — "general" or "slop".
        output: Where to write the validated artifact.
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

    data["report_type"] = report_type
    output.write_text(json.dumps(data, indent=2) + "\n")
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
        "report_type": data.get("report_type", "unknown"),
        "finding_count": len(findings),
        "tier1_count": sum(1 for f in findings if f.get("tier") == "tier1"),
        "tier2_count": sum(1 for f in findings if f.get("tier") == "tier2"),
    }
    print(json.dumps(result))
    sys.exit(0)


if __name__ == "__main__":
    app()
