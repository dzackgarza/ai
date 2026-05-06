// Adds custom tools to OpenCode
import { type Plugin, tool } from "@opencode-ai/plugin";

export const CustomToolsPlugin: Plugin = async (_ctx) => {
  return {
    tool: {
      mytool: tool({
        description: "This is a custom tool",
        args: {
          foo: tool.schema.string(),
        },
        async execute(args, context) {
          const { directory, worktree: _worktree } = context;
          return `Hello ${args.foo} from ${directory}`;
        },
      }),
    },
  };
};
