---
name: cleaning
description: Use when removing debris, dead code, unused files, or reorganizing any repository — code, docs, configs, notebooks, experiments, or mixed content.
---

# Cleaning

Safe, reversible, context-aware cleanup for any kind of repository content.

## Core Principles

**Cleaning ≠ Refactoring.** Cleaning removes what is unambiguously dead, misplaced, or debris. When you find something that needs restructuring or improvement, document it in `GAPS.md` and move on. Never start refactoring as part of a cleaning task.

**Holistic knowledge first.** Never trust file names or locations alone to determine purpose. Read content. Run `ls`, `tree`, or equivalent to build a full map of the repo before deciding anything.

**Reversibility always.** Every destructive action must be reversible by git. Commit before cleaning, use an `archive/` intermediate, and only delete in a final commit after user review.

---

## Pre-Cleaning Checklist

Before touching a single file:

1. **Commit all current work** — run `git add -A && git commit` to checkpoint the current state. This is non-negotiable.
2. **Create a worktree** — do all cleaning and reorganization in a new git worktree (`git worktree add ../repo-clean -b chore/clean`). Merge back to main only after user signoff.
3. **Build a repo map** — run `ls`, `tree -L 3`, and skim top-level READMEs. For non-trivial repos, delegate repo exploration to a subagent.
4. **Read before deciding** — for any file whose purpose is ambiguous from its name and location, read its content before classifying it.
5. **Write a planning document** — create `CLEANING_PLAN.md` at the repo root (or in a scratch location). Include: scope, what you've seen, your classification decisions, open questions. This document is your continuity mechanism across context compaction breaks.

---

## The Cleanup Worktree Workflow

```
1. git add -A && git commit        # checkpoint current state
2. git worktree add ../repo-clean -b chore/clean
3. cd ../repo-clean                # all work happens here
4. ... clean, organize, archive ...
5. git add -A && git commit -m "archive: move debris to archive/ for review"
6. [user reviews archive/]
7. git rm -r archive/ && git commit -m "clean: remove archived debris"
8. cd <original> && git merge chore/clean
9. git worktree remove ../repo-clean
```

Never delete directly from the main working tree. Always merge a reviewed worktree.

---

## Classification: Debris vs. Live vs. Incomplete

Before removing anything, classify it:

| Category                   | Description                                                         | Action                         |
| -------------------------- | ------------------------------------------------------------------- | ------------------------------ |
| **Debris**                 | Build artifacts, OS files, generated outputs, temp files, IDE state | Remove immediately             |
| **Dead code/docs**         | Confirmed unreferenced, no active purpose, not in-progress          | Archive → delete               |
| **Stale but referenced**   | Dead code that other code _mentions_ or hedges about                | Semantic refactor (→ GAPS.md)  |
| **Incomplete/in-progress** | Partial experiments, half-written docs, stub implementations        | Note in GAPS.md, do NOT delete |
| **Active**                 | Referenced, used, currently maintained                              | Leave alone                    |
| **Unclear**                | Can't determine purpose from name + content                         | Ask user                       |

**Never mistake a partial file for a broken one.** A half-written experiment or partially started notebook may be intentional work awaiting continuation, not a failed implementation to discard.

---

## Dead References: Semantic Removal (Not Laundering)

Removing a dead item is not enough if other code references it. Dead references must be fully resolved:

- **Laundering** (wrong): Remove `foo.py`, leave `if foo_exists: ...` and comments mentioning `foo` in other files.
- **Semantic removal** (correct): Find all references to removed items, analyze whether the referencing code now has unreachable branches, impossible conditions, or hedge logic, and refactor or remove that code too.

For each removed item:

1. Grep for its name, imports, and any string references across the entire repo.
2. For each hit: decide if the referencing code is now dead, nonsensical, or needs simplification.
3. If the cleanup is simple (remove an import, delete a dead branch): do it.
4. If the cleanup requires non-trivial restructuring: document in GAPS.md and leave a `# TODO(clean): ...` comment.

---

## Archive-Before-Delete Protocol

Never delete in the same commit you move. Use two commits:

**Commit 1 (archive):** Move everything to-be-deleted into `archive/YYYY-MM-DD/` at the repo root (or appropriate subdirectory). Do not delete yet. This commit is what the user reviews.

**Commit 2 (delete):** After user confirms the archive looks right, `git rm -r archive/` and commit. This is the only destructive commit.

The archive directory is temporary and should be added to `.gitignore` after deletion to prevent future accumulation.

---

## What Counts as Debris

Safely remove without user review (but still via archive protocol):

- Build outputs: `dist/`, `build/`, `.next/`, `out/`, `__pycache__/`, `*.pyc`, `*.pyo`
- Cache dirs: `.vite/`, `.turbo/`, `.parcel-cache/`, `.mypy_cache/`, `.pytest_cache/`
- Coverage/test reports: `coverage/`, `htmlcov/`, `.nyc_output/`, `test-results/`, `junit.xml`
- OS/IDE artifacts: `.DS_Store`, `Thumbs.db`, `*.swp`, `*.swo`, `.idea/` (if not shared)
- Temp/scratch files: `*.tmp`, `*.temp`, `tmp-*`, `scratch-*`, `debug-*` (verify not active)
- Stale logs: `*.log`, `npm-debug.log*`

**Do not remove without content inspection:**

- Anything modified in the last 7 days
- Files without a recognizable artifact/temp extension
- Anything referenced in docs, configs, or other source files

---

## Dead Code Detection

Use language tooling to surface candidates, then verify manually:

**Verification checklist before flagging as dead:**

- [ ] Zero direct references (LSP "find references" or grep with word boundaries)
- [ ] Not re-exported from a public module
- [ ] Not loaded dynamically (reflection, config-driven, plugin registry, string dispatch)
- [ ] Not behind conditional compilation for a feature that may be active elsewhere
- [ ] Not part of a public API surface (library crates, exported interfaces)
- [ ] Not referenced only in tests/examples (those usages count as "used")
- [ ] Not referenced in docs, comments, or macro expansions

If any check fails: **do not remove**. Include in a "deferred" section of your report.

**Language-specific tools:**

- TypeScript/JS: `npx ts-prune`, `npx unimported`, `npx depcheck`
- Python: `vulture`, `autoflake --check`
- Rust: `cargo clippy -- -W dead_code -W unused_imports`
- General: LSP "find references"; grep with `\bsymbol_name\b`

---

## GAPS.md: Tracking Incomplete and Deferred Work

Create or update `GAPS.md` at the repo root whenever you encounter:

- **Incomplete/partial files** that are not debris but need follow-up work
- **Refactoring needs** identified during cleaning (do NOT start the refactor; document it)
- **Dead references** requiring non-trivial semantic cleanup
- **Unclear files** the user needs to classify
- **Interrupted cleaning work** (if the session ends mid-clean, record exactly where you stopped)

Format:

```markdown
## GAPS

### Incomplete Work Needing Follow-up

- `experiments/lattice-search.py` — partially implemented, needs completion or decision to archive
- `notebooks/scratch.ipynb` — looks like an active experiment, status unknown

### Refactoring Needed (Do Not Clean Until Refactored)

- `src/loader.py` uses removed `PluginV1` interface — ~40 lines of dead branches, needs rewrite
- `configs/pipeline.yaml` references deprecated `old_format` key — downstream code needs updating

### Deferred Dead References (Non-Trivial)

- `docs/guide.md` mentions removed `foo` module in 3 places — update after confirming replacement

### Open Questions for User

- `data/legacy_export.csv` — unknown origin, 500MB, unclear if needed
```

---

## Subagent Delegation for Large Repos

For repos with more than ~50 files or multiple content areas, delegate exploration and classification to subagents:

- **Exploration subagent**: Map the repo, read file contents, produce a classification table (debris / dead / incomplete / active / unclear) for all non-obvious files.
- **Reference-checking subagent**: Given a list of candidate dead items, grep and LSP-check all references and return a verified "confirmed dead" list.
- **Semantic-cleanup subagent**: Given a confirmed dead item and its reference list, produce the minimal diff to remove all laundered references.

This preserves your context window for decision-making and synthesis, not mechanical scanning.

---

## Docs and Non-Code Cleanup

The same principles apply to documentation, prompts, notebooks, configs, downloaded files, and experiments:

**Archive before delete** — same two-commit protocol.
**Read before deciding** — a file named `scratch.md` may contain valuable notes; a file named `architecture.md` may be completely outdated.
**Distinguish historical from active** — completed sprint plans, POC summaries, and one-off analysis reports belong in `archive/`, not at the root. Core guides, onboarding docs, and operational references stay active.
**Preserve entry points** — if you collapse or archive docs, ensure nothing that was reachable from a README or TOC becomes a dead link.

For documentation specifically:

- Archive: sprint plans, task breakdowns, POC summaries, one-off reports, meeting notes
- Keep active: READMEs, architecture docs, guides, onboarding, operational references
- Update `.gitignore` to prevent future accumulation of generated reports

---

## Dependency Cleanup

When cleaning unused dependencies, always:

1. Remove one at a time
2. Run build + tests after each removal
3. Read changelogs before major version bumps
4. Commit each removal atomically (not in bulk)
5. Never touch transitive deps directly — only remove from `package.json` / `pyproject.toml` / `Cargo.toml`

---

## Continuity Over Context Breaks

Cleaning tasks frequently span multiple sessions. `CLEANING_PLAN.md` is your continuity document:

```markdown
# Cleaning Plan — [repo] — [date]

## Scope

[What was requested and why]

## Repo Map (summary)

[Key directories, rough counts, content types]

## Classification Decisions

[File/dir → category mapping with brief reasoning]

## Completed

[What has been done and committed]

## In Progress

[Current phase, what's been moved to archive/, what still needs verification]

## Remaining

[What phases remain: reference cleanup, deletions, .gitignore, GAPS.md update]

## Open Questions

[Files or decisions waiting on user input]
```

At the start of any resumed session: read `CLEANING_PLAN.md` first, then `GAPS.md`.

---

## Safety Rules

**NEVER:**

- Delete without archiving first
- Remove a file based on its name alone (read content)
- Remove anything referenced by another file without checking all callers
- Delete test files for active features
- Start refactoring as part of cleaning
- Operate directly on the main working tree (use a worktree)
- Treat an incomplete/partial file as broken without understanding its intent

**ALWAYS:**

- Commit before cleaning
- Work in a git worktree
- Use `git mv` for reorganization of tracked files
- Write CLEANING_PLAN.md before starting
- Write GAPS.md for incomplete work and deferred cleanups
- Run build + tests after any structural reorganization
- Get user signoff before the final deletion commit

---

## Cleaning Report Format

After completing a cleaning pass, produce a summary:

```markdown
# Cleaning Report — [repo] — [date]

## Actions Taken

- Removed N build artifacts (X MB)
- Archived M files → archive/YYYY-MM-DD/
- Deleted archived files (after user review)
- Moved K misplaced files
- Removed J dead imports/references

## Confirmed Dead (Removed)

| File | Reason |
| ---- | ------ |

## Archived (Awaiting Review)

| File | Reason |
| ---- | ------ |

## Not Removed (Excluded)

| File | Reason |
| ---- | ------ |

## GAPS Logged

[Summary of entries added to GAPS.md]

## Validation

- [ ] Tests passing
- [ ] Build succeeds
- [ ] No broken imports or dead links
- [ ] .gitignore updated
```
