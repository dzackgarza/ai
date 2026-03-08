#!/usr/bin/env bun

import { existsSync, readFileSync } from "fs";
import { resolve } from "path";
import { fileURLToPath, pathToFileURL } from "url";

type StepResult = {
  ok: boolean;
  label: string;
  stdout: string;
  stderr: string;
  status: number | null;
};

const PLUGINS_ROOT = resolve(import.meta.dir, "..");
const OPENCODE_ROOT = resolve(PLUGINS_ROOT, "..");
const CONFIG_PATH = resolve(OPENCODE_ROOT, "opencode.json");

function runStep(label: string, cmd: string[], cwd: string): StepResult {
  const proc = Bun.spawnSync(cmd, {
    cwd,
    env: process.env,
    stderr: "pipe",
    stdout: "pipe",
  });

  return {
    ok: proc.exitCode === 0,
    label,
    stdout: proc.stdout.toString(),
    stderr: proc.stderr.toString(),
    status: proc.exitCode,
  };
}

function activePluginEntrypoints(): string[] {
  const entries = new Set<string>();
  const localTools = resolve(PLUGINS_ROOT, "local-tools.ts");
  if (existsSync(localTools)) {
    entries.add(localTools);
  }

  const config = JSON.parse(readFileSync(CONFIG_PATH, "utf8")) as { plugin?: string[] };
  for (const plugin of config.plugin ?? []) {
    if (!plugin.startsWith("file://")) {
      continue;
    }
    const path = fileURLToPath(plugin);
    if (path.endsWith(".ts") && existsSync(path)) {
      entries.add(path);
    }
  }

  return [...entries].sort();
}

function printStep(result: StepResult): void {
  const status = result.ok ? "PASS" : "FAIL";
  console.log(`${status} ${result.label}`);
  if (result.stdout.trim()) {
    console.log(result.stdout.trim());
  }
  if (result.stderr.trim()) {
    console.error(result.stderr.trim());
  }
  if (!result.ok) {
    console.error(`exit code: ${result.status}`);
  }
  console.log("");
}

const failures: StepResult[] = [];

for (const result of [
  runStep("TypeScript typecheck", ["bunx", "tsc", "--noEmit"], PLUGINS_ROOT),
  runStep(
    "Bundle local-tools.ts",
    ["bun", "build", "--target", "bun", "--outdir", "/tmp/plugin-check", "local-tools.ts"],
    PLUGINS_ROOT,
  ),
]) {
  printStep(result);
  if (!result.ok) {
    failures.push(result);
  }
}

for (const entrypoint of activePluginEntrypoints()) {
  const result = runStep(
    `Import smoke test ${entrypoint}`,
    [
      "bun",
      "-e",
      `await import(${JSON.stringify(pathToFileURL(entrypoint).href)}); console.log("ok")`,
    ],
    PLUGINS_ROOT,
  );
  printStep(result);
  if (!result.ok) {
    failures.push(result);
  }
}

if (failures.length > 0) {
  console.error(`Plugin preflight failed: ${failures.length} step(s) errored.`);
  process.exit(1);
}

console.log("Plugin preflight passed.");
