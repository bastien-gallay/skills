# skill-template

Minimal skeleton for a new Class-A Claude skill. Copy this directory into a
fresh repo and replace the placeholder tokens.

## Layout

```text
.claude-plugin/plugin.json          # plugin manifest
.claude-plugin/marketplace.json     # single-plugin marketplace
.markdownlint.json                  # canonical lint config
skills/SKILL_NAME/SKILL.md          # the skill itself (name + trigger clause)
```

## Bootstrap

1. Copy this folder into a new repo `bastien-gallay/REPO_NAME`.
2. Rename `skills/SKILL_NAME/` to your skill's name.
3. Replace every `SKILL_NAME` and `REPO_NAME` token across the four files.
4. Write the `description` with an explicit `Use when …` trigger clause — this
   is what makes the skill discoverable.
5. Add the skill to the hub: an entry in `registry.json` and a plugin in the
   meta-marketplace `.claude-plugin/marketplace.json`.
6. Add a release runbook from `../docs/RELEASING.template.md`.

## Placeholder tokens

| Token | Replace with |
| --- | --- |
| `SKILL_NAME` | the skill/plugin name (kebab-case) |
| `REPO_NAME` | the GitHub repository name (may differ from the skill name) |
