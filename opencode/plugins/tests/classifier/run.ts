#!/usr/bin/env bun
// Classifier evaluation runner.
//
// Usage:
//   bun run run.ts [model-slug]
//
// Model slug prefixes:
//   (none)    → OpenRouter  (e.g. arcee-ai/trinity-large-preview:free)
//   groq/     → Groq        (e.g. groq/llama-3.3-70b-versatile)
//   nvidia/   → NVIDIA NIM  (e.g. nvidia/meta/llama-3.3-70b-instruct)
//   ollama/   → Ollama      (e.g. ollama/qwen3:4b)
//
// Defaults to arcee-ai/trinity-large-preview:free.
// Reads playbook from playbook.md and cases from cases.yaml.
// Writes per-run log to runs/{slug-safe}/{timestamp}.yaml.
// Updates cumulative scores in scores.yaml.
//
// Uses @instructor-ai/instructor for structured output enforcement:
// invalid JSON is retried automatically (up to MAX_RETRIES times).

import Instructor from "@instructor-ai/instructor";
import OpenAI from "openai";
import { z } from "zod";
import { parse, stringify } from "yaml";
import { join, dirname } from "path";
import { mkdirSync, readFileSync, writeFileSync } from "fs";

const DIR = dirname(import.meta.path);
const RUNS_DIR = join(DIR, "runs");
const DELAY_MS = 10000;
const MAX_RETRIES = 3;

// ---------------------------------------------------------------------------
// Provider routing
// ---------------------------------------------------------------------------

function endpointFor(model: string): { baseURL: string; modelId: string; apiKey: string } {
  if (model.startsWith("ollama/")) {
    return {
      baseURL: "http://localhost:11434/v1",
      modelId: model.slice("ollama/".length),
      apiKey: "ollama",
    };
  }
  if (model.startsWith("groq/")) {
    return {
      baseURL: "https://api.groq.com/openai/v1",
      modelId: model.slice("groq/".length),
      apiKey: process.env.GROQ_API_KEY ?? "",
    };
  }
  if (model.startsWith("nvidia/")) {
    return {
      baseURL: "https://integrate.api.nvidia.com/v1",
      modelId: model.slice("nvidia/".length),
      apiKey: process.env.NVIDIA_API_KEY ?? "",
    };
  }
  // Default: OpenRouter
  return {
    baseURL: "https://openrouter.ai/api/v1",
    modelId: model,
    apiKey: process.env.OPENROUTER_API_KEY ?? "",
  };
}

// ---------------------------------------------------------------------------
// Schema
// ---------------------------------------------------------------------------

const ClassificationSchema = z.object({
  tier: z.enum(["model-self", "knowledge", "C", "B", "A", "S"]),
  reasoning: z.string(),
});

type Classification = z.infer<typeof ClassificationSchema>;

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface Case {
  prompt: string;
  tier: string;
  label: string;
}

interface CaseResult {
  prompt: string;
  label: string;
  expected: string;
  got: string;
  pass: boolean;
  reasoning: string;
  latency_ms: number;
}

interface RunLog {
  model: string;
  timestamp: string;
  playbook_file: string;
  passed: number;
  total: number;
  score: number;
  results: CaseResult[];
}

interface ModelScore {
  total_runs: number;
  total_cases: number;
  total_passed: number;
  cumulative_score: number;
  last_run: string;
}

interface ScoresFile {
  models: Record<string, ModelScore>;
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function slugToDir(slug: string): string {
  return slug.replace(/\//g, "--").replace(/:/g, "-");
}

const delay = (ms: number) => new Promise(r => setTimeout(r, ms));

// ---------------------------------------------------------------------------
// Classify
// ---------------------------------------------------------------------------

async function classify(
  playbook: string,
  model: string,
  prompt: string,
): Promise<{ tier: string; reasoning: string; latency_ms: number }> {
  const t0 = Date.now();
  const { baseURL, modelId, apiKey } = endpointFor(model);

  const oai = new OpenAI({ baseURL, apiKey });
  const client = Instructor({ client: oai, mode: instructorMode });

  try {
    const result: Classification = await client.chat.completions.create({
      model: modelId,
      messages: [
        { role: "system", content: playbook },
        { role: "user", content: `Classify the following prompt:\n\n===\n${prompt}\n===` },
      ],
      response_model: { schema: ClassificationSchema, name: "Classification" },
      max_retries: MAX_RETRIES,
      max_tokens: instructorMode === "MD_JSON" ? 400 : 200,
      temperature: 0,
    });
    return { tier: result.tier, reasoning: result.reasoning, latency_ms: Date.now() - t0 };
  } catch (e: any) {
    return {
      tier: `ERROR: ${String(e?.message ?? e).slice(0, 80)}`,
      reasoning: "",
      latency_ms: Date.now() - t0,
    };
  }
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

// Optional --mode flag: bun run run.ts <slug> --mode MD_JSON
const modeArg = process.argv.indexOf("--mode");
const instructorMode = (modeArg !== -1 ? process.argv[modeArg + 1] : "JSON") as "JSON" | "MD_JSON";
if (instructorMode === "MD_JSON") console.log(`Instructor mode: MD_JSON (no response_format header)\n`);

const model = process.argv.find((a, i) => i >= 2 && !a.startsWith("--") && process.argv[i-1] !== "--mode") ?? "arcee-ai/trinity-large-preview:free";
const { apiKey } = endpointFor(model);
if (!model.startsWith("ollama/") && !apiKey) {
  console.error("API key not set for this provider"); process.exit(1);
}

const playbook = readFileSync(join(DIR, "playbook.md"), "utf8").trim();
const { cases } = parse(readFileSync(join(DIR, "cases.yaml"), "utf8")) as { cases: Case[] };

console.log(`Model:      ${model}`);
console.log(`Cases:      ${cases.length}`);
console.log(`Delay:      ${DELAY_MS}ms between requests`);
console.log(`Max retries: ${MAX_RETRIES}\n`);

const results: CaseResult[] = [];
let passed = 0;

for (let i = 0; i < cases.length; i++) {
  const { prompt, tier: expected, label } = cases[i];
  if (i > 0) await delay(DELAY_MS);

  const { tier: got, reasoning, latency_ms } = await classify(playbook, model, prompt);
  const pass = got === expected;
  if (pass) passed++;

  results.push({ prompt, label, expected, got, pass, reasoning, latency_ms });
  console.log(`${pass ? "PASS" : "FAIL"} [${label}] expected=${expected} got=${got} (${latency_ms}ms)`);
  console.log(`     "${prompt}"`);
  if (!pass && reasoning) console.log(`     reason: ${reasoning}`);
}

const score = passed / cases.length;
const timestamp = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);

console.log(`\n${passed}/${cases.length} passed (${(score * 100).toFixed(0)}%)`);

// ---------------------------------------------------------------------------
// Write run log
// ---------------------------------------------------------------------------

const runLog: RunLog = {
  model,
  timestamp: new Date().toISOString(),
  playbook_file: "classifier/playbook.md",
  passed,
  total: cases.length,
  score,
  results,
};

const runDir = join(RUNS_DIR, slugToDir(model));
mkdirSync(runDir, { recursive: true });
const runFile = join(runDir, `${timestamp}.yaml`);
writeFileSync(runFile, stringify(runLog));
console.log(`\nRun log: ${runFile}`);

// ---------------------------------------------------------------------------
// Update cumulative scores
// ---------------------------------------------------------------------------

const scoresPath = join(DIR, "scores.yaml");
const scoresRaw = readFileSync(scoresPath, "utf8");
const scores = parse(scoresRaw) as ScoresFile;
if (!scores.models) scores.models = {};

const prev = scores.models[model] ?? { total_runs: 0, total_cases: 0, total_passed: 0, cumulative_score: 0, last_run: "" };
scores.models[model] = {
  total_runs: prev.total_runs + 1,
  total_cases: prev.total_cases + cases.length,
  total_passed: prev.total_passed + passed,
  cumulative_score: (prev.total_passed + passed) / (prev.total_cases + cases.length),
  last_run: new Date().toISOString(),
};

writeFileSync(scoresPath, stringify(scores));
console.log(`Scores updated: ${(scores.models[model].cumulative_score * 100).toFixed(0)}% cumulative`);
