#!/usr/bin/env python3
"""CM01 · Carrossel-modelo da lapidação (23/11): "Acendeu no painel. Parar ou seguir?"
Linha proposta: "Manual de bolso" (valor/educacional) — cada card: pergunta + resposta curta no título,
e o card REAL do app (tela Sinais de problema) flutuando como prova. Base: direção B (navy + luz azul, Poppins).
Uso: python3 agencia/estudio/motores/cm01_luzes.py   → agencia/estudio/pecas/CM01/{carrossel,carrossel-tiktok}/
"""
import os, sys, html as H
AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(AQUI, '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'agencia', 'direcao-v2'))
sys.path.insert(0, AQUI)
from estaticos import grad_bg, celular, cta, PH45, PH916   # mesmo mockup, mesma régua
from recortes_app import recorte
from render_check import render

SAIDA = os.path.join(REPO, 'agencia', 'estudio', 'pecas', 'CM01')
SINAIS = 'rolagem/12-sinais-problema.png'
# índices dos cards na tela Sinais de problema (ver recortes_app.py)
OLEO, TEMP, INJ, BAT = 9, 10, 11, 13
N = 7

def ui(idx, w, top, cab=False, extra=''):
    """Card real do app, flutuando (sombra profunda + luz azul), cantos iguais aos do app."""
    arq, (sw, sh) = recorte(SINAIS, idx, cab)
    h = round(sh * w / sw); r = round(48 * w / sw)
    return (f"<div class=uicard style='position:absolute;left:50%;top:{top}px;width:{w}px;height:{h}px;margin-left:{-w//2}px;border-radius:{r}px;overflow:hidden;"
            f"box-shadow:0 0 0 2px rgba(255,255,255,.07),0 50px 90px rgba(0,0,0,.65),0 16px 30px rgba(0,0,0,.45),0 0 120px rgba(82,169,254,.22);{extra}'>"
            f"<img src='file://{arq}' style='display:block;width:100%;height:100%'></div>"), h

def pag(n, tt):
    if tt: return ''
    return f"<div class='pag t'>{n:02d} / {N:02d}</div>"

def titulo(l1, l2, top, tam):
    return (f"<div class=titB style='top:{top}px;font-size:{tam}px'>{H.escape(l1)}<br>"
            f"<span class=b>{H.escape(l2)}</span></div>")

def capa(tt):
    L = dict(t=230, tam=72, apo=420, pilha=None, w=800, gap=26, desl=1400) if tt else \
        dict(t=110, tam=88, apo=338, pilha=None, w=880, gap=24, desl=None)
    c = grad_bg('B', (50, 66)) + titulo('Acendeu no painel.', 'Parar ou seguir?', L['t'], L['tam'])
    c += (f"<div class=apoB style='top:{L['apo']}px;font-size:{42 if tt else 40}px'>As 4 luzes que você precisa entender.</div>")
    blocos = [ui(i, L['w'], 0, cab=True)[1] for i in (OLEO, TEMP, INJ, BAT)]
    total = sum(blocos) + L['gap']*3
    ini, fim = (L['apo'] + 90, L['desl'] - 50) if tt else (L['apo'] + 90, 1300)
    y = ini + (fim - ini - total)//2
    for idx in (OLEO, TEMP, INJ, BAT):
        bloco, h = ui(idx, L['w'], y, cab=True)
        c += bloco; y += h + L['gap']
    if tt:
        c += f"<div class=desliza style='bottom:auto;top:{L['desl']}px'>Deslize <b>→</b></div>"
    else:
        c += "<div class='pag t' style='color:#C6FF00'>Deslize →</div>"
    return c

def card_luz(n, idx, l1, l2, tt):
    # título em 2 linhas; o card do app fica centralizado no espaço que sobra
    if tt:
        w, top_t, tam, ini, fim = 800, 200, 62, 400, 1480
    else:
        w, top_t, tam, ini, fim = 900, 96, 76, 300, 1300
    h = ui(idx, w, 0)[1]
    bloco, h = ui(idx, w, ini + (fim - ini - h)//2)
    return grad_bg('B', (50, 62)) + titulo(l1, l2, top_t, tam) + bloco + pag(n, tt)

def prova(tt):
    if tt:
        t = titulo('Luzes e sinais da sua moto,', 'explicados no app.', 200, 54)
        a = "<div class=apoB style='top:352px;font-size:32px'>Os símbolos variam conforme o modelo.</div>"
        ph = celular('rolagem/12-sinais-problema', w=500, top=430, rola=7890)
    else:
        t = titulo('Luzes e sinais da sua moto,', 'explicados no app.', 88, 62)
        a = "<div class=apoB style='top:254px;font-size:30px'>Os símbolos variam conforme o modelo.</div>"
        ph = celular('rolagem/12-sinais-problema', w=470, top=318, rola=7890)
    return grad_bg('B', (50, 60)) + t + a + ph + pag(6, tt)

def final(tt):
    tit = 'Entenda sua moto<br><span class=b>antes do susto.</span>'
    if tt:
        return grad_bg('B', (50, 36)) + cta('B', tit, 'Baixe agora o MinhaMoto.', True, top=360, pad=140, H_=1920, selos_top=1330).replace('font-size:96px', 'font-size:80px')
    return grad_bg('B', (50, 36)) + cta('B', tit, 'Baixe agora o MinhaMoto.', True, top=170, H_=1350)

def cards(tt=False):
    return [
        capa(tt),
        card_luz(2, OLEO, 'Luz do óleo acesa?', 'Não dá pra esperar.', tt),
        card_luz(3, TEMP, 'O motor esquentou?', 'Espere antes de mexer.', tt),
        card_luz(4, INJ, 'Luz da injeção?', 'Atenção, sem pânico.', tt),
        card_luz(5, BAT, 'Luz da bateria?', 'Desligue só em casa.', tt),
        prova(tt),
        final(tt),
    ]

if __name__ == '__main__':
    so = sys.argv[1] if len(sys.argv) > 1 else 'todos'
    if so in ('todos', '45'):
        for i, c in enumerate(cards(False), 1):
            render(c, 1080, 1350, os.path.join(SAIDA, 'carrossel', f'{i:02d}.jpg'))
    if so in ('todos', 'tiktok'):
        for i, c in enumerate(cards(True), 1):
            render("<div class=tt>" + c + "</div>", 1080, 1920, os.path.join(SAIDA, 'carrossel-tiktok', f'{i:02d}.jpg'))
