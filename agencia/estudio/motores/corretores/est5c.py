#!/usr/bin/env python3
"""EST5-C · Historinha — corrigido em 24/11. Ângulo: quanto dinheiro você já perdeu por não saber responder uma dúvida.
Abre com a manchete "Quanto você já perdeu por uma dúvida?"; cena de hesitação no "O corretor travou."; CTA 4de4.
Voz: HOOK3 + trecho do corpo do AP DD 2. Uso: python3 est5c.py <saida.mp4>
"""
import sys
from motor import *
OUT = sys.argv[1] if len(sys.argv) > 1 else "EST5-C.mp4"
pc = Peca(OUT)
pc.fala(U + "aud/B_HOOK3_completo.wav", 0.37, 10.0, G_HOOK3, off=0.333, fim_ref=9.5)
H = pc.t; DA = t_de(pc, "DÁ UMA")
# "São +120 mapas visuais, claros e objetivos" — termina dentro da pausa real (5,46–5,76 s), sem vírgula na legenda.
# (Não vai até "documentação." de propósito: aí o áudio ficaria idêntico ao do EST2-B.)
pc.fala(BODY, 1.13, 5.64, G_BODY[:2] + [("CLAROS E OBJETIVOS.", 3.6)], fim_ref=5.46)
B1 = pc.t
pc.fala(CTA4, 0.0, 6.30, G_CTA4, fim_ref=5.9, cta=True)
CT = pc.cta_ini
d = DA / 4
pc.clipe(C4 + "sc_doc4.mp4", 0.3, d, 1.04)
pc.clipe(C4 + "sc_vendo.mp4", 2.0, d, 1.05)
pc.clipe(C4 + "sc_duv_corretor2.mp4", 0.4, d, 1.04)   # corretor parado, de costas, com o papel e sem resposta
pc.clipe(C4 + "sc_feliz.mp4", 0.4, DA - 3 * d, 1.05)
pc.clipe(C4 + "ip_fgts_pode.mp4", 1.85, H - DA, 1.03, vel=0.8)  # "dá uma olhada nesse material aqui" → O FGTS PODE
f = (CT - H) / 2
pc.clipe(C4 + "ip_fgts_nao.mp4", 0.2, f, 1.03)             # "São +120 mapas visuais,"
pc.clipe(C4 + "ip_somar.mp4", 0.0, CT - H - f, 1.03)       # "claros e objetivos."
pc.clipe(CTA4, 0.0, 6.30)
HIST = historia([(0, d, "Quanto você já perdeu\npor uma dúvida?"), (d, 2 * d, "O cliente perguntou:\n“Posso usar o FGTS?”"),
                 (2 * d, 3 * d, "O corretor travou."), (3 * d, DA, "Fechou com outro\ncorretor.")])
if __name__ == "__main__":
    render(pc, [HIST])
