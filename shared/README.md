# shared — the mutualized socle

Canonical building blocks copied into each Class-A skill repo. The hub keeps the
reference version here; repos vendor a copy (skills stay independently
installable, so the socle is duplicated on purpose, not symlinked).

| File | Purpose | Consumers |
| --- | --- | --- |
| `docs/RELEASING.template.md` | Fill-in release runbook for a single-plugin skill repo | Class-A skill repos |
| `skill-template/` | Minimal skeleton for a brand-new Class-A skill | new skills |
| `SCRIPTS.md` | CUPID rules for scripts shipped inside a skill | every plugin with scripts |

The markdownlint config is not copied: one `.markdownlint.jsonc` at the repo
root covers every plugin. A plugin that needs a different rule keeps its own
`.markdownlint.jsonc` that starts with
`"extends": "../../.markdownlint.jsonc"` and lists only what it changes. Run
markdownlint from the repo root.
