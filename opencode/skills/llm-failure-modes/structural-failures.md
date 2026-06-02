# Structural and Optimization Failures

> Part of [llm-failure-modes](SKILL.md).
> See there for editorial guidelines and cross-references.

1. **Fake success blocks debugging** - Suppressing errors with fallbacks, fabricated
   data, or silent recovery makes the system appear to work while hiding the actual
   failure. The error is no longer observable, so the path to diagnosis is closed.
   Work that could have fixed the root cause is spent investigating phantom behavior.

2. **Fallbacks multiply surface area** - Substituting static values, legacy APIs, or
   invented fixtures adds code that must now be maintained, tested, and debugged.
   Each fallback is a new branch that can fail independently.
   The problem space increases rather than reduces.
   Behavioral driver: fallback-legacy compulsion
   ([coding-failures.md](coding-failures.md) #20) — the agent's asymmetric risk model
   treats adding fallback code as safe and deleting legacy code as dangerous, so every
   refactor becomes additive instead of net-negative.

3. **Root-cause evasion creates churn** - Attacking proximal symptoms with guard
   clauses, `try/except`, or disabled checks leaves the upstream invariant violation
   intact. The bug resurfaces elsewhere, requiring another local fix.
   This cycle repeats until the accumulated patches exceed the complexity of the
   original system.

4. **Self-authored debris accumulates** - Code just written gets defended as backwards
   compatibility, memorialized in comments, or preserved "just in case".
   Each defense adds maintenance burden and blocks deletion.
   This is the structural consequence of fallback-legacy compulsion
   ([coding-failures.md](coding-failures.md) #20): when the agent won't delete its own
   output, every generation becomes permanent infrastructure.

5. **Error suppression plus blame shifting prevents signal** - Reframing new errors as
   pre-existing and suppressing them destroys the signal that would reveal the cause.
   The appearance of success is preserved at the cost of actual success.

6. **Wrapper slop dilutes effort** - A targeted fix wrapped in pages of fallback
   branches, defensive checks, comments, and scaffolding spreads reviewer attention
   thin. The core change is harder to verify; the surrounding debris may contain latent
   bugs.

7. **Context loss resets progress** - As context deepens, agents drift back into known
   bad patterns. Standing instructions are forgotten.
   Work that established constraints must be repeated.
