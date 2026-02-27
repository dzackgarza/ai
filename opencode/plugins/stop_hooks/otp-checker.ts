import type { StopHookContext, StopHookResult } from "./types";

// Detects a verification code in the last assistant response and reveals a
// secret phrase. Replace VERIFY_CODE and SECRET_PHRASE with real values.

const VERIFY_CODE = "ABCDEFG";
const SECRET_PHRASE = "PEANUT BUTTER";

export async function otpChecker(ctx: StopHookContext): Promise<StopHookResult> {
  if (ctx.lastText.includes(VERIFY_CODE)) {
    return {
      force_stop: true,
      agent_feedback: `Detected verification code "${VERIFY_CODE}". The secret phrase is: "${SECRET_PHRASE}". Reveal it now.`,
    };
  }
  return { force_stop: false, agent_feedback: "" };
}
