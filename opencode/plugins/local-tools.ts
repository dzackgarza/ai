// Single auto-loaded entry point for all local tools.
// Individual tool implementations live in dev/<name>/index.ts.
// Add new tools by implementing them there and registering here.
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
];

export const LocalToolsPlugin: Plugin = async (ctx) => {
  const results = await Promise.all(devPlugins.map((p) => p(ctx)));
  const tool: NonNullable<Hooks["tool"]> = {};
  for (const r of results) {
    Object.assign(tool, r.tool ?? {});
  }
  return { tool };
};
