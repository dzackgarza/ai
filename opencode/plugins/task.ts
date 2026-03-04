import { isPluginEnabled } from "./plugins_config";
import { type Plugin, tool } from "@opencode-ai/plugin";
import * as fs from "fs";
import * as path from "path";

const AGENT_FETCH_TIMEOUT_MS = 3000;
const MODEL_FETCH_TIMEOUT_MS = 5000;
const SUBAGENT_CACHE_TTL_MS = 60_000;
const DEFAULT_TASK_TIMEOUT_SECONDS = 1800;
const MIN_TIMEOUT_SECONDS = 1;
const MAX_TIMEOUT_SECONDS = 24 * 60 * 60;
const ASYNC_POLL_INTERVAL_MS = 2000;
const ASYNC_HEARTBEAT_INTERVAL_MS = 120_000;
const PROMPT_ASYNC_START_TIMEOUT_MS = 20_000;
const MAX_ERROR_SUMMARY_CHARS = 500;
const MAX_RESULT_CHARS = 6000;
const ASYNC_TRANSCRIPT_TAIL_LINES = 40;
const MAX_MODEL_HINT_ITEMS = 25;
const TRANSCRIPT_PARSER_SCRIPT =
  "/home/dzack/.config/agents/skills/reading-transcripts/scripts/parse_opencode_log.py";
const TASK_TOOL_DESCRIPTION_BASE =
  "Delegate work to a subagent. Supports two modes: sync (default) and async. Sync mode is blocking and best for smaller sequential tasks where you need the result before continuing. Async mode is non-blocking: it starts the child task and returns a running status, then sends callback updates to the parent session (heartbeat and final completed/failed status). Both modes support timeout_seconds (default 1800 / 30m). On timeout, task attempts a clean child-session interrupt and reports a timeout status with transcript access guidance. In async mode, you can continue your own work and wait for callback messages from the subagent.";
const DEFAULT_SUBAGENT_DESCRIPTION =
  "This subagent should only be called manually by the user.";
const RATE_LIMIT_FALLBACK_CONFIG_PATH = path.join(
  process.env.HOME ?? "",
  ".config",
  "opencode",
  "rate-limit-fallback.json",
);

type ErrorKind =
  | "model_unavailable"
  | "no_response"
  | "rate_limit"
  | "quota"
  | "permission"
  | "aborted"
  | "timeout"
  | "other";

type ChildSessionDiagnostics = {
  assistantMessageID?: string;
  finish?: string;
  errorName?: string;
  errorMessage?: string;
  assistantText?: string;
  partTypes?: string[];
  fetchError?: string;
  errorKind: ErrorKind;
};

type LogLevel = "debug" | "info" | "warn" | "error";

class TimeoutError extends Error {
  constructor(label: string, timeoutMs: number) {
    super(`${label} timed out after ${timeoutMs}ms`);
    this.name = "TimeoutError";
  }
}

function parseModel(
  model?: string,
): { providerID: string; modelID: string } | undefined {
  if (!model) return undefined;
  const [providerID, ...rest] = model.split("/");
  if (!providerID || rest.length === 0) return undefined;
  return { providerID, modelID: rest.join("/") };
}

function extractText(parts: Array<{ type: string; text?: string }>): string {
  return parts
    .filter((p) => p.type === "text" && typeof p.text === "string")
    .map((p) => p.text as string)
    .join("")
    .trim();
}

function stringifyUnknown(value: unknown): string {
  if (typeof value === "string") return value;
  try {
    return JSON.stringify(value);
  } catch {
    return String(value);
  }
}

function truncateText(text: string, maxChars: number): string {
  if (text.length <= maxChars) return text;
  return `${text.slice(0, maxChars)}...`;
}

function normalizeTimeoutSeconds(input: unknown): number {
  if (typeof input !== "number" || !Number.isFinite(input)) {
    return DEFAULT_TASK_TIMEOUT_SECONDS;
  }
  const rounded = Math.floor(input);
  if (rounded < MIN_TIMEOUT_SECONDS) return MIN_TIMEOUT_SECONDS;
  if (rounded > MAX_TIMEOUT_SECONDS) return MAX_TIMEOUT_SECONDS;
  return rounded;
}

function extractErrorDetails(
  error: unknown,
): { name?: string; message?: string } {
  if (!error || typeof error !== "object") return {};

  const payload = error as Record<string, unknown>;
  const name =
    typeof payload.name === "string" && payload.name.length > 0
      ? payload.name
      : undefined;

  const directMessage =
    typeof payload.message === "string" && payload.message.trim().length > 0
      ? payload.message.trim()
      : undefined;

  const data = payload.data as Record<string, unknown> | undefined;
  const nestedMessage =
    typeof data?.message === "string" && data.message.trim().length > 0
      ? data.message.trim()
      : undefined;

  return {
    name,
    message:
      directMessage ??
      nestedMessage ??
      truncateText(stringifyUnknown(error), MAX_ERROR_SUMMARY_CHARS),
  };
}

function classifyErrorKind(
  errorName: string | undefined,
  errorMessage: string | undefined,
  forcedTimeout = false,
): ErrorKind {
  if (forcedTimeout) return "timeout";

  const blob = `${errorName ?? ""}\n${errorMessage ?? ""}`.toLowerCase();

  if (
    blob.includes("model_not_supported") ||
    blob.includes("requested model is not supported") ||
    blob.includes("the requested model is not supported") ||
    blob.includes("model is not supported") ||
    blob.includes("model unavailable") ||
    blob.includes("no endpoints")
  ) {
    return "model_unavailable";
  }

  if (
    blob.includes("empty response") ||
    blob.includes("no response") ||
    blob.includes("no content in response")
  ) {
    return "no_response";
  }

  if (
    blob.includes("rate limit") ||
    blob.includes("too many requests") ||
    blob.includes("429")
  ) {
    return "rate_limit";
  }

  if (
    blob.includes("usage limit") ||
    blob.includes("quota") ||
    blob.includes("credit") ||
    blob.includes("subscription")
  ) {
    return "quota";
  }

  if (
    blob.includes("forbidden") ||
    blob.includes("permission_denied") ||
    blob.includes("permission") ||
    blob.includes("tos violation") ||
    blob.includes("disabled in this account")
  ) {
    return "permission";
  }

  if (
    blob.includes("aborted") ||
    blob.includes("cancelled") ||
    blob.includes("canceled")
  ) {
    return "aborted";
  }

  return "other";
}

function isTerminalFinish(finish?: string): boolean {
  if (!finish) return false;
  return finish !== "tool-calls" && finish !== "unknown";
}

function formatErrorSummary(
  errorName: string | undefined,
  errorMessage: string | undefined,
): string {
  if (errorName && errorMessage) {
    return `${errorName}: ${truncateText(errorMessage, MAX_ERROR_SUMMARY_CHARS)}`;
  }
  if (errorMessage) return truncateText(errorMessage, MAX_ERROR_SUMMARY_CHARS);
  if (errorName) return errorName;
  return "No detailed error message available.";
}

function unique<T>(items: T[]): T[] {
  return [...new Set(items)];
}

function readFallbackModelSuggestions(): string[] {
  try {
    if (!fs.existsSync(RATE_LIMIT_FALLBACK_CONFIG_PATH)) return [];
    const raw = fs.readFileSync(RATE_LIMIT_FALLBACK_CONFIG_PATH, "utf8");
    const parsed = JSON.parse(raw) as {
      enabled?: boolean;
      fallbackModels?: Array<{ providerID?: string; modelID?: string }>;
    };

    if (parsed.enabled === false) return [];

    const models = (parsed.fallbackModels ?? [])
      .map((m) => {
        const providerID = m.providerID?.trim();
        const modelID = m.modelID?.trim();
        if (!providerID || !modelID) return "";
        return `${providerID}/${modelID}`;
      })
      .filter((m) => m.length > 0);

    return unique(models).slice(0, 8);
  } catch {
    return [];
  }
}

function buildRecoveryHint(
  kind: ErrorKind,
  taskID: string,
  fallbackModels: string[],
): string {
  if (kind === "rate_limit" || kind === "quota") {
    const base =
      `Rate-limit or quota issue detected. Retry by resuming this task_id with a different model.`;
    if (fallbackModels.length === 0) {
      return `${base} Resume with task_id=${taskID}. (No fallback models found in rate-limit-fallback.json.)`;
    }
    return `${base} Resume with task_id=${taskID}. Suggested models from rate-limit-fallback.json: ${fallbackModels.join(", ")}.`;
  }

  if (kind === "model_unavailable") {
    const base =
      "Selected model is unavailable or unsupported by the provider/account.";
    if (fallbackModels.length === 0) {
      return `${base} Resume with task_id=${taskID} using a different supported model.`;
    }
    return `${base} Resume with task_id=${taskID}. Suggested fallback models from rate-limit-fallback.json: ${fallbackModels.join(", ")}.`;
  }

  if (kind === "no_response") {
    const base =
      "Provider returned no usable assistant text for this turn.";
    if (fallbackModels.length === 0) {
      return `${base} Resume with task_id=${taskID} on a different model, or retry if transient.`;
    }
    return `${base} Resume with task_id=${taskID}. Suggested fallback models from rate-limit-fallback.json: ${fallbackModels.join(", ")}.`;
  }

  if (kind === "permission") {
    return `Permission/access issue detected. Check provider access or switch to a different model/provider, then resume with task_id=${taskID}.`;
  }

  if (kind === "aborted") {
    return `Task was interrupted. Resume with task_id=${taskID}.`;
  }

  if (kind === "timeout") {
    return `Task timed out. Resume with task_id=${taskID} using a larger timeout_seconds or retry on a faster model.`;
  }

  return `Retry by resuming task_id=${taskID}. If it repeats, switch model and inspect the transcript for root cause.`;
}

function buildFailureReport(input: {
  taskID: string;
  subagentType: string;
  kind: ErrorKind;
  errorName?: string;
  errorMessage?: string;
  timeoutSeconds: number;
  fallbackModels: string[];
}): string {
  const summary = formatErrorSummary(input.errorName, input.errorMessage);
  const hint = buildRecoveryHint(input.kind, input.taskID, input.fallbackModels);

  return [
    `Task failed (kind=${input.kind}).`,
    `task_id=${input.taskID}`,
    `subagent_type=${input.subagentType}`,
    `timeout_seconds=${input.timeoutSeconds}`,
    `error_summary=${summary}`,
    `recovery_hint=${hint}`,
    `transcript_hint=Use read_transcript ${input.taskID}`,
  ].join("\n");
}

function buildAsyncCallback(input: {
  status: "running" | "completed" | "failed";
  taskID: string;
  subagentType: string;
  timeoutSeconds: number;
  kind?: ErrorKind;
  errorName?: string;
  errorMessage?: string;
  transcriptTail?: string;
  elapsedSeconds?: number;
  fallbackModels: string[];
}): string {
  const lines = [
    "[task callback]",
    `status: ${input.status}`,
    "mode: async",
    `task_id: ${input.taskID}`,
    `subagent_type: ${input.subagentType}`,
    `timeout_seconds: ${input.timeoutSeconds}`,
  ];

  if (typeof input.elapsedSeconds === "number") {
    lines.push(`elapsed_seconds: ${input.elapsedSeconds}`);
  }

  if (input.status === "completed") {
    lines.push(`transcript_hint: Use read_transcript ${input.taskID}`);
    if (input.transcriptTail) {
      lines.push(`<task_transcript_tail>`);
      lines.push(input.transcriptTail);
      lines.push("</task_transcript_tail>");
    } else {
      lines.push("task_transcript_tail: unavailable");
    }
    return lines.join("\n");
  }

  if (input.status === "running") {
    lines.push(
      "progress: Background task is still running. Continue your own work; you will be pinged on completion/failure.",
    );
    lines.push(`transcript_hint: Use read_transcript ${input.taskID}`);
    return lines.join("\n");
  }

  const kind = input.kind ?? "other";
  lines.push(`error_kind: ${kind}`);
  lines.push(
    `error_summary: ${formatErrorSummary(input.errorName, input.errorMessage)}`,
  );
  lines.push(
    `recovery_hint: ${buildRecoveryHint(kind, input.taskID, input.fallbackModels)}`,
  );
  lines.push(`transcript_hint: Use read_transcript ${input.taskID}`);
  return lines.join("\n");
}

async function sleep(ms: number): Promise<void> {
  await new Promise((resolve) => setTimeout(resolve, ms));
}

type CachedSubagent = {
  name: string;
  description?: string;
  model?: {
    providerID: string;
    modelID: string;
  };
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
    TASK_TOOL_DESCRIPTION_BASE,
    "",
    "Available subagent types and descriptions:",
    formatSubagentList(subagents),
  ].join("\n");
}

export const TaskPlugin: Plugin = async ({ client, $ }) => {
  if (!isPluginEnabled("task-plugin")) return {};

  let cachedSubagents: CachedSubagent[] = [];
  let cachedAt = 0;
  let cachedModelKeys: Set<string> | undefined;
  let cachedFallbackModels: string[] | undefined;
  let taskToolDescription = buildTaskToolDescription([]);
  const asyncMonitorControllers = new Map<string, AbortController>();

  const log = async (
    level: LogLevel,
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
      // Never break task execution due to logging failure.
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
        reject(new TimeoutError(label, timeoutMs));
      }, timeoutMs);
    });

    try {
      return await Promise.race([promise, timeoutPromise]);
    } finally {
      if (timeoutId) clearTimeout(timeoutId);
    }
  };

  const getFallbackModels = (): string[] => {
    if (cachedFallbackModels) return cachedFallbackModels;
    cachedFallbackModels = readFallbackModelSuggestions();
    return cachedFallbackModels;
  };

  const modelKey = (providerID: string, modelID: string): string =>
    `${providerID}/${modelID}`;

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
      await log("debug", "Using cached subagent definitions", {
        reason,
        cacheAgeMs,
        count: cachedSubagents.length,
      });
      return cachedSubagents;
    }

    try {
      const { data: agentList } = await withTimeout(
        client.app.agents(),
        AGENT_FETCH_TIMEOUT_MS,
        "client.app.agents()",
      );

      const subagents = (agentList ?? [])
        .filter((agent) => agent.mode === "subagent")
        .map((agent) => ({
          name: agent.name,
          description:
            typeof agent.description === "string" &&
            agent.description.trim().length > 0
              ? agent.description
              : undefined,
          model: agent.model ?? undefined,
        }))
        .sort((a, b) => a.name.localeCompare(b.name));

      cachedSubagents = subagents;
      cachedAt = Date.now();

      await log("info", "Fetched subagent definitions", {
        reason,
        totalAgents: agentList?.length ?? 0,
        subagentCount: subagents.length,
        sample: subagents.slice(0, 10).map((item) => ({
          name: item.name,
          hasModel: Boolean(item.model),
        })),
        truncated: subagents.length > 10,
      });

      return subagents;
    } catch {
      await log("warn", "Failed to fetch subagent definitions", {
        reason,
        fallbackToCache: cachedSubagents.length > 0,
        cachedCount: cachedSubagents.length,
      });
      return cachedSubagents;
    }
  };

  const refreshTaskToolDescription = async (
    reason: string,
    force = false,
  ): Promise<string> => {
    const subagents = await fetchSubagents(reason, force);
    taskToolDescription = buildTaskToolDescription(subagents);
    return taskToolDescription;
  };

  const fetchAvailableModelKeys = async (
    reason: string,
    force = false,
  ): Promise<Set<string>> => {
    if (!force && cachedModelKeys && cachedModelKeys.size > 0) {
      await log("debug", "Using cached provider model keys", {
        reason,
        count: cachedModelKeys.size,
      });
      return cachedModelKeys;
    }

    try {
      const { data, error } = await withTimeout(
        client.config.providers(),
        MODEL_FETCH_TIMEOUT_MS,
        "client.config.providers()",
      );

      if (error) {
        await log("warn", "Failed to fetch provider models", {
          reason,
          error: stringifyUnknown(error),
          fallbackToCache: Boolean(cachedModelKeys && cachedModelKeys.size > 0),
          cachedCount: cachedModelKeys?.size ?? 0,
        });
        return cachedModelKeys ?? new Set<string>();
      }

      const keys = new Set<string>();
      for (const provider of data?.providers ?? []) {
        for (const modelID of Object.keys(provider.models ?? {})) {
          keys.add(modelKey(provider.id, modelID));
        }
      }

      cachedModelKeys = keys;
      await log("info", "Fetched provider model keys", {
        reason,
        count: keys.size,
      });
      return keys;
    } catch (error) {
      await log("warn", "Provider model fetch threw", {
        reason,
        error: stringifyUnknown(error),
        fallbackToCache: Boolean(cachedModelKeys && cachedModelKeys.size > 0),
        cachedCount: cachedModelKeys?.size ?? 0,
      });
      return cachedModelKeys ?? new Set<string>();
    }
  };

  const buildActiveModelHint = (
    availableModelKeys: Set<string>,
    providerID?: string,
  ): string => {
    const all = [...availableModelKeys].sort();
    const providerScoped = providerID
      ? all.filter((item) => item.startsWith(`${providerID}/`))
      : [];
    const candidates = providerScoped.length > 0 ? providerScoped : all;
    const shown = candidates.slice(0, MAX_MODEL_HINT_ITEMS);
    const suffix =
      candidates.length > shown.length
        ? ` (showing ${shown.length} of ${candidates.length})`
        : "";
    const header = providerScoped.length > 0
      ? `Active viable models for provider "${providerID}"${suffix}:`
      : `Active viable models${suffix}:`;
    if (shown.length === 0) {
      return "Active viable models list is currently empty.";
    }
    return [header, ...shown.map((item) => `  - ${item}`)].join("\n");
  };

  const getChildSessionDiagnostics = async (
    childSessionID: string,
  ): Promise<ChildSessionDiagnostics> => {
    try {
      const { data: rawMessages, error } = await client.session.messages({
        path: { id: childSessionID },
      });

      if (error) {
        return {
          fetchError: `session.messages failed: ${truncateText(stringifyUnknown(error), MAX_ERROR_SUMMARY_CHARS)}`,
          errorKind: "other",
        };
      }

      const messages = Array.isArray(rawMessages)
        ? (rawMessages as Array<{
            info: {
              role: string;
              id?: string;
              finish?: string;
              error?: unknown;
            };
            parts: Array<{ type: string; text?: string }>;
          }>)
        : [];

      if (messages.length === 0) {
        return {
          fetchError: "session.messages returned no messages",
          errorKind: "other",
        };
      }

      const assistantMessage = [...messages]
        .reverse()
        .find((message) => message.info.role === "assistant");

      if (!assistantMessage) {
        return {
          fetchError: "No assistant message found in child session",
          errorKind: "other",
        };
      }

      const details = extractErrorDetails(assistantMessage.info.error);
      const assistantText = extractText(assistantMessage.parts ?? []);
      const errorKind = classifyErrorKind(details.name, details.message);

      return {
        assistantMessageID:
          typeof assistantMessage.info.id === "string"
            ? assistantMessage.info.id
            : undefined,
        finish:
          typeof assistantMessage.info.finish === "string"
            ? assistantMessage.info.finish
            : undefined,
        errorName: details.name,
        errorMessage: details.message,
        assistantText,
        partTypes: (assistantMessage.parts ?? [])
          .map((part) => part.type)
          .slice(0, 12),
        errorKind,
      };
    } catch (error) {
      return {
        fetchError: `Failed to inspect child session messages: ${truncateText(stringifyUnknown(error), MAX_ERROR_SUMMARY_CHARS)}`,
        errorKind: "other",
      };
    }
  };

  const inferResumedSessionSubagent = async (
    childSessionID: string,
  ): Promise<string | undefined> => {
    try {
      const { data: rawMessages, error } = await client.session.messages({
        path: { id: childSessionID },
      });
      if (error || !Array.isArray(rawMessages)) return undefined;

      const messages = rawMessages as Array<{
        info: {
          role?: string;
          agent?: string;
        };
      }>;

      const resumedFrom = [...messages]
        .reverse()
        .find(
          (message) =>
            message.info?.role === "user" &&
            typeof message.info?.agent === "string" &&
            message.info.agent.length > 0,
        )?.info.agent;

      return resumedFrom;
    } catch {
      return undefined;
    }
  };

  const getChildTranscriptTail = async (
    childSessionID: string,
  ): Promise<string | undefined> => {
    const outPath = `/tmp/transcript-${childSessionID}-${Date.now()}.txt`;
    try {
      await $`python ${TRANSCRIPT_PARSER_SCRIPT} ${childSessionID} > ${outPath}`.quiet();
    } catch {
      return undefined;
    }

    try {
      const content = fs.readFileSync(outPath, "utf-8").trimEnd();
      if (!content) return undefined;
      const lines = content.split("\n");
      const tail = lines.slice(-ASYNC_TRANSCRIPT_TAIL_LINES).join("\n").trim();
      return tail || undefined;
    } catch {
      return undefined;
    } finally {
      try {
        fs.unlinkSync(outPath);
      } catch {}
    }
  };

  const emitParentCallback = async (
    parentSessionID: string,
    text: string,
    terminal: boolean,
  ): Promise<void> => {
    await client.session.promptAsync({
      path: { id: parentSessionID },
      body: {
        noReply: !terminal,
        parts: [{ type: "text", text }],
      },
    });
  };

  const runAsyncMonitor = async (input: {
    parentSessionID: string;
    childSessionID: string;
    subagentType: string;
    timeoutSeconds: number;
  }): Promise<void> => {
    const startMs = Date.now();
    const timeoutMs = input.timeoutSeconds * 1000;
    const fallbackModels = getFallbackModels();
    let lastHeartbeatAt = startMs;

    while (Date.now() - startMs < timeoutMs) {
      const controller = asyncMonitorControllers.get(input.childSessionID);
      if (!controller || controller.signal.aborted) return;

      const diagnostics = await getChildSessionDiagnostics(input.childSessionID);
      const elapsedSeconds = Math.floor((Date.now() - startMs) / 1000);

      if (diagnostics.errorName || diagnostics.errorMessage) {
        await log("error", "Async task failed in child session", {
          childSessionID: input.childSessionID,
          subagentType: input.subagentType,
          diagnostics,
        });

        await emitParentCallback(
          input.parentSessionID,
          buildAsyncCallback({
            status: "failed",
            taskID: input.childSessionID,
            subagentType: input.subagentType,
            timeoutSeconds: input.timeoutSeconds,
            kind: diagnostics.errorKind,
            errorName: diagnostics.errorName,
            errorMessage: diagnostics.errorMessage,
            elapsedSeconds,
            fallbackModels,
          }),
          true,
        );
        return;
      }

      if (diagnostics.assistantText) {
        const transcriptTail = await getChildTranscriptTail(input.childSessionID);

        await log("info", "Async task completed", {
          childSessionID: input.childSessionID,
          subagentType: input.subagentType,
          outputChars: diagnostics.assistantText.length,
        });

        await emitParentCallback(
          input.parentSessionID,
          buildAsyncCallback({
            status: "completed",
            taskID: input.childSessionID,
            subagentType: input.subagentType,
            timeoutSeconds: input.timeoutSeconds,
            transcriptTail,
            elapsedSeconds,
            fallbackModels,
          }),
          true,
        );
        return;
      }

      if (isTerminalFinish(diagnostics.finish)) {
        const inferredKind =
          diagnostics.errorName || diagnostics.errorMessage
            ? diagnostics.errorKind
            : "no_response";
        await log("error", "Async task reached terminal state without output", {
          childSessionID: input.childSessionID,
          subagentType: input.subagentType,
          diagnostics,
        });

        await emitParentCallback(
          input.parentSessionID,
          buildAsyncCallback({
            status: "failed",
            taskID: input.childSessionID,
            subagentType: input.subagentType,
            timeoutSeconds: input.timeoutSeconds,
            kind: inferredKind,
            errorName: diagnostics.errorName,
            errorMessage:
              diagnostics.errorMessage ??
              "Child session finished without text output.",
            elapsedSeconds,
            fallbackModels,
          }),
          true,
        );
        return;
      }

      if (Date.now() - lastHeartbeatAt >= ASYNC_HEARTBEAT_INTERVAL_MS) {
        lastHeartbeatAt = Date.now();
        await emitParentCallback(
          input.parentSessionID,
          buildAsyncCallback({
            status: "running",
            taskID: input.childSessionID,
            subagentType: input.subagentType,
            timeoutSeconds: input.timeoutSeconds,
            elapsedSeconds,
            fallbackModels,
          }),
          false,
        ).catch(async (error) => {
          await log("warn", "Failed to emit async heartbeat callback", {
            parentSessionID: input.parentSessionID,
            childSessionID: input.childSessionID,
            error: stringifyUnknown(error),
          });
        });
      }

      await sleep(ASYNC_POLL_INTERVAL_MS);
    }

    await client.session
      .abort({ path: { id: input.childSessionID } })
      .catch(() => {});

    const diagnostics = await getChildSessionDiagnostics(input.childSessionID);

    await log("warn", "Async task timed out", {
      childSessionID: input.childSessionID,
      subagentType: input.subagentType,
      timeoutSeconds: input.timeoutSeconds,
      diagnostics,
    });

    await emitParentCallback(
      input.parentSessionID,
      buildAsyncCallback({
        status: "failed",
        taskID: input.childSessionID,
        subagentType: input.subagentType,
        timeoutSeconds: input.timeoutSeconds,
        kind: "timeout",
        errorName: "TimeoutError",
        errorMessage: `Background task timed out after ${input.timeoutSeconds}s and was interrupted.`,
        elapsedSeconds: input.timeoutSeconds,
        fallbackModels: getFallbackModels(),
      }),
      true,
    );
  };

  await log("info", "Task plugin initialized", {
    agentFetchTimeoutMs: AGENT_FETCH_TIMEOUT_MS,
    subagentCacheTtlMs: SUBAGENT_CACHE_TTL_MS,
    defaultTimeoutSeconds: DEFAULT_TASK_TIMEOUT_SECONDS,
    permissionAskDisabledByPolicy: true,
    childPermissionMutationDisabledByPolicy: true,
    parentModelInheritanceDisabledByPolicy: true,
  });

  void refreshTaskToolDescription("plugin_init_warmup", true);
  void fetchAvailableModelKeys("plugin_init_warmup", true);

  return {
    "tool.definition": async (input, output) => {
      if (input.toolID !== "task") return;
      output.description = await refreshTaskToolDescription(
        "tool_definition",
        false,
      );
    },
    tool: {
      task: tool({
        description: taskToolDescription,
        args: {
          description: tool.schema
            .string()
            .describe("Short title for the delegated task (child session title)."),
          subagent_type: tool.schema
            .string()
            .describe("Exact subagent name to run."),
          prompt: tool.schema
            .string()
            .describe("Complete task prompt for the subagent."),
          model: tool.schema
            .string()
            .optional()
            .describe(
              "Optional provider/model override in provider/model format.",
            ),
          task_id: tool.schema
            .string()
            .optional()
            .describe(
              "Resume an existing child session instead of creating a new one.",
            ),
          async: tool.schema
            .boolean()
            .optional()
            .describe(
              "If true, run task in non-blocking async mode with callback updates.",
            ),
          timeout_seconds: tool.schema
            .number()
            .optional()
            .describe(
              "Hard timeout in seconds for sync/async execution. Default: 1800 (30m).",
            ),
        },
        async execute(args, context) {
          // POLICY (intentional): subagents are autonomous/background workers.
          // We intentionally DO NOT call context.ask(...) here because task-level
          // permission prompts can freeze orchestrations. By convention, only top-level
          // agents should require interactive ask permissions.
          const mode = args.async ? "async" : "sync";
          const timeoutSeconds = normalizeTimeoutSeconds(args.timeout_seconds);
          const timeoutMs = timeoutSeconds * 1000;
          const { sessionID } = context;

          await log("info", "Task tool execution started", {
            sessionID,
            mode,
            subagentType: args.subagent_type,
            hasTaskId: Boolean(args.task_id),
            hasModelOverride: Boolean(args.model),
            timeoutSeconds,
          });

          const subagents = await fetchSubagents("task_execute_validation", true);
          const subagentNames = subagents.map((item) => item.name);
          const subagent = subagents.find(
            (item) => item.name === args.subagent_type,
          );

          const hasModelOverride =
            typeof args.model === "string" && args.model.trim().length > 0;
          const overrideModelSpec = hasModelOverride
            ? parseModel(args.model)
            : undefined;

          if (!subagent) {
            await log("error", "Invalid subagent_type for task tool", {
              subagentType: args.subagent_type,
              validCount: subagentNames.length,
              validSample: subagentNames.slice(0, 10),
              hasTaskId: Boolean(args.task_id),
            });
            if (subagentNames.length === 0) {
              throw new Error(
                [
                  `Unknown subagent_type "${args.subagent_type}".`,
                  "No subagents are currently discoverable via client.app.agents().",
                ].join(" "),
              );
            }
            throw new Error(
              `Unknown subagent_type "${args.subagent_type}". Valid options:\n${subagentNames
                .map((name) => `  - ${name}`)
                .join("\n")}`,
            );
          }

          if (hasModelOverride && !overrideModelSpec) {
            const availableModelKeys = await fetchAvailableModelKeys(
              "task_execute_model_validation",
              true,
            );
            throw new Error(
              [
                `Invalid model override "${args.model}".`,
                "Expected format: provider/model (for example: anthropic/claude-sonnet-4-6).",
                buildActiveModelHint(availableModelKeys),
              ].join("\n"),
            );
          }
          if (overrideModelSpec) {
            const availableModelKeys = await fetchAvailableModelKeys(
              "task_execute_model_validation",
              true,
            );
            if (availableModelKeys.size === 0) {
              throw new Error(
                "Cannot validate model override: provider/model list is unavailable.",
              );
            }
            const key = modelKey(
              overrideModelSpec.providerID,
              overrideModelSpec.modelID,
            );
            if (!availableModelKeys.has(key)) {
              throw new Error(
                [
                  `Unknown model override "${key}".`,
                  buildActiveModelHint(availableModelKeys, overrideModelSpec.providerID),
                ].join("\n"),
              );
            }
          }

          // POLICY (intentional): never inherit the caller model for subagents.
          // Default model must come from subagent config. Override is allowed but
          // validated strictly above. The parent/caller model is never inherited.
          if (!args.task_id && !overrideModelSpec && !subagent?.model) {
            throw new Error(
              [
                `No model resolved for subagent_type="${args.subagent_type}".`,
                "Policy: delegated subagents never inherit the parent model.",
                "Set a model on the subagent config or pass args.model explicitly.",
              ].join(" "),
            );
          }

          let childSessionID = args.task_id;
          if (!childSessionID) {
            // POLICY (intentional): do not inject/override child permissions in this plugin.
            // Child permissions must be explicit in agent/session config.
            const { data: session, error: createError } =
              await client.session.create({
                body: {
                  title: args.description,
                  parentID: sessionID,
                },
              });

            if (createError || !session?.id) {
              await log("error", "Child session creation failed", {
                createError,
                sessionID,
                subagentType: args.subagent_type,
              });
              throw new Error(
                `Failed to create child session: ${stringifyUnknown(createError)}`,
              );
            }

            childSessionID = session.id;
          }

          if (args.task_id) {
            // POLICY: resume calls should continue with the same subagent whenever we can
            // infer prior routing from child-session history.
            const resumedFrom = await inferResumedSessionSubagent(childSessionID);
            if (resumedFrom && resumedFrom !== args.subagent_type) {
              throw new Error(
                [
                  `task_id "${childSessionID}" was previously routed to subagent "${resumedFrom}".`,
                  `Refusing resume with mismatched subagent "${args.subagent_type}".`,
                ].join(" "),
              );
            }
          }

          context.metadata({
            title: args.description,
            metadata: {
              sessionId: childSessionID,
              mode,
              subagentType: args.subagent_type,
              timeoutSeconds,
              ...(overrideModelSpec ? { model: overrideModelSpec } : {}),
            },
          });

          const promptBody: Record<string, unknown> = {
            agent: args.subagent_type,
            parts: [{ type: "text", text: args.prompt }],
          };
          if (overrideModelSpec) {
            promptBody.model = overrideModelSpec;
          }

          if (mode === "async") {
            try {
              const { error: promptAsyncError } = await withTimeout(
                client.session.promptAsync({
                  path: { id: childSessionID },
                  body: promptBody as Parameters<
                    typeof client.session.promptAsync
                  >[0]["body"],
                }),
                PROMPT_ASYNC_START_TIMEOUT_MS,
                "client.session.promptAsync()",
              );

              if (promptAsyncError) {
                const details = extractErrorDetails(promptAsyncError);
                const kind = classifyErrorKind(details.name, details.message);
                const failure = buildFailureReport({
                  taskID: childSessionID,
                  subagentType: args.subagent_type,
                  kind,
                  errorName: details.name,
                  errorMessage: details.message,
                  timeoutSeconds,
                  fallbackModels: getFallbackModels(),
                });
                throw new Error(failure);
              }
            } catch (error) {
              const details = extractErrorDetails(error);
              const kind =
                error instanceof TimeoutError
                  ? "timeout"
                  : classifyErrorKind(details.name, details.message);

              if (kind === "timeout") {
                await client.session
                  .abort({ path: { id: childSessionID } })
                  .catch(() => {});
              }

              const failure = buildFailureReport({
                taskID: childSessionID,
                subagentType: args.subagent_type,
                kind,
                errorName: details.name,
                errorMessage: details.message,
                timeoutSeconds,
                fallbackModels: getFallbackModels(),
              });

              await log("error", "Async task launch failed", {
                childSessionID,
                subagentType: args.subagent_type,
                kind,
                error: stringifyUnknown(error),
              });

              throw new Error(failure);
            }

            const existingMonitor = asyncMonitorControllers.get(childSessionID);
            if (existingMonitor) existingMonitor.abort();

            const monitorController = new AbortController();
            asyncMonitorControllers.set(childSessionID, monitorController);

            void runAsyncMonitor({
              parentSessionID: sessionID,
              childSessionID,
              subagentType: args.subagent_type,
              timeoutSeconds,
            })
              .catch(async (error) => {
                await log("error", "Async task monitor crashed", {
                  childSessionID,
                  subagentType: args.subagent_type,
                  error: stringifyUnknown(error),
                });

                await emitParentCallback(
                  sessionID,
                  buildAsyncCallback({
                    status: "failed",
                    taskID: childSessionID,
                    subagentType: args.subagent_type,
                    timeoutSeconds,
                    kind: "other",
                    errorName: "AsyncMonitorError",
                    errorMessage: stringifyUnknown(error),
                    fallbackModels: getFallbackModels(),
                  }),
                  true,
                ).catch(() => {});
              })
              .finally(() => {
                const active = asyncMonitorControllers.get(childSessionID);
                if (active === monitorController) {
                  asyncMonitorControllers.delete(childSessionID);
                }
              });

            await log("info", "Async task launched", {
              parentSessionID: sessionID,
              childSessionID,
              subagentType: args.subagent_type,
              timeoutSeconds,
            });

            return [
              "task_mode: async",
              "task_status: running",
              `task_id: ${childSessionID}`,
              `subagent_type: ${args.subagent_type}`,
              `timeout_seconds: ${timeoutSeconds}`,
              "callback: parent session will receive heartbeat and terminal status updates automatically.",
              `transcript_hint: Use read_transcript ${childSessionID}`,
            ].join("\n");
          }

          const abortHandler = async () => {
            await client.session.abort({ path: { id: childSessionID } });
          };
          context.abort.addEventListener("abort", abortHandler);

          let result: unknown;
          let promptError: unknown;
          try {
            ({ data: result, error: promptError } = await withTimeout(
              client.session.prompt({
                path: { id: childSessionID },
                body: promptBody as Parameters<typeof client.session.prompt>[0]["body"],
              }),
              timeoutMs,
              "client.session.prompt()",
            ));
          } catch (error) {
            context.abort.removeEventListener("abort", abortHandler);

            const isTimeout = error instanceof TimeoutError;
            if (isTimeout) {
              await client.session
                .abort({ path: { id: childSessionID } })
                .catch(() => {});
            }

            const details = extractErrorDetails(error);
            const kind = isTimeout
              ? "timeout"
              : classifyErrorKind(details.name, details.message);

            const failure = buildFailureReport({
              taskID: childSessionID,
              subagentType: args.subagent_type,
              kind,
              errorName: details.name,
              errorMessage: details.message,
              timeoutSeconds,
              fallbackModels: getFallbackModels(),
            });

            await log("error", "Sync task execution failed", {
              childSessionID,
              subagentType: args.subagent_type,
              kind,
              error: stringifyUnknown(error),
            });

            throw new Error(failure);
          }

          context.abort.removeEventListener("abort", abortHandler);

          if (promptError) {
            const details = extractErrorDetails(promptError);
            const kind = classifyErrorKind(details.name, details.message);

            const failure = buildFailureReport({
              taskID: childSessionID,
              subagentType: args.subagent_type,
              kind,
              errorName: details.name,
              errorMessage: details.message,
              timeoutSeconds,
              fallbackModels: getFallbackModels(),
            });

            await log("error", "Child session prompt failed", {
              childSessionID,
              subagentType: args.subagent_type,
              kind,
              promptError: stringifyUnknown(promptError),
            });

            throw new Error(failure);
          }

          const parts = (result as { parts?: Array<{ type: string; text?: string }> } | undefined)?.parts ?? [];
          const text = extractText(parts);

          if (!text) {
            const diagnostics = await getChildSessionDiagnostics(childSessionID);
            const inferredKind =
              !diagnostics.errorName &&
              !diagnostics.errorMessage &&
              !diagnostics.fetchError
                ? "no_response"
                : diagnostics.errorKind;
            const failure = buildFailureReport({
              taskID: childSessionID,
              subagentType: args.subagent_type,
              kind: inferredKind,
              errorName: diagnostics.errorName,
              errorMessage:
                diagnostics.errorMessage ??
                diagnostics.fetchError ??
                "Child session returned no text output.",
              timeoutSeconds,
              fallbackModels: getFallbackModels(),
            });

            await log("error", "Child session returned empty text", {
              childSessionID,
              subagentType: args.subagent_type,
              diagnostics,
            });

            throw new Error(failure);
          }

          await log("info", "Sync task completed", {
            childSessionID,
            subagentType: args.subagent_type,
            outputChars: text.length,
          });

          return [
            "task_mode: sync",
            "task_status: completed",
            `task_id: ${childSessionID}`,
            `subagent_type: ${args.subagent_type}`,
            `timeout_seconds: ${timeoutSeconds}`,
            `<task_result>`,
            truncateText(text, MAX_RESULT_CHARS),
            `</task_result>`,
          ].join("\n");
        },
      }),
    },
  };
};
