#!/usr/bin/env python3
"""Roteiros AG01–AG10 — lote piloto v2, rodada 1 de correções (16/11). Rodar da raiz do repo.

Mudanças da rodada 1 (relatório do revisor em revisao/relatorio.md):
- AG01 e AG03 com ângulo novo (o antigo repetia B16 e E05).
- Telas do app: só gravações reais recortadas (sem barra de gravação), UMA moto por peça
  (Tiger 1200 27.500 km = rec-*, gravações atuais; combustível = recorte da tela do carrossel DV05 do Davi).
  Recorte com zoom ("crop") no que a copy cita.
- Fotos com marca de terceiro/placa estrangeira/cena asiática removidas (sem filmagens antigas do app).
- Fatos conferidos: consumo (AutoPapo, 10 manutenções que melhoram o consumo da moto),
  TWI/1,6 mm (AutoPapo + Res. Contran 913/2022), CG mais vendida (Garagem360, 224.750 no 1º sem/2025).
"""
import json, re

CTA = "📲 Baixe agora o MinhaMoto na App Store e no Google Play."
BASE = "#moto #motociclista #motoboy #manutencaodemoto #motosbrasil"

def leg(gancho, valor, quem, tags):
    ig = f"{gancho}\n\n{valor}\n\n📌 Salva pra não esquecer e manda pra quem {quem}.\n\n{CTA}\n\n{BASE} {tags} #minhamoto"
    t5 = " ".join((tags.split() + BASE.split())[:5])
    tt = f"{gancho} 📌 Salva e manda pra quem {quem}. {CTA} {t5} #fyp #motostiktok"
    return ig, tt

COMB = dict(print="dv-combustivel-resumo.png", crop=[0, 0, 458, 296])  # tela atual (carrossel DV05 do Davi)
SEMAF = dict(print="rec-saude-semaforo.png", crop=[10, 590, 1070, 1000])
SEMH = dict(print="rec-sem-historico.png", crop=[10, 690, 1070, 1240])
EMDIA = dict(print="rec-saude-emdia.png", crop=[10, 140, 1070, 520])
NOTIF = dict(print="rec-notificacoes.png", crop=[10, 680, 1070, 1400])
TEMPO = dict(print="rec-tempo.png", crop=[10, 980, 1070, 1800])

R = []

R.append(dict(id="AG01", titulo="Sua moto começou a beber mais?", linha="Educacional", estilo="dark", cards=[
    dict(layout="capa", kicker="Consumo", titulo="Sua moto começou a *beber mais?*", apoio="Antes de culpar a gasolina, olha a moto.",
         shot_top=740, shot_w=640, **COMB),
    dict(layout="texto", kicker="O sintoma", titulo="Média caindo é *aviso,* não azar.",
         apoio="Quando a moto passa a fazer menos km por litro, quase sempre tem manutenção pedindo atenção."),
    dict(layout="item", n=1, titulo="Pneu *murcho*", apoio="Mais atrito com o chão, mais força pra empurrar a moto. E mais gasolina no tanque."),
    dict(layout="item", n=2, titulo="Filtro de ar *sujo*", apoio="Entra menos ar no motor, e ele compensa queimando mais combustível."),
    dict(layout="item", n=3, titulo="Vela *gasta*", apoio="A queima fica imprecisa e parte da gasolina vai embora sem virar força."),
    dict(layout="item", n=4, titulo="Freio *preso*", apoio="Pinça travada ou freio apertado demais seguram a roda o tempo todo."),
    dict(layout="cta", titulo="Anota cada abastecida.\n*A média te avisa.*",
         apoio="No *MinhaMoto*, o consumo é calculado entre dois tanques cheios. Caiu a média, você percebe."),
], leg=leg("Sua moto tá fazendo menos km por litro? Nem sempre a culpa é da gasolina.",
           "Média caindo costuma ser aviso de manutenção: pneu murcho, filtro de ar sujo, vela gasta e freio preso fazem a moto beber mais. Anota cada abastecida e acompanha a média: quando ela cai, você descobre antes de gastar à toa.",
           "vive reclamando do preço da gasolina", "#consumodemoto #gasolina #economia")))

R.append(dict(id="AG02", titulo="5 barulhos que você não pode ignorar", linha="Dicas e hacks", estilo="foto", cards=[
    dict(layout="capa", kicker="Ouviu isso?", titulo="5 barulhos que você *não pode ignorar*", apoio="Sua moto avisa antes de quebrar.",
         foto="10103321.jpg", pos="center 60%"),
    dict(layout="item", n=1, titulo="Chiado metálico *na freada*", apoio="Pode ser pastilha no fim. Metal no metal come o disco junto.", foto="19949302.jpg"),
    dict(layout="item", n=2, titulo="Corrente *batendo*", apoio="Folga fora do ponto ou relação gasta. Regular custa pouco. Arrebentar custa caro.",
         foto="37131862-corrente.jpg", pos="70% center"),
    dict(layout="item", n=3, titulo="Ronco que cresce\n*com a velocidade*", apoio="Pode ser rolamento de roda. Quanto mais rápido, mais alto o barulho.", foto="17024710.jpg"),
    dict(layout="item", n=4, titulo="Estouro no escape\n*ao reduzir*", apoio="Pode ser entrada de ar ou mistura desregulada. Vale levar pra avaliar.",
         foto="29740729.jpg", pos="62% center"),
    dict(layout="item", n=5, titulo="Batendo pino\n*na subida*", apoio="Pode ser combustível ruim ou carbonização. Ignorar desgasta o motor por dentro.",
         foto="33233592.jpg", pos="center 40%"),
    dict(layout="cta", titulo="Ouviu um desses?\n*Leva no mecânico.*",
         apoio="E chega lá com o histórico da moto no *MinhaMoto*: o que foi feito, quando e com quantos km.", estilo="dark"),
], leg=leg("Sua moto avisa antes de quebrar. O problema é que quase ninguém escuta.",
           "Chiado na freada, corrente batendo, ronco que cresce com a velocidade, estouro no escape ao reduzir e motor batendo pino na subida. Nenhum desses dá pra ignorar. Na dúvida, leva no mecânico de confiança antes que o barulho vire conserto.",
           "acha que todo barulho é normal da moto", "#barulhonamoto #mecanicademoto #freiodemoto")))

R.append(dict(id="AG03", titulo="O aviso escondido no pneu (TWI)", linha="Educacional", estilo="claro", cards=[
    dict(layout="capa", marca="Pneu", titulo="Seu pneu tem um *aviso escondido.*", grande="TWI", grande_tam=330,
         apoio="Quase ninguém olha. E é ele que diz a hora certa da troca."),
    dict(layout="texto", marca="Pneu", titulo="TWI é o indicador *de desgaste.*",
         apoio="São ressaltos pequenos no fundo dos sulcos. A sigla TWI na lateral do pneu mostra onde eles ficam."),
    dict(layout="numero", marca="Pneu", grande="1,6", titulo="Milímetro: *o limite da lei.*",
         apoio="Pela Resolução 913/2022 do Contran, com menos de 1,6 mm de sulco o pneu não pode rodar."),
    dict(layout="texto", marca="Pneu", titulo="Banda na altura do TWI? *Hora de trocar.*",
         apoio="Se o sulco chegou no ressalto, o pneu já está no limite. Não espera ele ficar liso."),
    dict(layout="texto", marca="Pneu", titulo="Na chuva, *é aqui que pesa.*",
         apoio="Pneu gasto escoa menos água: freia pior e derrapa mais fácil no molhado."),
    dict(layout="cta", marca="Pneu", titulo="Anota a troca do pneu.\n*Acompanha o desgaste.*",
         apoio="No *MinhaMoto*, a troca fica registrada com data e km, junto com o resto da manutenção."),
], leg=leg("Todo pneu tem um aviso escondido que diz a hora da troca. Você sabe onde fica?",
           "O TWI é o indicador de desgaste: ressaltos no fundo dos sulcos, marcados pela sigla TWI na lateral. Quando a banda chega na altura dele, o pneu está no limite. Pela Resolução 913/2022 do Contran, abaixo de 1,6 mm de sulco o pneu não pode rodar.",
           "nunca olhou o sulco do pneu", "#pneudemoto #twi #segurancanotransito")))

R.append(dict(id="AG04", titulo="Moto com histórico vende melhor", linha="Curtos AIDA", estilo="dark", cards=[
    dict(layout="capa", kicker="Revenda", titulo="Duas motos iguais.\n*Só uma tem histórico.*", apoio="Adivinha qual delas o comprador leva.",
         shot_top=780, shot_w=860, **SEMH),
    dict(layout="texto", kicker="O medo dele", titulo="Quem compra usada tem um medo: *levar problema pra casa.*",
         apoio="Ele quer saber o que foi feito, quando e onde. “Sempre cuidei” não convence ninguém."),
    dict(layout="numero", grande="?", titulo="“Quando trocou o óleo?”\n*Você sabe responder?*",
         apoio="Sem registro, vira sua palavra contra a desconfiança dele. E desconfiança derruba o preço."),
    dict(layout="phone", kicker="Com histórico", titulo="O que foi feito e quando.\n*Tudo na tela.*",
         apoio="Cada serviço registrado vira argumento na hora de negociar.", **EMDIA),
    dict(layout="cta", titulo="O histórico de hoje\n*vale dinheiro amanhã.*", apoio="Baixe o *MinhaMoto* por R$19,90 e monte o histórico da sua moto."),
], leg=leg("Duas motos iguais, mesmo ano, mesmo km. Só uma tem histórico. Qual você compraria?",
           "Quem compra usada tem medo de levar problema pra casa, e “sempre cuidei” não convence ninguém. Serviço registrado, com data e km, convence e ajuda a segurar o preço na negociação.",
           "vai vender a moto esse ano", "#motousada #vendermoto #revenda")))

R.append(dict(id="AG05", titulo="Chuva chegando: 4 checagens", linha="Dicas e hacks", estilo="foto", cards=[
    dict(layout="capa", kicker="Época de chuva", titulo="Chuva chegando?\n*Confere antes de sair.*", apoio="4 checagens rápidas pra rodar seguro no molhado.",
         foto="5195494.jpg", pos="center 40%"),
    dict(layout="item", n=1, titulo="Sulco *do pneu*", apoio="Na chuva, pneu careca é aquaplanagem na certa. Confere o indicador TWI.", foto="14700339.jpg", pos="center 55%"),
    dict(layout="item", n=2, titulo="Pressão *certa*", apoio="Calibra com o pneu frio, na pressão do manual. Murcho no molhado é risco dobrado.", foto="5803314.jpg", pos="35% center"),
    dict(layout="item", n=3, titulo="Farol *e lanterna*", apoio="Na chuva, ver e ser visto pode salvar sua vida. Tudo acendendo?", foto="4686570.jpg"),
    dict(layout="item", n=4, titulo="Viseira *limpa*", apoio="Viseira riscada ou embaçada esconde o buraco e o carro freando. Limpa antes de sair.", foto="9835235.jpg"),
    dict(layout="cta", titulo="Moto revisada\n*encara a chuva.*", apoio="Registre cada cuidado no MinhaMoto e saiba o que vence antes do aperto.",
         foto="18550074.jpg", pos="60% center"),
], leg=leg("A chuva não avisa. Sua moto tá pronta pra ela?",
           "Antes da temporada de chuva, confere 4 coisas: sulco do pneu, pressão certa (com o pneu frio), farol e lanterna funcionando e viseira limpa. Na pista molhada, é isso que separa o susto do tombo.",
           "roda na chuva todo dia", "#chuva #pilotagemsegura #pneudemoto")))

R.append(dict(id="AG06", titulo="Por que todo mundo tem uma CG", linha="Marcas", estilo="claro", cards=[
    dict(layout="capa", marca="Marcas", titulo="Por que *todo mundo* tem uma CG?", grande="CG",
         apoio="Mais de 224 mil vendidas só no 1º semestre de 2025. Não é sorte."),
    dict(layout="item", marca="Marcas", n=1, titulo="Peça em *qualquer* autopeça", apoio="Do balcão do bairro à loja grande: achar peça de CG é fácil e costuma sair em conta."),
    dict(layout="item", marca="Marcas", n=2, titulo="Mecânico *que conhece*", apoio="Qualquer oficina já abriu uma CG. Isso economiza tempo e evita diagnóstico errado."),
    dict(layout="item", marca="Marcas", n=3, titulo="Revenda *que gira*", apoio="Muita gente procura. Moto que todo mundo quer vende mais fácil."),
    dict(layout="item", marca="Marcas", n=4, titulo="*Simples* de manter", apoio="Motor conhecido, manutenção sem mistério. Combina com quem roda todo dia."),
    dict(layout="texto", marca="Marcas", titulo="Mas atenção:\n*simples não é indestrutível.*", apoio="CG sem óleo trocado e com a relação esquecida também quebra. Como qualquer moto."),
    dict(layout="cta", marca="Marcas", titulo="Seja CG ou não:\n*moto que dura é moto cuidada.*", apoio="Registre cada manutenção no *MinhaMoto*."),
], leg=leg("Repara: em todo semáforo tem uma CG. E não é por acaso.",
           "A CG é a moto mais vendida do Brasil (mais de 224 mil só no 1º semestre de 2025). Peça em qualquer autopeça, mecânico que conhece, revenda que gira e manutenção sem mistério. Mas simples não é indestrutível: CG sem óleo trocado quebra como qualquer moto.",
           "tem ou já teve uma CG", "#hondacg #cg160 #honda")))

R.append(dict(id="AG07", titulo="Passou do prazo do óleo", linha="Educacional", estilo="dark", cards=[
    dict(layout="capa", kicker="Troca vencida", titulo="Passou do prazo do óleo. *E daí?*", apoio="O que acontece com a moto quando a troca atrasa.",
         shot_top=780, shot_w=860, **SEMAF),
    dict(layout="texto", kicker="Por dentro", titulo="Óleo velho *perde o poder de proteger.*",
         apoio="Com o uso, ele se degrada e acumula resíduo. Lubrifica pior, protege pior."),
    dict(layout="texto", kicker="O resultado", titulo="Mais atrito.\nMais calor.\n*Mais desgaste.*",
         apoio="O motor não quebra no dia seguinte. Ele vai se gastando calado."),
    dict(layout="numero", grande="2", titulo="O prazo vence *de dois jeitos.*",
         apoio="Por quilometragem e por tempo, o que chegar primeiro. O intervalo certo está no manual da sua moto."),
    dict(layout="phone", kicker="Sem decorar nada", titulo="O app conta *km e tempo* pra você.",
         apoio="Cada cuidado com o seu prazo. O que vence pelo tempo também aparece.", shot_w=820, **TEMPO),
    dict(layout="cta", titulo="Troca no prazo.\n*O motor dura mais.*", apoio="Baixe o *MinhaMoto* e nunca mais perca a data do óleo."),
], leg=leg("Passou uns mil km da troca de óleo. Nada aconteceu. Ainda.",
           "Óleo velho perde o poder de proteger: mais atrito, mais calor, mais desgaste. O motor não quebra no dia seguinte, ele vai se gastando calado. E o prazo vence de dois jeitos, por km e por tempo, o que chegar primeiro: confere o intervalo no manual da sua moto.",
           "sempre passa do prazo do óleo", "#trocadeoleo #oleodemoto #motordemoto")))

R.append(dict(id="AG08", titulo="Só quem trabalha de moto entende", linha="Temas gerais", estilo="dark", cards=[
    dict(layout="capa", kicker="Vida de motoboy", titulo="Só quem trabalha *de moto* entende.", grande="5", apoio="Se você vive disso, vai se ver nos 5."),
    dict(layout="item", n=1, titulo="Chuva não é desculpa.\n*É só mais um dia.*"),
    dict(layout="item", n=2, titulo="Você sabe o km da moto *melhor que a senha do banco.*"),
    dict(layout="item", n=3, titulo="Seu mecânico tem *seu número salvo.*", apoio="E o dele tá nos seus favoritos."),
    dict(layout="item", n=4, titulo="Gasolina subiu?\n*Você sente no mesmo dia.*"),
    dict(layout="item", n=5, titulo="Moto parada *é dia sem ganhar.*"),
    dict(layout="cta", titulo="Ela paga suas contas.\n*Cuida bem dela.*", apoio="Manutenção, gastos e documentos da sua moto no *MinhaMoto*."),
], leg=leg("Se a moto é seu ganha-pão, você vai se ver em todos esses.",
           "Chuva é só mais um dia, o mecânico tem seu número salvo e moto parada é dia sem ganhar. Quem vive da moto sabe: cuidar dela é cuidar do próprio bolso.",
           "faz entrega de moto todo dia", "#vidademotoboy #entregador #motofrete")))

R.append(dict(id="AG09", titulo="Sua memória não é um sistema de manutenção", linha="Curtos AIDA", estilo="claro", cards=[
    dict(layout="capa", marca="Memória", titulo="Sua memória *não é* sistema de manutenção.", apoio="E tá tudo bem. Ninguém lembra de tudo.",
         shot_top=760, shot_w=860, **EMDIA),
    dict(layout="texto", marca="Memória", titulo="Nota fiscal *some.*\nOficina *fecha.*\nMemória *falha.*", apoio="E quando você precisa da informação, ela sumiu junto."),
    dict(layout="numero", marca="Memória", grande="0", titulo="Esforço pra lembrar: *zero.*", apoio="Registrou uma vez, tá guardado. Data, km, peça e valor."),
    dict(layout="phone", marca="Memória", titulo="Saiu do prazo? *O app te avisa.*", apoio="O lembrete chega no celular quando um cuidado vence.", shot_w=820, **NOTIF),
    dict(layout="cta", marca="Memória", titulo="Você pilota.\n*O MinhaMoto lembra.*", apoio="Baixe agora por R$19,90 e tire a manutenção da cabeça."),
], leg=leg("Sua memória não foi feita pra lembrar troca de filtro, óleo e relação. E nem precisa.",
           "Nota fiscal some, oficina fecha, memória falha. Registra uma vez e pronto: o histórico fica guardado e, quando um cuidado sai do prazo, o lembrete chega no celular.",
           "esquece tudo da manutenção da moto", "#organizacao #manutencaopreventiva #revisaodemoto")))

R.append(dict(id="AG10", titulo="Moto parada: checklist antes de ligar", linha="Dicas e hacks", estilo="dark", cards=[
    dict(layout="capa", estilo="foto", kicker="Moto parada", titulo="Ficou parada?\n*Não sai ligando.*", apoio="Faz esse checklist antes de girar a chave.",
         foto="30817486.jpg", pos="45% center"),
    dict(layout="item", n=1, titulo="Calibra *os pneus.*", apoio="Pneu perde pressão parado. Rodar murcho gasta o pneu e tira a estabilidade."),
    dict(layout="item", n=2, titulo="Olha *a corrente.*", apoio="Ressecada ou com ferrugem? Limpa e lubrifica antes de rodar."),
    dict(layout="item", n=3, titulo="Testa *a bateria.*", apoio="Bateria descarrega com o tempo. Partida fraca? Carrega antes de insistir."),
    dict(layout="item", n=4, titulo="Confere *óleo e freio.*", apoio="Nível do óleo certo e freio firme na mão e no pé."),
    dict(layout="item", n=5, titulo="Desconfia da *gasolina velha.*", apoio="Combustível parado por muito tempo perde qualidade. Ficou meses? Vale avaliar."),
    dict(layout="cta", titulo="Moto parada também\n*tem prazo correndo.*", apoio="O *MinhaMoto* acompanha cada cuidado por km e por tempo. Baixe agora."),
], leg=leg("Moto ficou parada? Girar a chave e sair andando é o erro mais comum.",
           "Antes de rodar: calibra os pneus, olha a corrente, testa a bateria, confere óleo e freio e desconfia da gasolina velha. E lembra que moto parada também tem cuidado vencendo pelo tempo.",
           "deixa a moto parada na garagem", "#motoparada #bateriademoto #cuidadoscomamoto")))

def curly(o):
    if isinstance(o, str): return re.sub(r'"([^"]+)"', r'“\1”', o)
    if isinstance(o, (list, tuple)): return type(o)(curly(x) for x in o)
    if isinstance(o, dict): return {k: curly(v) for k, v in o.items()}
    return o

if __name__ == '__main__':
    R[:] = [curly(r) for r in R]
    for r in R:
        ig, tt = r.pop('leg')
        r['legenda_ig_fb'], r['legenda_tiktok'] = ig, tt
        json.dump(r, open(f"agencia/roteiros/{r['id']}.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(R), 'roteiros')
