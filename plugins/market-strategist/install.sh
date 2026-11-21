#!/usr/bin/env bash
# market-strategist — install the skill into a skills directory
#
# Usage:
#   ./install.sh                       # symlink into ~/.claude/skills (edits propagate)
#   ./install.sh --copy                # copy instead of symlink
#   ./install.sh --dir .claude/skills  # target another directory (project, other host)
#
# After install, use `/market-strategist` in Claude Code.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# The skill lives at skills/market-strategist/ (class-A layout); link that dir
# so <target>/market-strategist/SKILL.md resolves for discovery.
SKILL_SRC="$REPO_DIR/skills/market-strategist"
TARGET_DIR="$HOME/.claude/skills"
MODE="symlink"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --copy) MODE="copy"; shift ;;
    --dir) TARGET_DIR="${2:?--dir needs a path}"; shift 2 ;;
    -h|--help) sed -n '2,10p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "❌ Unknown argument: $1" >&2; exit 2 ;;
  esac
done

TARGET="$TARGET_DIR/market-strategist"

if [[ ! -f "$SKILL_SRC/SKILL.md" ]]; then
  echo "❌ Expected $SKILL_SRC/SKILL.md — is the repo layout intact?" >&2
  exit 1
fi

if [[ ! -f "$SKILL_SRC/references/frameworks.md" ]]; then
  echo "❌ Missing $SKILL_SRC/references/frameworks.md — the framework library" >&2
  echo "   is not optional; the skill degrades badly without it." >&2
  exit 1
fi

mkdir -p "$TARGET_DIR"

if [[ "$MODE" == "copy" ]]; then
  rm -rf "$TARGET"
  cp -R "$SKILL_SRC" "$TARGET"
  echo "✅ Skill copied to: $TARGET"
else
  ln -sfn "$SKILL_SRC" "$TARGET"
  echo "✅ Skill linked: $TARGET → $SKILL_SRC"
fi

echo
echo "Next: type /market-strategist <topic> in Claude Code."
