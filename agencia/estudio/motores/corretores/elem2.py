"""Conjunto 2 de elementos (25/11) — pra variar dos aprovados do EST2-A/EST8 (pedido do Léo: "você tá usando os mesmos
elementos em tudo"). Mesmas regras: centralizados acima da legenda do pronto (base 1335), cores do Mapa, Poppins,
ligados ao que ela fala, tempo pra ler. Estilos: anel de contagem, pílulas-adesivo inclinadas, palavra que troca
dentro de uma pílula navy, "Dúvida" riscada virando "Certeza", fileira de cartões navy que viram (flip)."""
from v3 import *
from elem import tl, FAIXA_Y

def _pilula_img(s, ic, tam=30, fundo=BRANCO, cor_txt=NAVY, cor_ic=TEAL):
    """Pílula pequena (RGBA própria) com disco de ícone à esquerda; volta a imagem pra poder girar/escalar."""
    tw = tl(s, 700, tam); h = int(tam * 2.3); r = h // 2 - 8
    w = int(10 + 2 * r + 16 + tw + 30)
    im = Image.new("RGBA", (w + 40, h + 50), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((20, 30, 20 + w, 30 + h), h / 2, fill=(0, 0, 0, 80))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(im); d.rounded_rectangle((20, 20, 20 + w, 20 + h), h / 2, fill=fundo + (255,))
    cx, cy = 20 + 10 + r, 20 + h / 2
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=cor_ic + (255,))
    if ic:
        icn = Image.open(ICON + ic + ".png").convert("RGBA").resize((int(r * 1.2), int(r * 1.2)), Image.LANCZOS)
        im.alpha_composite(icn, (int(cx - r * 0.6), int(cy - r * 0.6)))
    d.text((cx + r + 16, cy), s, font=fonte(700, tam), fill=cor_txt + (255,), anchor="lm")
    return im

def _colar(img, lay, cx, cy, esc=1.0, ang=0.0, alpha=1.0):
    if alpha <= 0 or esc <= 0.02: return
    if esc != 1.0: lay = lay.resize((max(1, int(lay.width * esc)), max(1, int(lay.height * esc))), Image.LANCZOS)
    if ang: lay = lay.rotate(ang, resample=Image.BICUBIC, expand=True)
    if alpha < 1: lay = lay.copy(); lay.putalpha(lay.getchannel("A").point(lambda v: int(v * alpha)))
    img.alpha_composite(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)))

_cache = {}
def _pil(s, ic, tam, **kw):
    k = (s, ic, tam, tuple(sorted(kw.items())))
    if k not in _cache: _cache[k] = _pilula_img(s, ic, tam, **kw)
    return _cache[k]

def anel(img, t, t0, t1, alvo=120, rotulo="mapas visuais"):
    """Contador dentro de um anel que vai se fechando (variação do contador da faixa)."""
    if not (t0 <= t < t1 + 0.3): return
    a = ease((t - t0) / 0.25) * (1 - ease((t - t1) / 0.3)); k = mola((t - t0) / 0.5)
    p = ease((t - t0) / 1.1); n = int(alvo * p)
    R = 140; cx = W / 2; cy = FAIXA_Y - R - 76 + int((1 - k) * 30)
    disco(img, cx, cy, R, BRANCO, a * 0.96)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.arc((cx - R + 14, cy - R + 14, cx + R - 14, cy + R - 14), 0, 360, fill=(222, 229, 238, int(255 * a)), width=14)
    if p > 0: d.arc((cx - R + 14, cy - R + 14, cx + R - 14, cy + R - 14), -90, -90 + 360 * p, fill=TEAL + (int(255 * a),), width=14)
    img.alpha_composite(lay)
    texto(img, (cx, cy - 6), f"+{n}", 800, 84, NAVY, a, anchor="mm")
    # rótulo numa pílula navy embaixo do anel
    tw = tl(rotulo, 700, 34); pw, ph = tw + 60, 64; py = cy + R + 4
    caixa(img, cx - pw / 2, py, cx + pw / 2, py + ph, ph / 2, NAVY, a)
    texto(img, (cx, py + ph / 2), rotulo, 700, 34, BRANCO, a, anchor="mm")
    if p >= 1: particulas(img, cx, cy, t - (t0 + 1.1), n=12, raio=170, seed=301)

def adesivos(img, t, t_in, t_out, itens, titulo=None, seed=400, tam=38, larg=960):
    """Pílulas-adesivo que pulam inclinadas (±3°), em até duas linhas, com título numa pílula navy por cima."""
    if not (t_in <= t < t_out + 0.3): return
    a = ease((t - t_in) / 0.3) * (1 - ease((t - t_out) / 0.3))
    pils = [_pil(s, ic, tam) for _, ic, s in itens]
    # quebra em linhas pela largura
    linhas, cur, cw = [], [], 0
    for i, p in enumerate(pils):
        if cur and cw + p.width - 30 > larg: linhas.append(cur); cur, cw = [], 0
        cur.append(i); cw += p.width - 30
    linhas.append(cur)
    lh = pils[0].height - 34; base = FAIXA_Y - 10
    rng = np.random.default_rng(seed); angs = rng.choice([-3, -2, 2, 3], size=len(pils))
    for li, lin in enumerate(linhas):
        cy = base - (len(linhas) - 1 - li) * lh - lh / 2
        tot = sum(pils[i].width - 30 for i in lin); x = W / 2 - tot / 2
        for i in lin:
            tk = itens[i][0]; pw = pils[i].width - 30
            if t >= tk:
                q = (t - tk) / 0.45
                _colar(img, pils[i], x + pw / 2, cy, esc=mola(q), ang=angs[i] * (1 - 0.3 * ease(q)), alpha=a * ease(q * 3))
                particulas(img, x + pw / 2, cy, t - tk, n=8, raio=90, seed=seed + i)
            x += pw
    if titulo:
        ty = base - len(linhas) * lh - 40; tw = tl(titulo, 700, 36)
        caixa(img, W / 2 - tw / 2 - 36, ty - 33, W / 2 + tw / 2 + 36, ty + 33, 33, NAVY, a)
        texto(img, (W / 2, ty), titulo, 700, 36, BRANCO, a, anchor="mm")

def palavra(img, t, itens, t_out, tam=66):
    """Uma pílula navy só; a palavra troca com deslize de baixo pra cima, ícone teal e sublinhado que cresce."""
    t_in = itens[0][0] - 0.15
    if not (t_in <= t < t_out + 0.3): return
    a = ease((t - t_in) / 0.3) * (1 - ease((t - t_out) / 0.3))
    i = max(k for k, it in enumerate(itens) if t >= it[0] - 0.15)
    tk, ic, s = itens[i]; q = ease((t - (tk - 0.15)) / 0.35)
    def larg(j): return 110 + tl(itens[j][2], 800, tam) + 60
    w = larg(i) if i == 0 else larg(i - 1) + (larg(i) - larg(i - 1)) * q
    h = 140; x0 = W / 2 - w / 2; y0 = FAIXA_Y - h + int((1 - mola((t - t_in) / 0.5)) * 30)
    caixa(img, x0, y0, x0 + w, y0 + h, h / 2, NAVY, a)
    cx, cy = x0 + 70, y0 + h / 2
    r = int(42 * mola((t - (tk - 0.15)) / 0.45)); disco(img, cx, cy, r, TEAL, a, sombra=False)
    if r > 14: icone(img, ic, cx, cy, int(r * 1.15), a)
    # palavra nova sobe; a anterior sai pra cima (recortado dentro da pílula)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    tx = x0 + 128; dy = int((1 - q) * 50)
    d.text((tx, cy + dy), s, font=fonte(800, tam), fill=BRANCO + (int(255 * a * q),), anchor="lm")
    if i > 0 and q < 1:
        d.text((tx, cy - int(q * 50)), itens[i - 1][2], font=fonte(800, tam), fill=BRANCO + (int(255 * a * (1 - q)),), anchor="lm")
    m = Image.new("L", img.size, 0); ImageDraw.Draw(m).rounded_rectangle((x0, y0 + 8, x0 + w, y0 + h - 8), h / 2, fill=255)
    lay.putalpha(Image.fromarray(np.minimum(np.array(lay.getchannel("A")), np.array(m))))
    img.alpha_composite(lay)
    uw = tl(s, 800, tam) * ease((t - tk) / 0.4)
    if uw > 2: caixa(img, tx, cy + 40, tx + uw, cy + 48, 4, TEAL, a, sombra=False)

def riscado(img, t, t0, tv, t1, de="Dúvida", para="Certeza"):
    """'Dúvida' em coral é riscada; em tv entra 'Certeza' em teal com check."""
    if not (t0 <= t < t1 + 0.3): return
    a = ease((t - t0) / 0.25) * (1 - ease((t - t1) / 0.3))
    tam = 50; w1 = tl(de, 800, tam); w2 = tl(para, 800, tam)
    wfull = 50 + w1 + 40 + 56 + 40 + 64 + 14 + w2 + 50
    q = ease((t - tv) / 0.4) if t >= tv else 0
    w = (50 + w1 + 50) + (wfull - (50 + w1 + 50)) * q
    h = 130; x0 = W / 2 - w / 2; y0 = FAIXA_Y - h + int((1 - mola((t - t0) / 0.5)) * 30)
    caixa(img, x0, y0, x0 + w, y0 + h, 36, BRANCO, a * 0.96)
    cy = y0 + h / 2; x = x0 + 50
    texto(img, (x, cy), de, 800, tam, CORAL, a * (1 - 0.45 * q), anchor="lm")
    s = ease((t - (t0 + 0.3)) / 0.35)
    if s > 0: caixa(img, x - 6, cy - 4, x - 6 + (w1 + 12) * s, cy + 6, 4, CORAL, a, sombra=False)
    if q > 0:
        xa = x + w1 + 40
        icone(img, "arrow-right", xa + 28, cy, 56, a * q)
        xc = xa + 56 + 40 + 32; r = int(32 * mola((t - tv) / 0.4))
        disco(img, xc, cy, r, TEAL, a, sombra=False)
        if r > 10: icone(img, "check", xc, cy, int(r * 1.2), a)
        texto(img, (xc + 32 + 14, cy), para, 800, tam, TEAL, a * q, anchor="lm")
        particulas(img, xc, cy, t - tv, n=10, raio=110, seed=377)

def cartoes_flip(img, t, t_in, t_out, itens, titulo=None, cw=172, ch=172, gap=14):
    """Fileira de cartões navy que viram (flip horizontal) um a um: ícone branco + rótulo teal claro."""
    if not (t_in <= t < t_out + 0.3): return
    a = ease((t - t_in) / 0.3) * (1 - ease((t - t_out) / 0.3))
    n = len(itens); tot = n * cw + (n - 1) * gap; x0 = W / 2 - tot / 2; y1 = FAIXA_Y - 10; y0 = y1 - ch
    if titulo:
        tw = tl(titulo, 700, 36)
        caixa(img, W / 2 - tw / 2 - 36, y0 - 90, W / 2 + tw / 2 + 36, y0 - 22, 34, BRANCO, a)
        texto(img, (W / 2, y0 - 56), titulo, 700, 36, NAVY, a, anchor="mm")
    for k, (tk, ic, rot) in enumerate(itens):
        if t < tk: continue
        q = (t - tk) / 0.4; sx = abs(math.cos((1 - ease(q)) * math.pi / 2)) if q < 1 else 1.0
        cx = x0 + k * (cw + gap) + cw / 2; ww = cw * sx
        if ww < 3: continue
        caixa(img, cx - ww / 2, y0, cx + ww / 2, y1, 26, NAVY, a)
        if sx > 0.5:
            al = a * (sx - 0.5) * 2
            iw = int(64 * sx)
            if iw > 8: icone(img, ic, cx, y0 + 66, int(iw * 1.15), al)
            texto(img, (cx, y0 + 136), rot, 700, 27 if n <= 5 else 22, (120, 222, 200), al, anchor="mm")
