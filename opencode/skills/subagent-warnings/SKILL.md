---
name: subagent-warnings
description: Use when reviewing finished subagent work, especially when a subagent claims success but the evidence may be thin, indirect, or overly optimistic.
---

# Subagent Warnings

Use this skill when a subagent finishes and you need to decide whether its work can be accepted as-is or needs more review.

## Core Policy

- Treat subagent summaries as leads, not proof.
- Decide review depth from evidence, not confidence or verbosity.
- Review only as deeply as the risk justifies, but never skip obvious verification when acceptance matters.

## Warning Signs

Load this skill and review more closely if any of the following are true:

- The task was broad, open-ended, or easy to reinterpret.
- The claimed result is larger than the visible diff.
- The diff is small, mechanical, or off-target relative to the request.
- The subagent reports success without showing tests, commands, or artifacts that would prove it.
- The transcript contains repeated retries, evasive summaries, or unexplained pivots.
- The change touches safety, correctness, data flow, permissions, or deletion logic.

## Review Ladder

Start at the lightest level that can falsify the claim:

- Check the diff if the task was primarily code changes.
- Check the transcript if you need to know what the subagent actually tried, verified, or skipped.
- Check tests or command outputs if correctness depends on execution rather than code shape.

For OpenCode sessions, use `ocm transcript <session-id>` when transcript evidence is needed.

## Decision Rule

- Accept the work if the evidence matches the task and there are no unresolved gaps.
- Review further if the evidence is incomplete, indirect, or inconsistent with the claim.
- Resume the subagent with specific gaps when you can name what is still unproven or off-target.

## Anti-Patterns

- Do not accept work because the summary sounds careful.
- Do not demand full transcript review for trivial, easily falsifiable changes.
- Do not confuse activity with completion.
