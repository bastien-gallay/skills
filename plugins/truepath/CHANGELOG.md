# Changelog

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
