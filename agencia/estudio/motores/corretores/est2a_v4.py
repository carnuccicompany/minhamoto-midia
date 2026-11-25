#!/usr/bin/env python3
"""EST2-A v4 (25/11) · Quiz "Você saberia responder?" — rodada 2 do Léo:
- o gancho não corta mais a fala dela: vai até o fim natural da frase ("...dá uma olhada no material que eu preparei…", pausa em 12,5 s);
- mais motion pra ficar dinâmico e diferente do EST8: ícone por pergunta (banco / casa / carteira) com estouro de partículas,
  "digitando…" antes do balão de abertura, selo "?" com mola, empurrão de câmera a cada pergunta, 3 checks no "estão no Mapa";
- balão de abertura refeito. Body/CTA = pronto AP DD 4 como está; sem preço.
"""
import sys
from v3 import *
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/corretores/out/EST2-A v4.mp4"
HOOK_FIM = 12.50
SEGS = [Seg(TRAB + "cortes4/hook4p.mov", 0.45, HOOK_FIM - 0.45),
        Seg(DD + "AP - DD 4.mp4", 15.15, 27.85),
        Seg(DD + "AP - DD 4.mp4", 66.65, 6.95)]
C1 = HOOK_FIM - 0.45; C2 = C1 + 27.85
Q = [(3.5, ["Quanto ele", "consegue financiar?"], "building-bank"),
     (5.25, ["Qual imóvel ele", "consegue comprar?"], "home-dollar"),
     (7.5, ["Quanto vai dar", "de entrada?"], "wallet")]
SN = 9.75
X0, X1 = 140, 940
_d0 = ImageDraw.Draw(Image.new("RGB", (1, 1)))
def tl(s, peso, tam): return _d0.textlength(s, font=fonte(peso, tam))

def rabo(img, x, y, cor, alpha):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).polygon([(x, y - 2), (x + 54, y - 2), (x - 8, y + 36)], fill=cor + (int(255 * alpha),))
    img.alpha_composite(lay)

def abertura(img, t):
    if t >= Q[0][0]: return
    y0 = 250
    if t < 0.5:                                         # "digitando…"
        a = ease((t - 0.03) / 0.12)
        if a <= 0: return
        x0 = W / 2 - 110
        caixa(img, x0, y0 + 40, x0 + 220, y0 + 150, 55, BRANCO, a); rabo(img, x0 + 40, y0 + 150, BRANCO, a)
        for i in range(3):
            ph = (t * 7 - i * 0.6); dy = -10 * max(0, math.sin(ph)) if ph > 0 else 0
            disco(img, x0 + 70 + i * 40, y0 + 95 + dy, 11, (150, 162, 180), a, sombra=False)
        return
    p = (t - 0.5) / 0.6; k = mola(p); a = ease(p * 3)
    l1, l2, tam = "Você saberia", "responder?", 82
    tw = max(tl(l1, 800, tam), tl(l2, 800, tam)); bw = tw + 2 * 60; bh = 2 * int(tam * 1.18) + 2 * 40
    s = 0.85 + 0.15 * k                                 # cresce com mola a partir do "digitando"
    cx, cy = W / 2, y0 + bh / 2
    x0, x1 = cx - bw * s / 2, cx + bw * s / 2; yy0, yy1 = cy - bh * s / 2, cy + bh * s / 2
    caixa(img, x0, yy0, x1, yy1, 46, BRANCO, a); rabo(img, x0 + 70, yy1, BRANCO, a)
    if p > 0.02:
        ta = ease((p - 0.02) * 6)
        texto(img, (cx, cy - int(tam * 0.59)), l1, 800, tam, NAVY, ta, anchor="mm")
        texto(img, (cx, cy + int(tam * 0.59)), l2, 800, tam, TEAL, ta, anchor="mm")
    # selo "?" coral pulando no canto
    q = (t - 0.75) / 0.5
    if q > 0:
        r = int(52 * mola(q)); wob = 4 * math.sin(t * 6) * math.exp(-(t - 0.75) * 0.8)
        disco(img, x1 - 18, yy0 + 8 + wob, r, CORAL, min(1, q * 3))
        if r > 20: icone(img, "help", x1 - 18, yy0 + 8 + wob, int(r * 1.25))
        particulas(img, x1 - 18, yy0 + 8, t - 0.75, seed=7)

def pergunta(img, t):
    if not (Q[0][0] <= t < SN + 0.22): return
    # cabeçalho fixo
    k = ease((t - Q[0][0]) / 0.25) * (1 - ease((t - SN) / 0.2))
    hw = tl("Você saberia responder?", 700, 34)
    caixa(img, W / 2 - hw / 2 - 28, 170, W / 2 + hw / 2 + 28, 232, 31, NAVY, k, sombra=False)
    texto(img, (W / 2, 201), "Você saberia responder?", 700, 34, BRANCO, k, anchor="mm")
    for i, (t0, lin, ic) in enumerate(Q):
        t1 = Q[i + 1][0] if i + 1 < len(Q) else SN
        if t0 <= t < t1: p = (t - t0) / 0.42; dx = int((1 - mola(p)) * 420); a = ease(p * 2.5)
        elif t1 <= t < t1 + 0.22: p = (t - t1) / 0.22; dx = -int(ease(p) * 380); a = 1 - p
        else: continue
        tam = 52; lh = int(tam * 1.22); pad = 34
        tw = max(tl(l, 700, tam) for l in lin); bw = min(X1 - X0, pad + 146 + tw + 120); bh = 2 * pad + 2 * lh
        x0 = W / 2 - bw / 2 + dx; y0 = 262
        caixa(img, x0, y0, x0 + bw, y0 + bh, 40, BRANCO, a); rabo(img, x0 + 70, y0 + bh, BRANCO, a)
        icx, icy = x0 + pad + 60, y0 + bh / 2
        ri = int(60 * (mola((t - t0) / 0.5) if t < t1 else 1))
        disco(img, icx, icy, ri, TEAL, a, sombra=False)
        if ri > 20: icone(img, ic, icx, icy, int(ri * 1.15), a)
        for j, l in enumerate(lin): texto(img, (x0 + pad + 146, y0 + pad + j * lh), l, 700, tam, NAVY, a)
        for kk in range(3):                               # progresso
            cx = x0 + bw - 30 - (2 - kk) * 24; c = TEAL if kk <= i else (205, 214, 226)
            disco(img, cx, y0 + 30, 7, c, a, sombra=False)
        if t < t1: particulas(img, icx, icy, t - t0, seed=i + 2)

def resposta(img, t):
    if not (SN <= t < C1): return
    p = (t - SN) / 0.45; a = ease(p * 2.5); dx = int((1 - mola(p)) * 300)
    l1, l2, tam = "As 3 respostas", "estão no Mapa.", 64
    tw = max(tl(l1, 800, tam), tl(l2, 800, tam)); bw = 50 + 120 + 24 + tw + 50; bh = 2 * int(tam * 1.2) + 2 * 36
    x0 = W / 2 - bw / 2 + dx; y0 = 232
    caixa(img, x0, y0, x0 + bw, y0 + bh, 44, TEAL, a); rabo(img, x0 + 70, y0 + bh, TEAL, a)
    icx, icy = x0 + 50 + 60, y0 + bh / 2
    disco(img, icx, icy, 60, NAVY, a, sombra=False); icone(img, "circle-check", icx, icy, 76, a)
    texto(img, (x0 + 50 + 144, y0 + 36), l1, 800, tam, BRANCO, a)
    texto(img, (x0 + 50 + 144, y0 + 36 + int(tam * 1.2)), l2, 800, tam, BRANCO, a)
    # os 3 checks das 3 perguntas, um por um
    for j in range(3):
        tj = SN + 0.55 + j * 0.28
        if t >= tj:
            r = int(26 * mola((t - tj) / 0.35)); cx = x0 + bw - 40 - (2 - j) * 62; cy = y0 + bh + 6
            disco(img, cx, cy, r, BRANCO, a)
            if r > 10:
                lay = Image.open(ICON + "check.png").convert("RGBA").resize((int(r * 1.3),) * 2, Image.LANCZOS)
                arr = np.array(lay); arr[..., :3] = TEAL; lay = Image.fromarray(arr)
                img.alpha_composite(lay, (int(cx - r * 0.65), int(cy - r * 0.65)))
    particulas(img, icx, icy, t - SN, seed=11, raio=200)

def cam(t):
    if t >= C1: return 1.0
    z = 1.0
    for tq in [Q[0][0], Q[1][0], Q[2][0], SN]:
        d = t - tq
        if 0 <= d < 1.4: z = max(z, 1 + 0.035 * (ease(d / 0.2) if d < 0.2 else 1 - ease((d - 0.2) / 1.2)))
    return z

SFX = [(0.05, "pop", -19), (0.5, "pop", -15), (0.75, "pop", -17)] + [(q[0], "pop", -15) for q in Q] + \
      [(SN, "pop", -14)] + [(SN + 0.55 + j * 0.28, "pop", -21) for j in range(3)] + [(C1 - 0.16, "whoosh", -13), (C2 - 0.16, "whoosh", -15)]
if __name__ == "__main__":
    d = render(SEGS, [abertura, pergunta, resposta], [C1, C2], SFX, OUT, cam=cam)
    print("ok", OUT, round(d, 2))
