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
    @ln -sf {{repo}}/AGENTS.md ~/.claude/CLAUDE.md
    @ln -sf {{repo}}/AGENTS.md ~/.codex/AGENTS.md
    @ln -sf {{repo}}/AGENTS.md ~/.gemini/GEMINI.md
    @ln -sf {{repo}}/AGENTS.md ~/.qwen/QWEN.md
    @ln -sf {{repo}}/AGENTS.md ~/.config/opencode/AGENTS.md
    @ln -sf {{repo}}/AGENTS.md ~/.config/kilo/AGENTS.md
    @ln -sf {{repo}}/AGENTS.md ~/.config/amp/AGENTS.md
    @ln -sf {{repo}}/AGENTS.md ~/.config/AGENTS.md
    @ln -sf {{repo}}/opencode ~/.config/opencode
    @ln -sf {{repo}}/opencode/rate-limit-fallback.json ~/.opencode/rate-limit-fallback.json
    @ln -sf {{repo}}/opencode/configs/cc-safety-net.json ~/.cc-safety-net/config.json
    @mkdir -p ~/.cc-safety-net
    # tmux config symlinks
    @ln -sf {{repo}}/dotfiles/tmux.conf ~/.tmux.conf
    @mkdir -p ~/.config/tmux-powerline/themes
    @ln -sf {{repo}}/dotfiles/tmux-powerline/themes/my-theme.sh ~/.config/tmux-powerline/themes/my-theme.sh
    @ln -sf {{repo}}/dotfiles/tmux-powerline/config.sh ~/.config/tmux-powerline/config.sh
    # Backup existing skills directories before creating symlinks
    @for dir in ~/.claude/skills ~/.codex/skills ~/.gemini/skills ~/.agents/skills ~/.qwen/skills ~/.config/agents/skills ~/.config/amp/skills ~/.kilocode/skills; do \
        if [ -d "$$dir" ] && [ ! -L "$$dir" ]; then \
            mv "$$dir" "$$dir.bak.$(date +%Y%m%d%H%M%S)"; \
        fi; \
    done
    @ln -sf {{repo}}/skills ~/.claude/skills
    @ln -sf {{repo}}/skills ~/.codex/skills
    @ln -sf {{repo}}/skills ~/.gemini/skills
    @ln -sf {{repo}}/skills ~/.agents/skills
    @ln -sf {{repo}}/skills ~/.qwen/skills
    @ln -sf {{repo}}/skills ~/.config/agents/skills
    @ln -sf {{repo}}/skills ~/.config/amp/skills
    @ln -sf {{repo}}/skills ~/.kilocode/skills
    @grep -q 'GEMINI_SYSTEM_MD' ~/.bashrc 2>/dev/null || printf '\n# System prompt overrides for Gemini/Qwen CLI\nexport GEMINI_SYSTEM_MD={{repo}}/prompts/interactive_agents/interactive.md\nexport QWEN_SYSTEM_MD={{repo}}/prompts/interactive_agents/interactive.md\n' >> ~/.bashrc
    @grep -q 'GEMINI_SYSTEM_MD' ~/.zshrc 2>/dev/null || printf '\n# System prompt overrides for Gemini/Qwen CLI\nexport GEMINI_SYSTEM_MD={{repo}}/prompts/interactive_agents/interactive.md\nexport QWEN_SYSTEM_MD={{repo}}/prompts/interactive_agents/interactive.md\n' >> ~/.zshrc
    @echo "✓ Installed"
    @echo ""
    @echo "Context files:    AGENTS.md → all harnesses"
    @echo "Skills:           {{repo}}/skills → all harnesses"
    @echo "System prompts:   GEMINI_SYSTEM_MD, QWEN_SYSTEM_MD → interactive.md (absolute path)"
    @echo "Env vars:         GEMINI_SYSTEM_MD, QWEN_SYSTEM_MD → bashrc, zshrc"
    @echo "OpenCode:         .opencode/ → ~/.config/opencode"
    @echo "Safety Net:       opencode/configs/cc-safety-net.json → ~/.cc-safety-net/config.json"

# Scaffold /var/sandbox/execa/ if not already initialized (idempotent)
# /var/sandbox/ is a plain dir hosting multiple project repos on demand.
# Usage: just sandbox
create-sandbox:
    @{{repo}}/scripts/scaffold-sandbox.sh

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
    {{repo}}/scripts/scaffold-sandbox.sh

# Sync centralized MCP config with ~/.envrc loaded through direnv.
# Usage: just sync-mcp-configs [--dry-run] [--harness codex]
sync-mcp-configs *ARGS="":
    #!/usr/bin/env bash
    set -euo pipefail
    cd "{{repo}}"
    direnv exec "$HOME" python3 mcp/sync_mcp_configs.py {{ARGS}}

# Check all usage limits
# Usage: just usage [--json] [--no-notify]
usage *ARGS="":
    @python {{repo}}/usage-limits/claude_usage.py {{ARGS}}
    @python {{repo}}/usage-limits/codex_usage.py {{ARGS}}
    @python {{repo}}/usage-limits/amp_usage.py {{ARGS}}
    @python {{repo}}/usage-limits/antigravity_usage.py {{ARGS}}
    @python {{repo}}/usage-limits/qwen_usage.py {{ARGS}}

# Check Codex usage limits
# Usage: just codex-usage [--json] [--no-notify]
codex-usage *ARGS="":
    @python {{repo}}/usage-limits/codex_usage.py {{ARGS}}

# Check Amp usage limits
# Usage: just amp-usage [--json] [--no-notify]
amp-usage *ARGS="":
    @python {{repo}}/usage-limits/amp_usage.py {{ARGS}}

# Check Antigravity usage limits
# Usage: just antigravity-usage [--json] [--no-notify]
antigravity-usage *ARGS="":
    @python {{repo}}/usage-limits/antigravity_usage.py {{ARGS}}

# Check Qwen usage limits
# Usage: just qwen-usage [--json] [--no-notify]
qwen-usage *ARGS="":
    @python {{repo}}/usage-limits/qwen_usage.py {{ARGS}}

# =============================================================================
# OpenCode (opencode/)
# =============================================================================

opencode-permissions-apply:
    @python {{repo}}/opencode/scripts/manage_permissions.py --apply

opencode-config-build:
    @python {{repo}}/opencode/scripts/build_config.py

opencode-rebuild: opencode-permissions-apply opencode-config-build

opencode-providers-validate *args="":
    @python {{repo}}/opencode/configs/providers/scripts/validate_models_dev.py {{args}}

opencode-openrouter-sync:
    @python {{repo}}/opencode/configs/providers/scripts/sync_openrouter_models.py

opencode-openrouter-probe-endpoints *args="":
    @python {{repo}}/opencode/configs/providers/scripts/probe_openrouter_endpoints.py {{args}}

opencode-openrouter-probe-tool-calling *args="":
    @python {{repo}}/opencode/configs/providers/scripts/probe_openrouter_tool_calling.py {{args}}

opencode-providers-debug provider="opencode":
    @python {{repo}}/opencode/configs/providers/scripts/debug_models_dev_provider.py {{provider}}

opencode-run-agent *args:
    @python {{repo}}/scripts/run_micro_agent.py {{args}}

opencode-plugins-check:
    @cd {{repo}}/opencode/plugins && bunx tsc --noEmit && bun test tests/unit/ examples/command-interceptor/command-interceptor.test.ts examples/prompt-router/tests/prompt-router.test.ts && bun build --target bun --outdir /tmp/plugin-check local-tools.ts

opencode-plugins-typecheck:
    @cd {{repo}}/opencode/plugins && bunx tsc --noEmit

opencode-plugins-test:
    @cd {{repo}}/opencode/plugins && bun test tests/unit/ examples/command-interceptor/command-interceptor.test.ts examples/prompt-router/tests/prompt-router.test.ts

opencode-plugins-compile:
    @cd {{repo}}/opencode/plugins && bun build --target bun --outdir /tmp/plugin-check local-tools.ts

opencode-plugins-classifier:
    @cd {{repo}}/opencode/plugins && bun run examples/prompt-router/tests/classifier/run.ts

opencode-plugins-classifier-model model:
    @cd {{repo}}/opencode/plugins && bun run examples/prompt-router/tests/classifier/run.ts {{model}}

opencode-plugins-classifier-mdjson model:
    @cd {{repo}}/opencode/plugins && bun run examples/prompt-router/tests/classifier/run.ts {{model}} --mode MD_JSON

opencode-plugins-behavior tier:
    @cd {{repo}}/opencode/plugins && PROMPT_ROUTER_ENABLED=true bash examples/prompt-router/tests/behavior/run.sh {{tier}}

opencode-plugins-baseline tier:
    @cd {{repo}}/opencode/plugins && PROMPT_ROUTER_ENABLED=false bash examples/prompt-router/tests/behavior/run.sh {{tier}}

opencode-plugins-callback-integration:
    @cd {{repo}}/opencode/plugins && bun test tests/unit/callback-integration.test.ts

opencode-harness *args:
    @cd {{repo}}/opencode/plugins/utilities/harness && bun run opx {{args}}

opencode-session *args:
    @cd {{repo}}/opencode/plugins && bun run utilities/harness/session-harness.ts {{args}}

opencode-snapshot-gc:
    @bash {{repo}}/opencode/scripts/maintenance/opencode_gc.sh
