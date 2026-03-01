// Centralized killswitches for all prompt-injection plugins.
// Set to true to KILL (disable), false to allow.
//
// Changes take effect immediately — no session restart needed.
// This file is re-evaluated on each message transform.
//
// ┌──────────────────────────────────────────────────────────────────────────┐
// │ RULE: Every new plugin MUST register a killswitch here before shipping.  │
// │ Format: <camelCasePluginName>: true  (start killed; enable deliberately) │
// └──────────────────────────────────────────────────────────────────────────┘

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
