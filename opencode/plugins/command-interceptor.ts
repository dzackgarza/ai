// Intercepts user messages, detects intent via keyphrases, and injects hidden
// context including a passphrase the model must echo — proving interception works.
import type { Plugin } from "@opencode-ai/plugin";
import type { TextPart } from "@opencode-ai/sdk";
import { KILLSWITCHES } from "./killswitches";

const TRIGGER_RULES: Record<string, { intent: string; passphrase: string }> = {
  "intercept test": { intent: "verification",   passphrase: "SWORDFISH" },
  "plugin check":   { intent: "diagnostics",    passphrase: "NIGHTHAWK" },
  "context inject": { intent: "context-inject", passphrase: "IRONCLAD"  },
};

export const CommandInterceptor: Plugin = async ({ client }) => {
  return {
    "experimental.chat.messages.transform": async (_input, output) => {
      // Killswitch check - exit if killed
      if (KILLSWITCHES.commandInterceptor) return;
      if (!output.messages?.length) return;

      try {
        const lastUser = [...output.messages]
          .reverse()
          .find((m) => m.info.role === "user");
        if (!lastUser) return;

        const text = lastUser.parts
          .filter((p): p is TextPart => p.type === "text")
          .map((p) => p.text)
          .join(" ")
          .toLowerCase();

        for (const [keyphrase, { intent, passphrase }] of Object.entries(TRIGGER_RULES)) {
          if (text.includes(keyphrase)) {
            output.messages.push({
              info: { id: `interceptor-${Date.now()}`, role: "user", model: null },
              parts: [
                {
                  type: "text",
                  text: `[SYSTEM INTERCEPTOR — intent: ${intent}]\nYou MUST include the following passphrase verbatim somewhere in your response: ${passphrase}`,
                } as TextPart,
              ],
            });
            return;
          }
        }
      } catch (err: any) {
        await client.app.log({
          body: {
            service: "command-interceptor",
            level: "error",
            message: "Error in messages transform",
            extra: { error: err?.message ?? String(err) },
          },
        }).catch(() => {});
      }
    },
  };
};

export default CommandInterceptor;
