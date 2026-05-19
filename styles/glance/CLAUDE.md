# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Glance is a tiny "prompt distribution" project: a single source prompt (`prompt.md`) that defines a "Glance Mode" formatting directive, plus two surface-specific derivatives:

- `claude-code/glance.md` — the `/glance` slash command (session-scoped, asks for an acknowledgement line)
- `claude-ai/glance-style.md` — the Claude.ai custom style text (no session framing, since it's selected from the picker)

There is **no build system, no tests, no package manager**. All "code" is Markdown.

## Architecture: source → derived

```
prompt.md  (canonical; shared body between <!-- glance:body:start/end --> markers)
   │
   ├── claude-code/glance.md.tmpl  ──build.sh──▶ claude-code/glance.md
   └── claude-ai/glance-style.md.tmpl ──build.sh──▶ claude-ai/glance-style.md
```

Each `*.md.tmpl` is a per-surface wrapper containing a `{{BODY}}`
placeholder that `build.sh` replaces with the marked region of
`prompt.md`.

When editing the prompt:

1. Edit the body inside the markers in `prompt.md`.
2. Run `./build.sh` to regenerate both derived files. Use
   `./build.sh --check` in pre-commit / CI to fail on drift.
3. The Claude.ai style must be re-pasted on claude.ai after a change — the install script only symlinks the Claude Code surface.

If you need surface-specific wording (framing, intro line,
acknowledgement), edit the relevant `.tmpl`. If you need to change the
shared rules, edit `prompt.md`. Never edit the generated `claude-code/glance.md`
or `claude-ai/glance-style.md` directly — your edits will be overwritten on
the next `./build.sh`.

## Install workflow

```bash
./install.sh          # symlink claude-code/glance.md → ~/.claude/commands/glance.md
./install.sh --copy   # copy instead (edits won't propagate)
```

Symlink mode is the default and means in-repo edits to `claude-code/glance.md` take effect immediately in Claude Code.

## Conventions

- Markdown files should pass `markdownlint` (per user global instructions).
- Keep ASCII diagrams under 80 columns — this is a content rule from the prompt itself and applies to docs in this repo too.
