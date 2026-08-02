# skills — Bastien Gallay's skills hub

A **meta-marketplace** and registry for the Claude skills I maintain. Each skill
lives in its **own repository** — versioned, released and distributed
independently. This hub aggregates them; it never vendors them.

Add every Class-A skill in one command:

```sh
/plugin marketplace add bastien-gallay/skills
```

Then `/plugin install <name>@skills` for any skill below.

## Two classes

| Class | What it is | Distribution |
| --- | --- | --- |
| **A — Skills** | Plugin-distributable Claude Code skills (`skills/<name>/SKILL.md` + manifests) | This meta-marketplace, or each repo's own single-plugin marketplace |
| **B — Styles** | Behavior toggles, dual-target (Claude Code + claude.ai) built from a canonical `prompt.md` | Each repo's `build.sh` / `install.sh` — not the marketplace |

## Skills (Class A)

| Skill | Repo | Domain | What it does |
| --- | --- | --- | --- |
| brainstorm | [bfw](https://github.com/bastien-gallay/bfw) | facilitation | Facilitated brainstorming with adaptive technique sequencing |
| contre-expertise | [contre-expertise](https://github.com/bastien-gallay/contre-expertise) | method-audit | Critical, sourced counter-assessment of a working method |
| feature-torture | [feature-torture](https://github.com/bastien-gallay/feature-torture) | product | Pressure-test one roadmap feature → a decision report |
| market-strategist | [market-strategist](https://github.com/bastien-gallay/market-strategist) | strategy | Market analysis, positioning, traction, pitch — it fills the framework, you react |
| pair-with-me | [pair-with-me](https://github.com/bastien-gallay/pair-with-me) | engineering | Work an issue as an adversarial pair, not a delegation |
| redaction | [redaction](https://github.com/bastien-gallay/redaction) | writing | Boucle d'édition critique pour écrits longs |
| rhetorical-analysis | [rhetorical-analysis-skill](https://github.com/bastien-gallay/rhetorical-analysis-skill) | critical-thinking | Analyse rhétorique et épistémologique d'un texte |
| meeting-screenshot-extractor | [meeting-screenshot-extractor](https://github.com/bastien-gallay/meeting-screenshot-extractor) | tooling | Build a CLI to extract relevant screenshots from a meeting video |

## Styles (Class B)

| Style | Repo | What it does |
| --- | --- | --- |
| flair | [flair](https://github.com/bastien-gallay/flair) | End answers with a short learning-flavored anecdote stack |
| glance | [glance](https://github.com/bastien-gallay/glance) | Optimize answers for at-a-glance readability |

Install a style from its own repo (e.g. `./install.sh` for the `/flair`
slash command, or paste its `claude-ai/` build into a claude.ai custom style).

## Source of truth

[`registry.json`](registry.json) is the machine-readable index that feeds both
this meta-marketplace and any presentation surface. `name` is the skill name,
which may differ from the repo name (`brainstorm` ← `bfw`,
`rhetorical-analysis` ← `rhetorical-analysis-skill`).

## Conventions & shared socle

- [`NORMALIZATION.md`](NORMALIZATION.md) — the canonical Class-A convention and the audit that produced this hub.
- [`shared/`](shared/) — the mutualized socle: canonical `.markdownlint.json`, a `docs/RELEASING` template, and a `skill-template/` skeleton for new Class-A skills.
