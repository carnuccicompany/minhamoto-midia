#!/usr/bin/env python3
"""Historinha cliente seguro (ex-EST5-A) v4 (25/11): EQ no gancho abafado + conjunto 2 de elementos (elem2).
EST5-A v3 (25/11) · Historinha "o cliente sentiu segurança" — no padrão aprovado (EST2-A v6 / EST8-A v5):
gancho = voz da AP DD 4 como veio (HOOK5 pt1, 0→7,8 s) sobre a história em 4 cenas com cartão de capítulo (ícone + progresso);
no "então dá uma olhada nesse material" entra o próprio pronto DD 4 (7,8→43,0 s: ela com o Mapa + body), legenda "custos" corrigida,
elementos centralizados acima da legenda; CTA = "Clique em Saiba Mais" da AP DD 10 + botão com toque. Sem preço, voz sem mexer.
"""
import sys
from v3 import *
from elem import *
from legfix import custos_dd4
from elem2 import *
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/corretores/out/Corretores - Historinha cliente seguro.mp4"
EQ4 = open("/home/claude/corretores/eq_hooks.txt").read().split("\n")[0]
COSTURA = 15.15   # pausa antes do "São +120": até aqui o áudio do pronto vem abafado → EQ; depois, cru
C4 = TRAB + "cortes4/"
DD4, DD10 = DD + "AP - DD 4.mp4", DD + "AP - DD 10 (ROI 10).mp4"
H1 = 7.8; C2 = 43.0
BEATS = [(0.0, 1.5, C4 + "sc_ap2.mp4", 0.6, "message-question", ["O cliente perguntou", "sobre o FGTS."]),
         (1.5, 4.2, C4 + "sc_doc4.mp4", 0.8, "list-check", ["Você explicou", "cada etapa."]),
         (4.2, 6.0, C4 + "sc_conv2.mp4", 0.4, "shield-check", ["Ele sentiu", "segurança."]),
         (6.0, H1, C4 + "sc_ap3.mp4", 0.6, "heart-handshake", ["E fechou", "com você."])]
SEGS = [Seg(src, s0, b - a, audio=False, zoom=1.04) for a, b, src, s0, _, _ in BEATS] + \
       [Seg(DD4, H1, C2 - H1, fx=custos_dd4), Seg(DD10, 2050 / 30, 73.70 - 2050 / 30)]
AUD = [Seg(DD4, 0.0, COSTURA, af=EQ4, fade_out=0.03, ganho=2.0), Seg(DD4, COSTURA, C2 - COSTURA, fade_in=0.03), Seg(DD10, 2050 / 30, 73.70 - 2050 / 30)]
CORTES = [b for _, b, *_ in BEATS[:-1]]

def capitulo(img, t):
    if t >= H1 + 0.05: return
    i = max(k for k, (a, *_r) in enumerate(BEATS) if t >= a)
    a, b, _, _, ic, lin = BEATS[i]
    p = (t - a) / 0.45; k = mola(p); al = ease(p * 3)
    if i == len(BEATS) - 1: al *= 1 - ease((t - (H1 - 0.15)) / 0.15)
    tam = 58; lh = int(tam * 1.2); tw = max(tl(l, 800, tam) for l in lin)
    w = 60 + 110 + 30 + tw + 60; h = 2 * lh + 2 * 40 + 34
    x0 = W / 2 - w / 2 + int((1 - k) * 120); y0 = 210
    caixa(img, x0, y0, x0 + w, y0 + h, 40, BRANCO, al)
    # progresso dos 4 capítulos
    for j in range(4):
        cx = x0 + 60 + j * 34; c = TEAL if j <= i else (205, 214, 226)
        disco(img, cx, y0 + 32, 8, c, al, sombra=False)
    icx, icy = x0 + 60 + 55, y0 + 34 + 40 + lh
    r = int(55 * mola((t - a) / 0.5)); disco(img, icx, icy, r, TEAL if i else CORAL, al, sombra=False)
    if r > 16: icone(img, ic, icx, icy, int(r * 1.15), al)
    for j, l in enumerate(lin):
        texto(img, (x0 + 60 + 110 + 30, y0 + 34 + 40 + j * lh), l, 800, tam, NAVY if j == 0 else TEAL, al)
    particulas(img, icx, icy, t - a, n=10, raio=120, seed=90 + i)

TEMAS = [(19.0, "pig-money", "FGTS"), (20.75, "home", "MCMV"), (22.0, "users-group", "Consórcio"),
         (23.0, "file-text", "Documentos"), (24.25, "calendar-time", "Prazos"), (25.0, "receipt", "Custos")]
JEITO = [(31.05, "photo", "Ilustrado"), (32.05, "layout-list", "Organizado"), (33.15, "bulb", "Fácil")]
FORMAS = [(39.65, "building-bank", "Financiar"), (39.95, "cash", "À vista"), (40.25, "pig-money", "FGTS"),
          (40.55, "users-group", "Consórcio"), (40.85, "arrows-exchange", "Permuta")]
def body(img, t):
    if not (H1 + 0.3 <= t < C2): return
    anel(img, t, 15.25, 17.3)
    adesivos(img, t, TEMAS[0][0] - 0.15, 26.0, TEMAS, "Tudo isso no Mapa", seed=450)
    palavra(img, t, JEITO, 34.75)
    riscado(img, t, 36.15, 36.7, 37.75)
    cartoes_flip(img, t, FORMAS[0][0] - 0.15, 42.55, FORMAS, "Todas as formas de aquisição")
def fim(img, t): cta(img, t, C2, tap=0.67)

def cam(t):
    if t >= H1: return 1.0
    for a, b, *_ in BEATS:
        if a <= t < b: return 1.0 + 0.045 * ((t - a) / (b - a))       # empurrão lento em cada cena da história
    return 1.0

SFX = [(a + 0.02, "pop", -15) for a, *_r in BEATS] + [(H1 - 0.16, "whoosh", -13)] + \
      [(15.25, "pop", -20)] + [(tk, "pop", -23) for tk, _, _ in TEMAS + JEITO + FORMAS] + [(36.15, "pop", -21), (36.7, "pop", -19)] + \
      [(C2 - 0.16, "whoosh", -15), (C2 + 0.10, "pop", -19), (C2 + 0.67, "pop", -16)]
OVS = [capitulo, body, fim]
if __name__ == "__main__":
    d = render(SEGS, [capitulo, body, fim], [H1, C2], SFX, OUT, audio_segs=AUD, cam=cam)
    print("ok", OUT, round(d, 2))
