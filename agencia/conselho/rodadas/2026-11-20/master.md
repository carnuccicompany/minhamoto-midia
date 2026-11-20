# Thomas Shelby (Direção-Geral e Jurídico) · fechamento do Conselho · 20/11/2026

Base: 10 posições (r1 e r2) dos diretores, 21 demandas em `demandas/itens/`, decisões de 19 e 20/11. Sem número absoluto, sem R$.

## 1. Gargalo do funil
Ninguém trouxe número de funil, então não existe etapa que eu possa culpar com prova. O que se vê em oito de oito posições é o mesmo buraco: **a medição entre o post/anúncio e a assinatura**. Sem SDK AppsFlyer e eventos `rc_*` na build de 23/11, `metas.json` ainda "aguardando" e `carnucci-dados` fora do ar, a autópsia da meta não acha culpado (regra de 20/11: sem número, sem culpado).
- **Assinantes pagos novos:** etapa mais suspeita, só como hipótese: **ativação antes do paywall** (Stark cita 55,4% dos cancelamentos de teste de 3 dias no dia 0, RevenueCat 2026, média de 115 mil apps, não é a nossa). Segunda suspeita: queda de teste para pago, que depende do tamanho do teste grátis, que ninguém no Conselho sabe. Tráfego pago hoje: 0% da meta, não há anúncio com número.
- **Infoprodutos (Corretores):** sem export de vendas e reembolso, não há etapa medida. Hipótese do Cardone (uma etapa quebra, sem aumentar verba) segue só hipótese; o 1º dado é o placar em % (D-mkt-1).
- Dado que vale (amostra de 9, é pista): Play 1 de 3 com 1★ por falha de sync; App Store 6 de 6 com 5★. O "40%" do Escobar está errado, o Stark corrigiu: é 33% de 3.

## 2. Quem supera algum diretor (tomada de cadeira)
**Ninguém.** A regra pede 4 semanas seguidas de mais resultado, com prova; o piloto tem 1 semana e nenhum agente tem número de resultado. Quem mais produz é o Fogg (19 posts no ar, `fila/estado.json`), mas produção não é resultado. Hemingway e Jobs têm 0 entregas. Sem risco de cadeira por enquanto.

## 3. Fios parados há 3 reuniões
Nenhum: `fios.md` está vazio. Os 5 pontos que valem virar fios na próxima ata: SDK/eventos da build (Turing, Escobar, Stark), plano por modelo (Disney, Greco, Bezos, Stark), teste grátis (Turing, Stark, Disney), vídeos A/B (Disney), 1★ Android (Bezos).

## 4. Demandas em cobrança 3
Nenhuma. Todas têm `cobrancas: 0` e nenhuma venceu (o primeiro prazo é 21/11 20h). O `quadro.json` está desatualizado (mostra 0 demandas; existem 21), então criei D-20261120-master-1 pro Ness regenerar.
**Em risco de virar dívida em 21/11 20h (P1):** D-dados-2 e D-trafego-1 (mesma pergunta, ao Davi) e D-mkt-1 (Turing já avisou que não cumpre, sem export). Quem deve se a P1 estourar: dados-2 está bloqueada com `lider`, então o devedor é quem não escalou a pergunta, e hoje quem tem a pergunta na mão sou eu (decisão 1 abaixo). D-mkt-1 é dívida do Léo (export), não do Turing.

**Cancelei (ruído, duplicadas):**
- D-20261120-trafego-1: duplicata de dados-2 (mesma pergunta ao Davi). Fica uma só; Escobar acompanha dados-2.
- D-20261120-dados-1: duplicata de cria-1 (tabela post, linha, ID, data sai de `fila/estado.json` do Fogg). O Hemingway recebe do Fogg.

**Criei:** D-20261120-master-1 (Ness: regenerar o quadro, P2, 21/11 12h) e D-20261120-master-2 (Hemingway: 1º relatório de 23/11 só com o que existe, em %, mais a lista "sem número / quem destrava", P2, 23/11).

## 5. Iniciativas
| Iniciativa | Veredito | Por quê |
|---|---|---|
| Turing: cobertura de atribuição (SDK, UTM, tabela post-ID) | **Aprovo, prioridade 1** | Destrava todas as outras. Meta: % de assinaturas novas com fonte na 1ª semana pós-build. |
| Escobar: "primeira semana com número", 1 campanha, modo proposta | **Aprovo só como proposta, sem verba** | Roda depois da build e da BM de contingência. **Corto o motivo "só iOS por 40% de 1★"** (dado errado). Se for só iOS, é por ter 6 de 6, e como pista. Peço o criativo genérico de controle que ele mesmo apontou. |
| Stark: aha antes do paywall | **Aprovo desenho (Jobs), não aprovo mexer no app** | Mockup em 23/11. Só vira pedido ao Davi com baseline de início de teste e teste→pago. |
| Disney: vídeo POV por modelo | **Aprovo só roteiro em texto** | Vídeos seguem parados (decisão 19/11); nome de modelo só depois do Davi confirmar cobertura (Stark recusou o sim). Critério +20% em salvamento/clique é bom, falta insight. |
| Bezos e Greco: "plano de revisão do SEU modelo" (loja) | **Fundo as duas numa só, dono Bezos, Greco pesquisa. Corto a de Greco como iniciativa separada** | Mesma hipótese de Disney e Stark: 4 iniciativas na mesma ideia. Nada de título/print com modelo antes da resposta do Davi. Teste oficial das lojas depois da linha de base. |
| Cardone: placar dos Corretores + 1 teste | **Aprovo o placar, adio o teste** | Sem dado não há etapa. Garantia de 7 dias (CDC art. 49) é custo previsível a medir. Regra da Meta: sem promessa de renda. |
| Reserva (pauteiro, roteirista, Napoleão etc.) | **Nego por ora** | Não há tarefa real e semanal. Disney pediu só depois do ranking do Turing; a fila cobre ~23 dias (até ~13/12). |
| Jurídico: promessa, preço e regra de loja | **Alertas** | (1) sem nome de modelo em loja/anúncio sem cobertura confirmada (promessa falsa vira cancelamento e reclamação). (2) Corretores: nada de promessa de ganho. (3) Resposta pública ao 1★ sem prazo de correção. Limites de caracteres da Apple e a regra de pedido de avaliação (Apple HIG e Google) não foram conferidos por ninguém; conferir antes de implementar. |

## 6. Perguntas pro Léo (3, juntas)
1. **Funil do app:** quantos dias dura o teste grátis, como são o onboarding e o paywall hoje e o app já pede avaliação? (Turing, Stark, Disney, Bezos). Sem isso o benchmark do RevenueCat não vale.
2. **Corretores:** vendem por qual plataforma, dá pra liberar export semanal de vendas e reembolso, existe meta semanal e o "sem Black Friday" vale também pra eles? (Cardone)
3. **Meta e lojas:** qual a meta semanal de assinantes novos (em % ou no Drive privado) e o custo máximo por assinante (Turing, Escobar); posso mandar o Ted Lasso publicar a resposta ao 1★ de sincronização (rascunho ec124592)? (Bezos)

## 7. Decisões pro Léo e o Davi
**D1 (Davi, até 21/11 20h): a build de 23/11 inclui SDK AppsFlyer, eventos `af_complete_registration` e `rc_*`, a propriedade "modelo da moto" e a data iOS/Android?**
- Recomendo: **sim, os três** (SDK e eventos; modelo da moto como propriedade do usuário; confirmar se o plano cobre CG 160, Pop 110i, Biz e Bros).
- Custo: horas de desenvolvimento do Davi (ele estima). Risco: atrasar a build de 23/11.
- Ganha: custo por assinante por campanha, funil por modelo, e destrava 6 demandas bloqueadas e a verba do Escobar.

**D2 (Léo): ligar a leitura dos dados.** Disparar o `insights.yml` à mão hoje e, quando criar o `carnucci-dados`, liberar leitura de RevenueCat, App Store Connect, Play Console e o export dos Corretores.
- Recomendo: **sim, nessa ordem** (insights.yml primeiro, 1 clique).
- Custo: poucos minutos do Léo agora; o resto na hora de logar no GitHub (já pendente).
- Ganha: 1º número real na próxima rodada (ranking por linha, funil por loja, placar dos Corretores) e a autópsia da meta passa a poder apontar o setor responsável.

**D3 (Léo): direção visual A ou B pros vídeos.**
- Recomendo: **decidir até 27/11** (a fila de carrosséis acaba por volta de 13/12, e o Disney precisa de ~1 semana pra produzir). Não reabro a decisão de 19/11; o fato novo é a data em que a fila acaba.
- Custo: o tempo do Léo vendo A1/A2/B1/B2. Se não decidir, a produção fica só em carrossel e a fila seca.
- Ganha: o vídeo POV por modelo (a única iniciativa de criativo com hipótese e critério de corte) entra no ar depois da build, e o Escobar passa a ter criativo pra testar.

