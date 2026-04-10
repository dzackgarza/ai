import type { Plugin } from '@opencode-ai/plugin';
import { readFileSync } from 'fs';

import {
  MISSING_SESSION_IDENTITY_MESSAGE,
  observedSessionIdentity,
} from './session-identity';

const PROMPT_PATH = '/home/dzack/ai/opencode/plugins/subagent-verification-prompt.txt';

/**
 * Subagent Verification Hook
 *
 * Injects a lightweight reminder into the parent session when a subagent
 * completes, prompting the agent to load the review skill if needed and decide
 * whether deeper verification is warranted.
 */
export const SubagentVerificationPlugin: Plugin = async ({ client }) => {
  return {
    'tool.execute.after': async (input) => {
      if (input.tool !== 'task') return;

      const parentSessionID = input.sessionID;
      const verificationPrompt = readFileSync(PROMPT_PATH, 'utf-8');
      const { data: messages } = await client.session.messages({
        path: { id: parentSessionID },
      });
      const identity = observedSessionIdentity(messages);

      if (!identity) {
        await client.app.log({
          body: {
            service: 'subagent-verification',
            level: 'error',
            message: MISSING_SESSION_IDENTITY_MESSAGE,
          },
        });
        return;
      }

      // Queue a follow-up turn so the parent actually resumes and verifies the
      // subagent result instead of silently staying idle.
      await client.session.promptAsync({
        path: { id: parentSessionID },
        body: {
          agent: identity.agent,
          model: identity.model,
          noReply: false,
          parts: [{ type: 'text', text: verificationPrompt, synthetic: true }],
        },
      });
    },
  };
};
