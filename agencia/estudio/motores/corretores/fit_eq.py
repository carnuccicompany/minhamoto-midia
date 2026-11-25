#!/usr/bin/env python3
"""Ajusta um EQ (firequalizer) pra um trecho da Gravação Dia 2 casar faixa a faixa com o take do CTA4 (método ltas do revisor:
energia relativa por faixa, quadros de fala). Itera até cada faixa ficar a ≤ 3 dB. Salva em novo/eq_grav.json."""
import sys, json, os, subprocess, numpy as np
BANDS = [(100, 250), (250, 500), (500, 700), (700, 850), (850, 1000), (1000, 2000), (2000, 4000), (4000, 8000)]
CENT = [160, 350, 600, 775, 925, 1400, 2800, 5600]
def perfil(arq, a=None, b=None, af=None):
    cmd = ["ffmpeg", "-loglevel", "error"] + (["-ss", str(a), "-t", str(b - a)] if a is not None else []) + ["-i", arq]
    if af: cmd += ["-af", af]
    y = np.frombuffer(subprocess.run(cmd + ["-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    N = 1024; n = len(y) // N; fr = y[:n * N].reshape(n, N); db = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-7); fr = fr[db > np.percentile(db, 50)]
    P = (np.abs(np.fft.rfft(fr * np.hanning(N), axis=1)) ** 2).mean(0); fq = np.fft.rfftfreq(N, 1 / 16000)
    L = np.array([10 * np.log10(P[(fq >= lo) & (fq < hi)].sum() + 1e-12) for lo, hi in BANDS]); return L - 10 * np.log10((10 ** (L / 10)).sum())
def fq(g):
    ent = ";".join([f"entry(20,{g[0]:.2f})"] + [f"entry({c},{x:.2f})" for c, x in zip(CENT, g)] + [f"entry(12000,{g[-1]:.2f})"])
    return f"firequalizer=gain_entry='{ent}'"
if __name__ == "__main__":
    U = "/mnt/user-data/uploads/Corretores/Criativos prontos/ESTUDIO 23-11/_trabalho/"
    G = os.path.join(os.path.dirname(os.path.abspath(__file__)), "novo/grav.wav")
    ref = perfil(U + "cortes2/cta4.mov", 0, 6.0)
    out = {}
    for nome, a, b in [("est10", 6.7, 28.6), ("est7", 29.4, 36.1), ("est8", 36.8, 47.0)]:
        g = np.zeros(len(BANDS))
        for it in range(12):
            p = perfil(G, a, b, fq(g)); d = ref - p
            if np.abs(d).max() <= 2.5: break
            g = g + 0.9 * np.sign(d) * np.maximum(0, np.abs(d) - 2.0)   # só mexe no que passa de 2 dB: EQ mais suave possível
        print(nome, "ganhos", g.round(1), "dif final", d.round(1))
        out[nome] = fq(g)
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "novo/eq_grav.json"), "w"), indent=1)
