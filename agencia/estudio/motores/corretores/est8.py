#!/usr/bin/env python3
"""EST8 · Antes × depois do corretor (sequencial) — piloto A, v2 (24/11, correções da revisão 4d).
ANTES: o corretor que trava (cenas de banco) enquanto ela diz o HOOK3 ("Você, corretor que sente que ainda não domina assuntos como
FGTS, Minha Casa Minha Vida, consórcio, documentação"); cada tema aparece com "?" na hora que ela fala.
Virada no "dá uma olhada nesse material aqui" (painel DEPOIS) → DEPOIS: corpo do Dia 2 (gravação limpa): "Assim, quando surgir uma
dúvida durante o atendimento, você consegue consultar o tema correspondente e entender o processo de forma visual, organizada e fácil
de aplicar na sua rotina", os mesmos 4 temas viram ✓ → CTA 4de4 + R$27,90. Voz só dela. ANTES sem cor, DEPOIS colorido; páginas do PDF inteiras num tablet.
Ângulo (ganho): responder qualquer pergunta do cliente na hora (confiança).
Uso: python3 est8.py <saida.mp4>
"""
import sys
from motor_novo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else "EST8-A.mp4"
pc = Peca(OUT, leg_y=1290, leg_y_cta=330, preco_y=430)
H3, PD = C4 + "hook3.mov", C5 + "pagdet.mp4"
pc.fala(H3, 0.25, 9.75, G_HOOK3, off=0.333, fim_ref=9.5)
legenda_desde_zero(pc)
H = pc.t
pc.silencio(0.10)
G0 = pc.t
pc.fala(GRAV, 36.78, 47.05, alinhar_grav(L5_DIA2, 36.78, 47.05), fim_ref=47.0, prender=False)
pc.silencio(0.15)
pc.fala(CTA4, 0.0, 6.05, G_CTA4N, fim_ref=6.0, cta=True)

f1, f2, f3, f4, DA = (t_de(pc, x) for x in ("FGTS", "MINHA CASA", "CONSÓRCIO", "DOCUMENTAÇÃO", "DÁ UMA"))
vc, ee, fac = t_de(pc, "VOCÊ CONSEGUE"), t_de(pc, "E ENTENDER"), t_de(pc, "ORGANIZADA")
pc.leg_y_trechos = [(vc, ee, 1415)]                     # com o tablet na tela, legenda abaixo dele
pc.leg_oculta = [(DA - 0.25, DA + 0.08)]                # nada de legenda por cima da cortina DEPOIS
pc.eq = {GRAV: eq_grav("est8")}                         # EQ por faixa (±3 dB do CTA4)

# ---- vídeo ---- ANTES sem cor (cliente perguntando → casal desconfiado); DEPOIS colorido
a1 = 3.6
pc.clipe(C5 + "ap1.mp4", 1.0, a1, 1.10, 1.0, cinza)               # o casal pergunta, o corretor não tem a resposta
pc.clipe(C5 + "duvida.mp4", 6.0, DA - a1, 1.04, 1.0, cinza)       # o casal desconfiado
pc.motion(folheia([(DA, 65), (DA + 1.0, 66)], fundo_mesa(PD, 2.5), larg=700, cy=650), H + 0.10 - DA)   # "dá uma olhada nesse material aqui" → o Mapa folheado (páginas inteiras)
pc.clipe(C4 + "sc_ap2.mp4", 0.2, vc - (H + 0.10), 1.04)           # "quando surgir uma dúvida durante o atendimento"
pc.motion(tablet([(vc, 53), (vc + (ee - vc) * 0.55, 49)], fundo_mesa(PD, 2.5)), ee - vc)   # "consulta o tema" → O FGTS PODE… / ONDE O FGTS ENTRA?
pc.clipe(U + "cortes3/doc3.mp4", 1.0, fac - ee, 1.04)             # "e entender o processo de forma visual"
pc.clipe(U + "cortes3/feliz.mp4", 1.6, pc.cta_ini - fac, 1.04)    # "organizada e fácil de aplicar na sua rotina" → venda fechada
pc.clipe(CTA4, 0.0, 6.05)

# ---- overlays ----
TEMAS = [("FGTS", f1), ("Minha Casa Minha Vida", f2), ("Consórcio", f3), ("Documentação", f4)]
def chips(img, t):
    antes = t < DA
    if not (antes or ee <= t < pc.cta_ini): return
    d = ImageDraw.Draw(img); fz = 36
    linhas = [TEMAS[:2], TEMAS[2:]]
    for r, lin in enumerate(linhas):
        ws = [d.textlength(n, font=fonte(800, fz)) + 2 * 30 + 58 for n, _ in lin]; gap = 16
        x = (W - (sum(ws) + gap)) / 2; y = 1052 + r * 92
        for (n, tf), w in zip(lin, ws):
            if antes:
                if t >= tf:
                    k = mola((t - tf) / 0.35); dy = int((1 - k) * 30)
                    pilula(img, x, y + dy, n, TERRA, fz=fz, icone="?", pad=30, alpha=min(1, (t - tf) / 0.12))
            else:
                j = TEMAS.index((n, tf)); t0 = ee + 0.12 * j
                if t >= t0:
                    k = mola((t - t0) / 0.35); dy = int((1 - k) * 30)
                    pilula(img, x, y + dy, n, TEAL2, fz=fz, icone="v", pad=30, alpha=min(1, (t - t0) / 0.12))
            x += w + gap

def selo(img, t):
    if t >= pc.cta_ini: return
    if t < DA - 0.05:
        pilula(img, W / 2, 165, "ANTES", TERRA, fz=58, icone="x", centro=True)
        pilula_ajusta(img, 290, "“Vou confirmar e te aviso.”", (255, 255, 255), cor=NAVY, fz=42)
    elif t >= H + 0.10 and not (vc <= t < ee):          # nas páginas, nada cobre o título
        pilula(img, W / 2, 165, "DEPOIS", TEAL2, fz=58, icone="v", centro=True)
        k = ease((t - H - 0.10) / 0.3)
        if k > 0: pilula_ajusta(img, 290 + int((1 - k) * 20), "Você responde na hora, com o Mapa.", (255, 255, 255), cor=NAVY, fz=42, alpha=k)

def painel(img, t):   # painel DEPOIS que cruza a tela e esconde o corte; o texto fica parado no centro da zona segura
    p = (t - (DA - 0.25)) / 0.5
    if not (0 <= p <= 1): return
    x = int(-W + p * 2 * W)            # em DA cobre a tela inteira
    cam = Image.new("RGB", (W, H_), TEAL2); ImageDraw.Draw(cam).text((W / 2, 900), "DEPOIS", font=fonte(800, 150), fill="white", anchor="mm")
    x0, x1 = max(0, x), min(W, x + W)
    if x1 > x0: img.paste(cam.crop((x0, 0, x1, H_)), (x0, 0))
H_ = 1920
if __name__ == "__main__":
    render(pc, [chips, selo, painel])
