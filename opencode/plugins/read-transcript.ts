import { isPluginEnabled } from "./plugins_config";
// Custom tool: read_transcript - exports and parses a session transcript to a file,
// returning head/tail preview and the file path for full review.
import { type Plugin, tool } from "@opencode-ai/plugin";

const PARSER_SCRIPT =
  "/home/dzack/.config/agents/skills/reading-transcripts/scripts/parse_opencode_log.py";

const PREVIEW_LINES = 30;

export const ReadTranscriptPlugin: Plugin = async ({ $, client }) => {
  if (!isPluginEnabled("read-transcript")) return {};

  return {
    tool: {
      read_transcript: tool({
        description:
          'Use when you need to read a session transcript. Requires a session ID starting with "ses_" (use the introspection tool to get your own).',
        args: {
          session_id: tool.schema.string(),
        },
        async execute(args) {
          const { session_id } = args;

          // Validate session exists before attempting export
          const { data: session } = await client.session.get({
            path: { id: session_id },
          });
          if (!session) {
            return `Session not found: ${session_id}\nUse list_sessions to find valid session IDs.`;
          }

          const outPath = `/tmp/transcript-${session_id}.txt`;

          try {
            await $`python ${PARSER_SCRIPT} ${session_id} > ${outPath}`.quiet();
          } catch (err: any) {
            const stderr = err?.stderr?.toString?.() ?? String(err);
            await client.app.log({
              body: {
                service: "read-transcript",
                level: "error",
                message: `Export failed for session ${session_id}`,
                extra: { stderr },
              },
            });
            return `Failed to export session ${session_id}: ${stderr || err}`;
          }

          const lines = (await $`wc -l < ${outPath}`.text()).trim();
          const totalLines = parseInt(lines, 10);

          if (totalLines === 0) {
            return `Export succeeded but produced no output for session ${session_id}.`;
          }

          const head = (
            await $`head -n ${PREVIEW_LINES} ${outPath}`.text()
          ).trim();
          const tail = (
            await $`tail -n ${PREVIEW_LINES} ${outPath}`.text()
          ).trim();

          const parts = [
            `Transcript saved to: ${outPath}`,
            `Total lines: ${totalLines}`,
            "",
            `=== FIRST ${PREVIEW_LINES} LINES ===`,
            head,
          ];

          if (totalLines > PREVIEW_LINES * 2) {
            parts.push(
              "",
              `... ${totalLines - PREVIEW_LINES * 2} lines omitted ...`,
              "",
              `=== LAST ${PREVIEW_LINES} LINES ===`,
              tail,
            );
          }

          return parts.join("\n");
        },
      }),
    },
  };
};
