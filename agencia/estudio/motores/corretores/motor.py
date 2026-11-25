#!/usr/bin/env python3
"""Motor comum das variações B/C dos Corretores (24/11). Mesma lógica dos pilotos est5.py / est2.py / est4.py:
recortes 1080x1920 feitos no PC do Léo, overlays em PIL, legenda palavra por palavra (palavra ativa amarela),
voz só da Ana Paula, loudnorm -14 LUFS (2 passadas), selo R$27,90 no CTA.
Novidade: o início de cada grupo da legenda é preso ao fim da pausa real mais próxima (librosa), e os cortes de
áudio caem em silêncio (os pontos a/b de cada fala são escolhidos dentro das pausas medidas).
"""
import os, subprocess, json, math, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

U = "/mnt/user-data/uploads/Corretores/Criativos prontos/ESTUDIO 23-11/_trabalho/"
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fontes/")
W, H, FPS = 1080, 1920, 30
AMARELO = (255, 214, 10); NAVY, TEAL = (14, 42, 84), (18, 160, 140)
TERRA, TEAL2, VERDE = (214, 88, 40), (16, 150, 128), (11, 79, 58)

@functools.lru_cache(None)
def fonte(peso, tam):
    return ImageFont.truetype(F + f"poppins-latin-{peso}-normal.ttf", tam)

# ---------------- pausas (librosa) ----------------
@functools.lru_cache(None)
def pausas(arq, thr_db=-24, min_len=0.05):
    import librosa
    if not arq.lower().endswith(".wav"):
        w = "/tmp/_p_" + os.path.basename(arq) + ".wav"
        if not os.path.exists(w): subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", arq, "-vn", "-ac", "1", "-ar", "16000", w], check=True)
        arq = w
    y, sr = librosa.load(arq, sr=16000)
    hop = 160; rms = librosa.feature.rms(y=y, frame_length=640, hop_length=hop)[0]
    db = 20 * np.log10(rms / (rms.max() + 1e-9) + 1e-9); sil = db < thr_db
    out, i, n = [], 0, len(sil)
    while i < n:
        if sil[i]:
            j = i
            while j < n and sil[j]: j += 1
            if (j - i) * hop / sr >= min_len: out.append((i * hop / sr, j * hop / sr))
            i = j
        else: i += 1
    return tuple(out)

def prende(arq, t, antes=0.35, depois=0.25):
    """Se houver fim de pausa em [t-antes, t+depois], devolve esse instante (início real da fala)."""
    cands = [b for a, b in pausas(arq) if t - antes <= b <= t + depois]
    return min(cands, key=lambda b: abs(b - t)) if cands else t

# ---------------- peça ----------------
class Peca:
    XF = 0.04   # crossfade entre takes (s)
    def __init__(self, out, leg_y=1290, leg_y_cta=330, leg_y_split=1440, preco_y=430, preco_wh=(440, 128), preco_fz=64, chips_y=(800, 1030)):
        assert not (900 - 50 < leg_y_split < 1010 + 50), "legenda nunca na divisória do split"
        self.chips_y = chips_y
        self.out = out; self.t = 0.0; self.aud = []; self.leg = []; self.vid = []; self.ov = []
        self.leg_y, self.leg_y_cta, self.leg_y_split = leg_y, leg_y_cta, leg_y_split
        self.preco_y, self.preco_wh, self.preco_fz = preco_y, preco_wh, preco_fz
        self.cta_ini = 1e9; self.split_fim = -1

    # fala: src = arquivo de áudio (wav/mov); [a,b] = trecho no arquivo (cortes em silêncio);
    # grupos = [(texto, t_ref)] ou [(texto, [t_ref por palavra])]; off: t_arquivo = t_ref + off; fim_ref = fim do último grupo
    def fala(self, src, a, b, grupos, off=0.0, fim_ref=None, gap=None, cta=False):
        if gap is None: gap = -self.XF if self.aud else 0.0
        pos = max(0.0, self.t + gap)
        self.aud.append((src, a, b, pos))
        self.leg = [(x0, min(x1, max(x0 + 0.05, pos)), g, ts) for x0, x1, g, ts in self.leg]
        if cta: self.cta_ini = pos
        conv = lambda s: pos + (s - a)
        gs = []
        for txt, tr in grupos:
            pal = txt.split()
            if isinstance(tr, (list, tuple)):
                ts = [x + off for x in tr]; assert len(ts) == len(pal), txt
            else:
                ts = [tr + off]
            ts[0] = max(a, prende(src, ts[0]))
            gs.append([txt, ts])
        for k in range(1, len(gs)):          # garante ordem
            gs[k][1][0] = max(gs[k][1][0], gs[k - 1][1][-1] + 0.05)
        fim = min(b, (fim_ref + off) if fim_ref is not None else b)
        for k, (txt, ts) in enumerate(gs):
            fim_g = gs[k + 1][1][0] if k + 1 < len(gs) else fim
            self.leg.append((conv(ts[0]), conv(fim_g), txt, [conv(x) for x in ts] if len(ts) > 1 else None))
        self.t = pos + (b - a)
        return pos

    def silencio(self, d): self.t += d

    # vídeo: clipes em sequência (devem somar a duração do áudio)
    def clipe(self, arq, ini, dur, zoom=1.0, vel=1.0, ycrop=None):
        self.vid.append(("c", arq, ini, dur, zoom, vel, ycrop))
    def split(self, cima, baixo, dur, chip_cima, chip_baixo):
        self.vid.append(("s", cima, baixo, dur, chip_cima, chip_baixo))
        self.split_fim = sum(v[3] for v in self.vid)

    # ---------------- overlays ----------------
    def legenda(self, img, t):
        for a, b, txt, ts in self.leg:
            if a <= t < b: break
        else: return
        d = ImageDraw.Draw(img); pal = txt.split()
        if ts: ativa = max(0, int(np.searchsorted(np.array(ts), t, side='right')) - 1)
        else:
            pesos = np.array([len(p) for p in pal], float); lim = a + (b - a) * np.cumsum(pesos) / pesos.sum()
            ativa = int(np.searchsorted(lim, t, side='right'))
        ativa = min(ativa, len(pal) - 1)
        cy = self.leg_y_split if t < self.split_fim else (self.leg_y_cta if t >= self.cta_ini else self.leg_y)
        fz = 66
        while True:
            fl = fonte(800, fz); esp = d.textlength(" ", font=fl)
            larg = sum(d.textlength(p, font=fl) for p in pal) + esp * (len(pal) - 1)
            if larg <= 800 or fz <= 50: break
            fz -= 2
        x = (W - larg) / 2
        for i, p in enumerate(pal):
            d.text((x, cy), p, font=fl, fill=AMARELO if i == ativa else (255, 255, 255), anchor="lm", stroke_width=7, stroke_fill=(0, 0, 0))
            x += d.textlength(p, font=fl) + esp

    def preco(self, img, t):
        if t < self.cta_ini + 2.6: return
        k = min(1, (t - self.cta_ini - 2.6) / 0.3); a = int(255 * k)
        d = ImageDraw.Draw(img, "RGBA"); w, h = self.preco_wh; x0 = (W - w) // 2; y0 = self.preco_y + int((1 - k) * 30)
        d.rounded_rectangle((x0, y0, x0 + w, y0 + h), radius=64, fill=VERDE + (a,))
        d.text((W / 2, y0 + h / 2 - 2), "R$27,90", font=fonte(800, self.preco_fz), fill=(255, 255, 255, a), anchor="mm")

# texto da história no topo (EST5): cards = [(ini, fim, "linha1\nlinha2")]; quebra manual; fonte encolhe por igual até caber em 800 px
def historia(cards):
    def f(img, t):
        for a, b, txt in cards:
            if a <= t < b: break
        else: return
        grad = Image.new("L", (W, 620)); grad.putdata(np.repeat(np.linspace(170, 0, 620).astype(np.uint8), W).tolist())
        img.paste(Image.new("RGB", (W, 620), (0, 0, 0)), (0, 0), grad)
        d = ImageDraw.Draw(img); linhas = txt.split("\n"); fz = 78
        while max(d.textlength(l, font=fonte(800, fz)) for l in linhas) > 800: fz -= 1
        k = min(1, (t - a) / 0.25); y = 250 + int((1 - k) * 24); fl = fonte(800, fz)
        for ln in linhas:
            d.text((W / 2, y), ln, font=fl, fill=(255, 255, 255), anchor="mm", stroke_width=3, stroke_fill=(0, 0, 0))
            y += int(fz * 1.28)
    return f

# cartão de quiz no topo (EST2): cards = [(ini, fim, contador, texto, respondida)]
def quiz(cards):
    def f(img, t):
        for a, b, cont, txt, ok in cards:
            if a <= t < b: break
        else: return
        x0, y0, w, h = 140, 170, 800, 150
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((x0, y0 + 10, x0 + w, y0 + h + 10), radius=36, fill=(0, 0, 0, 90))
        sh = sh.filter(ImageFilter.GaussianBlur(14)); img.paste(sh, (0, 0), sh)
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle((x0, y0, x0 + w, y0 + h), radius=36, fill=(255, 255, 255, 250))
        tx = x0 + 40
        if cont:
            d.rounded_rectangle((x0 + 30, y0 + 40, x0 + 150, y0 + 110), radius=35, fill=TEAL if ok else NAVY)
            d.text((x0 + 90, y0 + 75), cont, font=fonte(800, 38), fill="white", anchor="mm"); tx = x0 + 175
        txt_w = x0 + w - 40 - tx - (90 if cont else 0)
        fz = 46
        if d.textlength(txt, font=fonte(800, fz)) <= txt_w:
            d.text((tx, y0 + h / 2), txt, font=fonte(800, fz), fill=NAVY, anchor="lm")
        else:   # pergunta longa: 2 linhas equilibradas (nada de fonte miúda)
            pal = txt.split(); cortes = sorted(range(1, len(pal)), key=lambda k: abs(len(" ".join(pal[:k])) - len(" ".join(pal[k:]))))
            l1, l2 = " ".join(pal[:cortes[0]]), " ".join(pal[cortes[0]:]); fz = 42
            while max(d.textlength(l1, font=fonte(800, fz)), d.textlength(l2, font=fonte(800, fz))) > txt_w and fz > 30: fz -= 2
            d.text((tx, y0 + h / 2 - fz * 0.62), l1, font=fonte(800, fz), fill=NAVY, anchor="lm")
            d.text((tx, y0 + h / 2 + fz * 0.62), l2, font=fonte(800, fz), fill=NAVY, anchor="lm")
        cx, cy, r = x0 + w - 75, y0 + h / 2, 32
        if cont and not ok:
            p = (t - a) / (b - a)
            d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(220, 226, 236), width=9)
            d.arc((cx - r, cy - r, cx + r, cy + r), start=-90, end=-90 + 360 * (1 - p), fill=(230, 120, 60), width=9)
            d.text((cx, cy), str(max(1, math.ceil(b - t))), font=fonte(800, 38), fill=NAVY, anchor="mm")
        if cont and ok:
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=TEAL)
            d.line((cx - 14, cy + 1, cx - 4, cy + 12, cx + 15, cy - 11), fill="white", width=8, joint="curve")
    return f

def chip(d, y, txt, cor, icone):
    fz = 40
    while d.textlength(txt, font=fonte(800, fz)) + 130 > 800: fz -= 1
    fl = fonte(800, fz); w = d.textlength(txt, font=fl) + 130; x0 = (W - w) / 2
    d.rounded_rectangle((x0, y, x0 + w, y + 84), radius=42, fill=cor)
    cx, cy = x0 + 50, y + 42
    d.ellipse((cx - 24, cy - 24, cx + 24, cy + 24), fill="white")
    if icone == "x":
        d.line((cx - 10, cy - 10, cx + 10, cy + 10), fill=cor, width=7); d.line((cx - 10, cy + 10, cx + 10, cy - 10), fill=cor, width=7)
    else:
        d.line((cx - 11, cy + 1, cx - 3, cy + 10, cx + 12, cy - 9), fill=cor, width=7, joint="curve")
    d.text((x0 + 88, cy), txt, font=fl, fill="white", anchor="lm")

# ---------------- leitura de quadros ----------------
def tablet_pdf(n_pag, n, fundo, y0=150, larg=720):
    """Página n_pag do PDF do Mapa (nítida, inteira) num tablet desenhado, com aproximação lenta (nunca fica parada)."""
    pag = Image.open(f"/home/claude/corretores/novo/pag/p-{n_pag:03d}.png").convert("RGB")
    alt = round(larg * pag.height / pag.width); bz = 28; dw, dh = larg + 2 * bz, alt + 2 * bz; x0 = (W - dw) // 2
    pag = pag.resize((larg, alt), Image.LANCZOS)
    mask = Image.new("L", (larg, alt), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, larg - 1, alt - 1), radius=16, fill=255)
    base = fundo.copy()
    sh = Image.new("L", (W, H), 0); ImageDraw.Draw(sh).rounded_rectangle((x0, y0 + 22, x0 + dw, y0 + dh + 22), radius=52, fill=150)
    base.paste(Image.new("RGB", (W, H), (0, 0, 0)), (0, 0), sh.filter(ImageFilter.GaussianBlur(28)))
    d = ImageDraw.Draw(base); d.rounded_rectangle((x0, y0, x0 + dw, y0 + dh), radius=52, fill=(18, 20, 26))
    d.rounded_rectangle((x0 + 3, y0 + 3, x0 + dw - 3, y0 + dh - 3), radius=50, outline=(70, 74, 84), width=3)
    base.paste(pag, (x0 + bz, y0 + bz), mask)
    cy = y0 + dh / 2
    for i in range(n):
        z = 1 + 0.03 * i / max(1, n - 1); w2, h2 = round(W * z), round(H * z)
        im = base.resize((w2, h2), Image.BILINEAR); oy = int(cy * z - cy)
        yield im.crop(((w2 - W) // 2, oy, (w2 - W) // 2 + W, oy + H))

def leitor(arq, ini, dur, zoom=1.0, vel=1.0):
    if arq.startswith("tablet:"):
        fr = subprocess.run(["ffmpeg", "-loglevel", "quiet", "-ss", "0.5", "-i", U + "cortes4/ip_faixas2.mp4", "-frames:v", "1", "-vf", f"scale={W}:{H}",
                             "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        fundo = Image.frombytes("RGB", (W, H), fr).resize((W // 10, H // 10)).filter(ImageFilter.GaussianBlur(5)).resize((W, H))
        fundo = Image.eval(fundo, lambda v: int(v * 0.5))
        p = [int(x) for x in arq.split(":")[1:]]   # tablet:pagina[:topo:largura]
        yield from tablet_pdf(p[0], int(round(dur * FPS)), fundo, *p[1:]); return
    if arq.endswith(".png"):   # página impressa estável (quadro nítido com as duas margens): zoom final <= 1,0
        assert zoom <= 0.97, "página impressa: zoom final no máximo 1,0"
        base = Image.open(arq).convert("RGB").resize((W, H), Image.LANCZOS); n = int(round(dur * FPS))
        bg = base.resize((W // 8, H // 8)).filter(ImageFilter.GaussianBlur(6)).resize((W, H)); bg = Image.eval(bg, lambda v: int(v * 0.55))
        for i in range(n):
            s = zoom * (1 + 0.03 * i / max(1, n - 1)); w2, h2 = int(W * s), int(H * s)
            fr = bg.copy(); fr.paste(base.resize((w2, h2), Image.LANCZOS), ((W - w2) // 2, (H - h2) // 2)); yield fr
        return
    cmd = ["ffmpeg", "-loglevel", "quiet", "-ss", str(ini), "-t", str(dur * vel + 0.3), "-i", arq,
           "-vf", f"setpts=PTS/{vel},fps={FPS},scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE); n = int(round(dur * FPS)); im = None
    for i in range(n):
        buf = p.stdout.read(W * H * 3)
        if len(buf) == W * H * 3: im = Image.frombytes("RGB", (W, H), buf)
        assert im is not None, arq
        if zoom < 1.0:
            s = zoom * (1 + 0.03 * i / max(1, n - 1)); w2, h2 = int(W * s), int(H * s)
            bg = im.resize((W // 8, H // 8)).filter(ImageFilter.GaussianBlur(6)).resize((W, H)); bg = Image.eval(bg, lambda v: int(v * 0.55))
            bg.paste(im.resize((w2, h2), Image.LANCZOS), ((W - w2) // 2, (H - h2) // 2)); yield bg
        elif zoom != 1.0:
            s = 1 + (zoom - 1) * i / max(1, n - 1); cw, ch = W / s, H / s
            yield im.crop(((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2)).resize((W, H), Image.LANCZOS)
        else: yield im.copy()
    p.kill(); p.wait()

def metade(lista):
    for arq, ini, dur, y, *v in lista:     # 5º campo opcional: velocidade
        for im in leitor(arq, ini, dur, 1.0, v[0] if v else 1.0):
            yield im.crop((0, y, W, y + 960))

# ---------------- render ----------------
def render(pc, overlays=()):
    total = pc.t
    vdur = sum(v[3] for v in pc.vid)
    assert abs(vdur - total) < 0.04, f"vídeo {vdur:.3f}s x áudio {total:.3f}s"
    tmpv = f"/tmp/{os.path.basename(pc.out)}.v.mp4"
    enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", tmpv], stdin=subprocess.PIPE)
    fr = 0; nalvo = 0.0
    for v in pc.vid:
        nalvo += v[3]; n = int(round(nalvo * FPS)) - fr
        if v[0] == "c":
            _, arq, ini, dur, z, vel, yc = v
            gen = leitor(arq, ini, n / FPS, z, vel)
        else:
            _, cima, baixo, dur, cc, cb = v
            def gen_split(cima=cima, baixo=baixo, cc=cc, cb=cb, n=n):
                for k, (a, b) in enumerate(zip(metade(cima), metade(baixo))):
                    if k >= n: break
                    im = Image.new("RGB", (W, H)); im.paste(a, (0, 0)); im.paste(b, (0, 960))
                    d = ImageDraw.Draw(im); d.rectangle((0, 955, W, 965), fill="white")
                    chip(d, pc.chips_y[0], cc, TERRA, "x"); chip(d, pc.chips_y[1], cb, TEAL2, "v")
                    yield im
            gen = gen_split()
        k = 0
        for im in gen:
            t = fr / FPS
            for o in overlays: o(im, t)
            pc.legenda(im, t); pc.preco(im, t)
            enc.stdin.write(im.tobytes()); fr += 1; k += 1
        assert k == n, (v[:3], k, n)
    enc.stdin.close(); enc.wait()
    # áudio: trechos posicionados, micro-fades nos cortes (todos em silêncio), 2 passadas de loudnorm em -14 LUFS
    ins, filt, labs = [], [], []
    for j, (src, a, b, pos) in enumerate(pc.aud):
        ins += ["-i", src]; d = b - a
        xf = pc.XF
        filt.append(f"[{j}:a]atrim=start={a:.3f}:end={b:.3f},asetpts=PTS-STARTPTS,aresample=48000,pan=mono|c0=c0,"
                    f"afade=t=in:d={xf}:curve=qsin,afade=t=out:st={d - xf:.3f}:d={xf}:curve=qsin,adelay={int(round(pos * 1000))}[a{j}]")
        labs.append(f"[a{j}]")
    # leito: som ambiente real da sala (trecho sem fala do HOOK5 pt2, 7,60–8,25 s) em loop por baixo da peça inteira
    k = len(pc.aud); ins += ["-i", U + "aud/B_HOOK5_pt_2.wav"]
    filt.append(f"[{k}:a]atrim=start=7.60:end=8.25,asetpts=PTS-STARTPTS,aresample=48000,pan=mono|c0=c0,aloop=loop=-1:size=31200,"
                f"atrim=0:{total:.3f},volume=0.7[bed]"); labs.append("[bed]")
    base = ";".join(filt) + ";" + "".join(labs) + f"amix=inputs={len(labs)}:normalize=0:duration=longest,highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,apad=whole_dur={total:.3f},atrim=0:{total:.3f}"
    mix = f"/tmp/{os.path.basename(pc.out)}.mix.wav"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y"] + ins + ["-filter_complex", base + "[m]", "-map", "[m]", "-ar", "48000", mix], check=True)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", mix, "-af", "loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
    js = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=9:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:"
          f"measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmpv, "-i", mix, "-filter_complex", f"[1:a]{ln},aresample=48000[aout]",
                    "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                    "-t", f"{total:.3f}", "-movflags", "+faststart", pc.out], check=True)
    print("ok", pc.out, f"{total:.2f}s", fr, "quadros")

def folha(mp4, jpg, passo=0.5, cols=7, larg=216):
    """Folha de frames a cada `passo` s, com o tempo em cada quadro (revisão obrigatória)."""
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4], capture_output=True, text=True).stdout)
    n = int(dur / passo) + 1; rows = math.ceil(n / cols)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", mp4, "-vf",
                    f"fps=1/{passo},scale={larg}:-2,drawtext=fontfile={F}poppins-latin-700-normal.ttf:text='%{{pts\\:flt}}':x=4:y=4:fontsize=16:fontcolor=white:box=1:boxcolor=black@0.6,tile={cols}x{rows}:padding=2",
                    "-frames:v", "1", "-update", "1", jpg.replace(".jpg", ".png")], check=True)
    Image.open(jpg.replace(".jpg", ".png")).convert("RGB").save(jpg, quality=88); os.remove(jpg.replace(".jpg", ".png"))

def lufs(mp4):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", mp4, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    s = r.stderr[r.stderr.rindex("Summary:"):]
    return " ".join(s.split())

def t_de(pc, txt, depois=0.0):
    """Início (na peça) do primeiro grupo da legenda que começa com `txt`, a partir de `depois`."""
    for a, b, g, ts in pc.leg:
        if a >= depois and g.startswith(txt): return a
    raise KeyError(txt)

# falas reutilizadas (tempos de referência dos prontos; ver est4.py / est5.py / est2.py)
G_HOOK5_1 = [("CORRETOR,", 0.2), ("QUANTO MAIS VOCÊ", 1.0), ("ENTENDE A OPERAÇÃO", 1.6), ("QUE VOCÊ ESTÁ", 2.6), ("CONDUZINDO,", 3.0),
             ("MAIS SEGURANÇA VOCÊ", 4.2), ("CONSEGUE PASSAR", 5.2), ("PRO SEU CLIENTE", 5.8), ("NA HORA DO", 6.8), ("FECHAMENTO.", 7.4)]   # bruto = ref + 0,51; fim 7,95
G_HOOK5_2 = [("ENTÃO DÁ UMA", 8.0), ("OLHADA NESSE MATERIAL", 8.6), ("AQUI,", 9.6), ("QUE FOI JUSTAMENTE", 10.0), ("CRIADO PRA AMPLIAR", 10.8),
             ("ESSE SEU REPERTÓRIO", 12.0), ("E TORNAR O", 12.8), ("ATENDIMENTO MUITO MAIS", 13.6), ("PROFISSIONAL.", 14.6)]           # bruto = ref − 7,43; fim 15,1
# HOOK3 (AP DD 7): tempos por palavra lidos nas tiras da legenda do pronto; bruto = DD7 + 0,333 (correlação de áudio)
G_HOOK3 = [("VOCÊ,", 0.2), ("CORRETOR QUE SENTE", [0.6, 1.2, 1.4]), ("QUE AINDA NÃO", [1.7, 1.8, 2.0]), ("DOMINA ASSUNTOS COMO:", [2.2, 2.6, 3.0]),
           ("FGTS,", 3.6), ("MINHA CASA", [4.6, 4.8]), ("MINHA VIDA,", [5.2, 5.4]), ("CONSÓRCIO,", 5.8), ("DOCUMENTAÇÃO,", 6.6),
           ("DÁ UMA OLHADA", [7.6, 7.8, 8.0]), ("NESSE MATERIAL AQUI.", [8.4, 8.6, 9.2])]                                                  # fim 9,5
# HOOK2 (AP DD 5): bruto = DD5 (correlação de áudio)
G_HOOK2 = [("SE VOCÊ É", [0.0, 0.4, 0.6]), ("CORRETOR E ENTENDE", [0.8, 1.2, 1.4]), ("QUE AINDA NÃO", [1.8, 2.0, 2.2]), ("DOMINA OS", [2.4, 2.8]),
           ("DIFERENTES TIPOS", [3.0, 3.6]), ("DE AQUISIÇÃO", [3.8, 4.0]), ("DE IMÓVEL,", [4.6, 4.8]), ("DÁ UMA OLHADA", [5.4, 5.6, 5.8]),
           ("NESSE MATERIAL AQUI.", [6.2, 6.4, 6.8])]                                                                                     # fim 7,2
# corpo dela (AP DD 2), tempos no arquivo cortes2/dd2_body.wav
G_BODY = [("SÃO +120 MAPAS", 1.34), ("VISUAIS,", 3.2), ("CLAROS E OBJETIVOS,", 3.6), ("SOBRE FGTS,", 5.76), ("MINHA CASA", 7.2),
          ("MINHA VIDA,", 7.6), ("CONSÓRCIO,", 8.4), ("DOCUMENTAÇÃO.", 9.2)]                                                              # fim 10,08
# CTA 2de2 aposentado em 24/11 ("e tem acesso", concordância): só CTA 4de4
G_CTA4 = [("CLIQUE EM", [0.0, 0.4]), ("SAIBA MAIS", [0.6, 1.0]), ("E TENHA ACESSO", [1.2, 1.4, 1.6]), ("VITALÍCIO", 2.0), ("AO SEU MAPA", [2.8, 3.0, 3.2]),
          ("VISUAL COMPLETO", [3.6, 4.2]), ("DO FECHAMENTO", [4.6, 4.8]), ("IMOBILIÁRIO.", 5.4)]  # fim 5,9 · cta4.mov = DD5_fim − 7,6
# HOOK1 (AP DD 10): bruto pt1 = DD10 + 0,49; pt2 = DD10 − 6,855
G_HOOK1_1 = [("SE VOCÊ QUER", 0.0), ("SER O CORRETOR", 0.8), ("QUE SABE RESPONDER", 1.6), ("QUANDO A NEGOCIAÇÃO", 2.8), ("SAI DO BÁSICO,", 3.6),
             ("VOCÊ PRECISA DOMINAR", 4.8), ("MUITO MAIS DO", 6.0), ("QUE APENAS A", 6.4), ("VENDA.", 7.2)]   # fim 7,6
G_HOOK1_2 = [("E DÁ UMA", 7.6), ("OLHADA NESSE MATERIAL,", 8.4), ("PORQUE ELE FOI", 9.2), ("CRIADO JUSTAMENTE", 10.0), ("PARA TE PREPARAR", 10.8),
             ("PARA OS", 12.0), ("DIFERENTES", 12.4), ("CENÁRIOS QUE PODEM", 13.2), ("ACONTECER DURANTE O", 14.0), ("FECHAMENTO.", 14.8)]  # fim 15,4
# HOOK4 (AP DD 2): tempos por palavra das tiras do DD2; hook4.mov = ref + 0,45; corte final em 11,45 s (fechamento do /k/ de "que": antes do "que eu preparei")
G_HOOK4 = [("CORRETOR,", 0.4), ("VOCÊ SABE OLHAR", [0.8, 1.0, 1.2]), ("A RENDA", [1.6, 1.8]), ("DO SEU CLIENTE", [2.2, 2.4, 2.6]),
           ("E DIZER PRA ELE", [2.8, 3.0, 3.2, 3.45]), ("QUANTO QUE ELE", [3.6, 3.8, 4.0]), ("CONSEGUE FINANCIAR,", [4.2, 4.8]),
           ("QUAL O VALOR", [5.2, 5.35, 5.45]), ("DO IMÓVEL QUE", [5.6, 6.0, 6.4]), ("ELE CONSEGUE COMPRAR", [6.6, 6.8, 7.1]),
           ("E QUANTO QUE", [7.4, 7.6, 7.8]), ("ELE VAI TER", [8.0, 8.1, 8.25]), ("QUE DAR DE", [8.4, 8.55, 8.7]), ("ENTRADA?", 8.8),
           ("SE NÃO,", 9.77), ("DÁ UMA OLHADA", [10.0, 10.2, 10.4]), ("NO MATERIAL.", [10.8, 10.95])]   # fim 11,0
CTA4, BODY = U + "cortes2/cta4.mov", U + "cortes2/dd2_body.wav"
ST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stills/")
PAG_PLANTA = ST + "planta.png"
PAG_CONSORCIO = "tablet:66"   # o quadro do impresso do consórcio saía tremido: página 66 do PDF num tablet desenhado (nítida)   # quadros de pd_consorcio (0,233 s) e pd_planta (0,0 s)
C4 = U + "cortes4/"
