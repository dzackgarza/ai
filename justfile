set fallback := true
set script-interpreter := ['uv', 'run', '--script']

# Install symlinks for all CLI harnesses
# Usage: just install

repo := env_var_or_default("REPO", env_var("HOME") / "ai")
home := env_var("HOME")

# Repository targets (top-level source of truth)

opencode_dir := repo / "opencode"
quality_control_dir := repo / "quality-control"
dotfiles_dir := repo / "dotfiles"

# Core assets

agents_md := opencode_dir / "AGENTS.md"
skills_dir := opencode_dir / "skills"

# Linter/formatter configurations

ruff_config := quality_control_dir / "ruff-global.toml"
mypy_config := quality_control_dir / "mypy-global.ini"
black_config := quality_control_dir / "black-global.toml"
eslint_config := quality_control_dir / "eslint-global.json"
prettier_config := quality_control_dir / "prettier-global.json"

# Tool configs

cc_safety_net := opencode_dir / "configs" / "cc-safety-net.json"
tmux_conf := dotfiles_dir / "tmux.conf"
tmux_powerline_config := dotfiles_dir / "tmux-powerline" / "config.sh"
tmux_powerline_theme := dotfiles_dir / "tmux-powerline" / "themes" / "my-theme.sh"

# Harness home directories

claude_home := home / ".claude"
codex_home := home / ".codex"
gemini_home := home / ".gemini"
qwen_home := home / ".qwen"
opencode_home := home / ".config/opencode"
kilo_home := home / ".config/kilo"
amp_home := home / ".config/amp"
agents_home := home / ".agents"
kilocode_home := home / ".kilocode"
opencode_root := home / ".opencode"
cc_safety_net_home := home / ".cc-safety-net"

# Show available recipes

# Usage: just
default:
    @just --list

# Install all symlinks and environment variables
install:
    #!/usr/bin/env bash
    set -euo pipefail

    # Assertion of existence
    echo "Verifying repository targets..."
    for target in "{{ agents_md }}" "{{ skills_dir }}" "{{ ruff_config }}" "{{ mypy_config }}" \
                  "{{ black_config }}" "{{ eslint_config }}" "{{ prettier_config }}" \
                  "{{ cc_safety_net }}" "{{ tmux_conf }}" "{{ tmux_powerline_config }}" \
                  "{{ tmux_powerline_theme }}"; do
        if [ ! -e "$target" ]; then
            echo "Error: Target $target does not exist. Aborting."
            exit 1
        fi
    done
    echo "✓ All repository targets exist."

    mkdir -p "{{ claude_home }}" "{{ codex_home }}" "{{ gemini_home }}" "{{ qwen_home }}" \
             "{{ opencode_home }}" "{{ kilo_home }}" "{{ amp_home }}" "{{ agents_home }}" \
             "{{ kilocode_home }}" "{{ opencode_root }}" "{{ cc_safety_net_home }}"

    ln -snf "{{ agents_md }}" "{{ claude_home }}/CLAUDE.md"
    ln -snf "{{ agents_md }}" "{{ codex_home }}/AGENTS.md"
    ln -snf "{{ agents_md }}" "{{ gemini_home }}/GEMINI.md"
    ln -snf "{{ agents_md }}" "{{ qwen_home }}/QWEN.md"
    ln -snf "{{ agents_md }}" "{{ kilo_home }}/AGENTS.md"
    ln -snf "{{ agents_md }}" "{{ amp_home }}/AGENTS.md"
    ln -snf "{{ agents_md }}" "{{ home }}/.config/AGENTS.md"
    ln -snf "{{ opencode_dir }}" "{{ opencode_home }}"
    ln -snf "{{ opencode_dir }}/rate-limit-fallback.json" "{{ opencode_root }}/rate-limit-fallback.json"
    ln -snf "{{ cc_safety_net }}" "{{ cc_safety_net_home }}/config.json"

    # Linter/formatter configurations
    mkdir -p "{{ home }}/.config/ruff" "{{ home }}/.config/black"
    ln -snf "{{ ruff_config }}" "{{ home }}/.config/ruff/ruff.toml"
    ln -snf "{{ mypy_config }}" "{{ home }}/.mypy.ini"
    ln -snf "{{ black_config }}" "{{ home }}/.config/black/black.toml"
    ln -snf "{{ eslint_config }}" "{{ home }}/.eslintrc.json"
    ln -snf "{{ prettier_config }}" "{{ home }}/.prettierrc"

    # tmux config symlinks
    ln -snf "{{ tmux_conf }}" "{{ home }}/.tmux.conf"
    mkdir -p "{{ home }}/.config/tmux-powerline/themes"
    ln -snf "{{ tmux_powerline_theme }}" "{{ home }}/.config/tmux-powerline/themes/my-theme.sh"
    ln -snf "{{ tmux_powerline_config }}" "{{ home }}/.config/tmux-powerline/config.sh"

    # Backup existing skills directories before creating symlinks
    for dir in "{{ claude_home }}/skills" "{{ codex_home }}/skills" \
               "{{ agents_home }}/skills" "{{ qwen_home }}/skills" "{{ home }}/.config/agents/skills" \
               "{{ amp_home }}/skills" "{{ kilocode_home }}/skills"; do
        if [ -d "$dir" ] && [ ! -L "$dir" ]; then
            mv "$dir" "$dir.bak.$(date +%Y%m%d%H%M%S)"
        fi
    done
    ln -snf "{{ skills_dir }}" "{{ claude_home }}/skills"
    ln -snf "{{ skills_dir }}" "{{ codex_home }}/skills"
    ln -snf "{{ skills_dir }}" "{{ agents_home }}/skills"
    ln -snf "{{ skills_dir }}" "{{ qwen_home }}/skills"
    ln -snf "{{ skills_dir }}" "{{ home }}/.config/agents/skills"
    ln -snf "{{ skills_dir }}" "{{ amp_home }}/skills"
    ln -snf "{{ skills_dir }}" "{{ kilocode_home }}/skills"

    just --justfile {{ repo }}/justfile _update-shell-rc

    echo "✓ Environment installed"
    echo ""
    echo "Symlink targets (actual):"
    printf "%-30s -> %s\n" "~/.gemini/GEMINI.md" "$(readlink {{ gemini_home }}/GEMINI.md)"
    printf "%-30s -> %s\n" "~/.config/opencode" "$(readlink {{ opencode_home }})"
    printf "%-30s -> %s\n" "~/.config/ruff/ruff.toml" "$(readlink {{ home }}/.config/ruff/ruff.toml)"
    printf "%-30s -> %s\n" "~/.config/black/black.toml" "$(readlink {{ home }}/.config/black/black.toml)"
    printf "%-30s -> %s\n" "~/.mypy.ini" "$(readlink {{ home }}/.mypy.ini)"
    printf "%-30s -> %s\n" "~/.eslintrc.json" "$(readlink {{ home }}/.eslintrc.json)"
    printf "%-30s -> %s\n" "~/.prettierrc" "$(readlink {{ home }}/.prettierrc)"
    printf "%-30s -> %s\n" "~/.cc-safety-net/config.json" "$(readlink {{ cc_safety_net_home }}/config.json)"
    echo ""
    echo "System prompts (actual):"
    [ -f ~/.bashrc ] && grep "export GEMINI_SYSTEM_MD=" ~/.bashrc | tail -n 1
    [ -f ~/.bashrc ] && grep "export QWEN_SYSTEM_MD=" ~/.bashrc | tail -n 1
    [ -f ~/.zshrc ] && grep "export GEMINI_SYSTEM_MD=" ~/.zshrc | tail -n 1
    [ -f ~/.zshrc ] && grep "export QWEN_SYSTEM_MD=" ~/.zshrc | tail -n 1

# Update shell rc files with system prompt env vars (internal recipe)
_update-shell-rc:
    #!/usr/bin/env python3
    from pathlib import Path
    import re

    repo_root = Path("{{ repo }}").resolve()
    prompt_path = str((repo_root / "opencode/agents/interactive.md").resolve())
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

# Build all OpenCode components (agents, config, and documentation)
build: check-plugins build-agents build-config build-agents-md

# Surgical build for permissions only (uses compiled-agents workflow)
build-permissions:
    @just -f {{ repo }}/../opencode-plugins/clis/ai-prompts/justfile compile-agents
    @cd {{ repo }}/opencode && uv run --python .venv/bin/python permissions/main.py build

# Surgical build for config only (depends on permissions for skeleton update)
build-config: build-permissions
    @cd {{ repo }}/opencode && uv run --python .venv/bin/python scripts/build_config.py

# Build agent permission files (depends on config being built)
build-agents: build-permissions
    @echo "Agents built via build-permissions"

check-plugins:
    @cd {{ repo }}/opencode/plugins && bun run scripts/preflight.ts

# =============================================================================
# AGENTS.md Template
# =============================================================================

# Compile system/AGENTS template and write body to ~/ai/opencode/AGENTS.md
build-agents-md:
    @uvx --from git+https://github.com/dzackgarza/ai-prompts.git ai-prompts get system/AGENTS --json \
      | jq -r '.body' \
      | tee {{ repo }}/opencode/AGENTS.md \
      | wc -c \
      | xargs -I {} echo "Wrote {{ repo }}/opencode/AGENTS.md ({} bytes)"
    @just --justfile {{ justfile() }} _count-agents-tokens

# Count tokens in AGENTS.md using tiktoken (cl100k_base)
[private]
_count-agents-tokens:
    @uvx --with tiktoken python -c 'import tiktoken; from pathlib import Path; text = Path("{{ repo }}/opencode/AGENTS.md").read_text(); count = len(tiktoken.get_encoding("cl100k_base").encode(text)); print(f"{count} tokens")'

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

# =============================================================================
# Diagnostics
# =============================================================================
# Find broken symlinks in ~ (skips common ignored dirs)

# Usage: just broken-symlinks
broken-symlinks:
    #!/usr/bin/env bash
    set -euo pipefail

    # Directories to skip (common caches, build artifacts, gitignored dirs)
    skip_dirs=(
        "node_modules"
        "__pycache__"
        ".git"
        ".cache"
        ".npm"
        ".yarn"
        ".pnpm-store"
        ".venv"
        "venv"
        ".conda"
        ".local/share/virtualenvs"
        ".cargo"
        "target"
        "build"
        "dist"
        ".next"
        ".nuxt"
        ".turbo"
        ".swc"
        ".eslintcache"
        ".pytest_cache"
        ".mypy_cache"
        ".ruff_cache"
        ".coverage"
        "htmlcov"
        ".tox"
        ".eggs"
        "*.egg-info"
        ".sass-cache"
        ".DS_Store"
        "Thumbs.db"
        ".idea"
        ".vscode"
        ".vs"
        "logs"
        "tmp"
        "temp"
        ".tmp"
        ".temp"
        ".babel-cache"
        ".parcel-cache"
        ".vercel"
        ".netlify"
        ".firebase"
        ".amplify"
        ".serverless"
        ".wrangler"
        ".deno"
        ".bun"
        ".nx"
        ".turbo"
        "Trash"
        ".Trash"
        ".local/share/Trash"
    )

    # Build find command with -prune for each skip dir
    prune_expr=""
    for dir in "${skip_dirs[@]}"; do
        prune_expr="$prune_expr -name '$dir' -prune -o"
    done

    # Find all symlinks, test if target exists, report broken ones
    eval "find ~ $prune_expr -type l" 2>/dev/null | while read -r link; do
        if [ ! -e "$link" ]; then
            target=$(readlink "$link")
            printf "BROKEN: %s -> %s\n" "$link" "$target"
        fi
    done | sort

# Check markdown files for broken local file references

# Usage: just check-markdown [directory]
check-markdown *args:
    #!/usr/bin/env bash
    set -euo pipefail

    # Default to current directory if no args provided
    search_dir="${1:-.}"

    # Directories to skip (same as broken-symlinks)
    skip_dirs=(
        "node_modules"
        "__pycache__"
        ".git"
        ".cache"
        ".npm"
        ".yarn"
        ".pnpm-store"
        ".venv"
        "venv"
        ".conda"
        ".local/share/virtualenvs"
        ".cargo"
        "target"
        "build"
        "dist"
        ".next"
        ".nuxt"
        ".turbo"
        ".swc"
        ".eslintcache"
        ".pytest_cache"
        ".mypy_cache"
        ".ruff_cache"
        ".coverage"
        "htmlcov"
        ".tox"
        ".eggs"
        "*.egg-info"
        ".sass-cache"
        ".DS_Store"
        "Thumbs.db"
        ".idea"
        ".vscode"
        ".vs"
        "logs"
        "tmp"
        "temp"
        ".tmp"
        ".temp"
        ".babel-cache"
        ".parcel-cache"
        ".vercel"
        ".netlify"
        ".firebase"
        ".amplify"
        ".serverless"
        ".wrangler"
        ".deno"
        ".bun"
        ".nx"
        ".turbo"
        "Trash"
        ".Trash"
        ".local/share/Trash"
    )

    # Build find command with -prune for each skip dir
    prune_expr=""
    for dir in "${skip_dirs[@]}"; do
        prune_expr="$prune_expr -name '$dir' -prune -o"
    done

    # Find all markdown files and pass to lychee
    echo "Checking markdown files in: $search_dir"
    eval "find '$search_dir' $prune_expr -type f \( -name '*.md' -o -name '*.markdown' -o -name '*.mdx' \) -print0" 2>/dev/null | \
        xargs -0 lychee --no-progress
