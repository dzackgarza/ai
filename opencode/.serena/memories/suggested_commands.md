# Suggested Commands for OpenCode

## Formatting & Linting
- **Python Linting**: `uvx ruff check --fix <file>`
- **Python Formatting**: `uvx ruff format <file>`
- **General Formatting**: `npx prettier --write <file>` (Supports .md, .js, .ts, .json, .yaml, etc.)

## Testing
- **Comprehensive Model Test**: `./test-models-comprehensive.sh`
- **Single Model Test**: `./test-single-model.sh`
- **Tool Calling Test**: `./test-tool-calling-capability.sh`

## Execution
- **Run OpenCode Command**: `opencode run -m <model_id> "<prompt>"`
