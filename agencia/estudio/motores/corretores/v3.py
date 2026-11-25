#!/usr/bin/env python3
"""Motor v3 dos Corretores (25/11) — regra nova do Léo:
- body = trecho de criativo PRONTO que já vendeu, usado como está (vídeo, legenda, música e voz intactos; sem EQ, sem emenda de takes);
- motion só no gancho/CTA, texto em Poppins caixa normal (nada de legenda "quadrada"), cores do Mapa (navy/teal/coral, não azul de fundo);
- sem preço; transição forte (zoom + blur + flash) nos cortes; efeitos sonoros sutis.
"""
import subprocess, json, os, math, tempfile, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
F = "/home/claude/corretores/fontes/"
NAVY, TEAL, CORAL, BRANCO = (14, 42, 84), (16, 150, 128), (226, 76, 60), (255, 255, 255)
U = "/mnt/user-data/uploads/Corretores/"
TRAB = U + "Criativos prontos/ESTUDIO 23-11/_trabalho/"
DD = U + "Creative Lab/Ana Paula/PRONTOS/DD/"
_fc = {}
def fonte(peso, tam):
    k = (peso, tam)
    if k not in _fc: _fc[k] = ImageFont.truetype(F + f"poppins-latin-{peso}-normal.ttf", tam)
    return _fc[k]
def ease(x): x = min(1, max(0, x)); return 1 - (1 - x) ** 3
def mola(x):
    x = min(1, max(0, x))
    return 1 - math.cos(x * math.pi * 2.2) * math.exp(-5.5 * x)

class Seg:
    def __init__(self, src, t0, dur, vf="", audio=True, zoom=1.0, fx=None, fade_out=0.012):
        self.src, self.t0, self.dur, self.vf, self.audio, self.zoom, self.fx, self.fade_out = src, t0, dur, vf, audio, zoom, fx, fade_out

def ler(seg):
    """Gera quadros RGB 1080x1920 de um trecho (com filtro opcional)."""
    vf = f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
    if seg.zoom != 1.0: vf += f",scale=iw*{seg.zoom}:ih*{seg.zoom},crop={W}:{H}"
    if seg.vf: vf += "," + seg.vf
    n = round(seg.dur * FPS)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{seg.t0:.3f}", "-i", seg.src, "-t", f"{seg.dur + 0.5:.3f}",
                          "-vf", vf, "-pix_fmt", "rgb24", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    last = None
    for i in range(n):
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3: b = last
        last = b
        yield Image.frombuffer("RGB", (W, H), b, "raw", "RGB", 0, 1)
    p.stdout.close(); p.wait()

def loud(arq):
    r = subprocess.run(["ffmpeg", "-nostats", "-i", arq, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r)
    return float(m[-1])

def sfx_pop(sr=48000):
    t = np.arange(int(0.09 * sr)) / sr
    f = 900 * np.exp(-t * 18) + 280
    s = np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-t * 38)
    return s * 0.5
def sfx_whoosh(sr=48000, dur=0.32):
    n = int(dur * sr); rng = np.random.default_rng(3); x = rng.standard_normal(n)
    env = np.sin(np.linspace(0, np.pi, n)) ** 2
    # filtro passa-banda que sobe (varredura) — ruído suave, sem cara de sintetizado
    out = np.zeros(n); y1 = y2 = 0.0
    for i in range(n):
        fc = 300 + 2200 * (i / n)
        a = math.exp(-2 * math.pi * fc / sr)
        y1 = (1 - a) * x[i] + a * y1; y2 = (1 - a) * y1 + a * y2
        out[i] = y1 - y2
    out = out / (np.abs(out).max() + 1e-9)
    return out * env * 0.55

def montar_audio(segs, sfx, saida, alvo=-14.0):
    """Cada trecho de áudio entra como veio (só ganho linear pro mesmo LUFS + fade de 12 ms nas pontas)."""
    tmp = tempfile.mkdtemp()
    partes = []
    for i, s in enumerate(segs):
        a = f"{tmp}/a{i}.wav"
        if s.audio:
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s.t0:.3f}", "-t", f"{s.dur:.3f}", "-i", s.src, "-vn", "-ac", "2", "-ar", "48000", a], check=True)
            g = alvo - loud(a)
            b = f"{tmp}/b{i}.wav"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a, "-af",
                            f"volume={g:.2f}dB,afade=t=in:d=0.012,afade=t=out:st={s.dur - s.fade_out:.3f}:d={s.fade_out:.3f},apad=whole_dur={s.dur:.3f},atrim=0:{s.dur:.3f}", b], check=True)
        else:
            b = f"{tmp}/b{i}.wav"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo", "-t", f"{s.dur:.3f}", b], check=True)
        partes.append(b)
    import soundfile as sf
    voz = np.concatenate([sf.read(p)[0] for p in partes], axis=0)
    for t, kind, db in sfx:
        x = sfx_pop() if kind == "pop" else sfx_whoosh()
        x = x * (10 ** (db / 20)); i0 = int(t * 48000)
        e = min(len(voz), i0 + len(x)) - i0
        if e > 0: voz[i0:i0 + e] += x[:e, None]
    sf.write(f"{tmp}/mix.wav", voz, 48000)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{tmp}/mix.wav", "-af", "alimiter=limit=0.84:level=false", "-ar", "48000", saida], check=True)

def transicao(img, dt):
    """Corte com punch: dt = tempo desde o corte (negativo = antes). Zoom + blur + flash curtinho."""
    a = abs(dt)
    if a > 0.17: return img
    k = 1 - a / 0.17
    z = 1 + 0.10 * k
    w2, h2 = int(W * z), int(H * z)
    im = img.resize((w2, h2), Image.BILINEAR).crop(((w2 - W) // 2, (h2 - H) // 2, (w2 - W) // 2 + W, (h2 - H) // 2 + H))
    im = im.filter(ImageFilter.GaussianBlur(14 * k))
    if a < 0.05:
        im = Image.blend(im, Image.new("RGB", (W, H), BRANCO), 0.35 * (1 - a / 0.05))
    return im

def render(segs, overlays, cortes_fx, sfx, saida, audio_segs=None, cam=None):
    tmp = tempfile.mkdtemp(); aud = f"{tmp}/aud.wav"
    montar_audio(audio_segs or segs, sfx, aud)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-i", aud, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", saida], stdin=subprocess.PIPE)
    fr = 0
    for s in segs:
        for i_s, img in enumerate(ler(s)):
            t = fr / FPS
            if s.fx: img = s.fx(img, s.t0 + i_s / FPS)
            if cam:
                z = cam(t)
                if z > 1.0005:
                    w2, h2 = int(W * z), int(H * z)
                    img = img.resize((w2, h2), Image.BILINEAR).crop(((w2 - W) // 2, (h2 - H) // 2, (w2 - W) // 2 + W, (h2 - H) // 2 + H))
            img = img.convert("RGBA")
            for ov in overlays: ov(img, t)
            img = img.convert("RGB")
            for c in cortes_fx: img = transicao(img, t - c)
            enc.stdin.write(img.tobytes()); fr += 1
    enc.stdin.close(); enc.wait()
    return fr / FPS

# ---------- elementos ----------
def caixa(img, x0, y0, x1, y1, r, cor, alpha=1.0, sombra=True):
    if alpha <= 0: return
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    if sombra:
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((x0, y0 + 10, x1, y1 + 10), r, fill=(0, 0, 0, int(90 * alpha)))
        img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)))
    d.rounded_rectangle((x0, y0, x1, y1), r, fill=cor + (int(255 * alpha),))
    img.alpha_composite(lay)

def texto(img, xy, s, peso, tam, cor, alpha=1.0, anchor="la"):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).text(xy, s, font=fonte(peso, tam), fill=cor + (int(255 * alpha),), anchor=anchor)
    img.alpha_composite(lay)

ICON = "/home/claude/icons/png/"
_ic = {}
def icone(img, nome, cx, cy, tam, alpha=1.0):
    k = (nome, tam)
    if k not in _ic: _ic[k] = Image.open(ICON + nome + ".png").convert("RGBA").resize((tam, tam), Image.LANCZOS)
    ic = _ic[k]
    if alpha < 1:
        ic = ic.copy(); a = ic.getchannel("A").point(lambda v: int(v * alpha)); ic.putalpha(a)
    img.alpha_composite(ic, (int(cx - tam / 2), int(cy - tam / 2)))

def disco(img, cx, cy, r, cor, alpha=1.0, sombra=True):
    if alpha <= 0: return
    if sombra:
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse((cx - r, cy - r + 8, cx + r, cy + r + 8), fill=(0, 0, 0, int(80 * alpha)))
        img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).ellipse((cx - r, cy - r, cx + r, cy + r), fill=cor + (int(255 * alpha),))
    img.alpha_composite(lay)

def particulas(img, cx, cy, t, cores=(TEAL, CORAL, (255, 214, 10)), n=12, raio=170, seed=1):
    """Estouro de partículas (0 ≤ t ≤ 0.6 s)."""
    if not (0 <= t <= 0.6): return
    rng = np.random.default_rng(seed); lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    p = ease(t / 0.6); a = 1 - t / 0.6
    for i in range(n):
        ang = 2 * math.pi * i / n + rng.uniform(-0.2, 0.2); rr = raio * p * rng.uniform(0.7, 1.1)
        x, y = cx + math.cos(ang) * rr, cy + math.sin(ang) * rr; s = 9 * (1 - 0.5 * p)
        c = cores[i % len(cores)]
        d.ellipse((x - s, y - s, x + s, y + s), fill=c + (int(255 * a),))
    img.alpha_composite(lay)

def quebra(s, peso, tam, larg):
    d = ImageDraw.Draw(Image.new("RGB", (1, 1))); out, cur = [], ""
    for w in s.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fonte(peso, tam)) <= larg: cur = t
        else: out.append(cur); cur = w
    out.append(cur); return out
