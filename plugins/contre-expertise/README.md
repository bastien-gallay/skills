# contre-expertise

Skill Claude Code : contre-expertise critique et sourcée d'une méthode de
travail personnelle. Extraction du modèle en propositions falsifiables,
interview de l'auteur, deep research multi-agents, vérification adversariale
à deux étages (claims des fiches **et** conclusions du rapport), méthode
rivale (challenger), verdicts datés et périssables, plan d'action plafonné au
format expérimental, routable vers daily-ops.

## Installation

```sh
ln -s "$(pwd)/skills/contre-expertise" ~/.claude/skills/contre-expertise
```

## Usage

```text
/contre-expertise corpus:content/ecrits/mon-article/index.md calibre:standard
/contre-expertise slug:ma-methode --overwrite   # écrase (archive) la sortie en cours
/contre-expertise slug:ma-methode --reflect     # relance J+30 (diff des verdicts)
```

Le mode incrémental est le défaut : le skill reprend à la première phase dont
l'artefact manque sur disque (voir `SKILL.md` §2).

## Origine

Première exécution de référence : livre blanc « Coder plus lentement,
vraiment ? » (2026-06-11), analyse critique de la méthode décrite dans la
série d'articles *Coder avec l'IA*. Le skill encode les leçons de cette
exécution — y compris ses propres manques (contre-vérification du rapport,
plafond du plan d'action, économie de la méthode).

Les intégrations daily-ops futures sont suivies dans
[bastien-gallay/daily-ops#31 à #37](https://github.com/bastien-gallay/daily-ops/issues).
