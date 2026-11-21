# market-strategist

A Claude Code skill that acts as a strategic advisor: market analysis,
positioning, traction, pitch, and project communication — commercial or not.

Most strategy tooling hands you an empty canvas. This one fills it, commits to a
reading, names what is weak, and asks you the one question the analysis could
not answer. You react; it corrects. The deliverable is a move you can make this
week, not a completed template.

## What it does

```text
INTAKE → DETECT → PLAN → [FRAME → REACT → SYNTHESISE]* → DELIVER
```

It classifies the need, picks a sequence of **at most three** frameworks, runs
each one itself, and pushes back throughout.

| Need | Default sequence |
| --- | --- |
| Market scan | PESTEL → Competitive Map → Blue Ocean |
| Positioning | Competitive Map → Value Prop Canvas → Blue Ocean 4 Actions |
| Traction | Audience Profile → 19 Traction Channels → Growth Loop |
| Pitch | SONCAS → Argument Structure → Objection Map |
| Communication | Audience Profile → Message Architecture → Content Channels |
| Full strategy | BMC → Competitive Map → Value Prop → Traction |

## The library

Twenty-four frameworks in `skills/market-strategist/references/frameworks.md`,
each with a purpose, an execution procedure, a rendering shape, and its own key
question.

- **Well-known (1–14)** — PESTEL, Competitive Map, Blue Ocean 4 Actions, Value
  Proposition Canvas, Business Model Canvas, 19 Traction Channels, Growth Loop,
  SONCAS, Argument Structure, Objection Map, Audience Profile, Message
  Architecture, Content Channels, Porter's 5 Forces.
- **Lesser-known and emerging (15–24)** — Jobs-to-be-Done + Opportunity
  Scoring, Obviously Awesome, Wardley Maps, The Mom Test, Crossing the Chasm
  segments, Causal Loop Diagrams, Diffusion of Innovation, StoryBrand,
  Ecosystem Map, Enemy Framework.

`--original` draws from the second group, or goes looking for a cross-domain
lens — ecology for market dynamics, narrative theory for positioning, game
theory for competitive moves.

## What it is not

- **Not a workshop facilitator.** It never asks you to fill a canvas. It fills
  one and lets you correct it, because a wrong hypothesis you fix in ten
  seconds beats a blank grid you abandon.
- **Not a cheerleader.** Specific observation or silence. It flags the product
  chasing a market that does not exist, the traction plan sitting in one
  channel family, the pitch optimised for the speaker.
- **Not commercial by default.** For an open-source project, a community, or a
  body of professional expertise, it says *audience* not *clients*, *reach* not
  *conversion*, *impact* not *revenue* — unless you frame it commercially
  yourself.
- **Not a document generator.** It writes a file only when you pass
  `--output`.

## Install

```bash
./install.sh                    # symlink into ~/.claude/skills (edits propagate)
./install.sh --copy             # copy instead
./install.sh --dir .claude/skills   # install into a project, or another host
```

Then type `/market-strategist` in Claude Code.

## Usage

```text
/market-strategist SaaS audit tool for SMEs
/market-strategist --goal traction  a monthly local meetup, grow the audience
/market-strategist --goal pitch  convince a steering committee to fund an architecture overhaul
/market-strategist --goal communicate  fractional CTO positioning
/market-strategist --original  open-source CLI tool launch
/market-strategist --frameworks wardley,jtbd --output strategy.md  we're losing to a free rival
```

| Flag | Default | Effect |
| --- | --- | --- |
| `--goal` | auto-detect | `analyze` · `position` · `traction` · `pitch` · `communicate` · `full` |
| `--frameworks` | auto | Comma-separated; overrides detection |
| `--original` | off | Lesser-known or cross-domain framework |
| `--output FILE.md` | none | Also write the session to that path |

`GOAL=traction` and `TOPIC="..."` still work — earlier invocations used them.

## Portability

Plain prose over one reference file, with no runtime dependency beyond reading
that file. It runs in Claude Code, in Claude Desktop, and in any agent that can
read a directory. Where a capability is missing it degrades and says so: no web
search means lesser-known frameworks only; no file write means the `--output`
document is rendered inline.

## License

MIT.
