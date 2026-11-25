#!/usr/bin/env python3
"""LOTE1 · CM01 rodada 4 · "4 luzes no painel. Duas mandam parar na hora."
Público: quem vai trabalhar de moto · Tipo: dica/teste (manual de bolso) · Ângulo: medo de prejuízo · Tom: especialista
Estética: escuro premium · Capa: pergunta/teste · Final: CTA do app com "por R$19,90".
R4 (constituição 24/11): tela do app só no card 6 (mockup + card solto); cards 2–5 = conteúdo (luz de painel desenhada + copy).
Conteúdo das 4 luzes = textos do próprio app (tela Sinais de problema, iPhone 1.0).
Uso: python3 agencia/estudio/motores/lote1_cm01.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lote1_base import *
from recortes_app import trecho

NOME, N, T = 'CM01', 7, 'escuro'
SIN_ROL = 'ios-1.0/rolagem/12-sinais-problema.png'
_, _RUNS = __import__('recortes_app').cards(SIN_ROL)
ROLA_LUZES = _RUNS[9][0] - 150 - 430 + 177   # celular parado na seção 'Luzes de alerta em qualquer moto'
LUZES = [('oleo', VERM), ('temp', VERM), ('motor', AMBAR), ('bateria', AMBAR)]

def faixa_painel(atual, left, top, tam=46, gap=26):
    """As 4 luzes pequenas em fila; só a do card atual acesa (as outras apagadas)."""
    c = ''; caixa = round(tam * 1.55)
    for i, (nm, cor) in enumerate(LUZES):
        x = left + i * (caixa + gap)
        c += luz_painel(nm, tam, cor if i == atual else '#3A4558', x, top, aceso=(i == atual))
    return c

NOMES_CURTOS = ['Óleo', 'Temperatura', 'Injeção', 'Bateria']
def painel_rodape(atual, left, top, w):
    """R5 (25/11): barra de painel no rodapé (enche o espaço morto e amarra o card ao tema): as 4 luzes com o nome
    embaixo; só a do card acesa, as outras apagadas; contador "1 de 4"."""
    h = 190; tam = 54; caixa = round(tam * 1.55); col = w / 4
    c = (f"<div style='position:absolute;left:{left}px;top:{top}px;width:{w}px;height:{h}px;border-radius:40px;"
         f"background:linear-gradient(180deg,rgba(255,255,255,.06),rgba(255,255,255,.02));box-shadow:inset 0 0 0 2px rgba(255,255,255,.08)'></div>")
    for i, (nm, cor) in enumerate(LUZES):
        cx = left + col * i + col / 2; x = round(cx - caixa / 2)
        c += luz_painel(nm, tam, cor if i == atual else '#3A4558', x, top + 22, aceso=(i == atual))
        c += (f"<div style='position:absolute;left:{round(cx - col/2)}px;width:{round(col)}px;top:{top + 22 + caixa + 10}px;text-align:center;"
              f"font-family:j700;font-size:26px;color:{'#F4F7FC' if i == atual else 'rgba(255,255,255,.38)'}'>{NOMES_CURTOS[i]}</div>")
    return c

def capa(tt):
    if tt:
        L, w, Ty, tam = 140, 800, 300, 96
    else:
        L, w, Ty, tam = 90, 900, 120, 102
    c = fundo(T, (78, 70))
    c += titulo(['4 luzes no painel.', 'Duas mandam', 'parar na hora.'], L, Ty, tam, w=w, azul_de=1)
    ya = Ty + alt_titulo(3, tam) + 30
    c += apoio(['Você sabe quais?'], L, ya, 52 if not tt else 54, w=w, cor='#F4F7FC', peso='j700')
    # as 4 luzes, todas em branco (sem entregar a resposta pela cor), numeradas
    tam_i = 110 if not tt else 108
    caixa = round(tam_i * 1.55); gap = (w - 4 * caixa) // 3
    yl = 700 if not tt else 960
    for i, (nm, _) in enumerate(LUZES):
        x = L + i * (caixa + gap)
        c += luz_painel(nm, tam_i, '#EAF2FF', x, yl)
        c += (f"<div class=apoB style='left:{x}px;right:auto;width:{caixa}px;top:{yl + caixa + 22}px;text-align:center;font-family:j700;"
              f"font-size:34px;color:rgba(255,255,255,.6)'>{i + 1}</div>")
    c += desliza(L, 1210 if not tt else 1360, tt)
    return c

def luz(n, idx, nome_luz, status, cor_st, linhas, apo, lado, tt, modo='padrao', tam_tit=None):
    """modo 'padrao': ícone grande + rótulo ao lado; 'gigante': ícone enorme saindo do quadro à direita;
    'enorme': ícone pequeno e título ocupando 2/3 do card. (revisão 24/11: quebrar a mesmice dos cards 2–5)"""
    nm, cor = LUZES[idx]
    L, w = (140, 800) if tt else (90, 900)
    fundo_st = 'rgba(255,69,58,.16)' if cor_st == VERM else 'rgba(255,176,32,.16)'
    y_faixa = 1400 if tt else 1170
    if modo == 'gigante':
        c = fundo(T, (85, 18))
        tam_i = 300 if not tt else 330
        caixa = round(tam_i * 1.55)
        c += luz_painel(nm, tam_i, cor, 1080 - caixa - (60 if not tt else 140), 110 if not tt else 220, raio=140)
        yl = 180 if not tt else 760
        c += apoio(nome_luz.split(' · '), L, yl, 40 if not tt else 40, w=(1080 - caixa - 60 - L - 30) if not tt else 800, cor='#F4F7FC', peso='j700')
        c += pilula(status, fundo_st, cor_st, L, yl + (122 if (' · ' in nome_luz) else 76), tam=34)
        tam = tam_tit or (88 if not tt else 88)
        Ty = 680 if not tt else 1010
    elif modo == 'enorme':
        c = fundo(T, (20, 30))
        tam_i = 110 if not tt else 120
        caixa = round(tam_i * 1.55)
        ty_i = 140 if not tt else 260
        c += luz_painel(nm, tam_i, cor, L, ty_i)
        c += apoio([nome_luz], L + caixa + 36, ty_i + 4, 42, w=560, cor='#F4F7FC', peso='j700')
        c += pilula(status, fundo_st, cor_st, L + caixa + 36, ty_i + caixa - 64, tam=34)
        tam = tam_tit or (132 if not tt else 124)
        Ty = 470 if not tt else 640
    else:
        c = fundo(T, (22 if lado == 'esq' else 78, 18))
        tam_i = 200 if not tt else 230
        top_i = 150 if not tt else 260
        caixa = round(tam_i * 1.55)
        xi = L if lado == 'esq' else L + w - caixa
        c += luz_painel(nm, tam_i, cor, xi, top_i)
        xt = L + caixa + 44 if lado == 'esq' else L
        wt = w - caixa - 44
        c += apoio([nome_luz], xt, top_i + caixa // 2 - 78, 44, w=wt, cor='#F4F7FC', peso='j700')
        c += pilula(status, fundo_st, cor_st, xt, top_i + caixa // 2 + 6, tam=34)
        tam = tam_tit or (94 if not tt else 82)
        Ty = 600 if not tt else 820
    c += titulo(linhas, L, Ty, tam, w=w, azul_de=len(linhas) - 1)
    c += apoio(apo if isinstance(apo, list) else [apo], L, Ty + alt_titulo(len(linhas), tam) + 30, 38 if not tt else 38, w=w)
    if tt and modo == 'gigante': c += faixa_painel(idx, L, y_faixa, tam=46)
    else: c += painel_rodape(idx, L, 1120 if not tt else 1290, w)
    return c + pag(n, N, tt)

def tela(tt):
    """Card do app inteiro e contínuo (recorte real de 'Luz de pressão do óleo'), com um contorno azul por fora
    acendendo só a seção 'O que fazer' (destaque sem apagar nada do print)."""
    A, B = 9455, 10447
    arq, size = recorte(SIN_ROL, (48, A, 1131, B))
    s0, s1 = 9897, 10167            # seção 'O que fazer' (divisórias reais do card)
    L, w = (140, 800) if tt else (90, 900)
    c = fundo(T, (50, 60))
    ty = 330 if tt else 100
    tam = 72 if not tt else 66
    c += titulo(['Cada luz do painel,', 'explicada no app.'], L, ty, tam, w=w, azul_de=1)
    ya = ty + alt_titulo(2, tam) + 24
    c += apoio(['Com o que fazer e quando ir à oficina.'], L, ya, 38, w=w)
    cw, cl = w, L
    yc = ya + (150 if tt else 90)
    k = cw / size[0]
    glow = (f"<div style='position:absolute;left:{cl + cw//2 - 560}px;top:{yc - 150}px;width:1120px;height:{round(size[1]*k) + 300}px;"
            f"border-radius:50%;background:radial-gradient(closest-side, rgba(255,69,58,.14), rgba(0,0,0,0) 100%)'></div>")
    bloco, hc = card_solto(arq, size, cw, cl, yc)
    pad = 10
    anel = (f"<div style='position:absolute;left:{cl - pad}px;top:{yc + round((s0 - A)*k) - pad}px;width:{cw + 2*pad}px;height:{round((s1 - s0)*k) + 2*pad}px;"
            f"border:5px solid {AZUL_CLARO};border-radius:28px;box-shadow:0 0 36px rgba(82,169,254,.65),inset 0 0 24px rgba(82,169,254,.25)'></div>")
    return c + glow + bloco + anel + pag(6, N, tt)

def lista(tt):
    return [
        (T, capa(tt)),
        (T, luz(2, 0, 'Luz do óleo', 'Pare agora', VERM, ['Cada metro a mais', 'com ela acesa', 'sai do seu bolso.'],
                'Encoste e desligue o motor na hora.', 'esq', tt)),
        (T, luz(3, 1, 'Luz de temperatura · motos a água', 'Pare agora', VERM, ['Motor fervendo?', 'Não abra', 'o radiador.'],
                'O líquido sai sob pressão e queima.', 'dir', tt, modo='gigante')),
        (T, luz(4, 2, 'Luz da injeção', 'Atenção', AMBAR, ['Injeção acesa', 'não é motivo', 'pra pânico.'],
                ['Respondendo bem? Siga sem forçar', 'e passe no scanner.'], 'esq', tt, tam_tit=None)),
        (T, luz(5, 3, 'Luz da bateria', 'Atenção', AMBAR, ['Desligou,', 'pode não', 'pegar mais.'],
                'Não apague o motor longe de casa.', 'dir', tt, modo='enorme')),
        (T, tela(tt)),
        (T, final_app(tt, T, 'Seu painel avisa.', 'O MinhaMoto explica.', 'Baixe agora e entenda sua moto.', preco=True)),
    ]

if __name__ == '__main__':
    ok = render_lista(NOME, lista(False), lista(True))
    folha(NOME, 'CM01 r4 · 4 luzes no painel')
    sys.exit(0 if ok else 1)
