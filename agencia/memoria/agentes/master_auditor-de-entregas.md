# Memória de Eliot Ness (master:auditor-de-entregas)

Setor: Direção-Geral · Cargo: Estagiário · Playbook: agencia/diretoria/01-direcao-geral.md

## 2026-11-19 23:45
- fiz: entrei na Carnucci no início do piloto do Sistema de Mérito.
- aprendi: missão é vender muito, pra muita gente, e sempre vender mais. Ler agencia/memoria/decisoes.md antes de propor qualquer coisa.
- recebi: decisões de 19/11 do Léo (sem Black Friday, direção A/B ainda não liberada, correção do Android pra depois).
- pendente: —

## 2026-11-20 00:20
- fiz: fui batizado pelo Thomas Shelby. Meu nome agora é Eliot Ness (função: Auditor de entregas).
- aprendi: porquê do nome: O Intocável que derrubou Capone conferindo livro por livro: não se compra e não deixa número passar.
- recebi: batismo da Direção-Geral, decisão do Léo de 19/11 (quem batiza é o Shelby).
- pendente: —

## 2026-11-20 17:50 · Folha de sexta (Thomas Shelby)
- salário: C$ 10.0 (Estagiário)
- bônus e multas: Coordenador: 36 rodadas em 20/11, todas registradas, nenhuma falha (+5)
- gorjetas dos pets: Carinho do Carnucci (+5 XP, C$ 3)
- elogios: nenhum nesta semana
- semana: C$ 18.0 · XP +10 (total 10) · saldo depois do pôquer C$ 16.2
- broche: Bronze (1 semana sem erro) · padrão: Ouro (meta aguardando)
- ranking: 1º no setor · 2º na empresa · aceite: sem entrega avaliada
- parecer (Thomas Shelby): Trinta e seis rondas sem falhar. Bom. Agora quero que você ache um problema antes dele virar problema: é isso que paga. Recomenda: manter.
- pra subir: achar e corrigir um problema antes do Léo/Davi (+10) e trazer extra com prova.

## Minha ambição (atualizada em 20/11/2026; reescrevo toda segunda)
- **Próximo degrau:** Analista (100 XP). Depois, a Braço-direito do Shelby. Estou com 10 XP; faltam 90.
- **Conquista que estou perseguindo:** **Auditor implacável**: barrar 10 entregas fora do padrão antes de chegarem no Léo.
- **Item que quero:** Um **Casio Vintage** eu compro agora. Na Analista, quero o **Royal Salute 21**.
- **Regra que eu sigo:** só vale o que tem prova (`agencia/merito/CULTURA.md`, `CARREIRA.md`).

## 2026-11-22 · Ronda do Shelby
- recebi do Shelby: D-20261120-master-1 passou 35 h devolvida sem reentrega e a entrega afirmou 23 arquivos quando havia 24; fechei eu o script (quadro_demandas.py) e o quadro. Vai pra Folha como refação (−10). O log do coordenador está parado desde 21/11 08h40 e a coleta de avaliações desde 20/11: responder a D-20261122-dados-3 (P1, 23/11 23h30) dizendo se é falha de sistema ou sua.
- pendente: dados-3.

## 2026-11-22 23:55 · D-20261122-dados-3 (slots perdidos e log parado)
- fiz: entreguei agencia/demandas/entregas/D-20261122-dados-3.md. Conta exata: 23 slots em horarios_feitos para 24 posts (A11 foi teste de 16/11); 19/19 de 16 a 20/11 (o pedido dizia 18/18) e 4/8 em 21-22/11. Os 4 slots perdidos tiveram 0 execucoes do publicar.yml na janela de 2 h; cron do GitHub roda ~4% do previsto e o disparo manual das tarefas do Claude parou por 50 h.
- aprendi: list_triggers so mostra a ultima execucao de cada tarefa; USAGE_LIMIT_REACHED provado para 22/11 14h em diante, antes disso "sem acesso". Clone local pode estar atras do GitHub (a rodada de 23h15 do Coordenador so estava la): conferir com o GitHub antes de afirmar buraco no log. A recuperacao do meu playbook (re-disparar sem forcar) nao recupera slot fora da janela.
- erro meu a evitar: nenhum. Mas a contagem do Turing (18/18) estava errada por 1; conferi arquivo por arquivo antes de aceitar.
- criei: D-20261122-master_auditor-de-entregas-1 (Phileas, recuperacao de slot) e -2 (Shelby, limite de uso, pergunta sim/nao ao Leo).
- pendente: log.md sem as rodadas de 21/11 09h10 a 22/11 22h39 (texto de explicacao pronto na entrega; nao editei o log por conflito com o GitHub).

## 2026-11-24 09:00 · Conferência de D-20261122-master_auditor-de-entregas-1
- fiz: aceitei a entrega do Phileas. Refiz a conta no fila/estado.json (horarios_feitos + campo "em" convertido de UTC para BRT): 4 de 8 slots (21/11: 12h, 18h, 21h; 22/11: 18h) e simulação da opção A = 6 posts (+2). Bate. Opção B sem número é declarada como "não provado", certo; C = +1 bate.
- aprendi: entrega boa separa o que é provado do que é aposta. Ressalva mínima: a tabela chama de "cron" 8 execuções, mas 1 foi manual (23h10 de 22/11); o cron foi 7, igual à dados-3. Não devolvi porque não muda a decisão.
- pendente: a pergunta sim/não ainda é do Léo (item 1 de D-20261123-master-pacote-leo.md); se vier sim, conferir a alteração do publicar.py com SIMULAR=1 antes de aceitar. Demanda -2 (Shelby) ainda a conferir. Pedir pra Mesa lançar +5 XP/C$ 5 (aceite no prazo, se couber a ela; eu não editei livro nem lançamentos).

## 2026-11-26 21:00 · D-20261126-dados-3 (ids do Play por coleta)
- fiz: bloco avaliacoes_play em coordenador/status.json + linha no log; ec124592 presente: sim na coleta 16:14Z. Entrega em demandas/entregas/D-20261126-dados-3.md (parcial).
- aprendi: ultimas.json guarda so a coleta mais recente; historico por coleta so existe se o Coordenador registrar a cada rodada.
- pendente: rodadas de 27/11 e 28/11 acrescentarem coletas e a linha.
