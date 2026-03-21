---
name: opencode-upkeep-and-maintenance
description: Use when the OpenCode sidebar does not reflect the current git working tree state or shows stale snapshots.
---

# OpenCode Upkeep and Maintenance

## Core Policy

- **Sidebar Refresh:** If the sidebar is out of sync with the git state, run `oc-refresh-diff <session-id>` to force a fresh baseline from HEAD.
- **Database Safety:** Always backup the database before running maintenance scripts.
- **Critical Feature:** Snapshots are a critical feature for conversation context. Maintenance must focus on bug mitigation (leaks) and pruning stale data, not disabling the feature.
- **Irreversible Rollbacks:** Modifying snapshots (pruning or refreshing) makes it impossible to walk back individual steps in those sessions using OpenCode's native rollback features. Any subsequent rollbacks must be performed directly via git.

## Workflow: Reset Sidebar Baseline

Use when the sidebar is out of sync with the git state or contains stale snapshot references.

1.  **Backup Database:** `cp ~/.local/share/opencode/opencode.db ~/.local/share/opencode/opencode.db.bak`
2.  **Confirm Consequences:** Explicitly ask the user if they understand that native OpenCode rollbacks will be disabled for this session after the refresh.
3.  **Verify Status:** Ensure the session is not processing a turn.
4.  **Execute Refresh:** `oc-refresh-diff <session-id>`
    - **Effect:** Clears stale `snapshot` hashes from the DB and updates the snapshot git index to HEAD. This makes old tree objects unreachable so `git gc` can reclaim space.

## Workflow: Session Pruning

Pruning sessions is the canonical way to recover database space and snapshot disk space. **Perform pruning before investigating snapshot issues to avoid wasting resources on unneeded data.**

1.  **Rationale:** Trivial sessions (testing, "hello world", model checks) consume DB space and gigabytes of git snapshots. Pruning these reduces maintenance surface area.
2.  **Pull Candidates:**
    - List active: `curl -s http://127.0.0.1:4096/session`
    - List archived: `curl -s "http://127.0.0.1:4096/experimental/session?archived=true&limit=1000"`
3.  **Evaluate Candidates:**
    - **Archived:** Primary candidates for deletion.
    - **Stale:** Updated > 2 weeks ago? Ask user.
    - **Short (< 10 turns):** Likely one-offs. **Caution:** May be "primed" sessions for future use; ask user.
    - **Trivial:** Test runs, greetings, or "do X" one-offs.
4.  **Audit Transcripts:** Read the actual conversation to verify the session is unneeded.
5.  **Prune:** Present approved IDs/titles to the user and delete via `sqlite3` or API.

## Workflow: Mitigate Snapshot Disk Leaks

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
