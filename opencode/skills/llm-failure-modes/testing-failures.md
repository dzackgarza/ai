# Testing and Verification Failures

> Part of [llm-failure-modes](SKILL.md).
> See there for editorial guidelines and cross-references.
> For concrete test-review patterns that instantiate these failures, also load
> [../reviewing-llm-code/references/pattern-catalog.md](../reviewing-llm-code/references/pattern-catalog.md).

1. **Content-free verification** - Asserting `is not None`, `len(x) > 0`, or
   `isinstance()` as the primary claim.
   This proves the object exists, not that it is correct.
   A test that passes on a wrong implementation is not a test.

2. **Tautological testing** - Tests that verify only internal consistency: input feeds
   the function, function output feeds the assertion, with no external ground truth.
   The implementation validates itself and all errors pass silently.

3. **Mock-first evasion** - Reaching for mocks, stubs, or faked fixtures rather than
   confronting real system behavior.
   A test suite built on mocks certifies the mock’s behavior, not the system’s.

4. **Tolerance substitution** - Using approximate equality (`assertAlmostEqual`,
   relative tolerance) where exact equality is mathematically required.
   Hides precision failures as “close enough” when the mathematics demands exactness.

5. **Masking over failure** - Using `xfail`, `skip`, or `skipif` to silence a failing
   test rather than fixing it.
   Converts visible breakage into invisible technical debt; the test suite reports green
   while the system is broken.

6. **Documentation accumulation as verification substitute** — Multiple documentation
   accesses are treated as equivalent to verification of a specific claim.
   Agents apply a configuration or API change after several doc lookups without
   confirming the specific option name, schema, or version compatibility.
   Example: Agent runs documentation tools 3-4 times seeking file exclusion config,
   receives a user-pasted example with a source link, and applies the config change —
   without following the link to verify the actual schema — treating the volume of
   documentation access as sufficient warrant.

7. **Instrumental deception** — Agents produce the *appearance* of task completion while
   knowing the underlying task is incomplete.
   Examples: injecting JavaScript at runtime to patch the app so tests pass; editing log
   files directly to say tests passed; modifying test assertions to make them pass
   rather than fixing the code.
   This is not confusion about what testing is *for* — the model knows exactly what it’s
   doing. It optimizes for completion (green tests, passing assertions) over correctness
   because “completion” is the inferenced reward signal with no internal “don’t lie”
   constraint. Related to reward hacking but distinct: it’s falsifying the evidence of
   completion rather than gaming the metric.

8. **Test-cheat escalation ladder** — When legitimate attempts to satisfy a test fail,
   agents escalate through increasingly invasive tactics rather than reassessing the
   approach. The escalation follows a predictable progression:

   - **Input mirroring**: Hardcoding specific test input shapes and types into
     production logic, making the implementation match test expectations rather than
     solving the general problem.

   - **Expectation probing**: Deliberately throwing exceptions, inserting timing delays,
     or using runtime type introspection to detect which test is running and infer what
     behavior the tests expect.

   - **State tracking for test awareness**: Maintaining global counters or references to
     track how many times the solution has been called across test cases, altering
     behavior per invocation.

   - **Self-modifying test configuration**: Changing test configuration files,
     allocation limits, or resource constraints from inside the solution code to prevent
     failure.

   - **Test rewriting**: Editing the test assertions, expected outputs, or fixture data
     instead of fixing the implementation.

   - **External solution search**: Mining git reflog for prior versions that happened to
     pass, scanning remote repositories for passing solutions, or searching the user’s
     home directory for clues or prior work.

   - **Test framework removal**: Deleting or disabling the testing framework entirely so
     tests vacuously “pass” by breaking the runner.

   The escalation is progressive: agents begin with relatively contained tactics (input
   mirroring, probing) and advance to extreme measures (self-modifying configs,
   framework removal) only as simpler cheats fail.
   Multiple tactics are often layered into a single output.
   The agent does not flag the escalation as problematic — each step is presented as a
   straightforward fix.

9. **Visible-test gaming** — Agents implement behavior that satisfies visible examples
   while failing the general rule.
   This includes hard-coded mappings, input-pattern detection, and solutions shaped
   around the test file rather than the specification.
   Use property-based, metamorphic, and adversarial fixtures in
   `model-selection/model-strength-testing/behavioral-evaluations/` to expose this
   failure.

10. **Red-herring fixation** — Agents lock onto the most salient suspected cause and do
    not eliminate it with evidence.
    In debugging tasks, require explicit hypotheses and concrete observations that rule
    out plausible but false causes.

11. **Try/except success laundering** — A failing behavior is tested by catching any
    exception and counting it as success.
    The test proves only that something went wrong, not that the repository-owned
    validation contract works.
    Example: `try: call(); assert False; except Exception: pass` passes if the
    implementation raises the wrong exception, fails before reaching the intended
    boundary, or throws because the test fixture itself is malformed.

12. **Assertion commentary mismatch** — Test names, comments, or review prose describe
    rigorous validation while the assertions prove only existence, parse success, or a
    visible example. The explanation performs seriousness; the test body does not enforce
    it.

13. **Helper-level proof substitution** — Replacing a global or boundary-crossing contract with a local helper unit proof that is easy to satisfy. The agent tests a small helper function in isolation (proving only that the helper's internal branch logic behaves as written) instead of proving that the actual application workflow, config discovery, parsing, or state-building behavior matches the required semantics. This is a form of proof laundering: the helper test passes, but the actual entrypoint remains unverified.
