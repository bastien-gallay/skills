# redaction — Boucle d'édition critique pour écrits longs

Skill Claude Code (et hosts compatibles) qui transforme Claude en
**éditeur exigeant** sur des articles, billets et essais. Critique
honnête sans flatterie, détection de drift AI et de pièges propres à
l'auteur, boucle paragraphe-par-paragraphe avec scaffold puis report
dans le fichier — et un état persistant entre sessions porté par un
fichier de suivi.

## Why

La rédaction d'opinion longue avec un LLM dérape vers deux pièges
symétriques :

- *(a)* le LLM **rédige les paragraphes de prise de position à la place
  de l'auteur** — la voix se dilue, l'engagement s'efface.
- *(b)* le LLM **flatte le brouillon** plutôt que de signaler les
  dérives (thèse molle, hedging, registre LinkedIn, énumération qui
  esquive la nomination).

`redaction` impose un contrat de facilitation strict :

- **Claude ne rédige pas les paragraphes-cœur** où l'auteur prend
  position. Il scaffolde, critique, propose des formes — la voix reste
  celle de l'auteur.
- **Critique honnête sans flatterie.** Pas de « excellent ! » sur du
  consensus mou ; enthousiasme appuyé sur les vraies réussites
  (« bijoux »).
- **Une dérive principale par tour.** Pas de noyade sous 12 micro-issues
  — *le* piège central à corriger, nommé avec son code `Axx` (drift AI)
  ou `Bxx` (piège propre à l'auteur).

## What's in the box

```text
redaction/
├── .claude-plugin/
│   ├── plugin.json              # Manifeste Claude Code plugin
│   └── marketplace.json         # Catalog single-plugin
├── .github/workflows/release.yml
├── skills/
│   └── redaction/
│       ├── SKILL.md             # Prompt facilitateur
│       └── suivi-template.md    # Template du SUIVI-<basename>.md
├── docs/                        # Notes mainteneur (RELEASING, etc.)
├── CHANGELOG.md
├── CLAUDE.md
├── LICENSE
├── README.md
└── justfile                     # release + package automation
```

## Workflow

```text
Phase 0 : Cadrage (angle + méthodo + squelette + scaffold SUIVI)
   ↓
Phase 1 : Boucle paragraphe par paragraphe
   ├─ Scaffold (Claude)
   ├─ Draft V1 (utilisateur)
   ├─ Critique (Claude, tag Axx/Bxx)
   ├─ Draft V2 (utilisateur)
   └─ Report dans fichier + update SUIVI
   ↓
Phase 2 : Hygiène finale
```

Le fichier `.personal/ecriture/SUIVI-<basename>.md` est la **source de
vérité de l'état d'avancement** : thèse verrouillée, bijoux à préserver,
pièges traversés (avec code Axx/Bxx), décisions actées, journal de
session. Il survit aux sessions — à la reprise, Claude le lit en entier
avant toute critique et ne re-cadre pas ce qu'il verrouille.

## Pièges détectés

Catalogue propre au skill (cross-référencé aux codes `Axx`/`Bxx` de
`style-bastien.md` §0 quand un équivalent existe) :

| Piège | Code |
| --- | --- |
| Thèse molle (consensus mou) | *(candidat §0)* |
| Hedging | `A8` / `B3` |
| Registre LinkedIn / consulting / keynote | `B1` |
| Re-cloisonnement involontaire | *(candidat §0)* |
| Énumération qui esquive la nomination | *(candidat §0)* |
| Croissance quantitative au lieu de convergence | *(candidat §0)* |
| Transitions de mémoire / dissertation | `B4` |
| Pathos d'enfance / sur-affirmation | `B4` |
| Conclusion qui nuance au lieu d'appeler | `B2` |

## Installation

### En dev local (symlink, recommandé pour itérer sur le skill)

```bash
git clone <repo-url> ~/Dev/personal/skills/redaction
ln -s ~/Dev/personal/skills/redaction/skills/redaction \
      ~/.claude/skills/redaction
```

### Comme plugin Claude Code (quand un remote sera publié)

```bash
/plugin marketplace add <owner>/redaction
/plugin install redaction@redaction
```

## License

MIT — voir `LICENSE`.
