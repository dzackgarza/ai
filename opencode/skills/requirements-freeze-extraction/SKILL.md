---
name: requirements-freeze-extraction
description: >
  Use when a repository has accumulated features, rewrites, framework pivots,
  duplicated ownership, abandoned branches, incoherent architecture, or
  implementation residue that makes it unclear what the product actually is.
  Use when the user asks about freezing, requirements extraction, accretion
  creep, architectural reset, product specification, rewrite readiness, or
  preventing future scope creep. Use when a proposed feature would add behavior
  before the repo has a clear normative requirements document. Use when the repo
  has no durable document answering: what is this product, what does it own,
  what does it not own, what user-facing outcomes are required, and what old
  implementation choices are non-binding.
---

# Requirements Authority Freeze Skill

## Mission

When a repository shows accretion, competing architectures, feature creep, framework churn, or unclear ownership, stop product-changing work and establish a single implementation-independent requirements authority.

The existing repo is evidence. It is not authority.

This skill does not plan or execute a rewrite. It creates and maintains the document that a future rewrite, refactor, or continuation must obey.

## Decisive invariant

At the end of this skill, there is exactly one normative product/architecture requirements authority.

Every user-facing behavior, state owner, external contract, failure behavior, and anti-requirement is either recorded there or explicitly excluded.

All other artifacts are non-normative unless the authority document incorporates their claim.

## Core rule

The existing repository is evidence. The requirements document is authority.

A fact about the current implementation becomes normative only if it survives extraction as one of:

1. A user-facing requirement.
2. A necessary product invariant.
3. An ownership decision.
4. A failure behavior.
5. An external tool contract.
6. An explicit anti-requirement.

Everything else is legacy evidence, historical context, rejected accident, or implementation residue.

## Non-goals

This skill does not:

- Design the new implementation.
- Choose the rewrite framework, language, database, UI library, server substrate, or deployment target unless that choice is itself already a product requirement.
- Produce a migration plan.
- Produce a refactor plan.
- Patch the existing app.
- Preserve old code paths for compatibility.
- Convert every old feature into a future requirement.
- Create process documents that do not constrain product or architecture decisions.

The output is a requirements authority and maintenance protocol, not an implementation roadmap.

## When to freeze

Freeze product-changing work if any of these hold:

- No single requirements authority exists.
- Multiple docs imply incompatible product direction.
- The implementation contradicts the stated product model.
- A branch/PR introduces a substrate, framework, or ownership model not already authorized.
- Active TODOs/plans contain features whose user outcome or owner is unclear.
- Tests encode implementation behavior that has no corresponding product requirement.
- A proposed task would add feature surface before requirement ownership is settled.

Freeze means no new features, no framework migrations, no substrate changes, no semantic refactors, no feature-card expansion, and no PR merges that change product behavior.

Allowed work during freeze: critical data-loss/security fixes, inspection, extraction, and requirements-authority creation or maintenance.

## Required files

The requirements authority must be split into at least two normative layers plus one non-normative ledger.

### Layer 1: `REQUIREMENTS.md` (abstract product authority)

Normative. Technology-independent, framework-independent, implementation-independent.

Defines user-facing behavior, product state, invariants, ownership, workflows, forbidden behavior, and acceptance oracles.

Must pass the overnight-loss test:

> If all current code, tools, languages, frameworks, libraries, branches, and implementation files disappeared overnight, this document should still allow a competent implementer to reconstruct an app with essentially the same user-facing behavior and product semantics in an entirely different technical stack.

Must not contain implementation history, migration narrative, abandoned choices, branch names, PR stories, current file paths, framework names (unless user-facing), language names, package names, endpoint names (unless public API), or component names.

### Layer 2: `DESIGN-COMMITMENTS.md` (concrete design authority)

Normative. Records current binding choices about substrate, language, framework, external tools, file locations, protocols, packaging, deployment, and implementation-specific constraints.

Must pass the current-app reconstruction test:

> If all code were lost, `REQUIREMENTS.md` and `DESIGN-COMMITMENTS.md` together should allow a competent implementer to reconstruct the current user-facing behavior, operational assumptions, and concrete technical commitments closely enough that the result is recognizably the same present app, though not necessarily with the same internal structure.

Must not contain "we used to," "this replaced," "the old app did," "the branch attempted," chronological development narrative, or justifications from abandoned history.

### Evidence ledger: `REQUIREMENTS-LEDGER.md`

Non-normative. Records how old artifacts were classified.

This is the only place where historical evidence may appear.

Allowed classifications:

- requirement,
- anti-requirement,
- ownership decision,
- failure behavior,
- external contract,
- open decision,
- evidence only,
- rejected accident,
- obsolete historical context.

## `REQUIREMENTS.md` schema (abstract layer)

This schema describes `REQUIREMENTS.md`. All sections below are normative for the abstract product requirements.

Every claim in this file must pass the overnight-loss test: it must not reference current implementation internals, framework names, language names, file paths, component names, endpoint names (unless public API), historical context, branch names, or migration narrative.

### 0. Authority and freeze status

State:

> This document is the normative product and architecture requirements authority. The existing implementation, tests, branches, PRs, TODOs, and docs are evidence only. No current behavior, dependency, component, endpoint, file layout, test, or branch direction is inherited unless this document states the requirement it satisfies.

Also state:

- freeze status,
- date,
- scope,
- what kinds of changes are blocked until open decisions are resolved.

### 1. Product definition

Define the product without implementation accidents.

Must answer:

- What is this product?
- Who uses it?
- What primary outcome does it provide?
- What kind of system is it?
- What kind of system is it not?

### 2. Non-goals

List product boundaries.

A non-goal should prevent old experiments from returning as ambiguous "future work."

### 3. User-facing requirements

Every requirement uses this structure:

```md
REQ-000: Name

Outcome:
User-visible behavior:
Inputs:
Outputs:
State read:
State written:
Owner:
Failure behavior:
Acceptance oracle:
Evidence:
```

Rules:

- Requirements must describe outcomes, not implementation artifacts.
- Existing implementation nouns are forbidden unless they are product-contract nouns.
- "The current app does X" is not a requirement.
- Every retained requirement must have an owner and oracle.

### 4. Ownership model

Every capability has exactly one owner.

```md
| Capability | Owner | Non-owners | Rule | Forbidden duplication |
|---|---|---|---|---|
```

If ownership cannot be assigned, create an open decision. Do not allow dual ownership to remain implicit.

### 5. State model

For every durable or semantically important state item:

```md
State:
Owner:
Created by:
Read by:
Mutated by:
Persisted where:
Cleared by:
Invariants:
Invalid states:
```

This is mandatory for apps with documents, files, routes, workspaces, projects, sessions, generated artifacts, caches, accounts, plugins, jobs, or external tool state.

### 6. External contracts

For each intentional external dependency:

```md
External contract:
Required or optional:
Owned behavior:
Non-owned behavior:
Failure if unavailable:
Version/compatibility expectation:
Why this is product-level, not implementation residue:
```

Current dependencies not listed here are non-authoritative implementation residue.

### 7. Workflows

Workflows are end-to-end product contracts:

```md
Workflow:
Initial state:
User action:
System behavior:
Final state:
Failure cases:
Acceptance oracle:
```

Do not describe component trees, current endpoints, or implementation internals unless they are public API contracts.

### 8. Failure semantics

Specify product-level failure behavior for:

- invalid input,
- missing dependency,
- optional integration unavailable,
- external command failure,
- parse/compile/render failure,
- stale or conflicting state,
- partial output,
- corrupt config,
- interrupted operation,
- recovery.

Failure behavior must be explicit, not inherited from implementation defaults.

### 9. User-surprise and forbidden behavior inventory

`REQUIREMENTS.md` must contain a normative section titled:

```md
## User-Surprise and Forbidden Behavior Inventory
```

This section records behavior that is forbidden because it violates user expectation, state ownership, fail-fast semantics, product clarity, or explicit app policy.

#### Core rule

If the app cannot perform the requested product action under the current declared requirements, it must fail loudly and visibly at the relevant boundary.

It must not:

- invent substitute behavior,
- silently skip the action,
- continue with stale state,
- downgrade the operation,
- use a backup or temporary substitute as if it were canonical,
- catch the failure and proceed,
- log only to console,
- return a synthetic success result,
- hide the failure behind an "ok" field,
- produce partial output while claiming completion,
- or route the user into an unplanned recovery flow.

#### Boundary with failure documentation

The requirements authority may state:

```md
This condition is invalid and must surface as a hard failure.
```

It must not state:

```md
If this condition occurs, fall back to X, retry Y, route to Z, recover by doing W, or continue in degraded mode.
```

Permitted:

- name invalid states,
- name forbidden behavior,
- require clear surfacing of failure,
- require non-mutation of canonical state after failed preconditions,
- require that a command not claim success.

Forbidden:

- designing recovery UX,
- designing error routing,
- designing fallback behavior,
- anticipating broad classes of environmental failure and building compensating flows,
- specifying "graceful degradation,"
- adding optional modes to avoid failure,
- adding local suppressions or exception handlers.

#### Required forbidden-behavior table

The section must include a table:

```md
| Forbidden behavior | Why it surprises the user | Required product stance | Related state/owner | Evidence |
|---|---|---|---|---|
```

Allowed values for "Required product stance":

- hard failure,
- refuse action,
- do not mutate state,
- do not claim success,
- block until requirement is satisfied,
- delete/forbid feature,
- classify as out of scope,
- make ownership decision first.

Do not use values such as:

- fallback,
- retry,
- recover,
- continue,
- warn and proceed,
- best effort,
- partial success,
- compatibility mode,
- degraded mode.

#### Categories to inventory

Agents must inspect the repo and populate the forbidden-behavior inventory across all applicable categories below.

**1. Hidden or swallowed failure**

Forbidden patterns:

- `catch` blocks that only log and continue.
- Empty `catch` blocks.
- Suppressed stderr.
- Boolean `ok` responses that hide command failure.
- Console-only error reporting for user-visible failures.
- UI toasts that do not change command success/failure state.
- Returning placeholder output after a failed operation.
- Tests that ignore console errors or stderr.
- Tests that assert no crash when the correct behavior is hard failure.

Required stance: the operation must fail loudly at the boundary and must not claim success.

**2. Silent fallback**

Forbidden patterns:

- fallback to default config when required config is missing,
- fallback to another backend,
- fallback to stale generated files,
- fallback to cached data,
- fallback to backup files as canonical state,
- fallback to a different renderer,
- fallback to a different parser,
- fallback to a different route owner,
- fallback to a guessed path,
- fallback to an empty object, empty array, or placeholder value.

Required stance: missing required state or dependency is invalid. The app must stop the action.

**3. Degraded or partial success**

Forbidden patterns:

- "best effort" output,
- partial render with success status,
- partial save with success status,
- plugin failure with successful command state,
- skipped records treated as successful import,
- missing assets silently omitted,
- generated artifacts written despite invalid source,
- deployment/sync partial completion treated as complete.

Required stance: a product action either satisfies its declared acceptance oracle or fails.

**4. State substitution**

Forbidden patterns:

- temporary files used as canonical user files,
- backup files used as save targets,
- generated artifacts treated as source,
- cached manifests treated as authority,
- editor buffer identity treated as file identity,
- UI selection treated as persisted state,
- current implementation state treated as requirements authority,
- old branch behavior treated as product direction.

Required stance: only the declared state owner may define canonical state.

**5. Duplicate ownership**

Forbidden patterns:

- two route owners,
- two renderers for the same preview contract,
- two save authorities,
- two config authorities,
- two plugin systems,
- two file identity sources,
- two workspace roots,
- two state machines for the same user workflow,
- parallel Express and Tauri backends for the same operation,
- framework and app both owning the same layout/chrome.

Required stance: the requirements authority must assign exactly one owner or mark an open decision. Implementation must not proceed while ownership is split.

**6. User action misdirection**

Forbidden patterns:

- button label does not match operation,
- command claims to save but writes elsewhere,
- command claims to open but only stages a path,
- export action runs on stale file instead of current buffer,
- preview renders different content than the editor shows,
- "New" creates a real file before the user saves, unless explicitly required,
- "Save" uses a path not selected or previously established by the user,
- "Run plugin" proceeds without satisfying the plugin's declared preconditions.

Required stance: user-visible actions must correspond exactly to declared state transitions.

**7. Hidden mutation**

Forbidden patterns:

- mutating workspace root as a side effect of unrelated actions,
- changing renderer config during render,
- changing file identity during preview,
- creating files during "new buffer" unless specified,
- deleting user files during cleanup,
- modifying source content during preview,
- silently rewriting user input,
- changing global config from a local operation.

Required stance: only declared transitions may mutate declared state.

**8. Compatibility residue**

Forbidden patterns:

- deprecated paths retained for no current requirement,
- legacy flags,
- compatibility adapters for abandoned internal APIs,
- old feature branches preserved as runtime options,
- dual code paths for old and new behavior,
- "in case future callers need it" parameters,
- accepting both old and new schemas without a stated product contract.

Required stance: if no current requirement owns the behavior, delete or classify it as rejected residue.

**9. Specification laundering**

Forbidden patterns:

- TODO item treated as requirement,
- current test treated as product oracle without extraction,
- branch name treated as direction,
- PR body treated as authority,
- README claim overriding `REQUIREMENTS.md`,
- implementation behavior treated as invariant,
- stale design doc treated as still active,
- generated artifact treated as source truth.

Required stance: only `REQUIREMENTS.md` is normative. Everything else is evidence until classified.

**10. Validation theater**

Forbidden patterns:

- tests that only assert non-null values,
- tests that assert an `ok` flag without checking state,
- tests that mock the boundary whose behavior is under test,
- tests that prove helper behavior instead of user workflow,
- tests that pass if the app silently skips work,
- tests that accept warning-only failure,
- tests that assert implementation shape rather than product outcome.

Required stance: acceptance oracles must fail when the user-visible requirement is broken.

**11. Optionality creep**

Forbidden patterns:

- optional parameters for required state,
- optional config that the product cannot operate without,
- runtime modes to avoid choosing ownership,
- settings that expose unresolved architecture decisions,
- feature flags preserving incompatible behaviors,
- environment switches for product semantics.

Required stance: required state is required. Ownership decisions must be made in the requirements authority, not deferred into runtime options.

**12. Local workaround creep**

Forbidden patterns:

- repo-local QC bypasses,
- local whitelists,
- local relaxed validators,
- project-specific suppressions,
- warning-only checks,
- catch-all "ignore this case" branches,
- scripts that hide tool failures and synthesize success.

Required stance: the violation must be fixed, globally configured, or classified as out of scope. It must not be hidden locally.

#### Required per-requirement surprise audit

Every `REQ-*` entry must include a short subsection:

```md
Surprising behavior forbidden:
- ...
```

This subsection lists behavior that would violate the user's expected outcome.

Example:

```md
REQ-004: Run export plugin

Surprising behavior forbidden:
- Plugin must not run against an unsaved backup path.
- Plugin must not run against stale disk content when the editor buffer is dirty.
- Plugin must not report success if the command exits nonzero.
- Plugin must not create output in an implicit location not declared by the plugin contract.
- Plugin must not silently skip missing required tools.
```

#### Required state-machine integration

The abstract state machine must mark forbidden states that correspond to surprising behavior. Each invalid state must link to a forbidden-behavior entry.

Example:

```md
Invalid state:
pluginExecution = running while currentDocument = unsavedBuffer

Forbidden behavior:
Running a path-dependent plugin without canonical file identity.

Required stance:
Block/refuse action until the requirement is satisfied. Do not create a hidden temp file as substitute identity.
```

#### Required evidence pass

When applying this addendum, agents must search for evidence of surprising behavior in source code, tests, config files, scripts, workflow files, TODOs, old plans, open PRs, current branches, and commit messages that mention fallback, compatibility, graceful handling, recovery, warning, skip, optional, degraded, or best effort.

Search terms should include, when appropriate:

```text
fallback
graceful
recover
recovery
ignore
ignored
skip
optional
default
best effort
partial
warning
warn
try
catch
except
console.error
stderr
2>/dev/null
|| true
ok: true
success
compat
legacy
deprecated
degraded
mock
stub
```

These terms are evidence triggers only. Do not mechanically classify every match as a violation. Inspect the surrounding product boundary.

#### Output requirements

When this addendum is applied, the agent must report:

1. Which surprising-behavior categories were inspected.
2. Which forbidden behaviors were added to `REQUIREMENTS.md`.
3. Which invalid states were added to the abstract state machine.
4. Which current artifacts were classified as evidence only or rejected residue.
5. Whether any current behavior violates the fail-fast/no-hidden-error policy.
6. Whether product work remains frozen because surprising behavior or ownership remains unresolved.

#### Completion check

This addendum is complete only if:

- `REQUIREMENTS.md` contains a User-Surprise and Forbidden Behavior Inventory.
- Every major requirement lists surprising behavior forbidden for that requirement.
- The abstract state machine links invalid states to forbidden behaviors.
- No requirement designs fallback, recovery, graceful degradation, or error-routing behavior.
- Existing hidden-failure or fallback patterns are classified as violations, evidence-only, or explicitly out of scope.
- The document clearly states that app-level error handling is not being designed by this requirements process.

### 10. Abstract product state machine

`REQUIREMENTS.md` must contain a section titled:

```md
## Abstract Product State Machine
```

This section is normative.

It must describe the app as a finite or structured state machine at the product level.

The state machine may be hierarchical or factored when a single flat state graph would be unreadable. For example, document state, workspace state, render state, save state, authentication state, plugin state, and configuration state may be separate interacting submachines.

#### State-machine construction rule

Construct the state machine from requirements only.

Inputs:

* Product definition.
* User-facing requirements.
* Ownership model.
* State model.
* External contracts.
* Failure semantics.
* Happy-path user stories.
* Anti-requirements.

Forbidden inputs as authority:

* Current component hierarchy.
* Current route tree.
* Current endpoints.
* Current function names.
* Current framework lifecycle.
* Current database schema.
* Current temporary files.
* Current tests, except as evidence for product-level oracles.
* Current PR branch architecture.

Current implementation may be used only to discover possible states or failure modes. It does not authorize them.

#### Required state-machine fields

Each state machine or submachine must include:

```md
State machine:
Scope:
Owner:
State variables:
Initial states:
Terminal states, if any:
Events:
Transitions:
Invariants:
Invalid states:
Recovery states:
Acceptance oracles:
```

Each state must be specified as:

```md
State:
Meaning:
Required data:
Forbidden data:
Allowed events:
Forbidden events:
Invariants:
User-visible representation:
```

Each transition must be specified as:

```md
Transition:
From:
Event:
Preconditions:
System action:
To:
State written:
Failure transition:
User-visible result:
Acceptance oracle:
```

#### State variables

The state machine must explicitly define product-level state variables.

Examples:

```md
currentDocument:
  none | unsavedBuffer | savedFile(path)

bufferStatus:
  clean | dirty

renderStatus:
  idle | rendering | rendered | failed

saveStatus:
  idle | saving | saved | conflict | failed

workspace:
  unset | root(path)

configuration:
  missing | valid | invalid

pluginExecution:
  idle | blockedNeedsSave | running(plugin) | succeeded(output) | failed(error)
```

These are examples only. The actual variables must come from the product requirements.

#### Invalid states

The state machine must explicitly list invalid states.

Invalid states are as important as valid states because they prevent accretion.

Examples:

```md
Invalid:
- plugin running with no canonical document path when the plugin requires a path
- saved state with no known save target
- static route owned simultaneously by generated files and client router
- renderer configuration split between config file and ad hoc request fields
- backup file treated as canonical user file identity
- two backends owning the same save operation
```

Each invalid state should correspond to an anti-requirement or ownership rule.

### 11. Happy paths and expected user stories

`REQUIREMENTS.md` must contain a section titled:

```md
## Happy Paths and Expected User Stories
```

A happy path is the expected successful path through the product state machine.

Happy paths are not implementation tasks. They are user-level behavioral stories that establish normal operation.

#### Required fields

Each happy path must include:

```md
Story:
User intent:
Initial state:
Steps:
Expected state transitions:
Expected user-visible behavior:
State invariants preserved:
Acceptance oracle:
```

A happy path must avoid implementation-specific language unless the implementation detail is itself part of the product contract.

#### User-story requirements

Every major user-facing requirement must be covered by at least one happy-path story.

Each story must be written from the user's perspective, but with precise state transitions.

Example form:

```md
Story: Edit an unsaved document and save it

User intent:
The user wants to start writing without choosing a file path first,
preview the content, then save it to a chosen path.

Initial state:
- currentDocument = none
- bufferStatus = clean
- renderStatus = idle
- saveStatus = idle

Steps:
1. User types Markdown into the editor.
2. App records an unsaved buffer and marks it dirty.
3. App renders the buffer through the configured renderer.
4. User invokes Save.
5. App asks for a path because no canonical file exists.
6. User chooses a path.
7. App writes exactly the current buffer to that path.
8. App updates currentDocument to savedFile(path).
9. App marks bufferStatus clean and saveStatus saved.

Expected state transitions:
none/clean -> unsavedBuffer/dirty -> rendered -> saving -> savedFile(path)/clean

Expected user-visible behavior:
- Preview updates from the typed buffer.
- Save prompt appears only when a path is needed.
- After save, the visible file identity is the chosen path.
- No backup or temporary path is shown as the canonical document.

State invariants preserved:
- Renderer reads the current buffer text.
- Save writes the current buffer text.
- Canonical file identity is established only by user save/open action.
- Backup state never becomes document identity.

Acceptance oracle:
Given a fresh app with no opened file, when the user types text,
previews it, and saves to `/tmp/example.md`, then `/tmp/example.md`
contains exactly the typed text, the app reports `/tmp/example.md`
as the current file, the buffer is clean, and no plugin or render
path uses an internal backup file as document identity.
```

#### Failure paths

Happy paths do not replace failure semantics.

For every major happy path, the requirements authority must also define the expected failure transitions.

Use this form:

```md
Failure story:
Associated happy path:
Failure event:
Expected transition:
State preserved:
User-visible error:
Forbidden behavior:
Acceptance oracle:
```

Examples of failure events:

* renderer exits nonzero,
* save target changed externally,
* required config missing,
* plugin command fails,
* external tool unavailable,
* invalid content,
* permission denied,
* user cancels file picker,
* network or subprocess timeout,
* corrupt persisted state.

#### Coverage matrix

The requirements authority must include a coverage matrix linking requirements, state-machine states, transitions, happy paths, failure paths, and oracles.

Required table:

```md
| Requirement | State variables | Happy path | Failure path | Acceptance oracle |
|---|---|---|---|---|
```

A requirement without state-machine coverage is incomplete unless it is purely static and has no behavioral state.

#### State-machine acceptance checks

The state-machine section is incomplete if:

* A user-facing requirement has no corresponding state transition.
* A state variable has no owner.
* A transition writes state not declared in the state model.
* A happy path depends on current implementation structure.
* A failure path leaves canonical state ambiguous.
* A state can be owned by two layers.
* An invalid state is known but not forbidden by anti-requirement.
* A branch or old feature implies a state not represented in the authority document.
* A test can pass while the abstract state transition is broken.

#### Maintenance rule

Any future product change that introduces, removes, or changes a state, event, transition, user story, failure path, or state invariant must update the abstract state machine before or in the same change.

A product-changing PR is invalid if it changes behavior without updating:

* state variables,
* transitions,
* happy paths,
* failure paths,
* acceptance oracles,
* or the coverage matrix.

#### Boundary with rewrite work

The abstract state machine describes required product behavior.

It must not prescribe:

* framework,
* reducer/store library,
* database schema,
* class structure,
* component layout,
* API endpoint names,
* file layout,
* implementation language,
* process model,
* or deployment substrate.

Those are rewrite or implementation decisions and are outside this skill unless already fixed as product requirements.

### 12. Anti-requirements

Anti-requirements block recurrence of accretion.

```md
ANTI-000: Name

Forbidden state:
Why it violates ownership/product model:
Required alternative:
Evidence:
```

Examples:

- no dual backend for one operation,
- no SPA routing when static files own routes,
- no renderer-specific ad hoc request fields if config owns renderer command,
- no temp/backup file as canonical file identity,
- no compatibility shim for abandoned internal behavior,
- no feature card for an outcome owned by an external tool.

### 13. Open decisions

```md
DEC-000: Name

Question:
Why this blocks authority:
Evidence needed:
Allowed investigation:
Forbidden premature implementation:
```

Open decisions are specification blockers, not implementation tasks.

### 14. Acceptance oracles

Each oracle is implementation-independent:

```md
ORACLE-000

Given:
When:
Then:
Forbidden false positives:
```

Tests may later be derived from these. Current tests are evidence only.

### 15. Maintenance rule

State:

> Any change that adds, removes, or changes user-facing behavior, state ownership, external contracts, failure behavior, or architectural boundaries must update this document before or in the same change. Product-semantic code changes without a requirements-authority update are invalid.

## Layer split and decision rules

### Core distinction

The requirements authority must have at least two normative layers:

```md
Layer 1: Abstract Product Requirements

Technology-independent, language-independent, framework-independent, implementation-independent.
Defines user-facing behavior, product state, invariants, ownership, workflows, forbidden behavior, and acceptance oracles.

Layer 2: Concrete Design Commitments

Current binding choices about substrate, language, framework, external tools, file locations, protocols, packaging, deployment, and implementation-specific constraints.
These choices are recorded as current design decisions, not as abstract product requirements.
```

### Decision rule

For every extracted item, assign it to exactly one layer:

```md
Could the same user-facing behavior be implemented in a completely different
language/framework/tool stack?

Yes -> abstract requirement.

No, because the present app intentionally commits to a specific tool/substrate/
location/protocol -> concrete design commitment.

No, because it only reflects how the old code happened to work -> evidence only
or rejected accident.
```

### Required layer labels

Every normative item must be labeled with its layer:

```md
REQ-012 [abstract]
ANTI-004 [abstract]
STATE-003 [abstract]
ORACLE-009 [abstract]
DESIGN-007 [concrete]
CHECK-004 [concrete]
DEC-003 [open concrete decision]
```

Do not mix abstract and concrete claims under the same item.

### Interaction between layers

The abstract layer has priority over the concrete layer.

A concrete design commitment is invalid if it violates an abstract requirement, abstract state invariant, ownership rule, anti-requirement, forbidden behavior rule, or abstract acceptance oracle.

Concrete choices may specialize abstract requirements but may not rewrite them.

Example:

```md
Abstract:
The app must expose a canonical document identity before running a path-dependent plugin.

Concrete:
In the current Tauri app, canonical document identity is represented by an absolute
filesystem path stored in desktop backend state.
```

## Historical framing ban

The normative files must be present-tense and state-based.

Forbidden in `REQUIREMENTS.md` and `DESIGN-COMMITMENTS.md`:

```text
previously, formerly, old, legacy, migration, rewrite, pivot, replaced,
after, before, originally, branch, PR, commit, regression from,
workaround for old, kept for compatibility with, historically
```

These terms may appear in `REQUIREMENTS-LEDGER.md` only.

Instead of:

```md
The old Express backend was replaced by Tauri because the server architecture
caused duplicated state.
```

Write:

```md
Current design commitment:
The app substrate is Tauri. Product operations requiring filesystem access,
renderer execution, plugin execution, and local tool invocation are owned by
the desktop backend.
```

Instead of:

```md
React Router was removed because the app is not an SPA.
```

Write:

```md
Abstract requirement:
Navigation is owned by generated static routes. Client-side routing must not
define canonical route identity.
```

## `DESIGN-COMMITMENTS.md` schema (concrete layer)

`DESIGN-COMMITMENTS.md` must contain at least the following sections:

```md
# Design Commitments

## 0. Authority

This document records current concrete design commitments. It is normative only
when read together with REQUIREMENTS.md. It must not override abstract product
requirements.

## 1. Substrate commitments

Runtime, platform, backend/frontend split, desktop/browser/server model,
packaging model.

## 2. Language and framework commitments

Specific languages, UI frameworks, backend frameworks, build tools, package
managers, and runtime constraints.

## 3. External tool commitments

Specific CLIs, local tools, system services, user-level tool directories,
renderer commands, and plugin command conventions.

## 4. Storage and filesystem commitments

Concrete paths, config locations, state locations, asset locations,
generated-output locations, workspace rules.

## 5. Interface commitments

Concrete UI shell commitments, keyboard shortcuts, menu structure, dialogs,
public CLI commands, public API contracts, if binding.

## 6. Integration commitments

OS integration, editor integration, browser integration, citation manager
integration, diagram tool integration, sync/deploy integration.

## 7. Concrete acceptance checks

Checks that depend on concrete design choices, separate from abstract
acceptance oracles.

## 8. Open concrete decisions

Concrete choices not yet fixed, with forbidden premature implementation.
```

## Evidence ledger schema

```md
| Evidence item | Observed behavior/claim | Classification | Authority target | Notes |
|---|---|---|---|---|
```

Rules:

- A TODO is not a requirement.
- A test is not a requirement.
- A branch is not a direction.
- A dependency is not an external contract.
- A current behavior is not an invariant.
- A failed experiment may produce an anti-requirement or open decision.
- A feature survives only if it becomes a product outcome with owner and oracle.

## Procedure

### Step 1: Locate authority

Search existing docs for a file that already claims normative control over product behavior and architecture ownership.

If several files partially claim authority, choose one to become authority and demote the rest to evidence.

### Step 2: Declare freeze if needed

If authority is absent, contradicted, or incomplete, mark the repo frozen for product-changing work.

### Step 3: Inventory evidence

Inspect:

1. README and user docs.
2. Existing goals/spec/architecture docs.
3. Current UI/CLI/API surface.
4. Tests and fixtures.
5. Config/schema files.
6. Source entrypoints.
7. TODOs/plans/issues.
8. Open PRs and branches.
9. Recent commits showing pivots or reversions.
10. Archived experiments.

### Step 4: Extract product claims

For each evidence item, ask:

- What user outcome is this trying to provide?
- What state does it require?
- What layer owns the outcome?
- Is ownership duplicated?
- Is the feature still needed?
- Is it already owned externally?
- Is it an implementation accident?
- Does it reveal a failure mode to forbid?

### Step 5: Classify evidence

Write every significant item into the ledger using one allowed classification.

Unclear items become open decisions, not implicit requirements.

### Step 6: Split into layers and populate authority

For each extracted claim, assign it to exactly one layer using the decision rule:

```md
Could the same user-facing behavior be implemented in a completely different
language/framework/tool stack?

Yes -> REQUIREMENTS.md (abstract requirement).

No, because the present app intentionally commits to a specific
tool/substrate/location/protocol -> DESIGN-COMMITMENTS.md (concrete
design commitment).

No, because it only reflects how the old code happened to work -> evidence
only or rejected accident.
```

Only promote claims that survive as abstract requirements, concrete design commitments, ownership decisions, external contracts, failure semantics, anti-requirements, or open decisions. Everything else stays in the ledger.

Label every normative item with its layer: `REQ-001 [abstract]`, `DESIGN-007 [concrete]`.

### Step 7: Check authority integrity

The authority documents are incomplete if:

- any requirement lacks owner or oracle,
- any capability has two owners,
- any external dependency is included merely because the old code used it,
- any old branch is treated as a direction without product justification,
- any TODO remains active without a requirement,
- any test encodes product behavior not represented by an oracle,
- any implementation-specific choice is normative without independent justification,
- abstract requirements mention current implementation internals,
- concrete design commitments are mixed into abstract requirements,
- a requirement cannot survive replacing the entire technical stack (fails overnight-loss test),
- a concrete design decision lacks connection to an abstract requirement,
- normative documents narrate project history,
- the evidence ledger reads like a story rather than classified provenance.

### Step 8: Report status

Final report must state:

- frozen or not frozen,
- authority file created/updated,
- evidence file created/updated,
- major evidence classes inspected,
- open decisions,
- anti-requirements added,
- product-changing work now blocked,
- rewrite planning intentionally out of scope.

## Forbidden moves

Do not:

- Treat current implementation as a requirements document.
- Treat TODOs as requirements.
- Treat tests as requirements without extracting their user-facing oracle.
- Treat branches as future direction.
- Treat framework choice as requirement without product-level justification.
- Preserve legacy behavior for compatibility with an unreleased or abandoned internal implementation.
- Keep two owners for the same state or capability.
- Add settings to defer ownership decisions.
- Add adapters to avoid deleting obsolete paths.
- Convert an obviated feature into adjacent app work.
- Create broad process checklists that do not alter product authority.
- Mix abstract requirements and concrete design commitments in the same file.
- Use historical framing or banned terms (`previously`, `old`, `legacy`, `migration`, `rewrite`, `replaced`, etc.) in normative files.
- Let historical narrative leak from the evidence ledger into requirements or design documents.
- Begin rewrite planning inside this skill.

## Completion criteria

This skill is complete when:

- `REQUIREMENTS.md` exists or has been updated (abstract product authority).
- `DESIGN-COMMITMENTS.md` exists or has been updated (concrete design commitments).
- `REQUIREMENTS-LEDGER.md` exists or has been updated (non-normative evidence).
- Abstract requirements and concrete design commitments are separated into the correct files.
- Freeze status is explicit.
- Major existing features, branches, PRs, tests, and docs have been classified.
- Every retained requirement has owner, failure behavior, and acceptance oracle.
- Every abstract requirement passes the overnight-loss test.
- Every concrete design commitment has an associated abstract requirement.
- Duplicate ownership has been eliminated or marked as an open decision.
- Anti-requirements block known accretion paths.
- Future maintenance rules are stated.
- Normative files contain no historical narrative or banned framing terms.
- No rewrite process has been specified beyond declaring that future implementation must satisfy the normative files.

## Future maintenance protocol

### For a new feature

Before implementation:

1. Add or update the user-facing requirement in `REQUIREMENTS.md`.
2. Assign ownership.
3. Update state model if state changes.
4. Update failure semantics if failure behavior changes.
5. Add or update acceptance oracle.
6. Confirm no anti-requirement is violated.
7. Only then implement.

If the feature is already owned by an external tool, delete or reject the feature proposal instead of converting it into adjacent app work.

### For a bug fix

Before or during implementation:

1. Identify the violated requirement or oracle.
2. If none exists, add one.
3. Fix only the behavior needed to satisfy the requirement.
4. Do not create compatibility paths for the broken behavior unless explicitly required.

### For a refactor

Before implementation:

1. State which requirement, owner, or invariant is preserved.
2. Confirm no user-facing behavior is being smuggled in.
3. Confirm no duplicate owner is introduced.

If the refactor changes behavior, it is not just a refactor; update the requirements.

### For a framework or substrate change

Before implementation:

1. State the product requirement that the current substrate cannot satisfy.
2. State why the new substrate satisfies that product requirement.
3. Confirm the old substrate will be removed, not retained in parallel.
4. Add anti-requirements preventing dual-substrate operation unless dual-substrate operation is itself an explicit product requirement.

Do not implement substrate changes under infrastructure labels.

### For a branch or PR review

Classify the branch/PR as one of:

- Implements existing requirements.
- Reveals missing requirements.
- Reveals anti-requirements.
- Reveals open ownership decisions.
- Preserves implementation residue.
- Creates duplicate ownership.
- Out of scope.

A branch that changes product semantics without updating the relevant normative file (`REQUIREMENTS.md` for abstract requirements, `DESIGN-COMMITMENTS.md` for concrete design commitments) is not complete.
