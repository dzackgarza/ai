---
id: FEATURE-SAGE-MYPY-CATEGORY-OVERRIDE-PLUGIN
trackerStatus:
  type: feature
parents: []
dependsOn: []
plans:
- '[[PLAN-MYPY-PLUGIN-IMPLEMENTATION]]'
title: Mypy plugin for Sage category method override checking
status: complete
priority: high
description: 'Build a Sage-specific mypy plugin that makes @override work for Sage''s
  dynamic category method system (ParentMethods, ElementMethods, MorphismMethods)
  without requiring literal Python inheritance in category source files. The plugin
  injects static base/MRO edges derived from Sage''s runtime category resolution so
  that standard typing.override semantics function correctly during type checking.

  '
---

# Mypy Plugin for Sage Category Method Override Checking

## Objective

Build a Sage-specific mypy plugin that makes `@override` work for Sage's
dynamic category method system. See spec for full acceptance criteria.

## Location

Standalone tooling project, not embedded in research repo or Sage source tree.

- Repo: `~/ai/sage-mypy-category-plugin/`
- Plugin: `sage_mypy_category_plugin/plugin.py` (registers via `[mypy] plugins = sage_mypy_category_plugin.plugin`)
- Introspection: `sage_mypy_category_plugin/introspection.py`

## Implementation Summary (complete)

### Introspection module
Resolves method container direct bases from Sage's `dynamic_class.__bases__` —
not MRO, not `super_categories()`. Maps dynamic class bases back to source-level
method containers via `getattr(type(D), method_kind, None)`. Structural fullname
parser (no Sage imports at parse time). Verified: Rings→Rngs, Groups→Monoids,
Fields→EuclideanDomains/DivisionRings/PIDs/NoetherianRings.

### Plugin — MRO splice
mypy's `@override` check walks `info.mro` (checker.py:2331), not `info.bases`.
The `get_customize_class_mro_hook` fires after `calculate_mro()`, so modifying
`info.bases` alone has no effect. Fix: splice ancestor TypeInfos directly into
`info.mro` between the class itself and the final `object` entry:

```
info.mro = head + ancestor_typeinfos + [object]
```

TypeInfo lookup walks module symbol tables, handles filesystem prefix mismatch
between `tests.fixtures.sage.categories...` and normalized `sage.categories...`.

### Test results
12 passed, 4 skipped:
- 5 debug oracle (Rings, Sets, Groups, Fields, oracle-plugin consistency)
- 7 integration (valid/invalid override, diamond, element/morphism methods,
  signature mismatch, parameterized no-config)
- 4 skipped (renamed ancestor, cache invalidation, homset, parameterized configured)
