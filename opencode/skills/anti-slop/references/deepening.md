# Deepening: From Shallow Modules to Deep Interfaces

How to deepen a cluster of shallow modules safely, given its dependencies. Assumes the vocabulary in [`deepening-vocabulary.md`](deepening-vocabulary.md) — **module**, **interface**, **seam**, **adapter**, **leverage**, **locality**.

## The Constructive Inverse of Anti-Slop

Anti-slop detects shallow modules (pass-throughs, bespoke reinvention, interface inflation). This reference tells you what to replace them with: deep modules that concentrate leverage at their interface and locality in their implementation.

The **deletion test** is the key diagnostic. Imagine deleting the module:
- If complexity vanishes → it was a pass-through (shallow, delete it or deepen it)
- If complexity reappears across N callers → it was earning its keep (deep, preserve it)

## Dependency Categories

When assessing a candidate for deepening, classify its dependencies. The category determines how the deepened module is tested across its seam.

### 1. In-process

Pure computation, in-memory state, no I/O. Always deepenable — merge the modules and test through the new interface directly. No adapter needed.

### 2. Local-substitutable

Dependencies that have local test stand-ins (PGLite for Postgres, in-memory filesystem). Deepenable if the stand-in exists. The deepened module is tested with the stand-in running in the test suite. The seam is internal; no port at the module's external interface.

### 3. Remote but owned (Ports & Adapters)

Your own services across a network boundary (microservices, internal APIs). Define a **port** (interface) at the seam. The deep module owns the logic; the transport is injected as an **adapter**. Tests use an in-memory adapter. Production uses an HTTP/gRPC/queue adapter.

Recommendation shape: *"Define a port at the seam, implement an HTTP adapter for production and an in-memory adapter for testing, so the logic sits in one deep module even though it's deployed across a network."*

### 4. True external (Mock)

Third-party services (Stripe, Twilio, etc.) you don't control. The deepened module takes the external dependency as an injected port; tests provide a mock adapter.

## Seam Discipline

- **One adapter means a hypothetical seam. Two adapters means a real one.** Don't introduce a port unless at least two adapters are justified (typically production + test). A single-adapter seam is just indirection.

- **Internal seams vs external seams.** A deep module can have internal seams (private to its implementation, used by its own tests) as well as the external seam at its interface. Don't expose internal seams through the interface just because tests use them.

## Testing Strategy: Replace, Don't Layer

- Old unit tests on shallow modules become waste once tests at the deepened module's interface exist — delete them.
- Write new tests at the deepened module's interface. The **interface is the test surface**.
- Tests assert on observable outcomes through the interface, not internal state.
- Tests should survive internal refactors — they describe behaviour, not implementation. If a test has to change when the implementation changes, it's testing past the interface.

## Interface Design: Design It Twice

When exploring alternative interfaces for a deepened module, use a parallel sub-agent pattern. Your first idea is unlikely to be the best.

### Process

1. **Frame the problem space** — Write a user-facing explanation of the constraints: what invariants any new interface must satisfy, what dependencies it relies on (and their category), and a rough code sketch to ground the constraints.

2. **Spawn 3+ sub-agents in parallel** — each producing a radically different interface for the deepened module:
   - Agent 1: Minimize the interface — aim for 1-3 entry points max. Maximise leverage per entry point.
   - Agent 2: Maximise flexibility — support many use cases and extension.
   - Agent 3: Optimise for the most common caller — make the default case trivial.
   - Agent 4 (if applicable): Design around ports & adapters for cross-seam dependencies.

   Each outputs: interface types/methods/params plus invariants, usage example, what the implementation hides, dependency strategy and adapters, and trade-offs.

3. **Present and compare** — Contrast by **depth** (leverage at the interface), **locality** (where change concentrates), and **seam placement**. Give a strong recommendation, not a menu. If elements from different designs would combine well, propose a hybrid.

## Cross-References

- [`deepening-vocabulary.md`](deepening-vocabulary.md) — The glossary of terms used here.
- [`code-patterns.md`](code-patterns.md) — Detects the shallow patterns that deepening replaces.
- [`simplification.md`](simplification.md) — Patterns for simplifying existing code toward depth.
- **thermo-nuclear-code-quality-review** — Identifies missed deepening opportunities during code quality reviews. Uses this vocabulary for pass-through wrappers and "code judo" moves.
- **code-patterns/references/classes.md** — SRP and DIP overlap with deepening's emphasis on interface concentration.
- **addressing-shallow-work** — The "shallow work" concept maps directly to shallow modules. Deepening vocabulary gives it precise structure.