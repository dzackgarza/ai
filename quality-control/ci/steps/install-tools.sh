#!/usr/bin/env bash
set -euo pipefail

curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin sh
npm install -g opencode-ai
npm install -g cc-safety-net
