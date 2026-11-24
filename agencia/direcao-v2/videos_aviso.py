#!/usr/bin/env python3
"""A1 e B1 com a frase do aviso que o app cumpre (D-20261124-produto-2).
Só muda o texto da cena do aviso; telas, ritmo, CTA e preço são os de videos.py.
Frases aprovadas: 'O app lembra a troca pelo seu km.' / 'Avisa quando a troca estiver chegando, pela sua média de uso.'
Uso: python3 videos_aviso.py A1|B1 [prev]  ->  A/A1/video-aviso.mp4 e B/B1/video-aviso.mp4 (os originais não são tocados)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import videos
from motor import *

def _troca(v, t0, t1, novo):
    v.textos = [x for x in v.textos if not (x[0] == t0 and x[1] == t1)]
    v.texto(t0, t1, novo)

def A1():
    v = videos.A1()
    _troca(v, 13.2, 16.2, T_cap('O app lembra a troca / pelo seu km.', ['km.'], y=165, tam=64, ritmo=0.15))
    return v

def B1():
    v = videos.B1()
    _troca(v, 10.8, 14.0, T_tit(['Avisa quando a troca', 'estiver chegando,', 'pela sua média de uso.'], y=170, tam=62, hl_linhas=(1,)))
    return v

if __name__ == '__main__':
    vid = sys.argv[1]; modo = sys.argv[2] if len(sys.argv) > 2 else 'full'
    v = dict(A1=A1, B1=B1)[vid]()
    pasta = os.path.join(os.path.dirname(os.path.abspath(__file__)), vid[0], vid)
    if modo == 'prev':
        d = v.render(None, so_frames=[int(x*FPS) for x in ([15.0] if vid == 'A1' else [12.5])])
        print(d)
    else:
        v.render(os.path.join(pasta, 'video-aviso.mp4')); print('render ok', pasta)
