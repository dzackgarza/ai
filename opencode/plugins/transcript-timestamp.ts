import type { Plugin } from '@opencode-ai/plugin';

/**
 * Transcript Timestamp Plugin
 *
 * Injects current timestamp, session ID, and CWD into the system prompt
 * so the model has wall-clock datetime awareness on every turn.
 */
export const TranscriptTimestampPlugin: Plugin = async ({ directory }) => {
  return {
    'experimental.chat.system.transform': async (input, output) => {
      const sessionId = (input as { sessionID?: string }).sessionID ?? '';
      const now = new Date().toISOString();
      const timestamp = `<system-information>Session ID: ${sessionId}, Timestamp: ${now}, CWD: ${directory}</system-information>`;

      // Push to system array
      output.system.push(timestamp);
    },
  };
};
