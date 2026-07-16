#!/usr/bin/env node
import { existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, isAbsolute, resolve } from "node:path";

const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..", "..");
const pidfilePath = "/home/dzack/ai/mcp/sdl-mcp.pid";
const indexedExtensions = new Set([".ts",".tsx",".js",".jsx",".mjs",".cjs",".py",".pyw",".go",".java",".cs",".c",".h",".cpp",".hpp",".cc",".cxx",".hxx",".php",".phtml",".rs",".kt",".kts",".sh",".bash",".zsh"]);

const RUNTIME_REASON =
  "Run repo-local shell actions through SDL-MCP instead of native shell. Use sdl.workflow with runtimeExecute, default outputMode: \"minimal\", persistOutput: true, an explicit timeoutMs, stdin for multiline input, and runtimeQueryOutput only for focused follow-up output.";
const INDEXED_READ_REASON =
  "Use the SDL-MCP Iris retrieval ladder for indexed source reads. Start with sdl.context, then batch follow-ups through sdl.workflow using symbolSearch, symbolGetCard, codeSkeleton, codeHotPath, and codeNeedWindow only as a last resort with identifiersToFind and expectedLines.";
const INDEXED_WRITE_REASON =
  "Use SDL-MCP indexed-source edit tools instead of native writes. Prefer symbol.edit for one-symbol edits; use searchEditPreview with targeting:\"identifier\" for exact AST identifier replacements in supported structural languages, targeting:\"structural\" for tree-sitter capture edits, or operations[] for heterogeneous batches. Review astMatches/snippets, then apply the plan handle. If SDL edit tools cannot express the change, run a targeted script through sdl.workflow runtimeExecute with stdin.";
const NON_INDEXED_READ_REASON =
  "Use SDL-MCP file.read for non-indexed repository reads. Prefer sdl.file { op: \"read\" } or file.read with search, jsonPath, or bounded offset/limit instead of native file reads.";
const NON_INDEXED_WRITE_REASON =
  "Use SDL-MCP file.write for non-indexed repository writes. Prefer sdl.file { op: \"write\" } or file.write with one targeted write mode instead of native Write/Edit/apply_patch.";
const MCP_REASON =
  "Use SDL-MCP file/search/edit/runtime actions instead of non-SDL MCP file, search, write, or edit tools in this repository.";

if (!existsSync(pidfilePath)) {
  process.exit(0);
}

function deny(reason) {
  process.stdout.write(
    JSON.stringify({
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason: reason,
      },
    }),
  );
}

function normalize(value) {
  return String(value ?? "").replace(/\\/g, "/").toLowerCase();
}

function userHome() {
  return process.env.USERPROFILE || process.env.HOME || "";
}

function normalizeResolvedPath(value) {
  const raw = String(value ?? "").trim();
  if (!raw) {
    return "";
  }
  try {
    return normalize(isAbsolute(raw) ? resolve(raw) : resolve(repoRoot, raw));
  } catch {
    return normalize(raw);
  }
}

function pathIsWithin(path, parent) {
  const normalizedPath = normalizeResolvedPath(path);
  const normalizedParent = normalizeResolvedPath(parent);
  return (
    normalizedPath === normalizedParent ||
    normalizedPath.startsWith(normalizedParent + "/")
  );
}

function isRepoPath(path) {
  return pathIsWithin(path, repoRoot);
}

function isRepoInternalPath(path) {
  return (
    pathIsWithin(path, resolve(repoRoot, ".codex")) ||
    pathIsWithin(path, resolve(repoRoot, ".claude"))
  );
}

function isUserInternalPath(path) {
  const home = userHome();
  if (!home) {
    return false;
  }
  return [
    resolve(home, ".codex", "memories"),
    resolve(home, ".codex", "skills"),
    resolve(home, ".codex", "plugins"),
    resolve(home, ".codex", "sessions"),
    resolve(home, ".agents", "skills"),
    resolve(home, ".claude", "agents"),
    resolve(home, ".claude", "skills"),
  ].some((root) => pathIsWithin(path, root));
}

function isAllowedInternalPath(path) {
  return isRepoInternalPath(path) || (!isRepoPath(path) && isUserInternalPath(path));
}

function getToolInput(input) {
  return input.tool_input ?? input.toolInput ?? input.input ?? {};
}

function getToolName(input) {
  return String(input.tool_name ?? input.toolName ?? "");
}

function getHookEventName(input) {
  return String(input.hook_event_name ?? input.hookEventName ?? "");
}

function getCommand(toolInput) {
  return String(
    toolInput.command ??
      toolInput.cmd ??
      toolInput.script ??
      toolInput.args?.command ??
      "",
  );
}

function collectStringPaths(value, paths = []) {
  if (!value) {
    return paths;
  }
  if (Array.isArray(value)) {
    for (const entry of value) {
      collectStringPaths(entry, paths);
    }
    return paths;
  }
  if (typeof value === "object") {
    for (const [key, entry] of Object.entries(value)) {
      if (
        /^(file_path|filePath|path|filename|target_file|targetFile|old_path|oldPath|new_path|newPath)$/i.test(
          key,
        ) &&
        typeof entry === "string"
      ) {
        paths.push(entry);
      } else {
        collectStringPaths(entry, paths);
      }
    }
    return paths;
  }
  return paths;
}

function collectPatchPaths(toolInput) {
  const patch = String(toolInput.patch ?? toolInput.diff ?? "");
  const paths = [];
  for (const match of patch.matchAll(/^\*\*\* (?:Add|Update|Delete) File: (.+)$/gim)) {
    paths.push(match[1].trim());
  }
  return paths;
}

function getCandidatePaths(toolInput) {
  return [...collectStringPaths(toolInput), ...collectPatchPaths(toolInput)].filter(
    Boolean,
  );
}

function targetsRepo(input, serializedToolInput, toolInput, candidatePaths) {
  const normalizedRepoRoot = normalize(repoRoot);
  const cwd = input.cwd ?? toolInput.cwd ?? toolInput.workdir ?? toolInput.working_directory;
  return (
    normalize(cwd).startsWith(normalizedRepoRoot) ||
    normalize(serializedToolInput).includes(normalizedRepoRoot) ||
    candidatePaths.some((path) => isRepoPath(path))
  );
}

function containsIndexedSourcePath(value) {
  const normalized = normalize(value);
  if (normalized.includes("/src/") || normalized.includes("src/")) {
    return true;
  }
  for (const extension of indexedExtensions) {
    if (normalized.includes(extension)) {
      return true;
    }
  }
  return false;
}

function fileOperation(toolName) {
  const normalized = toolName.toLowerCase();
  if (normalized === "read" || normalized.endsWith(".read")) {
    return "read";
  }
  if (
    ["write", "edit", "multiedit", "notebookedit", "apply_patch"].some(
      (name) => normalized === name || normalized.endsWith("." + name),
    )
  ) {
    return "write";
  }
  return null;
}

function internalCommandLooksAllowed(command) {
  const normalized = normalize(command);
  const mentionsInternal =
    /(?:^|[\s"'\x60])\.(?:codex|claude)(?:[\/"'\x60\s]|$)/i.test(command) ||
    normalized.includes("/.codex/") ||
    normalized.includes("/.claude/") ||
    normalized.includes("/.agents/skills/");
  if (!mentionsInternal) {
    return false;
  }
  return !/(?:^|[\s"'\x60])(?:src|tests|docs|templates|native|scripts|config|packages|grammar-wrappers|README\.md|SDL\.md|AGENTS\.md|CODEX\.md|CLAUDE\.md|package(?:-lock)?\.json|tsconfig\.json|eslint\.config\.mjs)(?:[\/"'\x60\s]|$)/i.test(
    command,
  );
}

function nativeFileReason(toolName, toolInput, serializedToolInput, candidatePaths) {
  const operation = fileOperation(toolName);
  if (!operation) {
    return null;
  }
  const indexed =
    candidatePaths.some((path) => containsIndexedSourcePath(path)) ||
    containsIndexedSourcePath(serializedToolInput);
  if (operation === "read") {
    return indexed ? INDEXED_READ_REASON : NON_INDEXED_READ_REASON;
  }
  return indexed ? INDEXED_WRITE_REASON : NON_INDEXED_WRITE_REASON;
}

function isNativeFileTool(toolName) {
  return fileOperation(toolName) !== null;
}

function isShellTool(toolName) {
  const normalized = toolName.toLowerCase();
  return (
    normalized === "bash" ||
    normalized === "shell" ||
    normalized === "shell_command" ||
    normalized.endsWith(".shell_command")
  );
}

function isSdlMcpTool(toolName) {
  return /^mcp__sdl[_-]mcp__/.test(toolName);
}

function isNonSdlMcpFileTool(toolName) {
  return (
    /^mcp__/.test(toolName) &&
    !isSdlMcpTool(toolName) &&
    /(file|filesystem|fs|read|write|edit|search|grep|ripgrep|glob)/i.test(toolName)
  );
}

const rawInput = await new Promise((resolveInput) => {
  let data = "";
  process.stdin.setEncoding("utf8");
  process.stdin.on("data", (chunk) => {
    data += chunk;
  });
  process.stdin.on("end", () => resolveInput(data));
});

if (!rawInput.trim()) {
  process.exit(0);
}

let hookInput;
try {
  hookInput = JSON.parse(rawInput);
} catch {
  process.exit(0);
}

if (getHookEventName(hookInput) !== "PreToolUse") {
  process.exit(0);
}

const toolInput = getToolInput(hookInput);
const toolName = getToolName(hookInput);
const toolInputJson = JSON.stringify(toolInput);
const candidatePaths = getCandidatePaths(toolInput);

if (isSdlMcpTool(toolName)) {
  process.exit(0);
}

if (isShellTool(toolName)) {
  const command = getCommand(toolInput);
  if (internalCommandLooksAllowed(command)) {
    process.exit(0);
  }
  if (targetsRepo(hookInput, toolInputJson, toolInput, candidatePaths)) {
    deny(RUNTIME_REASON);
  }
  process.exit(0);
}

if (
  candidatePaths.length > 0 &&
  candidatePaths.every((path) => isAllowedInternalPath(path))
) {
  process.exit(0);
}

if (!targetsRepo(hookInput, toolInputJson, toolInput, candidatePaths)) {
  process.exit(0);
}

if (isNativeFileTool(toolName)) {
  deny(nativeFileReason(toolName, toolInput, toolInputJson, candidatePaths));
  process.exit(0);
}

if (isNonSdlMcpFileTool(toolName)) {
  deny(MCP_REASON);
}
