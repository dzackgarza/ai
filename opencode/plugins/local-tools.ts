import { type Plugin, tool } from "@opencode-ai/plugin"

// Re-export all enabled plugins as separate named exports
export { SleepPlugin } from "./dev/sleep/index" // ✓
// export { AsyncCommandPlugin } from "./dev/async-command/index" // ✗ not loading
// export { GitAddPlugin } from "./dev/git-add/index" // ✗ not loading
// export { GitCommitPlugin } from "./dev/git-commit/index" // ✗ not loading
export { IntrospectionPlugin } from "./dev/introspection/index" // ✓
export { ListSessionsPlugin } from "./dev/list-sessions/index" // ✓
export { ReadTranscriptPlugin } from "./dev/read-transcript/index" // ✓
// export { WritePlanPlugin } from "./dev/write-plan/index" // ✗ not loading
// export { PlanExitPlugin } from "./dev/plan-exit/index" // ✗ not loading

// Disabled plugins (commented out):
// export { CommandInterceptor } from "./dev/command-interceptor/index"
// export { ContextInjector } from "./dev/context-injector"
// export { CotTrivialInterceptor } from "./dev/cot-trivial-test"
//

export const CustomToolsPlugin: Plugin = async (_ctx) => {
  return {
    tool: {
      mytool: tool({
        description: "This is a custom tool",
        args: {
          foo: tool.schema.string(),
        },
        async execute(args, context) {
          const { directory, worktree } = context
          return `Hello ${args.foo} from ${directory} (worktree: ${worktree})`
        },
      }),
    },
  }
}
