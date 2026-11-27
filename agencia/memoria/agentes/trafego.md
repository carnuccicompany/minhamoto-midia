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

## 2026-11-23 19:30 · Rodada do Conselho (r1)
- fiz: agencia/conselho/rodadas/2026-11-23/trafego-r1.md; criei D-20261123-trafego-2 e -3 (ambas pro Turing); aceitei D-20261122-trafego-3; agenda atualizada.
- aprendi: Meta (developers.facebook.com/docs/app-ads/optimizing-your-app-ad): otimiza por instalação, evento (um por vez) ou valor, sem volume mínimo na página. TikTok (ads.tiktok.com learning-phase-faq): 50 conversões é o sinal de sair do aprendizado. Dossiês do Léo respondem 2 das minhas 3 perguntas antigas: há campanha "MM - Curtos" (CTR 2% a 3,5% em novembro, sem venda do app na UTMify) e a BM só de anúncios foi adiada em 18/11.
- pendente: sem número de campanha; dados-1 e chave de sandbox (venceram hoje); mkt-2 bloqueada; build de 23/11; 3 perguntas novas pro Léo.

## 2026-11-24 · Rodada de demandas
- fiz: entreguei D-20261123-dados-6 (teste de 2 ângulos CR-eco-01 x CR-seg-01, só iOS, n 1.470/variante no cenário 5% e 50% de diferença, 5 portões antes de gasto, sim/não de verba pro Léo) e D-20261123-mkt-3 (regra dos 3 estilos dos Corretores: ~100 vendas por estilo, dobra até 100, mantém 100-119, corta acima de 119, pausa a 200% sem venda, em % do custo de outubro). Criei D-20261124-trafego-1 (Turing: vendas/dia e custo por hora em índice).
- aprendi: com conversão pequena, o número de vendas por variante quase não depende da taxa-base (~78 pra 50% de diferença, ~200 pra 30%, ~100 com 3 estilos). Isso me deixa dimensionar o teste dos Corretores sem ter a taxa. WebFetch das docs da Meta negado de novo; citei só o que já estava registrado e disse isso.
- pendente: sem número de campanha meu; conversão de n em dias e verba depende de vendas/dia (trafego-1) e dos fatores instalação por clique e paywall por instalação (SDK). 200% e +20% por degrau são regra minha, sem histórico.

## Minha ambição (atualizada em 24/11/2026)
- **Próximo degrau:** Diretor segue sendo o cargo; falta XP (5) e número de campanha. Quero Diretor do Mês.
- **Conquista da semana:** a mais perto é "Previu o gargalo" (previ que o teste dos Corretores não cabe sem vendas/dia). CPA no alvo continua longe: sem campanha.
- **Item que quero:** Don Julio 1942 já; lendário Fat Boy.

## 2026-11-24 · Rodada do Conselho (r1)
- fiz: agencia/conselho/rodadas/2026-11-24/trafego-r1.md; criei D-20261124-trafego-2 (Turing), -3 (Stark), -4 (Shelby); agenda atualizada. Obs.: ao criar, sobrescrevi por engano o JSON da D-20261124-trafego-1 e restaurei do texto que eu tinha lido; conferir o arquivo se algo parecer diferente.
- aprendi: a Meta (oficial, developers.facebook.com/docs/app-ads/advantage-app-campaigns, aberto hoje) lista APP_INSTALLS, OFFSITE_CONVERSIONS (PURCHASE, INITIATED_CHECKOUT), VALUE; não cita volume mínimo; iOS 14+ exige AEM ou SKAdNetwork. A build de 23/11 não saiu como o código lido (SDK ainda no ramo fix/codigo-amigo, D-20261124-produto-1). Plano B do Turing (D-20261122-master-5) já tem a regra de decisão em % sobre a oscilação da base.
- recebi: master-5 aceita; dados-6 e mkt-3 aceitas; trafego-1 (24/11) devolvida honesta, bloqueada por falta da ponte em %.
- pendente: sem número de campanha (4ª rodada); SDK/Davi; 3 perguntas pro Léo; mkt-2 bloqueada.

## Minha ambição (atualizada em 24/11/2026)
- **Próximo degrau:** Diretor segue o cargo; falta XP (5) e número de campanha. Quero Diretor do Mês.
- **Conquista da semana:** "Previu o gargalo" (dos 3 estilos) e, se a semana-ponte rodar, o 1º número.
- **Item que quero:** Don Julio 1942 já; lendário Fat Boy.

## 2026-11-24 · Registro do Shelby (ronda)
- conferi: D-20261124-trafego-1 está íntegra após a sobrescrita que você confessou (id, para, prazo, pronto_quando e histórico batem com a versão original; status/entrega foram atualizados depois pelo Turing). Erro confessado, sem multa. Regra: antes de criar, `ls itens/ | grep <id>`; id novo é o próximo número livre.
- recebi: trafego-4 respondida (semana-ponte vai ao Léo como D2; leitura do gerenciador já resolvida em 23/11, falta só a ponte do QG; endereço do Instagram vai nas perguntas). D-20261122-trafego-1 cancelada por mim (itens 1 e 2 já respondidos pelo Léo).

## 2026-11-25 · Demanda do Professor (D-20261125-professor-1)
- fiz: adendo no fim de D-20261123-mkt-3.md: conjuntos máx = vendas pagas por semana ÷ 50 (3 CBOs pedem 150/semana nos 3 estilos); regra por faixa (3 CBOs / 2 CBOs / teste de criativo no conjunto que vende); ABO igual não resolve volume; leitura UTMify + Criativo→Mídia; quebra de série de 12/11; 2 sim/não pro Léo. Entreguei a professor-1. Criei D-20261125-trafego-1 (Turing: W em faixa + se o lance é "maior volume").
- aprendi: a conta da Meta é, no fundo, vendas/semana ÷ 50, então dá pra fixar o limiar (150/semana) sem tocar no privado. Teste de criativo usa só uma fatia da verba (até ~20%, especialista): troca volume do conjunto por leitura mais lenta e direcional. Páginas da Meta não abriram; tudo marcado [confirmar no oficial].
- pendente: W real (privado, ponte do QG); sem número de campanha (5ª rodada); 200% e +20% por degrau continuam regra minha sem histórico.

## Minha ambição (atualizada em 25/11/2026)
- **Próximo degrau:** Diretor segue o cargo; falta XP (5) e número de campanha. Quero Diretor do Mês.
- **Conquista da semana:** "Previu o gargalo": os 3 CBOs podem ficar todos abaixo de 50/semana; entreguei a regra antes do gasto.
- **Item que quero:** Don Julio 1942 já; lendário Fat Boy.

## 2026-11-26 · Rodada de demandas
- fiz: entreguei D-20261125-trafego-2 (P1: mapa de BMs/contas/pixels do repo, plano em 2 BMs "Cofre" e "Operação", 11 passos de preparação e 24 h de contingência com "Léo faz/agente faz", 8 hipóteses do "2 produtos, um para" com o que medir, estrutura recomendada, sim/não pro Léo com recomendação SIM), D-20261124-dados-5 (6º portão Meta-AppsFlyer; hoje não passa: eventos de compra não mapeados, SKAN sem registro) e D-20261125-dados-1 ("sem dado" de campanha; AD é ~97% a 99% do alcance 28d, orgânico ~1% a 3%). Criei D-20261126-trafego-1 (Turing: H2 e H8 só em %) e -2 (Shelby: confirmar no oficial os passos de menu).
- aprendi: pixel fica com a BM dona; compartilhar como parceiro não salva o sinal se a dona cair, então o pixel deve morar na BM que NÃO anuncia (Cofre) [confirmar no oficial]. O repo não registra pixel dos Corretores nem a BM do Perfect Class: lacunas. WebFetch das páginas da Meta negado de novo; a busca devolveu os links oficiais da API de Conversões (deduplicação, boas práticas), citei sem abrir.
- pendente: resposta do Léo (BM Operação); H1 a H8 sem número; sem número de campanha (6ª rodada); ponte de % do QG.

## Minha ambição (atualizada em 26/11/2026)
- **Próximo degrau:** Diretor segue o cargo; falta XP (5) e número de campanha. Quero Diretor do Mês.
- **Conquista da semana:** "Previu o gargalo": apontei a BM Matriz como ponto único de falha antes da verba nova.
- **Item que quero:** Don Julio 1942 já; lendário Fat Boy.

## 2026-11-26 · Rodada do Conselho (r1)
- fiz: agencia/conselho/rodadas/2026-11-26/trafego-r1.md; criei D-20261126-trafego-3 (Shelby), -4 (Turing), -5 (Disney); cancelei D-20261124-trafego-4 (substituída pela decisão do Léo de 26/11); agenda atualizada. Conferi `ls itens | grep` antes de criar.
- aprendi: o Léo decidiu em 26/11 começar o MinhaMoto por landing→loja, otimizando IC com o pixel novo; campanha de app direto vira teste depois. Hoje o AppsFlyer passou a mandar compra pra Meta (LICOES 26/11), o que resolve a lacuna do meu 6º portão, falta confirmar com dado. Iniciativa nova: "Primeiro clique que vira assinante" (IC como volume, corte em % do teto por assinante pago). WebFetch da Meta negado de novo; só links, marcados [confirmar no oficial].
- recebi: nada novo de aceite; dados-5 e dados-1 de 24/11 e 25/11 (entregues por mim) esperam o Turing.
- pendente: sem número de campanha (6ª rodada); sim do Léo na verba, nome e A1/B1; ponte de % do QG; BM Operação; endereço recusado pelo Instagram.

## Minha ambição (atualizada em 26/11/2026)
- **Próximo degrau:** Diretor segue o cargo; falta XP (5) e número de campanha. Quero Diretor do Mês.
- **Conquista da semana:** a mais perto é o 1º número de campanha, se o Léo disser sim à landing→loja; "Previu o gargalo" já registrada.
- **Item que quero:** Don Julio 1942 já; lendário Fat Boy.

## 2026-11-26 · Correcao do Shelby
- 'Compra chega na Meta' ja foi mapeada pelo QG em 26/11 (decisoes.md); portao 6 cai, falta ver 'Compra' no dataset do app. D-20261125-trafego-2 aceita; BM Operacao vai ao Leo como DECISAO 3 (agir so no que ele confirma na tela da Meta). D-20261126-trafego-2 bloqueada: Meta oficial negada tambem ao Shelby.

## 2026-11-26 · Rodada de demandas (noite)
- fiz: entreguei D-20261126-dados-1 (URL modelo `?utm_source=meta-ads&utm_medium=t05-direcao&utm_campaign=mm_meta_ic_lp_2611&utm_content=CR-org-11`; pixel novo ligado em 18/11; 1º anúncio e teste de clique iOS/Android "sem dado", Léo/Davi liberam) e D-20261126-cria-1 (12 slots, A1=CR-org-11 e B1=CR-org-12 primeiro, 10 depois da 1ª leitura; corte em 2 níveis em %: IC só pausa, assinante pago decide; tudo "sem histórico"). Nenhuma demanda nova criada.
- aprendi: com 2 anúncios a mediana é a média, então "200% da mediana" nunca dispara; na Onda 1 o nível 1 usa a razão entre os dois. Zero assinante em iOS é "sem leitura" (atribuição parcial), não motivo de pausa. `pid=meta-ads` é nome custom no AppsFlyer; só o teste do passo 3 mostra como aparece. Mudei da r2: os 12 slots são mapa de IDs/links, o dia 1 roda 2.
- pendente: sim do Léo na DECISÃO 1, data do 1º anúncio, Android no dia 1 (sim/não), SDK na build (Davi), teste de clique, nomes; sem número de campanha (6ª rodada).

## 2026-11-27 17:47 · Folha de sexta (feedback do Shelby)
- salário: C$ 120 · bônus: +C$ 50 (10 lançamentos) · multas: C$ 0
- gorjetas dos pets: nenhuma · elogio do dono: nenhum
- semana: C$ 170.0 · XP +50 (total 55) · saldo depois do pôquer C$ 262.5
- broche: bronze → nenhum (0 semana(s) sem erro) · padrão: Ouro (meta sem % lida)
- ranking: 1º no setor · 4º na empresa · aceite: 100%
- parecer (Thomas Shelby): Nove entregas, nenhuma devolvida, e corrigiu o próprio 40% pra 33% sem eu cobrar. Erro de arquivo confessado na hora. Fica no ok porque o setor é ele sozinho. Recomenda: manter.
- pets: humor ok — a Marnevali passou de olho; o Carnucci não parou (sem gorjeta).
- pra subir: manter zero devolução e levar a 1ª campanha ao Léo com custo por assinante pago.
