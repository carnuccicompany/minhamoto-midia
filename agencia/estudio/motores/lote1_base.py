#!/usr/bin/env python3
"""LOTE 1 (24/11) · base comum dos 5 carrosséis orgânicos do MinhaMoto.
Reaproveita: estaticos.py (celular, grad_bg, ICON, SELOS), recortes_app.py (recortes de card do app),
render_check.py (trava de layout). Régua: agencia/DESIGN-MINHAMOTO.md (★ constituição de 24/11).

Regras que este arquivo garante:
- telas SÓ de telas-app/ios-1.0/ (iPhone 1.0 build 33); o topo fixo também vem de ios-1.0 (o motor antigo pegava da raiz = main);
- dois temas: 'escuro' (navy premium com luz azul) e 'claro' (branco limpo, tinta navy);
- vermelho/âmbar só nos ícones de alerta (luz do painel);
- preço só "por R$19,90" (nunca por mês).
"""
import os, sys, html as H
AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(AQUI, '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'agencia', 'direcao-v2'))
sys.path.insert(0, AQUI)
import estaticos as E
from estaticos import grad_bg, ICON, SELOS
from render_check import render as _render
from PIL import Image

TELAS = os.path.join(REPO, 'agencia', 'designer', 'assets', 'telas-app')
IOS = 'ios-1.0'
CACHE = '/tmp/lote1-cache'
os.makedirs(CACHE, exist_ok=True)
PECAS = os.path.join(REPO, 'agencia', 'estudio', 'pecas', 'LOTE1')

AZUL, AZUL_ESC, AZUL_CLARO, LIMAO = '#287AF5', '#005FDE', '#52A9FE', '#C6FF00'
VERM, AMBAR = '#FF453A', '#FFB020'
NAVY_TXT = '#0A1A33'

# ---------- trava: só telas do iPhone ----------
def _so_ios(nome):
    if not nome.startswith(IOS + '/'):
        raise ValueError(f'tela fora de {IOS}/: {nome} (regra 24/11: só telas do iPhone)')
    return nome

def _topo_ios(nome):
    """Topo fixo (status + cabeçalho) tirado da tela PARADA do iPhone (ios-1.0/<nome>.png)."""
    base = os.path.basename(nome).replace('.png', '')
    src = os.path.join(TELAS, IOS, base + '.png')
    out = os.path.join(CACHE, f'topo_ios_{base}.png')
    if not os.path.exists(out):
        Image.open(src).crop((0, 0, 1179, 360)).save(out)
    return out
E.topo_fixo = _topo_ios   # celular() usa o nome global do módulo estaticos

def fone(nome, w, cx, top, rola=None, extra=''):
    """Mesmo mockup do motor (estaticos.celular), reto, com centro horizontal livre (pode sair do quadro)."""
    _so_ios(nome)
    h = E.celular(nome, w=w, top=top, rola=rola)
    return h.replace("<div class=ph style='top:", f"<div class=ph style='{extra}left:{cx}px;top:", 1)

def altura_fone(w):
    return E.altura_celular(w)

SOMBRA_ESC = "box-shadow:0 0 0 2px rgba(255,255,255,.10),0 40px 80px rgba(0,0,0,.7),0 14px 28px rgba(0,0,0,.5),0 0 90px rgba(82,169,254,.28)"
SOMBRA_CLA = "box-shadow:0 0 0 2px rgba(255,255,255,.10),0 40px 80px rgba(10,26,51,.35),0 14px 28px rgba(10,26,51,.25)"

def recorte(nome, box):
    """Recorta um trecho de uma tela do iPhone (box em px da imagem 1179 de largura)."""
    _so_ios(nome)
    arq = os.path.join(TELAS, nome if nome.endswith('.png') else nome + '.png')
    out = os.path.join(CACHE, os.path.basename(arq)[:-4] + '_%d_%d_%d_%d.png' % box)
    im = Image.open(arq).convert('RGB').crop(box); im.save(out)
    return out, im.size

def card_solto(arq, size, w, left, top, claro=False, rot=0):
    """Card do app 'solto', flutuando (com borda arredondada e sombra)."""
    sw, sh = size; h = round(sh * w / sw); r = round(46 * w / sw)
    sombra = SOMBRA_CLA if claro else SOMBRA_ESC
    tr = f"transform:rotate({rot}deg);" if rot else ''
    return (f"<div class=uicard style='position:absolute;left:{left}px;top:{top}px;width:{w}px;height:{h}px;border-radius:{r}px;overflow:hidden;{sombra};{tr}'>"
            f"<img src='file://{arq}' style='display:block;width:100%;height:100%'></div>"), h

# ---------- fundos ----------
CSS_CLARO = ("<style>.claro .titB{color:%s;text-shadow:none}.claro .titB .b{color:%s}.claro .apoB{color:#45536B}"
             ".claro .pag{color:rgba(10,26,51,.45)}.claro .desliza{color:%s;text-shadow:none}.claro .desliza b{color:%s}</style>") % (NAVY_TXT, AZUL_ESC, NAVY_TXT, AZUL)

def fundo(tema, luz=(50, 60)):
    if tema == 'escuro':
        return grad_bg('B', luz)
    return (CSS_CLARO +
            "<div class=fill style='background:linear-gradient(180deg,#FFFFFF 0%,#F4F7FC 60%,#E9F0FA 100%)'></div>"
            f"<div class=fill style='background:radial-gradient(48% 30% at {luz[0]}% {luz[1]}%, rgba(40,122,245,.16), rgba(40,122,245,0) 70%)'></div>")

def wrap(tema, corpo):
    return f"<div class='fill {'claro' if tema == 'claro' else ''}'>{corpo}</div>"

# ---------- texto ----------
def kicker(txt, left, top, tema='escuro', cor=None, tam=30, w=900, alinha='left'):
    cor = cor or (LIMAO if tema == 'escuro' else AZUL)
    txtcor = 'rgba(255,255,255,.75)' if tema == 'escuro' else 'rgba(10,26,51,.62)'
    glow = f"box-shadow:0 0 14px {cor}99;" if tema == 'escuro' else ''
    return (f"<div class=apoB style='left:{left}px;right:auto;width:{w}px;top:{top}px;text-align:{alinha};font-family:j600;font-size:{tam}px;"
            f"color:{txtcor};letter-spacing:.01em'><span style='display:inline-block;width:14px;height:14px;border-radius:50%;"
            f"background:{cor};{glow}margin-right:14px;vertical-align:2px'></span>{H.escape(txt)}</div>")

def titulo(linhas, left, top, tam, w=900, alinha='left', azul_de=None, lh=1.06):
    """linhas: lista (cada uma = 1 linha). azul_de: índice a partir do qual a linha fica em azul. Linha pode ter <b>…</b> = azul inline."""
    out = []
    for i, l in enumerate(linhas):
        t = H.escape(l).replace('&lt;b&gt;', "<span class=b>").replace('&lt;/b&gt;', '</span>')
        out.append(f"<span class=b>{t}</span>" if (azul_de is not None and i >= azul_de) else t)
    return (f"<div class=titB style='left:{left}px;right:auto;width:{w}px;top:{top}px;font-size:{tam}px;text-align:{alinha};"
            f"letter-spacing:-.035em;line-height:{lh}'>{'<br>'.join(out)}</div>")

def apoio(linhas, left, top, tam, w=900, alinha='left', cor=None, peso='j500'):
    c = f"color:{cor};" if cor else ''
    return (f"<div class=apoB style='left:{left}px;right:auto;width:{w}px;top:{top}px;font-size:{tam}px;text-align:{alinha};font-family:{peso};"
            f"line-height:1.34;{c}'>{'<br>'.join(H.escape(l) for l in linhas)}</div>")

def alt_titulo(n, tam, lh=1.06):
    return round(n * tam * lh)

def pag(n, total, tt):
    return '' if tt else f"<div class='pag t'>{n:02d} / {total:02d}</div>"

def desliza(left, top, tt, alinha='left'):
    return f"<div class=desliza style='left:{left}px;right:auto;bottom:auto;top:{top}px;text-align:{alinha}'>Deslize <b>→</b></div>"

def assinatura(top, tema, left=None, tt=False):
    """Selo pequeno da marca no rodapé (ícone + MinhaMoto)."""
    cor = '#F4F7FC' if tema == 'escuro' else NAVY_TXT
    pos = f"left:{left}px" if left is not None else "left:0;right:0;text-align:center"
    return (f"<div style='position:absolute;{pos};top:{top}px;font-family:j700;font-size:30px;color:{cor};letter-spacing:-.01em'>"
            f"<img src='file://{ICON}' style='width:54px;height:54px;border-radius:13px;vertical-align:middle;margin-right:14px'>MinhaMoto</div>")

# ---------- ícones (SVG desenhado aqui; nada de marca de terceiros) ----------
def svg(paths, tam, cor, sw=6):
    return (f"<svg width='{tam}' height='{tam}' viewBox='0 0 100 100' fill='none' stroke='{cor}' stroke-width='{sw}' "
            f"stroke-linecap='round' stroke-linejoin='round'>{paths}</svg>")

IC = {
    # luz de pressão do óleo (almotolia com gota)
    'oleo': "<path d='M14 46 h16 l6 -7 h22 l5 7 l22 -9 l-3 6 l-19 20 v9 h-49 z'/><path d='M30 46 v-6 M16 46 v26'/><path d='M89 50 c0 0 -5 7 -5 10 a5 5 0 0 0 10 0 c0 -3 -5 -10 -5 -10z' fill='currentColor'/>",
    # luz de temperatura (termômetro sobre ondas)
    'temp': "<path d='M50 14 v40'/><circle cx='50' cy='62' r='9'/><path d='M50 22 h12 M50 32 h9 M50 42 h12'/><path d='M14 80 q9 -7 18 0 t18 0 t18 0 t18 0'/>",
    # luz da injeção / motor
    'motor': "<path d='M22 40 h10 v-8 h22 v8 h12 l8 8 h8 v-6 h6 v26 h-6 v-6 h-8 l-6 10 h-34 l-6 -8 h-6 v8 h-6 v-26 h6 v8 h6 z'/><path d='M36 32 v-6 h16 v6'/>",
    # luz da bateria
    'bateria': "<rect x='12' y='30' width='76' height='48' rx='6'/><path d='M24 30 v-8 h12 v8 M64 30 v-8 h12 v8'/><path d='M26 54 h14 M33 47 v14 M60 54 h14'/>",
    # pneu (chuva)
    'pneu': "<circle cx='50' cy='50' r='36'/><circle cx='50' cy='50' r='16'/><path d='M50 14 v10 M50 76 v10 M14 50 h10 M76 50 h10 M24.5 24.5 l7 7 M68.5 68.5 l7 7 M24.5 75.5 l7 -7 M68.5 31.5 l7 -7'/>",
    # disco de freio
    'freio': "<circle cx='50' cy='50' r='36'/><circle cx='50' cy='50' r='10'/><circle cx='50' cy='27' r='3' fill='currentColor'/><circle cx='73' cy='50' r='3' fill='currentColor'/><circle cx='50' cy='73' r='3' fill='currentColor'/><circle cx='27' cy='50' r='3' fill='currentColor'/><path d='M70 16 a40 40 0 0 1 16 22' />",
    # corrente (elos)
    'corrente': "<rect x='8' y='36' width='34' height='28' rx='14'/><rect x='33' y='36' width='34' height='28' rx='14'/><rect x='58' y='36' width='34' height='28' rx='14'/><circle cx='25' cy='50' r='3' fill='currentColor'/><circle cx='50' cy='50' r='3' fill='currentColor'/><circle cx='75' cy='50' r='3' fill='currentColor'/>",
    # farol (luz)
    'farol': "<path d='M44 24 c-20 0 -30 12 -30 26 s10 26 30 26 z'/><path d='M58 32 h28 M58 50 h28 M58 68 h28'/>",
    # gota de chuva
    'gota': "<path d='M50 12 c0 0 -26 32 -26 50 a26 26 0 0 0 52 0 c0 -18 -26 -50 -26 -50z'/>",
    'x': "<path d='M30 30 L70 70 M70 30 L30 70'/>",
    # cronômetro
    'relogio': "<circle cx='50' cy='56' r='32'/><path d='M50 56 V38 M42 12 h16 M50 12 v12 M76 28 l6 -6'/>",
    # filtro de ar (elemento pregueado)
    'filtro': "<rect x='16' y='30' width='68' height='52' rx='8'/><path d='M30 38 v36 M42 38 v36 M54 38 v36 M66 38 v36'/><circle cx='26' cy='16' r='3' fill='currentColor'/><circle cx='44' cy='12' r='3' fill='currentColor'/><circle cx='62' cy='18' r='3' fill='currentColor'/><circle cx='78' cy='10' r='3' fill='currentColor'/>",
    # barulho (ondas)
    'som': "<path d='M14 40 h14 l18 -16 v52 l-18 -16 h-14 z'/><path d='M60 36 q8 14 0 28 M70 26 q16 24 0 48 M80 16 q24 34 0 68'/>",
    # manual (livro)
    'manual': "<path d='M50 24 c-10 -6 -24 -8 -36 -6 v60 c12 -2 26 0 36 6 c10 -6 24 -8 36 -6 v-60 c-12 -2 -26 0 -36 6 z'/><path d='M50 24 v60'/>",
    'ok': "<path d='M26 52 L43 68 L75 32'/>",
    'salvar': "<path d='M28 14 h44 v74 l-22 -16 l-22 16 z'/>",
    'enviar': "<path d='M88 14 L12 46 l32 10 l10 32 z'/><path d='M44 56 L88 14'/>",
    'aspas': "<path d='M20 62 c0 -16 6 -26 18 -30 M20 62 a10 10 0 1 0 20 0 a10 10 0 1 0 -20 0 M56 62 c0 -16 6 -26 18 -30 M56 62 a10 10 0 1 0 20 0 a10 10 0 1 0 -20 0'/>",
}

def icone(nome, tam, cor, sw=6):
    return svg(IC[nome].replace('currentColor', cor), tam, cor, sw)

def luz_painel(nome, tam, cor, left, top, aceso=True, raio=None):
    """Ícone dentro de uma 'janela' de painel escura, aceso com brilho da cor (luz de aviso)."""
    caixa = round(tam * 1.55); raio = raio if raio is not None else round(caixa * .28)
    glow = (f"<div style='position:absolute;left:{left + caixa//2 - caixa}px;top:{top + caixa//2 - caixa}px;width:{caixa*2}px;height:{caixa*2}px;"
            f"border-radius:50%;background:radial-gradient(closest-side,{cor}55,{cor}1A 55%,rgba(0,0,0,0) 100%)'></div>") if aceso else ''
    filt = f"filter:drop-shadow(0 0 {tam//10}px {cor}) drop-shadow(0 0 {tam//4}px {cor}88);" if aceso else 'opacity:.9;'
    return (glow + f"<div style='position:absolute;left:{left}px;top:{top}px;width:{caixa}px;height:{caixa}px;border-radius:{raio}px;"
            f"background:linear-gradient(160deg,#121a2a,#05080f);box-shadow:inset 0 0 0 2px rgba(255,255,255,.07),0 30px 60px rgba(0,0,0,.55);"
            f"display:flex;align-items:center;justify-content:center'><div style='{filt}line-height:0'>{icone(nome, tam, cor)}</div></div>")

def bloco_icone(nome, left, top, lado=300, tema='claro', cor=None):
    """Ícone grande num bloco arredondado (grafismo de apoio do card)."""
    cor = cor or (AZUL if tema == 'claro' else AZUL_CLARO)
    fundo_b = ("background:#FFFFFF;box-shadow:0 0 0 2px rgba(10,26,51,.05),0 40px 80px rgba(10,26,51,.14),0 10px 24px rgba(10,26,51,.08)"
               if tema == 'claro' else "background:linear-gradient(160deg,#121a2a,#05080f);box-shadow:inset 0 0 0 2px rgba(255,255,255,.07),0 30px 60px rgba(0,0,0,.55)")
    return (f"<div style='position:absolute;left:{left}px;top:{top}px;width:{lado}px;height:{lado}px;border-radius:{round(lado*.27)}px;{fundo_b};"
            f"display:flex;align-items:center;justify-content:center'>{icone(nome, round(lado*.58), cor, 5)}</div>")

def pilula(txt, cor_fundo, cor_txt, left, top, tam=30, icone_nome=None):
    ic = f"<span style='display:inline-block;vertical-align:-6px;margin-right:12px;line-height:0'>{icone(icone_nome, round(tam*1.1), cor_txt, 9)}</span>" if icone_nome else ''
    return (f"<div class=apoB style='left:{left}px;right:auto;width:auto;top:{top}px;text-align:left;font-family:j700;font-size:{tam}px;color:{cor_txt};"
            f"background:{cor_fundo};padding:{round(tam*.42)}px {round(tam*.9)}px;border-radius:999px;letter-spacing:-.005em;line-height:1.2'>{ic}{H.escape(txt)}</div>")

def arco_gauge(cx, cy, r, tema='escuro', opac=.16):
    """Grafismo de fundo: arco de velocímetro com traços (sai do quadro)."""
    import math
    cor = '255,255,255' if tema == 'escuro' else '10,26,51'
    tr = []
    for i in range(0, 41):
        a = math.radians(150 + i * 6)
        r1 = r - (34 if i % 5 == 0 else 18)
        tr.append(f"<line x1='{cx + r*math.cos(a):.1f}' y1='{cy + r*math.sin(a):.1f}' x2='{cx + r1*math.cos(a):.1f}' y2='{cy + r1*math.sin(a):.1f}' "
                  f"stroke='rgba({cor},{opac if i % 5 else opac*1.8})' stroke-width='{5 if i % 5 == 0 else 3}' stroke-linecap='round'/>")
    return f"<svg class=fill width='100%' height='100%' style='position:absolute;inset:0'>{''.join(tr)}</svg>"


# ---------- R5 (25/11): elementos aprovados no K6 (referência de motion) ----------
def notificacao(titulo_n, texto_n, left, top, w=900, tema='escuro', hora='agora', opac=1.0, escala=1.0, linhas=1):
    """Notificação de celular (estilo do K6): cartão claro com o ícone do MinhaMoto, nome do app, 'agora' e a mensagem.
    Texto real do app (nunca inventar função que o app não tem)."""
    f = escala; h = round((170 + 48 * (linhas - 1)) * f); r = round(40 * f); ic = round(84 * f)
    sombra = '0 30px 60px rgba(0,0,0,.45),0 8px 18px rgba(0,0,0,.3)' if tema == 'escuro' else '0 30px 60px rgba(10,26,51,.18),0 8px 18px rgba(10,26,51,.10)'
    return (f"<div class=uicard style='position:absolute;left:{left}px;top:{top}px;width:{w}px;height:{h}px;border-radius:{r}px;"
            f"background:rgba(248,250,253,.97);box-shadow:{sombra};opacity:{opac};display:flex;align-items:center'>"
            f"<img src='file://{ICON}' style='width:{ic}px;height:{ic}px;border-radius:{round(ic*.24)}px;margin:0 {round(28*f)}px 0 {round(30*f)}px'>"
            f"<div style='flex:1;min-width:0;padding-right:{round(30*f)}px'>"
            f"<div style='display:flex;justify-content:space-between;font-family:j700;font-size:{round(32*f)}px;color:{NAVY_TXT}'>"
            f"<span>{H.escape(titulo_n)}</span><span style='font-family:j500;font-size:{round(28*f)}px;color:#8A96AA'>{H.escape(hora)}</span></div>"
            f"<div style='font-family:j600;font-size:{round(38*f)}px;line-height:1.25;color:#24324A;margin-top:{round(8*f)}px;{'white-space:nowrap;overflow:hidden;text-overflow:ellipsis' if linhas == 1 else ''}'>{H.escape(texto_n) if linhas == 1 else '<br>'.join(H.escape(x) for x in texto_n.split(chr(10)))}</div>"
            f"</div></div>"), h

def marca_texto(left, top, w, h, cor='rgba(198,255,0,.38)', rot=-1.2):
    """Marca-texto translúcido atrás de uma palavra/linha (como no K6). Desenhar ANTES do texto."""
    return (f"<div style='position:absolute;left:{left}px;top:{top}px;width:{w}px;height:{h}px;border-radius:{round(h*.22)}px;"
            f"background:{cor};transform:rotate({rot}deg)'></div>")

# ---------- card final ----------
def final_app(tt, tema, l1, l2, sub, preco=False):
    """CTA do app: ícone com brilho redondo (sem halo quadrado), título, traço limão, apoio, preço opcional; selos separados embaixo."""
    top, selos, tam = (300, 1330, 76) if tt else (150, 1150, 84)
    glow_c = 'rgba(82,169,254,.42), rgba(40,122,245,.16) 55%' if tema == 'escuro' else 'rgba(40,122,245,.22), rgba(40,122,245,.07) 55%'
    glow = (f"<div style='position:absolute;left:50%;top:{top - 150}px;width:560px;height:560px;margin-left:-280px;border-radius:50%;"
            f"background:radial-gradient(closest-side, {glow_c}, rgba(0,0,0,0) 100%);filter:blur(6px)'></div>")
    ic = f"<img src='file://{ICON}' style='width:200px;height:200px;filter:drop-shadow(0 26px 34px rgba(0,0,0,.45))'>"
    t = (f"<div class=titB style='position:relative;left:0;right:0;width:auto;font-size:{tam}px;margin-top:52px;letter-spacing:-.035em;line-height:1.06'>"
         f"{H.escape(l1)}<br><span class=b>{H.escape(l2)}</span></div><span class=lm></span>")
    s = f"<div class=apoB style='position:relative;left:0;right:0;width:auto;font-size:{38 if tt else 42}px;margin-top:26px'>{H.escape(sub)}</div>"
    pr = "<div style='margin-top:44px'><span class=preco><i></i>por R$19,90</span></div>" if preco else ''
    pad = 140 if tt else 60
    corpo = f"<div style='position:absolute;left:{pad}px;right:{pad}px;top:{top}px;text-align:center'>{ic}{t}{s}{pr}</div>"
    se = f"<div style='position:absolute;left:0;right:0;top:{selos}px;text-align:center'><img src='file://{SELOS}' style='width:540px'></div>"
    return fundo(tema, (50, 30)) + glow + corpo + se

def final_salva(tt, tema, kick, linhas, azul_de, sub, tam=None):
    """'Salve e mande pro amigo que…': ícones salvar/enviar, título grande, assinatura da marca no rodapé."""
    if tt:
        L, w, T, tam = 140, 800, 330, tam or 76
    else:
        L, w, T, tam = 90, 900, 170, tam or 84
    cor = AZUL_CLARO if tema == 'escuro' else AZUL
    caixa = ("background:linear-gradient(160deg,#121a2a,#05080f);box-shadow:inset 0 0 0 2px rgba(255,255,255,.07),0 24px 50px rgba(0,0,0,.45)"
             if tema == 'escuro' else "background:#fff;box-shadow:0 0 0 2px rgba(10,26,51,.06),0 24px 50px rgba(10,26,51,.14)")
    ics = ''.join(f"<div style='display:inline-flex;width:132px;height:132px;border-radius:38px;{caixa};align-items:center;justify-content:center;margin-right:26px'>"
                  f"{icone(n, 70, cor, 7)}</div>" for n in ('salvar', 'enviar'))
    c = fundo(tema, (30, 30))
    c += f"<div style='position:absolute;left:{L}px;top:{T}px'>{ics}</div>"
    y = T + 132 + 64
    c += kicker(kick, L, y, tema, w=w)
    c += titulo(linhas, L, y + 58, tam, w=w, azul_de=azul_de)
    y2 = y + 58 + alt_titulo(len(linhas), tam) + 36
    c += apoio([sub], L, y2, 38 if tt else 40, w=w)
    c += assinatura(1380 if tt else 1180, tema, left=L)
    return c

# ---------- render ----------
def _render_tenta(html, w, h, saida, tentativas=6):
    """O Chrome às vezes cai por falta de memória quando outros renders rodam junto: tenta de novo."""
    import time
    for t in range(tentativas):
        try:
            return _render(html, w, h, saida)
        except Exception as e:
            print('   retentando', os.path.basename(saida), '-', str(e).splitlines()[0][:80]); time.sleep(8 + 6 * t)
    raise RuntimeError('render falhou: ' + saida)

def render_lista(nome, cards45, cards916):
    _render = _render_tenta
    ok = True
    pasta = os.path.join(PECAS, nome)
    for i, (tema, c) in enumerate(cards45, 1):
        ok &= _render(wrap(tema, c), 1080, 1350, os.path.join(pasta, 'carrossel', f'{i:02d}.jpg'))
    for i, (tema, c) in enumerate(cards916, 1):
        ok &= _render("<div class=tt>" + wrap(tema, c) + "</div>", 1080, 1920, os.path.join(pasta, 'carrossel-tiktok', f'{i:02d}.jpg'))
    return ok

def folha(nome, titulo_folha):
    """Folha de revisão: 4:5 em cima, 9:16 embaixo (com a zona segura marcada em verde)."""
    from PIL import ImageDraw, ImageFont
    pasta = os.path.join(PECAS, nome)
    a = sorted(os.listdir(os.path.join(pasta, 'carrossel'))); b = sorted(os.listdir(os.path.join(pasta, 'carrossel-tiktok')))
    w45, h45 = 360, 450; w9, h9 = 360, 640; gap = 16; n = max(len(a), len(b))
    W = gap + n * (w45 + gap); Hh = 60 + h45 + 60 + h9 + gap
    F = Image.new('RGB', (W, Hh), (24, 26, 30)); d = ImageDraw.Draw(F)
    fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 26) if os.path.exists('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf') else None
    d.text((gap, 16), titulo_folha + ' · 4:5', fill=(235, 235, 235), font=fnt)
    for i, f in enumerate(a):
        F.paste(Image.open(os.path.join(pasta, 'carrossel', f)).resize((w45, h45), Image.LANCZOS), (gap + i * (w45 + gap), 60))
    d.text((gap, 60 + h45 + 16), '9:16 (TikTok) · verde = zona segura x 140–940 / y 150–1500', fill=(235, 235, 235), font=fnt)
    for i, f in enumerate(b):
        x0, y0 = gap + i * (w45 + gap), 60 + h45 + 60
        F.paste(Image.open(os.path.join(pasta, 'carrossel-tiktok', f)).resize((w9, h9), Image.LANCZOS), (x0, y0))
        s = w9 / 1080
        d.rectangle([x0 + 140 * s, y0 + 150 * s, x0 + 940 * s, y0 + 1500 * s], outline=(170, 255, 60), width=2)
    F.save(os.path.join(pasta, 'folha-revisao.jpg'), quality=90)
    print('folha', os.path.join(pasta, 'folha-revisao.jpg'))

# ---------- grafismos da revisão (25/11) ----------
def chuva_luz(w, h, cx, topo, abertura, n=260, seed=7, intens=1.0):
    """Feixe de luz (farol) vindo de cima com a chuva aparecendo dentro dele. Só SVG, sem foto."""
    import random, math
    rnd = random.Random(seed)
    lw = abertura
    poly = f"{cx - 40},{topo} {cx + 40},{topo} {cx + lw},{h} {cx - lw},{h}"
    linhas = []
    for _ in range(n):
        y = rnd.uniform(topo + 40, h)
        frac = (y - topo) / (h - topo)
        meia = 40 + (lw - 40) * frac
        x = rnd.uniform(cx - meia, cx + meia)
        dist = abs(x - cx) / max(meia, 1)
        L = rnd.uniform(26, 70)
        op = (0.55 - 0.45 * dist) * rnd.uniform(.4, 1.0) * intens * (1 - 0.35 * frac)
        if op <= 0.03: continue
        dx = L * math.sin(math.radians(12)); dy = L * math.cos(math.radians(12))
        sw = rnd.choice([1.6, 2, 2.4])
        linhas.append(f"<line x1='{x:.1f}' y1='{y:.1f}' x2='{x - dx:.1f}' y2='{y + dy:.1f}' stroke='rgba(205,232,255,{op:.2f})' stroke-width='{sw}' stroke-linecap='round'/>")
    return (f"<svg class=fill width='{w}' height='{h}' style='position:absolute;left:0;top:0'>"
            f"<defs><linearGradient id='cone' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='rgba(165,215,255,.42)'/>"
            f"<stop offset='.55' stop-color='rgba(82,169,254,.12)'/><stop offset='1' stop-color='rgba(82,169,254,0)'/></linearGradient>"
            f"<filter id='bl'><feGaussianBlur stdDeviation='18'/></filter></defs>"
            f"<polygon points='{poly}' fill='url(#cone)' filter='url(#bl)'/>{''.join(linhas)}"
            f"<ellipse cx='{cx}' cy='{topo}' rx='120' ry='34' fill='rgba(225,242,255,.55)' filter='url(#bl)'/></svg>")

# ---------- fotos do banco Pexels (rodada 2, 24/11) ----------
FOTOS = os.path.join(REPO, 'agencia', 'designer', 'assets', 'fotos')

def foto_prep(fid, crop=None, borrar=(), escurece=1.0, nome=None, neutro=(), satura=1.0, frio=0.0):
    """Prepara a foto do banco (corte + borrão local em logo/marca legível) numa cópia em cache. Nunca mexe no asset."""
    from PIL import ImageFilter, ImageEnhance
    out = os.path.join(CACHE, (nome or f'foto_{fid}') + '.jpg')
    im = Image.open(os.path.join(FOTOS, f'{fid}.jpg')).convert('RGB')
    if borrar:
        from PIL import ImageDraw
        bl = im.filter(ImageFilter.GaussianBlur(5))
        m = Image.new('L', im.size, 0); d = ImageDraw.Draw(m)
        for r in borrar:
            if r[0] == 'disco':   # mostrador inteiro: desfoque uniforme até o aro (cx, cy, raio)
                _, cx, cy, rx, ry = r
                bl2 = im.filter(ImageFilter.GaussianBlur(3.5))
                m2 = Image.new('L', im.size, 0); ImageDraw.Draw(m2).ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=255)
                im = Image.composite(bl2, im, m2.filter(ImageFilter.GaussianBlur(3)))
            else:
                d.ellipse(r, fill=255)
        m = m.filter(ImageFilter.GaussianBlur(10))
        im = Image.composite(bl, im, m)
    if neutro:   # apaga a cor de pontos que viram mancha (ex.: farol esverdeado), sem borrar
        from PIL import ImageDraw, ImageOps
        g = ImageEnhance.Brightness(ImageOps.grayscale(im).convert('RGB')).enhance(.8)
        m = Image.new('L', im.size, 0); d = ImageDraw.Draw(m)
        for (cx, cy, rx, ry) in neutro: d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=255)
        im = Image.composite(g, im, m.filter(ImageFilter.GaussianBlur(14)))
    if satura != 1.0: im = ImageEnhance.Color(im).enhance(satura)
    if frio:
        azul = Image.new('RGB', im.size, (20, 60, 140))
        im = Image.blend(im, azul, frio)
    if crop: im = im.crop(crop)
    if escurece != 1.0: im = ImageEnhance.Brightness(im).enhance(escurece)
    im.save(out, quality=94)
    return out

def foto_fundo(arq, pos='50% 50%', degr='escuro', forca=.85, topo=.25, h=1350):
    """Foto em tela cheia (cover) + degradê pra legibilidade. degr: 'escuro' (preto embaixo) ou 'claro' (branco embaixo)."""
    if degr == 'escuro':
        g = (f"linear-gradient(180deg, rgba(1,7,17,{topo}) 0%, rgba(1,7,17,.05) 30%, rgba(1,7,17,{forca*.75:.2f}) 62%, rgba(1,7,17,{forca}) 100%)")
    elif degr == 'escuro_topo':
        g = (f"linear-gradient(180deg, rgba(1,7,17,{forca}) 0%, rgba(1,7,17,{forca*.7:.2f}) 35%, rgba(1,7,17,.05) 65%, rgba(1,7,17,{topo}) 100%)")
    else:
        g = (f"linear-gradient(180deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0) 38%, rgba(244,247,252,.92) 58%, #F4F7FC 70%)")
    return (f"<div class=fill style=\"background:url('file://{arq}') {pos}/cover\"></div>"
            f"<div class=fill style='background:{g}'></div>")
