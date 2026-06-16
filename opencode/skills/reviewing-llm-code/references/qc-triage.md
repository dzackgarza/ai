# QC Triage Protocol

This document defines the mandatory triage procedure when global QC checks
fail. It is a reference for the `reviewing-llm-code` skill — the slop report
subagent workflow defined below is owned by `reviewing-llm-code`.

## Core Policy

When a QC check fails and the triage directive is emitted, the agent MUST:

1. **STOP all work.** Immediately cease all current activity.
   Do not continue with any in-progress task.

2. **NOT probe QC configs.** Do not read, inspect, or modify any file in
   `~/ai-review-ci/`. Do not read the configs, scripts, tool pins,
   ML models, or templates in that directory. Probing QC is reward-hacking.

3. **NOT self-fix findings.** Do not attempt to fix any finding yourself.
   You will game the triage. All fixes must be delegated to a subagent
   that was not involved in producing the failing code.

4. **Present findings to the user immediately.** Show the complete QC output
   to the user. Do not filter, summarize, or interpret it. The raw tool
   output is the evidence.

5. **Wait for explicit user approval.** Do not proceed without explicit
   user approval. "Approval" means a direct statement that triage may begin.

## Classifying a Finding Before Triage

A QC finding's rule name is a **pointer to investigate**, never the definition of the
violation. Before disposing of any finding, classify the flagged code against the FULL
bridge-burning policy and cite the `POLICY.*` code it does or does not violate — not the
rule's literal label. A non-empty `except`, a rule named "empty X" that hit non-empty Y,
or any "the linter over-matched" intuition does NOT clear the code: ask whether the code
is slop under *any* policy (`FAIL_LOUD_BOUNDARY`, `NO_ERROR_DISCARD`, the graceful-handling
ban, `STRINGLY-ERRORS`, etc.).

Distinguish two failure kinds, because they have opposite dispositions:

- **Tool-execution failure** — the QC tool did not run: exit 127 (command not found),
  a crash, or a config-load error. This is a tooling defect, not a project-code finding.
  It is legitimate to diagnose the tool/environment and fix it upstream. Do NOT edit
  project code in response; do NOT report it as a code violation.
- **Tool finding** — the tool ran and flagged code. The flagged code must be classified
  against the full policy. A **"false positive" disposition, or any move to narrow,
  disable, `# noqa`, or otherwise weaken the detector, carries the same burden as a
  formal policy exception**: policy code, justification, replacement invariant, boundary
  proof, and audit trail. Siding with flagged code by weakening its detector is
  laundering — the precise reward-hack this protocol exists to stop.

The reviewer subagent (Step 1) MUST perform this classification explicitly and cite the
policy code, not the rule label. "The body is not literally empty / the rule mismatched"
is not a valid clearance.

## Triage Workflow (After User Approval)

Once the user approves, execute these steps in exactly this order:

### Step 1: Slop Report Subagent

Spawn a SUBAGENT to perform an `reviewing-llm-code` slop report on the QC
findings. This subagent must:

- Load the `reviewing-llm-code` skill
- Review the QC findings against the bridge-burning policy red-flag catalog
- Produce a structured report of all bridge-burning violations
- Identify the architectural root causes, not just the surface symptoms
- Return the report as its output

### Step 2: Fix Subagent

Spawn a **separate** SUBAGENT to fix the underlying architectural issues
identified by the slop report. This subagent must:

- Be a different subagent instance from the reviewer
- Receive the slop report as input
- Fix the architectural root causes, not just the surface symptoms
- Verify the fix passes QC by running `just test`
- Report the fix outcome back

The reviewer and fixer MUST be different subagent instances.
The reviewer analyses. The fixer fixes.
They are not the same agent.

## Prohibited Behaviors

| Behavior | Why | Instead |
|----------|-----|---------|
| Reading `~/ai-review-ci/` to "understand the tool" | Gives the agent config info it can later game | Read nothing. Present findings to user. |
| Running isolated checks (just `ruff`, just `mypy`) to "verify" | Cherry-picking bypasses the full QC gate | Run `just test` only (after fix subagent is done) |
| Adding bypass comments (`# noqa`, `@ts-ignore`) | Hides the symptom without fixing the cause | Fix the underlying code |
| Editing QC configs or thresholds | Weakens QC for all future runs | Change only project code |
| Merging the slop report and fix into one subagent | The reviewer games the fix criteria | Always separate subagents |
| Presenting partial or summarized QC output | The user cannot assess the full failure | Show complete raw tool output |
| Continuing work on the original task after QC fails | The original output is likely defective | Triage first, then assess if retry is needed |

## Evidence Requirements

Before reporting any triage step complete, these must be true:

- [ ] QC findings presented to user in full (raw tool output)
- [ ] User explicitly approved triage
- [ ] Slop report subagent produced a structured violation report
- [ ] Fix subagent made code changes and verified with `just test`
- [ ] Separate subagents were used for review and fix
