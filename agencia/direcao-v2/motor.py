#!/usr/bin/env python3
"""Motor de vídeo v2 — MinhaMoto.

Renderiza frame a frame no Chrome (Playwright) a partir de uma timeline em Python
e codifica com ffmpeg. Camadas: fundo (tela do app em tela cheia, foto com Ken Burns,
gradiente de marca), celular premium com a gravação real rodando dentro, textos
(legenda palavra-por-palavra, títulos, selo, CTA final).

Uso: from motor import Video; v=Video('A1', estilo='A'); v.add(...); v.render(saida)
"""
import os, json, math, subprocess, shutil, hashlib, html as H

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(AQUI, '..', '..'))
ASSETS = os.path.join(REPO, 'agencia', 'designer', 'assets')
FONTES = os.path.join(AQUI, 'fontes')
MATERIAL = os.path.join(REPO, 'agencia', 'referencias', 'material')
CACHE = '/tmp/v2cache'
W, Hh, FPS = 1080, 1920, 30
STATUS_H = 120          # barra de status gravada (com ponto vermelho) — sempre escondida/substituída

def ease(x):            # easeInOutCubic
    x = max(0.0, min(1.0, x))
    return 4*x*x*x if x < .5 else 1 - pow(-2*x + 2, 3)/2

def eout(x):            # easeOutCubic
    x = max(0.0, min(1.0, x)); return 1 - pow(1 - x, 3)

def eback(x):           # easeOutBack (pop)
    x = max(0.0, min(1.0, x)); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3*pow(x - 1, 3) + c1*pow(x - 1, 2)

def lerp(a, b, x): return a + (b - a)*x

def extrair(src, ss, dur, speed=1.0):
    """Extrai frames da gravação (30fps já acelerados) e devolve lista de caminhos."""
    key = hashlib.md5(f'{src}{ss}{dur}{speed}'.encode()).hexdigest()[:10]
    d = os.path.join(CACHE, key)
    if not os.path.isdir(d) or not os.listdir(d):
        os.makedirs(d, exist_ok=True)
        p = src if os.path.isabs(src) else os.path.join(MATERIAL, src)
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', str(ss), '-t', str(dur*speed), '-i', p,
                        '-vf', f'setpts=PTS/{speed},fps={FPS}', '-q:v', '2', os.path.join(d, '%05d.jpg')], check=True)
    fs = sorted(os.path.join(d, f) for f in os.listdir(d))
    return fs

def still(src, t):
    key = hashlib.md5(f'{src}{t}'.encode()).hexdigest()[:10]
    out = os.path.join(CACHE, f'still_{key}.png')
    if not os.path.exists(out):
        os.makedirs(CACHE, exist_ok=True)
        p = src if os.path.isabs(src) else os.path.join(MATERIAL, src)
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', str(t), '-i', p, '-frames:v', '1', out], check=True)
    return out

ESTILOS = {
  # A — Nativo/Rua: legenda grossa estilo TikTok, tela cheia, foto em movimento
  'A': dict(fonte='m900', titulo='m900', apoio='m800', destaque='#FFD400', branco='#FFFFFF',
            bg='radial-gradient(120% 80% at 50% 0%, #1a5cff 0%, #0b2a8a 45%, #050c24 100%)'),
  # B — Premium produto: Anton condensada, azul elétrico, celular 3D em fundo navy
  'B': dict(fonte='anton', titulo='anton', apoio='pop600', destaque='#3D8BFF', branco='#F4F7FC',
            bg='radial-gradient(90% 60% at 50% 38%, #12306b 0%, #08142e 55%, #03060f 100%)'),
}

CSS_FONTES = f"""
@font-face{{font-family:m900;src:url('file://{FONTES}/montserrat-latin-900-normal.woff2')}}
@font-face{{font-family:m800;src:url('file://{FONTES}/montserrat-latin-800-normal.woff2')}}
@font-face{{font-family:m600;src:url('file://{FONTES}/montserrat-latin-600-normal.woff2')}}
@font-face{{font-family:anton;src:url('file://{FONTES}/anton-latin-400-normal.woff2')}}
@font-face{{font-family:pop600;src:url('file://{FONTES}/poppins-latin-600-normal.woff2')}}
@font-face{{font-family:pop800;src:url('file://{FONTES}/poppins-latin-800-normal.woff2')}}
"""

PAGINA = """<!doctype html><html><head><meta charset=utf-8><style>
%(fontes)s
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#000}
#bg{position:absolute;inset:0;overflow:hidden}
#bg .grad{position:absolute;inset:0}
#bg img.full{position:absolute;left:0;top:0;width:1080px;transform-origin:50%% 50%%}
#bg img.foto{position:absolute;left:50%%;top:50%%;transform-origin:50%% 50%%}
#vignette{position:absolute;inset:0;pointer-events:none}
#luz{position:absolute;inset:-200px;pointer-events:none;mix-blend-mode:screen}
#phonewrap{position:absolute;left:50%%;top:50%%;width:0;height:0;perspective:2400px}
#phone{position:absolute;transform-style:preserve-3d}
.frame{position:absolute;inset:0;border-radius:118px;background:linear-gradient(145deg,#4a4f58,#1b1d22 30%%,#2c3038 60%%,#0d0e11);
  box-shadow:0 0 0 2px #5d636d inset, 0 0 0 9px #0a0b0d inset}
.btn{position:absolute;background:linear-gradient(90deg,#2a2d33,#4a4f58);border-radius:4px}
.screen{position:absolute;left:22px;top:22px;right:22px;bottom:22px;border-radius:98px;overflow:hidden;background:#07090d}
.screen img{position:absolute;left:0;top:0;width:100%%;transform-origin:50%% 0}
.sbar{position:absolute;left:0;right:0;top:0;height:6.2%%;background:linear-gradient(#07090d 70%%,rgba(7,9,13,0))}
.sbar .h{position:absolute;left:13%%;top:30%%;font:600 38px/1 -apple-system,'SF Pro',pop600,sans-serif;color:#fff;letter-spacing:.5px}
.sbar .r{position:absolute;right:10%%;top:32%%;display:flex;gap:12px;align-items:center}
.island{position:absolute;left:50%%;top:2.2%%;width:30%%;height:3.1%%;transform:translateX(-50%%);background:#000;border-radius:40px}
.glare{position:absolute;inset:0;border-radius:98px;background:linear-gradient(115deg,rgba(255,255,255,.13) 0%%,rgba(255,255,255,0) 28%%,rgba(255,255,255,0) 70%%,rgba(255,255,255,.05) 100%%);pointer-events:none}
.ring{position:absolute;border-radius:28px;border:5px solid #3D8BFF;box-shadow:0 0 0 6px rgba(61,139,255,.25),0 0 60px rgba(61,139,255,.6)}
.tap{position:absolute;width:120px;height:120px;border-radius:50%%;border:6px solid rgba(255,255,255,.9);background:rgba(255,255,255,.18)}
#txt{position:absolute;inset:0}
.t{position:absolute;text-align:center;left:70px;right:70px}
.cap{font-family:%(fonte)s;text-transform:uppercase;color:#fff;-webkit-text-stroke:10px #000;paint-order:stroke fill;
  text-shadow:0 10px 0 rgba(0,0,0,.6),0 0 60px rgba(0,0,0,.7);line-height:1.04;letter-spacing:.5px}
.cap .w{display:inline-block;margin:0 .14em;transform-origin:50%% 70%%}
.cap .hl{color:%(destaque)s}
.tit{font-family:%(titulo)s;text-transform:uppercase;color:%(branco)s;line-height:1.0;letter-spacing:1px}
.tit .hl{color:%(destaque)s}
.apo{font-family:%(apoio)s;color:#c9d6ea;line-height:1.3}
.badge{position:absolute;display:flex;align-items:center;gap:18px;padding:16px 28px 16px 18px;border-radius:70px;
  background:linear-gradient(135deg,#2b6dff,#123fc4);box-shadow:0 14px 40px rgba(0,0,0,.45),0 0 0 3px rgba(255,255,255,.18) inset;
  font-family:m900;font-size:40px;color:#fff;letter-spacing:1px}
.badge img{width:70px;height:70px;border-radius:18px}
.cta{position:absolute;left:0;right:0;text-align:center}
.cta img.ic{width:260px;height:260px;border-radius:62px;box-shadow:0 30px 80px rgba(0,0,0,.55),0 0 120px rgba(61,139,255,.55)}
.cta .selos{margin-top:46px}
.cta .selos img{width:640px}
.preco{display:inline-block;margin-top:34px;padding:18px 46px;border-radius:24px;background:#FFD400;color:#0a0a0a;font-family:m900;font-size:64px;
  box-shadow:0 14px 0 #b38f00,0 26px 60px rgba(0,0,0,.45)}
</style></head><body>
<div id=bg></div><div id=luz></div><div id=vignette></div>
<div id=phonewrap><div id=phone></div></div>
<div id=txt></div>
<script>
const cacheImgs={};
async function setImg(el, src){ if(el.getAttribute('src')!==src){ el.setAttribute('src',src); try{await el.decode()}catch(e){} } }
window.R = async function(s){
  // fundo
  const bg=document.getElementById('bg');
  if(bg.dataset.k!==s.bgk){ bg.innerHTML=s.bghtml; bg.dataset.k=s.bgk; }
  for(const im of bg.querySelectorAll('img')){ if(s.bgsrc && im.dataset.v==='1') await setImg(im,s.bgsrc); if(s.bgtr) im.style.transform=s.bgtr; }
  if(s.bgfilter!==undefined){ for(const im of bg.querySelectorAll('img')) im.style.filter=s.bgfilter; }
  document.getElementById('vignette').style.background=s.vig||'none';
  document.getElementById('luz').style.background=s.luz||'none';
  // celular
  const ph=document.getElementById('phone');
  if(s.phone){
    if(ph.dataset.k!==s.phone.k){ ph.innerHTML=s.phone.html; ph.dataset.k=s.phone.k; }
    ph.style.display='block';
    ph.style.width=s.phone.w+'px'; ph.style.height=s.phone.h+'px';
    ph.style.left=(-s.phone.w/2)+'px'; ph.style.top=(-s.phone.h/2)+'px';
    ph.style.transform=s.phone.tr; ph.style.filter=s.phone.shadow;
    const im=ph.querySelector('.screen img'); await setImg(im,s.phone.src); im.style.transform=s.phone.scr||'none';
    const ring=ph.querySelector('.ring'); if(ring){ if(s.phone.ring){ring.style.display='block'; Object.assign(ring.style,s.phone.ring);} else ring.style.display='none'; }
    const tap=ph.querySelector('.tap'); if(tap){ if(s.phone.tap){tap.style.display='block'; Object.assign(tap.style,s.phone.tap);} else tap.style.display='none'; }
  } else { ph.style.display='none'; }
  document.getElementById('txt').innerHTML=s.txt||'';
  for(const im of document.querySelectorAll('#txt img')){ try{await im.decode()}catch(e){} }
  await document.fonts.ready;
  return 1;
}
</script></body></html>"""

def phone_html():
    return ("<div class=frame></div>"
            "<div class='btn' style='left:-7px;top:22%;width:9px;height:7%'></div>"
            "<div class='btn' style='left:-7px;top:31%;width:9px;height:7%'></div>"
            "<div class='btn' style='left:-7px;top:15%;width:9px;height:4%'></div>"
            "<div class='btn' style='right:-7px;top:25%;width:9px;height:11%'></div>"
            "<div class=screen><img><div class=ring style='display:none'></div><div class=tap style='display:none'></div>"
            "<div class=sbar><div class=h>9:41</div><div class=r>"
            "<svg width=52 height=32 viewBox='0 0 52 32'><rect x=0 y=20 width=9 height=12 rx=2 fill=#fff /><rect x=14 y=14 width=9 height=18 rx=2 fill=#fff /><rect x=28 y=7 width=9 height=25 rx=2 fill=#fff /><rect x=42 y=0 width=9 height=32 rx=2 fill=#fff /></svg>"
            "<svg width=46 height=34 viewBox='0 0 46 34'><path d='M23 32l7-8a10 10 0 0 0-14 0z' fill=#fff /><path d='M9 17a20 20 0 0 1 28 0l-4 4a14 14 0 0 0-20 0z' fill=#fff /><path d='M2 10a30 30 0 0 1 42 0l-4 4a24 24 0 0 0-34 0z' fill=#fff /></svg>"
            "<svg width=70 height=34 viewBox='0 0 70 34'><rect x=1 y=1 width=60 height=32 rx=9 fill=none stroke=#fff stroke-opacity=.5 stroke-width=2 /><rect x=5 y=5 width=46 height=24 rx=6 fill=#fff /><rect x=64 y=11 width=5 height=12 rx=2 fill=#fff fill-opacity=.5 /></svg>"
            "</div></div><div class=island></div><div class=glare></div></div>")

def caption_html(palavras, hl, n_vis, idade_ult, y, tam, estilo, centro=True, largura=940):
    """Legenda palavra-por-palavra. palavras visíveis = n_vis; a última faz 'pop'."""
    out = []
    for i, p in enumerate(palavras):
        if i >= n_vis: break
        cls = 'w hl' if i in hl else 'w'
        st = ''
        if i == n_vis - 1 and idade_ult is not None:
            k = eback(min(1, idade_ult/0.16)); sc = 0.55 + 0.45*k
            st = f"transform:scale({sc:.3f})"
        out.append(f"<span class='{cls}' style='{st}'>{H.escape(p)}</span>")
    left = (W - largura)//2
    return (f"<div class='t cap' style='left:{left}px;right:{left}px;top:{y}px;font-size:{tam}px'>{''.join(out)}</div>")

class Video:
    def __init__(self, vid, estilo='A', dur=None):
        self.id, self.est = vid, ESTILOS[estilo]; self.estilo = estilo
        self.cenas = []      # (t0, t1, fn(t_local, t_global) -> state parcial)
        self.textos = []     # (t0, t1, fn(t_local) -> html)

    def cena(self, t0, t1, fn): self.cenas.append((t0, t1, fn))
    def texto(self, t0, t1, fn): self.textos.append((t0, t1, fn))

    def duracao(self): return max([c[1] for c in self.cenas] + [t[1] for t in self.textos])

    def estado(self, t):
        s = {'bgk': '', 'bghtml': '', 'txt': ''}
        for t0, t1, fn in self.cenas:
            if t0 <= t < t1 or (t >= t1 and t1 == self.duracao() and t0 <= t):
                s.update(fn(t - t0, t))
        s['txt'] = ''.join(fn(t - t0) for t0, t1, fn in self.textos if t0 <= t < t1)
        return s

    def render(self, saida, so_frames=None):
        from playwright.sync_api import sync_playwright
        n = int(round(self.duracao()*FPS))
        fdir = os.path.join('/tmp/v2render', self.id); shutil.rmtree(fdir, ignore_errors=True); os.makedirs(fdir)
        pag = PAGINA % dict(fontes=CSS_FONTES, **self.est)
        hp = os.path.join(fdir, 'p.html'); open(hp, 'w').write(pag)
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--force-color-profile=srgb', '--allow-file-access-from-files'])
            pg = b.new_page(viewport={'width': W, 'height': Hh})
            pg.goto('file://' + hp); pg.wait_for_timeout(300)
            quadros = range(n) if so_frames is None else so_frames
            for i in quadros:
                t = i/FPS
                pg.evaluate('s=>window.R(s)', self.estado(t))
                pg.screenshot(path=os.path.join(fdir, f'{i:05d}.jpg'), type='jpeg', quality=95)
            b.close()
        if so_frames is not None: return fdir
        os.makedirs(os.path.dirname(saida), exist_ok=True)
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-framerate', str(FPS), '-i', os.path.join(fdir, '%05d.jpg'),
                        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', saida], check=True)
        return fdir

# ---------- blocos prontos ----------

def bg_grad(estilo):
    css = ESTILOS[estilo]['bg']
    def f(tl, tg):
        luz = (f"radial-gradient(38% 22% at 50% 64%, rgba(61,139,255,.28), rgba(0,0,0,0) 70%), radial-gradient(40% 25% at {50+30*math.sin(tg*0.6):.1f}% {30+8*math.cos(tg*0.5):.1f}%, rgba(61,139,255,.22), rgba(0,0,0,0) 70%)")
        return {'bgk': 'grad'+estilo, 'bghtml': f"<div class=grad style=\"background:{css}\"></div>", 'luz': luz,
                'vig': 'radial-gradient(130% 90% at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,.55) 100%)', 'phone': None}
    return f

def bg_foto(arq, z0=1.08, z1=1.22, px=(0, 0), escurece=0.55, blur=0):
    p = os.path.join(ASSETS, 'fotos', arq)
    from PIL import Image
    iw, ih = Image.open(p).size
    sc = max(W/iw, Hh/ih)   # cobre a tela
    def f(tl, tg, dur=None):
        return {}
    def mk(dur):
        def g(tl, tg):
            k = ease(tl/dur); z = lerp(z0, z1, k)
            dx = lerp(px[0], px[1] if len(px) > 1 else px[0], k)
            tr = f"translate(-50%,-50%) translate({dx:.1f}px,0) scale({sc*z:.4f})"
            return {'bgk': 'foto'+arq, 'bghtml': f"<img class=foto data-v=0 src='file://{p}' style='width:{iw}px;height:{ih}px'>",
                    'bgtr': tr, 'bgfilter': f'brightness({escurece}) saturate(1.05)' + (f' blur({blur}px)' if blur else ''),
                    'vig': 'linear-gradient(rgba(0,0,0,.35),rgba(0,0,0,0) 30%,rgba(0,0,0,0) 60%,rgba(0,0,0,.55))', 'luz': 'none', 'phone': None}
        return g
    return mk

def bg_tela(src, ss, dur, speed=1.0, z0=1.0, z1=1.0, fy0=0.0, fy1=0.0, escurece=1.0, freeze_ult=0.0, still_t=None):
    """Gravação do app em TELA CHEIA, nítida. fy = deslocamento vertical (px no espaço 1080x2338) pra focar."""
    fs = [still(src, still_t)] if still_t is not None else extrair(src, ss, dur - freeze_ult, speed)
    def g(tl, tg):
        i = min(len(fs) - 1, int(tl*FPS))
        k = ease(tl/dur); z = lerp(z0, z1, k); fy = lerp(fy0, fy1, k)
        # imagem 1080x2338; esconder barra de status: começa em -STATUS_H; centraliza a janela 1920
        y = -STATUS_H - fy
        tr = f"translate(0,{y:.1f}px) scale({z:.4f})"
        return {'bgk': 'tela', 'bghtml': "<img class=full data-v=1>", 'bgsrc': 'file://' + fs[i], 'bgtr': tr,
                'bgfilter': f'brightness({escurece})', 'vig': 'linear-gradient(rgba(0,0,0,.3) 0%,rgba(0,0,0,0) 12%,rgba(0,0,0,0) 46%,rgba(0,0,0,.84) 56%,rgba(0,0,0,.84) 73%,rgba(0,0,0,.2) 85%,rgba(0,0,0,.45) 100%)',
                'luz': 'none', 'phone': None}
    return g

def celular(src, ss, dur, speed=1.0, w=760, x=0, y=60, rot=(-14, 0), tilt=(6, 0), esc=(0.92, 1.0), zoom=None,
            ring=None, tap=None, still_t=None, fundo='B', push=0.06):
    """Celular premium com a gravação real dentro. zoom=(z0,z1,fy0,fy1): zoom da TELA dentro do celular.
    rot/tilt/esc animam de -> pra (com ease) no início da cena (0.7s)."""
    h = int(w*2.164)
    fs = [still(src, still_t)] if still_t is not None else extrair(src, ss, dur, speed)
    bgf = bg_grad(fundo)
    def g(tl, tg):
        s = bgf(tl, tg)
        i = min(len(fs) - 1, int(tl*FPS))
        k = eout(tl/0.8)
        ry = lerp(rot[0], rot[1], k); rx = lerp(tilt[0], tilt[1], k); sc = lerp(esc[0], esc[1], k)
        flut = 6*math.sin(tg*1.4)
        sc *= 1 + push*ease(tl/dur)
        tr = f"translate({x}px,{y+flut:.1f}px) rotateY({ry:.2f}deg) rotateX({rx:.2f}deg) scale({sc:.4f})"
        shadow = "drop-shadow(0 60px 70px rgba(0,0,0,.6)) drop-shadow(0 20px 24px rgba(0,0,0,.45)) drop-shadow(0 0 90px rgba(61,139,255,.25))"
        scr = 'none'
        sw = w - 44
        if zoom:
            z0, z1, fy0, fy1 = zoom; kz = ease(max(0, (tl - 0.5))/max(0.01, dur - 0.9))
            z = lerp(z0, z1, kz); fy = lerp(fy0, fy1, kz)
            scr = f"translate(0,{-(fy*sw/1080):.1f}px) scale({z:.4f})"
            # escala relativa ao topo; transform-origin topo-centro
            scr = f"translate(0,{-(fy*sw/1080):.1f}px) scale({z:.4f})"
        else:
            scr = f"translate(0,{-(STATUS_H*0)*(sw/1080):.1f}px)"
        st = {'k': 'ph', 'html': phone_html(), 'w': w, 'h': h, 'tr': tr, 'shadow': shadow,
              'src': 'file://' + fs[i], 'scr': scr}
        if ring:
            r0, r1 = ring.get('t', (0.6, dur))
            if r0 <= tl <= r1:
                a = min(1, (tl - r0)/0.25)
                st['ring'] = {'left': ring['l'], 'top': ring['tp'], 'width': ring['w'], 'height': ring['h'], 'opacity': f'{a:.2f}'}
        if tap:
            t0 = tap.get('t', 0.8)
            if t0 <= tl <= t0 + 0.6:
                kk = (tl - t0)/0.6
                st['tap'] = {'left': tap['l'], 'top': tap['tp'], 'opacity': f'{1-kk:.2f}', 'transform': f'scale({0.6+0.6*kk:.2f})'}
        s['phone'] = st
        return s
    return g

def T_cap(texto, hl_words=(), y=760, tam=96, ritmo=None, largura=940, inst=False):
    """Legenda palavra-por-palavra. ritmo = s por palavra (padrão garante leitura). inst=True mostra tudo no frame 1 (gancho)."""
    palavras = texto.split()
    hl = {i for i, p in enumerate(palavras) if p.strip('.,!?…:"“”').upper() in {h.upper() for h in hl_words}}
    rit = ritmo or 0.16
    def f(tl):
        if inst:
            n = len(palavras); idade = tl if tl < 0.16 else None
            return caption_html(palavras, hl, n, idade, y, tam, None, largura=largura)
        n = min(len(palavras), 1 + int(tl/rit)); idade = tl - (n - 1)*rit
        return caption_html(palavras, hl, n, idade, y, tam, None, largura=largura)
    return f

def T_tit(linhas, y=200, tam=130, hl_linhas=(), apoio=None, tam_apoio=44, entra=0.0, largura=940):
    """Título editorial (estilo B) com revelação de baixo pra cima por linha."""
    def f(tl):
        out = []
        for i, ln in enumerate(linhas):
            k = eout((tl - entra - i*0.09)/0.35)
            if k <= 0: continue
            cls = "hl" if i in hl_linhas else ""
            out.append(f"<div style='overflow:hidden'><div class='{cls}' style='transform:translateY({(1-k)*105:.1f}%);opacity:{min(1,k*1.4):.2f}'>{H.escape(ln)}</div></div>")
        ap = ''
        if apoio:
            k = eout((tl - entra - len(linhas)*0.09 - 0.15)/0.35)
            if k > 0:
                ap = f"<div class=apo style='font-size:{tam_apoio}px;margin-top:26px;opacity:{k:.2f};transform:translateY({(1-k)*20:.0f}px)'>{H.escape(apoio)}</div>"
        left = (W - largura)//2
        return f"<div class='t tit' style='left:{left}px;right:{left}px;top:{y}px;font-size:{tam}px'>{''.join(out)}{ap}</div>"
    return f

def T_badge(texto='APP MINHAMOTO', y=170):
    ic = os.path.join(ASSETS, 'icon.png')
    def f(tl):
        k = eback(min(1, tl/0.3)); sc = 0.6 + 0.4*k
        return (f"<div class=badge style='left:50%;top:{y}px;transform:translateX(-50%) scale({sc:.3f})'>"
                f"<img src='file://{ic}'>{H.escape(texto)}</div>")
    return f

def T_cta(titulo, sub=None, preco=None, y=330, estilo='A'):
    ic = os.path.join(ASSETS, 'icon.png'); selos = os.path.join(ASSETS, 'selos-lojas.png')
    fam = 'm900' if estilo == 'A' else 'anton'
    def f(tl):
        k1 = eback(min(1, tl/0.35)); k2 = eout((tl - 0.25)/0.35); k3 = eout((tl - 0.45)/0.35); k4 = eback(max(0, min(1, (tl - 0.6)/0.35)))
        s = (f"<div class=cta style='top:{y}px'>"
             f"<img class=ic src='file://{ic}' style='transform:scale({0.5+0.5*k1:.3f})'>"
             f"<div style='font-family:{fam};font-size:{104 if estilo=='A' else 128}px;color:#fff;text-transform:uppercase;line-height:1.02;margin-top:56px;padding:0 60px;"
             f"opacity:{k2:.2f};transform:translateY({(1-k2)*30:.0f}px);{'-webkit-text-stroke:8px #000;paint-order:stroke fill;' if estilo=='A' else ''}'>{titulo}</div>")
        if sub:
            s += f"<div style='font-family:{'m800' if estilo=='A' else 'pop600'};font-size:46px;color:#dbe6ff;margin-top:22px;opacity:{k3:.2f}'>{H.escape(sub)}</div>"
        if preco:
            s += f"<div class=preco style='transform:scale({max(0.01,k4):.3f})'>{H.escape(preco)}</div>"
        s += f"<div class=selos style='opacity:{k3:.2f}'><img src='file://{selos}'></div></div>"
        return s
    return f
