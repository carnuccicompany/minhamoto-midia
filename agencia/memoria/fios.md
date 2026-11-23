# Fios de conversa abertos

Reuniões do Conselho até hoje: 20/11, 22/11 e 23/11. Fio que não se mexeu em 3 reuniões é apontado no master.md (23/11: F-001, F-002, F-004 e F-005 chegaram a 3).

## F-001 · Medição: SDK AppsFlyer e eventos rc_* na build de 23/11 (aberto, 20/11; atualizado 22/11)
- Turing: cobertura de atribuição é prioridade 1. Escobar: sem `rc_*` mapeados e sem teste de OneLink, verba zero. Stark escalou ao Davi (dados-2, P1 venceu 21/11 20h); Cardone, Bezos e Disney dependem da mesma resposta.
- 22/11 (Shelby): nenhuma resposta do Davi no repositório. Virou Decisão 1 da pauta de 22/11 (pacote único; dados-1 e produto-3 bloqueadas com a pergunta pronta). Plano B de medição pedido ao Turing (D-20261122-master-5, 24/11): se o SDK não entrar, a semana não fica sem número.
- 23/11 (Shelby): 3ª reunião sem resposta do Davi, PARADO. 07-canais registra RevenueCat, Meta, AppsFlyer e App Store Connect como ligados (robô, carnucci-dados), mas o SDK e os eventos dependem do Davi. Pacote de 10 sim/não pronto em entregas/D-20261123-master-pacote-davi.md; Decisão 1 de 23/11. Eu devia ter levado em 21/11 e 23/11: 2ª falha minha, vai pra Folha.

## F-002 · Plano de revisão do SEU modelo (aberto, 20/11; atualizado 22/11)
- Reduzido pelo Greco: só CG 160 (39% do top 5, Fenabrave via car.blog.br, fonte secundária), só como teste de loja/texto, sem nome de modelo em loja ou anúncio até o Davi confirmar cobertura (D-20261120-mercado-2) e o Turing dar a % por modelo (mercado-3). Dono Bezos.
- Critério de morte (Shelby): sem "sim" do Davi até 27/11 (folha de sexta), a iniciativa é encerrada e o modelo vira ideia pra depois.
- 23/11: 3 reuniões sem movimento (Greco confirma que mata em 27/11). A legenda de print "seu modelo" ficou cortada até o Davi confirmar cobertura (parecer lojas-3).

## F-003 · Duração do teste grátis (FECHADO em 22/11)
- Resolvido: o app NÃO tem teste grátis (Léo, 20/11, `diretoria/06-produto.md`). Stark, Turing e Greco corrigiram a posição em r1/r2 de 22/11. O Shelby corrigiu 00-SISTEMA-OPERACIONAL, 02-dados, 04-criativos, 06-produto, 09-comunidade, 10-juridico, 07-financeiro, ESTRUTURA-ENXUTA, atribuicao/comparativo-e-spec, PENDENCIAS, guia de avaliações e a memória do produto. Ninguém escreve "grátis" em loja, anúncio ou resposta.

## F-004 · Vídeos A/B (aberto, 20/11; atualizado 22/11)
- Disney parado. Fato novo: religar a produção diária também espera a direção (PENDENCIAS.md). Fila de carrossel: 89 pendentes, seca por volta de 14/12 a 4 por dia. Léo decide até 27/11 (Decisão 3). Há 2 reuniões parado.
- 23/11: 3 reuniões, PARADO. Disney muda o pedido: em vez de escolher A ou B por gosto, 1 sim/não sobre A1 e B1 como os 2 primeiros anúncios (Decisão 2 de 23/11). Escobar aceita como direção, sem veredito de ângulo (A1 e B1 diferem em mais de uma variável).

## F-005 · 1★ Android de sincronização (aberto, 20/11; atualizado 22/11)
- 1 de 3 no Play (33%, amostra de 3), 1 de 9 no total. Resposta (rascunho ec124592) sem OK há 3 dias; entrou na Pergunta 2. Correção do app só depois da build de 23/11 (decisão de 19/11). Ângulos "sem anúncio" e "dados salvos" fora enquanto o bug existir.
- 23/11: 3 reuniões sem OK, PARADO. Play: 2 avaliações (1 de 2 com 1★), amostra de n=2, pista e não padrão. Vira a Pergunta 3 de 23/11 (publicar a resposta e deixar o Ted responder 1-2★ de bug).

## F-006 · Tarefas agendadas dos executores paradas (aberto, 22/11)
- O log do coordenador não tem rodada depois de 21/11 08h40; não há coleta de avaliações depois de 20/11 21h; 3 de 7 slots de 21 e 22/11 sem post e os 4 postados saíram 50 a 102 min atrasados. Donos: Ness (D-20261122-dados-3, P1, 23/11 23h30) e Fogg (D-20261122-cria-1, P1, 23/11 20h).
- 23/11: andou. Coordenador voltou (rodada 19h12 ok), Fogg postou 12h, 15h e 18h no horário, dados-3 e cria-1 aceitas. Causa provada: limite de uso derrubou as tarefas (pacote ao Léo, itens 1 e 2). Fica aberto até 3 dias seguidos de 4 de 4 slots.

## Registro do Conselho 22/11 (1 linha por fala)
- Turing: funil em 6 etapas sem trial; 1ª leitura até 7 dias após build com SDK; UTM até 23/11 20h. Stark: fonte do "sem teste grátis" é o Léo, 20/11. Greco: iniciativa só CG 160, morre sem "sim" do Davi até 27/11; Sun Tzu prioriza mercado-1/2.
- Mesa 22/11: F-006 com causa parcial: publicar.yml sem execução no horário nos 4 slots perdidos; limite de uso das tarefas provado só de 22/11 14h; Léo libera o histórico.
- Próximo passo: Davi responde SDK/eventos antes da build de 23/11 (F-001); Léo decide vídeo A/B até 27/11 (F-004).

## F-007 · De onde vem o alcance (aberto, 23/11)
- Insights por post voltaram (coleta de 23/11 17h32): nos 26 posts de 16 a 23/11, mediana de 10 pessoas por post (~0,7% dos seguidores), 0 salvamentos, 1 compartilhamento. O alcance da conta em 28 dias é ordem de grandeza maior; a Meta diz que inclui anúncio, story e reel. Turing: dados-4 (placar com alcance por formato, P1 24/11 21h) e coleta diária aprovada hoje (dados-5). Disney, Escobar e Turing concordam: o feed orgânico de carrossel não carrega a meta; o pago é a única bancada com volume controlável.
- Fato novo: o Instagram do MinhaMoto está com link bloqueado (bio e stories), registro do Léo em 07-canais (23/11). Demanda D-20261123-master-1 (Escobar) confere o destino do anúncio.

## Registro do Conselho 23/11 (1 linha por fala)
- Turing: F-001 parado; hipótese "o alcance vem de outro formato". Disney: A1/B1 como anúncios; carrossel por volume não é alavanca. Greco: janela do IPVA 2027 só SP, 4 pautas. Cardone: garantia de 30 dias no CTA; vendas/dia -43% em novembro. Escobar: verba zero até o passo 7 do D+0; escada de evento. Stark: plano da moto mais cedo, só proposta. Bezos: legendas de benefício nos 3 primeiros prints; mata em 30/11 sem base.

## Mesa 23/11 (noite)
- Aceitas: cria-4, dados-4, master-1, master-dossie-1, mercado-1, produto-2. Devolvida: mercado-3 (Stark: mandar a tela com o selo e a versão). Turing sem leitura de UTMify/Meta/ASC: mkt-1, lojas-2, trafego-2 bloqueadas pro Léo.
