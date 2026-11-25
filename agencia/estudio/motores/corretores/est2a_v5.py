#!/usr/bin/env python3
"""EST2-A v5 (25/11) — rodada 3: legenda "custos" corrigida no pronto, fala inteira até o "você", card "Essas e muitas outras respostas estão no Mapa", motion elegante também no body (+120 / temas) e no CTA (botão Saiba mais).
Base: EST2-A v4 (25/11) · Quiz "Você saberia responder?" — rodada 2 do Léo:
- o gancho não corta mais a fala dela: vai até o fim natural da frase ("...dá uma olhada no material que eu preparei…", pausa em 12,5 s);
- mais motion pra ficar dinâmico e diferente do EST8: ícone por pergunta (banco / casa / carteira) com estouro de partículas,
  "digitando…" antes do balão de abertura, selo "?" com mola, empurrão de câmera a cada pergunta, 3 checks no "estão no Mapa";
- balão de abertura refeito. Body/CTA = pronto AP DD 4 como está; sem preço.
"""
import sys
from v3 import *
from legfix import custos_dd4
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/corretores/out/EST2-A v5.mp4"
HOOK_FIM = 12.95
SEGS = [Seg(TRAB + "cortes4/hook4p.mov", 0.45, HOOK_FIM - 0.45, fade_out=0.06),
        Seg(DD + "AP - DD 4.mp4", 15.15, 27.85, fx=custos_dd4),
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
    l1, l2, tam = "Essas e muitas outras", "respostas estão no Mapa.", 54
    tw = max(tl(l1, 800, tam), tl(l2, 800, tam)); bw = tw + 2 * 40; bh = 2 * int(tam * 1.22) + 2 * 34
    x0 = W / 2 - bw / 2 + dx; y0 = 232
    caixa(img, x0, y0, x0 + bw, y0 + bh, 44, TEAL, a); rabo(img, x0 + 70, y0 + bh, TEAL, a)
    texto(img, (W / 2 + dx, y0 + 34 + int(tam * 0.61)), l1, 800, tam, BRANCO, a, anchor="mm")
    texto(img, (W / 2 + dx, y0 + 34 + int(tam * 1.83)), l2, 800, tam, BRANCO, a, anchor="mm")
    # as 3 perguntas viram check e entra o "+120 mapas"
    cy = y0 + bh + 8; xr = x0 + bw - 36
    for j in range(3):
        tj = SN + 0.55 + j * 0.25
        if t >= tj:
            r = int(26 * mola((t - tj) / 0.35)); cx = xr - 280 + j * 62
            disco(img, cx, cy, r, BRANCO, a)
            if r > 10:
                lay = Image.open(ICON + "check.png").convert("RGBA").resize((int(r * 1.3),) * 2, Image.LANCZOS)
                arr = np.array(lay); arr[..., :3] = TEAL; lay = Image.fromarray(arr)
                img.alpha_composite(lay, (int(cx - r * 0.65), int(cy - r * 0.65)))
    t4 = SN + 0.55 + 3 * 0.25 + 0.1
    if t >= t4:
        k = mola((t - t4) / 0.4); w4 = tl("+120 mapas", 800, 30) + 40
        cx = xr - 70; caixa(img, cx - w4 / 2, cy - 26 + int((1 - k) * 20), cx + w4 / 2, cy + 26 + int((1 - k) * 20), 26, CORAL, min(1, (t - t4) * 6))
        texto(img, (cx, cy + int((1 - k) * 20)), "+120 mapas", 800, 30, BRANCO, min(1, (t - t4) * 6), anchor="mm")
        particulas(img, cx, cy, t - t4, seed=13, raio=120, n=10)

# ---------- body (elegante, num canto só, sem cobrir título de página) ----------
def ob(f): return C1 + (f - 15.15)          # tempo do arquivo do pronto → tempo do vídeo
TEMAS = [(19.0, "FGTS"), (20.75, "Minha Casa Minha Vida"), (22.0, "Consórcio"), (23.0, "Documentação"), (24.25, "Prazos"), (25.0, "Custos")]
# trechos depois dos temas (tempo relativo ao início do body, medido na legenda do pronto)
TEMAS2 = [(15.9, 16.9, "Ilustrado"), (16.9, 18.4, "Organizado"), (18.4, 20.0, "Fácil de entender"),
          (22.4, 24.4, "Todos os processos"), (24.4, 27.2, "Todas as formas de aquisição")]
def tag(img, t, t0, t1, txt, fundo, cor, icn=None, tam=36):
    if not (t0 <= t < t1 + 0.25): return
    p = (t - t0) / 0.4; a = ease(p * 3) * (1 - ease((t - t1) / 0.25)); dx = int((1 - mola(p)) * 160)
    w = tl(txt, 700, tam) + 2 * 26 + (52 if icn else 0); h = 70
    x1 = 940 + dx; x0 = x1 - w; y = 170
    caixa(img, x0, y, x1, y + h, h // 2, fundo, a)
    tx = x0 + 26
    if icn:
        disco(img, tx + 18, y + h / 2, 20, TEAL, a, sombra=False); icone(img, icn, tx + 18, y + h / 2, 26, a); tx += 52
    texto(img, (tx, y + h / 2), txt, 700, tam, cor, a, anchor="lm")
def body(img, t):
    if not (C1 <= t < C2): return
    f = 15.15 + (t - C1)
    if 15.25 <= f < 17.4:                      # "São +120 mapas…" com contador
        n = int(120 * ease((f - 15.25) / 0.9))
        tag(img, t, ob(15.25), ob(17.4), f"+{n} mapas visuais", TEAL, BRANCO, tam=38)
    for i, (f0, nome) in enumerate(TEMAS):
        f1 = TEMAS[i + 1][0] if i + 1 < len(TEMAS) else 25.7
        tag(img, t, ob(f0), ob(f1), nome, BRANCO, NAVY, icn="check")
        if f0 <= f < f0 + 0.6: particulas(img, 968, 205, f - f0, n=8, raio=90, seed=20 + i)
    for i, (o0, o1, nome) in enumerate(TEMAS2):
        tag(img, t, C1 + o0, C1 + o1, nome, BRANCO, NAVY, icn="check")
        if C1 + o0 <= t < C1 + o0 + 0.6: particulas(img, 968, 205, t - C1 - o0, n=8, raio=90, seed=40 + i)

# ---------- CTA: botão "Saiba mais" com toque ----------
def cta(img, t):
    if t < C2 or t > C2 + 3.0: return
    t0 = C2 + 0.10; tt = C2 + 0.62
    p = (t - t0) / 0.45; a = ease(p * 3) * (1 - ease((t - (C2 + 2.6)) / 0.35))
    if a <= 0: return
    s = 1.0 - (0.06 * math.sin(min(1, max(0, (t - tt) / 0.18)) * math.pi))
    w, h = 470 * s, 112 * s; cx, cy = W / 2, 300 + int((1 - mola(p)) * 40)
    caixa(img, cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, h / 2, TEAL, a)
    texto(img, (cx - 26, cy), "Saiba mais", 800, int(52 * s), BRANCO, a, anchor="mm")
    icone(img, "arrow-right", cx + 150 * s, cy, int(48 * s), a)
    # dedo tocando + onda
    if t >= tt - 0.35:
        q = (t - (tt - 0.35)) / 0.35
        hx = cx + 205 + int((1 - ease(q)) * 110); hy = cy + 62 + int((1 - ease(q)) * 110)
        lay = Image.open(ICON + "hand-click-navy.png").convert("RGBA").resize((96, 96), Image.LANCZOS)
        bg = Image.new("RGBA", (112, 112), (0, 0, 0, 0)); ImageDraw.Draw(bg).ellipse((0, 0, 111, 111), fill=(255, 255, 255, int(235 * a)))
        img.alpha_composite(bg, (int(hx - 56), int(hy - 56)))
        if a < 1: lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
        img.alpha_composite(lay, (int(hx - 48), int(hy - 48)))
    if tt <= t < tt + 0.6:
        r = int(60 + 260 * ease((t - tt) / 0.6)); al = int(160 * (1 - (t - tt) / 0.6))
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).ellipse((cx - r, cy - r * 0.45, cx + r, cy + r * 0.45), outline=(255, 255, 255, al), width=6)
        img.alpha_composite(lay)
        particulas(img, cx, cy, t - tt, seed=31, raio=260, n=14)

def cam(t):
    if t >= C1: return 1.0
    z = 1.0
    for tq in [Q[0][0], Q[1][0], Q[2][0], SN]:
        d = t - tq
        if 0 <= d < 1.4: z = max(z, 1 + 0.035 * (ease(d / 0.2) if d < 0.2 else 1 - ease((d - 0.2) / 1.2)))
    return z

SFX = [(0.05, "pop", -19), (0.5, "pop", -15), (0.75, "pop", -17)] + [(q[0], "pop", -15) for q in Q] + \
      [(SN, "pop", -14)] + [(SN + 0.55 + j * 0.25, "pop", -21) for j in range(3)] + [(SN + 1.40, "pop", -18)] + [(ob(15.25), "pop", -21)] + [(ob(f0), "pop", -23) for f0, _ in TEMAS] + [(C1 + o0, "pop", -23) for o0, _, _ in TEMAS2] + [(C2 + 0.10, "pop", -19), (C2 + 0.62, "pop", -16)] + [(C1 - 0.08, "whoosh", -17), (C2 - 0.16, "whoosh", -15)]
if __name__ == "__main__":
    d = render(SEGS, [abertura, pergunta, resposta, body, cta], [C1, C2], SFX, OUT, cam=cam)
    print("ok", OUT, round(d, 2))
