# shared — the mutualized socle

Canonical building blocks copied into each Class-A skill repo. The hub keeps the
reference version here; repos vendor a copy (skills stay independently
installable, so the socle is duplicated on purpose, not symlinked).

| File | Purpose | Consumers |
| --- | --- | --- |
| `.markdownlint.json` | Canonical markdownlint config (identical across all repos today) | every repo with Markdown |
| `docs/RELEASING.template.md` | Fill-in release runbook for a single-plugin skill repo | Class-A skill repos |
| `skill-template/` | Minimal skeleton for a brand-new Class-A skill | new skills |

## Syncing a repo to the socle

There is intentionally no automatic sync. When the canonical version changes,
copy it into the target repo and commit there. To check a repo is aligned:

```sh
diff shared/.markdownlint.json ../<repo>/.markdownlint.json
```
