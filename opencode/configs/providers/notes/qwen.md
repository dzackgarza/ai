# Qwen Web Provider

This provider proxies requests through the unofficial `qwen-api` gateway (`https://qwen.aikit.club/v1`), bridging to `chat.qwen.ai`.

## Configuration

- Config: `opencode/configs/providers/qwen.json`
- Base URL: `https://qwen.aikit.club/v1`
- Auth Env Var: `QWEN_API_KEY` (in `~/.envrc`)

## Session Extraction

Tokens are session JWTs extracted from Chromium browser storage. Use the helper script to extract and refresh:

```bash
uv run python opencode/configs/providers/scripts/extract_qwen_session.py --refresh
```

## Models

- Whitelisted: `qwen3.8-max`, `qwen3.7-plus`, `qwen3.7-max`, `qwen3.6-plus`, `qwen3.5-plus`, `qwen3.5-omni-plus`, `qwen3.8-omni-flash`, `qwen-deep-research`, `qwen-web-dev`, `qwen-full-stack`, `qwen-slides`
- Blacklisted: `qwen-image`, `qwen-video` (non-chat completions)
