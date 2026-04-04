# Model Blacklist Reasons

## NVIDIA

### `qwen/qwen3.5-397b-a17b`

Triggers "System message must be at the beginning" error — model has strict requirements about system prompt placement that conflict with how opencode structures API requests.

Reference: https://github.com/anomalyco/opencode/pull/15018

### `nvidia/llama-3.1-nemotron-ultra-253b-v1`

Too dumb — when asked what a repo's contents are, confabulates based on context instead of exploring.

### `qwen/qwen3-coder-480b-a35b-instruct`

- Quickly devolves into incorrect tool calls — inserts tool call XML into chat instead of emitting proper tool calls, which are not processed correctly by opencode.
- Parameter leakage: if `fallback_models` is defined in an agent markdown header, it leaks into the API request and NVIDIA rejects it as an unknown parameter.

## All Providers

### `gpt-4.1`

Claims it "ran tools without emitting a tool call" — outright lies and confabulation with post-hoc justification. Highly misleading and dangerous for real work.
