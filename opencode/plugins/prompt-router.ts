// Classifies every incoming user message and injects a passphrase relay
// instruction so the main agent echoes it before acting — proving the full
// pipeline (hook → classify → inject → model follows) end-to-end.
//
// Phase 1 (PoC): inject ONLY the passphrase relay. No routing instructions.
// Faux rules give deterministic classification for the fixed test prompts.
//
// Phase 2 (production): swap passphrase relay for ROUTING_INSTRUCTIONS below.

import Instructor from "@instructor-ai/instructor";
import OpenAI from "openai";
import { z } from "zod";
import type { Plugin } from "@opencode-ai/plugin";
import type { TextPart } from "@opencode-ai/sdk";

type Tier = "model-self" | "knowledge" | "C" | "B" | "A" | "S";

// ---------------------------------------------------------------------------
// Schema
// ---------------------------------------------------------------------------

const ClassificationSchema = z.object({
  tier: z.enum(["model-self", "knowledge", "C", "B", "A", "S"]),
  reasoning: z.string(),
});

// ---------------------------------------------------------------------------
// Model config — ordered by preference; first success wins
//
// Prefix convention (same as run.ts):
//   (none)   → OpenRouter
//   groq/    → Groq (generous free tier, fast LPU inference)
//   nvidia/  → NVIDIA NIM (direct, no OpenRouter daily cap)
//
// Avoid thinking models here — their content field is empty until after the
// reasoning budget is exhausted, making them slow and unreliable at max_tokens=200.
//
// mode: "JSON"    → response_format: json_object (default; fastest)
// mode: "MD_JSON" → prompt-based JSON in markdown block; use when json_object
//                   is unsupported (e.g. Mistral tokenizer on NVIDIA NIM)
// ---------------------------------------------------------------------------

interface ModelConfig { slug: string; mode: "JSON" | "MD_JSON"; maxTokens: number }

const CLASSIFIER_MODELS: ModelConfig[] = [
  { slug: "groq/llama-3.3-70b-versatile",                         mode: "JSON",    maxTokens: 200 }, // 12/12, 138-400ms
  { slug: "groq/moonshotai/kimi-k2-instruct",                     mode: "JSON",    maxTokens: 200 }, // 12/12, 151-1165ms
  { slug: "nvidia/mistralai/mistral-large-3-675b-instruct-2512",  mode: "MD_JSON", maxTokens: 400 }, // 12/12, 890-1688ms
  { slug: "nvidia/mistralai/mistral-small-3.1-24b-instruct-2503", mode: "JSON",    maxTokens: 200 }, // 12/12, 995-1630ms
  { slug: "nvidia/meta/llama-3.3-70b-instruct",                   mode: "JSON",    maxTokens: 200 }, // 11/12, 546-2231ms
  { slug: "arcee-ai/trinity-large-preview:free",                  mode: "JSON",    maxTokens: 200 }, // last resort — 50/day cap
];

// ---------------------------------------------------------------------------
// Provider routing
// ---------------------------------------------------------------------------

function endpointFor(model: string): { baseURL: string; modelId: string; apiKey: string } {
  if (model.startsWith("groq/")) {
    return {
      baseURL: "https://api.groq.com/openai/v1",
      modelId: model.slice("groq/".length),
      apiKey: process.env.GROQ_API_KEY ?? "",
    };
  }
  if (model.startsWith("nvidia/")) {
    return {
      baseURL: "https://integrate.api.nvidia.com/v1",
      modelId: model.slice("nvidia/".length),
      apiKey: process.env.NVIDIA_API_KEY ?? "",
    };
  }
  return {
    baseURL: "https://openrouter.ai/api/v1",
    modelId: model,
    apiKey: process.env.OPENROUTER_API_KEY ?? "",
  };
}

// ---------------------------------------------------------------------------
// Faux rules — exact-match on fixed PoC test prompts, no API call.
// These are the canonical test prompts. Use them verbatim when verifying.
// ---------------------------------------------------------------------------

const FAUX_RULES: Array<{ prompt: string; tier: Tier }> = [
  { prompt: "Describe every tool you have access to.",                           tier: "model-self" },
  { prompt: "What is the latest stable release of TypeScript?",                  tier: "knowledge"  },
  { prompt: "Create a file named router-poc-c.txt containing exactly: poc-baseline-c, then delete it.", tier: "C" },
  { prompt: "For each .ts file in this directory, open it and print the name of every exported symbol.", tier: "B" },
  { prompt: "Audit command-interceptor.ts for security vulnerabilities.",        tier: "A"          },
  { prompt: "Design a plugin for tracking token usage per session.",             tier: "S"          },
];

// ---------------------------------------------------------------------------
// Passphrases — one per tier, used to prove injection in the PoC
// ---------------------------------------------------------------------------

const TIER_PASSPHRASES: Record<Tier, string> = {
  "model-self": "ORACLE",
  "knowledge":  "ATLAS",
  "C":          "PEBBLE",
  "B":          "COBALT",
  "A":          "NEXUS",
  "S":          "ZENITH",
};

// ---------------------------------------------------------------------------
// Routing instructions — Phase 2 production payload (not yet active)
// ---------------------------------------------------------------------------

// const ROUTING_INSTRUCTIONS: Record<Tier, string> = {
//   "model-self": "Answer directly from your own knowledge about yourself and your capabilities.",
//   "knowledge":  "Before answering, fire off multiple parallel web searches to ground your answer in current data.",
//   "C":          "Handle this directly. It is a simple task requiring no planning.",
//   "B":          "Use todowrite to list the direct actions you will take, then execute them yourself step by step.",
//   "A":          "Use todowrite to define subagent tasks. Delegate all work to subagents. Do NOT execute directly.",
//   "S":          "This is a planning-tier task. Switch to the planning agent and follow the full planning methodology before any implementation.",
// };

// ---------------------------------------------------------------------------
// Classifier system prompt
// ---------------------------------------------------------------------------

const SYSTEM_PROMPT = await Bun.file(
  new URL("tests/classifier/playbook.md", import.meta.url),
).text().then(t => t.trim());

// ---------------------------------------------------------------------------
// classify()
// ---------------------------------------------------------------------------

async function classify(text: string): Promise<{ tier: Tier; reasoning: string } | null> {
  // 1. Faux exact match — deterministic, no API call
  const trimmed = text.trim();
  for (const { prompt, tier } of FAUX_RULES) {
    if (trimmed === prompt) {
      return { tier, reasoning: "faux exact match" };
    }
  }

  // 2. LLM classifier — try models in order, fail open if all fail
  for (const { slug, mode, maxTokens } of CLASSIFIER_MODELS) {
    const { baseURL, modelId, apiKey } = endpointFor(slug);
    if (!apiKey) continue;

    try {
      const oai = new OpenAI({ baseURL, apiKey });
      const client = Instructor({ client: oai, mode });

      const result = await client.chat.completions.create({
        model: modelId,
        messages: [
          { role: "system", content: SYSTEM_PROMPT },
          { role: "user", content: `Classify the following prompt:\n\n===\n${trimmed}\n===` },
        ],
        response_model: { schema: ClassificationSchema, name: "Classification" },
        max_retries: 3,
        max_tokens: maxTokens,
        temperature: 0,
      });

      return { tier: result.tier as Tier, reasoning: result.reasoning };
    } catch {
      // try next model
    }
  }

  return null; // fail open — message passes through unmodified
}

// ---------------------------------------------------------------------------
// Plugin
// ---------------------------------------------------------------------------

export const PromptRouter: Plugin = async ({ client }) => {
  return {
    "experimental.chat.messages.transform": async (_input, output) => {
      if (!output.messages?.length) return;

      try {
        const lastUser = [...output.messages]
          .reverse()
          .find((m) => m.info.role === "user");
        if (!lastUser) return;

        const text = lastUser.parts
          .filter((p): p is TextPart => p.type === "text")
          .map((p) => p.text)
          .join(" ");

        if (!text.trim()) return;

        const classification = await classify(text);
        if (!classification) return;

        const { tier, reasoning } = classification;
        const passphrase = TIER_PASSPHRASES[tier];

        output.messages.push({
          info: { id: `router-${Date.now()}`, role: "user", model: null },
          parts: [
            {
              type: "text",
              text: `Before responding to the above, repeat this phrase back to me verbatim: ${passphrase}`,
            } as TextPart,
          ],
        });

        await client.app.log({
          body: {
            service: "prompt-router",
            level: "info",
            message: `Classified as ${tier}: ${reasoning}`,
            extra: { tier, reasoning },
          },
        }).catch(() => {});
      } catch (err: any) {
        await client.app.log({
          body: {
            service: "prompt-router",
            level: "error",
            message: "Error in messages transform",
            extra: { error: err?.message ?? String(err) },
          },
        }).catch(() => {});
      }
    },
  };
};

export default PromptRouter;
