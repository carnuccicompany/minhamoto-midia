# Pacote de 3 perguntas sim/não ao Léo (Shelby, 23/11/2026)

Cobre: D-20261122-mkt_publicador-1, D-20261122-master_auditor-de-entregas-2, D-20261122-dados_relatorio-semanal-1. Só o Léo (ou o Davi) resolve; não decidi nada por eles.

## Contexto com prova
- Posts: 4 de 8 slots saíram em 21 e 22/11 (agencia/demandas/entregas/D-20261122-dados-3.md). Causa provada: 'Posts do horário', Coordenador e Mesa de Demandas falharam por USAGE_LIMIT_REACHED; o cron do GitHub roda bem abaixo do previsto. Cada slot perdido é um carrossel a menos no ar, ou seja, menos alcance pro funil de assinante pago.
- Medição: a chave de sandbox do RevenueCat->AppsFlyer está em branco (PENDENCIAS.md, 19/11). Sem ela o passo 5 (compra sandbox) pode não chegar ao AppsFlyer e o passo 7 do roteiro D+0 (D-20261122-dados-2.md) falha sem o app estar errado. Sem passo 7 provado, verba de tráfego fica em zero e não há custo por assinante.

## As perguntas (responder só sim ou não)
1. **Posts (prazo 23/11 20h):** Posso mudar o publicar.py para o GitHub recuperar sozinho o post do horário perdido (1 por rodada, máximo 4 por dia, janela até 23h59, sem mexer no conteúdo nem na ordem da fila)? Recomendação: sim. Se sim, o Fogg altera e valida com SIMULAR=1; nada vai ao ar além do que já está na fila aprovada.
2. **Limite de uso (prazo 23/11 23h55):** Posso reduzir o Coordenador de 2 rodadas por hora para 1 e manter o disparo dos posts, para o limite de uso não derrubar a publicação? Recomendação: sim. Pedido junto: abrir o histórico de execuções de 'Posts do horário' e do Coordenador entre 21/11 12h e 22/11 14h e dizer o motivo (só o Léo enxerga).
3. **Sandbox (prazo 23/11 14h):** Léo, você preenche a chave de sandbox do AppsFlyer na integração do RevenueCat antes da build de 23/11? Se não, o passo 7 só se prova com compra real de baixo risco, decisão dele.

## Quando chegar a resposta
- 1 sim: Fogg muda o script, valida, Ness confere. 2 sim: mexo nos horários da tarefa e registro em decisoes.md. 3 sim: Dados roda o D+0; não: Dados propõe a compra real e volta ao Léo.
- Levo as três juntas na notificação curta de segunda (regra do playbook: máximo 3 decisões, com recomendação).
