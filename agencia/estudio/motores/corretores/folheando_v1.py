#!/usr/bin/env python3
"""Folheando o Mapa (ex-EST7) v1 (25/11) — estrutura B, no padrão aprovado.
Gancho = voz da AP DD 2 (HOOK2, tratada com voz.py): "Corretor, você sabe olhar a renda do seu cliente e dizer pra ele quanto
ele consegue financiar, qual o valor do imóvel que ele consegue comprar e quanto vai ter que dar de entrada?" sobre o Mapa
impresso sendo folheado (pagdet), com um mini-mapa no estilo do material montando as 3 perguntas. Na pausa antes do
"Se não, dá uma olhada no material" entra o próprio pronto DD 2 (9,5→40,3 s), legenda "custos" corrigida, elementos do
conjunto 4 (linguagem do Mapa); CTA = AP sentada (DD 10, voz tratada) + botão com toque. Sem preço.
"""
import sys, pickle, numpy as np, soundfile as sf
from v3 import *
from elem import cta
from elem4 import *
import legfix2
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/corretores/out/Corretores - Folheando o Mapa.mp4"
C5 = TRAB + "cortes5/"; V = "/home/claude/corretores/voz/"
DD2, DD10 = DD + "AP - DD 2.mp4", DD + "AP - DD 10 (ROI 10).mp4"
FIX = pickle.load(open("/home/claude/corretores/fix_dd2.pkl", "rb"))
H1 = 9.5; C2 = 40.3; CTA0 = 2050 / 30; CTA_D = 73.70 - CTA0; COSTURA = 12.27
PG = C5 + "pagdet.mp4"
BEATS = [(0.0, 2.95, 3.0), (2.95, 5.2, 10.6), (5.2, 7.4, 23.5), (7.4, H1, 31.0)]   # (início, fim, ponto no vídeo do Mapa folheado)
SEGS = [Seg(PG, s0, b - a, audio=False, zoom=1.06) for a, b, s0 in BEATS] + \
       [Seg(DD2, H1, C2 - H1, fx=lambda im, tf: legfix2.aplica(FIX, im, tf)), Seg(DD10, CTA0, CTA_D)]
AUD = [Seg(V + "g2.wav", 0.0, COSTURA, fade_out=0.03), Seg(DD2, COSTURA, C2 - COSTURA, fade_in=0.03), Seg(V + "cta10.wav", 0.0, CTA_D)]
CORTES = [b for _, b, _ in BEATS[:-1]]

PERG = [(4.55, "cash", "Quanto ele financia"), (6.05, "home", "Qual imóvel ele compra"), (8.35, "wallet", "Quanto vai de entrada")]
def gancho(img, t): hook_mapa(img, t, 0.2, 1.55, PERG, H1 + 0.02)

# tempos = os do body do DD 4 − 2,767 s (mesmo body, conferido por correlação)
TEMAS = [(16.23, "pig-money", "FGTS"), (17.98, "home", "MCMV"), (19.23, "users-group", "Consórcio"),
         (20.23, "file-text", "Documentos"), (21.48, "calendar-time", "Prazos"), (22.23, "receipt", "Custos")]
JEITO = [(28.28, "photo", "Ilustrado"), (29.28, "layout-list", "Organizado"), (30.38, "bulb", "Fácil")]
FORMAS = [(36.88, "building-bank", "Financiar"), (37.18, "cash", "À vista"), (37.48, "pig-money", "FGTS"),
          (37.78, "users-group", "Consórcio"), (38.08, "arrows-exchange", "Permuta")]
def body(img, t):
    if not (H1 + 0.3 <= t < C2): return
    pilha(img, t, 12.48, 14.53)
    fluxo(img, t, TEMAS[0][0] - 0.15, 23.23, TEMAS, "Tudo isso no Mapa")
    blocos(img, t, JEITO, 31.98)
    alerta_saida(img, t, 33.38, 33.93, 34.98)
    rota(img, t, FORMAS[0][0] - 0.15, 39.78, FORMAS, "Todas as formas de aquisição")
def fim(img, t): cta(img, t, C2, tap=0.67)
def cam(t):
    if t >= H1: return 1.0
    for a, b, _ in BEATS:
        if a <= t < b: return 1.0 + 0.04 * ((t - a) / (b - a))
    return 1.0
SFX = [(0.22, "pop", -16), (1.55, "pop", -16)] + [(tk, "pop", -15) for tk, _, _ in PERG] + [(c - 0.1, "whoosh", -17) for c in CORTES] + \
      [(H1 - 0.16, "whoosh", -13), (12.48, "pop", -20)] + [(tk, "pop", -23) for tk, _, _ in TEMAS + JEITO + FORMAS] + \
      [(33.38, "pop", -21), (33.93, "pop", -19), (C2 - 0.16, "whoosh", -15), (C2 + 0.10, "pop", -19), (C2 + 0.67, "pop", -16)]
OVS = [gancho, body, fim]

def nivelar():
    """fala do gancho e do CTA no mesmo nível (percentil 80) da fala do body."""
    def p80(f, a, b):
        x, sr = sf.read(f); x = x.mean(1) if x.ndim > 1 else x; w = int(sr * .4); s = x[int(a * sr):int(b * sr)]
        return np.percentile([20 * np.log10(np.sqrt(np.mean(s[i:i + w] ** 2)) + 1e-9) for i in range(0, len(s) - w, w // 2)], 80)
    for _ in range(3):
        montar_audio(AUD, [], "/tmp/nv.wav"); rb = p80("/tmp/nv.wav", COSTURA + 0.5, C2 - 0.3)
        AUD[0].ganho += rb - p80("/tmp/nv.wav", 0.2, COSTURA - 0.2); AUD[2].ganho += rb - p80("/tmp/nv.wav", C2 + 0.1, C2 + CTA_D - 0.1)
    print("ganhos", round(AUD[0].ganho, 1), round(AUD[2].ganho, 1))
if __name__ == "__main__":
    nivelar()
    d = render(SEGS, OVS, [*CORTES, H1, C2], SFX, OUT, audio_segs=AUD, cam=cam)
    print("ok", OUT, round(d, 2))
