// =============================================================================
// RETIRED: async_subagent plugin
// =============================================================================
//
// Status: RETIRED (moved to plugins/dev/retired/)
// Replaced by: improved-task plugin
//
// Migration:
//   - OLD: async_subagent tool (this plugin)
//   - NEW: task tool from improved-task plugin
//
// The improved-task plugin (file:///home/dzack/opencode-plugins/improved-task/src/index.ts)
// supersedes this implementation with the following advantages:
//
//   1. Sync + Async modes
//      - OLD: async-only (fire-and-forget)
//      - NEW: sync (blocking) by default, explicit mode: "async" for background
//
//   2. Structured output
//      - OLD: plain text status messages
//      - NEW: JSON-like summary with status, session_id, transcript_path,
//            completion_confidence_score, num_tool_calls, duration_ms
//
//   3. Transcript tracking
//      - OLD: manual transcript tail via external parser script
//      - NEW: automatic transcript saved to temp file, path returned in output
//
//   4. Resume capability
//      - OLD: no resume support
//      - NEW: can resume task later with session_id parameter
//
//   5. Timeout handling
//      - OLD: simple timeout with error message
//      - NEW: configurable timeout with structured error reporting and
//            follow-up instructions
//
//   6. Plugin architecture
//      - OLD: standalone tool
//      - NEW: proper upstream plugin with lifecycle management
//
// Migration example:
//   OLD: async_subagent { agent: "Reviewer: Code", prompt: "...", time_estimate: 300 }
//   NEW: task { subagent_type: "Reviewer: Code", prompt: "...", mode: "async", timeout_ms: 300000 }
//
// =============================================================================

import { type Plugin, tool } from "@opencode-ai/plugin";
import * as fs from "fs";
import * as os from "os";
import * as path from "path";

const PARSER_SCRIPT =
  "/home/dzack/.config/agents/skills/reading-transcripts/scripts/parse_opencode_log.py";
const TRANSCRIPT_TAIL_LINES = 30;

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function parseModel(
  model?: string,
): { providerID: string; modelID: string } | undefined {
  if (!model) return undefined;
  const [providerID, ...rest] = model.split("/");
  if (!providerID || rest.length === 0) return undefined;
  return { providerID, modelID: rest.join("/") };
}

async function waitForAssistantText(
  client: any,
  sessionId: string,
  timeoutMs: number,
): Promise<string> {
  const start = Date.now();
  let lastText = "";

  while (Date.now() - start < timeoutMs) {
    const { data: messages } = await client.session.messages({
      path: { id: sessionId },
    });

    if (messages?.length) {
      const lastAssistant = [...messages]
        .reverse()
        .find((m: any) => m.info.role === "assistant");
      if (lastAssistant) {
        lastText = (lastAssistant.parts ?? [])
          .filter((p: any) => p.type === "text")
          .map((p: any) => p.text)
          .join("")
          .trim();
        if (lastText) return lastText;
      }
    }

    await sleep(1000);
  }

  return lastText;
}

let queue: Promise<void> = Promise.resolve();

function enqueue(task: () => Promise<void>): void {
  queue = queue.then(task, task).catch(() => {});
}

async function getTranscriptTail(
  shell: any,
  sessionId: string,
): Promise<string | undefined> {
  const outPath = path.join(
    os.tmpdir(),
    `transcript-${sessionId}-${Date.now()}.txt`,
  );
  try {
    await shell`
      python ${PARSER_SCRIPT} ${sessionId} > ${outPath}
    `.quiet();
  } catch (error) {
    return undefined;
  }

  try {
    const content = fs.readFileSync(outPath, "utf-8").trimEnd();
    if (!content) return undefined;
    const lines = content.split("\n");
    const tail = lines.slice(-TRANSCRIPT_TAIL_LINES).join("\n").trim();
    return tail || undefined;
  } catch {
    return undefined;
  } finally {
    try {
      fs.unlinkSync(outPath);
    } catch {}
  }
}

async function runSubagentBackground(
  sessionID: string,
  agent: string,
  prompt: string,
  _cwd: string,
  time_estimate: number,
  title: string,
  model: string | undefined,
  shell: any,
  client: any,
): Promise<void> {
  try {
    const { data: session } = await client.session.create({
      body: { title },
    });

    const childSessionID = session?.id;
    if (!childSessionID) {
      throw new Error("Failed to create subagent session.");
    }

    await client.session.promptAsync({
      path: { id: sessionID },
      body: {
        noReply: true,
        parts: [
          {
            type: "text",
            text: [
              "[async_subagent info]",
              `Session ID: ${childSessionID}`,
              "FYI only — no response needed.",
              "Use read_transcript with this ID to view progress.",
            ].join("\n"),
          },
        ],
      },
    });

    const modelSpec = parseModel(model);
    if (!modelSpec) {
      throw new Error(
        "Missing or invalid model. Provide provider/model (e.g. opencode/big-pickle).",
      );
    }

    await client.session.promptAsync({
      path: { id: childSessionID },
      body: {
        model: modelSpec,
        agent,
        parts: [{ type: "text", text: prompt }],
      },
    });

    const output = await waitForAssistantText(
      client,
      childSessionID,
      time_estimate * 1000,
    );
    if (!output) {
      throw new Error(
        `Timed out waiting for subagent response after ${time_estimate}s.`,
      );
    }

    const transcriptTail = await getTranscriptTail(shell, childSessionID);

    const result = [
      `[async_subagent completed]`,
      `Agent: ${agent}`,
      `Title: ${title}`,
      `Session ID: ${childSessionID}`,
      `Transcript: run read_transcript ${childSessionID}.`,
      `Please continue with your task using the subagent output above.`,
      `=== OUTPUT ===`,
      output,
      transcriptTail
        ? [
            "",
            `=== TRANSCRIPT TAIL (${TRANSCRIPT_TAIL_LINES} lines) ===`,
            transcriptTail,
          ].join("\n")
        : "",
    ]
      .filter((line) => line !== "")
      .join("\n");

    await client.session.promptAsync({
      path: { id: sessionID },
      body: {
        noReply: false,
        parts: [{ type: "text", text: result }],
      },
    });
  } catch (error: any) {
    const errText = [
      `[async_subagent failed]`,
      `Agent: ${agent}`,
      `Title: ${title}`,
      `Error: ${error.message}`,
    ].join("\n");

    await client.session
      .promptAsync({
        path: { id: sessionID },
        body: {
          noReply: false,
          parts: [{ type: "text", text: errText }],
        },
      })
      .catch(() => {});
  }
}

export const AsyncSubagentPlugin: Plugin = async ({ client, $ }) => {
  return {
    tool: {
      async_subagent: tool({
        description:
          "Use when you need a subagent to run in the background without blocking the current turn.",
        args: {
          agent: tool.schema
            .string()
            .describe(
              "The exact name of the subagent to launch (e.g. 'Reviewer: Code')",
            ),
          prompt: tool.schema
            .string()
            .describe(
              "The highly detailed task/prompt for the subagent to execute",
            ),
          model: tool.schema
            .string()
            .optional()
            .describe(
              "Optional provider/model to run the subagent with (e.g. opencode/big-pickle).",
            ),
          time_estimate: tool.schema
            .number()
            .optional()
            .describe(
              "Optional timeout in seconds to wait for the subagent response before reporting failure. Defaults to 1800 (30 minutes).",
            ),
        },
        async execute(args, context) {
          const { sessionID } = context;
          const cwd = process.cwd();
          const waitTime = args.time_estimate ?? 1800;
          const title = `async-subagent:${sessionID}:${Date.now()}`;
          const model = args.model;

          // Fire and forget, but serialize subagents to avoid overload
          enqueue(() =>
            runSubagentBackground(
              sessionID,
              args.agent,
              args.prompt,
              cwd,
              waitTime,
              title,
              model,
              $,
              client,
            ),
          );

          return [
            `[async_subagent launched]`,
            `  Agent:    ${args.agent}`,
            `  Dir:      ${cwd}`,
            `  Session:  ${sessionID}`,
            `  Title:    ${title}`,
            `  Model:    ${model ?? "(required)"}`,
            `  Timeout:  ${waitTime}s`,
            `The subagent has been queued. Use list_sessions to find the subagent session if needed.`,
          ].join("\n");
        },
      }),
    },
  };
};
