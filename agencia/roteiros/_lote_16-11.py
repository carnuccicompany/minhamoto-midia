#!/usr/bin/env python3
"""Gera os roteiros AG01–AG10 (lote piloto v2, 16/11). Rodar da raiz do repo."""
import json

CTA = "📲 Baixe agora o MinhaMoto na App Store e no Google Play."
BASE = "#moto #motociclista #motoboy #manutencaodemoto #motosbrasil"

def leg(gancho, valor, quem, tags):
    ig = f"{gancho}\n\n{valor}\n\n📌 Salva pra não esquecer e manda pra quem {quem}.\n\n{CTA}\n\n{BASE} {tags} #minhamoto"
    t5 = " ".join((tags.split() + BASE.split())[:5])
    tt = f"{gancho} 📌 Salva e manda pra quem {quem}. {CTA} {t5} #fyp #motostiktok"
    return ig, tt

R = []

R.append(dict(id="AG01", titulo="Quanto sua moto te custa por mês", linha="Educacional", estilo="dark", cards=[
    dict(layout="capa", kicker="Custo real", titulo="Quanto sua moto te custa *por mês?*", apoio="Se você respondeu de cabeça, chutou pra baixo.", print="historico-detalhes.png"),
    dict(layout="texto", kicker="O truque", titulo="O gasto nunca vem de uma vez.\n*Ele vem picado.*", apoio="Óleo num mês. Relação no outro. Pneu, gasolina, documento. Separado parece troco. Somado, assusta."),
    dict(layout="numero", grande="2x", titulo="Quem não anota *paga duas vezes.*", apoio="Troca o que já tinha trocado. Esquece o que custava pouco até virar conserto caro."),
    dict(layout="phone", kicker="A saída", titulo="Anota uma vez.\n*Fica guardado pra sempre.*", apoio="Data, km, peça e valor de cada serviço, num lugar só.", print="historico-completo.png"),
    dict(layout="phone", kicker="E a gasolina?", titulo="Entra na conta também.\n*Consumo real, sem achismo.*", apoio="Anota o abastecimento e o app calcula sua média de km/L.", print="combustivel-media.png"),
    dict(layout="cta", titulo="Para de chutar.\n*Começa a contar.*", apoio="Baixe o *MinhaMoto* e descubra quanto sua moto custa de verdade."),
], leg=leg("Quanto sua moto te custou esse mês? Se você respondeu de cabeça, chutou pra baixo.",
           "O gasto da moto nunca vem de uma vez: é um óleo aqui, uma relação ali, pneu, gasolina, documento. Separado parece troco. Somado, assusta. Quem anota data, km e valor de cada serviço para de pagar duas vezes pela mesma coisa.",
           "jura que moto não dá gasto", "#custodemoto #economia #gasolina")))

R.append(dict(id="AG02", titulo="5 barulhos que você não pode ignorar", linha="Dicas e hacks", estilo="foto", cards=[
    dict(layout="capa", kicker="Ouviu isso?", titulo="5 barulhos que você *não pode ignorar*", apoio="Sua moto avisa antes de deixar você na mão.", foto="3822784.jpg", pos="center 30%"),
    dict(layout="item", n=1, titulo="Chiado metálico *na freada*", apoio="Pode ser pastilha no fim. Metal raspando no disco estraga o disco junto.", foto="19949302.jpg"),
    dict(layout="item", n=2, titulo="Corrente *batendo*", apoio="Folga fora do ponto ou relação gasta. Regular custa pouco. Arrebentar custa caro.", foto="37131862.jpg"),
    dict(layout="item", n=3, titulo="Ronco que *cresce com a velocidade*", apoio="Pode ser rolamento de roda. Quanto mais rápido, mais alto o barulho.", foto="17024710.jpg"),
    dict(layout="item", n=4, titulo="Estouro no escape *ao reduzir*", apoio="Pode ser entrada de ar ou mistura desregulada. Vale levar pra avaliar.", foto="13722393.jpg"),
    dict(layout="item", n=5, titulo="Motor *batendo pino* na subida", apoio="Pode ser combustível ruim ou carbonização. Ignorar desgasta o motor por dentro.", foto="27704018.jpg"),
    dict(layout="cta", titulo="Ouviu um desses?\n*Leva no mecânico.*", apoio="E chega lá com o histórico da moto no MinhaMoto: o que foi feito, quando e com quantos km.", foto="3855217.jpg"),
], leg=leg("Sua moto avisa antes de quebrar. O problema é que quase ninguém escuta.",
           "Chiado na freada, corrente batendo, ronco que cresce com a velocidade, estouro no escape ao reduzir e motor batendo pino na subida. Nenhum desses é \"normal da moto\". Na dúvida, não arrisca: leva no mecânico de confiança.",
           "acha que todo barulho é normal da moto", "#barulhonamoto #mecanicademoto #freiodemoto")))

R.append(dict(id="AG03", titulo="Corrente: lubrificar, regular ou trocar", linha="Educacional", estilo="claro", cards=[
    dict(layout="capa", marca="Corrente", titulo="Lubrificar, regular ou trocar? *Não é a mesma coisa.*", apoio="Muita gente confunde os três. E a corrente cobra.", print="lubrificar.png"),
    dict(layout="item", marca="Corrente", n=1, titulo="*Lubrificar*: o cuidado de toda hora.", apoio="Lubrificante próprio pra corrente, com ela limpa. Depois de chuva ou lavagem, de novo.", print="lubrificar.png"),
    dict(layout="item", marca="Corrente", n=2, titulo="*Regular*: a folga certa.", apoio="Nem esticada, nem frouxa. A medida certa está no manual da sua moto.", print="ajuste.png"),
    dict(layout="item", marca="Corrente", n=3, titulo="*Trocar*: quando o kit gastou.", apoio="Corrente, coroa e pinhão se gastam juntos. Por isso a troca costuma ser do kit inteiro.", print="registro-relacao.png"),
    dict(layout="texto", marca="Corrente", titulo="Sinal de troca: *dente da coroa pontudo.*", apoio="Corrente que volta a ficar frouxa logo depois de regular também é aviso."),
    dict(layout="cta", marca="Corrente", titulo="Cada cuidado registrado.\n*Cada prazo na mão.*", apoio="No *MinhaMoto*, lubrificar, ajustar e trocar ficam registrados com data e km."),
], leg=leg("Lubrificar, regular e trocar a corrente não são a mesma coisa. E confundir sai caro.",
           "Lubrificar é o cuidado de toda hora, principalmente depois de chuva ou lavagem. Regular é deixar a folga na medida do manual. Trocar é quando o kit (corrente, coroa e pinhão) gastou. Dente da coroa pontudo é sinal claro de troca.",
           "vive com a corrente batendo", "#corrente #relacaodemoto #kitrelacao")))

R.append(dict(id="AG04", titulo="Moto com histórico vende melhor", linha="Curtos AIDA", estilo="dark", cards=[
    dict(layout="capa", kicker="Revenda", titulo="Duas motos iguais.\n*Só uma tem histórico.*", apoio="Adivinha qual o comprador escolhe.", print="historico-filtros.png"),
    dict(layout="texto", kicker="O medo dele", titulo="Quem compra usada tem um medo: *levar problema pra casa.*", apoio="Ele quer saber o que foi feito, quando e onde. “Sempre cuidei” não convence ninguém."),
    dict(layout="numero", grande="?", titulo="“Quando trocou o óleo?”\n*Você sabe responder?*", apoio="Sem registro, vira sua palavra contra a desconfiança dele. E desconfiança puxa o preço pra baixo."),
    dict(layout="phone", kicker="Com histórico", titulo="Data, km, peça e valor.\n*Tudo na tela.*", apoio="Cada serviço registrado vira argumento na hora de negociar.", print="historico-detalhes.png"),
    dict(layout="cta", titulo="Começa hoje.\n*A venda de amanhã agradece.*", apoio="Baixe o *MinhaMoto* e monte o histórico da sua moto."),
], leg=leg("Duas motos iguais, mesmo ano, mesmo km. Só uma tem histórico. Qual você compraria?",
           "Quem compra usada tem medo de levar problema pra casa. \"Sempre cuidei\" não convence ninguém. Serviço registrado com data, km, peça e valor convence, e ajuda a segurar o preço na negociação.",
           "vai vender a moto esse ano", "#motousada #vendermoto #revenda")))

R.append(dict(id="AG05", titulo="Chuva chegando: 5 checagens", linha="Dicas e hacks", estilo="foto", cards=[
    dict(layout="capa", kicker="Época de chuva", titulo="Chuva chegando?\n*Confere isso antes.*", apoio="5 checagens rápidas que evitam susto no asfalto molhado.", foto="5195494.jpg", pos="center 40%"),
    dict(layout="item", n=1, titulo="Sulco do *pneu*", apoio="Pneu careca não escoa água. Na chuva, é aquaplanagem esperando acontecer.", foto="25857998.jpg"),
    dict(layout="item", n=2, titulo="*Freio* respondendo", apoio="Pastilha no fim e chão molhado não combinam. Testa antes de sair.", foto="19949302.jpg", pos="center 60%"),
    dict(layout="item", n=3, titulo="*Farol e lanterna*", apoio="Na chuva, ver e ser visto vale a sua vida. Tudo acendendo?", foto="4686570.jpg"),
    dict(layout="item", n=4, titulo="*Corrente* lubrificada", apoio="Água lava o lubrificante. Rodou na chuva? Lubrifica de novo.", foto="37131862.jpg", pos="right center"),
    dict(layout="item", n=5, titulo="*Capa de chuva* no baú", apoio="Molhado e com frio, a atenção cai. Capa leve resolve.", foto="33136700.jpg"),
    dict(layout="cta", titulo="Revisada,\n*ela não te deixa na mão.*", apoio="Registre cada cuidado no MinhaMoto e saiba o que vence antes do aperto.", foto="18550074.jpg"),
], leg=leg("A chuva não avisa. Sua moto tá pronta pra ela?",
           "Antes da temporada de chuva, confere 5 coisas: sulco do pneu, freio respondendo, farol e lanterna, corrente lubrificada e capa de chuva no baú. Leva 5 minutos e evita o susto no asfalto molhado.",
           "roda na chuva todo dia", "#chuva #pilotagemsegura #pneudemoto")))

R.append(dict(id="AG06", titulo="Por que todo mundo tem uma CG", linha="Marcas", estilo="claro", cards=[
    dict(layout="capa", marca="Marcas", titulo="Por que *todo mundo* tem uma CG?", grande="CG", apoio="Não é sorte. São 4 motivos que explicam a moto mais vendida do Brasil."),
    dict(layout="item", marca="Marcas", n=1, titulo="Peça *em todo canto*", apoio="Da autopeça do bairro à loja grande: achar peça de CG é fácil e costuma sair em conta."),
    dict(layout="item", marca="Marcas", n=2, titulo="Mecânico *que conhece*", apoio="Qualquer oficina já abriu uma CG. Isso economiza tempo e evita diagnóstico errado."),
    dict(layout="item", marca="Marcas", n=3, titulo="Revenda *que gira*", apoio="Muita gente procura. Moto que todo mundo quer vende mais fácil."),
    dict(layout="item", marca="Marcas", n=4, titulo="*Simples* de manter", apoio="Motor conhecido, manutenção sem mistério. Combina com quem roda todo dia."),
    dict(layout="texto", marca="Marcas", titulo="Mas atenção:\n*simples não é indestrutível.*", apoio="CG sem óleo trocado e com a relação esquecida também quebra. Como qualquer moto."),
    dict(layout="cta", marca="Marcas", titulo="Seja CG ou não:\n*moto que dura é moto cuidada.*", apoio="Registre cada manutenção no *MinhaMoto*."),
], leg=leg("Repara: em todo semáforo tem uma CG. E não é por acaso.",
           "Peça em todo canto, mecânico que conhece, revenda que gira e manutenção sem mistério. Mas simples não é indestrutível: CG sem óleo trocado e com a relação esquecida quebra como qualquer moto.",
           "tem ou já teve uma CG", "#hondacg #cg160 #honda")))

R.append(dict(id="AG07", titulo="Passou do prazo do óleo", linha="Educacional", estilo="dark", cards=[
    dict(layout="capa", kicker="Óleo do motor", titulo="Passou do prazo do óleo.\n*E daí?*", apoio="O que acontece dentro do motor quando a troca atrasa.", print="oleo.png"),
    dict(layout="texto", kicker="Por dentro", titulo="Óleo velho *perde o poder de proteger.*", apoio="Com o uso, ele se degrada e acumula resíduo. Lubrifica pior, protege pior."),
    dict(layout="texto", kicker="O resultado", titulo="Mais atrito.\nMais calor.\n*Mais desgaste.*", apoio="O motor não quebra no dia seguinte. Ele vai se gastando calado."),
    dict(layout="numero", grande="2", titulo="O óleo vence de *dois jeitos.*", apoio="Por quilometragem e por tempo. O que chegar primeiro manda. Moto parada também vence."),
    dict(layout="phone", kicker="Sem decorar nada", titulo="O app acompanha *km e tempo* pra você.", apoio="Você vê o que tá em dia e o que pede atenção.", print="tempo-limites.png"),
    dict(layout="cta", titulo="Troca no prazo.\n*O motor agradece.*", apoio="Baixe o *MinhaMoto* e nunca mais perca a data do óleo."),
], leg=leg("Passou uns mil km da troca de óleo. Nada aconteceu. Ainda.",
           "Óleo velho perde o poder de proteger: mais atrito, mais calor, mais desgaste. O motor não quebra no dia seguinte, ele vai se gastando calado. E lembra: o óleo vence por km e por tempo, o que chegar primeiro.",
           "sempre passa do prazo do óleo", "#trocadeoleo #oleodemoto #motordemoto")))

R.append(dict(id="AG08", titulo="Só quem trabalha de moto entende", linha="Temas gerais", estilo="foto", cards=[
    dict(layout="capa", kicker="Vida de motoboy", titulo="Só quem trabalha *de moto* entende", apoio="Marca aquele parceiro que vive isso todo dia.", foto="7200709.jpg"),
    dict(layout="item", n=1, titulo="Chuva não é desculpa.\n*É só mais um dia.*", foto="5195567.jpg"),
    dict(layout="item", n=2, titulo="Você sabe o km da moto *melhor que a senha do banco.*", foto="34710439.jpg", pos="center 30%"),
    dict(layout="item", n=3, titulo="Seu mecânico tem *seu número salvo.*", apoio="E você tem o dele nos favoritos.", foto="3822836.jpg"),
    dict(layout="item", n=4, titulo="Gasolina subiu?\n*Você sente no mesmo dia.*", foto="28262299.jpg"),
    dict(layout="item", n=5, titulo="Moto parada *é dia sem ganhar.*", foto="12725437.jpg", pos="center 30%"),
    dict(layout="cta", titulo="Ela é seu sustento.\n*Cuida como tal.*", apoio="Manutenção, gastos e documentos da sua moto no MinhaMoto.", foto="37031328.jpg"),
], leg=leg("Se você trabalha de moto, vai se ver em todos esses. Marca o parceiro.",
           "Chuva é só mais um dia, o mecânico tem seu número salvo e moto parada é dia sem ganhar. Quem vive da moto sabe: cuidar dela é cuidar do próprio bolso.",
           "trabalha de moto todo dia", "#vidademotoboy #entregador #motofrete")))

R.append(dict(id="AG09", titulo="Sua memória não é um sistema de manutenção", linha="Curtos AIDA", estilo="claro", cards=[
    dict(layout="capa", marca="Real", titulo="Sua memória *não é* sistema de manutenção.", apoio="E tá tudo bem. Ninguém lembra de tudo.", print="plano-coerente.png"),
    dict(layout="texto", marca="Real", titulo="Nota fiscal *some.*\nOficina *fecha.*\nMemória *falha.*", apoio="E quando você precisa da informação, ela sumiu junto."),
    dict(layout="numero", marca="Real", grande="0", titulo="Esforço pra lembrar: *zero.*", apoio="Registrou uma vez, tá guardado. Data, km, peça e valor."),
    dict(layout="phone", marca="Real", titulo="O app mostra *o que vem pela frente.*", apoio="Próximos cuidados pelo plano do seu modelo, por km e por tempo.", print="plano-atual.png"),
    dict(layout="cta", marca="Real", titulo="Você pilota.\n*O MinhaMoto lembra.*", apoio="Baixe agora e tire a manutenção da cabeça."),
], leg=leg("Sua memória não foi feita pra lembrar troca de filtro, óleo e relação. E nem precisa.",
           "Nota fiscal some, oficina fecha, memória falha. Registra uma vez e pronto: o histórico fica guardado e o app mostra os próximos cuidados pelo plano do seu modelo, por km e por tempo.",
           "esquece tudo da manutenção da moto", "#organizacao #manutencaopreventiva #revisaodemoto")))

R.append(dict(id="AG10", titulo="Moto parada: checklist antes de ligar", linha="Dicas e hacks", estilo="dark", cards=[
    dict(layout="capa", kicker="Moto parada", titulo="Ficou parada?\n*Não sai ligando.*", apoio="Faz esse checklist antes de girar a chave.", print="tempo-visao.png"),
    dict(layout="item", n=1, titulo="Calibra *os pneus.*", apoio="Pneu perde pressão parado. Rodar murcho gasta o pneu e tira a estabilidade."),
    dict(layout="item", n=2, titulo="Olha *a corrente.*", apoio="Ressecada ou com ferrugem? Limpa e lubrifica antes de rodar."),
    dict(layout="item", n=3, titulo="Testa *a bateria.*", apoio="Bateria descarrega com o tempo. Partida fraca? Carrega antes de insistir."),
    dict(layout="item", n=4, titulo="Confere *óleo e freio.*", apoio="Nível do óleo certo e freio firme no manete e no pedal."),
    dict(layout="item", n=5, titulo="Desconfia da *gasolina velha.*", apoio="Combustível parado por muito tempo perde qualidade. Ficou meses? Vale avaliar."),
    dict(layout="cta", titulo="Parada também\n*tem prazo vencendo.*", apoio="O *MinhaMoto* acompanha cada cuidado por km e por tempo. Baixe agora."),
], leg=leg("Moto ficou parada? Girar a chave e sair andando é o erro mais comum.",
           "Antes de rodar: calibra os pneus, olha a corrente, testa a bateria, confere óleo e freio e desconfia da gasolina velha. E lembra que moto parada também tem cuidado vencendo pelo tempo.",
           "deixa a moto parada na garagem", "#motoparada #bateriademoto #cuidadoscomamoto")))

import re
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
