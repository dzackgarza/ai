# Install symlinks for all CLI harnesses
# Usage: just install

repo := env_var_or_default("REPO", env_var("HOME") / "ai")

# Install all symlinks and environment variables
install: install-context install-skills install-system-prompts
    @echo "✓ Installed"

# Install context file symlinks (appended to harness system prompt)
install-context:
    @mkdir -p ~/.claude ~/.codex ~/.gemini ~/.qwen ~/.config/opencode ~/.config/amp ~/.config ~/.agents ~/.kilocode
    @ln -sf {{repo}}/AGENTS.md ~/.claude/CLAUDE.md
    @ln -sf {{repo}}/AGENTS.md ~/.codex/AGENTS.md
    @ln -sf {{repo}}/AGENTS.md ~/.gemini/GEMINI.md
    @ln -sf {{repo}}/AGENTS.md ~/.qwen/QWEN.md
    @ln -sf {{repo}}/AGENTS.md ~/.config/opencode/AGENTS.md
    @ln -sf {{repo}}/AGENTS.md ~/.config/amp/AGENTS.md
    @ln -sf {{repo}}/AGENTS.md ~/.config/AGENTS.md
    @ln -sf {{repo}}/opencode/opencode.json ~/.config/opencode/opencode.json

# Install skills directory symlinks
install-skills:
    @mkdir -p ~/.claude ~/.gemini ~/.agents ~/.qwen ~/.config/agents ~/.config/amp ~/.kilocode
    @ln -sf {{repo}}/skills ~/.claude/skills
    @ln -sf {{repo}}/skills ~/.gemini/skills
    @ln -sf {{repo}}/skills ~/.agents/skills
    @ln -sf {{repo}}/skills ~/.qwen/skills
    @ln -sf {{repo}}/skills ~/.config/agents/skills
    @ln -sf {{repo}}/skills ~/.config/amp/skills
    @ln -sf {{repo}}/skills ~/.kilocode/skills

# Install system prompt override files and env vars
install-system-prompts:
    @mkdir -p ~/.gemini ~/.qwen
    @ln -sf {{repo}}/prompts/interactive_agents/interactive.md ~/.gemini/system.md
    @ln -sf {{repo}}/prompts/interactive_agents/interactive.md ~/.qwen/system.md
    @grep -q 'GEMINI_SYSTEM_MD' ~/.bashrc 2>/dev/null || printf '\n# System prompt overrides for Gemini/Qwen CLI\nexport GEMINI_SYSTEM_MD=true\nexport QWEN_SYSTEM_MD=true\n' >> ~/.bashrc
    @grep -q 'GEMINI_SYSTEM_MD' ~/.zshrc 2>/dev/null || printf '\n# System prompt overrides for Gemini/Qwen CLI\nexport GEMINI_SYSTEM_MD=true\nexport QWEN_SYSTEM_MD=true\n' >> ~/.zshrc
    @echo "Added GEMINI_SYSTEM_MD and QWEN_SYSTEM_MD to ~/.bashrc and ~/.zshrc"
    @echo ""
    @echo "Note: For OpenCode, the interactive agent prompt is configured via"
    @echo "the 'prompt' field in opencode.json (custom agents replace system prompt)."
