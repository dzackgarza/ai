# Architecture Minimization Playbook

Read this reference for dependency surveys, fork-vs-build decisions, architecture
decisions, concrete planning, and second-pass owned-surface minimization.

## Surface Minimization

Use `Architecture Minimizer` mode before choosing a stack.
Ask why any nontrivial local code should exist.

Survey each major behavior across:

- OS-native features;
- CLI tools;
- language libraries;
- frameworks;
- host app extension/plugin APIs;
- external APIs;
- local services;
- existing open-source apps;
- commercial apps;
- fork candidates;
- no-code or low-code glue;
- bespoke implementation.

For external tools, APIs, libraries, standards, package managers, or exact errors, load
`known-solution-first` and verify public contracts before local probing.

Write `architecture/dependency-survey.md` and `architecture/similar-project-survey.md`.
Evaluate candidates with:

```yaml
fit_to_obligations:
maturity:
maintenance_activity:
license:
security_history:
API_stability:
documentation_quality:
testability:
transitive_dependency_risk:
platform_support:
offline_support:
performance:
accessibility:
user_install_burden:
owned_integration_complexity:
```

For fork or existing-app candidates, capture:

```yaml
project:
license:
core_feature_match:
missing_features:
architecture_fit:
plugin_points:
active_maintenance:
codebase_size:
test_quality:
dependency_health:
difficulty_to_rebrand_or_retarget:
risk_of_fighting_upstream_architecture:
fork_burden:
recommendation:
```

Avoid alternate-provider planning unless the product explicitly owns multi-provider
selection as a user-visible behavior.
If no route satisfies must-have obligations, route back to requirements or MVP scoping.

## Owned-Surface Ledger

Write `architecture/owned-surface-ledger.yaml` for every nontrivial behavior:

```yaml
behavior:
local_owner: true | false
delegated_to:
version_or_package:
license:
why_delegate_or_own:
error_categories_eliminated:
residual_local_obligations:
tests_required:
```

Local ownership is allowed only when the survey records why delegation is worse:

- no suitable dependency exists;
- dependency fails a critical obligation;
- license is unacceptable;
- dependency is unmaintained or unstable;
- glue would exceed local implementation complexity;
- privacy/offline constraints are violated;
- testing or deployment becomes materially worse;
- upstream architecture fights the product.

Gate:

- every planned component maps to a ledger entry;
- every dependency maps to delegated behavior or infrastructure need;
- every locally owned behavior has a written non-delegation reason.

## Implementation Path Decision

Use `Architecture Arbiter` mode to choose one route:

- glue existing OS or CLI tools;
- write a thin wrapper around existing tools;
- build a plugin or extension inside a host app;
- fork an existing app;
- use a major framework/library and write an integration layer;
- build a custom app with heavy dependency delegation;
- build mostly bespoke implementation.

Mostly bespoke implementation is exceptional and requires strong justification.

Write ADRs in `architecture/ADR-*.md`:

```yaml
id:
decision:
status: accepted
context:
requirements_supported:
abstract_obligations_supported:
options_considered:
chosen_option:
why_not_simpler:
why_not_fork:
why_not_os_tool:
owned_surface_added:
owned_surface_eliminated:
risks:
reversal_plan:
```

Gate:

- selected path satisfies MVP abstract obligations, threat model, owned-surface budget,
  install/deploy constraints, license constraints, and maintenance burden.

## Concrete Implementation Planning

Use `Concrete Planner` mode only after the route is selected.
This is the first point where stack, runtime, schema, routes, packages, files, and module
boundaries may be specified.

Write `planning/implementation-plan.md` with:

```yaml
stack:
runtime:
package_manager:
frameworks:
libraries:
external_tools:
OS_integrations:
repository_structure:
modules:
public_APIs:
internal_interfaces:
schemas:
state_model:
error_model:
configuration_model:
logging_model:
test_strategy:
migration_strategy:
build_and_packaging:
CI_requirements:
```

For each component, add a code ownership budget:

```yaml
component:
planned_owner:
local_code_allowed:
local_code_forbidden:
max_bespoke_LOC:
```

Gate:

- no implementation begins until module boundaries and local ownership limits are
  explicit.

## Second Surface Minimization

Use `Plan Minimization Adversary` mode after the concrete plan exists.
For every planned module ask:

- can this be deleted;
- can this be delegated;
- can this be declarative configuration;
- can the framework, host app, OS, or a smaller mature library own it;
- can a different architecture remove it.

Write `planning/plan-minimization-review.md`.

Gate:

- viable surface-reducing alternatives are adopted or rejected with concrete evidence.
