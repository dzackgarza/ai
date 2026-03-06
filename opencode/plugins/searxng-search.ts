import { type Plugin, tool } from "@opencode-ai/plugin";
import { getEncoding } from "js-tiktoken";
import { createHash } from "node:crypto";
import { mkdir, unlink } from "node:fs/promises";
import { join } from "node:path";

type SearxngResult = {
  title: string;
  url: string;
  content: string;
  engine: string;
  category: string;
  publishedDate: string | null;
};

type SearxngResponse = {
  query: string;
  number_of_results: number;
  results: SearxngResult[];
  answers: string[];
  suggestions: string[];
  unresponsive_engines: Array<[string, string]>;
};

type SearchQueryInput = {
  q: string;
  category?: string;
  num_results?: number;
  numResults?: number;
  offset?: number;
  recency?: number;
  domains?: string[];
};

type CommandExecutionResult = {
  stdoutText: string;
  stderrText: string;
  exitCode: number;
};

type WebFetchHandlerInput = {
  url: URL;
};

type WebFetchHandlerResult = {
  routeName: string;
  sourceUrl: string;
  content: string;
};

type WebFetchDomainHandler = {
  name: string;
  domains: readonly string[];
  handle: (input: WebFetchHandlerInput) => Promise<WebFetchHandlerResult>;
};

const SEARXNG_INSTANCE_URL = (process.env.SEARXNG_INSTANCE_URL ?? "").trim();
const DEFAULT_TIMEOUT_MS = 15_000;
const WEBFETCH_COMMAND_TIMEOUT_MS = 30_000;
const DEFAULT_LIMIT = 8;
const MAX_LIMIT = 20;
const MAX_OFFSET = 200;
const MAX_PAGE_FETCHES = 20;
const WEBFETCH_INLINE_TOKEN_LIMIT = 20_000;
const WEBFETCH_CACHE_ENABLED = (process.env.WEBFETCH_CACHE_ENABLED ?? "1").trim() !== "0";
const WEBFETCH_CACHE_DIR = (
  process.env.WEBFETCH_CACHE_DIR ?? `${process.env.HOME ?? "/tmp"}/.cache/opencode-webfetch`
).trim();
const WEBFETCH_CACHE_TTL_DAYS = Number.parseInt(process.env.WEBFETCH_CACHE_TTL_DAYS ?? "90", 10);
const WEBFETCH_CACHE_TTL_MS =
  Number.isFinite(WEBFETCH_CACHE_TTL_DAYS) && WEBFETCH_CACHE_TTL_DAYS > 0
    ? WEBFETCH_CACHE_TTL_DAYS * 24 * 60 * 60 * 1000
    : 90 * 24 * 60 * 60 * 1000;
const TOKEN_ENCODER = getEncoding("o200k_base");
const PASSPHRASE_WEB_SEARCH = "PASS_WEB_SEARCH_SHADOW_20260305_6A9F";
const PASSPHRASE_WEBFETCH = "PASS_WEBFETCH_SHADOW_20260305_C3D2";
const GITHUB_DOMAINS = ["github.com", "www.github.com"] as const;
const REDDIT_DOMAINS = ["reddit.com", "www.reddit.com", "old.reddit.com", "api.reddit.com"] as const;
const REDDIT_APIFY_ACTOR = (process.env.REDDIT_APIFY_ACTOR ?? "spry_wholemeal/reddit-scraper").trim();

const NARROWING_CATEGORIES = [
  "news",
  "it",
  "npm",
  "pypi",
  "st",
  "gh",
  "hf",
  "ollama",
  "hn",
  "science",
  "arx",
  "cr",
  "gos",
  "se",
  "aa",
  "lg",
] as const;

const VALID_CATEGORIES = new Set<string>(NARROWING_CATEGORIES);
function normalizeBaseUrl(baseUrl: string): string {
  return baseUrl.replace(/\/+$/, "");
}

function parseLimit(limit?: number): number {
  if (!Number.isFinite(limit)) return DEFAULT_LIMIT;
  return Math.max(1, Math.min(MAX_LIMIT, Math.floor(limit ?? DEFAULT_LIMIT)));
}

function resolveOffset(offset?: number): { value: number; error?: string } {
  if (offset === undefined) return { value: 0 };
  if (!Number.isFinite(offset) || !Number.isInteger(offset) || offset < 0) {
    return {
      value: 0,
      error: `Invalid offset: ${JSON.stringify(offset)}. Offset must be a non-negative integer.`,
    };
  }
  if (offset > MAX_OFFSET) {
    return {
      value: 0,
      error: `Invalid offset: ${JSON.stringify(offset)}. Maximum supported offset is ${MAX_OFFSET}.`,
    };
  }
  return { value: offset };
}

function clampSnippet(text: string, maxLen = 280): string {
  const clean = text.trim().replace(/\s+/g, " ");
  if (clean.length <= maxLen) return clean;
  return `${clean.slice(0, maxLen - 1)}…`;
}

function countTokens(text: string): number {
  return TOKEN_ENCODER.encode(text).length;
}

function hostMatchesDomain(hostname: string, domain: string): boolean {
  return hostname === domain || hostname.endsWith(`.${domain}`);
}

type WebFetchCachePayload = {
  url: string;
  routeName: string;
  sourceUrl: string;
  content: string;
  cachedAt: string;
};

function webFetchCachePath(url: string): string {
  const digest = createHash("sha256").update(url).digest("hex");
  return join(WEBFETCH_CACHE_DIR, `${digest}.json`);
}

async function readWebFetchCache(url: string): Promise<WebFetchHandlerResult | undefined> {
  if (!WEBFETCH_CACHE_ENABLED) return undefined;
  const path = webFetchCachePath(url);
  const file = Bun.file(path);
  if (!(await file.exists())) return undefined;
  try {
    const raw = await file.text();
    const parsed = JSON.parse(raw) as Partial<WebFetchCachePayload>;
    if (
      parsed.url !== url ||
      typeof parsed.routeName !== "string" ||
      typeof parsed.sourceUrl !== "string" ||
      typeof parsed.content !== "string" ||
      typeof parsed.cachedAt !== "string"
    ) {
      return undefined;
    }
    const cachedAt = Date.parse(parsed.cachedAt);
    if (!Number.isFinite(cachedAt) || Date.now() - cachedAt > WEBFETCH_CACHE_TTL_MS) {
      await unlink(path).catch(() => {});
      return undefined;
    }
    return {
      routeName: parsed.routeName,
      sourceUrl: parsed.sourceUrl,
      content: parsed.content,
    };
  } catch {
    return undefined;
  }
}

async function writeWebFetchCache(url: string, result: WebFetchHandlerResult): Promise<void> {
  if (!WEBFETCH_CACHE_ENABLED) return;
  if (!result.content.trim()) return;
  await mkdir(WEBFETCH_CACHE_DIR, { recursive: true });
  const payload: WebFetchCachePayload = {
    url,
    routeName: result.routeName,
    sourceUrl: result.sourceUrl,
    content: result.content,
    cachedAt: new Date().toISOString(),
  };
  await Bun.write(webFetchCachePath(url), JSON.stringify(payload));
}

function findWebFetchHandler(
  handlers: readonly WebFetchDomainHandler[],
  url: URL,
): WebFetchDomainHandler | undefined {
  return handlers.find((handler) =>
    handler.domains.some((domain) => hostMatchesDomain(url.hostname, domain)),
  );
}

function normalizeGitHubRepo(repo: string): string {
  return repo.replace(/\.git$/i, "");
}

type GitHubCommandPlan = {
  args: string[];
  sourceUrl: string;
};

function buildGitHubCommandPlan(url: URL): GitHubCommandPlan {
  const rawSegments = url.pathname
    .split("/")
    .filter(Boolean)
    .map((segment) => decodeURIComponent(segment));

  if (rawSegments.length >= 2) {
    const owner = rawSegments[0]!;
    const repo = normalizeGitHubRepo(rawSegments[1]!);
    const repoRef = `${owner}/${repo}`;
    const scope = rawSegments[2];
    const tail = rawSegments.slice(3);

    if (scope === "issues" && /^\d+$/.test(tail[0] ?? "")) {
      return {
        args: ["gh", "issue", "view", tail[0]!, "--repo", repoRef, "--comments"],
        sourceUrl: `https://github.com/${repoRef}/issues/${tail[0]!}`,
      };
    }

    if (scope === "pull" && /^\d+$/.test(tail[0] ?? "")) {
      return {
        args: ["gh", "pr", "view", tail[0]!, "--repo", repoRef, "--comments"],
        sourceUrl: `https://github.com/${repoRef}/pull/${tail[0]!}`,
      };
    }

    if (scope === "blob" && tail.length >= 2) {
      const ref = tail[0]!;
      const filePath = tail.slice(1).join("/");
      return {
        args: [
          "gh",
          "api",
          `repos/${repoRef}/contents/${filePath}`,
          "-f",
          `ref=${ref}`,
          "-H",
          "Accept: application/vnd.github.raw+json",
        ],
        sourceUrl: `https://github.com/${repoRef}/blob/${ref}/${filePath}`,
      };
    }

    if (scope === "commit" && tail.length >= 1) {
      return {
        args: ["gh", "api", `repos/${repoRef}/commits/${tail[0]!}`],
        sourceUrl: `https://github.com/${repoRef}/commit/${tail[0]!}`,
      };
    }

    if (scope === "releases") {
      return {
        args: ["gh", "release", "list", "--repo", repoRef, "--limit", "20"],
        sourceUrl: `https://github.com/${repoRef}/releases`,
      };
    }

    if (scope === "issues") {
      return {
        args: ["gh", "issue", "list", "--repo", repoRef, "--limit", "30"],
        sourceUrl: `https://github.com/${repoRef}/issues`,
      };
    }

    if (scope === "pulls") {
      return {
        args: ["gh", "pr", "list", "--repo", repoRef, "--limit", "30"],
        sourceUrl: `https://github.com/${repoRef}/pulls`,
      };
    }

    return {
      args: ["gh", "repo", "view", repoRef, "--readme"],
      sourceUrl: `https://github.com/${repoRef}`,
    };
  }

  const fallbackQuery = rawSegments.join("/") || url.toString();
  return {
    args: ["gh", "search", "repos", fallbackQuery, "--limit", "20"],
    sourceUrl: url.toString(),
  };
}

async function runCommand(args: string[]): Promise<CommandExecutionResult> {
  const proc = Bun.spawn(args, {
    stdout: "pipe",
    stderr: "pipe",
  });

  const timeout = setTimeout(() => {
    proc.kill();
  }, WEBFETCH_COMMAND_TIMEOUT_MS);
  try {
    const [stdoutText, stderrText, exitCode] = await Promise.all([
      new Response(proc.stdout).text(),
      new Response(proc.stderr).text(),
      proc.exited,
    ]);
    return { stdoutText, stderrText, exitCode };
  } finally {
    clearTimeout(timeout);
  }
}

async function fetchWebContentWithW3M(url: URL): Promise<CommandExecutionResult> {
  return runCommand([
    "sh",
    "-lc",
    `curl -sSL --compressed --max-time 30 ${JSON.stringify(url.toString())} | w3m -dump -T text/html`,
  ]);
}

async function fetchHttpStatusCode(url: URL): Promise<number | undefined> {
  const result = await runCommand([
    "sh",
    "-lc",
    `curl -sSIL --compressed --max-time 30 -o /dev/null -w '%{http_code}' ${JSON.stringify(url.toString())}`,
  ]);
  if (result.exitCode !== 0) return undefined;
  const code = Number.parseInt(result.stdoutText.trim(), 10);
  if (!Number.isFinite(code)) return undefined;
  if (code < 100 || code > 599) return undefined;
  return code;
}

function formatArxivServiceMessage(input: {
  url: URL;
  statusCode?: number;
  content: string;
}): string | undefined {
  if (!hostMatchesDomain(input.url.hostname, "arxiv.org")) return undefined;
  const body = input.content.trim().toLowerCase();

  if (input.statusCode === 429 || body === "rate exceeded." || body === "rate exceeded") {
    return [
      "arXiv API case: `429 Rate exceeded`.",
      "Interpretation: this indicates arXiv server capacity pressure, not abusive request rate from your script.",
      "Action: retry later with backoff; keep polite spacing (~3 seconds) between repeated API calls.",
      "Reference: https://groups.google.com/a/arxiv.org/g/api/c/pNB3lnxf4mQ",
    ].join("\n");
  }

  if (input.statusCode === 503) {
    return [
      "arXiv API case: `503 Service Unavailable`.",
      "Interpretation: this is the excessive-use signal from arXiv API ops.",
      "Action: reduce request frequency, use smaller slices/paging, and keep polite spacing (~3 seconds) between repeated calls.",
      "Reference: https://groups.google.com/a/arxiv.org/g/api/c/pNB3lnxf4mQ",
    ].join("\n");
  }

  return undefined;
}

function buildArxivFallbackUrl(url: URL): URL | undefined {
  if (!hostMatchesDomain(url.hostname, "arxiv.org")) return undefined;
  if (url.pathname !== "/api/query") return undefined;

  const rawIdList = (url.searchParams.get("id_list") ?? "").trim();
  if (rawIdList) {
    const firstId = rawIdList
      .split(",")
      .map((item) => item.trim())
      .find((item) => item.length > 0);
    if (firstId) {
      const normalizedId = firstId.replace(/^arxiv:/i, "");
      const fallback = new URL("https://arxiv.org/");
      fallback.pathname = `/abs/${normalizedId}`;
      return fallback;
    }
  }

  const rawSearch = (url.searchParams.get("search_query") ?? "").trim();
  if (rawSearch) {
    const fallback = new URL("https://arxiv.org/search/");
    fallback.searchParams.set("query", rawSearch);
    fallback.searchParams.set("searchtype", "all");
    fallback.searchParams.set("source", "header");
    return fallback;
  }

  return undefined;
}

function isLikelyArxivErrorBody(content: string): boolean {
  const normalized = content.trim().toLowerCase();
  return (
    normalized === "rate exceeded." ||
    normalized === "rate exceeded" ||
    normalized === "service unavailable." ||
    normalized === "service unavailable" ||
    normalized === "service temporarily unavailable." ||
    normalized === "service temporarily unavailable" ||
    normalized.includes("service temporarily unavailable") ||
    normalized.includes("too many requests")
  );
}

async function formatWebFetchOutput(input: {
  routeName: string;
  sourceUrl: string;
  content: string;
}): Promise<string> {
  const text = input.content.trim();
  const prefix = [
    `Tool passphrase: ${PASSPHRASE_WEBFETCH}`,
    `Route: ${input.routeName}`,
    `Source URL: ${input.sourceUrl}`,
  ];
  if (!text) {
    return [...prefix, "", "No readable text content extracted from this page."].join("\n");
  }

  const inlineReport = [...prefix, "", text].join("\n");
  const tokenCount = countTokens(inlineReport);
  if (tokenCount > WEBFETCH_INLINE_TOKEN_LIMIT) {
    const outputPath = `/tmp/webfetch-${Date.now()}-${crypto.randomUUID()}.txt`;
    await Bun.write(outputPath, inlineReport);
    return [
      ...prefix,
      `Token count: ${tokenCount}`,
      `Saved full content: ${outputPath}`,
      `Full report exceeds inline limit (${WEBFETCH_INLINE_TOKEN_LIMIT} tokens).`,
      "Use your normal file-reading tools to inspect the saved file.",
    ].join("\n");
  }

  return [...prefix, `Token count: ${tokenCount}`, "", text].join("\n");
}

type RedditPostRef = {
  subreddit: string;
  postId: string;
  slug: string;
};

function extractRedditPostRef(url: URL): RedditPostRef | undefined {
  const match = url.pathname.match(/^\/r\/([^/]+)\/comments\/([a-z0-9]+)(?:\/([^/?#]+))?/i);
  if (!match) return undefined;
  const subreddit = decodeURIComponent(match[1] ?? "").trim();
  const postId = (match[2] ?? "").trim().toLowerCase();
  const slug = decodeURIComponent((match[3] ?? "").replace(/[_-]+/g, " ")).trim();
  if (!subreddit || !postId) return undefined;
  return { subreddit, postId, slug };
}

type RedditRecord = Record<string, unknown>;

function normalizeRedditId(raw: unknown): string {
  return String(raw ?? "")
    .trim()
    .toLowerCase()
    .replace(/^t[0-9]_/, "");
}

function redditText(raw: unknown): string {
  return String(raw ?? "").trim();
}

function renderRedditCommentTree(comments: RedditRecord[], postId: string): string[] {
  const byId = new Map<string, RedditRecord>();
  const children = new Map<string, RedditRecord[]>();
  for (const comment of comments) {
    const commentId = normalizeRedditId(comment.comment_id);
    if (!commentId) continue;
    byId.set(commentId, comment);
  }
  for (const comment of comments) {
    const commentId = normalizeRedditId(comment.comment_id);
    if (!commentId) continue;
    const parentId = normalizeRedditId(comment.parent_id);
    const key = byId.has(parentId) ? parentId : postId;
    const arr = children.get(key) ?? [];
    arr.push(comment);
    children.set(key, arr);
  }

  const sortByScoreThenTime = (a: RedditRecord, b: RedditRecord) => {
    const sa = Number(a.score ?? 0);
    const sb = Number(b.score ?? 0);
    if (sb !== sa) return sb - sa;
    const ta = Number(a.created_utc_ts ?? 0);
    const tb = Number(b.created_utc_ts ?? 0);
    return ta - tb;
  };

  const render = (parentId: string, depth: number, out: string[]) => {
    const items = [...(children.get(parentId) ?? [])].sort(sortByScoreThenTime);
    for (const comment of items) {
      const commentId = normalizeRedditId(comment.comment_id);
      if (!commentId) continue;
      const indent = "  ".repeat(depth);
      const author = String(comment.author ?? "[deleted]").trim() || "[deleted]";
      const score = Number(comment.score ?? 0);
      const body = redditText(comment.text);
      out.push(`${indent}- u/${author} (score ${score}):`);
      if (body) {
        for (const line of body.split(/\r?\n/)) {
          out.push(`${indent}  ${line}`);
        }
      } else {
        out.push(`${indent}  [no text]`);
      }
      render(commentId, depth + 1, out);
    }
  };

  const lines: string[] = [];
  render(postId, 0, lines);
  return lines;
}

function buildRedditSearchQuery(postRef: RedditPostRef): string {
  if (postRef.slug) return postRef.slug;
  return postRef.postId;
}

async function fetchRedditPostMarkdown(input: { url: URL }): Promise<WebFetchHandlerResult> {
  const postRef = extractRedditPostRef(input.url);
  if (!postRef) {
    const fallback = await fetchWebContentWithW3M(input.url);
    if (fallback.exitCode !== 0) {
      throw new Error(`reddit fallback fetch failed (exit ${fallback.exitCode}): ${fallback.stderrText.trim()}`);
    }
    return {
      routeName: "reddit",
      sourceUrl: input.url.toString(),
      content: fallback.stdoutText,
    };
  }

  const actorInput = {
    mode: "search",
    search: {
      queries: [buildRedditSearchQuery(postRef)],
      sort: "relevance",
      timeframe: "all",
      maxPostsPerQuery: 25,
      restrictToSubreddit: postRef.subreddit,
      includeNsfw: false,
      selfPostsOnly: false,
      commentsMode: "all",
      commentsMaxTopLevel: 100,
      commentsMaxDepth: 3,
      commentsHighEngagementMinScore: 10,
      commentsHighEngagementMinComments: 5,
      commentsHighEngagementFilterPosts: false,
      overrides: [],
      targets: [],
    },
    includeRaw: false,
    proxyConfiguration: {
      useApifyProxy: true,
      apifyProxyGroups: ["RESIDENTIAL"],
    },
    proxyCountry: "US",
    proxyRotationStrategy: "sticky_pool",
    proxyPoolSize: 10,
    requestDelayMs: 100,
  };

  const inputPath = `/tmp/reddit-apify-input-${Date.now()}-${crypto.randomUUID()}.json`;
  await Bun.write(inputPath, JSON.stringify(actorInput));
  try {
    const result = await runCommand([
      "apify",
      "call",
      REDDIT_APIFY_ACTOR,
      "--silent",
      "--output-dataset",
      "--input-file",
      inputPath,
    ]);
    if (result.exitCode !== 0) {
      throw new Error(`apify call failed (exit ${result.exitCode}): ${result.stderrText.trim()}`);
    }

    let items: RedditRecord[];
    try {
      const parsed = JSON.parse(result.stdoutText);
      if (!Array.isArray(parsed)) {
        throw new Error("dataset output is not an array");
      }
      items = parsed as RedditRecord[];
    } catch (error) {
      throw new Error(
        `apify output parse failed: ${error instanceof Error ? error.message : String(error)}`,
      );
    }

    const postMatch = items
      .filter((item) => item.record_type === "post")
      .find((item) => String(item.permalink ?? "").includes(`/comments/${postRef.postId}/`));
    if (!postMatch) {
      throw new Error(`no Reddit post match for permalink id ${postRef.postId}`);
    }

    const targetPostId = normalizeRedditId(postMatch.post_id) || postRef.postId;
    const comments = items.filter(
      (item) => item.record_type === "comment" && normalizeRedditId(item.post_id) === targetPostId,
    );

    const title = redditText(postMatch.title) || "[untitled]";
    const body = redditText(postMatch.text);
    const author = String(postMatch.author ?? "[deleted]").trim() || "[deleted]";
    const subreddit = String(postMatch.subreddit ?? postRef.subreddit).trim() || postRef.subreddit;
    const permalink = redditText(postMatch.permalink) || input.url.toString();
    const score = Number(postMatch.score ?? 0);
    const numComments = Number(postMatch.num_comments ?? comments.length);

    const lines: string[] = [
      "# Reddit Post",
      "",
      `- URL: ${input.url.toString()}`,
      `- Permalink: ${permalink}`,
      `- Subreddit: r/${subreddit}`,
      `- Author: u/${author}`,
      `- Score: ${score}`,
      `- Comments reported by post: ${numComments}`,
      `- Comments extracted: ${comments.length}`,
      "",
      "## Title",
      "",
      title,
      "",
      "## Body",
      "",
      body || "[no post body]",
      "",
      "## Comments (nested)",
      "",
    ];

    if (comments.length === 0) {
      lines.push("[no comments extracted]");
    } else {
      lines.push(...renderRedditCommentTree(comments, targetPostId));
    }

    return {
      routeName: "reddit",
      sourceUrl: permalink,
      content: lines.join("\n"),
    };
  } finally {
    await unlink(inputPath).catch(() => {});
  }
}

function augmentQueryWithDomains(query: string, domains: string[]): string {
  if (domains.length === 0) return query;
  // `site:` is query syntax forwarded to engines; behavior depends on engine support.
  const siteClauses = domains.map((domain) => `site:${domain}`);
  return `${query} (${siteClauses.join(" OR ")})`;
}

function mapRecencyToTimeRange(recency?: number): string | undefined {
  if (!Number.isFinite(recency)) return undefined;
  const days = Math.max(0, Math.floor(recency ?? 0));
  if (days <= 1) return "day";
  if (days <= 31) return "month";
  return "year";
}

function buildQueryUrl(baseUrl: string, args: { query: string; timeRange?: string; pageNumber?: number }): URL {
  const url = new URL(`${normalizeBaseUrl(baseUrl)}/search`);
  url.searchParams.set("q", args.query);
  url.searchParams.set("format", "json");

  if (args.timeRange) {
    url.searchParams.set("time_range", args.timeRange);
  }
  if (args.pageNumber && args.pageNumber > 1) {
    url.searchParams.set("pageno", String(args.pageNumber));
  }

  return url;
}

function asResponse(input: unknown): SearxngResponse {
  if (!input || typeof input !== "object") {
    throw new Error("Invalid search API response: expected object.");
  }
  const response = input as Record<string, unknown>;

  if (typeof response.query !== "string") {
    throw new Error("Invalid search API response: missing query.");
  }
  if (typeof response.number_of_results !== "number" || !Number.isFinite(response.number_of_results)) {
    throw new Error("Invalid search API response: missing number_of_results.");
  }
  if (!Array.isArray(response.results)) {
    throw new Error("Invalid search API response: missing results array.");
  }
  if (!Array.isArray(response.answers)) {
    throw new Error("Invalid search API response: missing answers array.");
  }
  if (!Array.isArray(response.suggestions)) {
    throw new Error("Invalid search API response: missing suggestions array.");
  }
  if (!Array.isArray(response.unresponsive_engines)) {
    throw new Error("Invalid search API response: missing unresponsive_engines array.");
  }

  for (const item of response.results) {
    if (!item || typeof item !== "object") {
      throw new Error("Invalid search API response: result item is not an object.");
    }
    const result = item as Record<string, unknown>;
    if (typeof result.title !== "string" || typeof result.url !== "string") {
      throw new Error("Invalid search API response: result item missing title/url.");
    }
    if (typeof result.content !== "string") {
      throw new Error("Invalid search API response: result item missing content.");
    }
    if (typeof result.engine !== "string" || typeof result.category !== "string") {
      throw new Error("Invalid search API response: result item missing engine/category.");
    }
    if (!(typeof result.publishedDate === "string" || result.publishedDate === null)) {
      throw new Error("Invalid search API response: invalid publishedDate.");
    }
  }

  return response as unknown as SearxngResponse;
}

function resolveCategory(category?: string): { bang?: string; error?: string } {
  if (!category) return {};
  const raw = category.trim().toLowerCase();
  if (!raw) return {};

  if (raw.startsWith("!")) {
    return {
      error:
        `Invalid category: ${JSON.stringify(category)}. ` +
        "Use bare category names only.",
    };
  }

  const normalized = raw;
  if (!VALID_CATEGORIES.has(normalized)) {
    return {
      error:
        `Invalid category: ${JSON.stringify(category)}. ` +
        `Allowed categories: ${NARROWING_CATEGORIES.join(", ")}.`,
    };
  }

  return { bang: `!${normalized}` };
}

function formatResults(input: {
  query: string;
  category?: string;
  response: SearxngResponse;
  offset: number;
  limit: number;
}): string {
  const top = input.response.results.slice(0, input.limit);
  const start = top.length > 0 ? input.offset + 1 : 0;
  const end = input.offset + top.length;
  const total = input.response.number_of_results;

  const lines: string[] = [];
  lines.push(`Query: ${input.query}`);
  if (input.category) {
    lines.push(`Category: ${input.category}`);
  }
  lines.push(`Offset: ${input.offset}`);
  lines.push(`Total results: ${total}`);
  if (top.length > 0) {
    lines.push(`Showing results: ${start}-${end} of ${total}`);
  } else {
    lines.push("Showing results: none");
  }
  lines.push(`Returned results: ${top.length}`);

  if (top.length === 0) {
    lines.push("No results returned.");
    if (input.response.answers.length > 0) {
      lines.push(`Answers: ${input.response.answers.map((x) => x.trim()).filter(Boolean).join(" | ")}`);
    }
    if (input.response.suggestions.length > 0) {
      lines.push(`Suggestions: ${input.response.suggestions.join(", ")}`);
    }
    lines.push("");
    lines.push("Continuation hints:");
    lines.push("- Snippets are truncated. Use webfetch on a selected URL to read full page contents.");
    lines.push(`- To continue pagination, rerun with offset ${input.offset + input.limit}.`);
    return lines.join("\n");
  }

  lines.push("");
  lines.push("Top results:");

  for (const [index, result] of top.entries()) {
    const rank = index + 1;
    const title = result.title.trim();
    const url = result.url.trim();
    lines.push(`${rank}. ${title}`);
    lines.push(`   URL: ${url}`);

    if (result.publishedDate) {
      lines.push(`   Published: ${result.publishedDate}`);
    }

    if (result.content.trim()) {
      lines.push(`   Snippet: ${clampSnippet(result.content)}`);
    }
  }

  lines.push("");
  lines.push("Continuation hints:");
  lines.push("- Snippets are truncated. Use webfetch on a selected URL to read full page contents.");
  lines.push(`- To continue pagination, rerun with offset ${input.offset + top.length}.`);

  return lines.join("\n");
}

export const ImprovedWebSearchPlugin: Plugin = async ({ client }) => {
  const webFetchDomainHandlers: readonly WebFetchDomainHandler[] = [
    {
      name: "reddit",
      domains: REDDIT_DOMAINS,
      handle: async ({ url }) => fetchRedditPostMarkdown({ url }),
    },
    {
      name: "github",
      domains: GITHUB_DOMAINS,
      handle: async ({ url }) => {
        const plan = buildGitHubCommandPlan(url);
        const result = await runCommand(plan.args);
        if (result.exitCode !== 0) {
          throw new Error(
            `gh command failed (exit ${result.exitCode}): ${result.stderrText.trim()}`,
          );
        }
        return {
          routeName: "github",
          sourceUrl: plan.sourceUrl,
          content: result.stdoutText,
        };
      },
    },
  ];

  return {
    tool: {
      webfetch: tool({
        description: "Use when you need to read a webpage URL as plain text content.",
        args: {
          url: tool.schema.string(),
          prompt: tool.schema.string().optional(),
        },
        async execute(args, context) {
          const rawUrl = args.url.trim();
          let parsed: URL;
          try {
            parsed = new URL(rawUrl);
          } catch {
            return [
              `Tool passphrase: ${PASSPHRASE_WEBFETCH}`,
              `Invalid URL: ${JSON.stringify(args.url)}.`,
            ].join("\n");
          }

          if (parsed.protocol !== "http:" && parsed.protocol !== "https:") {
            return [
              `Tool passphrase: ${PASSPHRASE_WEBFETCH}`,
              `Unsupported URL protocol for webfetch: ${parsed.protocol}`,
            ].join("\n");
          }

          await context.ask({
            permission: "webfetch",
            patterns: [parsed.toString()],
            always: ["*"],
            metadata: {
              url: parsed.toString(),
            },
          });

          context.metadata({
            title: `Web fetch: ${parsed.hostname}${parsed.pathname}`.slice(0, 120),
          });

          try {
            const cacheKey = parsed.toString();
            const cached = await readWebFetchCache(cacheKey);
            if (cached) {
              return formatWebFetchOutput({
                routeName: `${cached.routeName}/cache`,
                sourceUrl: cached.sourceUrl,
                content: cached.content,
              });
            }
            const handler = findWebFetchHandler(webFetchDomainHandlers, parsed);
            const fetched = handler
              ? await handler.handle({ url: parsed })
              : await (async () => {
                  const [statusCode, defaultResult] = await Promise.all([
                    fetchHttpStatusCode(parsed),
                    fetchWebContentWithW3M(parsed),
                  ]);
                  if (defaultResult.exitCode !== 0) {
                    throw new Error(
                      `default webfetch failed (exit ${defaultResult.exitCode}): ${defaultResult.stderrText.trim()}`,
                    );
                  }
                  const serviceMessage = formatArxivServiceMessage({
                    url: parsed,
                    statusCode,
                    content: defaultResult.stdoutText,
                  });
                  if (serviceMessage) {
                    const fallbackUrl = buildArxivFallbackUrl(parsed);
                    if (fallbackUrl) {
                      const fallbackResult = await fetchWebContentWithW3M(fallbackUrl);
                      if (
                        fallbackResult.exitCode === 0 &&
                        fallbackResult.stdoutText.trim().length > 0 &&
                        !isLikelyArxivErrorBody(fallbackResult.stdoutText)
                      ) {
                        return {
                          routeName: "default",
                          sourceUrl: fallbackUrl.toString(),
                          content: [
                            serviceMessage,
                            `Fallback: loaded arXiv web page via w3m from ${fallbackUrl.toString()}.`,
                            "",
                            fallbackResult.stdoutText,
                          ].join("\n"),
                        };
                      }
                    }
                    return {
                      routeName: "default",
                      sourceUrl: parsed.toString(),
                      content: serviceMessage,
                    };
                  }
                  return {
                    routeName: "default",
                    sourceUrl: parsed.toString(),
                    content: defaultResult.stdoutText,
                  };
                })();
            await writeWebFetchCache(cacheKey, fetched);

            return formatWebFetchOutput({
              routeName: fetched.routeName,
              sourceUrl: fetched.sourceUrl,
              content: fetched.content,
            });
          } catch (error) {
            const message = error instanceof Error ? error.message : String(error);
            await client.app.log({
              body: {
                service: "web-search-plugin",
                level: "error",
                message: "webfetch execution error",
                extra: {
                  url: parsed.toString(),
                  error: message,
                },
              },
            });
            return [
              `Tool passphrase: ${PASSPHRASE_WEBFETCH}`,
              "Failed to fetch URL.",
              "If this persists, ask the user to check webfetch/plugin logs.",
            ].join("\n");
          }
        },
      }),

      websearch: tool({
        description:
          "Use when you need to search the web. Optional categories for narrowing only: news, it, npm, pypi, st, gh, hf, ollama, hn, science, arx, cr, gos, se, aa, lg. Use offset and numResults to paginate.",
        args: {
          query: tool.schema.string(),
          category: tool.schema.string().optional(),
          numResults: tool.schema.number().optional(),
          num_results: tool.schema.number().optional(),
          offset: tool.schema.number().optional(),
          recency: tool.schema.number().optional(),
          domains: tool.schema.array(tool.schema.string()).optional(),
          search_query: tool.schema
            .array(
              tool.schema.object({
                q: tool.schema.string(),
                category: tool.schema.string().optional(),
                num_results: tool.schema.number().optional(),
                numResults: tool.schema.number().optional(),
                offset: tool.schema.number().optional(),
                recency: tool.schema.number().optional(),
                domains: tool.schema.array(tool.schema.string()).optional(),
              }),
            )
            .min(1)
            .optional(),
        },
        async execute(args, context) {
          const baseUrl = SEARXNG_INSTANCE_URL;
          if (!baseUrl) {
            return [
              `Tool passphrase: ${PASSPHRASE_WEB_SEARCH}`,
              "Web search is unavailable in this environment. Ask the user to check plugin configuration.",
            ].join("\n");
          }

          const rawQueries = args.search_query as SearchQueryInput[] | undefined;
          const queries: SearchQueryInput[] =
            rawQueries && rawQueries.length > 0
              ? rawQueries
              : [
                  {
                    q: args.query,
                    category: args.category,
                    num_results: args.num_results,
                    numResults: args.numResults,
                    offset: args.offset,
                    recency: args.recency,
                    domains: args.domains,
                  },
                ];
          const firstQuery = queries[0]?.q?.trim() ?? "";
          if (!firstQuery) {
            return [`Tool passphrase: ${PASSPHRASE_WEB_SEARCH}`, "Invalid search_query: first query is empty."].join("\n");
          }

          await context.ask({
            permission: "websearch",
            patterns: queries.map((item) => item.q.trim()).filter(Boolean),
            always: ["*"],
            metadata: {
              query: firstQuery,
              queryCount: queries.length,
            },
          });

          const firstLimit = parseLimit(queries[0]?.numResults ?? queries[0]?.num_results ?? args.numResults ?? args.num_results);

          context.metadata({
            title: `Web search: ${firstQuery.slice(0, 72)}`,
            metadata: {
              numResults: firstLimit,
              queryCount: queries.length,
            },
          });

          const timeoutSignal = AbortSignal.timeout(DEFAULT_TIMEOUT_MS);
          const signal = AbortSignal.any([context.abort, timeoutSignal]);

          const blocks: string[] = [];

          for (const [index, input] of queries.entries()) {
            const query = input.q.trim();
            if (!query) {
              blocks.push(`Query ${index + 1}: invalid empty query.`);
              continue;
            }

            const domains = (input.domains ?? [])
              .map((domain) => domain.trim())
              .filter(Boolean);

            const category = resolveCategory(input.category);
            if (category.error) {
              blocks.push(`Query ${index + 1}: ${category.error}`);
              continue;
            }

            const offset = resolveOffset(input.offset);
            if (offset.error) {
              blocks.push(`Query ${index + 1}: ${offset.error}`);
              continue;
            }
            const limit = parseLimit(input.numResults ?? input.num_results);

            let effectiveQuery = augmentQueryWithDomains(query, domains);
            if (category.bang) {
              effectiveQuery = `${category.bang} ${effectiveQuery}`;
            }

            try {
              const timeRange = mapRecencyToTimeRange(input.recency);
              const neededCount = offset.value + limit;
              const collected: SearxngResult[] = [];
              let firstResponse: SearxngResponse | undefined;

              for (let page = 1; page <= MAX_PAGE_FETCHES && collected.length < neededCount; page += 1) {
                const url = buildQueryUrl(baseUrl, {
                  query: effectiveQuery,
                  timeRange,
                  pageNumber: page,
                });
                const response = await fetch(url, {
                  method: "GET",
                  headers: {
                    accept: "application/json",
                  },
                  signal,
                });

                if (!response.ok) {
                  const body = await response.text();
                  await client.app.log({
                    body: {
                      service: "web-search-plugin",
                      level: "error",
                      message: `web_search request failed: HTTP ${response.status} ${response.statusText}`,
                      extra: {
                        queryIndex: index + 1,
                        query,
                        category: input.category ?? null,
                        offset: offset.value,
                        numResults: limit,
                        status: response.status,
                        statusText: response.statusText,
                        responseBody: clampSnippet(body, 2000),
                      },
                    },
                  });
                  blocks.push(
                    [
                      `Query ${index + 1}: search request failed (HTTP ${response.status}).`,
                      "If this persists, ask the user to check search backend/plugin logs.",
                    ]
                      .filter(Boolean)
                      .join("\n"),
                  );
                  firstResponse = undefined;
                  break;
                }

                const pageData = asResponse(await response.json());
                if (!firstResponse) {
                  firstResponse = pageData;
                }

                const pageResults = pageData.results;
                if (pageResults.length === 0) {
                  break;
                }
                collected.push(...pageResults);
              }

              if (!firstResponse) {
                continue;
              }

              const windowedResults = collected.slice(offset.value, offset.value + limit);
              const data: SearxngResponse = {
                ...firstResponse,
                results: windowedResults,
              };
              blocks.push(
                [
                  `Query ${index + 1}:`,
                  formatResults({
                    query,
                    category: input.category,
                    response: data,
                    offset: offset.value,
                    limit,
                  }),
                ].join("\n"),
              );
            } catch (error) {
              const message = error instanceof Error ? error.message : String(error);
              await client.app.log({
                body: {
                  service: "web-search-plugin",
                  level: "error",
                  message: "web_search execution error",
                  extra: {
                    queryIndex: index + 1,
                    query,
                    category: input.category ?? null,
                    offset: offset.value,
                    numResults: limit,
                    error: message,
                  },
                },
              });
              blocks.push(
                [
                  `Query ${index + 1}: search request failed.`,
                  "If this persists, ask the user to check search backend/plugin logs.",
                ].join("\n"),
              );
            }
          }

          return [`Tool passphrase: ${PASSPHRASE_WEB_SEARCH}`, "", blocks.join("\n\n---\n\n")].join("\n");
        },
      }),
    },
  };
};

// Backward-compatible export name while transitioning to improved-* naming.
export const SearxngSearchPlugin = ImprovedWebSearchPlugin;
