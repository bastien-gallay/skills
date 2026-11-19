# Product

## Register

product

## Users

- A developer reviewing a merge request: where do before and after diverge,
  which piece of code decides.
- A developer analysing a bug to fix it: follow the real path of one case.
- A product owner or business expert in a workshop, the page projected,
  deciding a rule; little reading of detail.
- Support or ops explaining a real case to a third party.
- An engineer giving a technical presentation.

## Product Purpose

truepath turns a process, a bug path or a rule under discussion into one
self-contained HTML page: a dot walks the real path through the graph, a
data panel shows what changes at each step, and scenarios play side by side
with their first difference marked. The verdicts come from the repository's
own code. Success: a reader who did not write the spec understands, in under
a minute, which case goes where and why, without reading the detail.

## Brand Personality

Pedagogical, alive, trustworthy. The page tells the path as a short story
in motion; the motion carries the explanation, the text only labels it.

## Anti-references

- Dense technical documentation where the picture is an afterthought.
- SaaS dashboards: hero metrics, card grids, decoration.
- Slides where text carries what the animation should show.

## Design Principles

1. Show, don't tell: the moving dot and the diff carry the meaning; prose
   is a caption, never a paragraph.
2. One glance links everything: matrix, graph and scenarios read as one
   object, a cell maps visibly to its path.
3. Time on screen follows importance: the dot spends time where the
   decision is, not where the drawing is long.
4. Proof is visible: every verdict shows where it came from.
5. Controls sit where the eye already is.

## Accessibility & Inclusion

WCAG 2.2 AA: contrast, full keyboard use, visible focus. Every animation
honours `prefers-reduced-motion`. Meaning never relies on colour alone.
