# Implementation-Adjacent Tier

> Load this after routing to the implementation-adjacent tier in `../SKILL.md`. The
> universal skeleton and policies there still apply; this file supplies the implementation
> body and quality bar.

An implementation-adjacent plan is a scoring rubric for one coherent piece of work:
endpoint, constraints, acceptance, proof. It is loose on mechanism and tight on outcome.

## First question: does this leaf need to exist?

Often it does not. When the parent plan already constrains the endpoint, a strong
implementer's own internal planning covers the rest, and writing a leaf artifact only steps
on their toes while tracking nothing more auditable than the resulting commits. Write a leaf
plan only when it coordinates multiple actors, preserves restartable state across a long or
risky task, or records a decision the commits alone would not explain. Otherwise hand the
implementer the parent rubric and let them work.

## Calibration: rubric, not leash

When you do write it, keep it a rubric: tight enough to (1) tell the implementer roughly
what the right endpoint is and (2) rank several independent implementations of it, and loose
enough that many implementations pass. Do not prescribe the exact diff or the lines to
touch — that is the implementer's job and is no more auditable than the commits.

## Body sections (replace the universal work-decomposition slot)

```markdown
## Task Plan
### <Task name>
- Obligation served:
- Files:
- Preconditions:
- Change:
- Acceptance criteria:
- Proof / verification:
- Commit boundary:

## System-Level Validation
- Real boundary checks:
- Regression checks:
- Review or artifact checks:
```

## Task quality

Every nontrivial task must answer:

- **Where:** exact file, module, command, route, artifact, or external surface.
- **What:** the concrete state change, not a vague action verb.
- **Why:** the obligation or milestone it serves.
- **Before:** dependencies and inputs that must already exist.
- **Done:** observable acceptance criteria.
- **Proof:** command, test, artifact, diff, or inspection that would fail if the work were
  wrong.
- **Commit:** the smallest coherent checkpoint boundary.

Even at this tier, **What** is the state change and **Where** is the surface; the exactness
that matters most lives in **Done** and **Proof**, which must be sharp enough to fail a
plausible broken implementation. Naming files and a change is fine; dictating the literal
diff is not.

For code tasks, include the TDD or reproducer sequence when applicable: write or identify
the failing proof, confirm it fails for the intended reason, implement narrowly, rerun the
same proof, then run the relevant system gate.

Tasks should be assignment-sized: small enough for a focused implementation pass, but not
so small that they track typing, file touching, classification, or environment trivia.
