---
name: contre-expertise
description: >
  Contre-expertise critique et sourcée d'une méthode de travail décrite par
  l'utilisateur (articles, notes, README de pratique) : extraction du modèle en
  propositions falsifiables, interview de l'auteur, deep research multi-agents
  (méthodes comparables, pratiques, sources), vérification adversariale à deux
  étages, méthode rivale (challenger), rapport à verdicts datés et plan d'action
  plafonné au format expérimental. Avance de façon incrémentale par défaut
  (reprise sur artefacts). Trigger : l'utilisateur tape /contre-expertise,
  demande de « passer ma méthode au crible », « analyse critique de ma façon de
  travailler », « contre-expertise de mes articles/pratiques », ou veut
  confronter sa pratique à l'état de l'art sans complaisance.
---

# Contre-expertise — v1

> **Ce que c'est.** Un audit à charge ET à décharge d'une méthode de travail
> personnelle, mené comme une instruction : grille falsifiable, recherche
> multi-agents, réfutation systématique, verdicts datés, plan d'action borné.
> Le facilitateur ne conforte pas — il instruit. Première exécution de
> référence : livre blanc du 2026-06-11 (`.personal/research/2026-06-11-livre-blanc-methode/`).
>
> **Sortie.** Un dossier `.personal/research/<date>-contre-expertise-<slug>/`
> contenant les fiches de recherche, les vérifications, un rapport (markdown ou
> Typst selon calibre) et un `plan-action.md` routable vers daily-ops.

## 0. Règles transversales (s'appliquent à toutes les phases)

1. **Non-complaisance.** Chaque agent et chaque synthèse reçoit la consigne
   « cherche à réfuter, pas à confirmer ». Le positif n'est gardé que s'il sert
   la calibration.
2. **`.personal/` s'écrit sur main.** Toujours en chemin absolu vers la copie
   principale, jamais dans le `.personal/` local d'un worktree.
3. **Aucune référence de mémoire.** Toute URL ou citation du rapport provient
   d'une fiche où elle a été obtenue par recherche/fetch vérifié. Une source
   attendue mais introuvable est déclarée introuvable, jamais inventée.
4. **Traçabilité mécanique.** Les propositions du modèle portent des IDs
   `P-xx` ; les claims des fiches portent des IDs `C-<unité>-<n>`
   (ex. `C-a1-2`) ; chaque verdict et chaque item du plan d'action référence
   ses IDs. Avant clôture, vérifier par grep que chaque C-id « nuancé » ou
   « fragilisé » est bien référencé ou amendé dans le rapport.
5. **Verdicts datés et périssables.** Chaque verdict porte sa date et une date
   de péremption (défaut : +6 mois ; +3 mois pour les sujets à benchmarks
   mouvants). Le mode `--reflect` ne ré-instruit que ce qui est périmé ou
   contesté.
6. **Un constat, un domicile.** Chaque constat du rapport a UN chapitre
   propriétaire ; les autres chapitres y renvoient au lieu de le répéter.
7. **Coût annoncé avant dépense.** Avant tout lancement de Workflow, annoncer
   le nombre d'agents et l'ordre de grandeur de tokens du calibre choisi, et
   obtenir confirmation (sauf si le calibre a été passé explicitement en
   argument).

## 1. Entrées et cadrage (phase 0)

Arguments acceptés (tous optionnels, demander ce qui manque) :

- `corpus:` chemins des textes décrivant la méthode (articles, notes, README).
- `slug:` nom court du dossier (sinon le dériver du sujet).
- `calibre:` `leger` | `standard` | `complet` (voir §3).
- `--overwrite` : désactive le mode incrémental (voir §2).
- `--reflect` : mode relance/diff (voir §8).

Cadrage : lire le corpus, reformuler en une phrase ce qui est audité et pour
quelle décision (publier ? améliorer ? trancher un débat ?). Si le calibre
manque, le demander via AskUserQuestion avec les coûts en face de chaque
option. Créer le dossier et initialiser `etat.md` depuis
`templates/etat.md` : décisions de cadrage, calibre, liste d'unités prévue,
horodatage.

## 2. Mode incrémental (défaut) et `--overwrite`

**Le skill reprend là où il s'est arrêté.** La vérité d'avancement est sur le
disque, pas en mémoire de session :

| Phase | Artefact de complétion |
| --- | --- |
| 1 Extraction | `notes/00-modele.md` |
| 2 Interview | `notes/01-interview.md` |
| 3 Recherche | toutes les fiches listées dans `etat.md` § unités |
| 4 Vérification | `notes/90-verifications.md` |
| 5 Challenger | `notes/95-challenger.md` |
| 6 Rapport | `rapport.md` ou `rapport.pdf` compilé |
| 7 Contre-vérification | `notes/98-contre-verification.md` + marqueur « corrections intégrées » dans `etat.md` |
| 8 Plan d'action | `plan-action.md` |
| 9 Clôture | marqueur « clos » + hash de commit dans `etat.md` |

À l'invocation : si le dossier du slug existe, lister les artefacts présents,
annoncer le point de reprise (« phases 1-3 faites, je reprends en phase 4 »)
et continuer. Une phase amont modifiée à la main invalide l'aval : le signaler
et proposer de re-dérouler. Cas particulier de la phase 3 : si un `runId` de
Workflow figure dans `etat.md` et que des fiches manquent, relancer avec
`resumeFromRunId` — les unités terminées reviennent du cache.

**`--overwrite`** : ne JAMAIS supprimer — renommer le dossier existant en
`<dossier>.bak-<date>` puis repartir de zéro. Mentionner le renommage à
l'utilisateur.

## 3. Calibres

| Calibre | Unités de recherche | Vérification | Livrable | Ordre de grandeur |
| --- | --- | --- | --- | --- |
| `leger` | ~5 (1-2 par axe) | 1 claim/fiche, 1 vote | note markdown 3-5 pages + plan | ~15 agents |
| `standard` | ~10 | 2 claims/fiche, 1 vote | rapport Typst ~15 pages + plan | ~30 agents |
| `complet` | ~17 | 2 claims/fiche + contre-vérif élargie | livre blanc Typst 30+ pages + plan | ~50 agents, >2,5 M tokens de sous-agents |

En `leger` et `standard` : tableaux de divergence plutôt que prose d'état de
l'art, annexes par référence aux fiches (pas de duplication), bibliographie
générée. Le mode `complet` reste réservé aux audits fondateurs.

## 4. Les phases

### Phase 1 — Extraction du modèle

Reconstituer la méthode en **propositions falsifiables numérotées** `P-xx`
(15-30 items : pratiques, croyances, choix de mesure), suivies d'une section
« points d'auto-incohérence à instruire » (les endroits où le corpus se
contredit ou s'exempte de ses propres règles). Gabarit :
`templates/grille-modele.md`. C'est la colonne vertébrale de tout le reste —
soigner la granularité : une proposition = une chose réfutable.

### Phase 2 — Interview (théorie professée vs théorie en usage)

Le corpus décrit ce que l'auteur *dit* faire. Avant de juger, poser 5-10
questions ciblées (AskUserQuestion, par lots de 4 max) du type : « la dernière
fois que tu as sauté P-08, c'était quoi le contexte ? », « P-14 : à quelle
fréquence réellement ? ». Marquer ensuite chaque P-xx :
`professée` / `confirmée en usage` / `contredite en usage` — et noter les
exemples concrets donnés. Les P-xx « contredites en usage » deviennent des
angles prioritaires d'instruction. Sortie : `notes/01-interview.md`.

### Phase 3 — Deep research multi-agents

Lancer un Workflow (l'invocation de ce skill vaut opt-in explicite) construit
depuis `templates/workflow-recherche.js`. Trois axes d'unités, à dimensionner
selon le calibre :

- **Axe A — méthodes comparables** : praticiens et institutions ayant publié
  un flux de travail sur le même sujet.
- **Axe B — pratiques en détail** : chaque pratique différenciante du modèle,
  instruite contre la littérature (mécanisme démontré / plausible / contredit).
- **Axe C — sources du corpus** : chaque source citée par l'auteur,
  contre-vérifiée (que dit-elle exactement, qui la conteste, l'usage est-il
  fidèle).

Consignes communes obligatoires dans chaque prompt d'unité :

1. À charge ET à décharge — ne pas conforter.
2. **Chercher activement les cas d'échec** de chaque méthode/pratique, pas
   seulement ses promoteurs (le biais de visibilité des praticiens célèbres
   est documenté — première exécution, fiche a3).
3. **Au moins une recherche en français** (ou autre langue pertinente) par
   unité quand le sujet s'y prête.
4. Fiche écrite sur disque (`notes/<unité>.md`, gabarit
   `templates/fiche-recherche.md`), retour structuré compact (résumé +
   claims).
5. Claims terminales avec IDs `C-<unité>-<n>` et URL source.

Consigner le `runId` dans `etat.md` dès le lancement (reprise).

### Phase 4 — Vérification adversariale des claims

Pour chaque claim : un agent chargé de la **réfuter** (source primaire
exigée). Verdicts : `corroborée` / `nuancée` / `fragilisée` / `réfutée` /
`introuvable`, chacun avec date de péremption. Sortie :
`notes/90-verifications.md` (généré proprement : titres sans ponctuation
finale, URLs entre `<>`). Puis **propager** : chaque nuance/correction est
reportée dans les fiches concernées ou notée comme correctif à appliquer en
phase 6 — la propagation se vérifie par les C-ids (règle 0.4).

### Phase 5 — Challenger

Construire le **steelman d'une méthode rivale** à partir des fiches : la
meilleure alternative cohérente (pas un épouvantail), avec ses choix opposés
aux P-xx les plus structurants. La comparer frontalement au modèle : sur quels
contextes le challenger gagne-t-il ? Qu'emprunterait-on ? Sortie :
`notes/95-challenger.md`. C'est l'antidote au confort de la comparaison à un
champ dispersé.

### Phase 6 — Rapport

Structure cible (à compresser selon calibre) : résumé exécutif · modèle
reconstruit · état de l'art (tableaux de divergence) · pratiques en détail ·
analyse d'écart (socle partagé / en plus / manquant / écart inversé) ·
critique des points de comparaison (n=1, biais de survie, comparants non
mesurés, asymétries de contexte) · sources : verdicts par statut ·
critique des fondamentaux (encadrés verdict : solide / fragile / critique) ·
**économie de la méthode** (tableau coût/bénéfice par pratique : temps,
tokens, ce que ça attrape — même grossier, jamais omis) · challenger ·
plan d'action (renvoi) · bibliographie.

Règles d'écriture : verdicts référencés par C-ids ; un constat = un domicile
(règle 0.6) ; la bibliographie est **générée depuis les fiches** (script ou
extraction), pas rédigée à la main ; en Typst, réutiliser le gabarit de mise
en page de la première exécution (`lib.typ` du livre blanc 2026-06-11).

### Phase 7 — Contre-vérification du rapport

L'étage que la première exécution avait manqué : les claims des fiches étaient
vérifiées, pas les conclusions du document. Lancer 3-6 agents (selon calibre)
chargés de **réfuter les verdicts et synthèses du rapport lui-même** (chaque
encadré verdict, le résumé exécutif, l'analyse d'écart), avec accès aux fiches.
Intégrer les corrections, les tracer dans `notes/98-contre-verification.md`,
poser le marqueur « corrections intégrées » dans `etat.md`. Un rapport qui
prêche la non-exemption doit se l'appliquer.

### Phase 8 — Plan d'action

Le livrable d'atterrissage — gabarit `templates/plan-action.md` :

1. **Scoring d'abord** : pour chaque action candidate, commencer par
   « recoupe quoi d'existant ? » (élimine les doublons avec ce que
   l'utilisateur fait déjà), puis Impact/Effort.
2. **Plafond strict** : 3 actions « maintenant » + 3 « ce mois » ; tout le
   reste en backlog daté. Un inventaire n'est pas un plan.
3. **Format expérimental obligatoire** pour toute action de type
   expérimentation : hypothèse · métrique · commande de baseline · durée ·
   date de revue. **Règle bloquante : pas d'expérimentation émise sans étape
   de baseline.**
4. **Routage daily-ops (état actuel de l'outil)** : produire en fin de fichier
   une section « à router » avec les items préformatés une ligne chacun,
   préfixés de leur trace `[src: <slug>/C-xx]`, que l'utilisateur route via
   `/do-add` (bloc du jour ou drop-in) ou colle dans `TODO.md`. Les dates de
   revue sont listées à part pour un éventuel `/schedule`.

<!--
AMÉLIORATIONS FUTURES — daily-ops (issues ouvertes le 2026-06-12) :
- #31 (échéancier --due) : router directement les items « ce mois » et les
  dates de revue avec leur échéance, au lieu de la liste à part.
- #32 (plan import + tags de provenance) : remplacer la section « à router »
  par `daily-ops plan import plan-action.md` — import en lot idempotent,
  le tag [src: …] devient natif et survit aux reports.
- #33 (report --json + compteur de reports) : le mode --reflect interroge
  daily-ops mécaniquement (« quelles actions taguées src:<slug> sont faites /
  zombies ? ») au lieu de demander à l'utilisateur.
- #34 (blocs expérimentation à cycle de vie) : émettre les expérimentations
  comme blocs `experiment` avec métadonnées portées par daily-ops.
- #35 (cadence par stream) : router les expérimentations vers un stream
  `experiments` surfacé aux dates de revue.
- #36 (IDs d'items persistants) : la traçabilité C-id → item survit aux
  reformulations.
- #37 (mode headless) : le routage ne dépend plus du /do-sod du jour.
-->

### Phase 9 — Clôture

1. `markdownlint` sur toutes les notes (config du site) ; compilation du
   rapport ; contrôle visuel de quelques pages si Typst.
2. Récap console en 3 blocs de bullets : *maintenant* / *ensuite* /
   *décisions ouvertes* — localisé, pas de prose.
3. Proposer le commit du dossier dans le repo privé `.personal` (demander
   avant tout commit hors sandbox, sauf autorisation de session).
4. Proposer un `/schedule` pour la revue J+30 en citant la date inscrite dans
   `plan-action.md`.

## 8. Mode `--reflect` (relance J+30)

Entrée : le dossier d'une contre-expertise close. Déroulé court, sans nouveau
fan-out complet :

1. Lire `etat.md`, `plan-action.md`, `notes/90-verifications.md`.
2. Demander à l'utilisateur le sort de chaque action « maintenant » / « ce
   mois » (faite / en cours / abandonnée / zombie) et les valeurs des
   métriques de baseline. <!-- futur : remplacé par daily-ops report #33 -->
3. Ré-instruire UNIQUEMENT : les verdicts périmés (date de péremption
   dépassée), les claims `fragilisées`, et les hypothèses d'expérimentations
   dont les mesures sont arrivées (1 agent par item, pas de fan-out complet).
4. Produire `reflect-<date>.md` : diff des verdicts (bougé / stable / périmé
   non re-vérifié), bilan des expérimentations, plan d'action re-priorisé
   (mêmes plafonds).

## 9. Pièges connus (hérités de la première exécution)

- Vérifier les claims des fiches ne vérifie PAS le rapport : ne jamais sauter
  la phase 7.
- Les chiffres « emblématiques » des fiches sont souvent des exemples
  motivants, pas des moyennes — reporter la portée exacte (cf. correctifs
  MUTGEN 100 %/4 %, Scott Logic 2 067 lignes).
- Les citations en chaîne cassent (cf. « 2,74× ») : toujours remonter à la
  source primaire avant de reprendre un chiffre.
- Générer `90-verifications.md` proprement dès le départ (lint) plutôt que de
  corriger après coup.
- Ne pas laisser les listes d'action gonfler : le plafond de la phase 8 est
  une règle, pas une suggestion.
