import { afterEach, beforeEach, describe, expect, it } from "bun:test";

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

async function loadPlugin(instanceUrl: string) {
  process.env.SEARXNG_INSTANCE_URL = instanceUrl;
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

  beforeEach(() => {
    globalThis.fetch = originalFetch;
    (Bun as any).spawn = originalSpawn;
    (Bun as any).write = originalWrite;
  });

  afterEach(() => {
    globalThis.fetch = originalFetch;
    (Bun as any).spawn = originalSpawn;
    (Bun as any).write = originalWrite;
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

    globalThis.fetch = async (input) => {
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

    expect(writes).toHaveLength(1);
    expect(writes[0]!.path.startsWith("/tmp/webfetch-")).toBe(true);
    expect(writes[0]!.content).toBe(largeText);

    expect(output).toContain("Tool passphrase: PASS_WEBFETCH_SHADOW_20260305_C3D2");
    expect(output).toContain("Content exceeds inline limit (20000 tokens).");
    expect(output).toContain(`Saved full content: ${writes[0]!.path}`);
    expect(output).toContain("Token count:");
  });
});
