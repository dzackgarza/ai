#!/usr/bin/env bash
# Shared hook-message functions — sourced by pre-commit and pre-push.
# OSOT: every git hook renders these same messages.
#
# Usage in a hook:
#   source "${QC_ROOT:-$HOME/ai/quality-control}/scripts/hook-messages.sh"
#   block_no_justfile
#   exit 1

RED='\033[0;31m'
NC='\033[0m'

block_no_justfile() {
    echo ""
    echo -e "${RED}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║  QC BLOCKED: No justfile found in project root.             ║${NC}"
    echo -e "${RED}╠══════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${RED}║                                                              ║${NC}"
    echo -e "${RED}║  Every project must have a justfile declaring its QC         ║${NC}"
    echo -e "${RED}║  type:                                                        ║${NC}"
    echo -e "${RED}║                                                              ║${NC}"
    echo -e "${RED}║      qc-type := \"python\"  # or bun, rust, sage              ║${NC}"
    echo -e "${RED}║                                                              ║${NC}"
    echo -e "${RED}║  See ~/ai/quality-control/ for the available justfiles.     ║${NC}"
    echo -e "${RED}╚══════════════════════════════════════════════════════════════╝${NC}"
}

block_no_qc_type() {
    echo ""
    echo -e "${RED}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║  QC BLOCKED: No qc-type variable in project justfile.       ║${NC}"
    echo -e "${RED}╠══════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${RED}║  Add:  qc-type := \"python\"  # or bun, rust, sage           ║${NC}"
    echo -e "${RED}╚══════════════════════════════════════════════════════════════╝${NC}"
}

block_invalid_qc_type() {
    local bad="$1"
    echo ""
    echo -e "${RED}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║  QC BLOCKED: Invalid qc-type '${bad}'.                      ║${NC}"
    echo -e "${RED}║  Valid values: python, bun, rust, sage                     ║${NC}"
    echo -e "${RED}╚══════════════════════════════════════════════════════════════╝${NC}"
}
