# Properties and structure (`STR-*`)


## `STR-1`: Use the forgetful functor

For a specified forgetful functor $U\colon\mathcal S\to\mathcal C$, full
faithfulness gives at most property, faithfulness gives at most structure, and
an arbitrary functor gives at most stuff. Repleteness is a separate condition
when an essential image is replaced by a full subcategory. Property language is
used only when each homotopy fiber of $U$ is empty or a contractible groupoid;
otherwise name the chosen structured object over $X$.

## `STR-2`: Name every chosen structure

A structure on $X$ is a chosen object in the fiber over $X$ of a specified
forgetful functor. When several choices exist, name the one used by the
construction. For example, for a commutative ring $R$, tensor product and
direct sum give the different monoidal structures $(R\text{-}\mathbf{Mod},
\otimes_R,R)$ and $(R\text{-}\mathbf{Mod},\oplus,0)$. Over a noncommutative
ring, state the bimodule, left-module, or right-module setting. A ring is a
group under addition, not under multiplication.

## `STR-3`: State every hypothesis

A theorem states every object property, characteristic restriction, limit
assumption, flatness assumption, and equality of named morphisms used in its
conclusion. If a construction uses a basis, embedding, section, presentation,
or other witness, name that witness in the construction.

## `STR-4`: Strict equality versus specified natural equivalence for a factorization

A factorization is described as "an equality $F=G\circ H$ or a specified
natural isomorphism $F\Rightarrow G\circ H$" as alternatives, conflating a
property (strict equality, which does not exist under an
$\infty$-categorical default where $\mathbf{Cat}:=\mathbf{Cat}_\infty$, as in
a document that adopts DEF-13)
with extra structure (a specified $2$-cell). In $\mathbf{Cat}_\infty$ a
factorization is always a tuple $(H,G,\alpha)$ with $\alpha$ a specified
natural equivalence.

**Banned:** "together with an equality $F=G\circ H$ or a specified natural
isomorphism $F\Rightarrow G\circ H$."

**Preferred:** "together with a specified natural equivalence
$\alpha\colon F\simeq G\circ H$." If the $1$-categorical strict case is
meant, state it as the truncation "$F=G\circ H$ on the nose, i.e.
$\alpha=\operatorname{id}$ in $\mathbf{Cat}_1$," not as an alternative to
the $\infty$-categorical structure.
