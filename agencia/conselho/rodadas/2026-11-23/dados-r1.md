# Alan Turing (Dados e Finanças) · Rodada 1 · 23/11/2026

**(a) Fios.** F-001 (SDK e eventos): 3 reuniões sem resposta do Davi, então digo parado. D-20261123-dados-2 (banco do app guarda onboarding e moto?) sai do mesmo silêncio. Sem isso, medição antes do paywall é cega. F-005: 1 de 3 no Play é pista, não padrão; o Play caiu de 3 para 2 avaliações entre 20 e 23/11 (`ultimas.json`) e a média de 3,67 era foto de janela móvel. F-006: o coordenador voltou (rodada 19h12 ok, `coordenador/status.json`), mas 4 slots de 21 e 22/11 ficaram perdidos. F-002 e F-004: sem opinião de dados.

**(b) Número da semana.** Novos pagantes e % da meta: sem número (`metas.json` pct nulo; RevenueCat não lido nesta sessão; `carnucci-dados` fora do alcance). O que eu medi e é novo: os insights por post voltaram (coleta de 23/11, `erros` vazio). Nos 26 posts de 16 a 23/11: mediana de alcance = 0,7% dos seguidores por post, 0 salvamentos, 1 compartilhamento, 5 interações no total (`dados/insights-2026-11-23.json`). Hemingway escreveu "zero métrica" às 8h26, estava certo na hora e agora está velho. O alcance da conta em 28 dias é ordem de grandeza maior que a soma dos posts de feed; a Meta diz que ele inclui anúncio, story e reel ([doc](https://developers.facebook.com/docs/instagram-platform/api-reference/instagram-user/insights)). Não sei de onde vem esse alcance.

**(c) Iniciativa: "De onde vem o alcance?" em 7 dias.** Hipótese: o feed orgânico de carrossel não carrega a meta; o alcance real vem de outro formato (story, reel ou anúncio) e é lá que dobrar. Número esperado: % do alcance de 28 dias por formato (AD, FEED, REELS, STORY) até 30/11, e a linha de base do funil por etapa na semana da build, como já prometi. Mexe na meta porque diz onde pôr a próxima hora e o próximo real. Precisa: coletor com breakdown (dados-4), coleta diária (dados-5), Davi no SDK (F-001).

**(d) Demandas criadas (3).**
- `D-20261123-dados-4` → Hemingway: placar refeito com insights e alcance por formato. P1, 24/11 21h.
- `D-20261123-dados-5` → Shelby: aprovar coleta diária do insights.yml (hoje só domingo). P2, 26/11.
- `D-20261123-dados-6` → Escobar (cópia Dados): proposta de teste pago mínimo, sem gastar. P2, 26/11.

**(e) Cobranças.** Eu cobro o Davi: D-20261120-dados-2 (venceu 21/11) e D-20261123-dados-2, via Shelby (D-20261122-dados-1, venceu hoje 12h, bloqueada pro líder). Cobro o Léo: D-20261123-dados-1 (leitura RevenueCat e lojas, 25/11) e D-20261122-ted-1 (nota do Play). Me atrasam por falta de dado: cria-2, mkt-1, lojas-3, mercado-3, todas bloqueadas, nenhuma vencida por culpa minha. Eu devo D-20261123-lojas-1 (30/11).

**(f) Equipe.** Hemingway entrega: master-2 e dados-2 aceitas, consertou o coletor (`scripts/insights.py`) e achou o vazamento de token ele mesmo. Deve: o placar novo (dados-4). Coletor, funil e anomalias seguem na reserva; o alerta de anomalia só volta com número diário.

**(g) Perguntas pro Léo.** 1) Posso ter leitura de RevenueCat, App Store Connect e Play Console (sim/não)? 2) A conta já rodou anúncio, boost ou story/reel nos últimos 28 dias (sim/não)? 3) Qual o alvo semanal de novos pagantes (só em %, do degrau 1)?
