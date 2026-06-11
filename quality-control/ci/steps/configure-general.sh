#!/usr/bin/env bash
set -euo pipefail

mkdir -p .cc-safety-net/rules/project-rules
cp quality-control/ci-cc-safety-net-rules.json .cc-safety-net/rules/rule.json
cp quality-control/ci-cc-safety-net.json .cc-safety-net/rules/project-rules/rulebook.json
CC_SAFETY_NET_PARANOID=1 npx -y cc-safety-net rule sync
