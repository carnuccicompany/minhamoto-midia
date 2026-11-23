# D-20261122-master_auditor-de-entregas-1 · Recuperar slot perdido no publicador: 3 opções com número

Autor: Phileas Fogg (mkt:publicador) · 23/11/2026 (10h40 BRT) · Fontes: `scripts/publicar.py`, `.github/workflows/publicar.yml`, `fila/estado.json`, execuções do workflow (`gh run list`, repo público) e a entrega `D-20261122-cria-1.md`. Nada foi alterado em `scripts/`.

## Resumo em 3 linhas
- O gargalo é o número de execuções do workflow, não o script: em 21 e 22/11 houve 8 execuções no total (+2 depois, de madrugada) e 4 delas postaram. Só a opção A (script recupera slot aberto do dia) transforma execução "sem slot" em post.
- Simulando A sobre as execuções reais de 21 e 22/11: 6 posts em vez de 4 (+2). B (mais crons) não tem como ser provada: o GitHub já rodou só 8 dos 192 disparos previstos em 48 h. C (forçar na mão) salva no máximo 1 e depende de alguém acordado.
- Recomendo A, com trava de 90 min entre posts. Pergunta sim/não no fim.

## Base real (horário de Brasília)
Execuções do `publicar.yml` de 21/11 a 23/11 (run id, evento, hora):

| Dia | Execuções (hora BRT) | Postou |
|---|---|---|
| 21/11 | 05:50 (44886756816), 13:26 (44924591759), 18:49 (44953525689), 22:41 (44972653541) | 13:26 M05, 18:49 A01, 22:41 DV21 |
| 22/11 | 05:53 (45004899085), 14:02 (45047201835), 19:24 (45077532096), 23:10 manual (45098696529) | só 19:24 E08 |
| 23/11 | 00:01 (45103530060), 09:12 (45172069147) | nada (fora de horário) |

Hoje o script só publica se a hora está em [slot, slot+2h) e o slot não consta em `horarios_feitos`. Resultado: 21/11 15h, 22/11 12h, 15h e 21h perdidos (a execução de 14:02 caiu 2 min fora da janela das 12h; a de 23:10 caiu 10 min fora da janela das 21h).

## Opção A · Janela até 23h59 do mesmo dia, publica o slot aberto mais antigo (máx. 1 por execução, 4 por dia)
- Mudança: em `publicar.py`, trocar "slot = o da janela de 2 h" por "slot aberto = o mais antigo de hoje, das 12h até agora, ainda fora de `horarios_feitos`". Mantém 1 post por execução, 4 por dia, ordem da fila e conteúdo. Não atravessa a meia-noite.
- Simulação nas execuções reais (só conta execuções que existiram):
  - 21/11: 13:26 vai pro slot 12h, 18:49 vai pro slot 15h (hoje vai pro 18h), 22:41 vai pro slot 18h. Total 3, igual ao real (3). Ganho 0, porque houve só 3 execuções úteis. O 21h fica sem post.
  - 22/11: 14:02 publica o slot 12h (hoje: nada), 19:24 publica o 15h, 23:10 publica o 18h (hoje: nada). Total 3, real 1. Ganho +2.
  - Soma 21 e 22/11: **6 posts, real 4: +2**. Ficam sem post 2 de 8 slots (21/11 21h, 22/11 21h) por falta de execução, não por regra.
- Risco: o post sai fora do horário nobre (o das 12h saindo às 14h, o das 18h às 23h). Dois posts muito juntos se duas execuções caírem em sequência; mitigação: trava de 90 min desde o último post (`em` do último item de `publicados`). Zero risco de duplicar: o slot recuperado entra em `horarios_feitos`.
- Validação possível sem publicar: `SIMULAR=1` com data/hora simulada. Custo: ~20 linhas.

## Opção B · Disparo extra do cron em xx:02 e xx:32 das 12h, 15h, 18h e 21h (editar o cron do workflow)
- Mudança: acrescentar ao `schedule` as horas 15,18,21,00 UTC nos minutos 2 e 32.
- Posts que teria salvo em 21 e 22/11: **não dá para provar**. O cron do GitHub rodou 8 vezes em 48 h para 192 previstos (intervalos de 4 a 8 h). Os minutos 7,22,37,52 já eram pedidos e quase nunca vieram; pedir mais minutos não muda o ritmo de entrega do GitHub. Pode salvar 0 ou alguns; não invento número.
- Risco: baixo (nada duplica pelo controle de slot), mas é aposta sem evidência.
- Serve como complemento de A, não como solução.

## Opção C · Backfill manual com `forcar` limitado a 1 post por slot perdido
- Hoje `forcar=1` ignora horário e não grava `horarios_feitos` fora de slot, então o mesmo slot pode ser "forçado" duas vezes.
- Posts que teria salvo: a única execução manual do período foi a de 22/11 23:10 sem `forcar`. Com `forcar`, teria salvo **1** (o do 21h de 22/11, às 23h10). Os outros 3 slots não tinham ninguém disparando, então 0.
- Risco: depende de alguém ativo na hora, post fora de hora, e precisa de trava para não passar de 4/dia. Mexer no script também.

## Comparação
| Opção | Posts salvos em 21 e 22/11 | Precisa de gente? | Mexe em `scripts/` | Risco |
|---|---|---|---|---|
| A | +2 (6 de 8) | não | sim (~20 linhas) | post fora do horário nobre; trava de 90 min cobre |
| B | não provado (0 a ?) | não | não (só workflow) | aposta; GitHub já ignora a maioria dos disparos |
| C | +1 | sim | sim | depende de pessoa; hora errada |

Limite que nenhuma opção resolve: se não houver execução, não há post. A causa raiz provável (tarefa "MM: Posts do horário" falhando por limite de uso) continua precisando do Léo/Davi, como em `D-20261122-mkt_publicador-1`.

## Situação de hoje
23/11 10h40: nenhum slot perdido ainda (12h abre em 1 h 20 min). A última execução do cron foi 09:12; vou conferir a de 12h e registrar run id.

## Pergunta para o Léo/Davi (sim/não)
Posso mudar o `scripts/publicar.py` para recuperar o slot aberto mais antigo do dia (máx. 1 por execução, 4 por dia, trava de 90 min entre posts, até 23h59, sem mexer em conteúdo ou ordem da fila)? Recomendo sim.
