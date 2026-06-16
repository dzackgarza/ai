# QC Triage Protocol

This document defines the mandatory triage procedure when global QC checks
fail. It is a reference for the `reviewing-llm-code` skill — the slop report
subagent workflow defined below is owned by `reviewing-llm-code`.

## Core Policy

The agent that hits a QC failure is, by construction, the party that produced or touched
the failing work. **That party loves its own slop**: its assessment of whether a finding
is real is biased toward "my code is fine," and is therefore inadmissible (see
`llm-failure-modes`: self-certification, verification theater; `anti-slop`). The whole
point of this protocol is that this agent — the orchestrator — is **disqualified from
judging the findings**. Judgment is delegated to an independent, policy-primed subagent.

This is a compliance constraint, not a structural gate. Do NOT "solve" it by adding a
checkpoint or gate you control — per `goalcraft`, *process is attack surface*; a gate the
adversary controls becomes the adversary's substitute objective. The fix is the removal
of your discretion, below.

When a QC check fails and the triage directive is emitted, the orchestrator MUST:

1. **Make ZERO judgment calls about any finding.** You may not decide, state, hint,
   imply, or act on whether a finding is real, false, a "false positive," slop, clean,
   "the tool over-matched," "probably fine," or "a tool bug rather than my code."
   **Forming the disposition at all is the violation** — not merely acting on it. The
   instant you catch yourself evaluating whether a finding is valid, STOP: that reflex is
   the slop-love bias this protocol exists to neutralize. Even distinguishing
   "tool-execution failure vs. code finding" is a judgment call, and is also delegated.

2. **STOP all work.** Cease the in-progress task. Do not continue.

3. **NOT probe QC configs.** Do not read, inspect, or modify any file in
   `~/ai-review-ci/`. Do not read the configs, scripts, tool pins,
   ML models, or templates in that directory. Probing QC is reward-hacking.

4. **NOT self-fix and NOT self-evaluate findings.** You will game the triage. Both the
   judgment (review) and the fix are delegated to subagents not involved in producing the
   failing code; they must be different instances.

5. **Present findings to the user immediately.** Show the complete raw QC output. Do not
   filter, summarize, or interpret it — interpretation is itself a judgment call (rule 1).

6. **Wait for explicit user approval.** Do not proceed without explicit
   user approval. "Approval" means a direct statement that triage may begin.

## Classification Belongs to the Reviewer Subagent — Never the Orchestrator

Classifying a finding is the policy-primed reviewer subagent's job (Step 1), and ONLY its
job. The orchestrator does not pre-classify, co-classify, "narrow down," or sanity-check
findings before, during, or after dispatch. The rules below bind the REVIEWER; the
orchestrator only routes the raw finding to it, unjudged.

The reviewer MUST:

- Treat a QC rule's name as a **pointer to investigate**, never the definition of the
  violation. Classify the flagged code against the FULL bridge-burning policy and cite the
  `POLICY.*` code. A non-empty `except`, a rule named "empty X" that hit non-empty Y, or
  any "the linter over-matched" intuition does NOT clear the code: ask whether it is slop
  under *any* policy (`FAIL_LOUD_BOUNDARY`, `NO_ERROR_DISCARD`, the graceful-handling ban,
  `STRINGLY-ERRORS`, etc.). Almost any try/except is slop on this system — emptiness is the
  wrong axis; presence-and-justification is the axis.
- Determine for itself whether the failure is a **tool-execution failure** (exit 127,
  crash, config-load error — a tooling defect, not a code finding) or a **tool finding** on
  code. The orchestrator must not pre-judge this split; "it's just a broken tool, my code is
  fine" is the canonical slop-love exit and is exactly why this call is the reviewer's.
- Treat a "false positive" disposition, or any move to narrow / disable / `# noqa` a
  detector, as carrying **formal policy-exception burden**: policy code, justification,
  replacement invariant, boundary proof, audit trail. Weakening a detector that flagged
  real slop is laundering — the precise reward-hack this protocol exists to stop. "The body
  is not literally empty / the rule mismatched" is not a valid clearance.

## Triage Workflow (After User Approval)

Once the user approves, execute these steps in exactly this order:

### Step 1: Slop Report Subagent

Spawn a SUBAGENT to perform an independent `reviewing-llm-code` slop report on the QC
findings. This subagent must:

- Load **all** the bridge-burning policies explicitly — name them in the dispatch:
  `policy-index` (and its `references/red-flags.md`, `runtime-control-flow.md`,
  `policies.md`, `test-proof-rules.md`, `remediations.md`), `anti-slop`,
  `reviewing-llm-code`, `bespoke-software-policy`, `test-guidelines`, and `fixing-slop`.
- Review the flagged code against the FULL policy, classify each finding, and cite the
  `POLICY.*` code (per "Classification Belongs to the Reviewer Subagent" above)
- Return its own verdict and a structured report of all bridge-burning violations,
  including architectural root causes

#### Dispatch hygiene: what you may and may NOT say to the reviewer

A review is **an independent attack on the finding, not a confirmation of the
orchestrator's opinion** (`goalcraft`: "Review: an independent attack on the completion
claim, not a disposition loop. Do not ask the adversary to classify its own residue.").
If you transmit your verdict, leaning, or prior analysis to the reviewer, you have **seeded
its conclusion and the review is VOID** — it will anchor on your prior, which is the exact
slop-love bias the delegation exists to bypass.

The dispatch to the reviewer MAY contain ONLY:
- the raw, verbatim QC / finding output (no paraphrase, no emphasis, no reordering);
- the file/line locations to examine;
- the instruction to load all policies explicitly and classify independently, citing codes;
- the instruction to return its own verdict.

The dispatch MUST NOT contain:
- any orchestrator verdict or leaning — "suspected false positive," "confirmed slop,"
  "I think this is fine / real," "this is probably a tool bug," "likely a graceful exit";
- any characterization of whether the finding is valid, or whether the code is clean/slop;
- any framing, hint, ordering, or emphasis that suggests the desired conclusion;
- the orchestrator's own prior analysis of the code.

State the finding and name the policies. Let the reviewer reach the verdict. Then route on
the **reviewer's** verdict — you never override it, "sanity-check" it, or substitute your
own. If you find you have an opinion about the outcome, that opinion is contraband: it does
not enter the dispatch and it does not survive the review.

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
| Orchestrator forming/stating a disposition ("false positive", "real", "clean", "tool bug") | The producer loves its own slop; its judgment of its own findings is inadmissible | Make no call; route the raw finding to a policy-primed reviewer |
| Seeding the reviewer with your verdict, leaning, framing, or prior analysis | Collapses the independent attack into confirmation of your prior | Dispatch raw finding + named policies only |
| "Doing it right" only once the user pushes back | Behaving correctly under supervision is not a corrected process; it relapses when unwatched | Never self-judge in the first place — the prohibition is unconditional |
| Reading `~/ai-review-ci/` to "understand the tool" | Gives the agent config info it can later game | Read nothing. Present findings to user. |
| Running isolated checks (just `ruff`, just `mypy`) to "verify" | Cherry-picking bypasses the full QC gate | Run `just test` only (after fix subagent is done) |
| Adding bypass comments (`# noqa`, `@ts-ignore`) | Hides the symptom without fixing the cause | Fix the underlying code |
| Editing QC configs or thresholds | Weakens QC for all future runs | Change only project code |
| Merging the slop report and fix into one subagent | The reviewer games the fix criteria | Always separate subagents |
| Presenting partial or summarized QC output | The user cannot assess the full failure | Show complete raw tool output |
| Continuing work on the original task after QC fails | The original output is likely defective | Triage first, then assess if retry is needed |

## Evidence Requirements

Before reporting any triage step complete, these must be true:

- [ ] The orchestrator issued NO disposition of any finding — real / false / slop / clean /
      tool-bug — at any point, before or after review
- [ ] The reviewer dispatch contained no orchestrator verdict, leaning, framing, or prior
      analysis (raw finding + named policies only)
- [ ] QC findings presented to user in full (raw tool output)
- [ ] User explicitly approved triage
- [ ] Slop report subagent loaded all policies explicitly and produced its own verdict +
      structured violation report
- [ ] Fix subagent made code changes and verified with `just test`
- [ ] Separate subagents were used for review and fix
