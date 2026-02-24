# Example Task: Self-Improvement - Auditing Management Performance

## Scenario

This task audits the management task itself. Previous managerial agents may have failed to properly address worker agent issues, allowing problems to persist across multiple runs. The goal is to identify why previous managers shirked or failed, and fix the management prompt/playbook to prevent recurrence.

## Scope Warning

This task does NOT fix worker agent issues directly. The scope is specifically: **why did the previous managerial agent fail to fix observed problems?** Fixing the actual worker issues is a separate task.

## Investigation Protocol

### 1. Baseline: When Should Managers Have Run?

```bash
date
crontab -l
# Identify scheduled management runs
```

Map expected management run times against actual execution records.

### 2. Identify Worker Failures Preceding Management Runs

For each management run, examine the worker agent state that preceded it:

- Were there failing worker runs with no resolution?
- Missing commits?
- Undiagnosed errors?
- Timeouts not addressed?
- Missing notifications?

A management run that follows clear worker failures should have addressed them.

### 3. Examine Manager Transcript

Read the managerial agent transcript carefully:

**Did the manager observe the failures?**
- Check if logs/transcripts were actually read
- Did the manager acknowledge the problems existed?

**What did the manager do in response?**
- Skimmed logs and declared "fixed" without evidence?
- Churned on "debugging" without converging?
- Determined an incorrect cause and applied ineffective fix?
- Labeled issues as minor, inconsequential, or "expected"?
- Gave up and claimed blockers without escalating properly?

**Was escalation appropriate?**
- If there was a real blocker requiring human intervention, was the user notified via ntfy?
- Is that notification visible in the published topic?
- If no notification exists but the manager claimed "blocked", this is a failure

### 4. Evidence of Failed Fixes

Most importantly: **did the "fix" actually fix anything?**

Look for:
- Same failure pattern appearing in logs AFTER the management run
- Manager transcript shows "fix applied" but subsequent runs still fail
- This is clear evidence of manager failure—not ambiguity

This does not require deep analysis. The evidence should be obvious:
- Failing logs before manager run
- Manager transcript claiming to fix
- Same failing logs after manager run

## Metacognitive Failure Classification

Determine what kind of reasoning failure occurred:

### Early Termination
- Manager stopped investigating after superficial review
- Concluded "nothing to do" or "already fixed" without verification
- Did not follow through on observed problems

### Trivial / Superficial Changes
- Made cosmetic edits to prompts/playbooks
- Added negations or warnings without addressing root cause
- Changes too small to affect the observed failure mode

### Performative Work
- Wrote extensive analysis that doesn't connect to action
- Produced "documentation" of problems without fixing them
- Busywork that looks like management without being management

### Debugging Theater
- Long transcripts of "investigating" without convergence
- Checked many things but never identified the issue
- Process without progress

### Operative Failures
- Knew what to fix but couldn't execute (git errors, file access issues)
- Good reasoning, poor implementation

### Reasoning Failures
- Could not determine the issue despite available evidence
- Misdiagnosed root cause
- Applied wrong fix to wrong problem

### Minimization
- Observed failures but labeled them as:
  - "Minor" or "inconsequential"
  - "Expected behavior"
  - "Within normal parameters"
  - "Already known"
- These are escape hatches to avoid doing reparative work

## Research Phase

Before fixing the management prompt/playbook, research:

- LLM agent metacognitive failures
- Manager/oversight agent architectures in frontier systems
- Arxiv papers on:
  - Agent self-improvement
  - Multi-agent coordination failures
  - Oversight and monitoring in agentic systems
- OpenAI/Anthropic/etc research on agent reliability

Ground proposed fixes in this research.

## Fix Protocol

### Git History Check

Before editing management prompt/playbook:

```bash
git log --oneline --follow -- ~/agents/lattice_interface/agent_supervisor/prompt.md
```

Look for:
- Oscillating changes on the same issue
- Fixes that were reverted or replaced
- Patterns suggesting the current framing is an attractor or local minimum

If history shows churn, the fundamental approach may be wrong. Research more deeply before editing.

### Edit Constraints

**This task is unique**: Meta items about agent management ARE relevant here. Unlike worker prompts where meta-commentary must not leak, the management prompt can and should discuss management principles explicitly.

However, still avoid:
- Over-specification that creates checklists
- Negation replacements (remove concepts, don't invert them)
- Changes ungrounded in specific transcript evidence

### Target the Specific Failure Mode

If the manager:
- Terminated early → add explicit "continue investigating" language
- Made trivial changes → require evidence of fix verification
- Did performative work → ban non-action-producing analysis
- Did debugging theater → require convergence criteria
- Minimized issues → explicitly ban that language and framing

Cross-reference with research on preventing that specific failure mode.

## Verification

After making changes:

1. Edits trace clearly from: observed manager failure → transcript evidence → research → fix
2. Git history shows positive gradient (not oscillation)
3. Changes target the specific metacognitive failure identified
4. Research grounding is explicit and from quality sources
5. Commit message explains the managerial failure being addressed

## Success Criteria

- Each historical management failure has root metacognitive cause identified
- Fixes are grounded in transcript evidence and research
- Management prompt/playbook addresses the specific failure pattern
- Git history shows improvements, not churn
- Meta-commentary about management is appropriate (this task only)

## Anti-Patterns to Avoid

- Fixing worker agent issues directly (out of scope)
- Declaring "nothing could have been done" without evidence
- Making management changes without reading actual manager transcripts
- Treating repeated failures as "expected" or "known"
- Churning edits on management prompts without addressing root framing
- Escalating to user when manager should have been able to fix
- Applying fixes that don't connect to the observed failure mode
