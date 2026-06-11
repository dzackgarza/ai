#!/usr/bin/env bash
set -euo pipefail

category="${1:?usage: fetch-context.sh <category> <output>}"
output="${2:?usage: fetch-context.sh <category> <output>}"

uv run quality-control/ci/fetch-reviewer-context.py \
  --repo "${GITHUB_REPOSITORY:?GITHUB_REPOSITORY is required}" \
  --categories "$category" \
  --output "$output"
