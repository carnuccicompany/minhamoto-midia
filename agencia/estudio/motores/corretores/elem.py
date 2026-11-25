"""Elementos aprovados (EST2-A v6, 25/11) reutilizáveis: faixa de ícones centralizada acima da legenda, contador +120,
"?"→"✓" (nunca mais na dúvida), botão "Saiba mais" com toque. Tudo parametrizado por tempo."""
from v3 import *
_d0 = ImageDraw.Draw(Image.new("RGB", (1, 1)))
def tl(s, peso, tam): return _d0.textlength(s, font=fonte(peso, tam))
FAIXA_Y = 1335
def faixa_icones(img, t, t_in, t_out, itens, titulo=None, seed=50):
    if not (t_in <= t < t_out + 0.3): return
    a = ease((t - t_in) / 0.3) * (1 - ease((t - t_out) / 0.3))
    n = len(itens); pad = 18; cw = min(160, (800 - 2 * pad) / n); th = 46 if titulo else 0
    w = n * cw + 2 * pad; h = 168 + th
    x0 = W / 2 - w / 2; y0 = FAIXA_Y - h + int((1 - ease((t - t_in) / 0.4)) * 30)
    caixa(img, x0, y0, x0 + w, y0 + h, 34, BRANCO, a * 0.94)
    if titulo: texto(img, (W / 2, y0 + 30), titulo, 700, 28, TEAL, a, anchor="mm")
    for k, (tk, ic, rot) in enumerate(itens):
        if t < tk: continue
        p = (t - tk) / 0.45; r = int(44 * mola(p)); cx = x0 + pad + cw * k + cw / 2; cy = y0 + th + 64
        disco(img, cx, cy, r, TEAL, a, sombra=False)
        if r > 14: icone(img, ic, cx, cy, int(r * 1.15), a)
        texto(img, (cx, y0 + th + 136), rot, 700, 19 if n >= 6 else 24, NAVY, a * ease(p * 3), anchor="mm")
        particulas(img, cx, cy, t - tk, n=8, raio=80, seed=seed + k)
def contador(img, t, t0, t1):
    if not (t0 <= t < t1 + 0.3): return
    a = ease((t - t0) / 0.25) * (1 - ease((t - t1) / 0.3)); k = mola((t - t0) / 0.5)
    n = int(120 * ease((t - t0) / 1.0))
    w, h = 470, 150; x0 = W / 2 - w / 2; y0 = FAIXA_Y - h + int((1 - k) * 30)
    caixa(img, x0, y0, x0 + w, y0 + h, 34, BRANCO, a * 0.94)
    disco(img, x0 + 84, y0 + h / 2, 52, TEAL, a, sombra=False); icone(img, "stack-2", x0 + 84, y0 + h / 2, 62, a)
    texto(img, (x0 + 158, y0 + 58), f"+{n}", 800, 72, NAVY, a, anchor="lm")
    texto(img, (x0 + 160, y0 + 112), "mapas visuais", 700, 30, TEAL, a, anchor="lm")
def duvida(img, t, t0, tv, t1):
    if not (t0 <= t < t1 + 0.3): return
    a = ease((t - t0) / 0.25) * (1 - ease((t - t1) / 0.3))
    w, h = 150 + tl("Nunca mais na dúvida", 800, 40) + 44, 140
    x0 = W / 2 - w / 2; y0 = FAIXA_Y - h + int((1 - mola((t - t0) / 0.5)) * 30)
    caixa(img, x0, y0, x0 + w, y0 + h, 34, BRANCO, a * 0.94)
    cx, cy = x0 + 80, y0 + h / 2
    if t < tv:
        disco(img, cx, cy, 48, CORAL, a, sombra=False); icone(img, "question-mark", cx, cy, 56, a)
    else:
        r = int(48 * mola((t - tv) / 0.4)); disco(img, cx, cy, r, TEAL, a, sombra=False)
        if r > 14: icone(img, "check", cx, cy, int(r * 1.15), a)
        particulas(img, cx, cy, t - tv, n=10, raio=110, seed=77)
    texto(img, (x0 + 150, cy), "Nunca mais na dúvida", 800, 40, NAVY, a, anchor="lm")
def cta(img, t, C2, tap=0.55):
    if t < C2 or t > C2 + 3.0: return
    t0 = C2 + 0.10; tt = C2 + tap
    p = (t - t0) / 0.45; a = ease(p * 3) * (1 - ease((t - (C2 + 2.6)) / 0.35))
    if a <= 0: return
    s = 1.0 - (0.06 * math.sin(min(1, max(0, (t - tt) / 0.18)) * math.pi))
    w, h = 470 * s, 112 * s; cx, cy = W / 2, 300 + int((1 - mola(p)) * 40)
    caixa(img, cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, h / 2, TEAL, a)
    texto(img, (cx - 26, cy), "Saiba mais", 800, int(52 * s), BRANCO, a, anchor="mm")
    icone(img, "arrow-right", cx + 150 * s, cy, int(48 * s), a)
    if t >= tt - 0.35:
        q = (t - (tt - 0.35)) / 0.35
        hx = cx + 205 + int((1 - ease(q)) * 110); hy = cy + 62 + int((1 - ease(q)) * 110)
        ds = 1.0 - 0.12 * math.sin(min(1, max(0, (t - tt) / 0.18)) * math.pi)
        lay = Image.open(ICON + "dedo.png").convert("RGBA"); sz = int(120 * ds); lay = lay.resize((sz, sz), Image.LANCZOS)
        if a < 1: lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
        img.alpha_composite(lay, (int(hx - sz * 0.42), int(hy - sz * 0.18)))
    if tt <= t < tt + 0.6:
        r = int(60 + 260 * ease((t - tt) / 0.6)); al = int(160 * (1 - (t - tt) / 0.6))
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).ellipse((cx - r, cy - r * 0.45, cx + r, cy + r * 0.45), outline=(255, 255, 255, al), width=6)
        img.alpha_composite(lay)
        particulas(img, cx, cy, t - tt, seed=31, raio=260, n=14)

