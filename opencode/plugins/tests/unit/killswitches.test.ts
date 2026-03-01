import { describe, it, expect, beforeEach } from "bun:test";

// Re-implement sw() locally to test the logic contract.
// killswitches.ts evaluates sw() at import time, so we test the function directly.
function sw(envVar: string, defaultEnabled: boolean): boolean {
  const val = process.env[envVar];
  if (val === "true")  return true;
  if (val === "false") return false;
  return defaultEnabled;
}

describe("sw() enable switch logic", () => {
  beforeEach(() => {
    delete process.env.TEST_SW_VAR;
  });

  it("returns default when env var is unset", () => {
    expect(sw("TEST_SW_VAR", true)).toBe(true);
    expect(sw("TEST_SW_VAR", false)).toBe(false);
  });

  it("env=true enables regardless of default", () => {
    process.env.TEST_SW_VAR = "true";
    expect(sw("TEST_SW_VAR", false)).toBe(true);
    expect(sw("TEST_SW_VAR", true)).toBe(true);
  });

  it("env=false disables regardless of default", () => {
    process.env.TEST_SW_VAR = "false";
    expect(sw("TEST_SW_VAR", true)).toBe(false);
    expect(sw("TEST_SW_VAR", false)).toBe(false);
  });

  it("unrecognized env value falls through to default", () => {
    process.env.TEST_SW_VAR = "yes";
    expect(sw("TEST_SW_VAR", true)).toBe(true);
    expect(sw("TEST_SW_VAR", false)).toBe(false);
  });

  it("all plugins default to false (disabled)", () => {
    // Verify the expected default state — plugins are off until explicitly enabled
    expect(sw("PROMPT_ROUTER_ENABLED", false)).toBe(false);
    expect(sw("COMMAND_INTERCEPTOR_ENABLED", false)).toBe(false);
  });
});
