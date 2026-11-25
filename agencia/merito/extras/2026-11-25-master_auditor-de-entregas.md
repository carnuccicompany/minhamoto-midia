## master:auditor-de-entregas · 2026-11-25 03:15
- tipo: risco
- o quê: existem duas tarefas agendadas com o mesmo nome "MM: Leitura da UTMify" e o mesmo horário (7h41 BRT), ambas ativas; no dia 25/11 as duas vão ler o mesmo painel e gravar o mesmo dados/utmify/AAAA-MM-DD.json (conflito de push e leitura em dobro). Sugestão ao dono (Shelby/Léo): manter só uma. Não mexi em nenhuma.
- prova: list_triggers 25/11 03h: trig_01LrrBMciRiMCgxqYi6XnqYe (criada 24/11 21:01 UTC, nunca disparou) e trig_01Crk41K7v444dUQVu9AmNFY (criada 24/11 17:28 UTC, última execução 24/11 20:52 UTC, SUCCEEDED), cron "41 7 * * *" nas duas
