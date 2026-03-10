/**
 * TypeScript subprocess wrapper for llm-runner and llm-templating-engine.
 *
 * Plugins never import Python directly. They shell into the JSON-first CLIs
 * installed in ~/ai/opencode/.venv and exchange structured JSON over stdin/stdout.
 */

import { spawnSync } from "child_process";
import { fileURLToPath } from "url";
import { resolve, dirname } from "path";

const _dir = dirname(fileURLToPath(import.meta.url));

const OPENCODE_ROOT = resolve(_dir, "../../../");
const PYTHON = resolve(_dir, "../../../.venv/bin/python");
const UV = "uv";
const TEMPLATE_RENDER = "llm-template-render";
const TEMPLATE_INSPECT = "llm-template-inspect";
const RUNNER_INVOKE = "llm-invoke";
const RUNNER_RUN = "llm-run";

export interface ErrorResponse {
  error: {
    type: string;
    message: string;
  };
}

export interface ChatMessage {
  role: "system" | "user" | "assistant" | "tool";
  content: string;
}

export interface TemplateReference {
  path?: string;
  text?: string;
  name?: string;
}

export interface TextFileBinding {
  name: string;
  path: string;
}

export interface Bindings {
  data?: Record<string, unknown>;
  text_files?: TextFileBinding[];
}

export interface TemplateOptions {
  search_paths?: string[];
  render_mode?: "body" | "document";
  strict_undefined?: boolean;
}

export interface TemplateDocument {
  path?: string | null;
  name?: string | null;
  frontmatter: Record<string, unknown>;
  body_template: string;
}

export interface InspectTemplateResponse {
  template: TemplateDocument;
}

export interface RenderTemplateResponse {
  template: TemplateDocument;
  rendered: {
    body: string;
    document: string;
  };
}

export interface InvokeOptions {
  temperature?: number;
  max_tokens?: number;
  retries?: number;
}

export interface LLMRequest {
  models: string[];
  messages: ChatMessage[];
  output_schema?: Record<string, unknown>;
  options?: InvokeOptions;
}

export interface InvokeResponse<T = unknown> {
  model: string;
  raw_text: string;
  structured: T | null;
}

export interface RunOverrides {
  models?: string[];
  temperature?: number;
  max_tokens?: number;
  retries?: number;
  output_schema?: Record<string, unknown>;
}

export interface RunRequest {
  template: TemplateReference;
  bindings?: Bindings;
  overrides?: RunOverrides;
}

export interface RunExecution {
  template_path: string;
  model: string;
  messages: ChatMessage[];
}

export interface FinalOutput<T = unknown> {
  text?: string | null;
  data?: T | null;
}

export interface RunResponse<T = unknown, TFinal = unknown> {
  run: RunExecution;
  response: InvokeResponse<T>;
  final_output: FinalOutput<TFinal>;
}

function parseError(stdout: string): string | null {
  try {
    const payload = JSON.parse(stdout) as ErrorResponse;
    if (typeof payload.error?.message === "string") {
      return payload.error.message;
    }
  } catch {
    return null;
  }
  return null;
}

function runJsonCommand<T>(command: string, request: object): T {
  const proc = spawnSync(UV, ["run", "--active", "--python", PYTHON, command], {
    cwd: OPENCODE_ROOT,
    input: JSON.stringify(request),
    encoding: "utf8",
    timeout: 60_000,
  });

  if (proc.error) {
    throw new Error(`${command} spawn error: ${proc.error.message}`);
  }

  const stdout = proc.stdout?.trim() ?? "";
  const stderr = proc.stderr?.trim() ?? "";
  if (proc.status !== 0) {
    const message =
      parseError(stdout) ?? (stderr || `${command} exited ${proc.status}`);
    throw new Error(`${command} error: ${message}`);
  }

  try {
    return JSON.parse(stdout) as T;
  } catch {
    throw new Error(`${command} returned non-JSON: ${stdout.slice(0, 200)}`);
  }
}

export async function callLLM<T = unknown>(
  request: LLMRequest,
): Promise<InvokeResponse<T>> {
  return runJsonCommand<InvokeResponse<T>>(RUNNER_INVOKE, request);
}

export async function inspectTemplate(path: string): Promise<TemplateDocument> {
  const response = runJsonCommand<InspectTemplateResponse>(TEMPLATE_INSPECT, {
    template: { path },
  });
  return response.template;
}

export async function renderTemplate(
  body: string,
  bindings: Record<string, unknown>,
  path?: string,
): Promise<string> {
  const response = runJsonCommand<RenderTemplateResponse>(TEMPLATE_RENDER, {
    template: path ? { text: body, name: path } : { text: body },
    bindings: { data: bindings },
  });
  return response.rendered.body;
}

export async function renderTemplatePath(
  path: string,
  bindings: Record<string, unknown>,
): Promise<string> {
  const response = runJsonCommand<RenderTemplateResponse>(TEMPLATE_RENDER, {
    template: { path },
    bindings: { data: bindings },
  });
  return response.rendered.body;
}

export async function runMicroAgent<T = unknown, TFinal = unknown>(
  path: string,
  bindings: Record<string, unknown>,
  options?: {
    model?: string;
    temperature?: number;
    max_tokens?: number;
    retries?: number;
  },
): Promise<RunResponse<T, TFinal>> {
  const overrides: RunOverrides = {};
  if (options?.model) {
    overrides.models = [options.model];
  }
  if (options?.temperature !== undefined) {
    overrides.temperature = options.temperature;
  }
  if (options?.max_tokens !== undefined) {
    overrides.max_tokens = options.max_tokens;
  }
  if (options?.retries !== undefined) {
    overrides.retries = options.retries;
  }

  return runJsonCommand<RunResponse<T, TFinal>>(RUNNER_RUN, {
    template: { path },
    bindings: { data: bindings },
    overrides,
  });
}
