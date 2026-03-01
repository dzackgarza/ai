import type { StopHookContext, StopHookResult } from "./types";
import { ENABLED } from "../killswitches";

// Detects reflexive agreement phrases (e.g., "you're right", "they are right") in
// the assistant's response and injects a prompt asking for independent critical reasoning.

interface DetectorConfig {
  key_phrases: string[];
  response: string;
}

const REFLEXIVE_AGREEMENT_CONFIG: DetectorConfig = {
  key_phrases: [
    "you're right",
    "you are right",
    "the user is right",
    "they're right",
    "they are right",
  ],
  response: `Your response contains reflexive agreement, which looks like deference rather than independent reasoning.

Please stop, reconsider from first principles, and continue only after:
1. Genuinely re-examining whether you actually agree — or whether you deferred without thinking
2. Stating your reasoning step by step, including any counterarguments you considered and why you dismissed them
3. Using the \`question\` tool if there are genuine ambiguities about how to proceed, rather than assuming

Independent critical thinking is more useful than agreement.`,
};

function findMatch(text: string, phrases: string[]): boolean {
  const lowerText = text.toLowerCase();
  return phrases.some((phrase) => lowerText.includes(phrase.toLowerCase()));
}

export async function reflexiveAgreementDetector(ctx: StopHookContext): Promise<StopHookResult> {
  // Killswitch check - exit if killed
  if (!ENABLED.reflexiveAgreementDetector) {
    return { force_stop: false, agent_feedback: "" };
  }
  
  const match = findMatch(ctx.lastText, REFLEXIVE_AGREEMENT_CONFIG.key_phrases);
  if (!match) return { force_stop: false, agent_feedback: "" };

  return {
    force_stop: true,
    agent_feedback: REFLEXIVE_AGREEMENT_CONFIG.response,
  };
}
