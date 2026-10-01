---
name: explainer-podcast
description: 讲解播客：拿用户给的原材料（采访/视频/文章）做多人对谈式深度讲解播客。结构固定为「播放原声 → 逐句讲解 → 重听原声」。用于"生成播客""做一期讲解""播客英文版"等请求。
---

# Explainer Podcast

Workflow skill. Produces a mixed explainer podcast episode: source clips + two-host dialogue (Alex & Jordan).

Before producing anything, listen to `examples/e01-chinese/e01-chinese-full.mp3` (and the English preview) and read `references/format.md` — the episode structure below is strict, not a suggestion.

## Workflow

0. **Ask first.** Before starting, ask the user two questions in plain text:
   1. 开场音乐想要什么类型？（默认：篮球氛围音乐）
   2. 每一集目标时长多少分钟？（默认：10–15 分钟）
   Do not start production until they answer. Their answers override the defaults everywhere below.
1. **Segment plan.** One episode covers 30–60 seconds of source material. Longer material → split into E01, E02, … Titles must carry an `E##` suffix.
2. **Extract clips.** From the source audio: `clip-full.wav` (the episode's full original segment) and `clip-s1..N.wav` (one per explained sentence, in order).
3. **Write scripts** (`Alex:` / `Jordan:` turns, spoken form — spell out numbers, split abbreviations like "N B A", no stage directions or markup). Per-script rules are in `references/format.md`.
4. **Synthesize** with `/opt/hatch/bin/tts` (see Tooling). Host voices are fixed: Alex = `avocado_v2:MAI_01`, Jordan = `avocado_v2:MAI_03`.
5. **Assemble** with `bin/assemble.py` (Chinese, 6 sentences + recap) or `bin/assemble_en.py` (English: `EP OUT TITLE N RECAP`). Produces the final MP3 + timestamped transcript.
6. **Deliver** the MP3 + transcript to the user.

## Tooling

- Dialogue: `/opt/hatch/bin/tts synthesize-script --script <txt> --speaker Alex=avocado_v2:MAI_01 --speaker Jordan=avocado_v2:MAI_03 --output <mp3> --language <en|zh>`
- Single line: `/opt/hatch/bin/tts speak --voice <voice-id> --output <mp3> --language <code> --text-stdin <<'TTS_INPUT' …` (note: `--voice`, not `--speaker`)
- Slow read-along: same `speak` with `--speed 80`, Alex's voice, cleaned source sentence (fillers removed).
- `--language` must match the text (default `en`; English output is highest quality).
- On transient backend failure ("truncated or empty audio"): retry the exact same request later — never change voice, text, or engine. Ladder: ~5m, ~10m, ~30m, ~1h, then stop and report.

## Operating Rules

1. Generate only — never publish without the user's explicit approval.
2. Follow `references/format.md` strictly: segment order, gaps, fixed phrases, and per-script rules.
3. Publishing limits: `podcast-helper publish` only accepts pure-TTS audio it generated itself (trusted audio handle); hand-mixed episodes (source clips + music) cannot go to the public RSS. For Spotify use `podcast-helper save-to-spotify` (cover jpg/png ≤ 1 MB); poll with `save-to-spotify --json episodes status <uri> --wait` until READY.
4. Keep the two hosts and their voices consistent across a series.
5. Keep episode work under `~/workspace/podcasts/<episode-slug>/`; don't rely on `/tmp` (it gets cleaned).
