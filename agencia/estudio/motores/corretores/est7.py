#!/usr/bin/env python3
"""EST7 · Folheando o Mapa com a Ana Paula narrando — piloto A, v2 (24/11, correções da revisão 4d).
Voz só dela: HOOK2 (bruto; rosto dela no começo e depois num círculo enquanto o Mapa é folheado página a página, páginas reais dos
tipos de aquisição inteiras: carta contemplada, consórcio, na planta, o que muda até as chaves) → corpo do Dia 2 (gravação limpa, com EQ pra casar com o take de câmera):
"Cada mapa mostra de forma clara quem participa do processo, quais documentos entram e em que ordem as etapas acontecem", com as
páginas certas do PDF passando inteiras num tablet (sem páginas fantasma) → CTA 4de4 + R$27,90.
Ângulo (ganho): saber o caminho inteiro depois do sim (quem, que documento, que ordem) e conduzir sem travar.
Uso: python3 est7.py <saida.mp4>
"""
import sys
from motor_novo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else "EST7-A.mp4"
pc = Peca(OUT, leg_y=1290, leg_y_cta=330, preco_y=430)
H2, PD = C5 + "hook2.mov", C5 + "pagdet.mp4"
pc.fala(H2, 0.05, 7.30, G_HOOK2, off=0.0, fim_ref=7.2)
legenda_desde_zero(pc)
H = pc.t
pc.silencio(0.10)
B1 = pc.t
pc.fala(GRAV, 29.36, 36.15, alinhar_grav(L4_DIA2, 29.36, 36.15), fim_ref=36.11, prender=False)
pc.silencio(0.15)
pc.fala(CTA4, 0.0, 6.05, G_CTA4N, fim_ref=6.0, cta=True)
qp, qd, qo = t_de(pc, "QUEM PARTICIPA"), t_de(pc, "QUAIS DOCUMENTOS"), t_de(pc, "E EM QUE")
CORTE = 1.75
pc.leg_y_trechos = [(CORTE, B1, 1210), (B1, pc.cta_ini, 1415)]   # legenda abaixo do caderno / do tablet
pc.eq = {GRAV: eq_grav("est7")}                     # EQ por faixa: a gravação do Dia 2 casa com o CTA4 (±3 dB por faixa)

CORTE = 1.75
pc.clipe(H2, 0.05, CORTE)                                  # ela pra câmera: "Se você é corretor e entende…"
# o Mapa folheado página a página (páginas reais do PDF, sempre inteiras, viradas uma a uma)
FOL = [(CORTE, 65), (CORTE + 1.35, 66), (CORTE + 2.75, 67), (CORTE + 4.15, 68)]   # carta contemplada → consórcio → na planta → o que muda até as chaves
pc.motion(folheia(FOL, fundo_mesa(PD, 2.5), larg=700, cy=650), B1 - CORTE)
pc.motion(tablet([(B1, 4), (qp, 12), (qd, 75), (qo, 105)], fundo_mesa(PD, 2.5)), pc.cta_ini - B1)
pc.clipe(CTA4, 0.0, 6.05)

def gancho(img, t):    # texto de gancho desde o 1º quadro
    if t < CORTE: pilula_ajusta(img, 175, "Você domina os tipos de aquisição?", (255, 255, 255), cor=NAVY, fz=52)
CARAS = [(0, 367, 713), (0.5, 540, 734), (1, 518, 756), (1.5, 562, 734), (2, 648, 799), (2.5, 562, 778), (3, 475, 713), (3.5, 518, 713),
         (4, 562, 713), (4.5, 518, 713), (5, 454, 756), (5.5, 562, 778), (6, 648, 691), (6.5, 583, 691), (7, 540, 682), (7.5, 540, 682)]
PP = PIP(H2, 0.05 + CORTE, CORTE, H, CARAS, cx=540, cy=1388, d=220, lado=600)   # embaixo do caderno, sem cobrir a página
if __name__ == "__main__":
    render(pc, [gancho, PP])
