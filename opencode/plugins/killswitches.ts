// Centralized enable switches for all plugins.
// true = plugin runs, false = plugin is off.
//
// Two ways to toggle:
//   1. Edit this file — takes effect on the next message, no restart needed.
//   2. Env var — for one-shot CLI invocations (e.g. PROMPT_ROUTER_ENABLED=true opencode run "...").
//      Has no effect on a running interactive session.
//
// ┌──────────────────────────────────────────────────────────────────────────┐
// │ RULE: Every new plugin MUST register an entry here before shipping.      │
// │ Format: <camelCaseName>: sw('PLUGIN_ENV_VAR_ENABLED', false)             │
// └──────────────────────────────────────────────────────────────────────────┘

// Returns true if the plugin should run, false if it should not.
// Env var takes precedence over the coded default.
const sw = (envVar: string, defaultEnabled: boolean): boolean => {
  const val = process.env[envVar];
  if (val === 'true')  return true;
  if (val === 'false') return false;
  return defaultEnabled;
};

export const ENABLED = {
  // Message transform plugins
  promptRouter:           sw('PROMPT_ROUTER_ENABLED',           false),
  commandInterceptor:     sw('COMMAND_INTERCEPTOR_ENABLED',     false),
  contextInjector:        sw('CONTEXT_INJECTOR_ENABLED',        false),
  cotTrivialInterceptor:  sw('COT_TRIVIAL_INTERCEPTOR_ENABLED', false),
  // Stop hooks
  otpChecker:                 sw('OTP_CHECKER_ENABLED',                 false),
  obviousQuestionDetector:    sw('OBVIOUS_QUESTION_DETECTOR_ENABLED',   false),
  reflexiveAgreementDetector: sw('REFLEXIVE_AGREEMENT_DETECTOR_ENABLED', false),
};
