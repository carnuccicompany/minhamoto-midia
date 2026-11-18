#!/usr/bin/env python3
"""Revisor automático de peças (vídeo 9:16, carrossel, story). Régua: agencia/DESIGN-MINHAMOTO.md.

Uso:
  python3 agencia/designer/revisar_video.py <video.mp4|imagem.jpg ...> [--roteiro arquivo.py|.json|.md]

Checagens (qualquer REPROVA bloqueia a entrega ao Léo):
  1. Mockup consistente (vídeo): extrai 4 quadros/s, localiza o celular (moldura escura com a tela do app) e
     compara a faixa da status bar/ilha entre todas as cenas. Diferença acima do limiar = REPROVA
     (ex.: ilha aparece numa cena e some na outra, alça de pop-up colada no topo).
  2. Cor proibida: amostra cada quadro procurando o amarelo antigo (#FFD400 / #F5B300). Área relevante = REPROVA.
  3. Texto proibido: OCR (tesseract, se instalado) em cada quadro; senão procura no roteiro (--roteiro).
     Lista: "demonstração", " tu ", "tua ", "teu ", "Prove.", "Nunca mais", "sei lá", "vitalício".
  4. Zona segura 9:16: texto claro grande fora de x 140–940 / y 150–1500 (só aviso no vídeo, pois o celular pode passar).
  5. Formato: 1080x1920 (vídeo/story/TikTok) ou 1080x1350 (carrossel 4:5); duração 7–25s.
Saída: relatório no terminal e código de saída 1 se houver REPROVA.
"""
import json, os, re, shutil, subprocess, sys, tempfile
from PIL import Image, ImageFilter
import numpy as np

PROIBIDOS = ["demonstração", "demonstracao", " tu ", " tua ", " teu ", "prove.", "nunca mais", "sei lá", "vitalício", "vitalicio"]
AMARELOS = [(0xFF, 0xD4, 0x00), (0xF5, 0xB3, 0x00)]


def quadros(video, fps=4):
    d = tempfile.mkdtemp(prefix='rev_')
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', video, '-vf', f'fps={fps}', os.path.join(d, '%05d.png')], check=True)
    return d, sorted(os.path.join(d, f) for f in os.listdir(d))


def duracao(video):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', video], capture_output=True, text=True)
    try: return float(r.stdout.strip())
    except ValueError: return 0.0


def achar_celular(a):
    """Retorna (x0, y0, x1) aproximado da tela do celular, achando o relógio "9:41" da status bar via OCR."""
    if not shutil.which('tesseract'): return None
    img = Image.fromarray(a.astype(np.uint8))
    t = tempfile.mktemp(suffix='.png'); img.convert('L').save(t)
    r = subprocess.run(['tesseract', t, '-', '--psm', '11', 'tsv'], capture_output=True, text=True); os.remove(t)
    for ln in r.stdout.splitlines()[1:]:
        c = ln.split('\t')
        if len(c) >= 12 and re.fullmatch(r'9[:.;]?41', c[11].strip()):
            l, tp, w, h = map(int, c[6:10])
            cx = img.width // 2
            x0 = max(0, l - int(w * 1.6)); x1 = min(img.width - 1, 2 * cx - x0)
            return x0, max(0, tp - int(h * 1.3)), x1
    return None


def topo_celular(img):
    a = np.asarray(img.convert('RGB')).astype(np.int16)
    c = achar_celular(a)
    if not c: return None
    x0, y0, x1 = c; w = x1 - x0
    if w < 250: return None
    faixa = img.crop((x0, y0, x1, y0 + int(w * 0.14))).convert('L').resize((240, 34))
    return np.asarray(faixa).astype(np.int16)


def amarelo_frac(img):
    a = np.asarray(img.convert('RGB').resize((270, 480))).astype(np.int16)
    tot = 0
    for c in AMARELOS:
        tot += (np.abs(a - np.array(c)).sum(axis=2) < 60).mean()
    return tot


def ocr(img):
    if not shutil.which('tesseract'): return None
    t = tempfile.mktemp(suffix='.png'); img.convert('L').save(t)
    r = subprocess.run(['tesseract', t, '-', '-l', 'por'], capture_output=True, text=True)
    os.remove(t); return r.stdout.lower()


def texto_fora_zona(img):
    """Pixels brancos fortes (texto) fora da zona segura, ignorando a área do celular."""
    a = np.asarray(img.convert('RGB')).astype(np.int16)
    h, w, _ = a.shape
    if (w, h) != (1080, 1920): return 0.0
    branco = (a.min(axis=2) > 235)
    c = None
    fora = branco.copy(); fora[150:1500, 140:940] = False
    return fora.mean()


def revisar(caminho, roteiro_txt=''):
    erros, avisos = [], []
    ext = caminho.lower().rsplit('.', 1)[-1]
    if ext in ('mp4', 'mov', 'webm'):
        dur = duracao(caminho)
        if not (7 <= dur <= 25): erros.append(f'duração {dur:.1f}s fora de 7–25s')
        d, fs = quadros(caminho)
        ims = [Image.open(f) for f in fs]
        if ims and ims[0].size != (1080, 1920): erros.append(f'resolução {ims[0].size}, esperado 1080x1920')
        topos = [(i, topo_celular(im)) for i, im in enumerate(ims)]
        topos = [(i, t) for i, t in topos if t is not None]
        if len(topos) >= 2:
            ref = np.median(np.stack([t for _, t in topos]), axis=0)
            for i, t in topos:
                dif = np.abs(t - ref).mean()
                if dif > 18: erros.append(f'mockup/topo do celular diferente em {i/4:.2f}s (dif {dif:.1f}) — ilha/barra inconsistente')
        for i, im in enumerate(ims):
            fr = amarelo_frac(im)
            if fr > 0.002: erros.append(f'amarelo proibido em {i/4:.2f}s ({fr*100:.2f}% da tela)')
            fz = texto_fora_zona(im)
            if fz > 0.0015: avisos.append(f'texto fora da zona segura em {i/4:.2f}s ({fz*100:.2f}%)')
        txt = ''
        for im in ims[::4]:
            o = ocr(im)
            if o is None: break
            txt += ' ' + o
        shutil.rmtree(d, ignore_errors=True)
        n = len(ims)
    else:
        im = Image.open(caminho); n = 1
        if im.size not in ((1080, 1920), (1080, 1350)): erros.append(f'resolução {im.size}')
        fr = amarelo_frac(im)
        if fr > 0.002: erros.append(f'amarelo proibido ({fr*100:.2f}% da tela)')
        if im.size == (1080, 1920):
            fz = texto_fora_zona(im)
            if fz > 0.0015: avisos.append(f'texto fora da zona segura ({fz*100:.2f}%)')
        txt = ocr(im) or ''
    base = (' ' + (txt or '') + ' ' + roteiro_txt.lower() + ' ')
    for p in PROIBIDOS:
        if p in base: erros.append(f'texto proibido: "{p.strip()}"')
    if not shutil.which('tesseract') and not roteiro_txt:
        avisos.append('sem OCR e sem --roteiro: texto não foi verificado automaticamente')
    return dict(arquivo=caminho, quadros=n, erros=sorted(set(erros)), avisos=sorted(set(avisos))[:6],
                status='REPROVA' if erros else 'PASSA')


if __name__ == '__main__':
    args = sys.argv[1:]; rot = ''
    if '--roteiro' in args:
        i = args.index('--roteiro'); rot = open(args[i + 1], encoding='utf-8').read(); del args[i:i + 2]
    res = [revisar(a, rot) for a in args]
    falhou = False
    for r in res:
        print(f"{r['status']:8} {r['arquivo']}  ({r['quadros']} quadros)")
        for e in r['erros']: print('   ✗', e)
        for a in r['avisos']: print('   !', a)
        falhou |= r['status'] == 'REPROVA'
    sys.exit(1 if falhou else 0)
