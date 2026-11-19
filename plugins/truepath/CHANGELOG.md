# Changelog

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
- After the tag `v0.1.1`, on `main` (#2, #3):
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
