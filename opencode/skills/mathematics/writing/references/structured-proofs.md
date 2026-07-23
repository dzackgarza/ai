# Structured Proofs (Lamport Style)

Source: Leslie Lamport, *How to Write a Proof* (1993),
`https://lamport.azurewebsites.net/pubs/lamport-how-to-write.pdf`.
The method is a practical refinement of natural deduction for the less formal proofs
of ordinary mathematics, "based on hierarchical structuring — a successful tool for
managing complexity." Its stated purpose: **make it much harder to prove things that
are not true.** Lamport's evidence: rewriting conventional proofs in this style
revealed serious mistakes in almost every one (including a published error in
Kelley's *General Topology* proof of Schroeder–Bernstein, rediscovered "within
minutes" of structuring it), and repeatedly exposed false conjectures that a
convincing prose sketch would have "proved."

This is the **default presentation for proofs and multi-step mathematical arguments**
in this system: in chat, in prose documents, in comments and docstrings, and in
LaTeX. Prose paragraph form is reserved for the lowest levels and for the situations
listed under "When prose is acceptable."

## Why prose proofs fail

- Proofs written in prose are hard to understand and hard to get right; anecdotal
  evidence suggests as many as a third of published mathematical papers contain
  incorrect theorems or proofs.
- The same two devices that made formulas readable — **naming** and **manifest
  structure** — make proofs readable. A prose proof hides its logical structure the
  way `(1)`-style prose hides a formula's structure.
- For an LLM author the failure is sharper: prose is where "clearly", skipped cases,
  and unbound variables hide. The structured format makes each omission visible as a
  missing step, a missing justification, or a missing Q.E.D. proof. It is a
  behavioral interlock, not a formatting preference.

## Anatomy of a structured proof

In order:

1. **Theorem statement** — precise, all quantifiers and types explicit.
2. **Proof sketch** (optional but preferred for nontrivial proofs) — a short informal
   road map explaining intuitively why the proof works. It carries no proof burden;
   it exists so the reader knows where the steps are going. Omit it only when the
   high-level steps are self-explanatory.
3. **Assume / Prove clauses** — numbered assumptions and the exact goal. They assert:
   to prove the theorem, it suffices to assume these and prove that. For a
   contradiction proof the goal is literally `False`.
4. **The proof body** — a numbered sequence of assertion steps ending in a **Q.E.D.
   step**. The Q.E.D. step's statement is the `Prove` goal; its proof explains how
   the preceding steps combine (and, in a case split, why the cases are exhaustive).
5. **Each step has its own proof**, recursively: either a short lowest-level
   paragraph proof, or another structured proof (its own Assume/Prove, steps, and
   Q.E.D.). The high-level steps alone read like the statement column of a
   two-column proof; the reader descends only where skeptical.

### Step constructs

- **Assertion step** — a claim, proved by its own lower-level proof.
- **`Choose`** (existential instantiation) — introduce witnesses with their
  properties as numbered parts: `Choose m, n in ZZ such that: 1. gcd(m,n) = 1,
  2. r = m/n.`
- **`Let:`** — definition of new symbols. Prefer an explicit "equals by definition"
  marker (Lamport uses `≜`; in text, `:=` is acceptable) so definitions are never
  confused with derived equalities.
- **`Assume:`/`Prove:` inside a step** — reduce the goal ("By the definition of gcd,
  it suffices to: Assume: 1. s divides m, 2. s divides n. Prove: s = ±1").
  This is the structured form of "it suffices to show".
- **`Case:`** — `Case: A` abbreviates `Assume: A, Prove: Q.E.D.` The final Q.E.D.
  step of the enclosing proof must prove the cases exhaustive. Case steps are more
  flexible than a rigid proof-by-cases block: a numbered step proved before the
  split can be cited inside every case.
- **Equality/relation chains** — a string of equalities (or any transitive relation:
  `<`, `≤`, `⟺`, `⟹`) with a bracketed justification on every line:

  ```
  Proof: m/n = (p/gcd(p,q)) / (q/gcd(p,q))   [definition of m and n]
             = p/q                            [simple algebra]
             = r                              [by <2>1]
  ```

  "Simple and direct … It should be used whenever possible."

### Numbering and references

Two schemes; both appear in this system.

- **Dotted scheme** for shallow proofs (≤ 3 levels): steps `1`, `2`, …; the proof of
  step `1` has steps `1.1`, `1.2`, …; the proof of `1.4` has `1.4.1`, ….
- **Level-bracket scheme** for anything deeper, and the default in fresh writing:
  `<1>1, <1>2, …` are the top-level steps; the proof of any level-1 step uses
  `<2>1, <2>2, …`; and so on. `<5>2` abbreviates a five-part number ending in 2.
  This is unambiguous because a step may be cited **only inside the proof of its
  parent** — only under the assumptions in force where it was proved — so at any
  point at most one step named `<5>2` is citable, and a reference always means the
  most recent one.
- **Assumption references**: `<2>:1` is assumption 1 of the current level-2 ancestor
  step's Assume clause; the theorem itself is the level-0 step, so `<0>:2` is the
  theorem's assumption 2. In the dotted scheme, `1.4:1` is assumption 1 in the proof
  of step 1.4.
- **Part references**: `<1>1.2` is part 2 of the statement of step `<1>1` (e.g. the
  second property of a `Choose`).
- Every citation of a step, assumption, or part is **by name**. This is what makes
  hypothesis usage searchable: in a properly written structured proof, plain text
  search reveals exactly where every assumption is used — which is how you check
  whether a hypothesis can be weakened.

## The discipline (what makes it work)

The format alone does not eliminate errors. The rules that do:

- **Depth rule of thumb**: expand the proof until the lowest-level statements are
  obvious, **then continue for one more level**. Most errors come from not carrying
  the proof to enough levels.
- Lowest-level paragraph proofs must be **short and completely transparent** ("By
  assumption <0>:1", "By <2>2 and the lemma"). If a leaf proof needs a paragraph of
  argument, it is not a leaf; give it structure.
- **"This case is similar to the previous one" is not acceptable.** Find the general
  step that makes the proof of both cases easy, prove it once before the split, and
  cite it in each case.
- Be a **skeptical reader of your own proof**. Structured proofs are longer than
  prose ones because they include more detail — that is the point. They "make it
  obvious when steps have been forgotten or important details omitted. They make it
  hard to be sloppy." The shortest proof is always "left as an exercise for the
  reader."
- **Two versions when length matters**: keep the fully expanded proof as the working
  artifact (for yourself, verifiers, and referees); produce a compressed version for
  final publication by collapsing the lowest levels into paragraph proofs. Compressing
  a structured proof is easy; the reverse is where errors hide. Never write only the
  compressed version of a nontrivial new result.
- **Read (and present) level by level**: first the `<1>` steps and Q.E.D., then the
  proofs of those steps. In an interactive setting, this is the progressive
  disclosure contract: show the top level; expand a step when the reader asks or
  when the claim is load-bearing and non-obvious.

## Worked example (house markdown rendering)

The paper's running example, in the exact form to produce in chat or markdown. The
proof is deliberately carried to a lower level than a human reader needs, to show
the mechanics.

**Theorem.** There does not exist $r \in \mathbf{Q}$ such that $r^2 = 2$.

**Proof sketch.** Assume $r^2 = 2$ for $r \in \mathbf{Q}$ and obtain a
contradiction. Writing $r = m/n$ in lowest terms (step <1>1), we deduce from
$(m/n)^2 = 2$ and the lemma (if $2 \mid n^2$ then $2 \mid n$) that both $m$ and $n$
are divisible by 2 (steps <1>2, <1>3).

- **Assume:** 1. $r \in \mathbf{Q}$  2. $r^2 = 2$
- **Prove:** False

- **<1>1.** Choose $m, n \in \mathbf{Z}$ such that: 1. $\gcd(m,n) = 1$  2. $r = m/n$
  - **<2>1.** Choose $p, q \in \mathbf{Z}$ such that $q \neq 0$ and $r = p/q$.
    - Proof: By assumption <0>:1.
  - **Let:** $m := p/\gcd(p,q)$, $\ n := q/\gcd(p,q)$
  - **<2>2.** $m, n \in \mathbf{Z}$
    - Proof: <2>1 and definition of $m$ and $n$.
  - **<2>3.** $r = m/n$
    - Proof: $m/n = \dfrac{p/\gcd(p,q)}{q/\gcd(p,q)}$ [definition of $m$, $n$]
      $= p/q$ [simple algebra] $= r$ [by <2>1].
  - **<2>4.** $\gcd(m,n) = 1$
    - Proof: By the definition of gcd, it suffices to:
      **Assume:** 1. $s \mid m$  2. $s \mid n$  **Prove:** $s = \pm 1$
    - **<3>1.** $s \cdot \gcd(p,q)$ divides $p$.  Proof: <2>:1 and the definition of $m$.
    - **<3>2.** $s \cdot \gcd(p,q)$ divides $q$.  Proof: <2>:2 and the definition of $n$.
    - **<3>3.** Q.E.D.  Proof: <3>1, <3>2, and the definition of gcd.
  - **<2>5.** Q.E.D.
- **<1>2.** $2 \mid m$.
  - **<2>1.** $m^2 = 2n^2$.  Proof: <1>1.2 implies $(m/n)^2 = 2$.
  - **<2>2.** Q.E.D.  Proof: By <2>1 and the lemma.
- **<1>3.** $2 \mid n$.
  - **<2>1.** Choose $p \in \mathbf{Z}$ such that $m = 2p$.  Proof: By <1>2.
  - **<2>2.** $n^2 = 2p^2$.
    - Proof: $2 = (m/n)^2$ [<1>1.2 and <0>:2] $= (2p/n)^2$ [<2>1] $= 4p^2/n^2$
      [algebra], from which the result follows easily by algebra.
  - **<2>3.** Q.E.D.  Proof: By <2>2 and the lemma.
- **<1>4.** Q.E.D.
  - Proof: <1>1.1, <1>2, <1>3, and definition of gcd. $\blacksquare$

## The Case construct (paper's Figure 6)

**Theorem.** All natural numbers are interesting.

- **Assume:** $n$ a natural number.  **Prove:** $n$ is interesting.
- **<1>1.** A number is interesting if it is the smallest number not in an
  interesting set.  Proof: By definition of interesting.
- **<1>2.** **Case:** $n = 0$.
  - Proof: By <1>1, since 0 is the smallest natural number not in $\emptyset$.
- **<1>3.** **Case:** 1. $n > 0$  2. $n - 1$ is interesting.
  - Proof: By <1>1, since case assumption <1>:1 implies that
    $\{k : k \le n-1\}$ is interesting.
- **<1>4.** Q.E.D.
  - Proof: Steps <1>2 and <1>3, assumption <0>, and mathematical induction.

Note `<1>1` is cited inside both cases — the reason Case steps beat a rigid
proof-by-cases block.

## Calibration by context

The format scales down; the discipline does not. What varies is the **depth carried
in the visible artifact**, never whether steps are named, goals stated, and
justifications attached.

| Context | Presentation |
|---|---|
| Chat argument, short claim | Assume/Prove + the `<1>` level only; each step gets a one-line bracketed proof. Offer to expand any step on request. |
| Chat, nontrivial or disputed claim | Full structure to the depth rule ("obvious + one more level"). This is where the format earns its keep — do not substitute a prose sketch because it is chat. |
| Prose document / notes / LaTeX | Proof sketch + structured proof. For LaTeX use nested `enumerate` or `pf`-style macros; keep step names citable in the text. |
| Papers for human venues | Working version fully structured; published version may compress the lowest levels into paragraph proofs. Keep the detailed version in the repo. |
| Docstrings / code comments carrying a correctness argument | Assume/Prove and the `<1>` steps as a compact block; cite invariants and lemmas by name. A correctness comment that is one prose paragraph is a red flag. |
| Formalization targets | The structured proof **is** the Lean skeleton: steps become `have`/`suffices`/`obtain`/`cases`, Assume/Prove becomes the goal statement, leaf proofs become tactic calls. Write the structured proof first, then transcribe. |

## When prose is acceptable

- Lowest-level leaf justifications (always).
- One-step or purely computational arguments where a single equality chain with
  bracketed reasons carries the whole burden.
- Restating a known result with a citation instead of a proof.
- A user explicitly asks for a prose or textbook-style exposition — then still keep
  variables bound, cases exhaustive, and justifications inline, and say that the
  structured version is available.

## Anti-patterns

| Pattern | Why bad | Do instead |
|---|---|---|
| Prose paragraph for a multi-step proof | Hides gaps; "as many as a third of published proofs are wrong" | Structured steps with named citations |
| "Similar to the previous case" | The paper's canonical banned move | Extract the shared general step before the split |
| Q.E.D. with no proof line | The combination logic (and case exhaustiveness) is exactly where errors hide | Prove the Q.E.D. step like any other |
| Citing "the above" / "what we showed" | Unsearchable, ambiguous | Cite by step name: `<2>3`, `<1>:2` |
| Deep detail everywhere in a chat answer | Buries the outline the reader needed | Top level first; expand on demand |
| Compressed proof as the only artifact for a new result | Errors survive in the omitted levels | Keep the expanded version; compress for presentation |
| Sketch promoted to proof | "Time and again … a proof sketch that could easily have been turned into a convincing conventional proof" was false | The sketch is a road map; burden lives in the steps |
