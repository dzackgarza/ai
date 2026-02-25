# Project Overview

## Purpose
A centralized configuration hub for AI agent harnesses, managing system prompts, context files, and skills to ensure consistent behavior across different tools (Claude Code, Gemini CLI, Qwen Code, OpenCode, etc.).

## Tech Stack
- **Prompts**: Markdown (`AGENTS.md`, `prompts/`).
- **Configuration**: YAML (`CHOOSING_MODELS.yaml`), JSON (`opencode/opencode.json`).
- **Automation**: Just (`justfile`), Bash.

## Key Directories
- `AGENTS.md`: Master context file.
- `skills/`: Shared agent skills.
- `prompts/`: Hierarchical agent definitions.
- `opencode/`: OpenCode-specific setup.
- `openrouter/`: Model selection configuration.