---
name: anti-slop
description: Comprehensive toolkit for detecting and eliminating "AI slop" - generic, low-quality AI-generated patterns in natural language, code, and design. Use when reviewing or improving content quality, preventing generic AI patterns, cleaning up existing content, or enforcing quality standards in writing, code, or design work.
---
# Anti-Slop Skill

Detect and eliminate generic AI-generated patterns ("slop") across natural language,
code, and design.

## What is AI Slop?

AI slop refers to telltale patterns that signal low-quality, generic AI-generated
content:

- **Text**: Overused phrases like “delve into,” excessive buzzwords, meta-commentary

- **Code**: Generic variable names, obvious comments, unnecessary abstraction

- **Design**: Cookie-cutter layouts, generic gradients, overused visual patterns

This skill helps identify and remove these patterns to create authentic, high-quality
content.

## When to Use This Skill

Apply anti-slop techniques when:

- Reviewing AI-generated content before delivery

- Creating original content and want to avoid generic patterns

- Cleaning up existing content that feels generic

- Establishing quality standards for a project

- User explicitly requests slop detection or cleanup

- Content has telltale signs of generic AI generation

## Core Workflow

### 1. Detect Slop

**For text files:**

```bash
python scripts/detect_slop.py <file> [--verbose]
```

This analyzes text and provides:

- Slop score (0-100, higher is worse)

- Specific pattern findings

- Actionable recommendations

**Manual detection:** Read the appropriate reference file for detailed patterns:

- `references/text-patterns.md` - Natural language slop patterns

- `references/code-patterns.md` - Programming slop patterns

- `references/design-patterns.md` - Visual/UX design slop patterns

### 2. Clean Slop

**Automated cleanup (text only):**

```bash
# Preview changes
python scripts/clean_slop.py <file>

# Apply changes (creates backup)
python scripts/clean_slop.py <file> --save

# Aggressive mode (may slightly change meaning)
python scripts/clean_slop.py <file> --save --aggressive
```

**Manual cleanup:** Apply strategies from the reference files based on detected
patterns.

## Text Slop Detection & Cleanup

### High-Priority Targets

**Remove immediately:**

- “delve into” → delete or replace with “examine”

- “navigate the complexities” → “handle” or delete

- “in today’s fast-paced world” → delete

- “it’s important to note that” → delete

- Meta-commentary about the document itself

**Simplify wordy phrases:**

- “in order to” → “to”

- “due to the fact that” → “because”

- “has the ability to” → “can”

**Replace buzzwords:**

- “leverage” → “use”

- “synergistic” → “cooperative”

- “paradigm shift” → “major change”

### Quality Principles

**Be direct:**

- Skip preambles and meta-commentary

- Lead with the actual point

- Cut transition words that don’t add meaning

**Be specific:**

- Replace generic terms with concrete examples

- Name specific things instead of “items,” "things," “data”

- Use precise verbs instead of vague action words

**Be authentic:**

- Vary sentence structure and length

- Use active voice predominantly

- Write in a voice appropriate to context, not corporate-generic

## Code Slop Detection & Cleanup

### High-Priority Targets

**Rename generic variables:**

- `data` → name what data it represents

- `result` → name what the result contains

- `temp` → name what you’re temporarily storing

- `item` → name what kind of item

**Remove obvious comments:**

```python
# Bad
# Create a user
user = User()

# Better - let code speak
user = User()
```

**Simplify over-engineered code:**

- Remove unnecessary abstraction layers

- Replace design patterns used without purpose

- Simplify complex implementations of simple tasks

**Improve function names:**

- `handleData()` → what are you doing with data?

- `processItems()` → what processing specifically?

- `manageUsers()` → what management action?

### Quality Principles

**Clarity over cleverness:**

- Write code that’s easy to understand

- Optimize only when profiling shows need

- Prefer simple solutions to complex ones

**Meaningful names:**

- Variable names should describe content

- Function names should describe action + object

- Class names should describe responsibility

**Appropriate documentation:**

- Document why, not what

- Skip documentation for self-evident code

- Focus documentation on public APIs and complex logic

## UX Anti-Pattern Detection

Frontend UX anti-patterns that cause measurable user harm.
Full detection heuristics with code examples in
[`references/ux-antipatterns.md`](references/ux-antipatterns.md).

### Core Axioms

Before checking individual rules, internalize these.
They are the “why” behind every item.

| # | Axiom | One-liner |
| --- | --- | --- |
| 1 | **Acknowledge every action** | Every user action must produce visible feedback within 100ms, even if the result takes seconds. |
| 2 | **Never destroy user input** | Not on error, not on navigation, not on timeout, not on refresh. |
| 3 | **State survives the unexpected** | Refresh, double-clicks, network loss — code must handle edge cases. |
| 4 | **Most recent intent wins** | Stale responses must never overwrite a newer user action. |
| 5 | **Explain every constraint** | If it’s disabled, say why. If it failed, say how to fix it. |
| 6 | **Don’t fight the platform** | Browser conventions, OS gestures, native controls, and accessibility APIs encode billions of hours of UX research. |

### Anti-Pattern Categories

| # | Category | User Harm |
| --- | --- | --- |
| 1 | Layout Stability | Click target moves; wrong thing clicked. |
| 2 | Feedback & Responsiveness | Action feels ignored; user retries or loses trust. |
| 3 | Error Handling & Recovery | User stuck with no way forward; input destroyed. |
| 4 | Forms & Input Interference | Platform fights the user’s typing; data mangled. |
| 5 | Focus | User is typing and the UI yanks them elsewhere. |
| 6 | Notifications, Interruptions & Dialogs | User’s flow broken; forced to parse ambiguous choices under pressure. |
| 7 | Navigation, Routing & State Persistence | User can’t go back; context evaporates on refresh or redirect. |
| 8 | Scroll & Viewport | Content unreachable or unstable; user fights the interface to see what they came for. |
| 9 | Timing, Debounce & Race Conditions | Actions fire twice, responses arrive stale. |
| 10 | Accessibility as UX | Entire interaction modes broken — keyboard users can’t navigate, touch users locked out. |
| 11 | Visual Layering & Rendering | UI elements overlap, clip, or hide each other. |
| 12 | Mobile & Viewport-Specific | Keyboard covers input, layout jumps on scroll. |
| 13 | Cumulative Decay & Long-Term UX | App degrades over time; preferences lost, performance rots. |

### Symptom → Category Quick Reference

| User complaint / code smell | Category |
| --- | --- |
| “Button does nothing when I click it” | 2. Feedback & Responsiveness |
| “I clicked the wrong thing — it moved” | 1. Layout Stability |
| “I lost my form data” | 4. Forms & Input Interference |
| “It says 'Something went wrong' with no explanation” | 3. Error Handling & Recovery |
| “The page jumped while I was typing” | 5. Focus |
| “I got the same notification 5 times” | 6. Notifications & Dialogs |
| “I logged in and it forgot where I was going” | 7. Navigation & State Persistence |
| “I scrolled back and lost my place” | 8. Scroll & Viewport |
| “My order was placed twice” | 9. Timing & Race Conditions |
| “I clicked delete and it just … deleted it” | 6. Notifications & Dialogs |
| “It’s been loading for 2 minutes with no progress bar” | 2. Feedback & Responsiveness |
| “I can’t use this with my keyboard” | 10. Accessibility as UX |
| “The dropdown is hidden behind the modal” | 11. Visual Layering |
| “The keyboard covers the input on my phone” | 12. Mobile & Viewport-Specific |
| “The app gets slower over time” | 13. Cumulative Decay |

### Common Mistakes

- **Flagging style preferences as anti-patterns.** A non-standard button shape is a
  design choice, not a UX violation.
  Only flag patterns that cause measurable user harm per the axioms.

- **Ignoring context.** A disabled button inside a wizard step IS explained by the
  wizard’s own flow. Check for nearby explanatory elements before reporting.

- **Suggesting fixes that break accessibility.** A fix that adds a visual indicator but
  removes keyboard access trades one violation for another.
  Verify fixes against Axiom 6.

- **Over-reporting on handled edge cases.** If the code already has an AbortController,
  don’t flag it for race conditions.
  Read the implementation before reporting.

- **Reporting framework internals as violations.** React’s `key` prop remounts, Next.js
  loading states, or SvelteKit form actions may handle anti-patterns at the framework
  level. Understand the framework before flagging.

## Reference Files

Consult these comprehensive guides when working on specific domains:

- **[text-patterns.md](references/text-patterns.md)** - Complete catalog of natural
  language slop patterns with detection rules and cleanup strategies

- **[code-patterns.md](references/code-patterns.md)** - Programming antipatterns across
  languages with refactoring guidance.
  Includes the **Introspection Red Flags** framework for `isinstance`, `hasattr`,
  `getattr`, `type()`, `issubclass`, `callable()` — ask why the code is guessing about
  shapes at runtime instead of asserting them through the type system.

- **[test-patterns.md](references/test-patterns.md)** - Testing slop patterns
  (content-free checks, tautologies, masking)

- **[design-patterns.md](references/design-patterns.md)** - Visual and UX design slop
  patterns with improvement strategies

- **[ux-antipatterns.md](references/ux-antipatterns.md)** - Frontend UX anti-pattern
  detection heuristics covering layout shifts, silent failures, double-submits, focus
  theft, missing feedback, and cumulative decay — with code-level detection signals and
  concrete fixes. (Source:
  [cassiozen/UX-antipatterns](https://github.com/cassiozen/UX-antipatterns))

Each reference includes:

- Pattern definitions and examples

- Detection signals (high/medium confidence)

- Context where patterns are acceptable

- Specific cleanup strategies

### Repo-Specific Extensions

The global patterns in this skill are sharpened for specific repos:

- **research repo** (`~/research`): Load `research-code-style` for repo-specific rules
  on assertions, optional types, semantic membership checks, and mathematical
  preconditions. Load `category-spec-style` for the audit rubric on runtime checks
  outside categorical predicates.
  Load `jerry-behaviour` to prevent checklist theater and paraphrase-as-review when
  evaluating agent-produced work.

## Scripts

### detect_slop.py

Analyzes text files for AI slop patterns.

**Usage:**

```bash
python scripts/detect_slop.py <file> [--verbose]
```

**Output:**

- Overall slop score (0-100)

- Category-specific findings

- Line numbers and examples

- Actionable recommendations

**Scoring:**

- 0-20: Low slop (authentic writing)

- 20-40: Moderate slop (some patterns)

- 40-60: High slop (many patterns)

- 60+: Severe slop (heavily generic)

### clean_slop.py

Automatically removes common slop patterns from text files.

**Usage:**

```bash
# Preview changes
python scripts/clean_slop.py <file>

# Save changes (creates backup)
python scripts/clean_slop.py <file> --save

# Save to different file
python scripts/clean_slop.py <file> --output clean_file.txt

# Aggressive mode
python scripts/clean_slop.py <file> --save --aggressive
```

**What it cleans:**

- High-risk phrases

- Wordy constructions

- Meta-commentary

- Excessive hedging

- Buzzwords

- Redundant qualifiers

- Empty intensifiers

**Safety:**

- Always creates `.backup` file when overwriting

- Preview mode shows changes before applying

- Preserves content meaning (non-aggressive mode)

## Best Practices

### Prevention Over Cure

**When creating content:**

1. Write with specific audience in mind

2. Use concrete examples over abstractions

3. Lead with the point, skip preambles

4. Choose words for precision, not impression

5. Review before considering it complete

### Context-Aware Cleanup

Not all patterns are always slop:

**Acceptable contexts:**

- Academic writing may need more hedging

- Legal documents require specific phrasing

- Internal documentation can use shortcuts

- Technical docs have domain-specific conventions

**Always consider:**

- Who is the audience?

- What is the purpose?

- Does this pattern serve a function?

- Is there a better alternative?

### Iterative Improvement

1. **Detect** - Run detection scripts or manual review

2. **Analyze** - Understand which patterns are truly problems

3. **Clean** - Apply automated cleanup where safe

4. **Review** - Manually verify changes maintain meaning

5. **Refine** - Fix remaining issues by hand

### Quality Over Automation

The scripts are tools, not replacements for judgment:

- Use automated detection to find candidates

- Apply automated cleanup to obvious patterns

- Manually review anything that changes meaning

- Exercise discretion based on context

## Integration Patterns

### Code Review

```bash
# Check files before committing
python scripts/detect_slop.py src/documentation.md --verbose

# Clean up automatically
python scripts/clean_slop.py src/documentation.md --save
```

### Content Pipeline

1. Create initial content

2. Run slop detection

3. Apply automated cleanup

4. Manual review and refinement

5. Final quality check

### Standards Enforcement

Create project-specific thresholds:

- Max acceptable slop score: 30

- Required manual review for scores > 20

- Auto-reject submissions with scores > 50

## Limitations

**Scripts only handle text:**

- Code slop detection is manual (use code-patterns.md)

- Design slop detection is manual (use design-patterns.md)

**Context sensitivity:**

- Scripts can’t understand all contexts

- Some “slop” may be appropriate in certain domains

- Always review automated changes

**Language coverage:**

- Detection patterns optimized for English

- Code patterns focus on common languages (Python, JS, Java)

- Design patterns are platform-agnostic

## Common Scenarios

### Scenario 1: Review AI-Generated Content

```bash
# User asks: "Can you review this article for AI slop?"
1. Read references/text-patterns.md for patterns to watch
2. Run: python scripts/detect_slop.py article.txt --verbose
3. Review findings and apply manual cleanup
4. Optionally run: python scripts/clean_slop.py article.txt --save
5. Do final manual review of cleaned content
```

### Scenario 2: Clean Up Codebase

```bash
# User asks: "Help me clean up generic AI patterns in my code"
1. Read references/code-patterns.md
2. Review code files manually for patterns
3. Create list of generic names to rename
4. Refactor following principles in code-patterns.md
5. Remove obvious comments and over-abstractions
```

### Scenario 3: Design Review

```bash
# User asks: "Does this design look too generic?"
1. Read references/design-patterns.md for the full pattern catalog
2. Check against high-confidence slop indicators
3. Identify specific issues (gradients, layouts, copy)
4. Provide specific recommendations from design-patterns.md
5. Suggest concrete alternatives
```

### Scenario 4: Frontend UX Review

```bash
# User asks: "Review this React component for UX issues"
1. Load references/ux-antipatterns.md for the full detection heuristics
2. Check each applicable anti-pattern category against the code
3. For each finding, state: the anti-pattern name, the user harm, and a concrete fix
4. Reference the core axioms to explain *why* it's a problem
5. Verify fixes don't violate other axioms (especially accessibility)
6. If no anti-patterns are found, state that the code is clean
```

### Scenario 5: Establish Quality Standards

```bash
# User asks: "Help me create quality standards for our team"
1. Review all three reference files
2. Identify patterns most relevant to user's domain
3. Create project-specific guidelines
4. Set up detection scripts in development pipeline
5. Document acceptable exceptions
```

## Tips for Success

**For text cleanup:**

- Run detection first to understand scope

- Use non-aggressive mode for important content

- Always review automated changes

- Focus on high-risk patterns first

**For code cleanup:**

- Start with renaming generic variables

- Remove obvious comments next

- Refactor over-engineered code last

- Test after each significant change

**For design cleanup:** See `references/design-patterns.md` for the full catalog,
detection signals, and cleanup strategies.

**General principles:**

- Quality > uniformity

- Context > rules

- Clarity > cleverness

- Specificity > generality

## Cross-References

- **jerry-behaviour** → Load alongside when evaluating whether slop-detection is working
  at the review level.
  Anti-slop detects the surface patterns (generic names, obvious comments, unnecessary
  abstraction). Jerry-behaviour detects the meta-level failure: evaluators who cannot
  recognize slop because they share the same slop-generating priors.

- **llm-failure-modes** → Load alongside when investigating why slop was produced.
  Many slop patterns stem from underlying cognitive failures — overconfidence,
  confabulation, premature solution generation, replacement instinct.
  Understanding these helps distinguish genuine quality issues from normal variation.

- **addressing-shallow-work** → Load alongside when the slop is structural rather than
  cosmetic. The deepest form of slop is code that destroys the abstraction before
  operating (regex-on-HTML, serialization-before-search).
  Surface-level cleanup cannot fix structurally wrong approaches.

- **ux-antipatterns** (reference) → Load alongside when reviewing frontend UI code.
  Detects user-facing patterns (layout shifts, silent failures, focus theft) that
  frustrate users but may not look like “code slop” to a reviewer focused on naming or
  abstraction quality.
