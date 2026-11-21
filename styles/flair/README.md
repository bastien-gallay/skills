# Flair

> Short, learning-flavored anecdotes on your AI's answers — a programming-language
> note and a productivity note, tucked just above the TL;DR. Shared across Claude
> Code and Claude.ai, derived from one source.

## What it does

When active, the assistant ends a substantive answer (one that has a `TL;DR`)
with a two-line **flair stack** right above the TL;DR:

```text
🧬  <one programming-language anecdote — italic, theme-emoji prefixed>
    <one efficiency / productivity anecdote — plain, concrete>
## TL;DR
```

- 🔁 **Rotating themes** — language features, history, compilers, code-quality
  metrics for Pack A; time-management, attention, productivity history for Pack B.
- 🎯 **Concrete only** — a name, a date, a study, or a quote; never platitudes.
- 🤫 **Stays out of the way** — fires *only* when a TL;DR is present, and skips
  sensitive topics (incidents, security, painful errors).
- 🧩 **Extensible** — packs are data. Add a "math history" or "etymology" pack by
  copying a pack block in [`prompt.md`](./prompt.md); the trigger never changes.

## Surfaces

| Surface     | Mechanism     | Default   | How to use                              |
|-------------|---------------|-----------|-----------------------------------------|
| Claude Code | Slash command | opt-in    | `/flair` to (re-)assert for the session |
| Claude Code | `CLAUDE.md`   | always-on | add the snippet below (recommended)     |
| Claude.ai   | Custom style  | per-chat  | pick **Flair** from the style picker    |

All three derive from a single source: [`prompt.md`](./prompt.md).

## Install

### Claude Code — the `/flair` command

```bash
git clone https://github.com/bastien-gallay/skills.git
cd skills/styles/flair
./install.sh
```

This symlinks `claude-code/flair.md` into `~/.claude/commands/flair.md`, so any
edit to the repo propagates automatically. Use `./install.sh --copy` to copy
instead of symlink.

### Claude Code — always-on (recommended)

The `/flair` command is *opt-in* (silent until you type it). If you want the
flair to appear automatically on every TL;DR answer, add a pointer to your
**user-global** `~/.claude/CLAUDE.md` (loads in every repo/session):

```markdown
- Response flair: on every answer that contains a TL;DR, prepend a short
  anecdote stack just above it — one programming-language line (italic,
  theme-emoji) then one efficiency line (plain, concrete). Full spec:
  ~/Dev/oss/skills/flair/prompt.md. One line per pack, rotate themes, skip
  sensitive topics.
```

### Claude.ai — the custom style

Follow [`claude-ai/flair-style.md`](./claude-ai/flair-style.md): create a custom
style named **Flair**, paste the instructions block, then pick it from the style
picker.

> ⚠️ Anthropic is migrating Custom styles to Skills (rollout from 2026-05-20).
> The menu path may change; Flair's Claude.ai surface will likely move to a Skill.

## Iterate

`prompt.md` is the source of truth. The shared body lives between the
`<!-- flair:body:start -->` / `<!-- flair:body:end -->` markers. When you change it:

1. Edit the body inside the markers in `prompt.md`.
2. Run `./build.sh` — regenerates `claude-code/flair.md` and
   `claude-ai/flair-style.md` from the per-surface templates (`*.md.tmpl`).
3. Re-paste the style on Claude.ai (the symlink only covers Claude Code).

`./build.sh --check` exits non-zero if the derived files drift from the source —
useful in pre-commit / CI.

The derived files diverge in their *wrapper*, not their *body*:

- The slash command starts with *"For the rest of this session…"* and asks for an
  acknowledgement line.
- The Claude.ai style is implicitly session-scoped (selected from the picker), so
  it omits the framing.

## On logging

There is currently **no automatic log** of the anecdotes delivered — no Claude
Code hook event sees the assistant's response text, so the flair lines can't be
captured to a file as they're emitted. If you want history, the closest option is
a manual `/capture` command you run after a response you liked.

## Why "Flair"

A small, optional ornament that adds character without changing the substance —
exactly what the anecdote stack is. Short, pronounceable in EN and FR.

## Roadmap

- [ ] `flair-auto` Skill that adapts the pack choice to the answer's domain.
- [ ] A third built-in pack (math history? etymology?) to prove extensibility.
- [ ] Optional `Stop`-hook logger, if a future hook event exposes response text.
