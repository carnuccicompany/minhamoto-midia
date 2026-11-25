#!/usr/bin/env python3
"""EST4-C · Split-screen — refeito em 24/11. Ângulo: depender menos de terceiros, ENTENDENDO o processo (sem opor correspondente
× corretor e sem prometer que o corretor faz o trabalho técnico). Chips "Depende de terceiros a cada dúvida" × "Você entende cada
etapa do processo". Voz: HOOK2 ("…ainda não domina os diferentes tipos de aquisição…") + corpo do AP DD 2 com a página certa em
cada tema (consórcio → "Consórcio não é financiamento"; documentação → "Leia a matrícula"). CTA 4de4.
Uso: python3 est4c.py <saida.mp4>
"""
import sys
from motor import *
OUT = sys.argv[1] if len(sys.argv) > 1 else "EST4-C.mp4"
pc = Peca(OUT)
pc.fala(U + "aud/B_HOOK2_completo.wav", 0.05, 7.45, G_HOOK2, off=0.0, fim_ref=7.2)
H = pc.t; DA = t_de(pc, "DÁ UMA")
pc.fala(BODY, 1.13, 10.40, G_BODY, fim_ref=10.08)
b2, r1, r2, r3, r4 = (t_de(pc, x, H) for x in ("CLAROS", "SOBRE FGTS", "MINHA CASA", "CONSÓRCIO", "DOCUMENTAÇÃO"))
pc.fala(CTA4, 0.0, 6.30, G_CTA4, fim_ref=5.9, cta=True)
CT = pc.cta_ini
s = DA / 2
pc.split([(C4 + "sc_ap2.mp4", 0.3, s, 450), (C4 + "sc_duvida.mp4", 1.5, s + 0.1, 260)],
         [(C4 + "ip_itbi.mp4", 0.0, s, 650), (C4 + "sc_doc3.mp4", 4.4, s + 0.1, 250)],
         DA, "Depende de terceiros a cada dúvida", "Você entende cada etapa do processo")
pc.clipe(C4 + "ip_usado.mp4", 0.5, H - DA, 1.03)            # "dá uma olhada nesse material aqui"
pc.clipe(C4 + "ip_parcelar.mp4", 0.4, b2 - H, 1.03)         # "São +120 mapas visuais,"
pc.clipe(PAG_PLANTA, 0, r1 - b2, 0.90)   # "claros e objetivos," (página inteira, as duas margens)
pc.clipe(C4 + "ip_onde_fgts.mp4", 0.3, r2 - r1, 1.03)       # FGTS
pc.clipe(C4 + "ip_faixas2.mp4", 0.2, r3 - r2, 1.03)         # Minha Casa Minha Vida
pc.clipe(PAG_CONSORCIO, 0, r4 - r3, 0.90)   # consórcio (página inteira, as duas margens)
pc.clipe(C4 + "ip_matricula.mp4", 0.9, CT - r4, 1.03)       # documentação
pc.clipe(CTA4, 0.0, 6.30)
if __name__ == "__main__":
    render(pc)
