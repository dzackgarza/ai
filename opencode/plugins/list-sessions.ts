// Custom tool: list_sessions - lists all sessions with metadata
import { type Plugin, tool } from "@opencode-ai/plugin";
import type { AssistantMessage } from "@opencode-ai/sdk";

function formatTime(epoch: number): string {
  return new Date(epoch).toISOString();
}

function duration(startMs: number, endMs: number): string {
  const diffS = Math.floor((endMs - startMs) / 1000);
  if (diffS < 60) return `${diffS}s`;
  if (diffS < 3600) return `${Math.floor(diffS / 60)}m ${diffS % 60}s`;
  const h = Math.floor(diffS / 3600);
  const m = Math.floor((diffS % 3600) / 60);
  return `${h}h ${m}m`;
}

export const ListSessionsPlugin: Plugin = async ({ client }) => {
  return {
    tool: {
      list_sessions: tool({
        description:
          "Use when you need to list OpenCode sessions with their IDs, titles, timestamps, turns, models, and tokens.",
        args: {
          limit: tool.schema.number().optional(),
        },
        async execute(args) {
          const { data: sessions } = await client.session.list({});
          if (!sessions?.length) return "No sessions found.";

          // Sort by most recently updated first
          const sorted = [...sessions].sort(
            (a, b) => b.time.updated - a.time.updated,
          );
          const limited = sorted.slice(0, args.limit ?? 25);

          const lines: string[] = [
            `Total sessions: ${sessions.length} (showing ${limited.length})`,
            "",
          ];

          for (const s of limited) {
            const parts = [
              `ID: ${s.id}`,
              `  Title:   ${s.title}`,
              `  Created: ${formatTime(s.time.created)}`,
              `  Updated: ${formatTime(s.time.updated)}`,
              `  Duration: ${duration(s.time.created, s.time.updated)}`,
            ];

            if (s.summary) {
              parts.push(
                `  Changes: +${s.summary.additions} -${s.summary.deletions} (${s.summary.files} files)`,
              );
            }

            {
              const { data: messages } = await client.session.messages({
                path: { id: s.id },
              });
              if (messages?.length) {
                const userTurns = messages.filter(
                  (m) => m.info.role === "user",
                ).length;
                const assistantMsgs = messages.filter(
                  (m) => m.info.role === "assistant",
                );
                parts.push(
                  `  Turns: ${messages.length} total (${userTurns} user, ${assistantMsgs.length} assistant)`,
                );

                // Aggregate stats from assistant messages
                const modelCounts = new Map<string, number>();
                let inputTokens = 0;
                let outputTokens = 0;
                let reasoningTokens = 0;
                let cacheRead = 0;
                let cacheWrite = 0;

                for (const m of assistantMsgs) {
                  const info = m.info as AssistantMessage;
                  const model = `${info.providerID}/${info.modelID}`;
                  modelCounts.set(model, (modelCounts.get(model) ?? 0) + 1);
                  if (info.tokens) {
                    inputTokens += info.tokens.input;
                    outputTokens += info.tokens.output;
                    reasoningTokens += info.tokens.reasoning;
                    cacheRead += info.tokens.cache.read;
                    cacheWrite += info.tokens.cache.write;
                  }
                }

                const modelSummary = [...modelCounts]
                  .map(([m, n]) => (n > 1 ? `${m} ×${n}` : m))
                  .join(", ");
                parts.push(`  Models: ${modelSummary}`);
                const totalTokens =
                  inputTokens + outputTokens + reasoningTokens;
                parts.push(
                  `  Tokens: ${totalTokens.toLocaleString()} total (in: ${inputTokens.toLocaleString()}, out: ${outputTokens.toLocaleString()}, reasoning: ${reasoningTokens.toLocaleString()})`,
                );
                if (cacheRead || cacheWrite) {
                  parts.push(
                    `  Cache: read ${cacheRead.toLocaleString()}, write ${cacheWrite.toLocaleString()}`,
                  );
                }
              }
            }

            lines.push(parts.join("\n"));
          }

          lines.push(
            "",
            "Tip: Use read_transcript with a session ID to read the full transcript.",
          );

          return lines.join("\n\n");
        },
      }),
    },
  };
};
