import type { Plugin } from '@opencode-ai/plugin';
import type { TextPart, UserMessage } from '@opencode-ai/sdk';

/**
 * Transcript Timestamp Plugin
 *
 * Injects current timestamp and session ID into the messages sent to the LLM
 * so the model has wall-clock datetime awareness when reading its conversation history.
 */
export const TranscriptTimestampPlugin: Plugin = async ({ client, directory }) => {
  return {
    'experimental.chat.messages.transform': async (input, output) => {
      if (!output.messages?.length) return;

      const now = new Date().toISOString();
      const sessionId = (input as any).sessionID ?? '';

      const text = `[Session ID: ${sessionId}, Timestamp: ${now}, CWD: ${directory}]`;

      output.messages.push({
        info: {
          id: 'injected-timestamp',
          role: 'user',
          sessionID: sessionId,
          time: { created: Date.now() },
        } as UserMessage,
        parts: [{ type: 'text', text } as TextPart],
      });
    },
  };
};
