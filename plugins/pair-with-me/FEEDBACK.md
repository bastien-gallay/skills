# pair-with-me — session feedback log

Accumulated, dated feedback from real sessions, to drive skill iteration. Newest
first. Factual capture of the user's words, lightly organized.

Once a batch has been folded into `SKILL.md`, archive it under
[`feedback/`](feedback/) as a date-prefixed, reviewed file.

## 2026-07-21 — install is silently broken; skill not discoverable

Surfaced while building an unrelated skill (`wrap`), not while pairing. Nothing
here is about the protocol; it is all about installation.

### The bug

`~/.claude/skills/pair-with-me` symlinked to the **repo root**
(`~/Dev/oss/skills/pair-with-me`) instead of `skills/pair-with-me`.
Consequence:

```console
$ ls ~/.claude/skills/pair-with-me/SKILL.md
ls: .../SKILL.md: No such file or directory
```

No `SKILL.md` at the link target means no frontmatter, means **no discovery**.
The skill does not appear in the available-skills list. It had presumably been
uninstalled-in-effect since the link was made (2026-06-21), while looking
installed to anyone who runs `ls ~/.claude/skills`.

`install.sh` creates the *correct* link (`$REPO_DIR/skills/pair-with-me`), so
the bad link predates it or was made by hand. Re-running `./install.sh` fixes
it — `ln -sfn` overwrites.

### Why it stayed invisible

The failure mode is silent in both directions: the link exists and resolves to
a real directory, so nothing errors; and a skill that fails to register simply
never appears, so there is no "missing" to notice. The only symptom is
`/pair-with-me` quietly not being offered.

### Candidate fixes, in order of appetite

1. **Nothing.** Re-run `install.sh` and move on. The bad link was a one-off
   hand-made artifact; the installer is already correct.
2. **Make `install.sh` self-healing.** Before linking, check whether
   `$TARGET/SKILL.md` resolves; if a link exists but points somewhere without a
   `SKILL.md`, say so explicitly rather than silently replacing it. Cheap, and
   turns a silent state into a printed one.
3. **A `--check` flag** that verifies the installed link resolves to a
   `SKILL.md` and exits non-zero otherwise. Useful only if this recurs.

Recommendation: (1) now, (2) if it ever happens again. Do not build (3) on one
occurrence.

### Resolution — 2026-11-21

Fix (1) applied during the move to the monorepo: the link now points at
`plugins/pair-with-me/skills/pair-with-me`, and the skill shows up again in the
available-skills list. The bad link had survived four months unnoticed — one
occurrence, so (2) is still not warranted.

<!-- No open feedback. Add new session notes above this line, newest first. -->
