#!/usr/bin/env python3
"""LOTE1 · CM01 rodada 4 · "4 luzes no painel. Duas mandam parar na hora."
Público: quem vai trabalhar de moto · Tipo: dica/teste (manual de bolso) · Ângulo: medo de prejuízo · Tom: especialista
Estética: escuro premium · Capa: pergunta/teste · Final: CTA do app (sem preço, 26/11).
R4 (constituição 24/11): tela do app só no card 6 (mockup + card solto); cards 2–5 = conteúdo (luz de painel desenhada + copy).
Conteúdo das 4 luzes = textos do próprio app (tela Sinais de problema, iPhone 1.0).
Uso: python3 agencia/estudio/motores/lote1_cm01.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lote1_base import *
import lote1_base as _B; _B.IOS = 'v1.0.2'   # r7 (26/11): telas do visual novo 1.0.2
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
    tam_i = 96 if not tt else 96
    caixa = round(tam_i * 1.55); gap = (w - 4 * caixa) // 3
    yl = 700 if not tt else 960
    for i, (nm, _) in enumerate(LUZES):
        x = L + i * (caixa + gap)
        c += (f"<div style='position:absolute;left:{x}px;top:{yl}px;width:{caixa}px;height:{caixa}px;border-radius:50%;"
              f"background:rgba(255,255,255,.06);box-shadow:inset 0 0 0 2px rgba(255,255,255,.12);display:flex;align-items:center;justify-content:center'>"
              f"<div style='line-height:0;opacity:.85'>{icone(nm, round(tam_i*.55), '#EAF2FF')}</div></div>")
        c += (f"<div class=apoB style='left:{x}px;right:auto;width:{caixa}px;top:{yl + caixa + 22}px;text-align:center;font-family:j700;"
              f"font-size:34px;color:rgba(255,255,255,.6)'>{i + 1}</div>")
    c += foto_base(foto_prep('6664916', crop=(0, 300, 1301, 1500), satura=.55, escurece=.7, frio=.1, nome='cm01r6_capa'), 880 if not tt else 1180, pos='50% 45%', altura=1350 if not tt else 1920)
    c += desliza(L, 1210 if not tt else 1360, tt)
    return c

FOTOS_LUZ = [('6664916', (0, 300, 1301, 1500), '50% 45%'), ('31664515', (0, 380, 1350, 1600), '50% 40%'),
             ('6664916', (150, 150, 1301, 1150), '45% 50%'), ('31664515', (100, 250, 1350, 1350), '55% 45%')]
def luz(n, idx, nome_luz, status, cor_st, linhas, apo, lado, tt, modo='padrao', tam_tit=None):
    """R6 (26/11): "ícones fortes demais" → ícone pequeno na cor da luz, sem janela nem brilho, ao lado do nome;
    foto REAL de painel de moto na metade de baixo (mundo do público), mesma gradação na peça toda."""
    nm, cor = LUZES[idx]
    L, w = (140, 800) if tt else (90, 900)
    fundo_st = 'rgba(255,69,58,.18)' if cor_st == VERM else 'rgba(255,176,32,.18)'
    fid, crop, pos = FOTOS_LUZ[idx]
    arq = foto_prep(fid, crop=crop, satura=.55, escurece=.85, frio=.1, nome=f'cm01r6_{idx}')
    c = fundo(T, (50, 10))
    c += foto_base(arq, 600 if not tt else 950, pos=pos, altura=1350 if not tt else 1920)
    yl = 150 if not tt else 300
    c += f"<div style='position:absolute;left:{L}px;top:{yl}px;line-height:0'>{icone(nm, 58, cor)}</div>"
    c += apoio([nome_luz.replace(' · ', ' (') + (')' if ' · ' in nome_luz else '')], L + 80, yl + 4, 38, w=w - 80, cor='#F4F7FC', peso='j700')
    c += pilula(status, fundo_st, cor_st, L, yl + 90, tam=32)
    tam = tam_tit or (94 if not tt else 82)
    Ty = yl + 210
    c += titulo(linhas, L, Ty, tam, w=w, azul_de=len(linhas) - 1)
    c += apoio(apo if isinstance(apo, list) else [apo], L, Ty + alt_titulo(len(linhas), tam) + 30, 40, w=w, cor='#F4F7FC')
    return c + pag(n, N, tt)

def tela(tt):
    """R6: o app só como tela REAL inteira no celular (sinais de problema, parado na luz de pressão do óleo)."""
    L, w = (140, 800) if tt else (90, 900)
    c = fundo(T, (50, 60))
    ty = 330 if tt else 100
    tam = 80 if not tt else 72
    c += titulo(['Cada luz do painel,', 'explicada no app.'], L, ty, tam, w=w, azul_de=1)
    ya = ty + alt_titulo(2, tam) + 24
    c += apoio(['Com o que fazer e quando ir à oficina.'], L, ya, 40, w=w)
    c += fone('v1.0.2/rolagem/12-sinais-problema', 660 if tt else 600, 540, ya + (130 if tt else 100), rola=8900)
    return c + pag(6, N, tt)

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
        (T, final_app(tt, T, 'Seu painel avisa.', 'O MinhaMoto explica.', 'Baixe agora e entenda sua moto.', preco=False)),
    ]

if __name__ == '__main__':
    ok = render_lista(NOME, lista(False), lista(True))
    folha(NOME, 'CM01 r4 · 4 luzes no painel')
    sys.exit(0 if ok else 1)
