#!/usr/bin/env python3
"""Checagem de sincronia: grupos da legenda x pausas reais do áudio final; energia nos pontos de corte (dB rel. ao pico da fala)."""
import sys, importlib, subprocess, numpy as np, librosa
# uso: python3 checar.py est5b out/EST5-B.mp4
nome, mp4 = sys.argv[1], sys.argv[2]
sys.argv = [nome, mp4]
mod = importlib.import_module(nome); pc = mod.pc
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", mp4, "-ac", "1", "-ar", "16000", "/tmp/_chk.wav"], check=True)
y, sr = librosa.load("/tmp/_chk.wav", sr=16000)
r = librosa.feature.rms(y=y, frame_length=640, hop_length=160)[0]; db = 20 * np.log10(r / r.max() + 1e-9)
def dbat(t): i = int(t * 100); return db[max(0, i - 2):i + 3].max() if i < len(db) else -99
# pausas no final
sil = db < -24; P = []; i = 0
while i < len(sil):
    if sil[i]:
        j = i
        while j < len(sil) and sil[j]: j += 1
        if j - i >= 5: P.append((i / 100, j / 100))
        i = j
    else: i += 1
print("pausas finais:", [(round(a, 2), round(b, 2)) for a, b in P])
for a, b, txt, ts in pc.leg:
    near = min(P, key=lambda p: abs(p[1] - a)) if P else (0, 0)
    flag = "  <-- fala começa %.2f" % near[1] if abs(near[1] - a) < 0.4 and abs(near[1] - a) > 0.08 else ""
    print(f"{a:6.2f}-{b:6.2f} [{dbat(a):5.0f}dB] {txt}{flag}")
for src, a, b, pos in pc.aud:
    import motor
    print("corte", src.split('/')[-1], f"a={a} ({pos:.2f}s)  b={b} ({pos + b - a:.2f}s)  energia no ponto final: {dbat(pos + b - a - 0.05):.0f} dB")
