# Agenda de Phileas Fogg (mkt:publicador)

## O que quero provar
- 4 de 4 slots por dia, atraso menor que 15 min, com o run id como prova.
- Que a fila nunca seca por surpresa: aviso por linha com a data, a 4/dia e ao ritmo real.

## Metas pessoais
- Voltar a 30 publicações seguidas no horário (a sequência quebrou em 21/11).
- Analista (100 XP): faltam 75 XP.

## Rotina a cada rodada
1. Comparar `horarios_feitos` em fila/estado.json com os slots já abertos; se faltar, dispatch manual dentro da janela de 2 h e abrir aviso com o run id.
2. Conferir `gh run list` do publicar.yml: execuções por dia e atraso do slot.
3. Recalcular dias de fila por linha (fila/carrosseis.json menos estado.json).

## Aguardando
- Léo/Davi: sim/não sobre recuperar slot perdido no publicar.py (D-20261122-mkt_publicador-1) e sobre o limite de uso das tarefas agendadas.
- Disney: plano de reposição por linha (D-20261122-mkt_publicador-2, 25/11).
- Ness: log do coordenador parado desde 21/11 08h40 (D-20261122-dados-3); minha entrega cita as mesmas provas.

- Léo/Davi: mesma pergunta, agora com 3 opções e números em entregas/D-20261122-master_auditor-de-entregas-1.md (recomendo A).

- Léo/Davi: sim/não do publicar.py reaberto em D-20261126-mkt_publicador-1 (24 e 26/11 18h sem post). Léo/Coordenador: last_run de 'MM: Posts do horário' em 26/11 18h02 BRT (prova que falta).
- Próxima rodada: conferir 21h de 26/11 e rodada das 12h de 27/11 em horarios_feitos (lembrar: BRT = UTC-3).

## Ideias guardadas
- Se o script passar a recuperar slot, mostrar no tiktok.html o aviso só quando o post sair de fato.
