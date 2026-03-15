#!/usr/bin/env bash
set -u

if ! command -v just >/dev/null 2>&1; then
  echo "warning: just not found; skipping OpenCode plugin cache clear" >&2
  exit 0
fi

if ! just --justfile "$HOME/justfile" opencode-clear-plugin-install-cache >/dev/null 2>&1; then
  echo "warning: failed to clear OpenCode plugin install cache" >&2
fi

exit 0
