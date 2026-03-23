import type { Plugin } from '@opencode-ai/plugin';
import type { TextPart, UserMessage } from '@opencode-ai/sdk';

/**
 * Transcript Timestamp Plugin
 *
 * Injects current timestamp, session ID, and CWD into the messages sent to the LLM
 * so the model has wall-clock datetime awareness when reading its conversation history.
 */
export const TranscriptTimestampPlugin: Plugin = async ({ directory }) => {
  return {
    'experimental.chat.messages.transform': async (_input, output) => {
      if (!output.messages?.length) return;

      const sessionId =
        output.messages
          .map((m) => (m.info as any).sessionID)
          .find((id) => typeof id === 'string' && id.length > 0) ?? '';

      const now = new Date().toISOString();
      output.messages.push({
        info: {
          id: 'injected-timestamp',
          role: 'user',
          sessionID: sessionId,
          time: { created: Date.now() },
        } as UserMessage,
        parts: [
          {
            type: 'text',
            text: `<system-information>Session ID: ${sessionId}, Timestamp: ${now}, CWD: ${directory}</system-information>`,
          } as TextPart,
        ],
      });
    },
  };
};
