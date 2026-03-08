# Permission Architecture Specification (2026)

This document defines role boundaries, delegation policy, and permission design for agent-based development in this repository.

## 1. Objectives

- Maximize delivered quality while minimizing paid-model token cost.
- Offload rote and high-volume tasks to cheaper/free subagents when risk is low.
- Reserve strong models for planning synthesis, integration decisions, and high-risk audits.
- Separate exploration, creation, and verification so one weak run cannot self-certify bad output.
- Prevent reward hacking, early quitting, false success reports, and hallucinated completion claims.

## 2. Core Operating Principles

1. **Role separation is mandatory**:
   - Exploration, implementation, and verification must be distinct roles.
2. **Orchestrator owns delegation**:
   - Planner does not assign workers.
   - Orchestrator chooses which subagents execute each plan item.
3. **Planner translates specs to plans**:
   - Planner ingests user/client specs and outputs structured execution plans.
4. **Rubric-based verification, not machine-check heuristics**:
   - In 2026, review quality comes from model-graded rubrics and review subagents.
5. **Single authority for integration**:
   - Final branch integration and canonical commits are controlled by Orchestrator.
6. **Permission policy is capability-first**:
   - Shared behavior lives in top-level reusable rule sets.
   - Agent profiles compose capabilities.
   - Per-agent exceptions exist only for truly role-specific needs.
7. **Permission policy is layered**:
   - Global baselines apply first, then category baselines, then role profiles, then narrow exceptions.
8. **Subagent recursion is disabled by default**:
   - Subagents should not spawn additional subagents unless explicitly whitelisted for a specialized coordinator role.

## 3. Major Roles and Responsibilities

## 3.1 Planner (Spec Translator)

Purpose:
- Convert user/client specs into structured plans, constraints, and acceptance rubrics.

Must do:
- Extract objectives, constraints, and dependencies.
- Produce execution-ready work breakdowns.
- Produce review rubrics (correctness, safety, maintainability, tests, risk).
- Trigger plan-review subagents when required by policy.

Must not do:
- Direct implementation.
- Subagent assignment decisions.
- Final integration decisions.

## 3.2 Orchestrator (Delegator + Integrator)

Purpose:
- Execute the plan by assigning work, coordinating subagents, auditing outputs, and integrating final changes.

Must do:
- Choose subagent role/model per task.
- Enforce staged flow: exploration -> implementation -> verification -> integration.
- Resolve conflicting subagent outputs.
- Run final integration checks.
- Own final git commits on canonical branch.

Must not do:
- Skip independent review for risky changes.
- Delegate away final integration accountability.

## 3.3 Explorer / Researcher

Purpose:
- Gather evidence: code locations, docs, interfaces, behavior traces, historical context.

Must do:
- Produce evidence-backed findings with references.
- Report uncertainty explicitly.

Must not do:
- Edit code.
- Claim implementation completion.

## 3.4 Writer Roles (Split for Isolation)

### 3.4.1 Source Writer

Purpose:
- Implement production code in `src/` only.

Must do:
- Modify only assigned source scope.
- Provide evidence of completion (diff + verification output).

Must not do:
- Read or edit `test/` or `tests/` when operating in strict TDD isolation mode.
- Approve own work.
- Perform final integration commits.

### 3.4.2 Test Writer

Purpose:
- Implement tests in `test/` and `tests/` only.

Must do:
- Translate requirements/rubric into behavior-focused tests.
- Provide evidence of completion (diff + verification output).

Must not do:
- Read or edit `src/` when operating in strict TDD isolation mode.
- Approve own work.
- Perform final integration commits.

### 3.4.3 Documentation Writer (Optional)

Purpose:
- Implement documentation updates in `docs/` only.

Must not do:
- Make source or test changes unless explicitly escalated to Orchestrator.

## 3.5 Reviewer / Auditor

Purpose:
- Independently evaluate output quality and correctness against rubric.

Must do:
- Grade against rubric dimensions.
- Identify omissions, regressions, hallucinated claims, and weak reasoning.
- Request targeted fixes.

Must not do:
- Rubber-stamp producer output.
- Share execution context that biases independence.

## 3.6 Interactive Agent (General Purpose, Non-Cycle)

Purpose:
- Handle ad hoc interactive work that is not part of a long-lived plan -> orchestrator cycle.

Typical tasks:
- quick debugging
- one-off edits
- exploratory Q&A with local code
- command execution support

Must do:
- stay responsive and conversational
- avoid unnecessary subagent fan-out for trivial tasks
- escalate to Orchestrator-led cycle when scope grows beyond interactive bounds

Must not do:
- impersonate full orchestration authority of Orchestrator
- bypass review for risky or high-blast-radius changes

## 4. Cost/Quality Strategy by Role

- **Cheap/free first** for:
  - repository exploration
  - repetitive transformations
  - boilerplate implementation
  - first-pass doc/test drafting
- **Strong models required** for:
  - ambiguous specs and complex planning synthesis
  - cross-module or high-risk refactors
  - security/permission policy audits
  - final integration decisions
  - dispute resolution between subagent outputs

Escalation triggers from cheap/free to strong:
- Two failed attempts on same task.
- Reviewer flags critical risk.
- Diff touches auth/permissions/security or broad architecture.
- Test failures are non-local or hard to diagnose.
- Evidence quality is low or claims conflict with observed artifacts.

## 5. Stage-Gated Workflow

1. **Spec Intake** (Planner)
   - Input: user/client requirements.
   - Output: structured plan + rubric.
2. **Plan Review** (Reviewer)
   - Output: approved or revised plan/rubric.
3. **Delegation Design** (Orchestrator)
   - Output: task allocation to subagent roles/models.
4. **Exploration** (Explorer)
   - Output: evidence package for implementation.
5. **Implementation** (Writer)
   - Output: scoped diffs + local verification evidence.
6. **Independent Verification** (Reviewer/Auditor)
   - Output: rubric score + required fixes.
7. **Integration** (Orchestrator)
   - Output: final composed diff, final checks, canonical commits.

No stage may self-certify its own output for the next gate.

## 5.1 Strict TDD Blind Workflow (Mandatory Default)

This mode intentionally prevents Source and Test writers from reading each other's directories and is the default policy.

1. Planner produces behavior spec + rubric in `.serena/plans/`.
2. Orchestrator assigns Test Writer first.
3. Test Writer writes tests from spec/rubric without `src/` visibility.
4. Orchestrator assigns Source Writer with spec/rubric and test-failure signals, without test file visibility.
5. Reviewer/Auditor validates full behavior with full visibility.
6. Orchestrator decides iterations and integrates final result.

Rationale:
- Prevents implementation-coupled test gaming.
- Forces spec-first behavior contracts.
- Improves confidence that tests describe intended behavior rather than mirrored internals.

Opt-out rule:
- Orchestrator may request temporary visibility exceptions only with explicit justification recorded in the plan.

## 5.2 Interactive Workflow (Outside Plan-Build Cycle)

This path is for general interactive work that does not need full pipeline orchestration.

1. Interactive agent scopes the task.
2. Interactive agent executes directly when low-risk and local.
3. Interactive agent escalates to Planner + Orchestrator cycle when complexity/risk exceeds interactive policy thresholds.

Escalation triggers:
- multi-stage or multi-role coordination needed
- cross-directory high-risk refactor
- security/permission-sensitive change
- ambiguous requirements needing formal rubric review

## 6. Permission Boundary Model

## 6.A Permission Inheritance Layers

Permissions should be composed in this order (least specific -> most specific):

1. **ALL_AGENTS_BASELINE**
   - applies to every agent type
   - includes universal safety rules and minimum operational controls
2. **PURE_AGENTS_BASELINE**
   - applies to single-role agents that should not orchestrate
3. **SUBAGENTS_BASELINE**
   - applies to all subagents
   - default recursion controls live here
4. **TOP_LEVEL_AGENTS_BASELINE**
   - applies to primary agents (`Planner`, `Orchestrator`, `Interactive`, etc.)
5. **ROLE_PROFILE**
   - role-specific permissions (`planner`, `orchestrator`, `src_writer_strict`, `reviewer`, `interactive_general`)
6. **NARROW_EXCEPTIONS**
   - explicit, documented deviations for special cases

### 6.A.1 Mandatory cross-cutting controls

For **ALL_SUBAGENTS** by default:
- `task`: deny
- `todoread`: deny
- `todowrite`: deny
- any recursive delegation tool: deny
- `async_command`: deny
- `async_subagent`: deny
- `introspection`: deny
- `list_sessions`: deny
- `read_transcript`: deny

Rationale:
- prevents uncontrolled recursion
- prevents cost blowups from delegation trees
- keeps responsibility on Orchestrator for assignment and orchestration

Allowed exception:
- only dedicated coordinator subagents, explicitly designated by Orchestrator policy, may receive `task`/`todoread`/`todowrite`: allow.

For **ALL_AGENTS**:
- `bash`: deny by default at global baseline
- `serena_execute_shell_command`: deny (non-overridable)
- Serena memory CRUD is allowed (`serena_read_memory`, `serena_list_memories`, `serena_write_memory`, `serena_edit_memory`, `serena_delete_memory`, `serena_rename_memory`)
- disable Serena onboarding/workflow helpers (`serena_onboarding`, `serena_prepare_for_new_conversation`, `serena_initial_instructions`, `serena_think_about_*`) and enforce this via global deny list
- Serena file read/write tools are path-scoped through role profiles (same policy boundary as built-in read/edit tools)
- require evidence-based completion claims

For **PURE_AGENTS** (all non-subagent agents, including top-level roles):
- allow coordination surfaces: `task`, `todoread`, `todowrite`
- allow `introspection`, `list_sessions`, and `read_transcript`
- keep role-specific scope controls in profile layers (`planner`, `orchestrator`, `interactive`, etc.)

## 6.0 Directory Layout Assumptions for Policy

Policy assumes these structured directories exist and are stable:
- `.serena/`
- `.serena/plans/`
- `docs/`
- `src/`
- `test/` and/or `tests/`

If a repository deviates, Orchestrator must adapt profiles while preserving the same isolation intent.

## 6.1 Planner permissions

Allow:
- read/search across repo
- plan artifacts write
- task dispatch request surface

Deny:
- general code edits
- git mutation
- final integration commands

## 6.2 Orchestrator permissions

Allow:
- broad read
- controlled write across project
- delegation tools
- integration validation commands
- git mutation required for canonical history via dedicated tools (`git_add`, `git_commit`)

Deny:
- unnecessary unrestricted destructive commands

## 6.3 Explorer permissions

Allow:
- read/search/web/doc lookup
- non-mutating shell inspection

Deny:
- edit/write/patch
- git mutation

## 6.4 Writer permissions

Allow:
- write only within assigned scope
- optional local checkpoint git in isolated worktree only (policy toggle), via `git_add`/`git_commit`

Deny:
- broad repo writes outside scope
- canonical-branch integration commits

### 6.4.A Source Writer (strict profile, default)

Allow:
- read/write `src/`
- read `.serena/plans/` for requirements context

Deny:
- read/write `test/`
- read/write `tests/`
- read/write `docs/` (unless explicitly required by Orchestrator)

### 6.4.B Test Writer (strict profile, default)

Allow:
- read/write `test/` and `tests/`
- read `.serena/plans/` for requirements context

Deny:
- read/write `src/`
- read/write `docs/` (unless explicitly required by Orchestrator)

### 6.4.C Docs Writer (strict profile, default)

Allow:
- read/write `docs/`
- read `.serena/plans/` for requirements context

Deny:
- read/write `src/`
- read/write `test/` and `tests/`

## 6.5 Reviewer/Auditor permissions

Allow:
- read/search
- verification via non-shell tools and independent evidence review

Deny:
- implementation edits by default (can use dedicated fixer profile if needed)
- final integration commits

## 6.6 Interactive Agent permissions

Allow:
- broad read/search
- controlled edits for low-risk tasks
- standard local verification commands
- `bash` command surface (role exception to global `bash: deny`)

Deny:
- broad orchestration permissions by default
- unrestricted recursive delegation
- canonical integration actions reserved for Orchestrator in cycle-mode work

## 7. Git Ownership Policy

Recommended default:
- **Orchestrator owns canonical branch history**.
- Writers operate in isolated worktrees.
- Writers may optionally create local checkpoint commits for structure.
- Orchestrator integrates approved work via cherry-pick/squash and performs final commit.

Tradeoffs:

- Orchestrator-only commits:
  - Pros: clean authoritative history, centralized accountability.
  - Cons: higher orchestrator load.
- Writer commits everywhere:
  - Pros: autonomy, less orchestrator overhead.
  - Cons: inconsistent quality bars, harder policy enforcement.
- Worktree isolation:
  - Pros: safer parallelism, clearer ownership, reduced accidental overlap.
  - Cons: slightly higher operational complexity.

Additional recommendation:
- Combine worktree isolation with directory isolation for Source/Test writers to enforce true TDD boundaries.

## 8. Anti-Reward-Hacking Controls

- Require evidence packets for each claimed completion:
  - changed files
  - commands run
  - key outputs
  - unresolved risks
- Independent reviewer must re-grade against rubric.
- Orchestrator samples strong-model audits even when cheap model passes.
- Repeated low-quality completions trigger automatic model escalation.
- “No evidence, no done” policy.

## 9. Rubric Framework for Reviews

Each task gets rubric scores (example dimensions):
- Requirement coverage
- Correctness of behavior
- Safety/security impact
- Test adequacy
- Code clarity/maintainability
- Regression risk
- Evidence quality

Reviewer output must include:
- score by dimension
- blocking findings
- confidence level
- required remediation

## 10. Mapping to Repository Configuration

Policy for changes:

1. Add/modify shared permission behavior in top-level capability rule sets in `scripts/manage_permissions.py` (for example `BASH_CAP_*` blocks).
2. Define and compose baseline layers (`ALL_AGENTS_BASELINE`, `PURE_AGENTS_BASELINE`, `SUBAGENTS_BASELINE`, `TOP_LEVEL_AGENTS_BASELINE`).
3. Compose role profiles from capabilities + baseline layers.
4. Add path-isolated writer profiles (`src_writer_strict`, `test_writer_strict`, optional `docs_writer_strict`) and map agents by role.
5. Add an `interactive_general` profile for non-cycle interactive work.
6. Keep role-specific exceptions minimal, explicit, and justified.
7. Add agent-specific permission differences only when role-specific behavior cannot be represented by shared composition.
8. Apply profile updates using script workflow:

```bash
python3 scripts/manage_permissions.py --apply
python3 scripts/build_config.py
```

Do not rely on direct edits to generated permission blocks in `configs/agents/*.json`, `configs/subagents/*.json`, or compiled `opencode.json`.

## 11. Default Boundary Recommendations

- Keep Planner plan-focused and non-delegating.
- Make Orchestrator the delegation authority and integration authority.
- Disable `task`, `todoread`, and `todowrite` on subagents by default to prevent recursion; whitelist only dedicated coordinator subagents.
- Use Interactive agent profile for ad hoc work outside plan-orchestrator cycle.
- Force role separation:
  - Explorers cannot write.
  - Source Writers and Test Writers are mutually blind by default.
  - Writers cannot approve.
  - Reviewers cannot silently integrate.
- Prefer cheap/free subagents for low-risk high-volume work.
- Require strong-model gates for high-risk or ambiguous changes.

This structure balances cost, speed, and quality while reducing failure modes from both weak and strong agents.
