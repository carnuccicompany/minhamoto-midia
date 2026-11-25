#!/usr/bin/env python3
"""LOTE1 · CM04 · "5 desculpas que todo motoboy já deu pra moto."
Tipo: meme / humor (formato conversa: você × a moto) · Público: motoboy / entregador · Tom: zoeira (sem palavrão)
Ângulo: medo de prejuízo, com humor · Estética: claro limpo · Capa: número/lista · Final: salve e mande pro parceiro.
Base: CNN Brasil 25/09/2026 (ruído "raramente desaparece sozinho"); comparação com "lembrar de cabeça" (permitida).
Tela: só o card 7 (06-historico no celular, grande, sem card solto e sem barra de abas). Revisão 24/11: capa de conversa,
respostas nº 2 e nº 5 novas, sem contador de página (bolinhas embaixo da bolha), final em conversa.
Uso: python3 agencia/estudio/motores/lote1_cm04.py
"""
import sys, os, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lote1_base import *

NOME, N, T = 'CM04', 8, 'claro'

def balao(linhas, quem, left, top, w, tam, lado='esq'):
    """Balão de conversa. lado 'esq' = você (branco); 'dir' = a moto (azul)."""
    if lado == 'esq':
        st = (f"background:#FFFFFF;color:{NAVY_TXT};border-radius:46px 46px 46px 12px;"
              "box-shadow:0 0 0 2px rgba(10,26,51,.05),0 30px 60px rgba(10,26,51,.12),0 8px 18px rgba(10,26,51,.06)")
        al, cor_l = 'left', 'rgba(10,26,51,.5)'
    else:
        st = (f"background:linear-gradient(135deg,{AZUL},{AZUL_ESC});color:#FFFFFF;border-radius:46px 46px 12px 46px;"
              "box-shadow:0 30px 60px rgba(0,95,222,.30),0 8px 18px rgba(0,95,222,.18)")
        al, cor_l = 'right', 'rgba(10,26,51,.5)'
    pad_v, pad_h = round(tam * .52), round(tam * .62)
    txt = '<br>'.join(H.escape(l) for l in linhas)
    lab = (f"<div class=apoB style='left:{left}px;right:auto;width:{w}px;top:{top}px;text-align:{al};font-family:j600;font-size:{round(tam*.42)}px;"
           f"color:{cor_l}'>{quem}</div>")
    box_top = top + round(tam * .42 * 1.34) + 16
    # o balão encolhe pro tamanho do texto e encosta do lado certo
    pos = f"left:{left}px" if lado == 'esq' else f"right:{1080 - left - w}px"
    b = (f"<div style='position:absolute;{pos};top:{box_top}px;{st};padding:{pad_v}px {pad_h}px'>"
         f"<div class=apoB style='position:relative;left:auto;right:auto;top:auto;text-align:left;font-family:j700;font-size:{tam}px;line-height:1.18;"
         f"color:inherit;letter-spacing:-.02em;white-space:nowrap'>{txt}</div></div>")
    altura = round(tam * .42 * 1.34) + 16 + 2 * pad_v + round(len(linhas) * tam * 1.18)
    return lab + b, altura

def pontos(atual, total, left, top):
    c = ''
    for i in range(total):
        on = i == atual
        c += (f"<div style='position:absolute;left:{left + i*44}px;top:{top}px;width:{28 if on else 14}px;height:14px;border-radius:14px;"
              f"background:{AZUL if on else 'rgba(10,26,51,.16)'}'></div>")
        if on: left += 14
    return c

def digitando(left, top, escala=1.0):
    """Bolha 'digitando…' da moto (três pontos)."""
    w, h = round(150 * escala), round(84 * escala)
    pts = ''.join(f"<span style='display:inline-block;width:{round(18*escala)}px;height:{round(18*escala)}px;border-radius:50%;background:#FFFFFF;"
                  f"opacity:{o};margin:0 {round(6*escala)}px'></span>" for o in (.95, .7, .45))
    return (f"<div style='position:absolute;right:{1080 - left}px;top:{top}px;width:{w}px;height:{h}px;border-radius:42px 42px 12px 42px;"
            f"background:linear-gradient(135deg,{AZUL},{AZUL_ESC});display:flex;align-items:center;justify-content:center;"
            f"box-shadow:0 20px 40px rgba(0,95,222,.25)'>{pts}</div>")

def capa(tt):
    """Capa em formato de conversa ocupando a tela: título em cima e as bolhas grandes."""
    L, w = (140, 800) if tt else (90, 900)
    c = fundo(T, (80, 70))
    ty = 240 if tt else 100
    tam = 88 if not tt else 84
    c += titulo(['5 desculpas', 'que todo motoboy', 'já deu pra moto.'], L, ty, tam, w=w, azul_de=2)
    ya = ty + alt_titulo(3, tam) + 24
    c += apoio(['A nº 3 é clássica.'], L, ya, 42, w=w, cor=NAVY_TXT, peso='j600')
    tb = 72 if not tt else 68
    yb = ya + (160 if tt else 120)
    b1, h1 = balao(['Depois eu vejo isso aí.'], 'Você', L, yb, w - 40, tb, 'esq')
    b2, h2 = balao(['Já ouvi essa antes.'], 'A moto', L + 40, yb + h1 + 40, w - 40, tb, 'dir')
    c += b1 + b2 + digitando(L + w, yb + h1 + 40 + h2 + 30, 1.1 if tt else 1.0)
    c += desliza(L, 1230 if not tt else 1420, tt)
    return c

def desculpa(n, voce, moto, tt, reacao=None, extra=None):
    """Conversa de 3 falas (você · a moto · você de novo), centrada na vertical; bolinhas embaixo."""
    L, w = (140, 800) if tt else (90, 900)
    tam = 68 if tt else 66
    tr = round(tam * .82)
    c = fundo(T, (20 if n % 2 else 80, 20))
    top = 340 if tt else 190
    c += pilula(f'Desculpa nº {n - 1}', NAVY_TXT, '#FFFFFF', L, top, tam=30)
    if extra == 'classica':   # a capa prometeu "a nº 3 é clássica": selo só nela
        c += pilula('A clássica', LIMAO, NAVY_TXT, L + 300, top, tam=30)
    y1 = top + (150 if tt else 110)
    b1, h1 = balao(voce, 'Você', L, y1, w - 60, tam, 'esq')
    y2 = y1 + h1 + (70 if tt else 44)
    b2, h2 = balao(moto, 'A moto', L + 60, y2, w - 60, tam, 'dir')
    c += b1 + b2
    yf = y2 + h2 + (70 if tt else 44)
    if reacao:
        b3, h3 = balao([reacao], 'Você', L, yf, w - 60, tr, 'esq')
        c += b3; yf += h3 + (50 if tt else 34)
        if extra == 'visto':
            c += (f"<div class=apoB style='left:{L}px;right:auto;width:{w - 60}px;top:{yf - (40 if tt else 26)}px;text-align:left;font-family:j600;"
                  f"font-size:26px;color:rgba(10,26,51,.45)'>Visto às 23:48</div>")
    if extra == 'digitando':
        c += digitando(L + w, yf, 1.0)
    c += pontos(n - 2, 5, 540 - 100, 1450 if tt else 1260)
    return c

def tela(tt):
    """R5 (25/11): o app responde na conversa: o "eu lembro de cabeça" é respondido com o registro REAL da troca de óleo
    (06-historico rolagem: 'Troca de óleo e filtro · 25/08/2026 · 27.100 km'), card solto sem os ícones de editar/excluir."""
    L, w = (140, 800) if tt else (90, 900)
    c = fundo(T, (70, 60))
    ty = 300 if tt else 110
    tam = 92 if not tt else 80
    c += titulo(['Quem não lembra,', 'anota no app.'], L, ty, tam, w=w, azul_de=1)
    ya = ty + alt_titulo(2, tam) + 24
    c += apoio(['Data, km e valor de cada serviço.'], L, ya, 40 if not tt else 38, w=w)
    tb = 66 if not tt else 64
    y1 = ya + (150 if tt else 110)
    b1, h1 = balao(['Eu lembro de cabeça.'], 'Você', L, y1, w - 60, tb, 'esq')
    c += b1
    arq, size = recorte('ios-1.0/rolagem/06-historico.png', (48, 2935, 1131, 3296))
    cw = w; yc = y1 + h1 + (100 if tt else 70)
    c += (f"<div class=apoB style='left:{L}px;right:auto;width:{cw}px;top:{yc - 46}px;text-align:right;font-family:j600;font-size:28px;"
          f"color:rgba(10,26,51,.5)'>MinhaMoto</div>")
    bloco, hc = card_solto(arq, size, cw, L, yc, claro=True)
    c += bloco
    b3, h3 = balao(['Tá. Você venceu.'], 'Você', L, yc + hc + (80 if tt else 56), w - 60, round(tb * .9), 'esq')
    return c + b3

def final(tt):
    """Fecha em formato de conversa: a moto pede, você manda."""
    L, w = (140, 800) if tt else (90, 900)
    c = fundo(T, (30, 80))
    y0 = 440 if tt else 290
    c += kicker('Salve este post', L, y0, T, w=w, tam=34)
    tb = 64 if not tt else 56
    y1 = y0 + 110
    b1, h1 = balao(['Mande isso pro parceiro', 'que sempre diz', '“depois do corre”'], 'A moto', L + 40, y1, w - 40, tb, 'dir')
    y2 = y1 + h1 + 60
    env = (f"<span style='display:inline-block;vertical-align:-8px;margin-left:18px;line-height:0'>{icone('enviar', round(tb*.8), AZUL, 8)}</span>")
    b2, h2 = balao(['Enviando agora.'], 'Você', L, y2, w - 40, tb, 'esq')
    b2 = b2.replace('Enviando agora.</div>', 'Enviando agora.' + env + '</div>')
    c += b1 + b2
    c += assinatura(1380 if tt else 1190, T, left=L)
    return c

def lista(tt):
    return [
        (T, capa(tt)),
        (T, desculpa(2, ['Tá barulhando,', 'mas tá andando.'], ['Tô avisando faz', 'três semanas.'], tt, 'Semana que vem eu vejo.')),
        (T, desculpa(3, ['Essa luz sempre', 'acendeu, é normal.'], ['Normal é eu te deixar', 'a pé na entrega.'], tt, 'Tá bom, amanhã eu olho.', extra='visto')),
        (T, desculpa(4, ['Depois do corre', 'eu troco o óleo.'], ['O corre não acaba.', 'Meu óleo, sim.'], tt, 'Essa doeu.', extra='classica')),
        (T, desculpa(5, ['A corrente tá', 'folgadinha, suave.'], ['Suave até ela', 'pular da coroa.'], tt, 'Amanhã eu ajusto.', extra='digitando')),
        (T, desculpa(6, ['Eu lembro de cabeça', 'quando troquei.'], ['Lembra? Então', 'fale a data.', 'Eu espero.'], tt, 'Foi… mês passado?')),
        (T, tela(tt)),
        (T, final(tt)),
    ]

if __name__ == '__main__':
    ok = render_lista(NOME, lista(False), lista(True))
    folha(NOME, 'CM04 · desculpas de motoboy (claro)')
    sys.exit(0 if ok else 1)
