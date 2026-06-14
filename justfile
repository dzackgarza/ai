set fallback := true
set script-interpreter := ['uv', 'run', '--script']
qc-type := "python"

# Install symlinks for all CLI harnesses
# Usage: just install

repo := env_var_or_default("REPO", env_var("HOME") / "ai")
home := env_var("HOME")

# Repository targets (top-level source of truth)

opencode_dir := repo / "opencode"
dotfiles_dir := repo / "dotfiles"

# Core assets

agents_md := opencode_dir / "AGENTS.md"
skills_dir := opencode_dir / "skills"

# Tool configs

cc_safety_net := opencode_dir / "configs" / "cc-safety-net.json"
opencode_permission_policy_config_dir := opencode_dir / "configs" / "opencode-permission-policy-compiler"
tmux_conf := dotfiles_dir / "tmux.conf"
tmux_powerline_config := dotfiles_dir / "tmux-powerline" / "config.sh"
tmux_powerline_theme := dotfiles_dir / "tmux-powerline" / "themes" / "my-theme.sh"

# Harness home directories

claude_home := home / ".claude"
codex_home := home / ".codex"
gemini_home := home / ".gemini"
qoder_home := home / ".qoder"
opencode_home := home / ".config/opencode"
opencode_permission_policy_home := home / ".config/opencode-permission-policy-compiler"
kilo_home := home / ".config/kilo"
agents_home := home / ".agents"
kilocode_home := home / ".kilocode"
opencode_root := home / ".opencode"
cc_safety_net_home := home / ".cc-safety-net"
managed_agents_dir := env_var_or_default("AGENTS_DIR", opencode_dir / "agents")
ai_prompts_source := "git+https://github.com/dzackgarza/ai-prompts.git"
policy_compiler_dir := repo / "../opencode-plugins/clis/opencode-permission-policy-compiler"

# Show available recipes

# Usage: just
default:
    @just --list

test:
    @just --justfile {{ justfile() }} check-markdown README.md AGENTS.md

# Install all symlinks and environment variables
install:
    #!/usr/bin/env bash
    set -euo pipefail

    # Assertion of existence
    echo "Verifying repository targets..."
    for target in "{{ agents_md }}" "{{ skills_dir }}" \
                  "{{ cc_safety_net }}" "{{ opencode_permission_policy_config_dir }}/config.toml" \
                  "{{ tmux_conf }}" "{{ tmux_powerline_config }}" \
                  "{{ tmux_powerline_theme }}"; do
        if [ ! -e "$target" ]; then
            echo "Error: Target $target does not exist. Aborting."
            exit 1
        fi
    done
    echo "✓ All repository targets exist."

    mkdir -p "{{ claude_home }}" "{{ codex_home }}" "{{ gemini_home }}" \
             "{{ qoder_home }}" "{{ opencode_home }}" "{{ kilo_home }}" \
             "{{ agents_home }}" "{{ kilocode_home }}" "{{ opencode_root }}" \
             "{{ cc_safety_net_home }}"

    ln -snf "{{ agents_md }}" "{{ claude_home }}/CLAUDE.md"
    ln -snf "{{ agents_md }}" "{{ codex_home }}/AGENTS.md"
    ln -snf "{{ agents_md }}" "{{ gemini_home }}/GEMINI.md"
    ln -snf "{{ agents_md }}" "{{ kilo_home }}/AGENTS.md"
    ln -snf "{{ agents_md }}" "{{ home }}/.config/AGENTS.md"
    ln -snf "{{ agents_md }}" "{{ gemini_home }}/AGENTS.md"
    ln -snf "{{ opencode_dir }}" "{{ opencode_home }}"
    if [ -d "{{ opencode_permission_policy_home }}" ] && [ ! -L "{{ opencode_permission_policy_home }}" ]; then
        mv "{{ opencode_permission_policy_home }}" "{{ opencode_permission_policy_home }}.bak.$(date +%Y%m%d%H%M%S)"
    fi
    ln -snf "{{ opencode_permission_policy_config_dir }}" "{{ opencode_permission_policy_home }}"
    ln -snf "{{ opencode_dir }}/rate-limit-fallback.json" "{{ opencode_root }}/rate-limit-fallback.json"
    ln -snf "{{ cc_safety_net }}" "{{ cc_safety_net_home }}/config.json"

    # tmux config symlinks
    ln -snf "{{ tmux_conf }}" "{{ home }}/.tmux.conf"
    mkdir -p "{{ home }}/.config/tmux-powerline/themes"
    ln -snf "{{ tmux_powerline_theme }}" "{{ home }}/.config/tmux-powerline/themes/my-theme.sh"
    ln -snf "{{ tmux_powerline_config }}" "{{ home }}/.config/tmux-powerline/config.sh"

    # Merge existing qoder skills into repo before symlinking
    if [ -d "{{ qoder_home }}/skills" ] && [ ! -L "{{ qoder_home }}/skills" ]; then
        echo "Found existing Qoder skills at {{ qoder_home }}/skills"
        for skill_dir in "{{ qoder_home }}/skills"/*/; do
            if [ -d "$skill_dir" ] && [ -f "$skill_dir/SKILL.md" ]; then
                skill_name=$(basename "$skill_dir")
                target="{{ skills_dir }}/$skill_name"
                if [ -d "$target" ]; then
                    echo "  Skill '$skill_name' already exists in repo (delete ours to adopt theirs)"
                else
                    echo "  Importing Qoder skill '$skill_name' into repo"
                    cp -r "$skill_dir" "$target"
                fi
            fi
        done
    fi

    # Backup existing skills directories before creating symlinks
    for dir in "{{ claude_home }}/skills" "{{ codex_home }}/skills" \
               "{{ agents_home }}/skills" "{{ home }}/.config/agents/skills" \
               "{{ kilocode_home }}/skills" "{{ qoder_home }}/skills" \
               "{{ gemini_home }}/skills" "{{ gemini_home }}/antigravity-cli/skills"; do
        if [ -d "$dir" ] && [ ! -L "$dir" ]; then
            mv "$dir" "$dir.bak.$(date +%Y%m%d%H%M%S)"
        fi
    done
    ln -snf "{{ skills_dir }}" "{{ claude_home }}/skills"
    ln -snf "{{ skills_dir }}" "{{ codex_home }}/skills"
    ln -snf "{{ skills_dir }}" "{{ agents_home }}/skills"
    ln -snf "{{ skills_dir }}" "{{ home }}/.config/agents/skills"
    ln -snf "{{ skills_dir }}" "{{ kilocode_home }}/skills"
    ln -snf "{{ skills_dir }}" "{{ qoder_home }}/skills"
    mkdir -p "{{ gemini_home }}/antigravity-cli"
    ln -snf "{{ skills_dir }}" "{{ gemini_home }}/antigravity-cli/skills"
    ln -snf "{{ skills_dir }}" "{{ gemini_home }}/skills"

    just --justfile {{ repo }}/justfile _update-shell-rc

    echo "✓ Environment installed"
    echo ""
    echo "Symlink targets (actual):"
    printf "%-30s -> %s\n" "~/.gemini/GEMINI.md" "$(readlink {{ gemini_home }}/GEMINI.md)"
    printf "%-30s -> %s\n" "~/.gemini/AGENTS.md" "$(readlink {{ gemini_home }}/AGENTS.md)"
    printf "%-30s -> %s\n" "~/.config/opencode" "$(readlink {{ opencode_home }})"
    printf "%-30s -> %s\n" "~/.config/opencode-permission-policy-compiler" "$(readlink {{ opencode_permission_policy_home }})"
    printf "%-30s -> %s\n" "~/.cc-safety-net/config.json" "$(readlink {{ cc_safety_net_home }}/config.json)"
    echo ""
    echo "System prompts (actual):"
    [ -f ~/.bashrc ] && grep "export GEMINI_SYSTEM_MD=" ~/.bashrc | tail -n 1
    [ -f ~/.zshrc ] && grep "export GEMINI_SYSTEM_MD=" ~/.zshrc | tail -n 1

# Update shell rc files with system prompt env vars (internal recipe)
_update-shell-rc:
    #!/usr/bin/env python3
    from pathlib import Path
    import re

    repo_root = Path("{{ repo }}").resolve()
    prompt_path = str((repo_root / "opencode/agents/interactive.md").resolve())
    marker = "# System prompt override for Gemini CLI"
    block = (
        f"\n{marker}\n"
        f"export GEMINI_SYSTEM_MD={prompt_path}\n"
    )
    pattern = re.compile(
        r"\n# System prompt override for Gemini CLI\n"
        r"export GEMINI_SYSTEM_MD=.*\n?",
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

# Build the full OpenCode pipeline in canonical order.
# Usage: just build
# Steps:
#   1. build-config — compile opencode.json from skeleton + provider fragments, apply global permission policy
#   2. build-agents — fetch ai-prompts slugs, compile managed agent markdown
#   3. _build-opencode-agents-md — render AGENTS.md template and count tokens
build: build-config build-agents _build-opencode-agents-md

# Build only the compiled OpenCode config pipeline.
# Usage: just build-config
# Steps:
#   1. _build-opencode-inject-agent-ext-dirs — sync external_directory whitelist from skeleton into primary agents
#   2. _build-opencode-config-compile — compile opencode.json from source config fragments
#   3. _build-opencode-config-apply-policy — apply global permission baseline to compiled config
build-config:
    @just --justfile {{ justfile() }} _build-opencode-inject-agent-ext-dirs
    @just --justfile {{ justfile() }} _build-opencode-config-compile
    # @just --justfile {{ justfile() }} _build-opencode-config-apply-policy

# Build only the managed OpenCode agent markdown files.
# Usage: just build-agents
# Steps:
#   - Fetch each published ai-prompts slug (autonomous, orchestrator, build, plan, etc.)
#   - Compile prompt permissions with external policy compiler
#   - Write generated markdown to managed agents directory
build-agents:
    @just --justfile {{ justfile() }} _build-opencode-managed-agents

[private]
_build-opencode-inject-agent-ext-dirs:
    @cd {{ repo }}/opencode && uv run --python .venv/bin/python scripts/inject_agent_permissions.py

[private]
_build-opencode-config-compile:
    @cd {{ repo }}/opencode && uv run --python .venv/bin/python scripts/build_config.py

[private]
_build-opencode-config-apply-policy:
    @cd {{ policy_compiler_dir }} && uv run opencode-permission-policy-compiler set-global-policy global

[private]
_build-opencode-managed-agents:
    #!/usr/bin/env bash
    set -euo pipefail

    output_dir="{{ managed_agents_dir }}"
    compiler_dir="{{ policy_compiler_dir }}"

    if [[ ! -d "$compiler_dir" ]]; then
        echo "Missing compiler repo: $compiler_dir" >&2
        exit 1
    fi

    mkdir -p "$output_dir"

    echo "Building autonomous.md from interactive-agents/autonomous"
    uvx --refresh --from {{ ai_prompts_source }} ai-prompts get interactive-agents/autonomous \
      | (cd "$compiler_dir" && uv run opencode-permission-policy-compiler) \
      > "$output_dir/autonomous.md"

    echo "Building orchestrator.md from interactive-agents/orchestrator"
    uvx --refresh --from {{ ai_prompts_source }} ai-prompts get interactive-agents/orchestrator \
      | (cd "$compiler_dir" && uv run opencode-permission-policy-compiler) \
      > "$output_dir/orchestrator.md"

    echo "Building build.md from interactive-agents/build"
    uvx --refresh --from {{ ai_prompts_source }} ai-prompts get interactive-agents/build \
      | (cd "$compiler_dir" && uv run opencode-permission-policy-compiler) \
      > "$output_dir/build.md"

    echo "Building plan.md from interactive-agents/plan"
    uvx --refresh --from {{ ai_prompts_source }} ai-prompts get interactive-agents/plan \
      | (cd "$compiler_dir" && uv run opencode-permission-policy-compiler) \
      > "$output_dir/plan.md"

    echo "Building compaction.md from micro-agents/compaction"
    uvx --refresh --from {{ ai_prompts_source }} ai-prompts get micro-agents/compaction \
      | (cd "$compiler_dir" && uv run opencode-permission-policy-compiler) \
      > "$output_dir/compaction.md"

    echo "Building correction-finder-ask.md from sub-agents/correction-finder-ask"
    uvx --refresh --from {{ ai_prompts_source }} ai-prompts get sub-agents/correction-finder-ask \
      | (cd "$compiler_dir" && uv run opencode-permission-policy-compiler) \
      > "$output_dir/correction-finder-ask.md"

    echo "Building general.md from sub-agents/general"
    uvx --refresh --from {{ ai_prompts_source }} ai-prompts get sub-agents/general \
      | (cd "$compiler_dir" && uv run opencode-permission-policy-compiler) \
      > "$output_dir/general.md"

    echo "Building explore.md from sub-agents/explore"
    uvx --refresh --from {{ ai_prompts_source }} ai-prompts get sub-agents/explore \
      | (cd "$compiler_dir" && uv run opencode-permission-policy-compiler) \
      > "$output_dir/explore.md"

    echo "Building interactive.md from interactive-agents/interactive"
    uvx --refresh --from {{ ai_prompts_source }} ai-prompts get interactive-agents/interactive \
      | (cd "$compiler_dir" && uv run opencode-permission-policy-compiler) \
      > "$output_dir/interactive.md"

    echo "Building minimal.md from interactive-agents/minimal"
    uvx --refresh --from {{ ai_prompts_source }} ai-prompts get interactive-agents/minimal \
      | (cd "$compiler_dir" && uv run opencode-permission-policy-compiler) \
      > "$output_dir/minimal.md"

    echo "Building prover.md from sub-agents/prover"
    uvx --refresh --from {{ ai_prompts_source }} ai-prompts get sub-agents/prover \
      | (cd "$compiler_dir" && uv run opencode-permission-policy-compiler) \
      > "$output_dir/prover.md"

    echo "Building summary.md from micro-agents/summary"
    uvx --refresh --from {{ ai_prompts_source }} ai-prompts get micro-agents/summary \
      | (cd "$compiler_dir" && uv run opencode-permission-policy-compiler) \
      > "$output_dir/summary.md"

    echo "Building title.md from micro-agents/title"
    uvx --refresh --from {{ ai_prompts_source }} ai-prompts get micro-agents/title \
      | (cd "$compiler_dir" && uv run opencode-permission-policy-compiler) \
      > "$output_dir/title.md"

    echo "Building unrestricted-test.md from interactive-agents/unrestricted-test"
    uvx --refresh --from {{ ai_prompts_source }} ai-prompts get interactive-agents/unrestricted-test \
      | (cd "$compiler_dir" && uv run opencode-permission-policy-compiler) \
      > "$output_dir/unrestricted-test.md"

    echo "Building sagemath-coder.md from sub-agents/sagemath-coder"
    uvx --refresh --from {{ ai_prompts_source }} ai-prompts get sub-agents/sagemath-coder \
      | (cd "$compiler_dir" && uv run opencode-permission-policy-compiler) \
      > "$output_dir/sagemath-coder.md"


# =============================================================================
# AGENTS.md Template
# =============================================================================

[private]
_build-opencode-agents-md:
    @just --justfile {{ justfile() }} _build-opencode-agents-md-render
    @just --justfile {{ justfile() }} count-tokens {{ repo }}/opencode/AGENTS.md

# Render the repo-local AGENTS.md from the published system template.
# Steps:
# - fetch the system/AGENTS prompt body from ai-prompts
# - write it into ~/ai/opencode/AGENTS.md
[private]
_build-opencode-agents-md-render:
    @uvx --from git+https://github.com/dzackgarza/ai-prompts.git ai-prompts get system/AGENTS --json \
      | jq -r '.text' \
      | tee {{ repo }}/opencode/AGENTS.md \
      | wc -c \
      | xargs -I {} echo "Wrote {{ repo }}/opencode/AGENTS.md ({} bytes)"

# Count tokens in any file using tiktoken (cl100k_base).
count-tokens file:
    @uvx --with tiktoken python -c 'import sys, tiktoken; from pathlib import Path; path = Path(sys.argv[1]); text = path.read_text(); count = len(tiktoken.get_encoding("cl100k_base").encode(text)); print(f"{path}: {count} tokens")' {{ file }}

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

# Check markdown files for broken local file references.
#
# Usage: just check-markdown [path ...]
check-markdown *args:
    #!/usr/bin/env bash
    set -euo pipefail

    repo_root="$(git rev-parse --show-toplevel)"
    markdown_files=()

    collect_tracked_markdown() {
        mapfile -d '' markdown_files < <(
            git -C "$repo_root" ls-files -z -- '*.md' '*.markdown' '*.mdx'
        )
    }

    collect_path_markdown() {
        local input="$1"

        if [[ -d "$input" ]]; then
            while IFS= read -r -d '' path; do
                markdown_files+=("$path")
            done < <(
                find "$input" -type f \
                    \( -name '*.md' -o -name '*.markdown' -o -name '*.mdx' \) \
                    -print0
            )
        else
            markdown_files+=("$input")
        fi
    }

    if [[ -z "{{ args }}" ]]; then
        collect_tracked_markdown
    else
        for input in {{ args }}; do
            collect_path_markdown "$input"
        done
    fi

    ((${#markdown_files[@]} > 0))
    lychee --offline --no-progress --root-dir "$repo_root" "${markdown_files[@]}"
