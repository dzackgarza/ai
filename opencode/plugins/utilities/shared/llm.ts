/**
 * TypeScript subprocess wrapper for the scripts.llm Python package.
 *
 * All LLM calls from plugins go through here. The canonical source of truth
 * for providers, schemas, retries, and fallback logic lives in scripts/llm/.
 * This module is a thin bridge: it serialises the request to JSON, spawns
 * the Python bridge process, and deserialises the response.
 *
 * Usage:
 *   import { callLLM, loadMicroAgent, renderTemplate, runMicroAgent } from "../../utilities/shared/llm";
 *
 *   const result = await callLLM<{ tier: string; reasoning: string }>({
 *     models: ["groq/llama-3.3-70b-versatile"],
 *     messages: [{ role: "user", content: "..." }],
 *     schema: "Classification",
 *   });
 *
 *   const agent = await loadMicroAgent("/abs/path/to/prompt.md");
 *   // agent.system  — system prompt string
 *   // agent.body    — Jinja2 template body (already rendered by Python if needed)
 *
 *   const classification = await runMicroAgent<{ tier: string; reasoning: string }>(
 *     "/abs/path/to/prompt.md",
 *     { prompt: "Describe every tool you have access to." },
 *   );
 */

import { spawnSync } from "child_process";
import { fileURLToPath } from "url";
import { resolve, dirname } from "path";

const _dir = dirname(fileURLToPath(import.meta.url));

const OPENCODE_ROOT = resolve(_dir, "../../../");
const PYTHON = resolve(_dir, "../../../.venv/bin/python");
const RUN_MICRO_AGENT = resolve(_dir, "../../../../scripts/run_micro_agent.py");
const UV = "uv";

// ---------------------------------------------------------------------------
// Request / response types
// ---------------------------------------------------------------------------

export interface LLMRequest {
  /** Ordered list of model slugs. First success wins. */
  models: string[];
  messages: { role: string; content: string }[];
  /** Name of a registered schema in llm.py (e.g. "Classification"). */
  schema?: string;
  temperature?: number;
  max_tokens?: number;
  retries?: number;
}

export type LLMResponse<T = unknown> =
  | { ok: true; result: T }
  | { ok: false; error: string };

// ---------------------------------------------------------------------------
// callLLM — LLM call with optional structured output
// ---------------------------------------------------------------------------

/**
 * Call the Python LLM module with the given request.
 *
 * Returns the parsed result on success, throws on failure.
 */
export async function callLLM<T = string>(req: LLMRequest): Promise<T> {
  const res = _run<T>(req);
  if (!res.ok) throw new Error(`scripts.llm error: ${res.error}`);
  return res.result;
}

// ---------------------------------------------------------------------------
// loadMicroAgent — parse a micro-agent .md file into system + body
// ---------------------------------------------------------------------------

export interface MicroAgent {
  system: string | null;
  body: string;
  frontmatter: Record<string, unknown>;
  path: string;
}

/**
 * Load and parse a markdown prompt template.
 *
 * Returns the parsed system prompt and Jinja2 body separately, ready to be
 * used as LLM messages. The body should be rendered with variables before use.
 *
 * Example:
 *   const agent = await loadMicroAgent("/abs/path/to/prompt.md");
 *   messages = [
 *     { role: "system", content: agent.system },
 *     { role: "user",   content: renderTemplate(agent.body, { prompt: text }) },
 *   ];
 */
export async function loadMicroAgent(path: string): Promise<MicroAgent> {
  const res = _run<MicroAgent>({ action: "load_micro_agent", path } as any);
  if (!res.ok) throw new Error(`scripts.llm micro-agent error: ${res.error}`);
  return res.result;
}

// ---------------------------------------------------------------------------
// renderTemplate — render a Jinja2 template body string with variables
// ---------------------------------------------------------------------------

/**
 * Render a Jinja2 template body string with the given variables.
 *
 * Used for local rendering (no LLM call) — e.g. the response_template.md
 * for the prompt router, which takes { tier } and returns the instruction
 * to inject into the conversation.
 *
 * Example:
 *   const instruction = await renderTemplate(agent.body, { tier: "C" });
 */
export async function renderTemplate(
  body: string,
  variables: Record<string, string>,
  path?: string,
): Promise<string> {
  const res = _run<string>({
    action: "render_template",
    body,
    path,
    variables,
  } as any);
  if (!res.ok) throw new Error(`scripts.llm render error: ${res.error}`);
  return res.result;
}

// ---------------------------------------------------------------------------
// runMicroAgent — invoke the canonical CLI runner for a prompt template
// ---------------------------------------------------------------------------

export async function runMicroAgent<T = string>(
  path: string,
  variables: Record<string, string>,
  options?: { model?: string; temperature?: number },
): Promise<T> {
  const args = ["run", "--active", "--python", PYTHON, RUN_MICRO_AGENT, path];
  for (const [key, value] of Object.entries(variables)) {
    args.push("--var", `${key}=${value}`);
  }
  if (options?.model) {
    args.push("--model", options.model);
  }
  if (options?.temperature !== undefined) {
    args.push("--temperature", String(options.temperature));
  }

  const proc = spawnSync(UV, args, {
    cwd: OPENCODE_ROOT,
    encoding: "utf8",
    timeout: 60_000,
  });

  if (proc.error) {
    throw new Error(`scripts.llm runner spawn error: ${proc.error.message}`);
  }
  if (proc.status !== 0) {
    const stderr = proc.stderr?.trim() ?? "";
    throw new Error(
      `scripts.run_micro_agent exited ${proc.status}${stderr ? `: ${stderr}` : ""}`,
    );
  }

  try {
    return JSON.parse(proc.stdout) as T;
  } catch {
    throw new Error(`run_micro_agent returned non-JSON: ${proc.stdout?.slice(0, 200)}`);
  }
}

// ---------------------------------------------------------------------------
// Internal: synchronous spawn (plugins run at import-time; spawnSync is fine)
// ---------------------------------------------------------------------------

function _run<T>(req: object): LLMResponse<T> {
  const input = JSON.stringify(req);
  const proc = spawnSync(UV, ["run", "--active", "--python", PYTHON, "-m", "scripts.llm.bridge"], {
    cwd: OPENCODE_ROOT,
    input,
    encoding: "utf8",
    timeout: 60_000,
  });

  if (proc.error) {
    return { ok: false, error: `spawn error: ${proc.error.message}` };
  }
  if (proc.status !== 0) {
    const stderr = proc.stderr?.trim() ?? "";
    return {
      ok: false,
      error: `scripts.llm.bridge exited ${proc.status}${stderr ? `: ${stderr}` : ""}`,
    };
  }

  try {
    return JSON.parse(proc.stdout) as LLMResponse<T>;
  } catch {
    return {
      ok: false,
      error: `llm.py returned non-JSON: ${proc.stdout?.slice(0, 200)}`,
    };
  }
}
