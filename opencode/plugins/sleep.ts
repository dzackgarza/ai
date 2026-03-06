import { isPluginEnabled } from "./plugins_config";
// Custom tools: sleep / sleep_until - real wall-clock waiting
import { type Plugin, tool } from "@opencode-ai/plugin";

function fmt(d: Date): string {
  return d.toISOString();
}

const MAX_SECONDS = 60 * 60; // 60 minutes

function parseSeconds(input: number): number | undefined {
  if (!Number.isFinite(input) || input < 0) return undefined;
  return input;
}

function formatScheduledSleep(input: {
  now: Date;
  seconds: number;
  wakeAt: Date;
  source: "sleep" | "sleep_until";
  timeoutBypassed: boolean;
}): string {
  return [
    "Scheduled background polling callback.",
    `  Source:         ${input.source}`,
    `  Current time:   ${fmt(input.now)}`,
    `  Wait duration:  ${input.seconds}s (${(input.seconds / 3600).toFixed(2)}h)`,
    `  Callback time:  ${fmt(input.wakeAt)}`,
    `  Safety limit:   ${MAX_SECONDS}s${input.timeoutBypassed ? " (bypassed via force=true)" : ""}`,
    "",
    "This tool returns immediately and does not block the current turn.",
    "A `noReply:false` callback will be sent at the scheduled time so the agent can act again if idle.",
  ].join("\n");
}

function formatSafetyRejection(seconds: number): string {
  const now = new Date();
  const expectedEnd = new Date(now.getTime() + seconds * 1000);
  return [
    `Rejected: requested sleep exceeds the 60-minute safety limit.`,
    ``,
    `  Current time:  ${fmt(now)}`,
    `  Requested:     ${seconds}s (${(seconds / 3600).toFixed(2)}h)`,
    `  Expected end:  ${fmt(expectedEnd)}`,
    ``,
    `If this schedule is intentional, rerun with force=true to bypass the limit.`,
  ].join("\n");
}

export const SleepPlugin: Plugin = async ({ client }) => {
  if (!isPluginEnabled("sleep")) return {};

  const scheduleWakeCallback = (input: {
    sessionID: string;
    seconds: number;
    source: "sleep" | "sleep_until";
    requestedAt: Date;
    wakeAt: Date;
  }): void => {
    const delayMs = Math.max(0, Math.round(input.seconds * 1000));
    const timer = setTimeout(() => {
      const firedAt = new Date();
      const callbackText = [
        "[sleep_poll_callback]",
        "status: fired",
        `source: ${input.source}`,
        `requested_at: ${fmt(input.requestedAt)}`,
        `scheduled_for: ${fmt(input.wakeAt)}`,
        `fired_at: ${fmt(firedAt)}`,
        "message: Requested wait completed. Continue with the next action if this callback is still relevant.",
      ].join("\n");
      void client.session
        .promptAsync({
          path: { id: input.sessionID },
          body: {
            noReply: false,
            parts: [{ type: "text", text: callbackText, synthetic: true }],
          },
        })
        .catch(() => {});
    }, delayMs);
    (timer as { unref?: () => void }).unref?.();
  };

  const queueSleep = (input: {
    sessionID: string;
    seconds: number;
    force: boolean;
    source: "sleep" | "sleep_until";
  }): string => {
    if (input.seconds > MAX_SECONDS && !input.force) {
      return formatSafetyRejection(input.seconds);
    }

    const now = new Date();
    const wakeAt = new Date(now.getTime() + input.seconds * 1000);
    scheduleWakeCallback({
      sessionID: input.sessionID,
      seconds: input.seconds,
      source: input.source,
      requestedAt: now,
      wakeAt,
    });

    return formatScheduledSleep({
      now,
      seconds: input.seconds,
      wakeAt,
      source: input.source,
      timeoutBypassed: input.seconds > MAX_SECONDS && input.force,
    });
  };

  return {
    tool: {
      sleep: tool({
        description:
          "Use when the agent needs to wait or pause for a real wall-clock duration before continuing. Use this instead of bash sleep commands.",
        args: {
          seconds: tool.schema.number(),
          force: tool.schema.boolean().optional(),
        },
        async execute(args, context) {
          const seconds = parseSeconds(args.seconds);
          if (seconds === undefined) {
            return `Invalid seconds: ${String(args.seconds)}. Expected a finite non-negative number.`;
          }
          return queueSleep({
            sessionID: context.sessionID,
            seconds,
            force: args.force ?? false,
            source: "sleep",
          });
        },
      }),

      sleep_until: tool({
        description:
          "Use when the agent needs to wait until a specific wall-clock time before continuing. Use this instead of bash sleep commands.",
        args: {
          iso_timestamp: tool.schema.string(),
          force: tool.schema.boolean().optional(),
        },
        async execute(args, context) {
          const target = new Date(args.iso_timestamp);
          if (Number.isNaN(target.getTime())) {
            return `Invalid iso_timestamp: ${JSON.stringify(args.iso_timestamp)}. Expected an ISO-8601 timestamp.`;
          }
          const seconds = Math.max(0, (target.getTime() - Date.now()) / 1000);
          return queueSleep({
            sessionID: context.sessionID,
            seconds,
            force: args.force ?? false,
            source: "sleep_until",
          });
        },
      }),
    },
  };
};
