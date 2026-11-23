---
name: truepath
description: Generate a self-contained HTML simulation that explains a process or a bug path step by step — one dot travels the real path, a data panel shows what changes at each step, "before / after" scenarios play side by side with their first divergence marked, and several ways can race on one clock, timed step by step. Verdicts are computed by the repository's own code (an oracle run on a frozen git snapshot) or by a declared JS port, and the build refuses to write anything that contradicts them. Use when asked to "show the process running", "animate this bug", "compare before and after the fix", « fais une simulation du process », « montre le cas avant/après », or to explain a decision rule with real or illustrative cases.
---

# truepath

One `spec.json` describes the process (nodes, edges), the scenarios (path,
messages, captions, inputs) and where the verdicts come from. `build.py`
computes the verdicts, lays the graph out, runs the checks, and writes one
offline `.html` — or nothing.

```text
spec.json ──┐
oracle/port ├─► build.py ──► checks C1–C19 ─► sim.html   (or nothing)
layout.py ──┘                                └► fixture.json (--export)
```

## First, the shape

Pick the shape from the question before writing a spec. The page earns its
place when the *path* differs between cases; when only a number or a list
changes and every case walks the same path, it does not.

| The question | Shape |
| --- | --- |
| one case, before and after a fix | one `pair` |
| one rule, a few cases | `scenarios` |
| several cases, each under two versions, rules or answers | a `grid` with `variants` (or `questions`): one matrix, each cell opening its case |
| timed runs whose path differs between cases (a step one case skips, a loop that turns more often): where does the time go, and why did it move | `scenarios` with a `measure`: one bar per case beside or under the graph (see *Measured time*) |
| a few ways to the same end, compared on one number (which is fastest) | `scenarios`, one per way, with a `measure` of `source: "estimate"` when nothing runs: the bars stand beside the graph; add a `race` to run them at once |
| every case walks the same path, only a count, a list or the time per step changes | not truepath: answer with a table, and say why no page was built |

More than two pairs comparing the same two versions is a grid: written as
pairs, the reader gets one tab per case and no table to compare them in.

Timed runs on one straight path are a table, however the time moved: the
dot walks the same line in every case and says nothing the rows do not. The
page earns its place when the path explains the time: the step an image no
longer runs, the loop that turned twelve times instead of two.

## Then, the view

The shape says what is compared; the view says how a path is drawn. They
are two choices: a grid's cell, a pair, a scenario open on whichever view
the spec names in `view`.

| The question | View |
| --- | --- |
| where it branches, which rule decides | `flow`, top to bottom (the default) |
| a long, nearly straight pipeline; a page to project on a wide screen | `flow-lr`, left to right |

When both fit, the user decides: ask it as a doubt, one question whose
options show each view as a small text sketch, yours first, and write the
answer in `view`. With no one to ask (an agent working alone), pick
yours, offer the other in `views`, and say so in the report. `views` lists
other views the page offers to switch to (`↓` `→` beside the zoom, or the
key `V`), on the same step; leave it out when one view says it, since each
one offered is one more drawing to read.
The same spec gives every view: nodes, edges and steps are not rewritten.

## Workflow

1. Find the unit to show: the function or module that decides the path.
   When the code lives in a remote repository, do not clone or build it:
   list its paths and fetch only that unit's files (see *Working from an
   excerpt*). Read its tests too: each one is a real case, already checked.
2. Copy the nearest example next to the subject's notes (see *Files*),
   rename `spec.json` to `<subject>.spec.json`.
3. Describe nodes and edges. Every sink node (an outcome) gets a `kind`;
   kinds are the only colours, each with a legend label. A branch's name
   leads to one place: when one answer can end two ways, what picks the way
   is a decision node of its own (C19). Choose the view (see *Then, the
   view*).
4. Choose where the verdicts come from (see below). By default, an `oracle`
   that runs the unit alone, its collaborators replaced by doubles, as a
   unit test would (see *Running the unit, not the system*); a JS `port`
   when the rule has no code yet.
5. Write the scenarios. Each declares its `origin`, its `inputs`, the
   `expect`ed verdict fields, and its `steps` along real edges. A page
   that shows a bug fix takes the bug as its `title`, said as the reader
   sees it (*the trail shows one transaction per territory*), the ticket
   and the change in `subtitle`. Name a case by what decides its path; an
   input that changes nothing on the path (a file format, say) stays out of
   the case's name.
6. Run `build.py --check`: the checks that need no verdict (paths, layout,
   texts), without the logic, nothing written. Write down your doubts: an
   open one is printed `?`, a question to ask, not a violation. Ask the
   user about the strongest ones before building (see *Doubts*);
   `build.py --dry-run` meanwhile runs the logic and every check, and
   still writes nothing, so the glue can be tried before the answers.
7. Build, then open the file:

   ```sh
   python3 <skill-dir>/scripts/build.py <subject>.spec.json
   ```

8. Read the violations, fix the spec — never the check.

`spec.json` builds `sim.html`, `<subject>.spec.json` builds
`<subject>.sim.html`; `-o` names another file.

Keys work wherever the focus is, a tab included, so a reader clicks a tab
and drives the case from the keyboard: `←` `→` a step, `Home` `End` the
first and last step, `Space` play or pause; on the tab row `↑` `↓` change
tab, and `1`…`9` open the tab of that rank. `V` switches to the next view,
when the spec offers more than one.

When a path comes back to a node (a loop), each branch leaving that node
gets a numbered badge per pass, right after the branch's label: *timeout*
`① ②`, *ok* `③` says the third try got through. A badge appears once
the dot has run that hop, with a short pop. Up to three badges sit side by
side, more read as a range (`1–11`) and the last pass. On a horizontal run
they sit above the line, never on it; in a pair, the side alone on a branch
keeps that row, and when both sides took it the `+` row mirrors the `−`
one under the line. The pass under way is filled; a badge names its step on
hover or focus, and a click or `Enter` takes the cursor there. Nodes passed
once get none: there the order is the path itself.

A click (or `Enter`) on a node of the path takes the cursor to the first
step that reaches it; on a node the cursor is already at, to the next one,
then round again: a loop's node walks its passes.

The address follows the reader: opening a case, picking another side or
another view adds an entry to the browser's history (`#case=…&minus=…&plus=…`,
`#tab=…`, `&view=…`), so Back and Forward retrace the way and a copied link
opens the same case.

The page opens paused on the first tab, with the detail panel open; the green
play button, under the diagram with the other controls and the keys that
drive them, starts it. The list of steps tells a step once the dot has
reached it; the ones to come are numbered blanks, still a click away.
Folding the panel switches to the overview: the whole path drawn, one dot
looping on it.

The diagram zooms with `−`, `+`, Ctrl/Cmd + wheel, a trackpad or two-finger
pinch, and the keys `+`, `-`, `0`; *Fit* (or `0`) shows it whole again. Once
zoomed, a drag or the wheel pans, and the view glides after the moving dot so
the current hop stays in sight (a race has its own camera, see *Design
rules*). A pan stops that following; Play, Restart and
*Fit* resume it. A case opens on the whole graph; when that draws its labels
under 12px, the first Play or step zooms to that size and follows the dots;
*Fit* and the overview show the whole graph.

## Where verdicts come from

| Source | Spec key | Use when | Marked in the panel |
| --- | --- | --- | --- |
| Oracle | `oracle` | the rule exists in a repository | `✓ code` |
| Port | `port: "decide.js"` | no code yet, a rule under discussion, a process with no code | `⚠ ported` |

**Oracle protocol.** `build.py` takes `git archive` of `oracle.ref` (never
the live checkout: a branch under work may move during the build), extracts
`oracle.paths`, links `oracle.link` (typically `node_modules`) and copies
`oracle.files` into it, then runs `oracle.cmd` in `oracle.cwd` with:

- `TRUEPATH_ORACLE_IN`: the path of a file holding a JSON array of every
  scenario's `inputs`;
- `TRUEPATH_ORACLE_OUT`: the path where to write a JSON array of verdicts,
  same order.

`TRUEPATH_SPEC_DIR` holds the spec's folder: a dependency cache kept next
to the spec (`CARGO_HOME`, an npm cache) is reached from it, never by
counting `../` out of the snapshot, whose depth is the build's business.
`cmd` runs without a shell, so `build.py` itself replaces
`$TRUEPATH_SPEC_DIR` in its arguments: `["env",
"CARGO_HOME=$TRUEPATH_SPEC_DIR/.cargo", "cargo", "run", "--offline", "-q"]`.

`cmd` is an argument list, run without a shell: to pin a toolchain, start it
with `env`, as in `["env", "JAVA_HOME=…", "mvn", "-o", "-q", "-Dtest=…",
"test"]` (a Java project's annotation processors, Lombok among them, may
fail on a JDK newer than the one the project targets).

`oracle.repo` is read from the spec's folder when it is relative. `link` and
`files` are both written `{path in the snapshot: where it comes from}`: a
path in the repository for `link`, a file next to the spec for `files`.
What `files` brings is not the ref's code: the footer names each such file
after the ref (`code of main @ 1a2b3c4 + from the spec: glue.py`). Code from
another ref, an old version to compare against say, belongs in its own
oracle run or in the snapshot's `paths`, not in `files`.

A verdict is an object of fields. `outcome` is required: it names the node the
path must end on, and is what ties a scenario to the logic. `basis` optionally
says, per field, whether real code computed it (`"code: …"`), the glue copied
a behaviour (`"port: …"`), a double answered it (`"double: …"`, shown
`◌ double`), or the simulation defines it (any other text, shown
`◇ definition`). The page shows that mark next to every panel value
whose field has a basis, its full text on hover, and `--export` asserts only
fields whose basis is code: a field with no basis counts as code under an
oracle, as ported under a `port`. One oracle can mix them: a rule still
under discussion is ported beside the rules the code already runs. Any
runner works: a test file of the
project's own framework, a script, a JUnit test for Java. The footer names
the ref and the short sha that produced the verdicts.

## Measured time

When the question is where a run spends its time (a CI job, a batch, a
request), the path is the process and the logic only says how it ends; the
times are measured on real runs. `measure` runs a command that reads them:

```json
"measure": {"cmd": ["node", "measure.js"], "stat": "mean", "unit": "s", "tolerance": 1}
```

The command runs in the spec's folder (or `cwd` under it), never on a
snapshot: measures are data, not code under test. It reads
`TRUEPATH_MEASURE_IN`, `[{id, inputs}]` in scenario order, and writes
`TRUEPATH_MEASURE_OUT`, one object per scenario:

```json
{"total": 152.3, "n": 4, "failed": 1, "excluded": [{"n": 2, "why": "with nothing to apply"}],
 "steps": {"WAIT": 4.5, "TOOLS": 35.3, "PLAN": 24.8},
 "basis": "measure: CI log of week 1; each run cut by the time stamps of its log lines"}
```

Measure where the reader meets the time. A page reload is felt in the
browser, which parses and draws what the server sent: a harness that stops
when the server has written its last byte misses the part that grows most
with the data. When the runs cannot reach that far, end the path where
the measure ends, name what it leaves out in `basis`, and raise it as a
doubt: the page must not read as the whole wait.

`total` is what a whole run took, `n` how many runs the `stat` (`mean` or
`median`) sums up, `failed` the failed runs left out (none: leave it out),
`excluded` the runs left out for another reason (`why` in the page's
language: a warm-up run, runs with nothing to do), `steps` the time on each
node, all passes through a loop together. `basis` says where the times come
from and how a run was cut into steps, in the page's language; when steps
run side by side, say which one a second counts for. With `median`, the
steps' medians need not add up to the median run: C16 holds within
`tolerance`, set to the gap the runs show. Keep the script that reads the
raw log next to the spec, so the page can be built again when the log
grows.

The page draws one bar per case, every case on one scale, running as the
graph runs: upright beside a top-to-bottom graph, its steps stacked down
in path order, and under a left-to-right one. Beside the graph, the
heights compare at a glance ways that share few steps (three ways to the
same end); under it, the segments line up steps that most cases share.
The case played is in bold, the node the dot is on is filled in every bar,
and `≠` outlines, in each bar after the first, the step that moved most
from the first bar; a step gone from that bar is outlined in the first. A
bar that shares no step with the first takes no mark: another way, not a
change.
A step whose time follows the load rather than the case (a plan that grows
with the modules applied) would take that mark from the change that
matters: `"compare": [nodes]` in `measure` names the steps the mark weighs.
Hovering a segment outlines its node; a click opens its case on the first
step that reaches it. A panel row may read
`measure.total` or `measure.n`, marked `◉ measured`. The footer names each
basis.

When nothing can be run (a game, a process on paper, a plan), the times
can still be worked out from a model of each step: `"source": "estimate"`.
The command then writes `{total, steps, basis}` only, with no `n` nor
`stat`; the page says *estimated* where it would say *measured*, and a
panel row reading the time is marked `≈ estimated`. Say in `basis` what
each step is assumed to take. An estimate never stands for a measure: when
runs exist, measure them.

A `race` runs its scenarios at once on the clock: each step lasts the time
of the nodes it reaches (a node reached twice in a loop shares its time
between its visits; a step with no time shares the timed step next to it),
so the fastest way
arrives first, the slowest after twelve seconds of clock at 1×, a little more
on screen since each arrival slows down and holds. A clock runs above
the graph, each bar fills in its dot's colour, the step list tells each
arrival, and the summary the order of arrival with each time.

Name a case by what it measures (*Week 1*, *before the cache*), and keep
the path faithful to the runs: a loop that turns twelve times in one week
and twice in the next is twelve passes and two, and its badges say so.

## Running the unit, not the system

The default oracle runs the unit that decides the path and nothing around
it, the way a unit test does: one function or module of the ref, compiled
or loaded alone, its collaborators (a database, a network client, a clock,
a signature scheme) replaced by doubles that answer what the scenario says.
Each scenario then shows one test path, and its verdict depends on the
unit's code and on the scenario, not on a deployment. Building the whole
system is the exception, for a path that crosses several units on purpose.

- **The unit stays unchanged.** Take it from the snapshot as committed;
  when it must be cut out of a larger file, cut it by markers (from the
  first type to the end of an `impl`, say) in the glue, never by editing
  it. What the language needs around it (types it names, a logger, an
  error crate) is glue, brought by `oracle.files`.
- **A double answers, it never decides.** A stub returns what the scenario's
  `inputs` say; a fake is a working toy (a hash, a signature that binds a
  message to a key) whose answers follow from its inputs, so a tampered
  input still fails for the right reason; a mock records what the unit
  asked it. Reach for the project's own test doubles first, when they come
  without the rest of the system.
- **What the unit asked is a verdict too.** A double that records its calls
  turns them into fields (`checked: true`, `sync: "forced"`): the panel then
  shows what the unit did, not only where it ended.
- **Mark what a double decided.** A field the stub's answer settles has a
  basis `double: …`, shown `◌ double`; a field the unit computed stays
  `code: …`, even when a mock recorded it: the unit decided to ask, the
  mock only wrote it down.
- **Say what stood in.** `oracle.doubles` lists each double:
  `{name, kind: stub|fake|mock, replaces}`. The footer names them
  (`· doubles: runner (stub), crypto (fake)`), and a field a double decides
  gets a `basis` that is not `code:`, so the panel marks it. A spec whose
  `files` bring glue without `doubles` is refused (`doubles: []` when the
  files only drive the run).
- **Prefer a small toolchain.** The compiler alone, or the language's
  package manager with a few small libraries the unit names (an error
  crate, say) when rewriting them would put toy code where the real one
  runs. Bring the lockfile through `files`, keep the dependency cache next
  to the spec (`TRUEPATH_SPEC_DIR`), and run offline once it is filled: the
  build then needs no network.
- **Cut the unit by markers, include it by path.** In Rust, `#[path]` on a
  module declared in its own file (`src/unit.rs` holding
  `#[path = "../excerpt/x.rs"] mod x;`), not in an inline module, whose
  path resolves under a folder `files` does not create. The glue's crate
  root then provides every `crate::…` the unit imports, as the project's
  own root did. `files` copies bytes: a lockfile or a binary fixture is
  brought as it is.

`examples/payment-retry/` is the pattern: `src/pay.js` unchanged, a stub
gateway and a mock clock in `glue/oracle.js`, a retry loop.

## Working from an excerpt

`scripts/fetch.py` reads a GitHub repository without cloning it:

```sh
python3 <skill-dir>/scripts/fetch.py tree OWNER/REPO --grep 'runtime/.*\.rs$'
python3 <skill-dir>/scripts/fetch.py get OWNER/REPO path/a.rs path/b.rs --into excerpt
```

`tree` lists the paths at the ref (`--ref`, the default branch otherwise),
to find the unit and its tests. `get` resolves the ref to one commit,
downloads the files unchanged, and commits them, with an `excerpt.json`
naming their origin, in a local git repository. That repository is the
oracle's `repo`: the footer then reads `code of OWNER/REPO @ 1a2b3c4,
excerpt of 2 files`, the upstream commit, not the local one. A later `get`
into the same directory adds files of that same commit only.

Fetch what the unit is, then what it needs to be read; what it needs to
run comes from doubles, not from more files.

## Doubts

Before building, list what you are unsure of, and rank it by how much a
wrong guess would change what the reader concludes:

- a double's answer that decides the outcome, inferred rather than read;
- a case no test of the project covers, so nothing confirms its path;
- code you read but did not run (a log message, a branch the doubles never
  reach);
- a compile-time choice that changes the branches shown: a feature flag, a
  build profile, a platform (the default build may differ from the one you
  chose to keep the unit small);
- a rule whose intent the code does not settle.

Ask the user about the strongest ones, one question at a time, through the
interactive question tool when there is one (its options are the plausible
answers, yours first, marked recommended), at most three before the first
build. Keep the rest in the spec, with what you assumed instead. Each
doubt is recorded in `doubts`: `{id, question, scenarios, answer?,
assumed?}`. C15 refuses a scenario that rests on a doubt with neither an
`answer` nor an `assumed` text, unless it is marked `undecided`, and prints
the question to ask. The answer, with who gave it, or the assumption, with
why it was not asked, stays in the spec: it is why the case reads the way
it does.

A test-file oracle can double as a regression suite: when
`TRUEPATH_ORACLE_IN` is set it writes the verdicts, otherwise it reads the
exported fixture and asserts it. The scenarios then live once, in the spec,
and run in CI. `examples/loyalty-tier/src/oracle.js` does both.

## Spec reference

| Key | Shape | Notes |
| --- | --- | --- |
| `title`, `subtitle`, `source` | strings | `source` lands in the footer; like every text of the spec they are shown as text, never read as HTML, except that `` `x` `` is shown as code (`` \` `` for a literal backtick; a tooltip or a tab drops the backticks) |
| `lang` | `en` (default) or `fr` | language of the page's own words; the spec's text is written in that language |
| `credit` | `true` (default) or `false` | `false` removes the *made with truepath* link at the end of the footer |
| `view` | `flow` (default) or `flow-lr` | how paths are drawn: top to bottom, or left to right, where a branch's name sits on the run entering its target; see *Then, the view* |
| `views` | a list of views | the other views the page offers to switch to; without it, no switch |
| `kinds` | `{id: {label, color}}` | at most 4 |
| `nodes` | `[{id, label, role?, kind?}]` | `role: "decision"` marks a branching point; where a path starts is found, and drawn round; sinks need `kind` |
| `edges` | `[[from, to, label]]` | label `""` for none; one edge per pair of nodes, its label naming every case it carries (`same or absent`) |
| `panel` | `[{label, value, at, labels?, digits?, compared?, series?}]` | `value` reads `inputs.x` or `verdict.y`; shown from step `at` (0 is the first), or `"last"` for each scenario's own last step (a result, in scenarios of different lengths); `labels` maps a value to what the page shows (`"true"`, `"false"`, `"null"`, `"[]"` for those values); `digits` zero-pads a numeric code to that length; `compared: true` for the row naming what a pair compares (the fix, the rule), left out of the first-divergence search and never marked `≠`; `series: true` when `value` is a list with one value per step from `at`, the last one kept: what a loop builds up line by line |
| `scenarios` | `[{id, tab, summary, origin, inputs, expect, steps, undecided?, caseName?}]` | `origin`: `{kind: real\|illustrative, text}`; `steps`: `[{hop: [from, to], message, caption}]`, or `hop: [from, via…, to]` to run through a node without stopping (a loop's return); a step with `motion: "fall"` speeds up as a body falls, lands in a puff of dust, and does not brake into its outcome; `undecided: true` flags a rule not decided yet; `caseName` names the case in an exported fixture |
| `races` | `[{scenarios, tab, summary}]` | 2 to 4 scenario ids run at once on one graph, a numbered dot each, in a tab of its own: unlike a pair, each scenario keeps its tab, and nothing is compared (no `≠`). With a `measure` for each, the race runs on one clock (see *Measured time*); otherwise the dots take a step together |
| `pairs` | `[{before, after, tab, summary}]` | two scenario ids, played as `−` and `+` on one graph, in one tab: a scenario in a pair gets no tab of its own; they may differ in length: the shorter stays on its outcome while the other goes on |
| `grid` | `{baseline, questions \| variants, cases, steps, expect?, show?, hover, summary?, caseHead?}` | cases × answers (or rules, fixes), instead of `scenarios` and `pairs`: see below |
| `oracle` | `{repo, ref, paths, link?, files?, doubles?, cwd, cmd}` | see above; `doubles` is required when `files` is given |
| `doubts` | `[{id, question, scenarios, answer?, assumed?}]` | what was asked before building, and the answer: see *Doubts* |
| `port` | path to a CommonJS file exporting `decide(inputs)` | used when there is no oracle |
| `measure` | `{cmd, stat, unit?, tolerance?, cwd?, compare?, source?}` | measured time per step: see *Measured time*; `source` is `runs` (the default) or `estimate`, which needs no `stat`; `stat` is `mean` or `median`, `unit` `s` by default, `tolerance` (1 by default) how far the steps may add up from the total; `compare` the nodes the `≠` mark weighs (all by default); scenarios and pairs, not a grid |
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
- `summary`: a line above the matrix: what the reader decides, in the
  business's words;
- `caseHead`: the head of the column of cases, when *Case* does not say
  what a row is (*Œuvre envoyée*, *Run*).

A flat `variants: [{id, label, short?, note?, inputs}]` with `baseline` as
an id still works: the matrix then has one section, every case against every variant.

The page opens on the matrix: one table per question, its cases against today
and each answer. A cell says how its case ends first, the outcome node's
label beside its kind's colour (`valeur perdue`, `stockée hors spec`), then
the value of the `show` field: a decision-maker reads the outcome, a
developer the value. `≠` marks the line that differs from today. Nothing else
is highlighted: one mark for change, so the eye lands on what changed.

Beside the matrix, the whole graph is drawn still: the cell under the
pointer or the keyboard focus lights its path there, so a row reads as a
route, not only as a value. The hint over the table starts above the cells,
not above the column of cases: it speaks of the cells. There is no tab per
case: a click on a cell opens it, today next to that answer, with the first
divergence marked. A click on a case's name opens it too, today next to the
section's first answer; under the pointer or the focus it lights that
cell's path, as the cell would.

The open case heads its page with `← matrix`, then the case itself as a
native select among the cases of its section (labelled by `caseHead`), and
`↑` `↓` buttons for its neighbours; the arrow keys do the same while the
case plays. Changing case keeps the `−` and `+` answers the reader chose,
so walking the section compares the same two answers case after case; the
buttons are disabled at the ends of the section. The case keeps its row of
the matrix under its summary, the two cells it compares marked `−` and
`+`; when both walk the same path, the case says so under its summary and
names the values that still differ (or none: a control case). A click (or
Enter) on another cell puts it on `+`, with Shift on `−`, so 1A plays next
to 1B, not only next to today; a one-line hint under the row says so on
screen. `← matrix` or Escape goes back, the focus on the cell the case was
opened from. A row with `"value": "answer"` and
`"compared": true` names the answer played; in a grid the case's row already
says it, so the panel leaves it out.

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
| C8 | a pair or a race naming a scenario that does not exist |
| C9 | a panel row that reads a field a scenario lacks, or a series row whose value is not a list |
| C10 | a matrix cell naming a panel row that does not exist |
| C11 | a case shown under a question whose cell still depends on another question |
| C12 | a case in no matrix section, or a section naming an unknown case |
| C13 | a panel row, or a value of a series, set to appear at a step the scenario does not have |
| C14 | a text over its budget (see *Text budget*) |
| C15 | a scenario resting on an unanswered doubt, unless it is `undecided`; a doubt naming an unknown case |
| C16 | measured steps that do not add up to the run's total, within `tolerance` |
| C17 | a time measured on a node that does not exist, or that the scenario's path does not reach |
| C18 | a measure without its `total`, its number of runs `n` (1 or more, not asked of an estimate) or its `basis`; a negative time |
| C19 | two branches leaving one node under one name: what picks one of them is a decision of its own, drawn as a node |

C3 and C4 are the point: a scenario that says something the code does not do
cannot be published. C6 guards the layout rather than the spec: boxes are
sized to their labels, so it fires only if `layout.py` stops doing so. Prove
a new check bites by breaking its input once, in `tests/`. Each check is one
function in `build.py`, listed in `CHECKS` under the id of this table.

A spec the build cannot read at all (a missing key, an edge to an unknown
node, a port that throws) is refused the same way, in plain words, before
the checks run.

## Text budget

The motion carries the explanation; the text labels it. Write the shortest
text that names what the reader sees, one sentence at most: a reader in a
workshop reads a line, not a paragraph, and a short spec is faster to write.
C14 refuses a text over its budget, in characters, backticks not counted,
measured once `{verdict.x}` and `{inputs.x}` are filled (`--check`, which
runs no logic, measures them unfilled):

| Text | At most |
| --- | --- |
| `title` | 60 |
| `subtitle` | 90 |
| a `summary` (scenario, pair, grid, case), an `origin.text` | 110 |
| a grid question's `text` | 90 |
| a step `caption` | 70 |
| a step `message` | 40 |
| a grid's `caseHead` | 40 |

Detail that does not fit belongs in `source`, which lands in the footer, or
in a `basis` text, shown on hover.

## Design rules

- One moving element per way: a dot, one hop at a time. Outside a race, every
  hop takes the same time, however long it is drawn (the run into an outcome
  and a fall excepted, below); the dot then stays long where
  the story is (a decision, the first divergence, an outcome) and briefly where
  it only passes. Time on screen follows meaning, not ink. A node the dot only
  passes through, a loop's return say, is a `via` of the step, not a step of its
  own. Two sides compared walk one graph, a dot each, marked `−` and `+` and
  moving in step; when one has fewer steps, its dot waits on its outcome while
  the other goes on. An edge both take is the path colour, an edge only one
  takes is that side's colour: the divergence is a fork in one drawing, not a
  difference between two thumbnails. In a race, two to four dots move on
  one clock instead, each step lasting its measured or estimated time.
- On a timed page, a short comet trails each dot: where it was a moment ago
  says how fast it goes. On every page, the run into an outcome slows down at
  its end, and an arrival rings out of the dot and pulses twice round the
  outcome's box.
  A step marked `motion: "fall"` is the exception: its dot speeds up all
  the way down, the distance growing with the square of the time, and lands
  in a puff of dust. A long fall reads best as one step through a node
  (`hop: [edge, falling, bottom]`), the time it takes kept short.
- In a race zoomed to readable labels (a graph that reads whole is not
  followed), the camera keeps the leader (the dot furthest along its own
  way) in sight: it frames the edge every running dot is on, zooming out no
  further than readable labels; when they no longer fit, it follows the
  leader alone, closer. It zooms back in only for a real gain and pans only
  when a way leaves the frame, so a loop does not make it breathe. The
  race's clock slows into each arrival and holds a moment on it, every dot
  alike, so the race stays fair. A pan by hand takes the view until Play
  or Restart; a zoom by hand or *Fit* keeps it the reader's until the tab
  is opened again.
- Taken edges are solid, untaken ones dashed and grey; nodes off the path fade.
- A loop's order is written where it branches: numbered badges on the
  branches leaving a node passed more than once, one per pass, set once
  the dot has taken them.
- Colour encodes the outcome kind only. In a pair, the first divergence is
  outlined amber and marked `≠`: the first step where the paths fork, on the
  last node both still share, or where a panel value differs, whichever comes
  first. The panel shows `−` / `+` columns.
- Illustrative scenarios only where no real case reaches that outcome; say
  where the real case comes from (ticket, record, measure, date).
- A grid shows one field per cell, under its outcome; three fields per cell
  made the matrix unreadable.
- A case opens on the whole graph, the fork and each side's outcome in
  sight; the first Play or step zooms to readable labels and follows the
  dots.
- Light theme by default, dark under `prefers-color-scheme`; no web font, so
  the file works offline.
- Under `prefers-reduced-motion` nothing glides, rings, trails or puffs: the
  camera jumps where it would glide, the dots land on
  their node at once and stay visible; meaning never rests on colour alone
  (`−` and `+` are written on the dots, `≠` beside the values).

## Files

Paths are relative to this file's folder.

| Path | Role |
| --- | --- |
| `scripts/build.py` | reads the spec, gets the verdicts, runs the checks, writes the page and the export |
| `scripts/runtime.html` | the page; `build.py` gives it what it shows, already formatted, and nothing else of the spec |
| `scripts/layout.py` | layered layout, top to bottom or left to right: boxes sized to their label, orthogonal edges |
| `scripts/fetch.py` | a few files of a GitHub repository, frozen at one commit, as a local repository an oracle can read |
| `examples/refund-window/` | a JS port and a before/after pair |
| `examples/free-shipping/` | a grid: two open questions, each decided on the cases it changes |
| `examples/loyalty-tier/` | an oracle on the folder's own `src/`, its glue and the fixture `--export` writes |
| `examples/payment-retry/` | an oracle running one unit alone, a stub and a mock in its glue, a loop and its passes |
| `examples/deploy-job/` | measured time: the same run over three weeks, left to right, a script averaging a fictitious CI log |
| `examples/canyon-chase/` | estimated time and two races: three plans that backfire, then a bird and a hunter past a cliff's edge, one of them falling |

Generated files (`.truepath/`, where an oracle's snapshots live, and `*.html`
next to a spec) are build output. The port examples keep their `sim.html`
so the skill can be seen without running it. The oracle examples
(`loyalty-tier`, `payment-retry`) keep none: their footer names the commit
that produced the verdicts, so the page changes with every commit, and they
build only inside a git repository that holds them.

## Limits

- One diagram type: the process flow, top to bottom or left to right.
  Sequence and architecture views are not built yet.
- Measured time is drawn for scenarios, pairs and races, not yet for a
  grid; a
  step's time is the sum of its passes, not one bar per pass.
- A step's `motion` knows one value, `fall`; a dot cannot yet hold still
  mid-edge.
- `C6` is measured on macOS (`ui-monospace`); a narrower Windows font only
  adds air.
- Steps are declared, not derived from the logic: C3 and C4 catch a wrong
  outcome, not a wrong intermediate message.
- A `series` row needs one value per step, and the logic does not know the
  steps: a list a loop builds (certificates verified one by one) is shown
  whole, `at: "last"`, unless the glue maps each pass to its step.
- `fetch.py` reads GitHub only, through `curl`; elsewhere, copy the files
  into a local git repository with an `excerpt.json` of the same shape.
