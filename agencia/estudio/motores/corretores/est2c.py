#!/usr/bin/env python3
"""EST2-C · Quiz — refeito em 24/11. Um ângulo só: saber responder quando a negociação sai do básico.
Voz: HOOK1 ("se você quer ser o corretor que sabe responder quando a negociação sai do básico…") e os cartões mostram exatamente
perguntas de cliente fora do básico, entrando em "quando a negociação sai do básico"; respostas no Mapa durante o pt2
("…criado justamente para te preparar para os diferentes cenários…"); CTA 4de4.
Abre com cena de corretor e cliente (rostos de frente) + cartão; corta pro rosto dela quando ela já está de frente.
Uso: python3 est2c.py <saida.mp4>
"""
import sys
from motor import *
OUT = sys.argv[1] if len(sys.argv) > 1 else "EST2-C.mp4"
pc = Peca(OUT, leg_y_cta=240, preco_y=318, preco_wh=(400, 110), preco_fz=58)
A1 = 0.55
pc.fala(C4 + "hook1p1.mov", A1, 8.06, G_HOOK1_1, off=0.49, fim_ref=7.6)
H1 = pc.t
pc.fala(U + "aud/B_HOOK1_pt_2.wav", 0.50, 8.30, G_HOOK1_2, off=-6.855, fim_ref=15.4)
pc.fala(CTA4, 0.0, 6.30, G_CTA4, fim_ref=5.9, cta=True)
CT = pc.cta_ini
sr, qn = t_de(pc, "QUE SABE"), t_de(pc, "QUANDO A")
q = (H1 - qn) / 3
pf = t_de(pc, "PORQUE ELE", H1); r = (CT - pf) / 3
P1, P2, P3 = "Posso usar o FGTS na entrada?", "Quando eu pego as chaves?", "A avaliação muda a entrada?"
Q = quiz([(0, qn, "", "Você saberia responder?", False),
          (qn, qn + q, "1/3", P1, False), (qn + q, qn + 2 * q, "2/3", P2, False), (qn + 2 * q, H1, "3/3", P3, False),
          (H1, pf, "", "As 3 respostas estão no Mapa.", False),
          (pf, pf + r, "1/3", P1, True), (pf + r, pf + 2 * r, "2/3", P2, True), (pf + 2 * r, CT, "3/3", P3, True)])
pc.clipe(C4 + "sc_doc3.mp4", 0.2, sr, 1.04)             # abre com corretor e cliente de frente
pc.clipe(C4 + "hook1p1.mov", A1 + sr, H1 - sr)          # rosto dela, em sincronia com a fala
pc.clipe(C4 + "ip_quemfaz.mp4", 0.6, pf - H1, 1.03)
pc.clipe(C4 + "ip_fgts_pode.mp4", 2.0, r, 1.03, vel=0.8)
pc.clipe(C4 + "ip_chaves.mp4", 0.9, r, 1.03, vel=0.3)    # Quando pagar e pegar as chaves (iPad)
pc.clipe(C4 + "ip_avaliacao2.mp4", 0.3, CT - pf - 2 * r, 1.03)
pc.clipe(CTA4, 0.0, 6.30)
if __name__ == "__main__":
    render(pc, [Q])
