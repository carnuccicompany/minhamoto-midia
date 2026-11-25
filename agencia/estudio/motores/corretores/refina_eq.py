#!/usr/bin/env python3
"""Refina o EQ da Gravação Dia 2 medindo a peça FINAL (método ltas do revisor): soma em cada faixa a diferença CTA − corpo.
Uso: python3 refina_eq.py est10 <mp4> <corpo_a> <corpo_b> <cta_a> <cta_b>"""
import sys, json, re, numpy as np
from fit_eq import perfil, fq
nome, mp4 = sys.argv[1], sys.argv[2]; a, b, c, d = map(float, sys.argv[3:7])
e = json.load(open("novo/eq_grav.json"))
g = np.array([float(x) for x in re.findall(r"entry\((\d+),(-?[\d.]+)\)", e[nome]) and [v for k, v in re.findall(r"entry\((\d+),(-?[\d.]+)\)", e[nome])][1:9]])
dif = perfil(mp4, c, d) - perfil(mp4, a, b)
print(nome, "dif antes", dif.round(1))
g = g + 0.6 * np.sign(dif) * np.maximum(0, np.abs(dif) - 1.5)
e[nome] = fq(g); json.dump(e, open("novo/eq_grav.json", "w"), indent=1); print("novos ganhos", g.round(1))
