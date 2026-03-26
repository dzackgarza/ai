# FREE MODELS

This document lists the available free model tiers across all configured providers.

## 🔵 CLAUDE MODELS (via Kiro — AWS Builder ID)

| Model | Prefix | Limit | Rate Limit |
| :--- | :--- | :--- | :--- |
| claude-sonnet-4.5 | kr/ | Unlimited | No reported daily cap |
| claude-haiku-4.5 | kr/ | Unlimited | No reported daily cap |
| claude-opus-4.6 | kr/ | Unlimited | Latest Opus via Kiro |

## 🟢 IFLOW MODELS (Free OAuth — No Credit Card)

| Model | Prefix | Limit | Rate Limit |
| :--- | :--- | :--- | :--- |
| kimi-k2-thinking | if/ | Unlimited | No reported cap |
| qwen3-coder-plus | if/ | Unlimited | No reported cap |
| deepseek-r1 | if/ | Unlimited | No reported cap |
| minimax-m2.1 | if/ | Unlimited | No reported cap |
| kimi-k2 | if/ | Unlimited | No reported cap |

## 🟡 QWEN MODELS (Device Code Auth)

| Model | Prefix | Limit | Rate Limit |
| :--- | :--- | :--- | :--- |
| qwen3-coder-plus | qw/ | Unlimited | No reported cap |
| qwen3-coder-flash | qw/ | Unlimited | No reported cap |
| qwen3-coder-next | qw/ | Unlimited | No reported cap |

## 🟣 GEMINI CLI (Google OAuth)

| Model | Prefix | Limit | Rate Limit |
| :--- | :--- | :--- | :--- |
| gemini-3-flash-preview | gc/ | 180K tok/month + 1K/day | Monthly reset |
| gemini-2.5-pro | gc/ | 180K/month (shared pool) | High quality |

## ⚫ NVIDIA NIM (Free API Key — build.nvidia.com)

| Tier | Daily Limit | Rate Limit | Notes |
| :--- | :--- | :--- | :--- |
| Free (Dev) | No token cap | ~40 RPM | 70+ models; transitioning to pure rate limits mid-2025 |

**Popular free models**: moonshotai/kimi-k2.5 (Kimi K2.5), z-ai/glm4.7 (GLM 4.7), deepseek-ai/deepseek-v3.2 (DeepSeek V3.2), nvidia/llama-3.3-70b-instruct, deepseek/deepseek-r1

## ⚪ CEREBRAS (Free API Key — inference.cerebras.ai)

| Tier | Daily Limit | Rate Limit | Notes |
| :--- | :--- | :--- | :--- |
| Free | 1M tokens/day | 60K TPM / 30 RPM | World's fastest LLM inference; resets daily |

**Available free**: llama-3.3-70b, llama-3.1-8b, deepseek-r1-distill-llama-70b

## 🔴 GROQ (Free API Key — console.groq.com)

| Tier | Daily Limit | Rate Limit | Notes |
| :--- | :--- | :--- | :--- |
| Free | 14.4K RPD | 30 RPM per model | No credit card; 429 on limit, not charged |

**Available free**: llama-3.3-70b-versatile, gemma2-9b-it, mixtral-8x7b

## 🔴 LONGCAT AI (Free API Key — longcat.chat) 🆕

| Model | Prefix | Daily Free Quota | Notes |
| :--- | :--- | :--- | :--- |
| LongCat-Flash-Lite | lc/ | 50M tokens 💥 | Largest free quota ever |
| LongCat-Flash-Chat | lc/ | 500K tokens | Multi-turn chat |
| LongCat-Flash-Thinking | lc/ | 500K tokens | Reasoning / CoT |
| LongCat-Flash-Thinking-2601 | lc/ | 500K tokens | Jan 2026 version |

100% free while in public beta. Sign up at longcat.chat with email or phone. Resets daily 00:00 UTC.

## 🟢 POLLINATIONS AI (No API Key Required) 🆕

| Model | Prefix | Rate Limit | Provider Behind |
| :--- | :--- | :--- | :--- |
| openai | pol/ | 1 req/15s | GPT-5 |
| claude | pol/ | 1 req/15s | Anthropic Claude |
| gemini | pol/ | 1 req/15s | Google Gemini |
| deepseek | pol/ | 1 req/15s | DeepSeek V3 |
| llama | pol/ | 1 req/15s | Meta Llama 4 Scout |
| mistral | pol/ | 1 req/15s | Mistral AI |

✨ **Zero friction**: No signup, no API key. Add the Pollinations provider with an empty key field and it works immediately.

## 🟠 CLOUDFLARE WORKERS AI (Free API Key — cloudflare.com) 🆕

| Tier | Daily Neurons | Equivalent Usage | Notes |
| :--- | :--- | :--- | :--- |
| Free | 10,000 | ~150 LLM responses | Global edge, 50+ models |

**Popular free models**: @cf/meta/llama-3.3-70b-instruct, @cf/google/gemma-3-12b-it, @cf/qwen/qwen2.5-coder-15b-instruct

Requires API Token + Account ID from dash.cloudflare.com. Store Account ID in provider settings.

## 🟣 SCALEWAY AI (1M Free Tokens — scaleway.com) 🆕

| Tier | Free Quota | Location | Notes |
| :--- | :--- | :--- | :--- |
| Free | 1M tokens | 🇫🇷 Paris, EU | No credit card needed within limits |

**Available free**: qwen3-235b-a22b-instruct-2507 (Qwen3 235B!), llama-3.1-70b-instruct, mistral-small-3.2-24b-instruct-2506, deepseek-v3-0324

EU/GDPR compliant. Get API key at console.scaleway.com.

---

## 💡 The Ultimate Free Stack (11 Providers, $0 Forever):

1.  **Kiro** (kr/)             → Claude Sonnet/Haiku UNLIMITED
2.  **iFlow** (if/)            → kimi-k2-thinking, qwen3-coder-plus, deepseek-r1 UNLIMITED
3.  **LongCat Lite** (lc/)     → LongCat-Flash-Lite — 50M tokens/day 🔥
4.  **Pollinations** (pol/)    → GPT-5, Claude, DeepSeek, Llama 4 — no key needed
5.  **Qwen** (qw/)             → qwen3-coder models UNLIMITED
6.  **Gemini** (gemini/)       → Gemini 2.5 Flash — 1,500 req/day free
7.  **Cloudflare AI** (cf/)    → 50+ models — 10K Neurons/day
8.  **Scaleway** (scw/)        → Qwen3 235B, Llama 70B — 1M free tokens (EU)
9.  **Groq** (groq/)           → Llama/Gemma — 14.4K req/day ultra-fast
10. **NVIDIA NIM** (nvidia/)   → 70+ open models — 40 RPM forever
11. **Cerebras** (cerebras/)   → Llama/Qwen world-fastest — 1M tok/day
