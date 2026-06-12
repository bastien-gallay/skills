// Gabarit de Workflow — phase 3 (recherche) + phase 4 (vérification).
// À adapter : DIR, DATE, CONTEXTE (résumé du modèle P-xx), UNITS (selon calibre),
// MAX_CLAIMS (1 en leger, 2 sinon). Valeurs en dur (pas de Date.now dans les
// scripts de Workflow ; `args` peut ne pas être transmis — codez les constantes).
// Consigner le runId retourné dans etat.md (reprise via resumeFromRunId).

export const meta = {
  name: 'contre-expertise-recherche',
  description: 'Fan-out de recherche + vérification adversariale des claims',
  phases: [
    { title: 'Recherche', detail: 'unités WebSearch/WebFetch sur 3 axes' },
    { title: 'Vérification', detail: 'réfutation adversariale des claims' },
  ],
}

const DIR = '/ABSOLU/vers/.personal/research/<date>-contre-expertise-<slug>'
const DATE = '<YYYY-MM-DD>'
const MAX_CLAIMS = 2

const CONTEXTE = `CONTEXTE — Nous sommes le ${DATE}.
<Résumé du modèle audité, 10-20 lignes, avec les P-xx structurants
et les limites avouées par l'auteur.>`

const CONSIGNES = `CONSIGNES COMMUNES :
1. Charge d'abord les outils web : ToolSearch query "select:WebSearch,WebFetch".
2. Croise plusieurs recherches (anglais ET français quand pertinent), puis
   WebFetch les sources primaires (au moins 4-6 fetches réussis). Une URL ne
   peut figurer dans ta note QUE si elle provient d'une recherche ou d'un
   fetch réussi — n'invente JAMAIS une référence de mémoire.
3. Cherche AUSSI ce qui contredit : ton rôle est d'instruire à charge et à
   décharge, pas de conforter. CHERCHE ACTIVEMENT les cas d'échec documentés
   (abandons, critiques publiées, retours négatifs) — pas seulement les
   promoteurs. Si une source attendue n'existe pas, dis-le explicitement.
4. Écris ta note complète en MARKDOWN FRANÇAIS dans le fichier indiqué
   (outil Write, chemin absolu), au format du gabarit fiche-recherche.md :
   fiches par source (métadonnées, résumé, convergences P-xx, tensions,
   citations), section « Cas d'échec trouvés », puis « Claims porteuses »
   avec IDs C-<unité>-<n>.
5. Markdownlint-propre : pas de ponctuation finale dans les titres, URLs
   entre <>, lignes vides autour des titres et listes.
6. Retour structuré : resume = 8-15 lignes denses ; claims_cles = les mêmes
   claims que dans la note (avec leurs IDs).`

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

const VERDICT_SCHEMA = {
  type: 'object',
  required: ['verdict', 'peremption', 'preuves', 'commentaire'],
  properties: {
    verdict: { type: 'string', enum: ['corroborée', 'nuancée', 'fragilisée', 'réfutée', 'introuvable'] },
    peremption: { type: 'string', description: 'YYYY-MM-DD — date au-delà de laquelle re-vérifier' },
    preuves: {
      type: 'array',
      items: { type: 'object', required: ['url'], properties: { url: { type: 'string' }, extrait: { type: 'string' } } },
    },
    commentaire: { type: 'string' },
  },
}

// Unités selon calibre — axe A (méthodes comparables), B (pratiques), C (sources du corpus).
const UNITS = [
  { id: 'a1-<slug>', mission: `MISSION : <documenter la famille de méthodes X ;
    points précis à instruire ; divergences attendues avec les P-xx>.` },
  // …
]

function researchPrompt(u) {
  return `${CONTEXTE}\n\n${u.mission}\n\n${CONSIGNES}\n\nFichier de note : ${DIR}/notes/${u.id}.md`
}

phase('Recherche')
log(`${UNITS.length} unités — notes dans ${DIR}/notes/`)

const results = await pipeline(
  UNITS,
  u => agent(researchPrompt(u), { label: `recherche:${u.id}`, phase: 'Recherche', schema: RESEARCH_SCHEMA }),
  (res, u) => {
    if (!res || !res.claims_cles || res.claims_cles.length === 0) return { unit: u.id, resume: res ? res.resume : null, claims: [] }
    return parallel(res.claims_cles.map(c => () =>
      agent(`Nous sommes le ${DATE}. Tu es un vérificateur adversarial. Essaie de RÉFUTER :

CLAIM ${c.id} : « ${c.claim} »
Source annoncée : ${c.source_url}

Charge les outils web (ToolSearch "select:WebSearch,WebFetch"), lis la source
primaire, vérifie qu'elle dit bien cela (chiffres exacts, portée — attention
aux exemples motivants présentés comme moyennes), puis cherche des sources
contraires (1-3 recherches). Fixe une date de péremption du verdict (+3 mois
si benchmarks mouvants, +6 mois sinon). Commentaire en français, précis.`,
        { label: `verif:${c.id}`, phase: 'Vérification', schema: VERDICT_SCHEMA })
        .then(v => ({ id: c.id, claim: c.claim, source_url: c.source_url, verdict: v }))
    )).then(verdicts => ({ unit: u.id, resume: res.resume, fichier: res.fichier, claims: verdicts.filter(Boolean) }))
  }
)

return { unites: results.filter(Boolean) }
