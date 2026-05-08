import { type Plugin, tool } from "@opencode-ai/plugin"

export const CanonicalSmokeFileproofPlugin: Plugin = async (_ctx) => {
  return {
    tool: {
      mytool_fileproof_20260310: tool({
        description: "This is a custom tool",
        args: {
          foo: tool.schema.string(),
        },
        async execute(_args, _context) {
          return "PASS_MYTOOL_FILEPROOF_20260310"
        },
      }),
    },
  }
}
