set fallback := true
set script-interpreter := ['uv', 'run', '--script']

# Install symlinks for all CLI harnesses
# Usage: just install

repo := env_var_or_default("REPO", env_var("HOME") / "ai")

# Show available recipes

# Usage: just
default:
    @just --list

# Install all symlinks and environment variables
install:
    #!/usr/bin/env bash
    set -euo pipefail
    mkdir -p ~/.claude ~/.codex ~/.gemini ~/.qwen ~/.config/opencode ~/.config/kilo ~/.config/amp ~/.config ~/.agents ~/.kilocode ~/.opencode
    ln -sf {{ repo }}/AGENTS.md ~/.claude/CLAUDE.md
    ln -sf {{ repo }}/AGENTS.md ~/.codex/AGENTS.md
    ln -sf {{ repo }}/AGENTS.md ~/.gemini/GEMINI.md
    ln -sf {{ repo }}/AGENTS.md ~/.qwen/QWEN.md
    ln -sf {{ repo }}/AGENTS.md ~/.config/opencode/AGENTS.md
    ln -sf {{ repo }}/AGENTS.md ~/.config/kilo/AGENTS.md
    ln -sf {{ repo }}/AGENTS.md ~/.config/amp/AGENTS.md
    ln -sf {{ repo }}/AGENTS.md ~/.config/AGENTS.md
    ln -sf {{ repo }}/opencode ~/.config/opencode
    ln -sf {{ repo }}/opencode/rate-limit-fallback.json ~/.opencode/rate-limit-fallback.json
    ln -sf {{ repo }}/opencode/configs/cc-safety-net.json ~/.cc-safety-net/config.json
    mkdir -p ~/.cc-safety-net
    
    # Linter/formatter configurations
    mkdir -p ~/.config/ruff ~/.config/black ~/.config/mypy ~/.config/eslint ~/.config/prettier
    ln -sf {{ repo }}/linter-configs/ruff-global.toml ~/.config/ruff/ruff.toml
    ln -sf {{ repo }}/linter-configs/mypy-global.ini ~/.mypy.ini
    ln -sf {{ repo }}/linter-configs/black-global.toml ~/.config/black/black.toml
    ln -sf {{ repo }}/linter-configs/eslint-global.json ~/.eslintrc.json
    ln -sf {{ repo }}/linter-configs/prettier-global.json ~/.prettierrc
    
    # tmux config symlinks
    ln -sf {{ repo }}/dotfiles/tmux.conf ~/.tmux.conf
    mkdir -p ~/.config/tmux-powerline/themes
    ln -sf {{ repo }}/dotfiles/tmux-powerline/themes/my-theme.sh ~/.config/tmux-powerline/themes/my-theme.sh
    ln -sf {{ repo }}/dotfiles/tmux-powerline/config.sh ~/.config/tmux-powerline/config.sh
    # Backup existing skills directories before creating symlinks
    for dir in ~/.claude/skills ~/.codex/skills ~/.gemini/skills ~/.agents/skills ~/.qwen/skills ~/.config/agents/skills ~/.config/amp/skills ~/.kilocode/skills; do \
        if [ -d "$$dir" ] && [ ! -L "$$dir" ]; then \
            mv "$$dir" "$$dir.bak.$(date +%Y%m%d%H%M%S)"; \
        fi; \
    done
    ln -sf {{ repo }}/skills ~/.claude/skills
    ln -sf {{ repo }}/skills ~/.codex/skills
    ln -sf {{ repo }}/skills ~/.gemini/skills
    ln -sf {{ repo }}/skills ~/.agents/skills
    ln -sf {{ repo }}/skills ~/.qwen/skills
    ln -sf {{ repo }}/skills ~/.config/agents/skills
    ln -sf {{ repo }}/skills ~/.config/amp/skills
    ln -sf {{ repo }}/skills ~/.kilocode/skills
    mkdir -p ~/.cache/ai-prompts/system-prompts
    cd {{ repo }}/opencode && uv run ai-prompts get interactive-agents/interactive > ~/.cache/ai-prompts/system-prompts/interactive.md
    just --justfile {{ repo }}/justfile _update-shell-rc
    echo "✓ Installed"
    echo ""
    echo "Context files:    AGENTS.md → all harnesses"
    echo "Skills:           {{ repo }}/skills → all harnesses"
    echo "System prompts:   GEMINI_SYSTEM_MD, QWEN_SYSTEM_MD → cached ai-prompts interactive slug"
    echo "Env vars:         GEMINI_SYSTEM_MD, QWEN_SYSTEM_MD → bashrc, zshrc"
    echo "OpenCode:         .opencode/ → ~/.config/opencode"
    echo "Safety Net:       opencode/configs/cc-safety-net.json → ~/.cc-safety-net/config.json"
    echo "Linter configs:   linter-configs/ → ~/.config/ (ruff, black, mypy, eslint, prettier)"

# Update shell rc files with system prompt env vars (internal recipe)
_update-shell-rc:
    #!/usr/bin/env python3
    from pathlib import Path
    import re

    prompt_path = str((Path.home() / ".cache/ai-prompts/system-prompts/interactive.md").resolve())
    marker = "# System prompt overrides for Gemini/Qwen CLI"
    block = (
        f"\n{marker}\n"
        f"export GEMINI_SYSTEM_MD={prompt_path}\n"
        f"export QWEN_SYSTEM_MD={prompt_path}\n"
    )
    pattern = re.compile(
        r"\n# System prompt overrides for Gemini/Qwen CLI\n"
        r"export GEMINI_SYSTEM_MD=.*\n"
        r"export QWEN_SYSTEM_MD=.*\n?",
        re.MULTILINE,
    )
    for rc_name in (".bashrc", ".zshrc"):
        rc_path = Path.home() / rc_name
        text = rc_path.read_text() if rc_path.exists() else ""
        if marker in text:
            text = pattern.sub(block, text, count=1)
        else:
            text = text.rstrip("\n") + block
        rc_path.write_text(text.rstrip("\n") + "\n")

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

run-microagent *args:
    @cd {{ repo }}/opencode && uv run --python .venv/bin/python llm-run {{ args }}


build-agents: check-plugins
    @cd {{ repo }}/opencode && uv run --python .venv/bin/python permissions/main.py build

build-permissions: check-plugins
    @cd {{ repo }}/opencode && uv run --python .venv/bin/python permissions/main.py apply

build-config: check-plugins
    @cd {{ repo }}/opencode && uv run --python .venv/bin/python scripts/build_config.py

check-plugins:
    @cd {{ repo }}/opencode/plugins && bun run scripts/preflight.ts

# =============================================================================
# AGENTS.md Template
# =============================================================================

# Compile system/AGENTS template and write body to ~/ai/AGENTS.md
[script]
build-agents-md:
    # /// script
    # requires-python = ">=3.11"
    # dependencies = ["tiktoken", "pyyaml", "jinja2"]
    # ///
    import sys
    sys.path.insert(0, "{{ repo }}/../opencode-plugins/ai-prompts/src")
    import os
    import tiktoken
    os.environ["PROMPTS_DIR"] = "{{ repo }}/../opencode-plugins/ai-prompts/prompts"
    from ai_prompts import get_prompt
    p = get_prompt("system/AGENTS")
    body = p.body
    count = len(tiktoken.get_encoding("cl100k_base").encode(body))
    with open("{{ repo }}/AGENTS.md", "w") as f:
        f.write(body)
    print(f"Wrote {{ repo }}/AGENTS.md ({count} tokens)")

# =============================================================================
# Linting & Formatting
# =============================================================================

# Python Linting (ruff check)
lint-python *args:
    uvx ruff check {{ args }}

# Python Formatting (ruff format)
fmt-python *args:
    uvx ruff format {{ args }}

# Python Type Checking (mypy)
mypy *args:
    uvx mypy {{ args }}

# JS/TS Linting (eslint)
lint-js *args:
    npx eslint {{ args }}

# JS/TS Formatting (prettier)
fmt-js *args:
    npx prettier --write {{ args }}
