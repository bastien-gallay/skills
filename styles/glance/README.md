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

| Surface     | Mechanism     | How to use            | Persists   |
|-------------|---------------|-----------------------|------------|
| Claude Code | Output style  | `/config` → **Glance**| Every turn |
| Claude Code | Slash command | `/glance`             | One-shot   |
| Claude.ai   | Custom style  | **Glance** in picker  | Every turn |

All three are derived from a single source: [`prompt.md`](./prompt.md).

> ⚠️ **Use the output style, not the slash command, for long sessions.**
> A slash command is injected once, as a user message. After a dozen
> exchanges it competes with everything said since, and a context
> compaction can drop it entirely — which is why Glance "wears off". An
> output style is part of the system prompt: it is re-presented on every
> turn. The slash command is kept for a one-off "make *this* answer
> scannable".

## Install

### Claude Code

```bash
git clone <this-repo> glance
cd glance
./install.sh
```

This symlinks both Claude Code surfaces, so any edit to the repo
propagates automatically:

| Repo file                     | Symlinked to                         |
|-------------------------------|--------------------------------------|
| `claude-code/glance.md`       | `~/.claude/commands/glance.md`       |
| `claude-code/glance-style.md` | `~/.claude/output-styles/glance.md`  |

Then activate the style once: open `/config` and pick **Glance** under
*Output style*. Claude Code remembers the selection across sessions
(it writes an `outputStyle` key into `~/.claude/settings.json`).

> There used to be a dedicated `/output-style` slash command. It was
> removed — as of Claude Code **2.1.218** the picker lives in `/config`
> ("For custom styles, open /config"). Output styles themselves are
> very much alive: `~/.claude/output-styles/` is still read, and
> `--safe-mode` lists them among the customizations it disables.

Use `--copy` instead of symlink if you prefer:

```bash
./install.sh --copy
```

### Claude.ai

In the prompt input (web or desktop app):

1. Click the **+** icon → **Use style** → **Create & edit styles**
2. Click the **Create custom style** button
3. Click the **Describe style instead** link (lower-right of the modal)
4. Select **Use custom instructions (advanced)**
5. Paste the contents of [`claude-ai/glance-style.md`](./claude-ai/glance-style.md)
   into the text area
6. Click **Create style**

To use it afterwards: **+** → **Use style** → **Glance**.

> ⚠️ Anthropic is migrating Custom styles to Skills. The menu path
> above may change; Glance's Claude.ai surface will likely move to a
> Skill.

## Iterate

`prompt.md` is the source of truth. The shared body lives between the
`<!-- glance:body:start -->` / `<!-- glance:body:end -->` markers. When
you change it:

1. Edit the body inside the markers in `prompt.md`
2. Run `./build.sh` — regenerates the three derived files from their
   per-surface templates (`*.md.tmpl`)
3. Re-paste the style on Claude.ai (the symlinks only cover Claude Code)

`./build.sh --check` exits non-zero if the derived files are out of
sync with the source — useful in pre-commit / CI.

The derived files diverge in their wrapper, not their body:

- The **slash command** starts with *"For the rest of this session..."*
  and asks for an acknowledgement line.
- The **Claude Code output style** carries frontmatter and no session
  framing — it is active as long as it is selected, so "for the rest of
  this session" would be wrong. Its `keep-coding-instructions: true` is
  load-bearing: without it, the style *replaces* Claude Code's default
  coding instructions instead of sitting alongside them. Glance is a
  formatting directive, not a new job description.
- The **Claude.ai style** is implicitly scoped by the picker, so it also
  omits the framing.

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
