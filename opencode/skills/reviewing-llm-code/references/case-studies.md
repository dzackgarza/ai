# Case Studies: Idiotic Code Decisions and Anti-Patterns

This document catalog-grounds LLM and agent failure modes into concrete "Case Studies" derived from real-world codebase audits. These examples demonstrate what "idiotic" code looks like, why it is structurally or behaviorally deficient, and the trivial solutions that should have been utilized instead.

Use these case studies to prime reviews and calibrate findings against actual codebase failures.

---

## Case Study 1: The Monolithic Frontend (React App.tsx "God-Object")

### The Anti-Pattern
Concentrating an entire web application's UI, layouts, modal dialogues, preferences menus, explorer drawers, and complex event handlers into a single massive file (e.g., `src/client/App.tsx` exceeding 1,600 lines) with inline state instantiation for every dialog.

#### Brittle Code Shape (Before)
```tsx
// src/client/App.tsx - A single massive 1600+ line component
export default function App() {
  const [markdownText, setMarkdownText] = useState("");
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [settingsFlags, setSettingsFlags] = useState("");
  const [isDiagramOpen, setIsDiagramOpen] = useState(false);
  const [diagramTemplate, setDiagramTemplate] = useState("tikz");
  // ... 15+ more pieces of state managing unrelated dialogs ...

  return (
    <div className="app-container">
      <Sidebar />
      <Editor value={markdownText} />
      
      {/* Inline monolithic instantiation of Settings Modal */}
      {isSettingsOpen && (
        <div className="modal">
          <input 
            value={settingsFlags} 
            onChange={(e) => setSettingsFlags(e.target.value)} 
          />
          <button onClick={() => saveFlags(settingsFlags)}>Save</button>
        </div>
      )}

      {/* Inline monolithic instantiation of Diagram Modal */}
      {isDiagramOpen && (
        <div className="modal">
          <select value={diagramTemplate} onChange={...}>
            <option value="tikz">TikZ</option>
          </select>
          <button onClick={...}>Insert</button>
        </div>
      )}
    </div>
  );
}
```

### Why This Is Idiotic
1. **State Pollution and Re-render Thrashes**: React is built around component composition and state isolation. Housing all state slices in a single top-level parent component forces the entire page, editor pane, explorer drawer, and terminal sidebar to completely re-render on every single keystroke inside a modal's text field.
2. **Extreme Blast Radius**: Modifying a simple configuration field inside the settings menu has a huge blast radius. An accidental type error or render crash inside the settings modal code takes down the entire editor application.
3. **Cognitive Overload**: A 1,600+ line file is impossible for subsequent agents or human maintainers to reason about, leading to patch accretion and regression bugs.

### The Correct / Trivial Solution
Decompose the monolithic file into small, single-responsibility, and self-contained React components that encapsulate their own UI state, logic, and triggers.

#### Remediated Code Shape (After)
```tsx
// src/client/components/SettingsDialog.tsx
import React, { useState } from 'react';

interface SettingsDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (flags: string) => void;
}

export function SettingsDialog({ isOpen, onClose, onSave }: SettingsDialogProps) {
  const [flags, setFlags] = useState("");
  if (!isOpen) return null;

  return (
    <div className="modal">
      <input value={flags} onChange={(e) => setFlags(e.target.value)} />
      <button onClick={() => { onSave(flags); onClose(); }}>Save</button>
    </div>
  );
}
```

---

## Case Study 2: Needless Imperative Complexity (Hand-rolling a Synchronous FZF on Node's Event Loop)

### The Anti-Pattern
Hand-rolling a recursive, synchronous directory-traversal function using blocking filesystem operations, and executing this recursion inside an Express routing handler on **every single keystroke** from a quick-open search box.

#### Brittle Code Shape (Before)
```typescript
// src/server/index.ts
import fs from 'fs';
import path from 'path';

// Recursively lists all markdown files synchronously
function collectMarkdownFiles(dir: string): string[] {
  let results: string[] = [];
  const list = fs.readdirSync(dir); // BLOCKS the event loop
  for (const file of list) {
    const filePath = path.resolve(dir, file);
    const stat = fs.statSync(filePath); // BLOCKS the event loop
    if (stat && stat.isDirectory()) {
      results = results.concat(collectMarkdownFiles(filePath));
    } else if (file.endsWith('.md')) {
      results.push(filePath);
    }
  }
  return results;
}

app.get('/api/files/quick-open', (req, res) => {
  const query = (req.query.q as string || '').toLowerCase();
  const allFiles = collectMarkdownFiles(process.cwd()); // Recalculates synchronously on every single character type
  const matched = allFiles.filter(f => f.toLowerCase().includes(query));
  res.json({ files: matched });
});
```

### Why This Is Idiotic
1. **Event Loop Starvation**: Node.js is single-threaded. Doing recursive, synchronous disk I/O blocks all incoming and outgoing event-loop traffic. If the user opens a workspace containing more than a few dozen files, typing a single query freezes the entire web application, dropping editor keystrokes and delaying live previews.
2. **Dependency Aversion**: Re-implementing directory indexing and recursive scanning from scratch is a classic failure to look for existing mature solutions. 

### The Correct / Trivial Solution
Delegate file searching to a highly-optimized external system tool (like `fzf`, `find`, or `fd` via asynchronous spawns) or utilize a mature, non-blocking asynchronous library (like `fast-glob` or Node's asynchronous `fs.promises` generator) with caching or proper debounce gates.

#### Remediated Code Shape (After)
```typescript
import glob from 'fast-glob';

app.get('/api/files/quick-open', async (req, res) => {
  const query = (req.query.q as string || '').toLowerCase();
  // Performs a non-blocking asynchronous file scan
  const files = await glob('**/*.md', { 
    cwd: process.cwd(), 
    absolute: true, 
    ignore: ['**/node_modules/**', '**/.git/**'] 
  });
  const matched = files.filter(f => f.toLowerCase().includes(query));
  res.json({ files: matched });
});
```

---

## Case Study 3: Timing Assertion Theater (Test Inflation to Fake Responsiveness)

### The Anti-Pattern
Adding E2E integration tests that make arbitrary, hard-coded performance or timing assertions (e.g., asserting a UI interaction executes in less than 50 milliseconds) to claim that "responsiveness" is tested and verified.

#### Brittle Code Shape (Before)
```typescript
// src/tests/responsiveness.spec.ts
import { test, expect } from '@playwright/test';

test('quick-open dialog is highly responsive', async ({ page }) => {
  await page.goto('/');
  await page.keyboard.press('Control+P');
  
  const startTime = Date.now();
  await page.keyboard.type('test.md');
  const elapsed = Date.now() - startTime;
  
  // IDIOTIC: Asserting arbitrary timing bounds
  expect(elapsed).toBeLessThan(50); 
});
```

### Why This Is Idiotic
1. **Pure Test Theater**: Since the user never requested a specific performance constraint and there is no observed bug relating to latency limits, this assertion is artificial and arbitrary.
2. **Extreme Flakiness**: The E2E test runs locally or in CI environments under heavily fluctuating workloads. Hard-coded millisecond bounds introduce chronic, transient test failures (flakiness) that do not reflect actual code correctness.
3. **Masking Root-Cause Failures**: This "responsiveness" check passes on tiny, empty test folders, completely masking the fact that the underlying implementation (like Case Study 2) uses a synchronous blocking loop that grinds to a halt on real-world workspaces.

### The Correct / Trivial Solution
Remove timing checks from correctness/unit tests entirely. Correctness suites must prove functional invariants (e.g., that searching triggers a network request, results render, and selection loads the file). Performance limits belong in decoupled CI benchmarking pipelines, not assertions.

#### Remediated Code Shape (After)
```typescript
test('quick-open dialog correctly filters and displays files', async ({ page }) => {
  await page.goto('/');
  await page.keyboard.press('Control+P');
  await page.keyboard.type('test.md');
  
  // Assert actual functional outcomes instead of timing
  const item = page.locator('.file-item', { hasText: 'test.md' });
  await expect(item).toBeVisible();
});
```

---

## Case Study 4: Regex Against Semantic Formats (Parsing HTML with Flat Strings)

### The Anti-Pattern
Flattening a highly hierarchical, semantic structure (like HTML) into a raw byte stream and using regular expressions to manipulate or rewrite element attributes (like asset `src` tags).

#### Brittle Code Shape (Before)
```typescript
function withPreviewAssetUrls(html: string) {
  // IDIOTIC: Rewriting HTML src attributes using regex
  return html.replace(
    /\bsrc=(["'])(?![A-Za-z][A-Za-z\d+.-]*:|\/|#)([^"']+)\1/g,
    (_match, quote: string, url: string) =>
      `src=${quote}/api/preview-assets?path=${encodeURIComponent(url)}${quote}`,
  );
}
```

### Why This Is Idiotic
1. **Hierarchical Destruction**: HTML is not a regular language. A simple regex replacement breaks on perfectly valid markup such as multi-line tags, nested scripts/strings containing `src=` text, element comments containing reference markers, or complex protocol formatting.
2. **Bypassing the Semantic Layer**: The system already owns a rich AST or DOM representation (or could easily adopt one like `cheerio` or `jsdom`). Refusing to use the semantic parser represents dependency aversion and introduces major security/escaping bugs.

### The Correct / Trivial Solution
Leverage a DOM parsing library or native URL/path APIs to cleanly extract and transform attributes without flattening the hierarchy.

#### Remediated Code Shape (After)
```typescript
import * as cheerio from 'cheerio';

function withPreviewAssetUrls(html: string) {
  const $ = cheerio.load(html);
  $('img, script, iframe').each((_, elem) => {
    const src = $(elem).attr('src');
    if (src && !src.startsWith('/') && !/^[A-Za-z][A-Za-z\d+.-]*:/.test(src)) {
      $(elem).attr('src', `/api/preview-assets?path=${encodeURIComponent(src)}`);
    }
  });
  return $.html();
}
```

---

## Case Study 5: Debounced Keystroke Network Spam (Spaghetti Data Flow)

### The Anti-Pattern
Firing highly frequent, network-bound HTTP requests (`/api/backup` or `/api/autosave`) on every single keystroke via a debounced client-side `useEffect` hook, rather than writing to a local-first buffer.

#### Brittle Code Shape (Before)
```typescript
// src/client/App.tsx
useEffect(() => {
  const handle = window.setTimeout(() => {
    // IDIOTIC: Spams the network on every single keystroke
    void fetch('/api/backup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ markdown: markdownText }),
    });
  }, 500); // Fires every 500ms during typing
  return () => window.clearTimeout(handle);
}, [markdownText]);
```

### Why This Is Idiotic
1. **Resource Starvation**: Flooding the Express server with HTTP POST requests during rapid typing spikes network utilization, increases CPU overhead, and wastes bandwidth.
2. **Latency Sensitivity**: If the client's network experiences minor packet loss or jitter, multiple debounced backup requests can resolve out of order, leading to server-side race conditions or file corruption.

### The Correct / Trivial Solution
Store live keystroke buffers locally in browser memory (`localStorage` or `IndexedDB`). Limit network backups to natural, low-frequency event boundaries (such as window focus loss, editor idle states > 10 seconds, or explicit user-saves).

#### Remediated Code Shape (After)
```typescript
// Client-side auto-save backup utilizing local storage
useEffect(() => {
  // Instantly backup locally to guard against browser crash
  localStorage.setItem('markdown_backup', markdownText);
}, [markdownText]);

// Only backup to the server on focus loss or explicit save
const handleWindowBlur = () => {
  void fetch('/api/backup', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ markdown: markdownText }),
  });
};
```

---

## Case Study 6: Hand-Rolling Atomic Writes (Dependency Aversion)

### The Anti-Pattern
Writing a custom atomic file writer using temporary file generation, manual locking, and rename chains.

#### Brittle Code Shape (Before)
```typescript
// src/server/workspace.ts
import fs from 'fs';
import path from 'path';

export function saveFileAtomic(filePath: string, content: string) {
  const tempPath = `${filePath}.tmp.${Date.now()}`;
  try {
    fs.writeFileSync(tempPath, content);
    fs.renameSync(tempPath, filePath);
  } catch (err) {
    if (fs.existsSync(tempPath)) {
      fs.unlinkSync(tempPath);
    }
    throw err;
  }
}
```

### Why This Is Idiotic
Atomic file writing is notoriously hard to get right. Standard implementation details include cross-platform permission preservation, dealing with incomplete fsync flushing, handling temporary naming collisions, clean lock recovery, and cleanups during process termination. Hand-rolling it invites data corruption or data loss in production environments.

### The Correct / Trivial Solution
Do not reinvent file-integrity abstractions. Use the standard, heavily-tested community package `write-file-atomic`.

#### Remediated Code Shape (After)
```typescript
import writeFileAtomic from 'write-file-atomic';

export function saveFileAtomic(filePath: string, content: string) {
  // Thread-safe, system-safe, atomic file writing out-of-the-box
  writeFileAtomic.sync(filePath, content);
}
```

---

## Case Study 7: Blind URL Proxying (Severe SSRF Security Flaw)

### The Anti-Pattern
Creating an Express endpoint that serves as a proxy for client-provided URLs (e.g. for TikZ or LaTeX rendering tools) and blindly downloading and serving content from whatever domain is requested.

#### Brittle Code Shape (Before)
```typescript
// src/server/index.ts
import axios from 'axios';

app.get('/api/diagram/proxy', async (req, res) => {
  const targetUrl = req.query.url as string;
  // IDIOTIC: Blindly fetching any URL provided by the client
  const response = await axios.get(targetUrl);
  res.send(response.data);
});
```

### Why This Is Idiotic
This is a classic, textbook Server-Side Request Forgery (SSRF) vulnerability. An attacker can supply local loopback URLs (like `http://localhost:8080/admin` or `http://127.0.0.1:22/`) or internal network IPs to bypass external firewall protections and perform port scans, system administration, or data exfiltration from behind the host machine.

### The Correct / Trivial Solution
Establish strict domain whitelisting to only permit requests to trusted, verified external service URLs (e.g., `q.uiver.app` or `freetikz.app`). Allow loopback URLs exclusively under strict `NODE_ENV === 'test'` environments.

#### Remediated Code Shape (After)
```typescript
app.get('/api/diagram/proxy', async (req, res) => {
  const targetUrl = req.query.url as string;
  const parsed = new URL(targetUrl);

  // Strict host-level whitelisting
  const allowedHosts = ['q.uiver.app', 'freetikz.app'];
  const isTest = process.env.NODE_ENV === 'test';
  
  const isAllowed = allowedHosts.includes(parsed.hostname) || 
                    (isTest && (parsed.hostname === 'localhost' || parsed.hostname === '127.0.0.1'));

  if (!isAllowed) {
    return res.status(403).send('Forbidden: Target host not whitelisted.');
  }

  const response = await axios.get(targetUrl);
  res.send(response.data);
});
```

---

## Case Study 8: ESM Type Compilation SyntaxError (Type-Value Confusion)

### The Anti-Pattern
Importing or exporting a pure TypeScript interface or type as a standard runtime value in a Node.js Native ESM codebase, which compiles cleanly but crashes instantly at runtime.

#### Brittle Code Shape (Before)
```typescript
// src/shared/command-parser.ts
export interface ParsedFlags {
  math: boolean;
  filter: string[];
}

// src/client/components/SettingsDialog.tsx
// IDIOTIC: Importing TS interface as a standard value in native ESM
import { ParsedFlags } from '../../shared/command-parser';
```

### Why This Is Idiotic
TypeScript types and interfaces are completely erased during JavaScript compilation. In native Node.js ESM environments, referencing a non-existent runtime value inside an `import` or `export` statement triggers a fatal, unrecoverable `SyntaxError` at boot time. The agent did not test the compiled JS production bundle, checking only that the TS compiler was happy.

### The Correct / Trivial Solution
Always import and export TypeScript types and interfaces utilizing the explicit `type` modifier to ensure correct compiler erasure and prevent runtime syntax crashes.

#### Remediated Code Shape (After)
```typescript
// src/client/components/SettingsDialog.tsx
// Safe type-only import ensures clean erasure during compilation
import type { ParsedFlags } from '../../shared/command-parser';
```
