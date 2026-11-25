#!/usr/bin/env python3
"""Só motion (ex-EST10) v1 (25/11) — ESTRUTURA A: sem voz nenhuma. Trilha original sintetizada (trilha.py, 100 BPM,
cortes no compasso de 2,4 s) + efeitos sonoros + texto animado + páginas reais do Mapa (PDF em alta).
Gancho chama o corretor e traz a dor ("o cliente perguntou e você travou?"), perguntas do cliente chegando como
notificação, virada "Nunca mais trave.", revelação da capa, 4 páginas com marca-texto, fechamento e CTA com toque.
Conjunto 5 de elementos: pílulas de manchete, notificações, palavra-por-batida, carrossel de páginas com marca-texto."""
import sys, os, subprocess
from v3 import *
from elem import tl
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/corretores/out/Corretores - So motion.mp4"
C4 = TRAB + "cortes4/"; PGS = "/home/claude/corretores/paginas/"; V = "/home/claude/corretores/voz/"
BG = V + "bg_papel.mp4"
if not os.path.exists(BG):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=0xF1F4F8:s=1080x1920:r=30:d=20", "-c:v", "libx264", "-pix_fmt", "yuv420p", BG], check=True)
BAR = 2.4
T_PERG, T_VIRA, T_CAPA, T_PAG, T_FECHA, T_CTA, FIM = 2.4, 7.2, 9.6, 12.0, 21.6, 24.0, 28.8
ESCURO = "eq=brightness=-0.06:saturation=0.9"
SEGS = [Seg(C4 + "sc_duv_corretor2.mp4", 0.6, T_PERG, ESCURO, audio=False, zoom=1.05),
        Seg(C4 + "sc_casal_duvida.mp4", 0.5, T_VIRA - T_PERG, ESCURO, audio=False, zoom=1.04),
        Seg(C4 + "sc_duvida.mp4", 0.3, T_CAPA - T_VIRA, "boxblur=18:2,eq=brightness=-0.22:saturation=0.7", audio=False, zoom=1.05),
        Seg(BG, 0.0, T_FECHA - T_CAPA, audio=False),
        Seg(C4 + "sc_feliz.mp4", 0.0, T_CTA - T_FECHA, ESCURO, audio=False, zoom=1.04),
        Seg(BG, 0.0, FIM - T_CTA, audio=False)]
AUD = [Seg(V + "trilha_motion.wav", 0.0, FIM, ganho=-1.5, fade_out=0.6)]
VERDE_CLARO = (120, 222, 200)

_pg = {}
def pagina(n, larg):
    k = (n, larg)
    if k not in _pg:
        f = [x for x in os.listdir(PGS) if x.startswith(f"p{n}-")][0]
        im = Image.open(PGS + f).convert("RGB"); h = int(im.height * larg / im.width); im = im.resize((larg, h), Image.LANCZOS)
        lay = Image.new("RGBA", (larg + 80, h + 80), (0, 0, 0, 0))
        sh = Image.new("RGBA", lay.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((40, 54, 40 + larg, 54 + h), 18, fill=(10, 30, 60, 110))
        lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
        m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, larg, h), 18, fill=255)
        lay.paste(im, (40, 40), m); _pg[k] = lay
    return _pg[k]
def colar(img, lay, cx, cy, esc=1.0, ang=0.0, alpha=1.0):
    if alpha <= 0.01 or esc <= 0.02: return
    if esc != 1.0: lay = lay.resize((max(1, int(lay.width * esc)), max(1, int(lay.height * esc))), Image.BILINEAR)
    if ang: lay = lay.rotate(ang, resample=Image.BICUBIC, expand=True)
    if alpha < 1: lay = lay.copy(); lay.putalpha(lay.getchannel("A").point(lambda v: int(v * alpha)))
    img.alpha_composite(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)))

def pilula(img, cx, cy, s, tam, fundo, cor, a, dx=0, ic=None, cor_ic=None):
    tw = tl(s, 800, tam); pad = 46; icw = (tam + 30) if ic else 0; w = tw + 2 * pad + icw; h = int(tam * 1.9)
    x0 = cx - w / 2 + dx; caixa(img, x0, cy - h / 2, x0 + w, cy + h / 2, h / 2, fundo, a)
    if ic:
        disco(img, x0 + pad + tam / 2 - 4, cy, tam * 0.62, cor_ic or TEAL, a, sombra=False); icone(img, ic, x0 + pad + tam / 2 - 4, cy, int(tam * 0.8), a)
    texto(img, (x0 + pad + icw, cy + 2), s, 800, tam, cor, a, anchor="lm")

# ---------- 1. gancho ----------
GANCHO = [(0.15, "Corretor,", NAVY, BRANCO), (0.6, "o cliente perguntou…", BRANCO, NAVY), (1.15, "e você travou?", CORAL, BRANCO)]
def gancho(img, t):
    if t >= T_PERG: return
    for k, (tk, s, fundo, cor) in enumerate(GANCHO):
        if t < tk: continue
        q = (t - tk) / 0.4; a = ease(q * 2.5) * (1 - ease((t - (T_PERG - 0.15)) / 0.15))
        dx = int((1 - mola(q)) * (-260 if k % 2 == 0 else 260))
        sh = 0
        if k == 2 and 0 < t - tk < 0.35: sh = int(10 * math.sin((t - tk) * 70) * (1 - (t - tk) / 0.35))   # tremidinha no "travou"
        pilula(img, W / 2 + sh, 1220 + k * 165, s, 70 if k else 84, fundo, cor, a, dx)

# ---------- 2. perguntas como notificação ----------
PERG = [(2.6, "Dá pra usar o FGTS?"), (3.55, "Quanto vou dar de entrada?"), (4.5, "Consórcio serve pra isso?"), (5.45, "Quem paga o ITBI?")]
def notificacoes(img, t):
    if not (T_PERG <= t < T_VIRA): return
    a_out = 1 - ease((t - (T_VIRA - 0.2)) / 0.2)
    vis = [k for k, (tk, _) in enumerate(PERG) if t >= tk]
    nh, gap, x0, x1 = 178, 22, 50, 1030
    for k in vis:
        tk, s = PERG[k]; q = ease((t - tk) / 0.35)
        # a mais nova fica em cima; as anteriores descem
        pos = 0
        for j in vis:
            if j > k: pos += ease((t - PERG[j][0]) / 0.35)
        y0 = 150 + pos * (nh + gap) - (1 - q) * 200
        al = a_out * q * (1 - 0.15 * min(pos, 3) / 3)
        caixa(img, x0, y0, x1, y0 + nh, 38, (250, 251, 253), al)
        disco(img, x0 + 76, y0 + nh / 2, 44, TEAL, al, sombra=False); icone(img, "message-question", x0 + 76, y0 + nh / 2, 52, al)
        texto(img, (x0 + 145, y0 + 54), "Cliente", 800, 36, NAVY, al, anchor="lm")
        texto(img, (x1 - 40, y0 + 54), "agora", 600, 30, (140, 152, 170), al, anchor="rm")
        texto(img, (x0 + 145, y0 + 118), s, 700, 48, (40, 52, 70), al, anchor="lm")

# ---------- 3. virada ----------
VIRA = [(7.25, "Nunca"), (7.85, "mais"), (8.45, "trave.")]
def virada(img, t):
    if not (T_VIRA <= t < T_CAPA): return
    a_out = 1 - ease((t - (T_CAPA - 0.12)) / 0.12)
    for k, (tk, s) in enumerate(VIRA):
        if t < tk: continue
        q = (t - tk) / 0.35; esc = 1.5 - 0.5 * mola(q); al = a_out * ease(q * 3)
        cor = BRANCO if k < 2 else VERDE_CLARO
        f = fonte(800, int(150 * esc)); lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(lay).text((W / 2, 720 + k * 190), s, font=f, fill=cor + (int(255 * al),), anchor="mm"); img.alpha_composite(lay)
    if t >= 9.0:
        u = ease((t - 9.0) / 0.3); tw = tl("trave.", 800, 150)
        caixa(img, W / 2 - tw / 2, 1180, W / 2 - tw / 2 + tw * u, 1196, 8, TEAL, a_out, sombra=False)

# ---------- 4. capa ----------
def capa(img, t):
    if not (T_CAPA <= t < T_PAG + 0.4): return
    q = (t - T_CAPA) / 0.6; out = ease((t - T_PAG) / 0.35)
    colar(img, pagina(1, 720), W / 2 - out * 900, 880, esc=0.55 + 0.45 * mola(q), ang=-9 * (1 - ease(q)) + out * 12, alpha=ease(q * 3))
    if t >= 10.5 and t < T_PAG:
        p = (t - 10.5) / 0.4; pilula(img, W / 2, 1620, "Tudo do fechamento, num lugar só", 40, NAVY, BRANCO, ease(p * 3) * (1 - ease((t - (T_PAG - 0.15)) / 0.15)), int((1 - mola(p)) * 200), ic="stack-2")
    if T_CAPA <= t < T_CAPA + 0.6: particulas(img, W / 2, 880, t - T_CAPA, n=16, raio=520, seed=901)

# ---------- 5. páginas com marca-texto ----------
PAGS = [(12.0, 53, "pig-money", "Quando o FGTS pode entrar"), (14.4, 66, "users-group", "Consórcio × financiamento"),
        (16.8, 40, "home", "Quanto o cliente pode comprar"), (19.2, 97, "receipt", "ITBI e registro: quem paga")]
def paginas(img, t):
    if not (T_PAG <= t < T_FECHA): return
    for k, (tk, n, ic, cap) in enumerate(PAGS):
        fim = PAGS[k + 1][0] if k + 1 < len(PAGS) else T_FECHA
        if not (tk - 0.01 <= t < fim + 0.35): continue
        qi = ease((t - tk) / 0.38); qo = ease((t - fim) / 0.35) if t >= fim else 0
        cx = W / 2 + (1 - qi) * 1000 - qo * 1000; ang = (1 - qi) * -10 + qo * 10
        lay = pagina(n, 800)
        colar(img, lay, cx, 1060, ang=ang, alpha=1.0)
        # marca-texto passando no título da página
        if t >= tk + 0.55 and qo == 0:
            u = ease((t - (tk + 0.55)) / 0.45); pw, ph = 800, lay.height - 80
            x0 = W / 2 - pw / 2 + 40; y0 = 1060 - ph / 2 + ph * 0.045
            hl = Image.new("RGBA", img.size, (0, 0, 0, 0))
            ImageDraw.Draw(hl).rounded_rectangle((x0, y0, x0 + (pw - 80) * u, y0 + ph * 0.115), 14, fill=(255, 214, 10, 70))
            img.alpha_composite(hl)
        a = ease((t - tk) / 0.3) * (1 - ease((t - (fim - 0.15)) / 0.15))
        pilula(img, W / 2, 300, cap, 46, BRANCO, NAVY, a, int((1 - mola((t - tk) / 0.45)) * 160), ic=ic, cor_ic=[TEAL, CORAL, NAVY, TEAL][k])
        texto(img, (W / 2, 205), f"{k + 1} de +120 mapas", 700, 30, (110, 124, 145), a, anchor="mm")

# ---------- 6. fechamento ----------
def fechamento(img, t):
    if not (T_FECHA <= t < T_CTA): return
    for k, (tk, s, fundo, cor, ic) in enumerate([(21.75, "Responda na hora.", BRANCO, NAVY, "check"), (22.35, "Feche com segurança.", TEAL, BRANCO, "shield-check")]):
        if t < tk: continue
        q = (t - tk) / 0.4; a = ease(q * 2.5) * (1 - ease((t - (T_CTA - 0.15)) / 0.15))
        pilula(img, W / 2, 1300 + k * 150, s, 64, fundo, cor, a, int((1 - mola(q)) * (-240 if k == 0 else 240)), ic=ic, cor_ic=TEAL if k == 0 else NAVY)

# ---------- 7. CTA ----------
def cta_final(img, t):
    if t < T_CTA: return
    q = (t - T_CTA) / 0.5
    texto(img, (W / 2, 250), "Mapa Visual Completo", 800, 64, NAVY, ease(q * 3), anchor="mm")
    texto(img, (W / 2, 330), "do Fechamento Imobiliário", 800, 52, TEAL, ease(q * 3), anchor="mm")
    colar(img, pagina(1, 560), W / 2, 900, esc=0.7 + 0.3 * mola(q), ang=-4 * (1 - ease(q)) + 3, alpha=ease(q * 3))
    tt = T_CTA + 1.2; p = (t - (T_CTA + 0.45)) / 0.45
    if p <= 0: return
    s = 1.0 - 0.06 * math.sin(min(1, max(0, (t - tt) / 0.18)) * math.pi)
    w, h = 560 * s, 128 * s; cx, cy = W / 2, 1520 + int((1 - mola(p)) * 60)
    caixa(img, cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, h / 2, TEAL, ease(p * 3))
    texto(img, (cx - 30, cy), "Saiba mais", 800, int(60 * s), BRANCO, ease(p * 3), anchor="mm")
    icone(img, "arrow-right", cx + 175 * s, cy, int(54 * s), ease(p * 3))
    texto(img, (W / 2, 1385), "Toque no botão e conheça o Mapa", 700, 40, (90, 104, 125), ease((t - (T_CTA + 0.8)) / 0.4), anchor="mm")
    if t >= tt - 0.35:
        qq = ease((t - (tt - 0.35)) / 0.35)
        hx = cx + 230 + int((1 - qq) * 120); hy = cy + 70 + int((1 - qq) * 120)
        ds = 1.0 - 0.12 * math.sin(min(1, max(0, (t - tt) / 0.18)) * math.pi)
        lay = Image.open(ICON + "dedo.png").convert("RGBA"); sz = int(130 * ds); lay = lay.resize((sz, sz), Image.LANCZOS)
        img.alpha_composite(lay, (int(hx - sz * 0.42), int(hy - sz * 0.18)))
    if tt <= t < tt + 0.6:
        r = int(70 + 300 * ease((t - tt) / 0.6)); al = int(160 * (1 - (t - tt) / 0.6))
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).ellipse((cx - r, cy - r * 0.45, cx + r, cy + r * 0.45), outline=TEAL + (al,), width=6)
        img.alpha_composite(lay); particulas(img, cx, cy, t - tt, seed=931, raio=280, n=14)

def fundo_papel(img, t):
    """manchas suaves verde-água/coral no fundo claro (só nas partes de papel)."""
    if not ((T_CAPA <= t < T_FECHA) or t >= T_CTA): return
    if not hasattr(fundo_papel, "lay"):
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.ellipse((-260, 1300, 520, 2080), fill=TEAL + (40,)); d.ellipse((620, -200, 1360, 540), fill=CORAL + (30,)); d.ellipse((700, 1500, 1200, 2000), fill=NAVY + (22,))
        fundo_papel.lay = lay.filter(ImageFilter.GaussianBlur(90))
    img.alpha_composite(fundo_papel.lay)

OVS = [fundo_papel, gancho, notificacoes, virada, capa, paginas, fechamento, cta_final]
def cam(t):
    if t < T_PERG: return 1.0 + 0.05 * t / T_PERG
    if t < T_VIRA: return 1.0 + 0.04 * (t - T_PERG) / (T_VIRA - T_PERG)
    if T_FECHA <= t < T_CTA: return 1.0 + 0.04 * (t - T_FECHA) / (T_CTA - T_FECHA)
    return 1.0
SFX = [(tk, "pop", -14) for tk, *_ in GANCHO] + [(tk, "pop", -12) for tk, _ in PERG] + [(tk, "pop", -13) for tk, _ in VIRA] + \
      [(T_PERG - 0.12, "whoosh", -14), (T_VIRA - 0.12, "whoosh", -14)] + [(tk - 0.1, "whoosh", -15) for tk, *_ in PAGS[1:]] + \
      [(T_PAG - 0.1, "whoosh", -15), (10.5, "pop", -16), (21.6 - 0.12, "whoosh", -14), (21.75, "pop", -14), (22.35, "pop", -14),
       (T_CTA - 0.12, "whoosh", -14), (T_CTA + 0.45, "pop", -15), (T_CTA + 1.2, "pop", -12)]
if __name__ == "__main__":
    d = render(SEGS, OVS, [T_PERG, T_VIRA, T_CAPA, T_FECHA, T_CTA], SFX, OUT, audio_segs=AUD, cam=cam)
    print("ok", OUT, round(d, 2))
