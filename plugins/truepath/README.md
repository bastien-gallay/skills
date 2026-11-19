# truepath

[![ci](https://github.com/bastien-gallay/truepath/actions/workflows/ci.yml/badge.svg)](https://github.com/bastien-gallay/truepath/actions/workflows/ci.yml)

![The free-shipping grid: the matrix of cases against answers, then a click
on a cell that differs plays that case, today next to the answer
](docs/free-shipping.gif)

An agent skill that turns a process, a bug path or a rule under discussion
into one self-contained HTML page: a dot walks the real path through the
graph, a data panel shows what changes at each step, and two scenarios play
side by side with their first difference marked.

What makes it more than an animation: the verdicts come from your
repository's own code, run on a frozen `git archive` of a ref, or from a
declared port of it. The build checks every scenario against them and
writes nothing if one disagrees.

```text
spec.json ──┐
oracle/port ├─► build.py ──► checks C1–C13 ─► sim.html   (or nothing)
layout.py ──┘                                └► fixture.json (--export)
```

## Status

0.1.1, tagged
[`v0.1.1`](https://github.com/bastien-gallay/truepath/releases/tag/v0.1.1)
on 2026-11-18. The spec vocabulary may still change before
1.0; [`CHANGELOG.md`](CHANGELOG.md) says what did. The examples build with 0
violations, and the two that keep their page rebuild it byte for byte; the
tests check both on every push to `main` and every pull request.
Known limits are listed under *Limits* in
[`SKILL.md`](skills/truepath/SKILL.md).

## Install

In Claude Code, as a plugin from this repository:

```text
/plugin marketplace add bastien-gallay/truepath
/plugin install truepath@truepath
```

Or from the [skills hub](https://github.com/bastien-gallay/skills), with the
other skills I maintain:

```text
/plugin marketplace add bastien-gallay/skills
/plugin install truepath@skills
```

For another agent, clone the repository and copy `skills/truepath/` into the
skills folder it reads:

```sh
git clone https://github.com/bastien-gallay/truepath.git
cp -R truepath/skills/truepath ~/.claude/skills/
```

Needs Python 3.9 or later (standard library only) and, for a JavaScript port
or a JavaScript oracle, Node.js. The page works offline: no web font, no CDN.

## Try it

```sh
python3 skills/truepath/scripts/build.py skills/truepath/examples/refund-window/spec.json
```

Then open `skills/truepath/examples/refund-window/sim.html`: a refund asked
on day 30, refused before an off-by-one fix and granted after it.

| Example | Shows | Verdicts from |
| --- | --- | --- |
| [`refund-window`](skills/truepath/examples/refund-window/) | a before/after pair | a JS port |
| [`free-shipping`](skills/truepath/examples/free-shipping/) | a grid: two open questions against three cases | a JS port |
| [`loyalty-tier`](skills/truepath/examples/loyalty-tier/) | an oracle, and the fixture it exports | the folder's own `src/tier.js`, as committed |

`loyalty-tier` reads its code through `git archive`, so it builds from a
clone of this repository, not from a bare copy of the folder.

## What it covers

- one scenario, played step by step;
- a before/after pair, its first divergence outlined;
- a grid of cases against the answers to one or more open questions, the
  matrix first, each cell opening the case.

The page opens paused, the play button green; the diagram zooms and pans,
and once zoomed the view follows the dot.

![A before/after pair: the same refund request refused on the left, granted
on the right, the decision where they part outlined
](docs/refund-window.png)

The full contract is in [`skills/truepath/SKILL.md`](skills/truepath/SKILL.md).

## Develop

```sh
python3 -m unittest discover -s tests
```

The tests break each check's input once and expect the build to refuse, then
play the built pages step by step under Node.js, without a browser. CI runs
them on Python 3.9 and 3.13, with `ruff check` on the code and
`markdownlint-cli2` on the docs.

## Related skills

truepath is listed in [bastien-gallay/skills](https://github.com/bastien-gallay/skills),
the registry of the skills I maintain. Two of them meet it often:

- [`show-me`](https://github.com/bastien-gallay/show-me) picks the visual a
  piece of content calls for; truepath builds one of them, the path through
  a process, and checks it against the code.
- [`wrap`](https://github.com/bastien-gallay/wrap) closes a milestone; its
  configuration for this repository is [`.wrap.md`](.wrap.md).

## Influences

[dashmotion](https://csthink.github.io/dashmotion/) showed how much a
diagram gains when something visibly travels along its edges. truepath takes
that idea somewhere else: a single dot, moved step by step by a scenario,
on a path the code has to agree with.

## License

MIT, see [`LICENSE`](LICENSE).
