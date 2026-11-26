## mkt:publicador · 2026-11-26 12:08
- tipo: risco
- o quê: A cobrança de 30 min do TikTok não é criada nas rodadas agendadas: o create_trigger exige aprovação do usuário e é recusado sem ninguém no chat; sem a cobrança, o Léo só recebe o aviso do horário. Sugestão: o Léo criar uma tarefa recorrente de lembrete (+30 min de cada rodada) ou aprovar a criação.
- prova: rodada de 26/11 12h02 (Brasília): create_trigger "Cobrança TikTok 12h" retornou "this call was not run ... needs the user's approval".
## mkt:publicador · 2026-11-26 12:08
- tipo: ideia
- o quê: Fila com 77 carrosséis pendentes (113 no total, 36 publicados) a 4 posts/dia dura ~19 dias; produzir novos carrosséis (principalmente S e E) antes de ~13/12 evita a fila zerar.
- prova: fila/carrosseis.json × fila/estado.json: 113 − 36 publicados = 77 pendentes após o J05 de 12h.
## mkt:publicador · 2026-11-26 15:06
- tipo: risco
- o quê: A cobrança de 30 min do TikTok falhou de novo (2ª rodada seguida): create_trigger recusado por exigir aprovação do usuário em execução agendada; 2 de 2 cobranças do dia não foram criadas, então o Léo só recebe o aviso do horário.
- prova: rodada de 26/11 15h02 (Brasília): create_trigger "Cobrança TikTok 15h" retornou "this call was not run ... needs the user's approval".
## mkt:publicador · 2026-11-26 15:06
- tipo: melhoria
- o quê: Fila agora com 76 carrosséis pendentes (37 publicados de 113) após o A04; próximo é DV09. Ritmo de 4/dia esgota em ~19 dias (cerca de 15/12).
- prova: fila/estado.json (A04 publicado 2026-11-26T18:04Z) × fila/carrosseis.json (113 itens).
