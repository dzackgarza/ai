# GAPS

Date: 2026-03-06  
Scope: current plugin workspace and active OpenCode wiring

## Remaining Gaps

1. Human TUI verification is still required for task observability Phase 1/2 behavior (live child-session visibility, parent tool metrics, async polling display updates).
2. `webfetch` domain routing is implemented for `github.com`, `reddit.com`, YouTube URLs, and `wikipedia.org` in `improved-webtools` (now wired as external plugin). Handlers for Stack Exchange sites, package registries (`pypi.org` / `npmjs.com` / `crates.io`), and Hugging Face are still pending.
3. Cache lifecycle is lazy-expiration on read; there is no background cleanup/pruning pass for stale entries.
4. API-viability checks (below) show several domains are only partial-replacement candidates (metadata parity but not full content parity).
5. Non-web unit suites (`prompt-router`, `command-interceptor`, `callback-integration`) still use synthetic test inputs and do not yet consume pinned real fixtures.
6. Documentation-backed validation is incomplete outside the most recent GitHub issue fix; several remaining command/API assumptions still rely on inferred behavior plus mocks rather than direct doc+live verification.

## Domain Handler Viability (API vs Web Parity)

Scope requested: `stackoverflow.com`, `stackexchange.com`, `meta.stackoverflow.com`, `meta.stackexchange.com`, `reddit.com`, `arxiv.org`, `wikipedia.org`, `pypi.org`, `npmjs.com`, `crates.io`, `huggingface.co`, `youtube.com`.

### 1) Stack Overflow / Stack Exchange / MSO / MSE

- Status: `Viable` for Q/A/comment content retrieval.
- Evidence:
  - Stack Exchange API supports per-site queries via `site` parameter using full domain names and has endpoints for questions, answers, and comments.
  - Custom filters include `withbody` and `*.body` fields for high-fidelity text retrieval.
  - Live check succeeded (`questions`, `answers`, `comments` with `filter=withbody` returned `body` fields).
- Links:
  - https://api.stackexchange.com/docs
  - https://api.stackexchange.com/docs/filters

### 2) Reddit

- Status: `Implemented (via Apify actor), still Partial for parity/risk`.
- Evidence:
  - Reddit API docs show listing endpoints, pagination (`limit` max 100, `after`/`before`) and comments endpoints.
  - Live unauthenticated JSON access from this environment is currently blocked/challenged (`403 Blocked`) on:
    - `https://www.reddit.com/.../.json`
    - `https://old.reddit.com/.../.json`
    - `https://api.reddit.com/...`
  - `datavorous/yars` test (README “scrape post details” path) was executed and returned `None` because upstream Reddit request returned `403`.
  - `yars` `search_reddit` and `scrape_user_data` also returned empty results due to `403`.
  - Current plugin route uses `apify call spry_wholemeal/reddit-scraper` to fetch post + comments and renders a nested markdown comment tree.
  - Current plugin route is covered by unit tests (`routes reddit posts through apify and renders nested markdown comments`).
- Links:
  - https://www.reddit.com/dev/api/
  - https://github.com/datavorous/yars

### 3) arXiv

- Status: `Partial` (metadata parity, not guaranteed full-content parity).
- Evidence:
  - arXiv exposes an API documented under “API for Metadata”.
  - Official docs do not present a fixed per-second quota; they recommend a polite 3-second delay between repeated calls and enforce result-size limits (`max_results <= 30000`, slices up to 2000).
  - arXiv API Discussion (official reply) states `429 Rate exceeded` is capacity-related and not a signal of abusive client rate; they state excessive use returns `503`.
  - Working assumption: API is strong for metadata/search; full paper content still depends on PDF/source retrieval.
- Links:
  - https://info.arxiv.org/help/api/
  - https://groups.google.com/a/arxiv.org/g/api/c/pNB3lnxf4mQ

### 4) Wikipedia / Wikimedia

- Status: `Viable` for page content retrieval.
- Evidence:
  - Core REST endpoints provide page `source` (wikitext) and HTML content.
  - Endpoint docs include explicit response schema containing `source`.
  - Note: Core REST is slated for gradual deprecation (starting July 2026); MediaWiki REST should be preferred for new handlers.
- Links:
  - https://api.wikimedia.org/wiki/Core_REST_API/Reference/Pages
  - https://api.wikimedia.org/wiki/Core_REST_API/Reference/Pages/Get_page_source

### 5) PyPI

- Status: `Viable` for package metadata and release/file information.
- Evidence:
  - Official JSON API returns project metadata, release artifacts, hashes, vulnerabilities, and release-specific responses.
  - Caveat: some keys are deprecated (`downloads`, `has_sig`, etc.).
- Links:
  - https://docs.pypi.org/api/json/

### 6) npm

- Status: `Viable` for package metadata/search/readme retrieval.
- Evidence:
  - Public registry API exposes package “packument” docs, search with pagination (`from`/`size`), `total`, and readme fields.
- Links:
  - https://raw.githubusercontent.com/npm/registry/master/docs/REGISTRY-API.md

### 7) crates.io

- Status: `Viable` for crate metadata/search/listing parity.
- Evidence:
  - Official data access policy includes sparse index, API, and OpenAPI URL with explicit limits.
  - Live `/api/v1/crates` call succeeded and returned `meta.total` plus crate metadata fields.
- Links:
  - https://crates.io/data-access
  - https://crates.io/api/openapi.json

### 8) Hugging Face

- Status: `Viable` for model/dataset repo metadata; `Partial` for full card/content parity.
- Evidence:
  - Hub API docs route to OpenAPI and document rate limits.
  - Live API calls to `/api/models` and `/api/models/{id}` succeeded and returned key metadata fields.
  - Some rich content can be missing unless additional repo files/card sources are fetched.
- Links:
  - https://huggingface.co/docs/hub/api
  - https://huggingface.co/.well-known/openapi.json

### 9) YouTube

- Status: `Implemented (caption-first + Whisper pipeline), still Partial for page-content parity`.
- Evidence:
  - Current plugin route uses yt-dlp with impersonation/runtime dependencies to extract English captions first, then falls back to Whisper transcription when captions are unavailable.
  - Data API supports metadata/resources and comments endpoints.
  - Captions API supports listing/downloading caption tracks, but `captions.list` does not include caption text itself and download/auth constraints apply.
  - Not all videos have usable captions, so transcript parity vs web/video is not guaranteed.
- Links:
  - https://developers.google.com/youtube/v3/docs
  - https://developers.google.com/youtube/v3/docs/captions
  - https://developers.google.com/youtube/v3/guides/implementation/captions

## Validation Status

1. `improved-task` wired as external plugin in `configs/config_skeleton.json`. Toggle `task-plugin` in `configs/local-plugins.json` to enable (currently `false`).
2. `improved-webtools` wired as external plugin in `configs/config_skeleton.json`. Replaces the deleted in-repo `searxng-search.ts` + `webfetch-handlers/`.
3. `task-plugin` toggle remains `false` in `configs/local-plugins.json` (`task.ts` removed from local plugins; control now via external plugin + toggle).
4. `callback-integration.test.ts` validates consolidated callback semantics across `task`, `sleep`, and `async_command`.

**Note:** Previous validation items 4–9 described tests in `tests/unit/searxng-search.test.ts`, `tests/unit/webfetch-handlers/handlers.test.ts`, and `tests/fixtures/real/` — these were removed when the in-repo webtools plugin was extracted to `improved-webtools`. Validation of the equivalent coverage in `/home/dzack/opencode-plugins/improved-webtools/` is pending.
