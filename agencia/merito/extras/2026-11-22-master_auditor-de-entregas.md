# Extras · master:auditor-de-entregas · 2026-11-22

## Extra 1 · Publicação ficou em 1 de 4 slots em 22/11
- **O que vi:** estado.json mostra só E08 (19h25 BRT) em 22/11; 12h, 15h e 21h ficaram sem post. A tarefa de horário falhou por limite de uso (21h02) e o cron do GitHub rodou às 14h02 sem publicar (fora da janela de 2h do scripts/publicar.py).
- **Prova:** fila/estado.json (24 publicados / 23 horarios_feitos); runs 45047201835 e 45098696529 de publicar.yml; JANELA_H=2.
- **Proposta:** disparar o cron do GitHub às :02 de 12/15/18/21h (e conferir o atraso) em vez de depender só da tarefa do Claude; reforça o plano de 4 posts/dia. Fila segue em 22 dias, sem urgência.
