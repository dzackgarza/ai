# Repo Audit

This is the post-hoc audit rubric for repos under `/home/dzack/opencode-plugins`.

Use it after implementation and before pushing or opening a PR. Record findings in task output, PR review, commit messages, or GitHub issues. Do not maintain a separate top-level `GAPS.md` or shadow audit doc.

If a rule is not relevant to the repo type, mark it `N/A` explicitly instead of silently skipping it.

For setup and development workflow, use `GUIDE.md`. For basic OpenCode CLI and manager
command forms, use `opencode-cli/SKILL.md`. For callback and delayed-delivery workflow
patterns, use `opencode-cli/async-injection.md`.

## Audit Method

- Inspect real files, configs, commands, transcripts, and test code. Do not audit from memory.
- For negative findings, cite the exact file, command, or evidence surface.
- When the claim concerns OpenCode behavior, inspect `opx transcript --json`, `opx debug trace`, transcript output, or an external side effect. Do not rely on scraped TUI output.
- Shared top-level policy docs may refer to canonical local workspace paths. Package repos must not commit user-specific runtime paths as part of their normal behavior, config, or examples.

## Shared Policy Surface

- Shared policy lives only in top-level `AGENTS.md` and `REPO_AUDIT.md`, both sourced from this skill.
- Package-local docs are package-specific and do not restate shared policy unless the package has a real exception.
- No stray top-level debug guides, gap trackers, audit shadows, or work-log docs.

## CLI-First Architecture

- Plugin repos expose a standalone Typer CLI as the primary product surface unless the repo is explicitly an internal helper or a non-plugin CLI package.
- The CLI is usable without OpenCode loaded and owns the canonical behavior, validation, and output contract.
- Plugin code is thin and limited to OpenCode-only concerns such as session wiring, hooks, permissions, metadata, and event publication.
- MCP wrappers, where present, delegate to the same CLI or shared library as the plugin. They do not carry a second implementation.
- Hook-only plugins still provide an independent CLI for the underlying transform, match, schedule, render, or indexing behavior.
- CLI help is progressive-disclosure oriented: top-level help, subcommand help, and setup guidance are present and readable.
- Missing credentials, databases, or external services fail with explicit setup messages that identify the missing prerequisite and the expected global env/config source.
- If a repo claims an exception to the CLI-first rule, the exception is documented explicitly and audited as `N/A` with rationale.

## Repo Hygiene

- No committed secrets, tokens, keys, or passwords in tracked files.
- No development debris such as `.serena/`, `__pycache__/`, scratch logs, temp dirs, or giant debug dumps.
- No package repo commits user-specific absolute runtime paths such as `/home/...`, `~/...`, or hardcoded local binary paths.
- Integration tests and plugins use centralized relative path resolution (e.g. `cliPath()` helper) instead of `process.cwd()` or hardcoded string paths.
- Repeated constants and config values have one source of truth.

## Config and Environment

- `.envrc` starts with `source_up` and `source /home/dzack/opencode-plugins/.testrc` (or equivalent absolute path) and `dotenv_if_exists .env` when the repo has a local `.envrc`.
- Tracked `.envrc` files contain placeholders or documented exports only, never live secret values.
- Environment variables used by the repo are documented in `.envrc` and in the package README when humans need to set them.
- If the repo runs OpenCode directly, it inherits isolation from `.testrc`. It does not override `OPENCODE_CONFIG` or XDG variables in its local `.envrc`.
- Fixed witness tokens, if used, come from env. They are never hardcoded in test source.
- `.config/` files and plugin symlinks avoid user-specific absolute paths when a relative path or repo-local path works.

## Automation

- The canonical automation entrypoint is lowercase `justfile`. No `Justfile`.
- The repo exposes the expected `just` recipes for its type, including `install`, `typecheck`, `test`, and `check`.
- Release/bump recipes exist where the repo is meant to publish.
- The `test` recipe clears `${XDG_CACHE_HOME:-$HOME/.cache}/opencode` before running.
- Package scripts and CI delegate to `just --justfile justfile ...` instead of calling raw `bun test`, `tsc`, `pytest`, or similar validation commands directly.
- Pre-commit hooks, if present, run `just check` rather than raw test commands.

## OpenCode Workflow

- The OpenCode binary is resolved from PATH only. No `OPENCODE_BIN`, `--opencode-bin`, or hardcoded binary fallbacks.
- `command opencode` appears only for process-level checks such as `opencode agent list`, `opencode models`, and starting a repo-local `opencode serve`.
- `opencode-manager` is the workflow and proof harness for real session tests. Use the
  public `opx` subcommands such as `one-shot`, `begin-session`, `chat`, `system`,
  `transcript`, `final`, and `delete`.
- `opx transcript --json` is the only approved transcript renderer or parser. No
  `opencode export` plus shell-filter fallback recipes appear in repo docs, tests, or
  helper scripts. If the manager surface is insufficient, the follow-up is an issue, not
  a fallback parser.
- No test uses `opencode run` or scraped interactive output as proof of workflow behavior.
- Manager package references use `git+https://...` or an npm slug, never `git+ssh://...`.
- Repo-local workflow tests use a repo-local custom-port `command opencode serve` when the behavior depends on repo-local config or env.
- If the test must exclude user-global OpenCode state, it isolates `XDG_CONFIG_HOME`, `XDG_CACHE_HOME`, `XDG_STATE_HOME`, and `OPENCODE_TEST_HOME`.
- No repo-local test depends on the shared/systemd `opencode serve` instance.

## Witness and Proof Rules

- `passphrase`, `nonce`, `UUID token`, `OTP`, and similar labels are all witness tokens.
- A proof is valid only if the witness first becomes available on the exact path being proved.
- Description/schema witnesses prove visibility only.
- Execution, resume, and callback proofs require a witness from tool output, a published report, or an external side effect that was unavailable beforehand.
- A fixed hidden witness can prove execution if it first appears only on the proved path and the test also checks transcript evidence, raw tool-use evidence, or an external side effect.
- A per-run claim such as liveness, fresh retrieval, or callback delivery requires a run-bound hidden witness.
- Execution witnesses never appear in prompts, system prompts, child-task prompts, or other pre-success model-visible text.
- The proof cannot depend on child-agent obedience, assistant honesty, or the model paraphrasing a hidden value.

## Integration Test Checks

- No mocks, monkeypatches, stubs, fake OpenCode sessions, or simulated provider behavior in integration tests.
- Integration tests create isolated runtimes with temp `XDG_CONFIG_HOME`, `XDG_CACHE_HOME`, and `XDG_STATE_HOME`. Add `OPENCODE_TEST_HOME` when global `.opencode` discovery must be suppressed.
- Tests use OS-assigned free ports rather than hardcoded port ranges.
- When local config/env matters, tests launch a repo-local custom-port `command opencode serve` inside `direnv`.
- Tests assert more than assistant final text. Valid evidence includes raw tool-use
  records, manager transcripts, debug trace output, or external side effects.
- If a test claims execution, it proves the relevant tool/report/effect actually happened.
- If a test claims a per-run property, it uses a run-bound hidden witness.
- If a fixed witness is used, it is read from env and never hardcoded.

## TypeScript Plugin Checks

- `package.json` declares the correct package name, semantic version, module entrypoint, and publish surface.
- `package.json` includes `"type": "module"`, an `"exports"` entry, and `"files"` when the package is meant to publish source directly.
- `package.json` scripts delegate to `just --justfile justfile ...`.
- TypeScript plugin repos do not hide the product behind `src/index.ts` alone; the repo also documents and ships the canonical standalone CLI path.
- `tsconfig.json` is strict and includes `noUnusedLocals`, `noUnusedParameters`, `noImplicitReturns`, `allowImportingTsExtensions`, `noEmit`, and lowercase `"moduleResolution": "bundler"` where relevant.
- `src/index.ts` exports the canonical plugin factory.
- `src/index.ts` stays adapter-sized. Core storage, parsing, fetch, reporting, and validation logic lives outside the OpenCode wrapper.
- Tool descriptions start with `Use when...` and avoid implementation leakage.

## Python and MCP Checks

- Python repos use `uv` with declared dependencies in `pyproject.toml`.
- Python-backed plugin repos expose the standalone CLI through Typer with documented commands or subcommands.
- The repository is a single Python package with `pyproject.toml` at the root. No separate `mcp-server/` directory.
- The MCP server is exposed as an `mcp` subcommand of the core CLI.
- The `uvx` command works directly against the repository URL (no-install mandate).
- No repo relies on ad hoc `pip install` or unmanaged local Python state.
- MCP wrappers reuse shared bridge code such as `mcp-shim` when that is the intended architecture.

## README and Human-Facing Docs

- The package README explains what the repo does, how to install or run the standalone CLI, and how to validate it.
- The package README documents required environment variables, defaults, and what they control.
- The README leads with the independent CLI and its examples. OpenCode plugin registration or MCP registration is secondary.
- Tooling repos document tool names, input shape, and representative output or evidence surfaces.
- Remote usage examples prefer `uvx` or `npx` when the package supports them.
- Remote usage examples use repo URLs or package names, not user-specific local paths.
- Human-facing docs stay informational. They do not become work logs or changelogs.

## Audit Output

When the audit finds a problem, record:

- The exact file or command surface
- The violated rule from this rubric
- The evidence that proves the violation
- The required fix or follow-up

When the audit finds nothing, say so explicitly and list any remaining unreviewed surfaces.
