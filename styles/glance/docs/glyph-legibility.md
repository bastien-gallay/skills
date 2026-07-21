# Glyph legibility — human test record

Record of what was tested on a real terminal, at the maintainer's own
font and size. Everything here comes from human judgement, not from a
model. It is the most reliable evidence in this repo.

Date: 2026-07-21

## Verdict: rejected

Circled and enclosed digits, all five variants tested:

| variant | sample | verdict |
| --- | --- | --- |
| thin circled | ① ② ③ | very hard to read |
| filled circled | ❶ ❷ ❸ | very hard to read |
| double circled | ⓵ ⓶ ⓷ | very hard to read |
| arrow circled | ➀ ➁ ➂ | very hard to read |
| arrow filled | ➊ ➋ ➌ | very hard to read |

The filled variants failing alongside the thin ones rules out contrast
as the cause. The enclosure itself is the problem: it shrinks the
useful glyph to a fraction of the cell, leaving too few pixels to tell
a 3 from an 8. Hence a class ban rather than a weight constraint.

Enforced by the "never use circled or enclosed alphanumerics" rule in
`prompt.md`.

## Verdict: allowed

The closed emoji set now named in `prompt.md`:

    ✅ ❌ ⚠️ 🎯 📊 🔍 →

## Verdict: tolerated, never encouraged

Enclosed alphabetics — `Ⓐ ⓐ ⓘ`. Reported as "hard but acceptable".
Not worth proposing as a scanning device; no reason to hunt them down
when quoted from a source.

## Verdict: fine, no action

Reported as causing no trouble:

| class | sample |
| --- | --- |
| box drawing | `└ │ ├ ┐ ┌ ┘ ─ ═` |
| math and arrows | `≥ ≤ ≠ × ± → ← ↔` |
| small geometric | `· ▸ ● ○ ▶ ▼ — –` |

## Untested — candidates for the next pass

Fine-detail glyphs, never put in front of a human:

| class | sample | why it is a risk |
| --- | --- | --- |
| check marks | `✓ ✔ ✗ ✘ ☑ ☒` | distinguishing detail is a few pixels |
| fine bullets | `‣ ▪ ▫ ◦ ⁃ ∙ ⋅` | near-identical to each other |
| super/subscript | `¹ ² ³ ₁ ₂ ₃` | rendered below body size |
| keyboard | `⌥ ⌘ ⇧ ⇥ ⎋ ⏎` | dense internal structure |
| continuation | `↳ ⤷ ⮑ ⌐ ⌁` | rare, low familiarity |
| alert | `‼ ⁇ ⁈ ⚑ ⚐` | two-glyph forms crowd |

## Separate concern: column width

`1️⃣` (emoji keycap) and `🄰 🅐` occupy two terminal columns. Even where
legible, they break table alignment and ASCII diagrams. This is a
layout argument, independent of legibility, and on its own is enough
to keep them out.

## Method note

An automated census over 30 generated responses never emitted a single
circled digit — the class the maintainer reported as the actual
problem. Corpus-driven glyph selection would have missed it entirely.
Ask the human.
