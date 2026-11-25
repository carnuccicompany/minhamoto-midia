#!/usr/bin/env python3
"""EST2-A v3 (25/11) · Quiz "Você saberia responder?" — correções do Léo:
balão do quiz refeito (cara de pergunta de cliente), perguntas somem quando ela diz "se não, dá uma olhada no material",
body longo = trecho do pronto AP DD 4 (15,15→43,0 s) como está, CTA = o próprio CTA do DD 4 ("Clique em Saiba Mais…"), sem preço.
"""
import sys
from v3 import *
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/corretores/out/EST2-A v3.mp4"
SEGS = [Seg(TRAB + "cortes4/hook4p.mov", 0.45, 11.0),
        Seg(DD + "AP - DD 4.mp4", 15.15, 27.85),
        Seg(DD + "AP - DD 4.mp4", 66.65, 6.95)]
C1 = 11.0; C2 = C1 + 27.85
Q = [(3.5, ["Quanto ele", "consegue financiar?"]), (5.25, ["Qual imóvel ele", "consegue comprar?"]), (7.5, ["Quanto vai dar", "de entrada?"])]
SN = 9.75
X0, X1 = 140, 940

def balao(img, y, linhas, tam, fundo, cor, alpha, dx=0, badge=None, prog=None):
    pad_x, pad_y, lh = 44, 30, int(tam * 1.22)
    h = pad_y * 2 + lh * len(linhas)
    d0 = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    tw = max(d0.textlength(l, font=fonte(700, tam)) for l in linhas)
    full = pad_x * 2 + tw + (92 if badge else 0) + (70 if prog else 0)
    full = min(X1 - X0, full)
    x0 = int(W / 2 - full / 2) + dx; x1 = int(W / 2 + full / 2) + dx
    caixa(img, x0, y, x1, y + h, 38, fundo, alpha)
    # rabinho do balão (pergunta chegando)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).polygon([(x0 + 70, y + h - 2), (x0 + 120, y + h - 2), (x0 + 62, y + h + 34)], fill=fundo + (int(255 * alpha),))
    img.alpha_composite(lay)
    tx = x0 + pad_x
    if badge:
        cx, cy = x0 + pad_x + 34, y + h / 2
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.ellipse((cx - 34, cy - 34, cx + 34, cy + 34), fill=TEAL + (int(255 * alpha),))
        d.text((cx, cy), badge, font=fonte(800, 38), fill=BRANCO + (int(255 * alpha),), anchor="mm")
        img.alpha_composite(lay); tx += 92
    for i, l in enumerate(linhas):
        texto(img, (tx, y + pad_y + i * lh), l, 700, tam, cor, alpha)
    if prog:
        n, tot = prog
        for k in range(tot):
            cx = x1 - 40 - (tot - 1 - k) * 26; cy = y + 34
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
            c = TEAL if k < n else (205, 214, 226)
            d.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=c + (int(255 * alpha),))
            img.alpha_composite(lay)
    return h

def quiz(img, t):
    if t >= C1: return
    if t < Q[0][0]:                                   # abertura: a pergunta grande
        k = mola((t - 0.05) / 0.55); a = ease((t - 0.05) / 0.18)
        if a <= 0: return
        y = 230 + int((1 - k) * 60)
        balao(img, y, ["Você saberia", "responder?"], 74, BRANCO, NAVY, a)
        return
    if t < SN:
        # cabeçalho pequeno fixo
        k = ease((t - Q[0][0]) / 0.25)
        lay_w = ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength("Você saberia responder?", font=fonte(700, 34))
        cx = W / 2; y = 170
        caixa(img, cx - lay_w / 2 - 28, y, cx + lay_w / 2 + 28, y + 62, 31, NAVY, k, sombra=False)
        texto(img, (cx, y + 31), "Você saberia responder?", 700, 34, BRANCO, k, anchor="mm")
        # pergunta da vez (entra pela direita com mola; a anterior sai pela esquerda)
        for i, (t0, q) in enumerate(Q):
            t1 = Q[i + 1][0] if i + 1 < len(Q) else SN
            lin = q
            if t0 <= t < t1:
                p = (t - t0) / 0.42; dx = int((1 - mola(p)) * 420); a = ease(p * 2.5)
                balao(img, 268, lin, 52, BRANCO, NAVY, a, dx=dx, badge=str(i + 1), prog=(i + 1, 3))
            elif t1 <= t < t1 + 0.22 and i + 1 < len(Q):
                p = (t - t1) / 0.22; balao(img, 268, lin, 52, BRANCO, NAVY, 1 - p, dx=-int(ease(p) * 380), badge=str(i + 1), prog=(i + 1, 3))
        return
    # "se não…": as perguntas saem e entra a resposta
    p = (t - SN) / 0.45; a = ease(p * 2.5)
    balao(img, 230, ["As 3 respostas", "estão no Mapa."], 64, TEAL, BRANCO, a, dx=int((1 - mola(p)) * 300))

SFX = [(0.05, "pop", -15), (Q[0][0], "pop", -17), (Q[1][0], "pop", -17), (Q[2][0], "pop", -17), (SN, "pop", -15),
       (C1 - 0.16, "whoosh", -13), (C2 - 0.16, "whoosh", -15)]
if __name__ == "__main__":
    d = render(SEGS, [quiz], [C1, C2], SFX, OUT)
    print("ok", OUT, round(d, 2))
