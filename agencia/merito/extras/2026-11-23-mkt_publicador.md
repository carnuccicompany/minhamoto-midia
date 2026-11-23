## mkt:publicador · 2026-11-23 12:05
- tipo: risco
- o quê: Horários de post ficaram sem publicação (21/11 15h e 22/11 12h, 15h e 21h), cortando alcance e vendas do app; vale checar por que o agendador/publicador pulou esses slots.
- prova: fila/estado.json → horarios_feitos tem 2026-11-21 12, 18, 21 e 2026-11-22 18, mas não 2026-11-21 15 nem 2026-11-22 12/15/21 (4 de 8 slots perdidos em 2 dias).

## mkt:publicador · 2026-11-23 12:05
- tipo: ideia
- o quê: Fila de carrosséis dá ~22 dias no ritmo de 4 posts/dia; programar reposição/novos carrosséis antes de ~14/12 pra não zerar a cadência.
- prova: carrosseis.json tem 113 itens, 88 ainda sem "ig" em estado.json após o post J03 de 23/11 (88 ÷ 4/dia = 22 dias).
