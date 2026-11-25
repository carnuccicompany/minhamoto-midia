#!/usr/bin/env python3
"""EST8-A v4 (25/11) · Antes × depois — refeito no PADRÃO APROVADO do EST2-A v6:
gancho = voz da AP DD 7 como veio sobre cenas em preto e branco (aprovado), agora com zoom lento, ícone por tema com "?",
partículas e empurrão de câmera; cortina "Depois" com check; body = DD 7 (7,45→37,3 s) como está, com a legenda "CURSOS"→"CUSTOS"
corrigida e os elementos centralizados acima da legenda (contador +120, temas, ilustrado/organizado/fácil, "?"→"✓", formas de
aquisição); CTA = "Clique em Saiba Mais" do DD 7 + botão "Saiba mais" com toque (dedo só símbolo). Sem preço, sem mexer na voz.
"""
import sys, pickle
from v3 import *
import legfix2
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/corretores/out/EST8-A v5.mp4"
C5 = TRAB + "cortes5/"
PB = "hue=s=0,eq=contrast=1.08:brightness=-0.02"
DD7 = DD + "AP - DD 7.mp4"
FIX = pickle.load(open("/home/claude/corretores/fix_dd7.pkl", "rb"))
def fx_dd7(img, tf): return legfix2.aplica(FIX, img, tf)
WIPE = 7.45; C2 = 37.3
SEGS = [Seg(C5 + "ap1.mp4", 1.0, 3.6, PB, audio=False, zoom=1.06),
        Seg(C5 + "duvida.mp4", 3.0, WIPE - 3.6, PB, audio=False, zoom=1.04),
        Seg(DD7, WIPE, C2 - WIPE, fx=fx_dd7),
        Seg(DD7, 62.45, 5.4)]
AUD = [Seg(DD7, 0.0, C2), Seg(DD7, 62.45, 5.4)]
_d0 = ImageDraw.Draw(Image.new("RGB", (1, 1)))
def tl(s, peso, tam): return _d0.textlength(s, font=fonte(peso, tam))

# ---------------- gancho (ANTES) ----------------
TEMAS_H = [(3.45, "pig-money", "FGTS"), (4.45, "home", "Minha Casa Minha Vida"), (5.7, "users-group", "Consórcio"), (6.45, "file-text", "Documentação")]
def pill(img, cx, y, s, fundo, cor, tam, alpha=1.0, dy=0, pad=30, peso=700):
    tw = tl(s, peso, tam); h = int(tam * 1.75)
    caixa(img, cx - tw / 2 - pad, y + dy, cx + tw / 2 + pad, y + dy + h, h // 2, fundo, alpha)
    texto(img, (cx, y + dy + h / 2), s, peso, tam, cor, alpha, anchor="mm")
def chip_q(img, cx, y, ic, nome, t, t0):
    p = (t - t0) / 0.45; a = ease(p * 3); k = mola(p); tam = 38
    tw = tl(nome, 700, tam); w = 58 + tw + 30 + 46; h = 72; dy = int((1 - k) * 34)
    x0 = cx - w / 2
    caixa(img, x0, y + dy, x0 + w, y + dy + h, h // 2, CORAL, a)
    icone(img, ic, x0 + 40, y + dy + h / 2, 38, a)
    texto(img, (x0 + 66, y + dy + h / 2), nome, 700, tam, BRANCO, a, anchor="lm")
    disco(img, x0 + w - 32, y + dy + h / 2, 20, BRANCO, a, sombra=False)
    texto(img, (x0 + w - 32, y + dy + h / 2 + 1), "?", 800, 28, CORAL, a, anchor="mm")
    particulas(img, x0 + 40, y + h / 2, t - t0, cores=(CORAL, BRANCO, (255, 214, 10)), n=8, raio=90, seed=int(t0 * 10))
def antes(img, t):
    if t >= WIPE: return
    a = ease((t - 0.05) / 0.2); k = mola((t - 0.05) / 0.5)
    pill(img, W / 2, 168, "Antes", CORAL, BRANCO, 52, a, dy=int((1 - k) * 30), pad=40, peso=800)
    a2 = ease((t - 0.35) / 0.2); k2 = mola((t - 0.35) / 0.5)
    pill(img, W / 2, 290, "“Vou confirmar e te aviso.”", BRANCO, NAVY, 44, a2, dy=int((1 - k2) * 30), pad=36)
    ys = [1150, 1240, 1330, 1420]
    for (t0, ic, nome), y in zip(TEMAS_H, ys):
        if t >= t0: chip_q(img, W / 2, y - 60, ic, nome, t, t0)
CORT_IN, CORT_HOLD, CORT_OUT = 0.28, 1.25, 0.32          # entra, fica parada pra ler, sai
def cortina(img, t):
    t0 = WIPE - CORT_IN
    if not (t0 <= t <= WIPE + CORT_HOLD + CORT_OUT): return
    if t < WIPE: x = int(W - ease((t - t0) / CORT_IN) * W)
    elif t < WIPE + CORT_HOLD: x = 0
    else: x = int(-ease((t - WIPE - CORT_HOLD) / CORT_OUT) * W)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rectangle((x, 0, x + W, H), fill=TEAL + (255,))
    img.alpha_composite(lay)
    disco(img, x + W / 2, 700, 70, BRANCO, 1, sombra=False)
    ck = Image.open(ICON + "check.png").convert("RGBA").resize((96, 96), Image.LANCZOS)
    arr = np.array(ck); arr[..., :3] = TEAL; img.alpha_composite(Image.fromarray(arr), (int(x + W / 2 - 48), 652))
    texto(img, (x + W / 2, 860), "Depois", 800, 132, BRANCO, 1, anchor="mm")
    k = ease((t - WIPE + 0.05) / 0.35) if t >= WIPE - 0.05 else 0
    texto(img, (x + W / 2, 990 + int((1 - k) * 20)), "Você responde na hora.", 700, 50, BRANCO, max(0.0, k), anchor="mm")

# ---------------- body (mesmo padrão do EST2-A aprovado; aqui o tempo do vídeo = tempo do DD 7) ----------------
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
def contador(img, t, t0=9.6, t1=11.7):
    if not (t0 <= t < t1 + 0.3): return
    a = ease((t - t0) / 0.25) * (1 - ease((t - t1) / 0.3)); k = mola((t - t0) / 0.5)
    n = int(120 * ease((t - t0) / 1.0))
    w, h = 470, 150; x0 = W / 2 - w / 2; y0 = FAIXA_Y - h + int((1 - k) * 30)
    caixa(img, x0, y0, x0 + w, y0 + h, 34, BRANCO, a * 0.94)
    disco(img, x0 + 84, y0 + h / 2, 52, TEAL, a, sombra=False); icone(img, "stack-2", x0 + 84, y0 + h / 2, 62, a)
    texto(img, (x0 + 158, y0 + 58), f"+{n}", 800, 72, NAVY, a, anchor="lm")
    texto(img, (x0 + 160, y0 + 112), "mapas visuais", 700, 30, TEAL, a, anchor="lm")
TEMAS = [(13.9, "pig-money", "FGTS"), (14.9, "home", "MCMV"), (16.4, "users-group", "Consórcio"),
         (17.4, "file-text", "Documentos"), (18.65, "calendar-time", "Prazos"), (19.4, "receipt", "Custos")]
JEITO = [(25.15, "photo", "Ilustrado"), (26.4, "layout-list", "Organizado"), (26.95, "bulb", "Fácil")]
FORMAS = [(34.9, "building-bank", "Financiar"), (35.2, "cash", "À vista"), (35.5, "pig-money", "FGTS"),
          (35.8, "users-group", "Consórcio"), (36.1, "arrows-exchange", "Permuta")]
def duvida(img, t, t0=30.65, tv=31.2, t1=32.3):
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
def body(img, t):
    if not (WIPE + CORT_HOLD + CORT_OUT <= t < C2): return
    contador(img, t)
    faixa_icones(img, t, TEMAS[0][0] - 0.15, 20.6, TEMAS, "Tudo isso no Mapa", seed=50)
    faixa_icones(img, t, JEITO[0][0] - 0.15, 28.4, JEITO, seed=60)
    duvida(img, t)
    faixa_icones(img, t, FORMAS[0][0] - 0.15, 37.0, FORMAS, "Todas as formas de aquisição", seed=70)

# ---------------- CTA (aprovado no EST2-A) ----------------
def cta(img, t):
    if t < C2 or t > C2 + 3.0: return
    t0 = C2 + 0.10; tt = C2 + 0.55
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

def cam(t):
    if t >= WIPE: return 1.0
    z = 1.0 + 0.05 * (t / WIPE)                      # zoom lento nas cenas em preto e branco (nada parado)
    for tq, _, _ in TEMAS_H:
        d = t - tq
        if 0 <= d < 1.2: z += 0.025 * (ease(d / 0.2) if d < 0.2 else 1 - ease((d - 0.2) / 1.0))
    return z

SFX = [(0.05, "pop", -15), (0.35, "pop", -18)] + [(t0, "pop", -17) for t0, _, _ in TEMAS_H] + [(WIPE - 0.32, "whoosh", -12), (WIPE + CORT_HOLD - 0.02, "whoosh", -15)] + \
      [(9.6, "pop", -20)] + [(tk, "pop", -23) for tk, _, _ in TEMAS + JEITO + FORMAS] + [(30.65, "pop", -21), (31.2, "pop", -19)] + \
      [(C2 - 0.16, "whoosh", -15), (C2 + 0.10, "pop", -19), (C2 + 0.55, "pop", -16)]
if __name__ == "__main__":
    d = render(SEGS, [antes, cortina, body, cta], [C2], SFX, OUT, audio_segs=AUD, cam=cam)
    print("ok", OUT, round(d, 2))
