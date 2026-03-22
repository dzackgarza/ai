import type { Plugin } from '@opencode-ai/plugin';

/**
 * Transcript Timestamp Plugin
 *
 * Injects current timestamp and session ID into the system context so the model
 * has wall-clock datetime awareness when reading its own conversation history.
 */
export const TranscriptTimestampPlugin: Plugin = async ({ client }) => {
  return {
    'experimental.chat.system.transform': async (input, output) => {
      const now = new Date().toISOString();
      const sessionId = input.sessionID;

      // Inject timestamp metadata into system context
      output.system.push(`
<session-metadata>
  Session ID: ${sessionId}
  Current Wall-Clock Time: ${now}
  
  Note: Use this timestamp to reason about time passage in this conversation.
  When referencing earlier messages, you can estimate their absolute time based on
  durations shown in context relative to this current timestamp.
</session-metadata>`);
    },
  };
};
