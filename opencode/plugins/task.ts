import { isPluginEnabled } from "./plugins_config";
import { type Plugin, tool } from "@opencode-ai/plugin";
import { promises as fs } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const DEFAULT_SUBAGENT_DESCRIPTION =
  "This subagent should only be called manually by the user.";

const TASK_DESCRIPTION_BASE =
  "Delegate work to a subagent using native task lifecycle semantics. Use this when you need a specialized subagent to handle scoped work and return a result.";
const AGENT_FETCH_TIMEOUT_MS = 3000;
const SUBAGENT_CACHE_TTL_MS = 60_000;
const TRANSCRIPT_JSON_MAX_CHARS = 12_000;
const ASYNC_HEARTBEAT_INTERVAL_MS = 15_000;
const DEFAULT_TASK_TIMEOUT_MS = 1_800_000;

type TaskModelRef = {
  providerID: string;
  modelID: string;
};

type CachedSubagent = {
  name: string;
  description?: string;
  mode?: string;
  model?: TaskModelRef;
  permission?: Array<{
    permission?: string;
  }>;
};

type PendingTaskMetadata = {
  title: string;
  metadata: {
    sessionId: string;
    model?: TaskModelRef;
  };
};

type ToolExecuteAfterInput = {
  tool: string;
  sessionID: string;
  callID?: string;
  args?: Record<string, unknown>;
};

type ToolExecuteAfterOutput = {
  title?: string;
  metadata?: Record<string, unknown>;
  output?: string;
};

type SessionMessagePart = {
  type?: string;
  text?: string;
  tool?: string;
  state?: {
    input?: unknown;
  };
};

type SessionMessage = {
  info?: {
    role?: string;
  };
  parts?: SessionMessagePart[];
};

type TranscriptBundle = {
  path: string;
  messageCount: number;
  toolCallCount: number;
};

type TaskTerminalSummary = {
  status: "completed" | "timeout";
  sessionID: string;
  subagentType: string;
  subagentModel: string;
  durationMs: number;
  numToolCalls: number;
  transcriptPath: string;
  completionConfidenceScore: number;
  finalResultText: string;
  timeoutMs?: number;
};

class TaskTimeoutError extends Error {
  constructor(label: string, timeoutMs: number) {
    super(`${label} timed out after ${timeoutMs}ms`);
    this.name = "TaskTimeoutError";
  }
}

function timeoutSeconds(timeoutMs: number): number {
  return Math.max(1, Math.round(timeoutMs / 1000));
}

function formatSubagentList(subagents: CachedSubagent[]): string {
  if (subagents.length === 0) {
    return "- (No subagents currently discoverable via client.app.agents())";
  }

  return subagents
    .map(
      (subagent) =>
        `- ${subagent.name}: ${subagent.description ?? DEFAULT_SUBAGENT_DESCRIPTION}`,
    )
    .join("\n");
}

function buildTaskToolDescription(subagents: CachedSubagent[]): string {
  return [
    TASK_DESCRIPTION_BASE,
    "",
    "Available subagent types and descriptions:",
    formatSubagentList(subagents),
  ].join("\n");
}

function extractText(parts: Array<{ type?: string; text?: string }>): string {
  return parts
    .filter((part) => part.type === "text" && typeof part.text === "string")
    .map((part) => part.text as string)
    .join("")
    .trim();
}

function callKey(sessionID: string, callID: string): string {
  return `${sessionID}:${callID}`;
}

function formatModelRef(model: TaskModelRef): string {
  return `${model.providerID}/${model.modelID}`;
}

function withTaskDisplayMetadata(input: {
  description: string;
  subagentType: string;
  model: TaskModelRef;
}): string {
  return `${input.description} [with subagent: ${input.subagentType}, ${formatModelRef(input.model)}]`;
}

function stringifyForTranscript(value: unknown): string {
  if (value === undefined) return "";
  if (typeof value === "string") return value.trim();

  try {
    const seen = new WeakSet<object>();
    const json = JSON.stringify(
      value,
      (_key, candidate) => {
        if (typeof candidate === "object" && candidate !== null) {
          if (seen.has(candidate as object)) return "[Circular]";
          seen.add(candidate as object);
        }
        return candidate;
      },
      2,
    );
    if (!json) return "";
    if (json.length <= TRANSCRIPT_JSON_MAX_CHARS) return json;
    return `${json.slice(0, TRANSCRIPT_JSON_MAX_CHARS)}\n... [truncated]`;
  } catch {
    return "";
  }
}

function renderTranscript(messages: SessionMessage[]): {
  narrative: string;
  toolCallCount: number;
} {
  const lines: string[] = [];
  let stepNumber = 1;
  let toolCallCount = 0;

  messages.forEach((message) => {
    const role = (message.info?.role ?? "unknown").toUpperCase();
    for (const part of message.parts ?? []) {
      if (part.type === "text") {
        const text = typeof part.text === "string" ? part.text.trim() : "";
        if (text.length > 0) {
          lines.push(`Step ${stepNumber}: ${role} message`);
          lines.push(text);
          lines.push("");
          stepNumber += 1;
        }
        continue;
      }

      if (part.type === "tool") {
        toolCallCount += 1;
        const toolName = typeof part.tool === "string" ? part.tool : "unknown";
        lines.push(`Step ${stepNumber}: TOOL call \`${toolName}\``);
        const renderedInput = stringifyForTranscript(part.state?.input);
        if (renderedInput.length > 0) {
          lines.push("Parameters:");
          lines.push("```json");
          lines.push(renderedInput);
          lines.push("```");
        }
        lines.push("");
        stepNumber += 1;
        continue;
      }
    }
  });
  const narrative = lines.join("\n").trim();
  return {
    narrative: narrative.length > 0 ? narrative : "No transcript steps were captured.",
    toolCallCount,
  };
}

function computeCompletionConfidenceScore(input: {
  messageCount: number;
  finalText: string;
}): number {
  if (input.messageCount === 0) return 0;
  if (input.finalText.trim().length === 0) return 0.25;
  return 0.6;
}

function buildTaskSummaryOutput(summary: TaskTerminalSummary): string {
  const timeoutFollowUp =
    summary.status === "timeout" && typeof summary.timeoutMs === "number"
      ? [
          `- Timeout reached: configured limit was ${timeoutSeconds(summary.timeoutMs)} seconds.`,
          `- If this was unexpected, inspect \`${summary.transcriptPath}\` for turn-by-turn timing details.`,
          `- Resume this session with \`session_id: ${summary.sessionID}\` to continue from current progress.`,
          "- If provider throughput appears constrained (for example, <10-20 turns/min), rerun with a different model and consult the `model-selection` skill.",
        ]
      : [];

  return [
    "---",
    `status: ${summary.status}`,
    `session_id: ${JSON.stringify(summary.sessionID)}`,
    `subagent_type: ${JSON.stringify(summary.subagentType)}`,
    `subagent_model: ${JSON.stringify(summary.subagentModel)}`,
    `duration_ms: ${summary.durationMs}`,
    `num_tool_calls: ${summary.numToolCalls}`,
    `transcript_path: ${JSON.stringify(summary.transcriptPath)}`,
    `completion_confidence_score: ${summary.completionConfidenceScore.toFixed(2)}`,
    "---",
    "",
    "## 1. Summarized Final Result",
    summary.finalResultText,
    "",
    "## 2. Git Diff Summary",
    "To be implemented in future versions of the task tool.",
    "",
    "## 3. Performance Report",
    "To be implemented in future versions of the task tool.",
    "",
    "## 4. Turn-by-turn summary",
    "Detailed turn-by-turn narrative and tool parameters are available in the transcript file.",
    "",
    "## 5. Follow-up Instructions",
    ...timeoutFollowUp,
    `- Full details: read the transcript directly at \`${summary.transcriptPath}\`.`,
    `- Continue this subagent session by calling \`task\` again with \`session_id: ${summary.sessionID}\` and a new \`prompt\`.`,
    "- Keep `subagent_type` unchanged when resuming, so continuation stays on the same specialist path.",
    "- If the provided `session_id` is invalid, the tool creates a new child session.",
  ].join("\n");
}

function buildAsyncRunningOutput(input: {
  sessionID: string;
  subagentType: string;
  subagentModel: string;
}): string {
  return [
    "---",
    "status: running",
    `session_id: ${JSON.stringify(input.sessionID)}`,
    `subagent_type: ${JSON.stringify(input.subagentType)}`,
    `subagent_model: ${JSON.stringify(input.subagentModel)}`,
    "---",
    "",
    "## Follow-up Instructions",
    "- This task is running in the background.",
    `- Monitor progress by opening child session \`${input.sessionID}\` in the TUI session tree.`,
    `- Continue this task later using \`session_id: ${input.sessionID}\`.`,
  ].join("\n");
}

function buildAsyncHeartbeat(input: {
  sessionID: string;
  subagentType: string;
  elapsedMs: number;
}): string {
  return [
    "[task_async_heartbeat]",
    "status: running",
    `session_id: ${input.sessionID}`,
    `subagent_type: ${input.subagentType}`,
    `elapsed_ms: ${input.elapsedMs}`,
  ].join("\n");
}

function buildAsyncFailureOutput(input: {
  sessionID: string;
  subagentType: string;
  subagentModel: string;
  elapsedMs: number;
  errorMessage: string;
}): string {
  return [
    "---",
    "status: failed",
    `session_id: ${JSON.stringify(input.sessionID)}`,
    `subagent_type: ${JSON.stringify(input.subagentType)}`,
    `subagent_model: ${JSON.stringify(input.subagentModel)}`,
    `duration_ms: ${input.elapsedMs}`,
    "---",
    "",
    "## Failure",
    input.errorMessage,
    "",
    "## Follow-up Instructions",
    `- Inspect child session \`${input.sessionID}\` in TUI for detailed failure context.`,
    `- Resume with \`session_id: ${input.sessionID}\` and corrective instructions.`,
  ].join("\n");
}

export const TaskPlugin: Plugin = async ({ client }) => {
  if (!isPluginEnabled("task-plugin")) return {};

  let cachedSubagents: CachedSubagent[] = [];
  let cachedAt = 0;
  let cachedDescription = buildTaskToolDescription([]);
  const pendingMetadataByCall = new Map<string, PendingTaskMetadata>();

  const log = async (
    level: "debug" | "info" | "warn" | "error",
    message: string,
    extra?: Record<string, unknown>,
  ): Promise<void> => {
    try {
      await client.app.log({
        body: {
          service: "task-plugin",
          level,
          message,
          extra,
        },
      });
    } catch {
      // Never break execution on logging failures.
    }
  };

  const withTimeout = async <T>(
    promise: Promise<T>,
    timeoutMs: number,
    label: string,
    onTimeout?: () => void | Promise<void>,
  ): Promise<T> => {
    let timeoutId: ReturnType<typeof setTimeout> | undefined;
    const timeoutPromise = new Promise<T>((_, reject) => {
      timeoutId = setTimeout(() => {
        void Promise.resolve(onTimeout?.()).finally(() => {
          reject(new TaskTimeoutError(label, timeoutMs));
        });
      }, timeoutMs);
    });
    try {
      return await Promise.race([promise, timeoutPromise]);
    } finally {
      if (timeoutId) clearTimeout(timeoutId);
    }
  };

  const fetchSubagents = async (
    reason: string,
    force = false,
  ): Promise<CachedSubagent[]> => {
    const cacheAgeMs = Date.now() - cachedAt;
    if (
      !force &&
      cachedSubagents.length > 0 &&
      cacheAgeMs < SUBAGENT_CACHE_TTL_MS
    ) {
      return cachedSubagents;
    }

    let agentList: Array<{
      name: string;
      description?: string;
      mode?: string;
      model?: TaskModelRef;
    }> = [];
    try {
      const response = await withTimeout(
        client.app.agents(),
        AGENT_FETCH_TIMEOUT_MS,
        "client.app.agents()",
      );
      const data = response.data;
      if (!Array.isArray(data)) {
        await log("warn", "Agent list unavailable; using cached subagents", {
          reason,
          hasCache: cachedSubagents.length > 0,
        });
        return cachedSubagents;
      }
      agentList = data.map((agent) => ({
        name: agent.name,
        description:
          typeof agent.description === "string" ? agent.description : undefined,
        mode: typeof agent.mode === "string" ? agent.mode : undefined,
        model: agent.model
          ? {
              providerID: agent.model.providerID,
              modelID: agent.model.modelID,
            }
          : undefined,
      }));
    } catch (error) {
      await log("warn", "Agent fetch timed out/failed; using cached subagents", {
        reason,
        hasCache: cachedSubagents.length > 0,
        error: String(error),
      });
      return cachedSubagents;
    }

    const subagents = agentList
      .filter((agent) => agent.mode !== "primary")
      .sort((a, b) => a.name.localeCompare(b.name));

    cachedSubagents = subagents;
    cachedAt = Date.now();
    cachedDescription = buildTaskToolDescription(subagents);
    return subagents;
  };

  const sessionExists = async (id: string): Promise<boolean> => {
    const { data, error } = await client.session.messages({ path: { id } });
    return !error && Array.isArray(data);
  };

  const resolveChildSessionID = async (input: {
    sessionID?: string;
    parentSessionID: string;
    title: string;
  }): Promise<string> => {
    if (input.sessionID && (await sessionExists(input.sessionID))) {
      return input.sessionID;
    }

    const { data: session, error } = await client.session.create({
      body: {
        title: input.title,
        parentID: input.parentSessionID,
      },
    });

    if (error || !session?.id) {
      throw new Error(`Failed to create child session: ${String(error)}`);
    }

    return session.id;
  };

  const resolveParentModel = async (input: {
    sessionID: string;
    messageID: string;
  }): Promise<TaskModelRef | undefined> => {
    const { data, error } = await client.session.message({
      path: {
        id: input.sessionID,
        messageID: input.messageID,
      },
    });

    if (error || !data || typeof data !== "object") return undefined;

    const info =
      typeof (data as { info?: unknown }).info === "object" &&
      (data as { info?: unknown }).info
        ? ((data as { info: Record<string, unknown> }).info ?? {})
        : {};

    const providerID =
      typeof info.providerID === "string" ? info.providerID : undefined;
    const modelID = typeof info.modelID === "string" ? info.modelID : undefined;
    if (!providerID || !modelID) return undefined;

    return { providerID, modelID };
  };

  const runChildPromptToTerminal = async (input: {
    childSessionID: string;
    subagent: CachedSubagent;
    model: TaskModelRef;
    prompt: string;
    timeoutMs?: number;
    abortSignal?: AbortSignal;
  }): Promise<TaskTerminalSummary> => {
    const abortHandler = async () => {
      await client.session.abort({ path: { id: input.childSessionID } }).catch(() => {});
    };
    input.abortSignal?.addEventListener("abort", abortHandler);

    try {
      const startedAt = Date.now();
      let text = "";
      let timedOut = false;
      try {
        const promptRequest = client.session.prompt({
          path: { id: input.childSessionID },
          body: {
            agent: input.subagent.name,
            model: input.model,
            parts: [{ type: "text", text: input.prompt }],
          },
        });
        const { data: result, error } =
          typeof input.timeoutMs === "number"
            ? await withTimeout(
                promptRequest,
                input.timeoutMs,
                `Subagent prompt for session ${input.childSessionID}`,
                async () => {
                  await log("warn", "Subagent prompt timed out; aborting child session", {
                    childSessionID: input.childSessionID,
                    timeoutMs: input.timeoutMs,
                    subagentType: input.subagent.name,
                  });
                  await client.session.abort({ path: { id: input.childSessionID } }).catch(() => {});
                },
              )
            : await promptRequest;

        if (error) {
          throw new Error(String(error));
        }

        const parts =
          (result as { parts?: Array<{ type?: string; text?: string }> } | undefined)
            ?.parts ?? [];
        text = extractText(parts);
      } catch (error) {
        if (error instanceof TaskTimeoutError) {
          timedOut = true;
          await log("warn", "Subagent timeout reached", {
            childSessionID: input.childSessionID,
            subagentType: input.subagent.name,
            timeoutMs: input.timeoutMs,
          });
        } else {
          throw error;
        }
      }

      const elapsedMs = Date.now() - startedAt;
      const finalResultText = timedOut
        ? [
            `Subagent timeout reached after ${
              typeof input.timeoutMs === "number"
                ? timeoutSeconds(input.timeoutMs)
                : timeoutSeconds(elapsedMs)
            } seconds.`,
            "The session transcript was still captured and may include partial progress up to the timeout boundary.",
          ].join(" ")
        : text.length > 0
          ? text
          : "Subagent completed without a text response.";
      const renderedModel = formatModelRef(input.model);
      const transcriptBundle = await (async (): Promise<TranscriptBundle> => {
        const { data: rawMessages, error: messagesError } =
          await client.session.messages({
            path: { id: input.childSessionID },
          });
        if (messagesError || !Array.isArray(rawMessages)) {
          throw new Error(
            `Failed to load child session messages: ${String(messagesError)}`,
          );
        }

        const messages = rawMessages as SessionMessage[];
        const transcript = renderTranscript(messages);
        const fullText = [
          "---",
          `session_id: ${JSON.stringify(input.childSessionID)}`,
          `subagent_type: ${JSON.stringify(input.subagent.name)}`,
          `subagent_model: ${JSON.stringify(renderedModel)}`,
          `generated_at: ${JSON.stringify(new Date().toISOString())}`,
          `num_messages: ${messages.length}`,
          `num_tool_calls: ${transcript.toolCallCount}`,
          "---",
          "",
          "# Subagent Transcript",
          "",
          "## Invocation Result Snapshot",
          finalResultText,
          "",
          "## Session Narrative",
          transcript.narrative,
        ].join("\n");
        const outPath = join(
          tmpdir(),
          `opencode-task-${input.childSessionID}-${Date.now()}.transcript.md`,
        );
        await fs.writeFile(outPath, `${fullText}\n`, "utf8");
        return {
          path: outPath,
          messageCount: messages.length,
          toolCallCount: transcript.toolCallCount,
        };
      })();
      const completionConfidenceScore = timedOut
        ? 0.25
        : computeCompletionConfidenceScore({
            messageCount: transcriptBundle.messageCount,
            finalText: text,
          });

      await log(timedOut ? "warn" : "info", timedOut ? "Task timed out" : "Task completed", {
        childSessionID: input.childSessionID,
        subagentType: input.subagent.name,
        elapsedMs,
        toolCallCount: transcriptBundle.toolCallCount,
        outputChars: text.length,
        transcriptPath: transcriptBundle.path,
        completionConfidenceScore,
        ...(timedOut && typeof input.timeoutMs === "number"
          ? { timeoutMs: input.timeoutMs, timeoutSeconds: timeoutSeconds(input.timeoutMs) }
          : {}),
      });

      return {
        status: timedOut ? "timeout" : "completed",
        sessionID: input.childSessionID,
        subagentType: input.subagent.name,
        subagentModel: renderedModel,
        durationMs: elapsedMs,
        numToolCalls: transcriptBundle.toolCallCount,
        transcriptPath: transcriptBundle.path,
        completionConfidenceScore,
        finalResultText,
        ...(timedOut && typeof input.timeoutMs === "number"
          ? { timeoutMs: input.timeoutMs }
          : {}),
      };
    } finally {
      input.abortSignal?.removeEventListener("abort", abortHandler);
    }
  };

  const emitParentCallback = async (input: {
    parentSessionID: string;
    text: string;
    terminal: boolean;
  }): Promise<void> => {
    await client.session.promptAsync({
      path: { id: input.parentSessionID },
      body: {
        noReply: !input.terminal,
        parts: [{ type: "text", text: input.text }],
      },
    });
  };

  const runAsyncLifecycle = async (input: {
    parentSessionID: string;
    childSessionID: string;
    subagent: CachedSubagent;
    model: TaskModelRef;
    prompt: string;
    timeoutMs?: number;
  }): Promise<void> => {
    const startedAt = Date.now();
    const heartbeat = setInterval(() => {
      const heartbeatText = buildAsyncHeartbeat({
        sessionID: input.childSessionID,
        subagentType: input.subagent.name,
        elapsedMs: Date.now() - startedAt,
      });
      void emitParentCallback({
        parentSessionID: input.parentSessionID,
        text: heartbeatText,
        terminal: false,
      }).catch(async (error) => {
        await log("warn", "Async heartbeat emit failed", {
          parentSessionID: input.parentSessionID,
          childSessionID: input.childSessionID,
          error: String(error),
        });
      });
    }, ASYNC_HEARTBEAT_INTERVAL_MS);
    (heartbeat as { unref?: () => void }).unref?.();

    try {
      const summary = await runChildPromptToTerminal({
        childSessionID: input.childSessionID,
        subagent: input.subagent,
        model: input.model,
        prompt: input.prompt,
        timeoutMs: input.timeoutMs,
      });
      await emitParentCallback({
        parentSessionID: input.parentSessionID,
        text: buildTaskSummaryOutput(summary),
        terminal: true,
      });
    } catch (error) {
      const failureText = buildAsyncFailureOutput({
        sessionID: input.childSessionID,
        subagentType: input.subagent.name,
        subagentModel: formatModelRef(input.model),
        elapsedMs: Date.now() - startedAt,
        errorMessage: String(error),
      });
      await log("error", "Async task failed", {
        parentSessionID: input.parentSessionID,
        childSessionID: input.childSessionID,
        error: String(error),
      });
      await emitParentCallback({
        parentSessionID: input.parentSessionID,
        text: failureText,
        terminal: true,
      }).catch(async (emitError) => {
        await log("error", "Async failure callback emit failed", {
          parentSessionID: input.parentSessionID,
          childSessionID: input.childSessionID,
          error: String(emitError),
        });
      });
    } finally {
      clearInterval(heartbeat);
    }
  };

  void fetchSubagents("plugin_init_warmup", false);

  return {
    "tool.definition": async (input, output) => {
      if (input.toolID !== "task") return;
      await fetchSubagents("tool_definition", false);
      output.description = cachedDescription;
    },

    "tool.execute.after": async (
      input: ToolExecuteAfterInput,
      output: ToolExecuteAfterOutput,
    ) => {
      if (input.tool !== "task") return;
      if (!input.callID || input.callID.length === 0) {
        throw new Error(
          "Task plugin contract violation: tool.execute.after missing callID for task.",
        );
      }

      const key = callKey(input.sessionID, input.callID);
      const pending = pendingMetadataByCall.get(key);
      pendingMetadataByCall.delete(key);
      if (!pending) {
        throw new Error(
          `Task plugin contract violation: missing pending metadata for task call ${input.callID}.`,
        );
      }

      output.title = pending.title;
      output.metadata = {
        ...(output.metadata ?? {}),
        sessionId: pending.metadata.sessionId,
        ...(pending.metadata.model ? { model: pending.metadata.model } : {}),
      };
    },

    tool: {
      task: tool({
        description: cachedDescription,
        args: {
          description: tool.schema
            .string()
            .describe("A short (3-5 words) description of the task"),
          prompt: tool.schema
            .string()
            .describe("The task for the agent to perform"),
          subagent_type: tool.schema
            .string()
            .describe("The type of specialized agent to use for this task"),
          mode: tool.schema
            .string()
            .optional()
            .describe(
              "Execution mode for delegation: `sync` (default, blocking) or `async` (non-blocking background).",
            ),
          timeout_ms: tool.schema
            .number()
            .optional()
            .describe(
              "Hard timeout in milliseconds (default: 1800000 = 30m). Do not usually change this; lower only for finite-turn tasks (roughly 10-20 turns/min) when hangs/provider stalls are suspected. See the `difficulty-and-time-estimation` skill before nontrivial changes.",
            ),
          session_id: tool.schema
            .string()
            .optional()
            .describe(
              "Optional existing session ID to resume instead of creating a new child session.",
            ),
          command: tool.schema
            .string()
            .optional()
            .describe("The command that triggered this task"),
        },
        async execute(args, context) {
          await fetchSubagents("task_execute", true);

          await context.ask({
            permission: "task",
            patterns: [args.subagent_type],
            always: ["*"],
            metadata: {
              description: args.description,
              subagent_type: args.subagent_type,
            },
          });

          const subagent = cachedSubagents.find(
            (agent) => agent.name === args.subagent_type,
          );
          if (!subagent) {
            throw new Error(
              `Unknown agent type: ${args.subagent_type} is not a valid agent type`,
            );
          }

          const childSessionID = await resolveChildSessionID({
            sessionID: args.session_id,
            parentSessionID: context.sessionID,
            title: `${args.description} (@${subagent.name} subagent)`,
          });

          const parentModel = await resolveParentModel({
            sessionID: context.sessionID,
            messageID: context.messageID,
          });
          const model = subagent.model ?? parentModel;
          if (!model) {
            throw new Error(
              [
                `No model resolved for subagent_type=\"${args.subagent_type}\".`,
                "Set a model on the subagent config or ensure the parent message has model metadata.",
              ].join(" "),
            );
          }

          const displayDescription = withTaskDisplayMetadata({
            description: args.description,
            subagentType: subagent.name,
            model,
          });
          (args as { description: string }).description = displayDescription;

          context.metadata({
            title: displayDescription,
            metadata: {
              sessionId: childSessionID,
              model,
            },
          });

          const maybeCallID =
            typeof (context as unknown as { callID?: string }).callID ===
            "string"
              ? (context as unknown as { callID: string }).callID
              : undefined;
          if (!maybeCallID || maybeCallID.length === 0) {
            throw new Error(
              "Task plugin contract violation: ToolContext.callID missing for task execution.",
            );
          }
          pendingMetadataByCall.set(callKey(context.sessionID, maybeCallID), {
            title: displayDescription,
            metadata: {
              sessionId: childSessionID,
              model,
            },
          });

          const mode = args.mode ? args.mode.trim().toLowerCase() : "sync";
          if (mode !== "sync" && mode !== "async") {
            throw new Error(
              `Invalid mode: ${JSON.stringify(args.mode)}. Expected "sync" or "async".`,
            );
          }
          let timeoutMs = DEFAULT_TASK_TIMEOUT_MS;
          if (args.timeout_ms !== undefined) {
            if (!Number.isFinite(args.timeout_ms)) {
              throw new Error(`Invalid timeout_ms: ${JSON.stringify(args.timeout_ms)}.`);
            }
            timeoutMs = Math.floor(args.timeout_ms);
            if (timeoutMs <= 0 || timeoutMs > 86_400_000) {
              throw new Error(
                `Invalid timeout_ms: ${JSON.stringify(args.timeout_ms)}. Expected 1..86400000.`,
              );
            }
          }

          if (mode === "async") {
            void runAsyncLifecycle({
              parentSessionID: context.sessionID,
              childSessionID,
              subagent,
              model,
              prompt: args.prompt,
              timeoutMs,
            });

            await log("info", "Async task dispatched", {
              parentSessionID: context.sessionID,
              childSessionID,
              subagentType: subagent.name,
              timeoutMs,
            });

            return buildAsyncRunningOutput({
              sessionID: childSessionID,
              subagentType: subagent.name,
              subagentModel: formatModelRef(model),
            });
          }

          const summary = await runChildPromptToTerminal({
            childSessionID,
            subagent,
            model,
            prompt: args.prompt,
            timeoutMs,
            abortSignal: context.abort,
          });
          return buildTaskSummaryOutput(summary);
        },
      }),
    },
  };
};
