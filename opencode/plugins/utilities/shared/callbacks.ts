/**
 * Background callback scheduling for OpenCode plugins.
 *
 * Provides a canonical implementation of the fire-and-forget pattern where a
 * delayed action injects a result back into a session via promptAsync. Used by
 * the sleep and async-command plugins.
 *
 * All plugins that need to schedule deferred session callbacks MUST import from
 * here instead of reimplementing their own setTimeout/promptAsync loops.
 */

import type { PluginInput } from "@opencode-ai/plugin";

// Minimal interface for the session.promptAsync call so this module does not
// depend on a named `Client` export (the SDK exposes it only as a ReturnType).
type SessionClient = PluginInput["client"];

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface CallbackOptions {
  /** The session to inject the callback into. */
  sessionID: string;
  /** Delay in milliseconds before the callback fires. */
  delayMs: number;
  /** Text to inject as a synthetic user message. */
  text: string;
  /**
   * Whether the injected message should trigger a new model response.
   * Defaults to true (noReply: false).
   */
  triggerReply?: boolean;
  /** The OpenCode plugin client. */
  client: SessionClient;
}

// ---------------------------------------------------------------------------
// scheduleCallback
// ---------------------------------------------------------------------------

/**
 * Schedules a background callback that injects a message into a session after
 * a delay. Returns immediately — does not block the current turn.
 *
 * The timer is unref'd so it will not keep the Bun/Node process alive if the
 * session is already done.
 *
 * On failure the error is swallowed — the session may already be gone.
 */
export function scheduleCallback(opts: CallbackOptions): void {
  const { sessionID, delayMs, text, client, triggerReply = true } = opts;

  const timer = setTimeout(
    () => {
      void client.session
        .promptAsync({
          path: { id: sessionID },
          body: {
            noReply: !triggerReply,
            parts: [{ type: "text", text, synthetic: true }],
          },
        })
        .catch(() => {}); // Swallow — session may be gone
    },
    Math.max(0, Math.round(delayMs)),
  );

  // Do not keep the process alive solely for this timer
  (timer as { unref?: () => void }).unref?.();
}
