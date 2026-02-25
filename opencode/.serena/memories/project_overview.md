# OpenCode Project Overview

## Purpose
Configuration and testing environment for OpenCode, an AI coding assistant orchestrator that supports multiple LLM providers and Model Context Protocol (MCP) servers.

## Tech Stack
- **AI Orchestration**: OpenCode CLI
- **Linting/Formatting**: Ruff (Python), Prettier (MD, JS, TS, JSON, YAML)
- **Scripting**: Bash
- **Tools**: MCP (Serena, Kindly, Context7, Morph, Cut-Copy-Paste)
- **Providers**: Google Gemini, OpenAI GPT, Anthropic Claude, Groq, OpenRouter, Ollama

## Code Style & Conventions
- **Python**: Follows Ruff standards.
- **Web/Data**: Follows Prettier standards.

## Project Structure
- `opencode.json`: Main configuration file defining agents, providers, and tools.
- `*.sh`: Testing and utility scripts for model verification.
- `.serena/`: Agent-specific configuration and durable memory storage.
