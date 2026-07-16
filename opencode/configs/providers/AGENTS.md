# Providers

This directory is the source of truth for provider configs.
Keep provider JSON files here, keep provider-specific notes beside them, and keep
repeatable provider maintenance scripts in `scripts/`.

## Source Of Truth

- Provider definitions: `*.json`

- Provider notes: `notes/`

- Provider maintenance scripts: `scripts/`

- Provider-specific local shims: `shims/`

## Canonical Recipes

From the repo root:

```bash
just providers-validate            # all providers, fails (exit 1) on drift
just providers-validate nvidia     # single provider, fails on drift
just providers-debug nvidia        # single provider, warn-only (no exit 1)
```

`providers-validate` checks directly-queryable providers (any config with
`options.baseURL`, e.g. NVIDIA NIM, VectorEngine, Antigravity) against their
own live `/models` endpoint — authoritative over the third-party models.dev
mirror. Every other provider is checked against models.dev. Either check
fails the run if a whitelisted model has rotated off the live catalog or a
live model isn't yet triaged into the whitelist or blacklist.

## Placement Rules

1. Put durable provider maintenance in `scripts/`.

2. Put provider-specific operational notes in `notes/`.

3. Put provider-specific local shims in `shims/` instead of inventing root-level plugin
   folders.

4. Archive superseded validation experiments outside this directory.

5. Edit the provider JSON source files here, then rebuild from the repo root.

## Special Cases

- Google Antigravity routing details: `notes/google-provider.md`

- OpenRouter vetting notes: `notes/openrouter-model-vetting.md`
