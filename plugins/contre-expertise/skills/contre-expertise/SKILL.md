---
name: contre-expertise
description: >
  Critical, sourced counter-assessment ("contre-expertise") of a working
  method described by the user (articles, notes, practice README): extraction
  of the model into falsifiable propositions, author interview, multi-agent
  deep research (comparable methods, practices, cited sources), two-stage
  adversarial verification, rival method (challenger steelman), report with
  dated perishable verdicts, and a capped action plan in experimental format.
  Progresses incrementally by default (resumes from on-disk artifacts).
  Trigger: the user types /contre-expertise, asks to "audit my method",
  "critically review the way I work", "stress-test my practices against the
  state of the art", « passer ma méthode au crible », « analyse critique de ma
  façon de travailler », or wants their practice confronted with the state of
  the art without flattery.
---

# Contre-expertise — v2

> **What it is.** A for-and-against audit of a personal working method, run
> like a judicial investigation: falsifiable grid, multi-agent research,
> systematic refutation, dated verdicts, bounded action plan. The facilitator
> does not reassure — it investigates.
>
> **Output.** A dossier `<output-root>/<date>-contre-expertise-<slug>/`
> containing research notes, verifications, a report (markdown or Typst
> depending on caliber) and an action plan routable to the user's task
> system.
>
> **Language.** These instructions are in English. All deliverables (notes,
> interview, report, action plan) and all agent prompts are written in the
> **dossier language** (see rule 0.8). Artifact *filenames* are fixed
> identifiers and are never localized (see §2).

## 0. Cross-cutting rules (apply to every phase)

1. **No flattery.** Every agent and every synthesis receives the instruction
   "seek to refute, not to confirm". Positive findings are kept only when
   they serve calibration.
2. **Personal-area writes go to the main checkout.** If the output root lives
   in a gitignored personal area (e.g. a `.personal/` directory) that exists
   physically only on the main copy of the repo, always write via an absolute
   path to that main copy — never into a worktree-local clone of it, where
   the files would vanish with the worktree.
3. **No references from memory.** Every URL or quotation in the report comes
   from a note where it was obtained through a verified search/fetch. An
   expected-but-not-found source is declared not found, never invented.
4. **Mechanical traceability.** Model propositions carry `P-xx` IDs; note
   claims carry `C-<unit>-<n>` IDs (e.g. `C-a1-2`); every verdict and every
   action-plan item references its IDs. Before closing, grep-check that every
   "nuanced" or "weakened" C-id is referenced or amended in the report.
5. **Dated, perishable verdicts.** Every verdict carries its date and an
   expiry date (default: +6 months; +3 months for fast-moving benchmark
   topics). `--reflect` mode re-investigates only what is expired or
   contested.
6. **One finding, one home.** Each finding in the report has ONE owning
   chapter; other chapters link to it instead of repeating it.
7. **Cost announced before spending.** Before launching any Workflow,
   announce the number of agents and the order of magnitude of tokens for
   the chosen caliber, and get confirmation (unless the caliber was passed
   explicitly as an argument).
8. **Dossier language.** Default: the dominant language of the corpus.
   Override with `lang:`. The verdict palette, section headings *inside*
   deliverables, interview questions and agent instructions are all rendered
   in that language — consistently across the whole dossier. Canonical
   verdict palette (localize as needed, keep one rendering per dossier):
   `corroborated / nuanced / weakened / refuted / not-found`
   (French rendering used by the reference execution: corroborée / nuancée /
   fragilisée / réfutée / introuvable).
9. **Corpus stratification — published vs unpublished.** At framing, tag
   every corpus piece `published` or `unpublished` (drafts, seeds, hidden
   /lab pages, private notes) and record the tags in `etat.md`. Propositions
   sourced *only* from unpublished material carry the tag through the grid,
   the report and the action plan, and may only be criticized
   **prospectively** ("what must not ship as-is") with an explicit
   disclaimer — never levelled with public claims. The author has not
   committed to a draft; a draft that carries unsourced material *and says
   so* is the drafting process working, not a fault of the method. The
   report names ONE owning chapter for this disclaimer (rule 0.6) and
   recalls the status at every mention.

## 1. Inputs and framing (phase 0)

Accepted arguments (all optional, ask for what is missing):

- `corpus:` paths of the texts describing the method (articles, notes,
  README).
- `slug:` short dossier name (otherwise derive it from the subject).
- `calibre:` `light` | `standard` | `full` (French aliases `leger`,
  `complet` accepted) — see §3.
- `lang:` language of all deliverables (default: corpus language).
- `out:` output root. Default resolution: `.personal/research/` if such a
  personal research area exists in the repo; otherwise `docs/contre-expertise/`;
  otherwise ask.
- `--overwrite`: disables incremental mode (see §2).
- `--reflect`: re-run/diff mode (see §8).

Framing: read the corpus, restate in one sentence what is being audited and
for which decision (publish? improve? settle a debate?). Tag every corpus
piece published / unpublished (rule 0.9). If the caliber is missing, ask via
AskUserQuestion with the costs alongside each option. Create the dossier and
initialize `etat.md` from `templates/etat.md`: framing decisions, caliber,
language, corpus tags, planned unit list, timestamp.

## 2. Incremental mode (default) and `--overwrite`

**The skill resumes where it stopped.** The truth about progress lives on
disk, not in session memory:

| Phase | Completion artifact |
| --- | --- |
| 1 Extraction | `notes/00-modele.md` |
| 2 Interview | `notes/01-interview.md` |
| 3 Research | every note listed in `etat.md` § units |
| 4 Verification | `notes/90-verifications.md` |
| 5 Challenger | `notes/95-challenger.md` |
| 6 Report | `rapport.md` or compiled `rapport.pdf` |
| 7 Counter-verification | `notes/98-contre-verification.md` + "corrections integrated" marker in `etat.md` |
| 8 Action plan | `plan-action.md` |
| 9 Closing | "closed" marker + commit hash in `etat.md` |

Artifact filenames are **fixed identifiers** — do not translate them, even
when the dossier language is not French (glossary: `etat` = state journal,
`modele` = model grid, `verifications` = claim verdicts, `rapport` = report,
`plan-action` = action plan). Renaming them breaks resume.

On invocation: if the slug's dossier exists, list the artifacts present,
announce the resume point ("phases 1-3 done, resuming at phase 4") and
continue. An upstream phase modified by hand invalidates downstream phases:
flag it and offer to re-run. Phase 3 special case: if a Workflow `runId` is
recorded in `etat.md` and notes are missing, relaunch with `resumeFromRunId`
— completed units return from cache.

**Adopting a pre-existing dossier** (validated on the reference execution):
when pointed at a dossier created *before* this skill existed, reconstruct
`etat.md` a posteriori — map existing artifacts to phases in a
correspondence table (including artifacts under other names, e.g. a compiled
white paper standing in for `rapport.pdf`), note which conventions are
missing (e.g. claims without C-ids, and the fallback trace format to use),
then resume at the first missing phase. Late phases run on a pre-existing
dossier are *more* adversarial, not less: a fresh interview or
counter-verification acts as new evidence against the existing report.

**`--overwrite`**: NEVER delete — rename the existing dossier to
`<dossier>.bak-<date>` then start clean. Tell the user about the rename.

## 3. Calibers

| Caliber | Research units | Verification | Deliverable | Order of magnitude |
| --- | --- | --- | --- | --- |
| `light` | ~5 (1-2 per axis) | 1 claim/note, 1 vote | 3-5 page markdown note + plan | ~15 agents |
| `standard` | ~10 | 2 claims/note, 1 vote | ~15 page Typst report + plan | ~30 agents |
| `full` | ~17 | 2 claims/note + extended counter-verification | 30+ page Typst white paper + plan | ~50 agents, >2.5M sub-agent tokens |

In `light` and `standard`: divergence tables rather than state-of-the-art
prose, appendices by reference to the notes (no duplication), generated
bibliography. `full` is reserved for founding audits.

**Per-phase sizing.** The caliber may differ per phase — typically when
resuming a `full` dossier where only late phases remain: run the remaining
phases `light` (e.g. 3 counter-verification agents instead of 6). Record the
decision in `etat.md`.

## 4. The phases

### Phase 1 — Model extraction

Reconstruct the method as **numbered falsifiable propositions** `P-xx`
(15-30 items: practices, beliefs, measurement choices), followed by a
section "self-inconsistencies to investigate" (where the corpus contradicts
itself or exempts itself from its own rules). Template:
`templates/grille-modele.md`. This is the backbone of everything else — get
the granularity right: one proposition = one refutable thing. Propositions
sourced only from unpublished corpus pieces carry the tag from rule 0.9 on
their grid line.

### Phase 2 — Interview (espoused theory vs theory-in-use)

The corpus describes what the author *says* they do. Before judging, ask
5-10 targeted questions (AskUserQuestion, batches of 4 max) such as: "the
last time you skipped P-08, what was the context?", "P-14: how often,
really?". Then mark each P-xx: `espoused` / `confirmed in use` /
`contradicted in use` — and record the concrete examples given. The
"contradicted in use" propositions become priority investigation angles.
Output: `notes/01-interview.md`.

Run this phase even when adopting a dossier whose report already exists —
the reference execution showed the interview can invert a report's central
diagnosis (there: which feedback loop was actually the weak one).

### Phase 3 — Multi-agent deep research

Launch a Workflow (invoking this skill counts as the explicit opt-in) built
from `templates/workflow-recherche.js`. Three axes of units, sized by
caliber:

- **Axis A — comparable methods**: practitioners and institutions who have
  published a workflow on the same subject.
- **Axis B — practices in detail**: each differentiating practice of the
  model, investigated against the literature (demonstrated / plausible /
  contradicted mechanism).
- **Axis C — corpus sources**: every source the author cites,
  counter-checked (what does it actually say, who disputes it, is the usage
  faithful).

Mandatory shared instructions in every unit prompt:

1. For AND against — do not flatter.
2. **Actively search for failure cases** of each method/practice, not only
   its promoters (the visibility bias of celebrity practitioners is
   documented — reference execution, note a3).
3. **At least one search in a non-English language** relevant to the corpus
   (or another pertinent language) per unit when the topic lends itself.
4. Note written to disk (`notes/<unit>.md`, template
   `templates/fiche-recherche.md`), compact structured return (summary +
   claims).
5. Terminal claims with `C-<unit>-<n>` IDs and source URL.
6. All note content in the dossier language.

Record the `runId` in `etat.md` as soon as the launch happens (resume).

### Phase 4 — Adversarial claim verification

For each claim: one agent tasked with **refuting** it (primary source
required). Verdicts from the palette of rule 0.8, each with an expiry date.
Output: `notes/90-verifications.md` (generated clean: headings without
trailing punctuation, URLs in `<>`). Then **propagate**: every nuance or
correction is carried into the affected notes or recorded as a fix to apply
in phase 6 — propagation is checked via the C-ids (rule 0.4).

### Phase 5 — Challenger

Build the **steelman of a rival method** from the notes: the best coherent
alternative (not a strawman), with choices opposed to the most structuring
P-xx. Confront it head-on: in which contexts does the challenger win? What
would you borrow? Output: `notes/95-challenger.md`. This is the antidote to
the comfort of comparing against a scattered field. If the interview
(phase 2) exposed propositions contradicted in use, aim the challenger's
strongest attack exactly there.

### Phase 6 — Report

Target structure (compress by caliber): executive summary · reconstructed
model · state of the art (divergence tables) · practices in detail · gap
analysis (shared base / extra / missing / inverted gaps) · critique of the
comparison points (n=1, survivorship bias, unmeasured comparators, context
asymmetries) · sources: verdicts by status · critique of the fundamentals
(verdict boxes: solid / fragile / critical) · **economics of the method**
(cost/benefit table per practice: time, tokens, what it catches — even
rough, never omitted) · challenger · action plan (pointer) · bibliography.

Writing rules: verdicts referenced by C-ids; one finding = one home (rule
0.6); critiques of propositions from unpublished material framed
prospectively, with the rule-0.9 disclaimer owned by one chapter; the
bibliography is **generated from the notes** (script or extraction), never
written from memory; in Typst, reuse the layout from a previous execution
when one exists.

### Phase 7 — Counter-verification of the report

The stage the first execution had skipped: note claims were verified, the
document's conclusions were not. Launch 3-6 agents (by caliber) tasked with
**refuting the report's own verdicts and syntheses** (each verdict box, the
executive summary, the gap analysis — and every lead-in sentence that
attributes a finding to an actor: "the author cites X" is grep-checkable
against the corpus), with access to the notes. Integrate
the corrections, trace them in `notes/98-contre-verification.md`, set the
"corrections integrated" marker in `etat.md`. A report that preaches
non-exemption must apply it to itself.

Integration pairing (validated on the reference execution): the ideal
corrector for perimeter X is the agent that counter-verified X (context
already loaded — continue it if the harness allows); otherwise spawn fresh
correctors per perimeter, passing them the findings verbatim plus your
orchestration arbitrations, with disjoint file perimeters so they can run in
parallel. Recompile/lint after integration; the orchestrator spot-checks the
most rewritten pages.

What this stage catches that claim verification cannot: verdicts placed
from memory in summary tables, prescribed reformulations never propagated
into the text, source misattributions between notes.

### Phase 8 — Action plan

The landing deliverable — template `templates/plan-action.md`:

1. **Scoring first**: for each candidate action, start with "what existing
   thing does this overlap?" (eliminates duplicates with what the user
   already does — including work the user has explicitly taken on
   elsewhere), then Impact/Effort.
2. **Hard cap**: 3 "now" actions + 3 "this month"; everything else goes to a
   dated backlog. An inventory is not a plan.
3. **Experimental format mandatory** for any experiment-type action:
   hypothesis · metric · baseline command · duration · review date.
   **Blocking rule: no experiment is emitted without a baseline step.**
4. **Task routing**: end the file with a "to route" section of preformatted
   one-line items, each prefixed with its trace `[src: <slug>/C-xx]`. The
   user routes them into their task system; review dates are listed
   separately for scheduling. Routing adapters, in order of preference:
   - **daily-ops** (if installed): route via `/do-add` (today's block or
     drop-in buffer). <!-- See "Future improvements" comment below. -->
   - **fallback**: paste the checklist into the project's TODO file, or
     leave it in `plan-action.md` as the canonical copy.

<!--
FUTURE IMPROVEMENTS — daily-ops adapter (issues opened 2026-06-12 on
bastien-gallay/daily-ops):
- #31 (--due dates): route "this month" items and review dates with their
  deadline instead of a separate list.
- #32 (plan import + provenance tags): replace the "to route" section with
  `daily-ops plan import plan-action.md` — idempotent bulk import, the
  [src: …] tag becomes native and survives carry-overs.
- #33 (report --json + carry counts): --reflect queries daily-ops
  mechanically ("which actions tagged src:<slug> are done / zombies?")
  instead of asking the user.
- #34 (experiment blocks lifecycle): emit experiments as `experiment` blocks
  with metadata carried by daily-ops.
- #35 (per-stream cadence): route experiments to an `experiments` stream
  surfaced at review dates.
- #36 (persistent item IDs): C-id → item traceability survives rewording.
- #37 (headless mode): routing no longer depends on the day's /do-sod.
-->

### Phase 9 — Closing

1. `markdownlint` on all notes (project config); compile the report; visual
   check of a few pages if Typst.
2. Console recap in 3 bullet blocks: *now* / *next* / *open decisions* —
   located (file, §), no prose.
3. Offer to commit the dossier in its repo (ask before any out-of-sandbox
   commit, unless a session-wide authorization exists).
4. Offer to schedule the J+30 review, quoting the date written in
   `plan-action.md`. If the review is scheduled on a headless/cloud runner,
   adapt: the runner does the mechanical parts (data harvest, re-instruction
   of expired/weakened verdicts, verdict diff, draft plan) and leaves the
   interview questions in the deliverable for the author; it commits on a
   branch, never on the main branch.

## 8. `--reflect` mode (J+30 re-run)

Input: the dossier of a closed contre-expertise. Short pass, no full
fan-out:

1. Read `etat.md`, `plan-action.md`, `notes/90-verifications.md`.
2. Ask the user the fate of each "now" / "this month" action (done / in
   progress / abandoned / zombie) and the baseline metric values.
   <!-- future: replaced by daily-ops report, issue #33 -->
3. Re-investigate ONLY: expired verdicts (past expiry date), `weakened`
   claims, and experiment hypotheses whose measurements have arrived (1
   agent per item, no full fan-out).
4. Produce `reflect-<date>.md`: verdict diff (moved / stable / expired
   not re-checked), experiment results, re-prioritized action plan (same
   caps).

## 9. Known pitfalls (from the reference executions)

- Verifying note claims does NOT verify the report: never skip phase 7. It
  catches from-memory verdicts in summary tables, unpropagated prescribed
  reformulations, and cross-note misattributions — none of which the C-id
  grep can see.
- "Emblematic" numbers in notes are often motivating examples, not means —
  report the exact scope (cf. the 100%/4% mutation-score case and the
  Scott Logic line counts in the reference execution).
- Citation chains break (cf. the "2.74×" case): always climb back to the
  primary source before reusing a number.
- Generate `90-verifications.md` lint-clean from the start rather than
  fixing it afterwards.
- Don't let action lists swell: the phase 8 cap is a rule, not a
  suggestion.
- A superlative ("the only one", "nobody else") is an existential claim
  beyond any finite corpus — write "no source in the corpus documents…"
  instead.
- When phases run out of nominal order (interview after the report), treat
  the late phase's findings as new evidence against the existing artifacts
  and re-derive what they invalidate — don't bolt them on as a footnote.
- **Verify lead-in attributions, not just verdicts.** Counter-verification
  (phase 7) naturally checks facts and verdict boxes; it misses framing
  sentences that attribute a finding to the wrong actor ("an example
  internal to the corpus" when the evidence came from the research notes
  and the trap threatens the report itself). For every "the author
  does/cites X" sentence, grep the corpus before letting it stand.
- **Never level published and unpublished material.** Criticizing a
  draft's unsourced numbers as if they were public claims is unfair twice
  over: the author hasn't committed to them, and a draft that flags its own
  gaps is the drafting process working. Rule 0.9 exists because the
  reference execution got this wrong (a seed-only proposition criticized at
  the same level as published claims, caught by the author, not by
  phase 7).
