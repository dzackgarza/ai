# Example Task: Debug Missing Cron Notifications

## Scenario

Notifications from cron-triggered agent runs are not appearing. Every cron job should produce exactly one notification (success or failure with explicit error details). We should see approximately one notification every 10 minutes.

## Investigation Steps

### 1. Baseline Check

Determine current time and inspect the crontab to identify what jobs should have run recently:

```bash
date
crontab -l
```

### 2. Check Notification Records

Review published notifications to see what actually finished and with what status:

```bash
# Check ntfy logs or notification history
# Compare expected vs actual notification count
```

### 3. Identify Gaps

For any cron job with no corresponding notification:
- This is a bug — every run must produce a notification
- Missing notifications indicate the agent runner has a failure path that doesn't report

### 4. Timeout Investigation

If agents are timing out:

1. **Test orchestrator health**: Run the same agent on trivial debug task(s) to verify basic operation
2. **Read live transcripts carefully**:
   - Is the agent running but churning in a loop?
   - Did the session hang entirely with no output?
   - Are there usage limit errors going unreported?

3. **Distinguish failure modes**:
   - Agent churning: bug in agent behavior or task design
   - Session hang: infrastructure or orchestrator bug
   - Silent usage limit: missing error handling in runner

### 5. Usage Limit Handling

If many usage limits are occurring:

```bash
# Send user notification summarizing limits and reset windows
ntfy send "Agent usage limits hit: [summary]. Windows reset at [times]. Consider switching agents for cron jobs."
```

Usage limits are unavoidable and require user action. The problem to fix is missing notifications, not the limits themselves.

### 6. Bug Fix Protocol

When you identify a bug in the agent runner:

1. **Prove it exists**: Gather specific evidence from logs/transcripts showing the exact failure path
2. **Fix with regression protection**:
   - Run linting (`npm run lint` or equivalent)
   - Run type checking (`npm run typecheck` or equivalent)
   - Run existing tests
   - Add new nontrivial tests that exercise the bug (no mocks, no long-running tasks)
3. **Commit with descriptive message**: The commit should clearly state what was broken and how it was fixed

### 7. Unknown Error Handling

If you cannot determine the cause:

1. **Deep read**: Go through transcripts and logs exhaustively first
2. **Record findings**: Create/update `agent_runner/TODO.md` with:
   - Exact timestamps of failures
   - Agent and task names
   - Relevant log excerpts
   - Hypotheses tested and ruled out
3. **Notify user**: Send ntfy notification requesting investigation assistance

## Success Criteria

- All cron jobs have corresponding notifications (success or explicit failure)
- Any bugs found are fixed with tests committed
- Usage limits are reported to user for their action
- Unknown issues are documented for human investigation

## Anti-Patterns to Avoid

- Assuming "no notification = success"
- Skipping the live transcript read
- Making changes without running lint/typecheck/tests
- Adding mock-based tests that don't exercise real failure paths
- Leaving TODO items without notifying the user
