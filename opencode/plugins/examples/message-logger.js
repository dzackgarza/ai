// Logs message parts to file
export const MessageLogger = async ({ $, directory }) => {
  return {
    event: async ({ event }) => {
      if (event.type !== "message.part.updated") return;

      const part = event.properties?.part;
      if (!part || part.type !== "text") return;

      const text = part.text;
      if (!text) return;

      const logPath = `${directory}/.opencode/messages.log`;
      await $`echo -e "[${new Date().toISOString()}] ${text}" >> ${logPath}`;
    },
  };
};
