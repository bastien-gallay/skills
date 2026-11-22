# Releasing redaction

Notes mainteneur sur la coupe d'une release. Pas linké depuis le README
public — interne.

## Ce qu'une release embarque

Pas de build runtime dans le repo. Une release est :

1. Une `version` bumpée dans `.claude-plugin/plugin.json`, seul endroit
   où vit la version (`just check-versions` vérifie que la marketplace
   racine n'en porte pas).
2. Un commit sur `main` avec ce changement.
3. Un tag git annoté `redaction/vX.Y.Z` sur ce commit.
4. Une entrée `CHANGELOG.md` décrivant ce qui change.
5. Un bundle `redaction-vX.Y.Z.skill` attaché à la GitHub Release —
   zip archive avec extension `.skill` (OS-registered Claude Desktop
   pour double-click install, accepté aussi par l'uploader web
   claude.ai). Construit par `just package` en CI
   (`.github/workflows/release.yml`) au push du tag.

Les utilisateurs récupèrent la release via :

- **Claude Code plugin** — `/plugin marketplace update skills` (ou
  auto-update au démarrage de session) lit la nouvelle `plugin.json`
  version et rafraîchit son cache. **Sauter le bump est un silent
  freeze** : les utilisateurs restent figés sur l'ancien code en cache.
  C'est l'invariant le plus important que le processus de release
  protège.
- **Claude Desktop / claude.ai** — download manuel du
  `redaction-vX.Y.Z.skill` depuis la page de la Release GitHub. Sur
  Desktop, double-click (extension OS-registered). Sur le web,
  upload via Settings → Capabilities → Skills.

## Processus manuel

### Prérequis

- `just` et `jq` sur le `PATH`.
- Working tree clean, sur `main`.
- Entrée `## vX.Y.Z — YYYY-MM-DD` créée dans `CHANGELOG.md` (renommer
  `## Unreleased` lors du release).

### Étapes

```bash
just check-versions   # sanity check
just release X.Y.Z    # bump manifestes + commit + tag annoté
git push && git push --tags   # déclenche le workflow release.yml
```

Le workflow `release` :

1. Vérifie que le tag matche `plugin.json`.
2. Re-vérifie `check-versions`.
3. Construit `dist/redaction-vX.Y.Z.skill` via `just package`.
4. Extrait la section CHANGELOG correspondante (`awk` sur `^## vX.Y.Z`).
5. Crée / met à jour la GitHub Release avec l'asset `.skill`.

## Failure modes connus

- **Mismatch tag ↔ manifeste** → le workflow échoue à l'étape
  « Assert tag matches plugin.json version ». Solution : retag local
  vers la bonne version, force-push (uniquement avant que la release
  GitHub soit publique).
- **CHANGELOG sans section pour le tag** → workflow échoue à l'étape
  « Extract CHANGELOG section ». Solution : éditer CHANGELOG, commit
  amend du release commit (uniquement avant push) ou bien produire un
  nouveau commit et un nouveau tag.
- **`dist/` non gitignored** → bundle .skill accidentellement commité.
  Vérifié par `.gitignore` (`dist/` listé).
