/**
 * DetailedEventLogger
 * 
 * This plugin logs every event received by OpenCode to a JSONL file.
 * It serves as a foundation for building other plugins by providing 
 * a way to observe the live data stream.
 */
export const DetailedEventLogger = async ({ $, directory }) => {
  const logDir = `${directory}/.opencode`;
  const logPath = `${logDir}/events.jsonl`;

  // Ensure the log directory exists
  await $`mkdir -p ${logDir}`;

  return {
    /**
     * The event hook is called for every system event.
     * Common event types include:
     * - message.updated
     * - message.part.updated
     * - tool.call.started
     * - tool.call.finished
     * - completion.started
     * - completion.finished
     */
    event: async ({ event }) => {
      try {
        const entry = {
          _timestamp: new Date().toISOString(),
          ...event,
        };

        // Append the event as a single line of JSON
        await $`echo ${JSON.stringify(entry)} >> ${logPath}`;
      } catch (err) {
        // Silently fail to avoid disrupting the main process
        console.error("DetailedEventLogger error:", err);
      }
    },
  };
};