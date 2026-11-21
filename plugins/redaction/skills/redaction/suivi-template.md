<!-- markdownlint-disable MD013 MD025 MD033 MD038 MD040 MD060 MD004 -->

# Template — fichier de suivi (`SUIVI-<basename>.md`)

> Modèle à scaffolder dans `.personal/ecriture/SUIVI-<basename>.md` à la
> première invocation de `/redaction` sur un écrit long. Référencé depuis
> `~/.claude/skills/redaction/SKILL.md`.
>
> **Règle de remplissage** : ne pas instancier les sections optionnelles
> tant qu'elles sont vides. Les laisser en commentaire HTML dans le
> scaffold initial — le skill les active quand le matériau apparaît.

---

# Suivi de rédaction — `<chemin/vers/article.md>`

Document de pilotage de *[titre court / contexte]*. Actualisé à chaque
jalon. À reprendre via `/redaction <chemin/vers/article.md>`.

Documents liés :

- *[brainstorm / méthodo amont, si pertinent]*
- *[autres écrits liés — série, version courte LinkedIn, etc.]*

---

## Métadonnées

| Champ | Valeur |
| --- | --- |
| **Fichier** | `<chemin>` |
| **Date publication prévue** | YYYY-MM-DD |
| **Statut** | `draft = true` |
| **Cible de longueur** | ~XXX mots |
| **Longueur actuelle** | ~XXX mots |
| **Date dernière session** | YYYY-MM-DD |

## Thèse (verrouillée)

> *[formulation courte — 1 à 3 lignes — celle que l'auteur signe]*

Variante mémorable *(exergue / sous-titre / accroche, optionnel)* :

> *[optionnel]*

## Architecture actuelle

```text
P1   │ [rôle rhétorique]                          [type]   ~XXX mots
P2   │ [...]                                      [...]    ~XXX mots
...
─────│ ≈ XXX mots
```

## Bijoux à préserver à travers les itérations

| Localisation | Phrase | Raison |
| --- | --- | --- |
| Pn | « ... » | ... |

## Pièges traversés et résolus

| Dérive | Code | Itération | Résolution |
| --- | --- | --- | --- |
| ... | `A5` / `B2` / *(candidat §0)* | Pn Vk | ... |

<!--
Code = référence à `.personal/style-bastien.md` §0
(Axx = drift AI, Bxx = piège Bastien). Si la dérive n'a pas de code §0,
la noter `(candidat §0)` — à promouvoir via `/redaction --retro` quand
3+ occurrences sont observées.
-->

## Décisions actées (ne pas rouvrir)

- *[décisions structurelles, de ton, de cadrage qui ne se ré-ouvrent pas]*

## Plan restant — ordre de passe

Du plus bloquant au plus cosmétique :

1. ...
2. ...

## Hygiène avant publication (checklist)

- [ ] Passes finales sur frictions accumulées.
- [ ] Frontmatter `description` à jour.
- [ ] Lint markdown (`markdownlint`).
- [ ] Build local (`zola serve`).
- [ ] Relecture à voix haute.
- [ ] `draft = false`.

## Journal de session

### YYYY-MM-DD

- *[bullets — 3 à 5 lignes max — diff résumé + bijoux nouveaux + frictions levées]*

<!--
=== Sections optionnelles — activer selon le type d'écrit ===

## Devil's Advocate — tenue des arguments
(articles d'opinion sourcés)

| # | Argument | Tenue | Critique hostile résiduelle |
| --- | --- | --- | --- |
| 1 | ... | ✅ / ⚠️ / ❌ | ... |

## Audit des passages auteur
(articles co-rédigés AI/auteur — passages marqués AJOUT BASTIEN, NOTE BASTIEN, etc.)

| # | Passage | État | Action |
| --- | --- | --- | --- |
| 1 | ... | ✅ / ⚠️ / ❌ | ... |

## Scorecard pièges
(articles dont le brainstorm initial a listé des pièges littéraires à surveiller)

| # | Piège | Statut |
| --- | --- | --- |
| 1 | ... | ✅ / ⚠️ / ❌ |

## Sourcing — solidité par référence
(articles citant des sources externes)

| Réf | Source | Solidité | Action |
| --- | --- | --- | --- |
| [1] | ... | ✅ primaire / ⚠️ vendor / ❌ faible | ... |

## Coquilles et typos
(passe finale — capturer ce que les linters n'ont pas attrapé)

- « ... » → « ... »

=== fin sections optionnelles ===
-->
