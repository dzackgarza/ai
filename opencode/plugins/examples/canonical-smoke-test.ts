/*
Canonical smoke test temporarily disabled in the autoloaded plugin directory.
Active file:// copy:
/home/dzack/ai/opencode/tools/canonical-plugin-probes/canonical-smoke-fileproof.ts

import { type Plugin, tool } from "@opencode-ai/plugin"

export const CanonicalSmokeTestPlugin: Plugin = async (_ctx) => {
  return {
    tool: {
      mytool: tool({
        description: "This is a custom tool",
        args: {
          foo: tool.schema.string(),
        },
        async execute(_args, _context) {
          return "PASS_MYTOOL_SHADOW_PROBE_20260310"
        },
      }),
    },
  }
}
*/
