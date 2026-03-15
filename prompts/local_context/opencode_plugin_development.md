<!-- AGENTS.md-OTP: X7K9-MNPR-QW42 -->

# OpenCode Plugin Development

This is the shared development guide for repos under `/home/dzack/opencode-plugins`.

- `AGENTS.md` tells you how to start and work.
- `REPO_AUDIT.md` tells you how to evaluate completed work.
- If guidance applies to every repo, keep it in one of those two docs. Package-local docs should describe package-specific behavior only.

## Orientation

- Each subdirectory is its own repo/package.
- The top-level `/home/dzack/opencode-plugins` repo stores shared policy/docs and is itself a git repo.
- `~/ai/opencode/plugins/` is a separate workspace. Do not change it from here unless the task is explicitly about that workspace.
- Many paths on this system are symlinks. Check file type before assuming two paths are different files.
- Never edit `~/ai/opencode/opencode.json` directly. The source of truth is `~/ai/opencode/configs/config_skeleton.json`; rebuild from `~/ai/opencode/` with `just rebuild`.

## Before Editing

- Work in the relevant repo. Use the top-level repo only for shared policy/docs.
- Checkpoint before every edit with `git add <file>` or a commit.
- Use the repo's lowercase `justfile`. Do not run test, typecheck, build, or publish commands directly if a `just` recipe exists.
- Run `direnv allow` when the repo has a local `.envrc`.
- Read the repo's `README.md` and local docs before changing behavior.
- Do not use destructive git commands such as `git checkout`, `git restore`, `git reset --hard`, or `git stash` in noisy repos.
- Keep one source of truth for repeated constants, config values, and shared policy text.

## Research and Tooling

- Use official docs first. For libraries/frameworks/APIs, use Context7 before guessing from CLI flags or source alone.
- Use `gh` for GitHub work, not github.com.
- Use `probe` for repo discovery and structural search.
- Load config-editing guidance before touching JSON or YAML.
- Use `command opencode` only when bypassing a shell alias matters.
- If a narrow search misses, broaden immediately before concluding anything is absent.

## OpenCode Workflow

- Resolve OpenCode from the user's PATH only. Do not add repo-local binary override knobs such as `OPENCODE_BIN`, `--opencode-bin`, or hardcoded `/home/.../opencode` paths.
- Use `command opencode` only for process-level checks such as `opencode agent list`, `opencode models`, and starting a repo-local `opencode serve`.
- Use `opencode-manager` as the workflow and proof harness. `opx` and `opx-session` are the canonical session surfaces.
- Do not use `opencode run` or interactive TUI output as proof.
- Do not scrape ANSI/TUI/stdout from interactive OpenCode sessions as evidence.
- If a workflow depends on repo-local config or env, start a repo-local `direnv exec . command opencode serve --hostname 127.0.0.1 --port <port>`.
- If a test must exclude user-global state, isolate `XDG_CONFIG_HOME`, `XDG_CACHE_HOME`, `XDG_STATE_HOME`, and `OPENCODE_TEST_HOME`.
- Do not use the shared/systemd `opencode serve` instance for repo-local workflow tests.

## Proof Design

- `passphrase`, `nonce`, `UUID token`, `OTP`, and similar labels are all witness tokens.
- A proof is valid only if the witness first becomes available on the exact path being proved.
- Description/schema witnesses prove visibility only.
- Execution, resume, and callback proofs must use a witness from tool output, a published report, or an external side effect that was unavailable beforehand.
- A fixed hidden witness can prove execution if it first appears only on the proved path and the test also checks transcript evidence, raw tool-use evidence, or an external side effect.
- A per-run claim such as liveness, fresh retrieval, or callback delivery needs a run-bound hidden witness.
- Never place an execution witness in prompts, system prompts, child-task prompts, or other pre-success model-visible text.
- No mocks, simulated success paths, or proofs that rely on assistant honesty.
- Strong evidence: raw tool-use data, `opx-session messages --json`, `opx debug trace`, transcripts, and external side effects. Weak evidence: assistant final text. Invalid evidence: scraped TUI or ANSI output.
- Prove the behavior manually once with `opx` / `opx-session`, then automate it.

## Repo Conventions

- `.envrc` must start with `source_up` and `dotenv_if_exists .env`. Tracked files must not contain live secrets.
- Package scripts and CI should delegate to `just --justfile justfile ...`.
- Package-local docs should stay package-local. Shared policy belongs here or in `REPO_AUDIT.md`.
- Use issues, PRs, commit messages, and Serena memory for tracking. Do not create top-level `GAPS.md`, `PLAN.md`, or similar work-log files.
- Prefer mature dependencies. Iterate on existing code instead of replacing whole files unless necessary.

## Negative Findings

When you searched and did not find something, report it in this format:

```text
- Searched: [specific sources, URLs, docs, commands run]
- Found: [what was or was not found]
- Conclusion: [labeled as inference — "I believe", "based on limited evidence"]
- Confidence: [High / Medium / Low]
- Gaps: [what remains unsearched]
```

- Never jump from "not found" to "does not exist".
