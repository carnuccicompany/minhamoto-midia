"""Conjunto 4 de elementos (25/11) — linguagem visual do PRÓPRIO Mapa (círculos numerados, caixas ALERTA/SAÍDA, fluxo
com setas, rota). Pro criativo "Folheando o Mapa". Mesmas regras: centralizado acima da legenda (base 1335), cores do Mapa,
Poppins caixa normal, ligado ao que ela fala, tempo pra ler, cartão do tamanho do texto."""
from v3 import *
from elem import tl, FAIXA_Y

CORES = [TEAL, CORAL, NAVY, TEAL, CORAL, NAVY]

def _num(img, cx, cy, r, n, cor, a):
    disco(img, cx, cy, r, cor, a, sombra=False)
    texto(img, (cx, cy + 1), str(n), 800, int(r * 1.15), BRANCO, a, anchor="mm")

def hook_mapa(img, t, t_hdr, t_renda, itens, t_fim, topo="Corretor, você sabe…", renda="Renda do cliente"):
    """Mini-mapa do gancho no estilo do material: cabeçalho navy, chip "Renda do cliente", seta, e as perguntas em caixas
    numeradas (círculo colorido 1/2/3) que entram quando ela fala. O cartão cresce com o conteúdo (nunca sobra branco)."""
    if not (t_hdr <= t < t_fim): return
    a = ease((t - t_hdr) / 0.3) * (1 - ease((t - (t_fim - 0.18)) / 0.18))
    tam = 50; rh = 112; gap = 14
    w = max(760, max(150 + tl(s, 700, tam) + 60 for _, _, s in itens)); x0 = W / 2 - w / 2
    y0 = 160 + int((1 - mola((t - t_hdr) / 0.5)) * -40)
    hh = 92; chip_h = 96
    # altura alvo conforme o que já entrou (anima o crescimento)
    def alt(nitens): return hh + (36 + chip_h + 30 if t >= t_renda else 0) + (nitens * (rh + gap) + 40 if nitens else 0) + 24
    vis = [k for k, it in enumerate(itens) if t >= it[0]]
    h = alt(len(vis))
    if vis:
        q = ease((t - itens[vis[-1]][0]) / 0.3); h = alt(len(vis) - 1) + (h - alt(len(vis) - 1)) * q
    elif t >= t_renda:
        q = ease((t - t_renda) / 0.3); h = hh + 24 + (36 + chip_h + 30) * q
    caixa(img, x0, y0, x0 + w, y0 + h, 40, BRANCO, a * 0.97)
    caixa(img, x0, y0, x0 + w, y0 + hh, 40, NAVY, a, sombra=False); caixa(img, x0, y0 + 46, x0 + w, y0 + hh, 0, NAVY, a, sombra=False)
    texto(img, (W / 2, y0 + hh / 2), topo, 800, 48, BRANCO, a, anchor="mm")
    cy = y0 + hh + 36 + chip_h / 2
    if t >= t_renda:
        q = (t - t_renda) / 0.45; s = mola(q); tw = tl(renda, 700, 44); pw = (tw + 150) * s; ph = chip_h
        caixa(img, W / 2 - pw / 2, cy - ph / 2, W / 2 + pw / 2, cy + ph / 2, ph / 2, (232, 246, 243), a, sombra=False)
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((W / 2 - pw / 2, cy - ph / 2, W / 2 + pw / 2, cy + ph / 2), ph / 2, outline=TEAL + (int(255 * a),), width=4); img.alpha_composite(lay)
        if s > 0.8:
            al = a * min(1, (s - 0.8) / 0.2)
            disco(img, W / 2 - tw / 2 - 32, cy, 32, TEAL, al, sombra=False); icone(img, "report-money", W / 2 - tw / 2 - 32, cy, 38, al)
            texto(img, (W / 2 - tw / 2 + 16, cy), renda, 700, 44, NAVY, al, anchor="lm")
        particulas(img, W / 2, cy, t - t_renda, n=8, raio=140, seed=601)
    base = cy + chip_h / 2 + 30
    if vis: _ic_cor(img, "arrow-down", W / 2, base + 2, 40, (170, 182, 198), a * ease((t - itens[0][0]) / 0.3))
    base += 26
    for k, (tk, ic, txt) in enumerate(itens):
        if t < tk: continue
        q = (t - tk) / 0.45; ry = base + k * (rh + gap); al = a * ease(q * 2); dx = int((1 - ease(q)) * 80)
        caixa(img, x0 + 30 + dx, ry, x0 + w - 30 + dx, ry + rh, 26, (244, 247, 250), al, sombra=False)
        caixa(img, x0 + 30 + dx, ry, x0 + 42 + dx, ry + rh, 0, CORES[k], al, sombra=False)
        _num(img, x0 + 100 + dx, ry + rh / 2, int(36 * mola(q)), k + 1, CORES[k], a)
        texto(img, (x0 + 158 + dx, ry + rh / 2), txt, 700, tam, NAVY, al, anchor="lm")
        particulas(img, x0 + 100, ry + rh / 2, t - tk, n=8, raio=100, seed=610 + k)

def pilha(img, t, t0, t1, alvo=120, rotulo="mapas visuais"):
    """Contador: três páginas brancas se abrindo em leque atrás de um cartão navy com "+120"."""
    if not (t0 <= t < t1 + 0.3): return
    a = ease((t - t0) / 0.25) * (1 - ease((t - t1) / 0.3)); k = mola((t - t0) / 0.5)
    n = int(alvo * ease((t - t0) / 1.0)); cx = W / 2; cy = FAIXA_Y - 120 + int((1 - k) * 30)
    pw, ph = 230, 170
    for i, ang in enumerate((-14, 0, 14)):
        e = ease((t - t0 - 0.1 * i) / 0.4) * ang
        pg = Image.new("RGBA", (pw + 40, ph + 40), (0, 0, 0, 0)); dd = ImageDraw.Draw(pg)
        dd.rounded_rectangle((20, 20, 20 + pw, 20 + ph), 16, fill=(255, 255, 255, int(255 * a)), outline=(214, 222, 232, int(255 * a)), width=3)
        dd.rounded_rectangle((40, 38, 40 + pw * 0.6, 54), 6, fill=CORES[i] + (int(255 * a),))
        for j in range(4): dd.rounded_rectangle((40, 72 + j * 24, 40 + pw * (0.85 - 0.12 * (j % 2)), 82 + j * 24), 4, fill=(222, 229, 238, int(255 * a)))
        pg = pg.rotate(-e, resample=Image.BICUBIC, expand=True)
        img.alpha_composite(pg, (int(cx - 150 + i * 150 - pg.width / 2 + (1 - i) * 0), int(cy - 40 - pg.height / 2)))
    w = 120 + tl(f"+{alvo}", 800, 70) + 30 + tl(rotulo, 700, 34) + 60; h = 120
    caixa(img, cx - w / 2, cy + 10, cx + w / 2, cy + 10 + h, h / 2, NAVY, a)
    disco(img, cx - w / 2 + 64, cy + 10 + h / 2, 40, TEAL, a, sombra=False); icone(img, "stack-2", cx - w / 2 + 64, cy + 10 + h / 2, 48, a)
    xt = cx - w / 2 + 120; texto(img, (xt, cy + 10 + h / 2), f"+{n}", 800, 70, BRANCO, a, anchor="lm")
    texto(img, (xt + tl(f"+{alvo}", 800, 70) + 30, cy + 10 + h / 2 + 4), rotulo, 700, 34, (120, 222, 200), a, anchor="lm")

def fluxo(img, t, t_in, t_out, itens, titulo=None):
    """Fluxo numerado do Mapa: círculos 1..n ligados por uma linha que vai se desenhando; rótulo embaixo de cada um."""
    if not (t_in <= t < t_out + 0.3): return
    a = ease((t - t_in) / 0.3) * (1 - ease((t - t_out) / 0.3))
    n = len(itens); cw = min(160, 930 / n); w = n * cw + 40; h = 210 + (60 if titulo else 0)
    x0 = W / 2 - w / 2; y0 = FAIXA_Y - h + int((1 - mola((t - t_in) / 0.5)) * 30)
    caixa(img, x0, y0, x0 + w, y0 + h, 34, BRANCO, a * 0.96)
    ty = y0 + (56 if titulo else 0)
    if titulo: texto(img, (W / 2, y0 + 40), titulo, 800, 38, NAVY, a, anchor="mm")
    cy = ty + 72; xs = [x0 + 20 + cw * k + cw / 2 for k in range(n)]
    ult = max([k for k, it in enumerate(itens) if t >= it[0]], default=-1)
    if ult >= 1:
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        q = ease((t - itens[ult][0]) / 0.3); xe = xs[ult - 1] + (xs[ult] - xs[ult - 1]) * q
        d.line((xs[0], cy, xe, cy), fill=(205, 214, 226, int(255 * a)), width=6); img.alpha_composite(lay)
    for k, (tk, ic, rot) in enumerate(itens):
        if t < tk: continue
        q = (t - tk) / 0.45; r = int(50 * mola(q))
        disco(img, xs[k], cy, r, CORES[k], a, sombra=False)
        if r > 14: icone(img, ic, xs[k], cy, int(r * 1.1), a)
        texto(img, (xs[k], cy + 84), rot, 700, 23 if n >= 6 else 28, NAVY, a * ease(q * 3), anchor="mm")
        particulas(img, xs[k], cy, t - tk, n=8, raio=80, seed=640 + k)

def blocos(img, t, itens, t_out, tam=52):
    """Três blocos coloridos (teal / coral / navy, como os cabeçalhos do Mapa) que caem com quique, um por palavra."""
    t_in = itens[0][0] - 0.15
    if not (t_in <= t < t_out + 0.3): return
    a = ease((t - t_in) / 0.3) * (1 - ease((t - t_out) / 0.3))
    gap = 18
    while True:
        ws = [96 + tl(s, 800, tam) + 34 for _, _, s in itens]; tot = sum(ws) + gap * (len(ws) - 1)
        if tot <= 980 or tam <= 30: break
        tam -= 2
    x = W / 2 - tot / 2; h = 116; y1 = FAIXA_Y - 14
    for k, ((tk, ic, s), wd) in enumerate(zip(itens, ws)):
        if t >= tk - 0.15:
            q = (t - (tk - 0.15)) / 0.5; dy = int((1 - mola(q)) * -160)
            caixa(img, x, y1 - h + dy, x + wd, y1 + dy, 26, CORES[k], a * ease(q * 3))
            disco(img, x + 52, y1 - h / 2 + dy, 30, BRANCO, a * ease(q * 3), sombra=False)
            _ic_cor(img, ic, x + 52, y1 - h / 2 + dy, 36, CORES[k], a * ease(q * 3))
            texto(img, (x + 96, y1 - h / 2 + dy), s, 800, tam, BRANCO, a * ease(q * 3), anchor="lm")
        x += wd + gap

_icc = {}
def _ic_cor(img, nome, cx, cy, tam, cor, alpha):
    k = (nome, tam, cor)
    if k not in _icc:
        ic = Image.open(ICON + nome + ".png").convert("RGBA").resize((tam, tam), Image.LANCZOS)
        sol = Image.new("RGBA", ic.size, cor + (255,)); sol.putalpha(ic.getchannel("A")); _icc[k] = sol
    ic = _icc[k]
    if alpha < 1: ic = ic.copy(); ic.putalpha(ic.getchannel("A").point(lambda v: int(v * alpha)))
    img.alpha_composite(ic, (int(cx - tam / 2), int(cy - tam / 2)))

def alerta_saida(img, t, t0, tv, t1, alerta="Cliente com dúvida", saida="Você responde na hora"):
    """Caixa ALERTA (coral) do Mapa vira caixa SAÍDA (teal) quando ela diz "nunca mais tenha dúvida"."""
    if not (t0 <= t < t1 + 0.3): return
    a = ease((t - t0) / 0.25) * (1 - ease((t - t1) / 0.3))
    q = ease((t - tv) / 0.35) if t >= tv else 0
    cor = tuple(int(CORAL[i] + (TEAL[i] - CORAL[i]) * q) for i in range(3))
    tag1, tag2 = "ALERTA", "SAÍDA"; tam = 48
    w1 = 60 + 70 + tl(alerta, 700, tam) + 50; w2 = 60 + 70 + tl(saida, 700, tam) + 50; w = w1 + (w2 - w1) * q
    h = 150; x0 = W / 2 - w / 2; y0 = FAIXA_Y - h + int((1 - mola((t - t0) / 0.5)) * 30)
    caixa(img, x0, y0, x0 + w, y0 + h, 30, BRANCO, a * 0.97)
    caixa(img, x0, y0, x0 + 18, y0 + h, 0, cor, a, sombra=False)
    tg = tag1 if q < 0.5 else tag2; tw = tl(tg, 800, 26)
    caixa(img, x0 + 50, y0 + 18, x0 + 50 + tw + 30, y0 + 56, 19, cor, a, sombra=False)
    texto(img, (x0 + 65, y0 + 37), tg, 800, 26, BRANCO, a, anchor="lm")
    cy = y0 + 104; ic = "alert-triangle" if q < 0.5 else "check"
    disco(img, x0 + 80, cy, 26, cor, a, sombra=False); icone(img, ic, x0 + 80, cy, 30, a)
    if q < 1: texto(img, (x0 + 124, cy), alerta, 700, tam, NAVY, a * (1 - q), anchor="lm")
    if q > 0:
        texto(img, (x0 + 124, cy), saida, 700, tam, NAVY, a * q, anchor="lm")
        particulas(img, x0 + 80, cy, t - tv, n=10, raio=110, seed=677)

def rota(img, t, t_in, t_out, itens, titulo=None):
    """Rota: linha tracejada que vai se desenhando com um pino caindo em cada forma de aquisição."""
    if not (t_in <= t < t_out + 0.3): return
    a = ease((t - t_in) / 0.3) * (1 - ease((t - t_out) / 0.3))
    n = len(itens); cw = 172; w = n * cw + 30; h = 210 + (60 if titulo else 0)
    x0 = W / 2 - w / 2; y0 = FAIXA_Y - h + int((1 - mola((t - t_in) / 0.5)) * 30)
    caixa(img, x0, y0, x0 + w, y0 + h, 34, BRANCO, a * 0.96)
    if titulo: texto(img, (W / 2, y0 + 40), titulo, 800, 38, NAVY, a, anchor="mm")
    ty = y0 + (60 if titulo else 0); cy = ty + 120
    xs = [x0 + 15 + cw * k + cw / 2 for k in range(n)]
    p = ease((t - t_in) / max(0.3, itens[-1][0] - t_in + 0.3)); xe = xs[0] - 40 + (xs[-1] + 40 - (xs[0] - 40)) * p
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); xx = xs[0] - 40
    while xx < xe: d.line((xx, cy, min(xx + 22, xe), cy), fill=NAVY + (int(200 * a),), width=6); xx += 36
    img.alpha_composite(lay)
    for k, (tk, ic, rot) in enumerate(itens):
        if t < tk: continue
        q = (t - tk) / 0.45; dy = int((1 - mola(q)) * -70)
        _ic_cor(img, "map-pin-filled", xs[k], cy - 42 + dy, 76, CORES[k], a * ease(q * 3))
        disco(img, xs[k], cy - 52 + dy, 15, BRANCO, a * ease(q * 3), sombra=False)
        texto(img, (xs[k], cy + 56), rot, 700, 28, NAVY, a * ease(q * 3), anchor="mm")
        particulas(img, xs[k], cy - 40, t - tk, n=8, raio=80, seed=690 + k)
