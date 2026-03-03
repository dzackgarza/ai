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
    @ln -sf {{repo}}/opencode/cc-safety-net.json ~/.cc-safety-net/config.json
    @mkdir -p ~/.cc-safety-net
    # tmux config symlinks
    @ln -sf {{repo}}/dotfiles/tmux.conf ~/.tmux.conf
    @mkdir -p ~/.config/tmux-powerline/themes
    @ln -sf {{repo}}/dotfiles/tmux-powerline/themes/my-theme.sh ~/.config/tmux-powerline/themes/my-theme.sh
    @ln -sf {{repo}}/dotfiles/tmux-powerline/config.sh ~/.config/tmux-powerline/config.sh
    # Backup existing skills directories before creating symlinks
    @for dir in ~/.claude/skills ~/.gemini/skills ~/.agents/skills ~/.qwen/skills ~/.config/agents/skills ~/.config/amp/skills ~/.kilocode/skills; do \
        if [ -d "$$dir" ] && [ ! -L "$$dir" ]; then \
            mv "$$dir" "$$dir.bak.$(date +%Y%m%d%H%M%S)"; \
        fi; \
    done
    @ln -sf {{repo}}/skills ~/.claude/skills
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
    @echo "Safety Net:       cc-safety-net.json → ~/.cc-safety-net/config.json"

# Scaffold /var/sandbox/execa/ if not already initialized (idempotent)
# /var/sandbox/ is a plain dir hosting multiple project repos on demand.
# Usage: just sandbox
sandbox:
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
