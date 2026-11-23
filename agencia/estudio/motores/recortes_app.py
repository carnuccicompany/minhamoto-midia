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
