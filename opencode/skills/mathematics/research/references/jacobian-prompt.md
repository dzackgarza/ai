# The Jacobian Conjecture Prompt: Dispatching a Solver Campaign

A problem-statement document for the Jacobian Conjecture, sharing the
template structure described in
[[mathematics/research/SKILL|mathematical-research]]. Parent:
[[mathematics/research/SKILL|mathematical-research]];
completion-game design theory: [[goalcraft/SKILL|goalcraft]].

Source: `https://aaronlou.com/jacobian_counterexample_prompt.pdf`.
Verbatim text below (page furniture removed); distilled rules follow.

> **Historical note.** On July 19, 2026, Levent Alpöge posted an explicit
> counterexample $F : \mathbb{C}^3 \to \mathbb{C}^3$ with constant nonzero
> Jacobian determinant and no polynomial inverse, reportedly found using the
> Claude Fable 5 model. The counterexample was rapidly verified by many
> mathematicians (see Wikipedia's *Jacobian conjecture* article, *Counterexample*
> section). The conjecture is therefore **resolved as false**. This prompt,
> which predates the resolution, is preserved as a historical dispatch artifact
> — the bidirectional (proof-or-counterexample) design and the
> characteristic-$p$ audit target are both illustrated by how the conjecture
> actually fell.

## Verbatim prompt

> **Current task statement**
>
> Let $n \geq 1$. A polynomial map $F : \mathbb{C}^n \to \mathbb{C}^n$ is a map
>
> $$F(x) = \big(F_1(x), \ldots, F_n(x)\big),$$
>
> where each $F_i \in \mathbb{C}[x_1, \ldots, x_n]$. Its Jacobian determinant is
>
> $$\det J_F = \det\!\left(\frac{\partial F_i}{\partial x_j}\right).$$
>
> Resolve the Jacobian Conjecture completely:
>
> Every polynomial map $F : \mathbb{C}^n \to \mathbb{C}^n$ with nonzero constant
> Jacobian determinant has a polynomial inverse.
>
> You must either:
>
> 1. Prove that for every $n \geq 1$, if $\det J_F \in \mathbb{C}^\times$, then
>    there exists a polynomial map $G : \mathbb{C}^n \to \mathbb{C}^n$ such that
>    $G \circ F = \mathrm{id}_{\mathbb{C}^n}$ and $F \circ G = \mathrm{id}_{\mathbb{C}^n}$;
> 2. Disprove the conjecture by giving an explicit polynomial map
>    $F : \mathbb{C}^n \to \mathbb{C}^n$ with nonzero constant Jacobian
>    determinant and proving rigorously that $F$ has no polynomial inverse.
>
> A complete disproof must include an explicit dimension $n$, explicit
> coordinate polynomials $F_1, \ldots, F_n$, an exact computation showing
> $\det J_F \in \mathbb{C}^\times$, and a complete proof that no polynomial
> inverse exists.
>
> Partial progress does not count unless it implies exactly one of the two
> resolutions above. In particular, proofs only in dimension 1 or 2,
> bounded-degree cases, homogeneous or cubic reductions without completing the
> reduced case, formal power-series inverses, local analytic inverses,
> injectivity assumptions, birationality assumptions, reductions to another
> unproved conjecture, computational verification through any fixed dimension or
> degree, or candidate counterexamples without a complete noninvertibility
> proof are insufficient.
>
> **Search and coordination requirements**
>
> Use multiagent v2 aggressively and dynamically. You have up to 64 concurrent
> agents available. Do not use a fixed assignment such as "N agents for
> strategy X." Instead, manage the search using the following heuristics:
>
> - Begin with a genuinely diverse portfolio of proof and counterexample
>   approaches. Agents should explore algebraic geometry, commutative algebra,
>   polynomial automorphism theory, degree growth, formal inverse expansions,
>   cubic homogeneous reductions, differential forms, étale morphisms,
>   invariant theory, valuations, Newton polyhedra, elimination theory, locally
>   nilpotent derivations, topology, model theory, and computational sanity
>   checks.
> - Preserve independence during early rounds. Do not tell most agents the
>   currently favored proof or counterexample strategy.
> - Maintain an explicit registry of approach families. Group agents by the
>   mathematical idea they are using, not by superficial wording. Redirect
>   agents when too many converge to the same incomplete route.
> - Do not allow one approach to dominate merely because it gives elegant
>   reductions. A route that ends at a lemma equivalent in strength to the
>   original conjecture is not close to completion unless it supplies a
>   genuinely new proof of that lemma.
> - When an approach stalls at a theorem-strength missing lemma, mark that
>   route as blocked. Continue only if someone proposes a materially new
>   mechanism, invariant, construction, or obstruction.
> - Keep several incompatible proof and disproof routes alive through multiple
>   rounds. Cross-pollinate ideas only after independent agents have exposed the
>   real strengths and gaps of their approaches.
> - Use adversarial agents throughout. Every affirmative proof must be checked
>   for confusion between formal and polynomial inverses, local and global
>   invertibility, analytic and algebraic arguments, hidden injectivity or
>   surjectivity assumptions, characteristic-zero dependence, degree bounds,
>   denominators introduced by inversion, unjustified convergence claims,
>   nonreversible reductions, and circular use of statements equivalent to the
>   Jacobian Conjecture.
> - Every proposed counterexample must be checked for exact Jacobian
>   determinant computation, hidden polynomial inverses, birational inverses,
>   coordinate changes that trivialize it, numerical artifacts, characteristic-$p$
>   phenomena mistakenly imported into $\mathbb{C}$, and incomplete
>   noninvertibility arguments.
> - Require agents to return concrete lemmas, constructions, equations, degree
>   estimates, explicit candidate maps, or counterexamples to proposed
>   sublemmas. Reject status reports, vague optimism, and claims that an
>   unproved global compatibility statement is "routine."
> - The root agent should repeatedly synthesize, challenge, redirect, and
>   launch new rounds. Do not stop after the first wave fails.
>
> Return only when either a complete affirmative proof or a complete explicit
> counterexample survives adversarial audit. Do not return a reduction, partial
> result, isolated missing lemma, "best effort" summary, or explanation of why
> the problem is difficult.
>
> Spend at least 8 hours on this before even thinking of returning or giving
> up.
>
> Public search may be used only for ordinary mathematical background or
> standard named theorems, not to search for a solution to this exact
> conjecture or benchmark. Do not search the public web merely to determine
> whether the Jacobian Conjecture is open, and do not answer that it is open.

## Distilled rules for dispatching solver campaigns

The shared dispatch rules (exact completion contract, pre-refuted
substitutes, portfolio over convergence, blind early rounds,
equivalent-strength trap, blocked-route ledger, artifact-only returns,
termination contract with effort floor, contamination hygiene) are
generic across problem-statement documents and are not repeated here.
What follows is the **domain-specific** material: the insufficiency
catalog and the adversarial checklists, both of which encode the known
failure modes of *this* problem, written before any candidate exists.

### Insufficiency catalog (what does not count as progress)

Verified against Wikipedia's *Jacobian conjecture* article and the primary
sources it cites (Keller 1939; Wang 1980; Bass–Connell–Wright 1982; Drużkowski;
Moh; Connell–van den Dries; Adjamagbo–van den Essen). Each row names the
verified result, not an inferred one.

| Outcome | Why insufficient |
|---|---|
| Bounded-degree proofs (Wang: degree 2; Moh: degree $\leq 100$ in two variables) | JC for fixed degree is decidable in principle; a fixed-degree proof does not lift to all degrees. Wang proved degree-2 (any dimension); Moh checked degree $\leq 100$ in two variables — both are bounded, neither resolves the full statement |
| Dimension-1 proof | In $n=1$ the claim reduces to "polynomial with nonzero constant derivative has a polynomial inverse," which is elementary (linear); the open content is $n \geq 2$ |
| Cubic homogeneous reductions without completing the reduced case | Bass–Connell–Wright (1982) showed JC reduces to maps of the form $F = (X_1 + H_1, \ldots, X_n + H_n)$ with each $H_i$ homogeneous cubic or zero. Drużkowski further reduced to *cubic linear type* ($H_i$ cubes of linear forms). de Bondt–van den Essen and Drużkowski independently reduced to the symmetric-Jacobian subcase. These reductions introduce additional variables and are themselves equivalent-strength unless the reduced case is actually proved — a reduction to an unproved case is zero progress |
| Formal power-series inverses | A formal inverse always exists by the inverse function theorem when $\det J_F \in \mathbb{C}^\times$; the open question is whether it has *finite* degree, i.e. is polynomial. Bass–Connell–Wright (1982) developed the formal inverse expansion precisely to study this; the formal expansion is the tool, not the conclusion |
| Local analytic inverses | Local analytic invertibility is automatic from $\det J_F \in \mathbb{C}^\times$ via the holomorphic inverse function theorem; the global polynomial inverse is the actual claim |
| Injectivity assumptions | The statement "nonzero constant Jacobian implies injectivity" is a reformulation equivalent to JC (the injectivity reformulation; see van den Essen's *Polynomial Automorphisms and the Jacobian Conjecture* for the equivalence). Keller's 1939 paper is the *original formulation* of the conjecture, not the injectivity reformulation; assuming injectivity is therefore assuming the conjecture, not a lemma |
| Birationality assumptions | Keller (1939) already proved the *birational* case ($\mathbb{K}(X) = \mathbb{K}(F)$). Campbell (complex case), Razar, and independently Wright proved the further subcase where $\mathbb{K}(X)$ is a Galois extension of $\mathbb{K}(F)$. Birationality plus the Jacobian condition does not by itself force polynomial invertibility without further work equivalent to JC |
| Reductions to another unproved conjecture | The Dixmier conjecture (every endomorphism of the Weyl algebra is an automorphism) *implies* JC (Bass–Connell–Wright 1982); the converse holds only in the form "JC in $2N$ variables implies Dixmier in $N$ dimensions" (Tsuchimoto; Belov-Kanel–Kontsevich). Citing Dixmier as a lemma is citing a *strictly stronger* unproved statement, which is a reduction, not a proof |
| Computational verification through any fixed dimension or degree | Finite verification does not imply the parametric statement; Connell–van den Dries showed that if JC is false, a counterexample exists with integer coefficients and Jacobian determinant 1, so any finite search that does not find it is merely inconclusive up to that bound |
| Candidate counterexamples without a complete noninvertibility proof | A map with $\det J_F \in \mathbb{C}^\times$ that is *suspected* non-invertible is not a counterexample without a rigorous no-polynomial-inverse argument; ruling out inverses up to some degree $d$ is not ruling out all degrees |

### Adversarial checklist for affirmative proofs

- **Formal vs. polynomial inverse.** The inverse function theorem gives a
  formal power-series inverse; that is *not* a polynomial inverse. Check that
  the proof terminates the degree-growth argument, not just the formal one.
- **Local vs. global invertibility.** Local analytic invertibility is automatic;
  the claim is global polynomial invertibility. Check that "invertible at every
  point" was not silently promoted to "globally invertible."
- **Analytic vs. algebraic arguments.** Analytic arguments (holomorphic,
  étale-local) must be backed by an algebraic conclusion; check that no
  analytic theorem was used where its algebraic conclusion was asserted but not
  derived.
- **Hidden injectivity or surjectivity assumptions.** "Since $\det J_F$ is a
  nonzero constant, $F$ is injective" is a reformulation *equivalent* to JC
  (the injectivity reformulation; see e.g. van den Essen's *Polynomial
  Automorphisms and the Jacobian Conjecture*). Any proof relying on injectivity
  is circular unless it proves injectivity from scratch. Keller's 1939 paper
  is the original formulation of the conjecture itself, not a reduction from
  it — do not cite "Keller" as if it were a separate lemma.
- **Characteristic-zero dependence.** All objects are over $\mathbb{C}$; check
  that no positive-characteristic theorem was imported without justification,
  and that a step valid only in characteristic $p$ was not used to conclude in
  characteristic zero.
- **Degree bounds.** A degree bound on a hypothetical inverse must be
  *derived*, not assumed; check that "degree of $G$ is bounded by …" is
  proved, not postulated.
- **Denominators introduced by inversion.** A rational inverse with
  denominators that happen to cancel on $\mathbb{C}^n$ does not become
  polynomial unless the cancellation is proved; check that no denominator was
  hand-waved away.
- **Unjustified convergence claims.** Formal series convergence is not the
  issue — the series is *always* a formal inverse — but any claim that the
  series truncates must be proved, not asserted.
- **Nonreversible reductions.** A reduction $P \Rightarrow Q$ where $Q$ is
  equivalent to JC is fine; a reduction where $Q$ is *strictly weaker* and is
  what was proved is goal substitution. Check the direction of every reduction.
- **Circular use of equivalent statements.** JC has several equivalent forms
  (the injectivity reformulation; the birational-with-Jacobian-condition case
  after Keller's 1939 birational proof; the cubic homogeneous reduction of
  Bass–Connell–Wright, which is equivalent-strength because it introduces
  variables). Check that the proof does not rely on one of them as a lemma
  without flagging the equivalence. The Dixmier conjecture is *not* equivalent:
  it strictly implies JC, so citing it is citing a stronger unproved
  statement.

### Adversarial checklist for counterexamples

- **Exact Jacobian determinant computation.** The $\det J_F \in \mathbb{C}^\times$
  claim must be an exact symbolic computation, not a numerical evaluation of a
  matrix with floating entries.
- **Hidden polynomial inverses.** A map that looks non-invertible may admit a
  non-obvious polynomial inverse; check against the full automorphism group,
  not just triangular maps.
- **Birational inverses.** A polynomial inverse implies a rational inverse
  (polynomial invertibility $\Rightarrow$ birationality). So exhibiting a
  rational inverse does *not* prove polynomial invertibility — the inverse
  must be polynomial, not merely rational. Conversely, proving "no rational
  inverse" *would* suffice to prove "no polynomial inverse" (contrapositive),
  but the harder and more common direction is proving noninvertibility for a
  map that *is* birational yet has no polynomial inverse.
- **Coordinate changes that reveal a hidden inverse.** Invertibility is
  invariant under automorphism: $F$ is invertible iff $\phi \circ F \circ \psi$
  is, for automorphisms $\phi, \psi$ of $\mathbb{C}^n$. The trap is the *opposite*
  of trivialization: a map that looks non-invertible in the chosen coordinates
  may admit a non-obvious polynomial inverse visible only after an
  automorphism. Check against the full automorphism group, not just triangular
  or affine coordinate changes.
- **Numerical artifacts.** A near-singular Jacobian is not a singular Jacobian;
  $\det J_F$ must be *exactly* a nonzero constant, not approximately one.
- **Characteristic-$p$ phenomena mistakenly imported into $\mathbb{C}$.** The
  naive analogue of JC *fails* in positive characteristic even in one variable:
  over a field of characteristic $p > 0$, the map $x \mapsto x - x^p$ has
  derivative $1 - px^{p-1} = 1$ (since $px = 0$) but has no inverse. So
  non-invertible maps with constant nonzero Jacobian exist in characteristic
  $p$, and a counterexample found over $\overline{\mathbb{F}_p}$ does *not*
  lift to $\mathbb{C}$. The transfer goes the other way: Connell–van den Dries
  proved that if JC is false in characteristic zero, a counterexample exists
  with integer coefficients and Jacobian determinant 1, so JC is true for all
  char-0 fields or for none. A proof that imports a positive-characteristic
  counterexample as evidence over $\mathbb{C}$ is therefore a characteristic
  error.
- **Incomplete noninvertibility arguments.** "No inverse of degree $\leq d$"
  for any fixed $d$ is not "no polynomial inverse"; the noninvertibility
  argument must rule out *all* degrees.

### What this prompt adds beyond the CDC template

1. **Bidirectional acceptance.** Unlike CDC (affirmative-only), the Jacobian
   prompt allows either a complete proof *or* a complete explicit
   counterexample, with a stated completeness contract for each. The
   dispatch side must keep both routes alive — the portfolio is genuinely
   two-sided.
2. **Reduction-equivalence trap named for the specific problem.** The
   injectivity reformulation of JC and the Bass–Connell–Wright cubic
   homogeneous reduction are JC-equivalent forms (the reduction introduces
   variables, so it is equivalent-strength, not a genuine simplification);
   the prompt names them so audit agents flag any proof that uses one as a
   lemma. Note the asymmetry with Dixmier: the Dixmier conjecture *strictly
   implies* JC, so citing it is citing a stronger unproved statement — a
   different failure mode from the equivalent-form trap.
3. **Formal-vs-polynomial inverse trap named explicitly.** The Jacobian
   Conjecture is uniquely prone to the "formal inverse exists, therefore
   polynomial inverse exists" slide (the formal power-series inverse always
   exists by the inverse function theorem when $\det J_F \in \mathbb{C}^\times$;
   the open question is whether it truncates). The prompt names it as a
   specific audit target.
4. **Characteristic-$p$ contamination.** The CDC prompt has no
   field-characteristic trap; the Jacobian prompt does, because JC is
   *false* in positive characteristic (the one-variable map $x \mapsto x - x^p$
   has Jacobian $1$ and no inverse), and positive-characteristic
   counterexamples do *not* transfer to $\mathbb{C}$. The transfer runs the
   other way: Connell–van den Dries showed char-0 truth is all-or-nothing via
   the integer-coefficient counterexample reduction. This is a
   problem-specific audit target that does not generalize — and, as it turned
   out, the actual counterexample (Alpöge, July 2026) lives in characteristic
   zero, not via transfer.

## References

Citations for the historical note and the distilled rules. Bibliographic data
from Wikipedia's *Jacobian conjecture* article reference list (accessed
2026-07-20). The verbatim prompt section has no citations — it is the source
PDF itself.

- Keller, Ott-Heinrich (1939). "Ganze Cremona-Transformationen".
  *Monatshefte für Mathematik und Physik* 47 (1): 299–306.
  doi:[10.1007/BF01695502](https://doi.org/10.1007%2FBF01695502). — Original
  formulation of the conjecture; proof of the birational case.
- Wang, Stuart Sui-Sheng (August 1980). "A Jacobian criterion for
  separability". *Journal of Algebra* 65 (2): 453–494.
  doi:[10.1016/0021-8693(80)90233-1](https://doi.org/10.1016%2F0021-8693%2880%2990233-1).
  — JC for polynomials of degree 2 (any dimension).
- Campbell, L. Andrew (1973). "A condition for a polynomial map to be
  invertible". *Mathematische Annalen* 205 (3): 243–248.
  doi:[10.1007/bf01349234](https://doi.org/10.1007%2Fbf01349234). — Galois-
  extension subcase of the birational case, complex maps.
- Razar, Michael (1979). "Polynomial maps with constant Jacobian". *Israel
  Journal of Mathematics* 32 (2–3): 97–106.
  doi:[10.1007/bf02764906](https://doi.org/10.1007%2Fbf02764906). — Galois-
  extension subcase, general case.
- Wright, David (1981). "On the Jacobian conjecture". *Illinois Journal of
  Mathematics* 25 (3): 423–440.
  doi:[10.1215/ijm/1256047158](https://doi.org/10.1215%2Fijm%2F1256047158).
  — Galois-extension subcase, independent of Razar.
- Bass, Hyman; Connell, Edwin H.; Wright, David (1982). "The Jacobian
  conjecture: Reduction of degree and formal expansion of the inverse".
  *Bulletin of the American Mathematical Society* 7 (2): 287–330.
  doi:[10.1090/S0273-0979-1982-15032-7](https://doi.org/10.1090%2FS0273-0979-1982-15032-7).
  [PDF](https://projecteuclid.org/journals/bulletin-of-the-american-mathematical-society-new-series/volume-7/issue-2/The-Jacobian-conjecture--Reduction-of-degree-and-formal-expansion/bams/1183549636.pdf).
  — Cubic homogeneous reduction; formal inverse expansion; Dixmier ⇒ JC.
- Drużkowski, Ludwik M. (1983). "An effective approach to Keller's Jacobian
  conjecture". *Mathematische Annalen* 264 (3): 303–313.
  doi:[10.1007/bf01459126](https://doi.org/10.1007%2Fbf01459126). — Reduction
  to cubic linear type ($H_i$ cubes of linear forms).
- Moh, Tzuong-Tsieng (1983). "On the Jacobian conjecture and the
  configurations of roots". *Journal für die reine und angewandte
  Mathematik* 1983 (340): 140–212.
  doi:[10.1515/crll.1983.340.140](https://doi.org/10.1515%2Fcrll.1983.340.140).
  — JC checked for degree $\leq 100$ in two variables.
- Connell, Edwin; van den Dries, Lou (1983). "Injective polynomial maps and
  the Jacobian conjecture". *Journal of Pure and Applied Algebra* 28 (3):
  235–239. doi:[10.1016/0022-4049(83)90094-4](https://doi.org/10.1016%2F0022-4049%2883%2990094-4).
  — If JC is false, a counterexample exists with integer coefficients and
  Jacobian determinant 1; char-0 all-or-nothing.
- de Bondt, Michiel; van den Essen, Arno (2005). "A reduction of the Jacobian
  conjecture to the symmetric case". *Proceedings of the American
  Mathematical Society* 133 (8): 2201–2205.
  doi:[10.1090/S0002-9939-05-07570-2](https://doi.org/10.1090%2FS0002-9939-05-07570-2).
  — Reduction to symmetric-Jacobian subcase.
- Drużkowski, Ludwik M. (2005). "The Jacobian conjecture: symmetric reduction
  and solution in the symmetric cubic linear case". *Annales Polonici
  Mathematici* 87: 83–92.
  doi:[10.4064/ap87-0-7](https://doi.org/10.4064%2Fap87-0-7). — Symmetric
  reduction, independent of de Bondt–van den Essen; symmetric cubic linear
  case solved.
- Tsuchimoto, Yoshifumi (2005). "Endomorphisms of Weyl algebra and
  $p$-curvatures". *Osaka Journal of Mathematics* 42 (2): 435–452. — JC in
  $2N$ variables ⇒ Dixmier in $N$ dimensions.
- Belov-Kanel, Alexei; Kontsevich, Maxim (2007). "The Jacobian conjecture is
  stably equivalent to the Dixmier conjecture". *Moscow Mathematical Journal*
  7 (2): 209–218. arXiv:[math/0512171](https://arxiv.org/abs/math/0512171).
  doi:[10.17323/1609-4514-2007-7-2-209-218](https://doi.org/10.17323%2F1609-4514-2007-7-2-209-218).
  — Independent proof of JC-$2N$ ⇒ Dixmier-$N$.
- Adjamagbo, Pascal Kossivi; van den Essen, Arno (2007). "A proof of the
  equivalence of the Dixmier, Jacobian and Poisson conjectures". *Acta
  Mathematica Vietnamica* 32: 205–214.
  [PDF](http://journals.math.ac.vn/acta/pdf/0702205.pdf). — Equivalence of
  Dixmier, Jacobian, and Poisson conjectures.
- van den Essen, Arno (1997). "Polynomial automorphisms and the Jacobian
  conjecture" (PDF). *Sémin. Congr.* vol. 2. Soc. Math. France. pp. 55–81.
  MR[1601194](https://mathscinet.ams.org/mathscinet-getitem?mr=1601194).
  — Survey cited for the injectivity reformulation equivalence.
- Alpöge, Levent (July 20, 2026). "hello there the jacobian conjecture is
  false" (Tweet). X.
  [https://x.com/__alpoge__/status/2079028340955197566](https://x.com/__alpoge__/status/2079028340955197566).
  — The counterexample post.
- Sparkes, Matthew (July 20, 2026). "AI's solution to 87-year-old riddle
  takes mathematicians by surprise". *New Scientist*.
  [https://www.newscientist.com/article/2580374-ais-solution-to-87-year-old-riddle-takes-mathematicians-by-surprise/](https://www.newscientist.com/article/2580374-ais-solution-to-87-year-old-riddle-takes-mathematicians-by-surprise/).
  — Press coverage of the counterexample.
- Rodríguez Díaz, Lázaro Orlando (2026). "On the origin of the Jacobian
  conjecture". *Comptes Rendus. Mathématique* 364 (G2): 363–370.
  doi:[10.5802/crmath.831](https://doi.org/10.5802/crmath.831).
  arXiv:[2512.23614](https://arxiv.org/abs/2512.23614). — Historical origin
  study of the conjecture.

### Source access log

- Wikipedia, *Jacobian conjecture*, accessed 2026-07-20:
  https://en.wikipedia.org/wiki/Jacobian_conjecture — primary source for all
  attributions, reductions, and the counterexample report.
- Wikipedia, *Dixmier conjecture*, accessed 2026-07-20:
  https://en.wikipedia.org/wiki/Dixmier_conjecture — Dixmier ⇒ JC direction.
- Wikipedia, *Ott-Heinrich Keller*, accessed 2026-07-20:
  https://en.wikipedia.org/wiki/Ott-Heinrich_Keller — Keller 1939 attribution.
- Alpöge tweet, fetched 2026-07-20:
  https://x.com/__alpoge__/status/2079028340955197566 — counterexample text.
- Source PDF (this extraction): https://aaronlou.com/jacobian_counterexample_prompt.pdf