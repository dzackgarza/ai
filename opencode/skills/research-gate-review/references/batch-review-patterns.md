# Batch Review Pipeline — Session 2026-05-07

## Proven batching pattern

The optimal pattern for dispatching 6-gate reviews at scale:

```
delegate_task(tasks=[
  {context: "6-GATE SPEC REVIEW... CARD: /path/to/card1.md", goal: "...", toolsets: ["terminal","file","web"]},
  {context: "6-GATE SPEC REVIEW... CARD: /path/to/card2.md", goal: "...", toolsets: ["terminal","file","web"]},
  {context: "6-GATE SPEC REVIEW... CARD: /path/to/card3.md", goal: "...", toolsets: ["terminal","file","web"]}
])
```

- 3 parallel subagents, 1 card each
- Throughput: ~3 cards per 8-10 minutes (verified across 5 batches, 14/15 successes, 1 timeout)
- Timeout rate: 1 in 15 (SPEC-MAPPING-LATTICES at 600s with 42 API calls)

## Card-type-specific context templates

### SPEC card context (compact)

```
6-GATE SPEC REVIEW (G1-G6):
G1 Source grounding - verify referenced files exist
G2 Sage surface completeness - all inventoried surfaces accounted
G3 Constructor route justification - mathematically valid routes
G4 Nonmathematical rejection - explicit rejections with rationale
G5 Ambiguity routing - unresolved issues routed to decision cards
G6 Obligation preservation - no weakening without replacement

CARD TO REVIEW: <path>

WRITE '## 6-Gate Protocol Review Log' into card body with concrete evidence.
Working directory: /home/dzack/research
```

### PHASE card context (compact)

```
6-GATE PHASE CARD REVIEW (G1 source grounding, G2 exit criteria checkable,
G3 task inventory complete, G4 no scope creep, G5 deps correct, G6 no weakening).

CARD: <path>

WRITE '## 6-Gate Protocol Review Log' into card body.
Working directory: /home/dzack/research
```

### PLAN card context (compact)

```
6-GATE PLAN CARD REVIEW (G1 source grounding, G2 exit criteria checkable,
G3 phase inventory complete, G4 scope containment, G5 deps correct, G6 no weakening).

CARD: <path>

Verify phase inventory, exit criteria, dependencies, scope.
WRITE '## 6-Gate Protocol Review Log' into card body.
Working directory: /home/dzack/research
```

## Bugs found by subagents this session

Real issues discovered across 15 reviews:

| Card | Gate | Finding |
|------|------|---------|
| SPEC-MAPPING-RINGS | G5 | 3 missing decision cards: roots-of-unity owner, Ore localization owner, q-adic lattice precision |
| SPEC-MAPPING-ALGEBRAS | G2 | 3 unaccounted Sage surfaces: semisimple_quotient(), Supercommutative(), radical() gap |
| SPEC-MAPPING-ALGEBRAS | G5 | Cellular subcategory missing decision card reference |
| SPEC-MAPPING-MODULES | G1 | Broken reference to deleted wrapper migration plan |
| SPEC-MAPPING-MODULES | G5 | ~15 uninventoried Sage module files on disk |
| SPEC-MAPPING-CAT | G1 | IsomorphicObjectsCategory table path wrong (cat/ vs sets/) |
| SPEC-MAPPING-FORMS | G1 | Stale theory file path (relocated during repo restructuring) |
| SPEC-MAPPING-FORMS | G1 | Source Coverage Ledger missing quadratic_form__local_field_invariants.py |
| SPEC-MAPPING-TENSOR | G5 | Stale TRIAGE.md reference (file deleted, superseded by decision card) |
| SPEC-DISCRIMINANTGROUP | G1 | Source rot: theory file deleted in checkpoint commit |
| SPEC-FORMS-ISOMETRY | G1 | Stale theory path (actual file under .agents/memories/) |
| SPEC-FORMS-DIVISIBILITY | G1 | 2 relocated theory file references |
| PHASE-CAT-OBJECT-SURFACE | G3 | Success criterion 5 lacks explicit child task owner |
| PHASE-LITERAL-METHOD | G3 | Stray undeclared task artifact in directory |
| PHASE-HOM-END-AUT | G5 | Self-referential dependsOn in wrapup task |
| PHASE-MODULE-WRAPPER | G5 | Self-referential dependsOn in wrapup task |
| PHASE-SETS-TOPOLOGICAL | G5 | Empty dependsOn; self-referential wrapup; premature review (4/6 children not complete) |
| PHASE-POSET | G4,G5 | Scope creep (set-partition tasks under poset phase); missing dependency edge between sibling tasks |
| PLAN-CATEGORY-SPEC-SOURCE-MAPS | G1,G5 | 8 dead source file references; dangling subplan reference to nonexistent PLAN-GEOMETRIC-CATEGORY-EXPANSION |
| PLAN-FOUNDATION-KERNEL | G1,G2,G3 | 5 migrated source files lack status annotations; YAML successCriteria and body checkboxes misaligned; coverage gaps for standard type aliases, module axioms, TwistedForms |
| PLAN-SMOKE-AUDIT | G1,G3,G5 | 2 dead links, 1 misattributed phase, missing phases for described work; cross-plan dependency undeclared in YAML |
| PLAN-GEOMETRIC-SOURCE-ADMISSION | G5 | YAML dependsOn: [] contradicts body dependency on PLAN-CATEGORY-SPEC-SOURCE-MAPS |
| PLAN-CURVE-COMPLEMENT-MONODROMY | G5 | Same pattern: empty dependsOn in YAML, body declares dependency |
| PLAN-STATIC-CATEGORY-REFINEMENT-ORDER | G1,G2,G4 | Dead reference to category-abc-spec.md; success criterion #1 falsified (11 table rows vs 30+ code returns); PartitionedSets row contradicts actual super_categories() return |
| PLAN-CONSTRUCTOR-ADMISSION | G4 | Minor: PHASE-VARIADIC has parent ambiguity (frontmatter says one plan, body says another) |

Recurring patterns:
- **Stale file references** (5 instances in specs, 4 in plans): theory files deleted or relocated during repo restructuring. Check `git log -- <path>` for every referenced file.
- **Self-referential dependsOn** (3 instances in phases): wrapup tasks listing themselves. Trivially detectable.
- **Missing decision cards** (2 instances): spec says "decision needed" but no card exists in decisions/.
- **YAML dependsOn contradicts body dependency** (3 instances in plans): plan body declares a cross-plan dependency, but frontmatter `dependsOn` is empty. Add the dependency to YAML.
- **Success criteria misalignment** (2 instances in plans): YAML `successCriteria` and body checkboxes mismatched or duplicated.
- **Phase misattribution** (2 instances): phase card parented to one plan in frontmatter but described as belonging to another in body prose.

## Triage before dispatch

Before dispatching any reviews, run this scan:

```python
import os, re

for root, dirs, files in os.walk('plans/features'):
    for f in files:
        if not f.endswith('.md'): continue
        path = os.path.join(root, f)
        with open(path) as fh: content = fh.read()
        m = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if not m: continue
        if 'status: needs-review' not in m.group(1): continue
        if '## 6-Gate Protocol Review Log' in content or '## Review Log' in content:
            # Card already reviewed — check if waiting for human
            last_review = content[content.rfind('## '):]
            if re.search(r'(human acceptance|human approval|pending human)', last_review, re.I):
                # Move to needs-human-input
                ...
            elif 'Gates failed' not in last_review or 'none' in last_review.lower():
                # All gates passed — promote to complete
                ...
```

Cards already reviewed but not promoted are almost always awaiting human signoff. Moving them to `needs-human-input` prevents redundant re-review.

## Large spec timeout recovery

SPEC-MAPPING-LATTICES (and similar >500-line mapping specs) will timeout at 600s. Recovery options:
1. Split review: "review only the lattice tier table" → separate subagent → "review only the constructor routes"
2. Give the subagent a grep-based checklist instead of asking it to read every Sage source file
3. Pre-compute source file existence and provide it in the context so the subagent doesn't spend API calls on `ls`/`find`
