---
description: Review product delivery and supporting machinery at milestones or when work stalls.
---

Read and apply the installed upstream skills
`.specify/extensions/frontier-simplify/skills/frontier-simplify/SKILL.md` and
`.specify/extensions/frontier-simplify/skills/frontier-simplify-audit/SKILL.md`.
Use a current review if it covers the work. At milestones and during prolonged
implementation, inspect actual delivery rather than relying on completion claims.
Review sooner when a design repeatedly fails or process prevents delivery.

Classify LOC by actual purpose. Product is the required implementation and its
behavioral tests, including independent domain specifications; support is the
infrastructure, governance, instrumentation and their tests. In a mathematical
project, preserving a selected cone and testing a mathematical assertion are
product; Custodian seals, timing-record hashes, and their meta-tests are support.
A defective product abstraction (such as reconstructing selections from
`Expr.mdata`) is not a delivered result. Judge the public execution path and
actual test behavior, not a commit message or a promised future use.

Run the upstream read-only helper with disjoint path expressions for this tree:

```sh
sh .specify/extensions/frontier-simplify/skills/frontier-simplify-audit/scripts/measure.sh '<support-path-regex>' '<product-path-regex>'
git log --first-parent --numstat --since='24 hours ago'
```

Compare the standing machinery-to-product LOC ratio and its trend, recent
support-only commit density, and actual delivered behavior. Approximate significant
mixed files; distinguish imported tooling and inherited acceptance specimens.
Do not credit an unsubstantiated classification as product. For substantial
implementation reviews, use the installed upstream frontier-simplify-review
skill; its optional runner is not a prerequisite.

If machinery rivals the product, support dominates recent work, or repeated
repairs fail to deliver, challenge the design, delete unnecessary machinery or
replace the failed abstraction. Keep the original requirements and real tests.
Apply the findings to the work and continue. No new review gate or audit ledger.
