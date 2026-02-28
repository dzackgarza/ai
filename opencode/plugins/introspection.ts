// Custom tool: introspection - gives the agent access to its own session metadata
import { type Plugin, tool } from "@opencode-ai/plugin";

export const IntrospectionPlugin: Plugin = async () => {
  return {
    tool: {
      introspection: tool({
        description:
          "Use when you need to know your own session ID, message ID, or agent name.",
        args: {},
        async execute(_args, context) {
          return [
            `Session ID: ${context.sessionID}`,
            `Message ID: ${context.messageID}`,
            `Agent: ${context.agent}`,
          ].join("\n");
        },
      }),
    },
  };
};
