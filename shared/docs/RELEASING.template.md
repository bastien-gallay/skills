# Releasing <SKILL_NAME>

Maintainer-facing notes on how a release is cut. Internal reference — not linked
from the public README.

## What a release actually ships

There is no build step in the repo itself. A release is:

1. A bumped `version` in `.claude-plugin/plugin.json`.
2. A bumped `metadata.version` **and** `plugins[0].version` in
   `.claude-plugin/marketplace.json` (both must match).
3. A commit on `main` with the above changes.
4. An annotated git tag `vX.Y.Z` on that commit.
5. A `CHANGELOG.md` entry describing what changed.
6. A `<SKILL_NAME>-vX.Y.Z.skill` bundle attached to the GitHub Release — a zip
   archive with the `.skill` extension.

## Distribution channels

- **Claude Code plugin channel** — `/plugin marketplace update <MARKETPLACE>`
  reads the new `plugin.json` version and refreshes its cache. **Skipping the
  version bump is a silent freeze: users stay on cached old code.** This is the
  single most important invariant the release process protects.
- **Meta-marketplace (`bastien-gallay/skills`)** — re-clones the repo on update.
- **Claude Desktop / claude.ai channel** — users download the `.skill` bundle
  from the GitHub Release page. Updates are manual.

## Steps

```sh
# 1. Ensure CHANGELOG has a `## vX.Y.Z` section and the tree is clean on main.
# 2. Bump both manifests (plugin.json + marketplace.json) to X.Y.Z.
# 3. Commit, tag, push.
git commit -am "chore: release vX.Y.Z"
git tag -a vX.Y.Z -m "vX.Y.Z"
git push && git push --tags
# 4. Build the .skill bundle (zip the plugin tree) and create the release.
gh release create vX.Y.Z dist/<SKILL_NAME>-vX.Y.Z.skill --title "vX.Y.Z" --notes-from-tag
```

## Invariants the process protects

- **Manifest versions aligned** — `plugin.json` and both `marketplace.json`
  version fields must match, or the plugin channel silently freezes.
- **CHANGELOG matches the tag** — no "released vX.Y.Z with vW.V.U in the changelog".
- **Clean tree, no tag re-use** — abort if the working tree is dirty or the tag exists.
