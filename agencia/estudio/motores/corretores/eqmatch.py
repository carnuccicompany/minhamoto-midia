"""Casa o timbre de um trecho (ex.: gancho abafado do pronto) com o body do mesmo pronto, por faixa de oitava.
Pedido do Léo (25/11): o início do EST5 estava abafado em relação ao resto."""
import numpy as np, soundfile as sf, subprocess, tempfile
from scipy.signal import welch
B = [(80, 160), (160, 320), (320, 640), (640, 1250), (1250, 2500), (2500, 5000), (5000, 10000), (10000, 16000)]
CEN = [113, 226, 453, 894, 1768, 3536, 7071, 12649]
def _bands(x, sr):
    f, P = welch(x, sr, nperseg=4096); o = np.array([10 * np.log10(P[(f >= lo) & (f < hi)].mean() + 1e-20) for lo, hi in B]); return o - o.mean()
def _wav(src, a, b, af=None):
    t = tempfile.mktemp(suffix=".wav"); cmd = ["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", str(b - a), "-i", src, "-ac", "1", "-ar", "48000"]
    if af: cmd += ["-af", af]
    subprocess.run(cmd + [t], check=True); x, sr = sf.read(t); return x, sr
def entradas(g): return "firequalizer=gain_entry='" + ";".join(f"entry({c},{v:.1f})" for c, v in zip(CEN, g)) + "'"
def casar(src, trecho, alvo, iters=3):
    xa, sr = _wav(src, *alvo); ta = _bands(xa, sr); g = np.zeros(len(B))
    for _ in range(iters):
        xt, sr = _wav(src, *trecho, af=entradas(g) if g.any() else None)
        d = ta - _bands(xt, sr); g = np.clip(g + 0.8 * d, -22, 14)
    xt, sr = _wav(src, *trecho, af=entradas(g)); res = ta - _bands(xt, sr)
    return entradas(g), np.round(res, 1)
