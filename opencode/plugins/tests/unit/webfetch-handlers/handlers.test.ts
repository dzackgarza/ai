import { afterEach, beforeEach, describe, expect, it } from "bun:test";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";

import {
  buildGitHubCommandPlan,
  fetchGitHubContent,
  fetchRedditPostMarkdown,
  fetchWikipediaMarkdown,
  fetchYoutubeTranscriptMarkdown,
} from "@webfetch-handlers";

function fixtureText(relativePath: string): string {
  const path = new URL(`../../fixtures/real/${relativePath}`, import.meta.url);
  return readFileSync(path, "utf8");
}

function fixtureJson<T>(relativePath: string): T {
  return JSON.parse(fixtureText(relativePath)) as T;
}

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

  it("builds github issue plans and fetches via runner with real gh fixture output", async () => {
    const issueFixture = fixtureText("github/issue-14460.json");
    const plan = buildGitHubCommandPlan(new URL("https://github.com/anomalyco/opencode/issues/8094"));
    expect(plan.args).toEqual([
      "gh",
      "issue",
      "view",
      "8094",
      "--repo",
      "anomalyco/opencode",
      "--json",
      "number,title,body,author,comments,state,url,labels",
    ]);

    const output = await fetchGitHubContent({
      url: new URL("https://github.com/anomalyco/opencode/issues/8094"),
      runCommand: async () => ({ stdoutText: issueFixture, stderrText: "", exitCode: 0 }),
    });

    expect(output.routeName).toBe("github");
    expect(output.sourceUrl).toBe("https://github.com/anomalyco/opencode/issues/8094");
    const parsed = JSON.parse(output.content) as Record<string, unknown>;
    expect(parsed.number).toBe(14460);
    expect(parsed.state).toBe("OPEN");
    expect(typeof parsed.title).toBe("string");
    expect(Array.isArray(parsed.comments)).toBe(true);
  });

  it("builds github command plans across all supported URL scopes", () => {
    const cases: Array<{
      url: string;
      args: string[];
      sourceUrl: string;
    }> = [
      {
        url: "https://github.com/anomalyco/opencode/pull/144",
        args: ["gh", "pr", "view", "144", "--repo", "anomalyco/opencode", "--comments"],
        sourceUrl: "https://github.com/anomalyco/opencode/pull/144",
      },
      {
        url: "https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/index.ts",
        args: [
          "gh",
          "api",
          "repos/anomalyco/opencode/contents/packages/opencode/src/index.ts",
          "-f",
          "ref=main",
          "-H",
          "Accept: application/vnd.github.raw+json",
        ],
        sourceUrl: "https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/index.ts",
      },
      {
        url: "https://github.com/anomalyco/opencode/commit/27c8fa5",
        args: ["gh", "api", "repos/anomalyco/opencode/commits/27c8fa5"],
        sourceUrl: "https://github.com/anomalyco/opencode/commit/27c8fa5",
      },
      {
        url: "https://github.com/anomalyco/opencode/releases",
        args: ["gh", "release", "list", "--repo", "anomalyco/opencode", "--limit", "20"],
        sourceUrl: "https://github.com/anomalyco/opencode/releases",
      },
      {
        url: "https://github.com/anomalyco/opencode/issues",
        args: ["gh", "issue", "list", "--repo", "anomalyco/opencode", "--limit", "30"],
        sourceUrl: "https://github.com/anomalyco/opencode/issues",
      },
      {
        url: "https://github.com/anomalyco/opencode/pulls",
        args: ["gh", "pr", "list", "--repo", "anomalyco/opencode", "--limit", "30"],
        sourceUrl: "https://github.com/anomalyco/opencode/pulls",
      },
      {
        url: "https://github.com/anomalyco/opencode",
        args: ["gh", "repo", "view", "anomalyco/opencode", "--readme"],
        sourceUrl: "https://github.com/anomalyco/opencode",
      },
      {
        url: "https://github.com/anomalyco",
        args: ["gh", "search", "repos", "anomalyco", "--limit", "20"],
        sourceUrl: "https://github.com/anomalyco",
      },
    ];

    for (const testCase of cases) {
      const plan = buildGitHubCommandPlan(new URL(testCase.url));
      expect(plan).toEqual({
        args: testCase.args,
        sourceUrl: testCase.sourceUrl,
      });
    }
  });

  it("renders reddit post/comment markdown from real apify dataset fixture", async () => {
    const fixture = fixtureJson<Array<Record<string, unknown>>>("reddit/apify-search-openai.json");
    const fixtureRaw = JSON.stringify(fixture);

    expect(Array.isArray(fixture)).toBe(true);
    expect(fixture[0]?.record_type).toBe("post");
    expect(typeof fixture[0]?.permalink).toBe("string");
    expect(fixture.some((item) => item.record_type === "comment")).toBe(true);

    const output = await fetchRedditPostMarkdown({
      url: new URL("https://www.reddit.com/r/OpenAI/comments/1hn44qh/anyone_else_excited_for_o3_mini_release/"),
      apifyActor: "mock/actor",
      runCommand: async () => ({ stdoutText: fixtureRaw, stderrText: "", exitCode: 0 }),
      fetchFallbackWithW3M: async () => ({ stdoutText: "unexpected fallback", stderrText: "", exitCode: 0 }),
    });

    expect(output.routeName).toBe("reddit");
    expect(output.sourceUrl).toBe("https://www.reddit.com/r/OpenAI/comments/1hn44qh/anyone_else_excited_for_o3_mini_release/");
    expect(output.content).toContain("# Reddit Post");
    expect(output.content).toContain("Anyone Else Excited for o3 Mini Release?");
    expect(output.content).toContain("## Comments (nested)");
    expect(output.content).toContain("- u/The_GSingh (score 20):");
    expect(output.content).toContain("  - u/Thinklikeachef (score 13):");
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

  it("extracts youtube captions from real yt-dlp subtitle fixture", async () => {
    const calls: string[][] = [];
    const listSubs = fixtureText("youtube/dQw4w9WgXcQ.list-subs.txt");
    const vtt = fixtureText("youtube/dQw4w9WgXcQ.en.vtt");

    const output = await fetchYoutubeTranscriptMarkdown({
      url: new URL("https://youtu.be/dQw4w9WgXcQ"),
      runCommand: async (args) => {
        calls.push(args);

        if (args.includes("--list-subs")) {
          return { stdoutText: listSubs, stderrText: "", exitCode: 0 };
        }

        if (args.includes("--write-subs")) {
          const outputIndex = args.indexOf("-o");
          const template = outputIndex >= 0 ? args[outputIndex + 1] : undefined;
          if (template) {
            const slash = template.lastIndexOf("/");
            const dir = slash >= 0 ? template.slice(0, slash) : ".";
            await Bun.$`mkdir -p ${dir}`.quiet();
            await Bun.write(`${dir}/dQw4w9WgXcQ.en.vtt`, vtt);
          }
          return { stdoutText: fixtureText("youtube/dQw4w9WgXcQ.write-subs.out"), stderrText: "", exitCode: 0 };
        }

        return { stdoutText: "", stderrText: "unexpected", exitCode: 1 };
      },
    });

    expect(calls.some((args) => args.includes("--list-subs"))).toBe(true);
    expect(calls.some((args) => args.includes("--write-subs"))).toBe(true);
    expect(output.routeName).toBe("youtube");
    expect(output.content).toContain("We're no strangers to");
  });

  it("falls back to whisper transcript path using real whisper fixture text", async () => {
    const calls: string[][] = [];
    const listSubs = fixtureText("youtube/dQw4w9WgXcQ.list-subs.txt");
    const whisperText = fixtureText("youtube/dQw4w9WgXcQ.whisper.txt");

    const output = await fetchYoutubeTranscriptMarkdown({
      url: new URL("https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
      runCommand: async (args) => {
        calls.push(args);

        if (args.includes("--list-subs")) {
          return { stdoutText: listSubs, stderrText: "", exitCode: 0 };
        }

        if (args.includes("--write-subs")) {
          // Simulate no subtitle artifact written, forcing audio+whisper path.
          return { stdoutText: fixtureText("youtube/dQw4w9WgXcQ.write-subs.out"), stderrText: "", exitCode: 0 };
        }

        if (args.includes("-x") && args.includes("--audio-format")) {
          const outputIndex = args.indexOf("-o");
          const template = outputIndex >= 0 ? args[outputIndex + 1] : undefined;
          if (template) {
            const audioPath = template.replace("%(id)s.%(ext)s", "dQw4w9WgXcQ.mp3");
            mkdirSync(dirname(audioPath), { recursive: true });
            writeFileSync(audioPath, "mp3 fixture bytes");
          }
          return {
            stdoutText: fixtureText("youtube/dQw4w9WgXcQ.download-audio.out"),
            stderrText: fixtureText("youtube/dQw4w9WgXcQ.download-audio.err"),
            exitCode: 0,
          };
        }

        if (args[0] === "uvx" && args.includes("whisper")) {
          const outputDirIndex = args.indexOf("--output_dir");
          const outputDir = outputDirIndex >= 0 ? args[outputDirIndex + 1] : undefined;
          if (outputDir) {
            mkdirSync(outputDir, { recursive: true });
            writeFileSync(join(outputDir, "dQw4w9WgXcQ.txt"), whisperText);
          }
          return {
            stdoutText: fixtureText("youtube/dQw4w9WgXcQ.whisper.out"),
            stderrText: fixtureText("youtube/dQw4w9WgXcQ.whisper.err"),
            exitCode: 0,
          };
        }

        return { stdoutText: "", stderrText: "unexpected", exitCode: 1 };
      },
    });

    expect(calls.some((args) => args.includes("--list-subs"))).toBe(true);
    expect(calls.some((args) => args.includes("--write-subs"))).toBe(true);
    expect(calls.some((args) => args.includes("-x") && args.includes("--audio-format"))).toBe(true);
    expect(calls.some((args) => args[0] === "uvx" && args.includes("whisper"))).toBe(true);
    expect(output.routeName).toBe("youtube");
    expect(output.content).toContain("Source: Whisper transcription (English)");
    expect(output.content).toContain("Never gonna let you down");
  });

  it("fetches wikipedia parse API then converts through external script runner using real parse fixture", async () => {
    const parseFixture = fixtureJson<Record<string, unknown>>("wikipedia/parse-fourier-transform.json");
    const converted = fixtureText("wikipedia/fourier-transform.converted.md");

    const fetchCalls: Array<{ url: string; userAgent?: string }> = [];
    (globalThis as any).fetch = async (input: string | Request | URL, init?: RequestInit) => {
      fetchCalls.push({
        url: String(input),
        userAgent:
          (init?.headers as Record<string, string> | undefined)?.["User-Agent"] ??
          (init?.headers as Record<string, string> | undefined)?.["user-agent"],
      });
      return new Response(JSON.stringify(parseFixture), {
        status: 200,
        headers: { "content-type": "application/json" },
      });
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
          stdoutText: converted,
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
    expect(output.content).toContain("# Fourier transform");
    expect(output.content).toContain("In [mathematics](https://en.wikipedia.org/wiki/Mathematics");
  });

  it("supports wikipedia index.php title URLs and normalizes source URL", async () => {
    const parseFixture = fixtureJson<Record<string, unknown>>("wikipedia/parse-wave-equation.json");
    const converted = fixtureText("wikipedia/wave-equation.converted.md");
    (globalThis as any).fetch = async () =>
      new Response(JSON.stringify(parseFixture), { status: 200, headers: { "content-type": "application/json" } });

    const output = await fetchWikipediaMarkdown({
      url: new URL("https://en.wikipedia.org/w/index.php?title=Wave_equation"),
      userAgent: "test-agent",
      converterScriptPath: "/tmp/mock_converter.py",
      convertTimeoutMs: 120000,
      runCommand: async () => ({
        stdoutText: converted,
        stderrText: "",
        exitCode: 0,
      }),
    });

    expect(output.routeName).toBe("wikipedia");
    expect(output.sourceUrl).toBe("https://en.wikipedia.org/wiki/Wave_equation");
    expect(output.content).toContain("# Wave equation");
    expect(output.content).toContain("The **wave equation** is a second-order linear");
  });

  it("returns subtitle-discovery failure report with real bot-check stderr fixture", async () => {
    const botCheckError = fixtureText("youtube/8S0FDjFBj8o.list-subs.err");
    const output = await fetchYoutubeTranscriptMarkdown({
      url: new URL("https://www.youtube.com/watch?v=8S0FDjFBj8o"),
      runCommand: async (args) => {
        if (args.includes("--list-subs")) {
          return { stdoutText: fixtureText("youtube/8S0FDjFBj8o.list-subs.out"), stderrText: botCheckError, exitCode: 1 };
        }
        return { stdoutText: "", stderrText: "", exitCode: 0 };
      },
    });

    expect(output.routeName).toBe("youtube");
    expect(output.content).toContain("Transcript extraction failed at subtitle discovery.");
    expect(output.content).toContain("Sign in to confirm you’re not a bot");
  });

  it("returns audio-stage failure report using real yt-dlp stderr fixture text", async () => {
    const listSubs = fixtureText("youtube/dQw4w9WgXcQ.list-subs.txt");
    const audioErr = fixtureText("youtube/dQw4w9WgXcQ.download-audio.err");
    const output = await fetchYoutubeTranscriptMarkdown({
      url: new URL("https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
      runCommand: async (args) => {
        if (args.includes("--list-subs")) {
          return { stdoutText: listSubs, stderrText: "", exitCode: 0 };
        }
        if (args.includes("--write-subs")) {
          return { stdoutText: "", stderrText: "", exitCode: 0 };
        }
        if (args.includes("-x") && args.includes("--audio-format")) {
          return { stdoutText: "", stderrText: audioErr, exitCode: 1 };
        }
        return { stdoutText: "", stderrText: "", exitCode: 0 };
      },
    });

    expect(output.routeName).toBe("youtube");
    expect(output.content).toContain("Transcript extraction failed at audio download stage.");
    expect(output.content).toContain("Reason:");
  });

  it("throws for unsupported wikipedia URL shapes", async () => {
    await expect(
      fetchWikipediaMarkdown({
        url: new URL("https://en.wikipedia.org/"),
        userAgent: "test-agent",
        converterScriptPath: "/tmp/mock_converter.py",
        convertTimeoutMs: 120000,
        runCommand: async () => ({ stdoutText: "", stderrText: "", exitCode: 0 }),
      }),
    ).rejects.toThrow(Error);
  });

  it("throws for wikipedia parse API error payloads from real API fixture", async () => {
    const missingPage = fixtureJson<Record<string, unknown>>("wikipedia/parse-missing-page.json");
    (globalThis as any).fetch = async () =>
      new Response(JSON.stringify(missingPage), { status: 200, headers: { "content-type": "application/json" } });

    await expect(
      fetchWikipediaMarkdown({
        url: new URL("https://en.wikipedia.org/wiki/Does_Not_Exist"),
        userAgent: "test-agent",
        converterScriptPath: "/tmp/mock_converter.py",
        convertTimeoutMs: 120000,
        runCommand: async () => ({ stdoutText: "", stderrText: "", exitCode: 0 }),
      }),
    ).rejects.toThrow(Error);
  });

});
