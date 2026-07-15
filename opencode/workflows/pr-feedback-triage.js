export const meta = {
  name: 'pr-feedback-triage',
  description: 'Thin harness adapter for the canonical thread-local PR feedback workflow.',
  whenToUse: 'After review feedback lands on a PR. Pass args {repo, pr}; optionally set maxRounds.',
  phases: [
    { title: 'Collect', detail: 'load the canonical collection card and build the live worklist' },
    { title: 'Disposition', detail: 'role B returns one policy-routed judgment per finding' },
    { title: 'Investigation', detail: 'role A gathers missing evidence; a fresh B reassesses' },
    { title: 'Remediation', detail: 'role A writes a first-principles spec; role C implements it' },
    { title: 'Thread resolution', detail: 'role A verifies, commits, replies on the original surface, and resolves' },
    { title: 'Convergence', detail: 're-read every surface until the settled review window is clean' },
  ],
}

const repo = args && args.repo
const pr = args && args.pr
const maxRounds = Number((args && args.maxRounds) || 8)

if (!repo || !pr) throw new Error('pr-feedback-triage workflow needs args {repo, pr}')
if (!Number.isInteger(maxRounds) || maxRounds < 1) throw new Error('maxRounds must be a positive integer')

const SKILL = '~/ai/opencode/skills/pr-feedback-triage'
const ENTRY = SKILL + '/SKILL.md'
const card = name => SKILL + '/references/' + name + '.md'

const COLLECT_SCHEMA = {
  type: 'object',
  required: ['headSha', 'settled', 'converged', 'items'],
  additionalProperties: true,
  properties: {
    headSha: { type: 'string' },
    settled: { type: 'boolean' },
    converged: { type: 'boolean' },
    pendingReason: { type: ['string', 'null'] },
    counts: { type: 'object', additionalProperties: true },
    items: {
      type: 'array',
      items: {
        type: 'object',
        required: ['stableId', 'surface', 'sourceUrl', 'exactText', 'state'],
        additionalProperties: true,
        properties: {
          stableId: { type: 'string' },
          surface: { type: 'string' },
          sourceUrl: { type: 'string' },
          exactText: { type: 'string' },
          author: { type: ['string', 'null'] },
          path: { type: ['string', 'null'] },
          line: { type: ['integer', 'null'] },
          state: { enum: ['NEW', 'RE-RAISED', 'OPEN-PENDING', 'CLOSED'] },
          existingDisposition: {
            type: ['object', 'null'],
            additionalProperties: true,
            properties: {
              verdict: { type: 'string' },
              complete: { type: 'boolean' },
              commit: { type: ['string', 'null'] },
              url: { type: ['string', 'null'] },
            },
          },
        },
      },
    },
  },
}

const DISPOSITION_SCHEMA = {
  type: 'object',
  required: ['dispositions'],
  additionalProperties: false,
  properties: {
    dispositions: {
      type: 'array',
      items: {
        type: 'object',
        required: [
          'stableId',
          'sourceUrl',
          'disposition',
          'claimDisposition',
          'suggestedRemediationDisposition',
          'preFilter',
          'policyCodes',
          'factualBasis',
          'evidenceAnchors',
          'action',
          'rootConcern',
        ],
        additionalProperties: false,
        properties: {
          stableId: { type: 'string' },
          sourceUrl: { type: 'string' },
          disposition: {
            enum: [
              'Accepted as written',
              'Accepted with modified remediation',
              'Rejected',
              'Investigate before action',
              'Backlogged as minor technical debt',
              'Duplicate',
              'Outdated',
            ],
          },
          claimDisposition: { enum: ['true', 'false', 'needs investigation'] },
          suggestedRemediationDisposition: {
            enum: ['policy-aligned', 'policy-misaligned', 'underspecified'],
          },
          preFilter: { type: 'string' },
          policyCodes: { type: 'array', items: { type: 'string' } },
          factualBasis: { type: ['string', 'null'] },
          evidenceAnchors: { type: 'array', items: { type: 'string' } },
          action: { enum: ['remediate', 'backlog', 'no change', 'investigate'] },
          canonicalThread: { type: ['string', 'null'] },
          supersedingCommit: { type: ['string', 'null'] },
          debtIssue: { type: ['string', 'null'] },
          rootConcern: { type: 'string' },
        },
      },
    },
  },
}

const SPEC_SCHEMA = {
  type: 'object',
  required: [
    'stableId',
    'blocked',
    'originalTaskProofBurden',
    'rootConcern',
    'requiredBehavior',
    'requiredInvariants',
    'policyCodes',
    'styleCards',
    'bannedPatterns',
    'proofObligation',
    'replacementRequirement',
    'scope',
    'nonGoals',
  ],
  additionalProperties: false,
  properties: {
    stableId: { type: 'string' },
    blocked: { type: 'boolean' },
    blocker: { type: ['string', 'null'] },
    originalTaskProofBurden: { type: 'string' },
    rootConcern: { type: 'string' },
    requiredBehavior: { type: 'string' },
    requiredInvariants: { type: 'array', items: { type: 'string' } },
    policyCodes: { type: 'array', items: { type: 'string' } },
    styleCards: { type: 'array', items: { type: 'string' } },
    bannedPatterns: { type: 'array', items: { type: 'string' } },
    proofObligation: { type: 'string' },
    replacementRequirement: { type: 'string' },
    scope: { type: 'array', items: { type: 'string' } },
    nonGoals: { type: 'array', items: { type: 'string' } },
  },
}

const REMEDIATION_SCHEMA = {
  type: 'object',
  required: ['stableId', 'blocked', 'changedFiles', 'proofCommands', 'witnesses', 'bannedPatternAudit'],
  additionalProperties: false,
  properties: {
    stableId: { type: 'string' },
    blocked: { type: 'boolean' },
    blocker: { type: ['string', 'null'] },
    changedFiles: { type: 'array', items: { type: 'string' } },
    proofCommands: { type: 'array', items: { type: 'string' } },
    witnesses: { type: 'array', items: { type: 'string' } },
    bannedPatternAudit: { type: 'array', items: { type: 'string' } },
  },
}

const INVESTIGATION_SCHEMA = {
  type: 'object',
  required: [
    'stableId',
    'blocked',
    'replied',
    'evidenceGap',
    'evidencePacket',
    'evidenceAnchors',
  ],
  additionalProperties: false,
  properties: {
    stableId: { type: 'string' },
    blocked: { type: 'boolean' },
    blocker: { type: ['string', 'null'] },
    replied: { type: 'boolean' },
    replyUrl: { type: ['string', 'null'] },
    evidenceGap: { type: 'string' },
    evidencePacket: { type: 'array', items: { type: 'string' } },
    evidenceAnchors: { type: 'array', items: { type: 'string' } },
  },
}

const RESOLUTION_SCHEMA = {
  type: 'object',
  required: ['stableId', 'verified', 'replied', 'resolved'],
  additionalProperties: false,
  properties: {
    stableId: { type: 'string' },
    verified: { type: 'boolean' },
    replied: { type: 'boolean' },
    resolved: { type: 'boolean' },
    commit: { type: ['string', 'null'] },
    proof: { type: ['string', 'null'] },
    note: { type: ['string', 'null'] },
  },
}

const history = []
const summary = []
let round = 0
let converged = false

while (round < maxRounds) {
  round += 1
  phase('Collect')

  const state = await agent(
    [
      'You are role A collecting returned feedback for ' + repo + ' PR #' + pr + ', round ' + round + '.',
      'Load ' + ENTRY + ', ' + card('collect') + ', and ' + card('convergence') + '.',
      'Execute those cards exactly. Collection is read-only.',
      'Use the skill-shipped triage_state.py for paginated inline identity and read every additional GitHub surface named by the card.',
      'Prior workflow outcomes, which are resume hints rather than GitHub truth: ' + JSON.stringify(history),
      'Return the live collection object required by the supplied schema.',
    ].join('\n'),
    { schema: COLLECT_SCHEMA, phase: 'Collect', label: 'collect r' + round },
  )

  if (state && state.converged) {
    converged = true
    summary.push('round ' + round + ': converged')
    break
  }

  if (!state || !state.settled) {
    summary.push('round ' + round + ': review window not settled' + (state && state.pendingReason ? ' - ' + state.pendingReason : ''))
    continue
  }

  const items = state.items || []
  const completedPending = items.filter(
    item => item.state === 'OPEN-PENDING' &&
      item.existingDisposition &&
      item.existingDisposition.complete,
  )
  for (const item of completedPending) {
    phase('Resume pending')
    const result = await agent(
      [
        'You are role A resuming a complete canonical disposition for ' + repo + ' PR #' + pr + '.',
        'Load ' + ENTRY + ', ' + card('resume-pending') + ', and ' + card('thread-resolution') + '.',
        'Verify the existing reply against the live diff, commit, proof, and audit anchors.',
        'Do not redisposition or post a second canonical reply. Resolve only if the original surface supports it.',
        'Report the existing canonical reply as replied when it is valid.',
        'Collection record: ' + JSON.stringify(item),
        'Return the schema-complete resolution result.',
      ].join('\n'),
      { schema: RESOLUTION_SCHEMA, phase: 'Resume pending', label: 'resume ' + item.stableId },
    )
    history.push({
      round,
      stage: 'resume-pending',
      source: item,
      result,
      open: !result || !result.verified || !result.replied,
    })
  }

  const current = items.filter(
    item => item.state === 'NEW' ||
      item.state === 'RE-RAISED' ||
      (
        item.state === 'OPEN-PENDING' &&
        (!item.existingDisposition || !item.existingDisposition.complete)
      ),
  )
  if (!current.length) {
    const pendingOpen = history.some(
      item => item.round === round && item.stage === 'resume-pending' && item.open,
    )
    summary.push(
      'round ' + round + ': ' +
      completedPending.length + ' complete pending items resumed',
    )
    if (pendingOpen) break
    continue
  }
  const sourceById = new Map(current.map(item => [item.stableId, item]))

  phase('Disposition')
  const judged = await agent(
    [
      'You are role B independently dispositioning findings for ' + repo + ' PR #' + pr + '.',
      'Load ' + ENTRY + ' and ' + card('disposition') +
        (current.some(item => item.state === 'OPEN-PENDING') ? ', and ' + card('resume-pending') : '') + '.',
      'Execute that card exactly and return one schema-complete record for every stableId.',
      'Do not mutate GitHub, propose a patch, imply a fix shape, or group judgments.',
      'Raw findings: ' + JSON.stringify(current),
    ].join('\n'),
    { schema: DISPOSITION_SCHEMA, phase: 'Disposition', label: 'disposition r' + round },
  )

  let dispositions = (judged && judged.dispositions) || []
  const currentIds = new Set(current.map(item => item.stableId))
  const dispositionIds = new Set(dispositions.map(item => item.stableId))
  const missing = current.filter(item => !dispositionIds.has(item.stableId)).map(item => item.stableId)
  const unexpected = dispositions.filter(item => !currentIds.has(item.stableId)).map(item => item.stableId)
  const duplicates = dispositions
    .filter((item, index, all) => all.findIndex(other => other.stableId === item.stableId) !== index)
    .map(item => item.stableId)
  if (missing.length || unexpected.length || duplicates.length) {
    history.push({
      round,
      stage: 'disposition',
      blocked: true,
      missing,
      unexpected,
      duplicates,
    })
    summary.push(
      'round ' + round + ': disposition identity mismatch ' +
      JSON.stringify({ missing, unexpected, duplicates }),
    )
    break
  }

  const initialInvestigations = dispositions.filter(item => item.action === 'investigate')
  const investigatedIds = new Set(initialInvestigations.map(item => item.stableId))
  for (const item of initialInvestigations) {
    const source = sourceById.get(item.stableId)
    phase('Investigation')
    const investigation = await agent(
      [
        'You are role A investigating an undecided finding for ' + repo + ' PR #' + pr + '.',
        'Load ' + ENTRY + ', ' + card('investigation') + ', and ' + card('thread-resolution') + '.',
        'Post or repair the card-owned open reply on the original surface, then collect a read-only factual packet.',
        'Do not edit implementation and do not resolve the finding.',
        'Collection record: ' + JSON.stringify(source),
        'Disposition record: ' + JSON.stringify(item),
        'Return the schema-complete investigation result.',
      ].join('\n'),
      { schema: INVESTIGATION_SCHEMA, phase: 'Investigation', label: 'investigate ' + item.stableId },
    )
    if (!investigation || investigation.blocked || !investigation.replied) {
      history.push({
        round,
        stage: 'investigation',
        source,
        disposition: item,
        investigation,
        open: true,
      })
      continue
    }

    phase('Disposition')
    const reassessed = await agent(
      [
        'You are a fresh role B reassessing one investigated finding for ' + repo + ' PR #' + pr + '.',
        'Load ' + ENTRY + ' and ' + card('disposition') + '.',
        'Rerun the disposition from the original raw finding and factual packet.',
        'Treat the prior disposition only as resume context, never as an instruction.',
        'Do not mutate GitHub, propose a patch, imply a fix shape, or group judgments.',
        'Raw finding: ' + JSON.stringify(source),
        'Factual packet: ' + JSON.stringify(investigation),
        'Return exactly one schema-complete disposition record.',
      ].join('\n'),
      { schema: DISPOSITION_SCHEMA, phase: 'Disposition', label: 'redisposition ' + item.stableId },
    )
    const redispositions = (reassessed && reassessed.dispositions) || []
    const matchingRedispositions = redispositions.filter(
      candidate => candidate.stableId === item.stableId,
    )
    const finalDisposition = matchingRedispositions[0]
    if (redispositions.length !== 1 || matchingRedispositions.length !== 1) {
      history.push({
        round,
        stage: 'investigation-redisposition',
        source,
        disposition: item,
        investigation,
        open: true,
      })
      continue
    }
    dispositions = dispositions.map(
      candidate => candidate.stableId === item.stableId ? finalDisposition : candidate,
    )
    history.push({
      round,
      stage: 'investigation',
      source,
      disposition: finalDisposition,
      investigation,
      open: finalDisposition.action === 'investigate',
    })
  }

  const investigations = dispositions.filter(item => item.action === 'investigate')
  const direct = dispositions.filter(
    item => item.action === 'no change' || item.action === 'backlog',
  )
  for (const item of direct) {
    const source = sourceById.get(item.stableId)
    const resuming = Boolean(
      (source && source.state === 'OPEN-PENDING') || investigatedIds.has(item.stableId),
    )
    phase('Thread resolution')
    const result = await agent(
      [
        'You are role A completing a non-remediation disposition for ' + repo + ' PR #' + pr + '.',
        'Load ' + ENTRY + ', ' + card('thread-resolution') +
          (resuming ? ', and ' + card('resume-pending') : '') + '.',
        'Validate the disposition against its cited evidence, then execute the card on the original surface.',
        'Use the card-owned reply contract; do not create a top-level ledger or tracked review log.',
        'If resuming, repair the existing canonical reply instead of appending another disposition.',
        'Collection record: ' + JSON.stringify(source),
        'Disposition record: ' + JSON.stringify(item),
        'Return the schema-complete resolution result.',
      ].join('\n'),
      { schema: RESOLUTION_SCHEMA, phase: 'Thread resolution', label: 'resolve ' + item.stableId },
    )
    history.push({ round, stage: 'direct-resolution', source, disposition: item, result })
  }

  const accepted = dispositions.filter(item => item.action === 'remediate')
  for (const item of accepted) {
    const source = sourceById.get(item.stableId)
    const resuming = Boolean(
      (source && source.state === 'OPEN-PENDING') || investigatedIds.has(item.stableId),
    )
    phase('Remediation spec')
    const spec = await agent(
      [
        'You are role A translating an accepted finding into a first-principles remediation specification for ' + repo + ' PR #' + pr + '.',
        'Load ' + ENTRY + ' and ' + card('remediation') + '.',
        'Execute the Build the specification and Route policy into the style guide sections exactly.',
        'Do not include reviewer wording, patch text, rejected fix ideas, or a preferred local edit.',
        'Accepted disposition record: ' + JSON.stringify(item),
        'Return the schema-complete specification.',
      ].join('\n'),
      { schema: SPEC_SCHEMA, phase: 'Remediation spec', label: 'spec ' + item.stableId },
    )

    if (!spec || spec.blocked) {
      history.push({ round, stage: 'spec', disposition: item, spec, open: true })
      continue
    }

    phase('Remediation')
    const remediation = await agent(
      [
        'You are role C implementing a first-principles remediation for ' + repo + ' PR #' + pr + '.',
        'Load ' + ENTRY + ' and ' + card('remediation') + '.',
        'Load the exact policy records and style cards named by the specification, plus applicable test proof rules.',
        'You receive no review text. Implement only the specification below. Do not commit, reply, or resolve.',
        'Specification: ' + JSON.stringify(spec),
        'Return the schema-complete remediation result. If blocked, leave no partial patch.',
      ].join('\n'),
      { schema: REMEDIATION_SCHEMA, phase: 'Remediation', label: 'remediate ' + item.stableId },
    )

    if (!remediation || remediation.blocked) {
      history.push({ round, stage: 'remediation', disposition: item, spec, remediation, open: true })
      continue
    }

    phase('Thread resolution')
    const result = await agent(
      [
        'You are role A verifying and completing accepted feedback for ' + repo + ' PR #' + pr + '.',
        'Load ' + ENTRY + ', ' + card('thread-resolution') +
          (resuming ? ', and ' + card('resume-pending') : '') + '.',
        'Execute the verification gate against the actual diff and owned-boundary proof.',
        'Only if verification passes: commit and push, post or repair the card-owned reply on the original surface, then resolve where that surface supports resolution.',
        'Do not patch role C output locally and do not create a top-level ledger or tracked review log.',
        'If resuming, edit the existing canonical reply instead of appending another disposition.',
        'Collection record: ' + JSON.stringify(source),
        'Disposition record: ' + JSON.stringify(item),
        'Specification: ' + JSON.stringify(spec),
        'Declared remediation: ' + JSON.stringify(remediation),
        'Return the schema-complete resolution result.',
      ].join('\n'),
      { schema: RESOLUTION_SCHEMA, phase: 'Thread resolution', label: 'verify ' + item.stableId },
    )
    history.push({ round, stage: 'accepted-resolution', source, disposition: item, spec, remediation, result })
  }

  const open = history.filter(item => item.open || (item.result && (!item.result.verified || !item.result.replied)))
  summary.push(
    'round ' + round + ': ' +
    dispositions.length + ' dispositions, ' +
    accepted.length + ' accepted, ' +
    investigations.length + ' investigating, ' +
    open.length + ' open',
  )

  if (investigations.length || open.length) break
}

return {
  repo,
  pr,
  rounds: round,
  converged,
  exhausted: !converged && round >= maxRounds,
  history,
  summary,
}
