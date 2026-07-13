export const meta = {
  name: 'pr-feedback-triage',
  description: 'Convergent PR review-feedback triage: collect -> pre-filtered disposition + current-PR spend gate -> A/B/C only for substantive findings -> linked debt backlog for minor findings -> loop until convergence.',
  whenToUse: 'After automated/human review feedback lands on a PR and you want the firewall-enforced triage loop run deterministically instead of hand-driving subagents. Pass args {repo, pr}.',
  phases: [
    { title: 'Collect', detail: 'run the triage harness; get worklist + convergence' },
    { title: 'Disposition', detail: 'role B: pre-filter + five-way spend gate, one disposition per finding' },
    { title: 'Remediate', detail: 'role C: first-principles spec per accepted current-PR finding' },
    { title: 'Verify', detail: 'by-hand declared-vs-actual, commit, three-stamp close' },
  ],
}

// Structural firewall: THIS SCRIPT is role A. It never disposes and never
// remediates. B (disposition) and C (remediation) are separate agent() calls so
// A cannot leak a verdict into remediation or self-dispose. The detailed
// procedure lives in the pr-feedback-triage skill; agents load it by role.

const repo = args && args.repo
const pr = args && args.pr
if (!repo || !pr) throw new Error('pr-feedback-triage workflow needs args {repo, pr}')

const SKILL = '~/ai/opencode/skills/pr-feedback-triage'
const HARNESS = SKILL + '/scripts/triage_state.py'
const MAX_ROUNDS = 8

const COLLECT_SCHEMA = {
  type: 'object', required: ['converged', 'worklist'], additionalProperties: true,
  properties: {
    converged: { type: 'boolean' },
    counts: { type: 'object', additionalProperties: true },
    worklist: { type: 'array', items: {
      type: 'object', required: ['key', 'state'], additionalProperties: true,
      properties: { key: { type: 'string' }, threadId: { type: 'string' }, path: { type: 'string' }, line: { type: ['integer', 'null'] }, state: { type: 'string' } } } },
  },
}
const DISPOSITION_SCHEMA = {
  type: 'object', required: ['dispositions'], additionalProperties: false,
  properties: { dispositions: { type: 'array', items: {
    type: 'object', required: ['key', 'verdict', 'action'], additionalProperties: true,
    properties: {
      key: { type: 'string' },
      verdict: { type: 'string' },                 // accepted / accepted-modified / backlogged-minor-debt / rejected / outdated / duplicate / investigate
      preFilter: { type: 'string' },               // recorded Pre-filter: line
      action: { type: 'string', enum: ['remediate', 'backlog', 'none', 'investigate'] },
      rootConcern: { type: 'string' },             // first-principles concern (NO reviewer wording)
      debtIssue: { type: 'string' },               // required by prompt when action=backlog
    } } } },
}
const REMEDIATION_SCHEMA = {
  type: 'object', required: ['key', 'blocked'], additionalProperties: true,
  properties: { key: { type: 'string' }, blocked: { type: 'boolean' }, blocker: { type: 'string' },
    changedFiles: { type: 'array', items: { type: 'string' } }, proof: { type: 'string' } },
}
const VERIFY_SCHEMA = {
  type: 'object', required: ['key', 'verified', 'closed'], additionalProperties: true,
  properties: { key: { type: 'string' }, verified: { type: 'boolean' }, closed: { type: 'boolean' },
    commit: { type: 'string' }, note: { type: 'string' } },
}

let round = 0
const summary = []
while (round < MAX_ROUNDS) {
  round++

  phase('Collect')
  const state = await agent(
    `Collect PR review-triage state for ${repo} PR #${pr}, round ${round}.\n` +
    `1. Find the PR head SHA; if a "PR Review" CI run for that SHA is still in progress, poll until it completes (it posts the round's findings).\n` +
    `2. Run: python3 ${HARNESS} --repo ${repo} --pr ${pr} --json\n` +
    `Return the parsed JSON exactly: {converged, counts, worklist[]}. Do not disposition or edit anything.`,
    { schema: COLLECT_SCHEMA, phase: 'Collect', label: `collect r${round}` })

  if (!state || state.converged) { summary.push(`round ${round}: converged`); break }
  const toDispose = (state.worklist || []).filter(w => w.state === 'NEW' || w.state === 'RE-RAISED')
  if (!toDispose.length) { summary.push(`round ${round}: nothing new to dispose`); break }

  // Role B — one disposition subagent over the round's findings. Runs the
  // mandatory pre-filter and current-PR spend gate BEFORE the five-way.
  phase('Disposition')
  const disp = await agent(
    `You are role B (independent disposition) for ${repo} PR #${pr}. Load ${SKILL}/SKILL.md, ${SKILL}/references/disposition-prefilter.md, and ~/ai/opencode/skills/git-guidelines/SKILL.md.\n` +
    `For EACH finding (by stable key), read the actual code at HEAD, run the disposition pre-filter and current-PR spend gate FIRST, record the Pre-filter line, then assign the five-way disposition. Resolve rejected/outdated/duplicate. Leave remediate/investigate findings open. For Backlogged as minor technical debt, append to an existing work-family GitHub debt issue or create one through the repository's issue route, post the thread disposition with every Gate 3 criterion and the issue link, then resolve it without role C.\n` +
    `You ONLY dispose — never propose a fix. Findings: ${JSON.stringify(toDispose)}\n` +
    `Return {dispositions[]} with, per finding: key, verdict, preFilter, action (remediate/backlog/none/investigate), rootConcern (first-principles, NO reviewer wording), and debtIssue (required URL when action=backlog).`,
    { schema: DISPOSITION_SCHEMA, phase: 'Disposition', label: `disposition r${round}` })

  const dispositions = (disp && disp.dispositions) || []
  const invalidBacklogs = dispositions.filter(d => d.action === 'backlog' && !d.debtIssue)
  if (invalidBacklogs.length) throw new Error(`backlogged findings need GitHub issue links: ${invalidBacklogs.map(d => d.key).join(', ')}`)
  const accepts = dispositions.filter(d => d.action === 'remediate' && d.rootConcern)
  const backlogged = dispositions.filter(d => d.action === 'backlog').length
  if (!accepts.length) { summary.push(`round ${round}: ${toDispose.length} findings, 0 accepts, ${backlogged} backlogged`); continue }

  // Role C + verify — pipeline each accept independently: remediate from the
  // first-principles rootConcern (A passes the concern, never reviewer wording),
  // then a separate verify+commit+close stage. Pipeline = no barrier; a finding
  // verifies as soon as its remediation lands.
  phase('Remediate')
  const results = await pipeline(accepts,
    a => agent(
      `You are role C (independent remediation) for ${repo} PR #${pr}. Load ${SKILL}/SKILL.md, anti-slop, fixing-slop, bespoke-software-policy, test-guidelines. Do NOT git commit.\n` +
      `Implement this from first principles (you were NOT given reviewer wording):\n${a.rootConcern}\n` +
      `Fail loud; no fallbacks/defaults/mocks; tests prove user-facing behavior. If it cannot be met cleanly, STOP and report blocked.\n` +
      `Return {key:'${a.key}', blocked, blocker, changedFiles[], proof}.`,
      { schema: REMEDIATION_SCHEMA, phase: 'Remediate', label: `remediate ${a.key}` }),
    (rem, a) => {
      if (!rem || rem.blocked) return { key: a.key, verified: false, closed: false, note: rem ? rem.blocker : 'remediation null' }
      return agent(
        `You are role A's verification gate for ${repo} PR #${pr}, finding ${a.key}. Load ${SKILL}/SKILL.md.\n` +
        `Phase-5 verify by hand: compare the declared remediation (${JSON.stringify(rem)}) against the ACTUAL code, answering each Phase-5 question; confirm the spec is honored and no banned patterns. Run lint/test/build.\n` +
        `If it passes: commit (co-author Claude Opus 4.8), push, and post the three-stamp closure (Disposition -> Remediation -> Verification with the commit hash) to the thread and resolve it. If it fails: report verified:false with the gap; do NOT commit.\n` +
        `Return {key:'${a.key}', verified, closed, commit, note}.`,
        { schema: VERIFY_SCHEMA, phase: 'Verify', label: `verify ${a.key}` })
    })

  const closed = results.filter(r => r && r.closed).length
  const blocked = results.filter(r => r && !r.verified).map(r => r && r.key)
  summary.push(`round ${round}: ${accepts.length} accepts, ${backlogged} backlogged, ${closed} closed${blocked.length ? ', blocked: ' + blocked.join(',') : ''}`)
  // Loop: re-collect. The push above triggers a fresh review round; convergence
  // is reached when a collect round returns converged or no finding requires
  // current-PR remediation. Backlogged debt is already linked and closed by B.
}

return { repo, pr, rounds: round, summary }
