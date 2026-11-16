#!/usr/bin/env python3
"""Motor de vídeo da agência MinhaMoto (Reels/TikTok 9:16).

Uso: python3 agencia/designer/video.py agencia/roteiros-video/VP01.json
Roteiro: {"id","titulo","formato","cenas":[{tipo, dur, ...}], legendas}
Tipos de cena:
  kinetic : linhas [str] (aparecem uma a uma, *destaque*), bg? ("dark"|"azul"), tam?
  photo   : foto, titulo, sub?, kicker?, n?            (Ken Burns + overlay)
  phone   : print, titulo, sub?                          (celular com sombra, zoom suave)
  quiz    : pergunta, opcoes[str], certa(int), revela(s) , explica?
  end     : titulo, sub?                                 (ícone + selos)
Saída: videos/<ID>/video.mp4, capa.jpg  — e revisao/<ID>-frames.jpg (1 frame a cada 0,5 s)
Renderiza frame a frame no Chrome (Playwright) e codifica com ffmpeg (H.264, 30 fps).
"""
import json, os, sys, subprocess, html, re, math

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(BASE, '..', '..'))
A = os.path.join(BASE, 'assets')
FPS = 30
W, H = 1080, 1920

def fmt(t):
    t = html.escape(t or '').replace('\\n', '\n').replace('\n', '<br>')
    return re.sub(r'\*(.+?)\*', r'<span class="ac">\1</span>', t)

FONTS = ''.join(f"@font-face{{font-family:Inter;src:url('file://{A}/fontes/inter-latin-{w}-normal.woff2');font-weight:{w}}}"
                for w in (400, 600, 700, 800, 900))

CSS = FONTS + """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;font-family:Inter,sans-serif;background:#05080f;-webkit-font-smoothing:antialiased}
.scene{position:absolute;inset:0;display:none;overflow:hidden}
.bg-dark{background:radial-gradient(80% 40% at 80% 10%,rgba(46,120,255,.32),rgba(46,120,255,0) 70%),
 radial-gradient(70% 35% at 0% 95%,rgba(46,120,255,.20),rgba(46,120,255,0) 70%),linear-gradient(175deg,#070b14,#04060b)}
.bg-azul{background:linear-gradient(160deg,#1f5fff,#0b3bd1)}
.t{font-weight:900;letter-spacing:-3px;line-height:1.02;color:#f4f7fb}
.t .ac{color:#3d8bff}
.bg-azul .t .ac{color:#0c0f14;background:#fff;padding:0 .12em;border-radius:8px}
.s{font-weight:600;color:#a9b8cd;line-height:1.3}
.s .ac{color:#fff;font-weight:800}
.k{display:inline-block;font-weight:800;font-size:30px;letter-spacing:5px;text-transform:uppercase;color:#fff;background:#1f5fff;padding:12px 22px;border-radius:10px}
.box{position:absolute;left:80px;right:160px}
.line{display:block;will-change:transform,opacity}
.photo{position:absolute;inset:-4%;background-size:cover;background-position:center}
.ov{position:absolute;inset:0;background:linear-gradient(to top,rgba(4,8,14,.97) 0%,rgba(4,8,14,.82) 38%,rgba(4,8,14,.30) 66%,rgba(4,8,14,.35) 100%)}
.phone{position:absolute;background:#0a0a0c;border-radius:74px;padding:14px;border:1px solid rgba(255,255,255,.08);
 box-shadow:0 60px 130px rgba(0,0,0,.8),0 0 140px rgba(46,120,255,.38)}
.phone img{display:block;width:100%;border-radius:60px}
.opt{display:flex;align-items:center;gap:28px;background:rgba(255,255,255,.06);border:3px solid rgba(255,255,255,.12);
 border-radius:28px;padding:30px 34px;margin-top:26px;font-weight:800;font-size:52px;color:#f4f7fb}
.opt b{display:inline-flex;width:76px;height:76px;border-radius:20px;background:#1f5fff;align-items:center;justify-content:center;font-size:44px;flex:none}
.opt.ok{background:#16a34a;border-color:#22c55e}
.opt.ko{opacity:.28}
.timer{font-weight:900;font-size:120px;color:#3d8bff}
.selos img{width:640px}
"""

def scene_html(i, c):
    t = c['tipo']
    if t == 'kinetic':
        bg = 'bg-azul' if c.get('bg') == 'azul' else 'bg-dark'
        size = c.get('tam', 118)
        lines = ''.join(f"<span class='line t' style='font-size:{size}px;margin-bottom:18px'>{fmt(l)}</span>" for l in c['linhas'])
        return f"<div class='scene {bg}' id='s{i}'><div class='box' style='top:0;bottom:0;display:flex;flex-direction:column;justify-content:center'>{lines}</div></div>"
    if t == 'photo':
        f = os.path.join(A, 'fotos', c['foto'])
        n = f"<div class='t' style='font-size:110px;color:#3d8bff;margin-bottom:6px'>{html.escape(str(c['n']))}</div>" if c.get('n') else ''
        k = f"<div class='k' style='margin-bottom:30px'>{fmt(c['kicker'])}</div>" if c.get('kicker') else ''
        sub = f"<div class='s' style='font-size:52px;margin-top:30px'>{fmt(c['sub'])}</div>" if c.get('sub') else ''
        return (f"<div class='scene' id='s{i}'><div class='photo' style=\"background-image:url('file://{f}');background-position:{c.get('pos','center')}\"></div><div class='ov'></div>"
                f"<div class='box' style='bottom:520px'>{n}{k}<div class='t line' style='font-size:{c.get('tam',112)}px;text-transform:uppercase'>{fmt(c['titulo'])}</div>{sub}</div></div>")
    if t == 'phone':
        p = os.path.join(A, 'prints', c['print'])
        sub = f"<div class='s' style='font-size:46px;margin-top:20px'>{fmt(c['sub'])}</div>" if c.get('sub') else ''
        return (f"<div class='scene bg-dark' id='s{i}'><div class='box' style='top:170px'><div class='t line' style='font-size:{c.get('tam',96)}px'>{fmt(c['titulo'])}</div>{sub}</div>"
                f"<div class='phone' style='left:260px;top:{c.get('top',600)}px;width:560px'><img src='file://{p}'></div></div>")
    if t == 'quiz':
        opts = ''.join(f"<div class='opt' data-i='{j}'><b>{'ABC'[j]}</b><span>{fmt(o)}</span></div>" for j, o in enumerate(c['opcoes']))
        ex = f"<div class='s ex' style='font-size:46px;margin-top:44px;opacity:0'>{fmt(c.get('explica',''))}</div>"
        return (f"<div class='scene bg-dark' id='s{i}'><div class='box' style='top:200px'>"
                f"<div class='k' style='margin-bottom:34px'>Quiz</div><div class='t line' style='font-size:{c.get('tam',100)}px'>{fmt(c['pergunta'])}</div>"
                f"<div style='margin-top:40px'>{opts}</div><div class='timer' style='margin-top:30px'></div>{ex}</div></div>")
    if t == 'end':
        sub = f"<div class='s' style='font-size:50px;margin-top:30px'>{fmt(c['sub'])}</div>" if c.get('sub') else ''
        return (f"<div class='scene bg-dark' id='s{i}'><div class='box' style='top:0;bottom:0;display:flex;flex-direction:column;justify-content:center'>"
                f"<img class='line' src='file://{A}/icon.png' style='width:170px;border-radius:40px;margin-bottom:50px;box-shadow:0 0 90px rgba(46,120,255,.5)'>"
                f"<div class='t line' style='font-size:{c.get('tam',112)}px'>{fmt(c['titulo'])}</div>{sub}"
                f"<div class='selos line' style='margin-top:70px'><img src='file://{A}/selos-lojas.png'></div></div></div>")
    raise ValueError(t)

JS = r"""
const S = window.SCENES;
const ease = x => 1 - Math.pow(1 - Math.min(Math.max(x,0),1), 3);
function pop(el, p){ const e=ease(p); el.style.opacity=Math.min(1,p*1.6); el.style.transform=`translateY(${(1-e)*60}px) scale(${0.94+0.06*e})`; }
window.render = function(t){
  let acc = 0, idx = 0;
  for (; idx < S.length; idx++){ if (t < acc + S[idx].dur || idx === S.length-1) break; acc += S[idx].dur; }
  const lr = t - acc, sc = S[idx]; const lt = lr + (idx===0 ? 0.4 : 0.1);
  document.querySelectorAll('.scene').forEach((e,i)=>e.style.display = i===idx ? 'block':'none');
  const root = document.getElementById('s'+idx);
  if (root.classList.contains('bg-dark')||root.classList.contains('bg-azul')){ root.style.backgroundSize='130% 130%'; root.style.backgroundPosition=`${50+18*Math.sin(t*0.6)}% ${50+12*Math.cos(t*0.5)}%`; }
  if (sc.tipo === 'kinetic'){
    const ls = root.querySelectorAll('.line'); const step = sc.passo || Math.min(0.55, (sc.dur*0.75)/ls.length);
    ls.forEach((l,i)=>{ const p=(lt - i*step + 0.25)/0.28; if(p<=0){l.style.opacity=0} else pop(l,p); });
  } else if (sc.tipo === 'photo'){
    root.querySelector('.photo').style.transform = `scale(${1.0 + 0.08*lt/sc.dur})`;
    root.querySelectorAll('.box > *').forEach((l,i)=>{ const p=(lt - i*0.12)/0.28; if(p<=0){l.style.opacity=0} else pop(l,p) });
  } else if (sc.tipo === 'phone'){
    const ph = root.querySelector('.phone'); const e = ease(lt/0.45);
    ph.style.transform = `translateY(${(1-e)*260}px) scale(${1+0.06*lt/sc.dur})`; ph.style.opacity = Math.min(1, lt/0.25);
    root.querySelectorAll('.box > *').forEach((l,i)=>{ const p=(lt - i*0.12)/0.28; if(p<=0){l.style.opacity=0} else pop(l,p) });
  } else if (sc.tipo === 'quiz'){
    const rv = sc.revela + (idx===0 ? 0.4 : 0.1); const opts = root.querySelectorAll('.opt');
    root.querySelectorAll('.box > .k, .box > .t').forEach((l,i)=>{ const p=(lt-i*0.1)/0.28; if(p<=0){l.style.opacity=0} else pop(l,p) });
    opts.forEach((o,i)=>{ const p=(lt-0.5-i*0.25)/0.28; if(p<=0){o.style.opacity=0} else pop(o,p);
      o.classList.toggle('ok', lt>=rv && i===sc.certa); o.classList.toggle('ko', lt>=rv && i!==sc.certa); if(lt>=rv && i!==sc.certa) o.style.opacity=.28; });
    const tm = root.querySelector('.timer'); const left = Math.ceil(rv - lt);
    tm.textContent = (lt>1.4 && lt<rv) ? left : '';
    const ex = root.querySelector('.ex'); ex.style.opacity = lt>=rv+0.4 ? Math.min(1,(lt-rv-0.4)/0.3) : 0;
  } else if (sc.tipo === 'end'){
    root.querySelectorAll('.line').forEach((l,i)=>{ const p=(lt - i*0.15)/0.3; if(p<=0){l.style.opacity=0} else pop(l,p) });
  }
};
document.fonts.ready.then(()=>{ document.body.dataset.ok=1; });
"""

def build(rot):
    scenes = ''.join(scene_html(i, c) for i, c in enumerate(rot['cenas']))
    data = json.dumps([{k: v for k, v in c.items()} for c in rot['cenas']], ensure_ascii=False)
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{scenes}"
            f"<script>window.SCENES={data};</script><script>{JS}</script></body></html>")

def main(path):
    rot = json.load(open(path, encoding='utf-8'))
    rid = rot['id']; out = os.path.join(REPO, 'videos', rid); os.makedirs(out, exist_ok=True)
    dur = sum(c['dur'] for c in rot['cenas']); n = int(round(dur * FPS))
    tmp = f'/tmp/video_{rid}.html'; open(tmp, 'w', encoding='utf-8').write(build(rot))
    mp4 = os.path.join(out, 'video.mp4')
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', mp4],
                          stdin=subprocess.PIPE)
    from playwright.sync_api import sync_playwright
    os.makedirs(os.path.join(REPO, 'revisao'), exist_ok=True)
    frames_review = []
    with sync_playwright() as pw:
        args = ['--no-sandbox', '--force-color-profile=srgb']
        b = (pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=args)
             if os.path.exists('/usr/bin/google-chrome') else pw.chromium.launch(args=args))
        pg = b.new_page(viewport={'width': W, 'height': H})
        pg.goto('file://' + tmp); pg.wait_for_selector('body[data-ok]', timeout=15000); pg.wait_for_timeout(300)
        for f in range(n):
            t = f / FPS
            pg.evaluate(f'render({t:.5f})')
            jpg = pg.screenshot(type='jpeg', quality=92)
            ff.stdin.write(jpg)
            if f % (FPS // 2) == 0: frames_review.append((t, jpg))
            if f == int(FPS * rot.get('capa_t', 1.2)): open(os.path.join(out, 'capa.jpg'), 'wb').write(jpg)
        b.close()
    ff.stdin.close(); ff.wait()
    # folha de frames (1 a cada 0,5 s)
    from PIL import Image, ImageDraw
    import io
    cw, ch = 216, 384; cols = 8; rows = math.ceil(len(frames_review) / cols)
    sheet = Image.new('RGB', (cols * cw, rows * (ch + 26)), 'white'); d = ImageDraw.Draw(sheet)
    for k, (t, jpg) in enumerate(frames_review):
        im = Image.open(io.BytesIO(jpg)).resize((cw, ch)); x = (k % cols) * cw; y = (k // cols) * (ch + 26)
        sheet.paste(im, (x, y)); d.text((x + 4, y + ch + 6), f'{t:.1f}s', fill='black')
    sheet.save(os.path.join(REPO, 'revisao', f'{rid}-frames.jpg'), quality=85)
    print(rid, f'{dur:.1f}s', n, 'frames ->', mp4)

if __name__ == '__main__':
    for p in sys.argv[1:]: main(p)
