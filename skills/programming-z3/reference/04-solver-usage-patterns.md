# 04 - Usage Patterns Built On Solver APIs

Source anchors: section 5, subsections 5.1-5.7 (approx lines 1239-1632).

## 5.1 Blocking Models / Enumeration

Baseline model-blocking pattern:

```python
from z3 import *

def block_model(s):
    m = s.model()
    s.add(Or([d() != m[d] for d in m.decls() if d.arity() == 0]))
```

Term-focused blocking:

```python
from z3 import *

def block_model_terms(s, terms):
    m = s.model()
    s.add(Or([t != m.eval(t, model_completion=True) for t in terms]))
```

Scope-based recursive variant avoids unbounded permanent lemma growth.

## 5.2 Maximal Satisfying Subsets (MSS)

Tutorial provides greedy MSS construction using model-guided extension and backbone hints.

Core idea:
- start from currently true predicates,
- attempt adding candidates,
- keep negatives as backbones when extension fails.

## 5.3 Enumerating Cores and Correction Sets (MARCO)

Tutorial includes MARCO structure:
- map solver tracks unexplored subset space,
- on sat seed: produce MSS and block supersets,
- on unsat seed: extract MUS and block subsets.

This is a practical template for complete MUS/MSS exploration in medium-size settings.

## 5.4 Bounded Model Checking (BMC)

Pattern from tutorial:
- unroll transition relation iteratively,
- assert reachability guard literal per depth,
- query sat under guard assumption,
- if sat, return witness model.

Notes:
- great for reachability bug finding;
- not complete for proving unreachability (tutorial points to IC3 for that).

## 5.5 Interpolation via Models + Cores

Tutorial demonstrates interpolation loop (`pogo`) combining:
- model extraction from side A,
- assumption checks against side B,
- unsat-core-based blocking clauses.

Use when you need constructive separators between inconsistent formula partitions.

## 5.6 Monadic Decomposition Prototype

Tutorial includes a recursive prototype for decomposition into single-variable components.

Takeaway for engineering:
- this is advanced and expensive;
- use as a specialized transformation when downstream automation needs monadic structure.

## 5.7 Contextual Subterm Simplification

Tutorial builds custom simplification using:
- subterm extraction,
- model evaluation cache,
- solver-assisted equivalence checks (`t1 != t2` under push/pop).

Pattern is useful when default `simplify(...)` is too local and context-blind.

## Decision Heuristics

- Need many models? Start with term-scoped blocking + recursion via scopes.
- Need diagnosis/explanations? Track assumptions and use cores.
- Need reachability witnesses? Use BMC pattern.
- Need stronger simplification under constraints? Use model+equivalence contextual simplifier.
