---
name: writing-readmes
description: Use when writing, reviewing, or improving a README file, especially when deciding what a repository entry point must tell consumers before they install, evaluate, or use it.
---

# Writing READMEs

Use this skill as the README-specific layer on top of `writing-documentation`.

The documentation skill owns the general workflow, style rules, and OSOT
policy. This skill owns the README acceptance contract: a README must let a
new consumer understand why the repo exists, decide whether it applies, install
it, run a first useful example, verify the result, and find deeper docs.

## Required Sequence

- Load `writing-documentation` first.
- Load `writing-documentation/reference/doc-types.md` and use its README
  section as the canonical structural source.
- Load `writing-documentation/reference/strunk-white-principles.md` for prose
  quality.
- Inspect the repository's public surfaces before rewriting: package metadata,
  CLI help, examples, docs, justfile or task runner, configuration schema, and
  existing README.
- Rewrite only after identifying the consumer path and the canonical sources
  that should be linked rather than duplicated.

## README Purpose

A README is the repository entry point for consumers and cloners.

It must answer:

- What is this repository?
- Why does it exist?
- Who should use it?
- What problem does it solve?
- What public interface does the user interact with?
- What prerequisites, credentials, permissions, or services are required?
- How does a user install it?
- How does a user run the smallest useful example?
- What output or behavior proves the example worked?
- What are the important limits, risks, unsupported cases, or maturity notes?
- Where should the reader go for reference, guides, architecture, operations,
  contributing, changelog, or support?

If a README cannot answer these, it has not done its job.

## Structure

Use the README section in `reference/doc-types.md` as the source of truth.
Adapt the order to the project, but preserve the reader path:

- Identify the project.
- Explain the concrete problem and audience.
- State status or maturity when it affects adoption.
- Show installation with prerequisites.
- Show quick start with expected output.
- Explain the main public capabilities when they are not obvious from the quick
  start.
- State configuration, credentials, permissions, persistence, network behavior,
  and data boundaries when relevant.
- State limits and unsupported cases.
- Link to canonical docs for details.
- State the license when applicable.

No section is mandatory by name.
Every required reader question must still be answered somewhere.

## OSOT For READMEs

Do not duplicate maintained reference material, but do not hide the first
usable path behind a link.

Include:

- the primary install command;
- the minimum viable command, import, API call, or workflow;
- required prerequisites and credentials;
- expected output or verification;
- one representative configuration example if configuration is required for
  first use;
- links to canonical references after the reader has enough context to choose
  them.

Link instead of copying:

- exhaustive CLI flag tables;
- complete API references;
- full configuration schemas;
- changelogs and release history;
- contributor workflows;
- architecture internals not required for first use;
- generated docs or help output.

Bad OSOT: "See docs" with no install or usage path.
Good OSOT: one runnable path in the README, then links to full references.

## What To Remove

Delete content that does not help a consumer decide, install, use, verify, or
understand boundaries:

- generic claims true of any project;
- marketing adjectives without evidence;
- popularity claims unless adoption itself changes the user's decision;
- badge walls and vanity badges;
- contributor process details better owned by `CONTRIBUTING.md`;
- full API or CLI references already generated elsewhere;
- internal function names, private modules, pipeline labels, or state paths the
  consumer never touches;
- development backstory unless it changes trust, status, or adoption risk;
- feature lists that do not explain the user-visible behavior.

Do not delete public names users must type: package names, commands, import
paths, public modules, public configuration keys, endpoint paths, file formats,
and documented state locations are consumer-facing facts.

## Public/Private Boundary Gate

Before keeping README material, identify:

- the ordinary noun for the artifact;
- the real reader and the decision or task they bring;
- the smallest complete input-to-output use case;
- the useful payload the README exposes before any governance or process material;
- which claims describe current behavior, future work, domain facts, or agent process.

Reject any README frame that requires private context before the reader can identify the
artifact, task, input, output, or evidence. Red flags include pass numbers, canonical
roots, custom status systems, ownership declarations, correction history, agent
instructions, prompt residues, and governance for roles or processes that do not exist
outside the agent workflow.

Do not repair a contaminated README by adding disclaimers such as "status lives
elsewhere" or "this README is not authoritative." If volatile status, agent-control
machinery, or correction history does not belong in the README, remove it and say
nothing. Public docs should not publish supervision history unless it changes adoption
risk for the reader.

## Evidence Rules

Every important claim needs evidence available to the reader.

- Performance claims need benchmark name, baseline, conditions, and result.
- Compatibility claims need versions or platforms.
- Security or privacy claims need the concrete mechanism or boundary.
- Production-readiness claims need the operational facts that make them true.
- "Works with X" needs setup or a link to setup.
- "Similar to X" is allowed only when it clarifies fit and states the
  difference.

If the evidence would be too long for the README, state the bounded result and
link to the canonical evidence.

## Surprises To Surface

State these before or near first use when they apply:

- required accounts, keys, tokens, or paid APIs;
- network calls and external services;
- local files, browser cookies, databases, caches, or credentials read;
- persistent state, generated files, and cache invalidation behavior;
- telemetry, analytics, or logging;
- destructive operations or writes outside the repository;
- unsupported platforms, data types, scale limits, or known failure modes;
- experimental, archived, internal-only, or unmaintained status.

## README Review Gate

Reject or rewrite a README when:

- it lacks installation or first-use instructions for a usable project;
- the quick start has no expected output or verification;
- it says what the project is but not why it exists;
- it describes internals before the consumer problem and public interface;
- it links to other docs instead of providing the entry path;
- it duplicates full reference material that has a canonical source;
- it hides credentials, network behavior, state, privacy, or destructive
  behavior;
- it uses arbitrary line limits to remove required facts;
- it has a "features" list where the reader still cannot tell what to do;
- it exposes agent-control machinery, correction history, private ontology, or
  invented institutional structure as if it were product documentation.

## Anti-Slop Rejection Patterns

> [!IMPORTANT]
> Any code, CLI examples, installation steps, or configuration options documented under this skill must adhere to the [Bridge-Burning Policies](file:///home/dzack/ai/opencode/skills/policy-index/SKILL.md#policy-registry) in `policy-index/SKILL.md`. These are non-negotiable hard constraints that eliminate runtime defaults, fallbacks, mocks, optional critical dependencies, and other agent validation-evasion pathways. Documented configuration options must represent a complete, fatal configuration regime rather than documenting default values or fallbacks in runtime logic.

Write READMEs that are honest, specific, and short.
Every sentence must earn its place.

## Core Policy

- A README answers: What is this?
  How do I use it?
  What do I need to know?
- Do not sell.
  Do not impress.
  Do not pad.
- If a sentence could be deleted without losing information, delete it.
- If a sentence is true of any project, delete it.

## Structural Requirements

A README needs at most these sections, in this order:

1. **Title** — project name only.
   No taglines.
2. **Description** — one to three sentences.
   What it is, what it does, who it's for.
3. **Installation** — exact commands.
   Prefer no-install solutions: `uvx`, `npx -y`, `curl | sh` when appropriate.
   No preamble.
4. **Usage** — minimal working example.
   Show, don't tell.
   Progressive disclosure: link to `--help`, doctor commands, or detailed docs rather than inlining everything.
5. **Configuration** — only if non-trivial defaults exist.
6. **License** — one line.

Everything else is optional and must justify its existence.

## What to Never Put in a README

### Marketing Language

Delete every instance of:

| Phrase | Why it's noise |
| --- | --- |
| "powerful" | Prove it or delete it |
| "flexible" | Prove it or delete it |
| "lightweight" | State the binary size or delete it |
| "blazingly fast" | State the benchmark or delete it |
| "modern" | Meaningless |
| "robust" | Meaningless |
| "seamless" | Meaningless |
| "battle-tested" | State the test count or delete it |
| "enterprise-grade" | Red flag, not a feature |
| "cutting-edge" | Meaningless |
| "revolutionary" | Almost never true |
| "game-changing" | Almost never true |
| "best-in-class" | Prove it or delete it |
| "industry-leading" | Prove it or delete it |
| "world-class" | Prove it or delete it |
| "next-generation" | Meaningless |
| "state-of-the-art" | Meaningless |
| "production-ready" | State what makes it so or delete it |
| "battle-hardened" | Meaningless |
| "rock-solid" | Meaningless |
| "effortless" | Meaningless |
| "intuitive" | Prove it or delete it |
| "elegant" | Subjective, delete it |

### Feature Counts as Flex

Delete:

- "50+ features"
- "100+ integrations"
- "1000+ stars"
- "10,000+ downloads"
- "Used by thousands of developers"
- Any claim where the number is the point

If a feature matters, describe it.
If a number matters, explain why.

### Vague Claims

Delete any sentence that could apply to any project:

- "This project is designed to make your workflow easier"
- "It provides a great developer experience"
- "It's easy to get started"
- "It works out of the box"
- "It's highly configurable"
- "It supports multiple platforms"
- "It's actively maintained"
- "It's well-documented"
- "Community-driven"

### Badge Spam

Badges are acceptable only if they answer a real question:

- Build status (CI pass/fail) — useful
- Version / npm version — useful
- License — useful
- Coverage — useful if relevant

Badges that are noise:

- "made with ❤️"
- "stars"
- "forks"
- "downloads"
- "PRs welcome"
- "contributions welcome"
- Any badge that exists to make the project look popular

Rule: max 4 badges.
If you need more, your README has a structural problem.

### Slop Phrases

Delete on sight:

- "Made with ❤️"
- "Don't forget to star this repo"
- "Powered by [framework]"
- "A modern, blazingly fast..."
- "Built with [tech stack list]"
- "Full-stack [thing]"
- "Batteries included"
- "Plug and play"
- "Zero config"
- "Out of the box"
- "It's like X for Y" (unless genuinely clarifying)
- "X on steroids"
- "The [thing] framework for [audience]"
- "Loved by developers"
- "Trusted by teams"
- "Ship faster"
- "Move fast"
- "Focus on what matters"
- "Stop wasting time on [boilerplate/infrastructure/etc]"
- "Finally, a [thing] that works"

### Corporate Jargon

Delete:

- "leverage" → use
- "utilize" → use
- "facilitate" → help
- "synergy" → delete entirely
- "paradigm" → delete entirely
- "ecosystem" → say what you mean
- "holistic" → delete entirely
- "streamline" → describe what you changed
- "empower" → delete entirely
- "deliver" → do or ship
- "solution" → describe the actual thing
- "space" → delete entirely (e.g., "the ML space")

### First-Person Narration

Do not write:

- "We built this because..."
- "I created this to solve..."
- "Our team needed..."
- "We believe..."
- "I think..."

State what the project does.
The backstory is noise.

### Acknowledgment Sections

Delete unless the project genuinely depends on specific upstream work:

- "Thanks to all contributors"
- "Shoutout to [person] for help"
- "Inspired by [thing]" (unless the inspiration is architecturally relevant)

## Theory of Mind

Write for the reader, not for yourself.

### The Reader Is Not You

The reader does not know your internals.
They do not know function names, variable names, module structure, or implementation strategy.
They arrived from a search engine or a link.
They are asking: "Is this the right tool for what I need?"

- Do not leak internal names.
  `fetch_raw`, `process_batch`, `load_config` are meaningless to readers.
  Describe what happens in plain language.
- Do not reference file formats, cache paths, or state directories unless the reader needs to interact with them.
- Do not assume the reader knows your dependency tree.
  "Powered by [library]" is noise unless the reader must configure that library.

### The README Is an Information Document, Not a Persuasive Piece

The reader's question is: "Should I use this?"
Not: "How impressive is this?"

A persuasive README actively obfuscates.
It replaces facts with claims, boundaries with hyperbole, and testability with slogans.
The reader walks away with a feeling ("this sounds powerful") instead of knowledge ("this solves X using Y, and I can verify it by doing Z").

Write so the reader can answer these questions:

1. **What problem does this solve?** — One sentence.
   The specific problem, not a category.
2. **What strategy does it use?** — The high-level approach, not a feature list.
3. **What is it similar to, and how does it differ?** — "It's like X for Y, but different because Z." Ground the reader in something they already know.
4. **How do I test it?** — Exact commands that produce inspectable output.
   "Run this, you'll see E, and if E matches your use case, it works."
5. **What are its limits?** — When does it break?
   What doesn't it do?
   What would make you NOT use it?

If the README can't answer these, it's not a README — it's a brochure.

### Agents Will Eat Your Slop

Many readers are AI agents.
They read your README and regurgitate it.
If your README says "a powerful, cutting-edge memory system with revolutionary compression-first philosophy," the agent will repeat that to its user.
The user asks "what does this repo do?"
and gets a fever dream of word salad — sci-fi adjectives, invented terminology, claims with no grounding.

This is not a hypothetical.
It is the default failure mode of persuasive READMEs on GitHub today.

Write so that an agent regurgitating your README produces a useful summary, not marketing copy.
That means:

- State the problem in plain language.
- State the strategy in plain language.
- State what it does and doesn't do.
- Avoid adjectives entirely.
- Avoid phrases that exist to impress rather than inform.

If an agent repeats your README back to a user, the user should get: "This solves X using Y. It's similar to Z but different because W. You can test it by running these commands."
Not: "This revolutionary system leverages cutting-edge compression-first philosophy to deliver state-of-the-art performance."

### The Reader Needs Boundaries, Not Claims

The reader does not need to be convinced.
They need to know the boundary of what this thing does so they can decide if it fits their problem.

A boundary is:
- "It handles text and images, not audio or video."
- "It requires an API key for X, but Y works without auth."
- "It's been tested on LoCoMo and Mem-Gallery, not on custom datasets."
- "It works when the input is under 10K tokens.
  Above that, it degrades."
- "It's similar to RAG-Mem but uses compression instead of re-ranking, which makes it faster but less precise on long-tail queries."

Claims without boundaries are useless.
"State-of-the-art on LoCoMo" tells the reader nothing unless they know what LoCoMo measures and what "state-of-the-art" means relative to what they need.

### Minimize Surprises

If the tool does something unexpected, say so upfront:

- "This reads your browser cookies" — say it, don't hide it.
- "This makes network calls to proprietary APIs" — say it.
- "This caches results and may serve stale data" — say it.
- "This requires [unexpected dependency]" — say it.

Surprises erode trust.
Honesty builds it.

### One Source of Truth

Do not duplicate information that lives elsewhere:

- **CLI help, `--help` flags, doctor commands** — do not re-document these in the README. The README should say "run `tool --help`" and move on.
  The CLI help is always current; the README is not.
- **Justfile recipes, Makefiles, package.json scripts** — do not copy recipe contents into the README. Put a "Development" section that says "run `just`" or "see `just --list`". The recipes are the source of truth.
- **Internal dev workflows** — do not publish contributor instructions, CI commands, release processes, or internal tooling in the README. That belongs in CONTRIBUTING.md or a developer guide.
  The README is for consumers and cloners, not contributors.

## Positive Patterns

These are the things that make a README work.

### State What It Does, Not What It Claims

Bad: "A powerful, modern tool for managing LLM usage across providers."
Good: "Uniform quota collection and rendering for CLI- and API-backed LLM providers."

The second sentence tells you exactly what it does.
You know if it's relevant to you.
No adjectives needed.

### Use Tables for Data, Not Decoration

Tables are good when you have structured data to aggregate:

| Provider | Strategy | How to set up |
| --- | --- | --- |
| Claude Code | OAuth credential | Run `claude login` |
| Cursor | SQLite database | Have Cursor installed |

Tables are bad when they're just badge walls or feature lists with no real data.

### Progressive Disclosure

Do not inline everything.
Link to live sources that are always current:

- `tool --help` instead of flag documentation
- `tool doctor` instead of troubleshooting steps
- CONTRIBUTING.md instead of dev workflow in README
- A docs site or wiki instead of a 500-line README

### Answer the Obvious Questions

If your tool does something surprising, explain it:

- "How does it get the data?"
  — especially for proprietary APIs.
  "Reads OAuth tokens from X" or "Scrapes using browser cookies" is honest and informative.
- "What does it cache and for how long?"
  — if caching exists, say so.
- "What permissions does it need?"
  — if it reads files or makes network calls, say so.

### Lists Are for Delineation, Not Bragging

A provider list answers: "Does this support what I use?"
It is not an achievement.
Do not enumerate unsupported things — that's implicit.
Do not add checkmarks or emojis to make the list look impressive.

### The Agent Amplification Loop

**Pattern:** Persuasive README slop gets regurgitated by agents as fact.

**Bad:**
> "A revolutionary memory system leveraging cutting-edge compression-first philosophy to deliver state-of-the-art performance on long-context tasks."

**What happens:** An agent reads this, a user asks "what does this repo do?", and the agent replies: "This is a revolutionary memory system that uses cutting-edge compression-first philosophy to deliver state-of-the-art performance."
The user now believes something they cannot verify, based on claims that mean nothing.

**Why it fails:** The README was written to impress, not to inform.
The agent has no mechanism to distinguish claims from facts.
It repeats what it reads.
The persuasive language becomes a self-amplifying loop of meaningless superlatives.

**Instead:** Write so that an agent regurgitating your README produces a useful summary.
> "SimpleMem stores and retrieves long-context memory.
> It compresses text at ingestion to reduce token usage, then retrieves relevant segments at query time.
> It scored 71.2 F1 on LoCoMo, versus 56.3 for the next-best system.
> It handles text and images, not audio or video."

The agent now repeats something the user can act on.

## Anti-Patterns with Case Studies

Each anti-pattern below is drawn from real AI slop.
The pattern name, a concrete example, why it fails, and what to write instead.

### 1. Feature Enumeration as Architecture

**Pattern:** Listing components as if naming them explains them.

**Bad:**
> "Selective Ingestion (entropy-driven filtering per modality), Progressive Retrieval (hybrid FAISS + BM25 with pyramid token-budget expansion), and Knowledge Graph Augmentation (multi-hop cross-modal reasoning)."

**Why it fails:** The reader finishes this and knows the system has three named features but not what any of them do, why they exist, or how they interact.
"pyramid token-budget expansion" describes a component by its own internal name.
It explains nothing.

**Instead:** Describe what the system does for the reader.
> "The system filters incoming data by relevance before storing it, retrieves information using both semantic and keyword search, and links related concepts across different input types."

If the reader needs implementation details, link to architecture docs.

### 2. Benchmarks Without Context

**Pattern:** Stating a number with no reference point.

**Bad:**
> "On the LoCoMo benchmark this delivers a 26.4% average F1 gain over prior systems while cutting inference-time token consumption by roughly 30x."

**Why it fails:** Which prior systems?
Under what conditions?
What was the baseline score?
Is 26.4% on a task that matters?
The number exists to impress, not to inform.
A reader cannot evaluate whether this matters for their use case.

**Instead:** State the number, the baseline, the conditions, and why the reader should care.
> "On LoCoMo, SimpleMem scores 71.2 F1 versus 56.3 for the next-best system (RAG-Mem), using 30x fewer tokens.
> This matters because LoCoMo tests long-conversation memory, which is the bottleneck for most production chatbots."

If the benchmark is not widely known, explain what it measures.

### 3. Development Narrative as Contribution

**Pattern:** The main selling point is how the system was built, not what it does.

**Bad:**
> "Its architecture was discovered by an autonomous research pipeline that ran around 50 experiments across two benchmarks, diagnosing failure modes, proposing architectural changes, and even repairing data-pipeline bugs with no human in the inner loop."

**Why it fails:** The contribution isn't the system — it's that the system was built by another system.
That's a demo of the build tool, not a description of the product.
The reader came to understand what this does for them, not how it was developed.

**Instead:** Describe what the system does.
If the build process is interesting, put it in a separate "Development" or "How This Was Built" section — but lead with the product.

### 4. Editorializing Results

**Pattern:** Telling the reader what to think about your data.

**Bad:**
> "Tellingly, the bug fixes and architectural changes each contributed more than all hyperparameter tuning combined, taking the system from a naive baseline to state-of-the-art on both LoCoMo and Mem-Gallery."

**Why it fails:** "Tellingly" is the author narrating their own results.
Technical writing presents data and lets the reader draw conclusions.
This tells a story where the conclusion is predetermined: "look how well this worked."

**Instead:** State the finding.
> "Bug fixes and architectural changes contributed more to performance than hyperparameter tuning.
> On LoCoMo, this moved the system from 45.1 to 71.2 F1; on Mem-Gallery, from 38.7 to 62.9 F1."

### 5. Taglines Instead of Integration

**Pattern:** Replacing technical explanation with a product slogan.

**Bad:**
> "One package, one mental model: compress losslessly, retrieve by intent, and let the system keep improving itself."

**Why it fails:** The actual integration question — how do these three systems share state, how does the multimodal backend route, how does EvolveMem's feedback loop interact with SimpleMem's compression — is completely absent.
"One mental model" is a marketing claim, not an architectural description.

**Instead:** Describe the integration.
> "`from simplemem import SimpleMem` loads the text core.
> Calling `simplemem.optimize()` starts EvolveMem's feedback loop, which reads SimpleMem's retrieval logs and adjusts scoring weights.
> The multimodal backend is lazy-loaded only when non-text inputs are detected."

### 6. Jargon That Self-References

**Pattern:** Naming components in a way that only makes sense if you already know the internals.

**Bad:**
> "Mechanism details (hybrid index layers, compression examples, retrieval planning): SimpleMem text memory"

**Why it fails:** "Mechanism details" signals "here's how it works" but then delivers internal names.
"hybrid index layers" — what kind of index?
what's hybrid about it?
"compression examples" — examples of what?
"retrieval planning" — planning what?
The reader has no entry point.

**Instead:** Use language the reader brings with them.
> "SimpleMem stores text in a compressed index that combines keyword and semantic search.
> It plans retrieval by estimating how much context the query needs and pulling only that much."

### 7. Vague Quantification

**Pattern:** Approximate numbers that exist to sound precise without being accountable.

**Bad:**
> "ran around 50 experiments", "roughly 30x", "more than all hyperparameter tuning combined"

**Why it fails:** "around 50" — is it 50? 47? 53? "roughly 30x" — is it 28x? 35x? The imprecision signals the number exists to impress, not to be scrutinized.
If you don't know the exact number, don't state it.

**Instead:** Use exact numbers, or say "approximately" and give a range.
> "The pipeline ran 47 experiments over 12 days."
> or "token consumption is 28-32x lower, depending on query complexity."

### 8. Emoji Section Headers

**Pattern:** Using emoji to decorate section headers.

**Bad:**
> "🧠 Omni-SimpleMem: multimodal memory" "🧬 EvolveMem: self-evolving retrieval"

**Why it fails:** This is a product landing page, not a research contribution.
Emoji headers signal "we're trying to make this feel exciting" rather than "we're trying to make this clear."

**Instead:** Use plain headers.
> "## Multimodal Memory" "## Self-Evolving Retrieval"

### 9. The "Fits Together" Section That Doesn't Explain Integration

**Pattern:** A section titled "how they fit together" that contains a code snippet and a slogan.

**Bad:**
> "from simplemem import SimpleMem gives you the text core with automatic routing to the multimodal backend, and simplemem.optimize(...) taps EvolveMem to tune retrieval for your own data."

**Why it fails:** This describes the API surface, not the integration.
What does "automatic routing" mean?
When does it route?
What triggers EvolveMem?
What data does it read?
The reader knows what function to call but not what happens when they call it.

**Instead:** Describe the mechanism, then show the code.
> "SimpleMem routes to the multimodal backend when input contains images or audio.
> EvolveMem reads SimpleMem's retrieval logs every N queries and adjusts scoring weights.
> Here's how to enable both:"
>
> ```python
> from simplemem import SimpleMem
> mem = SimpleMem(multimodal=True, evolve=True)
> ```

### 10. Selling the Feature List

**Pattern:** Describing a system as a list of impressive-sounding capabilities without explaining what they do.

**Bad:**
> "Selective Ingestion (entropy-driven filtering per modality), Progressive Retrieval (hybrid FAISS + BM25 with pyramid token-budget expansion), and Knowledge Graph Augmentation (multi-hop cross-modal reasoning)."

**Why it fails:** This is a brochure, not documentation.
The reader doesn't know which of these features matters for their use case, or whether any of them work well.
The list exists to make the system sound comprehensive.

**Instead:** Lead with the problem, not the features.
> "Most memory systems store everything and retrieve by relevance, which wastes tokens on irrelevant context.
> SimpleMem filters at ingestion time, so only relevant data is stored and retrieved."

Then, if the features matter, describe what each one does for the reader.

## Structural Anti-Patterns (Document-Level)

### The "Everything README"

A README that includes: full API reference, architecture diagram, contributing guide, changelog, FAQ, comparison table, roadmap, and a blog post.
Split it up.
Link to separate docs.

### The "Nothing README"

A README with: project name, one line of text, and a badge wall.
No installation, no usage, no example.
Worse than no README.

### The "Testimonial README"

A README that quotes users saying how great the project is.
This is marketing, not documentation.

### The "Comparison README"

A README that spends 80% of its length comparing itself to competitors.
State the difference in one sentence.
Link to a detailed comparison doc if needed.

### The "Philosophy README"

A README that opens with 500 words about why the author is dissatisfied with existing tools.
Get to the point.

## Validation Checklist

- [ ] `writing-documentation` was loaded and followed.
- [ ] `reference/doc-types.md` supplied the README structure.
- [ ] The README states the concrete problem and audience.
- [ ] The README explains why the repo exists.
- [ ] Installation includes prerequisites and verification.
- [ ] Quick start is runnable and includes expected output or observable
      behavior.
- [ ] Required public names are present.
- [ ] Credentials, permissions, network behavior, persistence, and data
      boundaries are disclosed when relevant.
- [ ] Limits, unsupported cases, and maturity are stated when they affect use.
- [ ] Canonical references are linked instead of duplicated.
- [ ] No arbitrary length rule removed information required by the consumer.
