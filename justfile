# Install symlinks for all CLI harnesses
# Usage: just install

repo := env_var_or_default("REPO", env_var("HOME") / "ai")

# Show available recipes

# Usage: just
default:
    @just --list

# Install all symlinks and environment variables
install:
    @mkdir -p ~/.claude ~/.codex ~/.gemini ~/.qwen ~/.config/opencode ~/.config/kilo ~/.config/amp ~/.config ~/.agents ~/.kilocode ~/.opencode
    @ln -sf {{ repo }}/AGENTS.md ~/.claude/CLAUDE.md
    @ln -sf {{ repo }}/AGENTS.md ~/.codex/AGENTS.md
    @ln -sf {{ repo }}/AGENTS.md ~/.gemini/GEMINI.md
    @ln -sf {{ repo }}/AGENTS.md ~/.qwen/QWEN.md
    @ln -sf {{ repo }}/AGENTS.md ~/.config/opencode/AGENTS.md
    @ln -sf {{ repo }}/AGENTS.md ~/.config/kilo/AGENTS.md
    @ln -sf {{ repo }}/AGENTS.md ~/.config/amp/AGENTS.md
    @ln -sf {{ repo }}/AGENTS.md ~/.config/AGENTS.md
    @ln -sf {{ repo }}/opencode ~/.config/opencode
    @ln -sf {{ repo }}/opencode/rate-limit-fallback.json ~/.opencode/rate-limit-fallback.json
    @ln -sf {{ repo }}/opencode/configs/cc-safety-net.json ~/.cc-safety-net/config.json
    @mkdir -p ~/.cc-safety-net
    # tmux config symlinks
    @ln -sf {{ repo }}/dotfiles/tmux.conf ~/.tmux.conf
    @mkdir -p ~/.config/tmux-powerline/themes
    @ln -sf {{ repo }}/dotfiles/tmux-powerline/themes/my-theme.sh ~/.config/tmux-powerline/themes/my-theme.sh
    @ln -sf {{ repo }}/dotfiles/tmux-powerline/config.sh ~/.config/tmux-powerline/config.sh
    # Backup existing skills directories before creating symlinks
    @for dir in ~/.claude/skills ~/.codex/skills ~/.gemini/skills ~/.agents/skills ~/.qwen/skills ~/.config/agents/skills ~/.config/amp/skills ~/.kilocode/skills; do \
        if [ -d "$$dir" ] && [ ! -L "$$dir" ]; then \
            mv "$$dir" "$$dir.bak.$(date +%Y%m%d%H%M%S)"; \
        fi; \
    done
    @ln -sf {{ repo }}/skills ~/.claude/skills
    @ln -sf {{ repo }}/skills ~/.codex/skills
    @ln -sf {{ repo }}/skills ~/.gemini/skills
    @ln -sf {{ repo }}/skills ~/.agents/skills
    @ln -sf {{ repo }}/skills ~/.qwen/skills
    @ln -sf {{ repo }}/skills ~/.config/agents/skills
    @ln -sf {{ repo }}/skills ~/.config/amp/skills
    @ln -sf {{ repo }}/skills ~/.kilocode/skills
    @grep -q 'GEMINI_SYSTEM_MD' ~/.bashrc 2>/dev/null || printf '\n# System prompt overrides for Gemini/Qwen CLI\nexport GEMINI_SYSTEM_MD={{ repo }}/prompts/interactive_agents/interactive.md\nexport QWEN_SYSTEM_MD={{ repo }}/prompts/interactive_agents/interactive.md\n' >> ~/.bashrc
    @grep -q 'GEMINI_SYSTEM_MD' ~/.zshrc 2>/dev/null || printf '\n# System prompt overrides for Gemini/Qwen CLI\nexport GEMINI_SYSTEM_MD={{ repo }}/prompts/interactive_agents/interactive.md\nexport QWEN_SYSTEM_MD={{ repo }}/prompts/interactive_agents/interactive.md\n' >> ~/.zshrc
    @echo "✓ Installed"
    @echo ""
    @echo "Context files:    AGENTS.md → all harnesses"
    @echo "Skills:           {{ repo }}/skills → all harnesses"
    @echo "System prompts:   GEMINI_SYSTEM_MD, QWEN_SYSTEM_MD → interactive.md (absolute path)"
    @echo "Env vars:         GEMINI_SYSTEM_MD, QWEN_SYSTEM_MD → bashrc, zshrc"
    @echo "OpenCode:         .opencode/ → ~/.config/opencode"
    @echo "Safety Net:       opencode/configs/cc-safety-net.json → ~/.cc-safety-net/config.json"

# Scaffold /var/sandbox/execa/ if not already initialized (idempotent)
# /var/sandbox/ is a plain dir hosting multiple project repos on demand.

# Usage: just sandbox
create-sandbox:
    @{{ repo }}/scripts/scaffold-sandbox.sh

# Reset /var/sandbox/execa/ and re-initialize from scratch
# Leaves other /var/sandbox/<subdir>/ repos untouched.

# Usage: just reset-sandbox
reset-sandbox:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "Resetting /var/sandbox/execa/..."
    if [[ -d /var/sandbox/execa ]]; then
        find /var/sandbox/execa -mindepth 1 -maxdepth 1 -exec rm -rf {} +
    fi
    {{ repo }}/scripts/scaffold-sandbox.sh

# Sync centralized MCP config with ~/.envrc loaded through direnv.

# Usage: just sync-mcp-configs [--dry-run] [--harness codex]
install-mcps *ARGS="":
    #!/usr/bin/env bash
    set -euo pipefail
    cd "{{ repo }}"
    direnv exec "$HOME" python3 mcp/sync_mcp_configs.py {{ ARGS }}

run-microagent *args:
    @cd {{ repo }}/opencode && uv run --python .venv/bin/python -m scripts.run_micro_agent {{ args }}

build-agents:
    @cd {{ repo }}/opencode && uv run --python .venv/bin/python permissions/main.py --build

opencode-plugins-check:
    @cd {{ repo }}/opencode/plugins && bunx tsc --noEmit && bun test tests/unit/ examples/command-interceptor/command-interceptor.test.ts examples/prompt-router/tests/prompt-router.test.ts && bun build --target bun --outdir /tmp/plugin-check local-tools.ts

opencode-plugins-test:
    @cd {{ repo }}/opencode/plugins && bun test tests/unit/ examples/command-interceptor/command-interceptor.test.ts examples/prompt-router/tests/prompt-router.test.ts

opencode-plugins-compile:
    @cd {{ repo }}/opencode/plugins && bun build --target bun --outdir /tmp/plugin-check local-tools.ts

opencode-plugins-classifier:
    @cd {{ repo }}/opencode/plugins && bun run examples/prompt-router/tests/classifier/run.ts

opencode-harness *args:
    @cd {{ repo }}/opencode/plugins/utilities/harness && bun run opx {{ args }}

opencode-session *args:
    @cd {{ repo }}/opencode/plugins && bun run utilities/harness/session-harness.ts {{ args }}

# =============================================================================
# OpenCode Provider Discovery (inline - no scripts)
# =============================================================================

# List all OpenRouter models from models.dev
opencode-openrouter-list:
    @curl -s https://models.dev/api.json | jq -r '.openrouter.models | keys[]'

# List OpenRouter free tier models
opencode-openrouter-free:
    @curl -s https://models.dev/api.json | jq -r '.openrouter.models | to_entries[] | select(.value.tier == "free") | .key'

# List OpenRouter models with tool support
opencode-openrouter-tools:
    @curl -s https://models.dev/api.json | jq -r '.openrouter.models | to_entries[] | select(.value.tools == true) | .key'

# List OpenRouter free models with tool support
opencode-openrouter-free-tools:
    @curl -s https://models.dev/api.json | jq -r '.openrouter.models | to_entries[] | select(.value.tier == "free" and .value.tools == true) | .key'

# Probe a model endpoint for responsiveness

# Usage: just opencode-openrouter-probe mistralai/mistral-small:free
opencode-openrouter-probe model:
    #!/usr/bin/env bash
    set -euo pipefail
    response=$(curl -s https://openrouter.ai/api/v1/chat/completions \
        -H "Authorization: Bearer $OPENROUTER_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"model\":\"$1\",\"messages\":[{\"role\":\"user\",\"content\":\"ping\"}],\"max_tokens\":5}")
    echo "$response" | jq -r 'if .error then "ERROR: \(.error.message)" else "OK" end'

# Test model tool-calling support

# Usage: just opencode-openrouter-probe-tools mistralai/mistral-small:free
opencode-openrouter-probe-tools model:
    #!/usr/bin/env bash
    set -euo pipefail
    response=$(curl -s https://openrouter.ai/api/v1/chat/completions \
        -H "Authorization: Bearer $OPENROUTER_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\":\"$1\",
            \"messages\":[{\"role\":\"user\",\"content\":\"Find files containing auth\"}],
            \"tools\":[{\"type\":\"function\",\"function\":{\"name\":\"search_files\",\"parameters\":{\"type\":\"object\",\"properties\":{\"query\":{\"type\":\"string\"}}}}}]
        }")
    echo "$response" | jq -r 'if .choices[0].message.tool_calls then "SUPPORTS_TOOLS" elif .error then "ERROR: \(.error.message)" else "NO_TOOL_SUPPORT" end'

# Full discovery: list free+tools models and probe each

# Usage: just opencode-openrouter-discover
opencode-openrouter-discover:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "=== OpenRouter Free Models with Tool Support ==="
    models=$(curl -s https://models.dev/api.json | jq -r '.openrouter.models | to_entries[] | select(.value.tier == "free" and .value.tools == true) | .key')
    for model in $models; do
        echo -n "$model: "
        response=$(curl -s https://openrouter.ai/api/v1/chat/completions \
            -H "Authorization: Bearer $OPENROUTER_API_KEY" \
            -H "Content-Type: application/json" \
            -d "{\"model\":\"$model\",\"messages\":[{\"role\":\"user\",\"content\":\"ping\"}],\"max_tokens\":5}")
        echo "$response" | jq -r 'if .error then "DOWN: \(.error.message)" else "UP" end'
    done

# Debug a provider from models.dev

# Usage: just opencode-provider-debug openrouter
opencode-provider-debug provider:
    @curl -s https://models.dev/api.json | jq -r '.{{ provider }}.models | to_entries[] | "  \(.key) - \(.value.name)"'
