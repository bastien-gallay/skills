# Changelog

## Unreleased

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
