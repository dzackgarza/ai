# Worked Example: the Rank-Four Counterexample

The concrete program every rule in
[[mathematical-research/SKILL|mathematical-research]] was distilled from. Read it to
calibrate register: the working objects are Hopf algebras over Artin local rings,
socle classes, and power words — not "functions" and "test cases." Source:
`github.com/j2d9w5xtjn-png/GrothendieckRankP2`.

## The question

Grothendieck asked whether a finite locally free group scheme of order $n$ is killed
by $n$. Deligne proved it for commutative group schemes; Oort–Tate settles prime
order; so rank $4 = 2^2$ with a noncommutative group law is the first open case.
Attribution required primary-source care: the printed 1970 SGA 3 statement and the
annotated re-edition carry different commutativity hypotheses — the program verified
which question it was answering before claiming to answer it
([[mathematical-research/references/program-shape|program-shape]]).

## The object

Over the base ring (length 9, characteristic exactly 4, residue field $\mathbf F_2$)

$$R=\mathbf Z[a,b]/(a^3,\;b^3,\;a^2b+2),$$

take the rank-four algebra $A=R[U,V]/(U^2-abU+b^2V,\;V^2-a^2V)$ — two nested monic
quadratic extensions, so freeness of rank $4=2\cdot2$ is structural. With
$\lambda=(1+aU)(1+bV)$, the comultiplication is skew-primitive against a group-like:

$$\Delta(U)=U\otimes1+\lambda\otimes U,\qquad
  \Delta(V)=V\otimes\lambda+1\otimes V,\qquad
  \Delta(\lambda)=\lambda\otimes\lambda.$$

## The decisive calculation

The $n$-th power word acts on coordinates through geometric sums:

$$[n]^\#(U)=(1+\lambda+\cdots+\lambda^{n-1})\,U.$$

Here $\lambda^2=1+2bV$ and $\lambda^4=1$, giving

$$[4]^\#(U)=2b\,UV\neq0,\qquad [8]^\#=\iota\varepsilon,
\qquad S=[7]^\#\ \text{(antipode as the \(n{-}1\) power word)}.$$

So $G=\operatorname{Spec}A$ has order four, is killed by eight, and is not killed by
four. Everything reduces to one exact statement: **$2b\neq0$ in $R$** — the socle
class survives. That single nonvanishing was certified three independent ways
([[mathematical-research/references/adversarial-audit|adversarial-audit]]): an M2
strong Gröbner basis over $\mathbf Z$ leaving $2s$ in nonzero normal form, an
explicit 512-element model $\mathbf Z/4\times\mathbf Z/4\times(\mathbf Z/2)^5$ of the
regular representation, and Lean's `two_b_ne_zero` through that witness module
([[mathematical-research/references/computer-algebra-patterns|computer-algebra-patterns]]).

The phenomenon is a mixed-characteristic carry: mod 2 the obstruction dies (the
equal-characteristic control run shows all nine target coordinates become members of
the ideal; in mixed characteristic exactly two survive). This is the concrete
instance behind the rule "the phenomenon may live in the terms your simplification
discards" ([[mathematical-research/references/computation|computation]]).

## The wall that preceded it

Before the counterexample, theory compressed the whole problem to one module. With
$q=[2]^\#$, $D=[4]^\#-\iota\varepsilon$, $\delta$ the regular-translation
determinant, and $J=((\mathrm{Id}-S)(A))$:

$$D=(1+\delta)(q-e),\qquad 2(1+\delta)J=0,\qquad (1+\delta)J^2=0,
\qquad\text{so}\qquad [4]=e\iff(1+\delta)J=0.$$

The exponent-8 theorem ("every rank-four group scheme over any base is killed by 8")
fits on one page — trace/determinant identities $c_2=2\chi-1-\delta$,
$q(\chi)=\chi^2-2c_2=2(1+\delta)$, then $ac=-4a$ forces $2D=qD=0$, hence
$[8]^\#=q^3=e$. That page is what a
[[mathematical-research/references/handoff|handoff]] "one-page proof sketch of the
headline result" looks like: re-derivable without opening any other file.

## The discovery chronology (what actually worked)

1. Exhaustive stratified UNSAT sweeps over residue-$\mathbf F_2$ bases of length
   $\le7$ closed hundreds of cases — and found nothing. Their real product was a
   trustworthy frontier, and theorems (block rigidity, Torti specialization) kept
   retiring whole strata mid-flight.
2. A universal mixed-characteristic chart around the fiber $\alpha_2^2$: length-632
   base, Hilbert function $(1,15,107,509)$. Exact filtered elimination modulo
   $\mathfrak q^4$ showed two fourth-power target coordinates survive, certified by
   dual nonmembership functionals.
3. Instead of deleting presentation variables ad hoc, the search was **dualized**:
   choose a cubic functional annihilating all cubic relations and nonzero on a
   target, then minimize a semantic invariant — catalecticant rank — over the
   admissible dual space. Rank dropped $7\to4$, realized by the inverse system
   $\mathcal G=X^{[2]}Z+XYD+YD^{[2]}+Z^{[3]}$; its apolar algebra is a length-10
   Gorenstein base with Hilbert function $(1,4,4,1)$.
4. The found object was re-verified by exact arithmetic in the explicit 1024-element
   ring; the 632-dimensional chart was demoted to history
   ([[mathematical-research/references/computation|computation]], truth sources).
5. Simplification was then its own research phase: length $10\to9$, then a
   human-scale presentation from the affine group, each round re-audited, the
   length-10 model archived (not deleted) for its extra subgroup/deformation
   content.

## Real ledger rows

From the frozen `CLAIM_LEDGER.tsv`, showing the status vocabulary doing real work
([[mathematical-research/references/claim-status|claim-status]]):

| id | claim | status | caveat |
|---|---|---|---|
| C2 | Rank-four groups are killed by 8 | `proved_independently_audited` | group law may be noncommutative |
| C5 | Deformations of $\alpha_2\rtimes\mu_2$ are killed by 4 | `literature_theorem_plus_checked_specialization` | the paper prints a false stronger killed-by-2 claim; [4] checked directly |
| C10 | $H=(1,2,2,1)$ type-two frontier complete | `bounded_computational_theorem` | 160 UNSAT + 30 vacuous rows, 510 audited logs |
| C12 | Principal length-seven frontier | `inconclusive_partial` | 12 closed / 2 vacuous / 5 unknown / 41 incomplete at freeze |
| C16 | A rank-four counterexample was found | `false` *(at the 07-10 freeze)* | no SAT candidate survived |

C16 flipped to true the same evening by the chart route — the frozen row was
correct *about its evidence*, which is exactly why frozen counts carry "rerun the
auditor before quoting" warnings.

## Register traps, each observed in this program

- $[n]$ is the $n$-th power **word** on a possibly noncommutative group scheme, not
  a homomorphism; $[4]^\#=(\mu\circ\Delta)^{\circ2}$ needs coassociativity and
  $\Delta$-multiplicativity, not commutativity of $G$.
- $G$ has sixteen rank-two subgroups **over $R$** — the count changes under base
  extension; a subgroup chain is not a normal filtration (none is normal: a rank-two
  normal subgroup would force $[4]=e$).
- $A^\vee$ is a noncommutative algebra: $\operatorname{Spec}(A^\vee)$ is not a
  Cartier dual; a module filtration of the $\mathrm{GL}_3$ embedding is not a
  subgroup filtration.
- Length-10 minimality inside the audited cubic chart is `solver_conditional` (an
  unreplayed Z3 UNSAT); global minimality at lengths 7–9 was a separately tracked
  open row. The two claims never merged.
- Presentations of "the same" object differ across artifacts ($\mathbf Z[a,b]$ vs
  $(\mathbf Z/4)[x,y]$ charts, differently-normalized quadrics): never transfer a
  coefficient formula between presentations without re-deriving it — a handoff
  checklist item after a near-miss.
