#!/usr/bin/env python3
"""EST4 · Split-screen corretor inseguro × corretor que domina — piloto A (23/11).
Voz: só a da Ana Paula (HOOK1 pt1/pt2 = gancho do AP DD 10, o que mais vendeu; CTA 2de2). Ângulo: ganho (responder qualquer pergunta).
Uso: python3 est4.py <saida.mp4>
"""
import os, sys, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

U = "/mnt/user-data/uploads/Corretores/Criativos prontos/ESTUDIO 23-11/_trabalho/"
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fontes/")
W, H, FPS = 1080, 1920, 30
OUT = sys.argv[1] if len(sys.argv) > 1 else "EST4-A.mp4"

SPLIT_FIM = 7.85
CTA_INI = 15.90
# metade de cima (inseguro) e de baixo (domina): (arquivo, início, duração, y do recorte 1080x960)
CIMA = [(U + "cortes/s3_conversa.mp4", 0.6, 2.40, 330), (U + "cortes/s2_duvida.mp4", 0.5, 2.50, 420), (U + "cortes/s4_vendodocs.mp4", 0.05, 2.95, 360)]
BAIXO = [(U + "cortes2/q2_renda_cabe.mp4", 1.4, 2.60, 520), (U + "cortes3/doc3.mp4", 1.0, 2.70, 380), (U + "cortes3/feliz.mp4", 2.0, 2.55, 300)]
CHEIA = [(U + "cortes/m1_carta.mp4", 0.0, 2.70, 1.04), (U + "cortes2/ipad_renda_numero.mp4", 0.6, 2.70, 1.05),
         (U + "cortes/m2_consorcio.mp4", 0.3, 2.65, 1.04), (U + "cortes/cta2.mov", 0.0, 5.65, 1.0)]
TOTAL = SPLIT_FIM + sum(c[2] for c in CHEIA)

def grupos(lista, desloc, fim_ref):
    return [(t + desloc, (lista[i + 1][1] if i + 1 < len(lista) else fim_ref) + desloc, txt) for i, (txt, t) in enumerate(lista)]
LEG = []
LEG += grupos([("SE VOCÊ QUER", 0.0), ("SER O CORRETOR", 0.8), ("QUE SABE RESPONDER", 1.6), ("QUANDO A NEGOCIAÇÃO", 2.8),
               ("SAI DO BÁSICO,", 3.6), ("VOCÊ PRECISA DOMINAR", 4.8), ("MUITO MAIS DO", 6.0), ("QUE APENAS A", 6.4), ("VENDA.", 7.2)], 0.14, 7.6)
LEG += grupos([("E DÁ UMA", 7.6), ("OLHADA NESSE MATERIAL,", 8.4), ("PORQUE ELE FOI", 9.2), ("CRIADO JUSTAMENTE", 10.0),
               ("PARA TE PREPARAR", 10.8), ("PARA OS", 12.0), ("DIFERENTES", 12.4), ("CENÁRIOS QUE PODEM", 13.2),
               ("ACONTECER DURANTE O", 14.0), ("FECHAMENTO.", 14.8)], 0.335, 15.4)
LEG += grupos([("CLIQUE EM SAIBA", 8.8), ("MAIS E TEM", 9.6), ("ACESSO VITALÍCIO", 10.2), ("AO MAPA VISUAL", 11.2),
               ("COMPLETO DO FECHAMENTO", 12.4), ("IMOBILIÁRIO.", 13.6)], 7.1, 14.2)

f_leg = ImageFont.truetype(F + "poppins-latin-800-normal.ttf", 66)
f_chip = ImageFont.truetype(F + "poppins-latin-800-normal.ttf", 40)
f_preco = ImageFont.truetype(F + "poppins-latin-800-normal.ttf", 64)
AMARELO = (255, 214, 10); TERRA = (214, 88, 40); TEAL = (16, 150, 128)

def legenda(img, t):
    for a, b, txt in LEG:
        if a <= t < b: break
    else: return
    d = ImageDraw.Draw(img); pal = txt.split()
    pesos = np.array([len(p) for p in pal], float); lim = a + (b - a) * np.cumsum(pesos) / pesos.sum()
    ativa = min(int(np.searchsorted(lim, t, side='right')), len(pal) - 1)
    cy = 960 if t < SPLIT_FIM else (330 if t >= CTA_INI else 1290)
    fz = 66
    while True:   # reduz a fonte até caber em 900 px (zona segura)
        fl = ImageFont.truetype(F + "poppins-latin-800-normal.ttf", fz)
        esp = d.textlength(" ", font=fl); larg = sum(d.textlength(p, font=fl) for p in pal) + esp * (len(pal) - 1)
        if larg <= 900 or fz <= 50: break
        fz -= 2
    x = (W - larg) / 2
    for i, p in enumerate(pal):
        d.text((x, cy), p, font=fl, fill=AMARELO if i == ativa else (255, 255, 255), anchor="lm", stroke_width=8, stroke_fill=(0, 0, 0))
        x += d.textlength(p, font=fl) + esp

def chip(d, y, txt, cor, icone):
    w = d.textlength(txt, font=f_chip) + 130; x0 = (W - w) / 2
    d.rounded_rectangle((x0, y, x0 + w, y + 84), radius=42, fill=cor)
    cx, cy = x0 + 50, y + 42
    d.ellipse((cx - 24, cy - 24, cx + 24, cy + 24), fill="white")
    if icone == "x":
        d.line((cx - 10, cy - 10, cx + 10, cy + 10), fill=cor, width=7); d.line((cx - 10, cy + 10, cx + 10, cy - 10), fill=cor, width=7)
    else:
        d.line((cx - 11, cy + 1, cx - 3, cy + 10, cx + 12, cy - 9), fill=cor, width=7, joint="curve")
    d.text((x0 + 88, cy), txt, font=f_chip, fill="white", anchor="lm")

def preco(img, t):
    if t < CTA_INI + 2.6: return
    k = min(1, (t - CTA_INI - 2.6) / 0.3); a = int(255 * k)
    d = ImageDraw.Draw(img, "RGBA"); w, h = 440, 128; x0 = (W - w) // 2; y0 = 430 + int((1 - k) * 30)
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), radius=64, fill=(11, 79, 58, a))
    d.text((W / 2, y0 + h / 2 - 2), "R$27,90", font=f_preco, fill=(255, 255, 255, a), anchor="mm")

def leitor(arq, ini, dur, z=1.0):
    cmd = ["ffmpeg", "-loglevel", "quiet", "-ss", str(ini), "-t", str(dur + 0.2), "-i", arq, "-vf", f"fps={FPS},scale={W}:{H}",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE); n = int(round(dur * FPS)); im = None
    for i in range(n):
        buf = p.stdout.read(W * H * 3)
        if len(buf) == W * H * 3: im = Image.frombytes("RGB", (W, H), buf)
        if z != 1.0:
            s = 1 + (z - 1) * i / max(1, n - 1); cw, ch = W / s, H / s
            yield im.crop(((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2)).resize((W, H), Image.LANCZOS)
        else: yield im
    p.kill()

def metade(lista):
    for arq, ini, dur, y in lista:
        for im in leitor(arq, ini, dur):
            yield im.crop((0, y, W, y + 960))

def main():
    tmpv = "/tmp/est4_video.mp4"
    enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", tmpv], stdin=subprocess.PIPE)
    fr = 0
    for cima, baixo in zip(metade(CIMA), metade(BAIXO)):
        t = fr / FPS; im = Image.new("RGB", (W, H)); im.paste(cima, (0, 0)); im.paste(baixo, (0, 960))
        d = ImageDraw.Draw(im); d.rectangle((0, 955, W, 965), fill="white")
        chip(d, 790, "“Vou confirmar e te aviso.”", TERRA, "x")
        chip(d, 1390, "Responde na hora, com o Mapa", TEAL, "v")
        legenda(im, t); enc.stdin.write(im.tobytes()); fr += 1
    assert abs(fr / FPS - SPLIT_FIM) < 0.05, fr
    for arq, ini, dur, z in CHEIA:
        for im in leitor(arq, ini, dur, z):
            t = fr / FPS; im = im.copy(); legenda(im, t); preco(im, t); enc.stdin.write(im.tobytes()); fr += 1
    enc.stdin.close(); enc.wait()
    filt = [f"[1:a]atrim=start=0.35,asetpts=PTS-STARTPTS,aresample=48000,pan=mono|c0=c0[a0]",
            f"[2:a]aresample=48000,pan=mono|c0=c0,adelay=7190[a1]",
            f"[3:a]aresample=48000,pan=mono|c0=c0,adelay={int(CTA_INI*1000)}[a2]",
            f"[a0][a1][a2]amix=inputs=3:normalize=0,highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,loudnorm=I=-14:TP=-1.5:LRA=9,atrim=0:{TOTAL},apad=whole_dur={TOTAL}[aout]"]
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmpv, "-i", U + "cortes3/HOOK1_pt_1.wav", "-i", U + "cortes3/HOOK1_pt_2.wav",
                    "-i", U + "cortes/cta2.mov", "-filter_complex", ";".join(filt), "-map", "0:v", "-map", "[aout]", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-shortest", "-movflags", "+faststart", OUT], check=True)
    print("ok", OUT, f"{TOTAL:.2f}s", fr)

if __name__ == "__main__":
    main()
