import { isPluginEnabled } from "./plugins_config";
// Custom tools: sleep / sleep_until - real wall-clock waiting
import { type Plugin, tool } from "@opencode-ai/plugin";

function fmt(d: Date): string {
  return d.toISOString();
}

const MAX_SECONDS = 60 * 60; // 60 minutes

async function doSleep(seconds: number, force = false): Promise<string> {
  if (seconds > MAX_SECONDS && !force) {
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
  const start = new Date();
  await new Promise((resolve) => setTimeout(resolve, seconds * 1000));
  const end = new Date();
  return `Slept ${seconds}s. Started: ${fmt(start)} — Ended: ${fmt(end)}`;
}

export const SleepPlugin: Plugin = async () => {
  if (!isPluginEnabled("sleep")) return {};
  return {
    tool: {
      sleep: tool({
        description:
          "Use when the agent needs to wait or pause for a real wall-clock duration before continuing. Use this instead of bash sleep commands.",
        args: {
          seconds: tool.schema.number(),
          force: tool.schema.boolean().optional(),
        },
        async execute(args) {
          return doSleep(args.seconds, args.force ?? false);
        },
      }),

      sleep_until: tool({
        description:
          "Use when the agent needs to wait until a specific wall-clock time before continuing. Use this instead of bash sleep commands.",
        args: {
          iso_timestamp: tool.schema.string(),
          force: tool.schema.boolean().optional(),
        },
        async execute(args) {
          const target = new Date(args.iso_timestamp);
          const seconds = Math.max(0, (target.getTime() - Date.now()) / 1000);
          return doSleep(seconds, args.force ?? false);
        },
      }),
    },
  };
};
