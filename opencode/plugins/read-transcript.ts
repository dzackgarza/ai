// Custom tool: read_transcript - exports and parses a session transcript to a file,
// returning head/tail preview and the file path for full review.
import { type Plugin, tool } from "@opencode-ai/plugin";

const PARSER_SCRIPT =
  "/home/dzack/.config/agents/skills/reading-transcripts/scripts/parse_opencode_log.py";

const PREVIEW_LINES = 30;

export const ReadTranscriptPlugin: Plugin = async ({ $ }) => {
  return {
    tool: {
      read_transcript: tool({
        description:
          "Use when you need to read a session transcript. Requires a session ID (use the introspection tool to get your own).",
        args: {
          session_id: tool.schema.string(),
        },
        async execute(args) {
          const { session_id } = args;
          const outPath = `/tmp/transcript-${session_id}.txt`;

          await $`opencode export ${session_id} | python ${PARSER_SCRIPT} - > ${outPath}`;

          const lines = (await $`wc -l < ${outPath}`.text()).trim();
          const totalLines = parseInt(lines, 10);

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
