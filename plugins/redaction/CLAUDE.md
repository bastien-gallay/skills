# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working
with code in this repository.

## What this repo is

`redaction` est un **package de skill Claude Code**, pas une application.
Pas de build runtime, pas de tests. Le « produit » est deux fichiers
markdown installés comme skill dans Claude Code et chargés comme prompt
en début de session :

- `skills/redaction/SKILL.md` — le prompt facilitateur. Définit le
  workflow (Phase 0 cadrage / Phase 1 boucle paragraphe-par-paragraphe /
  Phase 2 hygiène), le cycle de vie du fichier de suivi, la taxonomie
  des pièges (avec cross-référence Axx/Bxx vers `style-bastien.md` du
  repo consommateur), le format de retour, les anti-patterns.
- `skills/redaction/suivi-template.md` — template du fichier
  `SUIVI-<basename>.md` que le skill scaffolde automatiquement dans
  `.personal/ecriture/` du repo consommateur, au démarrage. Sections
  obligatoires + optionnelles (commentées dans le scaffold initial).

Le repo contient aussi les manifestes qui le rendent installable comme
plugin Claude Code :

- `.claude-plugin/plugin.json` — manifeste Claude Code. Plugin name =
  `redaction` ; skill auto-découvert à `skills/redaction/`.
- `.claude-plugin/marketplace.json` — catalog single-plugin permettant
  `/plugin marketplace add <owner>/redaction` puis
  `/plugin install redaction@redaction`. Source `"./"` car la racine du
  plugin = racine du marketplace.

## Installation locale (dev)

Symlink `~/.claude/skills/redaction → skills/redaction` (créé à
l'initialisation du repo). Toute édition de `SKILL.md` ou de
`suivi-template.md` est immédiatement reflétée dans Claude Code, sans
réinstallation.

```bash
ln -s ~/Dev/personal/skills/redaction/skills/redaction \
      ~/.claude/skills/redaction
```

## Architecture invariants

- **`SKILL.md` drive le process, `suivi-template.md` fournit la structure
  de l'état persistant.** Pas d'inlining du template dans SKILL.md (il
  serait dupliqué dans chaque scaffold) ; pas de logique de workflow
  dans le template (il est un scaffold pur, copiable verbatim).
- **Le SUIVI est l'état persistant entre sessions.** Toute évolution du
  workflow doit considérer son impact sur le format du SUIVI
  (rétrocompatibilité des SUIVI existants chez les consommateurs).
- **Codes `Axx`/`Bxx` référencent `style-bastien.md` §0.** Ce fichier
  vit dans le repo *consommateur* (par exemple
  `bastiengallay.com/.personal/`), **pas ici**. La cross-référence est
  par convention de nommage. Si la checklist §0 évolue, mettre à jour
  les tags dans `SKILL.md`. Les pièges propres au skill (sans code §0)
  sont marqués `(candidat §0)` et destinés à être promus en règle Axx
  ou Bxx du repo consommateur via un futur mode rétrospectif.
- **Pas de paragraphes de prise de position rédigés par Claude.**
  Interdit central du skill (cf. `SKILL.md` § « Anti-patterns côté
  Claude »). Toute évolution qui assouplirait cet interdit casserait
  la valeur de facilitation du skill.

## Release

Quick path :

```bash
just check-versions   # vérifie que plugin.json et marketplace.json sont alignés
just release 0.2.0    # bump + commit + tag (nécessite une section CHANGELOG.md correspondante)
just package          # construit dist/redaction-v<version>.skill
```

Voir `docs/RELEASING.md` pour les détails du processus.
