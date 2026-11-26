## mkt:publicador · 2026-11-26 12:08
- tipo: risco
- o quê: A cobrança de 30 min do TikTok não é criada nas rodadas agendadas: o create_trigger exige aprovação do usuário e é recusado sem ninguém no chat; sem a cobrança, o Léo só recebe o aviso do horário. Sugestão: o Léo criar uma tarefa recorrente de lembrete (+30 min de cada rodada) ou aprovar a criação.
- prova: rodada de 26/11 12h02 (Brasília): create_trigger "Cobrança TikTok 12h" retornou "this call was not run ... needs the user's approval".
## mkt:publicador · 2026-11-26 12:08
- tipo: ideia
- o quê: Fila com 77 carrosséis pendentes (113 no total, 36 publicados) a 4 posts/dia dura ~19 dias; produzir novos carrosséis (principalmente S e E) antes de ~13/12 evita a fila zerar.
- prova: fila/carrosseis.json × fila/estado.json: 113 − 36 publicados = 77 pendentes após o J05 de 12h.
