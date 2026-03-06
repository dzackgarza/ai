import type { CommandExecutionResult, RunCommand, WebFetchHandlerResult } from "../types.ts";

export const REDDIT_DOMAINS = ["reddit.com", "www.reddit.com", "old.reddit.com", "api.reddit.com"] as const;

type RedditPostRef = {
  subreddit: string;
  postId: string;
  slug?: string;
};

type RedditRecord = Record<string, unknown>;

function extractRedditPostRef(url: URL): RedditPostRef | undefined {
  const segments = url.pathname.split("/").filter(Boolean);
  if (segments.length < 4) return undefined;
  if (segments[0] !== "r") return undefined;
  if (segments[2] !== "comments") return undefined;
  return {
    subreddit: segments[1]!,
    postId: segments[3]!,
    slug: segments[4],
  };
}

function normalizeRedditId(raw: unknown): string {
  const value = String(raw ?? "").trim();
  if (!value) return "";
  const normalized = value.includes("_") ? value.split("_").slice(1).join("_") : value;
  return normalized.toLowerCase();
}

function redditText(raw: unknown): string {
  return String(raw ?? "").replace(/\r\n?/g, "\n").trim();
}

function renderRedditCommentTree(comments: RedditRecord[], postId: string): string[] {
  const byId = new Map<string, RedditRecord>();
  for (const comment of comments) {
    const id = normalizeRedditId(comment.comment_id);
    if (!id) continue;
    byId.set(id, comment);
  }

  const children = new Map<string, RedditRecord[]>();
  const root = postId.toLowerCase();

  for (const comment of comments) {
    const commentId = normalizeRedditId(comment.comment_id);
    if (!commentId) continue;
    const parentRaw = String(comment.parent_id ?? "").trim();
    const parentNormalized = normalizeRedditId(parentRaw);

    let parentKey = root;
    if (parentRaw.startsWith("t1_")) {
      parentKey = parentNormalized || root;
    } else if (parentRaw.startsWith("t3_")) {
      parentKey = root;
    } else if (parentNormalized && byId.has(parentNormalized)) {
      parentKey = parentNormalized;
    }

    const arr = children.get(parentKey) ?? [];
    arr.push(comment);
    children.set(parentKey, arr);
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

export async function fetchRedditPostMarkdown(input: {
  url: URL;
  runCommand: RunCommand;
  fetchFallbackWithW3M: (url: URL) => Promise<CommandExecutionResult>;
  apifyActor: string;
}): Promise<WebFetchHandlerResult> {
  const postRef = extractRedditPostRef(input.url);
  if (!postRef) {
    const fallback = await input.fetchFallbackWithW3M(input.url);
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
    const result = await input.runCommand([
      "apify",
      "call",
      input.apifyActor,
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
      throw new Error(`apify output parse failed: ${error instanceof Error ? error.message : String(error)}`);
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
    await Bun.$`rm -f ${inputPath}`.quiet();
  }
}
