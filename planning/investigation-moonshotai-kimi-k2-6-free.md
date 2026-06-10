
---
title: OpenRouter Models in OpenCode - Diagnostic Procedure
status: active
tags: [opencode, openrouter, models, diagnostics]
---

## Trigger

A user reports an OpenRouter model (especially a `:free` model) is not appearing in opencode's model list.

## Diagnostic Procedure

### Step 1: Check models.dev (canonical registry)

```bash
curl -s https://models.dev/api.json | jq '.openrouter.models | keys' | grep <model-slug>
```

If the model is **absent from models.dev**, that is the primary reason it does not appear in opencode by default. models.dev is OpenCode's built-in model registry — it determines what is auto-populated.

### Step 2: Check the local shadow config

Open `opencode/configs/providers/openrouter.json` and check:

- Is it in `models`? (whitelist — manually added to override models.dev gap)
- Is it in `blacklist`? (explicitly hidden)

The local config is a **shadow overlay** on top of models.dev, not a standalone list. A model must be in either models.dev OR the local whitelist to appear in opencode.

### Step 3: Check the live OpenRouter API

```bash
curl -s https://openrouter.ai/api/v1/models | jq '.data[].id' | grep <model>
```

A model may be live on OpenRouter but absent from both models.dev and the local whitelist. This means someone needs to add it to the whitelist.

## Context

Investigated 2026-05-28: `moonshotai/kimi-k2.6:free` was absent from models.dev and the local whitelist → invisible. `deepseek/deepseek-v4-flash:free` was already in models.dev (so it would appear once the whitelist was populated too, since models may need both).

## Verification

Run `just build-config` and confirm the validator shows no warnings about unaccounted free models.
