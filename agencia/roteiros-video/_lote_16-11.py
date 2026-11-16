#!/usr/bin/env python3
"""Roteiros dos 5 vídeos-piloto (VP01–VP05). Rodar da raiz do repo."""
import json, os

CTA = "📲 Baixe agora o MinhaMoto na App Store e no Google Play."
BASE = "#moto #motociclista #motoboy #manutencaodemoto #motosbrasil"

def leg(gancho, valor, quem, tags):
    ig = f"{gancho}\n\n{valor}\n\n📌 Salva e manda pra quem {quem}.\n\n{CTA}\n\n{BASE} {tags} #minhamoto"
    t5 = " ".join((tags.split() + BASE.split())[:5])
    tt = f"{gancho} 📌 Manda pra quem {quem}. {CTA} {t5} #fyp #motostiktok"
    return ig, tt

V = []
V.append(dict(id="VP01", titulo="Sua moto não quebra do nada", formato="Texto animado", capa_t=1.6, cenas=[
    dict(tipo="kinetic", dur=2.2, tam=150, linhas=["Sua moto", "não quebra", "*do nada.*"]),
    dict(tipo="kinetic", dur=3.0, tam=96, linhas=["Ela avisa antes:", "barulho novo,", "freio mais mole,", "corrente batendo."]),
    dict(tipo="kinetic", dur=2.2, tam=112, bg="azul", linhas=["Quem ignora,", "*paga o conserto.*"]),
    dict(tipo="kinetic", dur=2.2, tam=120, linhas=["Quem anota,", "*paga só a manutenção.*"]),
    dict(tipo="end", dur=2.8, titulo="Anota tudo no\n*MinhaMoto.*", sub="Baixe agora na App Store e no Google Play."),
    dict(tipo="kinetic", dur=0.8, tam=150, passo=0.08, linhas=["Sua moto", "não quebra", "*do nada.*"]),
], leg=leg("Sua moto não quebra do nada. Ela avisa antes.",
           "Barulho novo, freio mais mole, corrente batendo: tudo isso é aviso. Quem ignora paga o conserto. Quem anota e cuida no prazo paga só a manutenção.",
           "acha que a moto quebrou do nada", "#manutencaopreventiva #mecanicademoto #dicasdemoto")))

V.append(dict(id="VP02", titulo="O app em ação", formato="Tela do app em ação", capa_t=3.0, cenas=[
    dict(tipo="kinetic", dur=2.0, tam=120, passo=0.35, linhas=["Onde você anota", "a manutenção", "da sua *moto?*"]),
    dict(tipo="phone", dur=2.6, print="plano-atual.png", titulo="O app mostra\n*o que vence.*", sub="Pelo plano do seu modelo, por km."),
    dict(tipo="phone", dur=2.6, print="registro-filtro-oleo.png", titulo="Registra o serviço\n*em segundos.*", sub="Data, km, valor e peça."),
    dict(tipo="phone", dur=2.6, print="historico-completo.png", titulo="Tudo vira\n*histórico.*", sub="Com o quanto você pagou em cada serviço."),
    dict(tipo="phone", dur=2.6, print="tempo-limites.png", titulo="Controla\n*km e tempo.*", sub="Vale o primeiro limite que chegar."),
    dict(tipo="phone", dur=2.4, print="combustivel-media.png", titulo="E o consumo\n*de verdade.*", sub="Média calculada pelos abastecimentos."),
    dict(tipo="end", dur=2.6, titulo="Sua moto\n*no controle.*", sub="Baixe o MinhaMoto."),
], leg=leg("Caderninho, nota fiscal na carteira ou memória? Tem jeito melhor de cuidar da moto.",
           "No MinhaMoto você vê o que vence pelo plano do seu modelo, registra cada serviço em segundos, guarda o histórico com valores e acompanha o consumo real.",
           "ainda anota manutenção no caderninho", "#appdemoto #organizacao #revisaodemoto")))

V.append(dict(id="VP03", titulo="POV: o mecânico pergunta", formato="POV / meme", capa_t=1.4, cenas=[
    dict(tipo="photo", dur=3.4, foto="3822784.jpg", pos="center 30%", kicker="POV", tam=82,
         titulo="O mecânico pergunta: *quando foi a última troca de óleo?*"),
    dict(tipo="kinetic", dur=2.4, tam=124, linhas=["Você:", "“Uns 3 meses…", "ou 6?", "*Sei lá.*”"]),
    dict(tipo="kinetic", dur=1.4, tam=116, bg="azul", passo=0.25, linhas=["Quem usa o", "*MinhaMoto:*"]),
    dict(tipo="phone", dur=3.2, print="historico-completo.png", tam=80, titulo="“Dia 07/11, *18.400 km*, óleo 10W-30.”", sub="Mecânico respeita."),
    dict(tipo="end", dur=2.4, titulo="Seja o cliente\n*que sabe.*", sub="Baixe o MinhaMoto."),
], leg=leg("Todo mundo já foi o “uns 3 meses… ou 6?” na oficina.",
           "Quando o mecânico pergunta da última troca, quem tem o histórico responde na hora: data, km e qual óleo foi usado. É outra conversa.",
           "nunca lembra quando trocou o óleo", "#humor #oficinademoto #trocadeoleo")))

V.append(dict(id="VP04", titulo="5 erros que encurtam a vida da moto", formato="Lista rápida", capa_t=1.4, cenas=[
    dict(tipo="kinetic", dur=2.2, tam=120, passo=0.3, linhas=["5 erros que", "*encurtam a vida*", "da sua moto"]),
    dict(tipo="photo", dur=2.1, n=5, foto="25857998.jpg", titulo="Rodar com\n*pneu murcho*", sub="Gasta mais e tira a estabilidade."),
    dict(tipo="photo", dur=2.1, n=4, foto="37131862.jpg", pos="right center", titulo="Esquecer\n*a corrente*", sub="Sem lubrificar, o kit gasta antes."),
    dict(tipo="photo", dur=2.1, n=3, foto="17024710.jpg", titulo="Ignorar\n*barulho novo*", sub="Barulho é aviso. Não é frescura."),
    dict(tipo="photo", dur=2.1, n=2, foto="27704018.jpg", titulo="Passar do\n*prazo do óleo*", sub="O motor vai se gastando calado."),
    dict(tipo="photo", dur=2.1, n=1, foto="4792285.jpg", titulo="Não anotar\n*nada*", sub="Sem histórico, os outros erros voltam."),
    dict(tipo="end", dur=2.6, titulo="Erro número 1?\n*O app resolve.*", sub="Baixe o MinhaMoto."),
], leg=leg("O erro número 1 é o que quase todo motociclista comete.",
           "Pneu murcho, corrente esquecida, barulho ignorado, óleo vencido e, o pior de todos, não anotar nada. Sem histórico, os outros erros sempre voltam.",
           "precisa ver esse vídeo", "#errosdemoto #dicasdemoto #cuidadoscomamoto")))

V.append(dict(id="VP05", titulo="Quiz: o que significa 10W-30", formato="Quiz", capa_t=1.2, cenas=[
    dict(tipo="quiz", dur=9.0, pergunta="O que significa *10W-30* no óleo?", opcoes=["Tipo de pneu", "Viscosidade do óleo", "Código da peça"],
         certa=1, revela=5.0, explica="*10W*: como o óleo se comporta no frio. *30*: na temperatura de trabalho do motor."),
    dict(tipo="kinetic", dur=2.8, tam=104, linhas=["Regra de ouro:", "use o que o", "*manual da sua moto*", "indica."]),
    dict(tipo="end", dur=2.6, titulo="Óleo certo,\n*na hora certa.*", sub="O MinhaMoto guarda qual óleo você usou e mostra quando trocar."),
], leg=leg("Você acertou? Responde nos comentários antes de ver a resposta.",
           "10W-30 é a viscosidade do óleo: o 10W fala do comportamento no frio e o 30 da temperatura de trabalho do motor. Na dúvida, use sempre o que o manual da sua moto indica.",
           "acha que sabe tudo de moto", "#oleodemoto #quiz #10w30")))

if __name__ == '__main__':
    os.makedirs('agencia/roteiros-video', exist_ok=True)
    for v in V:
        v['legenda_ig_fb'], v['legenda_tiktok'] = v.pop('leg')
        json.dump(v, open(f"agencia/roteiros-video/{v['id']}.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(V), 'roteiros de vídeo')
