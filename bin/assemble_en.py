import subprocess, os, wave, sys
import numpy as np

SR = 44100
MUSIC = os.path.expanduser("~/workspace/podcasts/music")
BASE = os.path.expanduser("~/workspace/podcasts")

EP = sys.argv[1]
OUT = sys.argv[2]
TITLE = sys.argv[3]
N = int(sys.argv[4]) if len(sys.argv) > 4 else 4
RECAP = (sys.argv[5] == "1") if len(sys.argv) > 5 else False

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

def read(p):
    try:
        return open(p, encoding="utf-8").read().strip()
    except FileNotFoundError:
        return ""

seq = [("intro", 0.5), ("open", 0.5), ("full", 0.8)]
if os.path.exists(f"{D}/topen.mp3"):
    seq.append(("topen", 0.5))
for i in range(1, N + 1):
    seq += [(f"c{i}", 0.4), (f"exp{i}", 0.4), (f"c{i}", 0.4), ("ts", 0.3), (f"s{i}", 0.8)]
if RECAP:
    seq.append(("recap", 0.4))
seq += [("closeA", 0.4), ("full", 0.6), ("closeB", 0.5), ("outro", 0.0)]

FILES = {
    "intro": f"{MUSIC}/intro.wav", "outro": f"{MUSIC}/outro.wav",
    "ts": f"{D}/ts.mp3", "open": f"{D}/open.mp3",
    "full": f"{D}/clip-full.wav",
    "topen": f"{D}/topen.mp3",
    "closeA": f"{D}/closeA.mp3",
    "closeB": f"{D}/closeB.mp3",
}
if RECAP:
    FILES["recap"] = f"{D}/recap.mp3"
for i in range(1, N + 1):
    FILES[f"c{i}"] = f"{D}/clip-s{i}.wav"
    FILES[f"exp{i}"] = f"{D}/exp{i}.mp3"
    FILES[f"s{i}"] = f"{D}/slow{i}.mp3"

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

LABELS = {"intro": "[Intro music]", "open": "[Opening]", "full": "[Original audio - full]",
          "topen": "[Transition after full clip]",
          "ts": "[Transition] That was the original clip. Now, the slow read-along. You can read along with me.",
          "closeA": "[Closing - relisten]", "closeB": "[Closing]",
          "outro": "[Outro music]", "recap": "[Episode recap]"}
for i in range(1, N + 1):
    LABELS[f"c{i}"] = f"[Original clip {i}]"
    LABELS[f"s{i}"] = f"[Slow read-along {i}]"
    LABELS[f"exp{i}"] = f"[Explanation {i}]"

lines = [f"{TITLE}", ""]
for name, st, en in marks:
    lines.append(f"[{mmss(st)}] {LABELS[name]}")
    body = ""
    if name == "open":
        body = read(f"{D}/script-open.txt")
    elif name == "topen":
        body = read(f"{D}/script-topen.txt")
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

txt_path = f"{D}/{OUT}-transcript.txt"
open(txt_path, "w", encoding="utf-8").write("\n".join(lines))
print("Transcript:", txt_path, flush=True)

tl = open(f"{D}/asm/timeline.txt", "w")
for name, st, en in marks:
    tl.write(f"{mmss(st)}-{mmss(en)} {name}\n")
tl.close()
