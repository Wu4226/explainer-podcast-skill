import subprocess, os, wave, sys
import numpy as np

SR = 44100
MUSIC = os.path.expanduser("~/workspace/podcasts/music")
BASE = os.path.expanduser("~/workspace/podcasts")

EP = sys.argv[1]
OUT = sys.argv[2]
TITLE = sys.argv[3]

D = f"{BASE}/{EP}"
os.makedirs(f"{D}/asm", exist_ok=True)

def load_wav(path):
    p = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-ar", "44100", "-ac", "1",
         "-f", "f32le", "-acodec", "pcm_f32le", "-"],
        capture_output=True, check=True)
    return np.frombuffer(p.stdout, dtype=np.float32)

def silence(sec):
    return np.zeros(int(sec * SR), dtype=np.float32)

seq = [("intro", 0.5), ("open", 0.5), ("full", 0.8)]
for i in range(1, 7):
    seq += [(f"c{i}", 0.4), (f"exp{i}", 0.4), (f"c{i}", 0.4), ("ts", 0.3), (f"s{i}", 0.8)]
seq += [("recap", 0.4), ("closeA", 0.4), ("full", 0.6), ("closeB", 0.5), ("outro", 0.0)]

FILES = {
    "intro": f"{MUSIC}/intro.wav", "outro": f"{MUSIC}/outro.wav",
    "ts": f"{MUSIC}/trans-slow.wav", "open": f"{D}/open.wav",
    "full": f"{D}/clip-full.wav", "closeA": f"{D}/closeA.wav",
    "recap": f"{D}/recap.wav",
    "closeB": f"{D}/closeB.wav",
}
for i in range(1, 7):
    FILES[f"c{i}"] = f"{D}/clip-s{i}.wav"
    FILES[f"exp{i}"] = f"{D}/exp{i}.wav"
    FILES[f"s{i}"] = f"{D}/slow{i}.wav"

parts, marks, t = [], [], 0.0
for name, gap in seq:
    audio = load_wav(FILES[name])
    marks.append((name, t, t + len(audio) / SR))
    parts.append(audio)
    t += len(audio) / SR
    if gap:
        parts.append(silence(gap))
        t += gap

full = np.concatenate(parts)
full = full / max(1e-6, np.abs(full).max()) * 0.9
pcm = (full * 32767).astype(np.int16)

wav_path = f"{D}/asm/{OUT}.wav"
w = wave.open(wav_path, "wb")
w.setnchannels(1)
w.setsampwidth(2)
w.setframerate(SR)
w.writeframes(pcm.tobytes())
w.close()

mp3_path = f"{D}/{OUT}.mp3"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav_path,
                "-codec:a", "libmp3lame", "-b:a", "128k", mp3_path], check=True)

dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                      "-of", "csv=p=0", mp3_path], capture_output=True, text=True)
print(f"{OUT}: {float(dur.stdout.strip()):.1f}s -> {mp3_path}", flush=True)

def mmss(s):
    m, sec = divmod(int(s), 60)
    return f"{m:02d}:{sec:02d}"

LABELS = {"intro": "【片头音乐】", "open": "【开场】", "full": "【本集原声·完整】",
          "ts": "【过渡】原声听完了，下面是慢速朗读，你可以跟着一起读。",
          "closeA": "【结尾·重听】", "closeB": "【结尾】",
          "outro": "【片尾音乐】", "recap": "【本集小结】"}
for i in range(1, 7):
    LABELS[f"c{i}"] = f"【原声片段{i}】"
    LABELS[f"s{i}"] = f"【慢速朗读{i}】"
    LABELS[f"exp{i}"] = f"【讲解{i}】"

def read(p):
    try:
        return open(p, encoding="utf-8").read().strip()
    except FileNotFoundError:
        return ""

lines = [f"{TITLE}", ""]
for name, st, en in marks:
    lines.append(f"[{mmss(st)}] {LABELS[name]}")
    body = ""
    if name == "open":
        body = read(f"{D}/script-open.txt")
    elif name.startswith("exp"):
        body = read(f"{D}/script-{name}.txt")
    elif name == "recap":
        body = read(f"{D}/script-recap.txt")
    elif name == "closeA":
        body = read(f"{D}/script-closeA.txt")
    elif name == "closeB":
        body = read(f"{D}/script-closeB.txt")
    if body:
        lines.append(body)
    lines.append("")

txt_path = f"{D}/{OUT}-台词.txt"
open(txt_path, "w", encoding="utf-8").write("\n".join(lines))
print("台词本:", txt_path, flush=True)

tl = open(f"{D}/asm/timeline.txt", "w")
for name, st, en in marks:
    tl.write(f"{mmss(st)}-{mmss(en)} {name}\n")
tl.close()
