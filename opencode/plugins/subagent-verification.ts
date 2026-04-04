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
 * Injects a synthetic message into the parent session when a subagent (task tool)
 * completes, reminding the agent to verify the subagent's work rather than
 * accepting claims at face value.
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
