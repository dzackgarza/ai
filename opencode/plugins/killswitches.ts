// Centralized killswitches for prompt-injection plugins
// Set to true to KILL (disable), false to allow

export const KILLSWITCHES = {
  // Message transform plugins
  promptRouter: true,
  commandInterceptor: true,
  contextInjector: true,
  cotTrivialInterceptor: true,
  // Stop hooks
  otpChecker: true,
  obviousQuestionDetector: true,
  reflexiveAgreementDetector: true,
};
