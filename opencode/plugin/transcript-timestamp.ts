import type { Plugin } from '@opencode-ai/plugin';

/**
 * Transcript Timestamp Plugin
 *
 * Appends timestamp and session ID metadata to significant events in the transcript
 * so that future model contexts have wall-clock datetime information when reading
 * historical transcripts.
 */
export const TranscriptTimestampPlugin: Plugin = async ({ client }) => {
  return {
    event: async ({ event }) => {
      const sessionId =
        (event as any).properties?.sessionID || (event as any).sessionID;

      // Only process events that have a session ID and appear in transcripts
      if (!sessionId) return;

      const timestamp = new Date().toISOString();
      const metadata = `[Session ID: ${sessionId}, Timestamp: ${timestamp}]`;

      // Inject timestamp on key transcript events
      if (event.type === 'session.created') {
        await client.session.promptAsync({
          path: { id: sessionId },
          body: {
            parts: [
              {
                type: 'text',
                text: `<!-- ${metadata} Session started -->`,
              },
            ],
            noReply: true, // Don't trigger agent response
          },
        });
      }

      if (event.type === 'message.updated') {
        const message = (event as any).properties?.message;

        // Only timestamp user messages to avoid noise
        if (message?.role === 'user') {
          await client.session.promptAsync({
            path: { id: sessionId },
            body: {
              parts: [
                {
                  type: 'text',
                  text: `<!-- ${metadata} User message received -->`,
                },
              ],
              noReply: true,
            },
          });
        }
      }

      if (event.type === 'session.idle') {
        // Agent just finished responding - mark the timestamp
        await client.session.promptAsync({
          path: { id: sessionId },
          body: {
            parts: [
              {
                type: 'text',
                text: `<!-- ${metadata} Agent turn completed -->`,
              },
            ],
            noReply: true,
          },
        });
      }
    },
  };
};
