import { afterEach, beforeEach, describe, expect, it } from "bun:test";

import {
  buildGitHubCommandPlan,
  fetchGitHubContent,
  fetchRedditPostMarkdown,
  fetchWikipediaMarkdown,
  fetchYoutubeTranscriptMarkdown,
} from "../../../webfetch-handlers/index.ts";

describe("webfetch handler modules", () => {
  const originalFetch = globalThis.fetch;
  const originalSpawn = Bun.spawn;

  beforeEach(() => {
    globalThis.fetch = originalFetch;
    (Bun as any).spawn = originalSpawn;
  });

  afterEach(() => {
    globalThis.fetch = originalFetch;
    (Bun as any).spawn = originalSpawn;
  });

  it("builds github issue plans and fetches via runner", async () => {
    const plan = buildGitHubCommandPlan(new URL("https://github.com/anomalyco/opencode/issues/8094"));
    expect(plan.args).toEqual(["gh", "issue", "view", "8094", "--repo", "anomalyco/opencode", "--comments"]);

    const output = await fetchGitHubContent({
      url: new URL("https://github.com/anomalyco/opencode/issues/8094"),
      runCommand: async () => ({ stdoutText: "issue body", stderrText: "", exitCode: 0 }),
    });

    expect(output.routeName).toBe("github");
    expect(output.sourceUrl).toBe("https://github.com/anomalyco/opencode/issues/8094");
    expect(output.content).toBe("issue body");
  });

  it("uses reddit fallback path when URL is not a post permalink", async () => {
    const output = await fetchRedditPostMarkdown({
      url: new URL("https://www.reddit.com/r/test"),
      apifyActor: "mock/actor",
      runCommand: async () => ({ stdoutText: "", stderrText: "", exitCode: 0 }),
      fetchFallbackWithW3M: async () => ({ stdoutText: "fallback text", stderrText: "", exitCode: 0 }),
    });

    expect(output.routeName).toBe("reddit");
    expect(output.sourceUrl).toBe("https://www.reddit.com/r/test");
    expect(output.content).toBe("fallback text");
  });

  it("extracts youtube captions in handler module", async () => {
    const calls: string[][] = [];

    const output = await fetchYoutubeTranscriptMarkdown({
      url: new URL("https://youtu.be/abc123"),
      runCommand: async (args) => {
        calls.push(args);

        if (args.includes("--list-subs")) {
          return { stdoutText: "en vtt", stderrText: "", exitCode: 0 };
        }

        if (args.includes("--write-subs")) {
          const outputIndex = args.indexOf("-o");
          const template = outputIndex >= 0 ? args[outputIndex + 1] : undefined;
          if (template) {
            const slash = template.lastIndexOf("/");
            const dir = slash >= 0 ? template.slice(0, slash) : ".";
            await Bun.$`mkdir -p ${dir}`.quiet();
            await Bun.write(
              `${dir}/mock.en.vtt`,
              "WEBVTT\n\n00:00:00.000 --> 00:00:02.000\nHello from captions\n",
            );
          }
          return { stdoutText: "", stderrText: "", exitCode: 0 };
        }

        return { stdoutText: "", stderrText: "unexpected", exitCode: 1 };
      },
    });

    expect(calls.some((args) => args.includes("--list-subs"))).toBe(true);
    expect(calls.some((args) => args.includes("--write-subs"))).toBe(true);
    expect(output.routeName).toBe("youtube");
    expect(output.content).toContain("Hello from captions");
  });

  it("fetches wikipedia parse API then converts through external script runner", async () => {
    const fetchCalls: Array<{ url: string; userAgent?: string }> = [];
    (globalThis as any).fetch = async (input: string | Request | URL, init?: RequestInit) => {
      fetchCalls.push({
        url: String(input),
        userAgent:
          (init?.headers as Record<string, string> | undefined)?.["User-Agent"] ??
          (init?.headers as Record<string, string> | undefined)?.["user-agent"],
      });
      return new Response(
        JSON.stringify({
          parse: {
            title: "Fourier transform",
            displaytitle: "<span class='mw-page-title-main'>Fourier transform</span>",
            text: "<p>Math page body</p>",
          },
        }),
        { status: 200, headers: { "content-type": "application/json" } },
      );
    };

    const runCalls: string[][] = [];
    const output = await fetchWikipediaMarkdown({
      url: new URL("https://en.wikipedia.org/wiki/Fourier_transform"),
      userAgent: "test-agent",
      converterScriptPath: "/tmp/mock_converter.py",
      convertTimeoutMs: 120000,
      runCommand: async (args) => {
        runCalls.push(args);
        return {
          stdoutText: "https://en.wikipedia.org/wiki/Fourier_transform\n\n# Fourier transform\n\nMath page body",
          stderrText: "",
          exitCode: 0,
        };
      },
    });

    expect(fetchCalls).toHaveLength(1);
    expect(fetchCalls[0]?.url).toContain("/w/api.php?action=parse");
    expect(fetchCalls[0]?.userAgent).toBe("test-agent");
    expect(runCalls).toHaveLength(1);
    expect(runCalls[0]?.[0]).toBe("uvx");
    expect(runCalls[0]).toContain("python");
    expect(runCalls[0]).toContain("/tmp/mock_converter.py");
    expect(output.routeName).toBe("wikipedia");
    expect(output.sourceUrl).toBe("https://en.wikipedia.org/wiki/Fourier_transform");
  });
});
