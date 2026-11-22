# Releasing truepath

Maintainer notes: how a version is cut. There is no build step and no
bundle; a release is a commit on `main`, a tag on it, and a line in the hub.

## What a release is

| Where | What changes |
| --- | --- |
| `.claude-plugin/plugin.json` | `version` |
| `CHANGELOG.md` | a `## X.Y.Z` section, first in the file |
| `README.md` | the first line of `## Status`: version, tag and date (CI does not read it) |
| git | an annotated, signed tag `truepath/vX.Y.Z` on the commit that carries the above |
| GitHub | a release on that tag, its notes taken from the changelog section |
| [bastien-gallay/skills](https://github.com/bastien-gallay/skills) | `version` of the `truepath` entry in `registry.json`, and the file's `updated` |

The `plugin.json` version and the changelog heading must agree, and the root
marketplace must list truepath without a version: CI refuses a push where
they do not. Claude Code reads `plugin.json` to decide
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
   git tag -s truepath/vX.Y.Z -m "truepath X.Y.Z"
   git push origin truepath/vX.Y.Z
   gh release create truepath/vX.Y.Z --title "truepath X.Y.Z" --notes-file <the changelog section>
   ```

4. In the hub, on a branch: update the `truepath` entry of `registry.json`,
   run `node docs/build.mjs`, open a pull request.

## Which number

Before 1.0 the spec vocabulary may change. A change that makes an existing
`spec.json` stop building bumps the minor version and says so in the
changelog, with the old and the new key; anything else bumps the patch.

## What users get

- **Claude Code plugin**, from this repository or from the hub: in
  `/plugin`, tab *Marketplaces*, the marketplace, *Update marketplace*
  refreshes its listing and updates the plugins installed from it; one
  plugin alone is *Installed*, the plugin, *Update now*, or
  `claude plugin update truepath@skills` in a shell. There is no
  `/plugin update`. `/reload-plugins` loads the new version in an open
  session. Auto-update is off by default for a marketplace of one's own;
  it is turned on in the same *Marketplaces* menu. Source: the plugin
  install page of the Claude Code docs, read 2026-11-20.
- **A copied `skills/truepath/` folder**: nothing updates it; copy it again.
