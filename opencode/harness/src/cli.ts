#!/usr/bin/env bun
import { createOpencodeClient } from "@opencode-ai/sdk";
import { spawn } from "child_process";

const REQUEST_TIMEOUT_MS = 180000;
let RESOLVED_BASE_URL = "http://127.0.0.1:4096";
let AUTH_HEADER = "";

type KV = Record<string, string | boolean>;

type KnownLimitPattern = {
  providerID: string;
  modelID: string;
  match_regex: string;
  normalized_kind: "rate_limit";
  example_expected_substring: string;
};

function parseArgs(argv: string[]): { command: string; args: KV } {
  const [command = "help", ...rest] = argv;
  const args: KV = {};
  for (let i = 0; i < rest.length; i++) {
    const token = rest[i];
    if (!token.startsWith("--")) continue;
    const key = token.slice(2);
    const next = rest[i + 1];
    if (!next || next.startsWith("--")) {
      args[key] = true;
    } else {
      args[key] = next;
      i++;
    }
  }
  return { command, args };
}

function getString(args: KV, key: string, fallback = ""): string {
  const value = args[key];
  if (typeof value === "string") return value;
  return fallback;
}

function hasFlag(args: KV, key: string): boolean {
  return args[key] === true;
}

function parseModel(
  model?: string,
): { providerID: string; modelID: string } | undefined {
  if (!model) return undefined;
  const [providerID, ...rest] = model.split("/");
  if (!providerID || rest.length === 0) return undefined;
  return { providerID, modelID: rest.join("/") };
}

function flattenText(parts: Array<any>): string {
  return (parts ?? [])
    .filter((p) => p.type === "text")
    .map((p) => p.text ?? "")
    .join("")
    .trim();
}

function renderTranscript(messages: Array<any>, tailLines: number): string {
  const lines: string[] = [];
  for (const msg of messages) {
    const role = (msg.info?.role ?? "unknown").toUpperCase();
    const text = flattenText(msg.parts ?? []);
    if (!text) continue;
    lines.push(`[${role}]`);
    lines.push(text);
    lines.push("---");
  }
  return lines.slice(-tailLines).join("\n");
}

function renderAssistantText(messages: Array<any>): string {
  const lines: string[] = [];
  for (const msg of messages) {
    if (msg.info?.role !== "assistant") continue;
    const text = flattenText(msg.parts ?? []);
    if (!text) continue;
    lines.push(text);
  }
  return lines.join("\n");
}

function classifyError(err: any): string {
  const blob = JSON.stringify(err ?? {}).toLowerCase();
  if (
    blob.includes("rate limit") ||
    blob.includes("too many requests") ||
    blob.includes("429")
  )
    return "rate_limit";
  if (
    blob.includes("usage limit") ||
    blob.includes("quota") ||
    blob.includes("credit") ||
    blob.includes("subscription")
  )
    return "quota";
  if (
    blob.includes("forbidden") ||
    blob.includes("permission_denied") ||
    blob.includes("permission")
  )
    return "permission";
  if (blob.includes("aborted")) return "aborted";
  return "other";
}

function summarizeError(err: any): string {
  if (!err) return "";
  if (typeof err.message === "string") return err.message;
  if (typeof err?.data?.message === "string") return err.data.message;
  const txt = JSON.stringify(err);
  return txt.length > 300 ? `${txt.slice(0, 300)}...` : txt;
}

function normalizeErrorRecord(source: string, sessionID: string, info: any) {
  const errorObj = info?.error;
  return {
    source,
    sessionID,
    messageID: info?.id,
    providerID: info?.providerID,
    modelID: info?.modelID,
    agent: info?.agent,
    mode: info?.mode,
    kind: classifyError(errorObj?.data ?? errorObj),
    summary: summarizeError(errorObj?.data ?? errorObj),
    error: errorObj,
  };
}

async function readServiceLogLines(
  sessionID: string,
  sinceSec: number,
): Promise<string[]> {
  const cmd = `export XDG_RUNTIME_DIR=\"/run/user/$(id -u)\" DBUS_SESSION_BUS_ADDRESS=\"unix:path=/run/user/$(id -u)/bus\"; journalctl --user -u opencode-serve --since \"${sinceSec} seconds ago\" --no-pager -o cat`;
  return await new Promise<string[]>((resolve) => {
    const child = spawn("bash", ["-lc", cmd], {
      cwd: process.cwd(),
      env: process.env,
    });
    let out = "";
    child.stdout.on("data", (d) => {
      out += d.toString();
    });
    child.stderr.on("data", (d) => {
      out += d.toString();
    });
    child.on("close", () => {
      const lines = out
        .split("\n")
        .filter((line) => line.includes(sessionID))
        .filter((line) => {
          const s = line.toLowerCase();
          return (
            s.includes("service=session.processor") ||
            s.includes("service=llm") ||
            s.includes("ai_apicallerror") ||
            s.includes("rate limit") ||
            s.includes("usage limit") ||
            s.includes("quota") ||
            s.includes("subscription") ||
            s.includes("429")
          );
        });
      resolve(lines);
    });
    child.on("error", () => resolve([]));
  });
}

async function loadKnownLimitPatterns(): Promise<
  Record<string, KnownLimitPattern>
> {
  const configPath = `${import.meta.dir}/../config/known_limit_patterns.json`;
  const text = await Bun.file(configPath).text();
  return JSON.parse(text) as Record<string, KnownLimitPattern>;
}

async function runOneShotWithLogs(
  model: string,
  prompt: string,
  timeoutSec: number,
): Promise<string> {
  return await new Promise<string>((resolve, reject) => {
    const inner = `opencode run --print-logs --log-level DEBUG -m ${JSON.stringify(model)} ${JSON.stringify(prompt)}`;
    const shellCmd = `script -qec ${JSON.stringify(inner)} /dev/null`;
    const child = spawn("bash", ["-lc", shellCmd], {
      cwd: process.cwd(),
      env: process.env,
    });
    let out = "";
    const timer = setTimeout(() => {
      child.kill("SIGTERM");
    }, timeoutSec * 1000);
    child.stdout.on("data", (d) => {
      out += d.toString();
    });
    child.stderr.on("data", (d) => {
      out += d.toString();
    });
    child.on("error", (err) => {
      clearTimeout(timer);
      reject(err);
    });
    child.on("close", () => {
      clearTimeout(timer);
      resolve(out);
    });
  });
}

function extractKnownLimitEvent(
  raw: string,
  pattern: KnownLimitPattern,
): { matchedLine: string; evidence: string[] } | null {
  const lines = raw.split(/\r\n|\n|\r/g);
  const rx = new RegExp(pattern.match_regex, "i");
  let matchedLine = "";
  for (const line of lines) {
    if (rx.test(line)) {
      matchedLine = line.trim();
      break;
    }
  }
  if (!matchedLine) return null;

  const evidence = lines
    .filter((line) => {
      const s = line.toLowerCase();
      return (
        s.includes(`providerid=${pattern.providerID.toLowerCase()}`) ||
        s.includes(`modelid=${pattern.modelID.toLowerCase()}`) ||
        rx.test(line)
      );
    })
    .map((line) => compactLogLine(line.trim()))
    .filter((line) => {
      if (!line) return false;
      const s = line.toLowerCase();
      return (
        s.includes("service=") ||
        s.includes("providerid=") ||
        s.includes("modelid=") ||
        s.includes("ai_apicallerror") ||
        s.includes("rate limit") ||
        s.includes("status=")
      );
    })
    .slice(-6);

  return {
    matchedLine: compactLogLine(matchedLine),
    evidence,
  };
}

function compactLogLine(line: string, maxLen = 320): string {
  const normalized = line
    .replace(/\x1b\[[0-9;]*m/g, "")
    .replace(/error=\{.*$/i, "error=<omitted>")
    .replace(/responseBody=\".*$/i, 'responseBody="<omitted>')
    .replace(/requestBodyValues=\{.*$/i, "requestBodyValues=<omitted>");
  if (normalized.length <= maxLen) return normalized;
  return `${normalized.slice(0, maxLen - 3)}...`;
}

function makeClient() {
  let baseUrl = process.env.OPENCODE_BASE_URL ?? "http://127.0.0.1:4096";
  const username = process.env.OPENCODE_SERVER_USERNAME ?? "opencode";
  const password = process.env.OPENCODE_SERVER_PASSWORD ?? "";

  RESOLVED_BASE_URL = baseUrl;
  AUTH_HEADER = "";

  if (password) {
    const token = Buffer.from(`${username}:${password}`).toString("base64");
    AUTH_HEADER = `Basic ${token}`;
  }

  return createOpencodeClient({ baseUrl });
}

async function promptAsyncRequest(
  sessionID: string,
  body: Record<string, unknown>,
) {
  const headers: Record<string, string> = {
    "content-type": "application/json",
  };
  if (AUTH_HEADER) headers.authorization = AUTH_HEADER;

  const res = await fetch(
    `${RESOLVED_BASE_URL}/session/${encodeURIComponent(sessionID)}/prompt_async`,
    {
      method: "POST",
      headers,
      body: JSON.stringify(body),
    },
  );

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`prompt_async failed (${res.status}): ${text}`);
  }
}

async function cmdHealth(client: any) {
  const pathInfo = await client.path.get({});
  const project = await client.project.current({});
  console.log(
    JSON.stringify(
      { ok: true, path: pathInfo.data, project: project.data },
      null,
      2,
    ),
  );
}

async function cmdList(client: any) {
  const result = await client.session.list({});
  for (const s of result.data ?? []) {
    console.log(`${s.id}\t${s.title ?? ""}\t${s.time?.updated ?? ""}`);
  }
}

async function cmdNew(client: any, args: KV) {
  const title = getString(args, "title") || `opx:${Date.now()}`;
  const created = await client.session.create({ body: { title } });
  const sessionID = created.data?.id;
  if (!sessionID) throw new Error("Failed to create session");

  const prompt = getString(args, "prompt");
  const agent = getString(args, "agent");
  const model = parseModel(getString(args, "model"));
  const asyncMode = hasFlag(args, "async");

  if (prompt) {
    if (asyncMode) {
      await promptAsyncRequest(sessionID, {
        agent: agent || undefined,
        model,
        parts: [{ type: "text", text: prompt }],
      });
    } else {
      await client.session.prompt({
        timeout: REQUEST_TIMEOUT_MS,
        path: { id: sessionID },
        body: {
          agent: agent || undefined,
          model,
          parts: [{ type: "text", text: prompt }],
        },
      });
    }
  }

  console.log(sessionID);
}

async function cmdSend(client: any, args: KV) {
  const session = getString(args, "session");
  const prompt = getString(args, "prompt");
  if (!session || !prompt) {
    throw new Error("send requires --session and --prompt");
  }

  const agent = getString(args, "agent");
  const model = parseModel(getString(args, "model"));
  const asyncMode = hasFlag(args, "async");
  const noReply = hasFlag(args, "no-reply");

  if (asyncMode) {
    await promptAsyncRequest(session, {
      agent: agent || undefined,
      model,
      noReply,
      parts: [{ type: "text", text: prompt }],
    });
    console.log(session);
    return;
  }

  const res = await client.session.prompt({
    timeout: REQUEST_TIMEOUT_MS,
    path: { id: session },
    body: {
      agent: agent || undefined,
      model,
      noReply,
      parts: [{ type: "text", text: prompt }],
    },
  });

  console.log(flattenText(res.data?.parts ?? []) || session);
}

async function cmdMessages(client: any, args: KV) {
  const session = getString(args, "session");
  if (!session) throw new Error("messages requires --session");
  const result = await client.session.messages({ path: { id: session } });
  console.log(JSON.stringify(result.data ?? [], null, 2));
}

async function cmdTail(client: any, args: KV) {
  const session = getString(args, "session");
  if (!session) throw new Error("tail requires --session");
  const lines = Number(getString(args, "lines", "30"));
  const result = await client.session.messages({ path: { id: session } });
  console.log(renderTranscript(result.data ?? [], lines));
}

async function cmdErrors(client: any, args: KV) {
  const session = getString(args, "session");
  if (!session) throw new Error("errors requires --session");
  const result = await client.session.messages({ path: { id: session } });
  const rows = (result.data ?? [])
    .filter((m: any) => m.info?.role === "assistant" && m.info?.error)
    .map((m: any) => ({
      messageID: m.info?.id,
      created: m.info?.time?.created,
      completed: m.info?.time?.completed,
      providerID: m.info?.providerID,
      modelID: m.info?.modelID,
      mode: m.info?.mode,
      agent: m.info?.agent,
      errorName: m.info?.error?.name,
      errorData: m.info?.error?.data,
      text: flattenText(m.parts ?? []),
    }));

  console.log(JSON.stringify(rows, null, 2));
}

async function cmdLimitErrors(client: any, args: KV) {
  const session = getString(args, "session");
  if (!session) throw new Error("limit-errors requires --session");
  const verbose = hasFlag(args, "verbose");
  const result = await client.session.messages({ path: { id: session } });
  const all = (result.data ?? [])
    .filter((m: any) => m.info?.role === "assistant" && m.info?.error)
    .map((m: any) => ({
      sessionID: session,
      messageID: m.info?.id,
      created: m.info?.time?.created,
      providerID: m.info?.providerID,
      modelID: m.info?.modelID,
      agent: m.info?.agent,
      kind: classifyError(m.info?.error),
      summary: summarizeError(m.info?.error?.data ?? m.info?.error),
      error: m.info?.error,
    }));

  const filtered = all.filter((x: any) => x.kind !== "aborted");
  const out = (filtered.length ? filtered : all).map((x: any) =>
    verbose
      ? x
      : {
          sessionID: x.sessionID,
          messageID: x.messageID,
          providerID: x.providerID,
          modelID: x.modelID,
          kind: x.kind,
          summary: x.summary,
        },
  );
  console.log(JSON.stringify(out, null, 2));
}

async function cmdProbeLimit(client: any, args: KV) {
  const modelStr = getString(args, "model");
  if (!modelStr) throw new Error("probe-limit requires --model provider/model");
  const model = parseModel(modelStr);
  if (!model) throw new Error("Invalid --model format");

  const created = await client.session.create({
    body: { title: `opx-probe-limit:${modelStr}:${Date.now()}` },
  });
  const sessionID = created.data?.id;
  if (!sessionID) throw new Error("Failed to create probe session");

  await promptAsyncRequest(sessionID, {
    agent: getString(args, "agent", "Minimal"),
    model,
    parts: [
      {
        type: "text",
        text: getString(args, "prompt", "Reply with ONLY OK."),
      },
    ],
  });

  console.log(sessionID);
}

async function cmdProbeLimitKnown(args: KV) {
  const providerKey = getString(args, "provider");
  if (!providerKey) {
    throw new Error(
      "probe-limit-known requires --provider anthropic|opencode-minimax|opencode-big-pickle",
    );
  }

  const patterns = await loadKnownLimitPatterns();
  const pattern = patterns[providerKey];
  if (!pattern) {
    throw new Error(
      `Unknown provider key '${providerKey}'. Expected one of: ${Object.keys(patterns).join(", ")}`,
    );
  }

  const timeoutSec = Number(getString(args, "timeout", "60"));
  const prompt = getString(args, "prompt", "Reply with ONLY OK.");
  const model = `${pattern.providerID}/${pattern.modelID}`;
  const raw = await runOneShotWithLogs(model, prompt, timeoutSec);
  const match = extractKnownLimitEvent(raw, pattern);

  if (!match) {
    const hintLines = raw
      .split("\n")
      .filter((line) => {
        const s = line.toLowerCase();
        return (
          s.includes(`providerid=${pattern.providerID.toLowerCase()}`) ||
          s.includes(`modelid=${pattern.modelID.toLowerCase()}`) ||
          s.includes("service=session.processor")
        );
      })
      .slice(-12);

    console.log(
      JSON.stringify(
        {
          ok: false,
          available: false,
          code: "KNOWN_PATTERN_NOT_FOUND",
          providerKey,
          providerID: pattern.providerID,
          modelID: pattern.modelID,
          expectedPattern: pattern.match_regex,
          tail: hintLines,
        },
        null,
        2,
      ),
    );
    process.exitCode = 2;
    return;
  }

  console.log(
    JSON.stringify(
      {
        ok: true,
        available: false,
        providerKey,
        providerID: pattern.providerID,
        modelID: pattern.modelID,
        kind: pattern.normalized_kind,
        matched: match.matchedLine,
        evidence: match.evidence,
      },
      null,
      2,
    ),
  );
  process.exitCode = 2;
}

async function cmdProbeLimitTrace(client: any, args: KV) {
  const modelStr = getString(args, "model");
  if (!modelStr)
    throw new Error("probe-limit-trace requires --model provider/model");
  const model = parseModel(modelStr);
  if (!model) throw new Error("Invalid --model format");

  const timeoutSec = Number(getString(args, "timeout", "60"));
  const verbose = hasFlag(args, "verbose");
  const includeAborted = hasFlag(args, "include-aborted");

  const created = await client.session.create({
    body: { title: `opx-probe-limit-trace:${modelStr}:${Date.now()}` },
  });
  const sessionID = created.data?.id;
  if (!sessionID) throw new Error("Failed to create probe session");

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutSec * 1000);
  const stream = await client.event.subscribe({
    signal: controller.signal,
    query: { directory: process.cwd() },
  });

  const rows: any[] = [];
  const collector = (async () => {
    try {
      for await (const evt of stream.stream as AsyncGenerator<any>) {
        if (!evt || typeof evt !== "object") continue;

        if (evt.type === "message.updated") {
          const info = evt.properties?.info;
          if (
            !info ||
            info.sessionID !== sessionID ||
            info.role !== "assistant"
          )
            continue;
          if (info.error)
            rows.push(normalizeErrorRecord("message.updated", sessionID, info));
          continue;
        }

        if (evt.type === "session.error") {
          const sid = evt.properties?.sessionID;
          if (sid !== sessionID) continue;
          rows.push(
            normalizeErrorRecord("session.error", sessionID, {
              error: evt.properties?.error,
            }),
          );
        }
      }
    } catch {
      // timeout/abort closes stream
    }
  })();

  await promptAsyncRequest(sessionID, {
    agent: getString(args, "agent", "Minimal"),
    model,
    parts: [
      {
        type: "text",
        text: getString(args, "prompt", "Reply with ONLY OK."),
      },
    ],
  });

  await collector;
  clearTimeout(timer);

  const filtered = includeAborted
    ? rows
    : rows.filter((r) => r.kind !== "aborted");
  const outputRows = (filtered.length ? filtered : rows).map((r) =>
    verbose
      ? r
      : {
          source: r.source,
          sessionID: r.sessionID,
          providerID: r.providerID,
          modelID: r.modelID,
          kind: r.kind,
          summary: r.summary,
        },
  );

  console.log(
    JSON.stringify(
      {
        sessionID,
        model: modelStr,
        timeoutSec,
        matched: outputRows.length,
        rows: outputRows,
      },
      null,
      2,
    ),
  );
}

async function cmdTrace(client: any, args: KV) {
  const session = getString(args, "session");
  if (!session) throw new Error("trace requires --session");
  const timeoutSec = Number(getString(args, "timeout", "60"));
  const verbose = hasFlag(args, "verbose");
  const includeAborted = hasFlag(args, "include-aborted");
  const withServiceLog = !hasFlag(args, "no-service-log");

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutSec * 1000);

  const stream = await client.event.subscribe({
    signal: controller.signal,
    query: { directory: process.cwd() },
  });

  const rows: any[] = [];
  const existing = await client.session.messages({ path: { id: session } });
  for (const msg of existing.data ?? []) {
    if (msg.info?.role !== "assistant" || !msg.info?.error) continue;
    rows.push(normalizeErrorRecord("message.history", session, msg.info));
  }
  try {
    for await (const evt of stream.stream as AsyncGenerator<any>) {
      if (!evt || typeof evt !== "object") continue;

      if (evt.type === "message.updated") {
        const info = evt.properties?.info;
        if (!info || info.sessionID !== session || info.role !== "assistant")
          continue;
        if (!info.error) continue;
        rows.push(normalizeErrorRecord("message.updated", session, info));
        continue;
      }

      if (evt.type === "session.error") {
        const sid = evt.properties?.sessionID;
        if (sid !== session) continue;
        rows.push(
          normalizeErrorRecord("session.error", session, {
            error: evt.properties?.error,
          }),
        );
      }
    }
  } catch {
    // timeout/abort closes stream
  } finally {
    clearTimeout(timer);
  }

  const filtered = includeAborted
    ? rows
    : rows.filter((r) => r.kind !== "aborted");
  let outputRows = (filtered.length ? filtered : rows).map((r) =>
    verbose
      ? r
      : {
          source: r.source,
          sessionID: r.sessionID,
          providerID: r.providerID,
          modelID: r.modelID,
          kind: r.kind,
          summary: r.summary,
        },
  );

  if (withServiceLog) {
    const logLines = await readServiceLogLines(
      session,
      Math.max(timeoutSec + 30, 60),
    );
    const logRows = logLines.map((line) => {
      const kind = classifyError(line);
      return verbose
        ? { source: "service.log", sessionID: session, kind, line }
        : {
            source: "service.log",
            sessionID: session,
            kind,
            summary: line.length > 280 ? `${line.slice(0, 280)}...` : line,
          };
    });
    outputRows = [...outputRows, ...logRows];
  }

  console.log(
    JSON.stringify(
      {
        sessionID: session,
        timeoutSec,
        matched: outputRows.length,
        rows: outputRows,
      },
      null,
      2,
    ),
  );
}

async function cmdStatus(client: any) {
  const sessions = await client.session.list({});
  const out = (sessions.data ?? []).map((s: any) => ({
    id: s.id,
    title: s.title,
    updated: s.time?.updated,
  }));
  console.log(JSON.stringify(out, null, 2));
}

async function cmdWait(client: any, args: KV) {
  const session = getString(args, "session");
  if (!session) throw new Error("wait requires --session");
  const contains = getString(args, "contains");
  const timeout = Number(getString(args, "timeout", "120"));

  const start = Date.now();
  let stableCount = 0;
  let previousLength = -1;

  while ((Date.now() - start) / 1000 < timeout) {
    const messages =
      (
        await client.session.messages({
          timeout: REQUEST_TIMEOUT_MS,
          path: { id: session },
        })
      ).data ?? [];
    const assistantText = renderAssistantText(messages);

    if (contains && assistantText.includes(contains)) {
      console.log(`matched:${contains}`);
      return;
    }

    if (!contains) {
      if (messages.length === previousLength) {
        stableCount += 1;
      } else {
        stableCount = 0;
      }
      previousLength = messages.length;

      if (stableCount >= 3) {
        console.log("idle");
        return;
      }
    }

    await new Promise((r) => setTimeout(r, 1000));
  }

  console.log("timeout");
}

async function cmdDelete(client: any, args: KV) {
  const session = getString(args, "session");
  if (!session) throw new Error("delete requires --session");
  await client.session.delete({ path: { id: session } });
  console.log(session);
}

async function cmdAbort(client: any, args: KV) {
  const session = getString(args, "session");
  if (!session) throw new Error("abort requires --session");
  await client.session.abort({ path: { id: session } });
  console.log(session);
}

async function cmdProbeAsyncCommand(client: any, args: KV) {
  const modelStr = getString(args, "model", "opencode/big-pickle");
  const model = parseModel(modelStr);
  if (!model) throw new Error("Invalid --model format");

  const created = await client.session.create({
    body: { title: `opx-probe-async-command:${Date.now()}` },
  });
  const sessionID = created.data?.id;
  if (!sessionID) throw new Error("Failed to create probe session");

  await client.session.prompt({
    timeout: REQUEST_TIMEOUT_MS,
    path: { id: sessionID },
    body: {
      agent: getString(args, "agent", "Minimal"),
      model,
      parts: [
        {
          type: "text",
          text: [
            "Call async_command with seconds=4 and message=PROBE_PING.",
            "When callback arrives, reply with EXACTLY: PROBE_CALLBACK_CONTINUED.",
          ].join(" "),
        },
      ],
    },
  });

  const start = Date.now();
  while (Date.now() - start < 180000) {
    const messages = await client.session.messages({
      timeout: REQUEST_TIMEOUT_MS,
      path: { id: sessionID },
    });
    const tx = renderAssistantText(messages.data ?? []);
    if (tx.includes("PROBE_CALLBACK_CONTINUED")) {
      console.log(JSON.stringify({ ok: true, sessionID }, null, 2));
      return;
    }
    await new Promise((r) => setTimeout(r, 1000));
  }

  console.log(
    JSON.stringify({ ok: false, sessionID, reason: "timeout" }, null, 2),
  );
}

async function cmdProbeAsyncSubagent(client: any, args: KV) {
  const modelStr = getString(args, "model", "opencode/big-pickle");
  const model = parseModel(modelStr);
  if (!model) throw new Error("Invalid --model format");

  const created = await client.session.create({
    body: { title: `opx-probe-async-subagent:${Date.now()}` },
  });
  const sessionID = created.data?.id;
  if (!sessionID) throw new Error("Failed to create probe session");

  await client.session.prompt({
    timeout: REQUEST_TIMEOUT_MS,
    path: { id: sessionID },
    body: {
      agent: getString(args, "agent", "Minimal"),
      model,
      parts: [
        {
          type: "text",
          text: [
            "Call async_subagent with agent Minimal, model opencode/big-pickle, and prompt: Reply with only READY.",
            "When callback arrives, reply with EXACTLY: PROBE_SUBAGENT_CONTINUED.",
          ].join(" "),
        },
      ],
    },
  });

  const start = Date.now();
  while (Date.now() - start < 180000) {
    const messages = await client.session.messages({
      timeout: REQUEST_TIMEOUT_MS,
      path: { id: sessionID },
    });
    const tx = renderAssistantText(messages.data ?? []);
    if (tx.includes("PROBE_SUBAGENT_CONTINUED")) {
      console.log(JSON.stringify({ ok: true, sessionID }, null, 2));
      return;
    }
    await new Promise((r) => setTimeout(r, 1000));
  }

  console.log(
    JSON.stringify({ ok: false, sessionID, reason: "timeout" }, null, 2),
  );
}

function help() {
  const text = [
    "opx commands:",
    "  health",
    "  list",
    "  new --title <title> [--prompt <text>] [--agent <agent>] [--model provider/model] [--async]",
    "  send --session <id> --prompt <text> [--agent <agent>] [--model provider/model] [--async] [--no-reply]",
    "  messages --session <id>",
    "  tail --session <id> [--lines <n>]",
    "  errors --session <id>",
    "  limit-errors --session <id> [--verbose]",
    "  status",
    "  wait --session <id> [--contains <text>] [--timeout <sec>]",
    "  abort --session <id>",
    "  delete --session <id>",
    "  probe-async-command [--model provider/model] [--agent <agent>]",
    "  probe-async-subagent [--model provider/model] [--agent <agent>]",
    "  probe-limit --model provider/model [--agent <agent>] [--prompt <text>]",
    "  probe-limit-known --provider anthropic|opencode-minimax|opencode-big-pickle [--timeout <sec>] [--prompt <text>]",
    "  probe-limit-trace --model provider/model [--agent <agent>] [--prompt <text>] [--timeout <sec>] [--verbose] [--include-aborted]",
    "  trace --session <id> [--timeout <sec>] [--verbose] [--include-aborted] [--no-service-log]",
    "",
    "env:",
    "  OPENCODE_BASE_URL (default http://127.0.0.1:4096)",
    "  OPENCODE_SERVER_USERNAME (default opencode)",
    "  OPENCODE_SERVER_PASSWORD (optional)",
  ];
  console.log(text.join("\n"));
}

async function main() {
  const { command, args } = parseArgs(process.argv.slice(2));
  const client = makeClient();

  switch (command) {
    case "health":
      await cmdHealth(client);
      break;
    case "list":
      await cmdList(client);
      break;
    case "new":
      await cmdNew(client, args);
      break;
    case "send":
      await cmdSend(client, args);
      break;
    case "messages":
      await cmdMessages(client, args);
      break;
    case "tail":
      await cmdTail(client, args);
      break;
    case "errors":
      await cmdErrors(client, args);
      break;
    case "limit-errors":
      await cmdLimitErrors(client, args);
      break;
    case "status":
      await cmdStatus(client);
      break;
    case "wait":
      await cmdWait(client, args);
      break;
    case "abort":
      await cmdAbort(client, args);
      break;
    case "delete":
      await cmdDelete(client, args);
      break;
    case "probe-async-command":
      await cmdProbeAsyncCommand(client, args);
      break;
    case "probe-async-subagent":
      await cmdProbeAsyncSubagent(client, args);
      break;
    case "probe-limit":
      await cmdProbeLimit(client, args);
      break;
    case "probe-limit-known":
      await cmdProbeLimitKnown(args);
      break;
    case "probe-limit-trace":
      await cmdProbeLimitTrace(client, args);
      break;
    case "trace":
      await cmdTrace(client, args);
      break;
    default:
      help();
  }
}

main().catch((err) => {
  console.error(err instanceof Error ? err.message : String(err));
  process.exit(1);
});
