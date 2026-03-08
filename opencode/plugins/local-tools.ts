// Re-export all enabled plugins as separate named exports
// OpenCode loads each export as an independent plugin

export { SleepPlugin } from "./dev/sleep/index"
export { AsyncCommandPlugin } from "./dev/async-command/index"
export { GitAddPlugin } from "./dev/git-add/index"
export { GitCommitPlugin } from "./dev/git-commit/index"
export { IntrospectionPlugin } from "./dev/introspection/index"
export { ListSessionsPlugin } from "./dev/list-sessions/index"
export { ReadTranscriptPlugin } from "./dev/read-transcript/index"
export { WritePlanPlugin } from "./dev/write-plan/index"
export { PlanExitPlugin } from "./dev/plan-exit/index"
export { PromptRouter } from "./dev/prompt-router/index"

// Disabled plugins (commented out):
// export { CommandInterceptor } from "./dev/command-interceptor/index"
// export { ContextInjector } from "./dev/context-injector"
// export { CotTrivialInterceptor } from "./dev/cot-trivial-test"
// export { CustomToolsPlugin } from "./dev/custom-tools"
