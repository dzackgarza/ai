
---
title: OpenRouter Validator Must Flag Unaccounted Free Models
status: active
tags: [opencode, openrouter, validation, build_config]
---

## Trigger

When running `just build-config` (which calls `scripts/build_config.py`), the `validate_openrouter` function should catch any live OpenRouter free model that is absent from both the local whitelist and blacklist.

## Actionable Rule

The function computes `free_live_ids` (all models on OpenRouter priced at 0, or ending in `:free`). It must also compute:

```python
unaccounted_free = sorted(free_live_ids - whitelist - blacklist)
```

and log a warning with the full list (no truncation) for any models found. These models are gaps that need manual triage.

## Why

The local config is a shadow over models.dev. A live free model on OpenRouter that is absent from models.dev AND absent from the local whitelist falls through completely. The validator exists to maintain this invariant: every live free model should be accounted for (whitelisted, blacklisted, or confirmed absent from models.dev).

## Verification

Run `just build-config`. The output should contain either:
- `"All live free models are accounted for"` — no gaps
- A warning listing unaccounted model IDs — needs triage
