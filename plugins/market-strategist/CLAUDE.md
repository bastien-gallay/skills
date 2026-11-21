# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## What this repo is

A single-skill repository. It packages **one** skill — `market-strategist` —
and nothing else. There is no application, no build, no test suite. The product
is the protocol prose: `SKILL.md` and the framework library are the deliverable,
and every other file exists to install, lint, or document them.

## Files that matter

- **`skills/market-strategist/SKILL.md`** — the advisor protocol. YAML
  frontmatter (`name`, `description`, `user-invocable`, `argument-hint`) drives
  discovery and triggering; the body is what Claude executes. Structured §0–§10.
  The flag names in `argument-hint` must match §1's table, and the `--goal`
  values must match the need-type rows in §3.2 — those are the only
  cross-references that break silently.
- **`skills/market-strategist/references/frameworks.md`** — 24 framework
  entries, each with purpose, execution procedure, rendering shape, and key
  question. The anchors (`{#pestel}`, `{#wardley}`, …) are load-bearing: §3.2's
  sequences and §5's heuristics name frameworks, and a renamed anchor leaves
  them pointing at nothing. Adding an entry means adding it to the file's own
  table of contents *and* to the README's library list.
- **`README.md`** — human-facing summary; must stay in sync with `SKILL.md`'s
  spine but is not itself executed.
- **`install.sh`** — symlinks (default) or copies `skills/market-strategist`
  into a skills directory. Symlink is the intended mode so edits propagate live.

## Design decisions worth not re-litigating

- **The skill fills the framework; the user reacts.** This is the whole
  premise, and it is what separates the skill from every canvas template in
  circulation. A wrong hypothesis corrected in ten seconds beats a blank grid
  abandoned in five. Any edit that pushes work back onto the user — "list your
  competitors", "score these yourself" — is a regression, not a refinement.
- **Three frameworks maximum.** An earlier draft had no ceiling. The fourth
  framework consistently buys less than a sharp answer to the third, and a
  session that runs five is a session nobody acts on.
- **The reference file is read selectively, not wholesale.** The Claude Desktop
  original said "load it before executing any framework". At 772 lines that is
  a large fraction of a context window spent to run three entries. TOC first,
  then only what is in play.
- **`KEY=value` arguments are accepted, not documented as primary.** The
  original used `TOPIC="…" GOAL="…"`. Slash commands hand over free text, so
  flags are the real shape — but silently failing on an old invocation would be
  worse than parsing both. Unparseable text becomes topic, never an error.
- **Degradation is stated, never silent.** Original Mode sub-mode B needs web
  search; some hosts have none. The skill says which capability it lacks and
  falls back, because a framework whose origin it cannot name is an
  improvisation, and an improvisation presented as canon is the one failure
  mode a strategy advisor cannot recover from.
- **Non-commercial vocabulary is a rule, not a nicety.** Saying *clients* to
  someone running a community project imports goals they never had, and the
  analysis then optimises for them.
- **Examples carry no real project.** The Desktop original shipped with a named
  client and two personal projects in its quick-start block. A skill that
  travels to other people's setups must not carry them.

## Provenance

Ported 2026-08-02 from a Claude Desktop skill of the same name, authored by the
same person. The framework library came across unchanged; `SKILL.md` was
restructured to the house §-numbered shape, given flag-based invocation,
selective reference loading, explicit capability degradation, an anti-pattern
table, and a self-check.

## State — what is open

- **Settled.** The port is complete and installs cleanly. `0.1.0` is the first
  release.
- **Open, not ticketed — the flag parsing is written but unexercised.** Every
  session so far ran under the Desktop `KEY=value` form. The prediction to
  check on the first real run: whether free-text topics containing a literal
  `--` word get mis-consumed as flags.
- **Open, not ticketed — selective reference loading is untested against long
  sessions.** Reading the TOC then three entries is the design. Nobody has yet
  measured whether a `--goal full` session, which touches four frameworks and
  the heuristics, ends up loading most of the file anyway.
- **Unreleased publicly.** The manifests' `homepage` and `repository` point at
  `github.com/bastien-gallay/market-strategist`, which does not exist yet.

## Conventions

- **Markdown is linted with markdownlint** against `.markdownlint.jsonc`.
  `MD013` is disabled because the framework tables and the library's ASCII
  renderings run wide on purpose; keep prose wrapped at ~78 columns to match.
- **`.gitignore` covers five paths**: `.DS_Store`, `.personal/`, `dist/`,
  `node_modules/`, `.impeccable/`.
- Version bumps live in `.claude-plugin/plugin.json` *and* `marketplace.json` —
  both, or the plugin silently freezes.
