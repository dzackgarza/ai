---
name: project-initialization
description: "Use after cloning or switching to a repository for substantive work, or when it lacks a remote, QC hooks, a justfile, or memory."
---

# Project Initialization

This skill defines the normal form for projects on this machine. Use it before
substantive work that depends on shared project state so agents do not build on
half-initialized repositories,
stale branches, missing memory, or ad hoc QC.

The goal is not checklist theater. The goal is to make the project safe to work
in, then continue with the user's task.

## Trigger

Use this skill when repository-wide state can materially affect the requested work:

- before substantive feature or architectural implementation in an unfamiliar project;
- after cloning, creating, or switching to a project/worktree for such work;
- when requested work depends on `.agents/`, memory, [[justfile/SKILL|justfile]], hooks, CI, or QC
  surfaces that are missing or inconsistent;
- before work that will create or claim cross-session, multi-agent, public execution, or
  review state.

Do not use this skill for direct answers, read-only inspection, data labeling, narrow
research, one-off documentation or configuration edits, bounded scripts, direct commits,
or throwaway probes whose result does not depend on repository-wide state.
Repository presence alone is not a trigger.
If the work is bounded and reversible, default to the lighter route; ask only when the
classification changes the requested result or an irreversible action.

## Safety Rules

- Preserve user work. Do not overwrite dirty files, untracked artifacts, existing
  hooks, existing workflow files, or an existing [[justfile/SKILL|justfile]] without inspecting the
  current contents and explaining the migration.
- If git state is dirty, conflicted, diverged, or behind remote, load
  [[git-guidelines/SKILL|git-guidelines]] and resolve that state before feature work.
- Normalize by using the owning tool or scaffold, not by copying snippets from
  memory. Use [[agent-memory/SKILL|agent-memory]] for memory setup, [[justfile/SKILL|justfile]] for recipe design, and
  `~/ai-review-ci` for QC scaffolds/hooks/review workflows.
- If a project is intentionally tiny or non-code, record why a normal-form item is
  not applicable instead of forcing irrelevant infrastructure.

## Normal Form Checklist

### Git

Establish the repository boundary and freshness.

- Confirm you are inside a git repository:
  `git rev-parse --show-toplevel`.
- If there is no git root, stop project normalization until the intended project
  root is clear and a repository exists. Do not create `.agents/`, memory
  bindings, hooks, or QC scaffolds in an arbitrary directory.
- Check branch, dirty state, and untracked files:
  `git status --short --branch`.
- If a remote exists, fetch before judging freshness:
  `git fetch --quiet --prune --tags`.
- Confirm whether the current branch is up to date, ahead, behind, or diverged.
- If there is no remote, record that the confirmed git repo has no remote and
  skip freshness claims. Do not describe it as synced.

Do not pull, rebase, stash, discard, or initialize a repository in an ambiguous
directory without applying [[git-guidelines/SKILL|git-guidelines]].

### GitHub Public State

If the confirmed remote is GitHub-backed, establish the public execution graph before
treating local docs, plans, or transcripts as authoritative.

- Determine `<owner>/<repo>` from the remote.
- Check the wiki state. Use `references/github-wiki.md` for the exact wiki probes,
  first-page bootstrap behavior, and what belongs on the wiki versus GitHub execution
  surfaces.
- Inspect task-relevant open issue trees, sub-issues, dependencies, milestones, PRs,
  and draft PR claim maps. Search by the repo name, user-provided feature names,
  active branch, failing gate, and touched module when those terms exist.
- Treat the GitHub issue tree, sub-issue edges, blocker dependencies, GitHub Milestone
  scopes, linked PR claim maps, and review threads as canonical execution state. Wiki
  roadmap pages show the issue tree’s order. Local plans, `.agents` notes, memory records, transcripts, and
  scratchpads are leads unless the current GitHub surface confirms them.
- Before characterizing or normalizing an existing planning tree, load and read
  `plan/references/externalization.md`. You MUST read it before judging whether the tree
  is well-formed — whether a single root roadmap issue owns top-level order, whether nodes
  are story-shaped at their own altitude, whether milestones are scoped to subtree roots,
  and whether proof obligations live in the issue bodies. Do not call a tree well-formed or
  malformed from issue titles, labels, sub-issue edges, or milestone counts alone: that is
  structure, not conformance to the model. Treating structure as evidence of conformance is
  the failure this gate exists to prevent.
- Select the owning work-unit issue with itree. Use Spec Kit on that issue from the
  first planning stage. Consult `plan/references/externalization.md` when the work
  requires changes to the issue tree.
- When an observed failure class repeats, causes false green, blocks convergence, or
  requires human rescue, route it to the durable enforcement surface that owns it:
  wiki user stories or proof burdens for product obligations, issues/PR contracts for
  project work, skills for agent behavior, and fixtures or global QC gates for
  mechanically checkable rules.

Do not create GitHub issues, milestones, PRs, or wiki edits merely because they are
missing. Create or update them only when the user requested public tracking or the task
requires it; otherwise record the missing public surface as an initialization finding and
continue with the requested scope.

### Project Instructions

Load the repository's own instructions before editing.

- Read top-level `README*`, `AGENTS.md`, and nearby nested `AGENTS.md` files that
  govern the task path.
- Read the project constitution and the owning issue. Use Spec Kit for the plan
  and task list. Use [[agent-memory/SKILL|agent-memory]] for reusable knowledge.
- If instructions conflict, direct user instructions win; then prefer the most
  local repo instructions over broader AGENTS.md/global skill guidance.

### Native Spec Kit

For substantive feature work, use the installed Specify CLI and the shared
Frontier Simplify extension. In a project already initialized for Spec Kit:

```sh
specify extension list
specify extension add --dev ~/ai/spec-kit/extensions/frontier-simplify
```

Install only if absent; use the same native add command with `--force` to update
the shared extension when needed. For new projects, add
`--extension ~/ai/spec-kit/extensions/frontier-simplify` to `specify init`
with the appropriate agent integration. Do not reinitialize an existing feature.

Use `specify workflow run speckit --input spec="..."` for a complete new-feature
workflow when a supported agent integration is available. For work already
underway, follow the native skill for the current step and its configured hooks;
in a remote session, read and execute the installed hook command file directly
if there is no slash-command harness. The native artifact prerequisites still apply.
The shared `speckit-prerequisites` script only calls the upstream checker.
The extension owns the review instructions; no separate review workflow or
approval gate is needed.

### Durable Surface Convergence

When repo-local docs, scratchpads, plans, TODO files, or agent process notes already
exist, classify each one by durable owner before relying on it:

- current plan, task order, progress, and open obligations -> the owning itree issue, through Spec Kit;
- correction, trap, reusable decision, or durable agent behavior -> typed memory;
- durable project narrative, feature doctrine, architecture rationale, and readable
  roadmap/proof projections -> wiki;
- active user story, requirement, roadmap node, feature contract, proof burden,
  observed bug, inefficiency, gap, public handoff, or follow-up obligation -> GitHub
  issue tree, milestone, or PR claim map;
- private diagnostic recipe, hook helper, or guardrail script -> `.agents/`;
- temporary investigation notes -> delete before handoff or keep only as an explicitly
  non-authoritative scratchpad.

Do not normalize by copying the same content into every surface.
Promote the durable content to its owner, replace local residue with links when a pointer
is useful, and continue the user's task from the authoritative surface.

### `.agents/`

Every normal project root has a `.agents/` directory for agent-facing material.
This surface is not user-facing.

Expected contents, when applicable:

- `.agents/justfile` for private agent recipes, all marked `[private]`;
- small scripts used by those private recipes;
- no loose durable process docs that should be typed project memories instead.

[[agent-memory/SKILL|agent-memory]] binds the checkout by linking `.agents` and
`.hermes` to the vault-owned project directory. Use its initializer to create the links.

Create `.agents/` only when you know the project root. Do not scatter agent
artifacts in source directories.

### Agent Memory

Check the project memory binding during initialization.

- Load [[agent-memory/SKILL|agent-memory]] for the current command surface.
- Use the GitHub `uvx` runner to check memory tooling unless a verified setup has
  already placed [[agent-memory/SKILL|agent-memory]] on `PATH`:
  `uvx --python 3.14 --from git+https://github.com/dzackgarza/agent-memory agent-memory --help`,
  then `uvx --python 3.14 --from git+https://github.com/dzackgarza/agent-memory agent-memory doctor`.
  If either exits before showing help because a required runtime dependency is
  missing, treat that as setup failure and use the [[agent-memory/SKILL|agent-memory]] skill plus the
  `/home/dzack/gitclones/agent-memory` checkout to provision dependencies.
- Confirm that `.agents` and `.hermes` resolve to the project directory in the vault.
  To initialize a checkout for reusable memories, run
  `uvx --python 3.14 --from git+https://github.com/dzackgarza/agent-memory agent-memory init project --vault <vault>`,
  then `uvx --python 3.14 --from git+https://github.com/dzackgarza/agent-memory agent-memory doctor`.
- Confirm the bound project directory exists under the configured vault. A repo
  binding without a vault-side project directory is not initialized.
- Confirm native harness routes are in place according to
  `opencode/skills/agent-memory/references/harness-state-hijacking-research.md`:
  - Claude Code auto memory writes into the vault-owned Claude project
    directory.
  - [[codex/SKILL|Codex]] memories and memory extensions are routed into the vault, while
    `~/.codex/sessions/` and `~/.codex/archived_sessions/` remain normal [[codex/SKILL|Codex]]
    runtime directories outside the vault.
  - Agent instructions direct planning to the selected itree issue and its Spec Kit
    stages. Correct instructions that direct a harness to maintain another plan.
  - Antigravity/`agy` brain artifacts, when used for the project, preserve their
    native directory names and metadata while landing under the vault-owned
    compatibility area.
- Before implementation, search project/global memories for terms from the user
  task, repo name, active module, branch, and recent failure mode.
- Treat memories as leads. Verify drift-prone facts against the current repo
  before acting.
- If no relevant memory exists, say that briefly in the initialization stamp and
  continue.

### Justfile

The top-level [[justfile/SKILL|justfile]] is the project API.

- Load the [[justfile/SKILL|justfile]] skill before creating or changing recipes.
- Run `just --list` to understand the public surface.
- Public recipes should be small and user-facing: usually `build`, `test`,
  `test-ci` under global QC, `serve`, `run`, `setup`, or `clean` when genuinely
  useful.
- Internal diagnostics, slop checks, hook helpers, and anti-gaming surfaces belong
  in `.agents/justfile` as `[private]` recipes.
- If a global-QC project has no usable [[justfile/SKILL|justfile]], install or adapt the
  appropriate `~/ai-review-ci` scaffold instead of hand-writing copied snippets.

For central [[justfile/SKILL|justfile]] delegation, preserve the caller repository root with `-d .`
so the shared QC scans the target project, not `~/ai-review-ci`.

### Global QC And Review CI

`~/ai-review-ci` owns standard QC, hooks, and review workflows. Downstream repos
should stay thin.

Normal global-QC shape:

- top-level [[justfile/SKILL|justfile]] delegates public `test` and `test-ci` to the relevant
  `~/ai-review-ci/justfiles/<language>.just` with caller-root semantics;
- target repos do not copy generic QC configs, tool pins, hook scripts, or
  replacement lint/type/test stacks;
- repo-local project checks are private recipes composed after the global gate;
- hooks are installed either globally (`just install-global-hooks` from
  `~/ai-review-ci`) or repo-locally (`just install-repo-hooks <repo>`), depending
  on the project need;
- GitHub review workflows are installed through the `ai-review-ci` installer and
  remain thin repo-owned trigger configuration.

For a new project, prefer:

```bash
cd ~/ai-review-ci
just install-qc-scaffold <language> /path/to/project
uvx --from git+https://github.com/dzackgarza/ai-review-ci ai-review-ci install
```

Then verify from the target project:

```bash
just --list
just test
```

Run `just test-ci` when preparing push/CI or when the user's task requires the
full push-tier gate.

### Environment

If the project uses `direnv`, `.envrc`, toolchains, or local services, establish
that state before debugging product behavior.

- Do not invent missing secrets, remotes, service URLs, or local config.
- Hard-fail required env/auth/config inputs when the project requires them.
- Use [[tool-provisioning-and-environment-hygiene/SKILL|tool-provisioning-and-environment-hygiene]] for missing tools or install
  pathways.

## Mixed-State Normalization

When a project is partly initialized, normalize only the state that overlaps or blocks
the requested feature work. Preserve unrelated mixed state and continue within the
requested boundary unless the user asks for broader normalization.

Prefer this order:

1. Stabilize git state and freshness.
2. Inspect GitHub public state when the remote is GitHub-backed.
3. Classify local docs, plans, TODOs, and scratchpads by durable owner.
4. Load repo instructions and task-relevant memories.
6. Initialize or repair `.agents/` and memory binding.
7. Normalize [[justfile/SKILL|justfile]] public/private surfaces.
8. Delegate QC to `~/ai-review-ci` and install hooks/workflows where appropriate.
9. Run the smallest proof that the normalized surface works.
10. Continue the user's original task.

If normalization itself is nontrivial, make it a visible subtask and stop before
risky migrations. Do not silently turn a feature request into a broad repo
rewrite.

## Initialization Stamp

Before moving into implementation that actually required this skill, record a compact
status:

```markdown
Project initialization:
- Git: <root, branch, dirty/freshness/remote status>
- GitHub: <wiki state, relevant issues/milestones/PRs, canonical tracker or gap>
- Instructions: <README/AGENTS/memory surfaces checked>
- Memory: <initialized? relevant memories searched?>
- Durable state: <local docs/plans classified? migrations or pointers needed?>
- Justfile: <present? public surface? global-QC delegation?>
- QC/hooks/CI: <ai-review-ci scaffold/hooks/workflows status>
- Blockers or normalization done: <none / list>
```

Keep the stamp short. If everything is normal, one paragraph is enough.

## Reference Files

- `references/github-wiki.md`: wiki probes, first-page bootstrap, and what belongs on
  the wiki (user-story-first doctrine, proof burdens, roadmaps) versus GitHub execution
  surfaces.
- `references/durable-state-surfaces.md`: the one-owner state model (vault, GitHub
  execution surfaces, wiki, `.agents/`, scratch) and the mixed-state migration rules.
- `references/agents-directory.md`: the `.agents/` directory contract and the private
  agent-facing justfile pattern.
