# Harness State Routing Decisions

`agent-memory` owns durable memory, planning, and artifact tracking. Native
harnesses still write their own memory, plan, task, and artifact files on disk.
Initialization therefore routes those native disk surfaces into the
`agent-memory` vault while preserving CLI/app compatibility.

Use native settings where the harness exposes them; otherwise preserve the
harness's expected path shape with symlinks.

## Normal Vault Shape

Use a native-compatibility area for harness-owned layouts, separate from typed
project memory/planning records:

```text
<agent-memory-vault>/
  harnesses/
    claude/
      plans/
      projects/<encoded-project>/memory/
    codex/
      memories/
      memories_extensions/
    agy/
      brain/
  projects/<project-id>/
    memories/
    plans/
    artifacts/
```

Native harness paths point at `harnesses/`. `agent-memory` project records live
under `projects/<project-id>/`. Do not put Codex sessions or archived sessions in
the vault.

## Claude Code

Source anchors:

- <https://code.claude.com/docs/en/memory>
- <https://code.claude.com/docs/en/settings>

Decisions:

- Use Claude's `autoMemoryDirectory` setting for auto memory routing. Point it
  at the vault-owned Claude project directory, so Claude writes its `memory/`
  child there.
- Treat `~/.claude/projects/<encoded-project>/memory/` as a compatibility and
  backfill path. The encoded project normally looks like the project root with
  slashes slugged into dashes.
- If the default Claude project memory directory already has files, move them
  into the corresponding vault directory and replace the original `memory/` path
  with a symlink so native recall still works.
- Use Claude's `plansDirectory` setting for plan routing. Point it at the
  vault-owned Claude plans directory.
- If `~/.claude/plans/` already has files, move them into the configured
  `plansDirectory` target, then remove the default path. Do not leave a
  `~/.claude/plans` compatibility symlink once `plansDirectory` is set.
- Do not decode, classify, or reorganize Claude plan filenames. Claude plans are
  dumped into the configured plans directory and referenced from there.

## Codex

Source anchors:

- <https://developers.openai.com/codex/memories>
- <https://developers.openai.com/codex/config-reference>
- <https://developers.openai.com/codex/learn/best-practices>
- <https://developers.openai.com/cookbook/articles/codex_exec_plans>
- <https://developers.openai.com/codex/guides/agents-md>
- <https://developers.openai.com/codex/environment-variables>

Decisions:

- Route `~/.codex/memories/` to the vault-owned Codex memories directory with a
  symlink.
- Route `$CODEX_HOME/memories_extensions/` to the vault-owned Codex memory
  extensions directory when Chronicle or other memory extensions are in use.
- Keep `~/.codex/sessions/` and `~/.codex/archived_sessions/` as normal Codex
  runtime directories outside the vault. Sessions are not the memory or plan
  store.
- Built-in Codex plan mode, `update_plan`, proposed plans, todo-list deltas, and
  plan implementation requests are protocol/thread state. Do not route them by
  moving or symlinking sessions.
- Durable Codex execution plans are Markdown artifacts. Route the Markdown plan
  files named by `PLANS.md`/`AGENTS.md` guidance into the agent-memory project
  plan directory. If a repo-local path is needed for compatibility, make it a
  pointer, template, or symlink to the vault-owned plan location.
- Current official config docs and local desktop runtime evidence did not expose
  a fixed `~/.codex/plans/` directory or a `plansDirectory`-style Codex setting.
  Do not invent one during initialization.
- Do not move all of `CODEX_HOME` for memory routing. That also moves auth,
  config, sessions, skills, logs, plugins, and other Codex state.

## Antigravity / `agy`

Source anchors:

- <https://antigravity.google/assets/docs/antigravity-2-0/artifacts.md>
- <https://antigravity.google/assets/docs/antigravity-2-0/implementation-plan.md>
- <https://antigravity.google/assets/docs/antigravity-2-0/artifact-review.md>
- <https://antigravity.google/assets/docs/cli/cli-artifacts.md>
- <https://antigravity.google/assets/docs/cli/cli-conversations.md>

Decisions:

- `agy` brain state is disk state, not user-owned planning prose. The observed
  native root is `~/.gemini/antigravity/brain/`.
- Preserve UUID task directory names, `task.md`, `implementation_plan.md`,
  `organizational_plan.md`, `walkthrough.md`, `*.metadata.json`, `.resolved*`
  markers, and media/browser artifact directories.
- Route the brain root or selected task directories into the vault-owned
  `harnesses/agy/brain/` compatibility area. Do not rename or flatten task
  directories.

## Adoption Procedure

For each harness route:

1. Confirm the project is a git repository and has an initialized
   `agent-memory` project directory.
2. Locate the native harness path for this project.
3. If that path already contains files, move them into the matching vault
   compatibility path before replacing anything.
4. Use the harness's native setting when one exists; otherwise use a symlink that
   preserves the exact path shape the harness expects.
5. Verify with the native harness that the same memories, plans, or artifacts are
   still visible.

Do not re-open settled alternatives during initialization. The initialization
task is to ensure this structure is present and working.
