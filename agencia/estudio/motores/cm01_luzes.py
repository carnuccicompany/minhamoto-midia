#!/usr/bin/env python3
"""CM01 · Carrossel-modelo da lapidação — rodada 2 (23/11).
Tema: luzes do painel ("4 luzes no painel. Duas mandam parar na hora.").
Régua: agencia/DESIGN-MINHAMOTO.md (seção 23/11). Rodada 2 aplica: copy nova, mockup em posições diferentes
(saindo do quadro), card do app só às vezes e com a parte que importa acesa, trecho puxado pra fora do celular,
ícone final sem halo quadrado, títulos alinhados à esquerda com hierarquia mais forte.
Uso: python3 agencia/estudio/motores/cm01_luzes.py [45|tiktok]
"""
import os, sys, html as H
AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(AQUI, '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'agencia', 'direcao-v2'))
sys.path.insert(0, AQUI)
from estaticos import grad_bg, celular, ICON, SELOS
from recortes_app import trecho, destaque, cards
from render_check import render

SAIDA = os.path.join(REPO, 'agencia', 'estudio', 'pecas', 'CM01')
SIN = 'ios-1.0/rolagem/12-sinais-problema.png'   # telas do iPhone (iOS 1.0 build 33), regra 24/11
OLEO, TEMP, INJ, BAT = 9, 10, 11, 13          # índices dos cards na tela Sinais de problema
N = 7
_, RUNS = cards(SIN)

def rola_em(idx, y_tela=430):
    """Valor de rola que deixa o card idx começando em y_tela (px da tela 1179x2556), logo abaixo do cabeçalho fixo."""
    return RUNS[idx][0] - y_tela + 177

def fone(nome, w, cx, top, rot=0, tilt=0, rola=None):
    """Mesmo mockup do motor (estaticos.celular), com posição horizontal livre (pode sair do quadro)."""
    return celular(nome, w=w, top=top, rot=rot, tilt=tilt, rola=rola).replace("<div class=ph style='top:", f"<div class=ph style='left:{cx}px;top:", 1)

SOMBRA = "box-shadow:0 0 0 2px rgba(255,255,255,.08),0 40px 80px rgba(0,0,0,.7),0 14px 28px rgba(0,0,0,.5),0 0 90px rgba(82,169,254,.25)"

def imagem_card(arq, sw, sh, w, left, top, extra=''):
    h = round(sh * w / sw); r = round(48 * w / sw)
    return (f"<div class=uicard style='position:absolute;left:{left}px;top:{top}px;width:{w}px;height:{h}px;border-radius:{r}px;overflow:hidden;{SOMBRA};{extra}'>"
            f"<img src='file://{arq}' style='display:block;width:100%;height:100%'></div>"), h

def puxado(idx, w, left, top):
    """Cabeçalho + 'O que fazer' do card do app, puxado pra fora do celular e ampliado."""
    arq, (sw, sh) = trecho(SIN, idx, (0, 2))
    return imagem_card(arq, sw, sh, w, left, top)[0]

# ---------- texto ----------
def kicker(txt, left, top, tam=30, w=900):
    return (f"<div class=apoB style='left:{left}px;right:auto;width:{w}px;top:{top}px;text-align:left;font-family:j600;font-size:{tam}px;"
            f"color:rgba(255,255,255,.72);letter-spacing:.01em'><span style='display:inline-block;width:14px;height:14px;border-radius:50%;"
            f"background:#C6FF00;box-shadow:0 0 14px rgba(198,255,0,.6);margin-right:14px;vertical-align:2px'></span>{H.escape(txt)}</div>")

def titulo(linhas, left, top, tam, w=900, alinha='left', azul_de=1):
    """linhas: lista; a partir de azul_de, em azul claro."""
    partes = [H.escape(l) if i < azul_de else f"<span class=b>{H.escape(l)}</span>" for i, l in enumerate(linhas)]
    return (f"<div class=titB style='left:{left}px;right:auto;width:{w}px;top:{top}px;font-size:{tam}px;text-align:{alinha};"
            f"letter-spacing:-.035em;line-height:1.04'>{'<br>'.join(partes)}</div>")

def apoio(linhas, left, top, tam, w=900, alinha='left'):
    return (f"<div class=apoB style='left:{left}px;right:auto;width:{w}px;top:{top}px;font-size:{tam}px;text-align:{alinha};"
            f"line-height:1.32;color:#c9d6ea'>{'<br>'.join(H.escape(l) for l in linhas)}</div>")

def pag(n, tt):
    return '' if tt else f"<div class='pag t'>{n:02d} / {N:02d}</div>"

# ---------- cards ----------
def capa(tt):
    if tt:
        L, T, tam = 140, 230, 84
        c = grad_bg('B', (70, 70)) + titulo(['4 luzes no painel.', 'Duas mandam', 'parar na hora.'], L, T, tam, w=800)
        c += apoio(['Você sabe quais?'], L, T + 3*88 + 40, 42, w=800)
        c += fone('12-sinais-problema', 620, 760, 760)
        c += f"<div class=desliza style='left:{L}px;right:auto;bottom:auto;top:1400px;text-align:left'>Deslize <b>→</b></div>"
        return c
    L, T, tam = 90, 104, 90
    c = grad_bg('B', (72, 72)) + titulo(['4 luzes no painel.', 'Duas mandam', 'parar na hora.'], L, T, tam)
    c += apoio(['Você sabe quais?'], L, T + 3*94 + 34, 42)
    c += fone('12-sinais-problema', 600, 770, 560)
    c += f"<div class=desliza style='left:{L}px;right:auto;bottom:70px;text-align:left'>Deslize <b>→</b></div>"
    return c

def com_puxado(n, idx, kick, tit, apo, lado, tt):
    """Texto em cima; celular embaixo saindo do quadro de um lado; trecho do card puxado pro outro lado."""
    if tt:
        L, w, T, tam, ta = 140, 800, 200, 66, 32
        ph_top, ph_w, call_w, call_top = 720, 560, 620, 1010
        cx = 300 if lado == 'esq' else 780
        call_left = 320 if lado == 'esq' else 140   # trecho dentro da zona segura 9:16 (x 140–940)
    else:
        L, w, T, tam, ta = 90, 900, 96, 74, 34
        ph_top, ph_w, call_w, call_top = 500, 540, 620, 780
        cx = 290 if lado == 'esq' else 790
        call_left = 410 if lado == 'esq' else 50
    c = grad_bg('B', (30 if lado == 'esq' else 70, 75))
    c += kicker(kick, L, T, w=w)
    c += titulo(tit, L, T + 52, tam, w=w)
    c += apoio(apo, L, T + 52 + 2*round(tam*1.04) + 28, ta, w=w)
    # celular levemente apagado: o olho vai pro trecho puxado (Apple-style)
    c += fone(SIN, ph_w, cx, ph_top, rola=rola_em(idx, 480)).replace("<div class=ph style='", "<div class=ph style='filter:brightness(.55);", 1)
    c += puxado(idx, call_w, call_left, call_top)
    return c + pag(n, tt)

def card_grande(n, idx, kick, tit, apo, tt):
    """Trecho do card do app (cabeçalho + 'O que fazer') grande, saindo de cima do celular que aparece por baixo (apagado)."""
    arq, (sw, sh) = trecho(SIN, idx, (0, 2))   # 23/11 r2: nada de apagar partes do print
    if tt:
        L, w, T, tam, ta, cw, ph_w, ph_top = 140, 800, 200, 66, 30, 800, 640, 900
    else:
        L, w, T, tam, ta, cw, ph_w, ph_top = 90, 900, 96, 74, 32, 900, 640, 700
    c = grad_bg('B', (50, 70))
    c += kicker(kick, L, T, w=w)
    c += titulo(tit, L, T + 52, tam, w=w)
    y_apo = T + 52 + 2*round(tam*1.04) + 28
    c += apoio(apo, L, y_apo, ta, w=w)
    c += fone(SIN, ph_w, 540, ph_top, rola=rola_em(idx, 600)).replace("<div class=ph style='", "<div class=ph style='filter:brightness(.55);", 1)
    top_card = ph_top - 150 if not tt else ph_top - 170
    bloco, _ = imagem_card(arq, sw, sh, cw, (1080 - cw)//2, top_card)
    return c + bloco + pag(n, tt)

def lateral(n, idx, kick, tit, apo, tt):
    """Celular grande e girado à esquerda, saindo por baixo; texto em coluna à direita."""
    if tt:
        c = grad_bg('B', (28, 60))
        c += fone(SIN, 600, 250, 330, rola=rola_em(idx, 1100))
        x, w = 560, 380
        c += kicker(kick, x, 560, tam=28, w=w)
        c += titulo(tit, x, 610, 58, w=w, azul_de=2)
        c += apoio(apo, x, 610 + len(tit)*61 + 30, 29, w=w)
        return c + pag(n, tt)
    c = grad_bg('B', (28, 60))
    c += fone(SIN, 620, 270, 150, rola=rola_em(idx, 1100))
    x, w = 600, 420
    c += kicker(kick, x, 420, tam=28, w=w)
    c += titulo(tit, x, 470, 62, w=w, azul_de=2)
    c += apoio(apo, x, 470 + len(tit)*65 + 30, 30, w=w)
    return c + pag(n, tt)

def prova(tt):
    y_head = RUNS[3][0] - 150          # título "Comportamentos que indicam problema", logo acima do card 3
    if tt:
        c = grad_bg('B', (50, 70))
        c += titulo(['Luz, barulho, fumaça:', 'o app explica cada um.'], 140, 200, 60, w=800, alinha='center')
        c += apoio(['Com o que fazer e quando ir à oficina.'], 140, 350, 32, w=800, alinha='center')
        c += fone(SIN, 620, 540, 470, rola=y_head - 430 + 177)
        return c
    c = grad_bg('B', (50, 70))
    c += titulo(['Luz, barulho, fumaça:', 'o app explica cada um.'], 90, 92, 70, alinha='center')
    c += apoio(['Com o que fazer e quando ir à oficina.'], 90, 262, 34, alinha='center')
    c += fone(SIN, 600, 540, 360, rola=y_head - 430 + 177)
    return c + pag(6, tt)

def final(tt):
    """CTA: ícone com brilho redondo atrás (sem halo quadrado), título, traço limão, apoio, preço; selos separados embaixo."""
    top, selos, tam = (330, 1330, 74) if tt else (150, 1150, 82)
    glow = (f"<div style='position:absolute;left:50%;top:{top - 150}px;width:560px;height:560px;margin-left:-280px;border-radius:50%;"
            "background:radial-gradient(closest-side, rgba(82,169,254,.42), rgba(40,122,245,.16) 55%, rgba(0,0,0,0) 100%);filter:blur(6px)'></div>")
    ic = f"<img src='file://{ICON}' style='width:200px;height:200px;filter:drop-shadow(0 26px 34px rgba(0,0,0,.55))'>"
    t = (f"<div class=titB style='position:relative;left:0;right:0;font-size:{tam}px;margin-top:52px;letter-spacing:-.035em;line-height:1.04'>"
         "Seu painel avisa.<br><span class=b>O MinhaMoto explica.</span></div><span class=lm></span>")
    s = f"<div class=apoB style='position:relative;left:0;right:0;font-size:{38 if tt else 42}px;margin-top:26px'>Baixe agora e entenda sua moto.</div>"
    pr = "<div style='margin-top:44px'><span class=preco><i></i>por R$19,90</span></div>"
    pad = 140 if tt else 60
    corpo = f"<div style='position:absolute;left:{pad}px;right:{pad}px;top:{top}px;text-align:center'>{ic}{t}{s}{pr}</div>"
    se = f"<div style='position:absolute;left:0;right:0;top:{selos}px;text-align:center'><img src='file://{SELOS}' style='width:540px'></div>"
    return grad_bg('B', (50, 30)) + glow + corpo + se

def lista(tt=False):
    return [
        capa(tt),
        com_puxado(2, OLEO, 'Pare agora', ['Luz do óleo acesa', 'pode virar retífica.'],
                   ['Encoste em local seguro', 'e desligue o motor na hora.'], 'esq', tt),
        card_grande(3, TEMP, 'Pare agora', ['Motor quente', 'não se abre na pressa.'],
                    ['Com o motor quente, o líquido sai sob pressão.', 'Espere esfriar antes de mexer.'], tt),
        com_puxado(4, INJ, 'Atenção', ['Luz da injeção', 'não é sentença.'],
                   ['Dá pra chegar, sem forçar.', 'Depois, scanner pra ler o código.'], 'dir', tt),
        lateral(5, BAT, 'Atenção', ['Luz da', 'bateria?', 'Não desligue', 'na rua.'],
                ['Ela pode não estar', 'carregando. Desligou,', 'pode não ligar mais.'], tt),
        prova(tt),
        final(tt),
    ]

if __name__ == '__main__':
    so = sys.argv[1] if len(sys.argv) > 1 else 'todos'
    ok = True
    if so in ('todos', '45'):
        for i, c in enumerate(lista(False), 1):
            ok &= render(c, 1080, 1350, os.path.join(SAIDA, 'carrossel', f'{i:02d}.jpg'))
    if so in ('todos', 'tiktok'):
        for i, c in enumerate(lista(True), 1):
            ok &= render("<div class=tt>" + c + "</div>", 1080, 1920, os.path.join(SAIDA, 'carrossel-tiktok', f'{i:02d}.jpg'))
    sys.exit(0 if ok else 1)
