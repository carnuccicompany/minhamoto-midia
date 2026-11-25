#!/usr/bin/env python3
"""EST5-B · Historinha — refeito em 24/11. Um ângulo só: a venda que estava praticamente fechada e morreu no processo (perda).
Voz: HOOK2 ("se você é corretor e entende que ainda não domina os diferentes tipos de aquisição de imóvel, dá uma olhada nesse material aqui")
e o texto conta a mesma coisa: proposta aceita → cliente quis usar o consórcio → o corretor travou → a venda morreu.
Corpo do AP DD 2 com as páginas casadas com cada tema, CTA 4de4. Uso: python3 est5b.py <saida.mp4>
"""
import sys
from motor import *
OUT = sys.argv[1] if len(sys.argv) > 1 else "EST5-B.mp4"
pc = Peca(OUT)
pc.fala(U + "aud/B_HOOK2_completo.wav", 0.05, 7.45, G_HOOK2, off=0.0, fim_ref=7.2)
H = pc.t; DA = t_de(pc, "DÁ UMA")
pc.fala(BODY, 1.13, 10.40, G_BODY, fim_ref=10.08)
r1, r2, r3, r4 = (t_de(pc, x, H) for x in ("SOBRE FGTS", "MINHA CASA", "CONSÓRCIO", "DOCUMENTAÇÃO"))
pc.fala(CTA4, 0.0, 6.30, G_CTA4, fim_ref=5.9, cta=True)
CT = pc.cta_ini
c1, c2, c3 = DA * 0.23, DA * 0.55, DA * 0.78        # o cartão de 2 linhas fica mais tempo na tela
pc.clipe(C4 + "sc_doc3.mp4", 0.2, c1, 1.04)            # proposta aceita (rostos de frente)
pc.clipe(C4 + "sc_ap2.mp4", 0.3, c2 - c1, 1.05)        # o cliente quis usar o consórcio
pc.clipe(C4 + "sc_maos_tensas.mp4", 0.0, c3 - c2, 1.02, vel=0.9)   # o corretor travou (mãos tensas na mesa, sem resposta)
pc.clipe(C4 + "sc_duvida.mp4", 0.6, DA - c3, 1.04)     # a venda morreu (cliente com a mão na cabeça)
i = (r1 - DA) / 3
pc.clipe(C4 + "ip_quemfaz.mp4", 0.6, i, 1.03)         # "dá uma olhada nesse material aqui"
pc.clipe(C4 + "ip_usado.mp4", 0.5, i, 1.03)           # "São +120 mapas visuais,"
pc.clipe(C4 + "ip_parcelar.mp4", 0.4, r1 - DA - 2 * i, 1.03)   # "claros e objetivos,"
pc.clipe(C4 + "ip_fgts_pode.mp4", 2.1, r2 - r1, 1.03)      # FGTS
pc.clipe(C4 + "ip_faixas2.mp4", 0.0, r3 - r2, 1.03)        # Minha Casa Minha Vida
pc.clipe(PAG_CONSORCIO, 0, r4 - r3, 0.90)  # consórcio (página inteira)
pc.clipe(C4 + "ip_matricula.mp4", 0.9, CT - r4, 1.03)      # documentação
pc.clipe(CTA4, 0.0, 6.30)
HIST = historia([(0, c1, "Proposta aceita."), (c1, c2, "O cliente quis usar\no consórcio."),
                 (c2, c3, "O corretor travou."), (c3, DA, "E a venda morreu.")])
if __name__ == "__main__":
    render(pc, [HIST])
