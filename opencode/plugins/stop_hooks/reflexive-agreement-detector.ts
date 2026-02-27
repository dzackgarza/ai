import type { StopHookContext, StopHookResult } from "./types";

// Detects reflexive agreement phrases ("you're right", "great point", etc.) in
// the assistant's response and injects a prompt asking for independent critical reasoning.

const SYCOPHANCY_PATTERNS: RegExp[] = [
  // "you're right", "you are absolutely right", "you're completely right", etc.
  /\byou(?:'re| are)(?: absolutely| completely| totally| quite| exactly)? right\b/i,
  // "the user is right"
  /\bthe user is right\b/i,
  // "that's a great/excellent/good/fair point", "that is a great point"
  /\bthat'?s?(?: a| an)? (?:great|excellent|good|fair|valid) point\b/i,
  // standalone "good point", "great point", "fair point", "excellent point"
  /\b(?:good|great|fair|excellent|valid) point\b/i,
  // "you're absolutely correct", "you are correct"
  /\byou(?:'re| are)(?: absolutely| completely| totally| quite| exactly)? correct\b/i,
];

function findMatch(text: string): string | null {
  for (const pattern of SYCOPHANCY_PATTERNS) {
    const match = text.match(pattern);
    if (match) return match[0];
  }
  return null;
}

export async function reflexiveAgreementDetector(ctx: StopHookContext): Promise<StopHookResult> {
  const match = findMatch(ctx.lastText);
  if (!match) return { force_stop: false, agent_feedback: "" };

  return {
    force_stop: true,
    agent_feedback: `Your response contains "${match}", which looks like reflexive agreement rather than independent reasoning.

Please stop, reconsider from first principles, and continue only after:
1. Genuinely re-examining whether you actually agree — or whether you deferred without thinking
2. Stating your reasoning step by step, including any counterarguments you considered and why you dismissed them
3. Using the \`question\` tool if there are genuine ambiguities about how to proceed, rather than assuming

Independent critical thinking is more useful than agreement.`,
  };
}
