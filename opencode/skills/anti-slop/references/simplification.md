---
name: simplification
description: |
  Reference for reports specifically geared toward reducing owned surface.
  Start with the longest and most complex app-owned functions, determine whether
  the logic can be offloaded to a dependency, binary, CLI, or external program.
---

# Simplification

The goal: reduce the code the app owns by delegating logic to dependencies, system
binaries, CLI tools, shell built-ins, or external programs. The ideal app is glue.

## Process

1. **List the longest and most complex app-owned functions.** Sort by LOC or cyclomatic
   complexity. These are the candidates with the highest potential for elimination.

2. **Categorize what each function actually does.** Not how it does it — what
   observable, user-facing behavior does it power? Parse a file format? Transform data?
   Manage a process? Render output?

3. **Determine whether something external can obviate the owned logic.** For each
   function, ask: does a library, system binary, CLI tool, installed dependency, shell
   built-in, or language primitive already handle this category of work? Check the
   codebase's existing dependencies, the system's installed tools, and well-known
   libraries for the language.

4. **Map the tradeoff.** The question is never "is there a turnkey drop-in replacement?"
   It is: can the user have a similar experience without the app owning this logic?

   - **Same functionality, offloaded logic** — the clear winner. Delete the owned code,
     delegate to the external tool.
   - **Slightly altered interface** — requires analysis. If offloading changes how the
     user interacts with the feature, weigh the reduction in owned surface against the
     interface change. Offloading is still strongly preferred.
   - **Degraded or dropped feature** — typically a no-go, but must be discussed in the
     report. The analysis itself is valuable even if the conclusion is "keep."

5. **For each candidate, ask the origin question.** Why was this code introduced? What
   specific user request produced it? This is the narrative the report must provide —
   not just "this code is complex" but "this code was produced by an agent responding to
   a request for X, and the agent defaulted to implementing X from scratch instead of
   finding    whether X was already solved."

## Concrete example: the Ctrl+P popup

A user requested a Ctrl+P file/command palette in their app. An agent implemented a
bespoke in-app popup — input box, fuzzy matcher, result list, keyboard navigation. The
agent called it "clean," "minimal," "elegant." It was 100+ LOC of owned UI logic.

The correct answer: `fzf` or `dmenu`. These are mature, battle-tested external tools
that provide essentially the same behavior — fuzzy-filtered selection from a list with
keyboard navigation. The integration is a shell pipe: pipe a list of options into `fzf`,
read the selection from stdout.

The interface is not identical to VSCode's Ctrl+P. It opens in a terminal overlay or a
separate window. But the user gets essentially the same experience using tools they
already know — `fzf` is part of their daily workflow. The "cost" is declaring `fzf` as a
hard dependency, but that cost is zero: `fzf` is already installed on this system, fully
configured to the user's preferences.

Integrating with the user's existing environment and preferred tools is better than an
in-app bespoke solution. The user gets behavior consistent with what they already use
everywhere else. The app sheds 100+ LOC. The finding writes itself: delete the owned
popup, pipe through `fzf`.

## Concrete example: tilde expansion and shell requirements

An app stored paths like `~/my_folder` in an early config file. This required tilde
expansion. Code sprawled: bespoke regex-based tilde expansion, manual argument parsing,
flag handling for CLI invocations. A first review correctly identified the regex as slop
but suggested replacing it with a library — a myopic fix that still owns the logic.

The actual question: why is tilde expansion needed at all? The app was passing paths to
`sh -c` — an imaginary-user decision from the agent's enterprise training data. No one
asked: what shell does the user have on THIS system? The answer: `zsh`. There is a
`.zshrc` file. `zsh` handles tilde expansion natively and robustly. Declare `zsh` as a
hard requirement and delete every line of expansion and parsing code.

Even if this system didn't use `zsh`: `zsh` is trivially installable. Package
installation is robust, free, takes seconds, and is extremely well-supported. The
correct design philosophy is inverted from what the agent assumed: create an app with
many tight requirements and relax them later, introducing bespoke code only when a real
user request demands the relaxation. Do not let the agent preemptively relax
requirements on behalf of an imaginary unknown user.

The finding: delete `expand_tilde_in_command`, `parse_cli_args`, the `regex_lite`
dependency, and all associated logic. Use `zsh -c`. The owned surface drops to zero for
an entire category of functionality.

## Concrete example: regex as slop by default

Regex is a high-probability slop pattern. Most modern apps do not use complex regex.
Regex belongs in parsers, lexers, and compilers — none of which we build. If regex
appears in application code, it is almost certainly a hack to avoid proper contracts,
types, or a dependency.

String manipulation is extremely brittle, error-prone, and inscrutable to non-experts.
A tiny logic change can often obviate regex entirely. Example: a pandoc Lua filter
trying to match `:::{.remark}` lines with a complex regex attempting to capture the
exact syntax. The regex is essentially reinventing a leaf of the pandoc parser. The
replacement: `":::" in line and "remark" in line` — a simple containment conjunction
that is correct 99.99% of the time for actual written documents on this system. It is
infinitely simpler to read, maintain, and debug.

If the user HAPPENS to encounter the 0.01% edge case, they can normalize their data or
come back and request a fix — and then the complexity is warranted, documented, and
evidenced by explicit tests from real-world data. This is how software IS developed:
not by predicting edge cases, but by implementing the simple, correct, maintainable
solution and adding complexity only when real-world cases demand it.

When you encounter regex, ask: is it reinventing parsing that a library or external
tool already handles? Is there a semantic parser for this data type? Is the app hacking
raw strings to avoid setting up proper contracts, boundaries, and types? Is it avoiding
a dependency? Can the string search be replaced with simple containment checks,
possibly broken into cases, that work for the typical data on this system? The original
agent over-optimized for imagined edge cases and never ensured the happy path was
heavily tested before diving into speculative errors.

## Concrete example: ground-up reimplementation of a runtime primitive

```typescript
async function blobToBase64(blob: Blob) {
  const bytes = new Uint8Array(await blob.arrayBuffer());
  let binary = '';
  for (const byte of bytes) {
    binary += String.fromCharCode(byte);
  }
  return btoa(binary);
}
```

The browser already has `FileReader.readAsDataURL()`. The entire function — Uint8Array,
byte iteration, `String.fromCharCode`, `btoa` — is a ground-up reimplementation of an
API the agent never looked up. The fix is two lines wrapping `FileReader`. The function
should not exist.

The immediate red flags, visible without knowing `FileReader` or even the language:

- **Byte-level manipulation.** `Uint8Array`, `byte`, `arrayBuffer` — application code
  at the byte level. Never glue.
- **Manual iteration and accumulation.** `for` loop building a string byte-by-byte.
  First-principles implementation, not composition.
- **Format conversion between standard types.** `Blob` → `base64`. Both are web
  platform primitives. Conversion between standard formats is always solved.
- **Zero imports, zero dependencies.** No external calls. Pure language primitives.
  The function reinvents from nothing.
- **String concatenation in a loop.** `binary += ...` in a loop. Not just a
  performance issue — it proves the agent wrote the algorithm itself instead of
  finding the library call.

None of these signals require knowing the specific fix. The function's *shape* is the
slop. The correct decompilation exercise: "does anything in this runtime already
convert blobs to base64?" The answer is one search query away. The agent never asked.

Each finding must include:

- **The function** — file:line, LOC, what it does.
- **The user-facing behavior it powers** — the concrete feature a user experiences.
- **Delegation analysis** — every external tool, library, binary, or system capability
  that could absorb this concern, with explicit evaluation of each.
- **Tradeoff assessment** — same functionality, altered interface, or degraded feature.
- **Origin** — the likely user request and agent psychology that produced the owned
  implementation.
- **Recommendation** — delegate or keep, with justification.
