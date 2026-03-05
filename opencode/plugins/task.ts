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
};

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

function renderTranscript(messages: SessionMessage[]): string {
  const lines: string[] = [];
  let stepNumber = 1;

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
  const result = lines.join("\n").trim();
  return result.length > 0 ? result : "No transcript steps were captured.";
}

function computeCompletionConfidenceScore(input: {
  messageCount: number;
  finalText: string;
}): number {
  if (input.messageCount === 0) return 0;
  if (input.finalText.trim().length === 0) return 0.25;
  return 0.6;
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
  ): Promise<T> => {
    let timeoutId: ReturnType<typeof setTimeout> | undefined;
    const timeoutPromise = new Promise<T>((_, reject) => {
      timeoutId = setTimeout(() => {
        reject(new Error(`${label} timed out after ${timeoutMs}ms`));
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

          context.metadata({
            title: args.description,
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
            title: args.description,
            metadata: {
              sessionId: childSessionID,
              model,
            },
          });

          const abortHandler = async () => {
            await client.session.abort({ path: { id: childSessionID } }).catch(() => {});
          };
          context.abort.addEventListener("abort", abortHandler);

          try {
            const startedAt = Date.now();
            const { data: result, error } = await client.session.prompt({
              path: { id: childSessionID },
              body: {
                agent: subagent.name,
                model,
                parts: [{ type: "text", text: args.prompt }],
              },
            });

            if (error) {
              throw new Error(String(error));
            }

            const parts =
              (result as { parts?: Array<{ type?: string; text?: string }> } | undefined)
                ?.parts ?? [];
            const text = extractText(parts);
            const elapsedMs = Date.now() - startedAt;
            const transcriptBundle = await (async (): Promise<TranscriptBundle> => {
              const { data: rawMessages, error: messagesError } =
                await client.session.messages({
                  path: { id: childSessionID },
                });
              if (messagesError || !Array.isArray(rawMessages)) {
                throw new Error(
                  `Failed to load child session messages: ${String(messagesError)}`,
                );
              }

              const messages = rawMessages as SessionMessage[];
              const fullText = renderTranscript(messages);
              const outPath = join(
                tmpdir(),
                `opencode-task-${childSessionID}-${Date.now()}.transcript.md`,
              );
              await fs.writeFile(outPath, `${fullText}\n`, "utf8");
              return {
                path: outPath,
                messageCount: messages.length,
              };
            })();
            const completionConfidenceScore = computeCompletionConfidenceScore({
              messageCount: transcriptBundle.messageCount,
              finalText: text,
            });
            const renderedModel = formatModelRef(model);
            const finalResultText =
              text.length > 0 ? text : "Subagent completed without a text response.";

            await log("info", "Task completed", {
              childSessionID,
              subagentType: subagent.name,
              elapsedMs,
              outputChars: text.length,
              transcriptPath: transcriptBundle.path,
              completionConfidenceScore,
            });

            return [
              "---",
              "status: completed",
              `session_id: ${JSON.stringify(childSessionID)}`,
              `subagent_type: ${JSON.stringify(subagent.name)}`,
              `subagent_model: ${JSON.stringify(renderedModel)}`,
              `duration_ms: ${elapsedMs}`,
              `transcript_path: ${JSON.stringify(transcriptBundle.path)}`,
              `completion_confidence_score: ${completionConfidenceScore.toFixed(2)}`,
              "---",
              "",
              "## 1. Summarized Final Result",
              finalResultText,
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
              `- Full details: read the transcript directly at \`${transcriptBundle.path}\`.`,
              `- Continue this subagent session by calling \`task\` again with \`session_id: ${childSessionID}\` and a new \`prompt\`.`,
              "- Keep `subagent_type` unchanged when resuming, so continuation stays on the same specialist path.",
              "- If the provided `session_id` is invalid, the tool creates a new child session.",
            ].join("\n");
          } finally {
            context.abort.removeEventListener("abort", abortHandler);
          }
        },
      }),
    },
  };
};
