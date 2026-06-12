# Changelog

## 2.0.0 — 2026-06-12

Internationalization and genericization, after the first full field run
(incremental resume on the pre-existing reference dossier).

- SKILL.md and all templates rewritten in English (canonical); new `lang:`
  argument — all deliverables and agent prompts are produced in the dossier
  language (default: corpus language). Artifact filenames stay fixed
  identifiers.
- New `out:` argument — output root no longer hardwired to
  `.personal/research/`.
- Task routing generalized: the "to route" checklist is the universal
  output; daily-ops becomes an optional adapter (`/do-add`), with the
  planned deeper integration kept as comments (daily-ops#31–#37).
- Lessons from the first execution folded in: per-phase caliber sizing
  (§3), adopting a pre-existing dossier with a reconstructed `etat.md`
  (§2), verifier-as-corrector pairing for phase 7, headless adaptation of
  the J+30 reflect (phase 9), three new known pitfalls (from-memory
  verdicts in summary tables, superlatives beyond the corpus, out-of-order
  phases treated as new evidence).
- Repo made publication-ready: English README, MIT license, this changelog,
  anonymized example.

## 1.0.0 — 2026-06-12

Initial version (French), extracted from the white-paper execution of
2026-06-11: 9 phases, incremental-by-default with on-disk completion
artifacts, `--overwrite` (archive, never delete), `--reflect` J+30 mode,
adversarial verification with dated perishable verdicts, challenger
steelman, capped 3+3 action plan with mandatory baselines, daily-ops
routing.
