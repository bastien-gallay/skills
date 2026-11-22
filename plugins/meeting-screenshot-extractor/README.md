# meeting-screenshot-extractor

Builds a CLI Python tool to automatically extract relevant screenshots from a
meeting video, using a transcript and user-defined topics. Combines ffmpeg
for frame extraction with Claude vision for semantic validation in an
iterative feedback loop.

## Install

In Claude Code, from the `bastien-gallay/skills` marketplace:

```text
/plugin marketplace add bastien-gallay/skills
/plugin install meeting-screenshot-extractor@skills
```

Or copy `skills/meeting-screenshot-extractor/` into your project's
`.claude/skills/` directory.
