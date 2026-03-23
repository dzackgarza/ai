import type { Plugin } from '@opencode-ai/plugin';

/**
 * Transcript Timestamp Plugin
 *
 * Injects current timestamp and session ID into the system context so the model
 * has wall-clock datetime awareness when reading its own conversation history.
 */
export const TranscriptTimestampPlugin: Plugin = async ({ client, directory }) => {
  return {
    'experimental.chat.system.transform': async (input, output) => {
      const now = new Date().toISOString();
      const sessionId = input.sessionID;

      // Inject timestamp metadata into system context
      output.system.push(
        `[Session ID: ${sessionId}, Timestamp: ${now}, CWD: ${directory}]`,
      );
    },
  };
};
