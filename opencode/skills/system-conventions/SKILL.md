---
name: system-conventions
description: Use when choosing a config format, task runner, UI stack, package manager, or storage location; provisioning tools or dependencies; handling secrets or environment variables; selecting CLI tools for search, rename, or codemods; running long-lived commands; or migrating documentation between surfaces. Canonical problem-to-convention map for this system.
---
# System Conventions

Environment-wide conventions for this machine and its repos. Follow these by default;
deviate only with explicit user approval.

## Environment

- **Read all READMEs and AGENTS.md files** encountered.

- There are many symlinks on this system; check the file type if you find confusing
  duplication. Reusable agent-facing prompts live in the `ai-prompts` repo and are
  consumed by slug; `~/ai/prompts` is reserved for `local_context` overlays and
  repo-specific guidance.

- The `ai` project (`~/ai`) is a centralized configuration hub for AI agent harnesses
  (Claude Code, Gemini CLI, etc.), using Markdown for prompts and YAML/JSON for config.
  Key directories include AGENTS.md, skills/, and opencode/.

- Review CI is owned by `dzackgarza/ai-review-ci`; consuming repos carry only the
  `.github/workflows/review-{general,slop,pr}.yml` trigger files. Edit schedules,
  thresholds, and `with:` inputs in the consuming repo; edit review behavior upstream.
  Load [[policy-index/SKILL|policy-index]], [[anti-slop/SKILL|anti-slop]], or
  [[reviewing-llm-code/SKILL|reviewing-llm-code]] for behavior changes.

## Secrets and Environment Variables

- Never store or use local secrets or inline them into any shell commands.
  They must be stored in `~/.envrc`, trusted with `direnv allow`, and all projects
  should have a `.envrc` file that either sources `~/.envrc` directly or uses the
  `source_up` directive.

  - Project-local envrc files should be tracked via git, and thus never store true
    secrets, only env vars. If a project truly needs a local secret (rare), it should
    be in a gitignored `.env` file and the envrc file should source it.

- **Never** set env vars inline in shell commands (e.g., `MYSECRET=123 some_command`) —
  these are visible in the process list. Use env files or exports instead.

## Automation and Dependencies

- All project automation routes through `just`: always look for an existing justfile
  and use its recipes, and never run tests, type-checking, builds, publishing, or other
  workflows manually when a recipe exists. Load [[justfile/SKILL|justfile]] when working
  with justfiles or project tasks.

- Dependencies between projects should be routed through GitHub and use `uvx`/`npx -y`
  calls when possible, or explicitly declared as dependencies.
  Load [[tool-provisioning-and-environment-hygiene/SKILL|tool-provisioning-and-environment-hygiene]]
  before provisioning tools or dependencies. Do not tie across file system boundaries
  unless absolutely necessary.

- **Before editing any JSON or YAML file: load [[config-file-editing/SKILL|config-file-editing]].**
  Never raw-edit config files.

## Storage Locations

- PDF storage is managed in `~/pdf-extraction` with justfile recipes for extraction and
  conversion. Load [[reading-pdfs/SKILL|reading-pdfs]] before PDF extraction or
  conversion work.

- PDFs are stored in `~/pdfs` and should be organized into library-like subfolder trees.

## Standard Conventions Map

Problem → canonical system convention.

| Problem | Convention |
|---------|-----------|
| Bespoke config format choice | **TOML.** All bespoke project configs are TOML, parsed with a real TOML parser — never hand-rolled INI/regex parsing, never JSON/YAML for new bespoke configs. Use Python's `tomllib` (read) or `tomli-w`/`tomlkit` (write). |
| Config file location | **XDG-compliant paths.** Configs live under `~/.config/<app>/`, not as sidecar files attached to repos (which are just clutter). |
| Task runner | **justfile** ([[justfile/SKILL|justfile]] skill). Never Makefiles, `npm run`, `bun run`, or other ad-hoc runners unless absolutely required by an external constraint — and even then minimize their use so as not to confuse the single-runner convention. |
| Interactive wizards / prompts | **gum.** Any interactive CLI prompt, confirmation, selection, spinner, or wizard — use `gum`. |
| Search / filtering UX | **fzf.** Fuzzy search and interactive filtering of any list. |
| User-facing desktop menus | **dmenu / rofi.** Launchers, quick-select menus, and desktop-issued prompts. |
| Desktop widgets | **ags.** Bars, panels, system tray, and persistent desktop widgets. |
| JS-based projects | **bun.** Runtime and package execution for any JavaScript/TypeScript project. |
| JS dependency management | **pnpm.** Never `npm`. Install deps and run scripts via `pnpm`. |
| Nontrivial CLIs | **Python** ([[writing-scripts-and-cli-interfaces/SKILL|writing-scripts-and-cli-interfaces]] skill). Build command-line tools in Python, not shell, once the task outgrows a one-liner. |
| Memory | **agent-memory** ([[agent-memory/SKILL|agent-memory]] skill). Durable knowledge, plans, and project state live in the central vault. |
| Plans | **agent-memory** ([[agent-memory/SKILL|agent-memory]] skill). Always file plans as `plan` records with agent-memory, never as loose repo-local markdown. |
| System-wide search | **locate** (or `kpsewhich` for TeX), not `rg ~`-style filesystem crawls. Use the right index for the domain. |
| Mathematical calculations | **Prefer symbolic and semantic.** `sage`, `sympy`, GAP, Julia, Macaulay2, Singular — not naive float arithmetic. |
| Web UIs | **Vite + Svelte/React + Tailwind.** Never hand-roll HTML or CSS; use the framework's component and styling system. |
| Desktop UIs | **Tauri** ([[developing-linux-guis/SKILL|developing-linux-guis]] skill). Never Qt, Electron, or other heavy GUI frameworks. |
| Markdown parsing | **Pandoc CLI or package, use the AST.** Always semantic parsing, never regex. Embedded Pandoc + custom filters highly preferable to hand-rolled scraping solutions. |
| LaTeX parsing | **Pandoc AST, plastex.** Semantic parsing, never regex-based extraction. |
| Linters / type-checkers / autoformatters | **Always integrated in upstream QC.** Use locally and then push upstream. Prefer always-on, opinionated autoformatters and always use autofix flags. |
| Autoformatting markdown | **Flowmark fork.** Use the flowmark fork for semantic markdown autoformatting. |
| PDF parsing | **reading-pdfs** ([[reading-pdfs/SKILL|reading-pdfs]] skill). Use Mistral OCR API as primary extraction; MinerU for local structured extraction. Never hand-rolled PDF scraping. |
| Finding papers | **Local Zotero search first** ([[zotero/SKILL|zotero]] skill), which has markdown extractions — cite by BibTeX key. arxiv ([[arxiv/SKILL|arxiv]] skill) second, cite by URL. |
| APIs | **OpenAPI spec.** Always describe APIs with an OpenAPI specification. |
| Compliance, provenance, governance, release-identity machinery | **Minimal mechanism only.** Load [[policy-index/SKILL\|policy-index]] (`POLICY.NO_COMPLIANCE_MAXIMALISM`) before adding any hash, provenance manifest, release-identity chain, certification ledger, or programme-completion record. Calibrate to a single-maintainer personal research tool unless the user explicitly specifies a larger operational model. The diagnostic catalog is [[llm-failure-modes/coding-failures\|llm-failure-modes #25]]. |
| Greenfield is never greenfield | **Find 3–5 strong, vetted reference implementations first** ([[known-solution-first/SKILL\|known-solution-first]] skill). Borrow liberally — not as dependencies, but as a way to understand patterns in code that has already solved the problems. Never implement from scratch without first finding prior art. |

## CLI Tool Routing

Prefer tool-routing skills over memorized commands:

- Memory and agent-facing documentation: [[agent-memory/SKILL|agent-memory]]
- GitHub, `gh`, commits, PRs, issues, deletion: [[git-guidelines/SKILL|git-guidelines]]
- Project automation and command discovery: [[justfile/SKILL|justfile]]
- Local structure and debugging surfaces: [[reality-grounded-debugging/SKILL|reality-grounded-debugging]]
- External docs, Context7, DeepWiki, package/API/compiler/provider errors:
  [[known-solution-first/SKILL|known-solution-first]]
- Name/text discovery: `rg` and `fd`
- Semantic narrowing after broad discovery: `probe`
- Structural search and syntax-aware rewrites: `ast-grep`
- Workspace symbols/references/rename when the language server is known-good: `lsp-cli`
- Language-specific semantic rename: `gorename`, `clang-rename`, `ts-morph`, `rope`,
  or OpenRewrite
- Repeatable JavaScript/TypeScript codemods: `jscodeshift`
- JSON/YAML edits: [[config-file-editing/SKILL|config-file-editing]]
- Python scripts, `uv`, missing dependencies, install choices:
  [[tool-provisioning-and-environment-hygiene/SKILL|tool-provisioning-and-environment-hygiene]]
- PDFs: [[reading-pdfs/SKILL|reading-pdfs]]
- Markdown formatting and prose rewrites: [[writing/clarity/SKILL|writing-clearly-and-concisely]],
  [[writing/agent-audiences/SKILL|writing-for-agent-audiences]], and the project justfile
- Frontend and GUI work: [[design/SKILL|design]], [[responsive-design/SKILL|responsive-design]],
  [[developing-linux-guis/SKILL|developing-linux-guis]],
  [[visual-regression-testing/SKILL|visual-regression-testing]]
- Mathematical research tooling: [[mathematics/SKILL|mathematics]] (lattices, sagemath,
  and computation subskills), [[lean4/SKILL|lean4]], [[arxiv/SKILL|arxiv]],
  [[research-discovery/SKILL|research-discovery]]
- Persistent recurring tasks: [[scheduling-tasks-and-subagents/SKILL|scheduling-tasks-and-subagents]]
- Harness-specific waits or wakeups: [[codex/SKILL|codex]] or [[claude-code/SKILL|claude-code]],
  as applicable
- Delegated paid-model work: ask before using `gemini`, `codex`, `claude`, `qwen`, or
  `jules`; load the matching delegation skill first

When pushing text through `gh` or shell commands, avoid backticks in user-supplied
message bodies because they trigger shell escaping hazards.

## Long-Running Work

- For long-running commands, use PTYs/sessions and poll them.
  Do not create artificial short timeouts for ordinary engineering work.

- When you kick off a long-running background job — build, test suite, training run,
  batch, remote task, or dispatched agent — and will stop to wait for it, give the user
  an expected-completion ETA before you wait, grounded in the job's own reported
  duration, its historical runtime, or its observed progress rate. Do not go silent and
  leave the user blind to when the job should return. This concrete completion ETA for
  an already-running job is operational status, not a time estimate for proposed work,
  and is the explicit exception to the "never write time estimates" ban.

## Writing and Knowledge Transfer

- Never write or discuss time estimates for work you suggest (sole exception: the
  running-job ETA above). Never insert manual section counters in Markdown. Keep
  canonical facts in one source and route to it instead of restating dynamic metadata.

- After any knowledge-transfer edit, perform an explicit semantic comparison between
  the new destination docs and the old source material. Knowledge transfer includes
  moving instructions into skills, consolidating docs, retiring docs after migration,
  rewriting prompts, or replacing local procedures with global guidance. Check for lost
  endpoints, commands, hostnames, paths, credential models, state machines, evidence
  requirements, examples, warnings, and operational constraints. Any watering-down,
  vague summarization, generic regression-to-the-mean wording, missing concrete
  procedure, or weakened prohibition is a defect. Rectify it immediately before
  deleting, retiring, or relying on the old source.
