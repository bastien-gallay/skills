# Example — anatomy of the reference execution

Anonymized excerpts from the first full run (June 2026, `full` caliber: a
37-page Typst white paper auditing the author's AI-assisted development
method). The dossier itself is private; this shows the shapes the skill
produces. The reference dossier is in French — its dossier language —
excerpts are translated here.

## Dossier tree (after phase 9)

```text
2026-06-11-contre-expertise-<slug>/
├── etat.md                      # state journal + resume pointers
├── plan-action.md               # capped 3+3 action plan
├── rapport.pdf                  # compiled report (Typst, full caliber)
├── lib.typ · rapport.typ · sections/*.typ
└── notes/
    ├── 00-modele.md             # 29 falsifiable propositions P-01…P-29
    ├── 01-interview.md          # espoused vs in-use, 8 questions
    ├── a1…a6 b1…b5 c1…c6.md     # 17 research notes (3 axes)
    ├── 90-verifications.md      # 34 adversarial verdicts
    ├── 95-challenger.md         # rival-method steelman
    └── 98-contre-verification.md # the report refuted by 3 agents
```

## A proposition (phase 1)

> **P-16** — Constat: the generated tests drift to test-after despite
> directives. Fix: a 4th step **Reflect** (Red → Green → Refactor →
> Reflect): review the previous run, extract learnings, change the plan if
> needed. Claimed effects: Red respected, duplicate tests killed.

## What the interview did to it (phase 2)

> **P-16 — contradicted in use.** On ~10 recent cycles, **a minority
> (≤ 4/10)** had a real Reflect (producing a learning or a plan change).
> […] This is angle #1 of the action plan: before improving the Reflect,
> make it run.

The report had ranked this practice as its "demonstrated regime"
differentiator. One interview question inverted the report's central
diagnosis — which phase 7 then forced through every affected chapter.

## A verdict (phase 4)

> **Claim.** "<emblematic number> shows X" — Source announced: `<url>`
> **Verdict: nuanced** (expiry 2026-12) — The number is real but is a
> *motivating example, not a mean*, measured on a toy benchmark with one
> model; the prescribed reformulation restores the exact scope.

Out of 34 claims: 12 corroborated, 22 nuanced, 0 refuted, 0 not-found —
and the two summary-table rows the *report* had added from memory were
caught later, by phase 7, not by claim verification.

## An action (phase 8)

> ### 1. Make the micro Reflect actually run — instrument, then trigger `[src: <slug>/interview#P-16]`
>
> - Impact/Effort: **H / M**
> - Experiment — hypothesis: an end-of-cycle trigger raises real-Reflect
>   rate from ≤ 4/10 to ≥ 7/10 in 4 weeks · metric: per-cycle marker in
>   the daily journal · baseline: **2 weeks of counting BEFORE any
>   change** (blocking rule) · review: <date>.
