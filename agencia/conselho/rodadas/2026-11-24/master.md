# Thomas Shelby (Direção-Geral e Jurídico) · fechamento do Conselho · 24/11/2026

Base: 10 posições (7 r1 e 3 r2), 113 demandas em `demandas/itens/`, `fios.md`, `decisoes.md`, `conhecimento/`, `cadastro/itens.json`, os painéis e as memórias. Sem R$ de receita e sem número absoluto de assinantes (o `carnucci-dados` não abre nesta sessão). Quadro regenerado: 0 atrasadas, 15 abertas, 12 entregues, 44 aceitas, 20 bloqueadas pro líder (eram 27: reclassifiquei as que o Léo já resolveu e cancelei as caducas). JSON de todas as demandas válido; `vigia_segredos.py`: nenhum segredo.

## A. Ronda: o que corrigi e quem acionei

**Corrigi (no alcance do repositório), 1 linha cada**
- **`D-20261124-trafego-1.json` (Escobar sobrescreveu e restaurou):** conferi campo a campo contra a versão original do commit da manhã: id, de, para, copia, título, por_que, pronto_quando, prioridade e prazo idênticos; status, entrega e histórico foram atualizados depois pelo Turing (bloqueada por falta da ponte de %), e o arquivo de entrega existe. Íntegra. Erro confessado, sem multa.
- **Alcance por formato destravado:** apliquei em `scripts/insights.py` o patch que o Turing deixou pronto e esperava "OK do Davi" (só leitura, dentro de `tenta()`, sem chave nova, reversível). A coleta das 23h41 grava `ig_alcance_28d_formato` (ou o erro exato da Meta). Era correção pequena e minha; `D-20261123-dados_relatorio-semanal-1` voltou a `em_andamento`.
- **Afirmação sem prova no radar e na pauta:** radar de 24/11 (item 5, linha 2 da tabela, ideia de conteúdo) e `pautas/BANCO.md` diziam que quem anda de CG, Pop, Biz e Bros não tem app da Honda; a fonte (AutoPapo, 03/06) cita só NX500, CB 500 Hornet, CB 1000R e X-ADV. Risquei, marquei "hipótese, não provada" e bloqueei a pauta até a fonte oficial da Honda (cria-4).
- **`DESIGN-CORRETORES.md` se contradizia:** a seção 1 mandava citar o Pacote Completo a R$37,90 e riscava "R$27,90"; o Léo decidiu em 23/11 "R$27,90, sem parcelamento" (`conhecimento/05-marca.md`) e a seção 5 do próprio arquivo já dizia isso. Corrigi a seção 1 e o CTA.
- **Painel do Léo com ruído:** 27 demandas apareciam como "precisa do Léo/Davi". Reclassifiquei pra `qg` (falta só a ponte de resumo em %, que não é decisão dele) `D-20261120-mkt-2`, `D-20261120-lojas-3`, `D-20261123-dados-1`, `-lojas-2`, `-mkt-1` e `-trafego-2`, porque o Léo ligou RevenueCat, Meta Ads (duas contas), AppsFlyer e App Store Connect em 23/11 (`cadastro/itens.json`). Quatro demandas usavam o campo `pergunta` em vez de `pergunta_lider`: padronizei.
- **Canceladas com motivo (caducas ou respondidas):** `D-20261122-trafego-1` (itens 1 e 2 já respondidos pelo Léo em 23/11; o item 3 vive na `dados-2`), `D-20261122-mkt_publicador-1` e `D-20261122-master_auditor-de-entregas-2` (a causa, limite de uso, não se repetiu: 4 de 4 slots em 23/11 e 12h/15h em 24/11; reabrem se falhar), `D-20261124-lojas-3` (ficha personalizada do Play: Android fora da 1ª campanha) e `D-20261124-mercado-2` (nº de modelos do MotorManage não entra em nenhuma peça nossa).
- **Memória que faltava:** `decisoes.md` ganhou 24/11 (regra de preço do Léo, Canal v2, conexões de 23/11, patch, texto de garantia); `fios.md` com o registro de hoje e o estado de cada fio em 4 reuniões; `perguntas-pendentes.md` com as aprovadas de hoje e as riscadas; `PENDENCIAS.md` com a ponte de % como P1 do QG.
- **Fiz as demandas que eram minhas:** `D-20261124-cria-3` e `D-20261124-mkt-1` (parecer de promessa e garantia de 30 dias, gravado no fim de `entregas/D-20261123-mkt-2.md`: textos aprovados pra produzir em arquivo, sem a palavra "reembolso"; termos da Kavoo "não confirmados", só o Léo vê); `D-20261124-produto_analista-do-paywall-1` (3 perguntas da P-001 viraram itens 13 a 15 do pacote do Davi); `D-20261124-produto-3` (viraram o item 16, que vai primeiro); `D-20261124-trafego-4` (resposta: item 2 já resolvido, itens 1 e 3 abaixo); `D-20261124-dados-2` (vai ao Léo hoje, pergunta com relógio).
- **Parecer da frase do catálogo (Disney e Greco pediam):** "mais de 370 modelos de moto, escolha na lista" **aprovada pra roteiro e texto de loja**, porque o Stark leu no código de 17/11 377 modelos e escolha por lista. Proibido "qualquer moto", "todas as motos" e "377 com tabela oficial" (263 têm: 70%). Não vira pergunta ao Léo. Vale pro código de 17/11; o Davi confirma a build no pacote (item 6).

**Acionei (demandas de correção e estratégicas, diretor em cópia)**
- **Sun Tzu** `D-20261124-master-1` (P2, 26/11 20h, cc Greco): listar cada afirmação do radar que generaliza além da fonte, com escopo real e veredito fato/hipótese; item 5 reescrito. A confirmação oficial da Honda continua sendo a `cria-4` do Greco. Registrado na memória do Sun Tzu e do Greco. O Greco repetiu a afirmação na r1 dele: erro de fonte, sem multa; se voltar a aparecer sem prova, entra na escada.
- **Turing** `D-20261124-master-2` (estratégica, P2, 26/11 20h, cc Escobar e Cardone): especificar `dados/resumo-pct.json` (só %, índice e dias) pro QG construir a ponte. Nove demandas de cinco diretores estão paradas só por isso.
- **Escobar** (memória): antes de criar demanda, conferir se o id já existe (`ls itens | grep`); o 1º erro foi confessado.

**Conferência das correções das rodadas anteriores**
- Fechadas: `master-1` (Escobar, destino do anúncio x link do Instagram) segue no prazo (26/11), `mkt-1` do Cardone virou `D-20261124-mkt-1`/`cria-3` (minhas, entregues hoje), `master-4` e `dados-5` aceitas e aplicadas, `lojas-3` (parecer das legendas) fechada, Ness com a coleta de avaliações de 3 dias sem alerta corrigida por `D-20261124-lojas-1` (entregue).
- **Segue aberta e é minha:** o pacote do Davi. É a 4ª reunião. Hoje ele está num texto só, com 16 itens, numerados, e o item 16 (a build saiu?) no topo; mas só chega ao Davi pelo QG, e eu não alcanço o Léo nem o Davi desta sessão. **Pra Folha de sexta (27/11): repetição da falha (21, 23 e 24/11), refação por erro meu (−10) já anotada em 23/11; decisão de multa adicional é do Léo e do Davi, que avaliam o Diretor-Geral.**

## 1. Gargalo do funil
**App (assinantes pagos novos): a aquisição no topo, com a medição cega por baixo.** Número de hoje: o alcance de 28 dias da conta variou −0,4% de 23 pra 24/11; os 59 posts de feed explicam no máximo 9,9% dele (todos FEED, nenhum REELS); a mediana por post é 0,57% dos seguidores na semana de 17 a 24/11, com 2 salvamentos e 1 compartilhamento no total (`dados/insights-2026-11-24.json`, conferido pelo Turing e pela Disney, que adotou a janela dele). O orgânico não carrega a meta; o pago está em verba zero porque falta o SDK (build) e o D+0 de medição. Como o RevenueCat ainda não vira % pra esta sessão, nenhuma etapa abaixo do topo tem número: **sem número não tem culpado**. O que segura os pagantes novos agora é (1) o pago não ter começado e (2) a medição não ter chegado. Os dois dependem do Davi (build/SDK) e do QG (ponte).
**Infoprodutos (Corretores): criativo cansado e queda na entrada da página.** Novembro contra outubro (UTMify, `conhecimento/09-numeros.md`, 23/11): vendas por dia −43%, gasto por dia −32%, custo por venda +19%, ROAS de 1,88 pra 1,61; visualização de página por clique de ~92% pra ~75% (página aliviada em 23/11); 1 em 5 Pix gerados não é pago. O tributo da Meta (+12,15%, fonte de terceiro) não explica os +19%: o Cardone concluiu isso e eu aceito. Sem criativo novo desde o fim de outubro; o teste de 6 estilos (Historinha, Quiz, Split-screen primeiro) decidido pelo Léo em 23/11 é o remédio. Falta a semana 16 a 22/11 isolada e o reembolso, que dependem da ponte.

## 2. Quem supera algum diretor (tomada de cadeira)
Ninguém. A regra pede 4 semanas seguidas com prova e o piloto tem 4 rodadas. Quem mais entrega acima do cargo segue o **Sun Tzu** (radar no dia, mercado-1 e -2 aceitas), mas hoje levou um erro de fonte (Honda) que o tira da prateleira de elogio desta semana; **Jobs** (leu o código antes de propor, 3 aceitas, nenhuma devolvida) e **Hemingway** (dados-4 aceita, conferida pelo Turing) seguem em observação. Nenhum diretor está atrás de subagente com prova. Fogg entrega (4 de 4 em 23/11, 12h e 15h em 24/11), mas produção não é resultado de venda.

## 3. Fios parados há 3 reuniões (20, 22, 23 e 24/11)
- **F-001** medição (SDK e eventos): 4 reuniões sem resposta do Davi; o pacote subiu pra 16 itens. Vira D1. Eu continuo devendo o transporte.
- **F-004** vídeos A/B: 4 reuniões, Léo sem resposta; o pedido já é 1 sim/não só sobre A1 e B1 como anúncios. Vira D2 (prazo 26/11 20h).
- **F-005** 1★ de sincronização (Play, 1.0.1): 4 reuniões sem OK; o relógio real é 26/11 (sai da janela da API do Play, previsão do Turing, "provável"). Pergunta com relógio ao Léo hoje, não espera o bilhete.
- **F-002** "plano do SEU modelo": **andou**, não morre em 27/11. O critério de morte era o "sim" do Davi sobre cobertura; o Stark provou no código de 17/11 que CG 160, Pop 110i, Biz e NXR 160 Bros estão no catálogo com tabela oficial. Falta só o Davi dizer que a build de 23/11 não mudou isso (item 6 do pacote). Nome de modelo em loja ou anúncio continua fora até essa resposta.
- Andaram: F-006 (executores; fecha se 25/11 também der 4 de 4) e F-007 (alcance por formato na coleta de 25/11).

## 4. Demandas em cobrança 3
**Nenhuma** (`cobrancas` 0 em todas, nenhuma atrasada no quadro). **Quem está devendo, vencidas e bloqueadas por resposta de líder:**
- **Davi:** `D-20261120-dados-2` (P1, venceu 21/11 20h), `D-20261120-lojas-2`, `mercado-2`, `mercado-4` (23/11), `D-20261120-cria-3` (27/11), `D-20261123-dados-2`, `D-20261122-produto-3` e a nova `produto-3` de hoje (P1, 25/11 18h): todas dentro do pacote de 16 itens.
- **Léo:** `D-20261123-cria-2` (26/11 20h), `D-20261122-ted-1` e `D-20261124-dados-2` (relógio 26/11 12h), domínios das lojas e bibliotecas (`D-20261122-lojas-1`, `master-3`, `mercado-3`, `trafego-2`, `cria-3`; a mesma pergunta em cinco demandas).
- **QG:** a ponte de resumo em % (sete demandas, mais `trafego-1` e `produto-5`).
- **Eu:** o transporte do pacote. Nenhum diretor está devendo por descuido: Turing, Escobar, Cardone, Bezos, Disney, Stark e Greco entregaram o que dependia deles e foram honestos com "sem número". Os executores (Ness, Ted, Hemingway, Fogg, Sun Tzu) não têm nada vencido por culpa própria.

## 5. Iniciativas: o que aprovo e o que corto
| Iniciativa | Veredito | Por quê |
|---|---|---|
| Turing: "De onde vem o alcance?" (alcance por formato) | **Aprovo, prioridade 1** | É a única etapa do topo com número. Destravei o patch hoje; 1ª leitura na coleta de 25/11. |
| Disney + Greco + Bezos: ângulo catálogo ("mais de 370 modelos, escolha na lista") | **Aprovo, fundidas numa só, dono Disney (roteiros) e Bezos (loja)** | Os três propuseram a mesma coisa. Frase liberada por mim. Só roteiros em texto até 27/11 e legendas de benefício nos 3 primeiros prints (a Apple mostra até 3 nos resultados de busca). Nada no ar sem OK. Bezos mata em 30/11 sem base de visita→download; concordo. "Honda sem app" fica fora até a cria-4. |
| Escobar: semana-ponte iOS (1 campanha, link direto da loja, 7 dias) | **Aprovo como proposta; vai ao Léo (D2)** | É o único caminho pra um 1º custo por assinante se o SDK não entrar até 30/11. Verba zero até os portões (incluindo o 6º do Turing: Meta ligada ao AppsFlyer). |
| Cardone: garantia de 30 dias à vista no CTA | **Aprovo o texto; teste vai ao Léo (D3)** | Meu parecer está no arquivo da mkt-2. Condições: só "Garantia de 30 dias", sem "reembolso" até confirmar a Kavoo, sem promessa de renda. Black Friday: não, segue valendo. |
| Stark: plano da moto logo após o cadastro (P-001) | **Mantenho como proposta** | Sem baseline eu não prometo %. Fica no pacote do Davi (itens 13 a 15); sem SDK a leitura é cega. A pergunta "como conheceu o app" (trafego-3) entra depois do cadastro da moto e da tela do plano, como o Stark pede. |
| Greco: IPVA 2027 só SP | **Mantenho (reduzida)** | 4 pautas em texto, escopo SP na capa, "avisa na Garagem" e nunca "te notifica". |
| Pauta "Honda sem app" | **Corto até haver fonte** | Afirmação não provada. |
| Ficha personalizada do Play pra anúncio de Android (lojas-3) | **Corto** | Android fora da 1ª campanha. |
| Volta de agentes da reserva | **Nego** | Ninguém trouxe tarefa real e semanal. |

## 6. Perguntas dos diretores pro Léo que valem a pena (3, juntando repetidas)
Riscadas porque já estão respondidas ou não são dele: a garantia dos Corretores ser de 30 dias, a plataforma (Kavoo), o custo máximo e a meta em degraus (23/11); leitura de gerenciador, App Store Connect, RevenueCat, AppsFlyer (ligados em 23/11, falta a ponte do QG); build, pedido de avaliação, anúncio na tela e histórico entre aparelhos (são do Davi, no pacote); roteirizar vídeo do Léo ou do Davi (Disney; sem demanda dependente); frase "mais de 370 modelos" (eu liberei).
1. **Garantia dos Corretores, termos da Kavoo (Cardone e Disney):** a garantia de 30 dias é reembolso total? Como o cliente pede? A Kavoo manda o reembolso pra UTMify (status "reembolsado")? Resposta curta; só você vê isso no checkout. Sem ela o texto segue sem a palavra "reembolso".
2. **1★ do Google Play e nota (Bezos, Turing e Stark; relógio 26/11 12h, vai hoje pelo QG, não espera o bilhete):** posso publicar a resposta ao 1★ de sincronização (rascunho `ec124592`) e deixar o Ted responder 1 e 2★ de bug com o texto do guia? E qual a nota e o total de avaliações do Play hoje? Resposta de 1 a 3★ só sai com seu OK (`08-regras.md`).
3. **Acesso do ambiente (Bezos, Greco e Escobar; cinco demandas paradas desde 22/11):** libera apps.apple.com, play.google.com e as bibliotecas de anúncios da Meta e do TikTok pros agentes, ou cola título, subtítulo e os 3 primeiros prints das lojas e os 5 anúncios mais antigos de app de moto? E qual endereço o Instagram recusou (OneLink, minhamotopagina.online ou github.io)?

## DECISÕES PRO LÉO

### D1 · Build e medição: o Davi responde o pacote de 16 sim/não (o item 16 primeiro) e o Léo preenche a chave de sandbox do AppsFlyer no RevenueCat
- **título:** Build de 23/11 saiu? SDK AppsFlyer, eventos e `appsflyerID` entram? Chave de sandbox preenchida?
- **ctx:** O repositório do app tem último commit de 17/11 e o SDK segue num ramo (`cadastro/itens.json`); ninguém sabe se a build saiu. 4 reuniões sem resposta do Davi; 8 demandas e a verba do Escobar dependem disso. Texto completo em `demandas/entregas/D-20261123-master-pacote-davi.md`.
- **rec:** **Sim.** Item 16 (a build saiu? versão e dia) primeiro; depois 1 a 3 (SDK, `appsflyerID`, modelo da moto). Se só der um: o SDK. Léo: preencher a chave de sandbox (passo 7 do D+0). Plano B de medição (master-5) segue pronto se o Davi disser não.
- **custo:** ~30 min do Davi pra responder; risco de atrasar a build se o SDK entrar de última hora. Nada de dinheiro.
- **ganho:** custo por assinante por campanha, funil por etapa e por modelo; libera o D+0 do Escobar, a P-001 do Stark e a autópsia da meta. Sem isso a empresa segue sem % da meta.
- **destrava:** `dados-2`, `dados-1`, `produto-3`, `mercado-2`, `mercado-4`, `lojas-2`, `cria-3` (telas), `dados_relatorio-semanal-1` (sandbox), D+0 de medição.
- **prazo:** 25/11 18h (item 16); resto até 27/11.
- **quem:** Davi (pacote); Léo (chave de sandbox).

### D2 · Anúncios: A1 e B1 como os 2 primeiros de teste, e preparar a semana-ponte iOS (sem gastar)
- **título:** Aprovar A1 e B1 como 2 primeiros anúncios e autorizar o Escobar a preparar a semana-ponte iOS
- **ctx:** F-004 parado há 4 reuniões. A1 e B1 (com "por R$19,90" e as lojas; frase do aviso que o Stark aceitou, "o app lembra a troca pelo seu km") já existem. O orgânico (mediana 0,57% por post) não é bancada. A semana-ponte mede o 1º custo por assinante sem SDK, por loja, 7 dias.
- **rec:** **Sim, como direção, sem veredito de ângulo** (A1 e B1 diferem em mais de uma variável). Preparar só: o Escobar propõe a verba e **você aprova antes de ligar**; gasto só depois dos portões e dentro do teto da semana 1 (no privado). A promessa do aviso só vai ao ar com a resposta do Davi nos itens 11 e 12 (selo "Documento vencendo" e telas).
- **custo:** 2 minutos pra ver A1 e B1; nenhuma verba agora.
- **ganho:** o vídeo volta com número em vez de gosto; fecha o F-004; deixa 2 criativos com ID próprio prontos pra 1ª semana paga e troca "zero número" por decisão de escalar ou cortar até 14/12.
- **destrava:** `D-20261123-cria-2`, `D-20261124-trafego-4`, `trafego-3`, o brief do Escobar e o D+0.
- **prazo:** 26/11 20h.
- **quem:** Léo (e Davi se quiser ver a tela).

### D3 · Corretores: V2 de cada estilo = piloto + faixa "Garantia de 30 dias" (e preço R$27,90, sem parcelamento)
- **título:** Isolar a garantia no teste dos 3 estilos dos Corretores
- **ctx:** Os 5 concorrentes levantados têm garantia de 7 dias (provável piso do CDC); a nossa é 30. Hoje a V2 troca gancho e CTA ao mesmo tempo, então o teste não isola nada. Parecer de promessa já dado por mim (`entregas/D-20261123-mkt-2.md`). Custo por venda +19% e vendas por dia −43% em novembro.
- **rec:** **Sim.** V2 = gancho do piloto + faixa "Garantia de 30 dias · R$27,90" / "Clique em Saiba Mais"; cada estilo fica com 2 ganchos em vez de 3. Só depois de você responder a pergunta 1 (termos da Kavoo). Ninguém escreve "reembolso" antes disso.
- **custo:** 1 gancho a menos por estilo (3 peças); nenhuma verba nova (o teste de 23/11 já está decidido). Se a Kavoo impõe condição, o texto muda.
- **ganho:** leitura limpa de uma variável que custa quase nada e pode derrubar o custo por venda; meta do Cardone: −10% contra a versão sem garantia, com reembolso sem subir (alvo dele, não dado).
- **destrava:** reentrega da `D-20261123-mkt-2` (26/11 19h40), produção dos 9 criativos do EXP-20261123-1 e a leitura do Turing.
- **prazo:** 26/11 12h (a Disney reentrega às 19h40).
- **quem:** Léo.

## Pra Folha de sexta (27/11)
- **Shelby:** repetição do transporte do pacote do Davi (21, 23 e 24/11), −10 já anotado; avaliação do Léo e do Davi. Mérito: corrigi sozinho 5 itens e cancelei 5 demandas caducas.
- **Sun Tzu:** erro de fonte (generalizou além da AutoPapo): registro no broche, sem multa se a `master-1` for aceita de primeira; −10 se voltar devolvida.
- **Greco:** repetiu a afirmação na r1, sem verificar: erro leve de fonte, sem multa; aviso na ata.
- **Escobar:** sobrescreveu e restaurou `trafego-1`: erro confessado, broche cai um degrau, sem multa.
- **Ness:** nenhuma pendência hoje.
- **Elogio:** Jobs (P-001 + código lido), Turing (alcance com conta conferida e recusa do número que não leu).
