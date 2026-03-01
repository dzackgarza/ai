import type { Plugin } from "@opencode-ai/plugin";
import { KILLSWITCHES } from "./killswitches";

// ─────────────────────────────────────────────────────────────────────────────
// CoT Mid-Stream Interceptor — Test Plugin
//
// Tests the branch-pruning pattern:
//   1. Accumulate chain-of-thought text as it streams via message.part.delta
//   2. Detect trigger word in reasoning
//   3. Abort the stream and re-prompt with a corrective instruction
//
// Test prompt (use with --thinking or a thinking-enabled model):
//   "Think for 3 steps before answering: what is 12^3, and how do you compute it?"
//
// step-3.5's system prompt often causes it to classify tasks in CoT
// (e.g. "This is a trivial task..."). This plugin intercepts that and
// challenges the model to reconsider.
//
// To enable: place (or symlink) this file in your plugins directory.
// To disable: remove it.
// ─────────────────────────────────────────────────────────────────────────────

const TRIGGER_WORD = "trivial";

const CORRECTIVE_PROMPT =
  "In your CoT, you classified this task as trivial. Think carefully about whether or not you underestimated this task.";

export const CotTrivialInterceptor: Plugin = async ({ client }) => {
  // partID → sessionID for parts we know are reasoning type
  const reasoningPartSessions = new Map<string, string>();

  // sessionID → accumulated CoT text so far
  const cotAccumulator = new Map<string, string>();

  // Sessions already intercepted — prevents double-firing if more deltas
  // arrive after abort() is called but before the stream actually stops
  const intercepted = new Set<string>();

  return {
    event: async ({ event }) => {
      // Killswitch check - no-op if disabled
      if (!KILLSWITCHES.cotTrivialInterceptor) return;
      // Comment out to enable
      return;
      // ── Track which partIDs are reasoning parts ───────────────────────────
      if (event.type === "message.part.updated") {
        const part = (event as any).properties?.part;
        if (part?.type === "reasoning" && part?.id && part?.sessionID) {
          reasoningPartSessions.set(part.id, part.sessionID);
        }
        return;
      }

      // ── Accumulate and check CoT deltas ──────────────────────────────────
      if (event.type === "message.part.delta") {
        const props = (event as any).properties;
        const { partID, sessionID, field, delta } = props ?? {};

        if (!partID || !sessionID || field !== "text") return;
        if (!reasoningPartSessions.has(partID)) return;
        if (intercepted.has(sessionID)) return;

        const accumulated = (cotAccumulator.get(sessionID) ?? "") + delta;
        cotAccumulator.set(sessionID, accumulated);

        if (!accumulated.toLowerCase().includes(TRIGGER_WORD)) return;

        // Mark intercepted immediately — more deltas may arrive before the
        // stream actually stops, and we must not fire abort() twice
        intercepted.add(sessionID);

        await client.session.abort({ path: { id: sessionID } });

        await client.session.prompt({
          path: { id: sessionID },
          body: {
            noReply: false,
            parts: [{ type: "text", text: CORRECTIVE_PROMPT }],
          },
        });
      }

      // ── Clean up per-session state after session ends ─────────────────────
      if (event.type === "session.deleted") {
        const sessionID = (event as any).properties?.sessionID;
        if (!sessionID) return;
        for (const [partID, sid] of reasoningPartSessions) {
          if (sid === sessionID) reasoningPartSessions.delete(partID);
        }
        cotAccumulator.delete(sessionID);
        intercepted.delete(sessionID);
      }
    },
  };
};
