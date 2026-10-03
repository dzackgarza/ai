# Sage Wrapper Bug Patterns

Common bugs found when reviewing category-spec wrappers around Sage objects.

## Pattern 1: Broken Sage `__eq__` on Wrapper Classes

**Symptom:** `wrapper_obj == wrapper_obj` returns `False` even for identical content.

**Root cause:** Sage classes (e.g., `ImageSubobject`) don’t override `__eq__`, so Python
uses identity. The project declares `__eq__` as `@abstract_method` on the project
category, but Sage’s concrete (but broken) identity-based `__eq__` satisfies the
abstract check during `refine_category` without error.

**Fix:** Override `__eq__`, `__ne__`, `__hash__` on the project wrapper class:

```python
def __eq__(self, other: object) -> bool:
    if not isinstance(other, type(self)):
        return NotImplemented
    return list(self) == list(other)

def __ne__(self, other: object) -> bool:
    if not isinstance(other, type(self)):
        return NotImplemented
    return not self.__eq__(other)

def __hash__(self) -> int:
    return hash(tuple(self))
```

## Pattern 2: Raw Sage Return Without Project Refinement

**Symptom:** A method on a project category returns a Sage object directly, not refined
into the project category.

**Root cause:** Method calls `from sage.xxx import Foo` then `return Foo(...)`. The
result is a Sage object, so project-specific methods aren’t available.

**Fix:** Wrap with `refine_category`:

```python
raw = SageConstructor(...)
return refine_category(raw, [ProjectCategory()])
```

## Pattern 3: `@abstract_method` Delegating to Broken Sage Implementation

**Symptom:** A method is declared `@abstract_method` with `...`, relying on Sage’s
concrete implementation via inheritance.
But Sage’s implementation is broken or doesn’t exist.

**Root cause:** The abstract method check during `refine_category` only verifies the
method EXISTS, not that it WORKS correctly.

**Fix:** Provide a concrete project implementation:

```python
# Instead of:
@abstract_method
def submeetsemilattice(self, elements): ...

# Use:
@final
def submeetsemilattice(self, elements):
    raw = SageMeetSemilattice(self.subposet(closure))
    return refine_category(raw, [ProjectCategory])
```

## Pattern 4: Narrow `except` Clause

**Symptom:** `except ValueError:` misses other exception types.

**Root cause:** Sage methods can raise `TypeError` or other exceptions in edge cases
that the handler doesn’t catch.

**Fix:** Use `except (ValueError, TypeError):` or a broader catch where appropriate.

## Pattern 5: Private Attribute Probing Instead of Type Dispatch

**Symptom:** `getattr(self, "_private_attr", None)` to check Sage internals.

**Root cause:** Sage’s internal attribute names aren’t public API.

**Fix:** Use `isinstance` checks against documented Sage wrapper classes, or add a
public project accessor.

## Pattern 7: Method Resolution Changes When Routing Through Refined Parent

**Symptom:** Switching from `base_module.tensor(...)` to `component.tensor(...)` breaks
all constructors with `TypeError: unexpected keyword argument 'name'`.

**Root cause:** `base_module` (a `FiniteRankFreeModule`) has a `tensor()` method that
creates `FreeModuleTensor` elements with `name=`, `latex_name=`, `sym=`, `antisym=`
kwargs. The refined `component` (a `TensorFreeModule` inheriting from
`ReflexiveModule_abstract`) has a DIFFERENT `tensor()` method —
`ReflexiveModule_abstract.tensor_product()` — which does NOT accept those kwargs.

The fix from the previous session was to route through `base_module.tensor()` (the
known-working method) while still calling `component_module()` for the refinement side
effect:

```python
# Correct pattern:
self.component_module(base_module, tensor_type, sym=sym, antisym=antisym)
return base_module.tensor(tensor_type, name=name, latex_name=latex_name, sym=sym, antisym=antisym)
```

**Lesson:** Routing through a refined parent is not always correct — the refined parent
may have OVERRIDDEN the method with a different signature.
Always verify that the method you’re routing through has the expected parameter set.
When in doubt, route through the parent with the documented method, not the most-refined
parent.

## Pattern 8: `refine_category(test=False)` Hides Abstract Method Gaps

**Symptom:** `refine_category(..., test=True)` fails with
`AssertionError: Not implemented: alternating_algebra` but `test=False` passes silently.

**Root cause:** The `test=True` flag runs `_test_not_implemented_methods()` on the
refined object, catching abstract methods that haven’t been implemented yet.
Using `test=False` suppresses this check.

**Fix:** Record the abstract method gaps explicitly in the task’s work log.
Do not rely on `test=False` to silently skip coverage.
The frontier table should document every unimplemented abstract method, its owning
category, and the downstream card that will implement it.

## Pattern 9: Review Logs Not Written to Card Bodies

**Symptom:** Cards are promoted to `complete` without any review evidence in the file.
A future agent reads the card and sees only a status change with no record of what was
checked or verified.

**Root cause:** The coordinator dispatches subagent reviews, the subagent summarizes
findings in chat, the coordinator changes the status to `complete`, but neither writes a
review log into the card body file.

**Fix (for the coordinator):** After a subagent completes its review:

1. Read the card file to verify the subagent wrote the review log into it

2. If the subagent did NOT write to the file, extract the gate-by-gate findings from the
   subagent’s summary and write them into the card file yourself

3. THEN change the status

4. Never change status without first ensuring the review log exists in the file

A review that produces no durable artifact in the card file is indistinguishable from no
review at all.

## Pattern 10: Software Names Disguised as Mathematical Categories

**Symptom:** An axiom or category name describes the *data structure* or *implementation
constraint* rather than a *mathematical property of the objects*. The name is a compound
of implementation details.

**Example:** `Sets().Partitioned().FiniteTotallyOrderedBase()` —
“FiniteTotallyOrderedBase” is a compound of three words describing the base set’s
structure. It does not describe a property that partition objects have.

**Fix:** Replace with a chain of existing axioms that compose naturally:

- `Sets().Finite().TotallyOrdered().Partitioned()` reads as “partitions of a finite
  totally ordered set”

- Each link in the chain is an independently meaningful mathematical axiom

- The chain describes what the objects ARE, not what the base set looks like

**Detection:** When a name needs to be explained by saying “it’s a property of the X,
not of the Y” or “it describes the base,” it’s a software name.
A mathematical name should be self-explanatory in the context of its category chain.

## Pattern 12: Sage Supercategory Abstract Method Leakage

**Symptom:** Adding a new `CategoryWithAxiom` to a refinement chain causes
`AssertionError: Not implemented method: max` on object types that should not have that
method.

**Root cause:** The new category’s `super_categories` includes a Sage category (e.g.,
`Sets().Finite()`) whose `ParentMethods` declares abstract methods (e.g., `max`) that
are valid for sets-of-elements but invalid for sets-of-partitions.
Sage’s category machinery requires ALL parent methods from ALL supercategories to be
implemented.

**Example:** `TotallyOrderedSetsCategory` with `super_categories = [Sets().Finite()]`
was added to the refinement chain of `SetPartitions(3)`. Sage tried to call `max()` on
the partition set parent, which failed because partitions aren’t comparable by `<`.

**Fix:** Set `super_categories` to `[]` on supplemental categories that provide
convenience methods rather than mathematical refinements.
The category exists to carry methods, not to add abstract obligations:

```python
class TotallyOrderedSetsCategory(CategoryWithAxiom):
    @override
    @final
    def super_categories(self) -> list[Category]:
        return []  # No supercategory obligations — this class adds methods only
```

**Alternatively:** If the supercategory relationship IS mathematically correct, ensure
the parent object implements all required methods from the inherited chain.

**Symptom:** `ruff check --select F821` reports `undefined name 'Posets'` in files that
use `refine_category(raw, [Posets().JoinSemilattice().Finite()])`.

**Root cause:** `Posets` is imported inside `super_categories()` as a local import, but
used in sibling methods (`subjoinsemilattice`, `submeetsemilattice`) that don’t have
access to that scope.

**Fix:** Add the import locally in each method that uses it, matching the existing
local-import pattern:

```python
def subjoinsemilattice(self, elements):
    from sage.combinat.posets.lattices import JoinSemilattice as SageJoinSemilattice
    from .. import Posets       # <-- missing
    from ....utils import refine_category
    ...
```
