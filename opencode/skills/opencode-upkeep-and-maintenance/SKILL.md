---
name: opencode-upkeep-and-maintenance
description: Use when the OpenCode sidebar does not reflect the current git working tree state or shows stale snapshots.
---

# OpenCode Upkeep and Maintenance

## Core Policy

- **Authorization Required:** Agents MUST NOT perform any snapshot modification (deletion or refresh) without explicit user approval.
- **Rollback Invariant:** Modifying snapshots makes it impossible to walk back individual steps using native OpenCode features. Agents MUST verify the user understands this consequence and that no further backwards steps are intended for the session.
- **Database Safety:** Always backup the database before running maintenance scripts.
- **Feature Preservation:** Snapshots are a critical feature. Maintenance focuses solely on bug mitigation (leaks) and pruning unneeded data.

## Workflow: Reset Sidebar Baseline

Use when the sidebar is out of sync with the git state or contains stale snapshot references.

1.  **Safety Check:** Backup database: `cp ~/.local/share/opencode/opencode.db ~/.local/share/opencode/opencode.db.bak`
2.  **Prompt for Approval:** Explain that `oc-refresh-diff` disables native rollbacks for this session. Do not proceed until the user confirms they will use git for any future backwards steps.
3.  **Verify Session Status:** Ensure the target session is idle.
4.  **Execute Refresh:** `oc-refresh-diff <session-id>`
    - **Effect:** Clears stale references from the DB and index, making old objects reachable for `git gc`.

## Workflow: Session Pruning (Individual)

Pruning sessions recovers database space and snapshot disk space. **Perform pruning before investigating snapshot issues.**

1.  **Gather Evidence:**
    - List candidates via `GET /session` or `/experimental/session`.
    - Apply Candidate Decision Procedures (Archived, Stale > 2 weeks, Short < 10 turns, Trivial tests).
2.  **Audit Transcripts:** Read the actual conversation to verify the session is unneeded.
3.  **Present Options:** List candidate IDs/titles to the user.
4.  **Prompt for Deletion:** Obtain explicit authorization for the specific list before pruning via API or `sqlite3`.

## Workflow: En-Masse Pruning (Playbook)

Use for bulk cleanup of automated or ephemeral artifacts. **MANDATORY: Verify user authorization before execution.**

1.  **Backup Database:** `cp ~/.local/share/opencode/opencode.db ~/.local/share/opencode/opencode.db.bak`
2.  **Identify Ephemeral Candidates:**
    ```bash
    # Finds automated tools (opx, ocm) and unnamed scratchpads
    sqlite3 ~/.local/share/opencode/opencode.db \
      "SELECT id, title FROM session WHERE title LIKE 'opx:%' OR title LIKE 'ocm:%' OR title LIKE 'New session -%';" > prune_list.txt
    ```
3.  **Audit Sample:** Read 2-3 random transcripts from the list to ensure no "primed" context is being lost.
4.  **Transactional Deletion:**
    ```bash
    # Generate and run SQL transaction
    echo "BEGIN TRANSACTION;" > prune.sql
    cut -d'|' -f1 prune_list.txt | sed "s/.*/DELETE FROM session WHERE id = '&';/" >> prune.sql
    echo "COMMIT;" >> prune.sql
    sqlite3 ~/.local/share/opencode/opencode.db < prune.sql
    ```
5.  **Optimize Database:** Reclaim space from deleted rows and defragment:
    ```bash
    sqlite3 ~/.local/share/opencode/opencode.db "VACUUM;"
    ```
6.  **Reclaim Disk Space:** Physical recovery requires `git gc` in the snapshot repositories:
    ```bash
    # Targeted cleanup of repack leaks
    rm -f ~/.local/share/opencode/snapshot/*/objects/pack/tmp_pack_*
    # Full pruning GC
    for dir in ~/.local/share/opencode/snapshot/*; do
      [ -d "$dir" ] && git -C "$dir" gc --prune=now --quiet
    done
    ```

## Decision Procedures: Pruning Candidates

Use when disk space is exhausted due to orphaned repack artifacts (bugs in the snapshot system).

1.  **Diagnosis:** Determine if large files are caused by this bug:
    - **Find dominating snapshot:** `du -sh ~/.local/share/opencode/snapshot/* | sort -h`
    - **Inspect pack usage:** `du -sh ~/.local/share/opencode/snapshot/<id>/objects/pack/`
    - **List temporary artifacts:** `ls -lh ~/.local/share/opencode/snapshot/<id>/objects/pack/tmp_pack_*`
    - **Verify not in use:** `lsof +D ~/.local/share/opencode/snapshot/` (Ensure no `tmp_pack_*` files are open).
2.  **Targeted Cleanup:** If multi-gigabyte `tmp_pack_*` files are present and not open by any process:
    ```bash
    # Reclaims orphaned files without destroying history
    rm ~/.local/share/opencode/snapshot/*/objects/pack/tmp_pack_*
    ```
3.  **Trigger Garbage Collection:** Once references are cleared (via `oc-refresh-diff` or pruning), run:
    ```bash
    # Run inside the snapshot git directory (~/.local/share/opencode/snapshot/<id>)
    git gc --prune=now
    ```

## Workflow: Clear Plugin Cache

Use if plugin behavior is stale or if dependency installation fails in the plugin environment.

1.  **Identify Cache:** Default is `~/.cache/opencode` (override via `OPENCODE_PLUGIN_CACHE_DIR`).
2.  **Trash Stale Artifacts:**
    ```bash
    for p in node_modules package.json bun.lock; do
      [ -e "$HOME/.cache/opencode/$p" ] && gio trash "$HOME/.cache/opencode/$p"
    done
    ```

## Reference: OpenCode API

- `GET /session`: Active sessions (filtered).
- `GET /experimental/session?archived=true`: History including archived sessions.
- Query parameters: `?directory=...`, `?roots=true`, `?search=...`, `?limit=...`, `?start=<timestamp>`.

## Reference: OpenCode Database Schema

Use for manual inspection or when developing maintenance scripts.

- `project`: `id`, `worktree`, `name`
- `session`: `id`, `project_id`, `slug`, `directory`, `title`
- `message`: `id`, `session_id`, `data` (JSON: includes snapshot hashes)
- `part`: `id`, `message_id`, `data` (JSON: includes `step-start`/`step-finish` anchors)
- `todo`: `session_id`, `content`, `status`
- `workspace`: `id`, `project_id`, `directory`

## Environment Traps

- **Snapshot Invariant:** Sidebar state depends on internal tree hash anchors (step-start/step-finish), not direct git tracking. `oc-refresh-diff` resets these anchors to the current HEAD.
- **Cache Persistence:** OpenCode caches plugin artifacts in `~/.cache/opencode`. Stale `node_modules` or `bun.lock` here can break new plugin deployments.
- **Snapshot Leaks:** Failed snapshots or `git gc` attempts can leak multi-gigabyte `tmp_pack_*` files in `~/.local/share/opencode/snapshot/`. These bypass standard Git pruning because tree objects created by `git write-tree` remain reachable from the index. Large repos often crash during repack (OOM/disk pressure), orphaning these temporary artifacts.

## Validation Checklist

- [ ] Database backup exists at `~/.local/share/opencode/opencode.db.bak`.
- [ ] User confirmed that native rollbacks are no longer needed for the session (irreversible).
- [ ] `oc-refresh-diff` ran to completion (if refreshing sidebar).
- [ ] `~/.cache/opencode/node_modules` trashed (if clearing cache).
- [ ] Transcripts read and user approved deletion list (if pruning).
- [ ] Sidebar reflects real uncommitted changes.
