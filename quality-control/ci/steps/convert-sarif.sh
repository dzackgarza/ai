#!/usr/bin/env bash
set -euo pipefail

category="${1:?usage: convert-sarif.sh <category>}"
CONTROL_REPO="${GITHUB_WORKSPACE:?GITHUB_WORKSPACE is required}"

uv run /opt/ai-review/private/report-to-sarif.py \
  --artifact "$CONTROL_REPO/.review-report-artifact.json" \
  --output "$CONTROL_REPO/.review-report.sarif" \
  --category "$category"
