#!/usr/bin/env python3
"""Roteiros dos 5 vídeos-piloto (VP01–VP05) — rodada 1 de correções (16/11). Rodar da raiz do repo.

- Frases curtas, uma ideia por cena (o motor estende a cena até dar tempo de ler 2x).
- Tela do app = gravações atuais em agencia/referencias/material/ (mesma moto: Tiger 1200, 27.500 km),
  com a barra de status cortada (crop_topo=118). Nada de filmagem antiga.
- Preço "por R$19,90" no card final de VP02, VP03 e VP04 (nunca "vitalício").
- Todo vídeo termina com o gancho de novo (cena "eco") pra fechar o loop.
"""
import json, os

CTA = "📲 Baixe agora o MinhaMoto na App Store e no Google Play."
BASE = "#moto #motociclista #motoboy #manutencaodemoto #motosbrasil"

def leg(gancho, valor, quem, tags):
    ig = f"{gancho}\n\n{valor}\n\n📌 Salva pra não esquecer e manda pra quem {quem}.\n\n{CTA}\n\n{BASE} {tags} #minhamoto"
    t5 = " ".join((tags.split() + BASE.split())[:5])
    tt = f"{gancho} 📌 Salva e manda pra quem {quem}. {CTA} {t5} #fyp #motostiktok"
    return ig, tt

MAT = "agencia/referencias/material/"
V = []

HOOK1 = ["Sua moto", "não quebra", "*do nada.*"]
V.append(dict(id="VP01", titulo="Sua moto não quebra do nada", formato="Texto animado + fotos", capa_t=1.4, cenas=[
    dict(tipo="kinetic", dur=2.9, tam=156, linhas=HOOK1),
    dict(tipo="kinetic", dur=1.9, tam=150, linhas=["Ela *avisa* antes."]),
    dict(tipo="photo", dur=2.0, foto="17024710.jpg", titulo="Barulho *novo.*", tam=128),
    dict(tipo="photo", dur=2.0, foto="19949302.jpg", pos="center 75%", titulo="Freio *mais mole.*", tam=128),
    dict(tipo="photo", dur=2.0, foto="37131862-corrente.jpg", pos="70% center", titulo="Corrente *batendo.*", tam=128),
    dict(tipo="kinetic", dur=2.4, tam=132, bg="azul", linhas=["Quem ignora,", "*paga o conserto.*"]),
    dict(tipo="kinetic", dur=2.4, tam=132, linhas=["Quem anota,", "*paga só a manutenção.*"]),
    dict(tipo="end", dur=3.2, titulo="Anota tudo no\n*MinhaMoto.*", sub="Baixe agora."),
    dict(tipo="kinetic", dur=0.9, tam=156, passo=0.07, eco=True, linhas=HOOK1),
], leg=leg("Sua moto não quebra do nada. Ela avisa antes.",
           "Barulho novo, freio mais mole, corrente batendo: tudo isso é aviso. Quem ignora paga o conserto. Quem anota e cuida no prazo paga só a manutenção.",
           "acha que a moto quebrou do nada", "#manutencaopreventiva #mecanicademoto #dicasdemoto")))

HOOK2 = ["Caderninho,", "nota fiscal", "ou *memória?*"]
V.append(dict(id="VP02", titulo="O app em ação", formato="Tela do app em ação (gravação real)", capa_t=4.0, cenas=[
    dict(tipo="kinetic", dur=2.6, tam=140, passo=0.3, linhas=HOOK2),
    dict(tipo="clip", dur=3.6, video=MAT + "tela-cadastro-moto.mp4", ini=103.5, vel=1.8, crop_topo=118, top=560,
         titulo="Mostra o que *nunca foi feito.*", zoom=[1.0, 1.12], foco=[0.5, 0.3]),
    dict(tipo="clip", dur=3.3, video=MAT + "tela-saude-1.mp4", ini=7.0, vel=1.4, crop_topo=118, top=560,
         titulo="Separa o urgente *do que tá em dia.*", zoom=[1.0, 1.1], foco=[0.5, 0.4]),
    dict(tipo="clip", dur=2.8, video=MAT + "tela-saude-1.mp4", ini=16.0, vel=0.5, crop_topo=118, top=560,
         titulo="Fez o serviço? *Um toque.*", zoom=[1.05, 1.25], foco=[0.5, 0.66], toque=[1.3, 0.5, 0.658]),
    dict(tipo="clip", dur=2.9, video=MAT + "tela-notificacoes.mp4", ini=68.4, vel=1.0, crop_topo=118, top=560,
         titulo="E te avisa *quando vencer.*", zoom=[1.0, 1.35], foco=[0.5, 0.0]),
    dict(tipo="end", dur=3.2, titulo="Sua moto\n*no controle.*", sub="Baixe por R$19,90."),
    dict(tipo="kinetic", dur=0.9, tam=140, passo=0.07, eco=True, linhas=HOOK2),
], leg=leg("Caderninho, nota fiscal na carteira ou memória? Tem jeito melhor de cuidar da moto.",
           "No MinhaMoto você vê o que nunca foi feito, o que é urgente e o que tá em dia. Fez o serviço? Um toque registra. E quando um cuidado vence, o aviso chega no celular.",
           "ainda anota manutenção no caderninho", "#appdemoto #organizacao #revisaodemoto")))

V.append(dict(id="VP03", titulo="POV: o mecânico pergunta", formato="POV / meme", capa_t=1.6, cenas=[
    dict(tipo="photo", dur=2.4, foto="9607261.jpg", kicker="POV", titulo="O mecânico *pergunta:*", tam=124),
    dict(tipo="kinetic", dur=3.2, tam=116, linhas=["“Quando foi", "a última troca", "*de óleo?*”"]),
    dict(tipo="kinetic", dur=1.8, tam=150, linhas=["Você:", "“Uns 3 meses…”"]),
    dict(tipo="kinetic", dur=1.6, tam=170, linhas=["“…ou 6?”"]),
    dict(tipo="kinetic", dur=1.7, tam=190, linhas=["“*Sei lá.*”"]),
    dict(tipo="phone", dur=3.0, print="rec-saude-emdia.png", top=620, kicker="Com o MinhaMoto", titulo="“Tá tudo *aqui.*”", tam=96,
         zoom=[1.0, 1.25], foco=[0.5, 0.15]),
    dict(tipo="end", dur=3.2, titulo="Seja o cliente\n*que sabe.*", sub="Baixe por R$19,90."),
    dict(tipo="kinetic", dur=0.9, tam=124, passo=0.07, eco=True, linhas=["O mecânico", "*pergunta:*"]),
], leg=leg("Todo mundo já foi o “uns 3 meses… ou 6?” na oficina.",
           "Quando o mecânico pergunta da última troca, quem tem o histórico responde na hora e mostra na tela o que tá em dia. É outra conversa.",
           "nunca lembra quando trocou o óleo", "#humor #oficinademoto #trocadeoleo")))

HOOK4 = ["5 erros", "*que matam*", "sua moto"]
V.append(dict(id="VP04", titulo="5 erros que matam sua moto", formato="Lista rápida", capa_t=1.4, cenas=[
    dict(tipo="kinetic", dur=3.0, tam=128, passo=0.3, linhas=HOOK4),
    dict(tipo="photo", dur=2.6, n=5, foto="14700339.jpg", pos="center 55%", titulo="Rodar com\n*pneu murcho*"),
    dict(tipo="photo", dur=2.6, n=4, foto="37131862-corrente.jpg", pos="70% center", titulo="Esquecer\n*a corrente*"),
    dict(tipo="photo", dur=2.6, n=3, foto="17024710.jpg", titulo="Ignorar\n*barulho novo*"),
    dict(tipo="photo", dur=2.6, n=2, foto="31664515.jpg", titulo="Passar do\n*prazo do óleo*"),
    dict(tipo="photo", dur=2.6, n=1, foto="6446251.jpg", titulo="Não anotar\n*nada*"),
    dict(tipo="end", dur=3.4, titulo="Erro número 1?\n*O app resolve.*", sub="Baixe agora."),
    dict(tipo="kinetic", dur=0.9, tam=128, passo=0.07, eco=True, linhas=HOOK4),
], leg=leg("O erro número 1 é o que quase todo motociclista comete.",
           "Pneu murcho, corrente esquecida, barulho ignorado, óleo vencido e, o pior de todos, não anotar nada. Sem histórico, os outros erros sempre voltam.",
           "vive esquecendo a manutenção da moto", "#errosdemoto #dicasdemoto #cuidadoscomamoto")))

V.append(dict(id="VP05", titulo="Quiz: o que significa 10W-30", formato="Quiz", capa_t=1.2, cenas=[
    dict(tipo="quiz", dur=6.0, pergunta="O que significa *10W-30* no óleo?", opcoes=["Tipo de pneu", "Viscosidade", "Código da peça"],
         certa=1, revela=4.0, explica="*10W*: o óleo no frio."),
    dict(tipo="kinetic", dur=2.6, tam=132, linhas=["*30*: no motor", "quente."]),
    dict(tipo="kinetic", dur=3.0, tam=124, bg="azul", linhas=["Regra de ouro:", "*siga o manual.*"]),
    dict(tipo="end", dur=3.2, titulo="Óleo certo,\n*na hora certa.*", sub="O MinhaMoto guarda qual óleo você usou."),
    dict(tipo="kinetic", dur=0.9, tam=120, passo=0.07, eco=True, linhas=["O que significa", "*10W-30?*"]),
], leg=leg("Você acertaria essa? Comenta a letra antes de ver o final.",
           "No fim do vídeo tem a resposta e a regra de ouro pra nunca errar o óleo da sua moto.",
           "acha que sabe tudo de moto", "#oleodemoto #quiz #10w30")))

if __name__ == '__main__':
    os.makedirs('agencia/roteiros-video', exist_ok=True)
    for v in V:
        v['legenda_ig_fb'], v['legenda_tiktok'] = v.pop('leg')
        json.dump(v, open(f"agencia/roteiros-video/{v['id']}.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(V), 'roteiros de vídeo')
