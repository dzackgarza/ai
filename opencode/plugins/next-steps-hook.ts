import type { Plugin } from '@opencode-ai/plugin';

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

      // 4. Check for trigger phrases (normalized to lowercase)
      const normalizedText = lastText?.toLowerCase() ?? '';
      const triggers = ['next steps', 'should i continue'];
      const matched = triggers.some((t) => normalizedText.includes(t));

      if (matched) {
        // 5. Inject prompt to record next steps and continue
        await client.session.promptAsync({
          path: { id: sessionID },
          body: {
            noReply: false,
            parts: [
              {
                type: 'text',
                text: 'Record all of your next steps in a todo list, update and maintain your plan file, and proceed with all steps.',
              },
            ],
          },
        });
      }
    },
  };
};
