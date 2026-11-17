#!/usr/bin/env python3
"""Carrosséis (1080x1350) e stories (1080x1920) da direção v2, com o mesmo celular premium dos vídeos.
Render em 2x e redução LANCZOS pra nitidez máxima.
Uso: python3 estaticos.py [A|B|todos]
"""
import os, sys, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motor import CSS_FONTES, ASSETS, phone_html, still, ESTILOS, PAGINA
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
FOTOS = os.path.join(ASSETS, 'fotos')
ICON = os.path.join(ASSETS, 'icon.png'); SELOS = os.path.join(ASSETS, 'selos-lojas.png')

# CSS do celular reaproveitado da página de vídeo (mesmo acabamento)
CSS_PHONE = PAGINA.split('<style>')[1].split('</style>')[0] % dict(fontes='', **ESTILOS['A'])

BASE = """<!doctype html><html><head><meta charset=utf-8><style>%(fontes)s %(phone)s
html,body{width:%(w)dpx;height:%(h)dpx;overflow:hidden;background:#05070d}
.fill{position:absolute;inset:0}
.ph{position:absolute;left:50%%;width:0;height:0;perspective:2400px}
.ph #phone{position:absolute}
.capA{position:absolute;left:60px;right:60px;text-align:center;font-family:m900;text-transform:uppercase;color:#fff;
  -webkit-text-stroke:9px #000;paint-order:stroke fill;text-shadow:0 9px 0 rgba(0,0,0,.55),0 0 60px rgba(0,0,0,.7);line-height:1.05}
.capA .y{color:#FFD400}
.apoA{position:absolute;left:80px;right:80px;text-align:center;font-family:m800;color:#fff;text-shadow:0 4px 18px rgba(0,0,0,.8)}
.titB{position:absolute;left:60px;right:60px;text-align:center;font-family:anton;text-transform:uppercase;color:#F4F7FC;line-height:1.02;letter-spacing:1px;
  text-shadow:0 8px 30px rgba(0,0,0,.5)}
.titB .b{color:#3D8BFF}
.apoB{position:absolute;left:90px;right:90px;text-align:center;font-family:pop600;color:#b9c8e2;line-height:1.35}
.pag{position:absolute;bottom:44px;left:0;right:0;text-align:center;}
.pag.t{bottom:auto;top:40px;right:52px;left:auto;text-align:right;}
.pag{font-family:m800;font-size:28px;letter-spacing:4px;color:rgba(255,255,255,.55)}
.desliza{position:absolute;bottom:60px;left:0;right:0;text-align:center;font-family:m900;font-size:34px;color:#FFD400;letter-spacing:2px;text-shadow:0 3px 12px rgba(0,0,0,.8)}
.preco{display:inline-block;padding:16px 44px;border-radius:24px;background:#FFD400;color:#0a0a0a;font-family:m900;font-size:60px;box-shadow:0 12px 0 #b38f00,0 24px 60px rgba(0,0,0,.45)}
.precoB{display:inline-block;padding:16px 44px;border-radius:999px;background:linear-gradient(135deg,#3D8BFF,#1d5be0);color:#fff;font-family:anton;font-size:62px;letter-spacing:1px;
  box-shadow:0 0 0 3px rgba(255,255,255,.18) inset,0 20px 60px rgba(61,139,255,.45)}
</style></head><body>%(corpo)s</body></html>"""

def foto_bg(arq, escurece=0.5, blur=0, pos='50% 50%', vig=True):
    p = os.path.join(FOTOS, arq)
    f = f"filter:brightness({escurece}) saturate(1.05){' blur(%dpx)' % blur if blur else ''};"
    v = ("<div class=fill style='background:linear-gradient(rgba(0,0,0,.45),rgba(0,0,0,0) 35%,rgba(0,0,0,0) 60%,rgba(0,0,0,.6))'></div>" if vig else '')
    return (f"<div class=fill style=\"background:url('file://{p}') {pos}/cover;{f}transform:scale(1.06)\"></div>" + v)

def grad_bg(estilo='B', luz=(50, 62)):
    css = ESTILOS[estilo]['bg']
    return (f"<div class=fill style=\"background:{css}\"></div>"
            f"<div class=fill style='background:radial-gradient(45% 28% at {luz[0]}% {luz[1]}%, rgba(61,139,255,.35), rgba(0,0,0,0) 70%)'></div>"
            "<div class=fill style='background:radial-gradient(130% 90% at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,.5) 100%)'></div>")

def celular(tela_png, w=600, top=500, rot=0, tilt=0, ring=None, scr_y=0, scr_z=1.0):
    h = int(w*2.164)
    tr = f"rotateY({rot}deg) rotateX({tilt}deg)"
    shadow = "drop-shadow(0 60px 70px rgba(0,0,0,.6)) drop-shadow(0 20px 24px rgba(0,0,0,.45)) drop-shadow(0 0 90px rgba(61,139,255,.28))"
    inner = phone_html().replace('<img>', f"<img src='file://{tela_png}' style='transform:translate(0,{-scr_y}px) scale({scr_z})'>")
    if ring:
        inner = inner.replace("<div class=ring style='display:none'></div>",
                              f"<div class=ring style='left:{ring[0]}px;top:{ring[1]}px;width:{ring[2]}px;height:{ring[3]}px'></div>")
    return (f"<div class=ph style='top:{top + h//2}px'><div id=phone style='width:{w}px;height:{h}px;left:{-w//2}px;top:{-h//2}px;"
            f"transform:{tr};filter:{shadow}'>{inner}</div></div>")

def tela(src, t):
    return still(src, t)

def render(html_corpo, w, h, saida):
    from playwright.sync_api import sync_playwright
    doc = BASE % dict(fontes=CSS_FONTES, phone=CSS_PHONE, w=w, h=h, corpo=html_corpo)
    tmp = '/tmp/v2est.html'; open(tmp, 'w').write(doc)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--force-color-profile=srgb', '--allow-file-access-from-files'])
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2)
        pg.goto('file://' + tmp); pg.wait_for_timeout(700)
        pg.evaluate('document.fonts.ready')
        pg.screenshot(path='/tmp/v2est@2x.png'); b.close()
    os.makedirs(os.path.dirname(saida), exist_ok=True)
    Image.open('/tmp/v2est@2x.png').convert('RGB').resize((w, h), Image.LANCZOS).save(saida, quality=93)
    print('ok', saida)

def cta(estilo, titulo, sub, preco=True, top=260):
    ic = f"<img src='file://{ICON}' style='width:220px;height:220px;border-radius:52px;box-shadow:0 30px 80px rgba(0,0,0,.55),0 0 120px rgba(61,139,255,.55)'>"
    if estilo == 'A':
        t = f"<div class=capA style='position:relative;left:0;right:0;font-size:104px;margin-top:50px'>{titulo}</div>"
        s = f"<div class=apoA style='position:relative;left:0;right:0;font-size:44px;margin-top:22px'>{H.escape(sub)}</div>"
        pr = "<div style='margin-top:36px'><span class=preco>por R$19,90</span></div>" if preco else ''
    else:
        t = f"<div class=titB style='position:relative;left:0;right:0;font-size:132px;margin-top:50px'>{titulo}</div>"
        s = f"<div class=apoB style='position:relative;left:0;right:0;font-size:42px;margin-top:20px'>{H.escape(sub)}</div>"
        pr = "<div style='margin-top:36px'><span class=precoB>por R$19,90</span></div>" if preco else ''
    se = f"<div style='margin-top:44px'><img src='file://{SELOS}' style='width:600px'></div>"
    return f"<div style='position:absolute;left:0;right:0;top:{top}px;text-align:center'>{ic}{t}{s}{pr}{se}</div>"

# ---------------- CARROSSEL A (Nativo/Rua) ----------------
def carrossel_A():
    d = os.path.join(AQUI, 'A', 'carrossel'); W, Hc = 1080, 1350
    saude = tela('tela-saude-1.mp4', 13.0); manut = tela('tela-manutencao.mp4', 44.0); cad = tela('tela-cadastro-moto.mp4', 104)
    cards = [
        foto_bg('5195494.jpg', 0.55, pos='50% 40%') +
        "<div class=capA style='top:330px;font-size:140px'>TUA MOTO<br>TÁ EM DIA?<br><span class=y>PROVA.</span></div>"
        "<div class=desliza>DESLIZA PRA VER →</div>",
        foto_bg('3822836.jpg', 0.5) +
        "<div class=capA style='top:300px;font-size:112px'>O MECÂNICO<br>PERGUNTA.<br><span class=y>VOCÊ CHUTA.</span></div>"
        "<div class=apoA style='top:820px;font-size:52px'>“Uns 3 meses… ou 6? Sei lá.”</div><div class=pag>02 / 05</div>",
        foto_bg('3822836.jpg', 0.3, blur=14) +
        "<div class=capA style='top:90px;font-size:84px'>O QUE <span class=y>NUNCA</span> FOI FEITO<br>APARECE NA HORA</div>" +
        celular(cad, w=560, top=360) + "<div class='pag t'>03 / 05</div>",
        foto_bg('5195494.jpg', 0.3, blur=14) +
        "<div class=capA style='top:90px;font-size:84px'>O QUE <span class=y>VENCEU</span><br>FICA EM VERMELHO</div>" +
        celular(saude, w=560, top=360) + "<div class='pag t'>04 / 05</div>",
        grad_bg('A', (50, 40)) + cta('A', 'NUNCA MAIS<br>“SEI LÁ”', 'Baixe agora o MinhaMoto', True, top=230),
    ]
    for i, c in enumerate(cards, 1):
        render(c, W, Hc, os.path.join(d, f'{i:02d}.jpg'))

# ---------------- CARROSSEL B (Premium produto) ----------------
def carrossel_B():
    d = os.path.join(AQUI, 'B', 'carrossel'); W, Hc = 1080, 1350
    saude0 = tela('tela-saude-1.mp4', 1.0); saude = tela('tela-saude-1.mp4', 13.0)
    cad = tela('tela-cadastro-moto.mp4', 104); notif = tela('tela-notificacoes.mp4', 69.5); manut = tela('tela-manutencao.mp4', 44.0)
    def card(l1, l2, png, n, rot=-10, apoio=None):
        a = f"<div class=apoB style='top:{345}px;font-size:36px'>{H.escape(apoio)}</div>" if apoio else ''
        top = 430 if apoio else 380
        return (grad_bg('B') + f"<div class=titB style='top:96px;font-size:{92 if max(len(l1),len(l2))>16 else 118}px'>{H.escape(l1)}<br><span class=b>{H.escape(l2)}</span></div>"
                + a + celular(png, w=560, top=top, rot=rot, tilt=4) + f"<div class='pag t'>{n:02d} / 05</div>")
    cards = [
        card('ESQUECEU A TROCA?', 'A MOTO NÃO ESQUECE.', saude0, 1, rot=-12).replace("<div class='pag t'>01 / 05</div>", "<div class='pag t' style='color:#3D8BFF'>DESLIZA →</div>"),
        card('O QUE VENCEU', 'FICA EM VERMELHO', saude, 2, rot=10),
        card('O QUE NUNCA FOI FEITO', 'APARECE PRA VOCÊ', cad, 3, rot=-10),
        card('E O APP TE AVISA', 'NA HORA CERTA', notif, 4, rot=10),
        grad_bg('B', (50, 38)) + cta('B', 'BAIXE O<br><span class=b>MINHAMOTO</span>', 'Teu plano de revisão na palma da mão.', True, top=220),
    ]
    for i, c in enumerate(cards, 1):
        render(c, W, Hc, os.path.join(d, f'{i:02d}.jpg'))

# ---------------- STORIES (ST04 refeito: caixa de perguntas) ----------------
CAIXA = ("<div style='position:absolute;left:150px;right:150px;top:{top}px;height:330px;border-radius:44px;"
         "border:4px dashed rgba(255,255,255,.35);display:flex;align-items:center;justify-content:center;"
         "font-family:m800;font-size:30px;letter-spacing:3px;color:rgba(255,255,255,.45)'>STICKER DE PERGUNTAS AQUI</div>")

def story_A():
    c = (foto_bg('3822836.jpg', 0.42, pos='60% 50%') +
         f"<div style='position:absolute;left:0;right:0;top:250px;text-align:center'><img src='file://{ICON}' style='width:130px;height:130px;border-radius:32px;box-shadow:0 18px 50px rgba(0,0,0,.6)'></div>"
         "<div class=capA style='top:430px;font-size:100px'>TUA MOTO TÁ<br>FAZENDO UM<br><span class=y>BARULHO<br>ESTRANHO?</span></div>"
         "<div class=apoA style='top:960px;font-size:46px'>Manda tua dúvida de manutenção.<br>A gente responde aqui nos stories.</div>"
         + CAIXA.format(top=1190))
    render(c, 1080, 1920, os.path.join(AQUI, 'A', 'story', 'story.jpg'))

def story_B():
    c = (grad_bg('B', (50, 70)) +
         "<div class=fill style='background:radial-gradient(60% 30% at 50% 18%, rgba(61,139,255,.25), rgba(0,0,0,0) 70%)'></div>"
         f"<div style='position:absolute;left:0;right:0;top:240px;text-align:center'><img src='file://{ICON}' style='width:150px;height:150px;border-radius:36px;box-shadow:0 24px 60px rgba(0,0,0,.6),0 0 90px rgba(61,139,255,.6)'></div>"
         "<div class=titB style='top:450px;font-size:150px'>TIRA TUA<br><span class=b>DÚVIDA</span><br>DE MOTO</div>"
         "<div class=apoB style='top:1000px;font-size:44px'>Óleo, revisão, corrente, barulho estranho…<br>Pergunta que a gente responde.</div>"
         + CAIXA.format(top=1200))
    render(c, 1080, 1920, os.path.join(AQUI, 'B', 'story', 'story.jpg'))

if __name__ == '__main__':
    q = sys.argv[1] if len(sys.argv) > 1 else 'todos'
    if q in ('A', 'todos'): carrossel_A(); story_A()
    if q in ('B', 'todos'): carrossel_B(); story_B()
