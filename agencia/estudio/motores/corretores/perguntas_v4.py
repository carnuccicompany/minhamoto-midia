#!/usr/bin/env python3
"""Perguntas fora do básico (ex-EST2-C) v4 (25/11): EQ no gancho do DD 10 + conjunto 3 de elementos (elem3).
EST2-C v3 (25/11) · "As perguntas do cliente que saem do básico" — padrão aprovado:
gancho = voz da AP DD 10 como veio (HOOK1: "se você quer ser o corretor que sabe responder quando a negociação sai do básico…")
sobre uma cena desfocada com uma conversa de cliente (perguntas que NÃO são básicas, todas respondidas no Mapa) e a resposta
"Sei responder as três."; no "e dá uma olhada nesse material" entra o próprio pronto DD 10 (7,4→43,3 s), legenda "custos"
corrigida, elementos centralizados; CTA = "Clique em Saiba Mais" do DD 10 + botão com toque. Sem preço, voz sem mexer.
"""
import sys, pickle
from v3 import *
from elem import *
import legfix2
from elem3 import *
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/corretores/out/Corretores - Perguntas fora do basico.mp4"
EQ10 = open("/home/claude/corretores/eq_hooks.txt").read().split("\n")[1]
COSTURA = 15.42   # pausa antes do "São +120" no DD 10: gancho abafado → EQ; depois, cru
C4 = TRAB + "cortes4/"
DD10 = DD + "AP - DD 10 (ROI 10).mp4"
FIX = pickle.load(open("/home/claude/corretores/fix_dd10.pkl", "rb"))
H1 = 7.4; C2 = 43.3; CTA0 = 2050 / 30
FUNDO = "boxblur=14:2,eq=brightness=-0.10:saturation=0.85"
SEGS = [Seg(C4 + "sc_vendo.mp4", 0.3, 3.7, FUNDO, audio=False, zoom=1.05),
        Seg(C4 + "sc_duv_corretor.mp4", 0.3, H1 - 3.7, FUNDO, audio=False, zoom=1.05),
        Seg(DD10, H1, C2 - H1, fx=lambda im, tf: legfix2.aplica(FIX, im, tf)),
        Seg(DD10, CTA0, 73.70 - CTA0)]
AUD = [Seg(DD10, 0.0, COSTURA, af=EQ10, fade_out=0.03, ganho=1.5), Seg(DD10, COSTURA, C2 - COSTURA, fade_in=0.03), Seg(DD10, CTA0, 73.70 - CTA0)]

MSGS = [(0.65, ["A avaliação veio abaixo", "do valor. E agora?"]),
        (2.65, ["Dá pra usar FGTS em", "imóvel na planta?"]),
        (4.0, ["O vendedor tem dívida.", "Isso trava a venda?"])]
RESP = 5.75
X0, X1 = 140, 940
def bolha(img, x0, y, lin, fundo, cor, a, dx=0, tam=38, direita=False):
    lh = int(tam * 1.25); tw = max(tl(l, 600, tam) for l in lin); w = tw + 2 * 30; h = len(lin) * lh + 2 * 20
    if direita: x0 = X1 - 34 - w
    caixa(img, x0 + dx, y, x0 + dx + w, y + h, 28, fundo, a, sombra=False)
    for j, l in enumerate(lin): texto(img, (x0 + dx + 30, y + 20 + j * lh), l, 600, tam, cor, a)
    bolha.ult = (x0 + dx, x0 + dx + w, lh, tl(lin[-1], 600, tam))
    return h
def conversa(img, t):
    if t >= H1 + 0.05: return
    a = ease((t - 0.05) / 0.3) * (1 - ease((t - (H1 - 0.12)) / 0.12))
    # altura do cartão cresce conforme as mensagens chegam
    n = sum(1 for tm, _ in MSGS if t >= tm - 0.35); resp = t >= RESP - 0.1
    hh = 120 + 26 + sum(2 * int(38 * 1.25) + 40 + 22 for tm, _ in MSGS[:n]) + (2 * int(38 * 1.25) + 40 + 22 if resp else 0) + (90 if n < 3 and t > 0.3 else 0)
    y0 = 300
    caixa(img, X0, y0, X1, y0 + hh, 40, BRANCO, a * 0.97)
    # cabeçalho da conversa
    disco(img, X0 + 70, y0 + 60, 34, (205, 214, 226), a, sombra=False); icone(img, "user", X0 + 70, y0 + 60, 40, a)
    texto(img, (X0 + 122, y0 + 40), "Cliente", 700, 36, NAVY, a)
    texto(img, (X0 + 122, y0 + 82), "digitando…" if (n < 3 and t > 0.2) else "online", 600, 24, TEAL, a)
    ImageDraw.Draw(img)  # noop
    y = y0 + 120 + 26
    for i, (tm, lin) in enumerate(MSGS):
        if t < tm - 0.35: break
        if t < tm:                                          # "digitando…" antes de cada mensagem
            caixa(img, X0 + 34, y, X0 + 34 + 130, y + 66, 28, (238, 241, 245), a, sombra=False)
            for k in range(3):
                ph = (t * 7 - k * 0.6); dy = -8 * max(0, math.sin(ph)) if ph > 0 else 0
                disco(img, X0 + 34 + 34 + k * 31, y + 33 + dy, 8, (150, 162, 180), a, sombra=False)
            break
        p = (t - tm) / 0.4
        h = bolha(img, X0 + 34, y + int((1 - mola(p)) * 24), lin, (238, 241, 245), NAVY, a * ease(p * 3))
        if i == 2 and t >= tm + 0.1:                        # "sai do básico": selo coral
            q = (t - tm - 0.1) / 0.4; s = "Fora do básico"; w = tl(s, 800, 26) + 36
            bx1 = bolha.ult[1]; sx = min(bx1 - 70, X1 - 12 - w); sy = y - 30
            caixa(img, sx, sy + int((1 - mola(q)) * 20), sx + w, sy + 50 + int((1 - mola(q)) * 20), 25, CORAL, a * ease(q * 3), sombra=False)
            texto(img, (sx + w / 2, sy + 25 + int((1 - mola(q)) * 20)), s, 800, 26, BRANCO, a * ease(q * 3), anchor="mm")
            particulas(img, sx + w / 2, sy + 25, t - tm - 0.1, cores=(CORAL, (255, 214, 10), TEAL), n=10, raio=110, seed=5)
        y += h + 22
    if resp:
        p = (t - RESP) / 0.45
        if p > 0:
            yy = y + int((1 - mola(p)) * 24)
            h = bolha(img, 0, yy, ["Sei responder", "as três.      "], TEAL, BRANCO, a * ease(p * 3), direita=True)
            bx0, bx1, lh, lw = bolha.ult
            icone(img, "check", bx0 + 30 + tl("as três. ", 600, 38) + 22, yy + 20 + lh + lh * 0.5, 40, a * ease(p * 3))
            particulas(img, X1 - 120, y + h / 2, t - RESP, n=12, raio=150, seed=9)

TEMAS = [(19.75, "pig-money", "FGTS"), (20.75, "home", "MCMV"), (22.25, "users-group", "Consórcio"),
         (23.25, "file-text", "Documentos"), (24.5, "calendar-time", "Prazos"), (25.25, "receipt", "Custos")]
JEITO = [(31.0, "photo", "Ilustrado"), (32.25, "layout-list", "Organizado"), (33.25, "bulb", "Fácil")]
FORMAS = [(40.75, "building-bank", "Financiar"), (41.05, "cash", "À vista"), (41.35, "pig-money", "FGTS"),
          (41.65, "users-group", "Consórcio"), (41.95, "arrows-exchange", "Permuta")]
def body(img, t):
    if not (H1 + 0.3 <= t < C2): return
    carimbo(img, t, 15.5, 17.6)
    checklist(img, t, TEMAS[0][0] - 0.3, 26.3, TEMAS)
    marcatexto(img, t, JEITO, 34.6)
    chave(img, t, 36.5, 37.25, 38.2)
    deslizantes(img, t, FORMAS[0][0] - 0.15, 42.9, FORMAS, "Todas as formas de aquisição")
def fim(img, t): cta(img, t, C2, tap=0.67)
def cam(t):
    if t >= H1: return 1.0
    z = 1.0 + 0.04 * (t / H1)
    for tq in [m[0] for m in MSGS] + [RESP]:
        d = t - tq
        if 0 <= d < 1.0: z += 0.02 * (ease(d / 0.2) if d < 0.2 else 1 - ease((d - 0.2) / 0.8))
    return z

SFX = [(m[0], "pop", -15) for m in MSGS] + [(4.1, "pop", -18), (RESP, "pop", -14), (H1 - 0.16, "whoosh", -13)] + \
      [(15.5, "pop", -20)] + [(tk, "pop", -23) for tk, _, _ in TEMAS + JEITO + FORMAS] + [(36.5, "pop", -21), (37.25, "pop", -19)] + \
      [(C2 - 0.16, "whoosh", -15), (C2 + 0.10, "pop", -19), (C2 + 0.67, "pop", -16)]
OVS = [conversa, body, fim]
if __name__ == "__main__":
    d = render(SEGS, [conversa, body, fim], [H1, C2], SFX, OUT, audio_segs=AUD, cam=cam)
    print("ok", OUT, round(d, 2))
