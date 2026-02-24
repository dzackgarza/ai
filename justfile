# Install symlinks for all CLI harnesses
# Usage: just install

repo := env_var_or_default("REPO", env_var("HOME") / "ai")

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
    @ln -sf {{repo}}/opencode/opencode.json ~/.config/opencode/opencode.json
    @ln -sf {{repo}}/opencode/rate-limit-fallback.json ~/.opencode/rate-limit-fallback.json
    @ln -sf {{repo}}/skills ~/.claude/skills
    @ln -sf {{repo}}/skills ~/.gemini/skills
    @ln -sf {{repo}}/skills ~/.agents/skills
    @ln -sf {{repo}}/skills ~/.qwen/skills
    @ln -sf {{repo}}/skills ~/.config/agents/skills
    @ln -sf {{repo}}/skills ~/.config/amp/skills
    @ln -sf {{repo}}/skills ~/.kilocode/skills
    @ln -sf {{repo}}/prompts/interactive_agents/interactive.md ~/.gemini/system.md
    @ln -sf {{repo}}/prompts/interactive_agents/interactive.md ~/.qwen/system.md
    @grep -q 'GEMINI_SYSTEM_MD' ~/.bashrc 2>/dev/null || printf '\n# System prompt overrides for Gemini/Qwen CLI\nexport GEMINI_SYSTEM_MD=true\nexport QWEN_SYSTEM_MD=true\n' >> ~/.bashrc
    @grep -q 'GEMINI_SYSTEM_MD' ~/.zshrc 2>/dev/null || printf '\n# System prompt overrides for Gemini/Qwen CLI\nexport GEMINI_SYSTEM_MD=true\nexport QWEN_SYSTEM_MD=true\n' >> ~/.zshrc
    @echo "✓ Installed"
    @echo ""
    @echo "Context files:    AGENTS.md → all harnesses"
    @echo "Skills:           {{repo}}/skills → all harnesses"
    @echo "System prompts:   interactive.md → .gemini/system.md, .qwen/system.md"
    @echo "Env vars:         GEMINI_SYSTEM_MD, QWEN_SYSTEM_MD → bashrc, zshrc"
    @echo "OpenCode:         opencode.json, rate-limit-fallback.json"
