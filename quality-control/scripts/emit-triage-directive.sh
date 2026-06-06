#!/usr/bin/env bash
# emit-triage-directive.sh
#
# Prints the standardized QC triage directive to stdout.
# Called by justfile recipes when a QC check fails.
# Does NOT exit - the caller handles the exit code.
#
# Usage:
#   "$QC_DIR/scripts/emit-triage-directive.sh"
#   exit 1  # or $ec

set -euo pipefail

cat << 'TRIAGE_EOF'

================================================================================
  QC FAILURE — TRIAGE REQUIRED
================================================================================

  One or more quality control checks failed (see above for details).

  YOU ARE NOW IN TRIAGE MODE. Follow these rules EXACTLY:

  1.  Do NOT probe, inspect, or modify any file in ~/ai/quality-control/.
      The QC configs, scripts, checking tools, and ML models are centrally
      owned and authoritative. Probing them is reward-hacking.

  2.  Do NOT attempt to fix any of the findings yourself.
      You WILL game the triage if you try. All fixes must be delegated
      to a subagent not involved in producing the failing code.

  3.  Present ALL findings to the user immediately, with the full raw
      tool output. Do NOT filter, summarize, or interpret the results.

  4.  Wait for explicit user approval before proceeding.

  TRIAGE WORKFLOW (after user approval):

    Step 1 — Spawn a SUBAGENT to perform an llm-review slop report on
             the findings. Load the `reviewing-llm-code` skill in the
             subagent.

    Step 2 — Spawn a SEPARATE SUBAGENT to solve the underlying
             architectural issues. The reviewer and fixer MUST be
             different subagent instances.

  Load the qc-triage skill for the complete triage protocol:

    skill qc-triage

================================================================================
TRIAGE_EOF
