#!/usr/bin/env python3
"""EST9 · Mistura de motion com vídeo real — piloto A, v2 (24/11, correções da revisão 4d).
Takes dela (HOOK1 pt1/pt2, brutos, rosto e voz sincronizados) + grafismo animado: perguntas de cliente pipocando em volta dela
("quando a negociação sai do básico"), a rota do "sim" às chaves desenhada em motion ("dominar muito mais do que apenas a venda"),
páginas do Mapa em leque ("diferentes cenários") e o impresso folheado de verdade → CTA 4de4 + R$27,90. Voz só dela.
Abre com o take já sincronizado: 0,33 s levemente desfocado sob a pergunta grande "Posso usar o FGTS?" (ela ainda girando pra câmera)
e, a partir daí, ela nítida e de frente, com a pergunta virando balão abaixo do queixo.
Ângulo (ganho): qualificação e destaque — ser o corretor que sabe responder quando a negociação sai do básico.
Uso: python3 est9.py <saida.mp4>
"""
import sys
from motor_novo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else "EST9-A.mp4"
pc = Peca(OUT, leg_y=1290, leg_y_cta=330, preco_y=430)
P1, P2 = C5 + "hook1p1.mov", C5 + "hook1p2.mov"
G1 = [("SE VOCÊ QUER", 0.0), ("SER O CORRETOR", 0.8), ("QUE SABE RESPONDER", 1.6), ("QUANDO A NEGOCIAÇÃO", 2.8), ("SAI DO BÁSICO,", 3.6),
      ("VOCÊ PRECISA DOMINAR", 4.8), ("MUITO MAIS DO", 6.0), ("QUE APENAS A", 6.4), ("VENDA.", 7.2)]
G2 = [("E DÁ UMA", 7.6), ("OLHADA NESSE MATERIAL,", 8.4), ("PORQUE ELE FOI", 9.2), ("CRIADO JUSTAMENTE", 10.0), ("PARA TE PREPARAR", 10.8),
      ("PARA OS", 12.0), ("DIFERENTES", 12.4), ("CENÁRIOS QUE PODEM", 13.2), ("ACONTECER DURANTE O", 14.0), ("FECHAMENTO.", 14.8)]
pos1 = pc.fala(P1, 0.55, 8.06, G1, off=0.49, fim_ref=7.6)
pos2 = pc.fala(P2, 0.50, 8.27, G2, off=-6.855, fim_ref=15.4)
legenda_desde_zero(pc)
pc.fades = {0: 0.22}   # o bruto HOOK1 pt1 termina colado no fim do "venda": fade um pouco mais longo
INTRO = 0.33
pc.fadein = {1: 0.12}
pc.eq = {P1: "highpass=f=190,highpass=f=190", P2: "equalizer=f=2200:t=q:w=0.8:g=-7,highshelf=f=4000:g=-4,lowshelf=f=250:g=3"}   # o take da mesa é mais brilhante: casa com o pt1 e o CTA
pc.silencio(0.15)
pc.fala(CTA4, 0.0, 6.05, G_CTA4N, fim_ref=6.0, cta=True)

qs, qn, sb, vp = (t_de(pc, x) for x in ("QUE SABE", "QUANDO A", "SAI DO", "VOCÊ PRECISA"))
pq, pt, ac = t_de(pc, "PORQUE"), t_de(pc, "PARA TE"), t_de(pc, "ACONTECER")
dif = t_de(pc, "DIFERENTES")

# ---------- motion A: a rota do sim às chaves ----------
ROTA = [("Mostrar o imóvel", "ok"), ("O “sim” do cliente", "sim"), ("Crédito e avaliação", ""), ("FGTS e renda", ""),
        ("Documentação", ""), ("Cartório e registro", ""), ("Entrega das chaves", "")]
@functools.lru_cache(None)
def fundo_navy():
    im = Image.new("RGB", (W, H_), NAVY); d = ImageDraw.Draw(im)
    for r in range(900, 0, -30):   # brilho radial suave
        c = tuple(int(NAVY[i] + (40 - 40 * r / 900) * (1 if i else 0.6)) for i in range(3))
        d.ellipse((540 - r, 760 - r, 540 + r, 760 + r), fill=c)
    return im.filter(ImageFilter.GaussianBlur(40))
H_ = 1920
def rota(tl, t):
    im = fundo_navy().copy(); d = ImageDraw.Draw(im, "RGBA")
    x0, y0, dy = 215, 280, 150
    tempos = [0.0, 0.30] + [0.75 + 0.33 * i for i in range(5)]
    # linha que desce acompanhando os nós
    yfim = y0 + dy * sum(1 for tt in tempos if tl >= tt) - dy
    prog = min(1, max(0, (tl - 0.3) / 2.4)); ylin = y0 + (dy * 6) * ease(prog)
    d.line((x0, y0, x0, max(y0, min(ylin, y0 + dy * 6))), fill=TEAL + (255,), width=8)
    for i, ((txt, tipo), tt) in enumerate(zip(ROTA, tempos)):
        if tl < tt: continue
        k = mola((tl - tt) / 0.4); y = y0 + i * dy
        r = int((30 if tipo == "sim" else 24) * k)
        if tipo == "ok":
            d.ellipse((x0 - r, y - r, x0 + r, y + r), fill=(120, 140, 170, 255))
            d.line((x0 - 10, y + 1, x0 - 3, y + 9, x0 + 11, y - 8), fill=(255, 255, 255, 255), width=6)
            d.text((x0 + 60, y), txt, font=fonte(700, 52), fill=(150, 165, 190, int(255 * min(1, k))), anchor="lm")
        elif tipo == "sim":
            d.ellipse((x0 - r, y - r, x0 + r, y + r), fill=TEAL + (255,))
            w = d.textlength(txt, font=fonte(800, 58)) + 64
            d.rounded_rectangle((x0 + 50, y - 46, x0 + 50 + w, y + 46), radius=46, fill=TEAL + (int(255 * min(1, k)),))
            d.text((x0 + 82, y), txt, font=fonte(800, 58), fill=(255, 255, 255, int(255 * min(1, k))), anchor="lm")
        else:
            d.ellipse((x0 - r, y - r, x0 + r, y + r), fill=(255, 255, 255, 255))
            d.ellipse((x0 - r + 8, y - r + 8, x0 + r - 8, y + r - 8), fill=TERRA + (255,)) if r > 10 else None
            dx = int((1 - min(1, k)) * 40)
            d.text((x0 + 60 + dx, y), txt, font=fonte(800, 62), fill=(255, 255, 255, int(255 * min(1, (tl - tt) / 0.15))), anchor="lm")
    return im

# ---------- motion B: páginas em leque (diferentes cenários) ----------
CENAS = [111, 113, 46, 72, 65]
def leque(tl, t):
    im = fundo_navy().copy(); dur = ac - pt
    t_abre = dif - pt                       # no "diferentes" o leque abre
    for i, pg in enumerate(CENAS):
        te = -0.3 + 0.42 * i            # a 1ª carta já está na tela no 1º quadro (sem quadro vazio)
        if tl < te: continue
        k = ease((tl - te) / 0.45); ab = ease((tl - t_abre) / 0.6)
        ang_f = (i - 2) * 9 * ab; dx_f = (i - 2) * 115 * ab; dy_f = abs(i - 2) * 30 * ab
        cx = 540 + dx_f + (1 - k) * 700; cy = 730 + dy_f + (1 - k) * 120
        z = 1 + 0.03 * tl
        cola_cartao(im, pg, cx, cy, int(540 * z), ang=-ang_f + (1 - k) * -14, raio=14)
    return im

# ---------- bolhas de pergunta do cliente em volta dela ----------
BOLHAS = [(INTRO - 0.5, "Posso usar o FGTS?", "e", 1040), (qn, "A avaliação veio menor…", "d", 1130), (sb, "Quem paga o ITBI?", "e", 1220)]   # ≥ 120 px abaixo do queixo
def pergunta(img, t):
    if t >= INTRO: return
    pilula_ajusta(img, 760, "Posso usar o FGTS?", (255, 255, 255), cor=NAVY, fz=74)

def bolhas(img, t):
    if not (INTRO <= t < vp): return
    d = ImageDraw.Draw(img, "RGBA")
    for t0, txt, lado, y in BOLHAS:
        if t < t0: continue
        k = mola((t - t0) / 0.4); fl = fonte(700, 42); w = d.textlength(txt, font=fl) + 66; h = 84
        x = 150 if lado == "e" else 930 - w
        s = 0.5 + 0.5 * k; cx, cy = x + w / 2, y + h / 2
        bx0, by0, bx1, by1 = cx - w / 2 * s, cy - h / 2 * s, cx + w / 2 * s, cy + h / 2 * s
        sombra(img, (bx0, by0, bx1, by1), raio=42, blur=14, alpha=90, dy=8); d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle((bx0, by0, bx1, by1), radius=int(42 * s), fill=(255, 255, 255, 250))
        tx = bx0 + 34 * s if lado == "e" else bx1 - 34 * s
        cauda = [(bx0 + 40, by1 - 2), (bx0 + 28, by1 + 22), (bx0 + 70, by1 - 2)] if lado == "e" else [(bx1 - 40, by1 - 2), (bx1 - 28, by1 + 22), (bx1 - 70, by1 - 2)]
        d.polygon(cauda, fill=(255, 255, 255, 250))
        fs = fonte(700, max(8, int(42 * s)))         # o texto cresce junto com o balão (nunca balão vazio)
        d.text((cx, cy), txt, font=fs, fill=NAVY, anchor="mm")

# ---------- vídeo ----------
PD = C5 + "pagdet.mp4"
INTRO = 0.33                                                   # 0–0,33 s: o take já corre sincronizado (ela ainda girando pra câmera),
pc.clipe(P1, 0.55, INTRO, 1.0, 1.0, lambda im: Image.blend(im.filter(ImageFilter.GaussianBlur(7)), Image.new("RGB", im.size, (10, 14, 24)), 0.25))
pc.clipe(P1, 0.55 + INTRO, vp - INTRO)                         # levemente desfocado sob a pergunta grande; em 0,33 s ela está de frente, nítida
pc.motion(rota, pos2 - vp)                                     # "você precisa dominar muito mais do que apenas a venda."
ENT = 0.85                                                     # o take dela começa se ajeitando na cadeira: cobre com o impresso
pc.motion(folheia([(pos2, 70)], fundo_mesa(PD, 2.5), larg=700, cy=650), ENT)          # "E dá uma…" → DIRETO COM A INCORPORADORA (página inteira)
pc.clipe(P2, 0.50 + ENT, pq - pos2 - ENT)                      # "…olhada nesse material," (ela, sincronizada)
pc.motion(folheia([(pq, 70), (pq + 0.05, 69)], fundo_mesa(PD, 2.5), larg=700, cy=650), pt - pq)   # "porque ele foi criado justamente" → vira pra PARCELAR ENTRADA NÃO QUITA O IMÓVEL
pc.motion(leque, ac - pt)                                      # "para te preparar para os diferentes cenários que podem"
pc.clipe(P2, 0.50 + (ac - pos2), pc.cta_ini - ac)              # "acontecer durante o fechamento." (ela com o material)
pc.clipe(CTA4, 0.0, 6.05)
pc.leg_y_trechos = [(0, vp, 1420), (ac, pc.cta_ini, 330)]   # com ela segurando a capa: legenda acima da cabeça (queixo ~850, capa a partir de ~910)                     # legenda acima da capa que ela segura
if __name__ == "__main__":
    render(pc, [pergunta, bolhas])
