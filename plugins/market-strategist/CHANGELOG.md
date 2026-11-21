# Changelog

All notable changes to this skill are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.1.0] — 2026-08-02

First release. Ported from a Claude Desktop skill of the same name, restructured
as a standalone single-skill repository.

### Added

- `skills/market-strategist/SKILL.md` — the advisor protocol, structured §0–§10:
  always-on directives, invocation, the library, the session flow, original
  mode, selection heuristics, mandatory warnings, anti-patterns, the output
  template, portability, self-check.
- `skills/market-strategist/references/frameworks.md` — the 24-framework
  library, carried over unchanged: 14 well-known, 10 lesser-known or emerging,
  each with purpose, execution procedure, rendering shape, and key question.
- `install.sh`, with `--copy` and `--dir` so the skill can be installed
  per-project or into a non-default skills directory. It refuses to install a
  layout missing the framework library, which the skill degrades badly without.
- Plugin and single-plugin marketplace manifests.

### Changed from the Claude Desktop original

- **Flags replace `KEY=value` arguments.** `--goal`, `--frameworks`,
  `--original`, `--output`, with the topic as free text — the shape a Claude
  Code slash command actually receives. The `KEY=value` forms are still
  accepted as synonyms so older invocations keep working, and unparseable text
  is treated as topic rather than as an error.
- **The reference file is read selectively.** The original said "load it before
  executing any framework"; at 772 lines that is most of a context window spent
  to run three frameworks. It now reads the table of contents, then only the
  entries in play.
- **Capability degradation is explicit.** Original Mode's sub-mode B needs web
  search, which not every host provides; the skill now falls back to the
  lesser-known-frameworks sub-mode and says so, rather than improvising a
  framework with an invented origin. Same for a missing reference file and a
  missing write tool.
- **Anti-patterns and a self-check were added**, matching the house structure.
  The behavioural rules that were scattered through the original's prose are
  now a table you can fail against.
- **The examples were decoupled from real projects.** The original shipped with
  a named client and two personal projects in its quick-start block. A skill
  that travels to other people's setups should not carry them.
