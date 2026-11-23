# Thomas Shelby (Direção-Geral e Jurídico) · fechamento do Conselho · 22/11/2026

Base: 10 posições (7 r1 e 3 r2), 44 demandas em `demandas/itens/`, fios de `memoria/fios.md`, decisões de 19 e 20/11. Sem R$ e sem número absoluto de assinantes. Quadro regenerado: 0 atrasadas, 24 abertas, 7 aceitas, 13 bloqueadas pro líder.

## A. Ronda: o que corrigi e quem acionei

**Corrigi (no alcance do repositório)**
- **Teste grátis (conflito de 20/11 fechado):** `00-SISTEMA-OPERACIONAL.md` (quem somos e funil), `04-criativos.md` (anatomia do anúncio: "teste grátis" saiu da oferta), `06-produto.md` (5 trechos que ainda mandavam testar teste grátis e duração), `02-dados.md`, `09-comunidade.md`, `10-juridico.md`, `07-financeiro.md`, `ESTRUTURA-ENXUTA.md`, `conhecimento/README.md`, `02-produto.md` e `perguntas-pendentes.md` (perguntas de duração riscadas), `diretoria/memoria/produto.md` (item 5 descartado, benchmark de teste marcado como inválido), `PENDENCIAS.md` (postbacks sem eventos de trial).
- **`atribuicao/comparativo-e-spec.md`:** funil sem etapa de trial, START_TRIAL/TRIAL_STARTED/trial_conversion_rate retirados, "moto cadastrada" só se o Davi criar o evento.
- **`avaliacoes/guia.md` (o mais grave):** a resposta padrão de 1★ de preço dizia "O MinhaMoto tem teste grátis" e o Ted publica a partir dela: promessa falsa em público. Texto corrigido; nenhuma resposta já publicada em `respostas.json` citava teste.
- **Demandas:** D-20261120-produto-2 cancelada (premissa errada, escopo vive na D-20261122-mercado-1); D-20261122-mercado-1 reescrita no que o Greco já tinha trocado na r2 (o JSON ainda pedia duração de teste); D-20261120-lojas-3, D-20261122-lojas-2 e D-20261120-dados-2 sem "início de teste"/"dias de teste grátis"; D-20261122-mkt-2 cancelada (prematura, sem export nem decisão de infoproduto novo, e o Sun Tzu está lotado); D-20261120-master-1 fechada (ver abaixo).
- **`scripts/quadro_demandas.py`:** ordenação passa a ser atrasadas, depois P1 vivas (inclusive bloqueadas pro líder), depois o resto; era o ponto devolvido ao Ness na master-1. Quadro conferido contra `itens/`: 44 arquivos, 44 no quadro, todos JSON válido.
- **Memória:** `fios.md` reescrito (F-003 fechado, F-006 novo); `decisoes.md` ganhou o fato "sem teste grátis" e a extensão do "sem Black Friday" aos Corretores; mockup antigo do Jobs sem o botão "Começar teste grátis" e aviso no topo da entrega D-20261120-produto-1.

**Acionei (demandas de correção, diretor do setor em cópia)**
- **Escobar** `D-20261122-master-1` (P2, 24/11): tirar "teste iniciado" e "X dias grátis" da r1, linha de base em 6 etapas, trocar "93 na fila" (status.json parado em 21/11) por 89.
- **Disney** `D-20261122-master-2` (P2, 25/11): lote zero sem "grátis" nem "teste" (a r1 dizia que os roteiros diriam "teste grátis"); pergunta 3 cai.
- **Bezos** `D-20261122-master-3` (P2, 24/11): ler título, subtítulo e prints nas páginas públicas das lojas em vez de pedir ao Léo; avisar o Ted do guia corrigido.
- **Turing** `D-20261122-master-4` (P3, 25/11): fontar o 10,7% da RevenueCat da r2 (veio sem link) e confirmar minuta e funil sem trial.
- **Turing (estratégica)** `D-20261122-master-5` (P2, 24/11, cc Escobar, Stark): plano B de medição se o SDK não entrar na build de 23/11.
- **Ness:** D-20261120-master-1 passou 35 h sem reentrega e a entrega afirmou 23 arquivos quando havia 24; fechei eu a parte do script. Vai pra Folha como refação. O log do coordenador está parado desde 21/11 08h40; segue na D-20261122-dados-3 (P1).

**Conferência das correções que mandei em 20/11**
- Escobar corrigiu o "40%" pra 33% (1 de 3) na r1 sem eu cobrar: fechado. Stark e Turing confessaram a premissa de teste antes de alguém pegar: erro conta, broche cai um degrau, sem multa, como a regra manda.
- D-20261120-master-2 (Hemingway): aceita, no prazo.
- **Eu devo:** o pacote ao Davi pedido na dados-2 (P1, 21/11 20h) não tinha sido levado; só sai hoje, como Decisão 1. Pra Folha de sexta: prazo perdido do Shelby, quem avalia é o Léo.
- **Repetição:** nenhuma (todos os erros de hoje são de premissa herdada do 00-SISTEMA-OPERACIONAL, que era meu de corrigir e demorei). Sem multa por repetição nesta rodada.

## 1. Gargalo do funil
Ainda a **medição entre o post/anúncio e a assinatura**: sem SDK e eventos na build, sem leitura de RevenueCat e lojas e sem export dos Corretores, nenhum diretor tem % de etapa, e pela regra de 20/11 sem número não há culpado. Mas com o fato do Léo agora fixado (sem teste grátis) o desenho do funil muda e dá pra dizer onde procurar.
- **Assinantes pagos novos:** funil real: instalação, onboarding, moto cadastrada, paywall, compra inicial, renovação. Como o paywall é pago direto e não se mexe, o buraco mais provável é **antes do paywall** (valor visto antes de pedir dinheiro: Stark/Jobs, página da loja: Bezos), e a etapa que mais segura o novo pagante é **paywall > compra**, sem alavanca de oferta. É hipótese: régua externa só a do Turing (RevenueCat, média de apps, nunca meta nossa). Tráfego pago está em 0%: nenhum anúncio com número.
- **Infoprodutos (Corretores):** nenhuma etapa medida (sem export da plataforma, sem meta). Hipótese do Cardone (garantia e prova no checkout) fica só hipótese.
- **Segundo gargalo, operacional:** as tarefas agendadas dos executores não rodam desde 21/11 de manhã (coordenador, coleta de avaliações; 3 de 7 slots perdidos). Falha de sistema ou de agente: é o que a dados-3 deve dizer.

## 2. Quem supera algum diretor (tomada de cadeira)
Ninguém: a regra pede 4 semanas seguidas com prova e o piloto tem 2 rodadas. Quem mais entrega acima do cargo é o **Sun Tzu** (radar adiantado, mkt-3 com 3 dias de folga, mercado-1 aceita), mas está com 5 pedidos num só agente; priorizei mercado-1 e mercado-2 antes de lojas-1 e cria-3. Fogg: 24 posts no ar, mas atrasado e com 3 slots perdidos: produção não é resultado.

## 3. Fios parados há 3 reuniões
Nenhum chegou a 3 (só houve 20/11 e 22/11). Em risco de chegar: **F-001** (SDK/eventos, sem resposta do Davi) e **F-004** (vídeos A/B). F-003 fechado. F-006 novo (tarefas dos executores). F-002 tem critério de morte: sem "sim" do Davi até 27/11, encerra.

## 4. Demandas em cobrança 3
Nenhuma. A única atrasada (master-1, cobrança 2) foi fechada. Quem está devendo hoje: Ness (log parado e master-1 reentrega, na dados-3), Fogg (3 slots, cria-1) e eu (pacote ao Davi). Vencem amanhã: dados-3 de UTM (Turing→Escobar, 23/11 20h), trafego-2 (Escobar→Turing, mesma hora), lojas-1 (Ted, 21h).

## 5. Iniciativas
| Iniciativa | Veredito | Por quê |
|---|---|---|
| Turing: linha de base do funil na semana da build | **Aprovo, prioridade 1** | Funil em 6 etapas, sem trial. Plano B de medição obrigatório (master-5). |
| Escobar: "proposta pronta no dia do teste" (1 campanha, otimiza por compra inicial) | **Aprovo só como proposta, sem verba** | Corto "teste iniciado". Android fora da 1ª campanha pelo motivo certo: bug de sincronização conhecido, o app só corrige depois da build, e pagar instalação num app que falha é jogar dinheiro. Não pelo 1★ de 33%. |
| Disney: Lote zero, 10 roteiros em texto (5 Meta, 5 TikTok) | **Aprovo** | 25/11, sem vídeo, sem modelo, sem "grátis". 5 viram carrossel Curtos AIDA, repondo a linha de venda sem reativar ninguém. |
| Bezos: legendas de benefício nos 3 primeiros prints | **Aprovo o texto; nada vai à loja sem OK do Léo** | Apple só testa ícone, prints e vídeo, então o teste é de prints. Antes: ler a ficha atual (master-3), checagem de promessa (lojas-3). Tudo em texto até 28/11. |
| Stark: plano da moto visível antes do paywall | **Aprovo o desenho refeito, não aprovo mexer no app** | Pode estar moot se o app já mostra o plano antes do paywall (Pergunta 1, item 4). Proposta ao Davi só depois da 1ª leitura do funil; paywall intocado. |
| Greco: "plano do SEU modelo", só CG 160 | **Aprovo reduzido, com data de morte 27/11** | Sem nome de modelo em loja ou anúncio enquanto o Davi não confirmar cobertura; sem "sim" até 27/11, encerra. |
| Cardone: teste de garantia e prova nos Corretores | **Adio** | Sem export, sem meta e sem baseline não há como medir se a conversão paga o reembolso. Meta proíbe promessa de renda. A "+12,15%" de PIS/COFINS é fonte secundária: conferir na Central de Ajuda da Meta antes de usar. |
| Volta da reserva (pauteiro, roteirista, Edison, Saul Bass, Napoleão, etc.) | **Nego** | Ninguém trouxe tarefa real e semanal. A fila cobre até ~14/12. |
| Respostas do Ted sem aprovação | **Levo à Pergunta 2** | É publicação; só o Léo libera. |

## 6. Perguntas aprovadas pro Léo e o Davi (3, juntando repetidas)
O pacote que dados-1, produto-3, mkt-1 e trafego-1 pediam ao Léo e ao Davi foi juntado nestas três. As perguntas de duração do teste grátis (Turing, Greco, Bezos, Stark, Disney) caíram: o app não tem. Cortei também a pergunta do Disney sobre "qual post vendeu mais" (o ranking sai do insights.yml) e a do Greco sobre concorrentes e motoboy (decisão do Greco com o radar).

1. **Davi, sim/não em 7 itens sobre o app hoje:** (1) tem anúncio na tela? (2) a conta guarda o histórico entre aparelhos? (3) a moto é escolhida numa lista, sem digitar o modelo? (4) o usuário vê o plano de revisão da moto antes do paywall? (5) já existe pedido de avaliação, e só depois de "Registrar serviço", nunca após erro de sync? (6) o plano cobre CG 160, Pop 110i, Biz e Bros 160? (7) libera 5 prints ou gravações 9:16 da versão nova, sem dado de cliente, até 27/11? (Destrava dados-2, lojas-2, mercado-2, mercado-4, cria-3 e produto-3.)
2. **Léo:** (a) qual a meta semanal de assinantes pagos novos e o custo máximo por assinante? (informar no privado, nunca no repositório); (b) cria o BM só de anúncios antes da 1ª verba? (sim/não); (c) publica a resposta ao 1★ de sincronização (rascunho ec124592) e deixa o Ted responder sozinho 1 e 2★ de bug com o texto do guia, com aviso no celular? (sim/não). (Destrava trafego-1, dados e Escobar.)
3. **Léo, Corretores:** (a) a plataforma é a Kavoo e ela exporta vendas e reembolsos (CSV ou webhook)? libera um export semanal? (b) existe meta semanal de vendas dos infoprodutos (valor só no privado)? (c) a garantia atual é só os 7 dias da lei ou maior? Black Friday: vale o "não" de 19/11. (Destrava mkt-1, mkt-2 e o teste do Cardone.)

## 7. Decisões pro Léo e o Davi (3)
**D1 (Davi, até a noite de hoje, antes da build de 23/11): a build leva (a) SDK AppsFlyer com o appsflyerID enviado ao RevenueCat, (b) os eventos `onboarding_complete` e `paywall_view`, mais "moto cadastrada", e (c) o modelo da moto como propriedade do usuário?**
- Recomendo: **sim, os três.** Se só der pra (a), mande (a).
- Custo: horas de desenvolvimento do Davi e risco de atrasar a build.
- Ganha: custo por assinante por campanha, funil por etapa e por modelo, e destrava a verba do Escobar, 6 demandas e a autópsia da meta. Sem isso a próxima janela é 1 semana inteira sem custo por assinante. Se o Davi disser não, o plano B (master-5) entra.

**D2 (Léo): ligar a leitura dos dados.** Disparar o `insights.yml` à mão hoje (1 clique) e, quando criar o `carnucci-dados`, liberar leitura de RevenueCat, App Store Connect e Play Console.
- Recomendo: **sim, nessa ordem** (insights.yml primeiro; depois chaves só de leitura).
- Custo: minutos do Léo agora; as chaves na hora de logar no GitHub (já pendente). Nenhuma chave vai pro repositório.
- Ganha: 1º número real na próxima rodada (ranking de posts por linha, funil por loja, funil do app) e a autópsia da meta passa a apontar o setor responsável. Pergunta aberta desde 20/11.

**D3 (Léo): direção visual A ou B pros vídeos até 27/11.**
- Recomendo: **decidir até 27/11.** Fato novo desde 20/11: religar a produção diária também espera a direção, e a fila de carrossel (89) acaba por volta de 14/12 a 4 por dia.
- Custo: o tempo do Léo vendo A1, A2, B1 e B2. Sem decisão, a produção continua só em carrossel e a fila seca.
- Ganha: vídeo volta, o Escobar tem criativo pra testar e o Disney deixa de depender de 10 roteiros só em texto.

## Pra Folha de sexta (27/11)
- Ness: refação em master-1 (−10) e log parado, se a dados-3 mostrar falha dele e não do sistema.
- Shelby: prazo perdido do pacote ao Davi (dados-2, 21/11 20h) e demora em corrigir o 00-SISTEMA-OPERACIONAL; avaliação com o Léo e o Davi.
- Stark, Turing e Greco: erro de premissa confessado antes da cobrança; broche cai um degrau, sem multa.
- Elogio: Sun Tzu (entrega adiantada, com fonte e ressalva).
