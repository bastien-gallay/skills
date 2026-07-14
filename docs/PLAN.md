# Vitrine — plan de design

Page de présentation du hub `bastien-gallay/skills`. Vit **dans le repo**
(`docs/`), servie par GitHub Pages, **pilotée par `registry.json`** (source de
vérité unique — la page ne redéfinit jamais les données skill à la main).

## Sujet, audience, job

- **Sujet** : une *centrale* de skills Claude — un méta-marketplace + registre.
  Le mot « centrale » porte le concept : tableau de commande / standard
  d'échange, pas une simple grille de cartes.
- **Audience** : dev qui utilisent Claude Code et parcourent des skills à
  installer. Ils vivent dans un terminal, lisent des `plugin.json`, tapent
  `/plugin install`.
- **Job unique** : rendre les 9 modules découvrables et installables en un coup
  d'œil — nom, classe, statut, domaine, et la **commande d'install copiable**.

## Direction : le pupitre (control panel)

Pas de grille de cartes générique. Métaphore du **pupitre / standard** : chaque
skill est un *module* sur un tableau, avec sa **LED de statut** (stable/beta) et
son connecteur d'install. On assume le vocabulaire de l'instrument : voyants,
étiquettes gravées, rangées de modules, monospace pour tout ce qui est « signal »
(commandes, noms de plugin).

Risque esthétique assumé : traiter la commande d'install comme un **patch
lumineux** — au survol/copie, le connecteur « s'allume » (voyant ambre), comme
brancher un jack sur un standard. Un seul moment orchestré, pas d'animation
dispersée.

## Tokens

### Couleur

Neutres **encrés, pas gris purs** (biais chaud très léger côté ambre) :

- `--ink` `#17150F` — encre profonde (fond sombre), pas noir pur.
- `--paper` `#F5F1E8` — papier technique chaud (fond clair).
- `--graphite` `#3A362C` — texte/surfaces intermédiaires.
- `--signal` `#E8A317` — **ambre voyant** : l'accent unique (LED, patch actif).
  Un standard s'éclaire en ambre, pas en néon vert/vermillon.
- `--live` `#4FA88A` — vert-de-gris sourd : sémantique `class=skill` vs
  `class=style`, **pas** un second accent décoratif.
- `--dim` `#8B8474` — étiquettes gravées, méta, letter-spacing.

Statuts (sémantiques, distincts de l'accent) : `stable` = voyant `--live` plein ;
`beta` = voyant ambre clignotant discret (ou anneau creux).

Les deux thèmes sont dérivés au niveau des tokens (`:root`, `@media
prefers-color-scheme`, puis override `:root[data-theme=…]` dans les deux sens).
Le clair est le papier chaud, le sombre est l'encre — l'ambre marche sur les deux
grounds (baisser légèrement la luminance en clair).

### Type

Le sujet est un monde CLI → le **mono porte la personnalité**, pas un vernis.
On assume des **stacks système soignés** plutôt qu'un webfont data-URI de
150 Ko+ (choix délibéré : le dev lit son propre mono système ; honnête et sans
fallback silencieux) :

- **Display / signal** : `ui-monospace, "SF Mono", "JetBrains Mono", monospace`,
  poids fort, en capitales gravées avec letter-spacing pour les étiquettes.
- **Corps** : `system-ui, -apple-system, "Segoe UI", sans-serif`, humaniste,
  pour les descriptions.
- **Data / commandes** : le même mono, en bloc « connecteur » copiable.

Échelle typographique arrêtée (ex. 0.75 / 0.875 / 1 / 1.25 / 1.75 / 2.5 rem),
`text-wrap: balance` sur les titres, corps ~65 caractères, `tabular-nums` partout
où des chiffres/versions s'alignent.

> Si tu veux la vraie personnalité d'un mono display embarqué (ex. Departure
> Mono / Berkeley Mono-like), on l'inline en `@font-face` data-URI — à décider :
> +100-200 Ko sur la page. Défaut du plan : stack système.

### Layout

- **En-tête = plaque de la centrale** : nom du hub, la baseline, et LA commande
  maîtresse `/plugin marketplace add bastien-gallay/skills` en connecteur géant
  copiable. Pas de hero gigantesque décoratif — la plaque *est* le hero.
- **Sélecteur de classe** : bascule Skills / Styles (les deux classes A/B), qui
  filtre les modules. Encode une vérité du registre, pas une déco.
- **Tableau de modules** : grille responsive de modules-skill. Chaque module :
  LED de statut · nom (mono) · tag domaine gravé · description (corps) ·
  connecteur d'install copiable. `class=style` a un liseré `--live`.
- **Pied** : `registry.json` comme source de vérité (lien), lien vers
  `NORMALIZATION.md`, mention socle `shared/`.

## Technique

- **Un seul fichier** `docs/index.html` (CSS + JS inline), zéro dépendance
  externe (compatible Pages *et* une éventuelle prévisualisation Artifact).
- **Données** : `fetch('../registry.json')` en same-origin sur Pages → **single
  source réelle**, la page ne duplique jamais les entrées. (Fallback : petit
  script de build qui inline le registre si on veut aussi un Artifact autonome.)
- **A11y** : focus visible sur les connecteurs, bouton « copier » avec état,
  `prefers-reduced-motion` respecté (le patch s'allume sans transition).
- Rendu des modules par `class` et tri par `status` (stable avant beta).

## Ce qui n'est PAS templaté (revue anti-défaut)

- Pas de crème `#F4F1EA` + serif + terracotta : ici papier ambré + **mono** +
  voyant ambre, univers instrument.
- Pas de gradient violet-bleu, pas d'Inter/Space Grotesk, pas d'emoji-marqueurs.
- Les numéros/marqueurs ne sont utilisés que si l'ordre porte du sens
  (statut = tri réel) — sinon on s'abstient.
- Boldness dépensée à un seul endroit (le patch d'install qui s'allume) ; tout
  le reste reste calme.

## Séquence de travail

1. **Ce plan** (ici) — revu avant tout code.
2. **Build** `docs/index.html` piloté par `registry.json`.
3. **Passe copie** sur la prose *originale* de la page (plaque, baselines, pied)
   et sur ce plan — c'est là que `/impeccable` a sa place : polir les mots, pas
   échafauder le HTML. Les descriptions viennent du registre (non éditées ici).
