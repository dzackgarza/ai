import { afterEach, beforeEach, describe, expect, it } from "bun:test";
import { mkdtemp, rm } from "node:fs/promises";
import { join } from "node:path";

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
    const responses = new Map<string, any>();

    const q1 = "!news openai (site:example.com)";
    const q2 = "!science arxiv lattice";

    responses.set(`${q1}|1`, {
      query: q1,
      number_of_results: 10,
      results: [
        {
          title: "Q1-R1",
          url: "https://example.com/q1-r1",
          content: "first result",
          engine: "duckduckgo",
          category: "news",
          publishedDate: null,
        },
        {
          title: "Q1-R2",
          url: "https://example.com/q1-r2",
          content: "second result",
          engine: "duckduckgo",
          category: "news",
          publishedDate: "2026-03-06",
        },
      ],
      answers: [],
      suggestions: [],
      unresponsive_engines: [],
    });

    responses.set(`${q1}|2`, {
      query: q1,
      number_of_results: 10,
      results: [
        {
          title: "Q1-R3",
          url: "https://example.com/q1-r3",
          content: "third result",
          engine: "duckduckgo",
          category: "news",
          publishedDate: null,
        },
      ],
      answers: [],
      suggestions: [],
      unresponsive_engines: [],
    });

    responses.set(`${q2}|1`, {
      query: q2,
      number_of_results: 3,
      results: [
        {
          title: "Q2-R1",
          url: "https://example.org/q2-r1",
          content: "science result",
          engine: "duckduckgo",
          category: "science",
          publishedDate: null,
        },
      ],
      answers: [],
      suggestions: [],
      unresponsive_engines: [],
    });

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
            category: "news",
            domains: ["example.com"],
            num_results: 2,
            offset: 1,
          },
          {
            q: "arxiv lattice",
            category: "science",
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
    expect(output).toContain("Showing results: 2-3 of 10");
    expect(output).toContain("https://example.com/q1-r2");
    expect(output).toContain("https://example.com/q1-r3");
    expect(output).toContain("Query 2:");
    expect(output).toContain("https://example.org/q2-r1");
    expect(output).toContain("\n\n---\n\n");
  });

  it("writes oversized webfetch content to /tmp and reports saved path", async () => {
    const largeText = Array.from({ length: 25_000 }, () => "token").join(" ");
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
    expect(oversizedWrite!.content).toContain(largeText);

    expect(output).toContain("Tool passphrase: PASS_WEBFETCH_SHADOW_20260305_C3D2");
    expect(output).toContain("Route: default");
    expect(output).toContain("Full report exceeds inline limit (20000 tokens).");
    expect(output).toContain(`Saved full content: ${oversizedWrite!.path}`);
    expect(output).toContain("Token count:");
  });

  it("routes reddit posts through apify and renders nested markdown comments", async () => {
    const apifyDataset = [
      {
        record_type: "post",
        post_id: "abc123",
        permalink: "/r/test/comments/abc123/sample_post/",
        title: "Sample Post Title",
        text: "Sample post body.",
        author: "op_author",
        subreddit: "test",
        score: 42,
        num_comments: 3,
      },
      {
        record_type: "comment",
        post_id: "abc123",
        comment_id: "c1",
        parent_id: "t3_abc123",
        author: "top_level",
        score: 10,
        text: "Top level comment",
      },
      {
        record_type: "comment",
        post_id: "abc123",
        comment_id: "c2",
        parent_id: "t1_c1",
        author: "nested_user",
        score: 7,
        text: "Nested reply",
      },
      {
        record_type: "comment",
        post_id: "abc123",
        comment_id: "c3",
        parent_id: "t3_abc123",
        author: "second_top",
        score: 5,
        text: "Second top-level comment",
      },
    ];

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
        url: "https://www.reddit.com/r/test/comments/abc123/sample_post/",
      },
      context as any,
    );

    expect(output).toContain("Tool passphrase: PASS_WEBFETCH_SHADOW_20260305_C3D2");
    expect(output).toContain("Route: reddit");
    expect(output).toContain("Source URL: /r/test/comments/abc123/sample_post/");
    expect(output).toContain("# Reddit Post");
    expect(output).toContain("## Comments (nested)");
    expect(output).toContain("- u/top_level (score 10):");
    expect(output).toContain("Top level comment");
    expect(output).toContain("  - u/nested_user (score 7):");
    expect(output).toContain("Nested reply");
    expect(output).toContain("- u/second_top (score 5):");
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

    (Bun as any).spawn = (args: string[]) => {
      calls.push(args);
      return {
        stdout: streamFromText("github issue content"),
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
      "--comments",
    ]);

    expect(output).toContain("Tool passphrase: PASS_WEBFETCH_SHADOW_20260305_C3D2");
    expect(output).toContain("Route: github");
    expect(output).toContain("Source URL: https://github.com/anomalyco/opencode/issues/8094");
    expect(output).toContain("github issue content");
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
