# v2 Format Spec (strict)

Follow this exactly. `examples/e01-chinese/` is the reference build — when in doubt, match it.

## 0. Pre-production questions (ask the user first)

1. 开场音乐想要什么类型？(default: basketball ambience)
2. 每一集目标时长多少分钟？(default: 10–15 min)

Their answers override the defaults below.

## 1. Episode scope

- One episode = 30–60 seconds of source material; whole episode 10–15 minutes (or the user's chosen length).
- Longer material → split into E01, E02, … Episode titles must carry an `E##` suffix.

## 2. Segment order and gaps

Gaps are silence inserted after each segment.

| # | Segment | Source file | Gap after |
|---|---------|-------------|-----------|
| 1 | Intro music | `music/intro.wav` (user-chosen style) | 0.5s |
| 2 | Opening — short, straight into the topic | `open.mp3` ← `script-open.txt` | 0.5s |
| 3 | Full original clip of this episode | `clip-full.wav` | 0.8s |
| 4 | Host transition — exactly one line | `topen.mp3` ← `script-topen.txt` | 0.5s |
| 5 | Per sentence i (1..N): original clip → explanation → clip replay → fixed transition → slow read-along | `clip-s{i}.wav` / `exp{i}.mp3` / `clip-s{i}.wav` / `ts.mp3` / `slow{i}.mp3` | 0.4 / 0.4 / 0.4 / 0.3 / 0.8s |
| 6 | Recap — quick review of the episode's expressions (6-sentence episodes) | `recap.mp3` ← `script-recap.txt` | 0.4s |
| 7 | Closing: relisten cue → full clip replay → sign-off + next-episode preview → outro music | `closeA.mp3` / `clip-full.wav` / `closeB.mp3` / `music/outro.wav` | 0.4 / 0.6 / 0.5 / — |

## 3. Per-script rules

- `script-open.txt` — 2–4 turns. Name the show, name the episode topic and the source range being covered, end with the "listen to the full clip first" line. No lyrical preamble, get to the topic immediately.
- `script-topen.txt` — exactly one host line bridging the full clip into the sentence-by-sentence breakdown. E.g. EN: "Okay, you've heard the whole fifty-three seconds. Now let's take it line by line, starting with the first one." / ZH: "好，完整听完了，下面我们逐句拆解，先从第一句开始。"
- `script-exp{i}.txt` — one sentence explained: meaning + usage + cultural background, broken into small pieces. Concrete and specific; each host adds a distinct angle. Add a short spoken transition + brief pause between explanations.
- `script-recap.txt` — (6-sentence episodes only) rapid-fire review: one line per expression, alternating hosts.
- `script-closeA.txt` — the "let's listen to the full clip once more" cue. `script-closeB.txt` — next-episode preview + sign-off.

## 4. Fixed transition phrase (`ts`) — use verbatim

- Chinese: 原声听完了，下面是慢速朗读，你可以跟着一起读。
- English: "That was the original clip. Now, the slow read-along. You can read along with me."

## 5. Voices and TTS

- Alex = `avocado_v2:MAI_01`, Jordan = `avocado_v2:MAI_03`. Same hosts, same voices, every episode of a series.
- Script text must be spoken form: spell out numbers ("fifty-three"), split abbreviations ("N B A"), no stage directions or markup.
- Slow read-along: cleaned source sentence (fillers like "uh" removed), Alex's voice, `--speed 80`.

## 6. File layout

```text
~/workspace/podcasts/<episode-slug>/
  clip-full.wav  clip-s1..N.wav      # extracted source clips
  script-open.txt  script-topen.txt  script-exp1..N.txt
  script-recap.txt  script-closeA.txt  script-closeB.txt
  open.mp3  topen.mp3  exp1..N.mp3  ts.mp3  slow1..N.mp3
  recap.mp3  closeA.mp3  closeB.mp3
  <OUT>.mp3  <OUT>-transcript.txt
  asm/  # intermediates: timeline.txt, concatenated wav
```

## 7. Assemblers (in `bin/`)

- `assemble.py EP OUT TITLE` — Chinese, 6 sentences + recap.
- `assemble_en.py EP OUT TITLE N RECAP` — English, N sentences, `RECAP` = `1`/`0`. Auto-includes `topen.mp3` when present.

Both normalize to 44.1 kHz mono, peak-normalize to 0.9, encode 128k MP3, and write a timestamped transcript + `asm/timeline.txt`.
