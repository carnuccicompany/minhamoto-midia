#!/usr/bin/env python3
"""LOTE1 · CM03 · "Revisão da CG: de R$ 166 a R$ 1.418."
Tipo: comparação de custo · Público: iniciante (primeira moto) · Tom: especialista direto · Ângulo: controle (não ser pego de surpresa)
Estética: escuro premium (gráfico) · Capa: custo · Final: CTA do app (sem preço).
Números: Webmotors/WM1, 03/03/2025 — revisões da CG 160 Titan 2024 numa concessionária Honda de SP (peças + mão de obra).
Link em pecas/LOTE1/CM03/fontes.md. Arredondado ao real nos cards; nada calculado além de 24.000 km ÷ 30 km/dia.
Tela: só o card 5 (03-manutencao no celular, sem card solto). Revisão 24/11: capa com número herói sem entregar o km,
card 3 = orçamento de papel (nada que imite o app), mão de obra = 1.418,04 − 1.049,20 (aritmética), final com mini-gráfico.
Uso: python3 agencia/estudio/motores/lote1_cm03.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lote1_base import *

NOME, N, T = 'CM03', 6, 'escuro'
FONTE = 'Fonte: Webmotors (mar/2025), concessionária Honda em SP, CG 160 Titan 2024.'
REV = [('1 mil', 166), ('6 mil', 166), ('12 mil', 840), ('18 mil', 664), ('24 mil', 1418), ('30 mil', 320), ('36 mil', 1163)]
BR = lambda v: f"R$ {v:,}".replace(',', '.')

def nota_fonte(L, top, w, tt):
    linhas = [FONTE] if not tt else ['Fonte: Webmotors (mar/2025), concessionária', 'Honda em SP, CG 160 Titan 2024.']
    return apoio(linhas, L, top, 22 if not tt else 21, w=w, cor='rgba(255,255,255,.45)')

def barras(L, base, w, hmax, destaque=4, so=None, tam_lbl=24):
    """Gráfico de barras das 7 revisões (base = y da linha de base)."""
    n = len(REV); slot = w / n; bw = round(slot * .62); c = ''
    for i, (km, v) in enumerate(REV):
        if so is not None and i not in so: continue
        h = round(hmax * v / 1418); x = round(L + i * slot + (slot - bw) / 2)
        on = i == destaque
        cor = f"linear-gradient(180deg,{AZUL_CLARO},{AZUL})" if on else "linear-gradient(180deg,rgba(255,255,255,.26),rgba(255,255,255,.10))"
        glow = "box-shadow:0 0 50px rgba(82,169,254,.55);" if on else ''
        c += f"<div style='position:absolute;left:{x}px;top:{base - h}px;width:{bw}px;height:{h}px;border-radius:14px 14px 4px 4px;background:{cor};{glow}'></div>"
        c += (f"<div style='position:absolute;left:{round(L + i*slot)}px;width:{round(slot)}px;top:{base - h - tam_lbl - 18}px;text-align:center;white-space:nowrap;"
              f"font-family:{'j700' if on else 'j600'};font-size:{tam_lbl + (4 if on else 0)}px;color:{'#FFFFFF' if on else 'rgba(255,255,255,.7)'}'>{BR(v)}</div>")
        c += (f"<div style='position:absolute;left:{round(L + i*slot)}px;width:{round(slot)}px;top:{base + 16}px;text-align:center;white-space:nowrap;"
              f"font-family:j600;font-size:{tam_lbl}px;color:{LIMAO if on else 'rgba(255,255,255,.55)'}'>{km}</div>")
    c += f"<div style='position:absolute;left:{L}px;top:{base}px;width:{w}px;height:2px;background:rgba(255,255,255,.18)'></div>"
    return c

def capa(tt):
    """Capa: número gigante centralizado como herói. Sem rótulo de km (a resposta só aparece no card 2)."""
    L, w = (140, 800) if tt else (90, 900)
    c = fundo(T, (50, 52))
    y0 = 420 if tt else 120
    c += kicker('Primeira moto 0 km?', 0, y0, T, w=1080, alinha='center')
    c += titulo(['Revisão da CG:'], L, y0 + 80, 84 if not tt else 80, w=w, alinha='center')
    c += titulo(['de R$ 166 a'], L, y0 + 180, 84 if not tt else 80, w=w, alinha='center', azul_de=0)
    big = 250 if not tt else 222
    yb = y0 + 290
    c += (f"<div class=titB style='left:0;right:0;width:1080px;top:{yb}px;font-size:{big}px;text-align:center;letter-spacing:-.045em;line-height:1;"
          f"color:#FFFFFF;text-shadow:0 0 60px rgba(82,169,254,.55),0 20px 60px rgba(0,0,0,.5)'>R$ 1.418</div>")
    c += f"<div style='position:absolute;left:{540 - 60}px;top:{yb + big + 40}px;width:120px;height:8px;border-radius:8px;background:{LIMAO};box-shadow:0 0 22px rgba(198,255,0,.5)'></div>"
    c += apoio(['Você sabe quando vem a cara?'], L, yb + big + 90, 46 if not tt else 44, w=w, alinha='center', cor='#F4F7FC', peso='j600')
    c += desliza(0, 1225 if not tt else 1400, tt, alinha='center').replace("left:0px;right:auto", "left:0;right:0")
    return c

def grafico(tt):
    if tt:
        L, w, Ty, tam = 140, 800, 220, 88
        base, hmax, lbl = 1250, 480, 22
    else:
        L, w, Ty, tam = 90, 900, 110, 96
        base, hmax, lbl = 1110, 440, 24
    c = fundo(T, (60, 70))
    c += titulo(['A conta muda', 'a cada revisão.'], L, Ty, tam, w=w, azul_de=1)
    c += apoio(['CG 160 Titan, com peças e mão de obra.'], L, Ty + alt_titulo(2, tam) + 26, 36 if not tt else 34, w=w)
    c += barras(L, base, w, hmax, tam_lbl=lbl)
    c += nota_fonte(L, base + 80 if not tt else base + 90, w, tt)
    return c + pag(2, N, tt)

def nota(tt):
    """Card 3: orçamento de papel (claro, sem cara de app) com peças, mão de obra (aritmética) e total."""
    L, w = (140, 800) if tt else (90, 900)
    c = fundo(T, (30, 75))
    ty = 300 if tt else 130
    tam = 100 if not tt else 92
    c += titulo(['24 mil km:', 'a mais pesada.'], L, ty, tam, w=w, azul_de=1)
    ny = ty + alt_titulo(2, tam) + (150 if tt else 110)
    pw = w - 60
    linha = lambda a, b, peso='j500', tm=44, cor='#2A3445': (
        f"<div style='display:flex;align-items:baseline;white-space:nowrap;font-family:{peso};font-size:{tm}px;color:{cor};padding:16px 0'>"
        f"<span>{a}</span><span style='flex:1;border-bottom:3px dotted rgba(10,26,51,.25);margin:0 18px;transform:translateY(-8px)'></span><span>{b}</span></div>")
    corpo = (f"<div style='font-family:j600;font-size:26px;color:rgba(10,26,51,.5);letter-spacing:.02em'>Revisão · CG 160 Titan 2024</div>"
             f"<div style='height:3px;border-top:3px dashed rgba(10,26,51,.18);margin:22px 0 10px'></div>"
             + linha('Peças', 'R$ 1.049,20') + linha('Mão de obra', 'R$ 368,84') +
             f"<div style='height:3px;border-top:3px dashed rgba(10,26,51,.18);margin:12px 0 4px'></div>"
             + linha('Total', 'R$ 1.418,04', 'j800', 60, NAVY_TXT))
    c += (f"<div style='position:absolute;left:{L + 30}px;top:{ny}px;width:{pw}px;box-sizing:border-box;padding:56px 56px 40px;border-radius:10px;"
          f"background:linear-gradient(180deg,#FFFFFF,#F1F4F9);box-shadow:0 50px 90px rgba(0,0,0,.55);transform:rotate(-1.5deg)'>{corpo}</div>")
    # carimbo
    c += (f"<div style='position:absolute;left:{L + pw - 190}px;top:{ny - 46}px;padding:14px 26px;border:5px solid {AZUL};border-radius:14px;"
          f"font-family:j800;font-size:34px;color:{AZUL};transform:rotate(8deg);background:rgba(255,255,255,.92)'>24.000 km</div>")
    c += nota_fonte(L, 1200 if not tt else 1400, w, tt)
    return c + pag(3, N, tt)

def tempo(tt):
    if tt:
        L, w, Ty, tam = 140, 800, 300, 72
        ly = 1060
    else:
        L, w, Ty, tam = 90, 900, 200, 80
        ly = 860
    c = fundo(T, (70, 60))
    c += titulo(['Com 30 km por dia,', 'ela chega em', 'pouco mais de 2 anos.'], L, Ty, tam, w=w, azul_de=2)
    c += apoio(['Ou em 30 meses, o que vier primeiro.'], L, Ty + alt_titulo(3, tam) + 28, 38 if not tt else 34, w=w)
    # linha do tempo 0 → 24 mil km, com as revisões no caminho
    c += f"<div style='position:absolute;left:{L}px;top:{ly}px;width:{w}px;height:12px;border-radius:12px;background:rgba(255,255,255,.12)'></div>"
    c += f"<div style='position:absolute;left:{L}px;top:{ly}px;width:{w}px;height:12px;border-radius:12px;background:linear-gradient(90deg,rgba(82,169,254,.25),{AZUL_CLARO})'></div>"
    for km, lbl in [(0, '0 km'), (6, '6 mil'), (12, '12 mil'), (18, '18 mil'), (24, '24 mil')]:
        x = L + round(w * km / 24); on = km == 24
        r = 26 if on else 12
        st = (f"background:{AZUL_CLARO};box-shadow:0 0 0 8px rgba(82,169,254,.25),0 0 50px rgba(82,169,254,.8)" if on
              else f"background:{AZUL_CLARO};border:4px solid #0b1730")
        c += f"<div style='position:absolute;left:{x - r}px;top:{ly + 6 - r}px;width:{2*r}px;height:{2*r}px;border-radius:50%;box-sizing:border-box;{st}'></div>"
        if km in (1,):
            continue   # 1 mil fica colado no 0: só o ponto
        al = 'right' if on else ('left' if km == 0 else 'center')
        lx = x - 200 if al == 'right' else (x if al == 'left' else x - 100)
        c += (f"<div style='position:absolute;left:{lx}px;width:200px;top:{ly + 48}px;text-align:{al};white-space:nowrap;font-family:{'j700' if on else 'j600'};"
              f"font-size:{30 if on else 24}px;color:{'#fff' if on else 'rgba(255,255,255,.55)'}'>{lbl}</div>")
    return c + pag(4, N, tt)

def tela(tt):
    """Card 5: só o celular (Manutenção: 29.800 km, faltam 200 km pro marco). Texto casa com a tela."""
    L, w = (140, 800) if tt else (90, 900)
    c = fundo(T, (50, 60))
    ty = 260 if tt else 110
    tam = 76 if not tt else 72
    c += titulo(['Faltam 200 km pro', 'próximo marco.', 'O app te avisa antes.'], L, ty, tam, w=w, azul_de=2)
    ya = ty + alt_titulo(3, tam) + 24
    c += apoio(['E mostra o que entra em cada revisão.'], L, ya, 38 if not tt else 38, w=w)
    c += fone('ios-1.0/03-manutencao', 720 if tt else 600, 540, ya + (110 if tt else 90))
    return c + pag(5, N, tt)

def final(tt):
    """CTA alinhado à esquerda com mini-gráfico das 7 revisões (24 mil acesa)."""
    L, w = (140, 800) if tt else (90, 900)
    c = fundo(T, (80, 30))
    y0 = 260 if tt else 110
    c += f"<img src='file://{ICON}' style='position:absolute;left:{L}px;top:{y0}px;width:120px;height:120px;filter:drop-shadow(0 18px 26px rgba(0,0,0,.5))'>"
    tam = 84 if not tt else 76
    ty = y0 + 170
    c += titulo(['A revisão cara vem.', 'Melhor saber antes.'], L, ty, tam, w=w, azul_de=1)
    ya = ty + alt_titulo(2, tam) + 30
    c += apoio(['Baixe agora e acompanhe seu km.'], L, ya, 42 if not tt else 40, w=w, cor='#F4F7FC')
    base = ya + (520 if tt else 400)
    c += barras(L, base, w, 260 if tt else 220, tam_lbl=22)
    c += f"<img src='file://{SELOS}' style='position:absolute;left:{L}px;top:{1380 if tt else 1190}px;width:540px'>"
    return c

def lista(tt):
    return [
        (T, capa(tt)),
        (T, grafico(tt)),
        (T, nota(tt)),
        (T, tempo(tt)),
        (T, tela(tt)),
        (T, final(tt)),
    ]

if __name__ == '__main__':
    ok = render_lista(NOME, lista(False), lista(True))
    folha(NOME, 'CM03 · custo das revisões (escuro)')
    sys.exit(0 if ok else 1)
