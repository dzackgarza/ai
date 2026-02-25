# Plan Agent Addendum (Repo-Specific)

## Operating Rules (Hard Constraints)

1. **No Plan Finalization Without Test Review**: BEFORE you finalize the plan for implementation (i.e., before calling `plan_exit`), you MUST have the **Test Guidelines** subagent review the plan and identify any test methodology violations or non-substantive tests.
2. **Plan Must Be Fixable**: If the Test Guidelines subagent reports violations, you MUST revise the plan file to remove/replace the violating parts, then re-run the Test Guidelines review. Repeat until the review is clean or you are blocked by an explicit user decision.
3. **Plan Must Be Executable**: The plan MUST be fully detailed and directly executable (including specific test methodology and concrete oracles). If any plan detail is non-compliant with Test Guidelines, you MUST replace it with an equally specific, compliant alternative (do not vague it out).

## Process Addition

At the end of planning (Phase 4 / Final Plan), run this gate:

0. Ensure the plan is written/updated at the exact plan file path provided by the plan-mode system reminder.
1. Spawn **Test Guidelines** subagent with the plan file path and full plan contents.
2. Request a plan-level audit focusing on: (a) methodology compliance, (b) substantive oracles, (c) unverifiable steps.
3. Require the subagent to propose compliant replacements (not just removals) for any violating plan steps.
4. Apply the suggested edits to the plan file.
5. Re-run the Test Guidelines review if changes were made.
6. Only then call `plan_exit`.

---

${AgentSkills}

${SubAgents}

## Available Tools

${AvailableTools}
