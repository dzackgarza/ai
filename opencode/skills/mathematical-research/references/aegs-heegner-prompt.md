# KSBA Compactification of the Coble Heegner Divisor in $F_{\mathrm{En},2}$

A one-shot mathematical problem statement for a long-horizon remote worker, after the
template of [[mathematical-research/references/cdc-prompt|cdc-prompt]] and
[[mathematical-research/references/jacobian-prompt|jacobian-prompt]] (verbatim prompt
sections only). Parent: [[mathematical-research/SKILL|mathematical-research]].

## Verbatim prompt

> **Current task statement**
>
> **Objects and notation.** Fix the ground field $\mathbb C$.
>
> An *Enriques surface* is a smooth projective surface $Z$ with $K_Z\neq 0$,
> $2K_Z=0$, and $q=p_g=0$. A *degree-2 numerical polarization* on $Z$ is a nef line
> bundle $L_Z$ with $L_Z^2=2$ and $h^0(L_Z)\ge 3$ that is not linearly equivalent to a
> sum of two effective divisors. The coarse moduli space of smooth degree-2
> numerically polarized Enriques surfaces is
>
> $$\mathcal F_{\mathrm{En},2}=\mathbb D(T_{\mathrm{En}})/\Gamma_{\mathrm{En},2},$$
>
> where $T_{\mathrm{En}}\simeq U\oplus E_8(2)$ is the Enriques transcendental lattice,
> $\mathbb D$ is the associated type-IV period domain, and $\Gamma_{\mathrm{En},2}$ is
> the degree-2 arithmetic group. Write
> $\mathcal F_{\mathrm{En}}=\mathbb D(T_{\mathrm{En}})/\Gamma_{\mathrm{En}}$ for the
> unpolarized Enriques period quotient.
>
> The ambient K3 involution space
>
> $$\mathcal F_{(2,2,0)}=\mathbb D(T_{\mathrm{dP}})/\Gamma_{\mathrm{dP}},\qquad
> T_{\mathrm{dP}}\simeq U(2)\oplus\langle-2\rangle\oplus E_8(2),$$
>
> is the coarse moduli space of K3 surfaces with nonsymplectic involution and ADE
> singularities. The period-domain inclusion $T_{\mathrm{En}}\hookrightarrow
> T_{\mathrm{dP}}$ induces a finite map $\mathcal F_{\mathrm{En},2}\to\mathcal
> F_{(2,2,0)}$; the image is the Noether–Lefschetz locus imposing the additional
> $E_8(2)$ algebraic lattice. Write $\mathcal F_4$ for the degree-4 K3 involution
> quotient that appears as the second ambient space in the parent paper's diagrams.
>
> A *Coble surface* is a rational $S_2$-surface $V$ that arises as the quotient of a
> nodal K3 surface by an involution fixing the node. It carries a single
> $\frac{(1,1)}{4}$-singularity, i.e. a cyclic quotient singularity of index $4$,
> locally $\mathbb C^2/\mu_4$ with $\mu_4$ acting by $\mathrm{diag}(i,i)$. The minimal
> resolution of $V$ is a rational surface.
>
> The Baily–Borel compactification $\mathcal F_{\mathrm{En},2}^{\mathrm{BB}}$ has five
> 0-cusps (primitive isotropic lines) and nine 1-cusps (primitive isotropic planes).
> Each 0-cusp is a folding of one of two ambient K3 Coxeter diagrams by the Enriques
> involution.
>
> **KSBA stable pairs.** Let $B=\sum_i b_iB_i$ be an effective boundary with rational
> coefficients $0<b_i\le 1$. A projective variety $X$ is *deminormal* if it is $S_2$
> and normal crossing in codimension $1$. The pair $(X,B)$ has *semi-log-canonical*
> (slc) singularities if $K_X+B$ is $\mathbb Q$-Cartier and the normalization
> $(\bar X,\bar B+\bar D)$ is klt, where $\bar D$ is the conductor. For Enriques
> surfaces, the ramification divisor $R_Z$ (the fixed locus of the Enriques involution
> lifted to the K3 cover) is ample and serves as the stable polarization. The KSBA
> moduli space of stable pairs $(Z,\epsilon R_Z)$ with $0<\epsilon\ll 1$ and fixed
> $R_Z^2$ is a projective Deligne–Mumford stack with projective coarse moduli space.
>
> **The Heegner divisor.** There is a unique $\Gamma_{\mathrm{En}}$-orbit of
> $(-2)$-vectors $\alpha\in T_{\mathrm{En}}$. The associated hyperplane
>
> $$\Delta_2=\alpha^\perp\cap\mathcal F_{\mathrm{En},2}$$
>
> is a Heegner divisor in $\mathcal F_{\mathrm{En},2}$. It parameterizes degree-2
> numerically polarized Coble surfaces. Away from $\Delta_2$, the moduli space
> parameterizes genuine Enriques surfaces. The unpolarized Heegner divisor
> $\Delta=\alpha^\perp\cap\mathcal F_{\mathrm{En}}$ parameterizes Coble surfaces
> without the degree-2 polarization data.
>
> **The parent theorem (Alexeev–Engel–Garza–Schaffler, Theorem 5.9).** The
> normalization of $\overline{\mathcal F}_{\mathrm{En},2}^{\mathrm{KSBA}}$ — the
> closure of $\mathcal F_{\mathrm{En},2}$ in the KSBA moduli space of stable pairs
> $(Z,\epsilon R_Z)$ — is the semitoroidal compactification of $\mathcal
> F_{\mathrm{En},2}$ for the collection of semifans $\{\mathfrak F^k\}_{k=1,\dots,5}$.
> It is toroidal over 0-cusps $2$ and $4$, the 1-cusps adjacent to them, and 1-cusp
> $35$; strictly semitoroidal over the remaining cusps.
>
> **The problem.** Let $\overline{\Delta_2}^{\,\mathrm{KSBA}}$ denote the closure of
> $\Delta_2$ in the KSBA moduli space of stable pairs, taken inside the ambient KSBA
> compactification of the parent theorem.
>
> Resolve completely the KSBA compactification theorem for $\Delta_2$:
>
> Identify the normalization of $\overline{\Delta_2}^{\,\mathrm{KSBA}}$ as an explicit
> semitoroidal compactification of $\Delta_2$, with the toroidal-vs-strictly-
> semitoroidal locus determined cusp-by-cusp.
>
> A complete resolution must give the exact semifans and the exact
> toroidal-vs-strictly-semitoroidal locus, and must prove that the identified
> semitoroidal compactification is the normalization of
> $\overline{\Delta_2}^{\,\mathrm{KSBA}}$.
>
> Much as the parent paper answers, for $\mathcal F_{\mathrm{En},2}$, the questions
> "what are the cusps, what are the Coxeter diagrams, what are the semifans, what is
> the dlt model at each cusp, and what is the resulting semitoroidal compactification,"
> a positive solution to this problem should answer the analogous questions for
> $\Delta_2$. These are downstream consequences of the proof: a proof that correctly
> identifies the semitoroidal normalization of $\overline{\Delta_2}^{\,\mathrm{KSBA}}$
> must, as a consequence, be able to produce the following data. Phrased negatively,
> a proof that cannot produce this data is incomplete, regardless of whether the
> headline semitoroidal identification is argued, because the objects the theorem is
> about ($T_{\mathrm{Co}}$, $\Gamma_{\mathrm{Co}}$, $\Gamma_{\mathrm{Co},2}$, $R_V$,
> the Coxeter diagrams, the integral-affine structures, the semifans) are left
> unspecified and the theorem therefore has no content.
>
> 1. **Explicit Coble surfaces from $\mathbb P^1\times\mathbb P^1$.** Give an explicit
>    construction of the Coble surfaces in $\Delta_2$ by varying curves in
>    $\mathbb P^1\times\mathbb P^1$ (the model used in the parent paper's projective
>    diagram). State exactly which curves, in which linear system, produce Coble
>    surfaces with their $\frac{(1,1)}{4}$-singularity, and how variation of those
>    curves covers the Heegner divisor.
>
> 2. **The Coble transcendental lattice $T_{\mathrm{Co}}$.** Define
>    $T_{\mathrm{Co}}$ as the transcendental lattice obtained by the Coble
>    construction above. Give the explicit lattice (signature, rank, discriminant
>    form, and a decomposition into standard summands if one exists). Define the
>    period domain $\mathbb D_{T_{\mathrm{Co}}}$ and the unpolarized Coble period
>    quotient $\mathcal F_{\mathrm{Co}}=\mathbb D(T_{\mathrm{Co}})/\Gamma_{\mathrm{Co}}$
>    for the correct arithmetic group $\Gamma_{\mathrm{Co}}$ (state exactly which
>    group this is — the stabilizer of $T_{\mathrm{Co}}$ in the appropriate
>    overgroup, or whatever the correct definition is).
>
> 3. **The degree-2 Coble polarization.** Coble surfaces in $\Delta_2$ inherit a
>    natural degree-2 quasipolarization. Determine whether this quasipolarization is
>    in fact a polarization. Define the arithmetic group $\Gamma_{\mathrm{Co},2}$ for
>    the polarized Coble moduli and the polarized period quotient
>    $\mathcal F_{\mathrm{Co},2}=\mathbb D(T_{\mathrm{Co}})/\Gamma_{\mathrm{Co},2}$.
>    Clarify the relation between $\mathcal F_{\mathrm{Co}}$,
>    $\mathcal F_{\mathrm{Co},2}$, $\mathcal F_{\mathrm{En}}$, and
>    $\mathcal F_{\mathrm{En},2}$: which maps are finite, which are embeddings, which
>    are Noether–Lefschetz loci, and how they fit into a commutative diagram with
>    $\mathcal F_{(2,2,0)}$ and $\mathcal F_4$.
>
> 4. **The canonical system $|-2K_V|$.** For a Coble surface $V$ in $\Delta_2$,
>    describe $|-2K_V|$ explicitly. In particular, if
>    $|-2K_V|=\{C=C_1+\dots+C_n\}$ is reducible, give $n$ and the configuration of
>    the components $C_i$ (their genera, self-intersections, and intersection graph).
>    This divisor is the candidate for the stable polarization $R_V$ on the Coble
>    side; the description must be concrete enough to support the KSBA-pair
>    definition in subproblem 8.
>
> 5. **Cusp incidence for $\mathcal F_{\mathrm{Co}}$ and $\mathcal F_{\mathrm{Co},2}$.**
>    Give the 0-cusp and 1-cusp incidence diagrams for the Baily–Borel
>    compactifications of $\mathcal F_{\mathrm{Co}}$ and $\mathcal F_{\mathrm{Co},2}$.
>    For each cusp, give the isotropic sublattice of $T_{\mathrm{Co}}$ that defines
>    it and state whether the cusp survives under the maps to $\mathcal F_{\mathrm{En}}$
>    and $\mathcal F_{\mathrm{En},2}$.
>
> 6. **Coxeter diagrams at the 0-cusps.** For each 0-cusp of $\mathcal
>    F_{\mathrm{Co}}$ and $\mathcal F_{\mathrm{Co},2}$, give the relevant Coxeter
>    diagram (the reflection chamber for the cusp lattice, in the sense of Vinberg's
>    theory as used in the parent paper's §3). State exactly how each Coble Coxeter
>    diagram is obtained from the corresponding Enriques Coxeter diagram, and how it
>    relates to the ambient K3 Coxeter diagram. Identify whether the passage is a
>    "folding" of root lattices in the same sense as the Enriques involution fold of
>    the K3 diagram, a direct folding from K3 to Coble, or some other process. If it
>    is a folding, give the explicit fold map on simple-root labels.
>
> 7. **Parabolic and elliptic subdiagrams.** For each 0-cusp and 1-cusp of $\mathcal
>    F_{\mathrm{Co},2}$, identify the parabolic subdiagrams (giving Type II boundary
>    rays) and the elliptic subdiagrams (giving Type III boundary cones) of the
>    Coble Coxeter diagram. State how each relates to the corresponding parabolic
>    and elliptic subdiagrams for $\mathcal F_{\mathrm{En},2}$ and for the ambient K3
>    spaces $\mathcal F_{(2,2,0)}$ and $\mathcal F_4$.
>
> 8. **The KSBA space for Coble pairs.** Identify the KSBA moduli space that is the
>    target of the analogy with the parent theorem. Explicitly, the stable pairs are
>    $(V,\epsilon R_V)$ for some divisor $R_V$ on the Coble surface $V$; state what
>    $R_V$ is. If $R_V$ is the restriction of $R_Z$ from the Enriques side, prove it.
>    If $R_V$ is $|-2K_V|$, or a component thereof, or the pullback of $B$ through
>    the projective diagram, prove it. The choice of $R_V$ must be the one for which
>    the slc condition holds for the $\frac{(1,1)}{4}$-singularity at
>    $0<\epsilon\ll 1$ and for which the stable-pair moduli problem is well-posed.
>
> 9. **Integral-affine structures and dlt models.** For each 0-cusp and 1-cusp of
>    $\mathcal F_{\mathrm{Co},2}$, describe the integral-affine structure on the dual
>    complex of the Coble degeneration (the analogue of the parent paper's §4
>    integral-affine spheres and disks). Give the construction of the corresponding
>    dlt models for Coble degenerations. Where the parent paper's examples (e.g.
>    Examples 4.13–4.16, 6.3, 6.4, 6.6, 7.1) can be modified or generalized to the
>    Coble locus, show the modification explicitly and verify it reproduces the
>    claimed dlt model.
>
> 10. **The semifans.** Give the semifans for the semitoroidal compactification of
>     $\mathcal F_{\mathrm{Co},2}$ whose normalization is identified with
>     $\overline{\Delta_2}^{\,\mathrm{KSBA}}$. For each cusp of $\mathcal
>     F_{\mathrm{Co},2}$, state whether the semifan is a fan (toroidal locus) or a
>     genuine semifan (strictly semitoroidal locus). State how each Coble semifan
>     relates to the Enriques semifan $\mathfrak F^k$ of the parent theorem at the
>     corresponding cusp and to the ambient K3 ramification semifan
>     $\mathfrak F_{\mathrm{ram}}$.
>
> A proof that cannot answer any one of these ten questions is incomplete, regardless
> of whether the headline semitoroidal identification is argued. The questions are
> simultaneously (i) the specification of the objects the theorem is about, (ii) the
> downstream consequences a positive proof must enable, and (iii) the negative
> completeness gate: a proof that leaves $T_{\mathrm{Co}}$, $\Gamma_{\mathrm{Co}}$,
> $\Gamma_{\mathrm{Co},2}$, $R_V$, the Coxeter diagrams, the integral-affine
> structures, or the semifans unspecified has not identified what is being
> compactified or what the compactification is.
>
> **Computational evidence.** Back up any claim that a specific lattice, Coxeter
> diagram, cusp incidence, integral-affine structure, or semifan is what the problem
> states it is, with concrete symbolic computations and general reproducible scripts.
> Acceptable forms of evidence:
>
> - A symbolic computation (SageMath, Macaulay2, or equivalent) verifying the claimed
>   lattice invariants (signature, discriminant form, isomorphism type) of
>   $T_{\mathrm{Co}}$.
> - A script reproducing the cusp incidence diagram for $\mathcal F_{\mathrm{Co}}$
>   and $\mathcal F_{\mathrm{Co},2}$ from the lattice $T_{\mathrm{Co}}$ and the
>   arithmetic groups $\Gamma_{\mathrm{Co}}$, $\Gamma_{\mathrm{Co},2}$.
> - A script verifying, for each 0-cusp, that the claimed Coble Coxeter diagram is
>   the correct Vinberg chamber for the cusp lattice.
> - A script verifying the claimed fold map on simple-root labels, when the passage
>   to the Coble Coxeter diagram is a folding.
> - Concrete worked examples (e.g. a specific Coble surface from a specific curve in
>   $\mathbb P^1\times\mathbb P^1$, with its $|-2K_V|$ decomposition and its
>   degeneration at a specific cusp) where the claimed dlt model and semifan can be
>   asserted to hold by inspection.
>
> Any general-purpose, reusable code written for this evidence should be kept and
> included in the submission, with a clear statement of what it verifies and how to
> run it. Computational evidence is *supporting* evidence; it does not substitute for
> proof of the parametric statement.
>
> **Insufficiency catalog.** Partial progress does not count unless it implies exactly
> the resolution above. In particular, the following are insufficient:
>
> - Identifying $\overline{\Delta_2}^{\,\mathrm{KSBA}}$ only as *a* compactification of
>   $\Delta_2$ without identifying its normalization as semitoroidal.
> - Citing the parent theorem as a black box for $\Delta_2$. The restriction of a
>   semitoroidal compactification to a Heegner divisor is not in general the
>   semitoroidal compactification of the Heegner divisor; the restriction step
>   requires its own proof.
> - Producing a compactification of Coble surfaces by a separate moduli problem (e.g.
>   Garza's complete moduli of Coble surfaces) without proving that moduli problem is
>   the same as $\overline{\Delta_2}^{\,\mathrm{KSBA}}$: same objects, same
>   polarization, same stability condition, same boundary.
> - Producing a Kulikov or dlt model for Coble degenerations without identifying the
>   KSBA stable model (the relative $\operatorname{Proj}$ for $R_V$) and its
>   normalization.
> - Verifying the theorem only for a proper subset of the 0-cusps of $\mathcal
>   F_{\mathrm{Co},2}$, or only for the toroidal cusps, or only for the strictly
>   semitoroidal cusps.
> - Verifying the theorem only for the Type III (0-cusp) strata, or only for the Type
>   II (1-cusp) strata.
> - Identifying cusp intersections without identifying the semifans.
> - Identifying the semifans without proving they are the normalization of
>   $\overline{\Delta_2}^{\,\mathrm{KSBA}}$.
> - Proving the headline semitoroidal identification while leaving $T_{\mathrm{Co}}$,
>   $\Gamma_{\mathrm{Co}}$, $\Gamma_{\mathrm{Co},2}$, $R_V$, or the Coxeter diagrams
>   unspecified or defined only up to isomorphism without the explicit summand
>   decomposition, fold map, or divisor construction the subproblems require.
> - Defining $T_{\mathrm{Co}}$ only as "the transcendental lattice of a Coble surface"
>   without the explicit construction from subproblem 2.
> - Stating that the degree-2 Coble quasipolarization "is" a polarization without
>   proving it (subproblem 3 requires a determination, not an assumption).
> - Describing $|-2K_V|$ generically (e.g. "it is reducible") without the value of
>   $n$, the component configuration, and the intersection graph (subproblem 4
>   requires all three).
> - Producing Coxeter diagrams for $\mathcal F_{\mathrm{Co},2}$'s cusps without
>   identifying the passage from the Enriques (or K3) Coxeter diagrams, and without
>   identifying whether the passage is a folding, a direct construction, or some
>   other process (subproblem 6 requires all three).
> - Claiming a semifan is a fan (toroidal locus) or a genuine semifan (strictly
>   semitoroidal locus) without justifying the classification cusp-by-cusp
>   (subproblem 10 requires the classification and the relation to the Enriques and
>   K3 semifans).
> - Computational verification for finitely many monodromy vectors, finitely many
>   curves in $\mathbb P^1\times\mathbb P^1$, or finitely many cusps, without a
>   parametric argument covering the whole moduli space.
> - Scripts that verify a lattice invariant or a Coxeter-diagram computation without
>   a clear statement of what they verify, how to run them, and how the output
>   supports the claimed theorem. Code without a verification contract is not
>   computational evidence.
> - Computing the cusp incidence diagram of the BB compactification by working only in
>   $O(A_{T_{\mathrm{Co}}})$, without solving the lifting problem from
>   $O(A)$-orbits to $\Gamma_{\mathrm{Co},2}$-orbits of isotropic subspaces. This is
>   insufficient even if the $O(A)$-orbit computation is correct, because the lift is
>   not unique.
> - Defining $\Gamma_{\mathrm{Co},2}$ by fiat (e.g. as "the group for which the
>   semifans are the KSBA normalization"). This is circular and makes the theorem
>   trivially true; the group must be shown to be naturally induced by the Enriques
>   constructions or computed as the actual monodromy group of the polarized Coble
>   families.
> - Declaring a map between cusps of BB compactifications without exhibiting the
>   mechanism (lattice inclusion, isometry, monodromy) that produces it and proving it
>   is the unique lift. A declared permutation of cusp maps without this argument is
>   insufficient because equally valid permutations exist.
> - Assuming without proof that Coble surfaces smooth to Enriques surfaces. Only the
>   smoothing of the K3 cover is known a priori; the smoothing of the Coble quotient is
>   a separate claim requiring a separate argument (the node-fixing involution may not
>   extend over a smoothing).
> - Choosing the divisor $R_V$ individually for each Coble surface, without defining it
>   on the universal family and without proving compatibility with the divisors chosen
>   for $\mathcal F_{\mathrm{En},2}$, $\mathcal F_{(2,2,0)}$, and $\mathcal F_4$. An
>   $R_V$ not compatible with the Enriques and K3 divisors does not define a moduli
>   problem comparable to the parent theorem's.
> - Declaring $(V,\epsilon R_V)$ KSBA stable without proving $R_V$ is ample and
>   $\mathbb Q$-Cartier and the pair has slc singularities at the
>   $\frac{(1,1)}{4}$-singularity for $0<\epsilon\ll 1$.
> - A synthetic formulation that bypasses $\mathcal F_{\mathrm{En},2}$ and embeds
>   $\mathcal F_{\mathrm{Co},2}\to\mathcal F_{(2,2,0)}$ directly without re-proving
>   the parent theorems (recognizable divisor, cusp classification, finiteness,
>   semitoroidal identification) and without proving the construction factors through
>   the $\mathcal F_{\mathrm{En},2}$ constructions. A direct construction that does not
>   factor through the Enriques locus is a different theorem.
> - Curve computations in $\mathbb P^1\times\mathbb P^1$ asserted as conclusions
>   about the corresponding Coble surface, its K3 cover, or its Enriques quotient,
>   without the cover-and-quotient argument. No amount of curve reasoning alone proves
>   the Coble quotient has a $\frac{(1,1)}{4}$-singularity.
> - A list of roots in $e_i^\perp\!/\mathbb Z e_i$ asserted as the Coxeter diagram at a
>   cusp, without argument for the necessity, sufficiency, and simplicity of the root
>   system (typically via Vinberg's algorithm or a classification citation). A bare
>   list is a false Coxeter diagram.
> - A list of maximal parabolic subdiagrams asserted as the Type II boundary rays
>   without theory or computation showing the list is exhausted.
> - An argument that "these two vectors are in the same $O(A)$-orbit, therefore they
>   are in the same $\Gamma_{\mathrm{Co},2}$-orbit," without solving the lifting
>   problem. An orbit under $O(T_{\mathrm{Co}})$, $O^+(T_{\mathrm{Co}})$,
>   $\Gamma_{\mathrm{Co},2}$, or $O(A_{T_{\mathrm{Co}}})$ may split into multiple
>   orbits under any other of these groups, and passing between them requires
>   analyzing the relevant exact sequence or cokernel.
> - A candidate counterexample to the stated theorem without a complete proof that the
>   KSBA normalization is not semitoroidal for the stated semifans.
>
> **Adversarial checklist.** Every candidate proof must be checked for the following
> confusions:
>
> - **Coble surface $\neq$ Enriques surface.** A Coble surface is a rational
>   $S_2$-quotient of a nodal K3 by a node-fixing involution, carrying a
>   $\frac{(1,1)}{4}$-singularity. It is not an Enriques surface: its minimal
>   resolution is rational, so $K$ is not torsion. The slc stability condition for
>   Coble pairs uses a different canonical class than the Enriques condition.
>
> - **Restriction $\neq$ compactification of the restriction.** The parent theorem's
>   semifan $\mathfrak F^k$ is a semifan on the dual complex of the K3 degeneration at
>   cusp $k$. Its restriction to $\Delta_2$ is a fan on the dual complex of the Coble
>   degeneration at cusp $k$ only if the cones of $\mathfrak F^k$ that meet
>   $\Delta_2$'s intersection with cusp $k$ form a fan on the restricted dual complex.
>   The slide "the restriction of a semitoroidal compactification to a Heegner divisor
>   is the semitoroidal compactification of the Heegner divisor" is false in general.
>
> - **Node-fixing involution in families.** The Heegner divisor parameterizes
>   quotients by a node-fixing involution. In a family, the node may smooth, the
>   involution may fail to extend, or the node-fixing property may be lost at the
>   boundary.
>
> - **The $\frac{(1,1)}{4}$-singularity is not ADE.** It is a cyclic quotient
>   singularity of index $4$. The slc condition for $\frac{1}{r}(1,1)$-type
>   singularities on surfaces interacts with the boundary coefficient $\epsilon$.
>
> - **Two Heegner divisors in the same moduli space.** $\mathcal F_{\mathrm{En},2}$
>   contains two distinct Heegner divisors: the Coble divisor ($(-2)$-vector $\alpha$,
>   $\frac{(1,1)}{4}$-singularity, the target of this problem) and the unigonal
>   divisor ($(-4)$-vector $\beta$ with $\beta^\perp\simeq\langle 4\rangle\oplus
>   U\oplus E_8(2)$, $\mathbb P(1,1,2)$ double cover, §2.2 of the parent paper). Do
>   not confuse them.
>
> - **The folding construction specializes non-trivially.** Each 0-cusp of $\mathcal
>   F_{\mathrm{En},2}$ is a fold of an ambient K3 Coxeter diagram. The hyperplane
>   $\alpha^\perp$ cuts each folded diagram in a way that depends on the cusp.
>
> - **The dlt model is not the stable model.** The dlt or half-divisor quotient is an
>   intermediate object. The KSBA stable model is the relative $\operatorname{Proj}$
>   for the restricted ramification divisor.
>
> - **Normality $\neq$ irreducibility.** A stable Coble surface can be irreducible and
>   nonnormal: the $\frac{(1,1)}{4}$-singularity is an $S_2$-but-not-$R_1$ point, and
>   boundary self-gluings can produce irreducible nonnormal limits.
>
> - **Quasipolarization vs. polarization.** Subproblem 3 requires determining whether
>   the inherited degree-2 Coble quasipolarization is a polarization. These are not
>   the same: a quasipolarization is nef and big but may fail to be ample (it may
>   contract curves). The arithmetic group $\Gamma_{\mathrm{Co},2}$ and the period
>   quotient $\mathcal F_{\mathrm{Co},2}$ depend on which one it is. Check that the
>   determination is proved, not assumed, and that the moduli problem uses the
>   correct one.
>
> - **$\mathbb P^1\times\mathbb P^1$ model is the parent paper's model.** Subproblem 1
>   asks for the construction by varying curves in $\mathbb P^1\times\mathbb P^1$.
>   This is the model in the parent paper's §2.1 projective diagram (the quartic
>   del Pezzo double cover). Do not substitute a different projective model (e.g. the
>   $\mathbb P(1,1,2)$ unigonal model, which is the *other* Heegner divisor) without
>   explaining the change and proving it produces the same Coble surfaces.
>
> - **The canonical system $|-2K_V|$ is not the ramification divisor $R_Z$.** On an
>   Enriques surface, $R_Z$ is the fixed locus of the involution and is ample. On a
>   Coble surface, $|-2K_V|$ is a canonical-system object on a rational surface; it
>   is a candidate for $R_V$ but is not automatically the same divisor. Subproblem 8
>   requires proving the identification, not assuming it.
>
> - **Folding from Enriques vs. folding from K3.** The parent paper folds the K3
>   Coxeter diagram by the Enriques involution to get the Enriques Coxeter diagram.
>   The Coble Coxeter diagram could in principle be obtained by folding the Enriques
>   diagram further (Enriques $\to$ Coble) or by a different fold of the K3 diagram
>   directly (K3 $\to$ Coble). Subproblem 6 requires determining which, and giving
>   the explicit fold map on simple-root labels in either case.
>
> - **Cusp incidence in $\mathcal F_{\mathrm{Co},2}$ vs. $\mathcal F_{\mathrm{En},2}$.**
>   A cusp of $\mathcal F_{\mathrm{Co},2}$ maps to a cusp of $\mathcal
>   F_{\mathrm{En},2}$ under the inclusion, but not every cusp of $\mathcal
>   F_{\mathrm{En},2}$ is met by $\Delta_2$, and a cusp of $\mathcal F_{\mathrm{Co},2}$
>   may map to a lower-dimensional stratum of a cusp of $\mathcal F_{\mathrm{En},2}$.
>   Check the incidence diagram in both directions.
>
> - **Computational evidence vs. proof.** Subproblem evidence (lattice invariants,
>   Coxeter diagrams, fold maps, dlt examples) supports the claims but does not
>   substitute for proof of the parametric statement. A script that verifies a
>   lattice invariant for one choice of $T_{\mathrm{Co}}$ does not prove
>   $T_{\mathrm{Co}}$ is the correct transcendental lattice for the Coble
>   construction; the correctness proof is separate.
>
> - **Cusp incidence requires solving a lifting problem for orbits of isotropic
>   subspaces.** The cusp incidence diagram of the Baily–Borel compactification cannot
>   be computed by working only in $O(A_{T_{\mathrm{Co}}})$ (the orthogonal group of the
>   discriminant form). There is a lifting problem: orbits of isotropic subspaces in
>   the discriminant group do not in general lift uniquely to orbits of isotropic
>   subspaces in $T_{\mathrm{Co}}$. A proof using this technique must be at least as
>   explicit as Sterk's arguments in *Compactifications of the period space of Enriques
>   surfaces. II* for the cusps of $\mathcal F_{\mathrm{En},2}$: the lifting from
>   $O(A)$-orbits to $\Gamma$-orbits must be solved, not assumed.
>
> - **$\Gamma_{\mathrm{Co},2}$ cannot be defined by fiat.** A by-fiat definition of the
>   arithmetic group can be used to make the theorem trivially true (define
>   $\Gamma_{\mathrm{Co},2}$ to be exactly the group for which the semifans work). The
>   group must instead be shown to be either (i) naturally induced by the Enriques
>   constructions — i.e. the stabilizer of the relevant sublattice data inside
>   $\Gamma_{\mathrm{En},2}$ or $\Gamma_{\mathrm{dP}}$, with the stabilizer computed
>   explicitly — or (ii) computed from first principles as the actual monodromy group
>   of the relevant families of polarized Coble surfaces. Defining the group as the
>   answer to the theorem is circular.
>
> - **Maps between cusps of Baily–Borel compactifications require a lifting argument.**
>   A map between cusps of BB compactifications (and thus between their cusp diagrams)
>   cannot be declared without proof. By the theory of Baily–Borel (BB66), the lift of a
>   holomorphic map between arithmetic quotients, when it exists, is unique — but its
>   existence is not automatic, and there are equally valid candidate permutations of
>   cusp maps that one could declare. A proof must exhibit the exact mechanism
>   producing the cusp map (e.g. an inclusion of lattices, an isometry, a monodromy
>   computation) and show it is the unique lift; declaring a permutation without this
>   argument violates the uniqueness of lifting.
>
> - **Coble surfaces do not smooth to Enriques surfaces without proof.** It is known a
>   priori only that the K3 cover smooths to a family of K3 surfaces with involution,
>   whose quotients are Enriques surfaces. It does not follow automatically that the
>   Coble surfaces (the singular quotients at the Heegner divisor) smooth to Enriques
>   surfaces in the family — the smoothing of the quotient is a separate question from
>   the smoothing of the cover, and the node-fixing involution may not extend over a
>   smoothing. A proof that relies on Coble-to-Enriques smoothing must prove it; it
>   cannot assume it.
>
> - **The stable pair $(V,\epsilon R_V)$ cannot be chosen arbitrarily.** The divisor
>   $R_V$ must be chosen on the universal family, just as $R_Z$ is chosen on the
>   universal K3 family in the Enriques and K3 cases. It must be compatible with the
>   induced or restricted divisors chosen for $\mathcal F_{\mathrm{En},2}$,
>   $\mathcal F_{(2,2,0)}$, and $\mathcal F_4$ (the degree-4 polarized K3 space). A
>   proof that picks an $R_V$ for each Coble surface individually, with no
>   universal-family or compatibility argument, has not defined a moduli problem.
>
> - **KSBA stability of $(V,\epsilon R_V)$ must be proved, not assumed.** The pair
>   $(V,\epsilon R_V)$ is KSBA stable only if $R_V$ is ample and $\mathbb Q$-Cartier and
>   the pair has semi-log-canonical singularities (the standard KSBA condition). The
>   $\frac{(1,1)}{4}$-singularity is not automatically slc at $0<\epsilon\ll 1$; the slc
>   condition must be verified for the specific singularity and the specific
>   $\epsilon$-range. A proof that declares $(V,\epsilon R_V)$ stable without these
>   checks has not shown the moduli problem is well-posed.
>
> - **A synthetic formulation bypassing $\mathcal F_{\mathrm{En},2}$ must reprove the
>   parent theorems.** An alternative approach embeds $\mathcal F_{\mathrm{Co},2}\to
>   \mathcal F_{(2,2,0)}$ directly (e.g. by treating $T_{\mathrm{Co}}$ as an abstract
>   lattice and arguing directly about its period domain), bypassing the
>   $\mathcal F_{\mathrm{En},2}$ construction. This is a legitimate strategy, but it
>   requires re-proving versions of the theorems AEGS25 proves for the Enriques locus:
>   the recognizable-divisor theorem, the cusp classification, the finiteness of the
>   classifying map, and the semitoroidal identification. Furthermore, the resulting
>   construction must commute with and factor through the $\mathcal F_{\mathrm{En},2}$
>   constructions to be correct; a direct construction that does not factor through the
>   Enriques locus is a different theorem, not a proof of this one.
>
> - **Curve computations do not transfer to surface claims without argument.**
>   Computations about a curve in $\mathbb P^1\times\mathbb P^1$ (e.g. a $(4,4)$-curve)
>   do not, without additional argument, prove anything about the corresponding Coble
>   quotient of the covering K3 surface. The cover construction, the involution, the
>   quotient, and the singularity analysis must each be argued. No amount of reasoning
>   about the curve alone proves the Coble quotient has a $\frac{(1,1)}{4}$-singularity;
>   that conclusion requires the full cover-and-quotient argument.
>
> - **Coxeter diagram assertions require simple-system verification.** At a cusp
>   associated to an isotropic vector $e_i$, the relevant Coxeter diagram is the
>   reflection chamber for $e_i^\perp\!/\mathbb Z e_i$ in the hyperbolic lattice
>   $e_i^\perp\!/\mathbb Z e_i$. Producing a list of roots in this lattice and asserting
>   they form the Coxeter diagram is insufficient: one must show (i) the listed roots
>   form a simple system (linearly independent, pairwise inner products in $\{0,-1,-2,
>   \dots\}$, every other positive root a nonnegative combination), (ii) the system is
>   *necessary* (these roots are actually reflections in the cusp lattice), and (iii)
>   *sufficient* (the system generates the full reflection group, or the relevant
>   finite-index subgroup). This is typically done by Vinberg's algorithm or by an
>   indirect argument from the classification of reflective hyperbolic lattices. A list
>   of roots with no argument for necessity, sufficiency, and simplicity is a false
>   Coxeter diagram.
>
> - **Maximal parabolic subdiagrams cannot be listed as assertions.** Identifying the
>   maximal parabolic subdiagrams of a Coxeter diagram (giving the Type II rays) by
>   inspection is a common mistake. One must appeal to theory (e.g. Vinberg's
>   classification, or a computation) to show the set of maximal parabolic subdiagrams is
>   *exhausted* — otherwise the listed subdiagrams may be a proper subset of the actual
>   Type II rays, and the boundary structure of the semitoroidal compactification is
>   incomplete.
>
> - **Do not conflate orbits under $O(T_{\mathrm{Co}})$, $O^+(T_{\mathrm{Co}})$,
>   $\Gamma_{\mathrm{Co},2}$, and $O(A_{T_{\mathrm{Co}}})$.** These are four different
>   groups, and an orbit under one may split into multiple orbits under another. The
>   standard technique (as in Sterk) for passing between orbits is to show that the
>   subgroup $E(T_{\mathrm{Co}})$ of Eichler transvections is contained in the smaller
>   group, but even then, passing between the orbits of any two of these groups
>   typically requires analyzing an exact sequence or the cokernel of an inclusion. A
>   proof that argues "these two vectors are in the same $O(A)$-orbit, therefore they
>   are in the same $\Gamma_{\mathrm{Co},2}$-orbit" without solving the lifting problem
>   is incorrect. There is no guarantee that an orbit under $G_1$ does not split into
>   multiple orbits under $G_2 \subset G_1$, for any of the above $G_i$.
>
> **Termination.** Return only when a complete proof survives adversarial audit
> against the full checklist. Do not return a reduction, partial result, isolated
> missing lemma, "best effort" summary, or explanation of why the problem is
> difficult.
>
> **Contamination hygiene.** Public search may be used only for ordinary mathematical
> background or standard named theorems (KSBA stability, semitoroidal compactifications,
> recognizable divisors, Vinberg reflection theory, Looijenga's compactification
> theory, Coble surface geometry). Do not search for a solution to this exact problem
> or for a published proof of it. Do not answer that the problem is open.