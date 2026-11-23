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
