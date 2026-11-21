# Roadmap — évolutions du skill `/redaction`

Notes mainteneur listant les chantiers d'évolution post-v0.1.0. Pas
linké depuis le README public — interne (même convention que
`docs/RELEASING.md`).

## État livré (v0.1.0 — 2026-05-22)

- **P1 — fichier de suivi systématique.** Scaffold automatique de
  `.personal/ecriture/SUIVI-<basename>.md` chez le consommateur à la
  première invocation, lecture intégrale à la reprise, mise à jour
  tabulaire à chaque tour de boucle. Template dans
  `skills/redaction/suivi-template.md`.
- **P6 — cross-référencement Axx/Bxx.** Chaque piège du catalogue
  porte son code de référence vers `style-bastien.md` §0 du repo
  consommateur. Colonne `Code` ajoutée au format de retour. Les pièges
  propres au skill (Thèse molle, Re-cloisonnement, Énumération qui
  esquive, Croissance quantitative) sont marqués `(candidat §0)` —
  destinés à être promus via le futur mode rétrospectif (P3).

Voir `CHANGELOG.md` pour le détail.

## Contexte

Chantiers issus de l'analyse rétrospective du 2026-05-22 sur le corpus
de rédaction du repo consommateur `bastiengallay.com` — SUIVI des
articles `2026-05-15-amorce.md` (médité, ~900 mots, prose figée) et
`2026-05-21-avec-l-ia-je-code-plus-lentement.md` (pulsé, ~2100 mots,
section centrale à reprendre). L'analyse a aussi inspecté le profil
stylistique reverse-engineered (`.personal/style-bastien.md`, §0
checklist Axx/Bxx + §11 distinction médité/pulsé) et l'anti-corpus
(`.personal/style-corrections.md`).

---

## P2 — Linters externes en passe 1, LLM en passe 2

**Objectif** : déplacer la détection des coquilles, accords et fautes
mécaniques du LLM vers des outils déterministes. Le LLM se concentre
sur sa zone de valeur (voix, registre, rythme, drift Axx/Bxx).

**Justification** : la passe finale du SUIVI 05-21 a relevé 11 typos
manuellement (`audatieux`, `fournaux`, `assitants`, `me manque` en
sujet pluriel, etc.). Ces erreurs sont des règles mécaniques —
`hunspell` les attrape gratuitement, sans tokens.

**Pipeline cible** :

| Passe | Outil | Couvre |
| --- | --- | --- |
| 1a | `markdownlint` (déjà global) | structure markdown, lignes longues, codeticks |
| 1b | `aspell -l fr` ou `hunspell -d fr_FR` | typos pures |
| 1c | `vale` + style-pack FR (à constituer) | accords, ponctuation, faux-amis, registres |
| 2 | LLM | voix, registre, rythme, drift `Axx`/`Bxx` |

**Choix de stack à arbitrer** :

- LanguageTool full = très bonne couverture FR mais JVM ~500 MB +
  serveur local.
- `vale` (Go, ~10 MB) + style-pack FR custom = léger, programmable,
  mais demande un investissement initial pour porter les règles `Axx`
  facilement détectables (A1 « plongeons dans », A2 « en résumé »,
  A6 « tirer parti de », A7 « à l'ère de l'IA », A14 « la clé du
  succès »).
- Hybride : `hunspell` pour typos + `vale` pour registre.

**Effets sur le skill** :

- Section « Auto-corrections vs reformulations » devient triviale :
  les linters ne reformulent jamais.
- Le SUIVI section `Coquilles et typos` se vide automatiquement (les
  linters ont passé en CI).
- Sous-commande `/redaction --lint <fichier>` pour lancer les passes
  1a/1b/1c isolément.

**Effort estimé** : 1 session pour `markdownlint` + `hunspell`,
2-3 sessions pour `vale` + style-pack FR initial.

---

## P3 — Mode rétrospectif `/redaction --retro [scope]`

**Objectif** : calquer le mode rétrospectif de `/brainstorm`
(`~/.agents/skills/brainstorm/SKILL.md` §397-436) pour faire émerger
des patterns sur le corpus d'écrits longs.

**Sources** :

1. **Tier session-doc** : scan de `.personal/ecriture/SUIVI-*.md` chez
   le consommateur.
2. **Tier chat-level** : scan des sessions JSONL
   `~/.claude/projects/<repo>/` filtrées sur les fichiers
   `content/ecrits/*` (ou équivalent côté consommateur).
3. **Tier none** : si rien n'est lisible → refus en une phrase, pas de
   synthèse.

**Synthèse attendue** :

- Patterns de pièges récurrents (codes `Axx`/`Bxx` les plus fréquents).
- Distribution des verdicts (`✅` / `🔧` / `✂️`) par paragraphe-type.
- Durée moyenne par paragraphe (V0 → V+n).
- Ratio AI-écrit / Bastien-écrit (passages co-rédigés vs ré-écrits).
- Frictions de cadrage récurrentes (combien de re-cadrages par
  article).

**Sorties proposées** (jamais auto-appliquées — diff à valider) :

- Enrichissement de `style-bastien.md` §0 (promotion d'un pattern
  observé ≥3× en règle `Axx` ou `Bxx`) côté consommateur.
- Enrichissement de `style-corrections.md` (entrées qui auraient dû
  être capturées et ne l'ont pas été) côté consommateur.
- Ajustement de `skills/redaction/SKILL.md` (nouveaux pièges, seuils,
  formulations) côté repo skill.
- Rapport `.personal/ecriture/RETRO-YYYY-MM-DD.md` posé chez le
  consommateur pour archive.

**Première sortie probable** sur l'état actuel du corpus : les 3
candidats §0 actuellement dans SKILL.md (Re-cloisonnement, Énumération
qui esquive, Croissance quantitative) — vérifier leur fréquence sur le
corpus et promouvoir si applicable.

**Effort estimé** : 2-3 sessions (tier detection + synthèse + format
de diff). Premier scope : un seul article.

---

## P4 — Collecte automatique du style (greffon de P3)

**Objectif** : §11 de `style-bastien.md` (médité / pulsé) a été
produit à la main sur 2 articles. Automatiser cette analyse à mesure
que le corpus grandit.

**Heuristiques** :

- **Bijoux conservés ≥3 itérations** dans les SUIVI → candidats
  « tics signature » de §11.
- **Tournures auto-corrigées par l'auteur** dans les diffs git de
  `content/ecrits/*` → candidats `Axx` (si l'auteur réécrit, il y a eu
  drift AI).
- **Divergence registre** : un article tagué `médité` qui contient
  `du coup` / `en fait` → soit le tag est faux, soit la règle
  médité/pulsé doit s'assouplir.
- **Phrase-couperet en clôture** : signature claire de l'écrit médité
  (§11.2). Mesurable par longueur moyenne de la dernière phrase de
  paragraphe.

**Garde-fou** : promotion en règle = nécessairement validée par
l'auteur via diff, jamais écriture silencieuse. Le pattern « promotion
à ~10 entrées » de `style-corrections.md` est la cadence cible.

**Dépendance** : P3 doit être en place (le retro est le mécanisme de
collecte).

**Effort estimé** : 1-2 sessions par-dessus P3.

---

## P5 — Bibliothèque de styles `.personal/styles/`

**Objectif** : §11.5 de `style-bastien.md` distingue déjà médité vs
pulsé, mais le skill n'a pas de notion de registre. Permettre au
facilitateur d'adapter sa critique au registre cible.

**Convention côté consommateur** :

```text
.personal/styles/
  bastien.md         # invariant voix (= style-bastien.md déplacé/lien)
  medite.md          # registre essai long, scène d'ouverture, parataxe
  pulse.md           # premier jet, tolérance hedge, énumérations numérotées
  technique.md       # docs CLAUDE.md, README — un autre registre encore
  linkedin.md        # ~250 mots, accroche, redirection
```

**Contenu de chaque style** :

- Longueur de phrase visée (médiane, max).
- Tolérance hedge (interdit / fonctionnel uniquement / libre).
- Ponctuation et marqueurs oraux (interdits / autorisés / signatures).
- Repoussoirs aggravés ou levés par rapport à `bastien.md`.
- Exemples positifs et négatifs courts.

**Intégration au skill** :

- Argument `--style medite` (explicite).
- Auto-détection (frontmatter `kind:`, longueur cible, dossier
  d'accueil `content/ecrits/` vs `content/linkedin/`).
- Diagnostic combiné : voix d'auteur (`bastien`) ∩ registre cible
  (`medite`). Exemple : `🚨 B11 — du coup dans un médité ; OK en pulsé`.

**Dépendance** : pas de dépendance forte ; débloque P4 pour calibrer
les heuristiques par style.

**Effort estimé** : 1 session pour le scaffold de `medite.md` et
`pulse.md` (matière déjà dans §11), 0.5 session pour l'intégration au
skill.

---

## P7 — Capture incrémentale automatique de l'anti-corpus

**Objectif** : la règle « 1 paragraphe AI rejeté → 1 paire capturée
dans `style-corrections.md` » est manuelle et donc oubliée (0 entrée
à ce jour, alors que les sessions de rédaction en ont généré des
dizaines).

**Hook proposé** : quand le skill détecte que l'auteur réécrit > 70 %
d'un paragraphe AI ou rejette explicitement, **proposer** une entrée
formatée selon le template déjà défini dans `style-corrections.md`
(date, source, signal détecté avec code `Axx`/`Bxx`, paire verbatim).
Validation en un mot oui/non, pas en composition.

**Format de la proposition** :

```markdown
### YYYY-MM-DD — [titre court]

**Source :** [fichier ou conversation]
**Signal(s) détecté(s) :** A1, B2

**❌ Proposé par l'IA :**

> [bloc verbatim AI]

**✅ Réécrit par l'auteur :**

> [bloc verbatim post-réécriture]

**Note :** [optionnel — ce qui clivait, en une phrase]
```

**Dépendance** : P6 (codes Axx/Bxx déjà taggés dans la critique) —
livré en v0.1.0. P7 peut être livré dès que P3 ou P4 est lancé (le
mécanisme de capture devient utile à mesure que le retro le consomme).

**Effort estimé** : 0.5 session (le template existe côté consommateur,
le mécanisme est juste un déclencheur post-tour).

---

## Ordre d'attaque suggéré

| Ordre | Chantier | Pourquoi |
| --- | --- | --- |
| 1 | **P2 (linters)** | ROI immédiat, déterministe, indépendant. Soulage la passe finale (11 typos manuelles sur l'article IA). |
| 2 | **P5 (bibliothèque styles)** | Débloque P4 et précise tout le reste. Matière déjà dans §11. |
| 3 | **P3 + P4 (rétro + style auto)** | Le plus structurant ; nécessite P5 en amont pour calibrer les heuristiques par style. |
| 4 | **P7 (capture incrémentale auto)** | Petit add-on qui tombe quasi-gratuitement une fois P3/P6 en place. |
