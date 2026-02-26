// Hello world plugin - logs ROT13 of model responses
export const Rot13Logger = async ({ $, directory }) => {
  return {
    event: async ({ event }) => {
      // message.part.updated contains the actual text parts
      if (event.type !== "message.part.updated") return;

      const part = event.properties?.part;
      if (!part || part.type !== "text") return;

      const text = part.text;
      if (!text) return;

      // Only log assistant (model) responses
      const messageID = part.messageID;
      // We need to check if this is an assistant message
      // Let's also listen to message.updated to track roles

      // For now, log everything and let user filter
      const rot13 = text.replace(/[a-zA-Z]/g, (c) => {
        const base = c <= "Z" ? 65 : 97;
        return String.fromCharCode(((c.charCodeAt(0) - base + 13) % 26) + base);
      });

      // Write to file
      const logPath = `${directory}/.opencode/rot13-responses.log`;
      const timestamp = new Date().toISOString();

      await $`echo -e "[${timestamp}]\n${text}\n→ ${rot13}\n" >> ${logPath}`;
    },
  };
};
