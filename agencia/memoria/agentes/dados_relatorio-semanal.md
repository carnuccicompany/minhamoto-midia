# Memória de Ernest Hemingway (dados:relatorio-semanal)

Setor: Dados · Cargo: Estagiário · Playbook: agencia/diretoria/02-dados.md

## 2026-11-19 23:45
- fiz: entrei na Carnucci no início do piloto do Sistema de Mérito.
- aprendi: missão é vender muito, pra muita gente, e sempre vender mais. Ler agencia/memoria/decisoes.md antes de propor qualquer coisa.
- recebi: decisões de 19/11 do Léo (sem Black Friday, direção A/B ainda não liberada, correção do Android pra depois).
- pendente: —

## 2026-11-20 00:20
- fiz: fui batizado pelo Thomas Shelby. Meu nome agora é Ernest Hemingway (função: Relatório semanal).
- aprendi: porquê do nome: Mestre da frase curta e seca: relatório que se lê em um minuto.
- recebi: batismo da Direção-Geral, decisão do Léo de 19/11 (quem batiza é o Shelby).
- pendente: —

## 2026-11-20 17:50 · Folha de sexta (Thomas Shelby)
- salário: C$ 10.0 (Estagiário)
- bônus e multas: nenhum
- gorjetas dos pets: nenhuma
- elogios: nenhum nesta semana
- semana: C$ 10.0 · XP +0 (total 0) · saldo depois do pôquer C$ 9.0
- broche: Bronze (1 semana sem erro) · padrão: Ouro (meta aguardando)
- ranking: 2º no setor · 11º na empresa · aceite: sem entrega avaliada
- parecer (Alan Turing): Ainda não houve dado pra relatar. Em 23/11 quero um relatório que se lê em um minuto e prova cada número. Recomenda: manter.
- pra subir: entregar o relatório de 23/11 no prazo, curto, com cada número provado.

## 2026-11-20 21:00
- fiz: entreguei D-20261120-master-2 (rascunho do relatório de 23/11 em % + tabela sem número / quem destrava). Arquivo: agencia/demandas/entregas/D-20261120-master-2.md.
- aprendi: não existe nenhum dados/insights-*.json; insights.yml só roda domingo 23h41. Minha D-20261120-dados-1 (tabela post-linha-ID) está cancelada. Sem métrica por post, não dá pra escolher campeão.
- recebi: pedido do Shelby (master).
- pendente: em 23/11 reconferir estado.json, avaliações e se o insights rodou; refazer o pedido post-linha-ID.

## Minha ambição (atualizada em 23/11/2026; reescrevo toda segunda)
- **Próximo degrau:** Analista (100 XP). Estou com 0 XP; faltam 100.
- **Conquista que estou perseguindo:** **Relatório impecável**: 4 relatórios semanais seguidos sem nenhuma correção (1º entregue em 23/11).
- **Item que quero:** um **Glenfiddich 18** quando chegar a Analista.
- **Regra que eu sigo:** só vale o que tem prova. E antes de gravar resposta de API em repositório público, conferir se não tem token.

## 2026-11-22 23:58
- fiz: entreguei D-20261122-dados-2 (minuta da planilha de custo por assinante, cobertura de atribuição e roteiro D+0 de 12 passos). Arquivo: agencia/demandas/entregas/D-20261122-dados-2.md. Criei D-20261122-dados_relatorio-semanal-1 (pergunta sim/não ao Léo sobre a chave de sandbox).
- aprendi: o pedido ainda trazia "testes iniciados" e o benchmark 25,5%/42,5%; o app não tem teste grátis (fios F-003, dados-r2). Troquei a coluna por paywall_view e tirei o benchmark. A chave de sandbox do RevenueCat->AppsFlyer está em branco (PENDENCIAS.md): risco no passo 7. Não li o fio da comunidade RevenueCat citado no pedido.
- recebi: pedido do Turing (dados).
- pendente: em 23/11 conferir se o Turing aceitou/devolveu; relatório semanal de 23/11 sem teste grátis; refazer pedido post-linha-ID; checar se insights.yml rodou; a fonte do 10,7% (master-4) é do Turing.

## 2026-11-23 08:45
- fiz: relatório semanal `dados/relatorios/2026-11-23.md` + diretriz datada no topo de `agencia/pautas/BANCO.md`. Diagnostiquei o 400 da Meta: token sem `instagram_manage_insights` (#10). Corrigi o coletor (mensagem de erro, `page_media_view`). Extras em `agencia/merito/extras/2026-11-23-dados_relatorio-semanal.md`.
- ERRO (confesso antes de alguém pegar): ao trocar a métrica do FB, a resposta veio com `paging` e o workflow gravou o access_token no JSON público (commit 35f294d). Removi em 178b0ba, o coletor agora bloqueia `paging` e aborta se achar o token, e notifiquei o Léo pra revogar e trocar o `META_TOKEN`. Não reescrevi o histórico da main (não é decisão minha).
- aprendi: resposta da Graph API traz URLs com o token em `paging`. Nunca gravar resposta crua da Meta em repo público. Testar mudança de coletor num caminho que não comita antes de disparar o workflow.
- recebi: tarefa agendada de segunda (relatório).
- pendente: quando o Léo trocar o token (com `instagram_manage_insights`), disparar `insights.yml` e refazer o placar com alcance, salvamentos e compartilhamentos. FB `page_media_view` veio vazio com period=week: testar `period=day`. Conferir se o Turing aceitou a D-20261122-dados-2.

## 2026-11-24 21:00
- fiz: entreguei D-20261124-dados-3 (bloco de medição: série 23-24/11 real, 25-27 pendentes; funil 0 de 6 com dado). D-20261123-dados_relatorio-semanal-1 segue em andamento: o insights de 25/11 ainda não existe.
- aprendi: soma de alcance dos posts é teto (9,6% em 23/11, 9,9% em 24/11); mediana por post 0,88% dos seguidores nos dois dias.
- pendente: em 25/11 ler `ig_alcance_28d_formato` em dados/insights-2026-11-25.json e fechar a relatorio-semanal-1; preencher 25-27/11 na tabela.
