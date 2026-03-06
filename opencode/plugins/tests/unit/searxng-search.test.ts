import { afterEach, beforeEach, describe, expect, it } from "bun:test";
import { mkdtemp, rm } from "node:fs/promises";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";

type AskInput = {
  permission: string;
  patterns: string[];
  always: string[];
  metadata: Record<string, unknown>;
};

type MetadataInput = {
  title?: string;
  metadata?: Record<string, unknown>;
};

type MockContext = {
  sessionID: string;
  messageID: string;
  agent: string;
  directory: string;
  worktree: string;
  abort: AbortSignal;
  asks: AskInput[];
  metadatas: MetadataInput[];
  ask: (input: AskInput) => Promise<void>;
  metadata: (input: MetadataInput) => void;
};

function buildContext(): MockContext {
  const asks: AskInput[] = [];
  const metadatas: MetadataInput[] = [];
  return {
    sessionID: "ses_test",
    messageID: "msg_test",
    agent: "LocalMinimalShadow",
    directory: "/tmp",
    worktree: "/tmp",
    abort: new AbortController().signal,
    asks,
    metadatas,
    ask: async (input: AskInput) => {
      asks.push(input);
    },
    metadata: (input: MetadataInput) => {
      metadatas.push(input);
    },
  };
}

function streamFromText(text: string): ReadableStream<Uint8Array> {
  const bytes = new TextEncoder().encode(text);
  return new ReadableStream<Uint8Array>({
    start(controller) {
      controller.enqueue(bytes);
      controller.close();
    },
  });
}

function fixtureText(relativePath: string): string {
  const path = new URL(`../fixtures/real/${relativePath}`, import.meta.url);
  return readFileSync(path, "utf8");
}

function fixtureJson<T>(relativePath: string): T {
  return JSON.parse(fixtureText(relativePath)) as T;
}

async function loadPlugin(
  instanceUrl: string,
  options?: {
    webfetchCacheEnabled?: "0" | "1";
    webfetchCacheDir?: string;
    webfetchCacheTtlDays?: string;
  },
) {
  process.env.SEARXNG_INSTANCE_URL = instanceUrl;
  process.env.WEBFETCH_CACHE_ENABLED = options?.webfetchCacheEnabled ?? "1";
  process.env.WEBFETCH_CACHE_DIR =
    options?.webfetchCacheDir ??
    `/tmp/opencode-webfetch-test-${Date.now()}-${Math.random().toString(16).slice(2)}`;
  if (options?.webfetchCacheTtlDays) {
    process.env.WEBFETCH_CACHE_TTL_DAYS = options.webfetchCacheTtlDays;
  } else {
    delete process.env.WEBFETCH_CACHE_TTL_DAYS;
  }
  const mod = await import(
    new URL(`../../searxng-search.ts?ts=${Date.now()}-${Math.random()}`, import.meta.url).href
  );

  const client = {
    app: {
      log: async () => {},
    },
  };

  const plugin = await mod.ImprovedWebSearchPlugin({ client } as any);
  return {
    websearch: plugin.tool!.websearch,
    webfetch: plugin.tool!.webfetch,
  };
}

describe("searxng-search plugin", () => {
  const originalFetch = globalThis.fetch;
  const originalSpawn = Bun.spawn;
  const originalWrite = Bun.write;
  const originalSearxngUrl = process.env.SEARXNG_INSTANCE_URL;
  const originalCacheEnabled = process.env.WEBFETCH_CACHE_ENABLED;
  const originalCacheDir = process.env.WEBFETCH_CACHE_DIR;
  const originalCacheTtlDays = process.env.WEBFETCH_CACHE_TTL_DAYS;

  beforeEach(() => {
    globalThis.fetch = originalFetch;
    (Bun as any).spawn = originalSpawn;
    (Bun as any).write = originalWrite;
  });

  afterEach(() => {
    globalThis.fetch = originalFetch;
    (Bun as any).spawn = originalSpawn;
    (Bun as any).write = originalWrite;
    if (originalSearxngUrl === undefined) delete process.env.SEARXNG_INSTANCE_URL;
    else process.env.SEARXNG_INSTANCE_URL = originalSearxngUrl;
    if (originalCacheEnabled === undefined) delete process.env.WEBFETCH_CACHE_ENABLED;
    else process.env.WEBFETCH_CACHE_ENABLED = originalCacheEnabled;
    if (originalCacheDir === undefined) delete process.env.WEBFETCH_CACHE_DIR;
    else process.env.WEBFETCH_CACHE_DIR = originalCacheDir;
    if (originalCacheTtlDays === undefined) delete process.env.WEBFETCH_CACHE_TTL_DAYS;
    else process.env.WEBFETCH_CACHE_TTL_DAYS = originalCacheTtlDays;
  });

  it("formats batched websearch results with per-query pagination and separation", async () => {
    const pageOpenAI1 = fixtureJson<{
      results: Array<Record<string, unknown>>;
    }>("searxng/openai-page1.json");
    const pageOpenAI2 = fixtureJson<{
      results: Array<Record<string, unknown>>;
    }>("searxng/openai-page2.json");
    const pageArxiv1 = fixtureJson<{
      results: Array<Record<string, unknown>>;
    }>("searxng/arxiv-lattice-page1.json");
    const responses = new Map<string, unknown>([
      ["openai|1", pageOpenAI1 as unknown],
      ["openai|2", pageOpenAI2 as unknown],
      ["arxiv lattice|1", pageArxiv1 as unknown],
    ]);

    const openAiExpectedWindow = [
      ...pageOpenAI1.results,
      ...pageOpenAI2.results,
    ].slice(1, 3);
    const arxivFirst = pageArxiv1.results[0]!;

    (globalThis as any).fetch = async (input: string | Request | URL) => {
      const url = new URL(String(input));
      const q = url.searchParams.get("q") ?? "";
      const page = Number(url.searchParams.get("pageno") ?? "1");
      const key = `${q}|${page}`;
      const body = responses.get(key);
      if (!body) {
        return new Response(JSON.stringify({ error: `unexpected key ${key}` }), { status: 500 });
      }
      return new Response(JSON.stringify(body), {
        status: 200,
        headers: { "content-type": "application/json" },
      });
    };

    const { websearch } = await loadPlugin("http://localhost/searxng");
    const context = buildContext();

    const output = await websearch.execute(
      {
        query: "fallback query",
        search_query: [
          {
            q: "openai",
            num_results: 2,
            offset: 1,
          },
          {
            q: "arxiv lattice",
            num_results: 1,
          },
        ],
      },
      context as any,
    );

    expect(context.asks).toHaveLength(1);
    expect(context.asks[0]).toEqual({
      permission: "websearch",
      patterns: ["openai", "arxiv lattice"],
      always: ["*"],
      metadata: {
        query: "openai",
        queryCount: 2,
      },
    });

    expect(context.metadatas).toHaveLength(1);
    expect(context.metadatas[0]).toEqual({
      title: "Web search: openai",
      metadata: {
        numResults: 2,
        queryCount: 2,
      },
    });

    expect(output).toContain("Tool passphrase: PASS_WEB_SEARCH_SHADOW_20260305_6A9F");
    expect(output).toContain("Query 1:");
    expect(output).toContain("Showing results: 2-3 of 0");
    expect(output).toContain(String(openAiExpectedWindow[0]?.url ?? ""));
    expect(output).toContain(String(openAiExpectedWindow[1]?.url ?? ""));
    expect(output).toContain("Query 2:");
    expect(output).toContain(String(arxivFirst.url ?? ""));
    expect(output).toContain("\n\n---\n\n");
  });

  it("returns per-query validation errors for invalid category and offset", async () => {
    (globalThis as any).fetch = async () =>
      new Response(
        JSON.stringify({
          query: "unused",
          number_of_results: 0,
          results: [],
          answers: [],
          suggestions: [],
          unresponsive_engines: [],
        }),
        { status: 200, headers: { "content-type": "application/json" } },
      );

    const { websearch } = await loadPlugin("http://localhost/searxng");
    const context = buildContext();

    const output = await websearch.execute(
      {
        query: "unused",
        search_query: [
          { q: "query a", category: "invalid_category" },
          { q: "query b", offset: -1 },
        ],
      },
      context as any,
    );

    expect(output).toContain("Tool passphrase: PASS_WEB_SEARCH_SHADOW_20260305_6A9F");
    expect(output).toContain(`Query 1: Invalid category: "invalid_category".`);
    expect(output).toContain("Allowed categories: news, it, npm, pypi, st, gh, hf, ollama, hn, science, arx, cr, gos, se, aa, lg.");
    expect(output).toContain("Query 2: Invalid offset: -1. Offset must be a non-negative integer.");
  });

  it("writes oversized webfetch content to /tmp and reports saved path", async () => {
    const largeText = fixtureText("wikipedia/fourier-transform.converted.md");
    const largePrefix = largeText.slice(0, 600).trim();
    const writes: Array<{ path: string; content: string }> = [];

    (Bun as any).spawn = () => ({
      stdout: streamFromText(largeText),
      stderr: streamFromText(""),
      exited: Promise.resolve(0),
    });

    (Bun as any).write = async (path: string, content: string) => {
      writes.push({ path: String(path), content: String(content) });
    };

    const { webfetch } = await loadPlugin("http://localhost/searxng");
    const context = buildContext();

    const output = await webfetch.execute(
      {
        url: "https://example.com/big",
      },
      context as any,
    );

    expect(context.asks).toHaveLength(1);
    expect(context.asks[0]).toEqual({
      permission: "webfetch",
      patterns: ["https://example.com/big"],
      always: ["*"],
      metadata: {
        url: "https://example.com/big",
      },
    });

    expect(context.metadatas).toHaveLength(1);
    expect(context.metadatas[0]?.title).toBe("Web fetch: example.com/big");

    expect(writes).toHaveLength(2);
    const oversizedWrite = writes.find((item) => item.path.startsWith("/tmp/webfetch-"));
    const cacheWrite = writes.find((item) => item.path.endsWith(".json"));
    expect(oversizedWrite).toBeDefined();
    expect(cacheWrite).toBeDefined();
    expect(oversizedWrite!.content).toContain("Tool passphrase: PASS_WEBFETCH_SHADOW_20260305_C3D2");
    expect(oversizedWrite!.content).toContain(`Route: default`);
    expect(oversizedWrite!.content).toContain("Source URL: https://example.com/big");
    expect(oversizedWrite!.content).toContain(largePrefix);

    expect(output).toContain("Tool passphrase: PASS_WEBFETCH_SHADOW_20260305_C3D2");
    expect(output).toContain("Route: default");
    expect(output).toContain("Full report exceeds inline limit (20000 tokens).");
    expect(output).toContain(`Saved full content: ${oversizedWrite!.path}`);
    expect(output).toContain("Token count:");
  });

  it("routes reddit posts through apify and renders nested markdown comments", async () => {
    const apifyDataset = fixtureJson<Array<Record<string, unknown>>>("reddit/apify-search-openai.json");

    (Bun as any).spawn = (args: string[]) => {
      if (args[0] === "apify" && args[1] === "call") {
        return {
          stdout: streamFromText(JSON.stringify(apifyDataset)),
          stderr: streamFromText(""),
          exited: Promise.resolve(0),
        };
      }
      return {
        stdout: streamFromText(""),
        stderr: streamFromText("unexpected command"),
        exited: Promise.resolve(1),
      };
    };

    const { webfetch } = await loadPlugin("http://localhost/searxng");
    const context = buildContext();

    const output = await webfetch.execute(
      {
        url: "https://www.reddit.com/r/OpenAI/comments/1hn44qh/anyone_else_excited_for_o3_mini_release/",
      },
      context as any,
    );

    expect(output).toContain("Tool passphrase: PASS_WEBFETCH_SHADOW_20260305_C3D2");
    expect(output).toContain("Route: reddit");
    expect(output).toContain("Source URL: https://www.reddit.com/r/OpenAI/comments/1hn44qh/anyone_else_excited_for_o3_mini_release/");
    expect(output).toContain("# Reddit Post");
    expect(output).toContain("## Comments (nested)");
    expect(output).toContain("- u/The_GSingh (score 20):");
    expect(output).toContain("When is it even coming out");
    expect(output).toContain("  - u/Thinklikeachef (score 13):");
  });

  it("routes youtube URLs through transcript extraction pipeline", async () => {
    const calls: string[][] = [];
    const listSubs = fixtureText("youtube/dQw4w9WgXcQ.list-subs.txt");
    const vtt = fixtureText("youtube/dQw4w9WgXcQ.en.vtt");

    (Bun as any).spawn = (args: string[]) => {
      calls.push(args);

      if (args[0] === "uvx" && args.includes("yt-dlp") && args.includes("--list-subs")) {
        return {
          stdout: streamFromText(listSubs),
          stderr: streamFromText(""),
          exited: Promise.resolve(0),
        };
      }

      if (args[0] === "uvx" && args.includes("yt-dlp") && args.includes("--write-subs")) {
        const outputIndex = args.indexOf("-o");
        const template = outputIndex >= 0 ? args[outputIndex + 1] : undefined;
        if (template) {
          const dir = dirname(template);
          mkdirSync(dir, { recursive: true });
          writeFileSync(join(dir, "dQw4w9WgXcQ.en.vtt"), vtt);
        }
        return {
          stdout: streamFromText(fixtureText("youtube/dQw4w9WgXcQ.write-subs.out")),
          stderr: streamFromText(fixtureText("youtube/dQw4w9WgXcQ.write-subs.err")),
          exited: Promise.resolve(0),
        };
      }

      return {
        stdout: streamFromText(""),
        stderr: streamFromText("unexpected command"),
        exited: Promise.resolve(1),
      };
    };

    const { webfetch } = await loadPlugin("http://localhost/searxng");
    const context = buildContext();

    const output = await webfetch.execute(
      {
        url: "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
      },
      context as any,
    );

    expect(calls.some((args) => args.includes("--list-subs"))).toBe(true);
    expect(calls.some((args) => args.includes("--write-subs"))).toBe(true);
    expect(output).toContain("Tool passphrase: PASS_WEBFETCH_SHADOW_20260305_C3D2");
    expect(output).toContain("Route: youtube");
    expect(output).toContain("# YouTube Transcript");
    expect(output).toContain("Source: English captions (yt-dlp)");
    expect(output).toContain("We're no strangers to");
  });

  it("routes wikipedia URLs through parse API and markdown conversion", async () => {
    const calls: string[][] = [];
    const fetchCalls: Array<{ url: string; userAgent?: string }> = [];
    const parseFixture = fixtureJson<Record<string, unknown>>("wikipedia/parse-fourier-transform.json");
    const converted = fixtureText("wikipedia/fourier-transform.converted.md");
    const convertedShort = converted.split("\n").slice(0, 120).join("\n");

    (globalThis as any).fetch = async (input: string | Request | URL, init?: RequestInit) => {
      const url = String(input);
      fetchCalls.push({
        url,
        userAgent:
          (init?.headers as Record<string, string> | undefined)?.["User-Agent"] ??
          (init?.headers as Record<string, string> | undefined)?.["user-agent"],
      });
      return new Response(JSON.stringify(parseFixture), {
        status: 200,
        headers: { "content-type": "application/json" },
      });
    };

    (Bun as any).spawn = (args: string[]) => {
      calls.push(args);
      return {
        stdout: streamFromText(convertedShort),
        stderr: streamFromText(""),
        exited: Promise.resolve(0),
      };
    };

    const { webfetch } = await loadPlugin("http://localhost/searxng");
    const context = buildContext();

    const output = await webfetch.execute(
      {
        url: "https://en.wikipedia.org/wiki/Fourier_transform",
      },
      context as any,
    );

    expect(fetchCalls).toHaveLength(1);
    expect(fetchCalls[0]?.url).toContain(
      "https://en.wikipedia.org/w/api.php?action=parse&format=json&formatversion=2&prop=displaytitle%7Ctext&page=Fourier_transform",
    );
    expect(fetchCalls[0]?.userAgent).toBe("opencode-improved-webfetch/1.0 (plugin)");

    expect(calls).toHaveLength(1);
    expect(calls[0]?.[0]).toBe("uvx");
    expect(calls[0]).toContain("beautifulsoup4");
    expect(calls[0]).toContain("markdownify");
    expect(calls[0]).toContain("python");

    expect(output).toContain("Tool passphrase: PASS_WEBFETCH_SHADOW_20260305_C3D2");
    expect(output).toContain("Route: wikipedia");
    expect(output).toContain("Source URL: https://en.wikipedia.org/wiki/Fourier_transform");
    expect(output).toContain("# Fourier transform");
    expect(output).toContain("In [mathematics](https://en.wikipedia.org/wiki/Mathematics");
  });

  it("uses webfetch cache on repeated URL requests with cache enabled", async () => {
    const tempRoot = await mkdtemp("/tmp/opencode-webfetch-cache-test-");
    const cacheDir = join(tempRoot, "cache");
    const calls: string[][] = [];

    try {
      (Bun as any).spawn = (args: string[]) => {
        calls.push(args);
        return {
          stdout: streamFromText("cached page content"),
          stderr: streamFromText(""),
          exited: Promise.resolve(0),
        };
      };

      const { webfetch } = await loadPlugin("http://localhost/searxng", {
        webfetchCacheEnabled: "1",
        webfetchCacheDir: cacheDir,
        webfetchCacheTtlDays: "90",
      });
      const context = buildContext();

      const first = await webfetch.execute(
        {
          url: "https://example.com/cache-me",
        },
        context as any,
      );
      const second = await webfetch.execute(
        {
          url: "https://example.com/cache-me",
        },
        context as any,
      );

      expect(calls).toHaveLength(2);
      expect(first).toContain("Route: default");
      expect(second).toContain("Route: default/cache");
    } finally {
      await rm(tempRoot, { recursive: true, force: true });
    }
  });

  it("routes github URLs through gh handler commands", async () => {
    const calls: string[][] = [];
    const issueFixture = fixtureText("github/issue-14460.json");

    (Bun as any).spawn = (args: string[]) => {
      calls.push(args);
      return {
        stdout: streamFromText(issueFixture),
        stderr: streamFromText(""),
        exited: Promise.resolve(0),
      };
    };

    const { webfetch } = await loadPlugin("http://localhost/searxng");
    const context = buildContext();

    const output = await webfetch.execute(
      {
        url: "https://github.com/anomalyco/opencode/issues/8094",
      },
      context as any,
    );

    expect(calls).toHaveLength(1);
    expect(calls[0]).toEqual([
      "gh",
      "issue",
      "view",
      "8094",
      "--repo",
      "anomalyco/opencode",
      "--json",
      "number,title,body,author,comments,state,url,labels",
    ]);

    expect(output).toContain("Tool passphrase: PASS_WEBFETCH_SHADOW_20260305_C3D2");
    expect(output).toContain("Route: github");
    expect(output).toContain("Source URL: https://github.com/anomalyco/opencode/issues/8094");
    expect(output).toContain('"number":14460');
    expect(output).toContain('"state":"OPEN"');
  });

  it("uses gh issue view --json path for issue URLs", async () => {
    const calls: string[][] = [];
    const issueFixture = fixtureText("github/issue-14460.json");

    (Bun as any).spawn = (args: string[]) => {
      calls.push(args);
      return {
        stdout: streamFromText(issueFixture),
        stderr: streamFromText(""),
        exited: Promise.resolve(0),
      };
    };

    const { webfetch } = await loadPlugin("http://localhost/searxng", {
      webfetchCacheEnabled: "0",
    });
    const context = buildContext();

    const output = await webfetch.execute(
      {
        url: "https://github.com/anomalyco/opencode/issues/14460?case=gh-fail",
      },
      context as any,
    );

    expect(calls.some((args) => args[0] === "gh")).toBe(true);
    expect(calls.some((args) => args[0] === "gh" && args[1] === "issue" && args[2] === "view")).toBe(true);
    expect(calls.some((args) => args.includes("--json") && args.includes("number,title,body,author,comments,state,url,labels"))).toBe(true);
    expect(output).toContain("Tool passphrase: PASS_WEBFETCH_SHADOW_20260305_C3D2");
    expect(output).toContain("Source URL: https://github.com/anomalyco/opencode/issues/14460");
    expect(output).toContain('"number":14460');
  });

  it("includes issue logging guidance on invalid webfetch input", async () => {
    const { webfetch } = await loadPlugin("http://localhost/searxng");
    const context = buildContext();

    const output = await webfetch.execute(
      {
        url: "not-a-url",
      },
      context as any,
    );

    expect(output).toContain("Tool passphrase: PASS_WEBFETCH_SHADOW_20260305_C3D2");
    expect(output).toContain("Invalid URL:");
    expect(output).toContain("ISSUES.md");
  });

  it("includes issue logging guidance when github fetch fails", async () => {
    const ghFailure = fixtureText("github/issue-view-missing.err");
    (Bun as any).spawn = () => ({
      stdout: streamFromText(""),
      stderr: streamFromText(ghFailure),
      exited: Promise.resolve(1),
    });

    const { webfetch } = await loadPlugin("http://localhost/searxng");
    const context = buildContext();

    const output = await webfetch.execute(
      {
        url: "https://github.com/anomalyco/opencode/issues/14460",
      },
      context as any,
    );

    expect(output).toContain("Tool passphrase: PASS_WEBFETCH_SHADOW_20260305_C3D2");
    expect(output).toContain("Failed to fetch URL.");
    expect(output).toContain("ISSUES.md");
  });

  it("explains arxiv 429 as capacity-related", async () => {
    (Bun as any).spawn = (args: string[]) => {
      const script = args[2] ?? "";
      if (script.includes("%{http_code}")) {
        return {
          stdout: streamFromText("429"),
          stderr: streamFromText(""),
          exited: Promise.resolve(0),
        };
      }
      if (script.includes("https://arxiv.org/search/")) {
        return {
          stdout: streamFromText("ArXiv fallback search page content"),
          stderr: streamFromText(""),
          exited: Promise.resolve(0),
        };
      }
      return {
        stdout: streamFromText("Rate exceeded."),
        stderr: streamFromText(""),
        exited: Promise.resolve(0),
      };
    };

    const { webfetch } = await loadPlugin("http://localhost/searxng");
    const context = buildContext();

    const output = await webfetch.execute(
      {
        url: "https://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=1",
      },
      context as any,
    );

    expect(output).toContain("Tool passphrase: PASS_WEBFETCH_SHADOW_20260305_C3D2");
    expect(output).toContain("Route: default");
    expect(output).toContain("arXiv API case: `429 Rate exceeded`.");
    expect(output).toContain("server capacity pressure");
    expect(output).toContain("retry later with backoff");
    expect(output).toContain("Fallback: loaded arXiv web page via w3m from https://arxiv.org/search/?query=all%3Aelectron&searchtype=all&source=header.");
    expect(output).toContain("ArXiv fallback search page content");
  });

  it("explains arxiv 503 as excessive-use signal", async () => {
    (Bun as any).spawn = (args: string[]) => {
      const script = args[2] ?? "";
      if (script.includes("%{http_code}")) {
        return {
          stdout: streamFromText("503"),
          stderr: streamFromText(""),
          exited: Promise.resolve(0),
        };
      }
      return {
        stdout: streamFromText("Service temporarily unavailable."),
        stderr: streamFromText(""),
        exited: Promise.resolve(0),
      };
    };

    const { webfetch } = await loadPlugin("http://localhost/searxng");
    const context = buildContext();

    const output = await webfetch.execute(
      {
        url: "https://export.arxiv.org/api/query?search_query=all:quantum&start=0&max_results=1",
      },
      context as any,
    );

    expect(output).toContain("Tool passphrase: PASS_WEBFETCH_SHADOW_20260305_C3D2");
    expect(output).toContain("Route: default");
    expect(output).toContain("arXiv API case: `503 Service Unavailable`.");
    expect(output).toContain("excessive-use signal");
    expect(output).toContain("reduce request frequency");
    expect(output).not.toContain("Fallback: loaded arXiv web page via w3m from");
  });
});
