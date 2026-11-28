# D-20261126-mkt_publicador-1 · publicar.py recupera o slot aberto do dia

Autor: Phileas Fogg (mkt:publicador) · 27/11/2026 · Autorização: resposta do Shelby na própria demanda (27/11, correção de erro, só peças já aprovadas da fila, sem dinheiro). Nada foi publicado, nenhum run real foi disparado, `fila/estado.json` não foi alterado.

## O que mudou em `scripts/publicar.py`
- Antes: só publicava se a hora caísse em [slot, slot+2h). Execução atrasada além de 2 h perdia o slot (caso de 21/11 e 22/11, e provável em 24 e 26/11).
- Agora: slot aberto = horário de hoje (12h, 15h, 18h, 21h BRT) que já começou e não está em `horarios_feitos`. O script publica o mais antigo.
- Garantias (conforme o pronto_quando):
  - máx. 1 post por execução (o script já publica um carrossel e sai);
  - máx. 4 por dia: cada post consome um horário em `horarios_feitos`, então não existe 5º;
  - ordem da fila intacta: continua `próximo = primeiro da fila ainda não publicado`;
  - nunca de dia anterior: a lista de slots é montada só com a data de hoje em BRT; à 00h do dia seguinte os slots de ontem não reabrem;
  - `FORCAR=1`, `pausado`, redes e publicação em si: sem alteração.
- Removida a constante `JANELA_H` (não é mais usada). Acrescentado `AGORA_BRT` só com `SIMULAR=1`, para testar sem esperar a hora.

## Validação com SIMULAR=1 (saída real, cópia de scripts/ e fila/ fora do repositório)
Estado de partida: 27/11 sem slots feitos.

| Hora simulada (BRT) | feitos hoje | Resultado |
|---|---|---|
| 27/11 11:30 | nenhum | "Nenhum horário aberto". Nada |
| 27/11 14:02 | nenhum | slot aberto 12h, próximo E07 (antes: nada, fora da janela) |
| 27/11 19:24 | nenhum | slot aberto 12h (recupera o mais antigo) |
| 27/11 23:10 | nenhum | slot aberto 12h |
| 27/11 14:02 | 12h | nada (15h ainda não começou) |
| 27/11 15:10 | 12h | slot 15h |
| 27/11 19:00 | 12h, 15h, 18h | nada |
| 27/11 21:05 | 12h, 15h, 18h | slot 21h |
| 28/11 00:10 | (estado de 27/11) | nada: não recupera dia anterior |
| 28/11 12:03 | (estado de 27/11) | slot 28/11 12h |
| 27/11 22:00, estado real | 12h, 15h, 18h, 21h | nada (4/4 do dia) |

Ordem da fila: nos 6 casos que publicariam, o próximo foi sempre E07 (primeiro pendente). Sintaxe do arquivo conferida (`ast.parse`).

## Efeito esperado (do estudo de 23/11)
Sobre as execuções reais de 21 e 22/11: 6 posts em vez de 4 (+2). Limite que continua valendo: sem execução do cron/tarefa, não há post (24/11 18h teve zero execuções na janela). A causa "limite de uso das tarefas agendadas" segue com o Léo/Davi, e o last_run de "MM: Posts do horário" de 26/11 18h ainda falta.

## Risco e como reverter
- Post pode sair mais tarde que o horário nobre (ex.: o das 12h às 14h). Não há trava de 90 min entre posts: duas execuções seguidas com 2 slots abertos publicam 2 posts em sequência (um por execução). Se ficar ruim, proponho a trava (não estava autorizada, não pus).
- Reverter: restaurar a janela de 2 h (`inicio <= agora < inicio + 2h`).

## Como provar em produção (F-006)
Próxima rodada: `horarios_feitos` de 28/11 com 4 de 4 e o run id de cada. F-006 fecha com 3 dias de 4/4. Não afirmo ganho antes disso.
