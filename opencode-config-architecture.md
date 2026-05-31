
---
title: OpenCode Provider Config Architecture & Philosophy
status: active
tags: [opencode, providers, models, architecture]
---

## Design Goal

The user wants new OpenRouter free models available in opencode **immediately** when they appear on OpenRouter. No waiting for models.dev to update. No polluted model picker full of unusable garbage.

## How It Works

Three layers, each serving a purpose:

### 1. models.dev (OpenCode's built-in registry)

The default population source. May lag the actual provider by hours or days.

### 2. Local shadow (\`configs/providers/*.json\`)

An explicit override layer that gives the user **control**:

- **\`models\` (whitelist)**: Adds a model that exists on the provider but may not be in models.dev yet. This is how new useful models become available **immediately** without waiting for models.dev to catch up.

- **\`blacklist\`**: Removes a model that IS in models.dev (or exists on the provider) but should be hidden. This is how the user keeps their model picker clean — underpowered models, dead endpoints, garbage.

### 3. Validator (\`validate_openrouter\`)

Catches **disparities** so the user knows what needs triage:

- Models in the whitelist that disappeared from the provider
- Models that went paid
- **New free models on OpenRouter absent from both whitelist and blacklist** — these are newly available models the user hasn't evaluated yet. The validator flags them so they can be explicitly added (if useful) or blacklisted (if garbage).

## Why This Architecture

| Concern | Solution |
|---|---|
| New good models should be usable NOW | Local whitelist bypasses models.dev lag |
| Model picker should not be polluted | Blacklist removes garbage explicitly |
| User controls what's available | No auto-population of untrusted models |
| User should know what's new | Validator flags unaccounted models |

The local config gives the user **explicit curation control** over their model list. The validator is the feedback loop that tells them what needs their attention.
