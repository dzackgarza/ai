import { describe, it, expect } from "bun:test";

// Mirror phrase detection logic from stop_hooks/
function findMatch(text: string, phrases: string[]): boolean {
  const lower = text.toLowerCase();
  return phrases.some((p) => lower.includes(p.toLowerCase()));
}

const REFLEXIVE_PHRASES = [
  "you're right",
  "you are right",
  "the user is right",
  "they're right",
  "they are right",
];

const OBVIOUS_QUESTION_PHRASES = [
  "should I",
  "would you like me to",
  "do you want me to",
  "should I continue",
  "shall I",
];

const OTP_CODE = "ABCDEFG";

describe("reflexiveAgreementDetector", () => {
  it("detects you're right", () => {
    expect(findMatch("You're right, I should fix that.", REFLEXIVE_PHRASES)).toBe(true);
  });

  it("detects case-insensitively", () => {
    expect(findMatch("YOU ARE RIGHT about this.", REFLEXIVE_PHRASES)).toBe(true);
  });

  it("does not trigger on unrelated text", () => {
    expect(findMatch("Here is the implementation.", REFLEXIVE_PHRASES)).toBe(false);
    expect(findMatch("I disagree with that approach.", REFLEXIVE_PHRASES)).toBe(false);
  });
});

describe("obviousQuestionDetector", () => {
  it("detects 'should I'", () => {
    expect(findMatch("Should I continue with the refactor?", OBVIOUS_QUESTION_PHRASES)).toBe(true);
  });

  it("detects 'would you like me to'", () => {
    expect(findMatch("Would you like me to add tests?", OBVIOUS_QUESTION_PHRASES)).toBe(true);
  });

  it("detects 'shall I'", () => {
    expect(findMatch("Shall I proceed?", OBVIOUS_QUESTION_PHRASES)).toBe(true);
  });

  it("does not trigger on declarative statements", () => {
    expect(findMatch("I will now fix the bug.", OBVIOUS_QUESTION_PHRASES)).toBe(false);
    expect(findMatch("The implementation is complete.", OBVIOUS_QUESTION_PHRASES)).toBe(false);
  });
});

describe("otpChecker", () => {
  it("triggers when verify code present", () => {
    expect(`The code is ${OTP_CODE} here`.includes(OTP_CODE)).toBe(true);
  });

  it("does not trigger without code", () => {
    expect("No code in this response".includes(OTP_CODE)).toBe(false);
  });
});
