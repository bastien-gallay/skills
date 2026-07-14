# Normalisation des skills — audit & plan

Document fondateur du hub `bastien-gallay/skills`. Source : audit du 2026-07-14.

## 1. Deux classes, pas une

| Classe | Définition | Membres | Convention cible |
| --- | --- | --- | --- |
| **A — Skills** | Distribuable en plugin Claude Code | bfw, feature-torture, redaction, contre-expertise, pair-with-me, rhetorical-analysis | `.claude-plugin/plugin.json` + marketplace mono-plugin + `skills/<name>/SKILL.md` + README + RELEASING |
| **B — Styles** | Bascule de comportement, multi-cible (claude-code + claude-ai) | flair, glance | `prompt.md` + `claude-code/` + `claude-ai/` + `build.sh` + `install.sh` |

Les repos restent **séparés** (versioning + distribution indépendants). Le hub agrège, il ne fusionne pas.

## 2. Convention canonique — Classe A (Skills)

Référence = **feature-torture** / **redaction** (déjà conformes).

- **Emplacement SKILL.md** : `skills/<skill-name>/SKILL.md` (jamais à la racine).
- **Manifest** : `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` mono-plugin.
- **Frontmatter SKILL.md** : `name` + `description` en scalaire replié (`>`).
- **Règle de description** : doit contenir une clause explicite `Use when` / `Trigger:` avec les phrases de déclenchement. C'est ce qui rend le skill découvrable.
- **Docs** : `README.md`, `CHANGELOG.md`, `docs/RELEASING.md`, `.markdownlint.json`.
- **Nom repo ≠ nom skill** : toléré (`bfw`→`brainstorm`, `rhetorical-analysis-skill`→`rhetorical-analysis`) mais le registre doit mapper les deux.

## 3. Actions par skill

| Skill | Action | Effort | Risque |
| --- | --- | --- | --- |
| feature-torture | Aucune (référence) | — | — |
| redaction | Aucune (référence) | — | — |
| bfw | Enrichir la `description` avec une clause *Trigger/Use when* | XS | nul |
| contre-expertise | Ajouter `plugin.json` + `marketplace.json` mono-plugin | S | faible |
| pair-with-me | Déplacer `SKILL.md` → `skills/pair-with-me/SKILL.md` + ajouter manifests | M | moyen (dépend d'impeccable — vérifier chemins) |
| rhetorical-analysis | **Décidé : promouvoir en plugin.** Déplacer SKILL.md → `skills/rhetorical-analysis/`, ajouter `plugin.json` + `marketplace.json`. Conserver les cibles multi-agents (.cursor/.gemini/.opencode) en parallèle. | M | moyen (ne pas casser les cibles existantes) |
| flair | Aucune ; réétiqueter `category: style` dans le registre | XS | nul |
| glance | Aucune ; idem flair | XS | nul |

## 4. Orphelins racine

| Fichier | Nature | Décision |
| --- | --- | --- |
| `glance.tar.gz` | Artefact de build périmé (le repo glance existe) | ✅ **Supprimé** (2026-07-14) |
| `meeting-screenshot-extractor.skill` | Bundle `.skill` zippé, sans repo source ici | ✅ **Dézippé** en `meeting-screenshot-extractor/` (2026-07-14). Reste à : `git init` + ajouter manifests Classe A + pousser en repo dédié. |

## 5. Mutualisation (socle partagé `shared/`)

Fichiers dupliqués et divergents à extraire en versions canoniques :

- `.markdownlint.json` (présent dans bfw, redaction, rhetorical…)
- `docs/RELEASING.md` (dupliqué dans bfw, feature-torture, redaction)
- `build.sh` / `install.sh` (flair, glance — quasi identiques)
- `skill-template/` : squelette pour tout nouveau skill Classe A.

## 6. Source de vérité : `registry.json`

Un fichier machine-lisible qui alimente **et** le méta-marketplace **et** la page vitrine :

```jsonc
{
  "skills": [
    { "name": "brainstorm", "repo": "bfw", "class": "skill",
      "domain": "facilitation", "trigger": "...", "status": "stable" }
    // ...
  ]
}
```

## 6b. État d'exécution (2026-07-14)

Alignement fait par workflow multi-agents (1 agent/repo), commits **signés GPG, non poussés**, branche `chore/normalize-hub` (sauf meeting-screenshot : `main`).

| Skill | Commit | Statut |
| --- | --- | --- |
| bfw | `Add explicit trigger/use-when clause…` | ✅ signé |
| contre-expertise | `Add plugin and marketplace manifests…` | ✅ signé |
| pair-with-me | `Normalize pair-with-me to class-A…` | ✅ signé |
| rhetorical-analysis | `Promote rhetorical-analysis to a Class-A…` | ✅ signé |
| meeting-screenshot | `Normalize meeting-screenshot-extractor…` | ✅ signé (repo neuf) |

### Suivis — résolus (2026-07-14)

1. ✅ **pair-with-me / `install.sh`** : repointé sur `$REPO_DIR/skills/pair-with-me` (+ garde-fou sur `SKILL.md`). Commit signé sur `chore/normalize-hub`.
2. ✅ **bfw / doublon + gitignore** : pattern `brainstorm/`/`wip/` **ancrés** à la racine (`/brainstorm/`, `/wip/`) — il masquait `skills/brainstorm/` ; `.claude/skills/` explicitement ignoré. La copie locale dérivée (`.claude/skills/brainstorm/SKILL.md`, 11742 o vs 19292 o) est **conservée sur disque** (suppression refusée par le classifier, non nommée) mais neutralisée par le gitignore — à supprimer manuellement si voulu.
3. ✅ **rhetorical / copie `skills/`** : rendue **auto-portante** (option A) — `references/` + `assets/` vendorisés sous `skills/rhetorical-analysis/`, l'étape script bascule sur la console `generate-analysis`. La racine reste la source de build (`pyproject readme`, `package_skill.py`) ; `scripts/` reste le package Python racine.
4. ✅ **meeting-screenshot** : repo public `bastien-gallay/meeting-screenshot-extractor` **créé + `main` poussé**.

### État des PR

| Repo | Branche | PR |
| --- | --- | --- |
| bfw | `chore/normalize-hub` | #1 (normalisation + suivi gitignore) |
| contre-expertise | `chore/normalize-hub` | #1 |
| pair-with-me | `chore/normalize-hub` | #1 (+ suivi install.sh) |
| rhetorical-analysis-skill | `chore/normalize-hub` | #1 (+ suivi auto-portance) |
| skills (hub) | `feat/hub-socle` | #1 (registry + méta-marketplace + `shared/`) |

meeting-screenshot : poussé directement sur `main` (repo neuf, pas de PR).

## 7. Ordre d'exécution recommandé

1. Trancher les 2 décisions (rhetorical, meeting-screenshot orphelin).
2. Nettoyer les orphelins racine.
3. Aligner les 3 skills non conformes (bfw description, contre-expertise + pair-with-me manifests).
4. Extraire `shared/`.
5. Écrire `registry.json`.
6. Générer méta-marketplace + page vitrine depuis le registre.
