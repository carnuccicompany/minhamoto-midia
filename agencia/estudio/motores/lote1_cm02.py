#!/usr/bin/env python3
"""LOTE1 · CM02 (refeito 24/11 após revisão) · "Esquentar a moto por 5 minutos não protege o motor."
Tipo: mito × verdade · Público: hobby / fim de semana · Tom: mecânico parceiro · Ângulo: orgulho / cuidado com a moto
Estética: claro limpo · Capa: opinião forte, "5:00" gigante riscado, tudo centralizado · Final: salve e mande (eco do 5:00).
Revisão: sem ícones; 4 mitos com 4 composições (claro / bloco navy / painel azul / fundo azul = "o maior mito");
mitos reescritos (nada de espantalho), o maior mito entregue no card 5; card do app = linha real "Óleo do motor"
da 10-lista-revisao ampliada + celular sem sobreposição.
Fontes: AutoPapo 18/09/2026 · CNN Brasil 25/09/2026 (ver pecas/LOTE1/CM02/fontes.md).
Uso: python3 agencia/estudio/motores/lote1_cm02.py
"""
import sys, os, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lote1_base import *

NOME, N, T = 'CM02', 7, 'claro'
AP, CNN = 'Fonte: AutoPapo, 18/09/2026', 'Fonte: CNN Brasil, 25/09/2026'

def riscado(linhas, left, top, tam, w, cor, risco, alinha='left'):
    """Frase do mito com risco por cima (linha a linha)."""
    txt = '<br>'.join(f"<span style='text-decoration:line-through;text-decoration-thickness:.075em;text-decoration-color:{risco}'>{H.escape(l)}</span>" for l in linhas)
    return (f"<div class=titB style='left:{left}px;right:auto;width:{w}px;top:{top}px;font-size:{tam}px;text-align:{alinha};font-family:j700;"
            f"letter-spacing:-.02em;line-height:1.12;color:{cor};text-shadow:none'>{txt}</div>")

def verdade(linhas, left, top, tam, w, cor, alinha='left', azul_ult=None):
    out = []
    for i, l in enumerate(linhas):
        e = H.escape(l)
        out.append(f"<span style='color:{azul_ult}'>{e}</span>" if (azul_ult and i == len(linhas) - 1) else e)
    return (f"<div class=titB style='left:{left}px;right:auto;width:{w}px;top:{top}px;font-size:{tam}px;text-align:{alinha};font-family:j700;"
            f"letter-spacing:-.02em;line-height:1.16;color:{cor};text-shadow:none'>{'<br>'.join(out)}</div>")

def cinco(cx, top, tam, cor=NAVY_TXT, risco=AZUL, esp=None, txt='5:00', sombra=False):
    """'5:00' gigante com um traço azul cortando na diagonal. R5: sombra escura opcional (legível sobre foto clara)."""
    w = round(tam * (2.15 if len(txt) <= 4 else 2.7)); esp = esp or round(tam * .12)
    sh = "text-shadow:0 6px 30px rgba(1,7,17,.55),0 2px 8px rgba(1,7,17,.45);" if sombra else ''
    return (f"<div style='position:absolute;left:{cx - w//2}px;top:{top}px;width:{w}px;text-align:center;font-family:j800;font-size:{tam}px;"
            f"color:{cor};letter-spacing:-.04em;line-height:1;{sh}'>{txt}</div>"
            f"<div style='position:absolute;left:{cx - round(w*.55)}px;top:{top + round(tam*.48)}px;width:{round(w*1.1)}px;height:{esp}px;border-radius:{esp}px;"
            f"background:{risco};transform:rotate(-14deg);box-shadow:0 10px 30px rgba(40,122,245,.35)'></div>")

def capa(tt):
    """Foto real (10103321, Pexels): guidão e tanque azul ao sol; marca do tanque e do velocímetro borradas.
    '5:00' riscado em branco sobre a foto; título no claro embaixo."""
    L, w = (140, 800) if tt else (90, 900)
    borr = [('disco', 529, 381, 64, 58), (550, 820, 700, 1000)]
    arq = foto_prep('10103321', crop=(330, 0, 1230, 1000) if not tt else (430, 0, 1060, 1000), borrar=borr, nome='cm02_capa' + ('_tt' if tt else ''))
    hf = 1000 if tt else 800
    c = fundo(T, (50, 80))
    c += (f"<div style=\"position:absolute;left:0;top:0;width:1080px;height:{hf}px;background:url('file://{arq}') 50% 40%/cover\"></div>"
          f"<div style='position:absolute;left:0;top:0;width:1080px;height:{hf}px;background:linear-gradient(180deg,rgba(1,7,17,.25) 0%,rgba(1,7,17,0) 30%,rgba(244,247,252,0) 72%,#F4F7FC 100%)'></div>")
    if not tt:
        c += kicker('Mito de garagem', L, 110, 'escuro', w=w)
    c += cinco(540, (hf - 500) if tt else (hf - 420), 300 if tt else 260, cor='#FFFFFF', risco=AZUL, sombra=True)
    ty = hf - (10 if tt else 30)
    tam = 82 if not tt else 74
    c += titulo(['Esquentar a moto', 'por 5 minutos', 'não protege o motor.'], L, ty, tam, w=w, alinha='center', azul_de=2)
    c += apoio(['E esse nem é o maior mito da garagem.'], L, ty + alt_titulo(3, tam) + 24, 38, w=w, alinha='center')
    c += desliza(0, 1265 if not tt else 1420, tt, alinha='center').replace("left:0px;right:auto", "left:0;right:0")
    return c

def real(titulo_l, apo, L, top, tam, w, cor_t, cor_a, pil_bg, pil_fg, tt):
    c = pilula('A real', pil_bg, pil_fg, L, top, tam=30, icone_nome='ok')
    c += (f"<div class=titB style='left:{L}px;right:auto;width:{w}px;top:{top + 90}px;font-size:{tam}px;text-align:left;letter-spacing:-.035em;"
          f"line-height:1.04;color:{cor_t};text-shadow:none'>{'<br>'.join(H.escape(x) for x in titulo_l)}</div>")
    c += apoio([apo] if isinstance(apo, str) else apo, L, top + 90 + round(len(titulo_l) * tam * 1.04) + 30, 38 if not tt else 36, w=w, cor=cor_a)
    return c

def m1(tt):   # claro, texto em cima
    L, w = (140, 800) if tt else (90, 900)
    tm, tv = (64, 112) if tt else (66, 120)
    c = fundo(T, (85, 12))
    y = 400 if tt else 200
    c += pilula('Mito nº 1', NAVY_TXT, '#FFFFFF', L, y, tam=30, icone_nome='x')
    c += riscado(['Moto fria tem que', 'esquentar parada.'], L, y + 90, tm, w, 'rgba(10,26,51,.45)', AZUL)
    yv = y + 90 + round(2 * tm * 1.12) + 110
    c += bloco_icone('relogio', 1080 - (140 if tt else 90) - (220 if tt else 260), yv + 90, lado=220 if tt else 260)
    c += real(['Segundos', 'bastam.'], ['Parada por minutos, a moto a ar', 'esquenta demais.'], L, yv, tv, w, AZUL_ESC, '#45536B', AZUL, '#FFFFFF', tt)
    c += apoio([AP], L, 1200 if not tt else 1420, 24, w=600, cor='rgba(10,26,51,.45)')
    return c + pag(2, N, tt)

def m2(tt):   # bloco navy em cima (mito) + verdade no claro
    L, w = (140, 800) if tt else (90, 900)
    tm, tv = (64, 112) if tt else (66, 120)
    hb = 860 if tt else 560
    c = fundo(T, (50, 80))
    c += f"<div style='position:absolute;left:0;top:0;width:1080px;height:{hb}px;background:linear-gradient(160deg,#0B1B36,#020812)'></div>"
    c += f"<div style='position:absolute;left:0;top:0;width:1080px;height:{hb}px;background:radial-gradient(50% 60% at 80% 30%, rgba(82,169,254,.25), rgba(0,0,0,0) 70%)'></div>"
    y = 460 if tt else 230
    c += pilula('Mito nº 2', 'rgba(255,255,255,.12)', '#FFFFFF', L, y, tam=30, icone_nome='x')
    c += riscado(['Barulho estranho', 'some sozinho.'], L, y + 100, tm, w, 'rgba(255,255,255,.7)', AZUL_CLARO)
    yv = hb + 70
    c += bloco_icone('som', 1080 - (140 if tt else 90) - 200, yv + 90 + 2*round(tv*1.04) + 40, lado=200)
    c += real(['Não some.', 'Piora.'], ['Estalo, vibração e ruído metálico', 'raramente desaparecem sozinhos.'], L, yv, tv, w, NAVY_TXT, '#45536B', AZUL, '#FFFFFF', tt)
    c += apoio([CNN], L, 1240 if not tt else 1440, 24, w=600, cor='rgba(10,26,51,.45)')
    return c + pag(3, N, tt).replace("class='pag t'", "class='pag t' style='color:rgba(255,255,255,.55)'")

def m3(tt):   # mito no claro + verdade num painel azul
    L, w = (140, 800) if tt else (90, 900)
    tm, tv = (64, 86) if tt else (66, 100)
    c = fundo(T, (15, 15))
    y = 400 if tt else 200
    c += pilula('Mito nº 3', NAVY_TXT, '#FFFFFF', L, y, tam=30, icone_nome='x')
    c += riscado(['Óleo é tudo igual,', 'qualquer um serve.'], L, y + 90, tm, w, 'rgba(10,26,51,.45)', AZUL)
    yp = y + 90 + round(2 * tm * 1.12) + 70
    hp = 500 if not tt else 520
    c += (f"<div style='position:absolute;left:{L - 10}px;top:{yp}px;width:{w + 20}px;height:{hp}px;border-radius:48px;"
          f"background:linear-gradient(140deg,{AZUL},{AZUL_ESC});box-shadow:0 40px 80px rgba(0,95,222,.30)'></div>")
    c += real(['Vale o que', 'o manual pede.'], 'Viscosidade e norma certas, sempre.', L + 40, yp + 50, tv, w - 80, '#FFFFFF', 'rgba(255,255,255,.85)', 'rgba(255,255,255,.18)', '#FFFFFF', tt)
    c += apoio([CNN], L, 1200 if not tt else 1420, 24, w=600, cor='rgba(10,26,51,.45)')
    return c + pag(4, N, tt)

def m4(tt):   # fundo azul: o maior mito
    L, w = (140, 800) if tt else (90, 900)
    tm, tv = (64, 104) if tt else (66, 112)
    c = (f"<div class=fill style='background:linear-gradient(160deg,{AZUL} 0%,{AZUL_ESC} 60%,#0042A8 100%)'></div>"
         "<div class=fill style='background:radial-gradient(60% 40% at 85% 10%, rgba(255,255,255,.18), rgba(255,255,255,0) 70%)'></div>")
    y = 400 if tt else 200
    c += kicker('O maior mito de todos', L, y, 'escuro', w=w, tam=34)
    c += riscado(['Trocou o óleo,', 'o motor tá protegido.'], L, y + 80, tm, w, 'rgba(255,255,255,.72)', '#FFFFFF')
    yv = y + 80 + round(2 * tm * 1.12) + 90
    c += bloco_icone('filtro', 1080 - (140 if tt else 90) - (240 if tt else 280), (yv + 90 + 2*round(tv*1.04) + 150), lado=240 if tt else 280, tema='escuro', cor='#FFFFFF')
    c += real(['O vilão é o filtro', 'de ar sujo.'], 'A sujeira passa e contamina o óleo novo.', L, yv, tv, w, '#FFFFFF', 'rgba(255,255,255,.85)', '#FFFFFF', AZUL_ESC, tt)
    c += apoio([AP], L, 1200 if not tt else 1420, 24, w=600, cor='rgba(255,255,255,.6)')
    return c + pag(5, N, tt).replace("class='pag t'", "class='pag t' style='color:rgba(255,255,255,.6)'")

def tela(tt):
    arq, size = recorte('ios-1.0/rolagem/10-lista-revisao.png', (48, 1530, 1131, 1785))
    L, w = (140, 800) if tt else (90, 900)
    c = fundo(T, (50, 70))
    ty = 260 if tt else 110
    tam = 80 if not tt else 72
    c += titulo(['O óleo certo da', 'sua moto já tá no app.'], L, ty, tam, w=w, azul_de=1)
    yc = ty + alt_titulo(2, tam) + (70 if tt else 50)
    bloco, hc = card_solto(arq, size, w, L, yc, claro=True)
    c += bloco
    c += fone('ios-1.0/rolagem/10-lista-revisao', 640 if tt else 560, 540, yc + hc + 70, rola=1197)
    return c + pag(6, N, tt)

def final(tt):
    L, w = (140, 800) if tt else (90, 900)
    c = fundo(T, (50, 30))
    c += cinco(540, 320 if tt else 190, 260 if tt else 220, cor='rgba(10,26,51,.16)', risco=AZUL, txt='10:00')
    c += (f"<div style='position:absolute;left:0;right:0;top:{700 if tt else 540}px;text-align:center'><span style='display:inline-block;font-family:j700;font-size:36px;color:#fff;"
          f"background:{AZUL};padding:14px 34px;border-radius:999px;box-shadow:0 14px 30px rgba(40,122,245,.35)'>Salve este post</span></div>")
    tam = 80 if not tt else 72
    ty = 790 if tt else 630
    c += titulo(['Mande pro amigo', 'que esquenta a moto', 'por 10 minutos.'], L, ty, tam, w=w, alinha='center', azul_de=2)
    c += apoio(['Ele vai agradecer no próximo domingo.'], L, ty + alt_titulo(3, tam) + 30, 40, w=w, alinha='center')
    c += assinatura(1250 if tt else 1110, T)
    return c

def lista(tt):
    return [(T, capa(tt)), (T, m1(tt)), (T, m2(tt)), (T, m3(tt)), ('escuro', m4(tt)), (T, tela(tt)), (T, final(tt))]

if __name__ == '__main__':
    ok = render_lista(NOME, lista(False), lista(True))
    folha(NOME, 'CM02 · mitos (refeito)')
    sys.exit(0 if ok else 1)
