# Thomas Shelby (Direção-Geral e Jurídico) · fechamento do Conselho · 23/11/2026

Base: 10 posições (8 r1 e 2 r2), 83 demandas em `demandas/itens/`, fios de `memoria/fios.md`, decisões de 19 a 23/11, `conhecimento/` preenchido pelo Léo em 23/11 e o `master.md` de 22/11. Sem R$ de receita e sem número absoluto de assinantes. Quadro regenerado: 0 atrasadas, 20 abertas, 5 entregues, 26 aceitas, 23 bloqueadas pro líder.

## A. Ronda: o que corrigi e quem acionei

**Corrigi (no alcance do repositório), 1 linha cada**
- **Repositório público com dado pessoal:** tirei de `PENDENCIAS.md` o e-mail de login do Léo, o alias do Workspace e o Gmail da empresa; do `avaliacoes/guia.md` o número do WhatsApp (o próprio guia manda passar só por e-mail); de `corretores.md` e `conhecimento/01-empresa.md` a relação familiar da expert. O histórico do git ainda guarda e-mails e telefone: reescrever é do Léo, e só importa se ele quiser. `vigia_segredos.py`: nenhum segredo.
- **`quadro.json` estava velho** (64 de 83 demandas): regenerado pelo `quadro_demandas.py`. JSON de todas as 83 válido; nenhuma com agente em reserva como destinatário.
- **Demandas sujas:** tirei `bloqueio: lider` de `cria-2` e `trafego-1` (canceladas) e de `master_auditor-de-entregas-1` (entregue); padronizei `motivo_cancelamento` em `dados-1` e `trafego-1`; `mercado-3` ganhou `bloqueio: dados`; preenchi `pergunta_lider` em 6 bloqueadas que estavam sem pergunta (`cria-3`, `lojas-1`, `ted-1`, `dados_relatorio-semanal-1`, `auditor-2`, `mkt_publicador-1`).
- **Cancelamentos dos diretores conferidos:** `D-20261120-mkt-1` (Cardone) e `D-20261120-cria-2` (Disney) têm motivo válido, ambos com a demanda substituta já aberta (`D-20261123-mkt-1` e `D-20261123-dados-4`); não entram na lista de multa. Cancelei eu `D-20261123-cria-1` (8 carrosséis de reposição: a própria Disney disse que com 10 pessoas de alcance por post não é alavanca) e `D-20261122-mkt-1` (2 das 3 perguntas já respondidas em `conhecimento/`; a meta em valor não é necessária pro placar em %).
- **Memória e painéis:** `merito/metas.json` dizia "degrau 6 é o alvo" e `conhecimento/` diz degrau 4: corrigido; `dados/relatorios/2026-11-23.md` ganhou nota de atualização (insights voltaram, token revogado); `fios.md` (reuniões 20, 22 e 23/11, F-007 novo), `decisoes.md` (respostas do Léo de 23/11 e o link bloqueado do Instagram) e `perguntas-pendentes.md` atualizados.
- **Padrão de design:** o rótulo "PRÓXIMA REVISÃO" da proposta do Jobs (mockup e texto) estava em caixa-alta; virou "Próxima revisão" (DESIGN-MINHAMOTO.md, seção 2).
- **Dívidas minhas fechadas:** `D-20261122-lojas-3` (parecer de promessa: A1 e B1 "seu modelo" cortadas até o Davi confirmar cobertura; as outras passam com ajuste) e `D-20261123-produto_analista-do-paywall-1` (fluxo do app no `02-produto.md`). `D-20261123-dados-5` aprovada e aplicada: `insights.yml` roda todo dia às 23h41 BRT. `D-20261122-master-4` aceita (Turing retirou o 10,7% sem fonte em vez de manter).

**Acionei (demandas de correção, diretor em cópia)**
- **Escobar** `D-20261123-master-1` (P2, 26/11, cc Turing): o Léo registrou em 23/11 que o link do Instagram do MinhaMoto está bloqueado (bio e stories); ninguém ligou isso à verba. Antes do D+0, provar que o destino do anúncio não é o domínio marcado.
- **Cardone** `D-20261123-mkt-1` (escopo ampliado, mantém P1 24/11, Turing executa): dizer qual etapa dos Corretores mais perdeu desde 1/11.
- **Ness:** conferir e aceitar `D-20261122-master_auditor-de-entregas-1`, entregue e sem conferência (é demanda dele).
- **Sem multa nova de diretor.** Nenhum erro de premissa repetido desta vez: o texto do "teste grátis" não voltou em nenhuma das 10 posições.

**Conferência das correções de 22/11**
- `master-1` (Escobar), `master-2` (Disney) e `master-5` (Turing) aceitas no prazo e sem "grátis"; `master-4` aceita; `master-3` (Bezos) segue bloqueada: o proxy recusa as lojas, não é moleza dele. Vai pra Pergunta 2.
- **Eu devo, e repeti:** o pacote ao Davi (`dados-2`, P1 de 21/11) não foi levado em 21/11 nem em 22/11, e a `produto-3` (23/11 12h) e a `dados-1` (12h) também venceram. O texto está pronto agora em `entregas/D-20261123-master-pacote-davi.md`, mas só chega ao Davi no bilhete de decisões. **Pra Folha de sexta: multa pela repetição (refação por erro meu, −10), quem avalia é o Léo e o Davi.**

## 1. Gargalo do funil
**App (assinantes pagos novos): o topo.** Sem leitura de RevenueCat o % de cada etapa continua zerado, mas a etapa que já tem número é a pior: nos 26 posts de 16 a 23/11 a mediana de alcance é 10 pessoas por post (~0,7% dos seguidores), 0 salvamentos, 1 compartilhamento (`dados/insights-2026-11-23.json`, conferi a conta). O pago está em verba zero e o único anúncio que rodou (MM - Curtos, CTR de 2% a 3,5%) não mostra venda do app. O alcance de 28 dias da conta é ordem de grandeza maior que a soma dos posts, e ninguém sabe de onde vem (F-007). O Instagram do MinhaMoto está com link bloqueado. **Alcance e medição seguram os novos pagantes antes de paywall, loja ou preço.** A hipótese de "plano mais cedo" (Stark) continua hipótese: sem funil não há culpado.
**Infoprodutos (Corretores): a entrada da página e o criativo cansado.** Novembro contra outubro (UTMify, via Dados): vendas/dia −43%, gasto/dia −32%, custo por venda +19%, ROAS de 1,88 pra 1,61; visualização da página por clique de ~92% pra ~75%; 1 em 5 Pix gerados não é pago. Sem criativo novo desde o fim de outubro. A página pesada foi corrigida em 23/11; o teste de 6 estilos (Historinha, Quiz e Split-screen primeiro) já foi decidido pelo Léo. Parte da queda é menos verba (−32%): a etapa que piorou por unidade é página vista e custo por venda.

## 2. Quem supera algum diretor (tomada de cadeira)
Ninguém: a regra pede 4 semanas seguidas com prova e o piloto tem 3 rodadas. Quem mais entrega acima do cargo é o **Sun Tzu** (radar 24/11 adiantado, `mercado-1` e `mercado-2` aceitas, corrigiu o próprio "~1 dia" do Drivvo). Segue em observação. **Hemingway** achou e corrigiu o vazamento de token, mas foi efeito colateral de uma correção dele: erro confessado, broche cai um degrau, sem multa. **Fogg** recuperou os 3 slots de hoje no horário, mas produção não é resultado de venda.

## 3. Fios parados há 3 reuniões (20, 22 e 23/11)
- **F-001** medição (SDK e eventos): Davi sem resposta. Parte da culpa é minha (pacote não levado). Decisão 1.
- **F-002** "plano do SEU modelo": sem "sim" do Davi; morre em 27/11. A legenda "seu modelo" já foi cortada das legendas de loja.
- **F-004** vídeos A/B: Léo sem resposta. Mudei o pedido: um sim/não sobre A1 e B1 como anúncios (Decisão 2).
- **F-005** 1★ de sincronização: rascunho `ec124592` sem OK há 4 dias. Pergunta 3.
- F-006 (tarefas dos executores) andou: coordenador voltou, 3 de 3 slots no horário, causa provada (limite de uso). F-003 fechado. F-007 novo (alcance).

## 4. Demandas em cobrança 3
Nenhuma (`cobrancas` 0 em todas, nenhuma atrasada). **Quem está devendo, vencidas e bloqueadas pelo líder:** `D-20261120-dados-2` (P1, Davi, venceu 21/11 20h) e `lojas-2` (Davi, 23/11 12h); `D-20261122-produto-3`, `dados-1` (minhas, 23/11 12h); `mkt_publicador-1`, `auditor-2` e `dados_relatorio-semanal-1` (Léo, pacote de 23/11, prazos 14h a 23h55). Quem entrega e quem não deve nada vencido: Ness, Fogg, Ted, Sun Tzu, Jobs, Hemingway (dados-4 vence 24/11 21h). Eu estou na primeira linha dessa lista; os outros diretores não.

## 5. Iniciativas
| Iniciativa | Veredito | Por quê |
|---|---|---|
| Turing: "De onde vem o alcance?" (alcance por formato, linha de base na semana da build) | **Aprovo, prioridade 1** | É a primeira etapa do funil com número. Coleta diária aprovada hoje (`dados-5`). |
| Disney: A1 e B1 como os 2 primeiros anúncios | **Aprovo como proposta, sem verba** | Escobar tem razão: A1 e B1 diferem em mais de uma coisa, então entram como direção, sem veredito de ângulo. Check de promessa: "o motor paga a conta" passa (figura, sem número); "o aviso chega antes do prazo" (A1) e "na hora certa" (B1) só passam se a `cria-3` do Stark confirmar aviso de manutenção real e não prometer aviso de documento (o app só mostra selo na Garagem). Vai na Decisão 2. |
| Escobar: escada de evento (começa no evento com mais de 50 por semana e sobe) | **Aprovo só como proposta** | Verba continua em zero até o passo 7 do D+0 e o destino do anúncio provado (`master-1`). |
| Greco: janela do IPVA 2027 | **Aprovo reduzido** | Só SP (único calendário de fonte oficial), 4 pautas só em texto, confirmar moto na Sefaz-SP. Texto do app: "avisa na Garagem", nunca "te notifica". Não vale pergunta ao Léo. |
| Cardone: garantia de 30 dias no CTA | **Aprovo com condições** | Só "garantia de 30 dias" como na página, sem "incondicional", sem promessa de renda, sem "grátis"; reembolso no placar. Check meu antes de ir pro ar. O +12,15% de custo da Meta segue fonte secundária: não vira regra. Black Friday: não. |
| Stark: plano da moto mais cedo | **Mantenho a aprovação de 22/11** | Só proposta e só depois da 1ª leitura do funil; paywall intocado. |
| Bezos: legendas de benefício nos 3 primeiros prints | **Aprovo o texto, com o parecer lojas-3** | A1 e B1 cortadas até cobertura de modelo. Nada sobe em loja sem OK do Léo. Morre em 30/11 se não houver base de visita→download (concordo). |
| Disney: carrossel de reposição por volume (`cria-1`) | **Corto** | 10 pessoas de alcance por post e 0 salvamentos: não é alavanca de assinante. |
| Volta da reserva (pauteiro, roteirista, Edison, Saul Bass, Napoleão, Curie, House, etc.) | **Nego** | Ninguém trouxe tarefa real e semanal. Disney diz que o texto é dela e Escobar só pede volta com campanha rodando. |

## 6. Perguntas aprovadas pro Léo e o Davi (3, juntando repetidas)
Riscadas porque o Léo já respondeu em `conhecimento/` hoje: plataforma e garantia dos Corretores, meta em degraus, custo máximo por assinante, BM só de anúncios (adiada em 18/11). Riscadas por não valerem uma pergunta: Disney (roteirizar vídeo do Léo ou do Davi e "o que o assinante disse"; a voz do assinante sai das avaliações, `master-dossie-1`), Greco (série IPVA só SP, é pauta dele) e a pergunta de duração do teste grátis.

1. **Davi, 10 sim/não sobre o app e a build** (texto completo em `agencia/demandas/entregas/D-20261123-master-pacote-davi.md`): SDK e eventos, `appsflyerID` pro RevenueCat, modelo da moto como propriedade, botão "Testar aviso em 1 minuto" fora da versão pública, "Esse é o MinhaMoto" mantido, cobertura de CG 160/Pop 110i/Biz/Bros 160 e o que vê moto sem plano, moto escolhida em lista, anúncio na tela, histórico entre aparelhos, pedido de avaliação só após "Registrar serviço", contagem por dia de onboarding e cadastro de moto, 5 prints 9:16 até 27/11. (Stark, Turing, Escobar, Greco, Disney, Bezos)
2. **Léo, 3 respostas curtas:** (a) qual link o Instagram do MinhaMoto bloqueou (bio e stories) e já pediu revisão? (b) libera apps.apple.com, play.google.com e as bibliotecas de anúncios (Meta e TikTok) pro ambiente dos agentes, ou cola o que os diretores pedirem? (c) qual a nota e o total de avaliações do Google Play hoje? (Escobar, Bezos, Greco, Turing; destrava `master-3`, `lojas-1`, `ted-1`, `cria-3`, `mercado-3` e a `master-1` de hoje)
3. **Léo, sim/não:** publica a resposta ao 1★ de sincronização (rascunho `ec124592`, parado há 4 dias) e deixa o Ted responder 1 e 2★ de bug com o texto do guia, com aviso no celular? (Bezos, Stark, Turing)

## 7. Decisões pro Léo e o Davi (3)
**D1 (Davi, antes de fechar a build de 23/11; se já fechou, na próxima janela, em até 7 dias): a build leva (a) SDK AppsFlyer com o `appsflyerID` enviado ao RevenueCat, (b) os eventos `onboarding_complete`, `paywall_view` e "moto cadastrada" e (c) o modelo da moto como propriedade do usuário?**
- Recomendo: **sim, os três.** Se só der um, o SDK. O Léo já disse em 18/11 que o SDK entra; falta o Davi confirmar o escopo.
- Custo: horas de desenvolvimento do Davi e risco de atrasar a build.
- Ganha: custo por assinante por campanha, funil por etapa e por modelo; destrava a verba do Escobar, 6 demandas e a autópsia da meta. Se o Davi disser não, o plano B (`master-5`) entra. Pergunta aberta desde 20/11, 3 reuniões.

**D2 (Léo): os vídeos A1 e B1 (com "por R$19,90" e as lojas) viram os 2 primeiros anúncios de teste, o Escobar propõe a verba depois e você aprova?**
- Recomendo: **sim, como direção, sem veredito de ângulo.** A frase do "aviso" só vai ao ar se o Stark confirmar na `cria-3` (26/11).
- Custo: 2 minutos vendo A1 e B1. Nenhuma verba agora.
- Ganha: o vídeo volta com número em vez de gosto, fecha o F-004 (parado há 3 reuniões, decisão de 27/11) e deixa 2 criativos com ID próprio prontos pra 1ª semana paga. O orgânico (10 pessoas por post) não serve de bancada.

**D3 (Léo): o Dados lê, só leitura, o resumo em % do `carnucci-dados` (RevenueCat, App Store Connect, AppsFlyer e Meta, já ligados em 23/11) e você libera o Google Play Console só pra relatórios.**
- Recomendo: **sim.** O robô grava o número absoluto no privado e as sessões só devolvem % ao repositório público.
- Custo: minutos do Léo (no Play, uma conta de serviço só de relatórios). Nenhuma chave no repositório.
- Ganha: % por etapa e % da meta na próxima rodada, e a autópsia passa a apontar setor responsável. Sem isso o funil em % continua zerado; pergunta aberta desde 20/11.

## Pra Folha de sexta (27/11)
- **Shelby:** repetição do pacote ao Davi não levado (21/11 e 23/11, P1): refação por erro meu (−10); avaliação do Léo e do Davi.
- **Ness:** conferir `master_auditor-de-entregas-1`; refação da `master-1` de 22/11 segue valendo se a `dados-3` apontar falha dele.
- **Turing, Stark, Greco:** erro de premissa confessado em 22/11, broche já caiu; Turing retirou o 10,7% sem fonte antes da multa.
- **Hemingway:** vazamento de token foi efeito colateral de uma correção dele, confessado e corrigido; broche cai um degrau, sem multa. Entrega do placar novo (`dados-4`) vence 24/11 21h.
- **Elogio:** Sun Tzu (radar adiantado e erro próprio corrigido) e Jobs (leu o código antes de propor).
