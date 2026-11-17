#!/usr/bin/env python3
"""Motor de vídeo da agência MinhaMoto (Reels/TikTok 9:16) — v2 (pós-revisão 16/11).

Uso: python3 agencia/designer/video.py agencia/roteiros-video/VP01.json [...]
Roteiro: {"id","titulo","formato","cenas":[{tipo, dur, ...}], legendas}

Tipos de cena:
  kinetic : linhas [str] (entram uma a uma, *destaque*), bg? ("dark"|"azul"), tam?, passo?
  photo   : foto (assets/fotos/ ou caminho), titulo, sub?, kicker?, n?, pos?, tam?   (Ken Burns + overlay)
  phone   : print (assets/prints/ ou caminho), titulo?, sub?, kicker?,
            scroll? [y0,y1] (% da altura da tela), zoom? [z0,z1], foco? [fx,fy] (0–1), toque? [t,x,y]
  clip    : video (agencia/referencias/material/...), ini, vel?, titulo?, sub?, kicker?,
            zoom? [z0,z1], foco? [fx,fy], toque? [t,x,y]    (gravação real dentro do celular)
  quiz    : pergunta, opcoes[str], certa(int), revela(s), explica?
  end     : titulo, sub?                                 (ícone + selos)

Garantias automáticas (o render FALHA se alguma quebrar):
  - tempo de leitura: cada cena fica, depois que o texto inteiro entrou, >= 0,45 s/palavra + 0,6 s
    (a duração é estendida sozinha; o ajuste é impresso)
  - zona segura: nada de texto/celular/selos fora de x 40–920, y 150–1540
  - sem flash: nenhum frame isolado com salto de brilho em relação aos vizinhos
  - mídia carregada antes do 1º frame (sem frame preto em troca de cena)
  - palavra curta colada na seguinte (sem "a"/"o"/"no" solto no fim da linha); títulos balanceados
Transição: dissolve de 0,2 s entre cenas.
Saída: videos/<ID>/video.mp4, capa.jpg — e revisao/<ID>-frames.jpg (1 frame a cada 0,5 s)
"""
import json, os, sys, subprocess, html, re, math, io

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(BASE, '..', '..'))
A = os.path.join(BASE, 'assets')
FPS = 30
W, H = 1080, 1920
ZONA = dict(top=150, bottom=1540, left=40, right=920)
XF = 0.2  # dissolve entre cenas (s)

CURTAS = ('a', 'o', 'e', 'é', 'as', 'os', 'à', 'às', 'ao', 'aos', 'no', 'na', 'nos', 'nas', 'do', 'da', 'dos', 'das', 'de',
          'em', 'um', 'uma', 'com', 'que', 'por', 'pra', 'pro', 'seu', 'sua', 'se', 'te', 'me', 'só', 'já', 'não', 'nem',
          'tá', 'ou', 'mas', 'sem', 'até', 'você:')
_PAT = re.compile(r'(?<![\w])(' + '|'.join(re.escape(c) for c in sorted(CURTAS, key=len, reverse=True)) + r') (?=\S)', re.I)

def glue(t):
    for _ in range(2): t = _PAT.sub(lambda m: m.group(1) + ' ', t)
    return t

def fmt(t):
    t = html.escape(glue(t or '')).replace('\\n', '\n').replace('\n', '<br>')
    return re.sub(r'\*(.+?)\*', r'<span class="ac">\1</span>', t)

def palavras(*ts):
    return sum(len(re.findall(r'\w+', (t or '').replace('*', ''))) for t in ts)

FONTS = ''.join(f"@font-face{{font-family:Inter;src:url('file://{A}/fontes/inter-latin-{w}-normal.woff2');font-weight:{w}}}"
                for w in (400, 600, 700, 800, 900))

CSS = FONTS + """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;font-family:Inter,sans-serif;background:#05080f;-webkit-font-smoothing:antialiased}
.scene{position:absolute;inset:0;visibility:hidden;overflow:hidden;background:#05080f}
.bg-dark{background:radial-gradient(80% 40% at 80% 10%,rgba(46,120,255,.32),rgba(46,120,255,0) 70%),
 radial-gradient(70% 35% at 0% 95%,rgba(46,120,255,.20),rgba(46,120,255,0) 70%),linear-gradient(175deg,#070b14,#04060b)}
.bg-azul{background:linear-gradient(160deg,#1f5fff,#0b3bd1)}
.t{font-weight:900;letter-spacing:-3px;line-height:1.06;color:#f4f7fb;text-wrap:balance}
.t .ac{color:#4b8dff}
.bg-azul .t{line-height:1.16}
.bg-azul .t .ac{color:#0c0f14;background:#fff;padding:.02em .12em 0;border-radius:10px;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.hl-under > .ac{color:transparent!important}
.hl-over{position:absolute;left:0;top:0;width:100%;margin:0!important;pointer-events:none;opacity:1!important;transform:none!important}
.hl-over .ac{background:none!important}
.s{font-weight:600;color:#b4c2d6;line-height:1.3;text-wrap:pretty}
.s .ac{color:#fff;font-weight:800}
.k{display:inline-block;font-weight:800;font-size:32px;letter-spacing:5px;text-transform:uppercase;color:#fff;background:#1f5fff;padding:12px 22px;border-radius:10px}
.box{position:absolute;left:80px;right:200px}
.line{display:block;will-change:transform,opacity}
.photo{position:absolute;left:-4%;top:-4%;width:108%;height:108%;object-fit:cover}
.ov{position:absolute;inset:0;background:linear-gradient(to top,rgba(4,8,14,.97) 0%,rgba(4,8,14,.85) 36%,rgba(4,8,14,.35) 62%,rgba(4,8,14,.45) 100%)}
.pwin{position:absolute;overflow:visible}
.pbody{position:absolute;left:0;top:0;width:100%;background:#0a0a0c;border-radius:72px;padding:14px;border:1px solid rgba(255,255,255,.09);
 box-shadow:0 60px 130px rgba(0,0,0,.8),0 0 140px rgba(46,120,255,.38)}
.screen{position:relative;width:100%;border-radius:58px;overflow:hidden;background:#000}
.media{position:absolute;left:0;top:0;width:100%;display:block;transform-origin:50% 0}
.cut{position:absolute;left:-60px;right:-60px;height:220px;background:linear-gradient(rgba(5,8,15,0),#05080f 75%)}
.tap{position:absolute;width:120px;height:120px;margin:-60px 0 0 -60px;border-radius:50%;background:rgba(255,255,255,.35);
 border:5px solid rgba(255,255,255,.9);box-shadow:0 0 40px rgba(75,141,255,.8);opacity:0}
.opt{display:flex;align-items:center;gap:28px;background:rgba(255,255,255,.06);border:3px solid rgba(255,255,255,.14);
 border-radius:30px;padding:34px 36px;margin-top:28px;font-weight:800;font-size:60px;color:#f4f7fb}
.opt b{display:inline-flex;width:84px;height:84px;border-radius:22px;background:#1f5fff;align-items:center;justify-content:center;font-size:48px;flex:none}
.opt.ok{background:#16a34a;border-color:#22c55e}
.bar{height:16px;border-radius:8px;background:rgba(255,255,255,.12);overflow:hidden;margin-top:40px}
.bar i{display:block;height:100%;background:linear-gradient(90deg,#4b8dff,#1f5fff);border-radius:8px}
.selos img{width:640px}
"""

def media_path(p, pasta):
    if os.path.isabs(p): return p
    if p.startswith('agencia/') or p.startswith('carrosseis/'): return os.path.join(REPO, p)
    return os.path.join(A, pasta, p)

PHONE_W = 560
def phone_html(c, kind, top, src, ratio):
    """Celular com sombra; base cortada com degradê se passar da zona segura."""
    w = c.get('phone_w', PHONE_W); left = (W - w) // 2 - 40
    crop = c.get('crop_topo', 80 if kind == 'clip' else 0)   # px (na mídia original) de barra de status cortada
    sw = w - 28
    screen_h = sw * ratio - sw * crop / 1080.0
    body_h = screen_h + 28
    vis_h = min(body_h, ZONA['bottom'] - top)
    cut = (f"<div class='cut' style='top:{vis_h - 200:.0f}px'></div>" if vis_h < body_h else '')
    tag = (f"<video class='media' src='file://{src}' muted preload='auto' playsinline></video>" if kind == 'clip'
           else f"<img class='media' src='file://{src}'>")
    return (f"<div class='pwin' style='left:{left}px;top:{top}px;width:{w}px;height:{vis_h:.0f}px' data-crop='{crop}'>"
            f"<div class='pbody'><div class='screen' style='height:{screen_h:.0f}px'>{tag}<div class='tap'></div></div></div>"
            f"{cut}</div>")

def head_html(c, top, size_t=96):
    k = f"<div class='k' style='margin-bottom:30px'>{fmt(c['kicker'])}</div>" if c.get('kicker') else ''
    t = f"<div class='t' style='font-size:{c.get('tam', size_t)}px'>{fmt(c['titulo'])}</div>" if c.get('titulo') else ''
    s = f"<div class='s' style='font-size:{c.get('tam_sub', 52)}px;margin-top:22px'>{fmt(c['sub'])}</div>" if c.get('sub') else ''
    return f"<div class='box head' style='top:{top}px'>{k}{t}{s}</div>"

def media_ratio(src, kind):
    if kind == 'clip':
        out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height',
                              '-of', 'csv=p=0', src], capture_output=True, text=True).stdout.strip().split(',')
        w, h = int(out[0]), int(out[1])
    else:
        from PIL import Image
        w, h = Image.open(src).size
    return h / w

def scene_html(i, c):
    t = c['tipo']
    if t == 'kinetic':
        bg = 'bg-azul' if c.get('bg') == 'azul' else 'bg-dark'
        size = c.get('tam', 118)
        lines = ''.join(f"<span class='line t' style='font-size:{size}px;margin-bottom:22px'>{fmt(l)}</span>" for l in c['linhas'])
        return (f"<div class='scene {bg}' id='s{i}'><div class='box drift' style='top:{ZONA['top']+40}px;bottom:{H-ZONA['bottom']+40}px;"
                f"display:flex;flex-direction:column;justify-content:center'>{lines}</div></div>")
    if t == 'photo':
        f = media_path(c['foto'], 'fotos')
        n = f"<div class='t' style='font-size:120px;color:#4b8dff;margin-bottom:6px'>{html.escape(str(c['n']))}</div>" if c.get('n') else ''
        k = f"<div class='k' style='margin-bottom:30px'>{fmt(c['kicker'])}</div>" if c.get('kicker') else ''
        sub = f"<div class='s' style='font-size:{c.get('tam_sub', 54)}px;margin-top:30px'>{fmt(c['sub'])}</div>" if c.get('sub') else ''
        return (f"<div class='scene' id='s{i}'><img class='photo' src='file://{f}' style='object-position:{c.get('pos', 'center')}'><div class='ov'></div>"
                f"<div class='box drift' style='bottom:{H - ZONA['bottom'] + 30}px'>{n}{k}<div class='t line' style='font-size:{c.get('tam', 112)}px;"
                f"text-transform:uppercase'>{fmt(c['titulo'])}</div>{sub}</div></div>")
    if t in ('phone', 'clip'):
        src = media_path(c['print'] if t == 'phone' else c['video'], 'prints')
        ratio = media_ratio(src, t)
        head = head_html(c, ZONA['top'] + 20) if (c.get('titulo') or c.get('sub') or c.get('kicker')) else ''
        top = c.get('top', 640 if head else 260)
        return f"<div class='scene bg-dark' id='s{i}'>{head}{phone_html(c, t, top, src, ratio)}</div>"
    if t == 'quiz':
        opts = ''.join(f"<div class='opt' data-i='{j}'><b>{'ABC'[j]}</b><span>{fmt(o)}</span></div>" for j, o in enumerate(c['opcoes']))
        ex = f"<div class='s ex' style='font-size:58px;margin-top:40px;opacity:0;color:#e6edf7'>{fmt(c.get('explica', ''))}</div>"
        return (f"<div class='scene bg-dark' id='s{i}'><div class='box drift' style='top:{ZONA['top']+40}px'>"
                f"<div class='k' style='margin-bottom:34px'>Quiz</div><div class='t line' style='font-size:{c.get('tam', 104)}px'>{fmt(c['pergunta'])}</div>"
                f"<div class='opts' style='margin-top:40px'>{opts}</div><div class='bar'><i></i></div>{ex}</div></div>")
    if t == 'end':
        sub = f"<div class='s' style='font-size:54px;margin-top:30px'>{fmt(c['sub'])}</div>" if c.get('sub') else ''
        return (f"<div class='scene bg-dark' id='s{i}'><div class='box drift' style='top:{ZONA['top']+40}px;bottom:{H-ZONA['bottom']+40}px;"
                f"display:flex;flex-direction:column;justify-content:center'>"
                f"<img class='line icon' src='file://{A}/icon.png' style='width:170px;border-radius:40px;margin-bottom:50px;box-shadow:0 0 90px rgba(46,120,255,.5)'>"
                f"<div class='t line' style='font-size:{c.get('tam', 116)}px'>{fmt(c['titulo'])}</div>{sub}"
                f"<div class='selos line' style='margin-top:70px'><img src='file://{A}/selos-lojas.png'></div></div></div>")
    raise ValueError(t)

def ajustar_tempos(rot):
    """Estende cenas curtas demais pra leitura (>= 0,45 s/palavra + 0,6 s depois que tudo entrou)."""
    log = []
    for i, c in enumerate(rot['cenas']):
        t = c['tipo']; lead = 0.4 if i == 0 else 0.1
        if t == 'kinetic':
            n = len(c['linhas']); step = c.get('passo') or 0.32
            c['passo'] = step
            entra = max(0.0, (n - 1) * step + 0.28 - lead)
            w = palavras(*c['linhas'])
            need = entra + 0.45 * w + 0.6
            if c.get('eco'): need = 0  # repetição do gancho pro loop (já lido no início)
        elif t in ('photo', 'phone', 'clip', 'end'):
            w = palavras(c.get('kicker'), c.get('titulo'), c.get('sub'))
            need = (0.45 * w + 0.6 + 0.5) if w else 0
        elif t == 'quiz':
            wq = palavras(c['pergunta'], *c['opcoes'])
            entra = 0.5 + len(c['opcoes']) * 0.25 + 0.3
            c['revela'] = round(max(c.get('revela', 0), entra + 0.4 * wq), 2)
            we = palavras(c.get('explica'))
            need = c['revela'] + 0.7 + 0.45 * we + 0.6
        else:
            need = 0
        if c['dur'] < need - 1e-6:
            log.append(f"cena {i} ({t}): {c['dur']:.2f}s -> {need:.2f}s")
            c['dur'] = round(need + 0.05, 2)
    return log

JS = r"""
const S = window.SCENES;
const ease = x => 1 - Math.pow(1 - Math.min(Math.max(x,0),1), 3);
const inout = x => { x=Math.min(Math.max(x,0),1); return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2; };
function pop(el, p){ const e=ease(p); el.style.opacity=Math.min(1,Math.max(0,p*1.6)); el.style.transform=`translateY(${(1-e)*60}px) scale(${0.94+0.06*e})`; }
function lerp(a,b,x){ return a+(b-a)*x; }
function sceneAt(t){ let acc=0; for(let i=0;i<S.length;i++){ if(t<acc+S[i].dur||i===S.length-1) return [i,acc]; acc+=S[i].dur; } }
async function drawScene(idx, lr){
  const sc=S[idx], root=document.getElementById('s'+idx); const lt = lr + ((idx===0||sc.eco) ? 0.4 : 0.1); const prog = lr/sc.dur;
  if (root.classList.contains('bg-dark')||root.classList.contains('bg-azul')){ root.style.backgroundSize='130% 130%'; root.style.backgroundPosition=`${50+18*Math.sin((lr+idx)*0.6)}% ${50+12*Math.cos((lr+idx)*0.5)}%`; }
  const drift = root.querySelector('.drift'); if (drift){ drift.style.transformOrigin='0% 50%'; drift.style.transform=`scale(${1+0.045*prog})`; }
  if (sc.tipo==='kinetic'){
    root.querySelectorAll('.line').forEach((l,i)=>{ const p=(lt - i*sc.passo + 0.25)/0.28; if(p<=0){l.style.opacity=0} else pop(l,p); });
  } else if (sc.tipo==='photo'){
    root.querySelector('.photo').style.transform = `scale(${1.0 + 0.08*prog})`;
    root.querySelectorAll('.box > *').forEach((l,i)=>{ const p=(lt - i*0.12)/0.28; if(p<=0){l.style.opacity=0} else pop(l,p) });
  } else if (sc.tipo==='phone' || sc.tipo==='clip'){
    const pw = root.querySelector('.pwin'), m = root.querySelector('.media'), scr = root.querySelector('.screen');
    const e = ease(lt/0.45); pw.style.transform = `translateY(${(1-e)*260}px)`; pw.style.opacity = Math.min(1, lt/0.25);
    root.querySelectorAll('.head > *').forEach((l,i)=>{ const p=(lt - i*0.12)/0.28; if(p<=0){l.style.opacity=0} else pop(l,p) });
    const z = sc.zoom ? lerp(sc.zoom[0], sc.zoom[1], inout(prog)) : 1;
    const f = sc.foco || [0.5, 0.3];
    const crop = parseFloat(pw.dataset.crop)||0; const mh = m.getBoundingClientRect().height / (parseFloat(m.dataset.z||1));
    const cropPct = crop/ (sc.tipo==='clip' ? (m.videoHeight||2338) : (m.naturalHeight||1)) * 100;
    const sy = sc.scroll ? lerp(sc.scroll[0], sc.scroll[1], inout(prog)) : 0;
    m.style.transformOrigin = `${f[0]*100}% ${f[1]*100}%`;
    m.style.transform = `translateY(${-(cropPct + sy)}%) scale(${z})`;
    if (sc.tipo==='clip'){
      const tt = sc.ini + lr*(sc.vel||1);
      if (Math.abs(m.currentTime - tt) > 0.001){ await new Promise(res=>{ const done=()=>{m.removeEventListener('seeked',done);res()}; m.addEventListener('seeked',done); m.currentTime=tt; setTimeout(res,3000); }); }
    }
    const tap = root.querySelector('.tap');
    if (sc.toque){ const d = lr - sc.toque[0]; tap.style.left=(sc.toque[1]*100)+'%'; tap.style.top=(sc.toque[2]*100)+'%';
      tap.style.opacity = (d>=0 && d<0.6) ? (1 - d/0.6) : 0; tap.style.transform = `scale(${d>=0 ? 0.6+0.8*Math.min(d/0.6,1) : 0.6})`; }
  } else if (sc.tipo==='quiz'){
    const rv = sc.revela; const opts = root.querySelectorAll('.opt');
    root.querySelectorAll('.box > .k, .box > .t').forEach((l,i)=>{ const p=(lt-i*0.1)/0.28; if(p<=0){l.style.opacity=0} else pop(l,p) });
    opts.forEach((o,i)=>{ const p=(lt-0.5-i*0.25)/0.28; if(p<=0){o.style.opacity=0} else pop(o,p);
      o.classList.toggle('ok', lr>=rv && i===sc.certa); if(lr>=rv && i!==sc.certa) o.style.opacity=.25;
      if(lr>=rv && i===sc.certa){ const q=Math.min(1,(lr-rv)/0.3); o.style.transform=`scale(${1+0.04*Math.sin(q*Math.PI)})`; o.style.boxShadow=`0 0 ${40+30*Math.sin((lr-rv)*5)}px rgba(34,197,94,.55)`; } else { o.style.boxShadow='none'; } });
    const bar = root.querySelector('.bar'), bi = bar.querySelector('i');
    const p0 = 0.5 + opts.length*0.25 + 0.3; const bp = Math.min(1, Math.max(0, (lr - p0)/(rv - p0)));
    bi.style.width = (100 - bp*100) + '%'; bar.style.opacity = lr < rv ? 1 : Math.max(0, 1-(lr-rv)/0.3);
    const ex = root.querySelector('.ex'); const pe=(lr-rv-0.4)/0.3; if(pe<=0){ex.style.opacity=0} else pop(ex,pe);
  } else if (sc.tipo==='end'){
    root.querySelectorAll('.line').forEach((l,i)=>{ const p=(lt - i*0.15)/0.3; if(p<=0){l.style.opacity=0} else pop(l,p) });
  }
}
window.render = async function(t){
  const [idx, acc] = sceneAt(t); const lr = t - acc;
  document.querySelectorAll('.scene').forEach((e,i)=>{ e.style.visibility = 'hidden'; e.style.opacity = 1; e.style.zIndex = 0; });
  const cur = document.getElementById('s'+idx); cur.style.visibility='visible'; cur.style.zIndex=2;
  await drawScene(idx, lr);
  if (idx>0 && lr < XF){  // dissolve: cena anterior por baixo, atual entrando por cima
    const prev = document.getElementById('s'+(idx-1)); prev.style.visibility='visible'; prev.style.zIndex=1;
    await drawScene(idx-1, S[idx-1].dur - 0.0001 + lr);
    prev.querySelectorAll('.box, .head, .pwin').forEach(e=>e.style.opacity=0);  // só o fundo dissolve (sem texto fantasma)
    cur.style.opacity = Math.min(1, lr/XF);
  }
};
window.zona = function(){
  const v=[]; const cur=[...document.querySelectorAll('.scene')].find(s=>s.style.visibility==='visible'&&s.style.zIndex==='2');
  cur.querySelectorAll('.t:not(.hl-over), .s, .k, .opt, .selos img, .icon, .pwin, .bar').forEach(el=>{
    if (parseFloat(getComputedStyle(el).opacity) < 0.05) return;
    let anc=el; while(anc && anc!==cur){ if(parseFloat(getComputedStyle(anc).opacity)<0.05) return; anc=anc.parentElement; }
    const r = el.getBoundingClientRect(); if (r.width<2||r.height<2) return;
    const nome = (el.className||el.tagName).toString().split(' ')[0];
    if (r.top < ZT || r.bottom > ZB + 1 || r.left < ZL || r.right > ZR + 1)
      v.push(`${cur.id} ${nome} [${Math.round(r.left)},${Math.round(r.top)},${Math.round(r.right)},${Math.round(r.bottom)}] "${(el.innerText||'').slice(0,40).replace(/\n/g,' ')}"`);
  });
  return v;
};
window.preparar = async function(){
  await document.fonts.ready;
  await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));
  await Promise.all([...document.querySelectorAll('video')].map(v=> v.readyState>=2 ? 0 : new Promise(r=>{ v.addEventListener('loadeddata',r,{once:true}); setTimeout(r,8000); })));
  document.querySelectorAll('.t, .s').forEach(el=>{  // texto nunca estoura a caixa: reduz a fonte até caber
    let f=parseFloat(getComputedStyle(el).fontSize); const tr=el.style.transform; el.style.transform='none';
    while(el.scrollWidth > el.clientWidth + 1 && f > 40){ f-=3; el.style.fontSize=f+'px'; }
    el.style.transform=tr;
  });
  document.querySelectorAll('.t').forEach(el=>{   // marca-texto por baixo do texto (nunca corta letra)
    const ac=el.querySelector(':scope > .ac'); if(!ac) return;
    const bg=getComputedStyle(ac).backgroundColor; if(!bg||bg==='rgba(0, 0, 0, 0)') return;
    if(getComputedStyle(el).position==='static') el.style.position='relative';
    const c=el.cloneNode(true); c.className='t hl-over'; c.style.cssText='font-size:'+getComputedStyle(el).fontSize; el.classList.add('hl-under'); el.appendChild(c);
  });
  document.body.dataset.ok=1;
};
"""

def build(rot):
    scenes = ''.join(scene_html(i, c) for i, c in enumerate(rot['cenas']))
    data = json.dumps(rot['cenas'], ensure_ascii=False)
    consts = f"const XF={XF},ZT={ZONA['top']},ZB={ZONA['bottom']},ZL={ZONA['left']},ZR={ZONA['right']};"
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{scenes}"
            f"<script>window.SCENES={data};{consts}</script><script>{JS}</script></body></html>")

def luminancia(jpg):
    from PIL import Image
    im = Image.open(io.BytesIO(jpg)).convert('L').resize((54, 96))
    return sum(im.tobytes()) / (54 * 96)

def main(path, force=False):
    rot = json.load(open(path, encoding='utf-8'))
    rid = rot['id']; out = os.path.join(REPO, 'videos', rid); os.makedirs(out, exist_ok=True)
    for l in ajustar_tempos(rot): print(f'{rid} tempo de leitura: {l}')
    dur = sum(c['dur'] for c in rot['cenas']); n = int(round(dur * FPS))
    tmp = f'/tmp/video_{rid}.html'; open(tmp, 'w', encoding='utf-8').write(build(rot))
    mp4 = os.path.join(out, 'video.mp4')
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', mp4],
                          stdin=subprocess.PIPE)
    from playwright.sync_api import sync_playwright
    os.makedirs(os.path.join(REPO, 'revisao'), exist_ok=True)
    frames_review, lums, problemas = [], [], []
    # instantes de checagem da zona segura: 60% e fim de cada cena
    checks, acc = set(), 0.0
    for c in rot['cenas']:
        checks.add(int((acc + c['dur'] * 0.6) * FPS)); checks.add(int((acc + c['dur']) * FPS) - 2); acc += c['dur']
    with sync_playwright() as pw:
        args = ['--no-sandbox', '--force-color-profile=srgb', '--autoplay-policy=no-user-gesture-required']
        b = (pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=args)
             if os.path.exists('/usr/bin/google-chrome') else pw.chromium.launch(args=args))
        pg = b.new_page(viewport={'width': W, 'height': H})
        pg.goto('file://' + tmp); pg.evaluate('preparar()'); pg.wait_for_selector('body[data-ok]', timeout=20000)
        for f in range(n):
            t = f / FPS
            pg.evaluate(f'render({t:.5f})')
            if f in checks:
                for v in pg.evaluate('zona()'): problemas.append(f'zona segura @ {t:.2f}s: {v}')
            jpg = pg.screenshot(type='jpeg', quality=93)
            ff.stdin.write(jpg); lums.append(luminancia(jpg))
            if f % (FPS // 2) == 0: frames_review.append((t, jpg))
            if f == int(FPS * rot.get('capa_t', 1.2)): open(os.path.join(out, 'capa.jpg'), 'wb').write(jpg)
        b.close()
    ff.stdin.close(); ff.wait()
    for f in range(1, len(lums) - 1):   # flash: frame isolado com salto de brilho
        a, m, c = lums[f - 1], lums[f], lums[f + 1]
        if abs(m - a) > 14 and abs(m - c) > 14 and (m - a) * (m - c) > 0:
            problemas.append(f'flash no frame {f} ({f / FPS:.2f}s): brilho {a:.0f} -> {m:.0f} -> {c:.0f}')
    from PIL import Image, ImageDraw
    cw, ch = 216, 384; cols = 8; rows = math.ceil(len(frames_review) / cols)
    sheet = Image.new('RGB', (cols * cw, rows * (ch + 26)), 'white'); d = ImageDraw.Draw(sheet)
    for k, (t, jpg) in enumerate(frames_review):
        im = Image.open(io.BytesIO(jpg)).resize((cw, ch)); x = (k % cols) * cw; y = (k // cols) * (ch + 26)
        sheet.paste(im, (x, y)); d.text((x + 4, y + ch + 6), f'{t:.1f}s', fill='black')
    sheet.save(os.path.join(REPO, 'revisao', f'{rid}-frames.jpg'), quality=85)
    json.dump(rot, open(os.path.join(out, 'roteiro-renderizado.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(rid, f'{dur:.1f}s', n, 'frames ->', mp4)
    return problemas

if __name__ == '__main__':
    todos = []
    for p in sys.argv[1:]:
        todos += [f'{os.path.basename(p)}: {x}' for x in main(p)]
    if todos:
        print('\n'.join('PROBLEMA: ' + x for x in todos)); sys.exit(2)
