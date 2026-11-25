#!/usr/bin/env python3
"""EST2-A · Quiz "você saberia responder?" — piloto portado pro motor e corrigido em 24/11.
Cartão e legenda dentro de x 140–940; quebras "E DIZER PRA ELE | QUANTO QUE ELE | CONSEGUE FINANCIAR,"; HOOK4 cortado em 11,45 s
(antes do "que eu preparei", que o piloto deixava escapar); emendas com crossfade + som ambiente; CTA 4de4 com "SAIBA MAIS" inteiro.
Uso: python3 est2a.py <saida.mp4>
"""
import sys
from motor import *
OUT = sys.argv[1] if len(sys.argv) > 1 else "EST2-A.mp4"
C2 = U + "cortes2/"
pc = Peca(OUT, leg_y_cta=240, preco_y=318, preco_wh=(400, 110), preco_fz=58)
pc.fala(C4 + "hook4p.mov", 0.45, 11.45, G_HOOK4, off=0.45, fim_ref=11.0)
H = pc.t
pc.fala(BODY, 1.13, 10.40, G_BODY, fim_ref=10.08)
pc.fala(CTA4, 0.0, 6.30, G_CTA4, fim_ref=5.9, cta=True)
CT = pc.cta_ini
q1, q2, q3, sn = (t_de(pc, x) for x in ("QUANTO QUE ELE", "QUAL O VALOR", "E QUANTO QUE", "SE NÃO"))
a0 = H + 1.0; a = (CT - a0) / 3
Q = quiz([(0, q1, "", "Você saberia responder?", False),
          (q1, q2, "1/3", "Quanto ele consegue financiar?", False), (q2, q3, "2/3", "Qual o valor do imóvel?", False),
          (q3, sn, "3/3", "Quanto vai dar de entrada?", False), (sn, a0, "", "As 3 respostas estão no Mapa.", False),
          (a0, a0 + a, "1/3", "Quanto ele consegue financiar?", True), (a0 + a, a0 + 2 * a, "2/3", "Qual o valor do imóvel?", True),
          (a0 + 2 * a, CT, "3/3", "Quanto vai dar de entrada?", True)])
pc.clipe(C4 + "hook4p.mov", 0.45, H)   # recorte com pan: rosto dentro da zona desde o 1º quadro
pc.clipe(C2 + "ipad_intro.mp4", 0.3, 1.0, 1.03)
pc.clipe(C2 + "ipad_renda_cabe.mp4", 0.5, a, 1.03)     # Faixas de renda urbana
pc.clipe(C2 + "q2_renda_cabe.mp4", 1.2, a, 1.03)       # Renda e imóvel cabem?
pc.clipe(C2 + "q3_avaliacao.mp4", 0.9, CT - a0 - 2 * a, 1.03, vel=0.75)   # Avaliação muda a entrada
pc.clipe(CTA4, 0.0, 6.30)
if __name__ == "__main__":
    render(pc, [Q])
