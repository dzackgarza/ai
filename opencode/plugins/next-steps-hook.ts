import type { Plugin } from '@opencode-ai/plugin';

/**
 * Lookup table mapping trigger phrases to response messages.
 * Each entry contains:
 *   - phrases: array of trigger phrases (case-insensitive match)
 *   - response: the message to inject when any phrase matches
 */
const PHRASE_LOOKUP: Array<{ phrases: string[]; response: string }> = [
  {
    phrases: ['next steps', 'should i continue'],
    response:
      'Record all of your next steps in a todo list, update and maintain your plan file, and proceed with all steps.',
  },
  {
    phrases: ['acknowledged', 'confirmed'],
    response:
      'Information is never given to simply be acknowledged, and is always meant to be acted upon.',
  },
  {
    phrases: ['i will', 'i am continuing', 'continuing to'],
    response:
      'Do not simply announce intentions - follow through with the intended actions now, or use sleep/sleep_until if the next action should be delayed.',
  },
];

export const NextStepsHookPlugin: Plugin = async ({ client }) => {
  return {
    event: async ({ event }) => {
      // 1. Listen for session.idle event
      if (event.type !== 'session.idle') return;

      const sessionID = event.properties.sessionID;

      // 2. Fetch messages to get the last assistant response
      const { data: messages } = await client.session.messages({
        path: { id: sessionID },
      });

      // 3. Extract last assistant message text
      const lastAssistant = [...messages]
        .reverse()
        .find((m: any) => m.info.role === 'assistant');

      const lastText = lastAssistant?.parts
        ?.filter((p: any) => p.type === 'text')
        ?.map((p: any) => p.text)
        ?.join('');

      // 4. Check for trigger phrases and get matching response
      const normalizedText = lastText?.toLowerCase() ?? '';
      const matchedEntry = PHRASE_LOOKUP.find((entry) =>
        entry.phrases.some((phrase) => normalizedText.includes(phrase.toLowerCase())),
      );

      if (matchedEntry) {
        // 5. Inject the corresponding response
        await client.session.promptAsync({
          path: { id: sessionID },
          body: {
            noReply: false,
            parts: [
              {
                type: 'text',
                text: matchedEntry.response,
              },
            ],
          },
        });
      }
    },
  };
};
