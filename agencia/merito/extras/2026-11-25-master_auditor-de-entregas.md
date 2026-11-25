## master:auditor-de-entregas · 2026-11-25 03:15
- tipo: risco
- o quê: existem duas tarefas agendadas com o mesmo nome "MM: Leitura da UTMify" e o mesmo horário (7h41 BRT), ambas ativas; no dia 25/11 as duas vão ler o mesmo painel e gravar o mesmo dados/utmify/AAAA-MM-DD.json (conflito de push e leitura em dobro). Sugestão ao dono (Shelby/Léo): manter só uma. Não mexi em nenhuma.
- prova: list_triggers 25/11 03h: trig_01LrrBMciRiMCgxqYi6XnqYe (criada 24/11 21:01 UTC, nunca disparou) e trig_01Crk41K7v444dUQVu9AmNFY (criada 24/11 17:28 UTC, última execução 24/11 20:52 UTC, SUCCEEDED), cron "41 7 * * *" nas duas

## master:auditor-de-entregas · 2026-11-25 06:15
- tipo: risco
- o quê: o insights.yml faz `git push` sem `git pull --rebase` antes; quando outro commit entra no meio, a coleta roda mas o push é rejeitado e o arquivo do dia se perde. Sugestão pro Turing/Shelby: acrescentar `git pull --rebase` antes do push no workflow (não editei, workflow é fora do meu alcance).
- prova: run 45582922021 (25/11 06:11 BRT) salvou dados/insights-2026-11-25.json sem erro e falhou em "! [rejected] main -> main (fetch first)"; o re-disparo seguinte passou. Além disso o cron das 23h41 BRT de 24/11 não rodou (nenhum run "schedule" depois do #7 de 24/11 09:56 BRT).
