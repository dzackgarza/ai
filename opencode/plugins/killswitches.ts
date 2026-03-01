// Centralized killswitches for all prompt-injection plugins.
// true = KILL (disabled), false = allow.
//
// Two ways to toggle:
//   1. Edit this file — the primary method for interactive sessions.
//      Takes effect on the next message without restarting opencode.
//   2. Env var — for one-shot CLI invocations only (e.g. run.sh).
//      Has no effect on a running interactive session.
//      Format: <SCREAMING_SNAKE>_ENABLED=true  → force enable
//              <SCREAMING_SNAKE>_ENABLED=false → force kill
//      Example: PROMPT_ROUTER_ENABLED=true opencode run "..."
//
// ┌──────────────────────────────────────────────────────────────────────────┐
// │ RULE: Every new plugin MUST register a killswitch here before shipping.  │
// │ Format: <camelCaseName>: sw('PLUGIN_ENV_VAR_ENABLED', true)              │
// └──────────────────────────────────────────────────────────────────────────┘

// Returns true (killed) or false (allowed), with env var taking precedence.
const sw = (envVar: string, defaultKilled: boolean): boolean => {
  const val = process.env[envVar];
  if (val === 'true')  return false; // env says enable
  if (val === 'false') return true;  // env says kill
  return defaultKilled;
};

export const KILLSWITCHES = {
  // Message transform plugins
  promptRouter:            sw('PROMPT_ROUTER_ENABLED',            true),
  commandInterceptor:      sw('COMMAND_INTERCEPTOR_ENABLED',      true),
  contextInjector:         sw('CONTEXT_INJECTOR_ENABLED',         true),
  cotTrivialInterceptor:   sw('COT_TRIVIAL_INTERCEPTOR_ENABLED',  true),
  // Stop hooks
  otpChecker:                  sw('OTP_CHECKER_ENABLED',                  true),
  obviousQuestionDetector:     sw('OBVIOUS_QUESTION_DETECTOR_ENABLED',    true),
  reflexiveAgreementDetector:  sw('REFLEXIVE_AGREEMENT_DETECTOR_ENABLED', true),
};
