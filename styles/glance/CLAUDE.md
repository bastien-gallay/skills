# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Glance is a tiny "prompt distribution" project: a single source prompt (`prompt.md`) that defines a "Glance Mode" formatting directive, plus three surface-specific derivatives:

- `claude-code/glance-style.md` — the Claude Code **output style** (select it in `/config`). The primary surface: output styles are part of the system prompt, so the directive is re-presented every turn. Its frontmatter sets `keep-coding-instructions: true` so the style adds formatting rules rather than replacing Claude Code's default coding instructions.
- `claude-code/glance.md` — the `/glance` slash command (session-scoped, asks for an acknowledgement line). One-shot; kept for a single scannable answer.
- `claude-ai/glance-style.md` — the Claude.ai custom style text (no session framing, since it's selected from the picker)

Alongside the prompt:

- `docs/glyph-legibility.md` — what a human actually tested on a real
  terminal. Read it before changing any glyph or emoji rule; it is the
  only evidence in this repo that did not come from a model.

There are **no tests and no package manager**. The only build step is
`build.sh`, a shell script. All "code" is Markdown.

## Architecture: source → derived

    prompt.md — canonical; body between glance:body:start/end markers
    │
    ├── claude-code/glance-style.md.tmpl ─build.sh─▶ claude-code/glance-style.md
    ├── claude-code/glance.md.tmpl       ─build.sh─▶ claude-code/glance.md
    └── claude-ai/glance-style.md.tmpl   ─build.sh─▶ claude-ai/glance-style.md

Each `*.md.tmpl` is a per-surface wrapper containing a `{{BODY}}`
placeholder that `build.sh` replaces with the marked region of
`prompt.md`.

When editing the prompt:

1. Edit the body inside the markers in `prompt.md`.
2. Run `./build.sh` to regenerate all three derived files. Use
   `./build.sh --check` in pre-commit / CI to fail on drift.
3. The Claude.ai style must be re-pasted on claude.ai after a change — the install script only symlinks the Claude Code surfaces.

If you need surface-specific wording (framing, intro line,
acknowledgement), edit the relevant `.tmpl`. If you need to change the
shared rules, edit `prompt.md`. Never edit a generated file
(`claude-code/glance.md`, `claude-code/glance-style.md`,
`claude-ai/glance-style.md`) directly — your edits will be overwritten
on the next `./build.sh`.

## Install workflow

```bash
./install.sh          # symlink both Claude Code surfaces into ~/.claude/
./install.sh --copy   # copy instead (edits won't propagate)
```

`install.sh` symlinks **both** Claude Code surfaces —
`claude-code/glance.md` → `~/.claude/commands/glance.md`, and
`claude-code/glance-style.md` → `~/.claude/output-styles/glance.md`.
Symlink mode is the default and means in-repo edits take effect
immediately in Claude Code. The output style still has to be selected
once, in `/config` → *Output style*.

## Conventions

- Markdown files should pass `markdownlint` (per user global instructions).
  `.markdownlint.json` disables MD041 repo-wide: slash commands and style
  texts open with prose by design, so a first-line H1 does not apply here.
  Note `build.sh` only lints `prompt.md` and the two generated files —
  run `markdownlint` yourself when you touch `CLAUDE.md`, `README.md`,
  or `docs/`.
- Keep ASCII diagrams under 80 columns — this is a content rule from the prompt itself and applies to docs in this repo too.

## Traps

- **"For the rest of this session" is a wish, not a mechanism.** A
  slash command's text is injected *once*, as a user message. Ten
  exchanges later it competes with everything said since, and a context
  compaction can drop it outright — which is exactly the "Glance wears
  off mid-session" report that produced the output-style surface. If a
  directive has to hold for a whole session, it belongs somewhere that
  is re-presented every turn (output style, `CLAUDE.md`, a hook), not
  in a one-shot message.
- **The output style exists; the `/output-style` command does not.**
  Verified on Claude Code **2.1.218**: the picker moved into `/config`
  ("For custom styles, open /config"), and typing `/output-style`
  returns *Unknown command*. Don't infer the invocation from the
  feature's name — check the binary
  (`grep -a outputStyle "$(readlink -f "$(command -v claude)")"`)
  before writing it into the README. The frontmatter schema found the
  same way: `name`, `description`, `keep-coding-instructions`,
  `force-for-plugin`.
- **`$TMPDIR` does not hold the same value on both sides of the sandbox
  boundary.** Two symptoms seen so far. `build.sh` failing on `mktemp`
  ("Operation not permitted", `/var/folders/…`) is a sandbox artifact,
  not a repo bug — BSD `mktemp` with no template ignores `TMPDIR`, and
  the script is fine outside the sandbox, so do not "fix" it. And a file
  written to `$TMPDIR` in one mode is not there in the other: a backup
  saved under `/tmp/claude-501` vanished when read back from
  `/var/folders/…`. Pass absolute paths across that boundary, never
  `$TMPDIR`.
- **Commit each idea before opening the next edit.** Batching several
  edits into one file and splitting them afterwards does not work: the
  first `git add <file>` sweeps up everything written so far, producing
  one commit whose subject describes half its diff. Splitting after the
  fact then costs a history rewrite. This happened here, in the pass
  that had just restated "one commit is one idea".
- **The prompt's rules apply to this repo's own files.** When a rule in
  `prompt.md` seems to condemn something a repo file does deliberately,
  suspect the rule before the file: that is how "fenced blocks for code
  and terminal output only" was found too narrow — the Claude.ai
  template fences its style text for copy-paste, correctly.
