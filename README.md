# skills — Bastien Gallay's skills monorepo

Every Claude skill and style I maintain, in one repository. Each one keeps its
own directory, version, changelog and release tags; the marketplace at the root
serves all the Class-A skills.

Add every Class-A skill in one command:

```sh
/plugin marketplace add bastien-gallay/skills
```

Then `/plugin install <name>@skills` for any skill below.

## Layout

| Path | Holds |
| --- | --- |
| `plugins/<plugin>/` | One Class-A skill: `.claude-plugin/plugin.json`, `skills/<name>/SKILL.md`, its README, CHANGELOG and tooling |
| `styles/<style>/` | One Class-B style: canonical `prompt.md`, `build.sh`, `install.sh` |
| `.claude-plugin/marketplace.json` | The marketplace; each plugin is sourced by relative path |
| `.github/workflows/<plugin>*.yml` | Per-plugin CI and release, filtered on that plugin's path |
| `registry.json` | The machine-readable index (see below) |
| `shared/` | The mutualized socle: lint config, release template, skill skeleton |

Release tags carry the plugin prefix: `truepath/v0.3.3`, `bfw/v0.2.0`. Each
skill's history up to the migration comes from its former repository, whose
`main` was imported with its history.

## Two classes

| Class | What it is | Distribution |
| --- | --- | --- |
| **A — Skills** | Plugin-distributable Claude Code skills (`skills/<name>/SKILL.md` + manifests) | This marketplace |
| **B — Styles** | Behavior toggles, dual-target (Claude Code + claude.ai) built from a canonical `prompt.md` | Each style's `build.sh` / `install.sh` — not the marketplace |

## Skills (Class A)

| Skill | Path | Domain | What it does |
| --- | --- | --- | --- |
| brainstorm | [plugins/bfw](plugins/bfw) | facilitation | Facilitated brainstorming with adaptive technique sequencing |
| contre-expertise | [plugins/contre-expertise](plugins/contre-expertise) | method-audit | Critical, sourced counter-assessment of a working method |
| feature-torture | [plugins/feature-torture](plugins/feature-torture) | product | Pressure-test one roadmap feature → a decision report |
| market-strategist | [plugins/market-strategist](plugins/market-strategist) | strategy | Market analysis, positioning, traction, pitch — it fills the framework, you react |
| pair-with-me | [plugins/pair-with-me](plugins/pair-with-me) | engineering | Work an issue as an adversarial pair, not a delegation |
| redaction | [plugins/redaction](plugins/redaction) | writing | Boucle d'édition critique pour écrits longs |
| rhetorical-analysis | [plugins/rhetorical-analysis](plugins/rhetorical-analysis) | critical-thinking | Analyse rhétorique et épistémologique d'un texte |
| meeting-screenshot-extractor | [plugins/meeting-screenshot-extractor](plugins/meeting-screenshot-extractor) | tooling | Build a CLI to extract relevant screenshots from a meeting video |
| show-me | [plugins/show-me](plugins/show-me) | documentation | Pick the visual the content calls for, and how it renders on each target |
| truepath | [plugins/truepath](plugins/truepath) | documentation | Simulate a process or a bug path in one HTML page, checked against the code |
| shape | [plugins/shape](plugins/shape) | documentation | Improve a document for its reader's task, and prove nothing was lost |
| wrap | [plugins/wrap](plugins/wrap) | engineering | Close out a milestone with a 5S pass and leave an entry point for the next reader |

## Styles (Class B)

| Style | Path | What it does |
| --- | --- | --- |
| flair | [styles/flair](styles/flair) | End answers with a short learning-flavored anecdote stack |
| glance | [styles/glance](styles/glance) | Optimize answers for at-a-glance readability |
| transpeak | [styles/transpeak](styles/transpeak) | Answer in code rather than prose where the content has a shape |

Install a style from its directory (e.g. `styles/flair/install.sh` for the
`/flair` slash command, or paste its `claude-ai/` build into a claude.ai custom
style).

## Source of truth

[`registry.json`](registry.json) is the machine-readable index that feeds both
this marketplace and any presentation surface. `name` is the skill name, which
may differ from the directory name (`brainstorm` ← `bfw`); `repo` keeps the
name of the former standalone repository (`rhetorical-analysis-skill`).

## Conventions & shared socle

- [`NORMALIZATION.md`](NORMALIZATION.md) — the canonical Class-A convention and the audit that produced this hub.
- [`shared/`](shared/) — the mutualized socle: a `docs/RELEASING` template, a `skill-template/` skeleton for new Class-A skills, and [`SCRIPTS.md`](shared/SCRIPTS.md), the CUPID rules for scripts shipped inside a skill.
