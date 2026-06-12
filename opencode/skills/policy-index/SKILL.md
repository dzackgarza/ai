---
name: policy-index
description: Use before code review, slop review, PR feedback triage, testing, QC changes, or remediation when deciding which global policy skill owns the rule. Central source-of-truth index for bridge-burning policies, red-flag catalogs, proof/test rules, QC authority, and slop remediation.
---

# Policy Index

Central source-of-truth index for bridge-burning policies, red-flag catalogs, proof/test rules, QC authority, and slop remediation.

## Policy Routing Index

| Question | Canonical source |
| --- | --- |
| What hard bridge-burning policies apply? | [anti-slop/SKILL.md#Bridge-Burning Policies](file:///home/dzack/ai/opencode/skills/anti-slop/SKILL.md#Bridge-Burning-Policies) |
| What code/test red flags should I scan for? | [reviewing-llm-code/references/bridge-burning-red-flags.md](file:///home/dzack/ai/opencode/skills/reviewing-llm-code/references/bridge-burning-red-flags.md) |
| What runtime control-flow shapes are banned? | [reviewing-llm-code/references/runtime-control-flow-red-flags.md](file:///home/dzack/ai/opencode/skills/reviewing-llm-code/references/runtime-control-flow-red-flags.md) |
| What policy applies to creating files dynamically from code? | [reviewing-llm-code/references/bridge-burning-red-flags.md](file:///home/dzack/ai/opencode/skills/reviewing-llm-code/references/bridge-burning-red-flags.md) (red flag, remediation policy) + [fixing-slop/SKILL.md](file:///home/dzack/ai/opencode/skills/fixing-slop/SKILL.md) |
| What policy applies to embedding large strings/prompts/messages inline in code? | [reviewing-llm-code/references/bridge-burning-red-flags.md](file:///home/dzack/ai/opencode/skills/reviewing-llm-code/references/bridge-burning-red-flags.md) (red flag, remediation policy — "Inline large strings / prompts as data" section) |
| What policy applies to embedding one language inside another (code within code)? | [reviewing-llm-code/references/bridge-burning-red-flags.md](file:///home/dzack/ai/opencode/skills/reviewing-llm-code/references/bridge-burning-red-flags.md) (red flag, remediation policy — "Code within code / embedded cross-language programs" section) |
| How do I review LLM-produced code? | [reviewing-llm-code/SKILL.md](file:///home/dzack/ai/opencode/skills/reviewing-llm-code/SKILL.md) |
| How do I fix slop without laundering? | [fixing-slop/SKILL.md](file:///home/dzack/ai/opencode/skills/fixing-slop/SKILL.md) |
| What makes a test valid proof? | [test-guidelines/SKILL.md](file:///home/dzack/ai/opencode/skills/test-guidelines/SKILL.md) |
| What test assertion patterns are banned? | [test-guidelines/references/banned-test-shapes.md](file:///home/dzack/ai/opencode/skills/test-guidelines/references/banned-test-shapes.md) |
| Who owns QC invocation/config/tooling? | [quality-control/SKILL.md](file:///home/dzack/ai/opencode/skills/quality-control/SKILL.md) |
| How do I triage PR feedback? | [pr-feedback-triage/SKILL.md](file:///home/dzack/ai/opencode/skills/pr-feedback-triage/SKILL.md) |
| How do I debug without prior-shaped probing? | [reality-grounded-debugging](file:///home/dzack/ai/opencode/skills/reality-grounded-debugging/SKILL.md) + [systematic-debugging](file:///home/dzack/ai/opencode/skills/systematic-debugging/SKILL.md) |
| How do I handle external tool/library/compiler uncertainty? | [known-solution-first](file:///home/dzack/ai/opencode/skills/known-solution-first/SKILL.md) |
| How do I provision tools? | [tool-provisioning-and-environment-hygiene](file:///home/dzack/ai/opencode/skills/tool-provisioning-and-environment-hygiene/SKILL.md) |
