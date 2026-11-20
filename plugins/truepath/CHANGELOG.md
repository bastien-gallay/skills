# Changelog

## 0.3.2

From watching the race again: the fastest dot was lost before it arrived.

- A step with no time of its own (a decision, the run into an outcome)
  shares the time of the timed step next to it: a dot glides into its
  outcome instead of jumping down a long edge in a blink, and arrives on
  the clock at its measured time (`/kill` at 2.5 s, not 2.8 s).
- A dot that has just arrived stays framed, ahead of the leader, while its
  landing plays, then the camera goes back to the race.
- The race's camera moves far less: it frames the edge each dot is on, not
  the dot itself, so a loop that comes and goes no longer pumps the zoom;
  it zooms out at once when it must, back in only for a real gain, pans
  only when a way leaves the frame, and leaves the whole field for the
  leader alone, and back, with a margin either way. The zoom glides slower
  than the pan. In the drowning-against-fall race, the zoom now turns
  round once, where it breathed with every pass of the loop.

## 0.3.1

From watching the first race: the camera lost the leader, the dots
arrived without a sound, and a timed run looked like any other. Every
existing spec builds as before.

- A race's camera keeps the leader in sight: it frames every running dot,
  zooming out no further than readable labels, then follows the leader
  alone, closer, when they no longer fit. A pan or a zoom by hand still
  takes the view until Play or *Fit*.
- The race's clock slows into each arrival and holds a moment on it, for
  every dot alike; on any page, the hop into an outcome slows at its end.
- On a timed page (a `measure`, measured or estimated), a short comet
  trails each dot; it fades once the dot has arrived.
- An arrival rings out of the dot and pulses twice round the outcome's
  box. None of this moves under reduced motion.
- A panel row reading a measured time rounds it as its bar does: `32.65`
  read `32.6` in the panel and `32.7` on the bar.

## 0.3.0

A new kind of tab, the race (story S37): three ways to the same end,
compared on how long each takes, could be read one tab at a time, or two by
two as a pair that marked every step as a divergence. Every existing spec
builds as before.

- `races: [{scenarios, tab, summary}]` runs 2 to 4 scenarios at once on one
  graph, a numbered dot each, in its own colour; each scenario keeps its
  own tab, and nothing is compared: no `≠`. The panel has a column per
  side, the summary the order of arrival.
- With a measure for each side, measured or estimated, the race runs on
  one clock: each step lasts the time of the nodes it reaches, a node a
  loop reaches twice sharing its time between its visits, so the fastest
  way arrives first and the slowest after twelve seconds at 1×. A clock
  runs above the graph, each bar fills in its dot's colour, and the step
  list tells each arrival. Without a measure, the dots take a step
  together.
- Dots on one point sit side by side, however many there are.
- A pair's panel names its two sides by their tabs, not *before* and
  *after*: a pair is not always a fix.
- C14 counts a text as the page shows it: code marks do not count, an
  escaped backtick does.
- The README's status links the tag it names.

## 0.2.5

From three ways to the same end, compared on how long each takes, with
nothing to run: the reply drew a bar chart beside the flow, and that chart
said what the page did not. Every existing spec builds as before.

- The bars run as the graph does: upright beside a top-to-bottom graph,
  each case's steps stacked down in path order, its total above it; under
  a left-to-right one, as before. Ways that share few steps compare by
  height at a glance; the page showed each way's time only in its own tab.
- `measure.source: "estimate"` draws times worked out from a model of each
  step, when nothing can run: no `n`, no `stat`, and the page says
  *estimated* where it says *measured*, a panel row marked `≈ estimated`.
  An estimate read as `◇ definition` before.
- `≠` no longer marks a bar that shares no step with the first: another
  way is not a change.
- A short loop whose two ends lead their rows climbs on the left when
  boxes stand on their right: around them, it seemed to frame the next
  column. Its name and pass badges sit together, left of its lane.

## 0.2.4

From an agent, alone with the skill, timing a full reload of a board
companion on two workspaces: one straight path, its time moving with the
size of a journal. Every existing spec builds as before.

- The shape table no longer sends every timed run to a page: when every
  case walks the same straight path, the dot says nothing the rows do not,
  and the answer is a table. A page is for timed runs whose path explains
  the time: a step one case skips, a loop that turns more often.
- SKILL.md asks to measure where the reader meets the time: a reload is
  felt in the browser, which grows with the data more than the server
  does. A measure that stops earlier says so in its basis and asks it as a
  doubt.
- With `median`, C16 says that the steps' medians need not add up to the
  median run, and how to set `tolerance`; it spoke of a missing step.
- A bar no longer runs past its total: each segment kept a few pixels of
  padding however short it was, and nine of them pushed `≠` over `82.3 ms`.
  A name cut short ends with an ellipsis.
- A panel row reading a measured time shows it as its bar does, rounded
  and with its unit (`82.3 ms`, not `82.26`).
- A basis starting with `mesure :` no longer reads `mesuré : mesure :` in
  the footer; an oracle whose `ref` is a sha names it once.
- SKILL.md: with no one to ask about the view, pick one and offer the
  other in `views`; a warm-up run goes in `excluded`; `failed` is left out
  when no run failed.

## 0.2.3

From a first measured run on a real CI job, three days of a deploy whose
image stopped installing its tools, and whose plan grew with the work
applied. Every existing spec builds as before.

- `measure.compare` names the steps whose time compares from one case to
  the next: `≠` marked the plan, which grew with the work applied that day,
  and missed the install step the image had dropped. A step gone from a
  bar now takes the mark too, outlined in the first bar where it was.
- `excluded: [{n, why}]` in a measure says which runs were left out for
  another reason than a failure: runs with nothing to apply read as failed.
  The row says *hors calcul : 1 sans couche*, without an agreement to get
  wrong.
- A diagram drawn left to right grows taller when it zooms to readable
  labels, up to the room left on screen: it kept its thin strip, and the
  branches above and below the path ran off it. *Fit* gives the strip back.
- A timeline segment too narrow for its name shows none: a few letters
  said nothing. The name stays on hover.
- SKILL.md asks for a measure's basis in the page's language, and says
  where the paths of its *Files* table start.

## 0.2.2

Measured time (story S35), asked for by a CI job that walked the same steps
every week while its time moved. Every existing spec builds as before.

- `measure` runs a command that reads real runs and gives each scenario
  its time per node, the number of runs it sums up (`mean` or `median`),
  the failed runs left out and its basis. The page draws one bar per case
  under the graph, on one scale: the dot's node is filled in every bar,
  `≠` outlines the step that moved most from the first bar, and a click
  on a segment opens its case on that step. A panel row may read
  `measure.total`, marked `◉ measured`.
- C16 refuses steps that do not add up to the total, C17 a time on a node
  the path does not reach, C18 a measure without its total, its number of
  runs or its basis.
- The shape table no longer sends a timed run to a plain table: the same
  path, timed per step, is a page.
- `examples/deploy-job/`: the same deploy over three weeks, its tools
  installed by every run, then twelve modules planned each time, then two.

## 0.2.1

The view, chosen apart from the shape (stories S33–S34): a case drawn left
to right, and a switch between views when the spec offers both. Every
existing spec builds as before.

- `view: "flow-lr"` lays the ranks out left to right: the same layout on
  boxes turned a quarter, then turned back. A branch's name sits on the run
  entering its target, after a rail kept close to the source, and each gap
  is as wide as the names entering it, plus room for pass badges only
  where a loop comes back. Loops run under the drawing.
- `views` offers other views beside the zoom (`↓` `→`, or the key `V`):
  the page draws the same case again on the same step.
- SKILL.md picks the view from the question, after the shape, and asks
  the user when two fit.

## 0.2.0

From a design critique of a first real grid (`docs/design/story-map.md`,
stories S10–S13), then a second critique (S22–S27), then a first loop, a
line-by-line file parser (S28–S31).

- A loop leaving a box with neighbours on its right runs under their row,
  each loop in a corridor of its own, before it climbs: at mid-height it ran
  through the boxes beside it and seemed to chain them.
- A step may run through a node without stopping: `hop: [from, via…, to]`.
  A loop's return was a step of its own that said nothing new, and doubled
  the reading; one line of the parser is now one step. The dot takes the
  time of each edge it runs.
- The first divergence of a pair is also where the paths fork, on the last
  node both share: two parser runs that part at line 3 were marked only at
  the verdict, where the panel values first differ.
- A panel row may change step by step: `series: true` on a row whose value
  is a list, one value per step from `at`. A parser's open work grows line
  by line; one value per row showed only where it ended.
- A pair's `compared` row (the fix, the rule) is no longer marked `≠`: it
  differs by design, and the mark pointed at it as an effect.

From a first run on a project the author does not build: an excerpt of a
public repository, its unit run alone.

- The oracle runs the unit by default, the way a unit test does: one
  function or module, unchanged, its collaborators replaced by doubles that
  answer what the scenario says. `oracle.doubles` lists them, `{name, kind:
  stub|fake|mock, replaces}`, and the footer names them; glue brought by
  `files` without that list is refused.
- `scripts/fetch.py` lists a GitHub repository's paths and fetches a few
  files at one commit into a local git repository, with an `excerpt.json`
  naming their origin. The footer then names the upstream commit, not the
  local one that holds the copy.
- `doubts`: what the author was unsure of is asked before building, the
  strongest first, and the answer kept in the spec. C15 refuses a scenario
  resting on an unanswered doubt, unless it is `undecided`.

From a second run on that project, by an agent that had only the skill,
and from the author driving the page.

- A loop's order is written where it branches: on a node a path passes more
  than once, each branch leaving it gets a numbered badge per pass, set once
  the dot took it. `① ②` on *timeout*, `③` on *ok*: the third try got
  through. More than three passes on one branch read as a range and the
  last. A badge names its step on hover or focus; a click or `Enter` goes
  there.
- Keys work wherever the focus is: `Space` on a tab played nothing, it
  reopened the tab. `Home` `End` reach the first and last step; on the tab
  row `↑` `↓` change tab, and `1`…`9` open a tab.
- `build.py --check` runs the checks that need no verdict, without the
  logic, and writes nothing: doubts are asked before the first build, and
  a slow oracle no longer stands between a spec and its typos.
- A panel row may appear `at: "last"`, each scenario's own last step: a
  result row appeared too early in the longer scenarios.
- A `double: …` basis is marked `◌ double`, apart from a definition; the
  footer counts only the excerpt's files the oracle runs, not those
  fetched to be read; `TRUEPATH_SPEC_DIR` points the oracle to the spec's
  folder, where a dependency cache lives.
- A long value wraps inside the panel instead of running past its edge;
  the `≠` key is shown only on a page that compares two sides.
- `examples/payment-retry/`: a unit run alone, a stub and a mock in its
  glue, a retry loop and its passes.

From a third run, the agent again with only the skill, on a loop of three
passes.

- A pass badge sits after its branch's label (*parent returned* `①②③`):
  set at the end of the edge, it read as the next node's. A click on it now
  goes to its step: the pan gesture captured the pointer and swallowed the
  click. The diagram is a group, not an image, so a screen reader reaches
  the badges, which are buttons.
- `--check` prints an open doubt as a question to ask (`?`), not a
  violation; `--dry-run` runs the logic and every check, and writes
  nothing; a doubt may hold what was `assumed` instead of asked.
- `$TRUEPATH_SPEC_DIR` in `oracle.cmd` is replaced by the spec's folder,
  since the command runs without a shell; `files` are copied as bytes.
- A null on a panel row's way (`inputs.a.b`, `a` null) reads as null; two
  edges between the same nodes are refused, where the second silently
  replaced the first in the drawing.

- A matrix cell says how its case ends, the outcome's label beside its
  colour, then the value: `rien` read the same for a value lost, dropped on
  purpose, or lost again. The highlight of a split case is gone; `≠` is the
  only mark of change. The cell legend is a line of short keys.
- A case opens on the whole graph, the fork and both outcomes in sight and
  outlined; the readable zoom waits for the first Play or step, and is
  measured again when the window changes size.
- Keyboard: the focus stays on a cell picked with Enter, is drawn dashed so
  it never looks like a picked side, and Escape goes back to the matrix on
  the cell the case came from. Steps are buttons. The row says on screen
  that Shift picks `−`. Table headers carry `scope`. A change of the
  reduced-motion setting applies without a reload.
- The matrix hint is a muted caption, quieter than the verdict above it; a
  grid case's panel no longer repeats the answer its row already shows.

- C14 refuses a text over its budget: a subtitle over 90 characters, a
  summary over 110, a caption over 70, a step message over 40. `SKILL.md`
  says why under *Text budget*. A spec whose texts are longer no longer
  builds; shorten it, or move the detail into `source` or a `basis`.
- Prose stops at 75 characters a line: the subtitle, the summary, the
  matrix hint and the cell legend under it.
- Every hop takes the same time (0.65 s), however long it is drawn; the
  dot stays 1.7 s on a decision, the first divergence or an outcome, and
  0.45 s where it only passes. A long edge drawn around a box held the dot
  for 9 s, half the playback, on a step that decided nothing.
- An edge that would cross a box steps aside just past the boxes in its
  way, on the nearer side, instead of running around the whole drawing.
- The matrix has the graph beside it: the cell under the pointer or the
  focus lights its path, the first case where the answers disagree lit
  when the page opens.
- An open grid case keeps its row of the matrix above the diagrams, the
  compared cells marked `−` and `+`; a click on another cell compares it.
- Two sides compared (a pair, a grid case) walk one full-size graph, a dot
  each marked `−` and `+`; an edge only one side takes is drawn in that
  side's colour, so the divergence is a fork in one drawing. Two
  half-width diagrams drew node labels at 5px on a laptop.
- The case's diagram takes the height left below what sits above it; step
  by step, a view whose labels would be under 12px zooms to 12px and
  follows the dots. *Fit* and the overview show the whole graph.
- A straight edge's label sits below the junction it leaves from, on the
  part only that edge draws.
- Play, steps, speed and zoom sit under the diagram, with the keys that
  drive them; the bar at the top keeps only the tabs, or the way back to
  the matrix.
- The two rows of variant buttons are gone: in a grid case, the case's row
  picks both sides (click for `+`, Shift + click for `−`).
- The step list no longer tells what is still to come: a step reads once
  the dot has reached it.
- Projected at 1280×720, a grid case keeps its controls and its current
  step on screen: the way back to the matrix sits beside the case's row,
  the bar above goes, the origin takes one line (in full on hover), and
  the side panel scrolls within the screen, following the current step.
- The overview keeps the step's caption under the graph.
- Under reduced motion the dots no longer vanish: they land on their node
  at once, so the path is not told by edge colour alone. Boxes off the
  path stay readable.
- The values a matrix cell shows on hover are also said in words under
  the graph beside it, for the pointer and the keyboard focus alike.
- French page words keep `«` and `»` with their word, and `:` with the
  word before it.
- Where a value comes from is said once, under its table (`✓ code`,
  `⚠ ported`, `◇ definition`); a value keeps its glyph only when the
  table mixes several. The full text stays on hover.

## 0.1.2

Issues #2 and #3, and what a first use on a real repository showed.

- A matrix cell reads as clickable: a hint above the table says what a
  click opens, each cell carries a chevron, takes a ring on hover or
  focus, and is a button reachable by Tab and opened by Enter or Space;
  the first changed cell rings twice, not under reduced motion. On a
  narrow screen the table scrolls inside its card, never the page.
- The footer ends with *made with truepath* (*créé avec truepath*), a
  plain link; `"credit": false` in the spec removes it.
- `` `x` `` in spec text is shown as code; `` \` `` keeps a backtick.
  Tooltips, tabs and the `<title>` drop the backticks.
- A scenario played in a pair has no tab of its own: five pairs made
  fifteen tabs, ten of them half of a pair. `refund-window` opens on its
  one pair.
- `SKILL.md` opens on *First, the shape*: more than two pairs between the
  same two versions is a grid, and a comparison where every case walks
  the same path is a table, not a page.
- What `oracle.files` brings is named in the footer after the ref, so code
  from the spec is no longer shown as the ref's code.
- The README opens on the grid in motion; both pictures are retaken.

## 0.1.1

- The page opens paused; the play button is green until it is pressed, so
  the first click is obvious.
- The diagram zooms (`−`, `+`, *Fit*, Ctrl/Cmd + wheel, pinch, keys `+`,
  `-`, `0`) and pans by drag or wheel once zoomed; a pair zooms as one.
  Zoomed in, the view glides after the moving dot; a pan stops that, Play
  or *Fit* resumes it.
- A pair may have two scenarios of different lengths: the shorter stays on
  its outcome while the other goes on. C8 now refuses only a pair naming an
  unknown scenario. Every spec that built still builds.

## 0.1.0

- First version: scenarios, before/after pairs, the questions grid, oracle
  and port logic, checks C1–C13, English and French page words, its own
  layered layout.
- A verdict must carry an `outcome`: without one, nothing tied the path to
  the logic and the build passed by default.
- Spec text is shown as text: it can no longer close the page's script or
  be read as HTML.
- A spec that cannot be read is refused in plain words, not by a traceback.
- The oracle reads `TRUEPATH_ORACLE_IN` and writes `TRUEPATH_ORACLE_OUT`;
  its snapshots live in `.truepath/`.
- The spec says what things are: `port`, `subtitle`, `message`, `labels`,
  `digits`, `compared`, `undecided`, pairs of `before` and `after`, grid
  `cases`, `show` and `hover`. A node declares `role: "decision"`; where a
  path starts is found, not declared.
- The page receives what it shows, already formatted, and nothing else:
  no inputs, no expectations, no oracle settings.
- Two more examples: `free-shipping` (a questions grid) and `loyalty-tier`
  (an oracle on committed code, with its exported fixture).
- The played path is drawn over the edges it shares a stub with; the matrix
  no longer shows an empty toolbar.
- A `basis` is read by the word before its colon; a failed export writes
  no page; reduced motion stops the steps from advancing by themselves.
- After the tag `v0.1.0`, on `main`: the README shows the grid in motion and
  CI runs `ruff check`. The skill behaves the same.
