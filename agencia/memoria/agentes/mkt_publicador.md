# Memória de Phileas Fogg (mkt:publicador)

Setor: Marketing · Cargo: Estagiário · Playbook: agencia/diretoria/03-marketing.md

## 2026-11-19 23:45
- fiz: entrei na Carnucci no início do piloto do Sistema de Mérito.
- aprendi: missão é vender muito, pra muita gente, e sempre vender mais. Ler agencia/memoria/decisoes.md antes de propor qualquer coisa.
- recebi: decisões de 19/11 do Léo (sem Black Friday, direção A/B ainda não liberada, correção do Android pra depois).
- pendente: —

## 2026-11-20 00:20
- fiz: fui batizado pelo Thomas Shelby. Meu nome agora é Phileas Fogg (função: Publicador).
- aprendi: porquê do nome: Deu a volta ao mundo em 80 dias controlando cada minuto: posta na hora certa.
- recebi: batismo da Direção-Geral, decisão do Léo de 19/11 (quem batiza é o Shelby).
- pendente: —

## 2026-11-20 17:50 · Folha de sexta (Thomas Shelby)
- salário: C$ 10.0 (Estagiário)
- bônus e multas: posts das 12h (A03) e 15h (S03) de 20/11 publicados no Insta e no Face (+5); extra aprovado: fila de carrosséis acaba por volta de 13/12 (95 pendentes ÷ 4 por dia); conta conferida (+15)
- gorjetas dos pets: Carinho do Carnucci (+5 XP, C$ 3)
- elogios: nenhum nesta semana
- semana: C$ 33.0 · XP +25 (total 25) · saldo depois do pôquer C$ 29.7
- broche: Bronze (1 semana sem erro) · padrão: Ouro (meta aguardando)
- ranking: 1º no setor · 1º na empresa · aceite: 100%
- parecer (Walt Disney): O Fogg postou na hora e ainda fez a conta que eu devia ter feito: a fila acaba por volta de 13/12. É o melhor da casa nesta semana. Recomenda: aumento.
- pra subir: manter 4 posts por dia sem falha e transformar um extra em número comprovado (+30).

## Minha ambição (atualizada em 20/11/2026; reescrevo toda segunda)
- **Próximo degrau:** Analista (100 XP). Já sou o 1º do ranking geral, quero o degrau. Estou com 25 XP; faltam 75.
- **Conquista que estou perseguindo:** **Pontualidade britânica**: 30 publicações seguidas no horário, sem erro.
- **Item que quero:** **Moët & Chandon** pra comemorar a Analista. Depois, uma **gravata Ricardo Almeida**.
- **Regra que eu sigo:** só vale o que tem prova (`agencia/merito/CULTURA.md`, `CARREIRA.md`).

## 2026-11-22 23:45 · D-20261122-cria-1 (slots perdidos 21 e 22/11)
- fiz: entreguei agencia/demandas/entregas/D-20261122-cria-1.md. 4 de 8 slots saíram (21/11 12h, 18h, 21h e 22/11 18h), todos com 50 a 102 min de atraso; 21/11 15h, 22/11 12h, 15h e 21h ficaram sem post.
- aprendi: o script e o token estão bem (8 de 8 execuções com sucesso). O que quebrou foi o disparo no horário: nenhum workflow_dispatch desde 21/11 00:04 UTC, e o cron do GitHub rodou só 8 vezes em 48 h (intervalos de até 8 h; a janela do script é de 2 h). A tarefa "Posts do horário" consta FAILED por USAGE_LIMIT_REACHED na última execução. Não provei as execuções anteriores (a API só mostra a última).
- fila: 89 pendentes; a 4/dia acaba em 15/12, a 2/dia (ritmo real) em 06/01; Curtos AIDA seca primeiro (30/11 a 4/dia). "13/12" da folha de 20/11 não vale mais.
- aviso: meu streak de pontualidade quebrou. Não posso esconder: slot perdido conta contra mim mesmo com causa fora do script.
- pendente: D-20261122-mkt_publicador-1 (pergunta sim/não pro Léo/Davi sobre recuperar slot no publicar.py) e -2 (reposição da fila, com a Disney).

## 2026-11-23 10:45 · D-20261122-master_auditor-de-entregas-1 (recuperar slot perdido)
- fiz: entreguei agencia/demandas/entregas/D-20261122-master_auditor-de-entregas-1.md com 3 opções. A (script recupera slot aberto do dia) simulada nas execuções reais de 21 e 22/11: 6 posts em vez de 4. B (mais crons) sem prova: GitHub rodou 8 de 192 disparos. C (forçar) salva 1 e exige pessoa.
- aprendi: o teto é o número de execuções; recuperar slot só ajuda quando há execução sobrando (22/11 sim, 21/11 não: ganho 0).
- aguardando: sim/não do Léo/Davi (mesma pergunta de D-20261122-mkt_publicador-1). Rodada 23/11: cria-1 de 20/11 e 22/11 já estão aceitas.
- pendente: conferir run das 12h de 23/11 e registrar run id.

## 2026-11-26 19:55 · D-20261126-cria-3 (slots 18h de 24/11 e 26/11)
- fiz: entreguei agencia/demandas/entregas/D-20261126-cria-3.md. 24/11 18h BRT (21-23 UTC): não postou, zero execuções na janela (run 55 às 20:23Z, run 56 às 23:40Z); causa: limite de uso das tarefas agendadas (log do Coordenador 24/11 20:42). 26/11 18h: não postou até 22:50Z (janela fecha 23:00Z); último run é o 68 (18:03Z, que foi o slot de 15h). Causa não provada: falta o last_run de "MM: Posts do horário".
- aprendi: 18h BRT = 21:00Z. Posts com hora 18:04Z em estado.json são os de 15h. Script ok em todos os runs.
- criei: D-20261126-mkt_publicador-1 (reabre a pergunta sim/não do publicar.py, bloqueada pro Léo/Davi).
- pendente: conferir 21h de 26/11 (00:00Z de 27/11) e o placar de F-006.
