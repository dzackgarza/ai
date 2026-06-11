#!/usr/bin/env bash
set -euo pipefail

CONTROL_REPO="${GITHUB_WORKSPACE:?GITHUB_WORKSPACE is required}"
REVIEWER_REPO="/home/reviewer/repo"

cp "$REVIEWER_REPO/.review-report-artifact.json" "$CONTROL_REPO/.review-report-artifact.json"

if [ -f "$REVIEWER_REPO/.review-report-comment.md" ]; then
  cp "$REVIEWER_REPO/.review-report-comment.md" "$CONTROL_REPO/.review-report-comment.md"
fi
