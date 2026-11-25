#!/usr/bin/env python3
"""LOTE1 · CM05 (refeito 24/11 após revisão) · "A chuva chegou. Sua moto tá pronta pra ela?"
Tipo: checklist sazonal · Público: quem vai trabalhar de moto · Tom: mecânico parceiro · Ângulo: segurança
Estética: escuro premium com feixe de farol na chuva (SVG, sem foto) · Capa: tipografia gigante · Final: CTA app + "por R$19,90".
Revisão: sem ícones (tipografia forte no lugar), cada checagem com composição própria, card do app = trecho real
do sheet 28-item-proximo ampliado (sem 11-cuidados), copy nova.
Fontes: Portal do Trânsito 09/11/2026 · AutoPapo 01/07/2025 (ver pecas/LOTE1/CM05/fontes.md).
Uso: python3 agencia/estudio/motores/lote1_cm05.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lote1_base import *

NOME, N, T = 'CM05', 7, 'escuro'

def fundo_chuva(tt, cx, abertura, intens=1.0, seed=7, luz=(50, 20)):
    h = 1920 if tt else 1350
    return fundo(T, luz) + chuva_luz(1080, h, cx, -40, abertura, n=320 if tt else 260, seed=seed, intens=intens)

def barra(n, L, top, w, tt):
    """Etiqueta 'Checagem n de 4' + 4 segmentos (o atual aceso)."""
    c = kicker(f'Checagem {n} de 4', L, top, T, w=w, tam=30 if not tt else 32)
    seg = (w - 3 * 14) / 4
    for i in range(4):
        on = i < n
        c += (f"<div style='position:absolute;left:{round(L + i*(seg + 14))}px;top:{top + 58}px;width:{round(seg)}px;height:8px;border-radius:8px;"
              f"background:{AZUL_CLARO if on else 'rgba(255,255,255,.14)'};{'box-shadow:0 0 16px rgba(82,169,254,.7);' if i == n - 1 else ''}'></div>")
    return c

def capa(tt):
    """Foto real (5195567, Pexels): moto vindo na chuva com farol aceso. Título gigante embaixo."""
    L, w = (140, 800) if tt else (90, 900)
    h = 1920 if tt else 1350
    arq = foto_prep('5195567', satura=.6, frio=.12, crop=(510, 0, 1072, 1000) if tt else (395, 0, 1195, 1000), nome='cm05r5_capa_tt' if tt else 'cm05r5_capa')
    c = foto_fundo(arq, pos='50% 0%', forca=.92, topo=.15)
    ty = 820 if tt else 640
    tam = 190 if tt else 196
    c += titulo(['A chuva', 'chegou.'], L, ty, tam, w=w, lh=.98)
    y2 = ty + alt_titulo(2, tam, .98) + 24
    c += titulo(['Sua moto tá pronta pra ela?'], L, y2, 56 if not tt else 52, w=w, azul_de=0)
    c += apoio(['4 checagens antes de sair pro trampo.'], L, y2 + 90, 38 if not tt else 36, w=w, cor='#F4F7FC')
    c += desliza(L, 1255 if not tt else 1420, tt)
    return c

TOPO_IND = lambda tt: 230 if tt else 110

def check_foto(n, arq, pos, linhas, azul_de, apo, tt, tam=None, ty=None):
    """Check com foto de detalhe em tela cheia (degradê escuro embaixo), indicador fixo no topo."""
    L, w = (140, 800) if tt else (90, 900)
    c = foto_fundo(arq, pos=pos, forca=.94, topo=.55)
    c += barra(n, L, TOPO_IND(tt), 520, tt)
    tam = tam or (116 if not tt else 108)
    ty = ty or ((1500 - 80 - alt_titulo(len(linhas), tam, 1.0) - 60) if tt else (1350 - 90 - alt_titulo(len(linhas), tam, 1.0) - 60))
    c += titulo(linhas, L, ty, tam, w=w, azul_de=azul_de, lh=1.0)
    c += apoio([apo], L, ty + alt_titulo(len(linhas), tam, 1.0) + 26, 36 if not tt else 32, w=w, cor='#F4F7FC')
    return c

def foto_topo(arq, top, h_total):
    """Foto na largura do card (1080), deslocada verticalmente; abaixo dela, degradê até o navy."""
    return (f"<div class=fill style='background:#010711'></div>"
            f"<img src='file://{arq}' style='position:absolute;left:0;top:{top}px;width:1080px'>"
            f"<div class=fill style='background:linear-gradient(180deg,rgba(1,7,17,.55) 0%,rgba(1,7,17,0) 16%,rgba(1,7,17,0) 50%,rgba(1,7,17,.9) 74%,#010711 86%)'></div>")

def pneu(tt):
    """Foto 12731259 na largura, subida pra roda dianteira aparecer acima do título; farol neutralizado (sem mancha)."""
    L, w = (140, 800) if tt else (90, 900)
    arq = foto_prep('12731259', satura=.6, frio=.12, neutro=[(756, 968, 46, 44)], escurece=1.35, nome='cm05r5_pneu')
    c = foto_topo(arq, -120 if tt else -330, 1920 if tt else 1350)
    c += barra(1, L, TOPO_IND(tt), 520, tt)
    y1 = 1160 if tt else 1000
    c += titulo(['Pneu careca na chuva'], L, y1, 72, w=w)
    c += titulo(['vira sabão.'], L, y1 + 80, 128 if not tt else 124, w=w, azul_de=0, lh=1.0)
    c += apoio(['Confira o desgaste e a calibragem do manual.'], L, y1 + 80 + 140, 36 if not tt else 32, w=w, cor='#F4F7FC')
    return c + pag(2, N, tt)

def freio(tt):
    """Foto 19949302 (disco de freio dianteiro), esfriada pro tom da peça; texto em cima."""
    L, w = (140, 800) if tt else (90, 900)
    arq = foto_prep('19949302', crop=(0, 250, 1350, 1800), satura=.6, escurece=.95, frio=.12, nome='cm05r5_freio')
    c = foto_fundo(arq, pos='50% 100%', degr='escuro_topo', forca=.93, topo=.35)
    c += barra(2, L, TOPO_IND(tt), 520, tt)
    tam = 112 if not tt else 104
    ty = 380 if tt else 220
    c += titulo(['Freio chiando', 'ou mais fraco?'], L, ty, tam, w=w, lh=1.0)
    y2 = ty + alt_titulo(2, tam, 1.0) + 26
    c += titulo(['Passe na oficina hoje.'], L, y2, 70, w=w, azul_de=0)
    c += apoio(['Água e sujeira mudam a frenagem.'], L, y2 + 110, 38 if not tt else 36, w=w, cor='#F4F7FC')
    return c + pag(3, N, tt)

def corrente(tt):
    # foto original 37131862, sem a marca do quadro; 4:5 no enquadramento roda + corrente (sem ampliar demais)
    arq = foto_prep('37131862', satura=.6, frio=.12, crop=(560, 0, 1520, 1200) if not tt else (900, 300, 1500, 1200), escurece=1.15, nome='cm05r5_corr' + ('_tt' if tt else ''))
    L, w = (140, 800) if tt else (90, 900)
    c = foto_fundo(arq, pos='50% 50%', degr='escuro_topo', forca=.94, topo=.5)
    c += barra(3, L, TOPO_IND(tt), 520, tt)
    tam = 96 if not tt else 88
    linhas = ['Pegou chuva?', 'Limpe e lubrifique', 'a corrente.']
    ty = 380 if tt else 220
    c += titulo(linhas, L, ty, tam, w=w, azul_de=1, lh=1.0)
    c += apoio(['Antes de rodar de novo.'], L, ty + alt_titulo(3, tam, 1.0) + 26, 36 if not tt else 32, w=w, cor='#F4F7FC')
    return c + pag(4, N, tt)

def visto(tt):
    """Foto 33136700: moto parada na chuva com a luz do farol acesa; placa borrada; texto em cima (cobre o piloto)."""
    arq = foto_prep('33136700', satura=.6, frio=.12, borrar=[(760, 895, 1000, 1010)], crop=(0, 60, 1387, 1794) if not tt else None, nome='cm05r5_visto' + ('_tt' if tt else ''))
    L, w = (140, 800) if tt else (90, 900)
    c = foto_fundo(arq, pos='55% 50%', degr='escuro_topo', forca=.94, topo=.45)
    c += barra(4, L, TOPO_IND(tt), 520, tt)
    ty = 340 if tt else 220
    c += titulo(['Na chuva,', 'você precisa'], L, ty, 96 if not tt else 92, w=w, lh=1.0)
    y2 = ty + alt_titulo(2, 96 if not tt else 92, 1.0)
    c += (f"<div class=titB style='left:{L}px;right:auto;width:{w}px;top:{y2}px;font-size:{140 if not tt else 132}px;text-align:left;letter-spacing:-.035em;line-height:1.0;"
          f"color:{AZUL_CLARO};text-shadow:0 0 40px rgba(82,169,254,.85),0 0 90px rgba(82,169,254,.5)'>ser visto.</div>")
    c += apoio(['Teste farol, lanterna e setas antes de sair.'], L, y2 + (160 if not tt else 150), 36 if not tt else 32, w=w, cor='#F4F7FC')
    return c + pag(5, N, tt)

def tela(tt):
    """R5 (25/11): momento do app próprio da peça: o lembrete chega como notificação (recurso do K6), com o texto REAL
    do app ("Lubrificar quando a moto estiver com 29.900 km", tela 28-item-proximo), por cima do celular com essa tela."""
    L, w = (140, 800) if tt else (90, 900)
    c = fundo(T, (50, 70))
    ty = 330 if tt else 110
    tam = 74 if not tt else 62
    c += titulo(['A corrente não reclama.', 'O app lembra por ela.'], L, ty, tam, w=w, azul_de=1)
    yp = ty + alt_titulo(2, tam) + (300 if tt else 250)
    wf = 600 if tt else 560
    c += fone('ios-1.0/28-item-proximo.png', wf, 540, yp, extra='')
    yn = yp - (150 if tt else 140)
    nt, hn = notificacao('MinhaMoto', 'Lubrificar quando a moto\nestiver com 29.900 km', L - 20, yn, w=w + 40, linhas=2, escala=1.0 if not tt else .95)
    return c + nt + pag(6, N, tt)

def final(tt):
    """R5 (25/11): copy que não promete aviso de chuva (o app avisa manutenção por km) e ícone do app DENTRO do feixe."""
    L, w = (140, 800) if tt else (90, 900)
    c = fundo_chuva(tt, 540, 560, .9, seed=5)
    yi = 420 if tt else 130
    c += (f"<div style='position:absolute;left:50%;top:{yi - 90}px;width:420px;height:420px;margin-left:-210px;border-radius:50%;"
          f"background:radial-gradient(closest-side, rgba(150,200,255,.45), rgba(82,169,254,.12) 60%, rgba(0,0,0,0) 100%)'></div>")
    c += f"<img src='file://{ICON}' style='position:absolute;left:50%;margin-left:-90px;top:{yi}px;width:180px;height:180px;filter:drop-shadow(0 22px 30px rgba(0,0,0,.55))'>"
    tam = 88 if not tt else 64
    ty = yi + 180 + 90
    c += titulo(['Chuva não marca hora.', 'Sua manutenção, sim.'], 0 if not tt else 140, ty, tam, w=1080 if not tt else 800, alinha='center', azul_de=1)
    ya = ty + alt_titulo(2, tam) + 34
    c += apoio(['O MinhaMoto lembra no km certo.'], 0 if not tt else 140, ya, 42 if not tt else 40, w=1080 if not tt else 800, alinha='center', cor='#F4F7FC', peso='j600')
    c += f"<div style='position:absolute;left:0;right:0;text-align:center;top:{ya + 110}px'><span class=preco><i></i>por R$19,90</span></div>"
    c += f"<div style='position:absolute;left:0;right:0;text-align:center;top:{1380 if tt else 1190}px'><img src='file://{SELOS}' style='width:540px'></div>"
    return c

def lista(tt):
    return [(T, capa(tt)), (T, pneu(tt)), (T, freio(tt)), (T, corrente(tt)), (T, visto(tt)), (T, tela(tt)), (T, final(tt))]

if __name__ == '__main__':
    ok = render_lista(NOME, lista(False), lista(True))
    folha(NOME, 'CM05 · chuva (refeito)')
    sys.exit(0 if ok else 1)
