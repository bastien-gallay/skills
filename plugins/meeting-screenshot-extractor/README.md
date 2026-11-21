# meeting-screenshot-extractor

Builds a CLI Python tool to automatically extract relevant screenshots from a
meeting video, using a transcript and user-defined topics. Combines ffmpeg
for frame extraction with Claude vision for semantic validation in an
iterative feedback loop.

## Install

Add this repository as a Claude Code plugin marketplace and install the
`meeting-screenshot-extractor` plugin, or copy
`skills/meeting-screenshot-extractor/` into your project's `.claude/skills/`
directory.
