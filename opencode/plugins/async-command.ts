import { isPluginEnabled } from "./plugins_config";
// Custom tool: async_command - fires a background command without blocking the agent's current turn.
//
// When the command completes, it injects the result back via promptAsync():
//   - If the agent is idle: triggers a new response immediately.
//   - If the agent is mid-turn: the server queues the prompt; agent responds after the current
//     turn finishes. The agent is NOT interrupted.
//
// For now the only supported command is a timed sleep (seconds). This is intentional — the
// mechanism is what matters; the command surface can be extended later.

import { type Plugin, tool } from "@opencode-ai/plugin";

function fmt(d: Date): string {
  return d.toISOString();
}

async function runBackground(
  sessionID: string,
  seconds: number,
  client: any,
  message?: string,
): Promise<void> {
  const start = new Date();
  await new Promise((resolve) => setTimeout(resolve, seconds * 1000));
  const end = new Date();
  const elapsed = ((end.getTime() - start.getTime()) / 1000).toFixed(2);

  const lines = [
    `[async-command completed]`,
    `  Started:   ${fmt(start)}`,
    `  Completed: ${fmt(end)}`,
    `  Elapsed:   ${elapsed}s`,
    `  Passphrase: MANGO-DELTA-7`,
  ];
  if (message) lines.push(`  Message:   ${message}`);
  const result = lines.join("\n");

  await client.session.promptAsync({
    path: { id: sessionID },
    body: {
      // noReply: false — inject the result AND trigger a new model response.
      // If the session is currently busy, the server queues this until idle.
      noReply: false,
      parts: [{ type: "text", text: result, synthetic: true }],
    },
  });
}

export const AsyncCommandPlugin: Plugin = async ({ client }) => {
  if (!isPluginEnabled("async-command")) return {};
  return {
    tool: {
      async_command: tool({
        description:
          "Use when a background task should run without blocking the current work. The result is injected when the command finishes, whether the agent is idle or mid-turn.",
        args: {
          seconds: tool.schema.number(),
          message: tool.schema.string().optional(),
        },
        async execute(args, context) {
          const { sessionID } = context;
          const startedAt = new Date();

          // Fire and forget — do NOT await. Tool returns immediately.
          runBackground(sessionID, args.seconds, client, args.message).catch(async (err) => {
            // Best-effort: inject the error so the agent knows the task failed.
            await client.session.promptAsync({
              path: { id: sessionID },
              body: {
                noReply: false,
                parts: [
                  {
                    type: "text",
                    text: `[async-command failed]\n  Error: ${err?.message ?? String(err)}`,
                    synthetic: true,
                  },
                ],
              },
            }).catch(() => {}); // Swallow — session may be gone
          });

          return [
            `[async-command started]`,
            `  Session:  ${sessionID}`,
            `  Started:  ${fmt(startedAt)}`,
            `  Duration: ${args.seconds}s`,
            `  Expected: ${fmt(new Date(startedAt.getTime() + args.seconds * 1000))}`,
          ].join("\n");
        },
      }),
    },
  };
};
