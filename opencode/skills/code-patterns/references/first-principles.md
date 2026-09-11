# First Principles

The principles below decide most design questions before any domain knowledge is
applied. They are not code rules: the same principle settles where a method goes, who
owns a fact, what a test asserts, what a wiki page is for, and what an engine may
hard-code. Each is stated generally, then shown in several domains, because a principle
recognized in only one domain has not been learned.

Parent: [[code-patterns/general/general|general patterns]].

## 1. One Fact, One Owner

Every fact, rule, and behavior has exactly one place that owns it. Everywhere else
refers to that place.

Two owners is not redundancy; it is a contradiction waiting to be discovered, because
nothing keeps them equal. The second copy is usually written because reaching the first
was inconvenient at that moment.

- Declaring a catalogue in one file and asserting its contents in another tests that two
  hand-written lists agree. It proves nothing about the subject.
- A document that restates what a repository's code, plans, or issues already own goes
  stale the moment either moves, and the reader cannot tell which is current.
- Migrating material and keeping the source "for reference" leaves two owners. A
  migration ends with the source gone.
- A framework, kernel, or base class that supplies an obligation owns it. Hand-wiring
  what it supplies — initializer chains, registration, dispatch — is not diligence; it
  is a second owner that will drift.

**Check:** name the single place this fact lives. If you are writing it somewhere else,
write a reference instead.

## 2. Behavior Belongs With What It Governs

Put the operation on the thing it operates on, at the level where it is true of
everything at that level.

- A construction performed on an object is a method of that object: `A.localization(f)`,
  not `Localization(A, f)`. The method dispatches on what the object actually is; the
  free function does not.
- A method true of everything in a class of objects belongs at that class, not copied
  into each member.
- In a game, an interactive object owns its own activation data and responses. A central
  table in the player controller that knows what every object does has taken the
  behavior away from the thing that has it, and must be edited to add content.
- A leaf, plugin, or extension owns the correctness of its own domain. The core's job is
  that a correct declaration produces correct behavior — not to validate the leaf's
  subject matter.

**Check:** if adding a new instance requires editing a central file, the behavior is in
the wrong place.

## 3. Separate Concerns Where the Audience Changes

A concern boundary is where a different person, tool, or lifecycle takes over. Draw the
seam there, not where the file happened to grow.

- A source file that carries the model, the collision, the placement markers, and the
  animation is a working method, not an architecture. The export boundary decides what
  the consumer receives.
- Content that non-programmers author — art, levels, copy, data — must be addable
  without a code change. If a new prop or effect forces a programmer to teach the
  pipeline about it, the seam is in the wrong place.
- A facade written over a broken component so that types check is two components where
  there was one problem. Fix the component.

**Check:** who edits each side of this boundary, and how often? If the answer is the same
person for the same reason, it is not a boundary.

## 4. The Representation Is Not the Thing

A number, an encoding, a document, or a proxy stands for something. Optimizing the stand-
in moves away from the thing whenever the two come apart, and they always come apart
under pressure.

- A matrix is a morphism in coordinates. Extracting the matrix and building a new
  morphism from it leaves nothing that records which bases were in play.
- Equal invariants are a consequence of isomorphism, not a definition of it.
- Page count stands for a reference work's size; reducing it is reported as an
  improvement and is a loss. Lines of code stand for a mathematics project; the audience
  wants theorems and definitions.
- An error count stands for correctness. Driving the count down is not the same as
  solving the problem, and an edit justified only by the number moving is unjustified.
- A test that asserts what the implementation currently returns has substituted the
  implementation for the mathematics it was supposed to state.
- Documentation stands for intent. When most of it was written by agents, it records
  prior guesses; the user's own statements outrank it.

**Check:** state the thing, state what you are measuring or storing, and state whether
they are the same. If not, you are working on the wrong one.

## 5. Write at the Level Where the Statement Is True

Find the weakest hypotheses under which your claim holds, and write it there. An
argument that silently uses the case in front of you is not a cautious version of the
general claim; it is a different claim that breaks without warning.

- Comparing ranks of kernels tests injectivity only because the modules at hand are
  free. Nothing in the code says so, and nothing fails loudly when that stops being true.
- Hard-coding one animation, one ambient category, one layout, or one asset assumes the
  single case you were shown is the whole domain. It is usually the example that was
  convenient to describe.
- An example offered to explain a concept is not a ruling. There are many ways to model
  the same structure; the example fixes the idea, not the implementation.

**Check:** name the hypothesis your solution depends on, remove it, and see what breaks.

## 6. Interfaces State Obligations

A contract exists to tell an implementer what they must supply, at the moment they fail
to supply it.

- Abstract base classes exist for exactly this. Hand-rolled "raise unless overridden" is
  the wart the language feature removes, and a contract is working when one attempted
  instantiation makes every obligation legible.
- An interface that others must consume is shaped by the consumer's standard, not by
  what was convenient to expose. An endpoint that does not meet the standard its intended
  client requires serves no one.

**Check:** if an implementer forgets an obligation, when do they find out, and does the
message name what is missing?

## 7. Compose Before You Construct

If the thing you need is a combination of things that already exist, that is the answer,
not a disappointment. Less code to write, and the result inherits the correctness of its
parts instead of asserting its own.

- A quotient, slice, graded piece, or fiber is obtained by taking it from a construction
  that already exists, not by building a parallel bespoke object with its own API.
- Repeated hand-rolled one-off workflows are the signal that a reusable primitive is
  missing. Build the primitive once, then compose.

**Check:** can this be expressed with what is already here? If yes, the new code is the
defect.

## 8. Derive From Purpose, and Check Whether the Purpose Is Already Served

Before designing, state what the artifact is for and who uses it. Behavior follows from
that, and some requested work dissolves under it.

- A table of contents exists so a reader can navigate quickly. If a complete searchable
  site already exists, the need is obviated — the answer is not a better table of
  contents.
- A study reference exists to help someone learn; it is authored literature broken into
  pages for navigation, not a database of records. Organization follows the reader's
  task.
- A description exists to tell a reader what they get. Internal implementation choices
  are not the product.

**Check:** state the purpose and the user in one sentence. If you cannot, do not build
yet.

## 9. The Standard Pattern Already Exists

Nearly every problem here is well-trodden somewhere: a language idiom, a library, an
established pattern in the domain, a published formalization. Inventing where a standard
exists costs the invention plus the time to have the standard explained back to you.

- Domains have canonical patterns practitioners expect to find — interactable objects in
  games, standard sidebar behavior in applications, established idioms in a language.
- House style that deviates from the common practice of a field is deliberate and has
  reasons; those reasons live in the repository's documents, and an outsider's instinct
  is not evidence against them.
- A new noun you had to invent is evidence that you are not using the standard model.
  The word is the symptom; the design is the defect, and deleting the word repairs
  nothing.

**Check:** what is the established solution, and where is it documented? Search before
designing. [[known-solution-first/SKILL|known-solution-first]] owns the procedure.

## 10. Design for Whoever Changes It Next

Assume the next person arrives tomorrow, knows none of your context, and needs to change
exactly the thing you assumed was fixed.

- An artist will replace every animation and texture. A researcher will relax every
  hypothesis. A contributor will need to find what exists before they can extend it.
- A reference document is useful when a contributor can see what is available to build
  with. A dump of everything, with no index, search, or pagination, is not a simple
  design; it is an unusable one.
- A reader with none of your context — a user, a reviewer, a freshly started agent —
  cannot act on a report that only makes sense from inside your session.

**Check:** name the next reader and the change they will make. Does the artifact help
them make it?
