#!/usr/bin/env bash
set -euo pipefail

mode="${1:?usage: run-review.sh <mode> <template> <report_type>}"
template="${2:?usage: run-review.sh <mode> <template> <report_type>}"
report_type="${3:?usage: run-review.sh <mode> <template> <report_type>}"

CONTROL_REPO="${GITHUB_WORKSPACE:?GITHUB_WORKSPACE is required}"
REVIEWER_REPO="/home/reviewer/repo"

sudo -u reviewer -H env \
  PATH="/home/reviewer/bin:/usr/local/bin:/usr/bin:/bin" \
  REPORT_TYPE="$report_type" \
  REVIEWER_REPO="$REVIEWER_REPO" \
  CONTROL_REPO="$CONTROL_REPO" \
  GITHUB_BASE_REF="${GITHUB_BASE_REF:-main}" \
  PR_NUMBER="${PR_NUMBER:-0}" \
  bash -lc "cd '$REVIEWER_REPO' && python3 quality-control/run-review.py \
    --mode '$mode' \
    --skills-dir opencode/skills \
    --template '$template' \
    --base-ref \"\${GITHUB_BASE_REF:-main}\" \
    --pr-number \"\${PR_NUMBER:-0}\" \
    --reviewer-context .reviewer-context.md"
