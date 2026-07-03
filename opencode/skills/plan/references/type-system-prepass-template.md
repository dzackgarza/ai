# Type-System Pre-Pass Template (Mandatory Before Implementation-Adjacent Plans)

Use this as a required prerequisite artifact for any implementation-adjacent plan slice.
If this template is incomplete, the implementation plan is incomplete.

## 0) Traceability and scope

- Slice key/name:
- Source prompt/issue/reference driving this slice:
- Date and owner:
- Repository/module boundary:
- Chosen bounded context(s):

## 1) Domain vocabulary and bounded-context map

- List concepts and meanings as used by users and the domain:
  - Term:
  - Meaning:
  - Context(s) in which it is valid:
  - Confusable adjacent meanings:
- Explicitly reject any overloaded global/common terms that should NOT be shared across contexts.

## 2) Behavior research before implementation

Document what was researched and observed before code decisions:

- Invariants that must always hold:
  - invariant:
  - why:
  - where violated currently:
- Lifecycle/state transitions:
  - state:
  - required fields:
  - forbidden fields:
  - next/prev transitions:
- Valid examples:
  - case:
  - why valid:
- Invalid examples:
  - case:
  - failure mode:
- Edge/ambiguous/legacy cases:
  - case:
  - classification rule:

## 3) Core typed model (make illegal states unrepresentable)

### 3.1 Bounded primitives and identifiers

- Candidate primitives to brand/bracket:
  - raw type -> domain type
  - construction rule/constraint:

### 3.2 Product and sum types

- Product records with required invariants per state:
- Sum/discriminated variants:
- Error and failure unions:

### 3.3 Typed transitions

- Transition signatures:
  - input type -> output type
  - state precondition:
  - state postcondition:

## 3.4 Stub contracts and compile-time type checking

Capture how stubs/checkers prove the model before implementation ordering.

- Stub surfaces to model first (type declarations, adapter interfaces, command/event shapes, plugin APIs):
- Intended type-checker command(s) to validate them (`tsc`, `mypy`, `mcp`, etc.):
- Expected passing shape (exit code, flags, CI integration point):
- Expected intentional failures and what they should prevent:

## 4) Functional core vs effectful boundaries

- Pure transformation functions:
  - function:
  - input:
  - output:
  - invariant preserved:
- Effectful operations (ports/interfaces):
  - operation:
  - required port/interface:
  - side effects:
  - failure mode:

## 5) Boundary parser policy

- All external sources that are untrusted (set strict policy):
  - source:
  - raw input type:
  - parser/checker entrypoint:
  - normalization and error strategy:
- Parse-at-boundary points (must appear before domain/application logic):
  - point:
  - output domain type:

## 6) Shared algorithm-policy types

Capture domain algorithm choices before implementation details:

- Ordering semantics:
- Retry policy:
- Conflict-resolution rules:
- Rounding/precision policy:
- Pagination/ordering cursor policy:
- Idempotency/duplicate-prevention policy:
- Clock/time semantics:
- ID strategy and normalization policy:

## 7) Shared interfaces and architecture seams

- Facades and typed application entrypoints for this slice:
- Legacy integration mapping (if applicable):
  - legacy type:
  - adapter/parser:
  - legacy call path risk:
- Codec strategy:
  - Wire/row/request -> typed command/event
  - typed domain -> legacy persistence/response

## 8) Escape-hatch policy and debt ledger

For this slice, define explicit exception points:

- `any` / `Any` usage:
  - allowed? location:
  - rationale:
  - ticket/task to remove:
- `unknown` / `Unknown` usage:
  - allowed? location:
  - rationale:
- casts/assertions:
  - allowed? location:
  - justification:
- legacy dict/Any-like payloads:
  - allowed? location:
  - justification and expiry:

## 9) Migration and implementation sequencing (slice-first)

- Step 0 (characterization):
- Step 1 (model extraction and type commitments):
- Step 2 (codec seam construction):
- Step 3 (typed application facade):
- Step 4 (port adaptation of legacy services):
- Step 5 (entrypoint migration):
- Step 6 (strictness/architecture checks and ratchet):
- Step 7 (caller migration completeness):
- Step 8 (legacy cleanup once callers migrate):

## 10) Minimal artifacts for this slice

- Required docs in this slice:
  - behavior matrix doc:
  - transition table:
  - invariants doc:
  - type debt ledger:

## 11) Evidence and acceptance of pre-pass completion

- Evidence that valid examples are bounded and invalid examples are rejected:
- Evidence that typed boundaries are in place:
- Evidence that escape-hatch usage is intentional and reviewed:
- Evidence that the chosen typed stubs were checked by the declared type-checker command(s):
- Evidence that no implementation plan will begin from raw untyped payloads:
- Reviewer signature:

## 12) Linkages

- Implementation-adjacent plan key (to be created after pre-pass):
- Mandatory follow-on tasks that depend on this pre-pass:

---

### Fullness check (must all be true before implementation planning)

- [ ] Bounded contexts and terminology decided.
- [ ] Invariants, valid/invalid examples, and transitions documented.
- [ ] Domain model is represented as constrained primitives, product/sum forms, and typed errors.
- [ ] Pure vs effectful operations are separated with explicit ports.
- [ ] Parser policy is strict at boundaries and mapped to typed domain values.
- [ ] Shared algorithm-policy contracts are explicit.
- [ ] Escape-hatch ledger contains explicit exception handling and ownership.
- [ ] Pre-pass completion evidence and reviewer approval recorded.
