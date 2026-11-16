# Releasing truepath

Maintainer notes: how a version is cut. There is no build step and no
bundle; a release is a commit on `main`, a tag on it, and a line in the hub.

## What a release is

| Where | What changes |
| --- | --- |
| `.claude-plugin/plugin.json` | `version` |
| `.claude-plugin/marketplace.json` | `metadata.version` and `plugins[0].version` |
| `CHANGELOG.md` | a `## X.Y.Z` section, first in the file |
| `README.md` | the first line of `## Status` |
| git | an annotated, signed tag `vX.Y.Z` on the commit that carries the above |
| GitHub | a release on that tag, its notes taken from the changelog section |
| [bastien-gallay/skills](https://github.com/bastien-gallay/skills) | `version` and `updated` of the `truepath` entry in `registry.json` |

The three manifest versions and the changelog heading must agree: CI
refuses a push where they do not. Claude Code reads `plugin.json` to decide
whether an installed plugin is out of date, so a release without that bump
reaches nobody.

## Steps

1. Run what CI runs, listed under *Verification commands* in
   [`.wrap.md`](../.wrap.md). If `runtime.html` or `layout.py` changed,
   rebuild the port examples and commit their `sim.html` with the change.
2. Write the four version places of the table, commit as
   `truepath X.Y.Z: <the conclusion>`, push, and wait for CI.
3. Tag and publish:

   ```sh
   git tag -s vX.Y.Z -m "truepath X.Y.Z"
   git push origin vX.Y.Z
   gh release create vX.Y.Z --title "truepath X.Y.Z" --notes-file <the changelog section>
   ```

4. In the hub, on a branch: update the `truepath` entry of `registry.json`,
   run `node docs/build.mjs`, open a pull request.

## Which number

Before 1.0 the spec vocabulary may change. A change that makes an existing
`spec.json` stop building bumps the minor version and says so in the
changelog, with the old and the new key; anything else bumps the patch.

## What users get

- **Claude Code plugin**, from this repository or from the hub:
  `/plugin marketplace update` then `/plugin update` picks up the new
  `plugin.json` version.
- **A copied `skills/truepath/` folder**: nothing updates it; copy it again.
