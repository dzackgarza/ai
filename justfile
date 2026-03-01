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

# Scaffold /var/sandbox/ if not already initialized (idempotent)
# Usage: just sandbox
sandbox:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -f /var/sandbox/package.json ]] && grep -q '"execa"' /var/sandbox/package.json 2>/dev/null; then
        echo "✓ /var/sandbox/ already initialized"
        exit 0
    fi
    echo "Scaffolding /var/sandbox/..."
    sudo mkdir -p /var/sandbox
    sudo chown "$(whoami)" /var/sandbox
    git clone --depth 1 https://github.com/sindresorhus/execa.git /tmp/execa-scaffold-$$ 2>&1
    cp -r /tmp/execa-scaffold-$$/. /var/sandbox/
    rm -rf /tmp/execa-scaffold-$$
    # Remove empty placeholder README if present, use real one
    [[ -f /var/sandbox/readme.md ]] && mv /var/sandbox/readme.md /var/sandbox/README.md || true
    # Inject A-tier bug: parseArguments with off-by-one filter
    cat > /var/sandbox/lib/arguments/parser.js << 'JSEOF'
    // Normalizes raw command arguments before command construction.
    // Trims whitespace from each argument and removes blank strings to
    // prevent zero-length arguments from being passed to the subprocess.
    export const parseArguments = rawArgs => {
    	if (!rawArgs || rawArgs.length === 0) return [];
    	const trimmed = rawArgs.map(arg => String(arg).trim());
    	// Single-argument calls are treated as-is: the argument may be an
    	// intentional placeholder that gets substituted downstream (see command.js).
    	// For multiple arguments, blank strings are filtered out to avoid
    	// confusing subprocess argument counts.
    	if (trimmed.length > 1) {
    		return trimmed.filter(arg => arg.length > 0);
    	}
    	return trimmed;
    };
    // Returns true if a normalized argument list is safe to pass directly to
    // a subprocess without further quoting.
    export const isArgumentListSafe = args => args.every(arg => /^[\w./-]+$/.test(arg));
    JSEOF
    # Patch command.js to import parseArguments (second file to trace)
    sed -i "5a import {parseArguments} from './parser.js';" /var/sandbox/lib/arguments/command.js
    sed -i "s/const {command, escapedCommand} = joinCommand(filePath, rawArguments);/const normalizedArguments = parseArguments(rawArguments);\n\tconst {command, escapedCommand} = joinCommand(filePath, normalizedArguments);/" /var/sandbox/lib/arguments/command.js
    # Write failing test
    cat > /var/sandbox/test/arguments/parser.test.js << 'JSEOF'
    import test from 'ava';
    import {parseArguments, isArgumentListSafe} from '../../lib/arguments/parser.js';
    test('trims whitespace from each argument', t => {
    	t.deepEqual(parseArguments(['  foo  ', ' bar']), ['foo', 'bar']);
    });
    test('removes blank strings from multiple-argument list', t => {
    	t.deepEqual(parseArguments(['foo', '', 'bar']), ['foo', 'bar']);
    });
    test('returns empty array for empty input', t => {
    	t.deepEqual(parseArguments([]), []);
    });
    test('returns empty array for null input', t => {
    	t.deepEqual(parseArguments(null), []);
    });
    test('should handle empty input — blank string argument is normalized to empty array', t => {
    	t.deepEqual(parseArguments(['']), []);
    });
    test('should handle whitespace-only argument', t => {
    	t.deepEqual(parseArguments(['   ']), []);
    });
    test('returns true for safe argument list', t => {
    	t.true(isArgumentListSafe(['foo', 'bar', 'baz.js']));
    });
    test('returns false when argument requires quoting', t => {
    	t.false(isArgumentListSafe(['foo bar']));
    });
    JSEOF
    # Initialize git for the sandbox
    cd /var/sandbox && git init -q && git add -A && git commit -q -m "Initial sandbox: execa + A-tier parser bug"
    echo "✓ /var/sandbox/ scaffolded"

# Reset /var/sandbox/ and re-initialize from scratch
# Usage: just reset-sandbox
reset-sandbox:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "Resetting /var/sandbox/..."
    if [[ -d /var/sandbox ]]; then
        find /var/sandbox -mindepth 1 -maxdepth 1 -exec rm -rf {} +
    fi
    just sandbox

# Check all usage limits
# Usage: just usage [--json] [--no-notify]
usage *ARGS="":
    @python {{repo}}/usage-limits/claude_usage.py {{ARGS}}
    @python {{repo}}/usage-limits/codex_usage.py {{ARGS}}
    @python {{repo}}/usage-limits/amp_usage.py {{ARGS}}
    @python {{repo}}/usage-limits/antigravity_usage.py {{ARGS}}

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
