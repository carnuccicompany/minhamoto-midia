#!/usr/bin/env python3
"""EST5 · Historinha da venda que morreu — piloto A (23/11).
Monta no container a partir dos recortes 1080x1920 feitos no PC do Léo (ffmpeg pelo shell do dispositivo).
Voz: só a da Ana Paula (HOOK5 pt1/pt2 + CTA 2de2, brutos). Legenda refeita a partir das legendas dos prontos.
Uso: python3 est5.py <saida.mp4>
"""
import os, sys, subprocess, json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

C = "/mnt/user-data/uploads/Corretores/Criativos prontos/ESTUDIO 23-11/_trabalho/cortes/"
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fontes/")
W, H, FPS = 1080, 1920, 30
OUT = sys.argv[1] if len(sys.argv) > 1 else "EST5-A.mp4"

# ---------- linha do tempo (s) ----------
CLIPES = [  # arquivo, início no arquivo, duração, zoom (1 -> z)
    ("s1_fechando.mp4", 1.0, 1.9, 1.06),
    ("s4_vendodocs.mp4", 0.2, 1.9, 1.06),
    ("s3_conversa.mp4", 0.8, 2.0, 1.06),
    ("s2_duvida.mp4", 0.5, 2.1, 1.07),
    ("m1_carta.mp4", 0.0, 3.7, 1.04),
    ("m2_consorcio.mp4", 0.3, 3.7, 1.04),
    ("cta2.mov", 0.0, 5.65, 1.0),
]
T0 = np.cumsum([0] + [c[2] for c in CLIPES])          # início de cada clipe
TOTAL = float(T0[-1])
CTA_INI = float(T0[6])

# texto da história (topo), um por cena
HIST = [
    (T0[0], T0[1], "A proposta foi aceita."),
    (T0[1], T0[2], "Aí o cliente\nperguntou do FGTS…"),
    (T0[2], T0[3], "“Vou confirmar\ne te aviso.”"),
    (T0[3], T0[4], "Três dias depois,\no cliente esfriou."),
]

# legenda da fala dela: (texto do grupo, início no pronto de referência), convertidos pra linha do tempo
def grupos(lista, desloc, fim_ref):
    out = []
    for i, (txt, t) in enumerate(lista):
        t2 = lista[i + 1][1] if i + 1 < len(lista) else fim_ref
        out.append((t + desloc, t2 + desloc, txt))
    return out
LEG = []
LEG += grupos([("CORRETOR,", 0.2), ("QUANTO MAIS VOCÊ", 1.0), ("ENTENDE A OPERAÇÃO", 1.6), ("QUE VOCÊ ESTÁ", 2.6),
               ("CONDUZINDO,", 3.0), ("MAIS SEGURANÇA VOCÊ", 4.2), ("CONSEGUE PASSAR", 5.2), ("PRO SEU CLIENTE", 5.8),
               ("NA HORA DO", 6.8), ("FECHAMENTO.", 7.4)], 0.11, 7.95)
LEG += grupos([("ENTÃO DÁ UMA", 8.0), ("OLHADA NESSE MATERIAL", 8.6), ("AQUI,", 9.6), ("QUE FOI JUSTAMENTE", 10.0),
               ("CRIADO PRA AMPLIAR", 10.8), ("ESSE SEU REPERTÓRIO", 12.0), ("E TORNAR O", 12.8),
               ("ATENDIMENTO MUITO MAIS", 13.6), ("PROFISSIONAL.", 14.6)], 0.06, 15.1)
LEG += grupos([("CLIQUE EM SAIBA", 8.8), ("MAIS E TEM", 9.6), ("ACESSO VITALÍCIO", 10.2), ("AO MAPA VISUAL", 11.2),
               ("COMPLETO DO FECHAMENTO", 12.4), ("IMOBILIÁRIO.", 13.6)], 6.5, 14.2)

AUDIO = [("HOOK5_pt_1.wav", -0.40), ("HOOK5_pt_2.wav", 7.49), ("cta2.mov", CTA_INI)]   # (arquivo, posição; negativo = corta o começo)

# ---------- tipografia ----------
f_leg = ImageFont.truetype(F + "poppins-latin-800-normal.ttf", 66)
f_hist = ImageFont.truetype(F + "poppins-latin-800-normal.ttf", 78)
f_tag = ImageFont.truetype(F + "poppins-latin-700-normal.ttf", 40)
f_preco = ImageFont.truetype(F + "poppins-latin-800-normal.ttf", 64)
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
    cy = 330 if t >= CTA_INI else 1290
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

def preco(img, t):
    if t < CTA_INI + 2.6: return
    k = min(1, (t - CTA_INI - 2.6) / 0.3)
    d = ImageDraw.Draw(img, "RGBA")
    w, h = 440, 128; x0 = (W - w) // 2; y0 = 430 + int((1 - k) * 30)   # abaixo da legenda, acima da cabeça dela (não cobre o material)
    a = int(255 * k)
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), radius=64, fill=(11, 79, 58, a))
    d.text((W / 2, y0 + h / 2 - 2), "R$27,90", font=f_preco, fill=(255, 255, 255, a), anchor="mm")

def frames_clipe(arq, ini, dur, z):
    cmd = ["ffmpeg", "-loglevel", "error", "-ss", str(ini), "-t", str(dur), "-i", C + arq,
           "-vf", f"fps={FPS},scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
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
    tmpv = "/tmp/est5_video.mp4"
    enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", tmpv], stdin=subprocess.PIPE)
    fr = 0
    for k, (arq, ini, dur, z) in enumerate(CLIPES):
        for im in frames_clipe(arq, ini, dur, z):
            t = fr / FPS
            historia(im, t); legenda(im, t); preco(im, t)
            enc.stdin.write(im.tobytes()); fr += 1
    enc.stdin.close(); enc.wait()
    # áudio: só a voz dela, posicionada e normalizada
    ins, filt, labs = [], [], []
    for j, (arq, pos) in enumerate(AUDIO):
        ins += ["-i", C + arq]
        if pos < 0: filt.append(f"[{j+1}:a]atrim=start={-pos},asetpts=PTS-STARTPTS,aresample=48000,pan=mono|c0=c0[a{j}]")
        else: filt.append(f"[{j+1}:a]aresample=48000,pan=mono|c0=c0,adelay={int(pos*1000)}[a{j}]")
        labs.append(f"[a{j}]")
    filt.append("".join(labs) + f"amix=inputs={len(labs)}:normalize=0,highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,loudnorm=I=-14:TP=-1.5:LRA=9,atrim=0:{TOTAL},apad=whole_dur={TOTAL}[aout]")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmpv] + ins + ["-filter_complex", ";".join(filt), "-map", "0:v", "-map", "[aout]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-shortest", "-movflags", "+faststart", OUT], check=True)
    print("ok", OUT, f"{TOTAL:.2f}s", fr, "quadros")

if __name__ == "__main__":
    main()
