import type { PluginInput } from "@opencode-ai/plugin";
import type { AssistantMessage, UserMessage, Message, Part } from "@opencode-ai/sdk";

// ─── Shared types for stop hook functions ────────────────────────────────────
//
// Import these in your checker file:
//   import type { StopHookContext, StopHookResult } from "./types";

export type MessageWithParts = {
  info: Message;
  parts: Part[];
};

/**
 * Context passed to every stop hook function.
 *
 * Available fields:
 *
 *   sessionId       - ID of the current session
 *   client          - OpenCode SDK client (call any SDK method you need)
 *   messages        - Full message history: each entry has `info` (role, id,
 *                     timestamps, model, token counts, errors, etc.) and `parts`
 *                     (text, tool calls, reasoning blocks, file refs, etc.)
 *   lastMessage     - The assistant message that just completed. Always role
 *                     "assistant". `info` is AssistantMessage (modelID, cost,
 *                     tokens, finish reason, path, etc.)
 *   lastText        - Convenience: all TextParts from lastMessage joined as one
 *                     string. Use this for simple pattern matching.
 *   lastUserMessage - The most recent user message in history (the prompt that
 *                     triggered this response), or undefined if none.
 */
export type StopHookContext = {
  sessionId: string;
  client: PluginInput["client"];
  messages: MessageWithParts[];
  lastMessage: { info: AssistantMessage; parts: Part[] };
  lastText: string;
  lastUserMessage: { info: UserMessage; parts: Part[] } | undefined;
};

/**
 * Return value for every stop hook function.
 *
 *   force_stop      - Set to true to trigger feedback injection. If ANY
 *                     registered hook returns true, all non-empty agent_feedback
 *                     strings are collected and sent to the agent as a report.
 *   agent_feedback  - The message to include in the report. Shown even if
 *                     force_stop is false (as long as some other hook fired).
 *                     Return "" to contribute nothing.
 */
export type StopHookResult = {
  force_stop: boolean;
  agent_feedback: string;
};

export type StopHookFn = (ctx: StopHookContext) => Promise<StopHookResult>;
