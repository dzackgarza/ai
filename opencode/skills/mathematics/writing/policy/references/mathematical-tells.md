# Mathematical tells (`MA-*`)

Colloquial or reinvented parlance in place of the standard notion, or of the
definition the document already fixes. The remediation is the established
definition — cite it.

## `MA-1`: Prior substitution for the document's definition

An agent writes the definition it recalls from training or an external source
without reading the document's defining occurrence.

**Banned:** writing $a=b$ after the document has constructed only an isomorphism
$a\cong b$; calling a map a "classifier" without the universal property
required at its defining occurrence.

**Preferred:** read and cite the document's anchor. If that definition conflicts
with the literature, correct it at the defining occurrence and repair its
dependents; do not shadow it locally.

## `MA-2`: Coinage for a standard notion

A private word stands in for a notion with a standard name.

**Banned:** "cut" / "axiom cut" (→ full subcategory defined by a property, or
specified forgetful functor); "refinement" for a subcategory (→ full
subcategory); "least common category" (→ a greatest lower bound in the
specified preorder of categories, if it exists).

**Banned:** "blow-up point" for a pole; "wrap number" for the winding number;
"the value space of $M$" when the object is an $R$-module $W$.

**Preferred:** the standard term or the document's term: "pole"; "winding
number"; "Let $b\colon M\otimes_R M\to W$ be a $W$-valued bilinear form."

A private coinage, a colloquial term ("apex" for the vertex of a cone,
"carries", "identifies conventions"), or a confabulated term that sounds
technical but has no referent makes readers guess whether a new object was
introduced, and hides the details it stands for. Use the standard term and
link its defining occurrence (`XREF-5`). If the document has no definition of
the notion, add one. Define a genuinely new term before its first use.

## `MA-3`: Notation colliding with a standard meaning

A symbol is reused against its near-universal reading.

**Banned:** "$\mathbf{Sh}_\Sigma$" for a diagram/functor category ("$\mathbf{Sh}$"
is sheaves).

**Preferred:** a non-colliding symbol ("$\mathbf{Dia}_\Sigma$"), or the plain
construction ($\operatorname{Fun}(\Sigma, \mathcal C)$).

## `MA-4`: Elegant variation

The same object is renamed sentence to sentence to avoid repetition, so one
notion acquires several names.

**Preferred:** repeat the exact term. Notation retains its typed meaning
throughout the document.

## `MA-5`: Borrowed technical term without a definition

A word that carries a specific technical meaning (character, spectrum, kernel,
index, module, classified by) is used loosely to describe something that has
a different, standard name. A mathematician reads it as the technical term
and finds no matching definition — the word signals precision and delivers
none.

**Banned:** "the character of an axiom" (read as a group/representation
character; no such notion is defined); "the bilinear map classified by
$\mu$" (classified by means a classifying object represents a functor;
the correspondence is the tensor-hom adjunction).

**Preferred:** state the actual correspondence or property. "The bilinear
map $A\times A\to A$ corresponding to $\mu$ under the tensor-hom
adjunction." Use the standard name for the standard notion.

## `MA-6`: Cardinality label for an incidental count

Naming a structure by how many things it has — "trichotomy", "dichotomy", "the
three-fold", "$N$-fold" — asserts the count is mathematically load-bearing.

**Banned:** "the stuff / structure / property trichotomy" — nothing turns on
"three"; the classification is by fullness and faithfulness and, in higher
categories, by the truncation level of the homotopy fibers.

**Preferred:** name the classification by content, not by tally.

## `MA-7`: Backwards or premature notation

A symbol is introduced with `:=` pointing from the standard, primitive
notation to the coinage, or coined notation is used before it is defined.

**Banned:** "$E_A := B_A.A$" before either notation has a defining occurrence.

**Preferred:** first specify the family $p_A\colon E_A\to B_A$ and the map
$\chi\colon\mathcal C\to B_A$, then draw their pullback. Only afterward
introduce the shorthand, with `:=` pointing from the new symbol to the defined
expression. In general, define each object before any shorthand for it.

## `MA-8`: Compressed notation where the diagram is owed

A pullback written as the apex $A \times_C B$, or a universal family named only
by its classifying map $S \to M$, in place of the cartesian square that
records the projections and the universal property.

**Banned:** "the family is the base change $S \times_M U$"; "$S \to M$
classifies the family" as the whole of it.

**Preferred:** draw the square with both legs and the corner mark,
and use fiber-product notation only as a named shorthand for the apex once its
square is drawn. Where the house allows it, the square may be reached
through the linked definition of the fiber product: "the fiber is the
fiber product $X\times_Y 1$", with that definition linked. The reader
must reach both legs and the universal property; the apex alone gives
neither.

## `MA-9`: Colloquial "ownership" for a mathematical relation

"owns", "owned at", and "ownership" replace the relation that should be
stated.

**Banned:** "commutativity is owned at $\mathbf{Mag}$"; "the node that owns
the property"; "the object owns its local invariants".

**Preferred:** name the relation — "commutativity is a property of magmas",
"the category whose objects satisfy the property", "the invariants are
defined on the object".

## `MA-10`: Classifier language without a universal property

"classifier", "classifying category", and "universal family" are used as
labels before a representing or universal property is stated.

**Banned:** "$u_A\colon E_A\to B_A$ is the axiom classifier" with no
description of the objects it classifies or the equivalence it represents.

**Preferred:** state the property or structure directly. If a classifying
object or fibration exists, state its universal property and call a change
along a functor the pullback family.

## `MA-11`: An arrow without a typed map

A diagram connects mathematical nouns because they are related in the author's
head, without naming a functor, natural transformation, or map having the
displayed source and target.

**Banned:** an object-to-category edge for membership; a discriminant arrow
from the full lattice category when the construction is functorial only on its
core; an unlabeled edge whose direction could mean either inclusion or
forgetting structure.

**Preferred:** write the actual source, target, and arrow label. Replace
membership by prose, restrict a construction to its stated domain, and display
a set-valued invariant as a map from $\pi_0$.

## `MA-12`: Named maps referred to by count

Standard maps with standard names — the associator $\alpha$, the left unitor
$\lambda$, the right unitor $\varrho$ — are referred to as "the three
isomorphisms" or "the $n$ maps" instead of by name. The reader must infer
which maps from context.

**Banned:** "the three isomorphisms being the unique ones commuting with the
projections."

**Preferred:** "the associator $\alpha_{a,b,c}$ and the unitors
$\lambda_a$, $\varrho_a$." Name the maps. The count carries no mathematical
information.

## `MA-13`: A structure described pointwise instead of as a structure

A functor is a functor: source, target, name. A natural transformation is a
natural transformation: its components and the naturality square. A monoidal
structure is a tuple $(\mathcal{C}, \otimes, \mathbf{1}, \alpha, \lambda,
\varrho)$ with axioms. Each of these is a mathematical object with a type and
constituent data. A pointwise description — "a choice of $a \otimes b$ for
every $a$, $b$" — replaces the structure with a recipe for its output on
inputs, the way a programmer describes a function by what it returns. State
the structure; its pointwise behavior may follow.

**Banned:** "choose a product $a \times b$ for each pair of objects and set
$\otimes = \times$."

**Preferred:** "the product functor
$\times\colon\mathcal{C}\times\mathcal{C}\to\mathcal{C}$, together with a
terminal object $\mathbf{1}$ and the canonical associator and unitors,
defines a monoidal structure on $\mathcal{C}$."

## `MA-14`: Map out of a product called bilinear versus map out of the tensor product

A bilinear map is presented as a set map $b\colon M\times M\to W$ that
"is $A$-bilinear" in prose, instead of as a morphism
$b\colon M\otimes_A M\to W$ out of the tensor product. The product
$M\times M$ and the prose qualifier "bilinear" bloat the statement: they
introduce the underlying-set product, then add the $A$-bilinearity
conditions in English, instead of using the object that represents
bilinear maps. The tensor product is the representing object:
$\operatorname{Hom}(M\otimes_A M,W)\cong\operatorname{Bilin}_A(M\times
M,W)$ is the universal property that makes bilinearity precise. State the
tensor product and the morphism out of it.

**Banned:** "Let $W$ be an $A$-module and let $b\colon M\times M\to W$ be
$A$-bilinear." — $M$ is unbound, $M\times M$ is the set product, and
"$A$-bilinear" is a prose qualifier for the linearity conditions.

**Preferred:** "Let $M,W\in\mathbf{LMod}_A$ and
$b\colon M\otimes_A M\to W$ in $\mathbf{LMod}_A$" (or
$b\colon M\otimes_A^L M\to W$ for the derived product). The single
morphism out of the tensor product replaces the map out of the product
plus the English "bilinear."

## `MA-15`: Prose to avoid defining the annihilator

A paragraph of English — "every element is annihilated by a nonzero
element of $R$," "multiplication by every nonzero element of $R$ is
injective" — is used to avoid defining the annihilator ideal. The ideal
is the standard algebraic object; defining it once makes every later
torsion statement precise and short. Define the ideal.

Concrete standard: for $R$ an integral domain (discrete) and
$m\in M\in\mathbf{LMod}_R$, put
$\operatorname{Ann}_R(m):=\{r\in R\mid r\cdot m=0\}\trianglelefteq R$.
Then $M$ is torsion if $\operatorname{Ann}_R(m)\neq0$ for every $m\in M$
($\forall m\,\exists\,0\neq r$ with $r\cdot m=0$), torsion-free if
$\operatorname{Ann}_R(m)=0$ for $m\neq0$, equivalently
$r\cdot\colon M\to M$ injective for $0\neq r\in R$.

**Banned:** "M is torsion when every element is annihilated by a nonzero
element of $R$, and torsion-free when multiplication by every nonzero
element of $R$ is injective" — two English paragraphs with per-element
quantifiers hidden in prose.

**Preferred:** define $\operatorname{Ann}_R(m)$ once, then "$M$ is
torsion if $\operatorname{Ann}_R(m)\neq0$ for every $m\in M$;
torsion-free if $\operatorname{Ann}_R(m)=0$ for $m\neq0$."
