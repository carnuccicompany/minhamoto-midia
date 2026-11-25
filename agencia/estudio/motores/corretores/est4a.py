#!/usr/bin/env python3
"""EST4-A · Split-screen — piloto portado pro motor e corrigido em 24/11: legenda fora da divisória (y 1440), tudo em x 140–940,
chips "“Vou confirmar e te aviso.”" × "Você responde na hora, com o Mapa." colados na divisória, cenas sem o "olhando pro teto"
e sem o casal no sofá, página impressa inteira, CTA 4de4, áudio 48 kHz com crossfade. Voz: HOOK1 pt1+pt2.
Uso: python3 est4a.py <saida.mp4>
"""
import sys
from motor import *
OUT = sys.argv[1] if len(sys.argv) > 1 else "EST4-A.mp4"
pc = Peca(OUT)
pc.fala(U + "aud/B_HOOK1_pt_1.wav", 0.55, 8.06, G_HOOK1_1, off=0.49, fim_ref=7.6)
H1 = pc.t
pc.fala(U + "aud/B_HOOK1_pt_2.wav", 0.50, 8.30, G_HOOK1_2, off=-6.855, fim_ref=15.4)
pc.fala(CTA4, 0.0, 6.30, G_CTA4, fim_ref=5.9, cta=True)
CT = pc.cta_ini
s = H1 / 3   # (arquivo, início, duração, y do recorte 1080x960)
pc.split([(C4 + "sc_ap2.mp4", 0.3, s, 450), (C4 + "sc_maos_pasta.mp4", 0.0, s, 700), (C4 + "sc_vendo.mp4", 0.5, s + 0.1, 250)],
         [(C4 + "ip_fgts_pode.mp4", 1.0, s, 480), (C4 + "sc_doc3.mp4", 4.4, s, 250), (C4 + "sc_feliz.mp4", 0.8, s + 0.1, 430)],
         H1, "“Vou confirmar e te aviso.”", "Você responde na hora, com o Mapa.")
m = (CT - H1) / 3
pc.clipe(C4 + "ip_chaves.mp4", 0.7, m, 1.03, vel=0.3)          # Quando pagar e pegar as chaves
pc.clipe(C4 + "ip_perguntas.mp4", 0.2, 2.6, 1.03)               # Perguntas ao banco
pc.clipe(C4 + "ip_somar.mp4", 0.0, CT - H1 - m - 1.05 - 2.6, 1.03) # Somar renda ajuda sempre?
pc.clipe(PAG_CONSORCIO, 0, 1.05, 0.90)   # Consórcio não é financiamento (página inteira, as duas margens)
pc.clipe(CTA4, 0.0, 6.30)
if __name__ == "__main__":
    render(pc)
