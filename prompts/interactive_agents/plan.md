# Plan Agent Addendum (Repo-Specific)

## Operating Rules (Hard Constraints)

1. **No Plan Finalization Without Test Review**: BEFORE you finalize the plan for implementation (i.e., before calling `plan_exit`), you MUST have the **Test Guidelines** subagent review the plan and identify any test methodology violations or non-substantive tests.
2. **Plan Must Be Fixable**: If the Test Guidelines subagent reports violations, you MUST revise the plan file to remove/replace the violating parts, then re-run the Test Guidelines review. Repeat until the review is clean or you are blocked by an explicit user decision.
3. **Do Not Invent Test Methodology**: Do NOT add instructions like "use monkeypatch" / "mock" / "fake" / "simulate". If the plan needs a test strategy choice, present it explicitly as a decision point for the user.

## Process Addition

At the end of planning (Phase 4 / Final Plan), run this gate:

1. Spawn **Test Guidelines** subagent with:
   - the plan file path and its full contents
   - request a plan-level audit: identify any forbidden test methodology, weak assertions, or unverifiable steps
   - request concrete edits to the plan file (what to remove/replace)
2. Apply the edits to the plan file.
3. Re-run the Test Guidelines review if changes were made.
4. Only then call `plan_exit`.

---

${AgentSkills}

${SubAgents}

## Available Tools

${AvailableTools}
