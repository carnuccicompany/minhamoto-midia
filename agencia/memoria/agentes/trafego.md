# Memória de Pablo Escobar (trafego)

Setor: Tráfego · Cargo: Diretor · Playbook: agencia/diretoria/05-trafego.md

## 2026-11-19 23:45
- fiz: entrei na Carnucci no início do piloto do Sistema de Mérito.
- aprendi: missão é vender muito, pra muita gente, e sempre vender mais. Ler agencia/memoria/decisoes.md antes de propor qualquer coisa.
- recebi: decisões de 19/11 do Léo (sem Black Friday, direção A/B ainda não liberada, correção do Android pra depois).
- pendente: —

## 2026-11-20 17:50 · Folha de sexta (Thomas Shelby)
- salário: C$ 120.0 (Diretor)
- bônus e multas: entrega no prazo sem refazer: fala no Conselho de 19/11: travou verba sem rastreio fechado e pediu BM de contingência (+5)
- gorjetas dos pets: nenhuma
- elogios: nenhum nesta semana
- semana: C$ 125.0 · XP +5 (total 5) · saldo depois do pôquer C$ 112.5
- broche: Bronze (1 semana sem erro) · padrão: Ouro (meta aguardando)
- ranking: 1º no setor · 2º na empresa · aceite: sem entrega avaliada
- parecer (Thomas Shelby): Não queimar verba às cegas foi certo. Mas cadeira de Tráfego se paga com número de campanha, e não houve nenhum. Recomenda: manter.
- pets: humor fraco — a Marnevali passou acuadinha, de cabeça baixa, e o Carnucci não veio; a Fartuzzi encarou mais tempo atrás da sua cadeira.
- pra subir: trazer número de campanha (CPI, custo por instalação) assim que o rastreio fechar na build de 23/11.

## 2026-11-20 20:00 · Rodada do Conselho (r1)
- fiz: arquivo agencia/conselho/rodadas/2026-11-20/trafego-r1.md; criei D-20261120-trafego-1 (Stark), -2 (Turing), -3 (Disney); agenda própria criada.
- aprendi: AppsFlyer (oficial) diz que a TikTok só otimiza por evento padrão mapeado e recomenda mandar receita; postbacks Meta/TikTok hoje só af_app_opened (PENDENCIAS). Subagentes de Tráfego estão todos em reserva: não recebem demanda.
- pendente: sem número de campanha; esperar build de 23/11; 3 perguntas pro Léo (BM de anúncios, campanha rodando, custo máximo por assinante).

## Minha ambição (atualizada em 20/11/2026; reescrevo toda segunda)
- **Próximo degrau:** Diretor. Quero **Diretor do Mês** e o respeito da mesa.
- **Conquista que estou perseguindo:** **CPA no alvo**: a semana inteira no custo-alvo. Libera a Fat Boy.
- **Item que quero:** O **Don Julio 1942** eu compro já. Lendário: a **Harley-Davidson Fat Boy**.
- **Regra que eu sigo:** só vale o que tem prova (`agencia/merito/CULTURA.md`, `CARREIRA.md`).

## 2026-11-22 20:00 · Rodada do Conselho (r1)
- fiz: agencia/conselho/rodadas/2026-11-22/trafego-r1.md; criei D-20261122-trafego-1 (Shelby), -2 (Bezos), -3 (Turing); bloqueei D-20261120-mkt-2 por falta de acesso de leitura (nada alterado nas campanhas); agenda atualizada.
- aprendi: Meta (oficial, developers.facebook.com/docs/app-ads/advantage-app-campaigns) otimiza campanha de app por instalação, por evento padrão (PURCHASE, INITIATED_CHECKOUT) ou valor; evento custom exige custom_event_type=OTHER; SKAN só iOS 14.5+; sem volume mínimo na página. Corrigi meu erro da r1: Android 1★ era 1 de 3 (33%), não 40%.
- recebi: Disney entregou D-20261120-trafego-3 no prazo (aceita). Resposta do Davi sobre SDK (prazo 21/11 20h) não consta no repositório.
- pendente: sem número de campanha; build de 23/11; teste de OneLink; respostas do Léo (BM, campanha rodando, teto/meta). Subagentes de Tráfego seguem em reserva.

## 2026-11-22 · Ronda do Shelby
- recebi: demanda de correção D-20261122-master-1 (P2, 24/11): tirar 'teste iniciado' e 'X dias grátis' da r1, linha de base em 6 etapas sem teste, fila é 89 e não 93. O 40% de 1★ você mesmo corrigiu pra 33%, bom. Android fora da 1ª campanha vale pelo bug de sincronização, não pela %.
- pendente: entregar a master-1; UTM (dados-3) e trafego-2 vencem 23/11 20h.

## 2026-11-23 · Rodada de demandas
- fiz: entreguei D-20261122-master-1 (correção: sem teste/grátis, fila 89 = 113 menos 24), D-20261120-dados-3 (padrão de UTM: meta-ads/tiktok-ads, mm_<rede>_<evento>_<so>_<aamm>, CR-<ângulo>-<nn> no utm_content) e D-20261122-cria-2 (10 slots, 4 testes, corte em % do custo-alvo). Criei D-20261123-trafego-1 (Léo, sim/não nos nomes; bloqueio lider).
- aprendi: o orgânico (l/README.md) já usa utm_source instagram/tiktok/facebook e utm_campaign=organico; o pago tem que ficar separado. WebFetch dos docs da Meta e do TikTok não abriu hoje (permissão): citei só o que já estava em demanda/entrega, dizendo isso.
- pendente: sem número de campanha; 200%/100% do custo-alvo são regra minha sem histórico, depende do teto do Léo; não consegui ler o doc de UTM do Léo; trafego-2 (minha, vence 23/11 20h) segue com a dados (minuta em D-20261122-dados-2).

## 2026-11-23 13:30 · Conferência de demandas
- fiz: aceitei D-20261120-trafego-2 (dados-2 cobre colunas, roteiro D+0 e dono de cada pendência; sem R$). Ressalva: a tabela de UTM da trafego-2 diverge da minha dados-3 (meta vs meta-ads, cpc_conj01 vs t01-angulo, nome de campanha); pedi um padrão só, o da dados-3, até o Léo responder. D-20261120-dados-3: o arquivo é meu, então não confiro a mim mesmo; deixei 'entregue' para o Turing decidir.
- aprendi: o item dados-3 tem de=dados e para=trafego, mas o entregador fui eu; aceite do próprio trabalho não vale.
- pendente: verba zero até passos 3, 6, 7 do D+0; OK do Léo nos nomes (D-20261123-trafego-1).
