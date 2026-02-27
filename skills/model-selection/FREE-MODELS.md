# Free LLM API Providers

## Genuinely Free Tiers

These providers offer meaningful free tiers without requiring payment info.

| Provider                  | Base URL                                                   | API Key Env Var                                | Get Key                               | Notes                                           |
| ------------------------- | ---------------------------------------------------------- | ---------------------------------------------- | ------------------------------------- | ----------------------------------------------- |
| **Groq**                  | `api.groq.com/openai/v1`                                   | `GROQ_API_KEY`                                 | console.groq.com/keys                 | Rate-limited but free, OpenAI-compatible        |
| **NVIDIA NIM**            | `integrate.api.nvidia.com/v1`                              | `NVIDIA_API_KEY`                               | build.nvidia.com → Profile → API Keys | Free tier, OpenAI-compatible                    |
| **Mistral**               | `api.mistral.ai/v1`                                        | `MISTRAL_API_KEY`                              | codestral.mistral.ai → API Keys       | Includes Codestral, phone required              |
| **Cloudflare Workers AI** | `api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/v1` | `CLOUDFLARE_API_KEY` + `CLOUDFLARE_ACCOUNT_ID` | dash.cloudflare.com → API Tokens      | 10k neurons/day free                            |
| **OpenRouter**            | `openrouter.ai/api/v1`                                     | `OPENROUTER_API_KEY`                           | openrouter.ai/keys                    | `:free` models: 50 req/day, 20/min rate limit   |
| **SambaNova**             | `api.sambanova.ai/v1`                                      | `SAMBANOVA_API_KEY`                            | sambanova.ai/developers               | Free tier, requires `stream: true`              |
| **Cerebras**              | `api.cerebras.ai/v1`                                       | `CEREBRAS_API_KEY`                             | cerebras.ai                           | Free tier: 1K RPM, 1M tokens/min (gpt-oss-120b) |

## Laughably Small Free Tiers (Effectively Not Free)

These providers technically offer "free" tiers, but they're so limited they're not practical for development or testing.

| Provider             | Base URL                                   | API Key Env Var      | Get Key                          | Why It's Not Useful                               |
| -------------------- | ------------------------------------------ | -------------------- | -------------------------------- | ------------------------------------------------- |
| **Scaleway**         | `api.scaleway.ai/v1`                       | `SCALEWAY_API_KEY`   | console.scaleway.ai/iam/api-keys | 1M tokens ≈ $2 value, expires                     |
| **Fireworks AI**     | `api.fireworks.ai/inference/v1`            | `FIREWORKS_API_KEY`  | fireworks.ai → Settings          | $1 free credits (one-time trial)                  |
| **Hyperbolic**       | `api.hyperbolic.xyz/v1`                    | `HYPERBOLIC_API_KEY` | app.hyperbolic.ai/settings       | $1 free trial (one-time)                          |
| **Hugging Face**     | `api-inference.huggingface.co`             | `HF_TOKEN`           | huggingface.co/settings/tokens   | Free monthly credits too small for real use       |
| **Google AI Studio** | `generativelanguage.googleapis.com/v1beta` | `GOOGLE_API_KEY`     | aistudio.google.com/apikey       | Only Gemma models (not SOTA), geo-blocked regions |

## Not Free / Pay-Per-Use

These are paid services with no meaningful free tier.

| Provider        | Base URL                 | API Key Env Var       | Get Key                           | Pricing Model                 |
| --------------- | ------------------------ | --------------------- | --------------------------------- | ----------------------------- |
| **Replicate**   | `api.replicate.com/v1`   | `REPLICATE_API_TOKEN` | replicate.com/account/api-tokens  | Pay-per-prediction            |
| **Perplexity**  | `api.perplexity.ai`      | `PERPLEXITY_API_KEY`  | perplexity.ai/settings/api        | Tiered by spend               |
| **Together AI** | `api.together.xyz/v1`    | `TOGETHER_API_KEY`    | api.together.ai/settings/api-keys | Credits vary, never been free |
| **SiliconFlow** | `api.siliconflow.com/v1` | `SILICONFLOW_API_KEY` | cloud.siliconflow.cn/account/ak   | Quotas vary, unreliable       |
| **DeepInfra**   | `api.deepinfra.com/v1`   | `DEEPINFRA_API_KEY`   | deepinfra.com/dashboard           | Free tier removed 2025        |

---

## Test Commands

**Note:** Commands for "Not Free" and "Laughably Small" providers are included for reference only (e.g., if you already have an account). For genuinely free testing, use Groq, NVIDIA NIM, Mistral, Cloudflare, OpenRouter, or SambaNova.

### Groq

```bash
curl -s https://api.groq.com/openai/v1/chat/completions -H "Authorization: Bearer $GROQ_API_KEY" -H "Content-Type: application/json" -d '{"model":"llama-3.3-70b-versatile","messages":[{"role":"user","content":"Hello"}]}' | jq '.choices[0].message.content'
```

### NVIDIA NIM

```bash
curl -s https://integrate.api.nvidia.com/v1/chat/completions -H "Authorization: Bearer $NVIDIA_API_KEY" -H "Content-Type: application/json" -d '{"model":"meta/llama-3.1-8b-instruct","messages":[{"role":"user","content":"Hello"}]}' | jq '.choices[0].message.content'
```

### Mistral

```bash
curl -s https://api.mistral.ai/v1/chat/completions -H "Authorization: Bearer $MISTRAL_API_KEY" -H "Content-Type: application/json" -d '{"model":"mistral-small-latest","messages":[{"role":"user","content":"Hello"}]}' | jq '.choices[0].message.content'
```

### Cloudflare Workers AI

```bash
curl -s "https://api.cloudflare.com/client/v4/accounts/${CLOUDFLARE_ACCOUNT_ID}/ai/v1/chat/completions" -H "Authorization: Bearer $CLOUDFLARE_API_KEY" -H "Content-Type: application/json" -d '{"model":"@cf/meta/llama-3.1-8b-instruct","messages":[{"role":"user","content":"Hello"}]}' | jq '.choices[0].message.content'
```

### OpenRouter

```bash
curl -s https://openrouter.ai/api/v1/chat/completions -H "Authorization: Bearer $OPENROUTER_API_KEY" -H "Content-Type: application/json" -d '{"model":"openrouter/free","messages":[{"role":"user","content":"Hello"}]}' | jq '.choices[0].message.content'
```

### SambaNova

```bash
curl -s https://api.sambanova.ai/v1/chat/completions -H "Authorization: Bearer $SAMBANOVA_API_KEY" -H "Content-Type: application/json" -d '{"stream":true,"model":"Qwen3-235B","messages":[{"role":"user","content":"Hello"}]}'
```

### Cerebras

```bash
curl -s https://api.cerebras.ai/v1/chat/completions -H "Authorization: Bearer $CEREBRAS_API_KEY" -H "Content-Type: application/json" -d '{"model":"gpt-oss-120b","messages":[{"role":"user","content":"Hello"}]}' | jq '.choices[0].message.content'
```

### Replicate

```bash
curl -s https://api.replicate.com/v1/predictions -H "Authorization: Bearer $REPLICATE_API_TOKEN" -H "Content-Type: application/json" -H "Prefer: wait=5" -d '{"version":"replicate/hello-world:5c7d5dc6dd8bf75c1acaa8565735e7986bc5b66206b55cca93cb72c9bf15ccaa","input":{"text":"Hello"}}' | jq '.output'
```

### Google AI Studio

```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent" -H "x-goog-api-key: $GOOGLE_API_KEY" -H "Content-Type: application/json" -d '{"contents":[{"parts":[{"text":"Hello"}]}]}' | jq '.candidates[0].content.parts[0].text'
```

### Scaleway

```bash
curl -s https://api.scaleway.ai/v1/chat/completions -H "Authorization: Bearer $SCALEWAY_API_KEY" -H "Content-Type: application/json" -d '{"model":"mistralai/Mistral-7B-Instruct-v0.3","messages":[{"role":"user","content":"Hello"}]}' | jq '.choices[0].message.content'
```

### Fireworks AI

```bash
curl -s https://api.fireworks.ai/inference/v1/chat/completions -H "Authorization: Bearer $FIREWORKS_API_KEY" -H "Content-Type: application/json" -d '{"model":"accounts/fireworks/models/llama-v3p1-8b-instruct","messages":[{"role":"user","content":"Hello"}]}' | jq '.choices[0].message.content'
```

### Hyperbolic

```bash
curl -s https://api.hyperbolic.xyz/v1/chat/completions -H "Authorization: Bearer $HYPERBOLIC_API_KEY" -H "Content-Type: application/json" -d '{"model":"meta-llama/Llama-3.1-8B-Instruct","messages":[{"role":"user","content":"Hello"}]}' | jq '.choices[0].message.content'
```

### Together AI

```bash
curl -s https://api.together.xyz/v1/chat/completions -H "Authorization: Bearer $TOGETHER_API_KEY" -H "Content-Type: application/json" -d '{"model":"meta-llama/Llama-3.1-8B-Instruct-Turbo","messages":[{"role":"user","content":"Hello"}]}' | jq '.choices[0].message.content'
```

### SiliconFlow

```bash
curl -s https://api.siliconflow.com/v1/chat/completions -H "Authorization: Bearer $SILICONFLOW_API_KEY" -H "Content-Type: application/json" -d '{"model":"Qwen/Qwen2.5-7B-Instruct","messages":[{"role":"user","content":"Hello"}]}' | jq '.choices[0].message.content'
```

### Perplexity

```bash
curl -s https://api.perplexity.ai/chat/completions -H "Authorization: Bearer $PERPLEXITY_API_KEY" -H "Content-Type: application/json" -d '{"model":"sonar-pro","messages":[{"role":"user","content":"Hello"}]}' | jq '.choices[0].message.content'
```

### Hugging Face Inference

```bash
curl -s https://api-inference.huggingface.co/models/meta-llama/Llama-3.1-8B-Instruct -H "Authorization: Bearer $HF_TOKEN" -H "Content-Type: application/json" -d '{"inputs":"Hello"}' | jq '.[0].generated_text'
```
