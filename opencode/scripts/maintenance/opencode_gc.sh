#!/bin/bash
# Garbage collect opencode snapshot repositories to prevent orphaned object buildup

SNAPSHOT_DIR="/home/dzack/.local/share/opencode/snapshot"

if [ -d "$SNAPSHOT_DIR" ]; then
    for repo in "$SNAPSHOT_DIR"/*/; do
        if [ -d "$repo/.git" ] || [ -d "$repo/objects" ]; then
            echo "[$(date -Iseconds)] GC: $repo"
            (cd "$repo" && git gc --prune=now --aggressive 2>&1)
            echo "[$(date -Iseconds)] Done: $repo"
        fi
    done
fi
