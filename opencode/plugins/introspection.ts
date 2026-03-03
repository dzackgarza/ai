import { isPluginEnabled } from "./plugins_config";
// Custom tool: introspection - gives the agent access to its own session metadata
import { type Plugin, tool } from "@opencode-ai/plugin";

export const IntrospectionPlugin: Plugin = async ({ client }) => {
  if (!isPluginEnabled("introspection")) return {};
  return {
    tool: {
      introspection: tool({
        description:
          "Use when you need to know your own session ID, message ID, or agent name.",
        args: {},
        async execute(_args, context) {
          const { data: session } = await client.session.get({
            path: { id: context.sessionID },
          });

          return [
            `Session ID: ${context.sessionID}`,
            `Title: ${session?.title ?? "(unknown)"}`,
            `Message ID: ${context.messageID}`,
            `Agent: ${context.agent}`,
          ].join("\n");
        },
      }),
    },
  };
};
