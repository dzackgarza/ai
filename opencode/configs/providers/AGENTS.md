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

## Whitelist Criteria

A whitelist is the set of models an OpenCode agent can use. Every model in it
must pass all of these tests:

1. **It costs nothing on the account that this config uses.** A per-token
   price, a credit requirement, or a paid-plan gate (for example the Cloudflare
   Workers Paid plan) excludes the model. A catalog price on models.dev is
   evidence, but the account's own API response is the authority.
2. **It is a general chat model that can do agent work.** Embedding, reranking,
   image, video, speech, translation, PII, safety-classifier, router, and
   decision-only models (for example `jev-*`, `*-decision`) go in the
   blacklist.
3. **It is not substantially worse than Qwen3.7-Plus at agentic coding.** A
   model below that bar is not useful for any work that goes through
   OpenCode, whatever its size or price. Use the Vals.ai Terminal-Bench 2.1
   board (vals.ai/benchmarks/terminal-bench-2-1) as the primary evidence: all
   models there run in one harness, and Qwen 3.7 Plus scores 52.81 on it.
   "Substantially worse" means more than about 5% below. When a model is not
   on that board, compare on another shared benchmark (SWE-bench Pro, vendor
   Terminal-Bench figures against Qwen's vendor figures) and say which one.
   Size is only a weak signal: a 30B-A3B model scored 10.86 on that board.
4. **It is current.** Deprecated models, and obsolete generations such as
   `gpt-oss-120b`, go in the blacklist. A dated tag that duplicates a
   whitelisted id also goes in the blacklist.
5. **It answers a live call through `opencode run -m <provider>/<model>`.**
   The validator's catalog diff proves only that the id is listed. Providers
   deprecate models before their catalogs drop them, and models.dev lags
   behind both. Slow is not dead: NVIDIA NIM models are known to answer
   slowly.

A gateway that forwards to another configured provider gets no copy of that
provider's models. Kilo forwards to OpenRouter: its error bodies are
OpenRouter's, with OpenRouter's BYOK link, and its catalog carries almost
every OpenRouter id under the same name. So every Kilo id that is also in
OpenRouter's catalog goes in the Kilo blacklist, and the model is triaged and
used through `openrouter` directly. Kilo's routers that resolve to OpenRouter
slugs (`kilo-auto/*`, which reports the slug in `x-kilo-resolved-model`) are
blacklisted for the same reason. Only models that OpenRouter does not list can
be in the Kilo whitelist.

Tool-call support is assumed for current chat models of this size, so it
needs no separate test.

A provider that the user no longer uses has its fragment deleted and its id
added to `disabled_providers` in `../config_skeleton.json`. OpenCode's
built-in registry keeps listing a provider that has no local fragment, so
deleting the fragment alone is not enough.

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
