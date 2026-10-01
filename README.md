# explainer-podcast

A skill for producing **explainer podcasts**: take source material (an interview, video, or article) and turn it into a two-host deep-dive episode.

Fixed episode structure: **play the original → explain it line by line → listen to the original again**.

- Hosts: Alex (`avocado_v2:MAI_01`) & Jordan (`avocado_v2:MAI_03`)
- One episode covers 30–60 seconds of source material; 10–15 minutes total
- Per sentence: original clip → explanation (meaning + usage + cultural background) → clip replay → fixed transition → slow read-along
- `SKILL.md` — the workflow (trigger this skill with "生成播客", "做一期讲解", "播客英文版", …)
- `references/format.md` — the full v2 format spec (segment order, gaps, fixed phrases, file layout)
- `bin/assemble.py`, `bin/assemble_en.py` — episode assemblers (normalize, concatenate, encode MP3, write timestamped transcript)

Built from a real production run: a 3-episode Chinese series plus full-English versions, made with the `tts` CLI.
