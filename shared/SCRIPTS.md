# Scripts in skills — CUPID

A skill's `SKILL.md` is read by a model; its scripts are run by one. A script
that surprises the model costs a turn, a wrong claim, or both. Scripts shipped
under `plugins/*/` are held to the five CUPID properties, read as concrete
rules for that caller. Existing scripts have not been audited against them
yet; new and changed scripts meet them before merge.

| Property | Rule for a skill script |
| --- | --- |
| **Composable** | Input from arguments, files or stdin; result on stdout; diagnostics on stderr. No interactive prompt. A script can be called on its own, outside the skill. |
| **Unix philosophy** | One job per script. Two jobs, two scripts, chained by the skill or by a pipe — not a mode flag that switches behaviour. |
| **Predictable** | Same input, same output: stable ordering, no timestamps or random ids unless asked. Exit `0` on success, non-zero on failure, and the message says which input was at fault. No hidden state outside the paths it was given. |
| **Idiomatic** | Python runs with `uv run` and declares its dependencies (`pyproject.toml` or inline script metadata); Node uses `.mjs` with no build step. Follow the language's usual layout and naming. |
| **Domain-based** | Names come from the skill's domain (`fallacy`, `verdict`, `ledger`), not from plumbing (`helper`, `utils`, `manager`). A data contract between the model and a script (a JSON schema, a column list) lives in `assets/` or `references/` and is cited by `SKILL.md`. |

## Before merging a script

- It runs from a clean checkout with the command `SKILL.md` gives.
- It has at least one test that fixes its output for a known input.
- `--help` states what it reads, what it writes and its exit codes.
