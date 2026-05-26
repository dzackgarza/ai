# QC Ignore Justifications

Every global suppression in QC tool configuration must be justified here in prose.
No suppression is accepted without a written justification traceable to domain
constraints, naming conventions, or architectural realities that the tool was not
designed to accommodate.

Rule: if a finding can be fixed in code without violating project style docs or
mathematical conventions, fix the code.
If it cannot, justify the ignore here.
No third category ("too hard," “not worth it,” "phase-appropriate").

* * *

## ruff E741: Ambiguous variable name detection

**Status**: Globally disabled in `ruff-global.toml`.

**What the rule does**: Flags single-character variable names that are visually
ambiguous with numerals or other characters — `I` (vs `l`), `O` (vs `0`), `l` (vs `1`).

**Why we disable it**:

Mathematical code uses single-letter identifiers as standard notation.
This is not lazy naming — it is the canonical surface language of algebra, and replacing
these identifiers with descriptive names would make the code *less* readable to its
domain audience:

- `I` for an ideal is universal in commutative algebra and algebraic number theory.
  Replacing it with `the_ideal` or `ideal_obj` obscures the mathematical intent.
  A reader of algebraic code expects `I = R.ideal(6)` the same way they expect `i` for a
  loop index in imperative code.

- `R` for a ring, `M` for a module, `G` for a group, `V` for a vector space, `K` for a
  field, `L` for a lattice — these are the standard identifiers in every algebra
  textbook and Sage tutorial.
  Forcing `the_ring`, `the_module` is actively harmful to readability.

- `O` for an object in category-theoretic code follows the same pattern: objects of a
  category are conventionally denoted by single letters.

The `research-code-style` skill mandates: “All code must read like mathematical prose,
and semantically follow either a definition or a theorem.”
Mathematical prose uses single-letter identifiers for algebraic objects.
E741 contradicts this mandate.

The rule also has no mechanism for context: `I` in a function called
`_install_ideal_patch` is clearly an ideal, not a typo for `l`. E741 has no scope-level
granularity — it is either on or off per configuration.

**Alternatives considered**:

- Per-file `# noqa: E741` comments could be placed at every `I =` assignment site.
  Rejected: this would scatter comments across ~50+ files and is brittle (new `I =`
  assignments would produce new violations).
  The convention is universal, not exceptional.

- Raising the specificity to only suppress within `tests/` or `src/` directories.
  Rejected: the convention is equally valid in all math code, and a directory-scoped
  disable is harder to discover than a global one with a documented justification.

- Renaming variables to `ideal_` or `ideal_obj`. Rejected: degrades readability and
  violates the code-style mandate.

**Scope**: All projects.
E741 is disabled globally because mathematical code using standard algebraic identifiers
is not limited to the research repo — it appears in any project that does commutative
algebra, number theory, algebraic geometry, representation theory, or category theory
work.

**Review cadence**: If ruff ever adds a context-aware variant of E741 that accepts `I`
when assigned from known ideal constructors, or a per-pattern allowlist, this ignore
should be replaced with that narrower mechanism.

* * *

## ruff UP049: Private type parameter names in PEP 695 generics

**Status**: Globally disabled in `ruff-global.toml`.

**Governance note**: All entries in this file are human-justified decisions made with
explicit human review and sign-off.
Agents must never add entries to this file or add rules to `ruff-global.toml` without
explicit human-in-the-loop approval.
The permitted agent action is to flag a candidate rule for human review — not to make
the decision unilaterally.

**What the rule does**: In PEP 695 type parameter syntax (`def f[T: Bound](...)`), flags
type parameters whose names begin with `_` and renames them to drop the leading
underscore.

**Why we disable it**:

The `_` prefix on a name communicates *intent* to human readers: this identifier is an
internal implementation detail, not part of the public API surface.
This convention is well-established in Python and universally understood.
UP049’s premise — that the leading underscore is unnecessary because PEP 695 type
parameters are always function-scoped — conflates two distinct purposes of the `_`
convention:

- **Scoping signal**: “this name is not importable from outside the module.”
  UP049 is correct that PEP 695 type parameters are always locally scoped, so `_` adds
  nothing for scoping purposes.

- **Readability signal**: “this name is an internal mechanism; readers of call sites and
  subclasses need not concern themselves with it.”
  This purpose is entirely independent of scoping and is not addressed by PEP 695.

For this codebase, the type parameters involved (`_CatCachedMethod`,
`_BilinearCachedMethod`, `_FieldCachedMethod`, etc.)
are internal wrapper function types that appear nowhere in public documentation,
subclassing contracts, or user-facing API. Removing the `_` prefix promotes them to
apparently-public names with no semantic benefit and actively misleads readers about
which names belong to the public surface.

The user reviewed this rule during a live fix session (2026-05-13) and explicitly
concluded: the `_` prefix makes implicit behaviour *explicit* — the opposite of what
UP049 claims. The rule is wrong for this codebase.

**Alternatives considered**:

- Accept the rename and drop the `_` convention for PEP 695 type parameters only.
  Rejected: introduces a two-tier naming convention (old-style TypeVar uses `_`, PEP 695
  uses public names) with no readability benefit.

- Per-function `# noqa: UP049`. Rejected: scatters suppressions and is fragile as new
  generic wrappers are added.

**Scope**: All projects.
The readability argument for `_`-prefixed type parameters applies universally to any
codebase with internal generic wrapper functions.

**Review cadence**: If PEP 695 tooling develops a mechanism to mark type parameters as
explicitly non-public (analogous to `__all__` for modules), this ignore should be
replaced with that mechanism.
