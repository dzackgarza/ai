#!/usr/bin/env bash
set -euo pipefail

mkdir -p ~/.config/opencode
cp quality-control/ci-opencode.json ~/.config/opencode/opencode.json

mkdir -p ~/.config/opencode/skills
for skill in anti-slop reviewing-llm-code fixing-slop policy-index test-guidelines bespoke-software-policy tool-provisioning-and-environment-hygiene; do
  if [ -d "opencode/skills/$skill" ]; then
    cp -r "opencode/skills/$skill" ~/.config/opencode/skills/
  fi
  echo "installed $skill"
done

mkdir -p .cc-safety-net/rules/project-rules
cp quality-control/ci-cc-safety-net-rules.json .cc-safety-net/rules/rule.json
cp quality-control/ci-cc-safety-net.json .cc-safety-net/rules/project-rules/rulebook.json
CC_SAFETY_NET_PARANOID=1 npx -y cc-safety-net rule sync
