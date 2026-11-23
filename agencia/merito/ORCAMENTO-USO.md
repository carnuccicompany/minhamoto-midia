# Orçamento de uso dos agentes

> Criado em 23/11/2026. O plano é o **Max compartilhado** (Léo e Davi na mesma conta). O **limite semanal renova domingo às 23h**. Em 22/11 a tarefa "MM: Posts do horário" falhou às 21h02 por limite de uso (`USAGE_LIMIT_REACHED`): é o aviso de que o consumo tem que ser planejado.
> Este arquivo só documenta e recomenda. **Nenhuma tarefa é alterada sem o OK do Léo.**

## Tarefas agendadas (estado em 23/11/2026)

| Tarefa | Quando | Modelo | Rodadas/semana | Peso |
|---|---|---|---|---|
| MM: Coordenador 24h · :09 | toda hora | Sonnet | 168 | leve (cada uma), **pesado no total** |
| MM: Coordenador 24h · :39 | toda hora | Sonnet | 168 | leve (cada uma), **pesado no total** |
| MM: Posts do horário (Insta/Face) + aviso TikTok | 12h02, 15h02, 18h02, 21h02 | Sonnet | 28 | leve |
| MM: Respostas às avaliações das lojas | 9h13, 13h13, 17h13, 21h13 | Sonnet | 28 | leve |
| MM: Vigia do Gmail | 8h47, 13h47, 18h47 | Sonnet | 21 | leve |
| MM: Resumo da caixa (Moneypenny) | todo dia 7h53 | Opus | 7 | leve |
| MM: Mesa de Demandas | 10h37 e 14h37 | Sonnet | 14 | **pesado** (até 10 subagentes por rodada) |
| MM: Reunião do Conselho | todo dia 19h23 | Sonnet | 7 | **pesado** (7 diretores + réplicas + Shelby + Mesa) |
| MM: Relatório semanal de resultados (Hemingway) | segunda 8h26 | Opus | 1 | médio |
| MM: Plano da semana (Shelby) | segunda 8h41 | Sonnet | 1 | médio |
| MM: Relatório das lojas (Bezos) | segunda 10h23 | Sonnet | 1 | médio |
| MM: Radar de mercado semanal (Greco) | terça 9h37 | Opus | 1 | médio |
| MM: Folha de sexta | sexta 17h47 | Opus | 1 | **pesado** |
| MM: Fechamento da semana (Shelby) | sexta 19h17 | Sonnet | 1 | médio |
| MM: Fechamento do mês | dia 1, 9h17 | Opus | ~0,25 | pesado |
| MM: Cadeira em disputa | trimestral | Opus | ~0 | médio |
| Robôs do GitHub (coletar dados 4x/dia, publicar, insights) | GitHub Actions | — | — | **não gastam o plano do Claude** |

**Total: ~448 rodadas por semana**, das quais **336 (75%) são do Coordenador**.
Além das tarefas, o plano é dividido com o uso ao vivo: esta conversa (QG), o Estúdio Audiovisual (Opus, pesado: vídeo e imagem) e o Claude Code do Davi.

**As 3 que mais pesam:** Reunião do Conselho (diária, com muitos subagentes), Mesa de Demandas (2x/dia, com subagentes) e o Coordenador (pouco por rodada, mas 336 vezes por semana).

## Regras de modelo
- **Opus só onde a qualidade decide:** Estúdio Audiovisual (criação), análise semanal (Hemingway, Radar), Folha de sexta e Fechamento do mês.
- **Sonnet no resto:** rotinas, vigias, coordenação, Conselho e Mesa.
- Pendente de ajuste (precisa do Léo, o sistema não deixou o Claude trocar): o **Resumo da caixa (Moneypenny)** está em Opus e deveria estar em Sonnet. É só trocar o modelo na configuração da tarefa.

## Se o limite apertar: ordem de corte
Corte de cima pra baixo, um degrau por vez, e volte quando o limite renovar (domingo 23h):
1. **Coordenador:** de 2 por hora (:09 e :39) para 1 por hora (pausar o :09). Economiza ~168 rodadas/semana sem perder vigilância relevante.
2. **Respostas às avaliações:** de 4x para 2x por dia (9h13 e 17h13).
3. **Mesa de Demandas:** de 2x para 1x por dia (só 10h37), já que o Conselho também roda uma Mesa às 19h23.
4. **Vigia do Gmail:** de 3x para 2x (8h47 e 18h47); o Resumo da caixa das 7h53 cobre a manhã.
5. **Conselho:** só com o OK do Léo, rodar em dias alternados (seg, qua, sex).

**Nunca param:** Posts do horário (publicação e aviso do TikTok), Vigia do Gmail (pelo menos 1x/dia), a Reunião do Conselho (salvo decisão do Léo), Folha de sexta e a vigia de segredos do Coordenador (segurança é prioridade máxima).

## Como medir
- O **Coordenador**, em toda rodada, olha o `last_run` de cada tarefa (list_triggers). Se alguma falhou com `failure_reason` = `ROUTINE_RUN_FAILURE_REASON_USAGE_LIMIT_REACHED`, registra em `agencia/coordenador/log.md`: data, hora, tarefa, e quanto faltava pro limite renovar.
- Duas falhas por limite na mesma semana: o Coordenador avisa o Léo no celular com a recomendação do próximo degrau da ordem de corte.
- O **Shelby** revisa este arquivo no **Fechamento da semana (sexta)**: quantas falhas por limite, quais tarefas e se a ordem de corte precisa mudar. Anota a decisão em `agencia/memoria/decisoes.md`.
