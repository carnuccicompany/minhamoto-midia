#!/usr/bin/env python3
"""Carrosséis (1080x1350) e stories (1080x1920) da direção v2, com o mesmo celular premium dos vídeos.
Render em 2x e redução LANCZOS pra nitidez máxima.
Uso: python3 estaticos.py [A|B|todos]
"""
import os, sys, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motor import CSS_FONTES, ASSETS, phone_html, tela_app, topo_fixo, altura_celular, ESTILOS, PAGINA, TW, TOPO
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
.capA{position:absolute;left:90px;right:90px;text-align:center;font-family:j800;color:#fff;letter-spacing:-.035em;word-spacing:.1em;
  text-shadow:0 3px 6px rgba(0,0,0,.55),0 8px 40px rgba(0,0,0,.85);line-height:1.06}
.capA .y{color:#FFD400}
.apoA{position:absolute;left:90px;right:90px;text-align:center;font-family:j600;color:#fff;letter-spacing:-.01em;line-height:1.3;text-shadow:0 4px 18px rgba(0,0,0,.8)}
.titB{position:absolute;left:90px;right:90px;text-align:center;font-family:j800;color:#F4F7FC;line-height:1.05;letter-spacing:-.035em;word-spacing:.1em;
  text-shadow:0 8px 30px rgba(0,0,0,.5)}
.titB .b{color:#3D8BFF}
.apoB{position:absolute;left:90px;right:90px;text-align:center;font-family:j500;color:#b9c8e2;line-height:1.35;letter-spacing:-.01em}
.tt .capA,.tt .titB,.tt .apoA,.tt .apoB{left:140px;right:140px}
.pag{position:absolute;bottom:44px;left:0;right:0;text-align:center;}
.pag.t{bottom:auto;top:44px;right:90px;left:auto;text-align:right;}
.pag{font-family:j700;font-size:28px;letter-spacing:.06em;color:rgba(255,255,255,.55)}
.desliza{position:absolute;bottom:64px;left:0;right:0;text-align:center;font-family:j700;font-size:36px;color:#FFD400;letter-spacing:-.01em;text-shadow:0 3px 12px rgba(0,0,0,.8)}
.preco{display:inline-block;padding:16px 44px;border-radius:24px;background:#FFD400;color:#0a0a0a;font-family:j800;font-size:60px;letter-spacing:-.02em;box-shadow:0 12px 0 #b38f00,0 24px 60px rgba(0,0,0,.45)}
.precoB{display:inline-block;padding:16px 44px;border-radius:999px;background:linear-gradient(135deg,#3D8BFF,#1d5be0);color:#fff;font-family:j800;font-size:60px;letter-spacing:-.02em;
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

def celular(nome, w=600, top=500, rot=0, tilt=0, ring=None, rola=None):
    """Celular com a tela do app (telas-app/<nome>.png). rola=y: página inteira ('rolagem/..') parada em y (px no espaço 1179),
    com o topo fixo do app por cima."""
    h = altura_celular(w); e = (w - 44)/TW
    tr = f"rotateY({rot}deg) rotateX({tilt}deg)"
    shadow = "drop-shadow(0 60px 70px rgba(0,0,0,.6)) drop-shadow(0 20px 24px rgba(0,0,0,.45)) drop-shadow(0 0 90px rgba(61,139,255,.28))"
    src = tela_app(nome)
    if rola is not None:
        inner = phone_html().replace('<img><img class=topo style=\'display:none\'>',
            f"<img src='file://{src}' style='transform:translate(0,{(TOPO - rola)*e:.1f}px)'><img class=topo src='file://{topo_fixo(nome)}'>")
    else:
        inner = phone_html().replace('<img>', f"<img src='file://{src}'>", 1)
    if ring:
        inner = inner.replace("<div class=ring style='display:none'></div>",
                              f"<div class=ring style='left:{ring[0]}px;top:{ring[1]}px;width:{ring[2]}px;height:{ring[3]}px'></div>")
    return (f"<div class=ph style='top:{top + h//2}px'><div id=phone style='width:{w}px;height:{h}px;left:{-w//2}px;top:{-h//2}px;"
            f"transform:{tr};filter:{shadow}'>{inner}</div></div>")

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

def cta(estilo, titulo, sub, preco=True, top=260, pad=0):
    ic = f"<img src='file://{ICON}' style='width:220px;height:220px;border-radius:52px;box-shadow:0 30px 80px rgba(0,0,0,.55),0 0 120px rgba(61,139,255,.55)'>"
    if estilo == 'A':
        t = f"<div class=capA style='position:relative;left:0;right:0;font-size:112px;margin-top:50px'>{titulo}</div>"
        s = f"<div class=apoA style='position:relative;left:0;right:0;font-size:44px;margin-top:22px'>{H.escape(sub)}</div>"
        pr = "<div style='margin-top:36px'><span class=preco>por R$19,90</span></div>" if preco else ''
    else:
        t = f"<div class=titB style='position:relative;left:0;right:0;font-size:112px;margin-top:50px'>{titulo}</div>"
        s = f"<div class=apoB style='position:relative;left:0;right:0;font-size:42px;margin-top:20px'>{H.escape(sub)}</div>"
        pr = "<div style='margin-top:36px'><span class=precoB>por R$19,90</span></div>" if preco else ''
    se = f"<div style='margin-top:44px'><img src='file://{SELOS}' style='width:600px'></div>"
    return f"<div style='position:absolute;left:{pad}px;right:{pad}px;top:{top}px;text-align:center'>{ic}{t}{s}{pr}{se}</div>"

# ---------------- CARROSSEL A (Nativo/Rua) ----------------
def carrossel_A():
    d = os.path.join(AQUI, 'A', 'carrossel'); W, Hc = 1080, 1350
    cards = [
        foto_bg('5195494.jpg', 0.55, pos='50% 40%') +
        "<div class=capA style='top:400px;font-size:132px'>Tua moto<br>tá em dia?<br><span class=y>Prova.</span></div>"
        "<div class=desliza>Desliza pra ver →</div>",
        foto_bg('3822836.jpg', 0.5) +
        "<div class=capA style='top:380px;font-size:120px'>O mecânico<br>pergunta.<br><span class=y>Você chuta.</span></div>"
        "<div class=apoA style='top:830px;font-size:50px'>“Uns 3 meses… ou 6? Sei lá.”</div><div class=pag>02 / 05</div>",
        foto_bg('3822836.jpg', 0.3, blur=14) +
        "<div class=capA style='top:96px;font-size:80px'>O que <span class=y>nunca</span> foi feito<br>aparece na hora</div>" +
        celular('rolagem/19-saude-atrasados', w=540, top=390, rola=4600) + "<div class='pag t'>03 / 05</div>",
        foto_bg('5195494.jpg', 0.3, blur=14) +
        "<div class=capA style='top:96px;font-size:80px'>O que <span class=y>venceu</span><br>fica em vermelho</div>" +
        celular('rolagem/19-saude-atrasados', w=540, top=390, rola=3480) + "<div class='pag t'>04 / 05</div>",
        grad_bg('A', (50, 40)) + cta('A', 'Nunca mais<br><span class=y>“sei lá”</span>', 'Baixe agora o MinhaMoto', True, top=230),
    ]
    for i, c in enumerate(cards, 1):
        render(c, W, Hc, os.path.join(d, f'{i:02d}.jpg'))

# ---------------- CARROSSEL B (Premium produto) ----------------
def carrossel_B():
    d = os.path.join(AQUI, 'B', 'carrossel'); W, Hc = 1080, 1350
    def card(l1, l2, tela, n, rot=0, apoio=None, rola=None):
        a = f"<div class=apoB style='top:{345}px;font-size:36px'>{H.escape(apoio)}</div>" if apoio else ''
        top = 430 if apoio else 380
        return (grad_bg('B') + f"<div class=titB style='top:96px;font-size:80px'>{H.escape(l1)}<br><span class=b>{H.escape(l2)}</span></div>"
                + a + celular(tela, w=560, top=top, rot=rot, tilt=0, rola=rola) + f"<div class='pag t'>{n:02d} / 05</div>")
    cards = [
        card('Esqueceu a troca?', 'A moto não esquece.', '21-item-atrasado', 1).replace("<div class='pag t'>01 / 05</div>", "<div class='pag t' style='color:#3D8BFF'>Desliza →</div>"),
        card('O que venceu', 'fica em vermelho', '19-saude-atrasados', 2),
        card('O que nunca foi feito', 'aparece pra você', 'rolagem/19-saude-atrasados', 3, rola=4600),
        card('E o app te avisa', 'na hora certa', '15-notificacoes', 4),
        grad_bg('B', (50, 38)) + cta('B', 'Baixe o<br><span class=b>MinhaMoto</span>', 'Teu plano de revisão na palma da mão.', True, top=220),
    ]
    for i, c in enumerate(cards, 1):
        render(c, W, Hc, os.path.join(d, f'{i:02d}.jpg'))

# ---------------- STORIES (ST04 refeito: caixa de perguntas) ----------------
CAIXA = ("<div style='position:absolute;left:150px;right:150px;top:{top}px;height:330px;border-radius:44px;"
         "border:4px dashed rgba(255,255,255,.35);display:flex;align-items:center;justify-content:center;"
         "font-family:j600;font-size:32px;color:rgba(255,255,255,.45)'>Sticker de perguntas aqui</div>")

def story_A():
    c = (foto_bg('3822836.jpg', 0.42, pos='60% 50%') +
         f"<div style='position:absolute;left:0;right:0;top:250px;text-align:center'><img src='file://{ICON}' style='width:130px;height:130px;border-radius:32px;box-shadow:0 18px 50px rgba(0,0,0,.6)'></div>"
         "<div class=capA style='top:440px;font-size:104px'>Tua moto tá<br>fazendo um<br><span class=y>barulho estranho?</span></div>"
         "<div class=apoA style='top:960px;font-size:46px'>Manda tua dúvida de manutenção.<br>A gente responde aqui nos stories.</div>"
         + CAIXA.format(top=1140))
    render(c, 1080, 1920, os.path.join(AQUI, 'A', 'story', 'story.jpg'))

def story_B():
    c = (grad_bg('B', (50, 70)) +
         "<div class=fill style='background:radial-gradient(60% 30% at 50% 18%, rgba(61,139,255,.25), rgba(0,0,0,0) 70%)'></div>"
         f"<div style='position:absolute;left:0;right:0;top:240px;text-align:center'><img src='file://{ICON}' style='width:150px;height:150px;border-radius:36px;box-shadow:0 24px 60px rgba(0,0,0,.6),0 0 90px rgba(61,139,255,.6)'></div>"
         "<div class=titB style='top:460px;font-size:120px'>Tira tua<br><span class=b>dúvida</span><br>de moto</div>"
         "<div class=apoB style='top:1000px;font-size:44px'>Óleo, revisão, corrente, barulho estranho…<br>Pergunta que a gente responde.</div>"
         + CAIXA.format(top=1150))
    render(c, 1080, 1920, os.path.join(AQUI, 'B', 'story', 'story.jpg'))

# ---------------- VERSÕES TIKTOK 9:16 (1080x1920, zona segura: 150px topo, 420px base, 140px direita) ----------------
TTW, TTH = 1080, 1920

def carrossel_A_tiktok():
    d = os.path.join(AQUI, 'A', 'carrossel-tiktok')
    cards = [
        foto_bg('5195494.jpg', 0.55, pos='50% 40%') +
        "<div class=capA style='top:600px;font-size:132px'>Tua moto<br>tá em dia?<br><span class=y>Prova.</span></div>"
        "<div class=desliza style='bottom:auto;top:1400px'>Desliza pra ver →</div>",
        foto_bg('3822836.jpg', 0.5) +
        "<div class=capA style='top:560px;font-size:112px'>O mecânico<br>pergunta.<br><span class=y>Você chuta.</span></div>"
        "<div class=apoA style='top:990px;font-size:48px'>“Uns 3 meses… ou 6? Sei lá.”</div>"
        "<div class=pag style='bottom:auto;top:1420px'>02 / 05</div>",
        foto_bg('3822836.jpg', 0.3, blur=14) +
        "<div class=capA style='top:200px;font-size:70px'>O que <span class=y>nunca</span> foi feito<br>aparece na hora</div>" +
        celular('rolagem/19-saude-atrasados', w=500, top=468, rola=4600),
        foto_bg('5195494.jpg', 0.3, blur=14) +
        "<div class=capA style='top:200px;font-size:70px'>O que <span class=y>venceu</span><br>fica em vermelho</div>" +
        celular('rolagem/19-saude-atrasados', w=500, top=468, rola=3480),
        grad_bg('A', (50, 36)) + cta('A', 'Nunca mais<br><span class=y>“sei lá”</span>', 'Baixe agora o MinhaMoto', True, top=360, pad=140),
    ]
    for i, c in enumerate(cards, 1):
        render("<div class=tt>" + c + "</div>", TTW, TTH, os.path.join(d, f'{i:02d}.jpg'))

def carrossel_B_tiktok():
    d = os.path.join(AQUI, 'B', 'carrossel-tiktok')
    def card(l1, l2, tela, rola=None):
        return (grad_bg('B', (50, 55)) + f"<div class=titB style='top:200px;font-size:70px'>{H.escape(l1)}<br><span class=b>{H.escape(l2)}</span></div>"
                + celular(tela, w=500, top=468, rola=rola))
    cards = [
        card('Esqueceu a troca?', 'A moto não esquece.', '21-item-atrasado'),
        card('O que venceu', 'fica em vermelho', '19-saude-atrasados'),
        card('O que nunca foi feito', 'aparece pra você', 'rolagem/19-saude-atrasados', rola=4600),
        card('E o app te avisa', 'na hora certa', '15-notificacoes'),
        grad_bg('B', (50, 36)) + cta('B', 'Baixe o<br><span class=b>MinhaMoto</span>', 'Teu plano de revisão na palma da mão.', True, top=360, pad=140),
    ]
    for i, c in enumerate(cards, 1):
        render("<div class=tt>" + c + "</div>", TTW, TTH, os.path.join(d, f'{i:02d}.jpg'))

if __name__ == '__main__':
    q = sys.argv[1] if len(sys.argv) > 1 else 'todos'
    if q in ('A', 'todos'): carrossel_A(); story_A(); carrossel_A_tiktok()
    if q in ('B', 'todos'): carrossel_B(); story_B(); carrossel_B_tiktok()
    if q == 'tiktok': carrossel_A_tiktok(); carrossel_B_tiktok()
