// Custom tool: git_commit - runs git commit with the provided message
import { type Plugin, tool } from "@opencode-ai/plugin";

export const GitCommitPlugin: Plugin = async ({ $ }) => {
  return {
    tool: {
      git_commit: tool({
        description:
          "Use when the staging area is ready and changes should be committed. MUST ensure git add has been run before calling.",
        args: {
          message: tool.schema.string(),
        },
        async execute(args, context) {
          const { directory } = context;

          const result =
            await $`cd ${directory} && git commit --allow-empty -m ${args.message}`.nothrow();

          if (result.exitCode !== 0) {
            const output =
              result.stderr?.toString().trim() ||
              result.stdout?.toString().trim() ||
              "hook failed";
            return `[git_commit] Hook rejected commit: ${output}`;
          }

          return (
            result.stdout?.toString().trim() || "[git_commit] Commit successful"
          );
        },
      }),
    },
  };
};
