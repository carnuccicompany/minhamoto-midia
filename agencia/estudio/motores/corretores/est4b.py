#!/usr/bin/env python3
"""EST4-B · Split-screen "o cliente percebe quando o corretor não domina o processo" — corrigido em 24/11:
legenda fora da divisória (y 1440), chips colados na divisória (não cobrem rosto), recortes com cabeça inteira,
cenas sem o casal no sofá / olhando pro teto, página impressa inteira, crossfade + som ambiente, CTA 4de4. Voz: HOOK5 pt1+pt2.
Uso: python3 est4b.py <saida.mp4>
"""
import sys
from motor import *
OUT = sys.argv[1] if len(sys.argv) > 1 else "EST4-B.mp4"
pc = Peca(OUT)
pc.fala(U + "aud/B_HOOK5_pt_1.wav", 0.45, 8.25, G_HOOK5_1, off=0.51, fim_ref=7.95)
H1 = pc.t
pc.fala(U + "aud/B_HOOK5_pt_2.wav", 0.40, 7.95, G_HOOK5_2, off=-7.43, fim_ref=15.1)
pc.fala(CTA4, 0.0, 6.30, G_CTA4, fim_ref=5.9, cta=True)
CT = pc.cta_ini
s = H1 / 3
pc.split([(C4 + "sc_casal_duvida.mp4", 1.8, s, 150, 0.65), (C4 + "sc_casal_duvida.mp4", 1.8 + s * 0.65, s, 150, 0.65), (C4 + "sc_ap2.mp4", 0.2, s + 0.1, 450)],   # casal com a mão na cabeça, em câmera lenta (só o trecho da dúvida)
         [(C4 + "ip_quemfaz.mp4", 0.3, s, 950), (C4 + "sc_ap3.mp4", 0.2, s, 450), (C4 + "sc_doc4.mp4", 2.4, s + 0.1, 530)],
         H1, "O cliente percebe a dúvida.", "O cliente sente segurança.")
m = (CT - H1) / 3
pc.clipe(PAG_PLANTA, 0, m, 0.90)
pc.clipe(C4 + "ip_perguntas.mp4", 0.4, m, 1.03)
pc.clipe(C4 + "ip_afirmar.mp4", 0.5, CT - H1 - 2 * m, 1.03)
pc.clipe(CTA4, 0.0, 6.30)
if __name__ == "__main__":
    render(pc)
