// Injects context before agent processes user message
import type { Plugin } from "@opencode-ai/plugin";
import type { TextPart } from "@opencode-ai/sdk";

const CONTEXT_RULES: Record<string, string> = {
  "verification code is 123456":
    "[Context] Please repeat the passphrase back in your response: banana",
};

export const ContextInjector: Plugin = async ({ client }) => {
  return {
    "experimental.chat.messages.transform": async (input, output) => {
      if (!output.messages?.length) return;

      try {
        const lastUser = [...output.messages]
          .reverse()
          .find((m) => m.info.role === "user");
        if (!lastUser) return;

        const text = lastUser.parts
          .filter((p): p is TextPart => p.type === "text")
          .map((p) => p.text)
          .join(" ");
        const lower = text.toLowerCase();

        for (const [keyphrase, injection] of Object.entries(CONTEXT_RULES)) {
          if (lower.includes(keyphrase)) {
            output.messages.push({
              info: { id: "injected", role: "user", model: null },
              parts: [{ type: "text", text: injection } as TextPart],
            });
            return;
          }
        }
      } catch (err: any) {
        await client.app.log({
          body: {
            service: "context-injector",
            level: "error",
            message: "Error in messages transform",
            extra: { error: err?.message ?? String(err) },
          },
        }).catch(() => {});
      }
    },
  };
};
