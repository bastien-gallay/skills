# Transcript Format Reference

## VTT (WebVTT) — Preferred format

Standard output from most meeting platforms (Zoom, Teams, Google Meet).

### Example

```vtt
WEBVTT

00:00:05.000 --> 00:00:09.500
So today we'll be covering the microservices architecture
we proposed last quarter.

00:00:09.500 --> 00:00:14.200
Let me bring up the diagram on the slide.

00:00:14.200 --> 00:00:20.000
As you can see, we have three main services:
auth, catalog, and orders.
```

### Parsing with webvtt-py

```python
import webvtt

for caption in webvtt.read("transcript.vtt"):
    start_seconds = _vtt_time_to_seconds(caption.start)
    text = caption.text.strip()
```

Helper:

```python
def _vtt_time_to_seconds(ts: str) -> float:
    # ts format: "HH:MM:SS.mmm" or "MM:SS.mmm"
    parts = ts.replace(",", ".").split(":")
    if len(parts) == 3:
        h, m, s = parts
        return int(h) * 3600 + int(m) * 60 + float(s)
    else:
        m, s = parts
        return int(m) * 60 + float(s)
```

---

## SRT (SubRip) — Common alternative

```srt
1
00:00:05,000 --> 00:00:09,500
So today we'll be covering the microservices architecture
we proposed last quarter.

2
00:00:09,500 --> 00:00:14,200
Let me bring up the diagram on the slide.
```

### Parsing with srt library

```python
import srt

with open("transcript.srt") as f:
    subtitles = list(srt.parse(f.read()))

for sub in subtitles:
    start_seconds = sub.start.total_seconds()
    text = sub.content.strip()
```

---

## Plain text — Fallback (no native timestamps)

Any `.txt` file without embedded timestamps. The LLM infers approximate timestamps
from the narrative flow and total video duration (if provided).

### LLM prompt strategy

When using plain text, include video duration in the prompt if available:

```python
prompt = f"""
In this meeting transcript (total duration: {duration_hint}), find passages
most relevant to: "{topic}"

Return ONLY JSON: {{"timestamps": [{{"seconds": 123.5, "context": "...excerpt..."}}]}}

Estimate timestamps proportionally based on position in the text.
Provide up to {max_candidates} candidates, ordered by relevance.

TRANSCRIPT:
{transcript_text[:8000]}  # truncate if very long
"""
```

**Important**: plain text timestamps are estimates (±30–60s typical error).
The pipeline's iterative adjustment loop compensates for this imprecision.

---

## Detection logic

```python
def detect_format(path: str) -> str:
    ext = Path(path).suffix.lower()
    if ext == ".vtt":
        return "vtt"
    elif ext == ".srt":
        return "srt"
    else:
        return "text"  # .txt, .md, or anything else
```

---

## Timestamp precision by format

| Format | Precision | Notes                          |
|--------|-----------|--------------------------------|
| VTT    | ±0.1s     | Use as primary anchor          |
| SRT    | ±0.1s     | Use as primary anchor          |
| Text   | ±30–60s   | Pipeline iteration compensates |

For text transcripts with many topics, consider increasing `--max-attempts`
and decreasing `--step` (e.g., `--max-attempts 8 --step 5.0`) to give the
loop more room to converge.
