# Agenda de Alan Turing (dados)

## Metas pessoais
- Subir do 2º ao 1º lugar na empresa com número de negócio provado, não com opinião.
- Ter o primeiro funil com dado real (post -> instalação -> assinatura) até a build de 23/11 + 7 dias.
- Não perder a cadeira: sair do "precisa provar" (nota 2) na próxima Folha.

## Apostas
- Atribuição por post/UTM vale mais que qualquer dashboard bonito: sem ela, Tráfego e Criativos votam no escuro.
- Hipótese: o gargalo da meta é medição + etapa teste->pago, não volume de posts (4/dia, 24 dias de fila).

## Iniciativa em curso (atualizada 2026-11-22)
- "Linha de base do funil na semana da build" (23/11 a 30/11): cobertura de atribuicao (% de assinaturas novas com fonte; corte meu 80%) + conversoes instalacao->teste e teste->pago em % contra benchmark RevenueCat. Depende de D-20261122-dados-1 (SDK), D-20261120-dados-3 (UTM), RevenueCat lido, duracao do teste.

## Iniciativa anterior (2026-11-20)
- "Cobertura de atribuição": medir que % das assinaturas novas chega com fonte identificada. Pré-requisito: SDK AppsFlyer (D-20261120-dados-2), UTM padrão (D-20261120-dados-3), tabela de posts (D-20261120-dados-1).

## Pendências
- 22/11: slots de publicacao 50% em 21-22/11 e log do coordenador parado: D-20261122-dados-3 (Ness). Conferir 23/11 se insights.yml rodou (22/11 23h41 BRT).
- Devo ao Escobar: D-20261120-trafego-2 (23/11 20h), minuta com Hemingway em D-20261122-dados-2.
- Perguntas ao Leo: duracao do teste, alvo semanal e custo maximo por assinante, leitura RevenueCat/App Store Connect/Play Console.
- Coletor de insights só roda domingo 23h41 BRT (workflow insights.yml); ainda sem execução manual (precisa do Léo/Davi disparar workflow_dispatch).
- Sem acesso ao carnucci-dados nesta sessão.

## Atualização 2026-11-23
- Plano B de medição entregue (master-5). Se o SDK não entrar na build: leitura só de loja e RevenueCat, regra em % contra a oscilação da linha de base. Gatilho do Plano A: passos 3, 6 e 7 do D+0 passando em iOS e Android.
- Próximo: D-20261122-ted-1 (média do Play), D-20261122-trafego-3 (volume mínimo por variante, P3 29/11), D-20261120-dados-3 (padrão UTM confirmado no D+0).
- Esperando: Davi (F-001, SDK e eventos), Léo (D-20261123-dados-1 e sandbox RevenueCat), Davi (D-20261123-dados-2).
- Meta: 1ª leitura em % por etapa 7 dias após a versão com SDK publicada, iOS e Android separados.

## Atualização 2026-11-23 (noite)
- Entregues: trafego-3 (volume por variante), master-4 (régua 10,7% fora). Bloqueada pro Léo: ted-1 (nota oficial do Play). Criada: D-20261123-dados-3 (histórico de avaliações, lojas, P2 26/11).
- Próximo: cobrar Léo (Play e RevenueCat), Davi (F-001); conferir se Escobar aceitou D-20261120-dados-3; trocar a tabela de volume pela taxa própria quando sair.

## Atualização 2026-11-23 (rodada 1 do Conselho)
- Fato novo: insights por post voltaram (coleta de 23/11, sem erro). 26 posts de 16 a 23/11: mediana de alcance 0,7% dos seguidores, 0 salvamentos. Alcance da conta em 28 dias bem maior que a soma dos posts de feed; a doc da Meta diz que inclui anúncio, story e reel.
- Iniciativa nova: "De onde vem o alcance?" (breakdown por formato até 30/11). A linha de base do funil continua, depende do SDK (F-001).
- Criadas: D-20261123-dados-4 (Hemingway, placar refeito), -5 (Shelby, coleta diária), -6 (Escobar, proposta de teste pago mínimo).
- Esperando: Davi (F-001, dados-2), Léo (dados-1, ted-1). Devo: D-20261123-lojas-1 (30/11).

## Atualização 2026-11-24
- Prazos: 26/11 conferir resposta do Davi sobre o patch do alcance por formato e, se sim, ler por_formato na coleta de 27/11 (23h41 BRT de 26/11); 26/11 21h35 UTC checar se ec124592 sai do Play; 27/11 trafego-1 (preencher com UTMify em % quando a ponte existir); 30/11 trafego-3, cria-2 (leitura só quando o n existir), dados-5 e 1ª linha de base do funil.
- Iniciativa que trago: "De onde vem o alcance?" continua; agora com 59 posts FEED = <=9,9% do alcance e hipótese AD primeiro.
- Aposta: provar a janela de 7 dias do Play com a previsão de 26/11 (conta como "Previu o gargalo" se confirmar).
- Cobrar: Davi (patch insights.py, disparo diário de avaliacoes.yml), Léo (ec124592), Disney (dados-1: V2 = V1 + faixa), Shelby (dados-2).

## Atualização 2026-11-24 (rodada 1 do Conselho, noite)
- Iniciativa: "De onde vem o alcance?" continua. Hipótese: >=90% do alcance 28d vem de AD, REELS ou STORY, não de feed (feed <=9,9%). Prazo 30/11; depende do patch do insights.py e de token.
- Criadas: D-20261124-dados-3 (Hemingway, minuta 30/11), -4 (Ness, linha de insights diário no status), -5 (Escobar, portão Meta-AppsFlyer). Prazo 27/11 19h.
- Conferir 25/11: insights-2026-11-25.json (cron) para aceitar dados-5. 26/11 21h35 UTC: ec124592 sai do Play? 27/11: dados-1 (Disney) e as três de hoje.
- Aposta nova: sem integração SKAN Meta-AppsFlyer, o anúncio aparece como orgânico; vira portão antes da verba.

## Atualização 2026-11-25
- Fato novo: alcance 28d por formato (coleta 25/11): AD 98,8%, feed ~2%. A iniciativa "De onde vem o alcance?" muda de pergunta: de que campanha vem o AD (D-20261125-dados-1, Escobar, 27/11 19h).
- Entreguei master-2 (formato do resumo-pct.json). Espero: QG (ponte), Léo (UTMify), Davi (SDK, evento de moto).
- Prazos: 26/11 21h35Z ec124592 no Play; 27/11 dados-1 (Disney) e dados-1/3/4/5 abertas; 30/11 trafego-3, 1ª linha de base, relatório (D-20261125-dados-2).

## Atualização 2026-11-26
- Fato: alcance por formato estável (AD 98,8% -> 98,9%; feed 2,1% -> 1,8%). relatorio-semanal-1 entregue. Iniciativa segue: de que campanha vem o AD (D-20261125-dados-1, Escobar, 27/11 19h).
- Bloqueado: trafego-1 (W e tipo de lance) até a ponte de % do QG.
- Prazos: 27/11 conferir ec124592 na coleta; 30/11 relatório, trafego-3, linha de base.

## Atualização 2026-11-26 (rodada 1 do Conselho)
- Iniciativa nova: "Cobertura da landing até a compra" (decisão do Léo, 26/11: tráfego pra landing → loja, otimizando IC). Hipótese: >80% das instalações do anúncio com origem no Android (corte meu), menos no iOS; vazamento maior entre clique pra loja e compra. 1ª leitura 7 dias após o 1º clique pago. Precisa: data do pixel novo, UTMs conferidas, Meta-AppsFlyer com compra mapeada (portão 6), ponte de % do QG.
- Criadas: D-20261126-dados-1 (Escobar, P1 27/11 20h), -2 (Shelby: reatribuir master-1 da reserva e corrigir "teste iniciado" na PENDENCIAS l.105, P2 29/11), -3 (Ness: ids do Play por coleta, P1 27/11 20h).
- Prazos: 27/11 conferir ec124592 (previsão: sai após 26/11 21h35Z); 27/11 devolvida dados-3 do Hemingway; 30/11 relatório, trafego-3, linha de base; 01/12 produto-5.
- Aposta: IC não é assinante; custo por pagante só com RevenueCat ÷ gasto.

## Atualização 2026-11-26 (noite)
- Portão 6 corrigido: mapeado pelo QG; falta ver Compra no dataset (D-20261126-trafego-4 em_andamento, 'sem dado'). Regra por criativo escrita (cria-2): índice vs campanha, mínimo em pagantes, iOS piso/Android exato; limites a calibrar quando p0 existir.
- Prazos: 27/11 ec124592; 30/11 relatório, trafego-3, linha de base.

- 27/11 (Hemingway): relatório de 30/11 abre com o bloco de medição de D-20261124-dados-3; antes de afirmar variação, checar se o salto de 27/11 (+25,7%) se manteve em 28 e 29/11.
