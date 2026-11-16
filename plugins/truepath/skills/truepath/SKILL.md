---
name: truepath
description: Generate a self-contained HTML simulation that explains a process or a bug path step by step — one dot travels the real path, a data panel shows what changes at each step, and "before / after" scenarios play side by side with their first divergence marked. Verdicts are computed by the repository's own code (an oracle run on a frozen git snapshot) or by a declared JS port, and the build refuses to write anything that contradicts them. Use when asked to "show the process running", "animate this bug", "compare before and after the fix", « fais une simulation du process », « montre le cas avant/après », or to explain a decision rule with real or illustrative cases.
---

# truepath

One `spec.json` describes the process (nodes, edges), the scenarios (path,
messages, captions, inputs) and where the verdicts come from. `build.py`
computes the verdicts, lays the graph out, runs the checks, and writes one
offline `.html` — or nothing.

```text
spec.json ──┐
oracle/port ├─► build.py ──► checks C1–C13 ─► sim.html   (or nothing)
layout.py ──┘                                └► fixture.json (--export)
```

## Workflow

1. Copy the nearest example next to the subject's notes (see *Files*),
   rename `spec.json` to `<subject>.spec.json`.
2. Describe nodes and edges. Every sink node (an outcome) gets a `kind`;
   kinds are the only colours, each with a legend label.
3. Choose where the verdicts come from (see below): an `oracle` when the
   rule exists in code, a JS `port` otherwise.
4. Write the scenarios. Each declares its `origin`, its `inputs`, the
   `expect`ed verdict fields, and its `steps` along real edges.
5. Build, then open the file:

   ```sh
   python3 <skill-dir>/scripts/build.py <subject>.spec.json
   ```

6. Read the violations, fix the spec — never the check.

`spec.json` builds `sim.html`, `<subject>.spec.json` builds
`<subject>.sim.html`; `-o` names another file.

The page opens on the first tab with the detail panel open. Folding the panel
switches to the overview: the whole path drawn, one dot looping on it.

## Where verdicts come from

| Source | Spec key | Use when | Marked in the panel |
| --- | --- | --- | --- |
| Oracle | `oracle` | the rule exists in a repository | `✓ code` |
| Port | `port: "decide.js"` | no code yet, a rule under discussion, a process with no code | `⚠ ported` |

**Oracle protocol.** `build.py` takes `git archive` of `oracle.ref` (never
the live checkout: a branch under work may move during the build), extracts
`oracle.paths`, links `oracle.link` (typically `node_modules`) and copies
`oracle.files` into it, then runs `oracle.cmd` in `oracle.cwd` with:

- `TRUEPATH_ORACLE_IN`: a JSON array of every scenario's `inputs`;
- `TRUEPATH_ORACLE_OUT`: where to write a JSON array of verdicts, same order.

`oracle.repo` is read from the spec's folder when it is relative. `link` and
`files` are both written `{path in the snapshot: where it comes from}`: a
path in the repository for `link`, a file next to the spec for `files`.

A verdict is an object of fields. `outcome` is required: it names the node the
path must end on, and is what ties a scenario to the logic. `basis` optionally
says, per field, whether real code computed it (`"code: …"`), the glue copied
a behaviour (`"port: …"`), or the simulation defines it (any other text,
shown `◇ definition`). The page shows that mark next to every panel value
whose field has a basis, its full text on hover, and `--export` asserts only
fields whose basis is code: a field with no basis counts as code under an
oracle, as ported under a `port`. One oracle can mix them: a rule still
under discussion is ported beside the rules the code already runs. Any
runner works: a test file of the
project's own framework, a script, a JUnit test for Java. The footer names
the ref and the short sha that produced the verdicts.

A test-file oracle can double as a regression suite: when
`TRUEPATH_ORACLE_IN` is set it writes the verdicts, otherwise it reads the
exported fixture and asserts it. The scenarios then live once, in the spec,
and run in CI. `examples/loyalty-tier/src/oracle.js` does both.

## Spec reference

| Key | Shape | Notes |
| --- | --- | --- |
| `title`, `subtitle`, `source` | strings | `source` lands in the footer; like every text of the spec they are shown as text, never read as HTML |
| `lang` | `en` (default) or `fr` | language of the page's own words; the spec's text is written in that language |
| `kinds` | `{id: {label, color}}` | at most 4 |
| `nodes` | `[{id, label, role?, kind?}]` | `role: "decision"` marks a branching point; where a path starts is found, and drawn round; sinks need `kind` |
| `edges` | `[[from, to, label]]` | label `""` for none |
| `panel` | `[{label, value, at, labels?, digits?, compared?}]` | `value` reads `inputs.x` or `verdict.y`; shown from step `at` (0 is the first); `labels` maps a value to what the page shows (`"true"`, `"false"`, `"null"`, `"[]"` for those values); `digits` zero-pads a numeric code to that length; `compared: true` for the row naming what a pair compares (the fix, the rule), left out of the first-divergence search |
| `scenarios` | `[{id, tab, summary, origin, inputs, expect, steps, undecided?, caseName?}]` | `origin`: `{kind: real\|illustrative, text}`; `steps`: `[{hop: [from, to], message, caption}]`; `undecided: true` flags a rule not decided yet; `caseName` names the case in an exported fixture |
| `pairs` | `[{before, after, tab, summary}]` | two scenario ids, played side by side as `−` and `+`; same number of steps |
| `grid` | `{baseline, questions \| variants, cases, steps, expect?, show?, hover, summary?}` | cases × answers (or rules, fixes), instead of `scenarios` and `pairs`: see below |
| `oracle` | `{repo, ref, paths, link?, files?, cwd, cmd}` | see above |
| `port` | path to a CommonJS file exporting `decide(inputs)` | used when there is no oracle |
| `export` | `{dir, fixture, assert}` | `--export <worktree>` writes the fixture there |

## Comparing several rules: the grid

When the question is "what does each possible answer do to each case", declare
a `grid`. Prefer **questions** to a flat list of rules: the reader decides
question by question, so the page should be laid out that way.

- `baseline`: `{id, label, short?, inputs}`, what happens today;
- `questions`: `[{id, text, options: [{id, label, inputs}], cases, if?}]`.
  `cases` lists the cases that question is decided on; `if: {"Q1": "1A"}` asks
  it only after that answer. `build.py` derives one variant per coherent set
  of answers (`1A+2A`, `1A+2B`, `1B`), merging the options' `inputs`;
- `cases`: `[{id, label, summary, origin, inputs, steps?}]`; `label` names
  the row in words a reader knows, not a case code;
- `steps`: shared by all cells unless a case brings its own;
- `expect`: `{case: {variant: {field: value}}}`, checked by C3;
- `show`: the one panel row a matrix cell shows (by default the first of
  `hover`); `hover`: the rows a cell shows on hover;
- `summary`: a line above the matrix.

A flat `variants: [{id, label, short?, note?, inputs}]` with `baseline` as
an id still works: the matrix then has one section, every case against every variant.

The page opens on the matrix: one table per question, its cases against today
and each answer, the cell's line marked `≠` where it differs from today. There
is no tab per case: a click on a cell opens it, today next to that answer,
with the first divergence marked. Two button rows, `−` and `+`, pick either
side among the section's answers (1A next to 1B, not only next to today), each
named as its question names it; `← matrix` goes back. In the panel, a row
with `"value": "answer"` and `"compared": true` names the answer played.

**Step templates.** `message`, `caption` and `hop` may quote `{inputs.x}` or
`{verdict.y}`: they are filled after the logic ran, formatted like the panel
row reading the same path. A hop to `{verdict.outcome}` lets one step list
serve every rule.

## Checks

| Id | Refuses |
| --- | --- |
| C1 | a step whose hop is not an edge |
| C2 | a path that breaks, does not start at a source node, or has no step |
| C3 | an `expect` field the logic contradicts |
| C4 | a path that ends elsewhere than the logic's `outcome`, or a logic that gives none |
| C5 | an outcome without a kind, a kind without a legend, more than 4 kinds |
| C6 | a label wider than its box (13px monospace) |
| C7 | a scenario without an origin saying real or illustrative, and where from |
| C8 | a pair whose scenarios cannot advance together, or are unknown |
| C9 | a panel row that reads a field a scenario lacks |
| C10 | a matrix cell naming a panel row that does not exist |
| C11 | a case shown under a question whose cell still depends on another question |
| C12 | a case in no matrix section, or a section naming an unknown case |
| C13 | a panel row set to appear at a step the scenario does not have |

C3 and C4 are the point: a scenario that says something the code does not do
cannot be published. C6 guards the layout rather than the spec: boxes are
sized to their labels, so it fires only if `layout.py` stops doing so. Prove
a new check bites by breaking its input once, in `tests/`. Each check is one
function in `build.py`, listed in `CHECKS` under the id of this table.

A spec the build cannot read at all (a missing key, an edge to an unknown
node, a port that throws) is refused the same way, in plain words, before
the checks run.

## Design rules

- One moving element per diagram: a single dot, constant speed, one hop at a
  time. Two diagrams side by side move in step.
- Taken edges are solid, untaken ones dashed and grey; nodes off the path fade.
- Colour encodes the outcome kind only. In a pair, the first divergence (the
  first step where a panel value differs) is outlined amber and marked `≠` on
  both sides, and the panel shows `−` / `+` columns.
- Illustrative scenarios only where no real case reaches that outcome; say
  where the real case comes from (ticket, record, measure, date).
- A grid shows one field per cell; three fields per cell made the matrix
  unreadable.
- Light theme by default, dark under `prefers-color-scheme`; no web font, so
  the file works offline.

## Files

| Path | Role |
| --- | --- |
| `scripts/build.py` | reads the spec, gets the verdicts, runs the checks, writes the page and the export |
| `scripts/runtime.html` | the page; `build.py` gives it what it shows, already formatted, and nothing else of the spec |
| `scripts/layout.py` | layered layout: boxes sized to their label, orthogonal edges |
| `examples/refund-window/` | a JS port and a before/after pair |
| `examples/free-shipping/` | a grid: two open questions, each decided on the cases it changes |
| `examples/loyalty-tier/` | an oracle on the folder's own `src/`, its glue and the fixture `--export` writes |

Generated files (`.truepath/`, where an oracle's snapshots live, and `*.html`
next to a spec) are build output. The port examples keep their `sim.html`
so the skill can be seen without running it. `loyalty-tier` keeps none: its
footer names the commit that produced the verdicts, so the page changes with
every commit, and it builds only inside a git repository that holds it.

## Limits

- One diagram type: the process flow. Sequence and architecture views are not
  built.
- `C6` is measured on macOS (`ui-monospace`); a narrower Windows font only
  adds air.
- Steps are declared, not derived from the logic: C3 and C4 catch a wrong
  outcome, not a wrong intermediate message.
