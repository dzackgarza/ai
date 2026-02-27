// Custom tool: plan_exit - signals completion of planning phase with verification checklist
import { type Plugin, tool } from "@opencode-ai/plugin";

const VERIFICATION_CHECKLIST = `# Plan Exit Verification

Before exiting plan mode, verify:

## 1. Requirements Review
- Have you re-read the user's original request?
- Did you clarify ALL ambiguities with the user instead of assuming?
- Did you ask the 3-5 clarifying questions in Phase 1?

## 2. Documentation Review
- Does USER_SPEC.md exist and capture EVERY detail from the user?
- Did you review the spec to ensure nothing was missed?
- Are all edge cases and variations documented?

## 3. Subagent Review
- Did you spawn plan-reviewer to audit the plan?
- Did you have Test Guidelines review the test strategy?
- Did you iterate and address all feedback from reviewers?

## 4. Plan Quality
- Is the plan decomposed into micro-tasks (one file + test per task)?
- Does each task have a verification step with expected results?
- Are all dependencies and prerequisites clear?

## 5. Readiness Check
If ALL of the above are true, present this to the user:

---
**Plan is ready for build phase.**

To proceed:
1. Clear context (close any open file reads, memory reads)
2. Switch to build mode: use \`serena_switch_modes(["editing", "interactive"])\` or ask the user to do so
---

If ANY of the above are NOT complete, address them now before exiting.
`;

export const PlanExitPlugin: Plugin = async () => {
  return {
    tool: {
      plan_exit: tool({
        description:
          "Signals completion of planning phase. Returns a verification checklist to ensure plan quality before exiting.",
        args: {},
        async execute() {
          return VERIFICATION_CHECKLIST;
        },
      }),
    },
  };
};
