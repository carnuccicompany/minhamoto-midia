## dados:relatorio-semanal · 2026-11-23 08:40
- tipo: melhoria
- o quê: o coletor `scripts/insights.py` passou a gravar a mensagem da Meta nos erros. Saiu do "400 Bad Request" sem causa pra causa exata: falta a permissão `instagram_manage_insights` no token (código #10). `page_impressions`, que foi descontinuada, virou `page_media_view`.
- prova: commits 9898c65 e 89ba271; `dados/insights-2026-11-23.json` (`erros.ig_alcance_28d` e `insights_erro` com `(#10) Application does not have permission`).

## dados:relatorio-semanal · 2026-11-23 08:40
- tipo: risco
- o quê: o token da Meta foi gravado no repositório público pelos links de paginação da resposta. Isso foi efeito colateral da minha troca de métrica. Removi, bloqueei `paging`, pus uma trava que aborta a gravação se o token aparecer e avisei o Léo pra revogar. O token segue no histórico do git até ser revogado.
- prova: commit 35f294d (vazou) e 178b0ba (removido + trava); notificação ao Léo em 23/11 11:3x UTC.

## dados:relatorio-semanal · 2026-11-23 08:40
- tipo: risco
- o quê: o ritmo de publicação caiu de 100% dos horários (16-20/11) pra 50% (21-22/11) e 4 posts saíram 50 a 140 min atrasados. Se seguir assim, a fila dura mais, mas o feed perde 1 em cada 2 slots. Já está em D-20261122-dados-3 (Ness) e D-20261122-cria-1 (Fogg).
- prova: `fila/estado.json` (`horarios_feitos` sem 21/11 15h, 22/11 12h, 15h e 21h; M05 16:27Z, A01 21:50Z, DV21 01:42Z, E08 22:25Z).
