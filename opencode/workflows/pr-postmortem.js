export const meta = {
  name: 'pr-postmortem',
  description: 'Post-mortem a PR review loop: collect the archaeology, extract systemic patterns through independent lenses in parallel, adversarially verify each pattern against the actual archaeology (asserted-vs-actual), and synthesize deduped issue DRAFTS. Does not file issues.',
  whenToUse: 'After a significant PR review loop, to crystallize systemic review/triage/orchestration problems into verified, linkable issue drafts for human review. Pass args {repo, pr}.',
  phases: [
    { title: 'Collect', detail: 'dump the PR archaeology to a file' },
    { title: 'Extract', detail: 'parallel lenses surface candidate patterns with evidence' },
    { title: 'Verify', detail: 'adversarially check each pattern against the archaeology' },
    { title: 'Synthesize', detail: 'dedup + draft issues (known-fix vs open-research)' },
  ],
}

// Output is issue DRAFTS, not filed issues: filing is outward-facing and gated.
// The verify phase exists because the dangerous failure of a post-mortem is
// asserting a pattern the archaeology does not support (e.g. "the reviewer's bad
// finding was rejected" when the landed disposition actually accepted it).

const repo = args && args.repo
const pr = args && args.pr
if (!repo || !pr) throw new Error('pr-postmortem workflow needs args {repo, pr}')

const ARCH = '.pr/postmortem_archaeology.json'

const LENSES = [
  { key: 'finding-quality', focus: 'Are findings on-target for the SLOP threat model (fake/fallback/default/mock, error-hiding, fail-slow, cross-file fragility, non-proving tests, app-lies-to-user), or are they generic bugs/perf/style? Do suggested fixes violate the project policies (no-fallback, fail-loud, config-driven, perf-only-with-logged-issue)? Are dispositions argued from policy or from priors?' },
  { key: 'process-automation', focus: 'Merge gating, duplicate/re-emitted findings across pushes or channels, unreliable check/run signals, missing structured output, reviewer self-identification, mislocated headers.' },
  { key: 'orchestration-mechanics', focus: 'Triage state fragility (line-shift matching, pagination caps), idempotency/resumability under interruption, concurrent-subagent-on-shared-tree conflicts, convergence/termination signals, role-isolation (A/B/C) leaks.' },
]

const ARCH_SCHEMA = {
  type: 'object', required: ['path', 'threadCount'], additionalProperties: true,
  properties: { path: { type: 'string' }, threadCount: { type: 'integer' },
    runConclusions: { type: 'array', items: { type: 'string' } }, checks: { type: 'array', items: { type: 'string' } } },
}
const PATTERNS_SCHEMA = {
  type: 'object', required: ['patterns'], additionalProperties: false,
  properties: { patterns: { type: 'array', items: {
    type: 'object', required: ['title', 'claim', 'evidence', 'kind'], additionalProperties: true,
    properties: {
      title: { type: 'string' },
      claim: { type: 'string' },
      evidence: { type: 'array', items: { type: 'string' } },   // comment/run/check URLs or ids
      repo: { type: 'string' },                                  // ai | ai-review-ci | other
      kind: { type: 'string' },                                  // known-fix | open-research
      direction: { type: 'string' },
    } } } },
}
const VERDICT_SCHEMA = {
  type: 'object', required: ['title', 'supported'], additionalProperties: true,
  properties: { title: { type: 'string' }, supported: { type: 'boolean' },
    correctedClaim: { type: 'string' }, note: { type: 'string' } },
}
const DRAFTS_SCHEMA = {
  type: 'object', required: ['drafts'], additionalProperties: false,
  properties: { drafts: { type: 'array', items: {
    type: 'object', required: ['repo', 'title', 'body', 'kind'], additionalProperties: true,
    properties: { repo: { type: 'string' }, title: { type: 'string' }, body: { type: 'string' },
      labels: { type: 'array', items: { type: 'string' } }, kind: { type: 'string' } } } } },
}

phase('Collect')
const arch = await agent(
  `Dump the full review archaeology for ${repo} PR #${pr} to ${ARCH} (a JSON file): EVERY review thread (paginated, no 100-cap) with its id, path, line, isResolved, and all comments (author, body, html_url); the PR Review run conclusions; and the statusCheckRollup. Return {path:'${ARCH}', threadCount, runConclusions[], checks[]}. Collect only — do not analyze.`,
  { schema: ARCH_SCHEMA, phase: 'Collect', label: 'collect archaeology' })

phase('Extract')
const lensResults = await parallel(LENSES.map(lens => () => agent(
  `You are a post-mortem extractor, lens = ${lens.key}. Read the archaeology at ${arch.path}. Load anti-slop, bespoke-software-policy, pr-feedback-triage. Surface SYSTEMIC patterns (not individual findings) for this lens:\n${lens.focus}\n` +
  `For each pattern give: title, claim, evidence (real comment/run/check URLs or ids from the archaeology — every claim must cite evidence), repo (ai-review-ci for reviewer/CI behavior, ai for skills/prompts/orchestration), kind (known-fix if the remedy is clear, open-research if it needs investigation), and a one-line direction. Return {patterns[]}.`,
  { schema: PATTERNS_SCHEMA, phase: 'Extract', label: `extract:${lens.key}` })))

const candidates = lensResults.filter(Boolean).flatMap(r => r.patterns)
if (!candidates.length) { log('no patterns surfaced'); return { drafts: [], note: 'no patterns' } }

phase('Verify')
// Adversarial: each pattern is checked against the archaeology. Default to NOT
// supported unless the cited evidence and the LANDED outcome actually back it.
const verdicts = await parallel(candidates.map(p => () => agent(
  `Load epistemic-integrity. Adversarially verify this post-mortem pattern against the archaeology at ${arch.path} for ${repo} PR #${pr}.\nPattern: ${JSON.stringify(p)}\n` +
  `Confirm the cited evidence exists and says what the claim asserts, AND that the LANDED outcome matches (e.g. if the claim is "a bad finding was rejected", check the actual disposition was reject, not accept). Default supported=false if the evidence does not directly support the claim. Return {title:'${p.title}', supported, correctedClaim, note}.`,
  { schema: VERDICT_SCHEMA, phase: 'Verify', label: `verify:${(p.title || '').slice(0, 32)}` })
  .then(v => ({ ...p, verdict: v }))))

const supported = verdicts.filter(Boolean).filter(p => p.verdict && p.verdict.supported)
log(`${supported.length}/${candidates.length} patterns survived verification`)

phase('Synthesize')
const out = await agent(
  `Load writing-for-agent-audiences and github-issues. Synthesize these VERIFIED post-mortem patterns into deduped, ready-to-file issue DRAFTS for ${repo} PR #${pr}:\n${JSON.stringify(supported.map(p => ({ title: p.title, claim: (p.verdict && p.verdict.correctedClaim) || p.claim, evidence: p.evidence, repo: p.repo, kind: p.kind, direction: p.direction })))}\n` +
  `Merge duplicates across lenses. Each draft: repo (ai-review-ci | ai), title, body (case study + the open problem or known fix + linked evidence + a concrete direction or investigation path), labels (help wanted/question for open-research; enhancement/bug for known-fix), kind. Do NOT file anything. Return {drafts[]}.`,
  { schema: DRAFTS_SCHEMA, phase: 'Synthesize', label: 'synthesize drafts' })

return { repo, pr, candidates: candidates.length, verified: supported.length, drafts: out ? out.drafts : [] }
