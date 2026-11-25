"""Tratamento clássico da voz do gancho abafado (sem IA): tira a reverberação da sala (WPE, predição linear),
casa o timbre com o body do mesmo pronto (EQ por oitava) e a dinâmica (compressor), e mede tudo contra o body."""
import numpy as np, soundfile as sf, subprocess, tempfile
from scipy.signal import welch, butter, sosfiltfilt, hilbert, resample_poly
B = [(80,160),(160,320),(320,640),(640,1250),(1250,2500),(2500,5000),(5000,10000),(10000,16000)]
def wav(src, a=None, b=None, sr=48000):
    t = tempfile.mktemp(suffix=".wav"); cmd = ["ffmpeg","-v","error","-y"] + (["-ss",str(a),"-t",str(b-a)] if a is not None else []) + ["-i",src,"-ac","1","-ar",str(sr),t]
    subprocess.run(cmd, check=True); return sf.read(t)[0]
def ff(x, af, sr=48000):
    a = tempfile.mktemp(suffix=".wav"); b = tempfile.mktemp(suffix=".wav"); sf.write(a, x, sr, subtype="FLOAT")
    subprocess.run(["ffmpeg","-v","error","-y","-i",a,"-af",af,b], check=True); return sf.read(b)[0]
def bands(x, sr=48000):
    f, P = welch(x, sr, nperseg=4096); o = np.array([10*np.log10(P[(f>=lo)&(f<hi)].mean()+1e-20) for lo,hi in B]); return o - o.mean()
def modul(x, sr=48000):
    """profundidade de modulação 2–8 Hz do envelope em 1–4 kHz (reverberação achata isso)."""
    sos = butter(4, [1000, 4000], "bandpass", fs=sr, output="sos"); e = np.abs(hilbert(sosfiltfilt(sos, x)))
    e = resample_poly(e, 1, 480); fs = 100; f, P = welch(e - e.mean(), fs, nperseg=256)
    return 10*np.log10(P[(f>=2)&(f<=8)].sum() / (e.mean()**2 + 1e-20))
def dinam(x, sr=48000):
    w = int(sr*.05); r = np.array([20*np.log10(np.sqrt(np.mean(x[i:i+w]**2))+1e-9) for i in range(0,len(x)-w,w)])
    fala = r[r > np.percentile(r, 40)]; return round(np.percentile(fala,95)-np.percentile(fala,20),1)
def wpe(x, sr=48000, taps=12, delay=3, it=3):
    from nara_wpe.wpe import wpe as _wpe
    from nara_wpe.utils import stft, istft
    # WPE a 16 kHz-friendly STFT size em 48 k
    Y = stft(x[None], size=1024, shift=256).transpose(2, 0, 1)
    Z = _wpe(Y, taps=taps, delay=delay, iterations=it, statistics_mode="full").transpose(1, 2, 0)
    z = istft(Z, size=1024, shift=256)[0]; z = z[:len(x)]; return np.pad(z, (0, len(x)-len(z)))
def eq_casar(x, alvo_b, iters=4, lim=(-22, 14)):
    CEN = [113,226,453,894,1768,3536,7071,12649]; g = np.zeros(8)
    def af(g): return "firequalizer=gain_entry='" + ";".join(f"entry({c},{v:.1f})" for c,v in zip(CEN,g)) + "'"
    for _ in range(iters):
        y = ff(x, af(g)) if g.any() else x; g = np.clip(g + 0.8*(alvo_b - bands(y)), *lim)
    return ff(x, af(g)), af(g)
def relatorio(nome, x): print(f"{nome:22s} bandas {np.round(bands(x),1)}  modul {modul(x):6.1f}  dinam {dinam(x)}")

# ---------- v2: resolução de 1/3 de oitava + limpeza de chiado + de-esser + compressor ----------
TERCOS = [100,125,160,200,250,315,400,500,630,800,1000,1250,1600,2000,2500,3150,4000,5000,6300,8000,10000,12500,16000]
def bandas3(x, sr=48000):
    f, P = welch(x, sr, nperseg=8192); o = []
    for c in TERCOS:
        lo, hi = c / 2**(1/6), c * 2**(1/6); o.append(10*np.log10(P[(f>=lo)&(f<hi)].mean()+1e-20))
    o = np.array(o); return o - o[4:20].mean()
def af3(g): return "firequalizer=gain_entry='" + ";".join(f"entry({c},{v:.1f})" for c, v in zip(TERCOS, g)) + "'"
def eq3_casar(x, alvo, iters=5, lim=(-20, 14)):
    g = np.zeros(len(TERCOS))
    for _ in range(iters):
        y = ff(x, af3(g)) if g.any() else x; d = alvo - bandas3(y)
        d = np.convolve(np.pad(d, 1, mode="edge"), [0.25, 0.5, 0.25], "valid")   # suaviza: nada de "pente"
        g = np.clip(g + 0.7 * d, *lim)
    return af3(g)
def ruido_perfil(x, sr=48000):
    """nível do chiado nas pausas (dB) pra calibrar o afftdn."""
    w = int(sr*.03); r = np.array([np.sqrt(np.mean(x[i:i+w]**2)) for i in range(0, len(x)-w, w)])
    return 20*np.log10(np.percentile(r, 8) + 1e-9)
def cadeia(x, alvo3, nr=10, comp=True, deess=True):
    """limpeza leve → EQ 1/3 oitava casada → de-esser → compressor parecido com o do body."""
    nf = ruido_perfil(x)
    y = ff(x, f"highpass=f=75,afftdn=nr={nr}:nf={max(-80, min(-20, nf)):.0f}:tn=1")
    eq = eq3_casar(y, alvo3); y = ff(y, eq)
    if deess: y = ff(y, "deesser=i=0.35:m=0.5:f=0.5")
    if comp: y = ff(y, "acompressor=threshold=-26dB:ratio=2.2:attack=8:release=120:makeup=1.5")
    return y, eq
def relat3(nome, x, alvo3=None):
    b = bandas3(x); s = f"{nome:20s} modul {modul(x):5.1f} dinam {dinam(x):5.1f} pausas {ruido_perfil(x):6.1f}"
    if alvo3 is not None: s += f"  desvio1/3 máx {np.abs(b-alvo3)[2:21].max():4.1f} médio {np.abs(b-alvo3)[2:21].mean():4.1f}"
    print(s)

def so_fala(x, sr=48000, pct=50):
    w = int(sr*.04); fr = [x[i:i+w] for i in range(0, len(x)-w, w)]; r = np.array([np.sqrt(np.mean(f**2)) for f in fr])
    return np.concatenate([f for f, v in zip(fr, r) if v >= np.percentile(r, pct)])
def snr(x, sr=48000):
    w = int(sr*.03); r = np.array([20*np.log10(np.sqrt(np.mean(x[i:i+w]**2))+1e-9) for i in range(0, len(x)-w, w)])
    return round(np.percentile(r, 90) - np.percentile(r, 8), 1)
def eq3_fala(x, alvo, iters=7, lim=(-20, 15)):
    g = np.zeros(len(TERCOS))
    for _ in range(iters):
        y = ff(x, af3(g)) if g.any() else x; d = alvo - bandas3(so_fala(y))
        d = np.convolve(np.pad(d, 1, mode="edge"), [0.2, 0.6, 0.2], "valid"); g = np.clip(g + 0.75 * d, *lim)
    return af3(g)
def cadeia2(x, alvo_fala, snr_alvo, comp_ratio=1.0):
    y = ff(x, "highpass=f=80")
    eq = eq3_fala(y, alvo_fala); y = ff(y, eq)
    nr = 0
    for nr in (0, 6, 10, 14, 18):        # limpeza só até o chiado ficar no nível do body (sem som de "aquário")
        z = ff(y, f"afftdn=nr={nr}:nf=-50:tn=1") if nr else y
        if snr(z) >= snr_alvo - 1: break
    y = z
    y = ff(y, "deesser=i=0.3:m=0.5:f=0.5")
    if comp_ratio > 1: y = ff(y, f"acompressor=threshold=-24dB:ratio={comp_ratio}:attack=10:release=150:makeup=1")
    return y, eq, nr
def relat4(nome, x, alvo_fala):
    b = bandas3(so_fala(x)); print(f"{nome:20s} snr {snr(x):5.1f} dinam {dinam(x):5.1f} modul {modul(x):5.1f}  desvio fala máx {np.abs(b-alvo_fala)[2:21].max():4.1f} médio {np.abs(b-alvo_fala)[2:21].mean():4.1f}")

# ---------- v3 (25/11 17h): o problema medido é chiado/ambiente alto em relação à fala no gancho e no CTA ----------
# (pausa vs fala nos agudos: gancho −14 a −19 dB, body −31 dB). Cadeia: corta ronco → tira o chiado (spectral gating,
# perfil das pausas do próprio trecho) → EQ 1/3 de oitava casada SÓ nos trechos de fala com o body → de-esser → compressão leve.
def tratar(src, a, b, out, alvo_fala, prop=0.85, comp=1.6, gate_db=10, sr=48000):
    import noisereduce as nrd, soundfile as sf
    x = wav(src, a, b); x = ff(x, "highpass=f=100,highpass=f=100")
    w = int(sr*.03); fr = [x[i:i+w] for i in range(0, len(x)-w, w)]; r = np.array([np.sqrt(np.mean(f**2)) for f in fr])
    ruido = np.concatenate([f for f, v in zip(fr, r) if v <= np.percentile(r, 10)])
    y = nrd.reduce_noise(y=x, sr=sr, y_noise=ruido, stationary=True, prop_decrease=prop, n_fft=2048, time_mask_smooth_ms=60, freq_mask_smooth_hz=300)
    eq = eq3_fala(y, alvo_fala); y = ff(y, eq)
    y = ff(y, f"deesser=i=0.3:m=0.5:f=0.5,acompressor=threshold=-26dB:ratio={comp}:attack=10:release=150:makeup=1")
    if gate_db:   # expansor: abaixa só o ambiente entre as palavras (até gate_db), sem mexer na fala
        w2 = int(sr*.03); rr = np.array([20*np.log10(np.sqrt(np.mean(y[i:i+w2]**2))+1e-9) for i in range(0, len(y)-w2, w2)])
        thr = 10 ** ((np.percentile(rr, 25) + 3) / 20) / (np.abs(y).max() + 1e-9)
        y = y / (np.abs(y).max() + 1e-9)
        y = ff(y, f"agate=threshold={thr:.5f}:range={10**(-gate_db/20):.3f}:ratio=2.5:attack=4:release=140:knee=3:detection=rms")
    y = y / (np.abs(y).max() + 1e-9) * 0.7
    sf.write(out, np.stack([y, y], 1), sr); return eq
def alvo_body(src, a=16, b=42): return bandas3(so_fala(wav(src, a, b)))
