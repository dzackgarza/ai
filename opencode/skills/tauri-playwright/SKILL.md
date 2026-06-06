---
name: tauri-playwright
description: Use when setting up or debugging Playwright E2E testing for Tauri desktop apps using tauri-plugin-playwright. Triggers on Tauri testing, Playwright integration, native webview automation, or CI/CD for desktop apps.
---

# Tauri Playwright E2E Testing

Behavioral policy for testing Tauri apps with Playwright via tauri-plugin-playwright. Controls the real native webview (WKWebView, WebView2, WebKitGTK) with Playwright-compatible API.

## Core Policy

- Three testing modes from same test files: `browser` (headless Chromium, mocked IPC), `tauri` (socket bridge to real webview), `cdp` (Windows WebView2 direct CDP)
- The Rust plugin embeds a socket server in the Tauri app; TypeScript fixture connects via Unix socket or TCP
- Browser mode runs without Tauri (fast CI); Tauri mode requires running app; CDP mode Windows-only
- All actions auto-wait for visibility/enabled (5s default); assertions auto-retry
- Native screenshots use CoreGraphics (macOS) capturing real window; video via native frame capture + ffmpeg

## Decision Procedures

### Mode Selection

- **CI / fast feedback** → `browser` mode (no Rust build, headless Chromium)
- **True E2E / native behavior** → `tauri` mode (real webview, native screenshots)
- **Windows full Playwright API** → `cdp` mode (WebView2 CDP, full native Playwright)

### Project Setup Order

1. Add Rust plugin with optional `e2e-testing` feature flag
2. Install `@srsholmes/tauri-playwright` + `@playwright/test` npm packages
3. Create test fixtures with `createTauriTest()` configuring `devUrl`, `ipcMocks`, `mcpSocket`
4. Write tests using `tauriPage` fixture (extends Playwright Page with Tauri methods)
5. Configure `playwright.config.ts` with projects per mode
6. Run: browser mode standalone; Tauri mode requires `cargo tauri dev --features e2e-testing` in separate terminal

### IPC Mocking Strategy

- Mock all Tauri `invoke()` commands in browser mode via `ipcMocks` object
- Include plugin commands: `'plugin:fs|read'`, `'plugin:dialog|open'`
- Use `getCapturedInvokes(tauriPage)` to assert IPC calls were made
- Clear with `clearCapturedInvokes(tauriPage)` between tests

### Socket Configuration

- Default: Unix socket at `/tmp/tauri-playwright.sock`
- Custom: `PluginConfig::new().socket_path("/tmp/custom.sock").tcp_port(6274)`
- Fixture `mcpSocket` must match plugin socket path

## Environment Traps

| Trap | Mitigation |
|------|------------|
| Tauri 2.0 requires `"withGlobalTauri": true` in `tauri.conf.json` | Verify before setup; plugin won't connect otherwise |
| macOS screen recording permission required for native screenshots | Grant in System Settings → Privacy → Screen Recording |
| ffmpeg required for video stitching | Install via package manager; video fails silently without it |
| Socket file persists after test crashes | Clean `/tmp/tauri-playwright.sock` in test teardown or CI before run |
| `tauriPage` fixture not available in browser mode without fixture setup | Always use `createTauriTest()` fixture, not raw `@playwright/test` |
| WebView2 CDP needs `--remote-debugging-port=9222` env var | Set `WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS` before `cargo tauri dev` |
| Tauri mode needs dev server running on `devUrl` port | Configure `webServer` in playwright.config.ts with `reuseExistingServer` |

## Required Outputs

- **Setup**: Cargo.toml with optional feature, lib.rs plugin init, tauri.conf.json withGlobalTauri
- **Fixtures**: e2e/fixtures.ts exporting `test`, `expect` from `createTauriTest()`
- **Tests**: e2e/tests/*.spec.ts using `tauriPage` fixture with semantic selectors
- **Config**: playwright.config.ts with `projects` array for each mode, `webServer` for dev URL
- **CI**: GitHub Actions workflow running browser mode on ubuntu, Tauri mode on macOS

## Validation Checklist

- [ ] `tauri.conf.json` has `"withGlobalTauri": true`
- [ ] Rust plugin added with `optional = true` and feature-gated init
- [ ] `createTauriTest()` fixture created with `devUrl`, `ipcMocks`, `mcpSocket`
- [ ] Tests use `tauriPage` fixture (not `page`) for Tauri-specific methods
- [ ] `playwright.config.ts` defines projects: `browser-only`, `tauri`, optionally `cdp`
- [ ] `webServer` command starts Tauri dev server on correct port
- [ ] CI runs browser mode on ubuntu, Tauri mode on macOS
- [ ] Native screenshot/video artifacts uploaded in CI
- [ ] Socket path matches between plugin config and fixture `mcpSocket`

## Anti-Patterns

| Pattern | Why Bad | Do Instead |
|---------|---------|------------|
| Using raw `page` fixture instead of `tauriPage` | Loses Tauri IPC mocking, semantic selectors, native screenshots | Always use fixture from `createTauriTest()` |
| Hardcoding selectors without data-testid | Brittle; breaks on UI changes | Use `getByTestId`, `getByRole`, `getByText` semantic selectors |
| Running Tauri mode without dev server | Tests fail with connection errors | Configure `webServer` in playwright.config.ts |
| Forgetting `withGlobalTauri: true` | Plugin cannot inject JS into webview | Verify in tauri.conf.json before debugging |
| Not cleaning socket file between runs | "Address already in use" errors | Add cleanup step or use unique socket path per test run |
| Mocking only some IPC commands | Unmocked commands hang or error | Mock all `invoke()` calls used by tested code paths |
| Using CDP mode on non-Windows | WebView2 only on Windows | Guard CDP project with `process.platform === 'win32'` |

## Plugin API Essentials

- `tauri_plugin_playwright::init()` — default Unix socket
- `tauri_plugin_playwright::init_with_config(PluginConfig)` — custom socket/TCP
- `PluginConfig::new().socket_path(path).tcp_port(port)`
- Socket protocol: JSON-RPC over Unix socket / HTTP polling fallback

## Detailed API Reference

### Page Methods (all auto-wait 5s default)

**Interactions**: `click`, `dblclick`, `hover`, `fill`, `type`, `press`, `check`, `uncheck`, `selectOption`, `focus`, `blur`, `dragAndDrop`, `dispatchEvent`

**Queries** (auto-wait for element): `textContent`, `innerHTML`, `innerText`, `inputValue`, `getAttribute`, `boundingBox`, `getComputedStyle`, `allTextContents`

**State Checks** (instant, no waiting): `isVisible`, `isHidden`, `isChecked`, `isDisabled`, `isEnabled`, `isEditable`, `isFocused`, `count`

**Navigation**: `goto`, `reload`, `goBack`, `goForward`, `waitForURL`, `title`, `url`, `content`

**Waiting**: `waitForSelector`, `waitForFunction`, `waitForURL`

**Evaluate**: `evaluate<T>('window.innerWidth')`

### Semantic Selectors

`getByTestId`, `getByText`, `getByRole`, `getByLabel`, `getByPlaceholder`, `getByAltText`, `getByTitle`

### Locator API

**Actions**: `click`, `fill`, `press`, `clear`, `pressSequentially`, `dispatchEvent`

**Queries**: `textContent`, `innerText`, `inputValue`, `getAttribute`, `evaluate`

**State**: `isVisible`, `isChecked`, `isFocused`

**Refinement**: `nth`, `first`, `last`, `filter`, `all`

**Nesting**: `locator`, `getByTestId`, `getByText`

**Scrolling**: `scrollIntoViewIfNeeded`

### Assertions (auto-retry 5s default)

**Visibility**: `toBeVisible`, `toBeHidden`, `not.toBeVisible`

**Content**: `toContainText`, `toHaveText` (exact)

**Form**: `toHaveValue`, `toBeChecked`, `toBeEnabled`, `toBeDisabled`, `toBeEditable`, `toBeFocused`, `toBeEmpty`

**Attributes**: `toHaveAttribute`, `toHaveClass`, `toHaveCSS`, `toHaveId`

**Collections**: `toHaveCount`, `toBeAttached`

**Page-level**: `toHaveURL`, `toHaveTitle`

### Keyboard & Mouse

`keyboard.press`, `keyboard.type`, `keyboard.down`, `keyboard.up`, `mouse.click`, `mouse.dblclick`, `mouse.move`, `mouse.wheel`

### Network Mocking

`route(url, {status, body, contentType})`, `getNetworkRequests()`, `unroute`, `clearRoutes`

### Dialog Handling

`installDialogHandler({defaultConfirm, defaultPromptText})`, `getDialogs()`

### File Upload

`setInputFiles(selector, [{name, mimeType, buffer}])`

### Screenshots & Video

`screenshot()`, `screenshot({path})` — native CoreGraphics on macOS
`startRecording({path, fps})`, `stopRecording()` — native frame capture → ffmpeg → MP4
Auto-captures on failure, attaches to Playwright HTML report

### IPC Mocking (Browser Mode)

Mock any `invoke()` including plugin commands:
```typescript
ipcMocks: {
  greet: (args) => `Hello, ${args?.name}!`,
  'plugin:fs|read': () => 'file contents',
  'plugin:dialog|open': () => '/path/to/file',
}
```
Assert calls: `getCapturedInvokes(tauriPage)`, `clearCapturedInvokes(tauriPage)`

## Requirements

- **Tauri 2.0** with `"withGlobalTauri": true` in `tauri.conf.json`
- **Node.js 18+**
- **Rust toolchain** (for Tauri mode)
- **ffmpeg** (optional, for video stitching)
- **Screen recording permission** on macOS (for native screenshots)

## Canonical Reference Implementation (Bundled at `references/hello-world/`)

The bundled example is the ground truth for what a correct tauri-playwright setup looks like. Agents should recognize these patterns when inspecting a project:

**Project Structure:**
```
references/hello-world/
├── package.json              # @srsholmes/tauri-playwright as workspace dep, @playwright/test, scripts
├── tsconfig.json             # strict, ESNext, bundler moduleResolution
├── vite.config.ts            # port 1420, proxy for /pw-poll and /pw to localhost:6275
├── index.html                # minimal, mounts React root
├── src/
│   ├── main.tsx              # ReactDOM.render <App />
│   ├── App.tsx               # demo app: counter, greet IPC, todo, modal, upload, dialogs, drag-drop, API fetch
│   └── lib/
│       └── tauri.ts          # typed `invoke` wrapper exporting `api.greet(name: string)`
├── src-tauri/
│   ├── Cargo.toml            # optional `e2e-testing` feature, tauri-plugin-playwright path dep
│   ├── tauri.conf.json       # withGlobalTauri: true, devUrl: http://localhost:1420, devtools: true
│   └── src/
│       ├── main.rs           # thin entry calling lib::run()
│       └── lib.rs            # greet command + #[cfg(feature = "e2e-testing")] plugin init
└── e2e/
    ├── fixtures.ts           # createTauriTest with devUrl, ipcMocks, ipcContext, mcpSocket, tauriCwd
    ├── playwright.config.ts  # 3 projects: browser-only (mode:browser), tauri (mode:tauri), cdp (mode:cdp)
    └── tests/
        ├── counter.spec.ts   # basic click + textContent assertions
        ├── greet.spec.ts     # IPC round-trip, fill, click, Enter key
        ├── todo.spec.ts      # form, list, allTextContents, count, remove
        └── kitchen-sink.spec.ts  # comprehensive: title/url/content, geometry, evaluate, screenshots, failure artifacts
```

**Pattern Recognition — what correct implementations contain:**

| File | Required Patterns |
|------|-------------------|
| `tauri.conf.json` | `"withGlobalTauri": true`, `devUrl: "http://localhost:1420"`, `devtools: true` |
| `Cargo.toml` | `e2e-testing = ["tauri-plugin-playwright"]` feature, `tauri-plugin-playwright = { path = "...", optional = true }` |
| `lib.rs` | `#[cfg(feature = "e2e-testing")] builder.plugin(tauri_plugin_playwright::init())` |
| `fixtures.ts` | `createTauriTest({ devUrl, ipcMocks, ipcContext, mcpSocket, tauriCwd })` |
| `playwright.config.ts` | `projects: [{name: 'browser-only', use: {mode: 'browser'}}, {name: 'tauri', use: {mode: 'tauri'}}]`, `webServer: {command: 'pnpm dev', port: 1420, cwd: '..'}` |
| `vite.config.ts` | `server: {port: 1420, proxy: {'/pw-poll': 'http://127.0.0.1:6275', '/pw': 'http://127.0.0.1:6275'}}` |

## Architecture (Mental Model)

```
┌──────────────────┐  socket/JSON  ┌──────────────────────────────────┐
│  Playwright       │◄────────────►│  tauri-plugin-playwright          │
│  test runner      │              │  (Rust, embedded in your app)     │
│                   │              │                                   │
│  @srsholmes/      │              │  Socket server → JS injection     │
│  tauri-playwright │              │  HTTP polling  ← JS results       │
└──────────────────┘              └──────────────────────────────────┘
```

**Key insight**: The Rust plugin injects a JS bridge into the webview. Playwright talks to the bridge via socket. In `browser` mode, the fixture mocks the bridge entirely (no Tauri needed). In `tauri` mode, it talks to the real injected bridge. In `cdp` mode (Windows), Playwright connects directly to WebView2's CDP.