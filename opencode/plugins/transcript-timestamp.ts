import type { Plugin } from '@opencode-ai/plugin';

/**
 * Transcript Timestamp Plugin
 *
 * Injects current timestamp, session ID, and CWD into the system prompt so the
 * model has wall-clock datetime awareness when reading its conversation history.
 */
export const TranscriptTimestampPlugin: Plugin = async ({ directory }) => {
  return {
    'experimental.chat.system.transform': async (input, output) => {
      const now = new Date().toISOString();
      const parts = [`Timestamp: ${now}`, `CWD: ${directory}`];
      if (input.sessionID) parts.unshift(`Session ID: ${input.sessionID}`);
      output.system.push(`[${parts.join(', ')}]`);
    },
  };
};
