import { describe, it, expect } from "bun:test";

// Mirror faux rules from the prompt-router example.
type Tier = "model-self" | "knowledge" | "C" | "B" | "A" | "S";

const FAUX_RULES: Array<{ prompt: string; tier: Tier }> = [
  { prompt: "Describe every tool you have access to.",                           tier: "model-self" },
  { prompt: "What is the latest stable release of TypeScript?",                  tier: "knowledge"  },
  { prompt: "Create a file named router-poc-c.txt containing exactly: poc-baseline-c, then delete it.", tier: "C" },
  { prompt: "For each .ts file in this directory, open it and print the name of every exported symbol.", tier: "B" },
  { prompt: "Audit command-interceptor.ts for security vulnerabilities.",        tier: "A"          },
  { prompt: "Design a plugin for tracking token usage per session.",             tier: "S"          },
];

function fauxMatch(text: string): Tier | null {
  const trimmed = text.trim();
  for (const { prompt, tier } of FAUX_RULES) {
    if (trimmed === prompt) return tier;
  }
  return null;
}

describe("prompt-router faux rules", () => {
  it("matches each canonical prompt exactly", () => {
    for (const { prompt, tier } of FAUX_RULES) {
      expect(fauxMatch(prompt)).toBe(tier);
    }
  });

  it("trims whitespace before matching", () => {
    expect(fauxMatch("  Describe every tool you have access to.  ")).toBe("model-self");
  });

  it("returns null for partial matches", () => {
    expect(fauxMatch("Describe every tool")).toBeNull();
    expect(fauxMatch("Design a plugin")).toBeNull();
  });

  it("returns null for unrecognized prompts", () => {
    expect(fauxMatch("Hello, how are you?")).toBeNull();
    expect(fauxMatch("")).toBeNull();
  });

  it("is case-sensitive (exact match required)", () => {
    expect(fauxMatch("describe every tool you have access to.")).toBeNull();
  });
});
