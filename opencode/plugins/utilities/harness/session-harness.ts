#!/usr/bin/env bun
/**
 * Session Management CLI Harness - Full API
 *
 * Compatibility source snapshot during extraction to the standalone
 * `dzackgarza/opencode-manager` repo.
 *
 * Usage:
 *   opx-session <command> [options]
 *
 * Commands:
 *   list, get, children, create, update, delete
 *   abort, share, unshare, summarize
 *   messages, message
 *   prompt, command, shell
 *   revert, unrevert
 *   init, permission
 *   stats
 */

import { $ } from "bun";

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

const OPENCODE_BASE_URL = process.env.OPENCODE_BASE_URL ?? "http://localhost:4096";
const OPENCODE_API_KEY = process.env.OPENCODE_API_KEY;

const API_BASE = `${OPENCODE_BASE_URL}/api`;

const headers: Record<string, string> = {
  "Content-Type": "application/json",
};

if (OPENCODE_API_KEY) {
  headers["Authorization"] = `Bearer ${OPENCODE_API_KEY}`;
}

// ---------------------------------------------------------------------------
// Types (from OpenCode API)
// ---------------------------------------------------------------------------

interface Session {
  id: string;
  title: string;
  time: {
    created: number;
    updated: number;
  };
  summary?: {
    additions: number;
    deletions: number;
    files: number;
  };
  parentID?: string;
  shared?: boolean;
  shareUrl?: string;
}

interface Message {
  id: string;
  role: "user" | "assistant" | "system";
  providerID?: string;
  modelID?: string;
  time?: {
    created: number;
  };
  tokens?: {
    input: number;
    output: number;
    reasoning: number;
    cache: {
      read: number;
      write: number;
    };
  };
}

interface Part {
  type: string;
  text?: string;
  content?: string;
  [key: string]: any;
}

interface AssistantMessage extends Message {
  role: "assistant";
}

interface UserMessage extends Message {
  role: "user";
}

// ---------------------------------------------------------------------------
// API Client
// ---------------------------------------------------------------------------

async function apiRequest<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      ...headers,
      ...options?.headers,
    },
  });

  if (!response.ok) {
    const errorText = await response.text().catch(() => "Unknown error");
    throw new Error(`API error (${response.status}): ${errorText}`);
  }

  if (response.status === 204) {
    return {} as T;
  }

  return response.json() as Promise<T>;
}

// ---------------------------------------------------------------------------
// Session Operations - Full API
// ---------------------------------------------------------------------------

// session.list()
async function listSessions(): Promise<Session[]> {
  const { data } = await apiRequest<{ data: Session[] }>("/sessions");
  return (data ?? []).sort((a, b) => b.time.updated - a.time.updated);
}

// session.get({ path: { id } })
async function getSession(sessionID: string): Promise<Session | null> {
  try {
    const { data } = await apiRequest<{ data: Session }>(`/sessions/${sessionID}`);
    return data ?? null;
  } catch (error: any) {
    if (error.message?.includes("404")) {
      return null;
    }
    throw error;
  }
}

// session.children({ path: { id } })
async function getChildSessions(sessionID: string): Promise<Session[]> {
  try {
    const { data } = await apiRequest<{ data: Session[] }>(`/sessions/${sessionID}/children`);
    return (data ?? []).sort((a, b) => b.time.updated - a.time.updated);
  } catch (error: any) {
    if (error.message?.includes("404")) {
      return [];
    }
    throw error;
  }
}

// session.create({ body })
async function createSession(options?: { title?: string; parentID?: string }): Promise<Session> {
  const { data } = await apiRequest<{ data: Session }>("/sessions", {
    method: "POST",
    body: JSON.stringify({
      title: options?.title ?? `session-${Date.now()}`,
      parentID: options?.parentID,
    }),
  });
  
  if (!data) {
    throw new Error("Failed to create session");
  }
  
  return data;
}

// session.update({ path: { id }, body })
async function updateSession(sessionID: string, updates: { title?: string; [key: string]: any }): Promise<Session> {
  const { data } = await apiRequest<{ data: Session }>(`/sessions/${sessionID}`, {
    method: "PATCH",
    body: JSON.stringify(updates),
  });
  
  if (!data) {
    throw new Error("Failed to update session");
  }
  
  return data;
}

// session.delete({ path: { id } })
async function deleteSession(sessionID: string): Promise<boolean> {
  try {
    await apiRequest(`/sessions/${sessionID}`, {
      method: "DELETE",
    });
    return true;
  } catch (error: any) {
    if (error.message?.includes("404")) {
      return false;
    }
    throw error;
  }
}

// session.abort({ path: { id } })
async function abortSession(sessionID: string): Promise<boolean> {
  try {
    await apiRequest(`/sessions/${sessionID}/abort`, {
      method: "POST",
    });
    return true;
  } catch (error: any) {
    if (error.message?.includes("404")) {
      return false;
    }
    throw error;
  }
}

// session.share({ path: { id } })
async function shareSession(sessionID: string): Promise<Session> {
  const { data } = await apiRequest<{ data: Session }>(`/sessions/${sessionID}/share`, {
    method: "POST",
  });
  
  if (!data) {
    throw new Error("Failed to share session");
  }
  
  return data;
}

// session.unshare({ path: { id } })
async function unshareSession(sessionID: string): Promise<Session> {
  const { data } = await apiRequest<{ data: Session }>(`/sessions/${sessionID}/unshare`, {
    method: "POST",
  });
  
  if (!data) {
    throw new Error("Failed to unshare session");
  }
  
  return data;
}

// session.summarize({ path: { id }, body })
async function summarizeSession(sessionID: string, options?: { instruction?: string }): Promise<boolean> {
  try {
    await apiRequest(`/sessions/${sessionID}/summarize`, {
      method: "POST",
      body: JSON.stringify({
        instruction: options?.instruction,
      }),
    });
    return true;
  } catch (error: any) {
    if (error.message?.includes("404")) {
      return false;
    }
    throw error;
  }
}

// session.messages({ path: { id } })
async function getMessages(sessionID: string): Promise<Array<{ info: Message; parts: Part[] }>> {
  const { data } = await apiRequest<{ data: Array<{ info: Message; parts: Part[] }> }>(
    `/sessions/${sessionID}/messages`
  );
  return data ?? [];
}

// session.message({ path: { id, messageId } })
async function getMessage(sessionID: string, messageID: string): Promise<{ info: Message; parts: Part[] } | null> {
  try {
    const { data } = await apiRequest<{ data: { info: Message; parts: Part[] } }>(
      `/sessions/${sessionID}/messages/${messageID}`
    );
    return data ?? null;
  } catch (error: any) {
    if (error.message?.includes("404")) {
      return null;
    }
    throw error;
  }
}

// session.prompt({ path: { id }, body })
async function sendPrompt(
  sessionID: string,
  message: string,
  options?: { noReply?: boolean; outputFormat?: string }
): Promise<AssistantMessage | UserMessage> {
  const { data } = await apiRequest<{ data: AssistantMessage | UserMessage }>(
    `/sessions/${sessionID}/prompt`,
    {
      method: "POST",
      body: JSON.stringify({
        message,
        noReply: options?.noReply,
        outputFormat: options?.outputFormat,
      }),
    }
  );
  
  if (!data) {
    throw new Error("Failed to send prompt");
  }
  
  return data;
}

// session.command({ path: { id }, body })
async function sendCommand(
  sessionID: string,
  command: string,
  args?: string[]
): Promise<{ info: AssistantMessage; parts: Part[] }> {
  const { data } = await apiRequest<{ data: { info: AssistantMessage; parts: Part[] } }>(
    `/sessions/${sessionID}/command`,
    {
      method: "POST",
      body: JSON.stringify({ command, args }),
    }
  );
  
  if (!data) {
    throw new Error("Failed to send command");
  }
  
  return data;
}

// session.shell({ path: { id }, body })
async function runShell(
  sessionID: string,
  command: string
): Promise<AssistantMessage> {
  const { data } = await apiRequest<{ data: AssistantMessage }>(
    `/sessions/${sessionID}/shell`,
    {
      method: "POST",
      body: JSON.stringify({ command }),
    }
  );
  
  if (!data) {
    throw new Error("Failed to run shell command");
  }
  
  return data;
}

// session.revert({ path: { id }, body })
async function revertMessage(sessionID: string, messageID: string): Promise<Session> {
  const { data } = await apiRequest<{ data: Session }>(
    `/sessions/${sessionID}/revert`,
    {
      method: "POST",
      body: JSON.stringify({ messageID }),
    }
  );
  
  if (!data) {
    throw new Error("Failed to revert message");
  }
  
  return data;
}

// session.unrevert({ path: { id } })
async function unrevertSession(sessionID: string): Promise<Session> {
  const { data } = await apiRequest<{ data: Session }>(
    `/sessions/${sessionID}/unrevert`,
    {
      method: "POST",
    }
  );
  
  if (!data) {
    throw new Error("Failed to unrevert session");
  }
  
  return data;
}

// session.init({ path: { id }, body })
async function initSession(
  sessionID: string,
  options?: { analyze?: boolean; createAgentsMd?: boolean }
): Promise<boolean> {
  try {
    await apiRequest(`/sessions/${sessionID}/init`, {
      method: "POST",
      body: JSON.stringify({
        analyze: options?.analyze,
        createAgentsMd: options?.createAgentsMd,
      }),
    });
    return true;
  } catch (error: any) {
    if (error.message?.includes("404")) {
      return false;
    }
    throw error;
  }
}

// postSessionByIdPermissionsByPermissionId({ path, body })
async function respondToPermission(
  sessionID: string,
  permissionID: string,
  response: "allow" | "deny" | "allow-session" | "deny-session"
): Promise<boolean> {
  try {
    await apiRequest(`/sessions/${sessionID}/permissions/${permissionID}`, {
      method: "POST",
      body: JSON.stringify({ response }),
    });
    return true;
  } catch (error: any) {
    if (error.message?.includes("404")) {
      return false;
    }
    throw error;
  }
}

// ---------------------------------------------------------------------------
// Statistics
// ---------------------------------------------------------------------------

interface SessionStats {
  totalSessions: number;
  totalTurns: number;
  totalTokens: {
    input: number;
    output: number;
    reasoning: number;
  };
  averageTurnsPerSession: number;
  averageTokensPerSession: number;
  oldestSession: Session | null;
  newestSession: Session | null;
}

async function getStats(): Promise<SessionStats> {
  const sessions = await listSessions();
  
  if (sessions.length === 0) {
    return {
      totalSessions: 0,
      totalTurns: 0,
      totalTokens: { input: 0, output: 0, reasoning: 0 },
      averageTurnsPerSession: 0,
      averageTokensPerSession: 0,
      oldestSession: null,
      newestSession: null,
    };
  }
  
  let totalTurns = 0;
  let totalInputTokens = 0;
  let totalOutputTokens = 0;
  let totalReasoningTokens = 0;
  
  for (const session of sessions) {
    const messages = await getMessages(session.id);
    totalTurns += messages.length;
    
    for (const msg of messages) {
      if (msg.info.role === "assistant" && msg.info.tokens) {
        totalInputTokens += msg.info.tokens.input;
        totalOutputTokens += msg.info.tokens.output;
        totalReasoningTokens += msg.info.tokens.reasoning;
      }
    }
  }
  
  return {
    totalSessions: sessions.length,
    totalTurns,
    totalTokens: {
      input: totalInputTokens,
      output: totalOutputTokens,
      reasoning: totalReasoningTokens,
    },
    averageTurnsPerSession: Math.round(totalTurns / sessions.length),
    averageTokensPerSession: Math.round((totalInputTokens + totalOutputTokens + totalReasoningTokens) / sessions.length),
    oldestSession: sessions[sessions.length - 1] ?? null,
    newestSession: sessions[0] ?? null,
  };
}

// ---------------------------------------------------------------------------
// Formatters
// ---------------------------------------------------------------------------

function formatTime(epoch: number): string {
  return new Date(epoch).toISOString();
}

function formatDuration(startMs: number, endMs: number): string {
  const diffS = Math.floor((endMs - startMs) / 1000);
  if (diffS < 60) return `${diffS}s`;
  if (diffS < 3600) return `${Math.floor(diffS / 60)}m ${diffS % 60}s`;
  const h = Math.floor(diffS / 3600);
  const m = Math.floor((diffS % 3600) / 60);
  return `${h}h ${m}m`;
}

function formatSession(session: Session, verbose = false): string {
  const lines = [
    `ID: ${session.id}`,
    `  Title:   ${session.title}`,
    `  Created: ${formatTime(session.time.created)}`,
    `  Updated: ${formatTime(session.time.updated)}`,
    `  Duration: ${formatDuration(session.time.created, session.time.updated)}`,
  ];

  if (session.parentID) {
    lines.push(`  Parent:  ${session.parentID}`);
  }

  if (session.summary) {
    lines.push(
      `  Changes: +${session.summary.additions} -${session.summary.deletions} (${session.summary.files} files)`
    );
  }

  if (session.shared) {
    lines.push(`  Shared:  ${session.shareUrl ?? "yes"}`);
  }

  if (verbose) {
    lines.push(`  (use 'messages ${session.id}' to view transcript)`);
  }

  return lines.join("\n");
}

function formatMessage(msg: { info: Message; parts: Part[] }): string {
  const role = msg.info.role.toUpperCase();
  const time = formatTime(msg.info.time?.created ?? Date.now());
  
  let details = "";
  if (msg.info.role === "assistant") {
    const model = msg.info.providerID && msg.info.modelID 
      ? `${msg.info.providerID}/${msg.info.modelID}`
      : "unknown";
    details = ` [${model}]`;
    
    if (msg.info.tokens) {
      const total = msg.info.tokens.input + msg.info.tokens.output + msg.info.tokens.reasoning;
      details += ` ${total.toLocaleString()} tokens`;
    }
  }
  
  return `${role}${details} @ ${time}`;
}

// ---------------------------------------------------------------------------
// CLI Commands
// ---------------------------------------------------------------------------

async function cmdList(options: { limit?: number; json?: boolean }): Promise<void> {
  const sessions = await listSessions();
  const limited = options.limit ? sessions.slice(0, options.limit) : sessions;
  
  if (options.json) {
    console.log(JSON.stringify(limited, null, 2));
    return;
  }
  
  if (limited.length === 0) {
    console.log("No sessions found.");
    return;
  }
  
  console.log(`Total sessions: ${sessions.length}${options.limit ? ` (showing ${limited.length})` : ""}\n`);
  
  for (const session of limited) {
    console.log(formatSession(session, true));
    console.log();
  }
}

async function cmdGet(sessionID: string, options: { json?: boolean }): Promise<void> {
  const session = await getSession(sessionID);
  
  if (!session) {
    console.error(`Session not found: ${sessionID}`);
    process.exit(1);
  }
  
  if (options.json) {
    console.log(JSON.stringify(session, null, 2));
    return;
  }
  
  console.log(formatSession(session, true));
}

async function cmdChildren(sessionID: string, options: { json?: boolean }): Promise<void> {
  const children = await getChildSessions(sessionID);
  
  if (options.json) {
    console.log(JSON.stringify(children, null, 2));
    return;
  }
  
  if (children.length === 0) {
    console.log(`No child sessions for: ${sessionID}`);
    return;
  }
  
  console.log(`Child sessions of ${sessionID}: ${children.length}\n`);
  
  for (const child of children) {
    console.log(formatSession(child));
    console.log();
  }
}

async function cmdCreate(options: { title?: string; parent?: string }): Promise<void> {
  const session = await createSession({
    title: options.title,
    parentID: options.parent,
  });
  
  console.log(`Created session:`);
  console.log(`  ID:    ${session.id}`);
  console.log(`  Title: ${session.title}`);
  if (session.parentID) {
    console.log(`  Parent: ${session.parentID}`);
  }
}

async function cmdUpdate(sessionID: string, updates: { title?: string }): Promise<void> {
  const session = await updateSession(sessionID, updates);
  
  console.log(`Updated session:`);
  console.log(formatSession(session));
}

async function cmdDelete(sessionID: string): Promise<void> {
  const deleted = await deleteSession(sessionID);
  
  if (!deleted) {
    console.error(`Session not found: ${sessionID}`);
    process.exit(1);
  }
  
  console.log(`Deleted session: ${sessionID}`);
}

async function cmdAbort(sessionID: string): Promise<void> {
  const aborted = await abortSession(sessionID);
  
  if (!aborted) {
    console.error(`Session not found: ${sessionID}`);
    process.exit(1);
  }
  
  console.log(`Aborted session: ${sessionID}`);
}

async function cmdShare(sessionID: string): Promise<void> {
  const session = await shareSession(sessionID);
  
  console.log(`Shared session:`);
  console.log(`  ID:  ${session.id}`);
  console.log(`  URL: ${session.shareUrl ?? "(not available)"}`);
}

async function cmdUnshare(sessionID: string): Promise<void> {
  await unshareSession(sessionID);
  console.log(`Unshared session: ${sessionID}`);
}

async function cmdSummarize(sessionID: string, options: { instruction?: string }): Promise<void> {
  const summarized = await summarizeSession(sessionID, {
    instruction: options.instruction,
  });
  
  if (!summarized) {
    console.error(`Session not found: ${sessionID}`);
    process.exit(1);
  }
  
  console.log(`Summarization started for: ${sessionID}`);
}

async function cmdMessages(sessionID: string, options: { limit?: number; json?: boolean }): Promise<void> {
  const session = await getSession(sessionID);
  if (!session) {
    console.error(`Session not found: ${sessionID}`);
    process.exit(1);
  }
  
  const messages = await getMessages(sessionID);
  const limited = options.limit ? messages.slice(0, options.limit) : messages;
  
  if (options.json) {
    console.log(JSON.stringify(limited, null, 2));
    return;
  }
  
  console.log(`Session: ${session.title}`);
  console.log(`Messages: ${messages.length}${options.limit ? ` (showing ${limited.length})` : ""}\n`);
  
  for (const msg of limited) {
    console.log(formatMessage(msg));
  }
}

async function cmdMessage(sessionID: string, messageID: string, options: { json?: boolean }): Promise<void> {
  const msg = await getMessage(sessionID, messageID);
  
  if (!msg) {
    console.error(`Message not found: ${messageID} in session ${sessionID}`);
    process.exit(1);
  }
  
  if (options.json) {
    console.log(JSON.stringify(msg, null, 2));
    return;
  }
  
  console.log(formatMessage(msg));
  console.log();
  console.log("Parts:", msg.parts.length);
  for (const part of msg.parts) {
    console.log(`  - ${part.type}${part.text ? `: ${part.text.slice(0, 100)}` : ""}`);
  }
}

async function cmdPrompt(sessionID: string, message: string, options: { noReply?: boolean; outputFormat?: string }): Promise<void> {
  const result = await sendPrompt(sessionID, message, {
    noReply: options.noReply,
    outputFormat: options.outputFormat,
  });
  
  console.log(JSON.stringify(result, null, 2));
}

async function cmdCommand(sessionID: string, command: string, args: string[]): Promise<void> {
  const result = await sendCommand(sessionID, command, args);
  
  console.log(JSON.stringify(result, null, 2));
}

async function cmdShell(sessionID: string, command: string): Promise<void> {
  const result = await runShell(sessionID, command);
  
  console.log(JSON.stringify(result, null, 2));
}

async function cmdRevert(sessionID: string, messageID: string): Promise<void> {
  const session = await revertMessage(sessionID, messageID);
  
  console.log(`Reverted message ${messageID} in session ${session.id}`);
}

async function cmdUnrevert(sessionID: string): Promise<void> {
  const session = await unrevertSession(sessionID);
  
  console.log(`Unreverted session: ${session.id}`);
}

async function cmdInit(sessionID: string, options: { analyze?: boolean; createAgentsMd?: boolean }): Promise<void> {
  const initialized = await initSession(sessionID, {
    analyze: options.analyze,
    createAgentsMd: options.createAgentsMd,
  });
  
  if (!initialized) {
    console.error(`Session not found: ${sessionID}`);
    process.exit(1);
  }
  
  console.log(`Initialized session: ${sessionID}`);
}

async function cmdPermission(
  sessionID: string,
  permissionID: string,
  response: "allow" | "deny" | "allow-session" | "deny-session"
): Promise<void> {
  const responded = await respondToPermission(sessionID, permissionID, response);
  
  if (!responded) {
    console.error(`Permission not found: ${permissionID} in session ${sessionID}`);
    process.exit(1);
  }
  
  console.log(`Responded to permission ${permissionID}: ${response}`);
}

async function cmdStats(options: { json?: boolean }): Promise<void> {
  const stats = await getStats();
  
  if (options.json) {
    console.log(JSON.stringify(stats, null, 2));
    return;
  }
  
  console.log("Session Statistics");
  console.log("==================\n");
  console.log(`Total sessions:     ${stats.totalSessions}`);
  console.log(`Total turns:        ${stats.totalTurns.toLocaleString()}`);
  console.log(`Total tokens:       ${(stats.totalTokens.input + stats.totalTokens.output + stats.totalTokens.reasoning).toLocaleString()}`);
  console.log(`  - Input:          ${stats.totalTokens.input.toLocaleString()}`);
  console.log(`  - Output:         ${stats.totalTokens.output.toLocaleString()}`);
  console.log(`  - Reasoning:      ${stats.totalTokens.reasoning.toLocaleString()}`);
  console.log(`Avg turns/session:  ${stats.averageTurnsPerSession}`);
  console.log(`Avg tokens/session: ${stats.averageTokensPerSession.toLocaleString()}`);
  
  if (stats.oldestSession) {
    console.log(`\nOldest session:     ${stats.oldestSession.title} (${formatTime(stats.oldestSession.time.created)})`);
  }
  if (stats.newestSession) {
    console.log(`Newest session:     ${stats.newestSession.title} (${formatTime(stats.newestSession.time.updated)})`);
  }
}

function printHelp(): void {
  console.log(`
Session Management CLI Harness - Full API

Usage:
  opx-session <command> [options]

Session Management:
  list [--limit N] [--json]              List all sessions
  get <session-id> [--json]              Get session details
  children <session-id> [--json]         List child sessions
  create [--title "title"] [--parent]    Create a new session
  update <session-id> [--title "new"]    Update session properties
  delete <session-id>                    Delete a session
  abort <session-id>                     Abort a running session
  share <session-id>                     Share a session
  unshare <session-id>                   Unshare a session
  summarize <session-id> [--instruction] Start session summarization
  init <session-id> [--analyze]          Initialize session (analyze & AGENTS.md)

Messages:
  messages <session-id> [--limit N]      List messages in session
  message <session-id> <message-id>      Get single message details

Interaction:
  prompt <session-id> <message> [--no-reply] [--output-format]
  command <session-id> <command> [args]  Send command to session
  shell <session-id> <command>           Run shell command in session

History:
  revert <session-id> <message-id>       Revert a message
  unrevert <session-id>                  Restore reverted messages

Permissions:
  permission <session-id> <permission-id> <allow|deny|allow-session|deny-session>

Statistics:
  stats [--json]                         Show session statistics

Options:
  --json         Output as JSON
  --limit N      Limit results
  --no-reply     Don't wait for AI response (prompt only)
  --output-format  Request structured output format

Environment:
  OPENCODE_BASE_URL   Server URL (default: http://localhost:4096)
  OPENCODE_API_KEY    API key for authentication

Examples:
  opx-session list --limit 10
  opx-session messages ses_abc123 --json
  opx-session create --title "test" --parent ses_xyz
  opx-session prompt ses_abc123 "hello" --no-reply
  opx-session stats
`);
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args.includes("--help") || args.includes("-h")) {
    printHelp();
    return;
  }
  
  const command = args[0];
  const options: Record<string, string | boolean | number> = {};
  const positional: string[] = [];
  
  // Parse arguments
  for (let i = 1; i < args.length; i++) {
    const arg = args[i];
    
    if (arg.startsWith("--")) {
      const key = arg.slice(2);
      const nextArg = args[i + 1];
      
      if (nextArg && !nextArg.startsWith("--")) {
        if (!isNaN(Number(nextArg))) {
          options[key] = Number(nextArg);
        } else {
          options[key] = nextArg;
        }
        i++;
      } else {
        options[key] = true;
      }
    } else if (arg.startsWith("-") && arg.length === 2) {
      // Short flag - skip for now (not implemented)
    } else {
      positional.push(arg);
    }
  }
  
  try {
    switch (command) {
      case "list":
        await cmdList({
          limit: options.limit as number | undefined,
          json: !!options.json,
        });
        break;
        
      case "get":
        if (!positional[0]) {
          console.error("Error: session ID required");
          process.exit(1);
        }
        await cmdGet(positional[0], { json: !!options.json });
        break;
        
      case "children":
        if (!positional[0]) {
          console.error("Error: session ID required");
          process.exit(1);
        }
        await cmdChildren(positional[0], { json: !!options.json });
        break;
        
      case "create":
        await cmdCreate({
          title: options.title as string | undefined,
          parent: options.parent as string | undefined,
        });
        break;
        
      case "update":
        if (!positional[0]) {
          console.error("Error: session ID required");
          process.exit(1);
        }
        await cmdUpdate(positional[0], {
          title: options.title as string | undefined,
        });
        break;
        
      case "delete":
        if (!positional[0]) {
          console.error("Error: session ID required");
          process.exit(1);
        }
        await cmdDelete(positional[0]);
        break;
        
      case "abort":
        if (!positional[0]) {
          console.error("Error: session ID required");
          process.exit(1);
        }
        await cmdAbort(positional[0]);
        break;
        
      case "share":
        if (!positional[0]) {
          console.error("Error: session ID required");
          process.exit(1);
        }
        await cmdShare(positional[0]);
        break;
        
      case "unshare":
        if (!positional[0]) {
          console.error("Error: session ID required");
          process.exit(1);
        }
        await cmdUnshare(positional[0]);
        break;
        
      case "summarize":
        if (!positional[0]) {
          console.error("Error: session ID required");
          process.exit(1);
        }
        await cmdSummarize(positional[0], {
          instruction: options.instruction as string | undefined,
        });
        break;
        
      case "init":
        if (!positional[0]) {
          console.error("Error: session ID required");
          process.exit(1);
        }
        await cmdInit(positional[0], {
          analyze: !!options.analyze,
          createAgentsMd: !!options["create-agents-md"] || !!options.createAgentsMd,
        });
        break;
        
      case "messages":
        if (!positional[0]) {
          console.error("Error: session ID required");
          process.exit(1);
        }
        await cmdMessages(positional[0], {
          limit: options.limit as number | undefined,
          json: !!options.json,
        });
        break;
        
      case "message":
        if (!positional[0] || !positional[1]) {
          console.error("Error: session ID and message ID required");
          process.exit(1);
        }
        await cmdMessage(positional[0], positional[1], { json: !!options.json });
        break;
        
      case "prompt":
        if (!positional[0] || !positional[1]) {
          console.error("Error: session ID and message required");
          process.exit(1);
        }
        await cmdPrompt(positional[0], positional[1], {
          noReply: !!options["no-reply"] || !!options.noReply,
          outputFormat: options["output-format"] as string | undefined,
        });
        break;
        
      case "command":
        if (!positional[0] || !positional[1]) {
          console.error("Error: session ID and command required");
          process.exit(1);
        }
        await cmdCommand(positional[0], positional[1], positional.slice(2));
        break;
        
      case "shell":
        if (!positional[0] || !positional[1]) {
          console.error("Error: session ID and command required");
          process.exit(1);
        }
        await cmdShell(positional[0], positional[1]);
        break;
        
      case "revert":
        if (!positional[0] || !positional[1]) {
          console.error("Error: session ID and message ID required");
          process.exit(1);
        }
        await cmdRevert(positional[0], positional[1]);
        break;
        
      case "unrevert":
        if (!positional[0]) {
          console.error("Error: session ID required");
          process.exit(1);
        }
        await cmdUnrevert(positional[0]);
        break;
        
      case "permission":
        if (!positional[0] || !positional[1] || !positional[2]) {
          console.error("Error: session ID, permission ID, and response required");
          process.exit(1);
        }
        await cmdPermission(
          positional[0],
          positional[1],
          positional[2] as "allow" | "deny" | "allow-session" | "deny-session"
        );
        break;
        
      case "stats":
        await cmdStats({ json: !!options.json });
        break;
        
      default:
        console.error(`Unknown command: ${command}`);
        console.error("Run with --help for usage");
        process.exit(1);
    }
  } catch (error: any) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

// Export for programmatic use
export {
  listSessions,
  getSession,
  getChildSessions,
  createSession,
  updateSession,
  deleteSession,
  abortSession,
  shareSession,
  unshareSession,
  summarizeSession,
  getMessages,
  getMessage,
  sendPrompt,
  sendCommand,
  runShell,
  revertMessage,
  unrevertSession,
  initSession,
  respondToPermission,
  getStats,
};

// Run CLI only when this file is executed directly.
if (import.meta.main) {
  main();
}
