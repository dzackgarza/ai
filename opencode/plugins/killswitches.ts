// Centralized killswitches for prompt-injection plugins
// Set to true to KILL (disable), false to allow

export const KILLSWITCHES = {
  promptRouter: true,
  commandInterceptor: true,
  contextInjector: true,
  cotTrivialInterceptor: true,
};
