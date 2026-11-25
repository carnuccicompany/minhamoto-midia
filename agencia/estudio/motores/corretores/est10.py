#!/usr/bin/env python3
"""EST10 · Só motion (sem rosto), com a voz dela — piloto A, v2 REFEITO (24/11, correções da revisão 4d).
Gancho no 1º quadro: "CORRETOR, VOCÊ DOMINA TODAS AS FORMAS DE AQUISIÇÃO?" enquanto ela diz "Para ajudar você, corretor, a compreender
as principais formas de aquisição, pagamento e fechamento de imóveis…"; as formas pipocam como chips; entra a capa do Mapa; depois cada
forma que ela lista ("O material explica financiamento imobiliário, Minha Casa Minha Vida, FGTS…") entra como a página real do PDF no
tempo da palavra; "e muito mais" abre a grade das 125 páginas; CTA 4de4 com a capa e o selo R$27,90.
Voz só dela: corpo do Dia 2 (gravação limpa, um trecho contínuo, EQ pra casar com o CTA de câmera) + áudio do CTA 4de4 (sem o rosto).
Ângulo (ganho): repertório completo — todas as formas de aquisição num lugar só.
Uso: python3 est10.py <saida.mp4>
"""
import sys
from motor_novo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else "EST10-A.mp4"
pc = Peca(OUT, leg_y=1330, leg_y_cta=1330, preco_y=1150)
AL = alinhar_grav(L2_DIA2 + L3_DIA2, 6.70, 28.62)
# conferido no gráfico de energia (vales entre palavras): "minha casa minha vida, FGTS" começa no vale de 17,85 s, "casa" no vale
# fundo de 18,16, e "FGTS" depois da pausa da vírgula (19,25); "vista" logo depois do "à"
AJUSTE = {"MINHA CASA MINHA VIDA,": [17.85, 18.16, 18.47, 18.72], "FGTS,": [19.27], "COMPRA À VISTA,": [21.53, 21.93, 22.03]}
AL = [(txt, AJUSTE.get(txt, ts)) for txt, ts in AL]
pc.eq = {GRAV: eq_grav("est10")}                     # EQ por faixa (±3 dB do CTA4)
pc.fala(GRAV, 6.70, 28.62, AL, fim_ref=28.6, prender=False)
legenda_desde_zero(pc)
B = pc.t
pc.silencio(0.15)
pc.fala(CTA4, 0.0, 6.05, G_CTA4N, fim_ref=6.0, cta=True)

def tp(txt, palavra=0):
    for a, b, g, ts in pc.leg:
        if g.startswith(txt): return ts[palavra] if (ts and palavra) else a
    raise KeyError(txt)
SEQ = [(tp("O MATERIAL"), 1), (tp("FINANCIAMENTO"), 27), (tp("MINHA CASA"), 37), (tp("FGTS"), 53), (tp("COMPOSIÇÃO"), 57), (tp("COMPRA À"), 61),
       (tp("CONSÓRCIO"), 66), (tp("IMÓVEL NA"), 67), (tp("PERMUTA"), 72), (tp("DOCUMENTAÇÃO"), 75), (tp("MATRÍCULA"), 80), (tp("CERTIDÕES"), 90)]
mais = tp("E MUITO MAIS")
formas, pagto, dentro, cor_t = tp("AS PRINCIPAIS", 2), tp("PAGAMENTO"), tp("DENTRO"), tp("CORRETOR")

@functools.lru_cache(None)
def fundo():
    im = Image.new("RGB", (W, 1920), NAVY); d = ImageDraw.Draw(im)
    for r in range(1000, 0, -25):
        c = (int(NAVY[0] + 22 * (1 - r / 1000)), int(NAVY[1] + 34 * (1 - r / 1000)), int(NAVY[2] + 44 * (1 - r / 1000)))
        d.ellipse((540 - r, 760 - r, 540 + r, 760 + r), fill=c)
    return im.filter(ImageFilter.GaussianBlur(50))

@functools.lru_cache(None)
def mini(n, w): return pagina(n, w)

@functools.lru_cache(None)
def textura():
    w = 150; h = int(w * 1.414); cols = 8; rows = 12
    tx = Image.new("RGB", (cols * (w + 14), rows * (h + 14)), NAVY)
    for i in range(cols * rows): tx.paste(mini(1 + (i * 7) % 125, w), ((i % cols) * (w + 14), (i // cols) * (h + 14)))
    return tx
def fundo_t(t):
    im = fundo().copy(); tx = textura(); oy = int((t * 22) % (tx.height - 1920 - 10))
    im.paste(Image.blend(im, tx.crop((60, oy, 60 + W, oy + 1920)), 0.07)); return im

# --------- trecho 1: gancho (pergunta + formas) → capa ---------
CHIPS = ["Financiamento", "FGTS", "Minha Casa Minha Vida", "Consórcio", "Permuta", "Imóvel na planta"]
LEQUE = [27, 53, 66, 72]
def abertura(tl, t):
    im = fundo_t(t); d = ImageDraw.Draw(im, "RGBA")
    T_CAPA = pagto - 0.25
    sai = ease((t - (T_CAPA - 0.25)) / 0.25)             # a pergunta e os chips somem (fade) ANTES da capa entrar
    dy = 0; af = 1 - sai
    if sai < 1:
        base = im; im = im.copy(); d = ImageDraw.Draw(im, "RGBA")   # pergunta + chips numa camada: somem juntos no fade
        d.text((540, 300 + dy), "CORRETOR,", font=fonte(800, 118), fill=(255, 255, 255, 255), anchor="mm")
        for k, (ln, cor) in enumerate([("VOCÊ DOMINA", (255, 255, 255)), ("TODAS AS FORMAS", AMARELO), ("DE AQUISIÇÃO?", (255, 255, 255))]):
            fz = 84
            while d.textlength(ln, font=fonte(800, fz)) > 800: fz -= 2
            d.text((540, 450 + k * 100 + dy), ln, font=fonte(800, fz), fill=cor + (255,), anchor="mm")
        # as formas pipocam quando ela fala "as principais formas de aquisição"
        lin = [CHIPS[:2], CHIPS[2:3], CHIPS[3:5], CHIPS[5:]]     # 4 filas: cada fila ≤ 800 px (zona segura x 140–940)
        for r, row in enumerate(lin):
            ws = [d.textlength(n, font=fonte(800, 40)) + 68 for n in row]; gap = 16; x = (W - (sum(ws) + gap * (len(row) - 1))) / 2
            assert x >= 140, (row, x)
            for n, w in zip(row, ws):
                j = CHIPS.index(n); t0 = cor_t + 0.25 + 0.3 * j      # pipocam desde "corretor," até "formas de aquisição"
                if t >= t0:
                    k = mola((t - t0) / 0.35)
                    pilula(img=im, x=x, y=780 + r * 92 + int((1 - k) * 24) + dy, txt=n, fundo=TEAL2, fz=40, alpha=min(1, (t - t0) / 0.12))
                x += w + gap
        im = Image.blend(base, im, af)
    if t >= T_CAPA - 0.18:         # a capa começa a entrar enquanto a pergunta some (cruzado, sem quadro vazio)
        capa_leque(im, t, T_CAPA - 0.18)
    return im

LEQUE_PGS = [62, 4, 27, 53, 105, 118, 91, 101, 66, 72, 39, 80, 12, 57]
def capa_leque(im, t, t0, alpha_leque=1.0, dx=0, ang=0.0):
    """A capa entra já no lugar (escala + fade, sem cruzar a legenda) e fica com zoom lento; atrás dela um leque de 4 páginas
    que troca uma página a cada 0,6 s (a tela nunca fica parada)."""
    T0 = t0 + 0.35; ab = ease((t - T0) / 0.5)
    if ab > 0 and alpha_leque > 0.02:
        n = int((t - T0) / 0.6) if t >= T0 else -1
        for i in range(4):
            c = (n - i) // 4 + 1 if n >= i else 0
            pg = LEQUE_PGS[(i + 4 * c) % len(LEQUE_PGS)]
            tsw = T0 + 0.6 * (i + 4 * (c - 1)) if c > 0 else None
            sub = (1 - ease((t - tsw) / 0.3)) * 120 if tsw is not None else 0
            cola_cartao(im, pg, 540 + dx + (i - 1.5) * 175 * ab, 790 + abs(i - 1.5) * 28 * ab + sub, 520,
                        ang=-(i - 1.5) * 9 * ab, raio=12, alpha=alpha_leque)
    k = ease((t - t0) / 0.35); z = (0.9 + 0.1 * k) * (1 + 0.012 * max(0.0, t - t0))
    cola_cartao(im, 1, 540 + dx, 790, int(640 * z), raio=16, alpha=k, ang=ang)

# --------- trecho 2: cada forma de aquisição = a página dela ---------
def lista(tl, t):
    im = fundo_t(t)
    if t >= mais - 0.02:   # "e muito mais": grade das 125 abrindo
        k = ease((t - mais) / 0.8); cols = 9; w = 104
        cx0, cy0 = 540, 760; zz = 2.4 - 1.4 * k
        for n in range(1, 126):
            col, lin = (n - 1) % cols, (n - 1) // cols
            x = cx0 + (col - (cols - 1) / 2) * (w + 10) * zz; y = cy0 + (lin - 6.5) * (w * 1.414 + 10) * zz
            if -200 < x < 1280 and -200 < y < 2000: im.paste(mini(n, max(8, int(w * zz))), (int(x - w * zz / 2), int(y - w * 1.414 * zz / 2)))
        return im
    atual = max([i for i, (ts, _) in enumerate(SEQ) if t >= ts - 1e-6] or [0])
    ts, pg = SEQ[atual]
    k = ease((t - ts) / 0.32)
    if atual == 0:
        capa_leque(im, t, pagto - 0.43); return im
    if atual == 1 and k < 1:        # a capa (com o leque) sai pela esquerda
        T0c = pagto - 0.43
        capa_leque(im, t, T0c, 1.0, dx=-1100 * k, ang=6 * k)    # capa e leque saem juntos pela esquerda (sem transparência)
    elif atual > 1 and k < 1:       # a anterior sai pela esquerda
        pts, ppg = SEQ[atual - 1]; cola_cartao(im, ppg, 540 - 900 * k, 790, 640, ang=6 * k, raio=16)
    if atual > 0:
        d = ImageDraw.Draw(im, "RGBA")
        d.text((540, 215), "O QUE O MAPA EXPLICA", font=fonte(800, 50), fill=TEAL + (255,), anchor="mm")
        for j in range(11):
            x = 540 + (j - 5) * 46; on = j < atual; r = 11 if on else 8
            d.ellipse((x - r, 290 - r, x + r, 290 + r), fill=(TEAL + (255,)) if on else (255, 255, 255, 70))
    cx = 540 + (1 - k) * 900; z = 1 + 0.02 * max(0, t - ts)
    cola_cartao(im, pg, cx, 790, int(640 * z), ang=-6 * (1 - k), raio=16)
    return im

# --------- trecho 3: CTA (capa + selo) ---------
def cta(tl, t):
    im = fundo_t(t); k = mola(tl / 0.5); fl = 6 * math.sin(tl * 2.2)
    cola_cartao(im, 1, 540, 620 + fl + (1 - k) * 80, int(580 * (0.7 + 0.3 * k) * (1 + 0.012 * tl)), raio=16)   # leve zoom: o CTA não fica parado
    return im

pc.motion(abertura, SEQ[0][0])
pc.motion(lista, B + 0.15 - SEQ[0][0])
pc.motion(cta, 6.05)
if __name__ == "__main__":
    render(pc)
