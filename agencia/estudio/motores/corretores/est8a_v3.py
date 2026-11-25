#!/usr/bin/env python3
"""EST8-A v3 (25/11) · Antes × depois — correções do Léo:
gancho = voz da AP DD 7 como veio (já editada, com a trilha dela) sobre cenas em preto e branco (ele aprovou);
cortina DEPOIS entra no "dá uma olhada nesse material aqui" e revela o próprio pronto; body longo = DD 7 de 7,45 a 37,3 s
(material de verdade, legenda e música do pronto); CTA = "Clique em Saiba Mais…" do DD 7. Sem preço, sem voz montada.
"""
import sys
from v3 import *
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/corretores/out/EST8-A v3.mp4"
C5 = TRAB + "cortes5/"
PB = "hue=s=0,eq=contrast=1.08:brightness=-0.02"
DD7 = DD + "AP - DD 7.mp4"
SEGS = [Seg(C5 + "ap1.mp4", 1.0, 3.6, PB, audio=False, zoom=1.06),
        Seg(C5 + "duvida.mp4", 3.0, 3.85, PB, audio=False, zoom=1.04),
        Seg(DD7, 7.45, 29.85),
        Seg(DD7, 62.45, 5.4)]
AUD = [Seg(DD7, 0.0, 37.3), Seg(DD7, 62.45, 5.4)]
WIPE = 7.45; C2 = 37.3
TEMAS = [("FGTS", 3.45), ("Minha Casa Minha Vida", 4.45), ("Consórcio", 5.7), ("Documentação", 6.45)]

def pill(img, cx, y, s, fundo, cor, tam, alpha=1.0, dy=0, pad=30):
    tw = ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength(s, font=fonte(700, tam))
    h = int(tam * 1.75)
    caixa(img, cx - tw / 2 - pad, y + dy, cx + tw / 2 + pad, y + dy + h, h // 2, fundo, alpha)
    texto(img, (cx, y + dy + h / 2), s, 700, tam, cor, alpha, anchor="mm")
    return tw + 2 * pad

def antes(img, t):
    if t >= WIPE: return
    a = ease((t - 0.05) / 0.2); k = mola((t - 0.05) / 0.5)
    pill(img, W / 2, 168, "Antes", CORAL, BRANCO, 52, a, dy=int((1 - k) * 30), pad=40)
    a2 = ease((t - 0.35) / 0.2); k2 = mola((t - 0.35) / 0.5)
    pill(img, W / 2, 290, "“Vou confirmar e te aviso.”", BRANCO, NAVY, 44, a2, dy=int((1 - k2) * 30), pad=36)
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    rows = [TEMAS[:2], TEMAS[2:]]
    for r, lin in enumerate(rows):
        ws = [d.textlength(n + "?", font=fonte(700, 40)) + 60 for n, _ in lin]; gap = 18
        x = W / 2 - (sum(ws) + gap) / 2; y = 1230 + r * 96
        for (n, tf), w in zip(lin, ws):
            if t >= tf:
                k = mola((t - tf) / 0.4); a = ease((t - tf) / 0.12)
                pill(img, x + w / 2, y, n + "?", CORAL, BRANCO, 40, a, dy=int((1 - k) * 34))
            x += w + gap

def cortina(img, t):
    p = (t - (WIPE - 0.26)) / 0.56
    if not (0 <= p <= 1): return
    x = int(W - ease(min(1, p * 2)) * W) if p < 0.5 else int(-ease((p - 0.5) * 2) * W)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rectangle((x, 0, x + W, H), fill=TEAL + (255,))
    d.text((x + W / 2, 860), "Depois", font=fonte(800, 132), fill=BRANCO, anchor="mm")
    d.text((x + W / 2, 990), "Você responde na hora.", font=fonte(700, 50), fill=BRANCO, anchor="mm")
    img.alpha_composite(lay)

SFX = [(0.05, "pop", -15), (0.35, "pop", -18)] + [(tf, "pop", -18) for _, tf in TEMAS] + [(WIPE - 0.3, "whoosh", -12), (C2 - 0.16, "whoosh", -15)]
if __name__ == "__main__":
    d = render(SEGS, [antes, cortina], [C2], SFX, OUT, audio_segs=AUD)
    print("ok", OUT, round(d, 2))
