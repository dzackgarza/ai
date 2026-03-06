# Providers

This directory is the source of truth for provider configs. Keep provider JSON
files here, keep provider-specific notes beside them, and keep repeatable
provider maintenance scripts in `scripts/`.

## Source Of Truth

- Provider definitions: `*.json`
- Provider notes: `notes/`
- Provider maintenance scripts: `scripts/`

## Canonical Recipes

From the repo root:

```bash
just providers-validate
just providers-validate google
just openrouter-sync
just providers-debug opencode
```

## Placement Rules

1. Put durable provider maintenance in `scripts/`.
2. Put provider-specific operational notes in `notes/`.
3. Archive ad hoc probes and superseded validation experiments outside this directory.
4. Edit the provider JSON source files here, then rebuild from the repo root.

## Special Cases

- Google Antigravity routing details: `notes/google-provider.md`
