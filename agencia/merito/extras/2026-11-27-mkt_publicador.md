## mkt:publicador · 2026-11-26 21:10
- tipo: risco
- o quê: O CM01 saiu só no Facebook; o Instagram falhou (Graph 9007/2207027 "Media ID is not available": o contêiner do carrossel não estava pronto no media_publish). Como o FB entrou, o horário 21h foi marcado como feito e nenhum retry roda neste horário; o IG do CM01 só será tentado na próxima rodada, tirando o lugar do post seguinte. Sugestão: em publicar_ig, esperar status_code=FINISHED do contêiner (GET /{id}?fields=status_code) antes do media_publish, com até ~5 tentativas de 10 s.
- prova: run 45914499360 (Publicar carrossel, 27/11 00:04 UTC) log "FALHA ig: ... media_publish -> 400 ... 2207027"; fila/estado.json CM01 só com "fb".
## mkt:publicador · 2026-11-26 21:10
- tipo: risco
- o quê: A cobrança de 30 min do TikTok falhou pela 3ª rodada seguida: create_trigger é recusado em execução agendada por exigir aprovação do usuário; 3 de 3 cobranças do dia não foram criadas.
- prova: rodada de 26/11 21h02 (Brasília): create_trigger "Cobrança TikTok 21h" retornou "this call was not run ... needs the user's approval".
## mkt:publicador · 2026-11-26 21:10
- tipo: melhoria
- o quê: Fila com 81 pendentes de 118 carrosséis (37 já publicados) a 4/dia dura ~20 dias (até ~16/12); produzir novos antes disso evita zerar.
- prova: fila/carrosseis.json (118 itens) × fila/estado.json (CM01 sem ig; 81 sem "ig").

## mkt:publicador · 2026-11-27 12:10
- tipo: risco
- o quê: A cobrança de 30 min do TikTok das 12h (DV09) não foi criada: create_trigger é recusado em rodada agendada (exige aprovação do usuário). Já são 4 rodadas seguidas sem cobrança; sugestão: o Léo deixar uma tarefa recorrente de cobrança (cron 12h32/15h32/18h32/21h32 Brasília) criada por ele.
- prova: rodada de 27/11 12h02 (Brasília): create_trigger "Cobrança TikTok 12h" retornou "this call was not run ... needs the user's approval"; fila/estado.json mostra DV09 ig+fb publicado 15:05 UTC.
## mkt:publicador · 2026-11-27 15:10
- tipo: risco
- o quê: a cobrança do TikTok (30 min depois) depende de create_trigger, mas dentro da rodada agendada a criação de tarefa exige aprovação do Léo e foi bloqueada; sem ajuste, o lembrete das 15h não sai.
- prova: create_trigger "Cobrança TikTok 15h" recusado em 27/11 18:10 UTC com "needs the user's approval"; o carrossel E06 (Folga das válvulas) saiu às 18:04 UTC (estado.json).
- pedido de compra (opcional): —

## mkt:publicador · 2026-11-27 15:10
- tipo: ideia
- o quê: a fila tem 78 carrosséis sem IG; a 4 posts por dia dura cerca de 19 dias. Vale reservar tempo pra abastecer a fila antes de 14/12.
- prova: fila/carrosseis.json (118 itens) menos fila/estado.json (40 publicados) = 78.

## mkt:publicador · 2026-11-27 21:10
- tipo: risco
- o quê: a cobrança de 30 min do TikTok das 21h (CM02) também não foi criada; 5ª rodada seguida sem cobrança, porque create_trigger exige aprovação do Léo em rodada agendada. Sem ajuste, nenhum lembrete de 30 min sai.
- prova: create_trigger "Cobrança TikTok 18h" recusado em 27/11 21:0x UTC ("needs the user's approval"); CM02 publicado em 21:04 UTC (fila/estado.json).
