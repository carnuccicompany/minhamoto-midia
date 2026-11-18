#!/usr/bin/env python3
"""Carrosséis (1080x1350) e stories (1080x1920) da direção v2, com o mesmo celular premium dos vídeos.
Render em 2x e redução LANCZOS pra nitidez máxima.
Uso: python3 estaticos.py [A|B|todos]
"""
import os, sys, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motor import CSS_FONTES, ASSETS, phone_html, tela_app, topo_fixo, altura_celular, ESTILOS, PAGINA, TW, TOPO, AZUL, AZUL_ESC, AZUL_CLARO, LIMAO
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
FOTOS = os.path.join(ASSETS, 'fotos')
ICON = os.path.join(ASSETS, 'icon.png'); SELOS = os.path.join(ASSETS, 'selos-lojas.png')

# CSS do celular reaproveitado da página de vídeo (mesmo acabamento)
CSS_PHONE = PAGINA.split('<style>')[1].split('</style>')[0] % dict(fontes='', **ESTILOS['A'])

BASE = """<!doctype html><html><head><meta charset=utf-8><style>%(fontes)s %(phone)s
html,body{width:%(w)dpx;height:%(h)dpx;overflow:hidden;background:#010711}
.fill{position:absolute;inset:0}
.ph{position:absolute;left:50%%;width:0;height:0;perspective:2400px}
.ph #phone{position:absolute}
.capA{position:absolute;left:90px;right:90px;text-align:center;font-family:j800;color:#fff;letter-spacing:-.02em;
  text-shadow:0 3px 6px rgba(0,0,0,.55),0 8px 40px rgba(0,0,0,.85);line-height:1.12;text-wrap:balance}
.capA .y,.titB .b,.capA .b{color:%(azc)s}
.apoA{position:absolute;left:90px;right:90px;text-align:center;font-family:j500;color:#fff;letter-spacing:-.005em;line-height:1.35;text-shadow:0 4px 18px rgba(0,0,0,.8);text-wrap:balance}
.titB{position:absolute;left:90px;right:90px;text-align:center;font-family:j800;color:#F4F7FC;line-height:1.12;letter-spacing:-.02em;
  text-shadow:0 8px 30px rgba(0,0,0,.5);text-wrap:balance}
.apoB{position:absolute;left:90px;right:90px;text-align:center;font-family:j500;color:#c9d6ea;line-height:1.38;letter-spacing:-.005em;text-wrap:balance}
.tt .capA,.tt .titB,.tt .apoA,.tt .apoB{left:140px;right:140px}
.lm{display:block;width:96px;height:8px;border-radius:8px;background:%(lim)s;margin:28px auto 0;box-shadow:0 0 24px rgba(198,255,0,.45)}
.pag{position:absolute;bottom:44px;left:0;right:0;text-align:center;font-family:j600;font-size:28px;letter-spacing:.06em;color:rgba(255,255,255,.55)}
.pag.t{bottom:auto;top:44px;right:90px;left:auto;text-align:right;}
.desliza{position:absolute;bottom:70px;left:0;right:0;text-align:center;font-family:j600;font-size:36px;color:#fff;letter-spacing:-.005em;text-shadow:0 3px 12px rgba(0,0,0,.8)}
.desliza b{color:%(lim)s;font-family:j800}
.preco{display:inline-flex;align-items:center;gap:18px;padding:16px 44px 16px 32px;border-radius:999px;background:linear-gradient(135deg,%(az)s,%(aze)s);color:#fff;font-family:j700;font-size:56px;letter-spacing:-.01em;
  box-shadow:0 0 0 3px rgba(255,255,255,.16) inset,0 20px 60px rgba(40,122,245,.45)}
.preco i{width:20px;height:20px;border-radius:50%%;background:%(lim)s;box-shadow:0 0 18px rgba(198,255,0,.7)}
</style></head><body>%(corpo)s</body></html>"""

def foto_bg(arq, escurece=0.5, blur=0, pos='50% 50%', vig=True):
    p = os.path.join(FOTOS, arq)
    f = f"filter:brightness({escurece}) saturate(1.05){' blur(%dpx)' % blur if blur else ''};"
    v = ("<div class=fill style='background:linear-gradient(rgba(0,0,0,.45),rgba(0,0,0,0) 35%,rgba(0,0,0,0) 60%,rgba(0,0,0,.6))'></div>" if vig else '')
    return (f"<div class=fill style=\"background:url('file://{p}') {pos}/cover;{f}transform:scale(1.06)\"></div>" + v)

def grad_bg(estilo='B', luz=(50, 62)):
    css = ESTILOS[estilo]['bg']
    return (f"<div class=fill style=\"background:{css}\"></div>"
            f"<div class=fill style='background:radial-gradient(45% 28% at {luz[0]}% {luz[1]}%, rgba(82,169,254,.35), rgba(0,0,0,0) 70%)'></div>"
            "<div class=fill style='background:radial-gradient(130% 90% at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,.5) 100%)'></div>")

def celular(nome, w=600, top=500, rot=0, tilt=0, ring=None, rola=None):
    """Celular com a tela do app (telas-app/<nome>.png). rola=y: página inteira ('rolagem/..') parada em y (px no espaço 1179),
    com o topo fixo do app por cima."""
    h = altura_celular(w); e = (w - 44)/TW
    tr = f"rotateY({rot}deg) rotateX({tilt}deg)"
    shadow = "drop-shadow(0 60px 70px rgba(0,0,0,.6)) drop-shadow(0 20px 24px rgba(0,0,0,.45)) drop-shadow(0 0 90px rgba(82,169,254,.28))"
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
    doc = BASE % dict(fontes=CSS_FONTES, phone=CSS_PHONE, w=w, h=h, corpo=html_corpo, azc=AZUL_CLARO, az=AZUL, aze=AZUL_ESC, lim=LIMAO)
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

def cta(estilo, titulo, sub, preco=True, top=260, pad=0, selos_top=None, H_=1350):
    """Ícone + título + traço limão + apoio + preço; selos das lojas separados embaixo."""
    ic = f"<img src='file://{ICON}' style='width:200px;height:200px;border-radius:48px;box-shadow:0 30px 80px rgba(0,0,0,.55),0 0 120px rgba(82,169,254,.55)'>"
    cls = 'capA' if estilo == 'A' else 'titB'; ap = 'apoA' if estilo == 'A' else 'apoB'
    t = f"<div class={cls} style='position:relative;left:0;right:0;font-size:96px;margin-top:48px'>{titulo}</div><span class=lm></span>"
    s = f"<div class={ap} style='position:relative;left:0;right:0;font-size:44px;margin-top:24px'>{H.escape(sub)}</div>"
    pr = "<div style='margin-top:40px'><span class=preco><i></i>por R$19,90</span></div>" if preco else ''
    st = selos_top if selos_top is not None else H_ - 200
    se = f"<div style='position:absolute;left:0;right:0;top:{st}px;text-align:center'><img src='file://{SELOS}' style='width:540px'></div>"
    return f"<div style='position:absolute;left:{pad}px;right:{pad}px;top:{top}px;text-align:center'>{ic}{t}{s}{pr}</div>" + se

# Régua: agencia/DESIGN-MINHAMOTO.md. Celular sempre inteiro (sem corte), mesmo mockup em tudo.
PH45 = dict(w=480, top=330)      # 4:5 — celular inteiro: 330 → ~1320
PH916 = dict(w=560, top=390)     # 9:16 TikTok — celular maior, dentro da zona útil

def tit2(estilo, l1, l2, top, tam):
    c = 'capA' if estilo == 'A' else 'titB'
    return f"<div class={c} style='top:{top}px;font-size:{tam}px'>{H.escape(l1)}<br><span class=b>{H.escape(l2)}</span></div>"

def lista_A(tt=False):
    P = PH916 if tt else PH45; T = 190 if tt else 92; tam = 66 if tt else 64
    capa_top = 600 if tt else 420
    return [
        foto_bg('5195494.jpg', 0.55, pos='50% 40%') +
        f"<div class=capA style='top:{capa_top}px;font-size:{120 if tt else 124}px'>Manutenção<br>esquecida<br><span class=y>custa caro.</span></div>"
        + (f"<div class=desliza style='bottom:auto;top:1400px'>Deslize <b>→</b></div>" if tt else "<div class=desliza>Deslize <b>→</b></div>"),
        foto_bg('3822836.jpg', 0.5) +
        f"<div style='position:absolute;left:0;right:0;top:{capa_top - (40 if tt else 120)}px'>"
        f"<div class=capA style='position:relative;font-size:{100 if tt else 104}px'>O mecânico pergunta.<br><span class=y>Você sabe responder?</span></div>"
        f"<div class=apoA style='position:relative;margin-top:40px;font-size:46px'>Data, km e peça.<br>Tudo na palma da mão.</div></div>" + ("" if tt else "<div class=pag>02 / 05</div>"),
        foto_bg('3822836.jpg', 0.3, blur=14) + tit2('A', 'O que está em dia.', 'O que pede atenção.', T, tam) +
        celular('rolagem/02-saude', rola=1350, **P) + ("" if tt else "<div class='pag t'>03 / 05</div>"),
        foto_bg('5195494.jpg', 0.3, blur=14) + tit2('A', 'Cada serviço salvo,', 'com data e km.', T, tam) +
        celular('rolagem/06-historico', rola=900, **P) + ("" if tt else "<div class='pag t'>04 / 05</div>"),
        grad_bg('A', (50, 36)) + (cta('A', 'Controle total<br><span class=y>da sua moto.</span>', 'Na palma da mão.', True, top=360, pad=140, H_=1920, selos_top=1330) if tt
                                  else cta('A', 'Controle total<br><span class=y>da sua moto.</span>', 'Na palma da mão.', True, top=170, H_=1350)),
    ]

def lista_B(tt=False):
    P = PH916 if tt else PH45; T = 190 if tt else 92; tam = 66 if tt else 64
    def card(l1, l2, tela, n, rola=None):
        pg = "" if tt else (f"<div class='pag t'>{n:02d} / 05</div>" if n > 1 else "<div class='pag t' style='color:#C6FF00'>Deslize →</div>")
        return grad_bg('B', (50, 55)) + tit2('B', l1, l2, T, tam) + celular(tela, rola=rola, **P) + pg
    return [
        card('Esqueceu a troca?', 'A moto não esquece.', '02-saude', 1),
        card('Tudo o que vence', 'aparece primeiro.', 'rolagem/02-saude', 2, rola=3700),
        card('O histórico completo,', 'sempre com você.', '06-historico', 3),
        card('E o aviso chega', 'na hora certa.', '15-notificacoes', 4),
        grad_bg('B', (50, 36)) + (cta('B', 'Sua moto em dia,<br><span class=b>sem esforço.</span>', 'Baixe agora o MinhaMoto.', True, top=360, pad=140, H_=1920, selos_top=1330) if tt
                                  else cta('B', 'Sua moto em dia,<br><span class=b>sem esforço.</span>', 'Baixe agora o MinhaMoto.', True, top=170, H_=1350)),
    ]

def carrossel_A():
    for i, c in enumerate(lista_A(), 1): render(c, 1080, 1350, os.path.join(AQUI, 'A', 'carrossel', f'{i:02d}.jpg'))
def carrossel_B():
    for i, c in enumerate(lista_B(), 1): render(c, 1080, 1350, os.path.join(AQUI, 'B', 'carrossel', f'{i:02d}.jpg'))
def carrossel_A_tiktok():
    for i, c in enumerate(lista_A(True), 1): render("<div class=tt>" + c + "</div>", 1080, 1920, os.path.join(AQUI, 'A', 'carrossel-tiktok', f'{i:02d}.jpg'))
def carrossel_B_tiktok():
    for i, c in enumerate(lista_B(True), 1): render("<div class=tt>" + c + "</div>", 1080, 1920, os.path.join(AQUI, 'B', 'carrossel-tiktok', f'{i:02d}.jpg'))

# ---------------- STORIES (caixa de perguntas; o retângulo marca onde vai o sticker do Instagram) ----------------
CAIXA = ("<div style='position:absolute;left:150px;right:150px;top:{top}px;height:330px;border-radius:44px;"
         "border:4px dashed rgba(255,255,255,.35);display:flex;align-items:center;justify-content:center;"
         "font-family:j500;font-size:32px;color:rgba(255,255,255,.45)'>Sticker de perguntas aqui</div>")

def story_A():
    c = (foto_bg('3822836.jpg', 0.42, pos='60% 50%') +
         f"<div style='position:absolute;left:0;right:0;top:250px;text-align:center'><img src='file://{ICON}' style='width:130px;height:130px;border-radius:32px;box-shadow:0 18px 50px rgba(0,0,0,.6)'></div>"
         "<div style='position:absolute;left:140px;right:140px;top:430px'>"
         "<div class=capA style='position:relative;left:0;right:0;font-size:96px'>Barulho estranho<br><span class=y>na sua moto?</span></div><span class=lm></span>"
         "<div class=apoA style='position:relative;left:0;right:0;margin-top:30px;font-size:46px'>Envie sua dúvida.<br>Respondemos aqui nos stories.</div></div>"
         + CAIXA.format(top=1120))
    render(c, 1080, 1920, os.path.join(AQUI, 'A', 'story', 'story.jpg'))

def story_B():
    c = (grad_bg('B', (50, 70)) +
         "<div class=fill style='background:radial-gradient(60% 30% at 50% 18%, rgba(82,169,254,.25), rgba(0,0,0,0) 70%)'></div>"
         f"<div style='position:absolute;left:0;right:0;top:240px;text-align:center'><img src='file://{ICON}' style='width:150px;height:150px;border-radius:36px;box-shadow:0 24px 60px rgba(0,0,0,.6),0 0 90px rgba(82,169,254,.6)'></div>"
         "<div style='position:absolute;left:140px;right:140px;top:440px'>"
         "<div class=titB style='position:relative;left:0;right:0;font-size:96px'>Tire sua dúvida<br><span class=b>de manutenção.</span></div><span class=lm></span>"
         "<div class=apoB style='position:relative;left:0;right:0;margin-top:30px;font-size:44px'>Óleo, revisão, corrente, ruídos.<br>Pergunte e nós respondemos.</div></div>"
         + CAIXA.format(top=1120))
    render(c, 1080, 1920, os.path.join(AQUI, 'B', 'story', 'story.jpg'))

if __name__ == '__main__':
    q = sys.argv[1] if len(sys.argv) > 1 else 'todos'
    if q in ('A', 'todos'): carrossel_A(); story_A(); carrossel_A_tiktok()
    if q in ('B', 'todos'): carrossel_B(); story_B(); carrossel_B_tiktok()
    if q == 'tiktok': carrossel_A_tiktok(); carrossel_B_tiktok()
