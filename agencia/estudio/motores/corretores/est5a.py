#!/usr/bin/env python3
"""EST5-A · Historinha — refeito em 24/11 (revisão independente). Um ângulo só: CONFIANÇA (ganho).
Voz: HOOK5 pt1 ("quanto mais você entende a operação… mais segurança você consegue passar pro seu cliente na hora do fechamento")
e o texto conta exatamente isso: o cliente perguntou → você explicou cada etapa → ele sentiu segurança → fechou com você.
pt2 sobre o material, CTA 4de4. Uso: python3 est5a.py <saida.mp4>
"""
import sys
from motor import *
OUT = sys.argv[1] if len(sys.argv) > 1 else "EST5-A.mp4"
pc = Peca(OUT)
pc.fala(U + "aud/B_HOOK5_pt_1.wav", 0.45, 8.25, G_HOOK5_1, off=0.51, fim_ref=7.95)
H1 = pc.t
pc.fala(U + "aud/B_HOOK5_pt_2.wav", 0.40, 7.95, G_HOOK5_2, off=-7.43, fim_ref=15.1)
H2 = pc.t
pc.fala(CTA4, 0.0, 6.30, G_CTA4, fim_ref=5.9, cta=True)
CT = pc.cta_ini
d = H1 / 4
pc.clipe(C4 + "sc_vendo.mp4", 1.0, d, 1.05)          # cliente pergunta (casal lendo com o corretor)
pc.clipe(C4 + "sc_doc3.mp4", 0.3, d, 1.05)           # corretor explicando o documento
pc.clipe(C4 + "sc_doc4.mp4", 2.4, d, 1.05)           # clientes sorrindo, seguros
pc.clipe(C4 + "sc_doc3.mp4", 5.0, H1 - 3 * d, 1.04)  # aperto de mão → abraço
m = (CT - H1) / 3
pc.clipe(C4 + "ip_24h.mp4", 0.6, m, 1.03)
pc.clipe(C4 + "ip_itbi.mp4", 0.0, m, 1.03)
pc.clipe(C4 + "ip_afirmar.mp4", 0.5, CT - H1 - 2 * m, 1.03)
pc.clipe(CTA4, 0.0, 6.30)
HIST = historia([(0, d, "O cliente perguntou\nsobre o FGTS."), (d, 2 * d, "Você explicou\ncada etapa."),
                 (2 * d, 3 * d, "Ele sentiu\nsegurança."), (3 * d, H1, "E fechou com você.")])
if __name__ == "__main__":
    render(pc, [HIST])
