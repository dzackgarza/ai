import { type Plugin, tool } from "@opencode-ai/plugin";
import { getEncoding } from "js-tiktoken";

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

const SEARXNG_INSTANCE_URL = (process.env.SEARXNG_INSTANCE_URL ?? "").trim();
const DEFAULT_TIMEOUT_MS = 15_000;
const DEFAULT_LIMIT = 8;
const MAX_LIMIT = 20;
const MAX_OFFSET = 200;
const MAX_PAGE_FETCHES = 20;
const WEBFETCH_INLINE_TOKEN_LIMIT = 20_000;
const TOKEN_ENCODER = getEncoding("o200k_base");
const PASSPHRASE_WEB_SEARCH = "PASS_WEB_SEARCH_SHADOW_20260305_6A9F";
const PASSPHRASE_WEBFETCH = "PASS_WEBFETCH_SHADOW_20260305_C3D2";

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
            const proc = Bun.spawn(
              [
                "sh",
                "-lc",
                `curl -sSL --compressed --max-time 30 ${JSON.stringify(parsed.toString())} | w3m -dump -T text/html`,
              ],
              {
                stderr: "pipe",
                stdout: "pipe",
              },
            );

            const [stdoutText, stderrText, exitCode] = await Promise.all([
              new Response(proc.stdout).text(),
              new Response(proc.stderr).text(),
              proc.exited,
            ]);

            if (exitCode !== 0) {
              await client.app.log({
                body: {
                  service: "web-search-plugin",
                  level: "error",
                  message: `webfetch failed: exit ${exitCode}`,
                  extra: {
                    url: parsed.toString(),
                    stderr: stderrText.trim().slice(0, 2000),
                  },
                },
              });
              return [
                `Tool passphrase: ${PASSPHRASE_WEBFETCH}`,
                `Failed to fetch URL (exit ${exitCode}).`,
                "If this persists, ask the user to check webfetch/plugin logs.",
              ].join("\n");
            }

            const text = stdoutText.trim();
            if (!text) {
              return [
                `Tool passphrase: ${PASSPHRASE_WEBFETCH}`,
                `Source URL: ${parsed.toString()}`,
                "",
                "No readable text content extracted from this page.",
              ].join("\n");
            }

            const tokenCount = countTokens(text);
            if (tokenCount > WEBFETCH_INLINE_TOKEN_LIMIT) {
              const outputPath = `/tmp/webfetch-${Date.now()}-${crypto.randomUUID()}.txt`;
              await Bun.write(outputPath, text);
              return [
                `Tool passphrase: ${PASSPHRASE_WEBFETCH}`,
                `Source URL: ${parsed.toString()}`,
                `Token count: ${tokenCount}`,
                `Saved full content: ${outputPath}`,
                `Content exceeds inline limit (${WEBFETCH_INLINE_TOKEN_LIMIT} tokens).`,
                "Use your normal file-reading tools to inspect the saved file.",
              ].join("\n");
            }

            return [
              `Tool passphrase: ${PASSPHRASE_WEBFETCH}`,
              `Source URL: ${parsed.toString()}`,
              `Token count: ${tokenCount}`,
              "",
              text,
            ].join("\n");
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
