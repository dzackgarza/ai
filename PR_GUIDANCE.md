# Review Guidelines

These are additional requirements for reviewing agent work.
They do not replace the reviewer’s normal role, repo-specific standards, or technical
judgment. They provide the failure model that should shape the review.

The task is not merely to review a PR. The task is to decide whether a completion claim
is true under the original objective.
The standard is full, correct, provable completion against the original requirements and
repo guidelines. Anything less is incomplete work that must not be treated as a win.

## Failure Model

Agents systematically produce impressive non-completion.
Common patterns are: polished summaries that imply finished work, caveats that quietly
narrow the goal, reclassification without proof, delegated discovery presented as
resolution, process language that substitutes for evidence, merged PRs treated as
completion, passing checks treated as semantic proof, and artifacts that look
substantial while leaving required work unowned.

Treat the agent’s summary, PR description, closing comment, issue closure, “goal
completed” statement, and self-reported validations as untrusted.
They may be diagnostic pointers, but they are not evidence that the work is complete.
The evidence is the original issue or task, the code diff, tests, source/runtime facts,
review comments, and produced artifacts.

## Decisive Invariants

Preserve the original success condition.
Read the original issue or task before accepting any restatement of it.
Keep its quantifiers intact: “all,” “complete,” "full subset," “zero remaining,” and
similar terms cannot be quietly narrowed to examples, partial coverage, known blockers,
or whatever the PR happened to touch.

Nothing required may disappear silently.
A required work family must be implemented, explicitly falsified, or validly
reclassified with evidence that satisfies the issue’s own standard.
Partial implementation is not completion.
Future work is not completion.
Count reduction is not completion.
Resolved review threads are not completion.
Passing checks are not completion.
Substantial-looking work is not completion.
“Better than before” is not completion.

Goal substitution is the main thing to detect.
Ask whether the submitted work solves the original problem or merely produces a narrower
artifact: cleaner metadata, a partial subset, a better explanation, a new issue, a
renamed scope, a local workaround, or proof that someone should investigate later.

Technically correct administrative artifacts can be goal substitution.
A well-written issue, comment, audit note, scope statement, or enumeration of remaining
work may be required, but it does not complete implementation, testing, proof, or
downstream cleanup. If the original task requires execution, the artifact is only useful
insofar as it drives that execution; it must not become the stopping point.

Treat self-scoped remaining-work lists as a severe completion-laundering pattern.
When an agent is asked to enumerate remaining work, the domain is the original full
completion requirement, not the agent’s intended subset, the PR’s current shape, a
closeability criterion, or the work left after deferral and reclassification.
A valid enumeration subtracts only artifact-proven completed work from the original
contract. Deferrals, routed follow-ups, owner changes, and truthful incompletion notes
remain unresolved work unless the original task explicitly made that administrative
routing the whole deliverable.

If an agent repeats a narrowed enumeration after being corrected, treat that as a hard
misalignment signal, not as an innocent wording issue.
The reviewer should identify the original full requirement, the scope the agent
substituted, and the required work hidden by that substitution.

Silent reclassification is not resolution.
If the PR says remaining work is out-of-scope, research-owned, stub-owned, plugin-owned,
downstream-owned, or future-owned, require evidence from the relevant source/runtime
behavior, repo boundary, or original acceptance criteria.
A sentence in the PR description is not enough.

Ownership boundaries matter.
The submitting repo must prove its own claimed behavior and do the blocker forensics
required by its own issue.
Do not require a receiving or downstream repo to classify another project’s internal
uncertainty unless the original issue explicitly made that part of acceptance.
When an external issue is created, it should be written for that receiving repo, not for
a reader who already knows the submitting repo’s context.

## Evidence Expectations

Review tests as evidence, not as decoration.
Valid tests exercise the real production path or semantic requirement.
Be skeptical of helper-only tests, tautologies, assertions of the implementation’s own
output, bypasses around the runtime/plugin/stub path, example-only coverage where the
issue required full coverage, weakened assertions, and missing invalid-nearby cases
where the fix could overgeneralize.

For plugin work, the evidence should usually distinguish valid generic behavior from
invalid nearby ordinary Python and should not hard-code a downstream consumer.
For stubs work, the evidence should be source-backed: the upstream surface exists, the
stub matches public behavior, no fake API is added, no Any/object opacity escape is
introduced, and inherited-method inflation is not used unless source exposes that
surface.

Watch for code-level laundering: hard-coded consumer names, support for local research
abstractions as if they were external API, fake stubs, broad Any/object escapes, line
suppressions, diagnostic filtering, deletion of required data, broad type widening, and
any move that makes checks pass by weakening the problem instead of solving it.

## When Acting on Review Feedback

A positive disposition requires a commit.

Do not resolve an accepted review comment until the code/proof remediation is committed and the reply cites the commit.

Never reply “accepted,” “aligned,” “fixed,” “addressed,” or “will address” to a review thread unless the remediation is already committed. A thread cannot be resolved on intent or future work.

Rejected and modified feedback must be collected in a top-level PR comment titled `Review feedback disposition ledger` so resolved threads do not hide the audit trail.

Review comments are not implementation specs. The worker must translate accepted feedback into first-principles remediation requirements before assigning implementation.

For each comment:
- Identify the concern.
- Identify the proposed fix.
- Decide whether the concern is true under global + repo policy.
- Decide whether the proposed fix preserves those policies.
- If the concern is true but the fix is wrong, apply a policy-compatible remediation.

## Writing the Review

Write nuanced feedback for an intelligent reader.
Do not force a machine-readable template, a mandatory table, or a simplistic pass/fail
label when prose communicates the situation better.
Do make the completion judgment clear: whether the original task can be considered
complete, what evidence supports that judgment, and which unresolved requirements block
completion if any remain.

Do not foreground effort, progress, good intentions, volume of work, or “substantial”
partial implementation when required work remains.
Mention completed pieces only when they are necessary to identify the exact remaining
blockers or to prevent redoing already-correct work.
Do not compare incomplete work to “no work done” or “completely fake work”; compare it
to the expected standard: the task done correctly, completely, and provably.

When required work remains, lead with the incompleteness and the concrete blockers.
Do not make the reader excavate the missing work from beneath praise, context-setting,
or a narrative of what did get done.

Nuance belongs in the evidence and blocker analysis, not in softening the completion
standard. The review should make it easy to finish the work, not easy to feel satisfied
with less than the original contract required.
