#!/usr/bin/env python3
"""VENDA-MM-R1 · criativos de VENDA do MinhaMoto · rodada 2 (24/11/2026, depois da revisão independente).

6 vídeos 9:16 1080x1920 30 fps, sem voz (texto + efeitos sonoros), 2 por formato:
  V1/V2 tela do app em ação · V3/V4 historinha da dor · V5/V6 nativo TikTok/POV.
Régua: agencia/DESIGN-MINHAMOTO.md (★ constituição 24/11 + "Criativo de venda: regras da revisão independente").
Travas deste motor (qualquer falha = não renderiza):
  - telas SÓ de telas-app/ios-1.0/, nunca 15-notificacoes; barra de abas do iPhone também na rolagem;
  - cabeçalho/status bar idênticos em todas as telas (faixa preta, ilha nunca aparece e some);
  - destaque (recorte puxado) sai VOLTANDO pra linha real e some alinhado: checagem de fantasma por diferença de pixels;
  - texto: zona segura x 140–940 / y 150–1500, linha única, sem preposição no fim da linha, sem nome de peça partido,
    nunca encostando na tela do app; >= 0,35 s por palavra; nenhum quadro vazio (texto seguinte entra antes do anterior sumir);
  - CTA de 4 s com respiro (sem trecho parado > 1,5 s);
  - preço só "por R$19,90"; sem teste grátis; CTA "Baixe agora o MinhaMoto" + selos.

Uso:
  python3 venda_mm_r1.py check V1|todos     # travas (layout, leitura, quebras, fantasma)
  python3 venda_mm_r1.py prev V1 0 2.5 6    # quadros soltos em /home/claude/venda-mm/prev/
  python3 venda_mm_r1.py render V1|todos    # vídeo + áudio (sem música) + folha
  python3 venda_mm_r1.py audio V1           # refaz só o áudio/mux
  python3 venda_mm_r1.py trilha V1 faixa.mp3  # versão COM trilha (música -14 LUFS, efeitos 6 dB abaixo)
"""
import os, sys, math, json, re, subprocess, shutil, html as H
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(AQUI, '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'agencia', 'direcao-v2'))
sys.path.insert(0, AQUI)
import motor as M

IOS = os.path.join(REPO, 'agencia', 'designer', 'assets', 'telas-app', 'ios-1.0')
ASSETS = M.ASSETS
FOTOS = os.path.join(ASSETS, 'fotos')
ICON = os.path.join(ASSETS, 'icon.png')
SELOS = os.path.join(ASSETS, 'selos-lojas.png')
TMP = '/home/claude/venda-mm'
CACHE = os.path.join(TMP, 'cache2')
OUT = os.path.join(REPO, 'agencia', 'estudio', 'pecas', 'VENDA-MM-R1')
W, HH, FPS = 1080, 1920, 30
os.makedirs(CACHE, exist_ok=True)

AZUL, AZUL_ESC, AZUL_CLARO = '#287AF5', '#005FDE', '#52A9FE'
NAVY, NAVY2, PRETO = '#051F43', '#0F57A8', '#010711'
LIMAO = '#C6FF00'
VERM = '#FF453A'
PROIBIDAS = ['15-notificacoes']
SOBRA = 0.0             # sem sobreposição de texto com texto (vira texto duplicado); quadro nunca fica vazio porque sempre há foto ou celular

# ---------------------------------------------------------------- números do V4 (decisão do Léo, 24/11)
# Componente: pastilha de freio que gasta até o metal e risca o disco. Número = PREÇO DA PEÇA NOVA de fonte séria
# (concessionária Honda), com link e data em pecas/VENDA-MM-R1/fontes.md. O rodapé descreve exatamente o número.
V4_NUM = dict(pastilha='R$ 224', peca='R$ 606,28', rotulo='Disco novo:',
              rodape='Pastilha dianteira original Honda R$ 224,27 · Disco de freio dianteiro CG 160 Titan/Fan R$ 606,28 · '
                     'Winner Honda Store (Limeira/SP) · nov/2026')

ease, eout, eback, lerp = M.ease, M.eout, M.eback, M.lerp
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))

# ---------------------------------------------------------------- telas
def tela(nome):
    if any(p in nome for p in PROIBIDAS): raise ValueError('tela proibida: ' + nome)
    p = os.path.join(IOS, nome + '.png')
    if not os.path.exists(p): raise FileNotFoundError(p)
    return p

def cabecalho():
    """Status bar + barra do app (0–360). É idêntica em todas as rotas do iPhone (conferido pixel a pixel)."""
    out = os.path.join(CACHE, 'cabecalho.png')
    if not os.path.exists(out):
        Image.open(tela('rolagem/02-saude')).crop((0, 0, 1179, M.TOPO_FIXO)).save(out)
    return out

def faixa_status_folha():
    """Folha (pop-up) com fundo escurecido: status bar preta igual às outras telas + degradê até a folha.
    Sem isso a ilha do mockup aparece só nessa tela (fundo cinza) e some nas outras (regra 18/11)."""
    out = os.path.join(CACHE, 'faixa_folha.png')
    if not os.path.exists(out):
        im = Image.new('RGBA', (1179, 232), (0, 0, 0, 0))
        im.paste(Image.open(tela('rolagem/02-saude')).convert('RGBA').crop((0, 0, 1179, 177)), (0, 0))
        a = np.zeros((232, 1179), np.uint8); a[:177] = 255
        for y in range(177, 232): a[y] = int(255 * (1 - (y - 177) / 55) ** 1.4)
        px = np.asarray(im).copy(); px[177:, :, :3] = 0; px[:, :, 3] = a
        Image.fromarray(px, 'RGBA').save(out)
    return out

def barra_abas(tipo):
    """Barra de abas flutuante do iPhone 1.0, tirada das telas paradas (fundo limpo da 10; cápsula ativa da 02).
    tipo: 'nenhuma' (subpáginas: histórico, lista, documentos, cuidados) | 'saude' (aba Saúde ativa)."""
    out = os.path.join(CACHE, f'abas_{tipo}.png')
    if not os.path.exists(out):
        cx = (150, 2230, 1035, 2425)
        base = Image.open(tela('10-lista-revisao')).convert('RGBA').crop(cx)
        m = Image.new('L', base.size, 0); d = ImageDraw.Draw(m)
        d.rounded_rectangle((10, 16, 872, 188), radius=86, fill=255)
        if tipo == 'saude':
            s02 = Image.open(tela('02-saude')).convert('RGBA').crop(cx)
            mc = Image.new('L', base.size, 0); dc = ImageDraw.Draw(mc)
            dc.rounded_rectangle((31, 33, 247, 172), radius=68, fill=255)
            dc.rounded_rectangle((88, 6, 188, 34), radius=12, fill=255)
            mc = mc.filter(ImageFilter.GaussianBlur(1.5))
            base.paste(s02, (0, 0), mc)
            d.rounded_rectangle((88, 6, 188, 34), radius=12, fill=255)
        base.putalpha(m)
        base.save(out)
    return out

def recorte(nome, box):
    out = os.path.join(CACHE, 'rec_%s_%d_%d_%d_%d.png' % ((nome.replace('/', '_'),) + tuple(box)))
    if not os.path.exists(out):
        Image.open(tela(nome)).convert('RGB').crop(box).save(out)
    return out

# ---------------------------------------------------------------- página
CSS_MOCKUP = (M.PAGINA % dict(fontes=M.CSS_FONTES, **M.ESTILOS['B'])).split('<style>')[1].split('</style>')[0]
CSS = CSS_MOCKUP + """
#bg{position:absolute;inset:0;overflow:hidden}
#bgg{position:absolute;inset:0}
#bg img{position:absolute;display:none;transform-origin:50% 50%}
#vig{position:absolute;inset:0;pointer-events:none}
#gfx{position:absolute;inset:0}
.lay{position:absolute;inset:0;background:#000}
.lay img{position:absolute;left:0;top:0;width:100%}
.lay img.ab,#fixab{position:absolute;left:12.7226%;top:87.2457%;width:75.0636%}
#fixtopo{position:absolute;left:0;top:0;width:100%;display:none}
#phone .frame{box-shadow:0 0 0 2px #5d636d inset,0 0 0 9px #0a0b0d inset,0 60px 70px rgba(0,0,0,.6),0 20px 24px rgba(0,0,0,.45),0 0 90px rgba(82,169,254,.25)}
#call{position:absolute;left:0;top:0;display:none;transform-origin:50% 50%}
#call img{display:block;width:100%;height:100%;border-radius:22px}
#call i{position:absolute;inset:-3px;border-radius:25px;pointer-events:none}
.tapc{position:absolute;width:110px;height:110px;border-radius:50%;border:5px solid rgba(255,255,255,.9);background:rgba(255,255,255,.2);display:none}
.vc{position:absolute;left:144px;width:792px}
.vk{font-family:j600;font-size:34px;color:#dbe5f5;letter-spacing:-.005em;display:flex;align-items:center;gap:16px;margin-bottom:18px;white-space:nowrap}
.vk b{width:16px;height:16px;border-radius:50%;background:#C6FF00;box-shadow:0 0 16px rgba(198,255,0,.6);flex:none}
.vk.red b{background:#FF453A;box-shadow:0 0 16px rgba(255,69,58,.7)}
.ln{font-family:j800;color:#fff;letter-spacing:-.03em;line-height:1.08;white-space:nowrap;padding-bottom:.04em}
.ln .k{color:#C6FF00}
.ln .r{color:#FF453A}
.vs{font-family:j500;font-size:40px;color:#dbe5f5;line-height:1.3;letter-spacing:-.01em;margin-top:22px;white-space:nowrap}
.sh .ln,.sh .vk,.sh .vs{text-shadow:0 3px 8px rgba(0,0,0,.6),0 10px 44px rgba(0,0,0,.85)}
"""

PAGE = """<!doctype html><html><head><meta charset=utf-8><style>%s</style></head><body>
<div id=bg><div id=bgg></div><img id=bgi1><img id=bgi2></div><div id=luz></div><div id=vig></div>
<div id=gfx></div>
<div id=phonewrap><div id=phone>
 <div class=frame></div>
 <div class='btn' style='left:-7px;top:22%%;width:9px;height:7%%'></div>
 <div class='btn' style='left:-7px;top:31%%;width:9px;height:7%%'></div>
 <div class='btn' style='left:-7px;top:15%%;width:9px;height:4%%'></div>
 <div class='btn' style='right:-7px;top:25%%;width:9px;height:11%%'></div>
 <div class=screen>
  <div class=lay id=lay1><img class=pg><img class=ab><img class=tp></div>
  <div class=lay id=lay2><img class=pg><img class=ab><img class=tp></div>
  <div class=lay id=lay3><img class=pg><img class=ab><img class=tp></div>
  <img id=fixab style='display:none'><img id=fixtopo>
  <div class=tapc></div><div class=mask style='position:absolute;display:none'></div>
  <div class=foot><i></i></div><div class=island></div><div class=glare></div>
 </div>
</div></div>
<div id=call><img><i></i></div>
<div id=txt></div>
<script>
async function setImg(el, src){
  if(!src){ el.style.display='none'; return; }
  el.style.display='block';
  if(el.getAttribute('src')!==src){ el.setAttribute('src',src); try{await el.decode()}catch(e){} }
}
window.R = async function(s){
  document.getElementById('bgg').style.background = s.bg.grad || 'none';
  for(const k of ['1','2']){
    const b = s.bg['i'+k], el = document.getElementById('bgi'+k);
    if(b){ await setImg(el, b.src); el.style.left=b.left+'px'; el.style.top=b.top+'px'; el.style.width=b.w+'px'; el.style.height=b.h+'px';
           el.style.transform=b.tr||'none'; el.style.filter=b.filter||'none'; el.style.opacity=(b.op===undefined?1:b.op); el.style.display='block'; }
    else el.style.display='none';
  }
  document.getElementById('luz').style.background = s.luz || 'none';
  document.getElementById('vig').style.background = s.vig || 'none';
  document.getElementById('gfx').innerHTML = s.gfx || '';
  const ph = document.getElementById('phone');
  if(s.ph){
    const p = s.ph; ph.style.display='block';
    ph.style.width=p.w+'px'; ph.style.height=p.h+'px'; ph.style.left=(-p.w/2)+'px'; ph.style.top=(-p.h/2)+'px';
    ph.style.transform=p.tr; ph.style.opacity=p.op;
    for(const i of [1,2,3]){
      const L = p['l'+i], lay = document.getElementById('lay'+i);
      if(L){ lay.style.display='block'; lay.style.opacity=L.op; lay.style.clipPath=L.clip||'none'; lay.style.background=L.clip?'transparent':'#000'; lay.style.transform='translate('+(L.dx||0)+'px,'+(L.dy2||0)+'px)'; lay.style.boxShadow=L.sh||'none';
             await setImg(lay.querySelector('.pg'), L.src); lay.querySelector('.pg').style.transform='translateY('+L.dy+'px)';
             await setImg(lay.querySelector('.ab'), L.ab); await setImg(lay.querySelector('.tp'), L.topo); }
      else lay.style.display='none';
    }
    await setImg(document.getElementById('fixab'), p.fixab || null);
    await setImg(document.getElementById('fixtopo'), p.fixtopo || null);
    const mk = ph.querySelector('.mask');
    if(p.mask){ mk.style.display='block'; Object.assign(mk.style, p.mask); } else mk.style.display='none';
    const tp = ph.querySelector('.tapc');
    if(p.tap){ tp.style.display='block'; Object.assign(tp.style, p.tap); } else tp.style.display='none';
  } else ph.style.display='none';
  const c = document.getElementById('call');
  if(s.call){
    const k = s.call; c.style.display='block'; await setImg(c.querySelector('img'), k.src);
    c.style.left=k.left+'px'; c.style.top=k.top+'px'; c.style.width=k.w+'px'; c.style.height=k.h+'px';
    c.style.transform=k.tr; c.style.opacity=1; c.querySelector('i').style.boxShadow=k.ring;
    c.querySelector('img').style.boxShadow=k.sombra;
  } else c.style.display='none';
  document.getElementById('txt').innerHTML = s.txt || '';
  for(const im of document.querySelectorAll('#txt img,#gfx img')){ try{await im.decode()}catch(e){} }
  await document.fonts.ready;
  return 1;
}
window.MEDE = function(){
  const out = [];
  for(const el of document.querySelectorAll('#txt .ln,#txt .vk,#txt .vs,#txt .med,#gfx .med')){
    const r = el.getBoundingClientRect();
    const rg = document.createRange(); rg.selectNodeContents(el); const b = rg.getBoundingClientRect();
    out.push({cls: el.className, txt: el.textContent, x0: b.left, x1: b.right, y0: r.top, y1: r.bottom, sw: el.scrollWidth, cw: el.clientWidth,
              fs: parseFloat(getComputedStyle(el).fontSize)});
  }
  const c = document.getElementById('call');
  const cr = c.style.display==='block' ? c.getBoundingClientRect() : null;
  const ph = document.getElementById('phone');
  const pr = ph.style.display==='block' ? ph.querySelector('.screen').getBoundingClientRect() : null;
  return {txt: out, call: cr && {x0:cr.left,x1:cr.right,y0:cr.top,y1:cr.bottom}, scr: pr && {x0:pr.left,x1:pr.right,y0:pr.top,y1:pr.bottom}};
}
</script></body></html>""" % CSS

# ---------------------------------------------------------------- fundos
def bg_navy(tg):
    grad = f'radial-gradient(90% 60% at 50% 40%, {NAVY2} 0%, {NAVY} 52%, {PRETO} 100%)'
    luz = (f"radial-gradient(38% 22% at 50% 64%, rgba(82,169,254,.26), rgba(0,0,0,0) 70%), "
           f"radial-gradient(40% 25% at {50+30*math.sin(tg*0.6):.1f}% {30+8*math.cos(tg*0.5):.1f}%, rgba(82,169,254,.20), rgba(0,0,0,0) 70%)")
    return dict(bg=dict(grad=grad), luz=luz, vig='radial-gradient(130% 90% at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,.55) 100%)')

def bg_azul(tg):
    """Fundo azul vivo de marca (V6): diferente do navy dos outros."""
    grad = f'radial-gradient(95% 65% at 50% 30%, #4FA0FF 0%, {AZUL} 42%, #0A47C2 100%)'
    luz = f"radial-gradient(45% 25% at {50+25*math.sin(tg*0.5):.1f}% 20%, rgba(255,255,255,.16), rgba(255,255,255,0) 70%)"
    return dict(bg=dict(grad=grad), luz=luz, vig='radial-gradient(130% 90% at 50% 45%, rgba(0,0,0,0) 60%, rgba(0,10,40,.35) 100%)')

def _foto(arq):
    p = arq if os.path.isabs(arq) else os.path.join(FOTOS, arq); iw, ih = Image.open(p).size
    return 'file://' + p, iw, ih

def bg_foto(arq, tl, dur, z0=1.0, z1=1.08, fx0=0.5, fy0=0.5, fx1=0.5, fy1=0.5, brilho=1.0, contraste=1.04, sat=1.05,
            blur=0, topo=0.55, base=0.15, pb=False, tinta=None):
    """Foto cobrindo o 9:16 inteiro (sem faixa borrada), Ken Burns pelo ponto de foco (fx, fy).
    topo/base: escurecimento suave em cima (leitura do texto) e embaixo."""
    src, iw, ih = _foto(arq)
    k = ease(clamp(tl / max(0.01, dur)))
    z = lerp(z0, z1, k); fx = lerp(fx0, fx1, k); fy = lerp(fy0, fy1, k)
    sc = max(W / iw, HH / ih) * z
    cw, ch = iw * sc, ih * sc
    left = clamp(W / 2 - fx * cw, W - cw, 0); top = clamp(HH / 2 - fy * ch, HH - ch, 0)
    f = f'brightness({brilho:.2f}) contrast({contraste:.2f}) saturate({0 if pb else sat:.2f})' + (f' blur({blur}px)' if blur else '')
    i1 = dict(src=src, left=round(left, 2), top=round(top, 2), w=round(cw, 2), h=round(ch, 2), filter=f)
    vig = (f'linear-gradient(rgba(0,0,0,{topo:.2f}) 0%, rgba(0,0,0,{topo*0.45:.2f}) 22%, rgba(0,0,0,0) 42%, '
           f'rgba(0,0,0,0) 62%, rgba(0,0,0,{base:.2f}) 100%)')
    if tinta: vig = f'linear-gradient({tinta},{tinta}), ' + vig
    return dict(bg=dict(grad='#000', i1=i1), luz='none', vig=vig)

def lum(arq):
    """Luminância média da foto (0–255), pra igualar a exposição das fotos de uma mesma peça."""
    p = arq if os.path.isabs(arq) else os.path.join(FOTOS, arq)
    return float(np.asarray(Image.open(p).convert('L').resize((200, 200))).mean())

def bg_foto_fundo(arq, fx=0.5, fy=0.5, z=1.15, brilho=0.48):
    """Fundo das cenas de celular: a própria foto desfocada e escurecida (estilo A aprovado)."""
    return lambda tl, tg: bg_foto(arq, tl, 8, z, z + 0.04, fx, fy, fx, fy, brilho=brilho, blur=26, topo=0.35, base=0.35)

# ---------------------------------------------------------------- textos
PREPS = {'de', 'da', 'do', 'das', 'dos', 'com', 'a', 'o', 'as', 'os', 'e', 'em', 'no', 'na', 'nos', 'nas', 'pra', 'pro',
         'por', 'para', 'um', 'uma', 'ao', 'à', 'que', 'sem', 'sua', 'seu'}
NOMES = ['vela de ignição', 'óleo do motor', 'fluido de freio', 'kit relação', 'troca de óleo', 'filtro de ar',
         'pneu traseiro', 'primeira moto', 'dia perdido', 'plano de revisão']

def _limpa(s): return re.sub(r'[\[\]{}]', '', s)

def _linha_html(ln):
    e = H.escape(ln)
    e = re.sub(r'\[(.+?)\]', r"<span class=k>\1</span>", e)
    e = re.sub(r'\{(.+?)\}', r"<span class=r>\1</span>", e)
    return e

def palavras(c):
    t = ' '.join(c.get('lines', [])) + ' ' + (c.get('kicker') or '') + ' ' + (c.get('sup') or '') + ' ' + ' '.join(c.get('extra_txt', []))
    return len([w for w in re.sub(r'[\[\]{}…:,.!?→]', ' ', t).split() if w.strip()])

def card_html(c, tl, dur):
    """Bloco de texto. Entra linha a linha (sobe + desfoque); sai nos últimos 0,28 s (dur já inclui a SOBRA)."""
    hook = c.get('hook', False)
    tt = tl + (1.5 if hook else 0)
    sai = clamp((tl - (dur - 0.28)) / 0.28) if c.get('sai', True) else 0
    al = c.get('align', 'left'); tam = c.get('size', 72)
    out = []
    def anim(i):
        k = eout((tt - 0.07 * i) / 0.45)
        op = clamp(k * 1.3) * (1 - sai)
        return f"opacity:{op:.3f};filter:blur({(1-k)*10 + sai*6:.2f}px);transform:translateY({(1-k)*34 - sai*10:.1f}px)"
    i = 0
    if c.get('kicker'):
        jc = 'center' if al == 'center' else 'flex-start'
        out.append(f"<div class='vk{' red' if c.get('kicker_red') else ''}' style='justify-content:{jc};{anim(i)}'><b></b>{H.escape(c['kicker'])}</div>"); i += 1
    for ln in c['lines']:
        out.append(f"<div class=ln style='font-size:{tam}px;{anim(i)}'>{_linha_html(ln)}</div>"); i += 1
    if c.get('sup'):
        out.append(f"<div class=vs style='{anim(i+0.5)}'>{H.escape(c['sup'])}</div>")
    sc = f"transform:scale({1+0.04*(1-eout(tl/0.7)):.4f});transform-origin:{'50%' if al=='center' else '0%'} 0" if hook else ''
    return f"<div class='vc sh' style='top:{c['y']}px;text-align:{al};{sc}'>{''.join(out)}</div>"

def cta_html(c, tl):
    """CTA de 4 s: ícone com brilho redondo que respira, título, traço limão, 'Baixe agora o MinhaMoto.', selo de preço
    (pulsa 1 vez), selos das lojas embaixo. Nada fica 100% parado."""
    # título entra junto com o ícone (no 1º quadro do CTA já tem texto: nada de ícone sozinho)
    k1 = eback(clamp((tl + 0.1) / 0.38)); k2 = eout((tl + 0.14) / 0.42); k3 = eout((tl - 0.2) / 0.4)
    k4 = eback(clamp((tl - 0.55) / 0.38)); k5 = eout((tl - 0.8) / 0.45)
    pulso = 1 + 0.06 * math.sin(math.pi * clamp((tl - 2.2) / 0.5))
    resp = 0.5 + 0.5 * math.sin(tl * 2 * math.pi / 1.7)
    y = c.get('y', 300)
    tit = ''.join(f"<div class=ln style='font-size:76px'>{_linha_html(l)}</div>" for l in c['lines'])
    s = (f"<div style='position:absolute;left:{540-280}px;top:{y+100-280}px;width:560px;height:560px;border-radius:50%;"
         f"background:radial-gradient(circle, rgba(82,169,254,{(.34+.12*resp)*k1:.3f}) 0%, rgba(40,122,245,{(.12+.06*resp)*k1:.3f}) 38%, rgba(0,0,0,0) 70%)'></div>"
         f"<div style='position:absolute;left:0;right:0;top:{y}px;text-align:center'>"
         f"<img src='file://{ICON}' style='width:200px;height:200px;border-radius:46px;box-shadow:0 26px 70px rgba(0,0,0,.5);"
         f"transform:scale({(0.5+0.5*k1)*(1+0.012*resp):.4f})'>"
         f"<div class='vc sh' style='position:relative;left:144px;margin-top:48px;text-align:center;opacity:{clamp(k2*1.3):.3f};"
         f"transform:translateY({(1-k2)*30:.1f}px);filter:blur({(1-k2)*8:.1f}px)'>{tit}</div>"
         f"<div style='width:{96*k3:.0f}px;height:8px;border-radius:8px;background:{LIMAO};margin:28px auto 0;box-shadow:0 0 22px rgba(198,255,0,.45);opacity:{k3:.3f}'></div>"
         f"<div class='vs med sh' style='display:inline-block;margin-top:26px;font-size:46px;color:#eef3ff;opacity:{k3:.3f}'>Baixe agora o MinhaMoto.</div><br>"
         f"<div class=med style='display:inline-flex;align-items:center;gap:18px;margin-top:38px;padding:16px 44px 16px 34px;border-radius:999px;"
         f"background:linear-gradient(135deg,{AZUL},{AZUL_ESC});color:#fff;font-family:j700;font-size:56px;letter-spacing:-.01em;"
         f"box-shadow:0 0 0 3px rgba(255,255,255,.18) inset,0 20px 60px rgba(40,122,245,.45);transform:scale({max(0.01,k4)*pulso:.4f})'>"
         f"<i style='width:18px;height:18px;border-radius:50%;background:{LIMAO};box-shadow:0 0 18px rgba(198,255,0,.7)'></i>por R$19,90</div>"
         f"</div>"
         f"<div class=med style='position:absolute;left:{(W-520)//2}px;width:520px;top:{c.get('y_selos', 1345)}px;opacity:{k5:.3f};transform:translateY({(1-k5)*22:.1f}px)'>"
         f"<img src='file://{SELOS}' style='width:520px;display:block'></div>")
    return s

def tip_badge(n, y, tl, dur=99.0):
    k = eback(clamp((tl + 0.05) / 0.35)); sai = clamp((tl - (dur - 0.28)) / 0.28)
    return (f"<div style='position:absolute;left:{540-48}px;top:{y}px;width:96px;height:96px;border-radius:50%;background:{LIMAO};"
            f"display:flex;align-items:center;justify-content:center;font-family:j800;font-size:54px;color:{PRETO};"
            f"box-shadow:0 0 40px rgba(198,255,0,.45),0 10px 30px rgba(0,0,0,.4);transform:scale({k:.3f});opacity:{1-sai:.3f};filter:blur({6*sai:.1f}px)'>{n}</div>")

# ---------------------------------------------------------------- celular
PW = 700
PH = M.altura_celular(PW)          # 1466
SCR_H = PH - 44
P_CX, P_TOP = 540, 470
SW = PW - 44
E = SW / 1179.0

class Fone:
    """Celular único (mockup do motor.py). Segmentos de tela:
    dict(t0, t1, tela, rola=bool, keys=[(t, scroll)], abas='nenhuma'|'saude'|None, topo='cab'|'folha'|None,
         trans='push'|'sobe'|'desce', calls=[dict(box, t=(a,b), k=1.3, dy=-30, cor)], tap=dict(t, x, y))
    voo: dict(box, ate, seg=0): recorte gigante no começo que encolhe e encaixa na linha real (gancho do V1)."""
    def __init__(self, segs, entra=True, sai=True, top=P_TOP, pre=0.0, voo=None):
        self.segs = segs; self.entra = entra; self.sai = sai; self.pre = pre; self.voo = voo
        self.t0 = segs[0]['t0']; self.t1 = segs[-1]['t1']; self.cy = top + PH / 2
        for s in segs:
            s['src'] = 'file://' + tela(s['tela'])
            tp = s.get('topo', 'cab' if s.get('rola') else None)
            s['topo_src'] = {'cab': 'file://' + cabecalho(), 'folha': 'file://' + faixa_status_folha(), None: None}[tp]
            s['abas_src'] = ('file://' + barra_abas(s['abas'])) if s.get('abas') else None

    def scroll(self, s, t):
        ks = s.get('keys') or [(s['t0'], 0)]
        if t <= ks[0][0]: return ks[0][1]
        for (ta, ya), (tb, yb) in zip(ks, ks[1:]):
            if ta <= t <= tb: return lerp(ya, yb, ease((t - ta) / max(1e-6, tb - ta)))
        return ks[-1][1]

    def geo(self, t):
        tl = t - self.t0 + self.pre
        k = eout(tl / 0.9) if self.entra else 1.0
        ry = lerp(-12, 0, k); rx = lerp(5, 0, k); sc = lerp(0.93, 1.0, k)
        dy = lerp(1150, 0, eout(clamp(tl / 0.8))) if self.entra else 0
        op = 1.0   # entra deslizando, sem esmaecer: celular semitransparente deixa a faixa do topo diferente
        sc *= 1 + 0.03 * ease(clamp((t - self.t0) / max(0.01, self.t1 - self.t0)))
        if self.sai:   # sai deslizando pra baixo, sem esmaecer
            ks = clamp((t - (self.t1 - 0.38)) / 0.38)
            dy += 1100 * ks ** 2.2
        dy += 5 * math.sin(t * 1.3)
        return ry, rx, sc, dy, op

    def home(self, s, box, t, sc, dy):
        x0, y0, x1, y1 = box
        yy = self.scroll(s, t)
        scr_l = P_CX - PW / 2 + 22; scr_t = self.cy + dy - PH / 2 + 22
        hx = scr_l + (x0 + x1) / 2 * E; hy = scr_t + ((y0 + y1) / 2 - yy) * E
        hx = P_CX + (hx - P_CX) * sc; hy = (self.cy + dy) + (hy - (self.cy + dy)) * sc
        return hx, hy, (x1 - x0) * E * sc, (y1 - y0) * E * sc

    def _call_state(self, s, c, hx, hy, bw, bh, kk, ddy, ring_a):
        rgb = '255,69,58' if c.get('cor') == 'vermelho' else '82,169,254'
        return dict(src='file://' + recorte(s['tela'], c['box']), left=round(hx - bw / 2, 2), top=round(hy - bh / 2, 2),
                    w=round(bw, 2), h=round(bh, 2), tr=f"translateY({ddy:.2f}px) scale({kk:.4f})",
                    ring=f"0 0 0 3px rgba({rgb},{.9*ring_a:.2f}), 0 0 46px rgba({rgb},{.45*ring_a:.2f})",
                    sombra=f"0 34px 50px rgba(0,0,0,{.65*ring_a:.2f}),0 10px 18px rgba(0,0,0,{.5*ring_a:.2f})")

    def estado(self, t):
        call = None
        if self.voo and t < self.voo['ate']:
            v = self.voo; s = self.segs[v.get('seg', 0)]
            _, _, sc_e, dy_e, _ = self.geo(v['ate'])
            hx, hy, bw, bh = self.home(s, v['box'], v['ate'], sc_e, dy_e)
            k0 = v.get('largura', 900) / bw
            pt = v.get('parte', 0.5)
            p = ease(clamp((t - pt) / (v['ate'] - pt)))
            resp = (1 + 0.012 * math.sin(t * 6)) * (1 + 0.16 * (1 - eout(clamp(t / 0.4))))
            cx = lerp(540, hx, p); cy = lerp(v.get('y', 980), hy, p)
            kk = lerp(k0 * resp, 1.0, p)
            call = self._call_state(s, dict(box=v['box'], cor=v.get('cor')), cx, cy, bw, bh, kk, 0, 1 - p)
        if not (self.t0 <= t < self.t1): return None, call
        ry, rx, sc, dy, op = self.geo(t)
        tr = f"translate({P_CX - 540}px,{self.cy - 960 + dy:.1f}px) rotateY({ry:.2f}deg) rotateX({rx:.2f}deg) scale({sc:.4f})"
        i = max(j for j, s in enumerate(self.segs) if s['t0'] <= t)
        s = self.segs[i]
        def lay(sg, tt, o=1.0, dx=0.0, dy2=0.0, sh=None, ab=True, tp=True, clip=None):
            return dict(src=sg['src'], op=round(o, 3), dy=round(-self.scroll(sg, tt) * E, 2), dx=round(dx, 2), dy2=round(dy2, 2), sh=sh,
                        ab=sg['abas_src'] if ab else None, topo=sg['topo_src'] if tp else None, clip=clip)
        st = dict(w=PW, h=PH, tr=tr, op=round(op, 3))
        xf = (t - s['t0']) / 0.42
        if i > 0 and xf < 1:
            p = self.segs[i - 1]; k = ease(xf); tipo = s.get('trans', 'push')
            if tipo == 'push':
                fixa_tp = bool(s['topo_src']) and p['topo_src'] == s['topo_src']
                fixa_ab = bool(s['abas_src']) and p['abas_src'] == s['abas_src']
                st['l1'] = lay(p, p['t1'], 1.0, -0.28 * SW * k, ab=not fixa_ab, tp=not fixa_tp)
                st['l2'] = lay(s, t, 1.0, (1 - k) * SW, sh='-18px 0 40px rgba(0,0,0,.55)', ab=not fixa_ab, tp=not fixa_tp)
                st['fixtopo'] = s['topo_src'] if fixa_tp else None
                st['fixab'] = s['abas_src'] if fixa_ab else None
            elif tipo == 'sobe':     # folha abrindo como no iOS: o fundo escurece (esmaece) e o painel sobe opaco
                fy = s['folha_y'] * E; resto = SCR_H - fy
                st['l1'] = lay(p, p['t1'])
                st['l2'] = lay(s, t, k, clip=f'inset(0px 0px {resto:.1f}px 0px)')
                st['l3'] = lay(s, t, 1.0, 0, (1 - k) * resto, tp=False, clip=f'inset({fy:.1f}px 0px 0px 0px)')
            else:                    # 'desce': painel desce, fundo clareia e revela a tela de baixo
                fy = p['folha_y'] * E; resto = SCR_H - fy
                st['l1'] = lay(s, t)
                st['l2'] = lay(p, p['t1'], 1 - k, clip=f'inset(0px 0px {resto:.1f}px 0px)')
                st['l3'] = lay(p, p['t1'], 1.0, 0, k * resto, tp=False, clip=f'inset({fy:.1f}px 0px 0px 0px)')
        else:
            st['l1'] = lay(s, t)
        if self.voo and t < self.voo['ate'] and self.voo.get('mascara'):
            x0, y0, x1, y1 = self.voo['box']; yy = self.scroll(self.segs[self.voo.get('seg', 0)], t)
            st['mask'] = {'left': f'{(x0-6)*E:.1f}px', 'top': f'{(y0-6-yy)*E:.1f}px', 'width': f'{(x1-x0+12)*E:.1f}px',
                          'height': f'{(y1-y0+12)*E:.1f}px', 'background': self.voo['mascara'], 'borderRadius': '14px'}
        tp = s.get('tap')
        if tp and tp['t'] <= t <= tp['t'] + 0.55:
            kk = (t - tp['t']) / 0.55
            st['tap'] = {'left': f"{tp['x']*E-55:.1f}px", 'top': f"{(tp['y'] - self.scroll(s, t))*E-55:.1f}px",
                         'opacity': f'{1-kk:.2f}', 'transform': f'scale({0.6+0.6*kk:.2f})'}
        for c in s.get('calls', []):
            ta, tb = c['t']
            if not (ta <= t < tb) or op < 0.999: continue
            hx, hy, bw, bh = self.home(s, c['box'], t, sc, dy)
            K = c.get('k', 1.3)
            ki = eback(clamp((t - ta) / 0.42))            # sai da linha e cresce
            kr = ease(clamp((t - (tb - 0.3)) / 0.26))     # volta pra linha real e fica alinhado nos últimos quadros (sem fantasma)
            amp = ki * (1 - kr)
            kk = 1 + (K / sc - 1) * amp
            call = self._call_state(s, c, hx, hy, bw, bh, kk, c.get('dy', -30) * amp, min(1, ki * 1.4) * (1 - kr))
        return st, call

# ---------------------------------------------------------------- vídeo
class Video:
    def __init__(self, vid, titulo, dur):
        self.id = vid; self.titulo = titulo; self.dur = dur
        self.bgs = []; self.fones = []; self.cards = []; self.gfxs = []; self.ctas = []; self.sfx = []
    def bg(self, t0, t1, fn): self.bgs.append((t0, t1, fn))
    def fone(self, f): self.fones.append(f); return f
    def card(self, t0, t1, **c): c.update(t0=t0, t1=t1); self.cards.append(c)
    def gfx(self, t0, t1, fn): self.gfxs.append((t0, t1, fn))
    def cta(self, t0, **c): c.update(t0=t0, t1=self.dur); self.ctas.append(c)
    def som(self, t, nome, g=0.0): self.sfx.append((t, nome, g))

    def estado(self, t):
        s = dict(bg=dict(grad='#000'), luz='none', vig='none', gfx='', txt='', ph=None, call=None)
        for t0, t1, fn in self.bgs:
            if t0 <= t < t1 or (t1 >= self.dur and t >= t0): s.update(fn(t - t0, t))
        s['gfx'] = ''.join(fn(t - t0) for t0, t1, fn in self.gfxs if t0 <= t < t1)
        for f in self.fones:
            st, call = f.estado(t)
            if st: s['ph'] = st
            if call: s['call'] = call
        tx = []
        cta0 = min([c['t0'] for c in self.ctas] or [1e9])
        for c in self.cards:
            fim = c['t1'] + (SOBRA if c.get('sai', True) else 0)
            if c['t0'] < cta0 < fim: fim = cta0          # o CTA nunca entra por cima do texto anterior
            if c['t0'] <= t < fim: tx.append(card_html(c, t - c['t0'], fim - c['t0']))
        for c in self.ctas:
            if c['t0'] <= t: tx.append(cta_html(c, t - c['t0']))
        s['txt'] = ''.join(tx)
        return s

# ---------------------------------------------------------------- render e travas
def _browser(p):
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome',
                          args=['--no-sandbox', '--force-color-profile=srgb', '--allow-file-access-from-files', '--disable-gpu'])
    pg = b.new_page(viewport={'width': W, 'height': HH})
    hp = os.path.join(TMP, 'pagina2.html'); open(hp, 'w').write(PAGE)
    pg.goto('file://' + hp); pg.wait_for_timeout(300)
    return b, pg

def checar(v):
    from playwright.sync_api import sync_playwright
    import render_check as RC
    erros = []
    cta0 = min([c['t0'] for c in v.ctas] or [1e9])
    for c in v.cards:
        n = palavras(c)
        vis = (min(c['t1'], cta0) + SOBRA - c['t0']) - (0.0 if c.get('hook') else 0.45) - 0.28
        if vis < 0.35 * n - 1e-6:
            erros.append(f"{v.id} leitura curta: '{' / '.join(c['lines'])}' {n} palavras em {vis:.2f}s (mín {0.35*n:.2f}s)")
    for c in v.ctas:
        n = palavras(c); dur = c['t1'] - c['t0']
        if not (3.5 - 1e-6 <= dur <= 4.05): erros.append(f'{v.id} CTA com {dur:.2f}s (regra: 3,5–4 s)')
        if 0.35 * n + 1.2 > dur - 0.2 + 1e-6: erros.append(f'{v.id} CTA: título longo demais pra {dur:.1f}s')
    for c in v.cards + v.ctas:
        lns = [_limpa(l).strip() for l in c['lines']]
        for l in lns:
            ult = re.sub(r'[,.:;!?…]', '', l.split()[-1]).lower()
            if ult in PREPS: erros.append(f"{v.id} linha termina em '{ult}': '{l}'")
        for nm in NOMES:
            for a, b2 in zip(lns, lns[1:]):
                junto = (a + ' ' + b2).lower()
                if nm in junto and nm not in a.lower() and nm not in b2.lower():
                    erros.append(f"{v.id} nome partido na quebra de linha: '{nm}' em {lns}")
    with sync_playwright() as p:
        b, pg = _browser(p)
        for c in v.cards + v.ctas:
            t = min(c['t1'] - 0.2, c['t0'] + 1.6)
            pg.evaluate('s=>window.R(s)', v.estado(t))
            m = pg.evaluate('()=>window.MEDE()')
            for e in m['txt']:
                if e['x0'] < 139.5 or e['x1'] > 940.5 or e['y0'] < 149.5 or e['y1'] > 1500.5:
                    erros.append(f"{v.id} t={t:.2f} fora da zona segura: '{e['txt']}' x {e['x0']:.0f}-{e['x1']:.0f} y {e['y0']:.0f}-{e['y1']:.0f}")
                if 'ln' in e['cls'] and (e['y1'] - e['y0']) > e['fs'] * 1.5:
                    erros.append(f"{v.id} t={t:.2f} linha quebrou: '{e['txt']}'")
                if m['scr'] and 'ln' in e['cls'] and e['y1'] > m['scr']['y0'] - 8 and e['x1'] > m['scr']['x0'] and e['x0'] < m['scr']['x1']:
                    erros.append(f"{v.id} t={t:.2f} texto encosta na tela do app: '{e['txt']}'")
        viradas = sorted(set([c['t1'] for c in v.cards] + [c['t0'] for c in v.cards] + [c['t0'] for c in v.ctas]))
        for tv in viradas:
            for dt in (-0.05, 0.0, 0.05, 0.12):
                tt = tv + dt
                if not (0 <= tt < v.dur): continue
                s = v.estado(tt)
                if not (s['txt'] or s['ph'] or s['gfx'] or 'i1' in s['bg']):
                    erros.append(f'{v.id} quadro vazio em {tt:.2f}s')
        for f in v.fones:
            alvos = []
            for s in f.segs:
                for c in s.get('calls', []):
                    alvos += [(s, c, (c['t'][0] + c['t'][1]) / 2, 'meio'), (s, c, c['t'][1] - 1.0 / FPS, 'saída'), (s, c, c['t'][0], 'entrada')]
            if f.voo:
                alvos.append((f.segs[f.voo.get('seg', 0)], dict(box=f.voo['box']), f.voo['ate'] - 1.0 / FPS, 'pouso do gancho'))
            for s, c, t, quando in alvos:
                st = v.estado(t)
                pg.evaluate('s=>window.R(s)', st)
                m = pg.evaluate('()=>window.MEDE()')
                if quando == 'meio':
                    if m['call'] and (m['call']['x0'] < 139 or m['call']['x1'] > 941 or m['call']['y0'] < 150 or m['call']['y1'] > 1500):
                        erros.append(f"{v.id} t={t:.2f} recorte fora da zona: {m['call']}")
                    tops = [e['y1'] for e in m['txt'] if 'ln' in e['cls']]
                    if m['call'] and tops and m['call']['y0'] < max(tops) + 10:
                        erros.append(f"{v.id} t={t:.2f} recorte encosta no texto")
                    continue
                if not m['call'] or not st['ph']: continue
                cx = (int(m['call']['x0']) + 4, int(m['call']['y0']) + 4, int(m['call']['x1']) - 4, int(m['call']['y1']) - 4)
                a = os.path.join(TMP, f'fant_com_{v.id}_{os.getpid()}.png'); bb = os.path.join(TMP, f'fant_sem_{v.id}_{os.getpid()}.png')
                pg.evaluate('s=>window.R(s)', dict(st, txt='')); pg.screenshot(path=a)
                st_sem = dict(st, txt='', call=None); st_sem['ph'] = dict(st['ph']); st_sem['ph'].pop('mask', None)
                pg.evaluate('s=>window.R(s)', st_sem); pg.screenshot(path=bb)
                d = RC.fantasma(a, bb, cx)
                if d > RC.LIMIAR_FANTASMA:
                    erros.append(f"{v.id} t={t:.2f} FANTASMA na {quando} do recorte {c['box']}: diferença {d:.1f} (limite {RC.LIMIAR_FANTASMA})")
        b.close()
    return erros

def quadros(v, tempos, pasta):
    from playwright.sync_api import sync_playwright
    os.makedirs(pasta, exist_ok=True); out = []
    with sync_playwright() as p:
        b, pg = _browser(p)
        for t in tempos:
            pg.evaluate('s=>window.R(s)', v.estado(t))
            f = os.path.join(pasta, f'{v.id}_{t:06.2f}.jpg'); pg.screenshot(path=f, type='jpeg', quality=92); out.append(f)
        b.close()
    return out

def render_video(v, saida_mudo):
    from playwright.sync_api import sync_playwright
    n = int(round(v.dur * FPS))
    tmp = saida_mudo[:-4] + '.tmp.mp4'
    enc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-movflags', '+faststart', tmp],
                           stdin=subprocess.PIPE)
    with sync_playwright() as p:
        b, pg = _browser(p)
        for i in range(n):
            pg.evaluate('s=>window.R(s)', v.estado(i / FPS))
            enc.stdin.write(pg.screenshot(type='jpeg', quality=93))
            if i % 150 == 0: print(f'{v.id} quadro {i}/{n}', flush=True)
        b.close()
    enc.stdin.close()
    if enc.wait() != 0: raise RuntimeError('ffmpeg falhou')
    os.replace(tmp, saida_mudo)

# ---------------------------------------------------------------- áudio (efeitos; sem música)
SR = 48000
def _env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)

def _lp(x, fc):
    fc = np.broadcast_to(np.asarray(fc, float), x.shape)
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); acc = 0.0
    for i in range(len(x)):
        acc = (1 - a[i]) * x[i] + a[i] * acc; y[i] = acc
    return y

def _rosa(n, rng):
    w = rng.standard_normal(n + 4096)
    f = np.fft.rfft(w); k = np.arange(len(f)).astype(float); k[0] = 1
    x = np.fft.irfft(f / np.sqrt(k))[:n]
    return x / (np.abs(x).max() + 1e-9)

_SEMENTES = dict(whoosh=11, whoosh_leve=12, pop=13, clique=14, chave=15, notificacao=16, impacto=17, alerta=18)

def sfx(nome):
    rng = np.random.default_rng(_SEMENTES.get(nome, 1))
    if nome in ('whoosh', 'whoosh_leve'):
        d = 0.55; n = int(d * SR); t = np.arange(n) / SR
        x = _rosa(n, rng)
        fc = 250 + 2600 * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
        y = _lp(_lp(x, fc), fc) - _lp(x, 140)
        env = np.sin(np.pi * np.clip(t / d, 0, 1) ** 0.75) ** 2
        y = y * env / (np.abs(y * env).max() + 1e-9)
        L = y * (0.75 + 0.25 * t / d); R = y * (1.0 - 0.25 * t / d)
        g = 0.45 if nome == 'whoosh' else 0.26
        return np.stack([L, R], 1) * g
    if nome == 'pop':
        n = int(0.09 * SR); t = np.arange(n) / SR
        y = np.sin(2 * np.pi * (380 + 120 * np.exp(-t / 0.01)) * t) * _env(n, 0.003, 0.03)
        return np.stack([y, y], 1) * 0.42
    if nome == 'clique':
        n = int(0.04 * SR); t = np.arange(n) / SR
        y = _lp(rng.standard_normal(n), 3500) * _env(n, 0.0004, 0.0035)
        y += 0.35 * np.sin(2 * np.pi * 1200 * t) * _env(n, 0.0004, 0.006)
        return np.stack([y, y], 1) * 0.55
    if nome == 'chave':
        a = sfx('clique'); n = int(0.16 * SR); y = np.zeros((n, 2)); y[:len(a)] += a
        i = int(0.09 * SR); y[i:i + len(a)] += a * 0.8
        return y * 0.9
    if nome == 'notificacao':
        n = int(1.0 * SR); t = np.arange(n) / SR; y = np.zeros(n)
        for f0, t0 in ((1046.5, 0.0), (1568.0, 0.12)):
            tt = np.clip(t - t0, 0, None); on = (t >= t0)
            for h, a in ((1, 1.0), (2, 0.18), (3, 0.05)):
                y += on * a * np.sin(2 * np.pi * f0 * h * tt) * np.minimum(1, tt / 0.004) * np.exp(-tt / (0.28 / h))
        return np.stack([y, y], 1) * 0.26
    if nome == 'impacto':
        n = int(0.8 * SR); t = np.arange(n) / SR
        f = 42 + 55 * np.exp(-t / 0.08)
        y = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.006, 0.28)
        y += _lp(rng.standard_normal(n), 500) * _env(n, 0.002, 0.03) * 0.5
        return np.stack([y, y], 1) * 0.85
    if nome == 'alerta':
        n = int(0.4 * SR); t = np.arange(n) / SR; y = np.zeros(n)
        for t0 in (0.0, 0.16):
            tt = t - t0; on = (tt >= 0) & (tt < 0.1)
            y += on * np.sin(2 * np.pi * 880 * tt) * np.minimum(1, np.clip(tt, 0, None) / 0.006) * np.minimum(1, np.clip(0.1 - tt, 0, None) / 0.03)
        return np.stack([y, y], 1) * 0.14
    raise KeyError(nome)

def mixar(v, wav):
    n = int(round(v.dur * SR)); mix = np.zeros((n, 2))
    for t, nome, g in v.sfx:
        x = sfx(nome) * (10 ** (g / 20)); i = int(t * SR)
        m = min(len(x), n - i)
        if m > 0 and i >= 0: mix[i:i + m] += x[:m]
    pico = np.abs(mix).max()
    if pico > 0: mix *= 0.5 / pico
    import wave
    with wave.open(wav, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(mix, -1, 1) * 32767).astype('<i2').tobytes())

PRE = 'alimiter=limit=0.30:attack=0.5:release=40:level=disabled,'

def medir(arq):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', arq, '-af', 'loudnorm=I=-14:TP=-1.5:print_format=json', '-f', 'null', '-'],
                       capture_output=True, text=True)
    j = json.loads(r.stderr[r.stderr.rindex('{'):r.stderr.rindex('}') + 1])
    return float(j['input_i']), float(j['input_tp'])

def loudnorm(wav_in, wav_out, alvo=-14.0, pre=PRE):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', wav_in, '-af', pre + f'loudnorm=I={alvo}:TP=-2:LRA=11:print_format=json', '-f', 'null', '-'],
                       capture_output=True, text=True)
    j = json.loads(r.stderr[r.stderr.rindex('{'):r.stderr.rindex('}') + 1])
    af = pre + (f"loudnorm=I={alvo}:TP=-2:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
                f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,aresample=48000,"
                f"alimiter=limit=0.70:attack=1:release=60:level=disabled,lowpass=f=17000")
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', wav_in, '-af', af, '-ar', '48000', wav_out], check=True)
    for _ in range(3):
        i, tp = medir(wav_out)
        if abs(i - alvo) <= 0.3: break
        tmp = wav_out[:-4] + '_c.wav'
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', wav_out, '-af',
                        f'volume={alvo - i:.2f}dB,alimiter=limit=0.70:attack=1:release=60:level=disabled', '-ar', '48000', tmp], check=True)
        os.replace(tmp, wav_out)

def folha(video, saida, fps=2, col=8):
    from PIL import ImageFont
    d = os.path.join(TMP, 'folha_tmp_' + os.path.basename(saida)[:2] + f'_{os.getpid()}'); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', video, '-vf', f'fps={fps},scale=270:480', os.path.join(d, '%04d.png')], check=True)
    fs = sorted(os.listdir(d)); rows = math.ceil(len(fs) / col)
    s = Image.new('RGB', (col * 276, rows * 504), (255, 255, 255)); dr = ImageDraw.Draw(s)
    try: fnt = ImageFont.truetype('/home/claude/corretores/fontes/poppins-latin-600-normal.ttf', 16)
    except Exception: fnt = None
    for k, f in enumerate(fs):
        im = Image.open(os.path.join(d, f)); x = (k % col) * 276; y = (k // col) * 504
        s.paste(im, (x + 3, y + 22)); dr.text((x + 4, y + 2), f'{(k + 0.5) / fps:.2f}s', fill=(200, 0, 0), font=fnt)
    s.save(saida, quality=86)
    shutil.rmtree(d, ignore_errors=True)

def _mux(mudo, wav, saida):
    tmp = saida[:-4] + '.tmp.mp4'
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', mudo, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-shortest', '-movflags', '+faststart', tmp], check=True)
    os.replace(tmp, saida)

def render(v, so_audio=False):
    os.makedirs(OUT, exist_ok=True)
    base = os.path.join(OUT, f'{v.id} - {v.titulo}')
    mudo = os.path.join(TMP, f'{v.id}_mudo2.mp4')
    if not so_audio: render_video(v, mudo)
    w1 = os.path.join(TMP, f'{v.id}_sfx.wav'); w2 = os.path.join(TMP, f'{v.id}_sfx_ln.wav')
    mixar(v, w1); loudnorm(w1, w2)
    final = base + ' - sem musica.mp4'
    _mux(mudo, w2, final)
    folha(final, os.path.join(OUT, f'{v.id} - folha.jpg'))
    i, tp = medir(final)
    print(f'ok {final}  {v.dur:.2f}s  áudio {i:.1f} LUFS / TP {tp:.1f}')
    return final

def trilha(v, faixa):
    """Versão COM trilha: música a -14 LUFS, efeitos ~6 dB abaixo da música, fade de entrada/saída, limitador."""
    mudo = os.path.join(TMP, f'{v.id}_mudo2.mp4')
    if not os.path.exists(mudo): raise FileNotFoundError('renderize antes: ' + mudo)
    w_sfx = os.path.join(TMP, f'{v.id}_sfx.wav'); mixar(v, w_sfx)
    w_sfx20 = os.path.join(TMP, f'{v.id}_sfx_-20.wav'); loudnorm(w_sfx, w_sfx20, alvo=-20.0)
    w_mus = os.path.join(TMP, f'{v.id}_mus.wav')
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-stream_loop', '-1', '-i', faixa, '-t', f'{v.dur:.3f}', '-af',
                    f'afade=t=in:d=0.25,afade=t=out:st={v.dur-0.9:.3f}:d=0.9', '-ar', '48000', '-ac', '2', w_mus], check=True)
    w_mus14 = os.path.join(TMP, f'{v.id}_mus_-14.wav'); loudnorm(w_mus, w_mus14, alvo=-14.0, pre='')
    w_mix = os.path.join(TMP, f'{v.id}_trilha.wav')
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', w_mus14, '-i', w_sfx20, '-filter_complex',
                    '[0:a][1:a]amix=inputs=2:normalize=0,alimiter=limit=0.70:attack=1:release=80:level=disabled', '-ar', '48000', w_mix], check=True)
    final = os.path.join(OUT, f'{v.id} - {v.titulo}.mp4')
    _mux(mudo, w_mix, final)
    i, tp = medir(final)
    print(f'ok {final}  com trilha  {i:.1f} LUFS / TP {tp:.1f}')

# ================================================================ ROTEIROS · rodada 2
# Caixas dos recortes (px no espaço da tela 1179 de largura; páginas de rolagem = coordenada da página)
BOX_SAUDE_ALERTA = (100, 1806, 1080, 2042)    # "Troca vencida · Vela de ignição · Passou 300 km" (botão Ver em x 959)
BOX_SAUDE_CORRENTE = (50, 3780, 1129, 4025)   # "Lubrificar e ajustar a corrente · Aos 29.900 km · faltam 100"
BOX_SAUDE_OLEO = (50, 4705, 1129, 4882)       # "Óleo do motor · Em dia · Aos 33.100 km · faltam 3.300"
BOX_SAUDE_3 = (50, 4705, 1129, 5252)          # Óleo + Pastilhas/sapatas de freio + Pneus
BOX_21 = (30, 1352, 1150, 1650)               # folha "Vela de ignição · Era para trocar aos 29.500 km"
BOX_HIST_OLEO = (48, 2939, 1131, 3439)        # "Troca de óleo e filtro · 25/08/2026 · 27.100 km · R$ 120,00"
BOX_LISTA_OLEO = (48, 1560, 1131, 1785)       # "Óleo do motor · SAE 10W-30 API SL+ JASO MA"
BOX_LISTA_PNEU = (48, 3415, 1131, 3720)       # "Pneu traseiro · 29 psi sozinho · 33 psi com garupa · pneu frio"
BOX_DOCS = (48, 1496, 1131, 2041)             # "CRLV digital" + "CNH"
BOX_MARCO27 = (48, 655, 1131, 950)            # (tela parada 27) "30.000 km · Faltam 200 km · 20 itens a confirmar"
BOX_28 = (40, 330, 1150, 832)                 # folha "Alta prioridade · Lubrificar e ajustar a corrente · ... 29.900 km"
BOX_28_LEMBRETE = (40, 612, 1150, 832)        # "Lubrificar quando a moto estiver com 29.900 km · a cada 1.000 km"
BOX_29_TEMPO = (585, 660, 1115, 1035)         # card "Tempo · 4 itens · 1 em atenção"
BOX_29_BATERIA = (48, 1340, 1131, 1535)       # "Bateria · Tempo · Analisar · sem histórico"
BOX_22_OLEO = (60, 945, 1130, 1080)           # folha "Novo registro" · "Óleo do motor · Trocar"
BOX_11_CORRENTE = (48, 1688, 1131, 2272)      # "Corrente de transmissão" (cuidados do manual)

def _navy(): return lambda tl, tg: bg_navy(tg)
def _azul(): return lambda tl, tg: bg_azul(tg)

def foto(arq, dur, z0, z1, fx0, fy0, fx1=None, fy1=None, curva_out=False, tremor=None, **kw):
    """Cena de foto com Ken Burns. curva_out: movimento mais forte logo no começo (1º segundo). tremor: s do 'barulho'."""
    fx1 = fx0 if fx1 is None else fx1; fy1 = fy0 if fy1 is None else fy1
    def f(tl, tg):
        tt = dur * eout(clamp(tl / dur)) if curva_out else tl
        s = bg_foto(arq, tt, dur, z0, z1, fx0, fy0, fx1, fy1, **kw)
        if tremor is not None and tl > tremor:
            s['bg']['i1']['left'] += 16 * math.sin((tl - tremor) * 55) * math.exp(-(tl - tremor) / 0.13)
        return s
    return f

def sons_cta(v, t):
    v.som(t, 'whoosh', -3); v.som(t + 0.55, 'pop', -3); v.som(t + 0.85, 'pop', -9); v.som(t + 2.2, 'clique', -6)

# ---------------------------------------------------------------- grafismos (sobre foto, nunca sozinhos em fundo liso)
def _fmt(n): return f'{n:,.0f}'.replace(',', '.')

def g_v4_gancho(tl):
    """Contraste: a pastilha que ele adiou (no texto) × o disco novo (entra em 1,5 s). Rodapé com a fonte exata."""
    kl = eout(clamp((tl - 1.5) / 0.35)); k = eback(clamp((tl - 1.75) / 0.45)); op = clamp((tl - 1.75) / 0.12)
    kf = eout(clamp((tl - 2.2) / 0.4))
    return (f"<div style='position:absolute;left:{540-380}px;top:{940-380}px;width:760px;height:760px;border-radius:50%;"
            f"background:radial-gradient(circle, rgba(0,0,0,{.62*kl:.2f}) 0%, rgba(0,0,0,0) 68%)'></div>"
            f"<div class=med style='position:absolute;left:144px;width:792px;top:800px;text-align:center;font-family:j700;font-size:52px;"
            f"letter-spacing:-.02em;color:#fff;opacity:{kl:.3f};transform:translateY({(1-kl)*20:.0f}px);text-shadow:0 6px 30px rgba(0,0,0,.85)'>{V4_NUM['rotulo']}</div>"
            f"<div class=med style='position:absolute;left:144px;width:792px;top:880px;text-align:center;font-family:j800;font-size:150px;"
            f"letter-spacing:-.04em;line-height:1;color:{VERM};opacity:{op:.3f};transform:scale({max(.01,k):.3f});text-shadow:0 8px 40px rgba(0,0,0,.75)'>{V4_NUM['peca']}</div>"
            f"<div class=med style='position:absolute;left:144px;width:792px;top:1350px;text-align:center;font-family:j500;font-size:26px;line-height:1.4;padding:12px 18px;border-radius:16px;"
            f"background:rgba(0,0,0,.55);color:#eef3ff;opacity:{kf:.3f};white-space:normal'>{H.escape(V4_NUM['rodape'])}</div>")

def g_hodometro(tl):
    km = int(lerp(22400, 28900, ease(clamp((tl - 0.25) / 3.2))) // 10 * 10)
    red = clamp((tl - 3.3) / 0.4)
    caixas = ''
    for ch in _fmt(km):
        if ch == '.':
            caixas += "<div style='width:20px;display:flex;align-items:flex-end;justify-content:center;padding-bottom:22px;font-family:j700;font-size:70px;color:#9fb3d1'>.</div>"; continue
        caixas += (f"<div style='width:106px;height:150px;border-radius:20px;background:linear-gradient(#0d1b33,#060d1a);"
                   f"box-shadow:0 0 0 2px rgba(82,169,254,.35) inset,0 18px 40px rgba(0,0,0,.55);display:flex;align-items:center;justify-content:center;"
                   f"font-family:j700;font-size:96px;color:rgb(255,{int(lerp(255,69,red))},{int(lerp(255,58,red))})'>{ch}</div>")
    k = eout(clamp(tl / 0.4))
    return (f"<div style='position:absolute;left:0;right:0;top:1010px;display:flex;justify-content:center;gap:10px;opacity:{k:.3f};transform:translateY({(1-k)*30:.0f}px)'>{caixas}</div>"
            f"<div class=med style='position:absolute;left:140px;width:800px;top:1180px;text-align:center;font-family:j600;font-size:38px;color:#e6eeff;"
            f"text-shadow:0 4px 18px rgba(0,0,0,.8);opacity:{k:.3f}'>km rodados</div>")

# ============================================================ V1 · tela do app · motoboy/entregador · controle · ~18,8 s
def V1():
    v = Video('V1', 'Controle', 19.0)
    v.bg(0, 19.0, _navy())
    S = 'rolagem/02-saude'
    v.fone(Fone([
        dict(t0=0.55, t1=5.4, tela=S, rola=True, abas='saude', keys=[(0.55, 0), (2.6, 0), (3.4, 1046)],
             calls=[dict(box=BOX_SAUDE_ALERTA, t=(3.55, 5.0), cor='vermelho', dy=-30)],
             tap=dict(t=5.05, x=959, y=1924)),
        dict(t0=5.4, t1=8.6, tela='21-item-atrasado', trans='sobe', folha_y=1185,
             calls=[dict(box=BOX_21, t=(6.0, 8.35), cor='vermelho', k=1.25, dy=-40)]),
        dict(t0=8.6, t1=15.0, tela=S, rola=True, abas='saude', trans='desce',
             keys=[(8.6, 1046), (9.0, 1046), (9.8, 2963), (11.8, 2963), (12.6, 3872)],
             calls=[dict(box=BOX_SAUDE_CORRENTE, t=(10.0, 11.75), dy=-30), dict(box=BOX_SAUDE_3, t=(12.8, 14.6), dy=-40)]),
    ], voo=dict(box=BOX_SAUDE_ALERTA, ate=1.55, parte=0.6, largura=880, y=1000, cor='vermelho', mascara='rgb(11,12,15)')))
    v.card(0, 2.5, hook=True, lines=['Moto parada é', 'dia sem [ganhar].'], y=190, size=84)
    v.card(2.5, 5.4, lines=['O que vence primeiro', 'aparece [primeiro].'], y=200)
    v.card(5.4, 8.6, lines=['E mostra quando', '[era pra trocar].'], y=200)
    v.card(8.6, 11.8, lines=['Chegando a hora?', 'O app [avisa antes].'], y=200)
    v.card(11.8, 15.0, lines=['Óleo, freio, pneus:', 'tudo [no seu km].'], y=200)
    v.cta(15.0, lines=['Moto de trabalho', '[sob controle].'])
    v.som(0.0, 'alerta', 0); v.som(0.0, 'impacto', -9); v.som(0.55, 'whoosh_leve', -4); v.som(1.5, 'clique', -8)
    v.som(2.6, 'whoosh_leve', -9); v.som(3.55, 'pop', -4); v.som(5.05, 'clique', -2); v.som(5.4, 'whoosh_leve', -6)
    v.som(6.0, 'pop', -4); v.som(8.6, 'whoosh_leve', -6); v.som(10.0, 'notificacao', -2); v.som(12.6, 'whoosh_leve', -9); v.som(12.8, 'pop', -4)
    sons_cta(v, 15.0)
    return v

# ============================================================ V2 · tela do app · hobby · orgulho · ~30,8 s
FOTO_V2 = '12900279.jpg'     # moto na estrada de serra (POV do guidão); "HIMALAYAN" do tanque fica no escuro de baixo

def V2():
    v = Video('V2', 'Orgulho da moto', 30.75)
    v.bg(0, 3.4, foto(FOTO_V2, 3.4, 1.52, 1.44, 0.5, 0.0, 0.5, 0.0, curva_out=True, brilho=1.04, topo=0.6, base=0.7))
    v.bg(3.4, 23.6, bg_foto_fundo(FOTO_V2, 0.5, 0.0, 1.4))
    v.bg(23.6, 26.75, foto(FOTO_V2, 3.2, 2.05, 2.2, 0.45, 0.45, 0.46, 0.44, brilho=1.04, topo=0.6, base=0.9))   # painel dela, em km/h
    v.bg(26.75, 30.75, bg_foto_fundo(FOTO_V2, 0.5, 0.0, 1.4))
    v.fone(Fone([
        dict(t0=3.15, t1=8.6, tela='rolagem/06-historico', rola=True, abas='nenhuma', keys=[(3.15, 0), (4.3, 0), (5.4, 2550)],
             calls=[dict(box=BOX_HIST_OLEO, t=(5.6, 8.35), dy=-30)]),
        dict(t0=8.6, t1=13.6, tela='rolagem/10-lista-revisao', rola=True, abas='nenhuma', keys=[(8.6, 0), (9.2, 0), (10.2, 900)],
             calls=[dict(box=BOX_LISTA_OLEO, t=(10.4, 13.35), dy=-30)]),
        dict(t0=13.6, t1=18.6, tela='rolagem/07-documentos', rola=True, abas='nenhuma', keys=[(13.6, 0), (14.2, 0), (15.2, 850)],
             calls=[dict(box=BOX_DOCS, t=(15.4, 18.35), dy=-20)]),
        dict(t0=18.6, t1=23.6, tela='27-marco-30000', topo='cab',
             calls=[dict(box=BOX_MARCO27, t=(19.4, 23.3), dy=-20)]),
    ]))
    v.card(0, 3.4, hook=True, lines=['Moto bem cuidada', 'tem [histórico].'], sup='A sua tem?', y=190, size=80)
    v.card(3.4, 8.6, lines=['Cada serviço salvo,', 'com [data, km e valor].'], y=200)
    v.card(8.6, 13.6, lines=['O manual dela', '[na palma da mão].'], y=200)
    v.card(13.6, 18.6, lines=['CRLV, CNH e seguro', '[num lugar só].'], y=200)
    v.card(18.6, 23.6, lines=['A próxima revisão', '[já está no radar].'], y=200)
    v.card(23.6, 26.75, lines=['Seu capricho,', '[registrado].'], y=200, size=80)
    v.cta(26.75, lines=['Moto cuidada', '[se vê de longe].'])
    v.som(0.0, 'whoosh', -4); v.som(3.2, 'whoosh_leve', -4); v.som(4.3, 'whoosh_leve', -10); v.som(5.6, 'pop', -4)
    for t in (8.6, 13.6, 18.6): v.som(t, 'whoosh_leve', -7)
    for t in (10.4, 15.4, 19.4): v.som(t, 'pop', -4)
    v.som(23.6, 'whoosh', -6)
    sons_cta(v, 26.75)
    return v

# ============================================================ V3 · historinha · quem vai trabalhar de moto · medo de prejuízo · ~19,4 s
FOTO_V3 = '15802617.jpg'           # moto de trabalho parada na calçada, sol da manhã (sem pessoa)

def V3():
    v = Video('V3', 'Corrente no caminho do trabalho', 19.6)
    v.bg(0, 3.4, foto(FOTO_V3, 3.4, 1.34, 1.04, 0.62, 0.7, 0.6, 0.64, curva_out=True, brilho=1.08, topo=0.62, base=0.3))
    v.bg(3.4, 6.8, foto(FOTO_V3, 3.4, 1.38, 1.48, 0.86, 0.84, 0.88, 0.84, brilho=0.92, sat=0.85, topo=0.62, base=0.25))   # roda traseira da cub (neutro)
    v.bg(6.8, 10.2, foto(FOTO_V3, 3.4, 1.0, 1.06, 0.62, 0.6, 0.66, 0.6, brilho=0.95, sat=0.8, topo=0.62, base=0.3))
    v.bg(10.2, 19.6, bg_foto_fundo(FOTO_V3, 0.58, 0.6, 1.25, brilho=0.4))
    v.fone(Fone([dict(t0=10.0, t1=15.6, tela='28-item-proximo', topo='folha',
                      calls=[dict(box=BOX_28, t=(10.9, 12.45), k=1.25, dy=-20), dict(box=BOX_28_LEMBRETE, t=(12.95, 15.3), k=1.15, dy=5)])]))
    v.card(0, 3.4, hook=True, kicker='Segunda-feira, 7h40', kicker_red=True, lines=['A corrente [escapou]', 'indo pro trabalho.'], y=190, size=80)
    v.card(3.4, 6.8, lines=['Seca, folgada…', 'e [ninguém ajustou].'], y=200, size=80)
    v.card(6.8, 10.2, lines=['Atraso, guincho', 'e [dia perdido].'], y=200, size=80)
    v.card(10.2, 12.6, lines=['O MinhaMoto', '[teria avisado].'], y=200)
    v.card(12.6, 15.6, lines=['Lubrificar e ajustar', '[no km certo].'], y=200)
    v.cta(15.6, lines=['A moto avisa tarde.', 'O MinhaMoto, [antes].'])
    v.som(0.0, 'impacto', -6); v.som(0.05, 'whoosh_leve', -8); v.som(3.4, 'whoosh', -6); v.som(6.8, 'whoosh_leve', -6); v.som(7.0, 'impacto', -12)
    v.som(10.0, 'whoosh_leve', -5); v.som(10.9, 'notificacao', -1); v.som(12.95, 'pop', -4)
    sons_cta(v, 15.6)
    return v

# ============================================================ V4 · historinha · motoboy · economia · ~31,2 s (números em V4_NUM)
FOTO_V4A = '14534738.jpg'   # ferramentas na bancada (oficina)
FOTO_V4B = '6664916.jpg'    # moto de rua vermelha, painel digital (km); o chaveiro com marca fica fora do quadro
BOX_SAUDE_PAST = (50, 4889, 1129, 5071)       # "Pastilhas / sapatas de freio · Em dia · Aos 40.600 km · faltam 10.800"
BOX_SINAIS_FREIO = (48, 4241, 1131, 4662)     # "Freio esponjoso ou curso longo do manete · Pare agora · ... pastilhas no fim"
BOX_HIST_PAST = (48, 3587, 1131, 4207)        # "Pastilhas dianteiras e fluido de freio · 06/07/2026 · 25.600 km · R$ 150,00"

def V4():
    # O banco não tem foto de disco riscado nem de pastilha gasta: as cenas da causa usam planos neutros
    # (painel da moto de rua e bancada de oficina), nunca uma peça perfeita que desminta o texto (regra 15).
    v = Video('V4', 'Pastilha adiada risca o disco', 31.9)
    v.bg(0, 4.5, foto(FOTO_V4A, 4.5, 1.16, 1.02, 0.5, 0.45, 0.5, 0.5, curva_out=True, brilho=1.2, topo=0.6, base=0.45))
    v.bg(4.5, 8.5, foto(FOTO_V4B, 4.0, 1.75, 1.9, 0.6, 0.36, 0.62, 0.35, brilho=0.95, topo=0.62, base=0.85))   # painel com o km rodado
    v.bg(8.5, 12.5, foto(FOTO_V4B, 4.0, 1.3, 1.42, 0.22, 0.84, 0.25, 0.82, brilho=0.85, topo=0.62, base=0.3))
    v.bg(12.5, 15.9, foto(FOTO_V4A, 3.4, 1.7, 1.85, 0.3, 0.7, 0.32, 0.68, brilho=1.05, sat=0.8, topo=0.62, base=0.3, tremor=0.5))
    v.bg(15.9, 31.9, _navy())
    v.gfx(0, 4.5, g_v4_gancho)
    v.fone(Fone([
        dict(t0=15.7, t1=20.1, tela='rolagem/02-saude', rola=True, abas='saude', keys=[(15.7, 0), (16.7, 0), (17.7, 3800)],
             calls=[dict(box=BOX_SAUDE_PAST, t=(17.9, 19.85), dy=-30)]),
        dict(t0=20.1, t1=24.1, tela='rolagem/12-sinais-problema', rola=True, abas='nenhuma', keys=[(20.1, 3540)],
             calls=[dict(box=BOX_SINAIS_FREIO, t=(20.8, 23.85), k=1.18, dy=-10, cor='vermelho')]),
        dict(t0=24.1, t1=27.9, tela='rolagem/06-historico', rola=True, abas='nenhuma', keys=[(24.1, 2890)],
             calls=[dict(box=BOX_HIST_PAST, t=(24.7, 27.65), dy=-20)]),
    ]))
    v.card(0, 4.5, hook=True, lines=['Pastilha de freio:', f"[{V4_NUM['pastilha']}]. Ele adiou."], y=190, size=80,
           extra_txt=[V4_NUM['rotulo'] + ' ' + V4_NUM['peca']])
    v.card(4.5, 8.5, lines=['Rodando o dia todo,', 'a pastilha ficou', '[pra depois].'], y=200, size=76)
    v.card(8.5, 12.5, lines=['Gastou até o metal', 'e [riscou o disco].'], y=200, size=76)
    v.card(12.5, 15.9, lines=['Freio fraco, barulho…', 'e [disco novo].'], y=200, size=76)
    v.card(15.9, 20.1, lines=['O app mostra quando', '[trocar a pastilha].'], y=200)
    v.card(20.1, 24.1, lines=['E explica o sinal:', '[pastilha no fim].'], y=200)
    v.card(24.1, 27.9, lines=['Cada troca salva,', 'com [data e km].'], y=200)
    v.cta(27.9, lines=['Cuidar [custa menos]', 'que consertar.'])
    v.som(0.0, 'whoosh', -4); v.som(1.75, 'impacto', -3); v.som(1.8, 'alerta', -2)
    v.som(4.5, 'whoosh_leve', -6); v.som(8.5, 'whoosh_leve', -6); v.som(12.5, 'whoosh_leve', -6); v.som(13.0, 'impacto', -2)
    v.som(15.7, 'whoosh', -6); v.som(17.9, 'pop', -4); v.som(20.1, 'whoosh_leve', -6); v.som(20.8, 'alerta', -3)
    v.som(24.1, 'whoosh_leve', -6); v.som(24.7, 'pop', -4)
    sons_cta(v, 27.9)
    return v

# ============================================================ V5 · POV · hobby/fim de semana · medo de prejuízo · ~21,2 s
FOTO_V5 = '10196163.jpg'   # moto de passeio parada na garagem, clara (sem pessoa, sem marca legível)

def V5():
    v = Video('V5', 'Moto parada também vence', 23.1)
    v.bg(0, 4.0, foto(FOTO_V5, 4.0, 1.12, 1.0, 0.42, 0.56, 0.42, 0.58, curva_out=True, brilho=1.02, topo=0.55, base=0.2))
    v.bg(4.0, 8.0, foto(FOTO_V5, 4.0, 1.75, 1.85, 0.36, 0.83, 0.36, 0.8, brilho=1.0, topo=0.55, base=0.2))
    v.bg(8.0, 12.6, foto(FOTO_V5, 4.6, 1.9, 2.0, 0.38, 0.5, 0.39, 0.52, brilho=1.02, topo=0.55, base=0.2))
    v.bg(12.6, 23.1, bg_foto_fundo(FOTO_V5, 0.42, 0.55, 1.2, brilho=0.42))
    v.fone(Fone([dict(t0=12.4, t1=19.1, tela='29-manutencao-tempo', topo='cab',
                      calls=[dict(box=BOX_29_TEMPO, t=(13.3, 15.9), k=1.35, dy=-10), dict(box=BOX_29_BATERIA, t=(16.4, 18.8), dy=-30)])]))
    v.card(0, 4.0, hook=True, align='center', lines=['POV: domingo,', 'rolê marcado…', 'e a moto [não pega].'], y=190, size=80)
    v.card(4.0, 8.0, align='center', lines=['Bateria arriada.', 'Ficou [parada]', 'o mês todo.'], y=190, size=80)
    v.card(8.0, 12.6, align='center', lines=['Parada, a moto', 'também [tem prazo].'], sup='Bateria, óleo, fluido de freio.', y=200, size=72)
    v.card(12.6, 16.15, align='center', lines=['O MinhaMoto mostra', 'o que vence', '[pelo tempo].'], y=170)
    v.card(16.15, 19.1, align='center', lines=['E o que já pede', '[atenção].'], y=170)
    v.cta(19.1, lines=['Seu domingo de rolê,', '[sem surpresa].'])
    v.som(1.6, 'chave', -2); v.som(2.6, 'chave', -4); v.som(4.0, 'whoosh_leve', -7); v.som(8.0, 'whoosh_leve', -7)
    v.som(12.4, 'whoosh', -6); v.som(13.3, 'pop', -4); v.som(16.4, 'pop', -4); v.som(16.5, 'notificacao', -4)
    sons_cta(v, 19.1)
    return v

# ============================================================ V6 · POV · iniciante · controle · ~31,4 s
FOTO_V6 = '30817486.jpg'           # trail com capacete no banco, garagem clara (sem pessoa)
FOTO_V6B = '25857998.jpg'          # pneu de trilha de perto (a placa fica acima do quadro)
FOTO_V6C = '37131862.jpg'           # corrente de perto (só no V6; a marca no tanque fica fora do quadro)
FOTO_V6D = '13060251.jpg'           # scooter de banco inteiro (garupa), rua clara
G6 = dict(sat=0.82, contraste=1.08, tinta='rgba(8,40,96,.16)')   # um tratamento de cor só na peça (regra 19)
def b6(arq): return round(clamp(112 / lum(arq), 0.8, 1.9), 2)

def V6():
    v = Video('V6', 'Primeira moto', 31.55)
    v.bg(0, 3.8, foto(FOTO_V6, 3.8, 1.18, 1.04, 0.47, 0.66, 0.47, 0.68, curva_out=True, brilho=b6(FOTO_V6), topo=0.6, base=0.2, **G6))
    v.bg(3.8, 8.2, foto(FOTO_V6B, 4.4, 1.45, 1.55, 0.6, 0.66, 0.6, 0.68, brilho=b6(FOTO_V6B), topo=0.62, base=0.2, **G6))
    v.bg(8.2, 12.80, foto(FOTO_V6C, 4.6, 1.25, 1.35, 0.8, 0.66, 0.77, 0.66, brilho=min(1.35, b6(FOTO_V6C)), topo=0.62, base=0.2, **G6))
    v.bg(12.80, 17.20, foto(FOTO_V6D, 4.4, 1.14, 1.22, 0.4, 0.9, 0.42, 0.9, brilho=b6(FOTO_V6D), topo=0.78, base=0.2, **G6))
    v.bg(17.20, 31.55, _azul())
    v.gfx(3.8, 8.20, lambda tl: tip_badge(1, 190, tl, 4.40))
    v.gfx(8.2, 12.80, lambda tl: tip_badge(2, 190, tl, 4.60))
    v.gfx(12.80, 17.20, lambda tl: tip_badge(3, 190, tl, 4.40))
    v.fone(Fone([
        dict(t0=17.00, t1=22.60, tela='rolagem/10-lista-revisao', rola=True, abas='nenhuma', keys=[(17.00, 0), (18.20, 0), (19.40, 2700)],
             calls=[dict(box=BOX_LISTA_PNEU, t=(19.60, 22.35), dy=-30)]),
        dict(t0=22.60, t1=27.55, tela='rolagem/11-cuidados', rola=True, abas='nenhuma', keys=[(22.60, 0), (23.20, 0), (24.30, 1290)],
             calls=[dict(box=BOX_11_CORRENTE, t=(24.50, 27.10), dy=-10)]),
    ]))
    v.card(0, 3.8, hook=True, align='center', lines=['3 erros de quem tem', 'a [primeira moto].'], y=200, size=76)
    v.card(3.8, 8.2, align='center', lines=['Calibrar com o pneu', '[quente] dá errado.'], y=320, size=76)
    v.card(8.2, 12.80, align='center', lines=['Esquecer a corrente:', 'ela pede óleo', '[a cada 1.000 km].'], y=320, size=76)
    v.card(12.80, 17.20, align='center', lines=['Levar garupa', 'na pressão de quem', 'anda [sozinho].'], y=320, size=76)
    v.card(17.20, 22.60, lines=['O MinhaMoto traz isso', '[do seu modelo].'], y=200)
    v.card(22.60, 27.55, lines=['Com o passo a passo', '[do manual].'], y=200)
    v.cta(27.55, lines=['Primeira moto,', '[zero achismo].'])
    v.som(0.0, 'whoosh', -4); v.som(0.1, 'pop', -6)
    for t in (3.8, 8.2, 12.80): v.som(t, 'whoosh_leve', -7); v.som(t + 0.05, 'pop', -4)
    v.som(17.00, 'whoosh', -6); v.som(19.60, 'pop', -4); v.som(22.60, 'whoosh_leve', -7); v.som(24.50, 'pop', -4)
    sons_cta(v, 27.55)
    return v

VIDEOS = dict(V1=V1, V2=V2, V3=V3, V4=V4, V5=V5, V6=V6)


if __name__ == '__main__':
    modo, vid = sys.argv[1], sys.argv[2]
    ids = list(VIDEOS) if vid == 'todos' else vid.split(',')
    for i in ids:
        v = VIDEOS[i]()
        if modo == 'check':
            er = checar(v); print(i, 'OK' if not er else 'ERROS'); [print('  ✗', e) for e in er]
        elif modo == 'prev':
            ts = [float(x) for x in sys.argv[3:]] or [0, 2, 5, 9, 13, 17]
            print('\n'.join(quadros(v, ts, os.path.join(TMP, 'prev'))))
        elif modo == 'audio':
            render(v, so_audio=True)
        elif modo == 'trilha':
            trilha(v, sys.argv[3])
        elif modo == 'render':
            er = checar(v)
            if er: print('\n'.join(er)); sys.exit(1)
            render(v)
