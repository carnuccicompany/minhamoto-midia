# Alan Turing (Dados e Finanças) · Rodada 1 · 24/11/2026

**(a) Fios.** F-001: o Davi segue sem responder; sem SDK a medição antes do paywall é cega, e o plano B (master-5) já está entregue. F-005: o Play caiu de 3 para 1 avaliação em 4 dias (`dados/avaliacoes/ultimas.json`), é janela móvel de ~7 dias (provável, doc do Google bloqueada). Meu 1★ `ec124592` sai da coleta a partir de 26/11 18h35 BRT; sem OK do Léo a resposta se perde (D-20261124-dados-2). F-007: a hipótese "o feed não carrega a meta" ganhou número (abaixo). F-006: coordenador e posts em dia hoje (`coordenador/status.json`). F-002 e F-004: sem opinião de dados.

**(b) Número da semana.** Novos pagantes e % da meta: sem número. `metas.json` tem pct nulo, e faltam o RevenueCat e a ponte de resumo em % do `carnucci-dados`, que esta sessão não alcança. O que eu medi: o alcance 28d da conta variou -0,4% de 23 para 24/11, e os 59 posts de feed explicam no máximo 9,9% dele (`dados/insights-2026-11-24.json`). A mediana de alcance por post foi de 0,57% dos seguidores nos posts de 17 a 24/11, com 2 salvamentos e 1 compartilhamento no total. Nada disso é assinante.

**(c) Iniciativa que eu escolhi: "De onde vem o alcance?" até 30/11.** Hipótese: 90% ou mais do alcance vem de anúncio, story ou reel, não de carrossel de feed. Número esperado: % do alcance 28d por formato (AD, FEED, REELS, STORY) na coleta de 27/11 e, na segunda, o relatório com a série diária. Mexe na meta porque diz onde pôr a hora e a verba para chegar em pagante. Precisa do Davi (ou de quem aplicar) autorizando o patch do `insights.py` (pronto, em D-20261123-dados_relatorio-semanal-1) e de um token para testar. Se ficar em AD ou REELS, dobro a aposta lá; se não existir, o alcance é ruído e a medição de verdade só vem do SDK.

**(d) Demandas criadas (3).**
- `D-20261124-dados-3` → Hemingway (cópia Shelby): minuta do relatório de 30/11 com série de alcance em % e cobertura das 6 etapas. P2, 27/11 19h.
- `D-20261124-dados-4` → Ness (cópia Shelby): linha "insights diário" no status do coordenador, desde 25/11. P2, 27/11 19h.
- `D-20261124-dados-5` → Escobar (cópia Shelby): 6º portão no teste pago, Meta ligada ao AppsFlyer. Sem isso a AppsFlyer conta o anúncio como orgânico ([doc](https://support.appsflyer.com/hc/en-us/articles/360017095198)). P2, 27/11 19h.

**(e) Cobranças.** Cobro o Davi: D-20261120-dados-2 (venceu 21/11), D-20261123-dados-2 e o patch de alcance por formato. Cobro o Shelby: D-20261122-dados-1 (venceu 23/11 12h) e D-20261124-dados-2 (25/11 15h). Cobro o Léo: D-20261123-dados-1 e D-20261122-ted-1. Cobro a Disney: D-20261124-dados-1 (27/11). Me atrasam por falta de dado, nenhuma por culpa minha: trafego-1, mkt-1, lojas-2, trafego-2, mercado-3. Eu devo trafego-3 (30/11), e o Escobar espera o `dados-5` (25/11, o arquivo do cron).

**(f) Equipe.** Hemingway entrega: dados-4 aceita com 26 posts e soma conferidas por mim no JSON. Está devendo a prova da coleta de 25/11 (dados-5, ainda devolvida) e a minuta nova. Ness: lojas-1/24 entregue, mas a coleta de avaliações ficou 3 dias sem rodar sem alerta, e é isso que a dados-4 corrige. Os demais seguem na reserva.

**(g) Perguntas pro Léo.** 1) Aprova a resposta ao 1★ do Play (`ec124592`) até 26/11 12h (sim/não)? 2) O link do anúncio e a integração Meta-AppsFlyer já estão ligados (sim/não)? 3) Posso ter um resumo em % do RevenueCat e do Play (sim/não; se sim, qual o dia da semana)?
