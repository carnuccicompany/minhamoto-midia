#!/usr/bin/env python3
"""Renderizador oficial da agência MinhaMoto.

Uso: python3 agencia/designer/render.py agencia/roteiros/D201.json
Gera carrosseis/<ID>/01.jpg ... NN.jpg (1080x1350, q92) e atualiza manifest.json.

Tipos de card aceitos no roteiro:
  foto:      capa | passo | texto           (campos: titulo, apoio, foto, pos?, n)
  produto:   capa_produto | card_produto | cta  (titulo_navy, titulo_azul, apoio, print, rodape?)
  editorial: editorial                      (titulo, titulo_azul?, apoio, tema: claro|escuro)
O template do carrossel é o campo "template", mas cada card pode misturar
(ex.: carrossel foto com último card cta).
"""
import json, os, sys, html

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(BASE, '..', '..'))
ASSETS = os.path.join(BASE, 'assets')

def esc(t):
    return html.escape(t or '').replace('\\n', '<br>').replace('\n', '<br>')

def tam_titulo(t, base=84):
    n = len(t or '')
    if n <= 26: return base
    if n <= 44: return base - 10
    if n <= 64: return base - 20
    return base - 26

def marca_azul(texto):
    """Destaca MinhaMoto (e trechos entre *asteriscos*) em azul no apoio."""
    t = esc(texto)
    t = t.replace('MinhaMoto', '<b>MinhaMoto</b>')
    while '*' in t:
        t = t.replace('*', '<b>', 1).replace('*', '</b>', 1)
    return t

def tpl(nome):
    with open(os.path.join(BASE, 'templates', nome), encoding='utf-8') as f:
        return f.read().replace('%%ASSETS%%', ASSETS)

def html_foto(c):
    titulo = c['titulo'] if 'n' not in c else f"{c['n']}) {c['titulo']}"
    foto = c['foto']
    if not os.path.isabs(foto):
        foto = os.path.join(ASSETS, 'fotos', foto)
    apoio = f"<p>{esc(c['apoio'])}</p>" if c.get('apoio') else ''
    return (tpl('foto.html')
            .replace('%%FOTO%%', foto)
            .replace('%%POS%%', c.get('pos', 'center'))
            .replace('%%TSIZE%%', str(tam_titulo(titulo, 80)))
            .replace('%%TITULO%%', esc(titulo))
            .replace('%%APOIO%%', apoio))

def titulo_duotone(c):
    navy, azul = esc(c.get('titulo_navy', '')), esc(c.get('titulo_azul', ''))
    sep = '<br>' if c.get('quebra', True) and navy and azul else ' '
    return (navy + (sep if navy and azul else '') +
            (f"<span class='az'>{azul}</span>" if azul else ''))

def html_produto(c):
    titulo = titulo_duotone(c)
    texto_len = len(c.get('titulo_navy', '') + c.get('titulo_azul', ''))
    tsize = tam_titulo('x' * texto_len, 82)
    apoio = f"<div class='apoio'>{marca_azul(c['apoio'])}</div>" if c.get('apoio') else ''
    phone, rodape, selos, fade = '', '', '', ''
    if c.get('print'):
        p = c['print']
        if not os.path.isabs(p):
            p = os.path.join(ASSETS, 'prints', p)
        pw = c.get('phone_w', 365)
        pm = c.get('phone_m', 48)
        phone = f"<div class='phone'><img src='file://{p}'></div>"
        if c.get('cortar_base'):
            fade = "<div class='fade'></div>"
        phone = phone.replace('%%PW%%', str(pw))
    if c['tipo'] == 'capa_produto':
        rodape = f"<div class='rodape'>{esc(c.get('rodape', 'Deslize para entender'))} &nbsp;&#8594;</div>"
    if c['tipo'] == 'cta':
        selos = f"<div class='selos'><img src='file://{ASSETS}/selos-lojas.png'></div>"
    out = (tpl('produto.html')
           .replace('%%TSIZE%%', str(tsize))
           .replace('%%TITULO%%', titulo)
           .replace('%%APOIO%%', apoio)
           .replace('%%PHONE%%', phone)
           .replace('%%PW%%', str(c.get('phone_w', 365)))
           .replace('%%PM%%', str(c.get('phone_m', 48)))
           .replace('%%FADE%%', fade)
           .replace('%%RODAPE%%', rodape)
           .replace('%%SELOS%%', selos))
    return out

TEMAS = {
    'claro':  dict(BG='linear-gradient(160deg,#d7e4f3,#eef4fb)', COR_TITULO='#16365c', COR_DESTAQUE='#2f6fe4', COR_APOIO='#5b6b80'),
    'escuro': dict(BG='linear-gradient(165deg,#0d2236,#17405f 60%,#1b4e6b)', COR_TITULO='#f2f7fc', COR_DESTAQUE='#7fd4e8', COR_APOIO='#b8cfdd'),
}

def html_editorial(c):
    tema = TEMAS[c.get('tema', 'claro')]
    if c.get('titulo_navy') or c.get('titulo_azul'):
        titulo = titulo_duotone(c)
        tlen = len(c.get('titulo_navy', '') + c.get('titulo_azul', ''))
    else:
        titulo, tlen = esc(c['titulo']), len(c.get('titulo', ''))
    apoio = f"<p>{marca_azul(c['apoio'])}</p>" if c.get('apoio') else ''
    out = tpl('editorial.html')
    for k, v in tema.items():
        out = out.replace(f'%%{k}%%', v)
    return (out.replace('%%TSIZE%%', str(tam_titulo('x' * tlen, 88)))
               .replace('%%TITULO%%', titulo)
               .replace('%%APOIO%%', apoio))

BUILDERS = {'capa': html_foto, 'passo': html_foto, 'texto': html_foto,
            'capa_produto': html_produto, 'card_produto': html_produto, 'cta': html_produto,
            'editorial': html_editorial}

def main(path):
    rot = json.load(open(path, encoding='utf-8'))
    rid = rot['id']
    outdir = os.path.join(REPO, 'carrosseis', rid)
    os.makedirs(outdir, exist_ok=True)

    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path='/usr/bin/google-chrome',
                               args=['--no-sandbox', '--force-color-profile=srgb'])
        pg = b.new_page(viewport={'width': 1080, 'height': 1350})
        for i, card in enumerate(rot['cards'], 1):
            doc = BUILDERS[card['tipo']](card)
            tmp = f'/tmp/card_{rid}_{i}.html'
            open(tmp, 'w', encoding='utf-8').write(doc)
            pg.goto('file://' + tmp)
            pg.wait_for_timeout(250)
            pg.screenshot(path=os.path.join(outdir, f'{i:02d}.jpg'), type='jpeg', quality=92)
            print(f'{rid}/{i:02d}.jpg ok')
        b.close()

    mpath = os.path.join(REPO, 'manifest.json')
    m = json.load(open(mpath, encoding='utf-8'))
    m[rid] = {'origem': f"agencia - {rot['titulo']}",
              'cards': [f'{i:02d}.jpg' for i in range(1, len(rot['cards']) + 1)]}
    json.dump(m, open(mpath, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('manifest atualizado')

if __name__ == '__main__':
    main(sys.argv[1])
