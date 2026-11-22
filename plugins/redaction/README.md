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
│   └── plugin.json              # Manifeste Claude Code plugin
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

### Comme plugin Claude Code (marketplace)

```bash
/plugin marketplace add bastien-gallay/skills
/plugin install redaction@skills
```

### Comme skill `.skill` (Claude Desktop, claude.ai web)

Chaque release attache un bundle `redaction-vX.Y.Z.skill` (un zip avec
`redaction/SKILL.md` à la racine) — voir la page
[Releases](https://github.com/bastien-gallay/skills/releases) (tags `redaction/vX.Y.Z`).

- **Claude Desktop** : double-clic sur le `.skill` téléchargé (le format
  est enregistré par l'OS pour l'installation en un clic).
- **claude.ai (web)** : importer le `.skill` via l'uploader de skills.

> **Note hors Claude Code.** Le cœur du skill (boucle critique, taxonomie
> des pièges, interdit de rédaction des paragraphes-cœur) fonctionne
> partout. La **persistance fichier** du `SUIVI-*.md` suppose un
> filesystem ; sur un host sans écriture persistante, le skill bascule en
> **mode inline** — il maintient le SUIVI dans la conversation et
> l'exporte en fin de session pour que vous le recolliez à la reprise
> (cf. `SKILL.md`, section « Fallback sans filesystem persistant »).

### En dev local (symlink, recommandé pour itérer sur le skill)

```bash
git clone https://github.com/bastien-gallay/skills.git \
      ~/Dev/oss/skills-mono
ln -s ~/Dev/oss/skills-mono/plugins/redaction/skills/redaction \
      ~/.claude/skills/redaction
```

### Construire le bundle `.skill` localement

```bash
just package   # → dist/redaction-vX.Y.Z.skill
```

## License

MIT — voir `LICENSE`.
