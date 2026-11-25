"""Trilha original sintetizada (sem sample, sem direito autoral de terceiros) pro criativo só-motion dos Corretores.
100 BPM (1 compasso = 2,4 s), Am–F–C–G. Seções: intro (gancho) → batida entra (perguntas) → pausa com subida
(virada) → drop (revelação do Mapa) → groove (páginas) → final (CTA). Uso: gerar(secoes, dur, saida)."""
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
SR = 48000; BPM = 100; BEAT = 60 / BPM; BAR = 4 * BEAT
ACORDES = [[57, 60, 64], [53, 57, 60], [48, 52, 55, 60], [55, 59, 62]]   # Am F C G (midi)
RAIZ = [45, 41, 48, 43]
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def env(n, a, d, s=0.0, r=0.05):
    t = np.arange(n) / SR; e = np.where(t < a, t / max(a, 1e-4), s + (1 - s) * np.exp(-(t - a) / max(d, 1e-4)))
    rel = int(r * SR); e[-rel:] *= np.linspace(1, 0, rel) if rel < n else 1; return e
def lp(x, f, o=2): return sosfilt(butter(o, f, "low", fs=SR, output="sos"), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, "high", fs=SR, output="sos"), x)
def bp(x, a, b): return sosfilt(butter(2, [a, b], "band", fs=SR, output="sos"), x)
rng = np.random.default_rng(7)
def kick():
    n = int(0.45 * SR); t = np.arange(n) / SR; f = 45 + 110 * np.exp(-t * 28)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7.5); x += 0.3 * np.sin(2 * np.pi * 2200 * t) * np.exp(-t * 300)
    return np.tanh(1.6 * x) * 0.95
def clap():
    n = int(0.3 * SR); x = bp(rng.standard_normal(n), 900, 4000); e = np.zeros(n)
    for o in (0, 0.011, 0.022): i = int(o * SR); e[i:] += np.exp(-np.arange(n - i) / SR * 38)
    return x * e * 0.35
def hat(aberto=False):
    n = int((0.22 if aberto else 0.06) * SR); x = hp(rng.standard_normal(n), 7000, 4)
    return x * np.exp(-np.arange(n) / SR * (14 if aberto else 70)) * 0.16
def baixo(m, dur):
    n = int(dur * SR); t = np.arange(n) / SR; f = hz(m)
    x = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t); return np.tanh(1.4 * x) * env(n, 0.005, 0.25, 0.55, 0.04) * 0.42
def pad(notas, dur, brilho=1800):
    n = int(dur * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for m in notas:
        for dt in (-0.12, 0.0, 0.11):
            f = hz(m) * 2 ** (dt / 12); ph = rng.uniform(0, 1); x += 2 * ((f * t + ph) % 1) - 1
    x = lp(x / (len(notas) * 3), brilho, 2); return x * env(n, 0.35, 9, 1.0, 0.3) * 0.32
def pluck(m, dur=0.35):
    n = int(dur * SR); t = np.arange(n) / SR; f = hz(m)
    x = 2 * np.abs(2 * ((f * t) % 1) - 1) - 1; x = lp(x, 3500); return x * np.exp(-t * 9) * 0.22
def subida(dur):
    n = int(dur * SR); t = np.arange(n) / SR; x = hp(rng.standard_normal(n), 600)
    x = np.array([0.0]) if n == 0 else x
    sweep = np.zeros(n); f0, f1 = 400, 9000; fc = f0 * (f1 / f0) ** (t / dur)
    blocks = 64
    for i in range(0, n, n // blocks):
        j = min(n, i + n // blocks); sweep[i:j] = bp(rng.standard_normal(j - i), max(200, fc[i] * 0.7), min(20000, fc[i] * 1.3))
    return sweep * (t / dur) ** 2 * 0.35
def impacto():
    n = int(1.6 * SR); t = np.arange(n) / SR; f = 38 + 60 * np.exp(-t * 9)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.2) + 0.25 * lp(rng.standard_normal(n), 2500) * np.exp(-t * 6)
    return np.tanh(1.3 * x) * 0.9
def por(buf, x, t):
    i = int(t * SR); e = min(len(buf), i + len(x)) - i
    if e > 0: buf[i:i + e] += x[:e]
def gerar(dur, saida, intro=(0, 2.4), batida=(2.4, 7.2), pausa=(7.2, 9.6), drop=(9.6, 24.0), final=(24.0, 28.8)):
    n = int(dur * SR); dr = np.zeros(n); bs = np.zeros(n); pd = np.zeros(n); pl = np.zeros(n); fx = np.zeros(n)
    nb = int(np.ceil(dur / BAR))
    for b in range(nb):
        t0 = b * BAR; c = b % 4
        em_pausa = pausa[0] <= t0 < pausa[1]
        brilho = 900 if t0 < intro[1] else (1300 if em_pausa else 2200)
        pd_ = pad(ACORDES[c], BAR + 0.3, brilho); por(pd, pd_ * (0.8 if em_pausa else 1.0), t0)
        for k in range(8):                       # arpejo em colcheias
            m = ACORDES[c][k % len(ACORDES[c])] + (12 if k in (3, 7) else 0)
            if not em_pausa or k < 4: por(pl, pluck(m), t0 + k * BEAT / 2)
        if t0 >= batida[0] and not em_pausa:
            cheio = t0 >= drop[0]
            for k in range(4):
                tk = t0 + k * BEAT
                if k in (0, 2) or (cheio and k == 3 and b % 2): por(dr, kick(), tk)
                if k in (1, 3): por(dr, clap() * (1.0 if cheio else 0.6), tk)
                por(dr, hat(), tk + BEAT / 2)
                if cheio: por(dr, hat(), tk); por(dr, hat(True) * 0.5, tk + BEAT * 0.75)
            for k in range(4 if t0 >= drop[0] else 2):
                d = BEAT if t0 >= drop[0] else 2 * BEAT
                por(bs, baixo(RAIZ[c] + (12 if (k == 3 and t0 >= drop[0]) else 0), d * 0.9), t0 + k * d)
    por(fx, subida(pausa[1] - pausa[0]), pausa[0]); por(fx, impacto(), drop[0]); por(fx, impacto() * 0.6, 0.0)
    # "sidechain": pad e baixo abaixam em cada kick
    duck = np.ones(n)
    for b in range(nb):
        t0 = b * BAR
        if t0 >= batida[0] and not (pausa[0] <= t0 < pausa[1]):
            for k in (0, 2):
                i = int((t0 + k * BEAT) * SR); L = int(0.22 * SR); e = min(n, i + L) - i
                if e > 0: duck[i:i + e] = np.minimum(duck[i:i + e], 1 - 0.55 * np.exp(-np.arange(e) / SR * 12))
    mix = dr * 0.9 + bs * duck + pd * duck * 0.85 + pl * 0.7 + fx * 0.8
    fo = int(1.2 * SR); mix[-fo:] *= np.linspace(1, 0, fo)
    mix = np.tanh(mix * 1.1) / np.tanh(1.1)
    st = np.stack([mix + 0.004 * np.roll(pd, 220), mix + 0.004 * np.roll(pd, -220)], 1)
    st /= np.abs(st).max() / 0.8; sf.write(saida, st, SR); return saida
if __name__ == "__main__":
    gerar(28.8, "/home/claude/corretores/voz/trilha_motion.wav", batida=(0.0, 7.2)); print("ok")
