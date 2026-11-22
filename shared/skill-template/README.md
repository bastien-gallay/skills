# skill-template

Minimal skeleton for a new Class-A Claude skill. Copy this directory to
`plugins/<plugin>/` in the monorepo and replace the placeholder tokens.

## Layout

```text
.claude-plugin/plugin.json          # plugin manifest
skills/SKILL_NAME/SKILL.md          # the skill itself (name + trigger clause)
```

## Bootstrap

1. Copy this folder to `plugins/REPO_NAME/` (no `marketplace.json` of its own:
   the root marketplace serves every plugin).
2. Rename `skills/SKILL_NAME/` to your skill's name.
3. Replace every `SKILL_NAME` and `REPO_NAME` token across the four files.
4. Write the `description` with an explicit `Use when …` trigger clause — this
   is what makes the skill discoverable.
5. Add the skill to the root `registry.json` and to the root
   `.claude-plugin/marketplace.json` with `"source": "./plugins/REPO_NAME"`.
6. Add a release runbook from `../docs/RELEASING.template.md`.

## Placeholder tokens

| Token | Replace with |
| --- | --- |
| `SKILL_NAME` | the skill/plugin name (kebab-case) |
| `REPO_NAME` | the plugin directory name under `plugins/` (may differ from the skill name) |
