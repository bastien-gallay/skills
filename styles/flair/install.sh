#!/usr/bin/env bash
# Flair — install the slash command into ~/.claude/commands/
#
# Usage:
#   ./install.sh           # symlink (recommended — edits propagate)
#   ./install.sh --copy    # copy instead of symlink
#
# After install, use `/flair` in Claude Code to (re-)assert Response Flair.
# For Claude.ai: see claude-ai/flair-style.md
# For always-on behaviour: add the snippet from README ("Always-on") to
# your ~/.claude/CLAUDE.md.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE="$REPO_DIR/claude-code/flair.md"
TARGET_DIR="$HOME/.claude/commands"
TARGET="$TARGET_DIR/flair.md"

mkdir -p "$TARGET_DIR"

if [[ "${1:-}" == "--copy" ]]; then
  cp "$SOURCE" "$TARGET"
  echo "✅ Slash command copied to: $TARGET"
else
  ln -sf "$SOURCE" "$TARGET"
  echo "✅ Slash command linked: $TARGET → $SOURCE"
fi

echo
echo "Next steps:"
echo "  • Claude Code → type /flair in any session"
echo "  • Claude.ai   → see claude-ai/flair-style.md to install the style"
echo "  • Always-on   → see README 'Always-on' to add a ~/.claude/CLAUDE.md line"
