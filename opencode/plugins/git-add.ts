import { isPluginEnabled } from "./plugins_config";
// Custom tool: git_add - stages files for commit
import { type Plugin, tool } from "@opencode-ai/plugin";

export const GitAddPlugin: Plugin = async ({ $ }) => {
  if (!isPluginEnabled("git-add")) return {};
  return {
    tool: {
      git_add: tool({
        description:
          "Use when files need to be staged for commit. Accepts a list of file paths.",
        args: {
          files: tool.schema.array(tool.schema.string()),
        },
        async execute(args, context) {
          const { directory } = context;

          if (args.files.length === 0) {
            return "[git_add] No files specified.";
          }

          const result = await $`cd ${directory} && git add ${args.files}`.nothrow();

          if (result.exitCode !== 0) {
            const output = result.stderr?.toString().trim() || result.stdout?.toString().trim() || "hook failed";
            return `[git_add] Hook rejected: ${output}`;
          }

          return `[git_add] Staged ${args.files.length} file(s).`;
        },
      }),
    },
  };
};
