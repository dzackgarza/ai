# Build Agent Addendum (Repo-Specific)

## Operating Rules (Hard Constraints)

1. **Test Work Requires Test Guidelines Review**: If you add or modify tests (or change test methodology), you MUST have the **Test Guidelines** subagent review the resulting test changes before you finalize the work (e.g., before concluding the task or making a commit).
2. **Fix, Don’t Weaken**: If Test Guidelines reports violations, you MUST fix the tests (or the underlying code) with equally specific, compliant changes. Do not "paper over" findings by making the tests less specific.
3. **No Off-Plan Methodology Injection**: When executing from an approved plan file, do not introduce new test techniques or implementation approaches that are not in the plan. If a deviation is required, stop and ask the user.

## Process Addition

When tests are part of the change:

1. Ensure your changes are in the working tree (tests written/updated).
2. Spawn **Test Guidelines** subagent with:
   - the test files you changed (and any relevant production files)
   - request a compliance audit + concrete fixes
3. Apply the fixes.
4. Re-run the Test Guidelines review if changes were made.

---

${AgentSkills}

${SubAgents}

## Available Tools

${AvailableTools}
