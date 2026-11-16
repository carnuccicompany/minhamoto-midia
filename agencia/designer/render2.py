#!/usr/bin/env python3
"""Renderizador v2 da agência MinhaMoto — sistemas visuais DARK, FOTO e CLARO.

Uso: python3 agencia/designer/render2.py agencia/roteiros/AG02.json
Roteiro: {"id","titulo","linha","estilo": "dark|foto|claro", "cards":[...], legendas}
Card (campo "layout"):
  capa   : kicker?, titulo, apoio?, print? | foto?  (mostra "Arrasta →")
  texto  : kicker?, titulo, apoio?
  numero : grande (ex.: "R$ ?" / "5x" / "0"), titulo, apoio?
  item   : n, titulo, apoio?, foto? | print?
  phone  : kicker?, titulo, apoio?, print
  cta    : titulo, apoio?, print?    (selos das lojas)
Destaque: *palavra* no titulo/apoio vira cor de acento (ou marca-texto no claro).
Quebra de linha manual: \n
Gera carrosseis/<ID>/NN.jpg (1080x1350 q92) e atualiza manifest.json.
"""
import json, os, sys, html, re

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(BASE, '..', '..'))
A = os.path.join(BASE, 'assets')

def fmt(t):
    t = html.escape(t or '').replace('\\n', '\n').replace('\n', '<br>')
    t = re.sub(r'\*(.+?)\*', r'<span class="ac">\1</span>', t)
    return t

def img_path(p, pasta):
    return p if os.path.isabs(p) else os.path.join(A, pasta, p)

FONTS = ''.join(
    f"@font-face{{font-family:Inter;src:url('file://{A}/fontes/inter-latin-{w}-normal.woff2');font-weight:{w}}}"
    for w in (400, 600, 700, 800, 900))

BASE_CSS = FONTS + """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;overflow:hidden;font-family:Inter,sans-serif;-webkit-font-smoothing:antialiased}
.k{font-weight:800;font-size:26px;letter-spacing:5px;text-transform:uppercase}
.t{font-weight:900;letter-spacing:-2.5px;line-height:1.02}
.a{font-weight:600;line-height:1.34}
.phone{position:absolute;background:#0a0a0c;border-radius:62px;padding:12px}
.phone img{display:block;width:100%;border-radius:50px}
.selos img{width:560px;display:block}
.swipe{position:absolute;z-index:5;font-weight:800;font-size:28px;letter-spacing:3px;text-transform:uppercase}
"""

# ---------------- DARK ----------------
DARK = """
body{background:#05080f}
.bg{position:absolute;inset:0;background:
 radial-gradient(70% 45% at 85% 8%, rgba(46,120,255,.30), rgba(46,120,255,0) 70%),
 radial-gradient(60% 40% at 0% 100%, rgba(46,120,255,.18), rgba(46,120,255,0) 70%),
 linear-gradient(175deg,#070b14,#04060b)}
.grid{position:absolute;inset:0;opacity:.07;background-image:
 linear-gradient(#fff 1px,transparent 1px),linear-gradient(90deg,#fff 1px,transparent 1px);background-size:90px 90px;
 -webkit-mask-image:radial-gradient(80% 60% at 70% 20%,#000,transparent)}
.k{color:#3d8bff}
.t{color:#f4f7fb}
.t .ac{color:#3d8bff}
.a{color:#9aabc4}
.a .ac{color:#fff;font-weight:800}
.phone{border:1px solid rgba(255,255,255,.08);box-shadow:0 50px 110px rgba(0,0,0,.75),0 0 120px rgba(46,120,255,.35)}
.big{font-weight:900;color:transparent;-webkit-text-stroke:3px #3d8bff;letter-spacing:-8px;line-height:.9}
.n{color:#3d8bff}
.swipe{color:#3d8bff}
.line{position:absolute;height:6px;width:110px;background:#3d8bff;border-radius:3px}
"""

# ---------------- CLARO ----------------
CLARO = """
body{background:#f3f1ec}
.bg{position:absolute;inset:0;background:#f3f1ec}
.k{color:#0c0f14}
.t{color:#0c0f14}
.t .ac{background:#1f5fff;color:#fff;padding:0 .14em;margin:0 -.04em;-webkit-box-decoration-break:clone;box-decoration-break:clone;border-radius:6px}
.a{color:#3a3f48}
.a .ac{color:#1f5fff;font-weight:800}
.phone{box-shadow:0 46px 90px rgba(12,15,20,.35),0 12px 26px rgba(12,15,20,.22)}
.big{font-weight:900;color:#1f5fff;letter-spacing:-10px;line-height:.86}
.n{color:#1f5fff}
.swipe{color:#fff;background:#0c0f14;padding:16px 28px;border-radius:40px}
.rule{position:absolute;left:84px;right:84px;height:3px;background:#0c0f14}
.tag{position:absolute;right:84px;font-weight:900;font-size:26px;letter-spacing:4px;color:#0c0f14}
"""

# ---------------- FOTO ----------------
FOTO = """
body{background:#04080e}
.bgimg{position:absolute;inset:0;background-size:cover}
.ov{position:absolute;inset:0;background:linear-gradient(to top,rgba(4,8,14,.96) 0%,rgba(4,8,14,.80) 32%,rgba(4,8,14,.25) 62%,rgba(4,8,14,.10) 100%)}
.k{color:#fff;background:#1f5fff;display:inline-block;padding:10px 18px;border-radius:8px;font-size:24px;letter-spacing:4px}
.t{color:#fff;text-transform:uppercase;text-shadow:0 4px 30px rgba(0,0,0,.45)}
.t .ac{color:#4b8dff}
.a{color:#dbe4ef}
.a .ac{color:#fff;font-weight:800}
.n{color:#4b8dff}
.swipe{color:#fff}
.phone{box-shadow:0 50px 110px rgba(0,0,0,.8)}
"""

STYLES = {'dark': DARK, 'claro': CLARO, 'foto': FOTO}

def page(estilo, body):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE_CSS}{STYLES[estilo]}</style></head><body>{body}{FIT_JS}</body></html>"

# encolhe fontes .fit até caber na caixa (max-height)
FIT_JS = """<script>
document.fonts.ready.then(()=>{document.querySelectorAll('.fit').forEach(el=>{
 let s=parseFloat(getComputedStyle(el).fontSize);const mh=parseFloat(el.style.maxHeight)||1e9;
 el.style.maxHeight='none';el.style.height='auto';
 while((el.scrollHeight>mh||el.scrollWidth>el.clientWidth+4)&&s>30){s-=2;el.style.fontSize=s+'px'}
});document.body.dataset.ok=1});
</script>"""

def phone_html(c, left, top, width, rot=0):
    p = img_path(c['print'], 'prints')
    return (f"<div class='phone' style='left:{left}px;top:{top}px;width:{width}px;transform:rotate({rot}deg)'>"
            f"<img src='file://{p}'></div>")

def box(cls, txt, left, top, width, height, size, extra=''):
    return (f"<div class='{cls} fit' style='position:absolute;left:{left}px;top:{top}px;width:{width}px;"
            f"max-height:{height}px;height:{height}px;font-size:{size}px;{extra}'>{fmt(txt)}</div>")

def boxauto(cls, txt, left, top, width, maxh, size, extra=''):
    return (f"<div class='{cls} fit' style='position:absolute;left:{left}px;top:{top}px;width:{width}px;"
            f"max-height:{maxh}px;font-size:{size}px;{extra}'>{fmt(txt)}</div>")

SELOS = f"<img src='file://{A}/selos-lojas.png'>"

# ------------------------------------------------------------------ DARK / CLARO (layout em fluxo)
def T(txt, size, maxh, extra=''):
    return f"<div class='t fit' style='font-size:{size}px;max-height:{maxh}px;{extra}'>{fmt(txt)}</div>"
def AP(txt, size=42, extra=''):
    return f"<div class='a' style='font-size:{size}px;margin-top:30px;{extra}'>{fmt(txt)}</div>" if txt else ''
def K(txt):
    return f"<div class='k' style='margin-bottom:26px'>{fmt(txt)}</div>" if txt else ''
def col(inner, top, bottom, justify='flex-start', left=84, right=84):
    return (f"<div style='position:absolute;left:{left}px;right:{right}px;top:{top}px;bottom:{bottom}px;"
            f"display:flex;flex-direction:column;justify-content:{justify}'>{inner}</div>")
def phone_flow(c, width=500, rot=0):
    p = img_path(c['print'], 'prints')
    return (f"<div style='flex:1;position:relative;margin-top:56px;min-height:300px'>"
            f"<div class='phone' style='left:50%;top:0;width:{width}px;margin-left:-{width//2}px;transform:rotate({rot}deg)'>"
            f"<img src='file://{p}'></div></div>")

def flow(c, i, total, est):
    L = c['layout']; k = c.get('kicker'); out = ''
    top = 200 if est == 'claro' else 110
    if L == 'capa':
        has_p = bool(c.get('print'))
        if has_p:
            out += col(K(k) + T(c['titulo'], 124, 470) + AP(c.get('apoio'), 42, 'max-width:470px'), top, 200)
            out += phone_html(c, 600, 790, 430, -7 if est == 'dark' else 6)
        else:
            out += col(K(k) + T(c['titulo'], 132, 560) + AP(c.get('apoio'), 44, 'max-width:820px'), top, 200)
            if c.get('grande'):
                out += (f"<div class='big' style='position:absolute;right:56px;bottom:40px;font-size:440px;"
                        f"line-height:.8'>{fmt(c['grande'])}</div>")
        out += (f"<div class='swipe' style='left:84px;bottom:96px'>Arrasta →</div>")
    elif L == 'texto':
        out += col(K(k) + T(c['titulo'], 104, 620) + AP(c.get('apoio'), 46), top, 120, 'center')
    elif L == 'numero':
        out += col(f"<div class='big fit' style='font-size:340px;max-height:380px'>{fmt(c['grande'])}</div>"
                   + T(c['titulo'], 90, 420, 'margin-top:30px') + AP(c.get('apoio'), 44), top, 120, 'center')
    elif L == 'item':
        n = html.escape(str(c['n']).zfill(2))
        num = f"<div class='big' style='font-size:230px;margin-bottom:10px'>{n}</div>"
        if c.get('print'):
            out += col(num + T(c['titulo'], 76, 420) + AP(c.get('apoio'), 38), top, 120, 'center', 84, 470)
            out += phone_html(c, 640, 380 if est == 'dark' else 460, 380, 0 if est == 'dark' else 5)
        else:
            out += col(num + T(c['titulo'], 100, 500) + AP(c.get('apoio'), 46), top, 120, 'center')
    elif L == 'phone':
        out += col(K(k) + T(c['titulo'], 84, 340) + AP(c.get('apoio'), 38) + phone_flow(c), top, -400)
    elif L == 'cta':
        icon = (f"<img src='file://{A}/icon.png' style='width:128px;border-radius:30px;margin-bottom:46px;"
                f"box-shadow:0 0 70px rgba(46,120,255,.45)'>")
        out += col(icon + T(c['titulo'], 108, 520) + AP(c.get('apoio'), 44)
                   + f"<div class='selos' style='margin-top:64px'>{SELOS}</div>", top, 120, 'center')
    return out

def dark(c, i, total):
    return "<div class='bg'></div><div class='grid'></div>" + flow(c, i, total, 'dark')

def claro(c, i, total):
    head = (f"<div class='bg'></div><div class='rule' style='top:92px'></div>"
            f"<div class='k' style='position:absolute;left:84px;top:116px;font-size:24px'>{fmt(c.get('marca','MinhaMoto'))}</div>"
            f"<div class='tag' style='top:116px'>{i:02d}/{total:02d}</div>")
    return head + flow(c, i, total, 'claro')

# ------------------------------------------------------------------ FOTO
def foto(c, i, total):
    L = c['layout']
    f = img_path(c.get('foto', ''), 'fotos') if c.get('foto') else ''
    out = (f"<div class='bgimg' style=\"background-image:url('file://{f}');background-position:{c.get('pos','center')}\"></div>"
           if f else "<div class='bgimg' style='background:#0b1220'></div>")
    out += "<div class='ov'></div>"
    k = c.get('kicker')
    if L in ('capa', 'texto', 'item', 'numero'):
        pre = ''
        if L == 'item': pre = f"<div class='n' style='font-weight:900;font-size:64px;margin-bottom:10px'>{html.escape(str(c['n']).zfill(2))}</div>"
        if L == 'numero': pre = f"<div class='n' style='font-weight:900;font-size:200px;line-height:.9;letter-spacing:-6px;margin-bottom:10px'>{fmt(c['grande'])}</div>"
        if k: pre += f"<div class='k' style='margin-bottom:26px'>{fmt(k)}</div>"
        tsize = 118 if L == 'capa' else 96
        ap = f"<div class='a' style='font-size:42px;margin-top:26px;max-width:880px'>{fmt(c['apoio'])}</div>" if c.get('apoio') else ''
        swipe = "<div class='swipe' style='position:static;margin-top:44px'>Arrasta →</div>" if L == 'capa' else ''
        out += (f"<div style='position:absolute;left:76px;right:76px;bottom:{110 if L=='capa' else 120}px'>{pre}"
                f"<div class='t fit' style='font-size:{tsize}px;max-height:560px'>{fmt(c['titulo'])}</div>{ap}{swipe}</div>")
    elif L == 'cta':
        out += f"<img src='file://{A}/icon.png' style='position:absolute;left:76px;top:120px;width:120px;border-radius:28px'>"
        out += (f"<div style='position:absolute;left:76px;right:76px;bottom:120px'>"
                f"<div class='t fit' style='font-size:100px;max-height:520px'>{fmt(c['titulo'])}</div>"
                + (f"<div class='a' style='font-size:42px;margin-top:26px'>{fmt(c['apoio'])}</div>" if c.get('apoio') else '')
                + f"<div class='selos' style='margin-top:50px'>{SELOS}</div></div>")
    elif L == 'phone':
        out += boxauto('t', c['titulo'], 76, 110, 928, 300, 84)
        if c.get('apoio'): out += boxauto('a', c['apoio'], 76, 430, 900, 140, 38)
        out += phone_html(c, 310, 640, 460, 0)
    return out

BUILD = {'dark': dark, 'claro': claro, 'foto': foto}

def main(path):
    rot = json.load(open(path, encoding='utf-8'))
    rid, est = rot['id'], rot['estilo']
    outdir = os.path.join(REPO, 'carrosseis', rid)
    os.makedirs(outdir, exist_ok=True)
    for f in os.listdir(outdir):
        if f.endswith('.jpg'): os.remove(os.path.join(outdir, f))
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        args = ['--no-sandbox', '--force-color-profile=srgb']
        b = (pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=args)
             if os.path.exists('/usr/bin/google-chrome') else pw.chromium.launch(args=args))
        pg = b.new_page(viewport={'width': 1080, 'height': 1350})
        total = len(rot['cards'])
        for i, card in enumerate(rot['cards'], 1):
            doc = page(card.get('estilo', est), BUILD[card.get('estilo', est)](card, i, total))
            tmp = f'/tmp/card2_{rid}_{i}.html'
            open(tmp, 'w', encoding='utf-8').write(doc)
            pg.goto('file://' + tmp)
            pg.wait_for_selector('body[data-ok]', timeout=10000)
            pg.wait_for_timeout(150)
            pg.screenshot(path=os.path.join(outdir, f'{i:02d}.jpg'), type='jpeg', quality=92)
        b.close()
    mpath = os.path.join(REPO, 'manifest.json')
    m = json.load(open(mpath, encoding='utf-8'))
    m[rid] = {'origem': f"agencia v2 ({est}) - {rot['titulo']}",
              'cards': [f'{i:02d}.jpg' for i in range(1, len(rot['cards']) + 1)]}
    json.dump(m, open(mpath, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(rid, 'ok', len(rot['cards']), 'cards')

if __name__ == '__main__':
    for p in sys.argv[1:]:
        main(p)
