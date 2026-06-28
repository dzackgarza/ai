# QC Triage Protocol

This document defines the mandatory triage procedure when global QC checks fail. It is a
reference for the `reviewing-llm-code` skill and for the directive emitted by central QC.

## Role Boundary

The agent that hits a QC failure is the orchestrator for that failure. It may route the
failure, but it may not judge it or remediate it. Triage exists because the agent that
produced or touched the failing work is biased toward preserving that work.

The ban on reading `~/ai-review-ci/` is role-specific:

- During downstream QC triage, the orchestrator must not inspect `~/ai-review-ci/`, the
  QC configs, tool scripts, models, prompts, or remediation policy. Those are the
  surfaces it could use to game the gate.
- During explicit maintenance of `ai-review-ci` itself, inspecting `~/ai-review-ci/` is
  required. In that task, `ai-review-ci` is the source repository, not the forbidden
  downstream-triage target.

Do not collapse these two cases. A downstream remediation run and a central-QC guidance
edit have different ownership boundaries.

## Immediate Orchestrator Rules

When a QC check fails and the triage directive is emitted, the orchestrator MUST:

1. **Make no judgment calls about findings.** Do not decide, state, hint, imply, or act on
   whether a finding is real, false, clean, slop, a false positive, or a tool bug.

2. **Stop all work.** Cease the in-progress task. Do not continue the original work until
   triage has resolved the QC failure.

3. **Do not probe QC internals.** Do not read, inspect, or modify `~/ai-review-ci/` during
   downstream triage. Do not read the remediation policy yourself. The remediation
   subagent reads it when that role starts.

4. **Do not self-fix and do not self-evaluate.** Review/disposition and remediation are
   delegated to agents that were not involved in producing the failing code.

5. **Present the raw output.** Show the complete raw QC output to the user. Do not filter,
   summarize, group, reinterpret, or convert it into your own report.

6. **Wait for explicit approval.** Do not proceed until the user directly approves triage.

## Routing Gate After User Approval

After approval, route by the shape of the raw QC output. This is a mechanical routing
check, not a policy judgment:

- If the raw QC output already contains explicit `POLICY.*` findings with file/line
  locations, that output is already the disposition artifact. Do not spawn a slop-report
  or disposition subagent to restate it. Proceed directly to **Route C: Remediation**.
- If the raw output does not contain explicit `POLICY.*` findings, use **Route B:
  Disposition**, then **Route C: Remediation** for any violations B returns.
- If you are unsure whether the output contains explicit policy-coded findings, do not
  decide. Use Route B.

A Semgrep, ast-grep, or central QC result whose message is `POLICY.RUNTIME_DEFAULT`,
`POLICY.CRITICAL_DEPENDENCY`, `POLICY.NO_LEGACY_SHIM`, or another `POLICY.*` code is
policy-coded output. The policy violation report is already in front of you.

## Route B: Disposition Subagent

Use this route only when the raw output lacks explicit `POLICY.*` findings.

Spawn a subagent to determine policy-aligned dispositions. The subagent must:

- Load the disposition policies explicitly: `policy-index` plus its references
  `red-flags.md`, `runtime-control-flow.md`, `policies.md`, and `test-proof-rules.md`;
  `anti-slop`; `reviewing-llm-code`; `bespoke-software-policy`; and `test-guidelines`.
  Do not give B the remediation index; it belongs to C.
- Receive only the raw findings and file/line locations. Do not include the
  orchestrator's verdict, leaning, explanation, root-cause theory, or proposed fix.
- Determine for itself whether the raw output is a tool-execution failure, a tool finding,
  or cleared. The orchestrator does not pre-judge this split.
- Return dispositions only: `VIOLATION -> POLICY.*` or `CLEARED`, with quoted policy
  proof. A false-positive or detector-narrowing disposition carries formal
  policy-exception burden: policy code, justification, replacement invariant, boundary
  proof, and audit trail.


B is forbidden from proposing, sketching, or implying remediation, a correct shape, a
patch, or a refactor. If B proposes a fix, its output is contaminated and must be rerun.

## Route C: Remediation Subagent

Use this route for policy-coded QC output, or after Route B returns `VIOLATION -> POLICY.*`
dispositions.

Spawn a separate remediation subagent. The subagent must:

- Be a different agent from any disposition/review agent and from the orchestrator.
- Receive only the policy-coded findings: file/line, snippet when present in the raw QC
  output, and `POLICY.*` code. Do not include B's prose, root-cause narrative, suggested
  fix, or the orchestrator's opinion.
- Load the remediation policy index: `policy-index/references/remediations.md` (vendored
  in `ai-review-ci` runtime copies under `reviews/vendor/policy-index/references/remediations.md`) and `fixing-slop`.
- For each `POLICY.*` code, look up the matching `REMEDIATE.*` entry and derive the fix
  from the policy, not from another agent's suggestion.
- Implement the remediation in the target repository only.
- Verify with the target repository's canonical QC command, normally `just test` unless
  the emitted directive names a stricter target-repo command.
- Report the fix outcome and any blocker back to the orchestrator.

The orchestrator must not read the remediation policy during downstream triage. C reads it.

## Dispatch Hygiene

Dispatch prompts are part of the proof boundary. They must not seed the result.

For Route B, the dispatch may contain only:

- the raw, verbatim QC output or un-coded finding output;
- file/line locations from that output;
- the instruction to load the named disposition policies;
- the instruction to return dispositions only.

For Route C, the dispatch may contain only:

- policy-coded findings from the raw QC output or B's disposition list;
- file/line locations and snippets that came from the raw QC output;
- the instruction to load `policy-index/references/remediations.md` and `fixing-slop`;
- the instruction to remediate according to the matching `REMEDIATE.*` entries.

Do not include:

- "suspected false positive," "confirmed slop," "probably a tool bug," or any similar
  orchestrator leaning;
- root-cause narratives not produced by the assigned role;
- suggested fixes from B or from the orchestrator;
- excerpts from the remediation policy copied by the orchestrator.

## Prohibited Behaviors

| Behavior | Why | Instead |
| --- | --- | --- |
| Orchestrator reads `~/ai-review-ci/` during downstream triage | Gives the failing-code producer gate internals it can game | Present raw output, get approval, then delegate |
| Orchestrator reads the remediation policy during downstream triage | That is C's job and contaminates routing | Tell C to load `policy-index/references/remediations.md` |
| Spawning a slop-report subagent for already policy-coded QC output | Repeats the report and delays remediation | Treat the raw `POLICY.*` output as the disposition artifact and spawn C |
| Orchestrator forming/stating a finding disposition | The producer's self-judgment is inadmissible | Route without judgment |
| Seeding B or C with a verdict, leaning, or proposed fix | Collapses independent review/remediation into confirmation of the orchestrator | Dispatch raw findings or policy-coded dispositions only |
| B proposing remediation | Biases C toward B's preferred fix | B returns dispositions only |
| C receiving B's prose or suggested fix | Destroys C's independent derivation from the remediation index | C gets only `VIOLATION -> POLICY.*` entries |
| Running isolated checks to verify | Cherry-picks around the full gate | Run the target repo's canonical `just test` after remediation |
| Adding bypass comments or suppressions | Hides symptoms without satisfying policy | Fix the policy violation |
| Editing QC configs or thresholds during downstream triage | Weakens central QC for all consumers | Change only target project code |
| Continuing the original task after QC fails | The current output failed the gate | Triage first, then resume only if the fix leaves work remaining |

## Evidence Requirements

Before reporting triage complete, these must be true:

- [ ] Raw QC output was presented to the user without filtering or interpretation.
- [ ] The user explicitly approved triage.
- [ ] The orchestrator did not inspect `~/ai-review-ci/` or the remediation policy during
      downstream triage.
- [ ] The routing decision was mechanical: explicit `POLICY.*` output went directly to C;
      un-coded output went to B first.
- [ ] If B ran, B returned dispositions only and no remediation.
- [ ] C received only policy-coded findings, loaded the remediation policy index and
      `fixing-slop`, remediated from the matching `REMEDIATE.*` entries, and verified with
      the target repo's canonical QC command.
- [ ] B and C, when both are used, were different agents.
