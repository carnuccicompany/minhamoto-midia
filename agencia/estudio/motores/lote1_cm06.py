#!/usr/bin/env python3
"""LOTE1 · CM06 (24/11, no lugar do CM03 cancelado) · "Ninguém lê o manual da moto."
Tipo: manual traduzido / tutorial do app (função real "Conheça sua moto") · Público: iniciante · Tom: premium, direto
Ângulo: controle (saber os números da própria moto) · Estética: azul de marca chapado + claro (3ª cara do lote)
Capa: tipografia gigante sobre azul · Final: CTA do app centralizado no azul (sem preço).
Números: manual do proprietário Honda CG 160 Titan (página 110 pneus; página 68 corrente), conferidos em 24/11
e iguais aos do app (10-lista-revisao). Links em pecas/LOTE1/CM06/fontes.md.
Tela: só o card 5 (ios-1.0/13-conheca-moto no celular, barra de abas fora do quadro).
Uso: python3 agencia/estudio/motores/lote1_cm06.py
"""
import sys, os, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lote1_base import *

NOME, N = 'CM06', 6
FONTE = 'manuais do proprietário Honda CG 160 Titan S e CG 160 Start'
CLARO_AZ = '#0A1A33'   # 2ª linha em navy sobre o azul (contraste alto)

def fundo_azul(luz=(85, 10)):
    return (f"<style>.az .titB .b{{color:{CLARO_AZ};text-shadow:none}} .az .apoB{{color:rgba(255,255,255,.88)}} .az .pag{{color:rgba(255,255,255,.6)}}</style>"
            f"<div class=fill style='background:linear-gradient(160deg,{AZUL} 0%,{AZUL_ESC} 62%,#0042A8 100%)'></div>"
            f"<div class=fill style='background:radial-gradient(55% 40% at {luz[0]}% {luz[1]}%, rgba(255,255,255,.20), rgba(255,255,255,0) 70%)'></div>")

def numero(txt, left, top, tam, cor, alinha='left', w=900, glow=None):
    sh = f"text-shadow:0 0 50px {glow};" if glow else 'text-shadow:none;'
    return (f"<div class=titB style='left:{left}px;right:auto;width:{w}px;top:{top}px;font-size:{tam}px;text-align:{alinha};"
            f"letter-spacing:-.045em;line-height:1;color:{cor};{sh}'>{H.escape(txt)}</div>")

def livreto(left, top, w, rot=-8):
    """Livreto 'Manual do proprietário' desenhado (sem marca), fechado, com selo limão 'nunca aberto'."""
    h = round(w * 1.38)
    linhas = ''.join(f"<div style='height:12px;border-radius:6px;background:rgba(10,26,51,.10);margin-top:22px;width:{p}%'></div>" for p in (92, 80, 88, 64))
    corpo = (f"<div style='position:absolute;left:{left}px;top:{top}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);transform-origin:50% 50%'>"
             f"<div style='position:absolute;left:18px;top:18px;width:{w}px;height:{h}px;border-radius:22px;background:#D9E6F7'></div>"
             f"<div style='position:absolute;left:0;top:0;width:{w}px;height:{h}px;border-radius:22px;background:linear-gradient(170deg,#FFFFFF,#EEF3FA);"
             f"box-shadow:0 60px 90px rgba(0,25,80,.45),0 18px 30px rgba(0,25,80,.25);padding:{round(w*.12)}px;box-sizing:border-box'>"
             f"<div style='width:70px;height:10px;border-radius:5px;background:{AZUL}'></div>"
             f"<div style='font-family:j800;font-size:{round(w*.115)}px;line-height:1.05;color:{NAVY_TXT};letter-spacing:-.03em;margin-top:30px'>Manual do<br>proprietário</div>"
             f"{linhas}</div>"
             f"<div style='position:absolute;left:{round(w*.52)}px;top:{round(h*.60)}px;width:{round(w*.5)}px;height:{round(w*.5)}px;border-radius:50%;background:{LIMAO};"
             f"transform:rotate(14deg);display:flex;align-items:center;justify-content:center;text-align:center;font-family:j800;font-size:{round(w*.072)}px;line-height:1.05;"
             f"color:{NAVY_TXT};box-shadow:0 20px 40px rgba(0,25,80,.35)'>nunca<br>aberto</div></div>")
    return corpo

def capa(tt):
    L, w = (140, 800) if tt else (90, 900)
    c = "<div class='fill az'>" + fundo_azul((90, 0))
    y0 = 300 if tt else 110
    c += kicker('Primeira moto?', L, y0, 'escuro', w=w, tam=34)
    tam = 150 if not tt else 134
    c += titulo(['Ninguém lê', 'o manual', 'da moto.'], L, y0 + 90, tam, w=w, azul_de=1, lh=1.0)
    ya = y0 + 90 + alt_titulo(3, tam, 1.0) + 40
    c += apoio(['Então a gente leu: 3 números', 'que você precisa saber.'], L, ya, 42 if not tt else 40, w=w, cor='#FFFFFF', peso='j600')
    c += livreto(630 if not tt else 540, 800 if not tt else 1010, 360 if not tt else 400, rot=-9)
    c += desliza(L, 1240 if not tt else 1420, tt)
    return c + "</div>"

def kick_num(n, L, top, tt, tema='claro'):
    return kicker(f'{n} de 3 · Honda CG 160', L, top, tema, w=800, tam=30 if not tt else 32)

def fonte(L, top, tema='claro'):
    cor = 'rgba(10,26,51,.45)' if tema == 'claro' else 'rgba(255,255,255,.6)'
    return apoio(['Fonte: manuais do proprietário Honda', 'CG 160 Titan S (2021) e CG 160 Start (2022).'], L, top - 16, 22, w=800, cor=cor)

def pneu(tt):
    """Claro, duas colunas: frente × atrás, mesmo tamanho."""
    L, w = (140, 800) if tt else (90, 900)
    c = fundo('claro', (85, 15))
    y0 = 420 if tt else 250
    c += kick_num(1, L, y0, tt)
    c += titulo(['Quanto de ar', 'vai no pneu?'], L, y0 + 70, 84 if not tt else 80, w=w)
    yn = y0 + 70 + alt_titulo(2, 84 if not tt else 80) + (110 if tt else 80)
    big = 180 if not tt else 160
    for i, (num, lab) in enumerate([('25 psi', 'na frente'), ('29 psi', 'atrás, sem garupa')]):
        y = yn + i * (big + 50)
        c += numero(num, L, y, big, AZUL_ESC if i == 0 else NAVY_TXT, w=round(big * 2.75))
        c += apoio([lab], L + round(big * 2.85), y + big - 66, 40 if not tt else 36, w=w - round(big * 2.85), cor=NAVY_TXT, peso='j600')
    c += apoio(['Sempre com o pneu frio.'], L, yn + 2 * big + 50 + 40, 38, w=w, cor='#45536B')
    c += fonte(L, 1240 if not tt else 1440)
    return c + pag(2, N, tt)

def garupa(tt):
    """Azul chapado, número gigante centralizado."""
    L, w = (140, 800) if tt else (90, 900)
    c = "<div class='fill az'>" + fundo_azul((15, 85))
    y0 = 300 if tt else 130
    c += kick_num(2, 0, y0, tt, 'escuro').replace("left:0px;right:auto;width:800px", "left:0;right:0;width:1080px").replace("text-align:left", "text-align:center")
    c += titulo(['Vai levar garupa?'], L, y0 + 80, 84 if not tt else 80, w=w, alinha='center')
    big = 250 if not tt else 236
    yn = (560 if not tt else 760)
    c += numero('33 psi', 0, yn, big, '#FFFFFF', alinha='center', w=1080, glow='rgba(255,255,255,.35)')
    lw = round(big * 2.6)
    c += f"<div style='position:absolute;left:{540 - lw//2}px;top:{yn + big + 70}px;width:{lw}px;height:8px;border-radius:8px;background:{LIMAO};box-shadow:0 0 22px rgba(198,255,0,.5)'></div>"
    c += apoio(['no pneu de trás, com garupa.'], L, yn + big + 110, 44 if not tt else 42, w=w, alinha='center', cor='#FFFFFF', peso='j600')
    c += apoio(['Na frente continua 25 psi.'], L, yn + big + 180, 38 if not tt else 36, w=w, alinha='center')
    c += fonte(L, 1240 if not tt else 1440, 'escuro').replace("text-align:left", "text-align:center")
    return c + pag(3, N, tt) + "</div>"

def corrente(tt):
    """Claro, número alinhado à direita, alerta de 50 mm embaixo."""
    L, w = (140, 800) if tt else (90, 900)
    c = fundo('claro', (15, 20))
    y0 = 380 if tt else 220
    c += kick_num(3, L, y0, tt)
    c += titulo(['A corrente', 'tá folgada?'], L, y0 + 70, 84 if not tt else 80, w=w)
    big = 230 if not tt else 196
    yn = y0 + 70 + alt_titulo(2, 84 if not tt else 80) + (110 if tt else 70)
    c += numero('15–25', L, yn, big, AZUL_ESC, alinha='right', w=w)
    c += apoio(['mm de folga é o certo.'], L, yn + big + 20, 44 if not tt else 40, w=w, alinha='right', cor=NAVY_TXT, peso='j600')
    ya = yn + big + (150 if not tt else 170)
    c += pilula('Passou de 50 mm, não rode.', 'rgba(255,69,58,.12)', '#D92D20', L, ya, tam=36 if not tt else 34)
    c += fonte(L, 1240 if not tt else 1440)
    return c + pag(4, N, tt)

def tela(tt):
    """Celular com 13-conheca-moto + card solto: recorte contínuo e real das linhas de pneu de 10-lista-revisao (25 / 29 / 33 psi)."""
    L, w = (140, 800) if tt else (90, 900)
    arq, size = recorte('ios-1.0/rolagem/10-lista-revisao.png', (48, 3152, 1131, 3712))
    c = fundo('claro', (50, 60))
    ty = 260 if tt else 100
    tam = 70 if not tt else 62
    c += titulo(['Os números da sua moto', 'ficam no app.'], L, ty, tam, w=w, azul_de=1)
    ya = ty + alt_titulo(2, tam) + 24
    c += apoio(['Ficha do manual, item por item.'], L, ya, 40 if not tt else 38, w=w)
    yph = ya + (215 if tt else 129)
    c += fone('ios-1.0/13-conheca-moto', 720 if tt else 600, 540, yph)
    cw = w
    hc = round(size[1] * cw / size[0])
    yc = (1490 - hc) if tt else (1350 - 14 - hc)
    c += card_solto(arq, size, cw, L, yc, claro=True)[0]
    return c + pag(5, N, tt)

def final(tt):
    L, w = (140, 800) if tt else (90, 900)
    c = "<div class='fill az'>" + fundo_azul((50, 20))
    y0 = 440 if tt else 230
    c += (f"<div style='position:absolute;left:{540 - 130}px;top:{y0}px;width:260px;height:260px;border-radius:64px;background:#FFFFFF;"
          f"box-shadow:0 30px 60px rgba(0,30,90,.35);display:flex;align-items:center;justify-content:center'>"
          f"<img src='file://{ICON}' style='width:220px;height:220px;border-radius:52px'></div>")
    tam = 72 if not tt else 60
    ty = y0 + 360
    c += titulo(['O manual que ninguém lê,', 'agora no seu bolso.'], 60 if not tt else L, ty, tam, w=960 if not tt else w, alinha='center', azul_de=1)
    c += apoio(['Baixe agora o MinhaMoto.'], L, ty + alt_titulo(2, tam) + 34, 44 if not tt else 42, w=w, alinha='center', cor='#FFFFFF', peso='j600')
    c += f"<div style='position:absolute;left:0;right:0;top:{1030 if not tt else 1370}px;text-align:center'><img src='file://{SELOS}' style='width:540px'></div>"
    return c + "</div>"

def lista(tt):
    return [('escuro', capa(tt)), ('claro', pneu(tt)), ('escuro', garupa(tt)), ('claro', corrente(tt)), ('claro', tela(tt)), ('escuro', final(tt))]

if __name__ == '__main__':
    ok = render_lista(NOME, lista(False), lista(True))
    folha(NOME, 'CM06 · manual traduzido (iniciante)')
    sys.exit(0 if ok else 1)
