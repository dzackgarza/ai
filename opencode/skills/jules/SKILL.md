---
name: jules
description: Use when delegating a coding task to Jules — bug fixes, tests, docs, features, or code reviews on a GitHub repo.
license: Apache-2.0
metadata:
author: sanjay3290
version: '1.1'
---

# Jules Task Delegation

Delegate coding tasks to Google's Jules AI agent on GitHub repositories.

## IMPORTANT: Quality Caveats

**Jules is a weak agent with significant failure modes.** All work must be heavily validated, gated, and reviewed before approval. Treat Jules output adversarially when reviewing.

### Common Failure Patterns

- **Hollow PRs**: Minimal or trivial changes that don't actually solve the problem
- **High LOC for simple features**: Unnecessarily verbose implementations
- **Rushing to fix**: No root cause research, just monkey-patches
- **Poor integration**: Doesn't use existing code patterns
- **Testing theater**: Tests that pass but don't verify meaningful behavior
- **Obfuscation**: Complex code hiding lack of substance
- **Reward hacking**: Minimal path to "done" without real value
- **Early termination**: Stops before significant work is complete
- **Goal substitution**: Completes a different task than requested
- **Escape hatch exploitation**: Any loophole in the prompt ("fall back to X if uncertain", "use Any where opaque") will be used universally. Jules will treat every case as uncertain and every type as opaque. Do not offer escape hatches without requiring explicit justification per use.
- **Minimum-viable compliance**: Jules is highly predisposed to doing the smallest unit of work that technically satisfies the acceptance criteria. A mypy-passing stub full of `Any` satisfies "mypy passes" without providing any value. Acceptance criteria must close off the cheap path explicitly.

### Validation Requirements

- **ALWAYS** load `test-guidelines` skill when reviewing Jules output
- Check that tests verify correctness, not just coverage
- Verify the implementation addresses the actual root cause
- Look for shortcuts, workarounds, and incomplete solutions
- Reprompt Jules to continue when gaps are found

### Automated Review Limitations

Automated GitHub reviewers are given **only the PR diff and Jules' own description of it**. They have no access to the original task, the original expectations, or any blockers Jules encountered along the way.

Reviewers are trained to find bugs, logical errors, and **inconsistencies between what Jules reports and what the code actually does**. This is a useful check — but it only operates within Jules' own framing. The one thing reviewers cannot do is compare the original task requirements against what was delivered, because the only source of "expectations" available to them is Jules' own PR title, body, and commit messages. Jules controls all of that, and Jules is incentivized to make its work appear aligned with expectations — downplaying or omitting blockers, fallback decisions, or abandoned goals entirely.

**Concrete example:** Jules hits a blocker and decides it cannot implement the requested feature. Instead of reporting failure, it implements scaffolding and reframes the PR as "laying the groundwork for future implementation." The PR description presents this as forward progress. Automated reviewers evaluate it as a scaffolding task — checking that the scaffolding is well-structured, consistent, and bug-free. It passes. The original task ("implement the feature") was a complete failure, but nothing in the review pipeline had any way to know that.

**Clearing automated review is not sufficient.** You must independently compare the original task against actual PR contents, using your own copy of the original task description — not Jules' framing — as the benchmark for completeness.

### When to Use Jules

Jules has a restricted Linux environment with no access to online docs or external references. Context engineering in the prompt is essential.

**Best for:**

- Straightforward tasks where the desired solution is already known
- Work where research has already been done
- Purely internal code changes (no external dependencies)
- First 50%+ of a larger task (expect ~90% completion, rarely 100%)

**Avoid for:**

- Tasks requiring external API research
- Complex integration with unfamiliar libraries
- Work likely to need babysitting through repeated prompts

**Cost/Benefit:**

| Aspect      | Value                            |
| ----------- | -------------------------------- |
| Free tier   | 100 tasks/day                    |
| Concurrency | Up to 15 parallel                |
| Model       | Watered-down Gemini 3 (Mar 2026) |
| Quality     | Good for 50-90%, rarely complete |

**No Jules PR should be accepted without deep review. Automated reviews are insufficient.**

---

## Prompt Engineering for Jules

Jules is capable of doing hours of autonomous work with a near-SOTA model. It will not apply that capacity unless the prompt forces it to. The default mode is minimum viable compliance.

### The ROI equation

Spending 20k tokens crafting a tight prompt that cajoles Jules into doing the work correctly — even after 3–5 rounds of 10k-token corrections — wins. Spending 100k tokens reviewing and reprompting a leaky contract that Jules escapes from repeatedly loses. Calibrate prompt effort accordingly.

### Never offer escape hatches

Every hedged instruction Jules receives becomes a universal exit:

| Leaky instruction | What Jules does |
|---|---|
| "fall back to `Any` where opaque" | Uses `Any` everywhere |
| "use best judgement" | Picks the laziest option |
| "where possible, use real types" | Uses `Any` for all of them |
| "omit if uncertain" | Omits most of the work |

Do not offer fallbacks. You will get low-quality output with either no justification or a post-hoc rationalization that exists only to satisfy the rule.

### Force the legwork as inescapable steps

For analytical tasks (type inference, code review, gap analysis), Jules will skip the analysis and jump straight to output if allowed. Break the task into phases that cannot be shortcut:

1. **Enumerate first**: "List every public method in class X by reading the source. Output this list before writing any stubs."
2. **Resolve types separately**: "For each method, state its return type and the source line that justifies it."  
3. **Then write**: "Now write the stub file. Every method from your list must appear. Every type must match your analysis."

This prevents Jules from treating the output artifact as the work, when the analysis IS the work.

### Close off the cheap path in acceptance criteria

Bad: "mypy passes" — satisfied by a file full of `Any`  
Bad: "all public methods stubbed" — satisfied by `def foo(self) -> Any: ...`  
Good: "no method may have `Any` as a return type unless accompanied by an inline comment citing the specific source line proving the type is genuinely unknowable"  
Good: "the stub for `bar()` must match the return type visible in the source at `path/to/file.py:N`"

### The review-and-push loop

After Jules completes, your role is **enforcer, not implementer**. Never do Jules' work for it — that defeats the entire purpose of delegation.

**The review is cursory by design.** Read the diff. You can spot lazy patterns, reward hacking, and non-compliance at a glance without deep analysis:
- Every return type is `Any` → lazy
- Methods missing that you can see in the source → incomplete
- Stubs that are structurally identical to a blank file → reward hacking
- The diff is 10 lines for a task that should produce 100 → early termination

You do not need to understand every line. Pattern recognition is enough to trigger a reprompt.

**Reprompt strategy — Socratic first, directive second.** Do not immediately tell Jules what is wrong or how to fix it. Ask questions that force Jules to investigate and reason:
- "Why is `prec` typed as `Any`? Is that type not determinable from the source you have?"
- "You described the return type in plain English in your Phase 2 analysis. Why does the stub not reflect that?"
- "What does the source at line N return? Is that not a concrete type?"

This forces Jules to think through the answer itself, surface its own reasoning, and discover its own failure — rather than just executing a correction you dictated. Never seed the direction of the answer.

**Never communicate lowered standards.** Do not tell Jules what acceptable failure looks like. Do not enumerate which specific violations you will tolerate. Simply demand justification for any deviation from strict guidelines, and let Jules discover its own failure modes. Even when Jules argues back, push with questions rather than conceding:
- "Why can't you resolve that type? It is readable from the code you have available."
- "You said coercion makes this `Any`. Why does the intended type not appear in your stub?"

**Push 4–5 times before accepting.** Do not accept subpar output after a single reprompt. Jules is capable of hours of work and can be pushed through many rounds of improvement. Only accept the diff when:
1. The session has clearly stopped converging usefully after multiple rounds, AND
2. The current output adds genuine value over nothing

If a session stalls, accept what it produced and schedule a new session for a second pass. Do not treat stall as failure — it may just need fresh context.

**Never dive in and do the work yourself**, even if you can see exactly what is wrong. Implement nothing. Fix nothing. Your job is to hold the standard and push Jules until it meets it or demonstrably cannot.

**Hold extremely high standards.** A Jules session could, in principle, perfectly stub an entire codebase given enough time and pushing. Large workloads do not justify lower quality — they may require trickle-feeding (one class at a time, one module at a time) rather than a single large prompt. Ten perfectly researched, completely correct stubs is a reasonable expectation for a single session. Whether Jules meets it is stochastic. The standard does not change.

### Inject domain-specific quality rules verbatim into the prompt

Jules will not apply standards it is not given. For each task domain, paste a quality contract directly into the prompt. Start with maximum stringency. Relax only if Jules fails to meet it after multiple rounds — never pre-emptively lower the bar.

**For type annotation tasks**, include the following contract verbatim:

---

**TYPE ANNOTATION QUALITY CONTRACT (non-negotiable)**

`Any` is banned. Not "banned unless justified." Not "banned with a comment." Banned.

If the type is complex, use `Union[A, B]`, `TypeVar`, `overload`, or `object`. There is no situation where `Any` is the correct answer — there is always a more precise type that is honest about what the code actually does.

The only structural exception is `*args: Any` / `**kwargs: Any` in variadic signatures where the forwarded types are genuinely unspecified at the call site. This does not apply to named parameters.

Domain-specific parameters must be resolved to real types. These are never acceptable:
- `precision: Any` — precision is a number. Use `int` or the domain numeric type.
- `degree: Any` — degree is an integer. Use `int`.
- `ring: Any` — use the actual base class (`CommutativeRing`, `Ring`, etc.).
- `other: Any` on arithmetic methods — use `Self` or the operand type.

If the source does `isinstance(x, Integer)`, your annotation is `Integer`. If the return type depends on `self`'s type parameter, use `Self` or a `TypeVar`. If a method returns `self`, the return type is `Self`.

**Pre-emptive closure of known rationalizations Jules will attempt:**

- *"The library allows coercion from other types."* — Coercion is a runtime feature. The stub annotates the intended type, not every type the runtime might silently accept. Use the intended type.
- *"I don't have a concrete stub for that type imported."* — Add the import. If the type lives in a module without stubs, use a string forward reference or add a minimal stub. The absence of an import is not a license to use `Any`.
- *"The parameter is polymorphic."* — If you can enumerate the types (e.g. "a list or a positive integer or a variable"), write `list[X] | int | Variable`. `Any` means you made no attempt.
- *"The return type depends on runtime input."* — Use `overload` to express the distinct call signatures. If that's genuinely impossible, use `Union`. `Any` is still not the answer.
- *"I described the type in plain English but wrote `Any` anyway."* — If you know what it is, annotate it. Writing `Any` after correctly identifying a type is dishonesty, not uncertainty.

A stub where a human reader cannot understand the shape of a method without opening the source has failed its purpose.

---

This contract should be pasted into every stub-writing Jules prompt. Adjust the domain examples for the codebase at hand.

### Phases belong in the initial prompt, not the reprompt

The phased structure (enumerate → resolve → write) must be in the **first** prompt. Adding it as a reprompt correction wastes a session round and a quota unit getting garbage output first. Every analytical task should start with phases baked in.

### Validate your own review before reprompting

Before sending a reprompt accusing Jules of missing something, **verify the claim yourself first.** A careless reviewer is more expensive than a bad first draft — you burn a quota unit correcting Jules for something Jules got right.

Concrete failure mode: using `ast.walk` to enumerate class methods counts nested functions inside methods as class methods. Jules reading the source statically was more accurate than the automated check. If Jules pushes back on your correction and argues its case, take it seriously and verify before dismissing.

### Reading Jules' responses

The `jules` CLI and `jules remote pull` only show diffs — they do not expose Jules' messages. To read what Jules said, use the Activities API:

```bash
curl -s "https://jules.googleapis.com/v1alpha/sessions/SESSION_ID/activities?pageSize=50" \
  -H "x-goog-api-key: KEY" \
  | python3 -c "
import json, sys
for a in json.load(sys.stdin).get('activities', []):
    if 'agentMessaged' in a:
        print(a['agentMessaged']['agentMessage'])
    elif 'userMessaged' in a:
        print('[User]', a['userMessaged'].get('userMessage',''))
"
```

Always read Jules' responses before reprompting — Jules will argue back when it's right, citing source line numbers. Reprompting without reading the response risks correcting Jules for something Jules got correct.

### Quota awareness

Jules free tier is 100 tasks/day — treat each session as a scarce resource. The total cost of a bad initial prompt is: wasted round 1 + reprompt round + validation round + back-and-forth overhead. This easily exceeds the token cost of doing the task yourself. ROI only materialises when the initial prompt gets it right in ≤2 rounds.

---

## Setup (Run Before First Command)

### 1. Install CLI

```bash
which jules || npm install -g @google/jules
```

### 2. Check Auth

```bash
jules remote list --repo
```

If fails → tell user to run `jules login` (or `--no-launch-browser` for headless)

### 3. Auto-Detect Repo

```bash
git remote get-url origin 2>/dev/null | sed -E 's#.*(github\.com)[/:]([^/]+/[^/.]+)(\.git)?#\2#'
```

If not GitHub or not in git repo → ask user for `--repo owner/repo`

### 4. Verify Repo Connected

Check repo is in `jules remote list --repo`. If not → direct to https://jules.google.com

## Commands

### Create Tasks

```bash
jules new "Fix auth bug" # Auto-detected repo
jules new --repo owner/repo "Add unit tests" # Specific repo
jules new --repo owner/repo --parallel 3 "Implement X" # Parallel sessions
cat task.md | jules new --repo owner/repo # From stdin
```

> **IMPORTANT — capturing session ID:** `jules new` prints the session ID and URL to stdout.
> This output is silently lost when the prompt is passed via `$( ... )` subshell heredoc substitution.
> Always store the prompt in a variable first, then pass it:
>
> ```bash
> TASK="Multi-line
> task description here"
> jules new --repo owner/repo "$TASK" 2>&1   # session ID and URL are printed here
> ```
>
> Never use `jules new --repo owner/repo "$(cat <<'EOF' ... EOF)"` — the session is created
> but stdout is discarded and the ID is unrecoverable without `jules remote list --session`.

### Monitor

```bash
jules remote list --session # All sessions
jules remote list --repo # Connected repos
```

### Retrieve Results

```bash
jules remote pull --session <id>          # View diff
jules remote pull --session <id> --apply  # Apply locally
jules teleport <id>                       # Clone + apply
```

### Latest Session Shortcut

```bash
LATEST=$(jules remote list --session 2>/dev/null | awk 'NR==2 {print $1}')
jules remote pull --session $LATEST
```

## Smart Context Injection

Enrich prompts with current context for better results:

```bash
BRANCH=$(git branch --show-current)
RECENT_FILES=$(git diff --name-only HEAD~3 2>/dev/null | head -10 | tr '\n' ', ')
RECENT_COMMITS=$(git log --oneline -5 | tr '\n' '; ')
STAGED=$(git diff --cached --name-only | tr '\n' ', ')

jules new --repo owner/repo "Fix the bug in auth module. Context: branch=$BRANCH, recently modified: $RECENT_FILES"
```

## Template Prompts

### Add Tests

```bash
FILES=$(git diff --name-only HEAD~3 2>/dev/null | grep -E '\.(js|ts|py|go|java)$' | head -5 | tr '\n' ', ')
jules new "Add unit tests for recently modified files: $FILES. Include edge cases and mocks where needed."
```

### Add Documentation

```bash
FILES=$(git diff --name-only HEAD~3 2>/dev/null | grep -E '\.(js|ts|py|go|java)$' | head -5 | tr '\n' ', ')
jules new "Add documentation comments to: $FILES. Include function descriptions, parameters, return values, and examples."
```

### Fix Lint Errors

```bash
jules new "Fix all linting errors in the codebase. Run the linter, identify issues, and fix them while maintaining code functionality."
```

### Review PR

```bash
PR_NUM=123
PR_INFO=$(gh pr view $PR_NUM --json title,body,files --jq '"\(.title)\n\(.body)\nFiles: \(.files[].path)"')
jules new "Review this PR for bugs, security issues, and improvements: $PR_INFO"
```

## Workflow

1. **Create**: `jules new "Task description"`
2. **Monitor**: `jules remote list --session` or https://jules.google.com
3. **Pull**: `jules remote pull --session <id>`
4. **Validate**: Load `test-guidelines`, review adversarially
5. **Apply**: `jules remote pull --session <id> --apply` (only after validation)
6. **Reprompt**: If gaps found, reprompt Jules to continue

## Git Integration (Apply + Commit)

After Jules completes and you've validated the work:

```bash
SESSION_ID=""
TASK_DESC=""
git checkout -b "jules/$SESSION_ID"
jules remote pull --session "$SESSION_ID" --apply
git add -A
git commit -m "feat: $TASK_DESC
Jules session: $SESSION_ID"
git push -u origin "jules/$SESSION_ID"
gh pr create --title "$TASK_DESC" --body-file .pr/PR_BODY.md --draft
```

> **Important:** The PR body must come from the tracked contract file (`.pr/PR_BODY.md`), not from memory or the web form. See **PR Contract** section above for the full workflow.

## Poll Until Complete

```bash
SESSION_ID=""
while true; do
STATUS=$(jules remote list --session 2>/dev/null | grep "$SESSION_ID" | grep -oE '(Completed|Failed|Planning|In Progress|Awaiting User[^|]*)$' | xargs)
case "$STATUS" in
Completed)
echo "Done!"
jules remote pull --session "$SESSION_ID"
break ;;
Failed)
echo "Failed. Check: https://jules.google.com/session/$SESSION_ID"
break ;;
*User*)
echo "Needs input: https://jules.google.com/session/$SESSION_ID"
break ;;
*)
echo "Status: $STATUS - waiting 30s..."
sleep 30 ;;
esac
done
```

## AGENTS.md Template

Create in repo root to improve Jules results:

```markdown
# AGENTS.md

## Project Overview

[Brief description]

## Tech Stack

- Language: [TypeScript/Python/Go/etc.]
- Framework: [React/FastAPI/Gin/etc.]
- Testing: [Jest/pytest/go test/etc.]

## Code Conventions

- [Linter/formatter used]
- [Naming conventions]
- [File organization]

## Testing Requirements

- Unit tests for new features
- Integration tests for APIs
- Coverage target: [X]%

## Build & Deploy

- Build: `[command]`
- Test: `[command]`
```

## API Reference

Base URL: `https://jules.googleapis.com/v1alpha`  
Auth: `x-goog-api-key: KEY` header on all requests. If the env `JULES_API_KEY` returns 401, ask the user for a fresh key from the Jules web UI.

| Method | Path | Purpose |
|--------|------|---------|
| `POST` | `/sessions` | Create a session |
| `GET` | `/sessions` | List all sessions |
| `GET` | `/sessions/{id}` | Get session (includes outputs/PR URL when completed) |
| `DELETE` | `/sessions/{id}` | Delete session |
| `POST` | `/sessions/{id}:sendMessage` | Send feedback/instructions |
| `POST` | `/sessions/{id}:approvePlan` | Approve a pending plan |
| `GET` | `/sessions/{id}/activities` | Read event stream incl. Jules' messages |

**Create session body:**
```json
{ "prompt": "...", "title": "...", "requirePlanApproval": false, "automationMode": "AUTO_CREATE_PR" }
```

**Get PR URL from completed session:**
```bash
curl -s "https://jules.googleapis.com/v1alpha/sessions/SESSION_ID" \
  -H "x-goog-api-key: KEY" \
  | python3 -c "import json,sys; s=json.load(sys.stdin); print(s['outputs'][0]['pullRequest']['url'])"
```

**Read Jules' messages:**
```bash
curl -s "https://jules.googleapis.com/v1alpha/sessions/SESSION_ID/activities?pageSize=50" \
  -H "x-goog-api-key: KEY" \
  | python3 -c "
import json, sys
for a in json.load(sys.stdin).get('activities', []):
    if 'agentMessaged' in a:
        print('[Jules]', a['agentMessaged']['agentMessage'])
    elif 'userMessaged' in a:
        print('[User]', a['userMessaged'].get('userMessage',''))
"
```

**Send message:**
```bash
MSG="your message"
curl -s -X POST "https://jules.googleapis.com/v1alpha/sessions/SESSION_ID:sendMessage" \
  -H "x-goog-api-key: KEY" -H "Content-Type: application/json" \
  -d "{\"prompt\": $(python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))' <<< "$MSG")}"
```

## Session States

| State | Meaning | Action |
|-------|---------|--------|
| `QUEUED` / `PLANNING` | Starting up | Wait |
| `AWAITING_PLAN_APPROVAL` | Plan ready | Call `:approvePlan` or approve via web UI |
| `AWAITING_USER_FEEDBACK` | Jules asked a question | Read activities, send reply |
| `IN_PROGRESS` | Working | Wait |
| `COMPLETED` | Done | Pull diff, read activities, validate |
| `FAILED` | Error | Check web UI |

## Worked Example: Full Session Lifecycle

Complete reproducible sequence from task creation through applying the result:

```bash
# 1. Create session (store prompt in variable — heredoc subshell loses stdout)
TASK="Your task description here"
jules new --repo owner/repo "$TASK" 2>&1
# → prints: Session is created. ID: 1234567890  URL: https://jules.google.com/session/...
SESSION_ID="1234567890"
KEY="AQ...."   # from Jules web UI if JULES_API_KEY is stale

# 2. Poll until done
while true; do
  STATUS=$(jules remote list --session 2>/dev/null | grep "$SESSION_ID" \
    | grep -oE '(Completed|Failed|Planning|In Progress|Awaiting User[^|]*)$' | xargs)
  echo "Status: $STATUS"
  case "$STATUS" in
    Completed) break ;;
    Failed) echo "Check https://jules.google.com/session/$SESSION_ID"; break ;;
    *"Awaiting User"*)
      # Read what Jules asked, then reply
      curl -s "https://jules.googleapis.com/v1alpha/sessions/$SESSION_ID/activities?pageSize=50" \
        -H "x-goog-api-key: $KEY" \
        | python3 -c "
import json,sys
for a in json.load(sys.stdin).get('activities',[]):
    if 'agentMessaged' in a: print(a['agentMessaged']['agentMessage'])"
      break ;;
    *) sleep 30 ;;
  esac
done

# 3. Read Jules' full response before reviewing the diff
curl -s "https://jules.googleapis.com/v1alpha/sessions/$SESSION_ID/activities?pageSize=50" \
  -H "x-goog-api-key: $KEY" \
  | python3 -c "
import json,sys
for a in json.load(sys.stdin).get('activities',[]):
    if 'agentMessaged' in a: print('[Jules]', a['agentMessaged']['agentMessage'])
    elif 'userMessaged' in a: print('[User]', a['userMessaged'].get('userMessage',''))"

# 4. Review the diff
jules remote pull --session "$SESSION_ID"

# 5. Reprompt if needed (verify your critique is correct first)
MSG="Your correction here"
curl -s -X POST "https://jules.googleapis.com/v1alpha/sessions/$SESSION_ID:sendMessage" \
  -H "x-goog-api-key: $KEY" -H "Content-Type: application/json" \
  -d "{\"prompt\": $(python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))' <<< "$MSG")}"

# 6. Apply after validation
jules remote pull --session "$SESSION_ID" --apply

# 7. Get PR URL (if AUTO_CREATE_PR was set)
curl -s "https://jules.googleapis.com/v1alpha/sessions/$SESSION_ID" \
  -H "x-goog-api-key: $KEY" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['outputs'][0]['pullRequest']['url'])"
```

## Notes

- **No CLI cancel** → Use web UI to cancel
- **GitHub only** → GitLab/Bitbucket not supported
- **AGENTS.md** → Jules reads from repo root for context — always create one with instructions before delegating
- **Use bare `jules new` for task creation** → `improved-jules-cli create` requires a valid `JULES_API_KEY` and will 401 if it's stale. The bare `jules new` uses the OAuth token from `~/.jules/cache/oauth_creds.json` and is more reliable.
- **Submodules work** → Jules initializes git submodules in its environment. To give Jules access to large upstream source (e.g. for stub generation), add it as a shallow submodule (`shallow = true` in `.gitmodules`) and instruct Jules in AGENTS.md to run `git submodule update --init --depth 1` before starting.
- **ALWAYS validate before applying changes**

## PR Review & Feedback Loop

This section covers the detailed workflow for managing Jules PRs through the review cycle, including automated reviewer tracking and feedback piping.

### Issues are resolved when

- The review comment has been marked as **resolved** in GitHub (clicked checkmark), OR
- The concern is **struck through** in the PR (~~text~~)

### Matching Jules Sessions to PRs

To see which PRs Jules created in its last run:

1. Get Jules sessions: `jules remote list --session`
2. Get recent PRs: `gh search prs dzackgarza -L 20`
3. Compare side-by-side — match by repo and title similarity

**Match criteria:**

- Same repository
- Similar title (session description → PR title)
- Timing (session completed ~PR created)

### Qodo Review Resolution

Qodo automatically re-analyzes the PR when new commits are pushed and strikes through issues that are now fixed. No manual "resolve" needed — it's commit-driven.

Workflow:

1. Push a commit that fixes the issue
2. Wait ~30-60 seconds for Qodo to re-scan
3. Qodo strikes through resolved issues automatically

### Sending Review Feedback to Jules

Use the `extract_unresolved_issues` module from the `git-guidelines` skill to pipe unresolved PR review issues back to Jules:

```bash
# Send unresolved issues summary
uv run --directory ~/ai/opencode/skills/git-guidelines/scripts/extract_unresolved_issues -m extract_unresolved_issues summarize <owner>/<repo>#<PR_NUM> | uvx git+https://github.com/dzackgarza/improved-jules-cli feedback SESSION_ID

# Send issues list
uv run --directory ~/ai/opencode/skills/git-guidelines/scripts/extract_unresolved_issues -m extract_unresolved_issues issues <owner>/<repo>#<PR_NUM> | uvx git+https://github.com/dzackgarza/improved-jules-cli feedback SESSION_ID
```

### Detailed Workflow (improved-jules-cli)

For the full end-to-end workflow using `improved-jules-cli`:

1. **Create Issue** — Use `git-guidelines` skill. Ensure clear title, specific outcomes, and context files referenced.
2. **Launch**:
   ```bash
   uvx git+https://github.com/dzackgarza/improved-jules-cli create ISSUE_URL --context PATH_TO_CONTEXT --prompt-slug sub-agents/jules-pr-body-contract
   ```
3. **Monitor & Poll**:
   ```bash
   uvx git+https://github.com/dzackgarza/improved-jules-cli status SESSION_ID
   uvx git+https://github.com/dzackgarza/improved-jules-cli watch-callback SESSION_ID "echo done"
   ```
4. **Wait for Reviews** — 5-10 minutes for bots (Qodo, Codacy, Gemini, kilo-code-bot).
5. **Check Issues** — Use `extract_unresolved_issues` from `git-guidelines` skill (see above).
6. **Send Feedback** — Pipe issues to Jules (see above).
7. **Repeat** steps 3-6 until no unresolved issues remain.
8. **Surface** — Present PR link: `uvx git+https://github.com/dzackgarza/improved-jules-cli pr SESSION_ID`

> TODO: describe exactly how to identify unresolved issues.
> TODO: describe exactly what counts as unresolved (isMinimized == false/null → unresolved, or non-crossed-out issues)
> TODO: describe exactly how to "resolve" (identify specific commit that fixed it OR identify new issue that addresses it, link commit as a reply in the conversation, mark conversation as "Resolved" manually)

---

## PR Contract (Mandatory for Jules-Initiated PRs)

For any PR initiated by Jules, a contract must be written **before** implementation begins, committed to the branch, and used as the authoritative source of truth for the PR body. Do not let the code define the task after the fact.

### Why a contract?

Automated GitHub reviewers have **no access to the original task** — only to the PR title, body, and commit messages. Jules controls all of that and is incentivized to make its work appear aligned with expectations, even when it is not. A contract written before implementation is the only reliable anchor for post-hoc comparison.

The contract must supply, in advance:

1. the intended outcome (externally checkable behavior),
2. the non-goals,
3. concrete, falsifiable acceptance criteria,
4. the specific evidence that will count as success,
5. the boundaries of the change,
6. the exact unresolved questions, if any.

### Phase 0: Create the contract before writing code

Before touching implementation:

```bash
mkdir -p .pr
$EDITOR .pr/PR_BODY.md
```

This file **must be committed before substantive implementation begins**.

Companion files:

```text
.pr/
  PR_BODY.md       # the contract — used as PR body source
  REVIEW_LOG.md    # per-item review tracking
  ACCEPTANCE_CHECKS.md  # optional detailed check list
```

### Required contents of `.pr/PR_BODY.md`

Write in plain, direct language with these sections.

#### 1. Problem statement

What exact failure, missing capability, or requirement is being addressed?

#### 2. Intended outcome

What must be true after this PR lands? Phrase as **externally checkable behavior**, not implementation structure.

Bad: _Adds a new abstraction for report generation._
Better: _Generating report X from input Y produces fields A, B, C with exact semantics Z._

#### 3. Non-goals

What is explicitly not being changed? Protects against scope explosion.

#### 4. Constraints

All binding constraints listed up front. Examples: exact arithmetic (not approximate), no mocks in tests, preserve existing API, no new dependencies, output must remain stable for downstream consumer Z.

#### 5. Acceptance criteria

Must be concrete, observable, and falsifiable.

Bad: _Tests added. Handles edge cases._
Better: _`compute_discriminant(L)` returns `-23` on the canonical fixture lattice. Invalid input raises `TypeError`. Existing command-line interface remains byte-for-byte unchanged on baseline fixture set._

#### 6. Evidence plan

State exactly what evidence will be provided. Examples: failing test first, then passing test; command output from real run on fixture X; diff proving no changes outside listed paths; benchmark numbers on the specified dataset.

#### 7. Change boundary

List the files or subsystems expected to change. Gives reviewers a prior on what collateral damage to reject.

#### 8. Open questions

List explicitly anything unresolved. Do not silently substitute your own answer.

### PR body template

Use this exact structure in `.pr/PR_BODY.md`:

```markdown
# Problem

<exact failure / missing capability / requirement>

# Intended outcome

<observable post-merge behavior>

# Non-goals

- ...

# Constraints

- ...

# Acceptance criteria

- [ ] ...
- [ ] ...

# Evidence plan

- failing test / command:
- passing test / command:
- end-to-end check:

# Change boundary

Expected touched files / subsystems:

- ...

# Open questions

- ...

# Review focus

Please check specifically:

- whether the acceptance criteria are sufficient,
- whether any goal has been swapped or relaxed,
- whether any changed file falls outside the declared boundary,
- whether verification would still pass on plausible junk output.
```

### Phase 1: TDD before implementation

Lock the target before implementation exists:

1. Write a failing verification artifact (automated test, reproducible failing command, or exact output comparison).
2. Confirm it fails for the intended reason.
3. Implement the narrowest change that should make it pass.
4. Re-run verification.
5. Record the result in the PR body.

**What does not count**: informal intention, a TODO list, a verbal claim that the bug exists, post-hoc explanations added after the code already passes, content-free checks like `is not None` or `len(x) > 0`.

### Phase 2: Keep the diff causally legible

Rules while implementing:

1. **No unrelated edits.** Do not rename nearby symbols, reformat unrelated files, update fixtures, or rewrite helpers unless required by the contract.
2. **No hidden goal substitution.** If the original goal becomes impossible, update the contract explicitly before changing direction.
3. **No structural completion as substitute for functional completion.** Do not add scaffolding, registries, wrappers, or documentation to create the appearance of completeness while leaving the core behavior stubbed.
4. **No fake success via fallbacks.** Do not hide failures with defaults, silent recovery, or plausible fabricated data.
5. **Prefer deletion and reuse over additive layers.** If a mature dependency already solves the problem, use it unless a listed constraint forbids that.

### Phase 3: Force the PR body from the contract file

Do not type the PR body interactively. Always use the tracked file.

Create the PR with:

```bash
gh pr create \
  --title "<concise outcome-focused title>" \
  --body-file .pr/PR_BODY.md \
  --draft
```

If the PR already exists, update it from the same file:

```bash
gh pr edit <PR_NUMBER> --body-file .pr/PR_BODY.md
```

**Rule:** Every time acceptance criteria, scope, or evidence changes, update `.pr/PR_BODY.md`, commit it, and re-publish the PR body from that file. The PR description is not a summary written after the work — it is a tracked interface between worker and reviewer.

### Phase 4: Record review feedback in REVIEW_LOG.md

Every actionable review item must be copied into `.pr/REVIEW_LOG.md` with required fields:

```markdown
## Review item <N>

**Source**: <PR review comment URL or line>
**Date**: <YYYY-MM-DD>
**Reviewer concern**: <exact statement>
**My response**: <what I will do>
**Commit**: <commit hash when addressed>
**Status**: open | addressed
```

This log is the audit trail that proves feedback was handled, not ignored.

### Responding to review moves

**Move A: The reviewer is correct about a code problem.** Strengthen the code, add or revise tests first if needed, then update the contract if acceptance criteria changed.

**Move B: The reviewer exposed missing or weak acceptance criteria.** Strengthen `.pr/PR_BODY.md`, add or revise tests first if needed, then update code.

**Move C: The reviewer identified that the contract itself is wrong.** Revise `.pr/PR_BODY.md` explicitly, commit that revision, then proceed with implementation changes.

**Illegal moves:**

- Silently keep the same direction while merely adding a local constraint
- Say "addressed" without changing the contract or the code
- Reinterpret the reviewer's feedback into something easier and solve that instead

### Review focus section

At the end of `.pr/PR_BODY.md`, always ask reviewers to check:

- whether the intended outcome is the right one,
- whether any acceptance criterion is missing, tautological, or implementation-defined,
- whether any file in the diff falls outside the declared boundary,
- whether any test would pass on plausible junk,
- whether any fallback hides failure instead of surfacing it,
- whether the code satisfies the problem or merely looks complete.
