#!/usr/bin/env python3
"""EST2-B · Quiz "Você domina esses 4 temas?" — corrigido em 24/11: abre com ela de frente (0,37 s), consórcio em página inteira,
cartão do meio troca de texto (não fica 6 s parado), crossfade + som ambiente, CTA 4de4. Uso: python3 est2b.py <saida.mp4>
"""
import sys
from motor import *
OUT = sys.argv[1] if len(sys.argv) > 1 else "EST2-B.mp4"
pc = Peca(OUT, leg_y_cta=240, preco_y=318, preco_wh=(400, 110), preco_fz=58)
pc.fala(C4 + "hook3.mov", 0.37, 10.0, G_HOOK3, off=0.333, fim_ref=9.5)
H = pc.t
pc.fala(BODY, 1.13, 10.40, G_BODY, fim_ref=10.08)
pc.fala(CTA4, 0.0, 6.30, G_CTA4, fim_ref=5.9, cta=True)
CT = pc.cta_ini
f1, f2, f3, f4, da = (t_de(pc, x) for x in ("FGTS", "MINHA CASA", "CONSÓRCIO", "DOCUMENTAÇÃO", "DÁ UMA"))
r1, r2, r3, r4 = (t_de(pc, x, H) for x in ("SOBRE FGTS", "MINHA CASA", "CONSÓRCIO", "DOCUMENTAÇÃO"))
Q = quiz([(0, f1, "", "Você domina esses 4 temas?", False),
          (f1, f2, "1/4", "FGTS", False), (f2, f3, "2/4", "Minha Casa Minha Vida", False),
          (f3, f4, "3/4", "Consórcio", False), (f4, da, "4/4", "Documentação", False),
          (da, H, "", "Os 4 estão no Mapa.", False), (H, r1, "", "Veja cada um:", False),
          (r1, r2, "1/4", "FGTS", True), (r2, r3, "2/4", "Minha Casa Minha Vida", True),
          (r3, r4, "3/4", "Consórcio", True), (r4, CT, "4/4", "Documentação", True)])
pc.clipe(C4 + "hook3.mov", 0.37, H)
i1 = (r1 - H) / 2
pc.clipe(C4 + "ip_quemfaz.mp4", 0.6, i1, 1.03)
pc.clipe(C4 + "ip_perguntas.mp4", 0.4, r1 - H - i1, 1.03)
pc.clipe(C4 + "ip_fgts_pode.mp4", 2.2, r2 - r1, 1.03)
pc.clipe(C4 + "ip_faixas2.mp4", 0.0, r3 - r2, 1.03)
pc.clipe(PAG_CONSORCIO + ":360:600", 0, r4 - r3, 0.90)   # tablet menor e mais baixo: o cartão do quiz não cobre o título
pc.clipe(C4 + "ip_matricula.mp4", 0.9, CT - r4, 1.03)
pc.clipe(CTA4, 0.0, 6.30)
if __name__ == "__main__":
    render(pc, [Q])
