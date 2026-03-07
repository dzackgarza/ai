// Classifies every incoming user message and injects tier-specific behavioral
// instructions into the conversation so the main agent operates in the correct
// cognitive mode before acting.
//
// Tiers (see scripts/templates/tiers/*.md for full instructions):
//   model-self — answer from context/self-knowledge; use reading-transcripts for history
//   knowledge  — search before answering; never answer from training data
//   C          — act immediately; TodoWrite only if 3+ steps
//   B          — iterate uniformly across a set; TodoWrite the list first
//   A          — investigate before acting; delegate reads to subagents
//   S          — scope with todos, gather context, hand off to plan mode

import { appendFileSync } from "fs";
import { randomUUID } from "crypto";
import type { Plugin } from "@opencode-ai/plugin";
import type { TextPart, UserMessage } from "@opencode-ai/sdk";
import { callLLM, loadTemplate } from "../../utilities/shared/llm";

type Tier = "model-self" | "knowledge" | "C" | "B" | "A" | "S";

// ---------------------------------------------------------------------------
// Model list — ordered by preference; first success wins.
//
// All provider/mode logic lives in scripts/llm.py — this is just a slug list.
// ---------------------------------------------------------------------------

const CLASSIFIER_MODELS: string[] = [
  "groq/llama-3.3-70b-versatile",
  "groq/moonshotai/kimi-k2-instruct",
  "nvidia/mistralai/mistral-large-3-675b-instruct-2512",
  "nvidia/mistralai/mistral-small-3.1-24b-instruct-2503",
  "nvidia/meta/llama-3.3-70b-instruct",
  "arcee-ai/trinity-large-preview:free",
];

// ---------------------------------------------------------------------------
// Session identity — stable per process for log correlation
// ---------------------------------------------------------------------------

const SESSION_ID = process.env.OPENCODE_SESSION_ID ?? randomUUID();
const LOG_PATH = "/var/sandbox/.prompt-router.log";

function appendLog(entry: {
  ts: string;
  session_id: string;
  prompt: string;
  tier: string;
  reasoning: string;
  injected: boolean;
}): void {
  try {
    appendFileSync(LOG_PATH, JSON.stringify(entry) + "\n");
  } catch {
    // Log directory may not exist in dev — silently skip
  }
}

// ---------------------------------------------------------------------------
// Faux rules — exact-match on canonical test prompts; no API call.
// Use these verbatim when verifying the injection pipeline end-to-end.
// ---------------------------------------------------------------------------

const FAUX_RULES: Array<{ prompt: string; tier: Tier }> = [
  { prompt: "Describe every tool you have access to.", tier: "model-self" },
  {
    prompt: "What is the latest stable release of TypeScript?",
    tier: "knowledge",
  },
  {
    prompt:
      "Create a file named router-poc-c.txt containing exactly: poc-baseline-c, then delete it.",
    tier: "C",
  },
  {
    prompt:
      "For each .ts file in this directory, open it and print the name of every exported symbol.",
    tier: "B",
  },
  {
    prompt: "Audit command-interceptor.ts for security vulnerabilities.",
    tier: "A",
  },
  {
    prompt: "Design a plugin for tracking token usage per session.",
    tier: "S",
  },
];

// ---------------------------------------------------------------------------
// Tier instructions + classifier system prompt — loaded from canonical
// scripts/templates/ via llm.py at startup.
// ---------------------------------------------------------------------------

const TIER_INSTRUCTIONS: Record<Tier, string> = Object.fromEntries(
  await Promise.all(
    (["model-self", "knowledge", "C", "B", "A", "S"] as const).map(
      async (tier) => [tier, await loadTemplate(`tiers/${tier}`)],
    ),
  ),
) as Record<Tier, string>;

const SYSTEM_PROMPT = await loadTemplate("classifier/playbook");

// ---------------------------------------------------------------------------
// classify()
// ---------------------------------------------------------------------------

async function classify(
  text: string,
): Promise<{ tier: Tier; reasoning: string } | null> {
  // 1. Faux exact match — deterministic, no API call
  const trimmed = text.trim();
  for (const { prompt, tier } of FAUX_RULES) {
    if (trimmed === prompt) {
      return { tier, reasoning: "faux exact match" };
    }
  }

  // 2. LLM classifier — llm.py handles provider routing, retries, fallback
  try {
    const result = await callLLM<{ tier: Tier; reasoning: string }>({
      models: CLASSIFIER_MODELS,
      messages: [
        { role: "system", content: SYSTEM_PROMPT },
        {
          role: "user",
          content: `Classify the following prompt:\n\n===\n${trimmed}\n===`,
        },
      ],
      schema: "Classification",
      temperature: 0,
      max_tokens: 200,
    });
    return result;
  } catch {
    return null; // fail open — message passes through unmodified
  }
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
        const instruction = TIER_INSTRUCTIONS[tier];

        output.messages.push({
          info: {
            id: `router-${Date.now()}`,
            role: "user",
            sessionID: "",
            time: { created: Date.now() },
          } as UserMessage,
          parts: [{ type: "text", text: instruction } as TextPart],
        });

        appendLog({
          ts: new Date().toISOString(),
          session_id: SESSION_ID,
          prompt: text.slice(0, 500),
          tier,
          reasoning,
          injected: true,
        });

        await client.app
          .log({
            body: {
              service: "prompt-router",
              level: "info",
              message: `Classified as ${tier}: ${reasoning}`,
              extra: { tier, reasoning },
            },
          })
          .catch(() => {});
      } catch (err: any) {
        await client.app
          .log({
            body: {
              service: "prompt-router",
              level: "error",
              message: "Error in messages transform",
              extra: { error: err?.message ?? String(err) },
            },
          })
          .catch(() => {});
      }
    },
  };
};

export default PromptRouter;
