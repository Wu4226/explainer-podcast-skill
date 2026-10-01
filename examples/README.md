# Examples

Two complete Episode 1 builds of the same series — read these before producing a new episode.

## e01-chinese/ — 中文讲解版（完整成品，7:06）

- `transcript.txt` — timestamped transcript （台词本） of the finished episode.
- `scripts/` — the exact scripts used: `script-open.txt`, `script-exp1..4.txt`, `script-closeA.txt`, `script-closeB.txt`.

Source material: the first 53 seconds of the Mind The Game Steph Curry interview. 4 sentences explained, no recap segment.

## e01-english/ — 全英文讲解版

Same episode, fully in English.

- `scripts/` — `script-open.txt`, `script-topen.txt` (the host transition line after the full clip), `script-exp1..4.txt`, `script-closeA.txt`, `script-closeB.txt`, `transition-slow-read.txt` (the fixed slow-read transition phrase).

Note the English fixed transition phrase: "That was the original clip. Now, the slow read-along. You can read along with me."

## Reference audio

The finished MP3s (`e01-v2-full.mp3`, `e01-en-v2-full.mp3`) are the production builds; regenerate them any time from `scripts/` + source clips with `bin/assemble.py` / `bin/assemble_en.py`.
