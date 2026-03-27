// Re-export all enabled plugins as separate named exports
export { GitCheckpointPlugin } from './git-checkpoint-plugin';
export { LintPlugin } from './lint-plugin';
// NextStepsHookPlugin: loaded directly from plugins/ directory
export { TranscriptTimestampPlugin } from './transcript-timestamp';
// export { SleepPlugin } from './dev/sleep/index'; // retired: use at/crontab instead
// export { AsyncCommandPlugin } from "./dev/async-command/index" // ✗ not loading
// export { GitAddPlugin } from "./dev/git-add/index" // ✗ not loading
// export { GitCommitPlugin } from "./dev/git-commit/index" // ✗ not loading
// export { IntrospectionPlugin } from "./dev/retired/introspection" // retired: superseded by timestamp injection
// export { ListSessionsPlugin } from './dev/list-sessions/index'; // retired: use ocm instead
// export { ReadTranscriptPlugin } from './dev/read-transcript/index'; // retired: use ocm instead
// export { WritePlanPlugin } from "./dev/write-plan/index" // ✗ not loading
// export { PlanExitPlugin } from "./dev/plan-exit/index" // ✗ not loading

// Disabled plugins (commented out):
// export { CommandInterceptor } from "./dev/command-interceptor/index"
// export { ContextInjector } from "./dev/context-injector"
// export { CotTrivialInterceptor } from "./dev/cot-trivial-test"
//
