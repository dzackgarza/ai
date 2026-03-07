/**
 * TypeScript subprocess wrapper for scripts/llm.py.
 *
 * All LLM calls from plugins go through here. The canonical source of truth
 * for providers, schemas, retries, and fallback logic lives in scripts/llm.py.
 * This module is a thin bridge: it serialises the request to JSON, spawns
 * the Python process, and deserialises the response.
 *
 * Usage:
 *   import { callLLM, loadTemplate } from "../../utilities/shared/llm";
 *
 *   const result = await callLLM<{ tier: string; reasoning: string }>({
 *     models: ["groq/llama-3.3-70b-versatile"],
 *     messages: [{ role: "user", content: "..." }],
 *     schema: "Classification",
 *   });
 */

import { spawnSync } from "child_process";
import { fileURLToPath } from "url";
import { resolve, dirname } from "path";

const _dir = dirname(fileURLToPath(import.meta.url));

// Path to scripts/llm.py — canonical LLM dispatch module.
const LLM_PY = resolve(_dir, "../../../scripts/llm.py");

// Python binary: prefer the venv, fall back to system python3.
const PYTHON = resolve(_dir, "../../../.venv/bin/python");

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
  if (!res.ok) throw new Error(`llm.py error: ${res.error}`);
  return res.result;
}

// ---------------------------------------------------------------------------
// loadTemplate — fetch a template file by name
// ---------------------------------------------------------------------------

/**
 * Load a template from scripts/templates/ by name.
 *
 * Examples:
 *   await loadTemplate("classifier/playbook")  // returns playbook.md contents
 *   await loadTemplate("tiers/A")              // returns tiers/A.md contents
 */
export async function loadTemplate(name: string): Promise<string> {
  const res = _run<string>({ action: "load_template", template: name } as any);
  if (!res.ok) throw new Error(`llm.py template error: ${res.error}`);
  return res.result;
}

// ---------------------------------------------------------------------------
// Internal: synchronous spawn (plugins run at import-time; spawnSync is fine)
// ---------------------------------------------------------------------------

function _run<T>(req: object): LLMResponse<T> {
  const input = JSON.stringify(req);
  const proc = spawnSync(PYTHON, [LLM_PY], {
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
      error: `llm.py exited ${proc.status}${stderr ? `: ${stderr}` : ""}`,
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
