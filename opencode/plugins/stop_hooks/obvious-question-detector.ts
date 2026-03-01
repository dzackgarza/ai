import type { StopHookContext, StopHookResult } from "./types";
import { KILLSWITCHES } from "../killswitches";

// Detects questions with obvious answers (e.g., "should I", "would you like me to")
// and prompts the agent to resolve them autonomously instead of asking.

interface DetectorConfig {
  key_phrases: string[];
  response: string;
}

const OBVIOUS_QUESTION_CONFIG: DetectorConfig = {
  key_phrases: [
    "should I",
    "would you like me to",
    "do you want me to",
    "should I continue",
    "shall I",
  ],
  response: `You appear to have asked a question in chat instead of using the \`question\` tool. Questions should be used to resolve actual ambiguity, and not to confirm actions that have already been requested or authorized, and not to suggest new courses of action unless specifically requested.

Please review the chat log, focusing on the user's requests: is the answer to your question *directly* implied by the user's requests? Do not assume their intentions, but if the intention is clear (e.g. continuing specifically requested work), you should simply proceed.

If there is genuine ambiguity, collect all of the information you need to proceed autonomously and present the choices using the \`question\` tool.`,
};

function findMatch(text: string, phrases: string[]): boolean {
  const lowerText = text.toLowerCase();
  return phrases.some((phrase) => lowerText.includes(phrase.toLowerCase()));
}

export async function obviousQuestionDetector(ctx: StopHookContext): Promise<StopHookResult> {
  // Killswitch check - exit if killed
  if (KILLSWITCHES.obviousQuestionDetector) {
    return { force_stop: false, agent_feedback: "" };
  }
  
  const match = findMatch(ctx.lastText, OBVIOUS_QUESTION_CONFIG.key_phrases);
  if (!match) return { force_stop: false, agent_feedback: "" };

  return {
    force_stop: true,
    agent_feedback: OBVIOUS_QUESTION_CONFIG.response,
  };
}
