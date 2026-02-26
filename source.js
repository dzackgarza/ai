```
#!/usr/bin/env node
/**
* @file free-coding-models.js
* @description Live terminal availability checker for coding LLM models with OpenCode & OpenClaw integration.
*
* @details
* This CLI tool discovers and benchmarks language models optimized for coding.
* It runs in an alternate screen buffer, pings all models in parallel, re-pings successful ones
* multiple times for reliable latency measurements, and prints a clean final table.
* During benchmarking, users can navigate with arrow keys and press Enter to act on the selected model.
*
* 🎯 Key features:
* - Parallel pings across all models with animated real-time updates (multi-provider)
* - Continuous monitoring with 2-second ping intervals (never stops)
* - Rolling averages calculated from ALL successful pings since start
* - Best-per-tier highlighting with medals (🥇🥈🥉)
* - Interactive navigation with arrow keys directly in the table
* - Instant OpenCode OR OpenClaw action on Enter key press
* - Startup mode menu (OpenCode CLI vs OpenCode Desktop vs OpenClaw) when no flag is given
* - Automatic config detection and model setup for both tools
* - JSON config stored in ~/.free-coding-models.json (auto-migrates from old plain-text)
* - Multi-provider support via sources.js (NIM/Groq/Cerebras/OpenRouter/Hugging Face/Replicate/DeepInfra/... — extensible)
* - Settings screen (P key) to manage API keys, provider toggles, analytics, and manual updates
* - Favorites system: toggle with F, pin rows to top, persist between sessions
* - Uptime percentage tracking (successful pings / total pings)
* - Sortable columns (R/Y/O/M/L/A/S/N/H/V/B/U keys)
* - Tier filtering via T key (cycles S+→S→A+→A→A-→B+→B→C→All)
*
* → Functions:
* - `loadConfig` / `saveConfig` / `getApiKey`: Multi-provider JSON config via lib/config.js
* - `promptTelemetryConsent`: First-run consent flow for anonymous analytics
* - `getTelemetryDistinctId`: Generate/reuse a stable anonymous ID for telemetry
* - `getTelemetryTerminal`: Infer terminal family (Terminal.app, iTerm2, kitty, etc.)
* - `isTelemetryDebugEnabled` / `telemetryDebug`: Optional runtime telemetry diagnostics via env
* - `sendUsageTelemetry`: Fire-and-forget anonymous app-start event
* - `ensureFavoritesConfig` / `toggleFavoriteModel`: Persist and toggle pinned favorites
* - `promptApiKey`: Interactive wizard for first-time multi-provider API key setup
* - `promptModeSelection`: Startup menu to choose OpenCode vs OpenClaw
* - `buildPingRequest` / `ping`: Build provider-specific probe requests and measure latency
* - `renderTable`: Generate ASCII table with colored latency indicators and status emojis
* - `getAvg`: Calculate average latency from all successful pings
* - `getVerdict`: Determine verdict string based on average latency (Overloaded for 429)
* - `getUptime`: Calculate uptime percentage from ping history
* - `sortResults`: Sort models by various columns
* - `checkNvidiaNimConfig`: Check if NVIDIA NIM provider is configured in OpenCode
* - `isTcpPortAvailable` / `resolveOpenCodeTmuxPort`: Pick a safe OpenCode port when running in tmux
* - `startOpenCode`: Launch OpenCode CLI with selected model (configures if needed)
* - `startOpenCodeDesktop`: Set model in shared config & open OpenCode Desktop app
* - `loadOpenClawConfig` / `saveOpenClawConfig`: Manage ~/.openclaw/openclaw.json
* - `startOpenClaw`: Set selected model as default in OpenClaw config (remote, no launch)
* - `filterByTier`: Filter models by tier letter prefix (S, A, B, C)
* - `main`: Orchestrates CLI flow, wizard, ping loops, animation, and output
*
* 📦 Dependencies:
* - Node.js 18+ (native fetch)
* - chalk: Terminal styling and colors
* - readline: Interactive input handling
* - sources.js: Model definitions from all providers
*
* ⚙️ Configuration:
* - API keys stored per-provider in ~/.free-coding-models.json (0600 perms)
* - Old ~/.free-coding-models plain-text auto-migrated as nvidia key on first run
* - Env vars override config: NVIDIA_API_KEY, GROQ_API_KEY, CEREBRAS_API_KEY, OPENROUTER_API_KEY, HUGGINGFACE_API_KEY/HF_TOKEN, REPLICATE_API_TOKEN, DEEPINFRA_API_KEY/DEEPINFRA_TOKEN, FIREWORKS_API_KEY, SILICONFLOW_API_KEY, TOGETHER_API_KEY, PERPLEXITY_API_KEY, etc.
* - Cloudflare Workers AI requires both CLOUDFLARE_API_TOKEN (or CLOUDFLARE_API_KEY) and CLOUDFLARE_ACCOUNT_ID
* - Models loaded from sources.js — all provider/model definitions are centralized there
* - OpenCode config: ~/.config/opencode/opencode.json
* - OpenClaw config: ~/.openclaw/openclaw.json
* - Ping timeout: 15s per attempt
* - Ping interval: 2 seconds (continuous monitoring mode)
* - Animation: 12 FPS with braille spinners
*
* 🚀 CLI flags:
* - (no flag): Show startup menu → choose OpenCode or OpenClaw
* - --opencode: OpenCode CLI mode (launch CLI with selected model)
* - --opencode-desktop: OpenCode Desktop mode (set model & open Desktop app)
* - --openclaw: OpenClaw mode (set selected model as default in OpenClaw)
* - --best: Show only top-tier models (A+, S, S+)
* - --fiable: Analyze 10s and output the most reliable model
* - --no-telemetry: Disable anonymous usage analytics for this run
* - --tier S/A/B/C: Filter models by tier letter (S=S+/S, A=A+/A/A-, B=B+/B, C=C)
*
* @see {@link https://build.nvidia.com} NVIDIA API key generation
* @see {@link https://github.com/opencode-ai/opencode} OpenCode repository
* @see {@link https://openclaw.ai} OpenClaw documentation
*/

import chalk from 'chalk'
import { createRequire } from 'module'
import { readFileSync, writeFileSync, existsSync, copyFileSync, mkdirSync } from 'fs'
import { randomUUID } from 'crypto'
import { homedir } from 'os'
import { join, dirname } from 'path'
import { createServer } from 'net'
import { MODELS, sources } from '../sources.js'
import { patchOpenClawModelsJson } from '../patch-openclaw-models.js'
import { getAvg, getVerdict, getUptime, getP95, getJitter, getStabilityScore, sortResults, filterByTier, findBestModel, parseArgs, TIER_ORDER, VERDICT_ORDER, TIER_LETTER_MAP } from '../lib/utils.js'
import { loadConfig, saveConfig, getApiKey, isProviderEnabled } from '../lib/config.js'

const require = createRequire(import.meta.url)
const readline = require('readline')

// ─── Version check ────────────────────────────────────────────────────────────
const pkg = require('../package.json')
const LOCAL_VERSION = pkg.version
const TELEMETRY_CONSENT_VERSION = 1
const TELEMETRY_TIMEOUT = 1_200
const POSTHOG_CAPTURE_PATH = '/i/v0/e/'
const POSTHOG_DEFAULT_HOST = 'https://eu.i.posthog.com'
// 📖 Consent ASCII banner shown before telemetry choice to make first-run intent explicit.
const TELEMETRY_CONSENT_ASCII = [
'███████ ██████ ███████ ███████ ██████ ██████ ██████ ██ ███ ██ ██████ ███ ███ ██████ ██████ ███████ ██ ███████',
'██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ████ ██ ██ ████ ████ ██ ██ ██ ██ ██ ██ ██',
'█████ ██████ █████ █████ █████ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ███ █████ ██ ████ ██ ██ ██ ██ ██ █████ ██ ███████',
'██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██',
'██ ██ ██ ███████ ███████ ██████ ██████ ██████ ██ ██ ████ ██████ ██ ██ ██████ ██████ ███████ ███████ ███████',
'',
'',
]
// 📖 Maintainer defaults for global npm telemetry (safe to publish: project key is a public ingest token).
const POSTHOG_PROJECT_KEY_DEFAULT = 'phc_5P1n8HaLof6nHM0tKJYt4bV5pj2XPb272fLVigwf1YQ'
const POSTHOG_HOST_DEFAULT = 'https://eu.i.posthog.com'

// 📖 parseTelemetryEnv: Convert env var strings into booleans.
// 📖 Returns true/false when value is recognized, otherwise null.
function parseTelemetryEnv(value) {
if (typeof value !== 'string') return null
const normalized = value.trim().toLowerCase()
if (['1', 'true', 'yes', 'on'].includes(normalized)) return true
if (['0', 'false', 'no', 'off'].includes(normalized)) return false
return null
}

// 📖 Optional debug switch for telemetry troubleshooting (disabled by default).
function isTelemetryDebugEnabled() {
return parseTelemetryEnv(process.env.FREE_CODING_MODELS_TELEMETRY_DEBUG) === true
}

// 📖 Writes telemetry debug traces to stderr only when explicitly enabled.
function telemetryDebug(message, meta = null) {
if (!isTelemetryDebugEnabled()) return
const prefix = '[telemetry-debug]'
if (meta === null) {
process.stderr.write(`${prefix} ${message}\n`)
return
}
try {
process.stderr.write(`${prefix} ${message} ${JSON.stringify(meta)}\n`)
} catch {
process.stderr.write(`${prefix} ${message}\n`)
}
}

// 📖 Ensure telemetry config shape exists even on old config files.
function ensureTelemetryConfig(config) {
if (!config.telemetry || typeof config.telemetry !== 'object') {
config.telemetry = { enabled: null, consentVersion: 0, anonymousId: null }
}
if (typeof config.telemetry.enabled !== 'boolean') config.telemetry.enabled = null
if (typeof config.telemetry.consentVersion !== 'number') config.telemetry.consentVersion = 0
if (typeof config.telemetry.anonymousId !== 'string' || !config.telemetry.anonymousId.trim()) {
config.telemetry.anonymousId = null
}
}

// 📖 Ensure favorites config shape exists and remains clean.
// 📖 Stored format: ["providerKey/modelId", ...] in insertion order.
function ensureFavoritesConfig(config) {
if (!Array.isArray(config.favorites)) config.favorites = []
const seen = new Set()
config.favorites = config.favorites.filter((entry) => {
if (typeof entry !== 'string' || entry.trim().length === 0) return false
if (seen.has(entry)) return false
seen.add(entry)
return true
})
}

// 📖 Build deterministic key used to persist one favorite model row.
function toFavoriteKey(providerKey, modelId) {
return `${providerKey}/${modelId}`
}

// 📖 Sync per-row favorite metadata from config (used by renderer and sorter).
function syncFavoriteFlags(results, config) {
ensureFavoritesConfig(config)
const favoriteRankMap = new Map(config.favorites.map((entry, index) => [entry, index]))
for (const row of results) {
const favoriteKey = toFavoriteKey(row.providerKey, row.modelId)
const rank = favoriteRankMap.get(favoriteKey)
row.favoriteKey = favoriteKey
row.isFavorite = rank !== undefined
row.favoriteRank = rank !== undefined ? rank : Number.MAX_SAFE_INTEGER
}
}

// 📖 Toggle favorite state and persist immediately.
// 📖 Returns true when row is now favorite, false when removed.
function toggleFavoriteModel(config, providerKey, modelId) {
ensureFavoritesConfig(config)
const favoriteKey = toFavoriteKey(providerKey, modelId)
const existingIndex = config.favorites.indexOf(favoriteKey)
if (existingIndex >= 0) {
config.favorites.splice(existingIndex, 1)
saveConfig(config)
return false
}
config.favorites.push(favoriteKey)
saveConfig(config)
return true
}

// 📖 Create or reuse a persistent anonymous distinct_id for PostHog.
// 📖 Stored locally in config so one user is stable over time without personal data.
function getTelemetryDistinctId(config) {
ensureTelemetryConfig(config)
if (config.telemetry.anonymousId) return config.telemetry.anonymousId

config.telemetry.anonymousId = `anon_${randomUUID()}`
saveConfig(config)
return config.telemetry.anonymousId
}

// 📖 Convert Node platform to human-readable system name for analytics segmentation.
function getTelemetrySystem() {
if (process.platform === 'darwin') return 'macOS'
if (process.platform === 'win32') return 'Windows'
if (process.platform === 'linux') return 'Linux'
return process.platform
}

// 📖 Infer terminal family from environment hints for coarse usage segmentation.
// 📖 Never sends full env dumps; only a normalized terminal label is emitted.
function getTelemetryTerminal() {
const termProgramRaw = (process.env.TERM_PROGRAM || '').trim()
const termProgram = termProgramRaw.toLowerCase()
const term = (process.env.TERM || '').toLowerCase()

if (termProgram === 'apple_terminal') return 'Terminal.app'
if (termProgram === 'iterm.app') return 'iTerm2'
if (termProgram === 'warpterminal' || process.env.WARP_IS_LOCAL_SHELL_SESSION) return 'Warp'
if (process.env.WT_SESSION) return 'Windows Terminal'
if (process.env.KITTY_WINDOW_ID || term.includes('kitty')) return 'kitty'
if (process.env.GHOSTTY_RESOURCES_DIR || term.includes('ghostty')) return 'Ghostty'
if (process.env.WEZTERM_PANE || termProgram === 'wezterm') return 'WezTerm'
if (process.env.KONSOLE_VERSION || termProgram === 'konsole') return 'Konsole'
if (process.env.GNOME_TERMINAL_SCREEN || termProgram === 'gnome-terminal') return 'GNOME Terminal'
if (process.env.TERMINAL_EMULATOR === 'JetBrains-JediTerm') return 'JetBrains Terminal'
if (process.env.TABBY_CONFIG_DIRECTORY || termProgram === 'tabby') return 'Tabby'
if (termProgram === 'vscode' || process.env.VSCODE_GIT_IPC_HANDLE) return 'VS Code Terminal'
if (process.env.ALACRITTY_SOCKET || term.includes('alacritty') || termProgram === 'alacritty') return 'Alacritty'
if (term.includes('foot') || termProgram === 'foot') return 'foot'
if (termProgram === 'hyper' || process.env.HYPER) return 'Hyper'
if (process.env.TMUX) return 'tmux'
if (process.env.STY) return 'screen'
// 📖 Generic fallback for many terminals exposing TERM_PROGRAM (e.g., Rio, Contour, etc.).
if (termProgramRaw) return termProgramRaw
if (term) return term

return 'unknown'
}

// 📖 Prompt consent on first run (or when consent schema version changes).
// 📖 This prompt is skipped when the env var explicitly controls telemetry.
async function promptTelemetryConsent(config, cliArgs) {
if (cliArgs.noTelemetry) return

const envTelemetry = parseTelemetryEnv(process.env.FREE_CODING_MODELS_TELEMETRY)
if (envTelemetry !== null) return

ensureTelemetryConfig(config)
const hasStoredChoice = typeof config.telemetry.enabled === 'boolean'
const isConsentCurrent = config.telemetry.consentVersion >= TELEMETRY_CONSENT_VERSION
if (hasStoredChoice && isConsentCurrent) return

// 📖 Non-interactive runs should never hang waiting for input.
if (!process.stdin.isTTY || !process.stdout.isTTY) {
// 📖 Do not mutate persisted consent in headless runs.
// 📖 We simply skip the prompt; runtime telemetry remains governed by env/config precedence.
return
}

const options = [
{ label: 'Accept & Continue', value: true, emoji: '💖🥰💖' },
{ label: 'Reject and Continue', value: false, emoji: '😢' },
]
let selected = 0 // 📖 Default selection is Accept & Continue.

const accepted = await new Promise((resolve) => {
const render = () => {
const EL = '\x1b[K'
const lines = []
for (const asciiLine of TELEMETRY_CONSENT_ASCII) {
lines.push(chalk.greenBright(asciiLine))
}
lines.push(chalk.greenBright(`free-coding-models (v${LOCAL_VERSION})`))
lines.push(chalk.greenBright('Welcome ! Would you like to help improve the app and fix bugs by activating PostHog telemetry (anonymous & secure)'))
lines.push(chalk.greenBright("anonymous telemetry analytics (we don't collect anything from you)"))
lines.push('')

for (let i = 0; i < options.length; i++) {
const isSelected = i === selected
const option = options[i]
const buttonText = `${option.emoji} ${option.label}`

let button
if (isSelected && option.value) button = chalk.black.bgGreenBright(` ${buttonText} `)
else if (isSelected && !option.value) button = chalk.black.bgRedBright(` ${buttonText} `)
else if (option.value) button = chalk.greenBright(` ${buttonText} `)
else button = chalk.redBright(` ${buttonText} `)

const prefix = isSelected ? chalk.cyan(' ❯ ') : chalk.dim(' ')
lines.push(prefix + button)
}

lines.push('')
lines.push(chalk.dim(' ↑↓ Navigate • Enter Select'))
lines.push(chalk.dim(' You can change this later in Settings (P).'))
lines.push('')

// 📖 Avoid full-screen clear escape here to prevent title/header offset issues in some terminals.
const cleared = lines.map(l => l + EL)
const terminalRows = process.stdout.rows || 24
const remaining = Math.max(0, terminalRows - cleared.length)
for (let i = 0; i < remaining; i++) cleared.push(EL)
process.stdout.write('\x1b[H' + cleared.join('\n'))
}

const cleanup = () => {
if (process.stdin.isTTY) process.stdin.setRawMode(false)
process.stdin.removeListener('keypress', onKeyPress)
process.stdin.pause()
}

const onKeyPress = (_str, key) => {
if (!key) return

if (key.ctrl && key.name === 'c') {
cleanup()
resolve(false)
return
}

if ((key.name === 'up' || key.name === 'left') && selected > 0) {
selected--
render()
return
}

if ((key.name === 'down' || key.name === 'right') && selected < options.length - 1) {
selected++
render()
return
}

if (key.name === 'return') {
cleanup()
resolve(options[selected].value)
}
}

readline.emitKeypressEvents(process.stdin)
process.stdin.setEncoding('utf8')
process.stdin.resume()
if (process.stdin.isTTY) process.stdin.setRawMode(true)
process.stdin.on('keypress', onKeyPress)
render()
})

config.telemetry.enabled = accepted
config.telemetry.consentVersion = TELEMETRY_CONSENT_VERSION
saveConfig(config)

console.log()
if (accepted) {
console.log(chalk.green(' ✅ Analytics enabled. You can disable it later in Settings (P) or with --no-telemetry.'))
} else {
console.log(chalk.yellow(' Analytics disabled. You can enable it later in Settings (P).'))
}
console.log()
}

// 📖 Resolve telemetry effective state with clear precedence:
// 📖 CLI flag > env var > config file > disabled by default.
function isTelemetryEnabled(config, cliArgs) {
if (cliArgs.noTelemetry) return false
const envTelemetry = parseTelemetryEnv(process.env.FREE_CODING_MODELS_TELEMETRY)
if (envTelemetry !== null) return envTelemetry
ensureTelemetryConfig(config)
return config.telemetry.enabled === true
}

// 📖 Fire-and-forget analytics ping: never blocks UX, never throws.
async function sendUsageTelemetry(config, cliArgs, payload) {
if (!isTelemetryEnabled(config, cliArgs)) {
telemetryDebug('skip: telemetry disabled', {
cliNoTelemetry: cliArgs.noTelemetry === true,
envTelemetry: process.env.FREE_CODING_MODELS_TELEMETRY || null,
configEnabled: config?.telemetry?.enabled ?? null,
})
return
}

const apiKey = (
process.env.FREE_CODING_MODELS_POSTHOG_KEY ||
process.env.POSTHOG_PROJECT_API_KEY ||
POSTHOG_PROJECT_KEY_DEFAULT ||
''
).trim()
if (!apiKey) {
telemetryDebug('skip: missing api key')
return
}

const host = (
process.env.FREE_CODING_MODELS_POSTHOG_HOST ||
process.env.POSTHOG_HOST ||
POSTHOG_HOST_DEFAULT ||
POSTHOG_DEFAULT_HOST
).trim().replace(/\/+$/, '')
if (!host) {
telemetryDebug('skip: missing host')
return
}

try {
const endpoint = `${host}${POSTHOG_CAPTURE_PATH}`
const distinctId = getTelemetryDistinctId(config)
const timestamp = typeof payload?.ts === 'string' ? payload.ts : new Date().toISOString()
const signal = (typeof AbortSignal !== 'undefined' && typeof AbortSignal.timeout === 'function')
? AbortSignal.timeout(TELEMETRY_TIMEOUT)
: undefined

const posthogBody = {
api_key: apiKey,
event: payload?.event || 'app_start',
distinct_id: distinctId,
timestamp,
properties: {
$process_person_profile: false,
source: 'cli',
app: 'free-coding-models',
version: payload?.version || LOCAL_VERSION,
app_version: payload?.version || LOCAL_VERSION,
mode: payload?.mode || 'opencode',
system: getTelemetrySystem(),
terminal: getTelemetryTerminal(),
},
}

await fetch(endpoint, {
method: 'POST',
headers: { 'content-type': 'application/json' },
body: JSON.stringify(posthogBody),
signal,
})
telemetryDebug('sent', {
event: posthogBody.event,
endpoint,
mode: posthogBody.properties.mode,
system: posthogBody.properties.system,
terminal: posthogBody.properties.terminal,
})
} catch {
// 📖 Ignore failures silently: analytics must never break the CLI.
telemetryDebug('error: send failed')
}
}

// 📖 checkForUpdateDetailed: Fetch npm latest version with explicit error details.
// 📖 Used by settings manual-check flow to display meaningful status in the UI.
async function checkForUpdateDetailed() {
try {
const res = await fetch('https://registry.npmjs.org/free-coding-models/latest', { signal: AbortSignal.timeout(5000) })
if (!res.ok) return { latestVersion: null, error: `HTTP ${res.status}` }
const data = await res.json()
if (data.version && data.version !== LOCAL_VERSION) return { latestVersion: data.version, error: null }
return { latestVersion: null, error: null }
} catch (error) {
const message = error instanceof Error ? error.message : 'Unknown error'
return { latestVersion: null, error: message }
}
}

// 📖 checkForUpdate: Backward-compatible wrapper for startup update prompt.
async function checkForUpdate() {
const { latestVersion } = await checkForUpdateDetailed()
return latestVersion
}

function runUpdate(latestVersion) {
const { execSync } = require('child_process')
console.log()
console.log(chalk.bold.cyan(' ⬆ Updating free-coding-models to v' + latestVersion + '...'))
console.log()

try {
// 📖 Force install from npm registry (ignore local cache)
// 📖 Use --prefer-online to ensure we get the latest published version
execSync(`npm i -g free-coding-models@${latestVersion} --prefer-online`, { stdio: 'inherit' })
console.log()
console.log(chalk.green(' ✅ Update complete! Version ' + latestVersion + ' installed.'))
console.log()
console.log(chalk.dim(' 🔄 Restarting with new version...'))
console.log()

// 📖 Relaunch automatically with the same arguments
const args = process.argv.slice(2)
execSync(`node bin/free-coding-models.js ${args.join(' ')}`, { stdio: 'inherit' })
process.exit(0)
} catch (err) {
console.log()
// 📖 Check if error is permission-related (EACCES or EPERM)
const isPermissionError = err.code === 'EACCES' || err.code === 'EPERM' ||
(err.stderr && (err.stderr.includes('EACCES') || err.stderr.includes('permission') ||
err.stderr.includes('EACCES'))) ||
(err.message && (err.message.includes('EACCES') || err.message.includes('permission')))

if (isPermissionError) {
console.log(chalk.yellow(' ⚠️ Permission denied. Retrying with sudo...'))
console.log()
try {
execSync(`sudo npm i -g free-coding-models@${latestVersion} --prefer-online`, { stdio: 'inherit' })
console.log()
console.log(chalk.green(' ✅ Update complete with sudo! Version ' + latestVersion + ' installed.'))
console.log()
console.log(chalk.dim(' 🔄 Restarting with new version...'))
console.log()

// 📖 Relaunch automatically with the same arguments
const args = process.argv.slice(2)
execSync(`node bin/free-coding-models.js ${args.join(' ')}`, { stdio: 'inherit' })
process.exit(0)
} catch (sudoErr) {
console.log()
console.log(chalk.red(' ✖ Update failed even with sudo. Try manually:'))
console.log(chalk.dim(' sudo npm i -g free-coding-models@' + latestVersion))
console.log()
}
} else {
console.log(chalk.red(' ✖ Update failed. Try manually: npm i -g free-coding-models@' + latestVersion))
console.log()
}
}
process.exit(1)
}

// 📖 Config is now managed via lib/config.js (JSON format ~/.free-coding-models.json)
// 📖 loadConfig/saveConfig/getApiKey are imported above

// ─── First-run wizard ─────────────────────────────────────────────────────────
// 📖 Shown when NO provider has a key configured yet.
// 📖 Steps through all configured providers sequentially — each is optional (Enter to skip).
// 📖 At least one key must be entered to proceed. Keys saved to ~/.free-coding-models.json.
// 📖 Returns the nvidia key (or null) for backward-compat with the rest of main().
async function promptApiKey(config) {
console.log()
console.log(chalk.bold(' 🔑 First-time setup — API keys'))
console.log(chalk.dim(' Enter keys for any provider you want to use. Press Enter to skip one.'))
console.log()

// 📖 Build providers from sources to keep setup in sync with actual supported providers.
const providers = Object.keys(sources).map((key) => {
const meta = PROVIDER_METADATA[key] || {}
return {
key,
label: meta.label || sources[key]?.name || key,
color: meta.color || chalk.white,
url: meta.signupUrl || 'https://example.com',
hint: meta.signupHint || 'Create API key',
}
})

const rl = readline.createInterface({ input: process.stdin, output: process.stdout })

// 📖 Ask a single question — returns trimmed string or '' for skip
const ask = (question) => new Promise((resolve) => {
rl.question(question, (answer) => resolve(answer.trim()))
})

for (const p of providers) {
console.log(` ${p.color('●')} ${chalk.bold(p.label)}`)
console.log(chalk.dim(` Free key at: `) + chalk.cyanBright(p.url))
console.log(chalk.dim(` ${p.hint}`))
const answer = await ask(chalk.dim(` Enter key (or Enter to skip): `))
console.log()
if (answer) {
config.apiKeys[p.key] = answer
}
}

rl.close()

// 📖 Check at least one key was entered
const anyKey = Object.values(config.apiKeys).some(v => v)
if (!anyKey) {
return null
}

saveConfig(config)
const savedCount = Object.values(config.apiKeys).filter(v => v).length
console.log(chalk.green(` ✅ ${savedCount} key(s) saved to ~/.free-coding-models.json`))
console.log(chalk.dim(' You can add or change keys anytime with the ') + chalk.yellow('P') + chalk.dim(' key in the TUI.'))
console.log()

// 📖 Return nvidia key for backward-compat (main() checks it exists before continuing)
return config.apiKeys.nvidia || Object.values(config.apiKeys).find(v => v) || null
}

// ─── Update notification menu ──────────────────────────────────────────────
// 📖 Shown ONLY when a new version is available, to prompt user to update
// 📖 Centered, clean presentation that doesn't block normal usage
// 📖 Returns 'update', 'changelogs', or null to continue without update
async function promptUpdateNotification(latestVersion) {
if (!latestVersion) return null

return new Promise((resolve) => {
let selected = 0
const options = [
{
label: 'Update now',
icon: '⬆',
description: `Update free-coding-models to v${latestVersion}`,
},
{
label: 'Read Changelogs',
icon: '📋',
description: 'Open GitHub changelog',
},
{
label: 'Continue without update',
icon: '▶',
description: 'Use current version',
},
]

// 📖 Centered render function
const render = () => {
process.stdout.write('\x1b[2J\x1b[H') // clear screen + cursor home

// 📖 Calculate centering
const terminalWidth = process.stdout.columns || 80
const maxWidth = Math.min(terminalWidth - 4, 70)
const centerPad = ' '.repeat(Math.max(0, Math.floor((terminalWidth - maxWidth) / 2)))

console.log()
console.log(centerPad + chalk.bold.red(' ⚠ UPDATE AVAILABLE'))
console.log(centerPad + chalk.red(` Version ${latestVersion} is ready to install`))
console.log()
console.log(centerPad + chalk.bold(' ⚡ Free Coding Models') + chalk.dim(` v${LOCAL_VERSION}`))
console.log()

for (let i = 0; i < options.length; i++) {
const isSelected = i === selected
const bullet = isSelected ? chalk.bold.cyan(' ❯ ') : chalk.dim(' ')
const label = isSelected
? chalk.bold.white(options[i].icon + ' ' + options[i].label)
: chalk.dim(options[i].icon + ' ' + options[i].label)

console.log(centerPad + bullet + label)
console.log(centerPad + chalk.dim(' ' + options[i].description))
console.log()
}

console.log(centerPad + chalk.dim(' ↑↓ Navigate • Enter Select • Ctrl+C Continue'))
console.log()
}

render()

readline.emitKeypressEvents(process.stdin)
if (process.stdin.isTTY) process.stdin.setRawMode(true)

const onKey = (_str, key) => {
if (!key) return
if (key.ctrl && key.name === 'c') {
if (process.stdin.isTTY) process.stdin.setRawMode(false)
process.stdin.removeListener('keypress', onKey)
resolve(null) // Continue without update
return
}
if (key.name === 'up' && selected > 0) {
selected--
render()
} else if (key.name === 'down' && selected < options.length - 1) {
selected++
render()
} else if (key.name === 'return') {
if (process.stdin.isTTY) process.stdin.setRawMode(false)
process.stdin.removeListener('keypress', onKey)
process.stdin.pause()

if (selected === 0) resolve('update')
else if (selected === 1) resolve('changelogs')
else resolve(null) // Continue without update
}
}

process.stdin.on('keypress', onKey)
})
}

// ─── Alternate screen control ─────────────────────────────────────────────────
// 📖 \x1b[?1049h = enter alt screen \x1b[?1049l = leave alt screen
// 📖 \x1b[?25l = hide cursor \x1b[?25h = show cursor
// 📖 \x1b[H = cursor to top
// 📖 NOTE: We avoid \x1b[2J (clear screen) because Ghostty scrolls cleared
// 📖 content into the scrollback on the alt screen, pushing the header off-screen.
// 📖 Instead we overwrite in place: cursor home, then \x1b[K (erase to EOL) per line.
// 📖 \x1b[?7l disables auto-wrap so wide rows clip at the right edge instead of
// 📖 wrapping to the next line (which would double the row height and overflow).
const ALT_ENTER = '\x1b[?1049h\x1b[?25l\x1b[?7l'
const ALT_LEAVE = '\x1b[?7h\x1b[?1049l\x1b[?25h'
const ALT_HOME = '\x1b[H'

// ─── API Configuration ───────────────────────────────────────────────────────────
// 📖 Models are now loaded from sources.js to support multiple providers
// 📖 This allows easy addition of new model sources beyond NVIDIA NIM

const PING_TIMEOUT = 15_000 // 📖 15s per attempt before abort - slow models get more time
const PING_INTERVAL = 3_000 // 📖 Ping all models every 3 seconds in continuous mode

const FPS = 12
const COL_MODEL = 22
// 📖 COL_MS = dashes in hline per ping column = visual width including 2 padding spaces
// 📖 Max value: 12001ms = 7 chars. padStart(COL_MS-2) fits content, +2 spaces = COL_MS dashes
// 📖 COL_MS 11 → content padded to 9 → handles up to "12001ms" (7 chars) with room
const COL_MS = 11

// ─── Styling ──────────────────────────────────────────────────────────────────
// 📖 Tier colors: green gradient (best) → yellow → orange → red (worst)
// 📖 Uses chalk.rgb() for fine-grained color control across 8 tier levels
const TIER_COLOR = {
'S+': t => chalk.bold.rgb(0, 255, 80)(t), // 🟢 bright neon green — elite
'S': t => chalk.bold.rgb(80, 220, 0)(t), // 🟢 green — excellent
'A+': t => chalk.bold.rgb(170, 210, 0)(t), // 🟡 yellow-green — great
'A': t => chalk.bold.rgb(240, 190, 0)(t), // 🟡 yellow — good
'A-': t => chalk.bold.rgb(255, 130, 0)(t), // 🟠 amber — decent
'B+': t => chalk.bold.rgb(255, 70, 0)(t), // 🟠 orange-red — average
'B': t => chalk.bold.rgb(210, 20, 0)(t), // 🔴 red — below avg
'C': t => chalk.bold.rgb(140, 0, 0)(t), // 🔴 dark red — lightweight
}

// 📖 COL_MS - 2 = visual content width (the 2 padding spaces are handled by │ x │ template)
const CELL_W = COL_MS - 2 // 9 chars of content per ms cell

const msCell = (ms) => {
if (ms === null) return chalk.dim('—'.padStart(CELL_W))
const str = String(ms).padStart(CELL_W)
if (ms === 'TIMEOUT') return chalk.red(str)
if (ms < 500) return chalk.greenBright(str)
if (ms < 1500) return chalk.yellow(str)
return chalk.red(str)
}

const FRAMES = ['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏']
// 📖 Spinner cell: braille (1-wide) + padding to fill CELL_W visual chars
const spinCell = (f, o = 0) => chalk.dim.yellow(FRAMES[(f + o) % FRAMES.length].padEnd(CELL_W))

// 📖 Overlay-specific backgrounds so Settings (P) and Help (K) are visually distinct
// 📖 from the main table and from each other.
const SETTINGS_OVERLAY_BG = chalk.bgRgb(14, 20, 30)
const HELP_OVERLAY_BG = chalk.bgRgb(24, 16, 32)
const OVERLAY_PANEL_WIDTH = 116

// 📖 Strip ANSI color/control sequences to estimate visible text width before padding.
function stripAnsi(input) {
return String(input).replace(/\x1b\[[0-9;]*m/g, '').replace(/\x1b\][^\x1b]*\x1b\\/g, '')
}

// 📖 Calculate display width of a string in terminal columns.
// 📖 Emojis and other wide characters occupy 2 columns, variation selectors (U+FE0F) are zero-width.
// 📖 This avoids pulling in a full `string-width` dependency for a lightweight CLI tool.
function displayWidth(str) {
const plain = stripAnsi(String(str))
let w = 0
for (const ch of plain) {
const cp = ch.codePointAt(0)
// Zero-width: variation selectors (FE00-FE0F), zero-width joiner/non-joiner, combining marks
if ((cp >= 0xFE00 && cp <= 0xFE0F) || cp === 0x200D || cp === 0x200C || cp === 0x20E3) continue
// Wide: CJK, emoji (most above U+1F000), fullwidth forms
if (
cp > 0x1F000 || // emoji & symbols
(cp >= 0x2600 && cp <= 0x27BF) || // misc symbols, dingbats
(cp >= 0x2300 && cp <= 0x23FF) || // misc technical (⏳, ⏰, etc.)
(cp >= 0x2700 && cp <= 0x27BF) || // dingbats
(cp >= 0xFE10 && cp <= 0xFE19) || // vertical forms
(cp >= 0xFF01 && cp <= 0xFF60) || // fullwidth ASCII
(cp >= 0xFFE0 && cp <= 0xFFE6) || // fullwidth signs
(cp >= 0x4E00 && cp <= 0x9FFF) || // CJK unified
(cp >= 0x3000 && cp <= 0x303F) || // CJK symbols
(cp >= 0x2B50 && cp <= 0x2B55) || // stars, circles
cp === 0x2705 || cp === 0x2714 || cp === 0x2716 || // check/cross marks
cp === 0x26A0 // ⚠ warning sign
) {
w += 2
} else {
w += 1
}
}
return w
}

// 📖 Left-pad (padEnd equivalent) using display width instead of string length.
// 📖 Ensures columns with emoji text align correctly in the terminal.
function padEndDisplay(str, width) {
const dw = displayWidth(str)
const need = Math.max(0, width - dw)
return str + ' '.repeat(need)
}

// 📖 Tint overlay lines with a fixed dark panel width so the background is clearly visible.
function tintOverlayLines(lines, bgColor) {
return lines.map((line) => {
const text = String(line)
const visibleWidth = stripAnsi(text).length
const padding = ' '.repeat(Math.max(0, OVERLAY_PANEL_WIDTH - visibleWidth))
return bgColor(text + padding)
})
}

// 📖 Clamp overlay scroll to valid bounds for the current terminal height.
function clampOverlayOffset(offset, totalLines, terminalRows) {
const viewportRows = Math.max(1, terminalRows || 1)
const maxOffset = Math.max(0, totalLines - viewportRows)
return Math.max(0, Math.min(maxOffset, offset))
}

// 📖 Ensure a target line is visible inside overlay viewport (used by Settings cursor).
function keepOverlayTargetVisible(offset, targetLine, totalLines, terminalRows) {
const viewportRows = Math.max(1, terminalRows || 1)
let next = clampOverlayOffset(offset, totalLines, terminalRows)
if (targetLine < next) next = targetLine
else if (targetLine >= next + viewportRows) next = targetLine - viewportRows + 1
return clampOverlayOffset(next, totalLines, terminalRows)
}

// 📖 Slice overlay lines to terminal viewport and pad with blanks to avoid stale frames.
function sliceOverlayLines(lines, offset, terminalRows) {
const viewportRows = Math.max(1, terminalRows || 1)
const nextOffset = clampOverlayOffset(offset, lines.length, terminalRows)
const visible = lines.slice(nextOffset, nextOffset + viewportRows)
while (visible.length < viewportRows) visible.push('')
return { visible, offset: nextOffset }
}

// ─── Table renderer ───────────────────────────────────────────────────────────

// 📖 Core logic functions (getAvg, getVerdict, getUptime, sortResults, etc.)
// 📖 are imported from lib/utils.js for testability

// ─── Viewport calculation ────────────────────────────────────────────────────
// 📖 Keep these constants in sync with renderTable() fixed shell lines.
// 📖 If this drifts, model rows overflow and can push the title row out of view.
const TABLE_HEADER_LINES = 4 // 📖 title, spacer, column headers, separator
const TABLE_FOOTER_LINES = 6 // 📖 spacer, hints, spacer, credit+contributors, discord, spacer
const TABLE_FIXED_LINES = TABLE_HEADER_LINES + TABLE_FOOTER_LINES

// 📖 Computes the visible slice of model rows that fits in the terminal.
// 📖 When scroll indicators are needed, they each consume 1 line from the model budget.
function calculateViewport(terminalRows, scrollOffset, totalModels) {
if (terminalRows <= 0) return { startIdx: 0, endIdx: totalModels, hasAbove: false, hasBelow: false }
let maxSlots = terminalRows - TABLE_FIXED_LINES
if (maxSlots < 1) maxSlots = 1
if (totalModels <= maxSlots) return { startIdx: 0, endIdx: totalModels, hasAbove: false, hasBelow: false }

const hasAbove = scrollOffset > 0
const hasBelow = scrollOffset + maxSlots - (hasAbove ? 1 : 0) < totalModels
// Recalculate with indicator lines accounted for
const modelSlots = maxSlots - (hasAbove ? 1 : 0) - (hasBelow ? 1 : 0)
const endIdx = Math.min(scrollOffset + modelSlots, totalModels)
return { startIdx: scrollOffset, endIdx, hasAbove, hasBelow }
}

// 📖 Favorites are always pinned at the top and keep insertion order.
// 📖 Non-favorites still use the active sort column/direction.
function sortResultsWithPinnedFavorites(results, sortColumn, sortDirection) {
const favoriteRows = results
.filter((r) => r.isFavorite)
.sort((a, b) => a.favoriteRank - b.favoriteRank)
const nonFavoriteRows = sortResults(results.filter((r) => !r.isFavorite), sortColumn, sortDirection)
return [...favoriteRows, ...nonFavoriteRows]
}

// 📖 renderTable: mode param controls footer hint text (opencode vs openclaw)
function renderTable(results, pendingPings, frame, cursor = null, sortColumn = 'avg', sortDirection = 'asc', pingInterval = PING_INTERVAL, lastPingTime = Date.now(), mode = 'opencode', tierFilterMode = 0, scrollOffset = 0, terminalRows = 0, originFilterMode = 0) {
// 📖 Filter out hidden models for display
const visibleResults = results.filter(r => !r.hidden)

const up = visibleResults.filter(r => r.status === 'up').length
const down = visibleResults.filter(r => r.status === 'down').length
const timeout = visibleResults.filter(r => r.status === 'timeout').length
const pending = visibleResults.filter(r => r.status === 'pending').length

// 📖 Calculate seconds until next ping
const timeSinceLastPing = Date.now() - lastPingTime
const timeUntilNextPing = Math.max(0, pingInterval - timeSinceLastPing)
const secondsUntilNext = Math.ceil(timeUntilNextPing / 1000)

const phase = pending > 0
? chalk.dim(`discovering — ${pending} remaining…`)
: pendingPings > 0
? chalk.dim(`pinging — ${pendingPings} in flight…`)
: chalk.dim(`next ping ${secondsUntilNext}s`)

// 📖 Mode badge shown in header so user knows what Enter will do
// 📖 Now includes key hint for mode toggle
let modeBadge
if (mode === 'openclaw') {
modeBadge = chalk.bold.rgb(255, 100, 50)(' [🦞 OpenClaw]')
} else if (mode === 'opencode-desktop') {
modeBadge = chalk.bold.rgb(0, 200, 255)(' [🖥 Desktop]')
} else {
modeBadge = chalk.bold.rgb(0, 200, 255)(' [💻 CLI]')
}

// 📖 Add mode toggle hint
const modeHint = chalk.dim.yellow(' (Z to toggle)')

// 📖 Tier filter badge shown when filtering is active (shows exact tier name)
const TIER_CYCLE_NAMES = [null, 'S+', 'S', 'A+', 'A', 'A-', 'B+', 'B', 'C']
let tierBadge = ''
if (tierFilterMode > 0) {
tierBadge = chalk.bold.rgb(255, 200, 0)(` [${TIER_CYCLE_NAMES[tierFilterMode]}]`)
}

// 📖 Origin filter badge — shown when filtering by provider is active
let originBadge = ''
if (originFilterMode > 0) {
const originKeys = [null, ...Object.keys(sources)]
const activeOriginKey = originKeys[originFilterMode]
const activeOriginName = activeOriginKey ? sources[activeOriginKey]?.name ?? activeOriginKey : null
if (activeOriginName) {
originBadge = chalk.bold.rgb(100, 200, 255)(` [${activeOriginName}]`)
}
}

// 📖 Column widths (generous spacing with margins)
const W_RANK = 6
const W_TIER = 6
const W_CTX = 6
const W_SOURCE = 14
const W_MODEL = 26
const W_SWE = 9
const W_PING = 14
const W_AVG = 11
const W_STATUS = 18
const W_VERDICT = 14
const W_STAB = 11
const W_UPTIME = 6

// 📖 Sort models using the shared helper
const sorted = sortResultsWithPinnedFavorites(visibleResults, sortColumn, sortDirection)

const lines = [
` ${chalk.bold('⚡ Free Coding Models')} ${chalk.dim('v' + LOCAL_VERSION)}${modeBadge}${modeHint}${tierBadge}${originBadge} ` +
chalk.greenBright(`✅ ${up}`) + chalk.dim(' up ') +
chalk.yellow(`⏳ ${timeout}`) + chalk.dim(' timeout ') +
chalk.red(`❌ ${down}`) + chalk.dim(' down ') +
phase,
'',
]

// 📖 Header row with sorting indicators
// 📖 NOTE: padEnd on chalk strings counts ANSI codes, breaking alignment
// 📖 Solution: build plain text first, then colorize
const dir = sortDirection === 'asc' ? '↑' : '↓'

const rankH = 'Rank'
const tierH = 'Tier'
const originH = 'Origin'
const modelH = 'Model'
const sweH = sortColumn === 'swe' ? dir + ' SWE%' : 'SWE%'
const ctxH = sortColumn === 'ctx' ? dir + ' CTX' : 'CTX'
const pingH = sortColumn === 'ping' ? dir + ' Latest Ping' : 'Latest Ping'
const avgH = sortColumn === 'avg' ? dir + ' Avg Ping' : 'Avg Ping'
const healthH = sortColumn === 'condition' ? dir + ' Health' : 'Health'
const verdictH = sortColumn === 'verdict' ? dir + ' Verdict' : 'Verdict'
const stabH = sortColumn === 'stability' ? dir + ' Stability' : 'Stability'
const uptimeH = sortColumn === 'uptime' ? dir + ' Up%' : 'Up%'

// 📖 Helper to colorize first letter for keyboard shortcuts
// 📖 IMPORTANT: Pad PLAIN TEXT first, then apply colors to avoid alignment issues
const colorFirst = (text, width, colorFn = chalk.yellow) => {
const first = text[0]
const rest = text.slice(1)
const plainText = first + rest
const padding = ' '.repeat(Math.max(0, width - plainText.length))
return colorFn(first) + chalk.dim(rest + padding)
}

// 📖 Now colorize after padding is calculated on plain text
const rankH_c = colorFirst(rankH, W_RANK)
const tierH_c = colorFirst('Tier', W_TIER)
const originLabel = 'Origin'
const originH_c = sortColumn === 'origin'
? chalk.bold.cyan(originLabel.padEnd(W_SOURCE))
: (originFilterMode > 0 ? chalk.bold.rgb(100, 200, 255)(originLabel.padEnd(W_SOURCE)) : (() => {
// 📖 Custom colorization for Origin: highlight 'N' (the filter key) at the end
const padding = ' '.repeat(Math.max(0, W_SOURCE - originLabel.length))
return chalk.dim('Origi') + chalk.yellow('N') + chalk.dim(padding)
})())
const modelH_c = colorFirst(modelH, W_MODEL)
const sweH_c = sortColumn === 'swe' ? chalk.bold.cyan(sweH.padEnd(W_SWE)) : colorFirst(sweH, W_SWE)
const ctxH_c = sortColumn === 'ctx' ? chalk.bold.cyan(ctxH.padEnd(W_CTX)) : colorFirst(ctxH, W_CTX)
const pingH_c = sortColumn === 'ping' ? chalk.bold.cyan(pingH.padEnd(W_PING)) : colorFirst('Latest Ping', W_PING)
const avgH_c = sortColumn === 'avg' ? chalk.bold.cyan(avgH.padEnd(W_AVG)) : colorFirst('Avg Ping', W_AVG)
const healthH_c = sortColumn === 'condition' ? chalk.bold.cyan(healthH.padEnd(W_STATUS)) : colorFirst('Health', W_STATUS)
const verdictH_c = sortColumn === 'verdict' ? chalk.bold.cyan(verdictH.padEnd(W_VERDICT)) : colorFirst(verdictH, W_VERDICT)
// 📖 Custom colorization for Stability: highlight 'B' (the sort key) since 'S' is taken by SWE
const stabH_c = sortColumn === 'stability' ? chalk.bold.cyan(stabH.padEnd(W_STAB)) : (() => {
const plain = 'Stability'
const padding = ' '.repeat(Math.max(0, W_STAB - plain.length))
return chalk.dim('Sta') + chalk.white.bold('B') + chalk.dim('ility' + padding)
})()
const uptimeH_c = sortColumn === 'uptime' ? chalk.bold.cyan(uptimeH.padEnd(W_UPTIME)) : colorFirst(uptimeH, W_UPTIME, chalk.green)

// 📖 Header with proper spacing (column order: Rank, Tier, SWE%, CTX, Model, Origin, Latest Ping, Avg Ping, Health, Verdict, Stability, Up%)
lines.push(' ' + rankH_c + ' ' + tierH_c + ' ' + sweH_c + ' ' + ctxH_c + ' ' + modelH_c + ' ' + originH_c + ' ' + pingH_c + ' ' + avgH_c + ' ' + healthH_c + ' ' + verdictH_c + ' ' + stabH_c + ' ' + uptimeH_c)

// 📖 Separator line
lines.push(
' ' +
chalk.dim('─'.repeat(W_RANK)) + ' ' +
chalk.dim('─'.repeat(W_TIER)) + ' ' +
chalk.dim('─'.repeat(W_SWE)) + ' ' +
chalk.dim('─'.repeat(W_CTX)) + ' ' +
'─'.repeat(W_MODEL) + ' ' +
'─'.repeat(W_SOURCE) + ' ' +
chalk.dim('─'.repeat(W_PING)) + ' ' +
chalk.dim('─'.repeat(W_AVG)) + ' ' +
chalk.dim('─'.repeat(W_STATUS)) + ' ' +
chalk.dim('─'.repeat(W_VERDICT)) + ' ' +
chalk.dim('─'.repeat(W_STAB)) + ' ' +
chalk.dim('─'.repeat(W_UPTIME))
)

// 📖 Viewport clipping: only render models that fit on screen
const vp = calculateViewport(terminalRows, scrollOffset, sorted.length)

if (vp.hasAbove) {
lines.push(chalk.dim(` ... ${vp.startIdx} more above ...`))
}

for (let i = vp.startIdx; i < vp.endIdx; i++) {
const r = sorted[i]
const tierFn = TIER_COLOR[r.tier] ?? (t => chalk.white(t))

const isCursor = cursor !== null && i === cursor

// 📖 Left-aligned columns - pad plain text first, then colorize
const num = chalk.dim(String(r.idx).padEnd(W_RANK))
const tier = tierFn(r.tier.padEnd(W_TIER))
// 📖 Show provider name from sources map (NIM / Groq / Cerebras)
const providerName = sources[r.providerKey]?.name ?? r.providerKey ?? 'NIM'
const source = chalk.green(providerName.padEnd(W_SOURCE))
// 📖 Favorites: always reserve 2 display columns at the start of Model column.
// 📖 ⭐ (2 cols) for favorites, ' ' (2 spaces) for non-favorites — keeps alignment stable.
const favoritePrefix = r.isFavorite ? '⭐' : ' '
const prefixDisplayWidth = 2
const nameWidth = Math.max(0, W_MODEL - prefixDisplayWidth)
const name = favoritePrefix + r.label.slice(0, nameWidth).padEnd(nameWidth)
const sweScore = r.sweScore ?? '—'
// 📖 SWE% colorized on the same gradient as Tier:
// ≥70% bright neon green (S+), ≥60% green (S), ≥50% yellow-green (A+),
// ≥40% yellow (A), ≥35% amber (A-), ≥30% orange-red (B+),
// ≥20% red (B), <20% dark red (C), '—' dim
let sweCell
if (sweScore === '—') {
sweCell = chalk.dim(sweScore.padEnd(W_SWE))
} else {
const sweVal = parseFloat(sweScore)
const swePadded = sweScore.padEnd(W_SWE)
if (sweVal >= 70) sweCell = chalk.bold.rgb(0, 255, 80)(swePadded)
else if (sweVal >= 60) sweCell = chalk.bold.rgb(80, 220, 0)(swePadded)
else if (sweVal >= 50) sweCell = chalk.bold.rgb(170, 210, 0)(swePadded)
else if (sweVal >= 40) sweCell = chalk.rgb(240, 190, 0)(swePadded)
else if (sweVal >= 35) sweCell = chalk.rgb(255, 130, 0)(swePadded)
else if (sweVal >= 30) sweCell = chalk.rgb(255, 70, 0)(swePadded)
else if (sweVal >= 20) sweCell = chalk.rgb(210, 20, 0)(swePadded)
else sweCell = chalk.rgb(140, 0, 0)(swePadded)
}

// 📖 Context window column - colorized by size (larger = better)
const ctxRaw = r.ctx ?? '—'
const ctxCell = ctxRaw !== '—' && (ctxRaw.includes('128k') || ctxRaw.includes('200k') || ctxRaw.includes('1m'))
? chalk.greenBright(ctxRaw.padEnd(W_CTX))
: ctxRaw !== '—' && (ctxRaw.includes('32k') || ctxRaw.includes('64k'))
? chalk.cyan(ctxRaw.padEnd(W_CTX))
: chalk.dim(ctxRaw.padEnd(W_CTX))

// 📖 Latest ping - pings are objects: { ms, code }
// 📖 Show response time for 200 (success) and 401 (no-auth but server is reachable)
const latestPing = r.pings.length > 0 ? r.pings[r.pings.length - 1] : null
let pingCell
if (!latestPing) {
pingCell = chalk.dim('———'.padEnd(W_PING))
} else if (latestPing.code === '200') {
// 📖 Success - show response time
const str = String(latestPing.ms).padEnd(W_PING)
pingCell = latestPing.ms < 500 ? chalk.greenBright(str) : latestPing.ms < 1500 ? chalk.yellow(str) : chalk.red(str)
} else if (latestPing.code === '401') {
// 📖 401 = no API key but server IS reachable — still show latency in dim
pingCell = chalk.dim(String(latestPing.ms).padEnd(W_PING))
} else {
// 📖 Error or timeout - show "———" (error code is already in Status column)
pingCell = chalk.dim('———'.padEnd(W_PING))
}

// 📖 Avg ping (just number, no "ms")
const avg = getAvg(r)
let avgCell
if (avg !== Infinity) {
const str = String(avg).padEnd(W_AVG)
avgCell = avg < 500 ? chalk.greenBright(str) : avg < 1500 ? chalk.yellow(str) : chalk.red(str)
} else {
avgCell = chalk.dim('———'.padEnd(W_AVG))
}

// 📖 Status column - build plain text with emoji, pad, then colorize
// 📖 Different emojis for different error codes
let statusText, statusColor
if (r.status === 'noauth') {
// 📖 Server responded but needs an API key — shown dimly since it IS reachable
statusText = `🔑 NO KEY`
statusColor = (s) => chalk.dim(s)
} else if (r.status === 'pending') {
statusText = `${FRAMES[frame % FRAMES.length]} wait`
statusColor = (s) => chalk.dim.yellow(s)
} else if (r.status === 'up') {
statusText = `✅ UP`
statusColor = (s) => s
} else if (r.status === 'timeout') {
statusText = `⏳ TIMEOUT`
statusColor = (s) => chalk.yellow(s)
} else if (r.status === 'down') {
const code = r.httpCode ?? 'ERR'
// 📖 Different emojis for different error codes
const errorEmojis = {
'429': '🔥', // Rate limited / overloaded
'404': '🚫', // Not found
'500': '💥', // Internal server error
'502': '🔌', // Bad gateway
'503': '🔒', // Service unavailable
'504': '⏰', // Gateway timeout
}
const emoji = errorEmojis[code] || '❌'
statusText = `${emoji} ${code}`
statusColor = (s) => chalk.red(s)
} else {
statusText = '?'
statusColor = (s) => chalk.dim(s)
}
const status = statusColor(padEndDisplay(statusText, W_STATUS))

// 📖 Verdict column - use getVerdict() for stability-aware verdicts, then render with emoji
const verdict = getVerdict(r)
let verdictText, verdictColor
// 📖 Verdict colors follow the same green→red gradient as TIER_COLOR / SWE%
switch (verdict) {
case 'Perfect':
verdictText = 'Perfect 🚀'
verdictColor = (s) => chalk.bold.rgb(0, 255, 180)(s) // bright cyan-green — stands out from Normal
break
case 'Normal':
verdictText = 'Normal ✅'
verdictColor = (s) => chalk.bold.rgb(140, 200, 0)(s) // lime-yellow — clearly warmer than Perfect
break
case 'Spiky':
verdictText = 'Spiky 📈'
verdictColor = (s) => chalk.bold.rgb(170, 210, 0)(s) // A+ yellow-green
break
case 'Slow':
verdictText = 'Slow 🐢'
verdictColor = (s) => chalk.bold.rgb(255, 130, 0)(s) // A- amber
break
case 'Very Slow':
verdictText = 'Very Slow 🐌'
verdictColor = (s) => chalk.bold.rgb(255, 70, 0)(s) // B+ orange-red
break
case 'Overloaded':
verdictText = 'Overloaded 🔥'
verdictColor = (s) => chalk.bold.rgb(210, 20, 0)(s) // B red
break
case 'Unstable':
verdictText = 'Unstable ⚠️'
verdictColor = (s) => chalk.bold.rgb(175, 10, 0)(s) // between B and C
break
case 'Not Active':
verdictText = 'Not Active 👻'
verdictColor = (s) => chalk.dim(s)
break
case 'Pending':
verdictText = 'Pending ⏳'
verdictColor = (s) => chalk.dim(s)
break
default:
verdictText = 'Unusable 💀'
verdictColor = (s) => chalk.bold.rgb(140, 0, 0)(s) // C dark red
break
}
// 📖 Use padEndDisplay to account for emoji display width (2 cols each) so all rows align
const speedCell = verdictColor(padEndDisplay(verdictText, W_VERDICT))

// 📖 Stability column - composite score (0–100) from p95 + jitter + spikes + uptime
// 📖 Left-aligned to sit flush under the column header
const stabScore = getStabilityScore(r)
let stabCell
if (stabScore < 0) {
stabCell = chalk.dim('———'.padEnd(W_STAB))
} else if (stabScore >= 80) {
stabCell = chalk.greenBright(String(stabScore).padEnd(W_STAB))
} else if (stabScore >= 60) {
stabCell = chalk.cyan(String(stabScore).padEnd(W_STAB))
} else if (stabScore >= 40) {
stabCell = chalk.yellow(String(stabScore).padEnd(W_STAB))
} else {
stabCell = chalk.red(String(stabScore).padEnd(W_STAB))
}

// 📖 Uptime column - percentage of successful pings
// 📖 Left-aligned to sit flush under the column header
const uptimePercent = getUptime(r)
const uptimeStr = uptimePercent + '%'
let uptimeCell
if (uptimePercent >= 90) {
uptimeCell = c

…(truncated)

