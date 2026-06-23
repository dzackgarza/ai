---
name: project-initialization
description: >-
  Use at the start of work in any repository, after cloning or switching projects,
  or when a project appears partially set up. Establishes the normal project form:
  git/remote freshness, GitHub public state, durable surface ownership, SDL-MCP
  registration/indexing, .agents, agent-memory, justfile, ai-review-ci QC/hooks/CI,
  and task-relevant memory lookup before implementation.
---

# Project Initialization

This skill defines the normal form for projects on this machine. Use it before
substantive project work so agents do not build on half-initialized repositories,
stale branches, missing memory, or ad hoc QC.

The goal is not checklist theater. The goal is to make the project safe to work
in, then continue with the user's task.

## Trigger

Use this skill:

- at the start of a session in a repository;
- after cloning, creating, or switching to a project/worktree;
- when `.agents/`, memory, `justfile`, hooks, CI, or QC surfaces are missing or
  inconsistent;
- before implementing work in a repo whose state has not been established in the
  current session.

Skip only for trivial one-command answers outside a project, or when the user
explicitly asks you not to inspect or normalize project state.

## Safety Rules

- Preserve user work. Do not overwrite dirty files, untracked artifacts, existing
  hooks, existing workflow files, or an existing `justfile` without inspecting the
  current contents and explaining the migration.
- If git state is dirty, conflicted, diverged, or behind remote, load
  `git-guidelines` and resolve that state before feature work.
- Normalize by using the owning tool or scaffold, not by copying snippets from
  memory. Use `agent-memory` for memory setup, `justfile` for recipe design, and
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
directory without applying `git-guidelines`.

### GitHub Public State

If the confirmed remote is GitHub-backed, establish the public execution graph before
treating local docs, plans, or transcripts as authoritative.

- Determine `<owner>/<repo>` from the remote.
- Check the wiki state. Use the GitHub Wiki section of the active `AGENTS.md`
  guidance for the exact wiki probes and first-page bootstrap behavior.
- Inspect task-relevant open milestones, issues, PRs, and draft PRs. Search by the
  repo name, user-provided feature names, active branch, failing gate, and touched
  module when those terms exist.
- Treat linked milestones, controlling issues, child issues, PR contracts, and review
  threads as canonical execution state. Local plans, `.agents` notes, memory records,
  transcripts, and scratchpads are leads unless the current GitHub surface confirms
  them.
- For long-horizon, cross-repo, or review-track work, externalize finalized plans into
  a GitHub issue tree, milestone, or draft PR using `creating-implementation-plans` and
  `git-guidelines`. Once public artifacts exist, they become the tracker; local plans
  may explain derivation but must not stay authoritative.
- When an observed failure class repeats, causes false green, blocks convergence, or
  requires human rescue, route it to the durable enforcement surface that owns it:
  wiki user stories or proof burdens for product obligations, issues/PR contracts for
  project work, skills for agent behavior, and fixtures or global QC gates for
  mechanically checkable rules.

Do not create GitHub issues, milestones, PRs, or wiki edits merely because they are
missing. Create or update them only when the user requested public tracking or the task
requires it; otherwise record the missing public surface as an initialization finding and
continue with the requested scope.

### SDL-MCP

If the client exposes SDL-MCP, or repo instructions require it, make the repository
available to SDL before broad code exploration or edits.

- Check `repo.status` for the repository id you expect to use.
- If `repo.status` reports that the repository is not registered, run
  `repo.register` with the confirmed git root and a stable repo id, then run
  `index.refresh` in `full` mode.
- If `repo.status` reports stale or missing indexed state and the task depends on
  current code, run `index.refresh` in `incremental` mode. Do not refresh by habit.
- If refresh runs asynchronously, poll `repo.status` until the index is ready before
  relying on graph-backed retrieval.
- Once registered/current, start task context with `sdl.context` using `precise` or
  `broad` mode according to the task.

If SDL-MCP is unavailable, record that in the initialization stamp and use the
repository's documented fallback path. In repos that ship `SDL.md`, treat it as the
fallback workflow when the client cannot load the SDL-MCP skill.

### Project Instructions

Load the repository's own instructions before editing.

- Read top-level `README*`, `AGENTS.md`, and nearby nested `AGENTS.md` files that
  govern the task path.
- If the repo has design docs or an `agent-memory` pointer, inspect them before
  inventing a workflow. Planning state belongs in `agent-memory`, not loose
  repo-local planning files.
- If instructions conflict, direct user instructions win; then prefer the most
  local repo instructions over broader AGENTSmd/global skill guidance.

### Durable Surface Convergence

When repo-local docs, scratchpads, plans, TODO files, or agent process notes already
exist, classify each one by durable owner before relying on it:

- plan, phase state, queue, or residue ledger -> `agent-memory` plan record;
- correction, trap, reusable decision, or durable agent behavior -> typed memory;
- user story, requirement, roadmap, feature doctrine, proof burden, or architecture
  rationale -> wiki;
- observed bug, inefficiency, gap, public handoff, or follow-up obligation -> GitHub
  issue, milestone, or PR;
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

Project memory binding is not a `.agents/` child. `agent-memory` owns the binding
through `.agent-memory.toml` at the repository root. Do not create or maintain
memory directories by hand.

Create `.agents/` only when you know the project root. Do not scatter agent
artifacts in source directories.

### Agent Memory

Project memory and planning state are part of initialization, not an
afterthought. The goal is to confirm the normal structure exists and repair it
when it is missing.

- Load `agent-memory` for the current command surface.
- Use the GitHub `uvx` runner to check memory tooling unless a verified setup has
  already placed `agent-memory` on `PATH`:
  `uvx --python 3.14 --from git+https://github.com/dzackgarza/agent-memory agent-memory --help`,
  then `uvx --python 3.14 --from git+https://github.com/dzackgarza/agent-memory agent-memory doctor`.
  If either exits before showing help because a required runtime dependency is
  missing, treat that as setup failure and use the `agent-memory` skill plus the
  `/home/dzack/gitclones/agent-memory` checkout to provision dependencies.
- Confirm the repository has a root `.agent-memory.toml` binding. If it is
  missing and the project should keep memory/planning state, run
  `uvx --python 3.14 --from git+https://github.com/dzackgarza/agent-memory agent-memory init project --vault <vault>`,
  then `uvx --python 3.14 --from git+https://github.com/dzackgarza/agent-memory agent-memory doctor`.
- Confirm the bound project directory exists under the configured vault. A repo
  binding without a vault-side project directory is not initialized.
- Confirm native harness routes are in place according to
  `opencode/skills/agent-memory/references/harness-state-hijacking-research.md`:
  - Claude Code auto memory writes into the vault-owned Claude project
    directory, and Claude plans use `plansDirectory` pointed at the vault.
  - Codex memories and memory extensions are routed into the vault, while
    `~/.codex/sessions/` and `~/.codex/archived_sessions/` remain normal Codex
    runtime directories outside the vault.
  - Durable Codex ExecPlan Markdown files resolve to the agent-memory project
    plan directory through `PLANS.md`/`AGENTS.md` guidance or a compatibility
    pointer/symlink.
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

The top-level `justfile` is the project API.

- Load the `justfile` skill before creating or changing recipes.
- Run `just --list` to understand the public surface.
- Public recipes should be small and user-facing: usually `build`, `test`,
  `test-ci` under global QC, `serve`, `run`, `setup`, or `clean` when genuinely
  useful.
- Internal diagnostics, slop checks, hook helpers, and anti-gaming surfaces belong
  in `.agents/justfile` as `[private]` recipes.
- If a global-QC project has no usable `justfile`, install or adapt the
  appropriate `~/ai-review-ci` scaffold instead of hand-writing copied snippets.

For central justfile delegation, preserve the caller repository root with `-d .`
so the shared QC scans the target project, not `~/ai-review-ci`.

### Global QC And Review CI

`~/ai-review-ci` owns standard QC, hooks, and review workflows. Downstream repos
should stay thin.

Normal global-QC shape:

- top-level `justfile` delegates public `test` and `test-ci` to the relevant
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
- Use `tool-provisioning-and-environment-hygiene` for missing tools or install
  pathways.

## Mixed-State Normalization

When a project is partly initialized, normalize before feature work unless the
user explicitly requested only an audit or diagnosis.

Prefer this order:

1. Stabilize git state and freshness.
2. Inspect GitHub public state when the remote is GitHub-backed.
3. Classify local docs, plans, TODOs, and scratchpads by durable owner.
4. Register or refresh SDL-MCP context if available/required.
5. Load repo instructions and task-relevant memories.
6. Initialize or repair `.agents/` and memory binding.
7. Normalize `justfile` public/private surfaces.
8. Delegate QC to `~/ai-review-ci` and install hooks/workflows where appropriate.
9. Run the smallest proof that the normalized surface works.
10. Continue the user's original task.

If normalization itself is nontrivial, make it a visible subtask and stop before
risky migrations. Do not silently turn a feature request into a broad repo
rewrite.

## Initialization Stamp

Before moving into implementation, record a compact status:

```markdown
Project initialization:
- Git: <root, branch, dirty/freshness/remote status>
- GitHub: <wiki state, relevant issues/milestones/PRs, canonical tracker or gap>
- SDL-MCP: <registered/current/unavailable/not applicable>
- Instructions: <README/AGENTS/memory surfaces checked>
- Memory: <initialized? relevant memories searched?>
- Durable state: <local docs/plans classified? migrations or pointers needed?>
- Justfile: <present? public surface? global-QC delegation?>
- QC/hooks/CI: <ai-review-ci scaffold/hooks/workflows status>
- Blockers or normalization done: <none / list>
```

Keep the stamp short. If everything is normal, one paragraph is enough.
