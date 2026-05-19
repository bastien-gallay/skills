#!/usr/bin/env bash
# Glance — install the slash command into ~/.claude/commands/
#
# Usage:
#   ./install.sh           # symlink (recommended — edits propagate)
#   ./install.sh --copy    # copy instead of symlink
#
# After install, use `/glance` in Claude Code to activate Glance Mode.
# For Claude.ai: see claude-ai/glance-style.md

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE="$REPO_DIR/claude-code/glance.md"
TARGET_DIR="$HOME/.claude/commands"
TARGET="$TARGET_DIR/glance.md"

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
echo "  • Claude Code → type /glance in any session"
echo "  • Claude.ai   → see claude-ai/glance-style.md to install the style"
