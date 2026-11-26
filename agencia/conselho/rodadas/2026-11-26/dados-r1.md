# Alan Turing (Dados e Finanças) · Rodada 1 · 26/11/2026

**(a) Fios.** F-001: o Davi segue sem resposta no repositório, então SDK e eventos continuam sem prova; a decisão do Léo de hoje (tráfego pra landing, depois loja) me serve: o OneLink da landing já recebe as UTMs, e a AppsFlyer diz que o Smart Script dá "web-to-app attribution" para todas as fontes ([doc](https://support.appsflyer.com/hc/en-us/articles/360000677217)). A página não fala de limite no iOS; o "Android exato, iOS parcial" é registro do Léo (PENDENCIAS l.105), e eu meço isso, não presumo. Aviso: otimizar por IC mede clique pra loja, não assinante; custo por pagante só existe com RevenueCat ÷ gasto. F-005: `ec124592` ainda está na última coleta (`dados/avaliacoes/ultimas.json`, 26/11 16h14Z); minha previsão de saída é depois de 21h35Z, confiro em 27/11. F-007: fechado pelo número abaixo. F-002, F-004, F-006: sem opinião de dados.

**(b) Número da semana.** Novos pagantes e % da meta: sem número. `metas.json` tem pct nulo e o `carnucci-dados` não está acessível nesta sessão (a ponte de resumo em % é pendência do QG). O que medi: alcance 28d da conta +0,05% de 25 para 26/11; anúncio (AD) 98,9% dele, feed 1,8%, story 1,3%, carrossel 1,1%, post 0,7% (soma passa de 100%: mesma pessoa em mais de um formato; REELS sem dado) (`dados/insights-2026-11-26.json`, cron, erros vazio). Nada disso é assinante.

**(c) Iniciativa: "Cobertura da landing até a compra", 1ª leitura 7 dias depois do 1º clique pago.** Hipótese: com a campanha de IC, mais de 80% das instalações do anúncio chegam com origem no Android (meu corte) e bem menos no iOS; o vazamento maior fica entre clique pra loja e compra, não no clique. Número esperado: % de instalações com origem identificada por plataforma, e IC → instalação → compra em %, iOS e Android separados. Mexe na meta porque sem isso o Escobar escala no escuro e o gasto não vira pagante legível. Preciso: data do pixel novo e do 1º anúncio (Léo), UTMs conferidas no OneLink (Escobar), integração Meta-AppsFlyer com compra mapeada (portão 6, hoje não passa), e a ponte de % do QG.

**(d) Demandas criadas (3).**
- `D-20261126-dados-1` → Escobar: URL modelo do anúncio com UTMs no padrão, data do pixel novo e teste de clique a verba zero. P1, 27/11 20h.
- `D-20261126-dados-2` → Shelby: reatribuir `master-1` (está num agente da reserva) e corrigir "teste iniciado" na PENDENCIAS l.105 (app sem teste grátis). P2, 29/11 20h.
- `D-20261126-dados-3` → Ness: registrar no status os ids do Play por coleta, pra provar ou matar a janela de 7 dias. P1, 27/11 20h.

**(e) Cobranças.** Davi: D-20261120-dados-2, D-20261123-dados-2, F-001 (bloqueadas pro líder). Léo: D-20261123-dados-1 e D-20261122-ted-1 (nota do Play). Shelby: D-20261122-dados-1, D-20261124-dados-2 (venceu 25/11 15h). Me travam por falta de dado: trafego-1/2 de 23 a 25/11, mkt-1, lojas-2, mercado-3, mkt-2. Aceito hoje `D-20261125-dados-1` (entregue "sem dado" como o pronto_quando previa). Eu devo: trafego-3 e a linha de base do funil (30/11), produto-5 (01/12).

**(f) Equipe.** Ness entrega: dados-4 aceita, `insights_diario` no `coordenador/status.json` de 25 e 26/11. Hemingway está devendo: `D-20261124-dados-3` voltou hoje às 12h (faltam as linhas de 25 e 26/11, que já existem nos JSONs) e `D-20261125-dados-2` (relatório de 30/11). O coletor (Nightingale) está na reserva e a `master-1` ficou com ele: erro de atribuição, não dele.

**(g) Perguntas ao Léo.** 1) Em que dia entra o pixel novo e vai ao ar o 1º anúncio de IC (data)? 2) Qual a nota e o total de avaliações que o Google Play mostra hoje (ted-1)?
