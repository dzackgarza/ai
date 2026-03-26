# Providers

This directory is the source of truth for provider configs. Keep provider JSON
files here, keep provider-specific notes beside them, and keep repeatable
provider maintenance scripts in `scripts/`.

## Source Of Truth

- Provider definitions: `*.json`
- Provider notes: `notes/`
- Provider maintenance scripts: `scripts/`
- Provider-specific local shims: `shims/`

## Canonical Recipes

From the repo root:

```bash
just providers-validate
just providers-validate google
just openrouter-sync
just providers-debug opencode
just openrouter-probe-endpoints
just openrouter-probe-tool-calling
```

## Placement Rules

1. Put durable provider maintenance in `scripts/`.
2. Put provider-specific operational notes in `notes/`.
3. Put provider-specific local shims in `shims/` instead of inventing root-level plugin folders.
4. Archive superseded validation experiments outside this directory.
5. Edit the provider JSON source files here, then rebuild from the repo root.

## Special Cases

- Google Antigravity routing details: `notes/google-provider.md`
- OpenRouter vetting notes: `notes/openrouter-model-vetting.md`
- Free model tiers and stack: `FREE_MODELS.md`
