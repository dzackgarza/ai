#!/usr/bin/env node
// Drives the user's already-running, already-logged-in Chrome/Chromium over CDP to
// consult ChatGPT and extract the response: attach over CDP, create/reuse a tab,
// attach the prompt as a real file upload (not a pasted string — avoids composer-fill
// length/truncation issues), submit via a native DOM click on the send button
// (Playwright's synthetic Enter/click paths are unreliable against this composer),
// then poll the last conversation turn for text-stability past the thinking-placeholder
// state before extracting. Does not touch a dedicated browser profile and does not use
// temporary chat mode: the user's real, already-authenticated browser and conversation
// history are the required substrate.
//
// This script trusts the caller to use it reasonably; it does not implement proof
// machinery (nonces, hashes, model-allowlists) to guard against misuse. It does assert
// on expected page structure at each step and dumps diagnostic data on failure so a
// human/agent can update the selectors when ChatGPT's UI changes.
//
// Usage:
//   New consultation:
//     node chatgpt_cdp_consult.js --prompt-file <path> [--message <text>]
//       [--endpoint http://127.0.0.1:9222] [--max-wait-ms 480000] [--out <path>]
//
//   Follow-up in an existing conversation:
//     node chatgpt_cdp_consult.js --conversation-url <url> --prompt-file <path> ...
//
//   Resume polling an in-flight response without resubmitting (e.g. after a prior
//   run's wait window elapsed — check its `finalUrl` field):
//     node chatgpt_cdp_consult.js --conversation-url <url> --poll-only ...

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { createRequire } = require('module');

const LOCK_DIR = '/tmp/chatgpt-cdp-consult.lock';
const DEFAULT_MESSAGE = 'See the attached brief and respond according to its instructions.';
// Known transient status strings ChatGPT shows before real content exists. This list
// is not exhaustive — ChatGPT has several short tool-status labels ("Searching",
// "Reading documents", "Analyzing", ...) depending on what the model is doing — so
// completion detection also requires a minimum text length (see MIN_REAL_ANSWER_LEN)
// as a general safety net rather than trying to enumerate every possible status label.
const PLACEHOLDER_TEXTS = new Set(['pro thinking', 'thinking', 'thinking...', 'reading documents', 'reading document', '']);
const MIN_REAL_ANSWER_LEN = 30;

// page.evaluate() has no built-in timeout and can hang indefinitely against a
// long-held CDP connection (a click evaluate() call has sat for 6+ minutes with zero
// progress against a page object held open across several prior awaits, while a fresh
// connectOverCDP + evaluate against the same tab resolved in under a second). Wrap
// evaluate calls so a genuine stall fails loudly with a clear error instead of
// hanging the whole script.
function evaluateWithTimeout(page, fn, arg, ms = 15000) {
  const evalPromise = arg === undefined ? page.evaluate(fn) : page.evaluate(fn, arg);
  const timeoutPromise = new Promise((_, reject) => {
    setTimeout(() => reject(new Error(`page.evaluate() did not resolve within ${ms}ms (stale CDP connection?)`)), ms);
  });
  return Promise.race([evalPromise, timeoutPromise]);
}

function loadPlaywright() {
  // Resolve dynamically instead of hard-coding a specific Node version's global
  // package path (that broke portability across Node upgrades/other machines). Try a
  // direct require first, then fall back to the globally installed @playwright/cli,
  // which bundles its own playwright dependency.
  try {
    return require('playwright');
  } catch (directRequireError) {
    let globalRoot;
    try {
      globalRoot = execSync('npm root -g', { encoding: 'utf8' }).trim();
    } catch (npmError) {
      throw new Error(`playwright not resolvable: no direct dependency, and 'npm root -g' failed: ${npmError.message}`);
    }
    const cliPkg = path.join(globalRoot, '@playwright', 'cli', 'package.json');
    if (!fs.existsSync(cliPkg)) {
      throw new Error(`playwright not resolvable: no direct dependency and no @playwright/cli found at ${cliPkg}. Install with: npm install -g @playwright/cli`);
    }
    return createRequire(cliPkg)('playwright');
  }
}

function parseArgs(argv) {
  const args = { endpoint: 'http://127.0.0.1:9222', maxWaitMs: 480000, message: DEFAULT_MESSAGE };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--prompt-file') args.promptFile = argv[++i];
    else if (a === '--message') args.message = argv[++i];
    else if (a === '--endpoint') args.endpoint = argv[++i];
    else if (a === '--max-wait-ms') args.maxWaitMs = Number(argv[++i]);
    else if (a === '--out') args.out = argv[++i];
    else if (a === '--conversation-url') args.conversationUrl = argv[++i];
    else if (a === '--poll-only') args.pollOnly = true;
    else throw new Error(`unknown argument: ${a}`);
  }
  if (!args.pollOnly && !args.promptFile) {
    throw new Error('--prompt-file is required unless --poll-only is set (the prompt is attached as a file, never inlined into a shell command)');
  }
  return args;
}

function acquireLock() {
  try {
    fs.mkdirSync(LOCK_DIR);
  } catch (error) {
    if (error.code === 'EEXIST') throw new Error(`frontier model session busy: lock held at ${LOCK_DIR}`);
    throw error;
  }
}

function releaseLock() {
  try {
    fs.rmdirSync(LOCK_DIR);
  } catch (error) {
    // already gone or never created; not fatal
  }
}

async function dumpDiagnostics(page, label) {
  try {
    const testids = await page.evaluate(() => {
      const ids = Array.from(document.querySelectorAll('[data-testid]')).map((el) => el.getAttribute('data-testid'));
      return [...new Set(ids)].slice(0, 80);
    });
    const shotPath = `/tmp/chatgpt-cdp-consult-diagnostic-${Date.now()}.png`;
    await page.screenshot({ path: shotPath }).catch(() => {});
    return { label, url: page.url(), visibleTestids: testids, screenshot: shotPath };
  } catch (error) {
    return { label, error: String(error) };
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const endpointHost = new URL(args.endpoint).hostname;
  if (!['127.0.0.1', 'localhost', '::1'].includes(endpointHost)) {
    throw new Error(`CDP endpoint host '${endpointHost}' is not loopback; refusing to attach to a non-local endpoint`);
  }

  const { chromium } = loadPlaywright();
  const out = { endpoint: args.endpoint };
  let browser;
  let page;

  acquireLock();
  try {
    const versionResponse = await fetch(args.endpoint + '/json/version');
    if (!versionResponse.ok) throw new Error(`CDP endpoint not reachable: HTTP ${versionResponse.status}`);
    const version = await versionResponse.json();
    if (!version.webSocketDebuggerUrl) throw new Error('CDP endpoint has no webSocketDebuggerUrl');

    browser = await chromium.connectOverCDP(args.endpoint, { timeout: 10000, noDefaults: true });
    out.connected = true;
    const context = browser.contexts()[0];
    if (!context) throw new Error('CDP browser has no existing browser context');

    page = await context.newPage();
    await page.bringToFront();
    const targetUrl = args.conversationUrl || 'https://chatgpt.com/';
    await page.goto(targetUrl, { waitUntil: 'domcontentloaded', timeout: 45000 });
    await page.waitForTimeout(7000);

    const pre = await evaluateWithTimeout(page, () => {
      const text = document.body?.innerText || '';
      return {
        hasLogin: /\bLog in\b|\bSign up\b/i.test(text),
        hasPromptBox: /Ask anything|Message ChatGPT/i.test(text) || document.querySelectorAll('textarea, [contenteditable="true"]').length > 0,
      };
    });
    out.pre = pre;
    if (pre.hasLogin) throw new Error('ChatGPT session is logged out in this browser; abort (do not attempt credential entry)');

    if (!args.pollOnly) {
      if (!pre.hasPromptBox) {
        out.diagnostics = await dumpDiagnostics(page, 'composer not found');
        throw new Error('No composer found on page; see out.diagnostics for the visible testids/screenshot to update this script against the current ChatGPT UI');
      }

      // Attach the prompt as a real file upload rather than pasting it into the
      // composer: this sidesteps composer-fill length/truncation concerns entirely.
      // #upload-files is ChatGPT's general (non-image-only) hidden file input.
      const fileInput = page.locator('#upload-files');
      const fileInputExists = await fileInput.count();
      if (!fileInputExists) {
        out.diagnostics = await dumpDiagnostics(page, 'file input not found');
        throw new Error('#upload-files not found on page; see out.diagnostics — ChatGPT UI likely changed, update the selector');
      }
      await fileInput.setInputFiles(path.resolve(args.promptFile));

      const box = page.locator('#prompt-textarea, textarea, [contenteditable="true"]').last();
      await box.waitFor({ state: 'visible', timeout: 15000 });
      await box.fill(args.message, { timeout: 15000 });

      // The send button stays disabled while the attached file is still uploading
      // server-side, even after its chip has visually finished rendering. Clicking
      // send before the button is actually enabled was observed to silently no-op
      // (the click event fires, but no message posts) — so poll for the real
      // enabled state instead of a fixed guess-length wait.
      const uploadReady = await (async () => {
        for (let i = 0; i < 20; i++) {
          const disabled = await evaluateWithTimeout(page, () => {
            const btn = document.querySelector('button[data-testid="send-button"], button[aria-label="Send prompt"]');
            return btn ? btn.disabled : null;
          }, undefined, 10000);
          if (disabled === false) return true;
          await page.waitForTimeout(1000);
        }
        return false;
      })();
      out.uploadReady = uploadReady;
      if (!uploadReady) {
        out.diagnostics = await dumpDiagnostics(page, 'send button never became enabled (upload stuck?)');
        throw new Error('send button did not become enabled within 20s of attaching the file; see out.diagnostics');
      }

      // Submit via a native DOM click dispatched inside the page, not Playwright's
      // synthetic mouse/keyboard input. Both `page.keyboard.press('Enter')` and
      // Playwright's `locator.click()` (force or not) are unreliable against this
      // composer: Enter intermittently gets swallowed, raw mouse coordinates from
      // getBoundingClientRect() land off target, and locator.click() times out
      // waiting for the element to be "stable" because the composer never stops
      // micro-animating. `element.click()` invoked via page.evaluate() bypasses all
      // of that and reliably triggers React's onClick handler.
      const clickResult = await evaluateWithTimeout(page, () => {
        const btn = document.querySelector('button[data-testid="send-button"], button[aria-label="Send prompt"]');
        if (!btn) return { found: false };
        btn.click();
        return { found: true, disabledAfter: btn.disabled };
      }, undefined, 20000);
      out.submit = clickResult;
      if (!clickResult.found) {
        out.diagnostics = await dumpDiagnostics(page, 'send button not found');
        throw new Error('send button not found on page; see out.diagnostics — update the selector against the current ChatGPT UI');
      }

      // Confirm the click actually produced a new conversation turn (not just that
      // the DOM click event fired) before moving on to the completion-poll loop.
      const submitConfirmed = await (async () => {
        for (let i = 0; i < 15; i++) {
          const turnCount = await evaluateWithTimeout(page, () => document.querySelectorAll('[data-testid^="conversation-turn-"]').length, undefined, 10000);
          if (turnCount >= 1) return true;
          await page.waitForTimeout(1000);
        }
        return false;
      })();
      out.submitConfirmed = submitConfirmed;
      if (!submitConfirmed) {
        out.diagnostics = await dumpDiagnostics(page, 'click fired but no conversation turn appeared within 15s');
        throw new Error('send button click did not produce a conversation turn within 15s; see out.diagnostics — the click may have silently no-op\'d');
      }
    }

    // Completion signal: neither a global "Thinking" text match nor a "Stop
    // generating" button-text match proved reliable — the former can keep matching a
    // leftover collapsed reasoning-summary element well after the real answer
    // finished, and the latter never reliably went true even while actively
    // streaming. Bare turn-text stability is not enough either: the "Pro thinking"
    // placeholder itself sits static for a few seconds before streaming starts.
    // Require text stability AND that the stable text is not a known placeholder.
    const startingTurnCount = args.pollOnly ? 0 : (args.conversationUrl ? await evaluateWithTimeout(page, () => document.querySelectorAll('[data-testid^="conversation-turn-"]').length) : 0);
    const requiredTurnCount = args.pollOnly ? Math.max(1, startingTurnCount) : startingTurnCount + 2;
    const start = Date.now();
    let last = null;
    let prevTurnText = null;
    let stableCount = 0;
    while (Date.now() - start < args.maxWaitMs) {
      await page.waitForTimeout(1500);
      last = await evaluateWithTimeout(page, () => {
        const body = document.body?.innerText || '';
        const turnEls = document.querySelectorAll('[data-testid^="conversation-turn-"]');
        const lastEl = turnEls[turnEls.length - 1];
        return {
          turnCount: turnEls.length,
          lastTurnText: lastEl ? (lastEl.innerText || lastEl.textContent || '').trim() : null,
          stopVisible: /Stop (generating|answering)|Stop streaming/i.test(body),
          hasError: /Something went wrong|There was an error|Unable to load/i.test(body),
        };
      }, undefined, 20000);
      if (last.hasError) break;
      // Exclude known placeholder strings AND require a minimum length: ChatGPT has
      // several short transient tool-status labels beyond the ones we've directly
      // observed ("Searching", "Analyzing", ...), so a length floor generalizes
      // against the whole class instead of chasing each label individually.
      const isPlaceholder = last.lastTurnText
        && (PLACEHOLDER_TEXTS.has(last.lastTurnText.trim().toLowerCase()) || last.lastTurnText.trim().length < MIN_REAL_ANSWER_LEN);
      if (last.turnCount >= requiredTurnCount && !last.stopVisible && last.lastTurnText && !isPlaceholder) {
        stableCount = last.lastTurnText === prevTurnText ? stableCount + 1 : 0;
        prevTurnText = last.lastTurnText;
        if (stableCount >= 2) break;
      } else {
        stableCount = 0;
        prevTurnText = last.lastTurnText;
      }
    }
    out.waitState = last;
    out.responseDetected = Boolean(last && last.turnCount >= requiredTurnCount && !last.stopVisible && stableCount >= 2 && !last.hasError);

    out.turns = await evaluateWithTimeout(page, () => {
      const els = Array.from(document.querySelectorAll('[data-testid^="conversation-turn-"]'));
      return els.map((el, idx) => ({
        idx,
        testid: el.getAttribute('data-testid'),
        role: el.getAttribute('data-message-author-role')
          || el.querySelector('[data-message-author-role]')?.getAttribute('data-message-author-role')
          || null,
        text: (el.innerText || el.textContent || '').trim(),
      }));
    });
    out.latestTurnText = out.turns.length ? out.turns[out.turns.length - 1].text : null;
    out.finalUrl = page.url();

    if (!out.responseDetected && !last?.hasError) {
      // The wait window elapsed without confirmed completion. Report the conversation
      // URL so the caller can resume polling this same conversation instead of
      // resubmitting the prompt (resubmitting duplicates an already-in-flight,
      // possibly-expensive consultation).
      out.resumeHint = `node ${path.basename(__filename)} --conversation-url ${out.finalUrl} --poll-only --max-wait-ms <longer>`;
    }
  } catch (error) {
    out.error = String((error && (error.stack || error.message)) || error);
  } finally {
    releaseLock();
    try {
      if (page) await page.close();
      out.closedCreatedPage = true;
    } catch (error) {
      out.closeError = String(error);
    }
    try {
      if (browser) await browser.close(); // detaches from CDP; does not close the real browser
      out.detached = true;
    } catch (error) {
      out.detachError = String(error);
    }
  }

  const json = JSON.stringify(out, null, 2);
  if (args.out) fs.writeFileSync(args.out, json);
  console.log(json);
  process.exit(out.error ? 1 : 0);
}

main();
