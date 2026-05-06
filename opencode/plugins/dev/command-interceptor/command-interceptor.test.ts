import { describe, it, expect } from "bun:test";

// Mirror the trigger rules from command-interceptor.ts
const TRIGGER_RULES: Record<string, { intent: string; passphrase: string }> = {
  "intercept test": { intent: "verification",   passphrase: "SWORDFISH" },
  "plugin check":   { intent: "diagnostics",    passphrase: "NIGHTHAWK" },
  "context inject": { intent: "context-inject", passphrase: "IRONCLAD"  },
};

function matchTrigger(text: string) {
  const lower = text.toLowerCase();
  for (const [keyphrase, rule] of Object.entries(TRIGGER_RULES)) {
    if (lower.includes(keyphrase)) return rule;
  }
  return null;
}

describe("CommandInterceptor trigger matching", () => {
  it("matches exact keyphrase", () => {
    expect(matchTrigger("intercept test")).toEqual({ intent: "verification", passphrase: "SWORDFISH" });
  });

  it("matches keyphrase case-insensitively", () => {
    expect(matchTrigger("INTERCEPT TEST")).not.toBeNull();
    expect(matchTrigger("INTERCEPT TEST")?.passphrase).toBe("SWORDFISH");
    expect(matchTrigger("Intercept Test")).not.toBeNull();
  });

  it("matches keyphrase embedded in longer text", () => {
    expect(matchTrigger("please run plugin check now")).not.toBeNull();
    expect(matchTrigger("please run plugin check now")?.intent).toBe("diagnostics");
  });

  it("returns null for non-matching text", () => {
    expect(matchTrigger("hello world")).toBeNull();
    expect(matchTrigger("")).toBeNull();
    expect(matchTrigger("interception testing")).toBeNull(); // not a substring match
  });

  it("matches context inject keyphrase", () => {
    expect(matchTrigger("context inject please")).not.toBeNull();
  });
});
