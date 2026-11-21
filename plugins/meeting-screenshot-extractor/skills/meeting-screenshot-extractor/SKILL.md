---
name: meeting-screenshot-extractor
description: >
  Builds a CLI Python tool to automatically extract relevant screenshots from a meeting
  video, using a transcript and user-defined topics. Combines ffmpeg for frame extraction
  with Claude vision for semantic validation in an iterative feedback loop.
  Use this skill whenever the user wants to extract screenshots or frames from a video
  based on topics, themes, or transcript passages — even if they don't say "skill" or
  "CLI". Trigger on: "extract screenshots from video", "capture frames from meeting",
  "find slide in recording", "screenshot at timestamp", "video + transcript + topics",
  "grab frame when X is discussed". Also trigger when the user provides a video file
  and a transcript and wants to find visual moments matching descriptions.
---

# Meeting Screenshot Extractor Skill

Scaffolds and implements a complete Python CLI project that extracts validated screenshots
from a meeting video, guided by a transcript and a list of topics.

The pipeline: **topic → timestamps (transcript search) → ffmpeg frame → Claude vision
validation → adjust timestamp if needed → final screenshot**.

---

## Workflow overview

```text
PHASE 1 → Project scaffolding     (pyproject.toml, structure, deps)
PHASE 2 → Core modules            (transcript, extractor, verifier, pipeline)
PHASE 3 → CLI interface           (Click + Rich, extract + batch commands)
PHASE 4 → Tests & README          (pytest, .env.example, usage docs)
```

Implement all phases in sequence. Each phase is self-contained and testable.

---

## PHASE 1 — Project scaffolding

### Goal

Create the full project skeleton with dependencies and configuration.

### Project structure to create

```text
meeting-screenshot-extractor/
├── pyproject.toml
├── README.md
├── .env.example
├── src/
│   └── meeting_screenshots/
│       ├── __init__.py
│       ├── cli.py
│       ├── transcript.py
│       ├── extractor.py
│       ├── verifier.py
│       ├── pipeline.py
│       └── models.py
└── tests/
    ├── __init__.py
    ├── test_transcript.py
    ├── test_extractor.py
    └── test_verifier.py
```

### pyproject.toml

```toml
[project]
name = "meeting-screenshot-extractor"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "anthropic>=0.40.0",
    "click>=8.1",
    "rich>=13.0",
    "python-dotenv>=1.0",
    "webvtt-py>=0.5",
    "srt>=3.5",
]

[project.scripts]
meeting-screenshots = "meeting_screenshots.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

### .env.example

```bash
ANTHROPIC_API_KEY=sk-ant-...
DEFAULT_SCORE_THRESHOLD=7
DEFAULT_MAX_ATTEMPTS=5
DEFAULT_STEP_SECONDS=3.0
```

---

## PHASE 2 — Core modules

### `models.py` — Shared types

```python
from dataclasses import dataclass, field

@dataclass
class TimestampCandidate:
    seconds: float
    context: str        # transcript excerpt around the timestamp
    confidence: float   # 0.0–1.0

@dataclass
class VerificationResult:
    ok: bool
    score: int          # 0–10
    reason: str
    suggestion: str | None  # "before" | "after" | None

@dataclass
class ScreenshotResult:
    topic: str
    timestamp: float
    image_path: str | None
    score: int
    attempts: int
    success: bool
```

---

### `transcript.py` — Timestamp search

Two modes depending on transcript format:

**Mode A — Timestamped transcript (VTT/SRT)** *(preferred)*

- Parse `.vtt` with `webvtt` library, `.srt` with `srt` library
- Lexical keyword search in segment text (split topic into words, match any)
- Return native timestamps with surrounding context

**Mode B — Plain text transcript** *(fallback)*

- Call `claude-opus-4-5` with the full transcript
- System prompt: `"You are a meeting analyst. Return only valid JSON, no markdown."`
- User prompt template:

  ```text
  In this meeting transcript, find the passages most relevant to: "{topic}"
  Return ONLY JSON: {"timestamps": [{"seconds": 123.5, "context": "...excerpt..."}]}
  Estimate timestamps proportionally if the transcript has no explicit times.
  
  TRANSCRIPT:
  {transcript_text}
  ```

- Parse JSON response; fallback to `[]` on any parse error

**Public signature:**

```python
def find_timestamps_for_topic(
    transcript_path: str,
    topic: str,
    max_candidates: int = 3
) -> list[TimestampCandidate]
```

Auto-detect format from file extension (`.vtt`, `.srt` → Mode A, else → Mode B).

---

### `extractor.py` — ffmpeg wrapper

```python
def extract_frame(
    video_path: str,
    timestamp: float,
    output_path: str,
    quality: int = 2
) -> bool
```

Build and run:

```bash
ffmpeg -y -ss {timestamp} -i {video_path} -vframes 1 -q:v {quality} {output_path}
```

- `-ss` MUST be before `-i` (input seeking — critical for performance on long videos)
- Return `True` if `returncode == 0` AND output file exists and is non-empty
- Log stderr via Rich on failure
- Raise `FileNotFoundError` with clear message if `ffmpeg` is not in PATH

---

### `verifier.py` — Claude vision check

```python
def verify_screenshot(
    image_path: str,
    topic: str
) -> VerificationResult
```

1. Read image, encode to base64
2. Call `claude-opus-4-5` with:
   - System: `"You are a meeting screenshot reviewer. Return only valid JSON, no markdown, no code fences."`
   - User content: image block + text:

     ```text
     Does this meeting screenshot illustrate: "{topic}"?
     
     Return JSON: {"ok": true/false, "score": 0-10, "reason": "...", "suggestion": "before"|"after"|null}
     - "before": the right moment seems to be just before this frame
     - "after": the right moment seems to be just after this frame
     - null: looks good, or no clear directional hint
     ```

3. Parse JSON; on failure return `VerificationResult(ok=False, score=0, reason="parse error", suggestion=None)`

---

### `pipeline.py` — Orchestration loop

```python
def find_best_screenshot(
    video_path: str,
    transcript_path: str,
    topic: str,
    output_dir: str = "screenshots",
    max_attempts: int = 5,
    step_seconds: float = 3.0,
    score_threshold: int = 7,
    verbose: bool = False
) -> ScreenshotResult
```

**Algorithm:**

```python
candidates = find_timestamps_for_topic(transcript_path, topic)
for base_ts in candidates:
    ts = base_ts
    best_score = 0
    for attempt in 1..max_attempts:
        frame_path = f"{output_dir}/{sanitize(topic)}_{ts:.1f}s_a{attempt}.jpg"
        ok = extract_frame(video_path, ts, frame_path)
        if not ok: break
        result = verify_screenshot(frame_path, topic)
        if result.score > best_score: best_score = result.score
        if result.ok and result.score >= score_threshold:
            return ScreenshotResult(success=True, timestamp=ts, image_path=frame_path, ...)
        # Adjust timestamp
        if result.suggestion == "after":  ts += step_seconds
        elif result.suggestion == "before": ts -= step_seconds
        else:  # alternating exploration: +step, -step, +2*step, -2*step, ...
            direction = +1 if attempt % 2 == 1 else -1
            ts = base_ts + direction * step_seconds * ((attempt // 2) + 1)
        ts = max(0.0, ts)
return ScreenshotResult(success=False, score=best_score, ...)
```

Helper: `sanitize(topic)` → lowercase, non-alphanumeric replaced by `_`, truncated to 30 chars.

---

## PHASE 3 — CLI interface

### `cli.py` — Click + Rich

Two commands under a `@click.group()` named `main`.

#### Command `extract` — single topic

```bash
meeting-screenshots extract \
  --video reunion.mp4 \
  --transcript transcript.vtt \
  --topic "microservices architecture slide" \
  --output-dir ./screenshots \
  --max-attempts 5 \
  --step 3.0 \
  --threshold 7 \
  --verbose
```

Output: path to the best screenshot, or an error message.

#### Command `batch` — multiple topics from file

```bash
meeting-screenshots batch \
  --video reunion.mp4 \
  --transcript transcript.vtt \
  --topics-file topics.txt \
  --output-dir ./screenshots \
  --report results.json \
  --verbose
```

- `topics.txt`: one topic per line, blank lines and `#` comments ignored
- Progress bar via `rich.progress.Progress`
- Final summary table via `rich.table.Table`:
  columns: Topic | Timestamp | Score | Attempts | Path | Status (✓/✗)
- Write `results.json` with the list of `ScreenshotResult` objects serialized

#### Global option

- `--dry-run`: print what would be done, no ffmpeg calls, no API calls

#### Rich output conventions

- Green = success (`[green]✓[/green]`)
- Red = failure (`[red]✗[/red]`)
- Yellow = warning / degraded (`[yellow]⚠[/yellow]`)
- Use `rich.console.Console(stderr=True)` for logs, stdout for final paths only

---

## PHASE 4 — Tests & README

### Tests (pytest + pytest-mock)

**`test_transcript.py`**

- Mock `anthropic.Anthropic` client
- Test VTT parsing with a fixture `.vtt` string
- Test SRT parsing with a fixture `.srt` string
- Test LLM fallback: mock returns valid JSON, assert candidates parsed correctly
- Test LLM fallback: mock returns invalid JSON, assert empty list returned

**`test_extractor.py`**

- Mock `subprocess.run` to return `returncode=0` + create a dummy file
- Assert ffmpeg command has `-ss` BEFORE `-i`
- Test with `returncode=1` → returns `False`
- Test missing ffmpeg → raises `FileNotFoundError`

**`test_verifier.py`**

- Mock `anthropic.Anthropic` client
- Test valid JSON response → correct `VerificationResult`
- Test invalid JSON → fallback result with `score=0`
- Test `suggestion="before"` / `"after"` / `null` parsing

### README.md sections

1. **Prerequisites**: Python 3.11+, ffmpeg (`brew install ffmpeg` / `apt install ffmpeg`), Anthropic API key
2. **Installation**: `uv pip install -e .`
3. **Configuration**: copy `.env.example` → `.env`, fill `ANTHROPIC_API_KEY`
4. **Supported transcript formats**: VTT (preferred), SRT, plain text
5. **Usage**: examples of both `extract` and `batch` commands
6. **How it works**: one-paragraph explanation of the pipeline
7. **Cost considerations**: note that vision calls cost more; keep `--max-attempts` low

---

## Edge cases to handle

| Case | Expected behavior |
| --- | --- |
| ffmpeg not in PATH | `FileNotFoundError` with install instructions |
| Timestamp > video duration | Clamp to `video_duration - 2.0` (use ffprobe to get duration) |
| Empty transcript | Log warning, return `ScreenshotResult(success=False)` |
| Invalid JSON from LLM | Log warning, fallback to empty list / score=0 |
| Score never reaches threshold | Return best attempt found, `success=False`, log best score |
| Batch with many topics | Sequential processing (no parallelism — controls API costs) |
| `--dry-run` mode | Print planned actions, no subprocess or API calls |

---

## Implementation notes

- Use `python-dotenv` `load_dotenv()` at CLI startup to load `.env`
- `ANTHROPIC_API_KEY` also picked up automatically by the Anthropic SDK from env
- For ffprobe duration: `ffprobe -v quiet -print_format json -show_format {video}` → parse `format.duration`
- All file paths in output: use `pathlib.Path` throughout, convert to `str` only at subprocess boundaries
- Model to use for all API calls: `claude-opus-4-5`

---

## Quality checklist before delivery

- [ ] `uv pip install -e .` runs without error
- [ ] `meeting-screenshots --help` shows both commands
- [ ] `extract` command works end-to-end with a real video + transcript
- [ ] `batch` command produces a valid `results.json`
- [ ] All tests pass: `pytest tests/ -v`
- [ ] `-ss` is before `-i` in the ffmpeg command (verified in test)
- [ ] Missing ffmpeg produces a clear error message
- [ ] `--dry-run` makes zero API calls and zero subprocess calls

For full transcript format handling details, see `references/transcript-formats.md`.
