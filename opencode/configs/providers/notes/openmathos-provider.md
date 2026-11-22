# Open Math OS (`openmathos`)

Open Math OS is an OpenAI-compatible gateway that serves open-weight models.

- Base URL: `https://os.openmathmodel.org/v1`
- Auth: bearer token. The key is `OPENMATH_OS_API_KEY` in `~/.envrc`.
- Setup reference: <https://os.openmathmodel.org/v1/doc/opencode>
- Model list: <https://os.openmathmodel.org/v1/models> (needs the key).

## Why a static fragment

`openmathos` is absent from models.dev. The fragment `openmathos.json` therefore
names each allowed model in `models`, and `scripts/build_config.py` checks the
fragment against the provider's own live `/v1/models` (the `options.baseURL`
branch of `providers-validate`). Run:

```bash
just providers-validate openmathos
```

The catalog is 8 models. A new live model fails that check until it is triaged
into `whitelist` or `blacklist`.

## The discovery plugin

The provider's own doc offers `opencode-models-discovery@2.1.0` (repo:
<https://github.com/yuhp/opencode-models-discovery>) so OpenCode loads the whole
catalog without a model list. This config does not use it. The plugin injects
every live model, which bypasses the whitelist policy in `../AGENTS.md`
(criterion 3, the Qwen3.7-Plus bar). The static fragment keeps the policy in
force and stays verifiable through `providers-validate`. The doc itself lists an
explicit `models` map as the alternative for single-run automation.

## Model triage

The catalog has no chat-model exclusions (no embedding, image, or router ids).

Whitelisted:

| Model | Score | Same-model precedent |
| --- | ---: | --- |
| `moonshotai/kimi-k3.1-pro` | 75 | `nvidia`, `ollama-cloud` |
| `deepseek/deepseek-v4.1-flash` | 50 | `ollama-cloud`, `opencode`, `tokenharbor` |
| `z-ai/glm-5.3` | 49 | `ollama-cloud` |
| `z-ai/glm-5.3-flash` | 41 | `nvidia`, `ollama-cloud` |
| `mistralai/mistral-large-4-0` | 35 | `nvidia`, `ollama-cloud` |
| `meta/muse-spark-open` | 33 | `ollama-cloud` |
| `thinkingmachines/inkling-2-small` | 11 | `ollama-cloud` |

Blacklisted:

| Model | Reason |
| --- | --- |
| `nvidia/nemotron-3-super-120b-a12b` | Below the Qwen3.7-Plus bar. Blacklisted on `nvidia`, `ollama-cloud`, `openrouter`, and `kilo` as the weak tier of the Nemotron 3 series. |

The whitelist mirrors the verdict for the same model on `ollama-cloud`, which
also serves open-weight models for free. Scores and display names come from
`model-scores.md`.

## Model metadata

Open Math OS reports a context window and capabilities for each model. The
fragment does not copy them: every provider fragment in this directory names its
whitelisted models only, and OpenCode applies its own defaults. If a model's
limit must be correct in the picker, add `limit` to the model entry.

## Key delivery to the background service

A session on the background service (`opencode serve --service`) reads provider
keys from the service process environment, which the service keeps from its
start. A key added to `~/.envrc` after the service started is absent until the
service restarts. Until then this provider fails with

```
a team's models are called with one of its API keys (`nuc_ak_...`)
```

That message is the provider's reply to a missing or wrong bearer token: an
unauthenticated `curl` returns the same body. `opencode run --standalone` starts
a private server that inherits the calling shell's direnv environment, so it
succeeds while the shared service fails. Restart the service from a direnv shell
so the new process inherits the key:

```bash
direnv exec . opencode service restart
```

`~/.envrc` reaches the repo environment through `source_up` in `.envrc`.
