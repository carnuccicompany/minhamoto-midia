#!/usr/bin/env python3
"""Recorta cards da UI do app (telas-app/rolagem) pra usar como 'print flutuante' nos carrosséis.
Detecta automaticamente as bordas do card e a primeira linha divisória (cabeçalho)."""
import os, sys
import numpy as np
from PIL import Image

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
TELAS = os.path.join(REPO, 'agencia', 'designer', 'assets', 'telas-app')
CACHE = '/tmp/estudio-recortes'

def cards(nome):
    im = np.array(Image.open(os.path.join(TELAS, nome)).convert('RGB')).astype(int)
    col = im[:, 90, :].sum(1); bg = im[:, 5, :].sum(1)
    dentro = abs(col - bg) > 6
    runs, s = [], None
    for y, v in enumerate(dentro):
        if v and s is None: s = y
        if not v and s is not None:
            if y - s > 150: runs.append((s, y))
            s = None
    return im, runs

def divisoria(im, a, b):
    sub = im[a:b, 200:1000].sum(2)
    for i in range(60, b - a - 3):
        r = sub[i]
        if r.std() < 7 and 60 < r.mean() < 140 and abs(sub[i - 4].mean() - r.mean()) > 20:
            return a + i
    return None

def recorte(nome, idx, so_cabecalho=False):
    im, runs = cards(nome)
    a, b = runs[idx]
    if so_cabecalho:
        d = divisoria(im, a, b); b = d - 1 if d else a + 176
    os.makedirs(CACHE, exist_ok=True)
    out = os.path.join(CACHE, f"{os.path.basename(nome)[:-4]}_{idx}{'_cab' if so_cabecalho else ''}.png")
    Image.open(os.path.join(TELAS, nome)).convert('RGB').crop((48, a, 1131, b)).save(out)
    return out, (1083, b - a)

if __name__ == '__main__':
    im, runs = cards(sys.argv[1]); print(runs)

def divisorias(im, a, b):
    sub = im[a:b, 200:1000].sum(2); out = []
    for i in range(60, b - a - 3):
        r = sub[i]
        if r.std() < 7 and 60 < r.mean() < 140 and abs(sub[i - 4].mean() - r.mean()) > 20 and (not out or a + i - out[-1] > 10):
            out.append(a + i)
    return out

def trecho(nome, idx, secoes=(0, 2)):
    """Monta um card só com as seções pedidas (0 = cabeçalho, 1 = 'O que significa', 2 = 'O que fazer', 3 = 'Quando ir à oficina'),
    na ordem, como se o card tivesse só elas. Devolve (arquivo, (w, h))."""
    im, runs = cards(nome); a, b = runs[idx]
    d = divisorias(im, a, b)
    limites = [a] + d                       # seção k vai de limites[k] até limites[k+1]
    src = Image.open(os.path.join(TELAS, nome)).convert('RGB')
    partes = []
    for j, k in enumerate(secoes):
        y0 = limites[k] + (0 if k == 0 else 3)
        y1 = limites[k + 1] + (3 if j < len(secoes) - 1 else -1)   # mantém a linha divisória entre seções; tira a borda no fim
        partes.append(src.crop((48, y0, 1131, y1)))
    H = sum(p.size[1] for p in partes) + 18
    out = Image.new('RGB', (1083, H), partes[-1].getpixel((540, partes[-1].size[1] - 6)))
    y = 0
    for p in partes: out.paste(p, (0, y)); y += p.size[1]
    os.makedirs(CACHE, exist_ok=True)
    arq = os.path.join(CACHE, f"{os.path.basename(nome)[:-4]}_{idx}_{'-'.join(map(str, secoes))}.png")
    out.save(arq)
    return arq, out.size

def destaque(nome, idx, foco=2, fator=0.32):
    """Card inteiro do app, com o cabeçalho e a seção 'foco' acesos e as outras seções apagadas (fator de brilho).
    Faz o olho ir direto no que importa sem mexer no layout real do app."""
    from PIL import ImageEnhance
    im, runs = cards(nome); a, b = runs[idx]
    d = divisorias(im, a, b); lim = [a] + d
    src = Image.open(os.path.join(TELAS, nome)).convert('RGB').crop((48, a, 1131, b))
    for k in range(1, len(lim) - 1):
        if k == foco: continue
        y0, y1 = lim[k] - a + 4, lim[k + 1] - a - 1
        faixa = src.crop((0, y0, src.size[0], y1))
        src.paste(ImageEnhance.Brightness(faixa).enhance(fator), (0, y0))
    os.makedirs(CACHE, exist_ok=True)
    arq = os.path.join(CACHE, f"{os.path.basename(nome)[:-4]}_{idx}_foco{foco}.png")
    src.save(arq); return arq, src.size
