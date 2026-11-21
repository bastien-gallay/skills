#!/usr/bin/env bash
# Glance — install the Claude Code surfaces into ~/.claude/
#
# Usage:
#   ./install.sh           # symlink (recommended — edits propagate)
#   ./install.sh --copy    # copy instead of symlink
#
# Installs two surfaces:
#   • slash command → /glance               (one-shot, session-scoped)
#   • output style  → /output-style Glance  (persistent — survives compaction)
#
# For Claude.ai: see claude-ai/glance-style.md

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

MODE="link"
[[ "${1:-}" == "--copy" ]] && MODE="copy"

install_one() {
  local source="$1" target_dir="$2" target="$2/$3"
  mkdir -p "$target_dir"
  if [[ "$MODE" == "copy" ]]; then
    cp "$source" "$target"
    echo "✅ copied: $target"
  else
    ln -sf "$source" "$target"
    echo "✅ linked: $target → $source"
  fi
}

install_one "$REPO_DIR/claude-code/glance.md" \
            "$HOME/.claude/commands" "glance.md"
install_one "$REPO_DIR/claude-code/glance-style.md" \
            "$HOME/.claude/output-styles" "glance.md"

echo
echo "Next steps:"
echo "  • Claude Code → /output-style Glance   (persistent, recommended)"
echo "  • Claude Code → /glance                (one-shot, this session)"
echo "  • Claude.ai   → see claude-ai/glance-style.md to install the style"
