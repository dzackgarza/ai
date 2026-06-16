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

## The Three Roles (each unbiased by what it is not allowed to see)

Triage is split across three isolated roles. The isolation IS the mechanism: each role is
kept unbiased by being denied the inputs that would let it launder.

- **A — Orchestrator** (this agent): is alerted to the QC findings and routes them. Makes
  no judgment, proposes no disposition, proposes no fix. Sees everything, decides nothing.
- **B — Disposition subagent**: is given ONLY the raw findings + locations, is forced to
  read all policies, and determines policy-aligned **dispositions** (per finding: is it a
  real violation, and which `POLICY.*` does it violate — or is it cleared, with the policy
  proof). **B is never shown, and never proposes, a remediation or fix.** B does not see
  the fixer, the remediation index, or any "correct shape." Disposition only.
- **C — Remediation subagent**: is given ONLY B's policy-aligned dispositions (the
  violations + their `POLICY.*` codes), looks each up in the **remediation policy index**
  (`policy-index/references/remediations.md`), and from that derives and implements the
  policy-aligned fix. C does not receive B's prose, "root causes," or any suggested fix —
  C derives the remediation from the policy index, not from anyone's opinion.

Why B may not suggest fixes: if B proposes a remediation, B's bias about *how much* to
change (minimize, under-fix, launder) propagates to C, and the independence is gone. The
disposition→remediation firewall forces C to derive the fix from the canonical remediation
index given only "what policy is violated," not "what B thinks should change."

## Triage Workflow (After User Approval)

Once the user approves, execute these steps in exactly this order:

### Step 1: Disposition Subagent (B)

Spawn a SUBAGENT to determine policy-aligned dispositions for the QC findings. This
subagent must:

- Load **all** the disposition policies explicitly — name them in the dispatch:
  `policy-index` (and its `references/red-flags.md`, `runtime-control-flow.md`,
  `policies.md`, `test-proof-rules.md`), `anti-slop`, `reviewing-llm-code`,
  `bespoke-software-policy`, and `test-guidelines`. (It is NOT given the remediation index
  — that belongs to C.)
- Review the flagged code against the FULL policy and, per finding, return a **disposition
  only**: VIOLATION (with the `POLICY.*` code it violates) or CLEARED (with the quoted
  policy proof). Cite codes, not rule labels (per "Classification Belongs to the Reviewer
  Subagent" above).

**B is forbidden from proposing, sketching, or implying any remediation, fix, "correct
shape," patch, or refactor.** Its entire output is the disposition list: finding → verdict
→ `POLICY.*` code. If B emits a fix suggestion, its output is contaminated and must be
re-run — the suggestion would bias C. B never sees C, the fixer, or the remediation index.

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

### Step 2: Remediation Subagent (C)

Spawn a **separate** SUBAGENT to remediate. This subagent must:

- Be a different instance from B.
- Receive ONLY B's policy-aligned dispositions — the list of `VIOLATION → POLICY.* code`
  entries (with file/line). It MUST NOT receive B's prose, "root causes," any suggested
  fix, or the orchestrator's opinion. Dispatch hygiene (above) applies to C as well: no
  seeded remediation.
- Load the **remediation policy index** (`policy-index/references/remediations.md`) plus
  `fixing-slop`. For each disposition, look up the `POLICY.*` code in the index, read the
  matching `REMEDIATE.*` entry, and derive the policy-aligned fix from it — not from anyone's
  suggestion.
- Implement the fix, then verify with `just test`.
- Report the fix outcome back.

B, C, and the orchestrator are three different agents. B disposes (no fixes). C remediates
from the index (given only dispositions). A routes (no judgment). None of them does another's
job.

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
| Merging disposition and remediation into one subagent | B games the fix criteria | Always separate B and C |
| B (disposition) proposing a fix / "correct shape" / refactor | Biases C toward B's preferred (possibly under-) fix | B returns dispositions + `POLICY.*` codes only |
| C (remediation) receiving B's prose or a suggested fix | Destroys C's independent derivation from the remediation index | C gets only `VIOLATION → POLICY.*` dispositions; derives fix from `remediations.md` |
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
- [ ] Disposition subagent (B) loaded all policies explicitly and returned dispositions
      ONLY (`VIOLATION → POLICY.*` / CLEARED) — no remediation, fix, or "correct shape"
- [ ] Remediation subagent (C) received only B's dispositions, derived fixes from
      `policy-index/references/remediations.md`, and verified with `just test`
- [ ] A, B, and C were three different agents; none did another's job
