# contre-expertise

A [Claude Code](https://claude.com/claude-code) skill that runs a critical,
sourced **counter-assessment of your own working method** — the way a
judicial investigation treats a testimony, not the way a coach treats a
client.

*Contre-expertise* is French for "counter-assessment" / "second expert
opinion". The skill was born auditing its author's own AI-assisted
development method, and it keeps the French name.

## What it does

Given a corpus that describes how you work (articles, notes, a practice
README), the skill:

1. **Extracts the model** into numbered falsifiable propositions (`P-xx`),
   including the corpus's self-inconsistencies.
2. **Interviews you** — espoused theory vs theory-in-use: what you *say*
   you do vs what you actually do. Contradicted propositions become
   priority investigation angles.
3. **Runs multi-agent deep research** across three axes: comparable
   methods, each differentiating practice against the literature, and every
   source you cite (counter-checked).
4. **Adversarially verifies** every carrying claim — agents are prompted to
   *refute*, primary sources required, verdicts dated and perishable.
5. **Builds a challenger** — the steelman of a rival method, aimed at your
   weakest confirmed spot.
6. **Writes a report** (markdown or Typst by caliber) with verdict boxes
   and a mandatory "economics of the method" section.
7. **Counter-verifies the report itself** — the stage most reviews skip:
   agents refute the report's own syntheses, catching from-memory verdicts
   and unpropagated corrections.
8. **Lands on a capped action plan** — 3 actions now + 3 this month, hard
   cap; experiments require a baseline step before any change.

It progresses **incrementally by default**: the truth about progress lives
on disk, and the skill resumes at the first missing artifact — including on
dossiers created before the skill existed.

## Install

```sh
git clone https://github.com/bastien-gallay/contre-expertise
ln -s "$(pwd)/contre-expertise/skills/contre-expertise" ~/.claude/skills/contre-expertise
```

## Usage

```text
/contre-expertise corpus:docs/how-i-work.md calibre:standard
/contre-expertise slug:my-method --overwrite   # archive current output, restart
/contre-expertise slug:my-method --reflect     # J+30 re-run (verdict diff)
```

Arguments (all optional — the skill asks for what is missing):

| Argument | Meaning | Default |
| --- | --- | --- |
| `corpus:` | paths of the texts describing the method | asked |
| `slug:` | short dossier name | derived |
| `calibre:` | `light` / `standard` / `full` | asked, with costs |
| `lang:` | language of all deliverables | corpus language |
| `out:` | output root | `.personal/research/` if present, else `docs/contre-expertise/` |

## Language

The skill instructions are English. **Everything it produces** — notes,
interview, report, action plan, agent prompts — is written in the language
of your corpus (override with `lang:`). Artifact filenames (`etat.md`,
`rapport.md`, `plan-action.md`…) are fixed identifiers and are never
localized: incremental resume depends on them.

## Task-system integration

The action plan ends with a preformatted "to route" checklist, each item
carrying its evidence trace (`[src: <slug>/C-xx]`). If
[daily-ops](https://github.com/bastien-gallay/daily-ops) is installed, the
items route through `/do-add`; otherwise the checklist itself is the
canonical copy. Planned deeper integrations are tracked in
[daily-ops#31–#37](https://github.com/bastien-gallay/daily-ops/issues).

## Origin

Reference execution: a 37-page white paper auditing the author's own
AI-assisted development method (June 2026, private dossier). The skill
encodes that execution's lessons — including its own failures: the report
counter-verification it had skipped, the from-memory verdicts that stage
caught, and the interview that inverted the report's central diagnosis.

## License

[MIT](LICENSE)
