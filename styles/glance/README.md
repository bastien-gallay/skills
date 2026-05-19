# Glance

> A shared visual mode for Claude.ai and Claude Code.
> Turns dense topics into at-a-glance answers: tables, ASCII diagrams,
> bullets, and a TL;DR when it counts.

## What it does

When activated, Claude formats its responses for **at-a-glance readability**:

- 📊 Tables, bullets, and ASCII diagrams instead of long prose
- ✂️ Short, precise sentences — no filler, no hedging
- 🎯 Functional emojis as signals (`✅ ❌ ⚠️ → 📊`), not decoration
- 🔑 **Bold** on key terms and values
- 📝 TL;DR block at the end when the response is long

## Surfaces

| Surface     | Mechanism      | How to use         |
|-------------|----------------|--------------------|
| Claude Code | Slash command  | `/glance`          |
| Claude.ai   | Custom style   | Pick **Glance** from the style picker |

Both are derived from a single source: [`prompt.md`](./prompt.md).

## Install

### Claude Code

```bash
git clone <this-repo> glance
cd glance
./install.sh
```

This symlinks `claude-code/glance.md` into `~/.claude/commands/glance.md`,
so any edit to the repo propagates automatically.

Use `--copy` instead of symlink if you prefer:

```bash
./install.sh --copy
```

### Claude.ai

See [`claude-ai/glance-style.md`](./claude-ai/glance-style.md) for the
exact text to paste into Settings → Custom styles → Create.

## Iterate

`prompt.md` is the source of truth. The shared body lives between the
`<!-- glance:body:start -->` / `<!-- glance:body:end -->` markers. When
you change it:

1. Edit the body inside the markers in `prompt.md`
2. Run `./build.sh` — regenerates `claude-code/glance.md` and
   `claude-ai/glance-style.md` from per-surface templates
   (`*.md.tmpl`)
3. Re-paste the style on Claude.ai (the symlink only covers Claude Code)

`./build.sh --check` exits non-zero if the derived files are out of
sync with the source — useful in pre-commit / CI.

The two derived files diverge in their wrapper, not their body:

- The slash command starts with *"For the rest of this session..."* and
  asks for an acknowledgement line.
- The Claude.ai style is implicitly session-scoped (selected from the
  picker), so it omits the framing.

## Why "Glance"

The prompt itself says *"optimize for at-a-glance readability"* — the
name is a direct echo of the function. Pronounceable in EN and FR,
short, no negative connotation.

## Roadmap

- [ ] Add a `glance-auto` Claude Code Skill that triggers without
      explicit invocation when a question would benefit from dense
      formatting
- [ ] Generate `.cursorrules` / Codex-compatible variants from the same
      source
