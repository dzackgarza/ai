import type { Plugin } from '@opencode-ai/plugin';
import type { UserMessage } from '@opencode-ai/sdk';

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
      'You have acknowledged or simply observed information instead of acting upon it. This information was given to you to imply an obvious course of action, which you should now carry out. Only if there is genuine ambiguity should you ask the user what to do.',
  },
  {
    phrases: ['i will', 'i am continuing', 'continuing to'],
    response:
      'Do not simply announce intentions - follow through with the intended actions now, or use sleep/sleep_until if the next action should be delayed.',
  },
  {
    phrases: ['not completed:'],
    response:
      'If there is an unambiguous outstanding tasks or incomplete work, you should simply complete it.',
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

      if (!messages) {
        await client.app.log({
          body: {
            service: 'next-steps-hook',
            level: 'error',
            message: `No messages found in session ${sessionID}`,
          },
        });
        return;
      }

      // 3. Extract last assistant message text
      const lastAssistant = messages
        .slice()
        .reverse()
        .find((m) => m.info.role === 'assistant');

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
        // 5. Get the last user message to extract the current model
        const lastUserMessage = messages
          .slice()
          .reverse()
          .find(
            (m): m is { info: UserMessage; parts: any[] } => m.info.role === 'user',
          );

        if (!lastUserMessage) {
          await client.app.log({
            body: {
              service: 'next-steps-hook',
              level: 'error',
              message: 'No user message found in session history',
            },
          });
          return;
        }

        // 6. Inject the corresponding response using the same model
        await client.session.promptAsync({
          path: { id: sessionID },
          body: {
            model: {
              providerID: lastUserMessage.info.model.providerID,
              modelID: lastUserMessage.info.model.modelID,
            },
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
