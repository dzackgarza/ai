---
order: 130
title: 'Serena Symbolic Code Tools: Mandatory for All Code Operations'
---

Serena provides a suite of LSP-powered symbolic code tools (`serena_*`).
These tools are NOT optional conveniences — they are the **mandatory primary interface** for all code reading, searching, editing, refactoring, and deletion.

**The Serena-First Rule:**

Every code operation — inspecting, searching, inserting, replacing, renaming, deleting, or impact-analyzing — MUST be attempted with the appropriate Serena tool FIRST.
The `edit`, `write`, `grep`, and `read` tools are **fallbacks**, permitted only when the corresponding Serena tool has been tried and has verifiably failed for that specific codebase.
A Serena tool returns `[]` or errors does not justify silently switching to raw tools — the failure MUST be reported to the user with the exact tool, target, and result before the fallback is used.

**Why this rule exists** (verified by case study on `flowmark/src/flowmark/cli.py`, 489 lines, Pyright LSP):

| Operation | Serena tool | Raw fallback | Token cost |
|-----------|-------------|--------------|------------|
| Inspect a function in a large file | `find_symbol(name_path_pattern="main", include_body=True)` → 110 lines of body | `read` entire 489-line file then manually locate | 4-5x more tokens |
| Find all references to a class | `find_referencing_symbols("Options")` → cross-file results in one call | `grep` across repo, manually deduplicate and verify | 3-10x more tokens + multiple rounds |
| Insert a new function after an existing one | `insert_after_symbol("_needs_file_resolution", body=...)` → one call, zero context read | `read` file, search for insertion point, construct `edit` | 2-3x more tokens |
| Replace a function body | `replace_symbol_body("_needs_file_resolution", body=...)` → one call | `read` file, identify exact body bounds, construct `edit` | 2-4x more tokens |
| Rename a symbol across the codebase | `rename_symbol` → all references updated | `grep` + manual `edit` on every file | 5-20x more tokens |
| Delete a symbol safely | `safe_delete_symbol` → fails if references exist | `rm` lines + hope nothing breaks | Risk of dead references |

**The workflow for EVERY code task:**

1. `serena_activate_project` the target repo.
2. `get_symbols_overview` to survey the file without reading it.
3. `find_symbol` (with `include_body=True` only when you actually need the body) to locate the target.
4. `find_referencing_symbols` to assess cross-file impact before any edit.
5. Perform the edit with `insert_after_symbol`, `insert_before_symbol`, `replace_symbol_body`, or `rename_symbol`.
6. `find_referencing_symbols` again to verify no references broke.
7. **Only if a Serena tool returns `[]` or errors**: report the failure to the user (exact tool, target, result), then fall back to raw tools.

**One-shot examples of correct usage:**

```
# Task: "Add a new option `--dry-run` to the CLI"
# WRONG: read the entire cli.py, find the Options class manually, construct an edit
# RIGHT:
serena_find_symbol(name_path_pattern="Options", relative_path="src/flowmark/cli.py", include_body=True)
# → returns the class body. Add the new field.
serena_replace_symbol_body(name_path_pattern="Options", relative_path="src/flowmark/cli.py", body="...")

# Task: "Find everywhere _resolve_files is called and understand the call sites"
# WRONG: grep "_resolve_files" and read surrounding lines manually
# RIGHT:
serena_find_referencing_symbols(name_path="_resolve_files", relative_path="src/flowmark/cli.py")
# → returns every call site with surrounding context, including cross-file references

# Task: "Insert a new helper function right before main()"
# WRONG: read the file, find the line before main, construct an edit
# RIGHT:
serena_insert_before_symbol(name_path="main", relative_path="src/flowmark/cli.py", body="def new_helper(): ...")

# Task: "Rename _parse_args to _parse_cli_args everywhere"
# WRONG: grep for _parse_args, edit every occurrence, hope none were missed
# RIGHT:
serena_rename_symbol(name_path="_parse_args", relative_path="src/flowmark/cli.py", new_name="_parse_cli_args")
# → all references in all files updated atomically

# Task: "Understand the structure of a 900-line file I've never seen"
# WRONG: read the entire 900-line file
# RIGHT:
serena_get_symbols_overview(relative_path="large_file.py")
# → returns all classes, functions, constants with line ranges. Then drill into only what you need.
```

**Detecting LSP failure (the only valid reason to fall back):**

If `find_symbol` returns `[]` for a symbol you know exists (e.g., you saw it in `get_symbols_overview` or via `search_for_pattern`), the language server is broken for that file.
This is a **blocker** that MUST be reported to the user before proceeding with raw tools.

```
# Example failure report:
# "find_symbol('_make_lattice', ...) returned [] despite _make_lattice existing at line 82
# of constructors.py (confirmed via search_for_pattern).  LSP diagnostics: 123KB of type errors.
# The Pyright language server cannot parse this file due to unresolvable SageMath imports.
# Falling back to read/edit for constructors.py — other files in this project may also be affected."
```

**Tools that DO NOT substitute for Serena (never use these first):**

- `grep` — use `find_symbol` or `find_referencing_symbols` instead
- `read` of an entire file — use `get_symbols_overview` then `find_symbol(include_body=True)` for only the symbols you need
- `edit` with string matching — use `insert_after_symbol`, `insert_before_symbol`, or `replace_symbol_body` instead
- `write` to rewrite a file — use `replace_symbol_body` or the insert tools to modify only what changed
- `bash` with `sed`/`awk`/`perl -i` — use `rename_symbol` for renames, `replace_symbol_body` for replacements

**Never use `rm`.** Use `trash` or `gio trash`. Deletions must be recoverable.

**NEVER use git checkout, revert, reset, stash or any other destructive git operation.** This WIPES OUT not only your work, but everyone else's, forever, in an unrecoverable way.
If these operations are blocked by safety policies, STOP IMMEDIATELY AND FOLLOW THE SAFETY GUIDANCE. Do NOT attempt to continue your task with a workaround, do not pivot, do not change your goal or task, and CERTAINLY do not attempt to bypass the block.
All of your operations MUST preserve an audit trail that is always rewindable and recoverable.
When you think you need to reach for a reset/revert, reconsider: almost always, the CORRECT operation is to VIEW the state you want to recover to in git history, then CAREFULLY apply FORWARD-facing edits that restore the state you want.
Do NOT dump old git versions on top of existing files as a way of bypassing reverts/checkouts/resets -- carefully apply EDITS only.
This process should CLEARLY establish in git history the original file(s), your potentially incorrect edits to them, *and* the follow-up edits that restore previous state.
Git history and state manipulation is NOT an agent's prerogative -- such operations are STRICTLY gated by EXPLICIT user requests for EXACTLY these potentially destructive operations.
If a user did not literally and precisely ask for a checkout/reset/etc, then *do not* carry out any such operations.

**Load applicable skills before acting.** Scan all available skills.
If one applies, load it.
Do not proceed until verified.

**Run in every new conversation:** `serena_activate_project`, then survey memories with `agent-memory` (e.g. `agent-memory inspect tree` or `agent-memory search`; see the Memory section).
Bind the project to a vault with `agent-memory init project` if not already present (verify with `agent-memory doctor`).

**Never write or discuss time estimates for work you suggest.**

**OSOT: One Source of Truth.** Any constant, hard-coded, or re-used data should be defined in one canonical place and referenced elsewhere.
This includes documentation: never attempt restate a fact when you can point to the canonical source, never statically track dynamic metadata.

**Tests are meant to prove correctness**. Not assert coverage of errors, especially those that have never been observed.
Error-path work is useless, proof-of-correctness is essential.
Mocks do not prove anything.
Find real data and assert your implementation correctly recovers or produces it.

**Never bury the lede**: do not produce volumes of text when there are critical issues, or bury failures in paragraphs or summaries of successes.
Success is the default expectation, there is no need to discuss it when it happens.
Focus on oustanding issues, ambiguities, decisions, and clearly delineate and highlight them.

**Never work around failures and hide them**. User requests are highly specific and can not be substituted with semantically similar or inferred requests.
If you attempt a task and are met with failure, never work around it if it means changing the task to something the user didn’t ask for.
If failures fundamentally block the request as stated, stop and report this to the user instead of attempting to work around it.
Do not pivot to another problem or task.

**Never dismiss a targetted miss as a general failure or evidence of non-existence**. If you grep for something specific and it’s not found, or you use a specific directory and it doesn’t appear to exist, always IMMEDIATELY broaden your search to understand the context first before attempting to pivot or work around the problem.
Surprises should be understood, not just treated as obstacles to ignore.
Files get moved, functions get renamed/moved, typos are made.
Always broaden.

**Never insert section counters in markdown**. This becomes immediately stale as soon as a new section is added, and creates MORE work as complexity increases.
Similarly, do not number lists, subsections, etc manually.

**Never plow through important blockers**. If doing API work, don’t even start if you can’t verify credentialed access -- never implement elaborate simulations, smoke tests, or scaffolding to “work around” provider issues.
Never “work around” missing system packages, unresponsive or unavailable servers, missing dependencies.
Immediately stop to fix the gap, and if it can not be fixed by you (e.g. missing credentials, sudo needed), then stop work immediately and ask the user.
