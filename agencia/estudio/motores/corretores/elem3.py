"""Conjunto 3 de elementos (25/11) — terceiro estilo, pra não repetir o do EST2-A (faixa) nem o da historinha (elem2).
Estilos: número grande com contorno ("+120" carimbado), checklist em 2 colunas que vai ticando, palavras com marca-texto
varrendo, chave liga/desliga "Na dúvida → Seguro", pílulas navy que deslizam dos lados. Mesmas regras de posição e cor."""
from v3 import *
from elem import tl, FAIXA_Y

def _texto_contorno(img, xy, s, peso, tam, cor, borda, larg, alpha=1.0, anchor="mm", esc=1.0, ang=0.0):
    f = fonte(peso, int(tam * esc)); d0 = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    bb = d0.textbbox((0, 0), s, font=f, stroke_width=larg); w, h = bb[2] - bb[0] + 40, bb[3] - bb[1] + 40
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((w / 2, h / 2), s, font=f, fill=cor + (255,), stroke_width=larg, stroke_fill=borda + (255,), anchor="mm")
    if ang: lay = lay.rotate(ang, resample=Image.BICUBIC, expand=True)
    if alpha < 1: lay.putalpha(lay.getchannel("A").point(lambda v: int(v * alpha)))
    img.alpha_composite(lay, (int(xy[0] - lay.width / 2), int(xy[1] - lay.height / 2)))

def carimbo(img, t, t0, t1, alvo=120, rotulo="mapas visuais"):
    """'+120' enorme, branco com contorno navy, entra girando de leve e assenta; rótulo numa pílula teal."""
    if not (t0 <= t < t1 + 0.3): return
    a = ease((t - t0) / 0.2) * (1 - ease((t - t1) / 0.3)); q = (t - t0) / 0.5
    n = int(alvo * ease((t - t0) / 0.9)); esc = 1.6 - 0.6 * mola(q); ang = -8 * (1 - ease(q)) + 3
    cy = FAIXA_Y - 170
    _texto_contorno(img, (W / 2, cy), f"+{n}", 800, 150, BRANCO, NAVY, 12, a, esc=esc, ang=ang)
    tw = tl(rotulo, 700, 36); pw, ph = tw + 64, 66; py = FAIXA_Y - 82
    p2 = ease((t - t0 - 0.3) / 0.3)
    caixa(img, W / 2 - pw / 2 * p2, py, W / 2 + pw / 2 * p2, py + ph, ph / 2, TEAL, a)
    if p2 > 0.7: texto(img, (W / 2, py + ph / 2), rotulo, 700, 36, BRANCO, a * (p2 - 0.7) / 0.3, anchor="mm")
    if t >= t0 + 0.9: particulas(img, W / 2, cy, t - (t0 + 0.9), n=14, raio=230, seed=501)

def checklist(img, t, t_in, t_out, itens, titulo="Tudo isso no Mapa", tam=36):
    """Cartão branco com título e 2 colunas; cada tema entra com um check que se desenha quando ela fala."""
    if not (t_in <= t < t_out + 0.3): return
    a = ease((t - t_in) / 0.3) * (1 - ease((t - t_out) / 0.3))
    n = len(itens); linhas = (n + 1) // 2; lh = 68; colw = 340
    w = 2 * colw + 80; h = 86 + linhas * lh + 26
    x0 = W / 2 - w / 2; y0 = FAIXA_Y - h + int((1 - mola((t - t_in) / 0.5)) * 30)
    caixa(img, x0, y0, x0 + w, y0 + h, 34, BRANCO, a * 0.96)
    caixa(img, x0, y0, x0 + w, y0 + 70, 34, NAVY, a, sombra=False); caixa(img, x0, y0 + 36, x0 + w, y0 + 70, 0, NAVY, a, sombra=False)
    texto(img, (W / 2, y0 + 36), titulo, 700, 34, BRANCO, a, anchor="mm")
    for k, (tk, ic, rot) in enumerate(itens):
        col, lin = k // linhas, k % linhas
        cx = x0 + 40 + col * colw + 30; cy = y0 + 86 + lin * lh + lh / 2
        on = t >= tk; q = (t - tk) / 0.35 if on else 0
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.ellipse((cx - 22, cy - 22, cx + 22, cy + 22), outline=(205, 214, 226, int(255 * a)), width=4)
        img.alpha_composite(lay)
        if on:
            disco(img, cx, cy, int(24 * mola(q)), TEAL, a, sombra=False)
            if q > 0.4: icone(img, "check", cx, cy, 30, a * min(1, (q - 0.4) / 0.4))
            particulas(img, cx, cy, t - tk, n=6, raio=60, seed=520 + k)
        texto(img, (cx + 40, cy), rot, 700, tam, NAVY if on else (170, 182, 198), a, anchor="lm")

def marcatexto(img, t, itens, t_out, tam=58):
    """As três palavras numa linha; um marca-texto teal varre atrás de cada uma quando ela fala."""
    t_in = itens[0][0] - 0.3
    if not (t_in <= t < t_out + 0.3): return
    a = ease((t - t_in) / 0.3) * (1 - ease((t - t_out) / 0.3))
    pal = [s for _, _, s in itens]; gap = 52
    ws = [tl(s, 800, tam) for s in pal]; tot = sum(ws) + gap * (len(pal) - 1)
    w = tot + 100; h = 140; x0 = W / 2 - w / 2; y0 = FAIXA_Y - h + int((1 - mola((t - t_in) / 0.5)) * 30)
    caixa(img, x0, y0, x0 + w, y0 + h, 30, BRANCO, a * 0.96)
    x = x0 + 50; cy = y0 + h / 2
    for (tk, _, s), wd in zip(itens, ws):
        q = ease((t - tk) / 0.35) if t >= tk else 0
        if q > 0: caixa(img, x - 14, cy - 40, x - 14 + (wd + 28) * q, cy + 42, 14, TEAL, a, sombra=False)
        cor = BRANCO if q > 0.55 else NAVY
        texto(img, (x, cy + 2), s, 800, tam, cor, a, anchor="lm")
        x += wd + gap

def chave(img, t, t0, tv, t1, de="Na dúvida", para="Seguro"):
    """Chave liga/desliga: bolinha sai do coral ('Na dúvida') e vai pro teal ('Seguro') em tv."""
    if not (t0 <= t < t1 + 0.3): return
    a = ease((t - t0) / 0.25) * (1 - ease((t - t1) / 0.3))
    tam = 54; wl = max(tl(de, 800, tam), tl(para, 800, tam))
    sw, sh = 170, 94; w = 50 + sw + 36 + wl + 50; h = 150
    x0 = W / 2 - w / 2; y0 = FAIXA_Y - h + int((1 - mola((t - t0) / 0.5)) * 30)
    caixa(img, x0, y0, x0 + w, y0 + h, 36, BRANCO, a * 0.96)
    q = ease((t - tv) / 0.35) if t >= tv else 0
    cor = tuple(int(CORAL[i] + (TEAL[i] - CORAL[i]) * q) for i in range(3))
    sx0, sy0 = x0 + 50, y0 + (h - sh) / 2
    caixa(img, sx0, sy0, sx0 + sw, sy0 + sh, sh / 2, cor, a, sombra=False)
    kx = sx0 + sh / 2 + (sw - sh) * q
    disco(img, kx, sy0 + sh / 2, sh / 2 - 8, BRANCO, a)
    tx = sx0 + sw + 36; cy = y0 + h / 2
    texto(img, (tx, cy - int(q * 40)), de, 800, tam, CORAL, a * (1 - q), anchor="lm")
    if q > 0:
        texto(img, (tx, cy + int((1 - q) * 40)), para, 800, tam, TEAL, a * q, anchor="lm")
        particulas(img, kx, sy0 + sh / 2, t - tv, n=10, raio=120, seed=577)

def deslizantes(img, t, t_in, t_out, itens, titulo=None, tam=42):
    """Pílulas navy (ícone em disco teal + texto branco) que entram deslizando, alternando esquerda/direita, em 2 linhas."""
    if not (t_in <= t < t_out + 0.3): return
    a = ease((t - t_in) / 0.3) * (1 - ease((t - t_out) / 0.3))
    h = 92; r = 34; gap = 16
    larg = [10 + 2 * r + 16 + tl(s, 700, tam) + 30 for _, _, s in itens]
    corte = (len(itens) + 1) // 2; linhas = [list(range(corte)), list(range(corte, len(itens)))]
    for li, lin in enumerate(linhas):
        cy = FAIXA_Y - 10 - (1 - li) * (h + gap) - h / 2
        tot = sum(larg[i] for i in lin) + gap * (len(lin) - 1); x = W / 2 - tot / 2
        for i in lin:
            tk, ic, s = itens[i]; wd = larg[i]
            if t >= tk:
                q = ease((t - tk) / 0.4); lado = -1 if i % 2 == 0 else 1
                dx = lado * (1 - q) * 260
                caixa(img, x + dx, cy - h / 2, x + dx + wd, cy + h / 2, h / 2, NAVY, a * q)
                cx = x + dx + 10 + r; disco(img, cx, cy, r, TEAL, a * q, sombra=False); icone(img, ic, cx, cy, int(r * 1.2), a * q)
                texto(img, (cx + r + 16, cy), s, 700, tam, BRANCO, a * q, anchor="lm")
            x += wd + gap
    if titulo:
        ty = FAIXA_Y - 10 - 2 * (h + gap) - 30; tw = tl(titulo, 700, 36)
        caixa(img, W / 2 - tw / 2 - 36, ty - 33, W / 2 + tw / 2 + 36, ty + 33, 33, BRANCO, a)
        texto(img, (W / 2, ty), titulo, 700, 36, NAVY, a, anchor="mm")
