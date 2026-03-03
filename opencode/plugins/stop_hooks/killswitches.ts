function sw(envVar: string, defaultEnabled: boolean): boolean {
  const val = process.env[envVar];
  if (val === "true") return true;
  if (val === "false") return false;
  return defaultEnabled;
}

export const ENABLED = {
  otpChecker: sw("OTP_CHECKER_ENABLED", false),
  reflexiveAgreementDetector: sw("REFLEXIVE_AGREEMENT_DETECTOR_ENABLED", false),
  obviousQuestionDetector: sw("OBVIOUS_QUESTION_DETECTOR_ENABLED", false),
};
