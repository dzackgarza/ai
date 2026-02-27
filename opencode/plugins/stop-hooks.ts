import type { Plugin } from "@opencode-ai/plugin";
import type { AssistantMessage, UserMessage, TextPart } from "@opencode-ai/sdk";
import type { StopHookFn, MessageWithParts } from "./stop_hooks/types";

// ═══════════════════════════════════════════════════════════════════════════════
// REGISTERED STOP HOOKS
//
// To add a new stop hook:
//   1. Create a file under stop_hooks/ (e.g. stop_hooks/my-checker.ts)
//   2. Export one async function: (ctx: StopHookContext) => Promise<StopHookResult>
//      See stop_hooks/types.ts for full context and return type docs.
//   3. Import it below and add it to STOP_HOOKS.
//
// DO NOT modify anything outside this section.
// ═══════════════════════════════════════════════════════════════════════════════

import { otpChecker } from "./stop_hooks/otp-checker";
import { reflexiveAgreementDetector } from "./stop_hooks/reflexive-agreement-detector";

const STOP_HOOKS: StopHookFn[] = [otpChecker, reflexiveAgreementDetector];

// ═══════════════════════════════════════════════════════════════════════════════
// MECHANISM — do not modify
// ═══════════════════════════════════════════════════════════════════════════════

function extractText(message: MessageWithParts): string {
  return message.parts
    .filter((p): p is TextPart => p.type === "text")
    .map((p) => p.text)
    .join("");
}

export const StopHooks: Plugin = async ({ client }) => {
  const lastSeenMessageId = new Map<string, string>();

  return {
    event: async ({ event }) => {
      // Comment out to enable
      return;
      if (event.type !== "session.idle") return;

      const sessionId = event.properties.sessionID;

      const { data: messages } = await client.session.messages({
        path: { id: sessionId },
      });
      if (!messages || messages.length === 0) return;

      const lastMessage = messages[messages.length - 1];
      if (lastMessage.info.role !== "assistant") return;

      // Deduplicate: skip if we already processed this message
      if (lastSeenMessageId.get(sessionId) === lastMessage.info.id) return;
      lastSeenMessageId.set(sessionId, lastMessage.info.id);

      const lastText = extractText(lastMessage);
      const lastUserMessage = [...messages]
        .reverse()
        .find((m) => m.info.role === "user") as
        | { info: UserMessage; parts: MessageWithParts["parts"] }
        | undefined;

      const ctx = {
        sessionId,
        client,
        messages,
        lastMessage: lastMessage as {
          info: AssistantMessage;
          parts: MessageWithParts["parts"];
        },
        lastText,
        lastUserMessage,
      };

      const results = await Promise.all(STOP_HOOKS.map((fn) => fn(ctx)));

      if (!results.some((r) => r.force_stop)) return;

      const feedbackLines = results
        .filter((r) => r.agent_feedback)
        .map((r) => `• ${r.agent_feedback}`);

      const report = [
        "**[Stop Hook Report]**",
        "",
        "One or more stop conditions were triggered:",
        "",
        ...feedbackLines,
      ].join("\n");

      await client.session.prompt({
        path: { id: sessionId },
        body: {
          noReply: false,
          parts: [{ type: "text", text: report }],
        },
      });
    },
  };
};
