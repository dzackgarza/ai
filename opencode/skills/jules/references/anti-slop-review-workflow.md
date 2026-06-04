# Jules Anti-Slop Review Workflow

Use when leveraging Jules as a low-cost reviewer for LLM-produced code, especially PRs,
branches, or recent commits that may contain slop. Jules is not the authority and must
not implement fixes by default. Jules produces an evidence-backed anti-slop issue; a
stronger controller validates and triages the issue afterward.

## Core Doctrine

Jules is a review-assistance worker, not a completion authority.

Jules may:
- inspect a branch/PR/diff,
- apply the full anti-slop curriculum supplied in the prompt,
- identify candidate slop patterns,
- produce a structured anti-slop report,
- open a GitHub issue containing the findings.

Jules may not by default:
- implement fixes,
- mutate code,
- resolve review threads,
- approve or reject PRs,
- mark its own findings as authoritative,
- substitute generic code-review advice for anti-slop pattern findings.

This fits the existing `reviewing-llm-code` rule: the review is not a normal bug list, and findings must match loaded patterns or be dropped.

## Required Controller Workflow

The controller, not Jules, owns context preparation and validation.

1. Identify the target: PR URL, branch, commit range, or local diff.
2. Build a context bundle containing the full anti-slop guidance, not a summary.
3. Include the original task/issue/PR contract if available.
4. Tell Jules that its only deliverable is a GitHub issue with evidence-backed findings.
5. After Jules opens the issue, the controller reviews the issue under `reviewing-subagent-work` and `reviewing-llm-code`.
6. Accepted findings become implementation work for a stronger agent or a separate task.
7. Invalid findings are rejected explicitly in a comment on the issue.

The existing Jules skill says Jules has a restricted Linux environment and no access to online docs or external references, so context engineering in the prompt is essential. Therefore the controller should not rely on Jules finding the anti-slop skills itself. It should paste or attach the full relevant text.

## Anti-Slop Context Bundle

The prompt should include full content, or a generated bundled excerpt, from:
- [reviewing-llm-code](file:///home/dzack/ai/opencode/skills/reviewing-llm-code/SKILL.md)
- [anti-slop](file:///home/dzack/ai/opencode/skills/anti-slop/SKILL.md)
- [pattern-catalog](file:///home/dzack/ai/opencode/skills/reviewing-llm-code/references/pattern-catalog.md)
- [coding-failures](file:///home/dzack/ai/opencode/skills/llm-failure-modes/coding-failures.md)
- [testing-failures](file:///home/dzack/ai/opencode/skills/llm-failure-modes/testing-failures.md)
- [structural-failures](file:///home/dzack/ai/opencode/skills/llm-failure-modes/structural-failures.md)
- [field-observations](file:///home/dzack/ai/opencode/skills/llm-failure-modes/field-observations.md)
- [reviewing-subagent-work](file:///home/dzack/ai/opencode/skills/reviewing-subagent-work/SKILL.md)
- [test-guidelines](file:///home/dzack/ai/opencode/skills/test-guidelines/SKILL.md) if tests/QC are in the diff
- [known-solution-first](file:///home/dzack/ai/opencode/skills/known-solution-first/SKILL.md) if dependency/tool reinvention is likely

This is consistent with `reviewing-llm-code`, which says the reviewer must load `anti-slop`, the pattern catalog, `llm-failure-modes`, `addressing-shallow-work`, and `reviewing-subagent-work` before producing review findings.

## Jules Prompt Template

Use this canonical template when instructing Jules:

```markdown
You are Jules. You are not implementing code in this task.

You are performing an anti-slop review of LLM-produced work. Your job is to find
implementation-quality failures that match the supplied anti-slop and LLM-failure-mode
guidance.

You must not perform a normal generic code review. Do not report generic security,
performance, edge-case, sandboxing, compatibility, or style suggestions unless they
map directly to one of the supplied anti-slop patterns and are supported by concrete code
evidence.

You must not edit code. You must not create a PR. Your deliverable is a GitHub issue
containing the anti-slop report.

Target:
- Repository: <owner/repo>
- PR/branch/commit range: <target>
- Original task / issue / PR contract: <paste or summarize with link>
- Files or subsystems in scope: <list>
- Files or subsystems out of scope: <list>

Authoritative review curriculum follows. Treat this text as policy. Do not weaken it.
<PASTE FULL REVIEWING-LLM-CODE + ANTI-SLOP + PATTERN CATALOG + FAILURE MODES + TEST GUIDELINES IF RELEVANT>

Review procedure:
1. Read the original task or PR contract first.
2. Read the diff and changed files.
3. Identify candidate findings only when they match the supplied anti-slop patterns.
4. For each candidate finding, provide exact file/line evidence.
5. Separate user design choices from implementation slop.
6. Do not list normal bugs unless the bug is evidence of a slop pattern.
7. Do not suggest generic enterprise hardening, graceful fallback, mocks, skips,
   defensive edge handling, or micro-optimizations.
8. Prefer deletion, reuse, centralization, known dependencies, and global QC integration
   as remediation directions when supported by the evidence.

Create a GitHub issue titled:

Anti-slop review: <target title or PR number>

The issue body must use this structure:

# Anti-slop review target

- Repository:
- PR / branch / commit:
- Original task / contract:
- Date:
- Reviewer: Jules
- Scope reviewed:

# Executive finding

One paragraph: does the work appear structurally sound, or does it contain candidate
LLM slop requiring human triage?

# Findings

For each finding:

## Finding N: <pattern name>

- Pattern: <exact pattern from supplied guidance>
- Evidence:
  - <file:line> — <what the code does>
  - <file:line> — <supporting evidence>
- Why this is slop:
  <explain how the evidence matches the pattern, not a generic opinion>
- Why this is not merely a user design choice:
  <apply the design-choice gate>
- Likely remediation direction:
  <delete/reuse/centralize/replace with dependency/add proof surface/etc.>
- Confidence: high | medium | low
- What would falsify this finding:
  <specific evidence that would show the finding is wrong>

# Non-findings / deliberately rejected generic comments

List any tempting generic review comments you rejected, such as performance micro-optimizations,
sandbox paranoia, graceful fallback advice, or broad edge-case hardening.

# Suggested triage order

Order findings by expected quality impact and ease of validation.

# Caveat

This issue is a candidate anti-slop report produced by Jules. It requires validation by a
stronger reviewer before implementation work begins.
```

This final caveat is important. It prevents the issue from being mistaken for authoritative truth.

## Issue-Opening Mechanics

The subskill prefers issue creation, not PR creation.

Recommended controller/Jules command shape:

```bash
cat .jules/anti-slop-review-prompt.md | jules new --repo owner/repo
```

or, using the existing improved CLI pattern:

```bash
uvx git+https://github.com/dzackgarza/improved-jules-cli create \
  <ISSUE_OR_PR_URL> \
  --context .jules/anti-slop-review-prompt.md \
  --prompt-slug sub-agents/jules-anti-slop-review
```

If Jules cannot open the issue directly, it must produce the exact issue body and stop. The controller then opens the issue manually. The issue should follow the existing issue-writing rules: deep description, proof/evidence, concrete expected behavior, no implementation code, no detailed implementation plan, and no time estimates.

## Required Validation after Jules Produces the Issue

Do not treat a Jules anti-slop issue as accepted findings.

After the issue is created:
1. Load `reviewing-subagent-work`.
2. Load `reviewing-llm-code` and `anti-slop`.
3. For each Jules finding, check whether:
   - the cited file/line exists,
   - the cited code says what Jules claims,
   - the pattern name matches the evidence,
   - the issue distinguishes user design from implementation slop,
   - the suggested remediation does not import generic PR-review slop.
4. Comment on the issue with dispositions:
   - accepted,
   - accepted with modified remediation,
   - rejected,
   - needs investigation.
5. Do not implement from the Jules issue until this validation comment exists.

This uses the existing `reviewing-subagent-work` principle: a subagent’s output must prove something based on concrete evidence; self-reports are not correctness evidence.

## What Jules Should Be Good at Here

Jules can help by:
- reading many changed files cheaply,
- producing candidate pattern matches,
- noticing repeated implementation smells,
- finding duplicated local patches,
- enumerating suspicious proof surfaces,
- creating a durable issue that stronger agents can triage.

Jules should not be asked to:
- decide whether the PR should merge,
- independently resolve review comments,
- implement anti-slop refactors,
- decide policy conflicts,
- perform external-tool research,
- invent fixes for complex architecture.

This aligns with the current Jules skill’s own “best for / avoid for” guidance: Jules is best for straightforward tasks where research is already done and should be avoided for tasks requiring external API research or unfamiliar integrations.

## Controller Checklist Before Launching Jules

- [ ] Target PR/branch/commit identified.
- [ ] Original task or PR contract included.
- [ ] Full anti-slop/reviewing-llm-code/pattern-catalog guidance included.
- [ ] Tests/QC guidance included if tests are in scope.
- [ ] Jules explicitly forbidden from editing code.
- [ ] Jules deliverable is a GitHub issue.
- [ ] Issue template included.
- [ ] Controller plans to validate the issue before implementation.
