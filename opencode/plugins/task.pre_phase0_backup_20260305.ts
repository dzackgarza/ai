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
const ASYNC_HEARTBEAT_INTERVAL_MS = 120_000;
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
const ASYNC_TRACE_ENABLED = process.env.TASK_ASYNC_TRACE !== "0";
const ASYNC_TRACE_TO_APP_LOG_ENABLED =
  process.env.TASK_ASYNC_TRACE_TO_APP_LOG !== "0";
const ASYNC_LAUNCH_STRATEGY =
  process.env.TASK_ASYNC_LAUNCH_STRATEGY ?? "native";
const ASYNC_TRACE_PATH =
  process.env.TASK_ASYNC_TRACE_PATH ?? "/tmp/task-async-trace.jsonl";

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

type TaskSessionSummary = {
  totalMessages: number;
  assistantMessages: number;
  toolCalls: number;
  lastToolName?: string;
  lastToolTitle?: string;
  lastAssistantTextChars: number;
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
  status: "heartbeat" | "completed" | "failed";
  taskID: string;
  subagentType: string;
  timeoutSeconds: number;
  kind?: ErrorKind;
  errorName?: string;
  errorMessage?: string;
  transcriptTail?: string;
  elapsedSeconds?: number;
  observedToolCalls?: number;
  sessionSummary?: string;
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
  if (typeof input.observedToolCalls === "number") {
    lines.push(`tool_calls_observed: ${input.observedToolCalls}`);
  }

  if (input.status === "completed") {
    lines.push(`transcript_hint: Use read_transcript ${input.taskID}`);
    if (input.sessionSummary) {
      lines.push(input.sessionSummary);
    } else {
      lines.push("task_session_summary: unavailable");
    }
    if (input.transcriptTail) {
      lines.push(`<task_transcript_tail>`);
      lines.push(input.transcriptTail);
      lines.push("</task_transcript_tail>");
    } else {
      lines.push("task_transcript_tail: unavailable");
    }
    return lines.join("\n");
  }

  if (input.status === "heartbeat") {
    lines.push(
      "progress: Background task is still running. Continue your own work; you will be pinged on completion/failure.",
    );
    if (input.sessionSummary) {
      lines.push(input.sessionSummary);
    }
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
  if (input.sessionSummary) {
    lines.push(input.sessionSummary);
  }
  lines.push(`transcript_hint: Use read_transcript ${input.taskID}`);
  return lines.join("\n");
}

function formatTaskSessionSummary(summary: TaskSessionSummary): string {
  const lines = [
    "<task_session_summary>",
    `total_messages: ${summary.totalMessages}`,
    `assistant_messages: ${summary.assistantMessages}`,
    `tool_calls: ${summary.toolCalls}`,
    `last_assistant_text_chars: ${summary.lastAssistantTextChars}`,
  ];
  if (summary.lastToolName) {
    lines.push(`last_tool_name: ${summary.lastToolName}`);
  }
  if (summary.lastToolTitle) {
    lines.push(`last_tool_title: ${summary.lastToolTitle}`);
  }
  lines.push("</task_session_summary>");
  return lines.join("\n");
}

type CachedSubagent = {
  name: string;
  description?: string;
  model?: {
    providerID: string;
    modelID: string;
  };
};

type ToolContextWithCallID = {
  callID?: string;
};

type TaskModelRef = {
  providerID: string;
  modelID: string;
};

type ParentTaskRef = {
  parentSessionID: string;
  parentMessageID: string;
  parentCallID: string;
  childSessionID: string;
  mode: "sync" | "async";
  subagentType: string;
  description: string;
  timeoutSeconds: number;
  model?: TaskModelRef;
};

type AsyncPhase1State = {
  ref: ParentTaskRef;
  startedAtMs: number;
  heartbeatTimer: ReturnType<typeof setInterval>;
  timeoutTimer: ReturnType<typeof setTimeout>;
  seenToolPartIDs: Set<string>;
  terminalEmitted: boolean;
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

export const TaskPlugin: Plugin = async ({ client, $, serverUrl, directory }) => {
  if (!isPluginEnabled("task-plugin")) return {};

  let cachedSubagents: CachedSubagent[] = [];
  let cachedAt = 0;
  let cachedModelKeys: Set<string> | undefined;
  let cachedFallbackModels: string[] | undefined;
  let taskToolDescription = buildTaskToolDescription([]);
  const encodedDirectory =
    /[^\x00-\x7F]/.test(directory) ? encodeURIComponent(directory) : directory;
  const asyncPhase1States = new Map<string, AsyncPhase1State>();
  const asyncTraceRefs = new Map<string, ParentTaskRef>();
  const parentTaskRefsByCallKey = new Map<string, ParentTaskRef>();
  const asyncTraceCounters = new Map<
    string,
    {
      messageUpdated: number;
      partUpdated: number;
      partDelta: number;
      sessionStatus: number;
      sessionUpdated: number;
      other: number;
    }
  >();

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

  if (ASYNC_TRACE_ENABLED) {
    try {
      fs.mkdirSync(path.dirname(ASYNC_TRACE_PATH), { recursive: true });
      fs.appendFileSync(
        ASYNC_TRACE_PATH,
        JSON.stringify({
          ts: Date.now(),
          iso: new Date().toISOString(),
          type: "trace.init",
          directory,
        }) + "\n",
      );
    } catch {
      // Trace logging is best effort only.
    }
  }

  const trace = (type: string, payload: Record<string, unknown>): void => {
    if (!ASYNC_TRACE_ENABLED) return;
    const record = {
      ts: Date.now(),
      iso: new Date().toISOString(),
      type,
      ...payload,
    };
    if (ASYNC_TRACE_TO_APP_LOG_ENABLED) {
      void log("debug", `trace.${type}`, payload);
    }
    try {
      fs.appendFileSync(
        ASYNC_TRACE_PATH,
        JSON.stringify(record) + "\n",
      );
    } catch {
      // Trace logging is best effort only.
    }
  };

  const initAsyncTraceCounters = (childSessionID: string): void => {
    asyncTraceCounters.set(childSessionID, {
      messageUpdated: 0,
      partUpdated: 0,
      partDelta: 0,
      sessionStatus: 0,
      sessionUpdated: 0,
      other: 0,
    });
  };

  const parentTaskCallKey = (input: {
    parentSessionID: string;
    parentMessageID: string;
    parentCallID: string;
  }): string => `${input.parentSessionID}:${input.parentMessageID}:${input.parentCallID}`;

  const patchParentTaskPart = async (part: Record<string, unknown>): Promise<void> => {
    const sessionID = part.sessionID;
    const messageID = part.messageID;
    const partID = part.id;
    if (
      typeof sessionID !== "string" ||
      typeof messageID !== "string" ||
      typeof partID !== "string"
    ) {
      throw new Error("Invalid parent task part: missing id/sessionID/messageID.");
    }

    const partPath = `/session/${encodeURIComponent(
      sessionID,
    )}/message/${encodeURIComponent(messageID)}/part/${encodeURIComponent(partID)}`;
    const url = new URL(partPath, serverUrl);
    const response = await fetch(url, {
      method: "PATCH",
      headers: {
        "content-type": "application/json",
        "x-opencode-directory": encodedDirectory,
      },
      body: JSON.stringify(part),
    });

    if (!response.ok) {
      const text = await response.text().catch(() => "");
      throw new Error(
        `Failed to patch parent task part (${response.status}): ${text || response.statusText}`,
      );
    }
  };

  const rehydrateParentTaskPart = async (input: {
    part: Record<string, unknown>;
    ref: ParentTaskRef;
  }): Promise<void> => {
    const state =
      typeof input.part.state === "object" && input.part.state
        ? (input.part.state as Record<string, unknown>)
        : undefined;
    if (!state) return;

    const status =
      typeof state.status === "string" ? state.status : undefined;
    if (!status || status === "pending") return;

    const existingMetadata =
      typeof state.metadata === "object" && state.metadata
        ? (state.metadata as Record<string, unknown>)
        : {};

    const desiredMetadata: Record<string, unknown> = {
      ...existingMetadata,
      sessionId: input.ref.childSessionID,
      mode: input.ref.mode,
      subagentType: input.ref.subagentType,
      timeoutSeconds: input.ref.timeoutSeconds,
    };
    if (input.ref.model) {
      desiredMetadata.model = input.ref.model;
    }

    const existingSessionId =
      typeof existingMetadata.sessionId === "string"
        ? existingMetadata.sessionId
        : undefined;
    const existingTitle =
      typeof state.title === "string" && state.title.trim().length > 0
        ? state.title
        : undefined;
    if (
      existingSessionId === input.ref.childSessionID &&
      existingTitle === input.ref.description
    ) {
      return;
    }

    await patchParentTaskPart({
      ...input.part,
      state: {
        ...state,
        title: input.ref.description,
        metadata: desiredMetadata,
      },
    });
  };

  const bumpAsyncTraceCounter = (
    childSessionID: string,
    type: string,
  ): void => {
    const current = asyncTraceCounters.get(childSessionID);
    if (!current) return;
    if (type === "message.updated") current.messageUpdated += 1;
    else if (type === "message.part.updated") current.partUpdated += 1;
    else if (type === "message.part.delta") current.partDelta += 1;
    else if (type === "session.status") current.sessionStatus += 1;
    else if (type === "session.updated") current.sessionUpdated += 1;
    else current.other += 1;
    asyncTraceCounters.set(childSessionID, current);
  };

  const summarizeAsyncTrace = (
    childSessionID: string,
    reason: string,
    extra?: Record<string, unknown>,
  ): void => {
    const counters = asyncTraceCounters.get(childSessionID);
    trace("async.trace.summary", {
      childSessionID,
      reason,
      counters,
      ...extra,
    });
  };

  const isTrackedTraceSession = (sessionID: string | undefined): boolean => {
    if (!sessionID) return false;
    if (asyncTraceRefs.has(sessionID)) return true;
    for (const ref of asyncTraceRefs.values()) {
      if (ref.parentSessionID === sessionID) return true;
    }
    return false;
  };

  const childSessionsForEvent = (sessionID: string | undefined): string[] => {
    if (!sessionID) return [];
    const out: string[] = [];
    for (const ref of asyncTraceRefs.values()) {
      if (
        ref.childSessionID === sessionID ||
        ref.parentSessionID === sessionID
      ) {
        out.push(ref.childSessionID);
      }
    }
    return out;
  };

  const extractEventSessionID = (event: {
    type: string;
    properties?: unknown;
  }): string | undefined => {
    const properties =
      typeof event.properties === "object" && event.properties
        ? (event.properties as Record<string, unknown>)
        : {};

    if (event.type === "message.updated") {
      const info =
        typeof properties.info === "object" && properties.info
          ? (properties.info as Record<string, unknown>)
          : {};
      return typeof info.sessionID === "string" ? info.sessionID : undefined;
    }

    if (event.type === "message.part.updated") {
      const part =
        typeof properties.part === "object" && properties.part
          ? (properties.part as Record<string, unknown>)
          : {};
      return typeof part.sessionID === "string" ? part.sessionID : undefined;
    }

    if (event.type === "message.part.delta") {
      return typeof properties.sessionID === "string"
        ? properties.sessionID
        : undefined;
    }

    if (event.type === "message.removed") {
      return typeof properties.sessionID === "string"
        ? properties.sessionID
        : undefined;
    }

    if (event.type === "session.status") {
      return typeof properties.sessionID === "string"
        ? properties.sessionID
        : undefined;
    }

    if (event.type === "session.updated") {
      const info =
        typeof properties.info === "object" && properties.info
          ? (properties.info as Record<string, unknown>)
          : {};
      return typeof info.id === "string" ? info.id : undefined;
    }

    return undefined;
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

  const collectChildSessionSummary = async (
    childSessionID: string,
  ): Promise<TaskSessionSummary | undefined> => {
    try {
      const { data: rawMessages, error } = await client.session.messages({
        path: { id: childSessionID },
      });
      if (error || !Array.isArray(rawMessages)) return undefined;

      const messages = rawMessages as Array<{
        info: { role?: string };
        parts?: Array<{
          id?: string;
          type?: string;
          tool?: string;
          text?: string;
          state?: { title?: string };
        }>;
      }>;

      let toolCalls = 0;
      let lastToolName: string | undefined;
      let lastToolTitle: string | undefined;
      let lastAssistantTextChars = 0;

      const assistantMessages = messages.filter(
        (message) => message.info?.role === "assistant",
      );
      for (const message of assistantMessages) {
        for (const part of message.parts ?? []) {
          if (part?.type === "tool") {
            toolCalls += 1;
            if (typeof part.tool === "string" && part.tool.length > 0) {
              lastToolName = part.tool;
            }
            if (
              part.state &&
              typeof part.state.title === "string" &&
              part.state.title.length > 0
            ) {
              lastToolTitle = part.state.title;
            }
          } else if (part?.type === "text" && typeof part.text === "string") {
            lastAssistantTextChars = part.text.length;
          }
        }
      }

      return {
        totalMessages: messages.length,
        assistantMessages: assistantMessages.length,
        toolCalls,
        lastToolName,
        lastToolTitle,
        lastAssistantTextChars,
      };
    } catch {
      return undefined;
    }
  };

  const emitParentCallback = async (
    parentSessionID: string,
    text: string,
    terminal: boolean,
  ): Promise<void> => {
    trace("async.parent_callback.emit", {
      parentSessionID,
      terminal,
      preview: text.slice(0, 200),
    });
    await client.session.promptAsync({
      path: { id: parentSessionID },
      body: {
        noReply: !terminal,
        parts: [{ type: "text", text }],
      },
    });
  };

  const clearAsyncPhase1State = (
    childSessionID: string,
    reason: string,
    extra?: Record<string, unknown>,
  ): void => {
    const state = asyncPhase1States.get(childSessionID);
    if (state) {
      clearInterval(state.heartbeatTimer);
      clearTimeout(state.timeoutTimer);
      asyncPhase1States.delete(childSessionID);
      parentTaskRefsByCallKey.delete(parentTaskCallKey(state.ref));
    }
    summarizeAsyncTrace(childSessionID, reason, extra);
    asyncTraceRefs.delete(childSessionID);
    asyncTraceCounters.delete(childSessionID);
  };

  const emitAsyncHeartbeat = async (childSessionID: string): Promise<void> => {
    const state = asyncPhase1States.get(childSessionID);
    if (!state || state.terminalEmitted) return;

    const elapsedSeconds = Math.floor((Date.now() - state.startedAtMs) / 1000);
    const fallbackModels = getFallbackModels();
    const summary = await collectChildSessionSummary(childSessionID);

    await emitParentCallback(
      state.ref.parentSessionID,
      buildAsyncCallback({
        status: "heartbeat",
        taskID: state.ref.childSessionID,
        subagentType: state.ref.subagentType,
        timeoutSeconds: state.ref.timeoutSeconds,
        elapsedSeconds,
        observedToolCalls: state.seenToolPartIDs.size,
        sessionSummary: summary ? formatTaskSessionSummary(summary) : undefined,
        fallbackModels,
      }),
      false,
    ).catch(async (error) => {
      await log("warn", "Failed to emit async heartbeat callback", {
        parentSessionID: state.ref.parentSessionID,
        childSessionID,
        error: stringifyUnknown(error),
      });
    });
  };

  const emitAsyncTerminalCallback = async (
    childSessionID: string,
    launchError?: unknown,
  ): Promise<void> => {
    const state = asyncPhase1States.get(childSessionID);
    if (!state || state.terminalEmitted) return;
    state.terminalEmitted = true;

    const fallbackModels = getFallbackModels();
    const elapsedSeconds = Math.floor((Date.now() - state.startedAtMs) / 1000);
    const summary = await collectChildSessionSummary(childSessionID);
    const sessionSummary = summary ? formatTaskSessionSummary(summary) : undefined;

    if (launchError) {
      const details = extractErrorDetails(launchError);
      const kind = classifyErrorKind(details.name, details.message);
      await emitParentCallback(
        state.ref.parentSessionID,
        buildAsyncCallback({
          status: "failed",
          taskID: childSessionID,
          subagentType: state.ref.subagentType,
          timeoutSeconds: state.ref.timeoutSeconds,
          kind,
          errorName: details.name,
          errorMessage: details.message,
          elapsedSeconds,
          observedToolCalls: state.seenToolPartIDs.size,
          sessionSummary,
          fallbackModels,
        }),
        true,
      ).catch(async (error) => {
        await log("warn", "Failed to emit async failed callback", {
          parentSessionID: state.ref.parentSessionID,
          childSessionID,
          error: stringifyUnknown(error),
        });
      });
      clearAsyncPhase1State(childSessionID, "phase1.terminal.failed_launch", {
        elapsedSeconds,
        kind,
      });
      return;
    }

    const diagnostics = await getChildSessionDiagnostics(childSessionID);
    if (
      diagnostics.errorName ||
      diagnostics.errorMessage ||
      (isTerminalFinish(diagnostics.finish) && !diagnostics.assistantText)
    ) {
      const errorMessage =
        diagnostics.errorMessage ??
        "Child session completed without assistant text output.";
      await emitParentCallback(
        state.ref.parentSessionID,
        buildAsyncCallback({
          status: "failed",
          taskID: childSessionID,
          subagentType: state.ref.subagentType,
          timeoutSeconds: state.ref.timeoutSeconds,
          kind: diagnostics.errorKind,
          errorName: diagnostics.errorName,
          errorMessage,
          elapsedSeconds,
          observedToolCalls: state.seenToolPartIDs.size,
          sessionSummary,
          fallbackModels,
        }),
        true,
      ).catch(async (error) => {
        await log("warn", "Failed to emit async failed callback", {
          parentSessionID: state.ref.parentSessionID,
          childSessionID,
          error: stringifyUnknown(error),
        });
      });
      clearAsyncPhase1State(childSessionID, "phase1.terminal.failed_child", {
        elapsedSeconds,
        kind: diagnostics.errorKind,
      });
      return;
    }

    const transcriptTail = await getChildTranscriptTail(childSessionID);
    await emitParentCallback(
      state.ref.parentSessionID,
      buildAsyncCallback({
        status: "completed",
        taskID: childSessionID,
        subagentType: state.ref.subagentType,
        timeoutSeconds: state.ref.timeoutSeconds,
        transcriptTail,
        elapsedSeconds,
        observedToolCalls: state.seenToolPartIDs.size,
        sessionSummary,
        fallbackModels,
      }),
      true,
    ).catch(async (error) => {
      await log("warn", "Failed to emit async completed callback", {
        parentSessionID: state.ref.parentSessionID,
        childSessionID,
        error: stringifyUnknown(error),
      });
    });
    clearAsyncPhase1State(childSessionID, "phase1.terminal.completed", {
      elapsedSeconds,
      transcriptTailPresent: Boolean(transcriptTail),
    });
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
    event: async ({ event }) => {
      const eventType = event.type as string;
      const properties =
        typeof event.properties === "object" && event.properties
          ? (event.properties as Record<string, unknown>)
          : {};

      if (eventType === "message.part.updated") {
        const part =
          typeof properties.part === "object" && properties.part
            ? (properties.part as Record<string, unknown>)
            : undefined;

        if (
          part &&
          part.type === "tool" &&
          part.tool === "task" &&
          typeof part.callID === "string" &&
          typeof part.sessionID === "string" &&
          typeof part.messageID === "string"
        ) {
          const key = parentTaskCallKey({
            parentSessionID: part.sessionID,
            parentMessageID: part.messageID,
            parentCallID: part.callID,
          });
          const ref = parentTaskRefsByCallKey.get(key);
          if (ref) {
            await rehydrateParentTaskPart({ part, ref }).catch(async (error) => {
              await log("warn", "Failed to rehydrate parent task part metadata", {
                parentSessionID: ref.parentSessionID,
                parentMessageID: ref.parentMessageID,
                parentCallID: ref.parentCallID,
                childSessionID: ref.childSessionID,
                mode: ref.mode,
                error: stringifyUnknown(error),
              });
            });
            const partState =
              typeof part.state === "object" && part.state
                ? (part.state as Record<string, unknown>)
                : undefined;
            const status =
              partState && typeof partState.status === "string"
                ? partState.status
                : undefined;
            if (status === "completed" || status === "error") {
              parentTaskRefsByCallKey.delete(key);
            }
          }
        }

        const partSessionID =
          part && typeof part.sessionID === "string" ? part.sessionID : undefined;
        if (
          part &&
          partSessionID &&
          asyncPhase1States.has(partSessionID) &&
          part.type === "tool" &&
          typeof part.id === "string"
        ) {
          const state = asyncPhase1States.get(partSessionID);
          if (state) state.seenToolPartIDs.add(part.id);
        }
      }

      if (!ASYNC_TRACE_ENABLED) return;
      const sessionID = extractEventSessionID(event);
      if (!isTrackedTraceSession(sessionID)) return;
      const relatedChildren = childSessionsForEvent(sessionID);
      for (const childSessionID of relatedChildren) {
        bumpAsyncTraceCounter(childSessionID, eventType);
      }

      trace("async.event", {
        eventType,
        sessionID,
        relatedChildren,
        properties:
          eventType === "message.part.delta"
            ? {
                sessionID: properties.sessionID,
                messageID: properties.messageID,
                partID: properties.partID,
                field: properties.field,
                deltaChars:
                  typeof properties.delta === "string"
                    ? properties.delta.length
                    : undefined,
              }
            : properties,
      });
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
          const resolvedModelSpec = overrideModelSpec ?? subagent?.model;

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

          const contextWithCallID = context as ToolContextWithCallID;
          const parentCallID =
            typeof contextWithCallID.callID === "string"
              ? contextWithCallID.callID
              : "";
          const parentTaskRef =
            parentCallID.length > 0
              ? ({
                  parentSessionID: sessionID,
                  parentMessageID: context.messageID,
                  parentCallID,
                  childSessionID,
                  mode,
                  subagentType: args.subagent_type,
                  description: args.description,
                  timeoutSeconds,
                  ...(resolvedModelSpec ? { model: resolvedModelSpec } : {}),
                } satisfies ParentTaskRef)
              : undefined;
          if (parentTaskRef) {
            parentTaskRefsByCallKey.set(
              parentTaskCallKey(parentTaskRef),
              parentTaskRef,
            );
          }

          context.metadata({
            title: args.description,
            metadata: {
              sessionId: childSessionID,
              mode,
              subagentType: args.subagent_type,
              timeoutSeconds,
              ...(resolvedModelSpec ? { model: resolvedModelSpec } : {}),
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
            const traceRef: ParentTaskRef = {
              parentSessionID: sessionID,
              parentMessageID: context.messageID,
              parentCallID,
              childSessionID,
              mode: "async",
              subagentType: args.subagent_type,
              description: args.description,
              timeoutSeconds,
              ...(resolvedModelSpec ? { model: resolvedModelSpec } : {}),
            };
            asyncTraceRefs.set(childSessionID, traceRef);
            initAsyncTraceCounters(childSessionID);

            trace("async.trace.bind.native", {
              parentSessionID: sessionID,
              parentMessageID: context.messageID,
              parentCallID:
                typeof contextWithCallID.callID === "string"
                  ? contextWithCallID.callID
                  : undefined,
              childSessionID,
              subagentType: args.subagent_type,
              timeoutSeconds,
              resumed: Boolean(args.task_id),
              launchStrategy: ASYNC_LAUNCH_STRATEGY,
            });
            trace("async.launch.native.dispatch", {
              childSessionID,
              subagentType: args.subagent_type,
              timeoutSeconds,
              launchStrategy: ASYNC_LAUNCH_STRATEGY,
            });
            await log("info", "Async task launch (phase1-native) started", {
              parentSessionID: sessionID,
              childSessionID,
              subagentType: args.subagent_type,
              timeoutSeconds,
              launchStrategy: ASYNC_LAUNCH_STRATEGY,
            });

            const startedAtMs = Date.now();
            const heartbeatTimer = setInterval(() => {
              void emitAsyncHeartbeat(childSessionID);
            }, ASYNC_HEARTBEAT_INTERVAL_MS);
            const timeoutTimer = setTimeout(() => {
              trace("async.phase1.timeout.fire", {
                parentSessionID: sessionID,
                childSessionID,
                subagentType: args.subagent_type,
                timeoutSeconds,
              });
              void client.session
                .abort({ path: { id: childSessionID } })
                .catch(() => {});
              void emitAsyncTerminalCallback(
                childSessionID,
                new TimeoutError("async phase1 launch", timeoutSeconds * 1000),
              );
            }, timeoutSeconds * 1000);

            asyncPhase1States.set(childSessionID, {
              ref: traceRef,
              startedAtMs,
              heartbeatTimer,
              timeoutTimer,
              seenToolPartIDs: new Set<string>(),
              terminalEmitted: false,
            });

            void client.session
              .prompt({
                path: { id: childSessionID },
                body: promptBody as Parameters<typeof client.session.prompt>[0]["body"],
              })
              .then(async ({ error }) => {
                if (error) {
                  const details = extractErrorDetails(error);
                  trace("async.launch.native.error", {
                    childSessionID,
                    subagentType: args.subagent_type,
                    errorName: details.name,
                    errorMessage: details.message,
                  });
                  await log("error", "Async task launch (phase1-native) failed", {
                    parentSessionID: sessionID,
                    childSessionID,
                    subagentType: args.subagent_type,
                    errorName: details.name,
                    errorMessage: details.message,
                  });
                  await emitAsyncTerminalCallback(childSessionID, error);
                  return;
                }

                trace("async.launch.native.completed", {
                  childSessionID,
                  subagentType: args.subagent_type,
                });
                await log("info", "Async task completed (phase1-native)", {
                  parentSessionID: sessionID,
                  childSessionID,
                  subagentType: args.subagent_type,
                });
                await emitAsyncTerminalCallback(childSessionID);
              })
              .catch(async (error) => {
                const details = extractErrorDetails(error);
                trace("async.launch.native.threw", {
                  childSessionID,
                  subagentType: args.subagent_type,
                  errorName: details.name,
                  errorMessage: details.message,
                });
                await log("error", "Async task launch (phase1-native) threw", {
                  parentSessionID: sessionID,
                  childSessionID,
                  subagentType: args.subagent_type,
                  errorName: details.name,
                  errorMessage: details.message,
                });
                await emitAsyncTerminalCallback(childSessionID, error);
              });

            return [
              "task_mode: async",
              "task_status: running",
              `task_id: ${childSessionID}`,
              `subagent_type: ${args.subagent_type}`,
              `timeout_seconds: ${timeoutSeconds}`,
              "callback_mode: heartbeat_and_terminal_via_parent_callbacks",
              "ui_visibility: child session progress/events flow through native session tree.",
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
          const sessionSummary = await collectChildSessionSummary(childSessionID);

          return [
            "task_mode: sync",
            "task_status: completed",
            `task_id: ${childSessionID}`,
            `subagent_type: ${args.subagent_type}`,
            `timeout_seconds: ${timeoutSeconds}`,
            `<task_result>`,
            truncateText(text, MAX_RESULT_CHARS),
            `</task_result>`,
            sessionSummary
              ? formatTaskSessionSummary(sessionSummary)
              : "task_session_summary: unavailable",
          ].join("\n");
        },
      }),
    },
  };
};
