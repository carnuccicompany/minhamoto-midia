"""Prévia rápida: python3 prev.py script.py t1 t2 ... → folha com os quadros (timeline = tempo do arquivo do pronto no body)."""
import sys, importlib.util, subprocess, numpy as np
from PIL import Image
spec = importlib.util.spec_from_file_location("m", sys.argv[1]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
ts = [float(x) for x in sys.argv[2:]]; out = []
for t in ts:
    acc = 0; seg = None
    for s in m.SEGS:
        if acc <= t < acc + s.dur: seg = s; break
        acc += s.dur
    ft = seg.t0 + (t - acc)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{ft:.3f}", "-i", seg.src, "-frames:v", "1", "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    img = Image.frombytes("RGB", (1080, 1920), raw).convert("RGBA")
    for ov in m.__dict__.get("OVS", []): ov(img, t)
    out.append(img.convert("RGB").resize((360, 640)))
sheet = Image.new("RGB", (360 * min(5, len(out)), 640 * ((len(out) + 4) // 5)))
for i, im in enumerate(out): sheet.paste(im, ((i % 5) * 360, (i // 5) * 640))
sheet.save("/tmp/prev.png")
