// Single auto-loaded entry point for all local tools.
// This file is the registry: to enable or disable a tool, add or remove its import and entry below.
// Individual tool implementations live in dev/<name>/index.ts.
//
// Registration policy:
//   - Every plugin in dev/ MUST be imported here (source of truth).
//   - To activate: add to devPlugins[].
//   - To deactivate: comment out in devPlugins[] (keep the import).
import { type Plugin, type Hooks } from "@opencode-ai/plugin";
import { SleepPlugin } from "./dev/sleep/index";
import { AsyncCommandPlugin } from "./dev/async-command/index";
import { GitAddPlugin } from "./dev/git-add/index";
import { GitCommitPlugin } from "./dev/git-commit/index";
import { IntrospectionPlugin } from "./dev/introspection/index";
import { ListSessionsPlugin } from "./dev/list-sessions/index";
import { ReadTranscriptPlugin } from "./dev/read-transcript/index";
import { WritePlanPlugin } from "./dev/write-plan/index";
import { PlanExitPlugin } from "./dev/plan-exit/index";
import { PromptRouter } from "./dev/prompt-router/index";
import { CommandInterceptor } from "./dev/command-interceptor/index";
import { ContextInjector } from "./dev/context-injector";
import { CotTrivialInterceptor } from "./dev/cot-trivial-test";
import { CustomToolsPlugin } from "./dev/custom-tools";

// Plugins registered but not currently active.
// Move to devPlugins[] to activate.
const _inactive: Record<string, Plugin> = {
  CommandInterceptor, // dev testing tool — activate when testing intercept pipeline
  ContextInjector, // earlier intercept example — superseded by CommandInterceptor
  CotTrivialInterceptor, // self-disabled (return; guard) — activate to test CoT branch-pruning
  CustomToolsPlugin, // placeholder example tool — activate to add mytool
};
void _inactive; // referenced to satisfy TS; never called

const devPlugins: Plugin[] = [
  SleepPlugin,
  AsyncCommandPlugin,
  GitAddPlugin,
  GitCommitPlugin,
  IntrospectionPlugin,
  ListSessionsPlugin,
  ReadTranscriptPlugin,
  WritePlanPlugin,
  PlanExitPlugin,
  PromptRouter,
];

export const LocalToolsPlugin: Plugin = async (ctx) => {
  const results = await Promise.all(devPlugins.map((p) => p(ctx)));
  const tool: NonNullable<Hooks["tool"]> = {};
  for (const r of results) {
    Object.assign(tool, r.tool ?? {});
  }
  return { tool };
};
