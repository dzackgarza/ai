// Custom tool: list_sessions - lists all sessions with metadata
import { type Plugin, tool } from "@opencode-ai/plugin";

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
          "Use when you need to list OpenCode sessions with their IDs, titles, timestamps, and stats. Set include_turns=true to also count messages per session (slower).",
        args: {
          include_turns: tool.schema.boolean().optional(),
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

            if (args.include_turns) {
              const { data: messages } = await client.session.messages({
                path: { id: s.id },
              });
              const total = messages?.length ?? 0;
              const userTurns =
                messages?.filter((m) => m.info.role === "user").length ?? 0;
              const assistantTurns =
                messages?.filter((m) => m.info.role === "assistant").length ?? 0;
              parts.push(
                `  Turns: ${total} total (${userTurns} user, ${assistantTurns} assistant)`,
              );
            }

            lines.push(parts.join("\n"));
          }

          return lines.join("\n\n");
        },
      }),
    },
  };
};
