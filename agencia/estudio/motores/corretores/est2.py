#!/usr/bin/env python3
"""EST2 · Quiz "você saberia responder?" — piloto A (23/11). Motor derivado do est5.py.
Monta no container a partir dos recortes 1080x1920 feitos no PC do Léo (ffmpeg pelo shell do dispositivo).
Voz: só a da Ana Paula (HOOK5 pt1/pt2 + CTA 2de2, brutos). Legenda refeita a partir das legendas dos prontos.
Uso: python3 est5.py <saida.mp4>
"""
import os, sys, subprocess, json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

C = "/mnt/user-data/uploads/Corretores/Criativos prontos/ESTUDIO 23-11/_trabalho/cortes2/"
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fontes/")
W, H, FPS = 1080, 1920, 30
OUT = sys.argv[1] if len(sys.argv) > 1 else "EST5-A.mp4"

# ---------- linha do tempo (s) ----------
CLIPES = [  # arquivo, início no arquivo, duração na peça, zoom, velocidade (1 = normal)
    ("hook4.mov", 0.45, 11.43, 1.0, 1.0),
    ("ipad_intro.mp4", 0.3, 0.97, 1.04, 1.0),
    ("ipad_renda_cabe.mp4", 0.5, 2.70, 1.05, 1.0),     # Faixas de renda urbana  -> resposta 1
    ("q2_renda_cabe.mp4", 1.4, 2.60, 1.05, 1.0),       # Renda e imóvel cabem?   -> resposta 2
    ("q3_avaliacao.mp4", 0.9, 2.60, 1.06, 0.73),       # Avaliação muda a entrada -> resposta 3 (levemente mais lento)
    ("cta4.mov", 0.0, 6.38, 1.0, 1.0),
]
T0 = np.cumsum([0] + [c[2] for c in CLIPES]); TOTAL = float(T0[-1]); CTA_INI = float(T0[5])
HIST = []
def grupos(lista, desloc, fim_ref):
    out = []
    for i, (txt, t) in enumerate(lista):
        t2 = lista[i + 1][1] if i + 1 < len(lista) else fim_ref
        out.append((t + desloc, t2 + desloc, txt))
    return out
LEG = []
LEG += grupos([("CORRETOR,", 0.4), ("VOCÊ SABE OLHAR", 0.8), ("A RENDA", 1.6), ("DO SEU CLIENTE", 2.4), ("E DIZER PRA", 2.8),
               ("ELE QUANTO QUE", 3.6), ("ELE CONSEGUE", 4.0), ("FINANCIAR,", 4.8), ("QUAL O VALOR", 5.2), ("DO IMÓVEL QUE", 5.6),
               ("ELE CONSEGUE COMPRAR", 6.8), ("E QUANTO QUE", 7.6), ("ELE VAI TER", 8.0), ("QUE DAR DE", 8.4), ("ENTRADA?", 8.8),
               ("SE NÃO,", 9.77), ("DÁ UMA OLHADA", 10.0), ("NO MATERIAL.", 10.8)], 0.0, 11.43)
LEG += grupos([("SÃO +120 MAPAS", 1.34), ("VISUAIS,", 3.2), ("CLAROS E OBJETIVOS,", 3.6), ("SOBRE FGTS,", 5.76), ("MINHA CASA", 7.2),
               ("MINHA VIDA,", 7.6), ("CONSÓRCIO,", 8.4), ("DOCUMENTAÇÃO.", 9.2)], 10.19, 10.11)
LEG += grupos([("CLIQUE EM SAIBA", 7.6), ("MAIS E TENHA", 8.6), ("ACESSO VITALÍCIO", 9.2), ("AO SEU MAPA", 10.4), ("VISUAL COMPLETO DO", 11.2),
               ("FECHAMENTO IMOBILIÁRIO.", 12.4)], 12.7, 13.6)
AUDIO = [("hook4.mov", -0.45, 11.43), ("dd2_body.wav", "body", None), ("cta4.mov", CTA_INI, None)]
# quiz (cartão no topo): (ini, fim, contador, texto, respondida)
QUIZ = [
    (0.0, 3.6, "", "Você saberia responder?", False),
    (3.6, 5.2, "1/3", "Quanto ele consegue financiar?", False),
    (5.2, 7.6, "2/3", "Qual o valor do imóvel?", False),
    (7.6, 9.77, "3/3", "Quanto vai dar de entrada?", False),
    (9.77, T0[2], "", "As 3 respostas estão no Mapa.", False),
    (T0[2], T0[3], "1/3", "Quanto ele consegue financiar?", True),
    (T0[3], T0[4], "2/3", "Qual o valor do imóvel?", True),
    (T0[4], T0[5], "3/3", "Quanto vai dar de entrada?", True),
]

# ---------- tipografia ----------
f_leg = ImageFont.truetype(F + "poppins-latin-800-normal.ttf", 66)
f_hist = ImageFont.truetype(F + "poppins-latin-800-normal.ttf", 78)
f_tag = ImageFont.truetype(F + "poppins-latin-700-normal.ttf", 40)
f_preco = ImageFont.truetype(F + "poppins-latin-800-normal.ttf", 58)
AMARELO = (255, 214, 10)

def quebra(draw, txt, font, maxw):
    pal, linhas, cur = txt.split(), [], ""
    for p in pal:
        t = (cur + " " + p).strip()
        if draw.textlength(t, font=font) <= maxw: cur = t
        else: linhas.append(cur); cur = p
    linhas.append(cur); return linhas

def legenda(img, t):
    for a, b, txt in LEG:
        if a <= t < b: break
    else: return
    d = ImageDraw.Draw(img)
    pal = txt.split()
    # palavra ativa: divide o tempo do grupo pelo tamanho das palavras
    pesos = np.array([len(p) for p in pal], float); lim = a + (b - a) * np.cumsum(pesos) / pesos.sum()
    ativa = int(np.searchsorted(lim, t, side='right')); ativa = min(ativa, len(pal) - 1)
    cy = 240 if t >= CTA_INI else 1290
    esp = d.textlength(" ", font=f_leg)
    larg = sum(d.textlength(p, font=f_leg) for p in pal) + esp * (len(pal) - 1)
    x = (W - larg) / 2
    for i, p in enumerate(pal):
        cor = AMARELO if i == ativa else (255, 255, 255)
        d.text((x, cy), p, font=f_leg, fill=cor, anchor="lm", stroke_width=7, stroke_fill=(0, 0, 0))
        x += d.textlength(p, font=f_leg) + esp

def historia(img, t):
    for a, b, txt in HIST:
        if a <= t < b: break
    else: return
    # degradê escuro no topo pra leitura
    grad = Image.new("L", (W, 620))
    gd = np.linspace(170, 0, 620).astype(np.uint8)
    grad.putdata(np.repeat(gd, W).tolist())
    preto = Image.new("RGB", (W, 620), (0, 0, 0))
    img.paste(preto, (0, 0), grad)
    d = ImageDraw.Draw(img)
    linhas = txt.split("\n")   # quebra manual: nada de palavra solta
    assert all(d.textlength(l, font=f_hist) <= 880 for l in linhas), txt
    # entra com leve subida nos primeiros 0,25 s
    k = min(1, (t - a) / 0.25); dy = int((1 - k) * 24)
    y = 250 + dy
    for ln in linhas:
        d.text((W / 2, y), ln, font=f_hist, fill=(255, 255, 255), anchor="mm", stroke_width=3, stroke_fill=(0, 0, 0))
        y += 100

f_quiz = ImageFont.truetype(F + "poppins-latin-800-normal.ttf", 46)
f_cont = ImageFont.truetype(F + "poppins-latin-800-normal.ttf", 38)
NAVY, TEAL = (14, 42, 84), (18, 160, 140)
def quiz(img, t):
    for a, b, cont, txt, ok in QUIZ:
        if a <= t < b: break
    else: return
    d = ImageDraw.Draw(img, "RGBA")
    x0, y0, w, h = 90, 170, 900, 150
    k = min(1, (t - a) / 0.18)
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle((x0, y0 + 10, x0 + w, y0 + h + 10), radius=36, fill=(0, 0, 0, 90))
    img.paste(sh.filter(ImageFilter.GaussianBlur(14)), (0, 0), sh.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), radius=36, fill=(255, 255, 255, 250))
    tx = x0 + 40
    if cont:
        # selo do contador (verde quando respondida)
        cor = TEAL if ok else NAVY
        d.rounded_rectangle((x0 + 30, y0 + 40, x0 + 30 + 120, y0 + 110), radius=35, fill=cor)
        d.text((x0 + 90, y0 + 75), ("✓ " if False else "") + cont, font=f_cont, fill="white", anchor="mm")
        tx = x0 + 175
    txt_w = x0 + w - 40 - tx - (90 if (cont and not ok) else 0) - (70 if ok else 0)
    fz = 46
    while d.textlength(txt, font=ImageFont.truetype(F + "poppins-latin-800-normal.ttf", fz)) > txt_w and fz > 30: fz -= 2
    d.text((tx, y0 + h / 2), txt, font=ImageFont.truetype(F + "poppins-latin-800-normal.ttf", fz), fill=NAVY, anchor="lm")
    cx, cy, r = x0 + w - 75, y0 + h / 2, 32
    if cont and not ok:
        # cronômetro: anel que esvazia durante a pergunta
        p = (t - a) / (b - a)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(220, 226, 236), width=9)
        d.arc((cx - r, cy - r, cx + r, cy + r), start=-90, end=-90 + 360 * (1 - p), fill=(230, 120, 60), width=9)
        seg = max(1, math.ceil((b - t)))
        d.text((cx, cy), str(seg), font=f_cont, fill=NAVY, anchor="mm")
    if ok:
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=TEAL)
        d.line((cx - 14, cy + 1, cx - 4, cy + 12, cx + 15, cy - 11), fill="white", width=8, joint="curve")

def preco(img, t):
    if t < CTA_INI + 2.6: return
    k = min(1, (t - CTA_INI - 2.6) / 0.3)
    d = ImageDraw.Draw(img, "RGBA")
    w, h = 400, 110; x0 = (W - w) // 2; y0 = 318 + int((1 - k) * 24)   # abaixo da legenda, acima da cabeça dela (não cobre o material)
    a = int(255 * k)
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), radius=64, fill=(11, 79, 58, a))
    d.text((W / 2, y0 + h / 2 - 2), "R$27,90", font=f_preco, fill=(255, 255, 255, a), anchor="mm")

def frames_clipe(arq, ini, dur, z, vel=1.0):
    cmd = ["ffmpeg", "-loglevel", "error", "-ss", str(ini), "-t", str(dur * vel + 0.2), "-i", C + arq,
           "-vf", f"setpts=PTS/{vel},fps={FPS},scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    n = int(round(dur * FPS)); i = 0
    while i < n:
        buf = p.stdout.read(W * H * 3)
        if len(buf) < W * H * 3: break
        im = Image.frombytes("RGB", (W, H), buf)
        if z != 1.0:
            s = 1 + (z - 1) * (i / max(1, n - 1))
            cw, ch = W / s, H / s
            im = im.crop(((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2)).resize((W, H), Image.LANCZOS)
        yield im; i += 1
    # se o clipe acabar antes, repete o último quadro
    while i < n: yield im; i += 1
    p.stdout.close(); p.wait()

def main():
    tmpv = "/tmp/est2_video.mp4"
    enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", tmpv], stdin=subprocess.PIPE)
    fr = 0
    for k, (arq, ini, dur, z, vel) in enumerate(CLIPES):
        for im in frames_clipe(arq, ini, dur, z, vel):
            t = fr / FPS
            quiz(im, t); legenda(im, t); preco(im, t)
            enc.stdin.write(im.tobytes()); fr += 1
    enc.stdin.close(); enc.wait()
    # áudio: só a voz dela, posicionada e normalizada
    ins, filt, labs = [], [], []
    ins += ["-i", C + "hook4.mov", "-i", C + "dd2_body.wav", "-i", C + "cta4.mov"]
    filt.append(f"[1:a]atrim=start=0.45:end=11.88,asetpts=PTS-STARTPTS,aresample=48000,pan=mono|c0=c0,afade=t=out:st={11.43-0.03}:d=0.03[a0]")
    filt.append(f"[2:a]atrim=start=1.24:end=10.11,asetpts=PTS-STARTPTS,aresample=48000,pan=mono|c0=c0,afade=t=in:d=0.02,adelay={int(T0[1]*1000)}[a1]")
    filt.append(f"[3:a]aresample=48000,pan=mono|c0=c0,adelay={int(CTA_INI*1000)}[a2]")
    labs = ["[a0]", "[a1]", "[a2]"]
    filt.append("".join(labs) + f"amix=inputs={len(labs)}:normalize=0,highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,loudnorm=I=-14:TP=-1.5:LRA=9,atrim=0:{TOTAL},apad=whole_dur={TOTAL}[aout]")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmpv] + ins + ["-filter_complex", ";".join(filt), "-map", "0:v", "-map", "[aout]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-shortest", "-movflags", "+faststart", OUT], check=True)
    print("ok", OUT, f"{TOTAL:.2f}s", fr, "quadros")

if __name__ == "__main__":
    main()
