---
order: 20
tags:
- source-owner-context
- source-owner-preference
- source-system-contract
- function-orient
- function-constrain
- function-procedure
- function-route
- function-allocate
- retest-policy-change
- retest-toolchain-change
- retest-environment-change
title: Conventions for This System
---

- **Read all READMEs and AGENTS.md files** encountered.

- There are many symlinks on this system, check the file type if you find confusing duplication.
  Reusable agent-facing prompts now live in the `ai-prompts` repo and are consumed by slug; `~/ai/prompts` is reserved for `local_context` overlays and repo-specific guidance.

- Never store or use local secrets or inline them into any shell commands.
  They must be stored in ~/.envrc, trusted with `direnv allow`, and all projects should have a .envrc file that either sources ~/.envrc directly or uses the `source_up` directive.

  - Project-local envrc files should be tracked via git, and thus never store true secrets, only env vars.
    If a project truly needs a local secret (rare), then it should be in a gitignore .env file and the envrc file should source it.

- All project automation routes through `just`: always look for an existing justfile and use its recipes, and never run tests, type-checking, builds, publishing, or other workflows manually when a recipe exists.
  Load the `justfile` skill when working with justfiles or project tasks.

- Dependencies between projects should be routed through github and use `uvx`/`npx -y`
  calls when possible, or explicitly declared as dependencies.
  Load `tool-provisioning-and-environment-hygiene` before provisioning tools or
  dependencies.
  Do not tie across file system boundaries unless absolutely necessary.

- **Never** set env vars inline in shell commands (e.g., `MYSECRET=123 some_command`) — these are visible in the process list.
  Use env files or exports instead.

- PDF storage is managed in `~/pdf-extraction` with justfile recipes for extraction and conversion.
  Load `reading-pdfs` before PDF extraction or conversion work.

- PDFs are stored in `~/pdfs` and should be organized into library-like subfolder trees.

- Review CI is owned by `dzackgarza/ai-review-ci`; this repo carries only the
  `.github/workflows/review-{general,slop,pr}.yml` trigger files. Edit schedules,
  thresholds, and `with:` inputs here; edit review behavior upstream.
  Load `policy-index`, `anti-slop`, or `reviewing-llm-code` for behavior changes.

- **Before editing any JSON or YAML file: LOAD `config-file-editing` skill.** Never raw-edit config files.
