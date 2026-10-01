# v2 Format Spec

The episode structure, in order. Gaps are silence inserted after each segment.

| # | Segment | Source file | Gap after |
|---|---------|-------------|-----------|
| 1 | Intro music (basketball ambience) | `music/intro.wav` | 0.5s |
| 2 | Opening (short, straight into topic) | `open.mp3` ← `script-open.txt` | 0.5s |
| 3 | Full original clip of this episode | `clip-full.wav` | 0.8s |
| 4 | Host transition line | `topen.mp3` ← `script-topen.txt` | 0.5s |
| 5 | Per sentence i (1..N): original clip → explanation → clip replay → fixed transition → slow read-along | `clip-s{i}.wav` / `exp{i}.mp3` / `clip-s{i}.wav` / `ts.mp3` / `slow{i}.mp3` | 0.4 / 0.4 / 0.4 / 0.3 / 0.8s |
| 6 | Recap — quick review of the episode's expressions (6-sentence episodes) | `recap.mp3` ← `script-recap.txt` | 0.4s |
| 7 | Closing: relisten intro → full clip replay → sign-off + next-episode preview → outro music | `closeA.mp3` / `clip-full.wav` / `closeB.mp3` / `music/outro.wav` | 0.4 / 0.6 / 0.5 / — |

## Fixed transition phrase (`ts`)

- Chinese: 原声听完了，下面是慢速朗读
- English: "That was the original clip. Now, the slow read-along. You can read along with me."

## Per-episode file layout

```text
~/workspace/podcasts/<episode-slug>/
  clip-full.wav  clip-s1..N.wav      # extracted source clips
  script-open.txt  script-topen.txt  script-exp1..N.txt
  script-recap.txt  script-closeA.txt  script-closeB.txt
  open.mp3  topen.mp3  exp1..N.mp3  ts.mp3  slow1..N.mp3
  recap.mp3  closeA.mp3  closeB.mp3
  <OUT>.mp3  <OUT>-transcript.txt  (or <OUT>-台词.txt)
  asm/  # intermediates: timeline.txt, concatenated wav
```

## Assemblers (in `bin/`)

- `assemble.py EP OUT TITLE` — Chinese, 6 sentences + recap.
- `assemble_en.py EP OUT TITLE N RECAP` — English, N sentences, `RECAP` = `1`/`0`. Auto-includes `topen.mp3` when present.

Both normalize to 44.1 kHz mono, peak-normalize to 0.9, encode 128k MP3, and write a timestamped transcript + `asm/timeline.txt`.

## Notes

- One episode = 30–60 seconds of source material; whole episode 10–15 minutes.
- Explanations stay concrete: meaning + usage + cultural background, broken into small pieces. Add a short spoken transition + brief pause between explanations.
- Slow read-along uses the cleaned source sentence (fillers like "uh" removed), Alex's voice at `--speed 80`.
