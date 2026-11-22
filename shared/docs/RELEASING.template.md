# Releasing <SKILL_NAME>

Maintainer-facing notes on how a release is cut. Internal reference — not linked
from the public README.

## What a release actually ships

There is no build step in the repo itself. A release is:

1. A bumped `version` in `.claude-plugin/plugin.json` — the only place the
   version lives; the root marketplace lists the plugin without one.
2. A commit on `main` with that change.
3. An annotated git tag `<PLUGIN>/vX.Y.Z` on that commit.
4. A `CHANGELOG.md` entry describing what changed.
5. A `<SKILL_NAME>-vX.Y.Z.skill` bundle attached to the GitHub Release — a zip
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
# 2. Bump plugin.json to X.Y.Z.
# 3. Commit, tag, push.
git commit -m "chore(<PLUGIN>): release vX.Y.Z" .claude-plugin/plugin.json
git tag -a <PLUGIN>/vX.Y.Z -m "Release <PLUGIN> vX.Y.Z"
git push && git push origin <PLUGIN>/vX.Y.Z
# 4. Build the .skill bundle (zip the plugin tree) and create the release.
gh release create <PLUGIN>/vX.Y.Z dist/<SKILL_NAME>-vX.Y.Z.skill --title "<PLUGIN> vX.Y.Z" --notes-from-tag
```

## Invariants the process protects

- **One version** — `plugin.json` carries it and nothing else does; skip the
  bump and the plugin channel silently freezes.
- **CHANGELOG matches the tag** — no "released vX.Y.Z with vW.V.U in the changelog".
- **Clean tree, no tag re-use** — abort if the working tree is dirty or the tag exists.
