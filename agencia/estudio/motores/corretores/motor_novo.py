#!/usr/bin/env python3
"""Motor dos estilos novos EST7–EST10 dos Corretores (24/11), copiado do motor.py das variações B/C.
Acrescenta: trechos em motion (quadro gerado em PIL), PIP redondo do rosto dela, páginas do PDF em alta,
legenda casada palavra a palavra com os vales de energia da voz (librosa).
Base: Mesma lógica dos pilotos est5.py / est2.py / est4.py:
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
    def __init__(self, out, leg_y=1290, leg_y_cta=330, leg_y_split=960, preco_y=430, preco_wh=(440, 128), preco_fz=64):
        self.out = out; self.t = 0.0; self.aud = []; self.leg = []; self.vid = []; self.ov = []
        self.leg_y, self.leg_y_cta, self.leg_y_split = leg_y, leg_y_cta, leg_y_split
        self.preco_y, self.preco_wh, self.preco_fz = preco_y, preco_wh, preco_fz
        self.cta_ini = 1e9; self.split_fim = -1

    # fala: src = arquivo de áudio (wav/mov); [a,b] = trecho no arquivo (cortes em silêncio);
    # grupos = [(texto, t_ref)] ou [(texto, [t_ref por palavra])]; off: t_arquivo = t_ref + off; fim_ref = fim do último grupo
    def fala(self, src, a, b, grupos, off=0.0, fim_ref=None, gap=0.0, cta=False, prender=True):
        pos = self.t + gap
        self.aud.append((src, a, b, pos))
        if cta: self.cta_ini = pos
        conv = lambda s: pos + (s - a)
        gs = []
        for txt, tr in grupos:
            pal = txt.split()
            if isinstance(tr, (list, tuple)):
                ts = [x + off for x in tr]; assert len(ts) == len(pal), txt
            else:
                ts = [tr + off]
            ts[0] = max(a, prende(src, ts[0]) if prender else ts[0])
            for j in range(1, len(ts)): ts[j] = max(ts[j], ts[j - 1] + 0.06)
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
    def motion(self, func, dur):
        """func(tl, t) -> Image RGB 1080x1920 (tl = tempo local do trecho, t = tempo na peça)."""
        self.vid.append(("m", func, 0, dur))

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
        for t0, t1, yy in getattr(self, "leg_y_trechos", []):
            if t0 <= t < t1: cy = yy
        for t0, t1 in getattr(self, "leg_oculta", []):
            if t0 <= t < t1: return
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
def leitor(arq, ini, dur, zoom=1.0, vel=1.0):
    cmd = ["ffmpeg", "-loglevel", "quiet", "-ss", str(ini), "-t", str(dur * vel + 0.3), "-i", arq,
           "-vf", f"setpts=PTS/{vel},fps={FPS},scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE); n = int(round(dur * FPS)); im = None
    for i in range(n):
        buf = p.stdout.read(W * H * 3)
        if len(buf) == W * H * 3: im = Image.frombytes("RGB", (W, H), buf)
        assert im is not None, arq
        if zoom != 1.0:
            s = 1 + (zoom - 1) * i / max(1, n - 1); cw, ch = W / s, H / s
            yield im.crop(((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2)).resize((W, H), Image.LANCZOS)
        else: yield im.copy()
    p.kill(); p.wait()

def metade(lista):
    for arq, ini, dur, y in lista:
        for im in leitor(arq, ini, dur):
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
            if callable(yc): gen = (yc(im) for im in gen)
        elif v[0] == "m":
            _, func, _z, dur = v; t_ini = fr / FPS
            def gen_m(func=func, n=n, t_ini=t_ini):
                for k in range(n): yield func(k / FPS, t_ini + k / FPS)
            gen = gen_m()
        else:
            _, cima, baixo, dur, cc, cb = v
            def gen_split(cima=cima, baixo=baixo, cc=cc, cb=cb, n=n):
                for k, (a, b) in enumerate(zip(metade(cima), metade(baixo))):
                    if k >= n: break
                    im = Image.new("RGB", (W, H)); im.paste(a, (0, 0)); im.paste(b, (0, 960))
                    d = ImageDraw.Draw(im); d.rectangle((0, 955, W, 965), fill="white")
                    chip(d, 790, cc, TERRA, "x"); chip(d, 1390, cb, TEAL2, "v")
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
    # áudio (24/11, revisão 4d): trechos posicionados com crossfade de 40 ms; nas emendas entra o som ambiente do próprio take
    # (nunca silêncio zerado); a gravação do Dia 2 recebe EQ pra casar com o timbre dos takes de câmera; 48 kHz.
    XF = 0.04
    ins, filt, labs = [], [], []
    segs = sorted(pc.aud, key=lambda x: x[3])
    def eq_de(src):
        if src in getattr(pc, "eq", {}): return "," + pc.eq[src]
        return ("," + EQ_GRAV) if src == GRAV else ""
    for j, (src, a, b, pos) in enumerate(segs):
        dfile = duracao(src); fo = getattr(pc, "fades", {}).get(j, XF)
        a2 = max(0.0, a - XF / 2); b2 = min(dfile, b + XF / 2); p2 = pos - (a - a2); d = b2 - a2
        ins += ["-i", src]; k = len(ins) // 2 - 1
        filt.append(f"[{k}:a]atrim=start={a2:.3f}:end={b2:.3f},asetpts=PTS-STARTPTS,aresample=48000,pan=mono|c0=c0{eq_de(src)},"
                    f"afade=t=in:d={getattr(pc, 'fadein', {}).get(j, XF)},afade=t=out:st={d - fo:.3f}:d={fo},adelay={int(round(max(0, p2) * 1000))}[s{j}]")
        labs.append(f"[s{j}]")
    for j in range(len(segs) - 1):     # emenda: som ambiente do take que entra, por baixo do crossfade
        src0, a0, b0, pos0 = segs[j]; src1, a1, b1, pos1 = segs[j + 1]
        fim0 = pos0 + (b0 - a0); gap = pos1 - fim0
        if gap < 0.005: continue
        rt = som_ambiente(src1); ini = max(0.0, fim0 - XF); dur = (pos1 + XF) - ini
        ins += ["-i", rt]; k = len(ins) // 2 - 1
        filt.append(f"[{k}:a]atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,aresample=48000,pan=mono|c0=c0{eq_de(src1)},"
                    f"afade=t=in:d={XF},afade=t=out:st={dur - XF:.3f}:d={XF},adelay={int(round(ini * 1000))}[r{j}]")
        labs.append(f"[r{j}]")
    base = ";".join(filt) + ";" + "".join(labs) + f"amix=inputs={len(labs)}:normalize=0,highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,apad=whole_dur={total:.3f},atrim=0:{total:.3f}"
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
G_CTA2 = [("CLIQUE EM SAIBA", 0.0), ("MAIS E TEM", 0.8), ("ACESSO VITALÍCIO", 1.4), ("AO MAPA VISUAL", 2.4), ("COMPLETO DO FECHAMENTO", 3.6), ("IMOBILIÁRIO.", 4.8)]  # fim 5,4
G_CTA4 = [("CLIQUE EM SAIBA", 0.0), ("MAIS E TENHA", 1.0), ("ACESSO VITALÍCIO", 1.6), ("AO SEU MAPA", 2.8), ("VISUAL COMPLETO DO", 3.6), ("FECHAMENTO IMOBILIÁRIO.", 4.8)]  # fim 5,9
CTA2, CTA4, BODY = U + "cortes/cta2.mov", U + "cortes2/cta4.mov", U + "cortes2/dd2_body.wav"
C4 = U + "cortes4/"


# ======================= extensões EST7–EST10 =======================
NOVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "novo/")
GRAV = NOVO + "grav.wav"          # narração do corpo do Dia 2 (voz dela, Drive "Gravação AP Dia 2.m4a")
C5 = U + "cortes5/"
CREME = (246, 241, 231)

@functools.lru_cache(None)
def energia(arq):
    import librosa
    if not arq.lower().endswith(".wav"):
        w = "/tmp/_e_" + os.path.basename(arq) + ".wav"
        if not os.path.exists(w): subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", arq, "-vn", "-ac", "1", "-ar", "16000", w], check=True)
        arq = w
    y, sr = librosa.load(arq, sr=16000)
    r = librosa.feature.rms(y=y, frame_length=400, hop_length=80)[0]
    db = 20 * np.log10(r / (r.max() + 1e-9) + 1e-9)
    return np.convolve(db, np.ones(3) / 3, "same")      # 5 ms por amostra

def vale(arq, t, antes=0.25, depois=0.2, lim=-18):
    """Vale de energia mais fundo perto de t (fronteira entre palavras); se não houver vale abaixo de `lim`, devolve t."""
    db = energia(arq); i0, i1 = max(0, int((t - antes) / 0.005)), min(len(db) - 1, int((t + depois) / 0.005))
    if i1 <= i0: return t
    k = i0 + int(np.argmin(db[i0:i1]))
    return k * 0.005 if db[k] < lim else t

SILABAS_FIXAS = {"FGTS": 4, "+120": 4, "12": 2, "ITBI": 4, "MCMV": 4}
def silabas(p):
    import re
    q = p.strip(",.;:!?").upper()
    if q in SILABAS_FIXAS: return SILABAS_FIXAS[q]
    return max(1, len(re.findall(r"[aeiouáéíóúâêôãõàAEIOUÁÉÍÓÚÂÊÔÃÕÀ]+", p)))

def grupos_grav(lista, off, lag=0.15):
    """lista = [(texto, t_no_pronto AP-4 Dia 2)]; off(t) = deslocamento pronto→gravação. Devolve [(texto, [t por palavra])] na gravação."""
    ini = [vale(GRAV, t - off(t) - lag) for _, t in lista]
    out = []
    for k, (txt, _) in enumerate(lista):
        pal = txt.split(); t0 = ini[k]
        t1 = ini[k + 1] if k + 1 < len(lista) else t0 + 0.9 * len(pal)
        if len(pal) == 1: out.append((txt, [t0])); continue
        w = np.array([silabas(p) for p in pal], float); cum = t0 + (t1 - t0) * np.concatenate([[0], np.cumsum(w)[:-1]]) / w.sum()
        ts = [t0] + [vale(GRAV, x, 0.1, 0.1, -16) for x in cum[1:]]
        for j in range(1, len(ts)): ts[j] = max(ts[j], ts[j - 1] + 0.08)
        out.append((txt, ts))
    return out

def off_dia2(t):   # pronto AP-4 Dia 2 = gravação + off (o editor tirou pausas em 3 pontos)
    return 42.87 if t < 57.4 else (42.43 if t < 70.95 else (41.80 if t < 77.95 else 41.03))

@functools.lru_cache(None)
def pagina(n, larg=None):
    im = Image.open(NOVO + f"pag/p-{n:03d}.png").convert("RGB")
    if larg: im = im.resize((larg, round(im.height * larg / im.width)), Image.LANCZOS)
    return im

def sombra(img, caixa, raio=28, blur=26, alpha=110, dy=18):
    x0, y0, x1, y1 = [int(v) for v in caixa]
    sh = Image.new("L", img.size, 0); ImageDraw.Draw(sh).rounded_rectangle((x0, y0 + dy, x1, y1 + dy), radius=raio, fill=alpha)
    sh = sh.filter(ImageFilter.GaussianBlur(blur)); img.paste(Image.new("RGB", img.size, (0, 0, 0)), (0, 0), sh)

def cola_cartao(img, pg, cx, cy, larg, ang=0.0, alpha=1.0, raio=18, borda=0):
    """Página do Mapa como cartão (cantos arredondados, sombra), centro (cx, cy), largura larg, rotação ang (graus)."""
    p = pagina(pg, int(larg)) if isinstance(pg, int) else pg.resize((int(larg), round(pg.height * larg / pg.width)), Image.LANCZOS)
    if borda:
        q = Image.new("RGB", (p.width + 2 * borda, p.height + 2 * borda), (255, 255, 255)); q.paste(p, (borda, borda)); p = q
    m = Image.new("L", p.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, p.width - 1, p.height - 1), radius=raio, fill=int(255 * alpha))
    if ang:
        p = p.rotate(ang, Image.BICUBIC, expand=True); m = m.rotate(ang, Image.BICUBIC, expand=True)
    x0, y0 = int(cx - p.width / 2), int(cy - p.height / 2)
    sh = Image.new("L", img.size, 0); sh.paste(m.point(lambda v: int(v * 0.45)), (x0, y0 + 20)); sh = sh.filter(ImageFilter.GaussianBlur(22))
    img.paste(Image.new("RGB", img.size, (20, 24, 40)), (0, 0), sh)
    img.paste(p, (x0, y0), m)

def ease(x): x = min(1, max(0, x)); return 1 - (1 - x) ** 3
def mola(x):   # entra passando um pouco e volta
    x = min(1, max(0, x)); return 1 - math.cos(x * math.pi * 2.2) * math.exp(-5.5 * x)

class PIP:
    """Rosto dela num círculo, sincronizado com o próprio áudio do take. caras = [(t_arquivo, cx, cy)] (centro do rosto no quadro 1080x1920)."""
    def __init__(self, arq, a, pos, t1, caras, cx=770, cy=330, d=300, lado=560):
        self.arq, self.a, self.pos, self.t1, self.caras = arq, a, pos, t1, caras
        self.cx, self.cy, self.d, self.lado = cx, cy, d, lado; self.gen = None; self.k = -1; self.ultimo = None
    def _frame(self, t):
        if self.gen is None: self.gen = leitor(self.arq, self.a, self.t1 - self.pos + 0.5)
        alvo = int(round((t - self.pos) * FPS))
        while self.k < alvo:
            try: self.ultimo = next(self.gen)
            except StopIteration: break
            self.k += 1
        return self.ultimo
    def __call__(self, img, t):
        if not (self.pos <= t < self.t1): return
        f = self._frame(t)
        if f is None: return
        ta = self.a + (t - self.pos); xs = [c[0] for c in self.caras]
        fx, fy = np.interp(ta, xs, [c[1] for c in self.caras]), np.interp(ta, xs, [c[2] for c in self.caras])
        L = self.lado; box = (int(fx - L / 2), int(fy - L * 0.45), int(fx + L / 2), int(fy + L * 0.55))
        k = ease((t - self.pos) / 0.25) * (1 - ease((t - (self.t1 - 0.25)) / 0.25))
        d = max(2, int(self.d * (0.6 + 0.4 * k)))
        rosto = f.crop(box).resize((d, d), Image.LANCZOS)
        m = Image.new("L", (d, d), 0); ImageDraw.Draw(m).ellipse((0, 0, d - 1, d - 1), fill=int(255 * k))
        x0, y0 = int(self.cx - d / 2), int(self.cy - d / 2)
        sh = Image.new("L", img.size, 0); ImageDraw.Draw(sh).ellipse((x0 - 6, y0 + 8, x0 + d + 6, y0 + d + 20), fill=int(120 * k)); sh = sh.filter(ImageFilter.GaussianBlur(18))
        img.paste(Image.new("RGB", img.size, (0, 0, 0)), (0, 0), sh)
        ring = Image.new("L", (d + 16, d + 16), 0); ImageDraw.Draw(ring).ellipse((0, 0, d + 15, d + 15), fill=int(255 * k))
        img.paste(Image.new("RGB", ring.size, (255, 255, 255)), (x0 - 8, y0 - 8), ring)
        img.paste(rosto, (x0, y0), m)

def pilula(img, x, y, txt, fundo, cor=(255, 255, 255), fz=40, alpha=1.0, icone=None, pad=34, centro=False):
    """Pílula com texto; com alpha < 1 tudo (fundo, ícone e texto) é desenhado numa camada e misturado (o texto some junto)."""
    if alpha <= 0.01:
        fl = fonte(800, fz); w = ImageDraw.Draw(img).textlength(txt, font=fl) + 2 * pad + (58 if icone else 0); return w, int(fz * 1.9)
    if alpha < 0.999:
        cam = img.copy(); r = pilula(cam, x, y, txt, fundo, cor, fz, 1.0, icone, pad, centro)
        img.paste(Image.blend(img, cam, alpha)); return r
    d = ImageDraw.Draw(img, "RGBA"); fl = fonte(800, fz); w = d.textlength(txt, font=fl) + 2 * pad + (58 if icone else 0); h = int(fz * 1.9)
    if centro: x = x - w / 2
    a = int(255 * alpha)
    d.rounded_rectangle((x, y, x + w, y + h), radius=h // 2, fill=fundo + (a,))
    tx = x + pad
    if icone:
        cx, cy, r = x + pad + 20, y + h / 2, 21
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, a))
        if icone == "?": d.text((cx, cy + 1), "?", font=fonte(800, 30), fill=fundo + (a,), anchor="mm")
        elif icone == "v": d.line((cx - 10, cy + 1, cx - 3, cy + 9, cx + 11, cy - 8), fill=fundo + (a,), width=6, joint="curve")
        elif icone == "x":
            d.line((cx - 8, cy - 8, cx + 8, cy + 8), fill=fundo + (a,), width=6); d.line((cx - 8, cy + 8, cx + 8, cy - 8), fill=fundo + (a,), width=6)
        tx += 58
    d.text((tx, y + h / 2), txt, font=fl, fill=cor + (a,), anchor="lm")
    return w, h


# ---------- áudio: EQ da gravação do Dia 2, som ambiente, durações ----------
# Medido com o método do revisor (centróide em 16 kHz): gravação Dia 2 = 750–920 Hz; takes de câmera = 1.000–1.360 Hz.
# Com este EQ a gravação fica em 1.110–1.430 Hz (trechos usados: 1.200–1.230 Hz), a menos de ~150 Hz dos takes vizinhos.
EQ_GRAV = "highshelf=f=2000:g=5,equalizer=f=220:t=q:w=1:g=-4"

@functools.lru_cache(None)
def duracao(arq):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", arq], capture_output=True, text=True).stdout)

@functools.lru_cache(None)
def som_ambiente(arq, janela=0.35, total=4.0):
    """Trecho mais silencioso (sem fala) do próprio take, repetido com sobreposição suave até `total` s. Devolve um wav 48 kHz."""
    import soundfile as sf
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", arq, "-vn", "-ac", "1", "-ar", "48000", "-f", "f32le", "-"], capture_output=True).stdout
    y = np.frombuffer(raw, np.float32).copy(); sr = 48000; n = int(janela * sr); hop = int(0.01 * sr)
    marg = int(0.05 * sr); melhor, kbest = 1e9, marg
    for k in range(marg, len(y) - n - marg, hop):
        e = float(np.sqrt(np.mean(y[k:k + n] ** 2)))
        if 1e-6 < e < melhor: melhor, kbest = e, k
    pedaco = y[kbest:kbest + n]; ov = int(0.08 * sr); w = np.hanning(2 * ov)
    out = np.zeros(int(total * sr) + n); p = 0
    while p + n < len(out):
        q = pedaco.copy(); q[:ov] *= w[:ov]; q[-ov:] *= w[ov:]; out[p:p + n] += q; p += n - ov
    caminho = f"/tmp/_amb_{abs(hash(arq))}.wav"; sf.write(caminho, out[:int(total * sr)].astype(np.float32), sr)
    return caminho

def palavras_grav(spec, lag=0.10):
    """spec = [(texto, [t de cada palavra no pronto AP-4 Dia 2])] — tempos da palavra amarela lidos quadro a quadro (10 qps) na legenda
    do pronto. Converte pra gravação (off_dia2 − atraso da legenda) e prende cada palavra no vale de energia mais próximo (±0,10 s)."""
    out = []
    for txt, tp in spec:
        assert len(tp) == len(txt.split()), txt
        ts = [vale(GRAV, t - off_dia2(t) - lag, 0.10, 0.10, -18) for t in tp]
        for j in range(1, len(ts)): ts[j] = max(ts[j], ts[j - 1] + 0.08)
        out.append((txt, ts))
    return out

# CTA 4de4 ("…e tenha acesso vitalício ao seu Mapa…"), tempos por palavra no arquivo cortes2/cta4.mov: palavra amarela do pronto AP-DD5
# (proxy dd/AP___DD5_fim = cta4 + 7,58 s, casado por envelope de energia r=0,99) conferida com os vales de energia. "SAIBA MAIS" junto.
G_CTA4N = [("CLIQUE EM SAIBA MAIS", [0.02, 0.26, 0.46, 0.93]), ("E TENHA ACESSO VITALÍCIO", [1.18, 1.28, 1.57, 1.95]),
           ("AO SEU MAPA VISUAL", [2.74, 3.01, 3.20, 3.65]), ("COMPLETO DO", [4.15, 4.42]), ("FECHAMENTO IMOBILIÁRIO.", [4.67, 5.30])]   # fim 6,0


# ---------- quadro parado, tablet com as páginas do PDF, efeitos ----------
@functools.lru_cache(None)
def quadro(arq, t):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", str(t), "-i", arq, "-frames:v", "1", "-vf", f"scale={W}:{H}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return Image.frombytes("RGB", (W, H), raw[:W * H * 3])

def cinza(im):   # "antes": sem cor, um pouco mais escuro e frio
    g = im.convert("L").convert("RGB")
    return Image.blend(g, Image.new("RGB", im.size, (30, 40, 60)), 0.18)

def fundo_mesa(arq, t, escurece=0.45, blur=28):
    im = quadro(arq, t).filter(ImageFilter.GaussianBlur(blur))
    return Image.blend(im, Image.new("RGB", im.size, (10, 14, 24)), escurece)

def tablet(paginas, fundo, larg=780, topo=150, troca=0.22):
    """paginas = [(t_inicio_na_peça, n_da_página)] em ordem. Página inteira na largura da tela do tablet; troca = página deslizando
    (corte seco no resto, sem páginas sobrepostas)."""
    alt = round(larg * 1754 / 1241); bz = 30; dw, dh = larg + 2 * bz, alt + 2 * bz; x0 = (W - dw) // 2; y0 = topo
    tela = Image.new("L", (larg, alt), 0); ImageDraw.Draw(tela).rounded_rectangle((0, 0, larg - 1, alt - 1), radius=18, fill=255)
    def f(tl, t):
        im = fundo.copy()
        sombra(im, (x0, y0, x0 + dw, y0 + dh), raio=56, blur=30, alpha=150, dy=24)
        d = ImageDraw.Draw(im); d.rounded_rectangle((x0, y0, x0 + dw, y0 + dh), radius=56, fill=(18, 20, 26))
        d.rounded_rectangle((x0 + 3, y0 + 3, x0 + dw - 3, y0 + dh - 3), radius=54, outline=(70, 74, 84), width=3)
        i = max([k for k, (ts, _) in enumerate(paginas) if t >= ts - 1e-6] or [0]); ts, pg = paginas[i]
        scr = Image.new("RGB", (larg, alt), (255, 255, 255)); p = (t - ts) / troca
        if i > 0 and p < 1:
            e = ease(p); prev = pagina(paginas[i - 1][1], larg)
            scr.paste(prev, (int(-larg * e), 0)); scr.paste(pagina(pg, larg), (int(larg * (1 - e)), 0))
        else: scr.paste(pagina(pg, larg), (0, 0))
        im.paste(scr, (x0 + bz, y0 + bz), tela)
        z = 1 + 0.025 * min(1.0, max(0.0, t - ts) / 2.0)      # aproximação lenta em cada página (a tela nunca fica parada)
        if z > 1.0005:
            w2, h2 = round(W * z), round(H * z); im = im.resize((w2, h2), Image.BILINEAR)
            cy = (y0 + dh / 2) * z - (y0 + dh / 2); im = im.crop(((w2 - W) // 2, int(cy), (w2 - W) // 2 + W, int(cy) + H))
        return im
    return f


# ---------- falas da "Gravação AP Dia 2" palavra por palavra (tempos no pronto AP-4 Dia 2, palavra amarela a 10 qps) ----------
L2_DIA2 = [("PARA AJUDAR VOCÊ,", [49.8, 49.9, 50.3]), ("CORRETOR,", [50.7]), ("A COMPREENDER", [51.4, 51.6]), ("AS PRINCIPAIS FORMAS", [52.2, 52.3, 52.8]),
           ("DE AQUISIÇÃO,", [53.1, 53.2]), ("PAGAMENTO E FECHAMENTO", [54.2, 54.8, 55.1]), ("DE IMÓVEIS", [55.5, 55.7]),
           ("DENTRO DE TRANSAÇÕES", [56.3, 56.6, 56.8]), ("IMOBILIÁRIAS.", [57.2])]
L3_DIA2 = [("O MATERIAL EXPLICA", [58.0, 58.3, 58.7]), ("FINANCIAMENTO IMOBILIÁRIO,", [59.1, 59.7]), ("MINHA CASA MINHA VIDA,", [60.4, 60.6, 61.0, 61.1]),
           ("FGTS,", [61.7]), ("COMPOSIÇÃO DE RENDA,", [62.7, 63.3, 63.5]), ("COMPRA À VISTA,", [64.1, 64.3, 64.6]), ("CONSÓRCIO,", [65.3]),
           ("IMÓVEL NA PLANTA,", [66.1, 66.6, 66.8]), ("PERMUTA,", [67.2]), ("DOCUMENTAÇÃO,", [68.0]), ("MATRÍCULA,", [69.0]),
           ("CERTIDÕES", [69.8]), ("E MUITO MAIS.", [70.5, 70.6, 70.8])]
L4_DIA2 = [("CADA MAPA MOSTRA", [71.2, 71.5, 72.0]), ("DE FORMA CLARA", [72.4, 72.5, 72.7]), ("QUEM PARTICIPA", [73.2, 73.5]), ("DO PROCESSO,", [74.0, 74.1]),
           ("QUAIS DOCUMENTOS ENTRAM", [74.9, 75.2, 75.8]), ("E EM QUE ORDEM", [76.2, 76.25, 76.3, 76.5]), ("AS ETAPAS ACONTECEM.", [76.9, 77.0, 77.5])]
L5_DIA2 = [("ASSIM, QUANDO SURGIR", [78.0, 78.4, 78.7]), ("UMA DÚVIDA", [79.2, 79.3]), ("DURANTE O ATENDIMENTO,", [79.7, 79.9, 80.1]),
           ("VOCÊ CONSEGUE CONSULTAR", [81.1, 81.2, 81.6]), ("O TEMA CORRESPONDENTE", [82.1, 82.2, 82.5]), ("E ENTENDER", [83.3, 83.4]),
           ("O PROCESSO", [83.8, 83.9]), ("DE FORMA VISUAL,", [84.2, 84.4, 84.7]), ("ORGANIZADA E FÁCIL", [85.4, 86.0, 86.2]),
           ("DE APLICAR", [86.5, 86.7]), ("NA SUA ROTINA.", [87.2, 87.3, 87.5])]

def legenda_desde_zero(pc):
    """O primeiro grupo da legenda já aparece no quadro 0 (gancho com texto desde o 1º quadro)."""
    a, b, txt, ts = pc.leg[0]
    pc.leg[0] = (0.0, b, txt, ([0.0] + ts[1:]) if ts else None)

def pilula_ajusta(img, y, txt, fundo, cor=(255, 255, 255), fz=46, alpha=1.0, icone=None, maxw=800):
    d = ImageDraw.Draw(img)
    while d.textlength(txt, font=fonte(800, fz)) + 68 + (58 if icone else 0) > maxw and fz > 26: fz -= 1
    return pilula(img, W / 2, y, txt, fundo, cor=cor, fz=fz, alpha=alpha, icone=icone, centro=True)


# ---------- alinhamento da gravação do Dia 2 (sem modelo de transcrição) ----------
SIL_FIXAS = {"FGTS": 4, "À": 1, "E": 1, "O": 1, "A": 1, "AS": 1, "DE": 1, "DO": 1, "NA": 1, "EM": 1, "QUE": 1, "UMA": 2, "SUA": 2,
             "IMOBILIÁRIAS": 6, "IMOBILIÁRIO": 6, "FINANCIAMENTO": 5, "COMPREENDER": 4, "TRANSAÇÕES": 3, "CERTIDÕES": 3,
             "DOCUMENTAÇÃO": 5, "COMPOSIÇÃO": 4, "AQUISIÇÃO": 4, "CONSÓRCIO": 3, "CORRESPONDENTE": 5, "ATENDIMENTO": 5,
             "PRINCIPAIS": 3, "MATRÍCULA": 4, "PARTICIPA": 4, "DOCUMENTOS": 4, "ACONTECEM": 4, "VOCÊ": 2, "CORRETOR": 3}
def sil(p):
    q = p.strip(",.;:!?").upper()
    return SIL_FIXAS.get(q, silabas(q))

def frases_grav(a, b, lim=-26, minp=0.06):
    """Trechos de fala entre pausas reais (energia < lim por ≥ minp s) dentro de [a, b] da gravação."""
    db = energia(GRAV); i0, i1 = int(a / 0.005), int(b / 0.005); sil_ = db[i0:i1] < lim
    out = []; i = 0; ini = None
    while i < len(sil_):
        if not sil_[i]:
            if ini is None: ini = i
            i += 1
        else:
            j = i
            while j < len(sil_) and sil_[j]: j += 1
            if (j - i) * 0.005 >= minp or j == len(sil_):
                if ini is not None: out.append(((i0 + ini) * 0.005, (i0 + i) * 0.005)); ini = None
            i = j
    if ini is not None: out.append(((i0 + ini) * 0.005, b))
    return out

def alinhar_grav(spec, a, b, lag=0.05):
    """Tempos por palavra na gravação, sem modelo de transcrição:
    1) acha os trechos de fala entre pausas reais (energia);
    2) reparte as palavras (em ordem) entre os trechos por programação dinâmica: o 1º tempo de cada trecho tem que bater com a palavra
       amarela do pronto AP-4 Dia 2 e a velocidade (s por sílaba) tem que ficar coerente entre os trechos;
    3) dentro do trecho, cada palavra fica na média entre a divisão por sílabas e o espaçamento da legenda do pronto, presa no vale
       de energia mais próximo (±0,08 s).
    Nenhuma palavra começa dentro de uma pausa."""
    fr = [f for f in frases_grav(a, b) if f[1] - f[0] >= 0.10]
    pal = [(w, t - off_dia2(t) - lag) for txt, tp in spec for w, t in zip(txt.split(), tp)]
    n, m = len(pal), len(fr); S = [sil(w) for w, _ in pal]; cs = np.concatenate([[0], np.cumsum(S)])
    r = sum(x1 - x0 for x0, x1 in fr) / cs[-1]
    INF = 1e18; best = np.full((m + 1, n + 1), INF); arg = np.zeros((m + 1, n + 1), int); best[0, 0] = 0
    for k in range(1, m + 1):
        x0, x1 = fr[k - 1]; d = x1 - x0
        for j in range(1, n + 1):
            for i in range(k - 1, j):
                if best[k - 1, i] >= INF: continue
                sy = cs[j] - cs[i]
                c = ((pal[i][1] - x0) / 0.15) ** 2 + ((math.log(d / (sy * r))) / 0.35) ** 2
                if best[k - 1, i] + c < best[k, j]: best[k, j] = best[k - 1, i] + c; arg[k, j] = i
    cortes = [n]; j = n
    for k in range(m, 0, -1): j = arg[k, j]; cortes.append(j)
    cortes = cortes[::-1]
    tempos = [None] * n
    for k in range(m):
        i0, i1 = cortes[k], cortes[k + 1]; x0, x1 = fr[k]
        w = np.array(S[i0:i1], float); cum = x0 + (x1 - x0) * np.concatenate([[0], np.cumsum(w)[:-1]]) / w.sum()
        for q, j in enumerate(range(i0, i1)):
            if q == 0: tempos[j] = x0; continue
            pr = min(x0 + (pal[j][1] - pal[i0][1]), x1 - 0.12 * (i1 - j))      # espaçamento do pronto, ancorado no início do trecho
            tempos[j] = vale(GRAV, 0.5 * (cum[q] + pr), 0.08, 0.08, -12)      # média das duas estimativas, presa no vale
    for j in range(1, n): tempos[j] = max(tempos[j], tempos[j - 1] + 0.07)
    out = []; p = 0
    for txt, tp in spec:
        k = len(txt.split()); out.append((txt, [float(x) for x in tempos[p:p + k]])); p += k
    return out

def encolhe(im, s=0.86):
    """Quadro do impresso reduzido (página inteira com folga nas laterais) sobre o mesmo quadro desfocado e escurecido."""
    fundo = Image.blend(im.resize((W // 8, H // 8)).filter(ImageFilter.GaussianBlur(4)).resize((W, H)), Image.new("RGB", (W, H), (10, 14, 24)), 0.35)
    p = im.resize((round(W * s), round(H * s)), Image.LANCZOS); fundo.paste(p, ((W - p.width) // 2, (H - p.height) // 2)); return fundo


# ---------- EQ da Gravação Dia 2 por faixa (fit_eq.py → novo/eq_grav.json, alvo: CTA4 faixa a faixa ±3 dB) ----------
def eq_grav(nome):
    return json.load(open(NOVO + "eq_grav.json"))[nome]

# ---------- folheando: páginas reais do PDF, inteiras, viradas uma a uma (sem páginas fantasma) ----------
def folheia(paginas, fundo, larg=860, cy=900, virada=0.32):
    """paginas = [(t_inicio_na_peça, n_da_página)]. Caderno com espiral no centro da tela; em cada troca a página de cima vira para
    a esquerda (encolhe até a espiral, com sombra) e mostra a de baixo. A página aparece sempre inteira, com margem dos dois lados."""
    alt = round(larg * 1754 / 1241); x0 = (W - larg) // 2; y0 = int(cy - alt / 2)
    def f(tl, t):
        im = fundo.copy()
        i = max([k for k, (ts, _) in enumerate(paginas) if t >= ts - 1e-6] or [0]); ts, pg = paginas[i]
        z = 1 + 0.02 * min(1.0, max(0.0, t - ts) / 1.5)
        L = int(larg * z); A = int(alt * z); xx = (W - L) // 2; yy = int(cy - A / 2)
        sombra(im, (xx, yy, xx + L, yy + A), raio=10, blur=26, alpha=150, dy=20)
        base = pagina(pg, L).resize((L, A)); im.paste(base, (xx, yy))
        p = (t - ts) / virada
        if i > 0 and p < 1:                       # a página anterior virando por cima
            e = ease(p); wv = int(L * (1 - e) * (1 - 0.0 * e))
            if wv > 2:
                prev = pagina(paginas[i - 1][1], L).resize((wv, A))
                esc = Image.new("RGB", prev.size, (0, 0, 0)); prev = Image.blend(prev, esc, 0.35 * e)
                im.paste(prev, (xx, yy))
                d = ImageDraw.Draw(im, "RGBA"); d.rectangle((xx + wv - 6, yy, xx + wv, yy + A), fill=(0, 0, 0, int(90 * (1 - e))))
        d = ImageDraw.Draw(im)                   # espiral
        for k in range(18):
            yk = yy + 40 + k * (A - 80) / 17
            d.ellipse((xx - 16, yk - 9, xx + 16, yk + 9), outline=(40, 40, 46), width=5)
        return im
    return f
