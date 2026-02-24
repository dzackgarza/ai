# Example Task: Operational Issues - Commit and Workflow Failures

## Scenario

Agents are failing operational requirements: not creating commits, mismanaging git state, or polluting docs with changelog data that belongs in commit messages. A successful run requires: startup → read task → nontrivial work → cohesive commit → success notification with meaningful progress summary.

## Prerequisites: Triage First

Before investigating commit failures, check for more urgent issues:

```bash
date
crontab -l
# Check recent ntfy notifications
```

If there are timeouts or usage limit failures, triage those separately. Commit investigation applies only to runs that had opportunity to commit but didn't.

## Primary Failure Mode: No Commit Created

### Investigation

1. **Check notification records** for failures mentioning "no commit" or "empty changeset"
2. **Read the transcript deeply** to determine:
   - Did the agent do partial work then quit early? (prompt adherence issue)
   - Did the agent do real work but forget to commit? (operational instruction issue)
   - Did the agent encounter git errors they couldn't resolve? (tool fluency issue)

### Differentiating Causes

**Partial work / early quit**:
- Transcript shows agent reasoning that "enough" was done
- CoT reveals false completion signals or underestimated scope
- Fix: Prompt/playbook updates for stricter task adherence

**Real work, forgot commit**:
- Transcript shows substantive tool calls and file edits
- No git commands near session end
- Agent may have hit token/time limits before commit step
- Fix: Earlier/louder commit instructions in workflow

**Git confusion**:
- Transcript shows git commands that failed or produced unexpected results
- Agent may have been unable to interpret status
- Fix: Clearer git workflow guidance

## Fix Strategies

### Prompt/Playbook Updates

When agents consistently fail to commit or quit early:

1. **Research task adherence** in LLM literature:
   - Arxiv papers on instruction following
   - OpenAI/Anthropic research on weaker model behavior
   - Frontier lab publications on workflow compliance

2. **Update instructions** based on findings:
   - Add explicit commit requirements earlier in workflow
   - Frame commit as mandatory, not optional
   - Remove any language that could signal "good enough to stop"

3. **Avoid over-prescription**:
   - Don't mandate exact commit message formats
   - Don't create rigid checklists agents follow blindly
   - Allow dynamic response to changing circumstances
   - Stochastic agents need flexibility, not rules engines

### Model Capability Issues

If a specific model consistently fails task adherence despite prompt fixes:

1. **Document the pattern**: Log all failed instances with timestamps, task names, and failure modes
2. **Notify user via ntfy**:
   ```
   Model [model_name] consistently failing task adherence on [task_type].
   Instances: [count] failures over [time_period].
   Suggest replacing with more capable agent for this task.
   ```
3. This is a last resort—prompt fixes should be attempted first

## Secondary Failure Mode: Git State Confusion

Agents may get confused by complicated git status (uncommitted changes, merge conflicts, detached HEAD).

### Resolution Protocol

1. **Never throw away uncommitted work**
2. **Never use destructive operations** (reset --hard, checkout --force, clean -fd)
3. **Treat git as time-indexed checkpoints**:
   ```bash
   # Check current state
   git status
   git log --oneline -5
   
   # Commit any uncommitted work to preserve it
   git add -A
   git commit -m "WIP: preserving state before cleanup"
   
   # Only after preserving, clean up to stable state
   ```

4. Goal is to prevent future agent confusion, not to achieve "clean" state at the cost of lost work

### Prompt/Playbook Guidance

Add language that:
- Requires agents to commit before major operations
- Explains git as checkpoint system, not pristine state machine
- Discourages destructive git commands
- Provides fallback behaviors for confusing states

## Tertiary Failure Mode: Changelog Pollution

Agents recording history/progress in wrong places:

- TODO docs with "completed" sections
- Memories that summarize what was done
- Documentation files with changelog sections
- Any artifact that duplicates git history

### Why This Is Harmful

1. Creates false completion signals for future agents
2. Duplicates information that git already tracks
3. Pollutes agent-facing docs with non-actionable historical data
4. Biases toward early completion when changelogs show "progress"

### Fix Strategy

1. **Ban changelog-style content** in docs and memories:
   - Prompts should explicitly forbid "recording what was done"
   - Memories should only contain actionable insight for future work
   - Docs should describe current state, not history of changes

2. **Redirect to commit messages**:
   - Extensive commit messages are the correct place for history
   - Agents should write detailed commits explaining what and why
   - Git is the authoritative changelog

3. **Clean up existing pollution**:
   - Remove changelog sections from docs
   - Delete memories that are pure history
   - Do NOT add "this was removed" notes—just remove

## Research Requirements

Before making prompt changes:

1. **Read actual research** on:
   - Task adherence in language models
   - Workflow compliance for LLM agents
   - Failure modes in agentic systems
   - Arxiv papers, not blogs
   - Frontier model firm publications (OpenAI, Anthropic, Google DeepMind)

2. **Ground changes in evidence**:
   - Specific transcript excerpts showing failure
   - Research explaining why the failure occurs
   - Principles that address the root cause

## Success Criteria

- All commit-related failures have root causes identified
- Fixes are grounded in transcript evidence and research
- Git state is clean without losing any work
- No changelog pollution in docs or memories
- Prompts ban harmful behaviors without being rigidly prescriptive
- Model capability issues are escalated to user with evidence

## Anti-Patterns to Avoid

- Mandating exact commit message formats (inflexible)
- Creating checklists for git operations (agents follow blindly)
- Using destructive git commands to "clean up"
- Adding changelog sections anywhere except commit messages
- Making prompt changes without transcript evidence
- Escalating to user before attempting prompt fixes
- Over-specifying workflows that must adapt to changing circumstances
