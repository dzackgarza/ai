# @override on Sage Category Methods — Solutions Discussion

## The Problem

Sage’s category framework uses metaclass-driven method injection.
Categories define `ParentMethods`, `ElementMethods`, and `MorphismMethods` as inner
classes. At runtime, when categories are joined (e.g., `FinitePosets` joins `Posets` and
`FiniteSets`), the metaclass merges these method surfaces into the concrete object.
A method defined in `FinitePosets.ParentMethods` genuinely overrides one from
`Posets.ParentMethods` — but through metaclass assembly, not Python class inheritance.

Code in `category_specs/` decorates these methods with `@override`. At runtime (Python
3.12+), `@override` is enforced — if the method doesn’t actually override anything,
Python raises `TypeError` at class definition time.
This works correctly because the metaclass has already assembled the method resolution
at that point.

Mypy cannot see this.
It sees `ParentMethods` as a standalone class with no base class defining the overridden
method. It reports:

```
error: Method "is_finite" is marked as an override,
but no base method was found with this name  [misc]
```

~300 of these across the `category_specs/` tree.

## Why Explicit Inheritance Is Wrong (Option B Rejected)

The proposal to make `ParentMethods` explicitly inherit from a supercategory’s
`ParentMethods`:

```python
class ParentMethods(Sets.ParentMethods):  # NO
    @override
    def is_finite(self) -> bool: ...
```

This is architecturally incorrect for a fundamental reason: **a new branching
subcategory tree must not need to know about any supercategory methods.**

Sage is open source.
Any random contributor can add a new subcategory.
If the convention says “inherit from the right parent’s `ParentMethods`,” then every new
contributor must:

- Know which parent to inherit from (non-obvious in diamond hierarchies)

- Know that this convention exists at all (it’s not a Sage convention — it’s a
  repo-local hack)

- Remember to do it on every new `ParentMethods` class

One forgotten inheritance, and the static checking silently breaks.
The methods still work at runtime (Sage’s metaclass doesn’t care about Python
inheritance on `ParentMethods`), but mypy stops verifying `@override`. Drift accumulates
with no signal.

Worse: methods that reference `self.base_ring()` etc.
start working in mypy for classes that DID inherit, but fail silently for classes that
didn’t. The result is a fractured static-analysis surface where some categories get full
checking and others get none, and the difference is invisible to contributors.

This is the wrong model.
The right model is: Sage’s category resolution machinery *knows* what the ancestor
methods are. Make the tooling ask Sage, not require every contributor to manually
re-declare the relationship.

## Option A: Suppress with `# type: ignore[misc]` (Fallback, Not Solution)

Add `# type: ignore[misc]` to every `@override` line that mypy can’t verify.

**Pros**: Preserves runtime `@override` checking.
No structural change.

**Cons**: ~300 comments across ~50+ files.
Ongoing maintenance burden.
Doesn’t solve `attr-defined` cascades (`self.base_ring()`, `self.is_finite()` etc.
still produce mypy errors because mypy doesn’t know `self`’s method surface).
This is noise suppression, not a fix.

## Option C: Mypy Plugin (The Correct Solution)

### Why It’s Simpler Than It Looks

The logic is straightforward.
The plugin doesn’t need to understand category theory or reimplement Sage’s metaclass.
It needs to do exactly one thing: **ask Sage what methods exist on ancestor categories,
then verify `@override` against that set.**

Sage already has the machinery.
Given a category class `C`:

- `C.super_categories()` returns the parent categories

- Each parent has a `ParentMethods` (or `ElementMethods`, `MorphismMethods`) inner class

- Those inner classes have methods

The plugin’s job:

1. **Detect**: When mypy encounters `class ParentMethods(...)` nested inside a class
   that is (or inherits from) a Sage category, intercept type-checking.

2. **Identify the enclosing category**: Walk up the AST or use the class’s qualified
   name. The enclosing class is the category — e.g., `_FinitePosets` nested inside
   `category_specs.sets.subcategories.finite`.

3. **Resolve ancestor methods**: Call `enclosing_class.super_categories()` at
   type-checking time (Sage must be importable; it already is in the QC environment —
   the `_sage-syntax` recipe prepases `.sage` files).
   Collect the union of all method names from all ancestor `ParentMethods` classes.

4. **Verify `@override`**: For each method in this `ParentMethods` decorated with
   `@override`, check that its name appears in the ancestor method set.
   If yes, suppress the `misc: override` error.
   If no, let the error through (it’s a real bug).

5. **Improve `self` typing** (stretch): When type-checking a method body inside
   `ParentMethods`, resolve `self` as the category’s concrete object type rather than
   the `ParentMethods` mixin.
   This fixes `attr-defined` errors on `self.base_ring()` etc.
   This is harder than step 4 but follows the same principle: ask Sage what `self`
   actually is at runtime.

### Plugin Scope

This is not a general “Sage mypy plugin” requiring deep integration with every Sage
subsystem. It is a focused plugin that:

- Hooks into mypy’s `get_base_class_hook` or `get_metaclass_hook` callback

- Makes one Sage API call (`super_categories()`) per category class

- Caches results (category hierarchies don’t change during a type-check run)

- Lives at `~/ai/quality-control/sage_category_plugin.py` or similar

- Registered via mypy config: `plugins = ["sage_category_plugin"]`

### Verification

The correctness condition is: for every `@override`-decorated method in a
`ParentMethods` class whose enclosing category is recognized, the method name MUST
appear in at least one ancestor category’s `ParentMethods`. This is exactly what
`@override` means — and exactly what Sage’s metaclass enforces at runtime.
The plugin makes mypy enforce it at type-check time too.

## Recommendation

**Primary**: Option C — mypy plugin.
This is the architecturally correct solution.
It leverages Sage’s own category resolution rather than requiring manual inheritance
declarations that drift.
Write it at `~/ai/quality-control/` as a reusable plugin, registered in the global mypy
config.

**Fallback for methods the plugin can’t resolve**: Option A — `# type: ignore[misc]` on
individual methods where the plugin hits an edge case (unimportable category, circular
dependency during type-check, etc.). This should be rare.

**Not acceptable**: Option B (explicit inheritance).
Architecturally wrong for the reasons above.
Not to be used.

* * *

## Technical Addendum: Minimal-Reinvention Implementation Path

> Appended 2026-05-10 from user-provided implementation spec.

The plugin should not reconstruct Sage’s category graph.
It should ask Sage for the dynamic classes Sage already constructed, then project their
direct base edges onto the literal source-level method-container classes.

### The Key Sage Facts

`ParentMethods` is only a container and “does not inherit from anything”; Sage builds
the actual hierarchy dynamically in `C.parent_class`, and similarly for `ElementMethods`
and `MorphismMethods`.

`C.parent_class` contains methods from `C.ParentMethods` and has bases given by the
parent classes of the supercategories of `C`; analogously, `C.element_class` uses
`ElementMethods`, and `C.morphism_class` uses `MorphismMethods`.

Sage already computes ordered supercategories using C3; `_super_categories_for_classes`
is specifically for constructing bases of `parent_class`, `element_class`, etc.

So the extraction target is:

```
Sage dynamic edge:
    C.parent_class.__bases__ contains D.parent_class

Static mypy edge to inject:
    C.ParentMethods inherits from D.ParentMethods
```

**Not**:

- recompute `C.super_categories()`

- reimplement C3

- enumerate inherited methods

- generate protocols

### Sage-Side Helper: Direct Dynamic-Base Projection

Add one tiny introspection module:

```
sage.categories.mypy_support
```

It should expose:

```python
def method_container_direct_bases(
    source_fullname: str,
) -> list[str]: ...
```

Input examples:

```
sage.categories.rings.Rings.ParentMethods
sage.categories.rings.Rings.ElementMethods
sage.categories.rings.Rings.MorphismMethods
sage.categories.objects.Objects.Homsets.ParentMethods
sage.categories.monoids.Monoids.Finite.ParentMethods
```

Output example:

```python
[
  "sage.categories.rngs.Rngs.ParentMethods",
  "sage.categories.semirings.Semirings.ParentMethods",
]
```

The algorithm:

```python
def method_container_direct_bases(source_fullname):
    module_name, qualname = split_module_and_qualname(source_fullname)
    module = importlib.import_module(module_name)

    category_path, method_kind = parse_method_container_qualname(qualname)
    # Example:
    #   "Rings.ParentMethods"
    #       category_path = ("Rings",)
    #       method_kind = "ParentMethods"
    #   "Objects.Homsets.ParentMethods"
    #       category_path = ("Objects", "Homsets")
    #       method_kind = "ParentMethods"

    C = instantiate_category(module, category_path)

    dyn_attr = {
        "ParentMethods": "parent_class",
        "ElementMethods": "element_class",
        "MorphismMethods": "morphism_class",
        "SubcategoryMethods": "subcategory_class",
    }[method_kind]

    dynamic_class = getattr(C, dyn_attr)
    dynamic_bases = dynamic_class.__bases__

    # Use Sage's own ordered categories only as a lookup table.
    # Do not recompute the graph or C3 order.
    candidates = C.all_super_categories(proper=True)
    dynamic_to_category = {
        getattr(D, dyn_attr): D
        for D in candidates
        if hasattr(D, dyn_attr)
    }

    result = []
    for B in dynamic_bases:
        D = dynamic_to_category.get(B)
        if D is None:
            continue  # object or non-category runtime base; optionally diagnose

        source_container = getattr(type(D), method_kind, None)
        if source_container is not None:
            result.append(fullname(source_container))

    return dedupe_preserving_order(result)
```

This uses `dynamic_class.__bases__`, **not** `dynamic_class.mro()`, because mypy should
be given the direct base graph and then calculate the transitive MRO itself.
Injecting the full runtime MRO as direct bases would distort the class graph.

For `SubcategoryMethods`, Sage documents `subcategory_class` as the dynamic class that
includes methods from `SubcategoryMethods` and derives from the corresponding classes of
supercategories.

### Category Instantiation Rule

Use Sage’s own representative mechanism first.
Sage has `Category.an_instance()`, and parameterized categories should overload this
default implementation to provide appropriate arguments.

So the resolver should prefer:

```python
cat = category_cls.an_instance()
```

rather than `cat = category_cls()`.

For nested category paths such as `Objects.Homsets.ParentMethods`, resolve as:

```python
cat = Objects.an_instance()
cat = cat.Homsets()
```

For axiom-style paths such as `Monoids.Finite.ParentMethods`, resolve as:

```python
cat = Monoids.an_instance()
cat = cat.Finite()
```

This avoids reconstructing axiom or functorial-construction logic.
The source path merely tells the helper which Sage method to call.

Parameterized categories remain the one unavoidable ambiguity: a source container such
as `Algebras.ParentMethods` does not determine whether the relevant runtime category is
`Algebras(QQ)`, `Algebras(ZZ)`, etc.
Sage documents that these can produce different parent/element classes depending on the
base.

Therefore the helper should support modes:

- **default**: use `category_cls.an_instance()`

- **configured**: use explicit representatives for selected classes

- **strict**: refuse unresolved parameterized categories unless configured

No parameter guessing.

### Mypy-Side Plugin Hook

Mypy’s plugin API is the intended surface: it supports plugins for frameworks whose
runtime semantics are not expressible using ordinary PEP 484 types, and
`get_customize_class_mro_hook()` exists to modify a class MRO before the class body is
analyzed.

Boilerplate shape:

```python
from mypy.plugin import Plugin, ClassDefContext

class SageCategoryPlugin(Plugin):
    def get_customize_class_mro_hook(self, fullname: str):
        if is_sage_method_container_fullname(fullname):
            return sage_method_container_mro_hook
        return None

def plugin(version: str):
    return SageCategoryPlugin
```

Configured by:

```toml
[mypy]
plugins = sage.typing.mypy_plugin
```

### Hook Callback Behavior

The hook should do only one thing: add direct Sage semantic bases to the literal
method-container class.

Pseudo-procedure:

```python
def sage_method_container_mro_hook(ctx: ClassDefContext) -> None:
    info = ctx.cls.info
    fullname = info.fullname

    base_fullnames = sage.categories.mypy_support.method_container_direct_bases(
        fullname
    )

    base_infos = []
    for base_fullname in base_fullnames:
        base_info = lookup_typeinfo(ctx, base_fullname)
        if base_info is None:
            ctx.api.defer()
            return
        base_infos.append(base_info)

    inject_base_infos(info, base_infos)
    recalculate_or_update_mro(info)
```

The injected bases should be appended after any explicit bases already written on the
method container: existing explicit bases first, then Sage semantic category-method
bases.

Reason: if a method container has an explicit non-category mixin base, mypy already sees
it, and Sage’s dynamic-class machinery separately inserts the semantic category bases.
Sage’s dynamic class documentation says dynamically constructed classes can insert
methods from a supplied class while also using the supplied bases and explicit dynamic
bases.

So conceptually:

```python
class C:
    class ParentMethods(SomeExplicitMixin):
        ...
```

becomes, for mypy only:

```python
class C:
    class ParentMethods(SomeExplicitMixin, A.ParentMethods, B.ParentMethods):
        ...
```

No method enumeration occurs.

### Dependency Handling

`get_customize_class_mro_hook()` may need ancestor TypeInfos from modules mypy has not
loaded yet. Use `get_additional_deps()` to declare those dynamic dependencies.

For each source file/module M, the plugin should ask Sage:

```python
def module_method_container_dependencies(module_fullname: str) -> list[str]: ...
```

This helper should:

1. Import the Sage module

2. Find literal nested method containers in that module

3. Call `method_container_direct_bases()` on each

4. Return the modules containing those base containers

Then `get_additional_deps(file)` returns those module names to mypy.

This is important for incremental mode: changing `A.ParentMethods.f` should invalidate
checks of `B.ParentMethods.@override f` if Sage says B semantically inherits from A.

### Matching Target Classes

The plugin should not match every class named `ParentMethods`. It should ask Sage’s
parser:

```python
def is_sage_method_container_fullname(fullname: str) -> bool:
    return sage.categories.mypy_support.parse_method_container_fullname(fullname) is not None
```

The parser should accept only containers that actually sit under a Sage category source
class.

Accepted terminal names: `ParentMethods`, `ElementMethods`, `MorphismMethods`,
`SubcategoryMethods`.

Accepted nested examples: `Rings.ParentMethods`, `Objects.Homsets.ParentMethods`,
`Objects.Homsets.ElementMethods`, `Monoids.Finite.ParentMethods`.

Rejected examples: `some.random.ParentMethods`, `non_category_class.ParentMethods`.

### Exact Projection Invariant

For a source class:

```python
class C(Category):
    class ParentMethods:
        @override
        def f(self): ...
```

the helper computes:

```python
C_instance = C.an_instance()
runtime_bases = C_instance.parent_class.__bases__
```

If `runtime_bases == (A_instance.parent_class, B_instance.parent_class)`, then the
plugin injects `class C.ParentMethods(A.ParentMethods, B.ParentMethods): ...` in mypy’s
internal graph.

The same mapping applies for `ElementMethods` (via `element_class.__bases__`),
`MorphismMethods` (via `morphism_class.__bases__`), and `SubcategoryMethods` (via
`subcategory_class.__bases__`).

This is the entire semantic bridge.

### Diagnostic Policy

The plugin should not silently invent bases.

Recommended diagnostics:

| Code | Condition |
| --- | --- |
| `sage-category-unresolved` | could not instantiate source category |
| `sage-category-parameterized` | category source class is parameterized and no representative was configured |
| `sage-category-base-unmapped` | Sage dynamic base could not be mapped back to a source method container |
| `sage-category-typeinfo-missing` | source base fullname resolved in Sage but not in mypy |

In non-strict mode, unresolved cases can be skipped.
In strict mode, unresolved cases should be hard errors because missing base injection
makes `@override` results incomplete.

### Debug Oracle

A debug command should print the projection without invoking mypy internals:

```
sage -python -m sage.categories.mypy_support \
    sage.categories.rings.Rings.ParentMethods
```

Expected output shape:

```
sage.categories.rings.Rings.ParentMethods
  dynamic class: sage.categories.rings.Rings.parent_class
  dynamic bases:
    sage.categories.rngs.Rngs.parent_class
    sage.categories.semirings.Semirings.parent_class
  injected static bases:
    sage.categories.rngs.Rngs.ParentMethods
    sage.categories.semirings.Semirings.ParentMethods
```

This makes plugin failures inspectable without implementing shadow files as the main
path.

### Minimal Implementation Surface

**Sage side** (`sage.categories.mypy_support`):

- `parse_method_container_fullname(fullname)`

- `instantiate_category_from_source_path(module, category_path)`

- `method_container_direct_bases(fullname)`

- `module_method_container_dependencies(module_fullname)`

- `debug_projection(fullname)`

**Mypy side** (`sage.typing.mypy_plugin`):

- `plugin(version)`

- `SageCategoryPlugin.get_customize_class_mro_hook(fullname)`

- `SageCategoryPlugin.get_additional_deps(file)`

- `SageCategoryPlugin.report_config_data(ctx)`

No Sage-side category resolution is reimplemented.
The only Sage-side logic is:

```
literal source fullname
    → Sage category instance
    → Sage dynamic method class
    → its direct dynamic bases
    → corresponding literal method containers
```

The mypy plugin then injects those literal containers as ordinary static bases and lets
mypy’s existing `@override` machinery perform the check.
