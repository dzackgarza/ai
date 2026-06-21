---
order: 20
title: Conventions for This System
---

- **Read all READMEs and AGENTS.md files** encountered.

- There are many symlinks on this system, check the file type if you find confusing duplication.
  Reusable agent-facing prompts now live in the `ai-prompts` repo and are consumed by slug; `~/ai/prompts` is reserved for `local_context` overlays and repo-specific guidance.

- Never store or use local secrets or inline them into any shell commands.
  They must be stored in ~/.envrc, trusted with `direnv allow`, and all projects should have a .envrc file that either sources ~/.envrc directly or uses the `source_up` directive.

  - Project-local envrc files should be tracked via git, and thus never store true secrets, only env vars.
    If a project truly needs a local secret (rare), then it should be in a gitignore .env file and the envrc file should source it.

- All projects must have centralized recipes in a justfile and be run with `just`. Always look for one and use its recipes, never bypass them.

  - In particular, all tests, type-checking, builds, publishing, etc must be routed through `just`, never run such processes or commands “manually”.

- Dependencies between projects should be routed through github and use `uvx`/`npx -y` calls when possible, or explicitly declared as dependencies.
  Do not tie across file system boundaries unless absolutely necessary.

- **Never** set env vars inline in shell commands (e.g., `MYSECRET=123 some_command`) — these are visible in the process list.
  Use env files or exports instead.

- PDF storage is managed in `~/pdf-extraction` with justfile recipes for extraction and conversion.

- PDFs are stored in `~/pdfs` and should be organized into library-like subfolder trees.

- Review CI is owned by `dzackgarza/ai-review-ci`; this repo carries only the
  `.github/workflows/review-{general,slop,pr}.yml` trigger files. Edit schedules,
  thresholds, and `with:` inputs here; edit review behavior upstream.

- **Before editing any JSON or YAML file: LOAD `config-file-editing` skill.** Never raw-edit config files.
