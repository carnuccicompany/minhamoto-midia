# Alan Turing (Dados e Finanças) · Rodada 1 · 20/11/2026

**(a) Fios:** `memoria/fios.md` está vazio, não há fio aberto. Da ata de 19/11 mantenho o meu: coletor rodado e SDK AppsFlyer. O Shelby me deu bronca com razão: eu disse o que falta e não trouxe o que tem. Hoje trago.

**(b) Número da semana:** não tenho assinante novo, e não vou chutar. `dados/relatorios/index.json` está vazio, não existe `dados/insights-*.json` e o carnucci-dados não abre nesta sessão. O que existe de medido: `fila/estado.json` mostra 19 posts publicados com ID (16 a 20/11), e `coordenador/status.json` mostra 94 na fila. Isso é produção, não venda. `metas.json` segue "aguardando": o Léo não deu o alvo.

**(c) Iniciativa que escolhi: cobertura de atribuição.** Hipótese: o gargalo é medir, não postar (4 posts/dia, 23 dias de fila, zero elo post -> assinatura). Sem isso o Pablo não calcula custo por assinante e eu não faço autópsia com culpado. Número esperado: na 1ª semana após a build de 23/11, medir que % das assinaturas novas chega com fonte identificada. Não prometo valor, o primeiro dado é a linha de base. Preciso de: SDK AppsFlyer na build, UTM padrão, tabela post -> ID, e o Léo ou o Davi disparando o `insights.yml` à mão (`workflow_dispatch`), porque ele só roda domingo 23h41. Como mexe na meta: sem fonte, não sei qual canal dobrar, e dobrar o canal certo é o que sobe assinante novo.

**Benchmark pra comparar quando houver dado** (RevenueCat, State of Subscription Apps 2026): conversão teste -> pago mediana 25,5% em testes de menos de 4 dias e 42,5% em testes de 17 a 32 dias; paywall rígido 10,7% no dia 35, freemium 2,1% ([fonte](https://www.revenuecat.com/blog/growth/subscription-app-trends-benchmarks-2026)). O Stark deve saber qual é o nosso teste; é pergunta 1 abaixo.

**(d) Demandas criadas (3):**
- D-20261120-dados-1 -> Hemingway: tabela post, linha editorial, ID IG/FB, data. P2, 23/11.
- D-20261120-dados-2 -> Stark (cópia produto): confirmar SDK AppsFlyer + RevenueCat na build de 23/11 e lista de eventos. P1, 21/11.
- D-20261120-dados-3 -> Escobar: padrão único de campanha e UTM. P2, 23/11.

**(e) Cobranças:** quadro de demandas está vazio, nenhuma atrasada. Sigo cobrando o SDK (agora tem id: dados-2) e o padrão de UTM (dados-3). Não cobro ninguém por atraso que ainda não existe.

**(f) Equipe:** Hemingway: 0 entregas, sem prova até hoje, pois o relatório só sai em 23/11; dei prazo e demanda dados-1 pra ele ter o que relatar. Os três subagentes de dados (coletor, funil, anomalias) estão na reserva. Peço a volta do coletor só se o `insights.yml` falhar, com o número da falha na mão.

**(g) Perguntas pro Léo:**
1. O teste grátis do MinhaMoto dura quantos dias? (resposta curta)
2. Qual a meta de assinantes pagos novos por semana? O número absoluto vai pro Drive privado.
3. Posso pedir ao Davi para disparar o workflow `insights.yml` hoje? (sim/não)
