// Workflow template — phase 3 (research) + phase 4 (verification).
// Adapt: DIR, DATE, LANG, CONTEXT (P-xx model summary), UNITS (by caliber),
// MAX_CLAIMS (1 in light, 2 otherwise). Hardcode the values (no Date.now in
// Workflow scripts; `args` may not be transmitted — code the constants).
// Record the returned runId in etat.md (resume via resumeFromRunId).
//
// Language: write the whole instantiated script — CONTEXT, missions,
// shared instructions, verdict enum labels — in the DOSSIER language, so
// that sub-agents produce notes and verdicts in that language. The example
// strings below are English; the reference execution used French
// (palette: corroborée / nuancée / fragilisée / réfutée / introuvable).

export const meta = {
  name: 'contre-expertise-research',
  description: 'Research fan-out + adversarial verification of claims',
  phases: [
    { title: 'Research', detail: 'WebSearch/WebFetch units across 3 axes' },
    { title: 'Verification', detail: 'adversarial refutation of claims' },
  ],
}

const DIR = '/ABSOLUTE/path/to/<output-root>/<date>-contre-expertise-<slug>'
const DATE = '<YYYY-MM-DD>'
const MAX_CLAIMS = 2

const CONTEXT = `CONTEXT — Today is ${DATE}.
<Summary of the audited model, 10-20 lines, with the structuring P-xx
and the limits the author admits.>`

const SHARED_INSTRUCTIONS = `SHARED INSTRUCTIONS:
1. Load the web tools first: ToolSearch query "select:WebSearch,WebFetch".
2. Cross-check several searches (English AND the corpus language when
   relevant), then WebFetch the primary sources (at least 4-6 successful
   fetches). A URL may appear in your note ONLY if it came from a search or
   a successful fetch — NEVER invent a reference from memory.
3. Also search for what contradicts: your role is to investigate for and
   against, not to comfort. ACTIVELY SEARCH for documented failure cases
   (abandonments, published critiques, negative reports) — not only the
   promoters. If an expected source does not exist, say so explicitly.
4. Write your full note in MARKDOWN, in the dossier language, to the
   indicated file (Write tool, absolute path), following the
   fiche-recherche.md template: per-source entries (metadata, summary,
   P-xx convergences, tensions, quotations), a "Failure cases found"
   section, then "Carrying claims" with C-<unit>-<n> IDs.
5. Markdownlint-clean: no trailing punctuation in headings, URLs in <>,
   blank lines around headings and lists.
6. Structured return: resume = 8-15 dense lines; claims_cles = the same
   claims as in the note (with their IDs).`

const RESEARCH_SCHEMA = {
  type: 'object',
  required: ['fichier', 'resume', 'claims_cles'],
  properties: {
    fichier: { type: 'string' },
    resume: { type: 'string' },
    claims_cles: {
      type: 'array', maxItems: MAX_CLAIMS,
      items: {
        type: 'object', required: ['id', 'claim', 'source_url'],
        properties: {
          id: { type: 'string' },
          claim: { type: 'string' },
          source_url: { type: 'string' },
        },
      },
    },
  },
}

// Localize the enum labels to the dossier language when instantiating —
// they end up verbatim in 90-verifications.md.
const VERDICT_SCHEMA = {
  type: 'object',
  required: ['verdict', 'peremption', 'preuves', 'commentaire'],
  properties: {
    verdict: { type: 'string', enum: ['corroborated', 'nuanced', 'weakened', 'refuted', 'not-found'] },
    peremption: { type: 'string', description: 'YYYY-MM-DD — date after which to re-verify' },
    preuves: {
      type: 'array',
      items: { type: 'object', required: ['url'], properties: { url: { type: 'string' }, extrait: { type: 'string' } } },
    },
    commentaire: { type: 'string' },
  },
}

// Units by caliber — axis A (comparable methods), B (practices), C (corpus sources).
const UNITS = [
  { id: 'a1-<slug>', mission: `MISSION: <document method family X;
    precise points to investigate; expected divergences with the P-xx>.` },
  // …
]

function researchPrompt(u) {
  return `${CONTEXT}\n\n${u.mission}\n\n${SHARED_INSTRUCTIONS}\n\nNote file: ${DIR}/notes/${u.id}.md`
}

phase('Research')
log(`${UNITS.length} units — notes in ${DIR}/notes/`)

const results = await pipeline(
  UNITS,
  u => agent(researchPrompt(u), { label: `research:${u.id}`, phase: 'Research', schema: RESEARCH_SCHEMA }),
  (res, u) => {
    if (!res || !res.claims_cles || res.claims_cles.length === 0) return { unit: u.id, resume: res ? res.resume : null, claims: [] }
    return parallel(res.claims_cles.map(c => () =>
      agent(`Today is ${DATE}. You are an adversarial verifier. Try to REFUTE:

CLAIM ${c.id}: "${c.claim}"
Announced source: ${c.source_url}

Load the web tools (ToolSearch "select:WebSearch,WebFetch"), read the
primary source, check that it really says this (exact figures, scope —
beware of motivating examples presented as averages), then search for
contrary sources (1-3 searches). Set an expiry date for the verdict
(+3 months for fast-moving benchmark topics, +6 months otherwise).
Comment in the dossier language, precise.`,
        { label: `verify:${c.id}`, phase: 'Verification', schema: VERDICT_SCHEMA })
        .then(v => ({ id: c.id, claim: c.claim, source_url: c.source_url, verdict: v }))
    )).then(verdicts => ({ unit: u.id, resume: res.resume, fichier: res.fichier, claims: verdicts.filter(Boolean) }))
  }
)

return { unites: results.filter(Boolean) }
