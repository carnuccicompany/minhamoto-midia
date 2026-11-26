# Thomas Shelby (Direção-Geral e Jurídico) · fechamento do Conselho · 26/11/2026

Base: 10 posições (7 r1 e 3 r2), 22 demandas novas de 26/11, `fios.md`, `decisoes.md`, `conhecimento/`, `cadastro/itens.json`, entregas de 23 a 25/11, painéis e memórias. **O `carnucci-dados` (privado) não abre nesta sessão: a ponte de % (`dados/resumo-pct.json`, pendência do QG desde 23/11) segue sem existir, então não há % da meta nem funil abaixo do topo, e o briefing privado depende do QG.** Sem R$ de receita e sem número absoluto de assinantes. Quadro regenerado: 0 atrasadas, 26 abertas ou em andamento, 12 entregues, 63 aceitas, 19 bloqueadas pro líder. JSON de todas as demandas válido; `vigia_segredos.py`: nenhum segredo. **Nada grave que não possa esperar até as 9h.**

## A. Ronda: o que corrigi e quem acionei

**Corrigi (no alcance do repositório), 1 linha cada**
- **Pix dos Corretores (D-20261126-mkt-2):** o Léo cancelou em 25/11 e NUCLEO, LICOES, FUNDAMENTOS, NOVIDADES, a aula de 25/11, `06-historico.md`, `estudio/produtos/corretores.md` §8 e `rodizio.json` ainda diziam "adiada"; agora todos dizem "cancelada, não propor de novo". Kavoo ganhou link e data em FONTES e NOVIDADES (texto comercial, Pix e reembolso não confirmados).
- **`PENDENCIAS.md` l.105 (D-20261126-dados-2):** "custo por teste iniciado" trocado por custo por assinante pago (o app não tem teste grátis); anotei a decisão do Léo de 26/11 (landing → loja, IC). `D-20261125-master-1` saiu do coletor (reserva) e foi pro Hemingway (ativo).
- **`decisoes.md`:** a decisão do Léo de 26/11 estava solta no fim do arquivo, sem data; agora está no bloco 26/11, junto com o fato de que **a compra e o cadastro do app passaram a chegar na Meta** (QG mapeou no AppsFlyer em 26/11, `trafego/LICOES.md`).
- **`trafego/LICOES.md`:** dizia "ou pra StartTrial" como evento de volume; o app não tem teste grátis, StartTrial nunca dispara. Risquei e expliquei.
- **`trafego/NUCLEO.md`:** afirmava "BM só de anúncios reaberta em 25/11 (decisão do Léo)"; não há registro. Corrigi: foi proposta do Escobar, decisão pendente (agora DECISÃO 3).
- **Pacote do Davi (D-20261126-produto-1, D-20261124-produto_analista-do-paywall-1):** reescrito em v3: 19 itens viraram 9 perguntas (A a I); SDK, `appsflyerID` no RevenueCat, postbacks e tela "Esse é o MinhaMoto" riscados com a prova do código de 25/11 lido pelo Stark (a confirmar pelo Davi); anexo da P-001 incluído; a pergunta que vai primeiro (A: a 1.0.2 está nas lojas? que dia?) o Léo responde olhando as lojas.
- **Demandas minhas fechadas:** `D-20261126-trafego-3` (entregue: os 2 sim/não são a DECISÃO 1); `D-20261125-trafego-2` (aceita, com a ressalva de que nenhum passo de menu da Meta foi confirmado no oficial); `D-20261120-mercado-2` cancelada (superada por mercado-1, catálogo dos 4 líderes provado); `D-20261126-trafego-2` bloqueada (a leitura de `developers.facebook.com` foi negada também aqui; não inventei confirmação).
- **Fios e quadro:** `fios.md` atualizado (5 reuniões, F-008 novo); quadro regenerado.

**Acionei (demandas de correção e estratégica, diretor em cópia)**
- **Turing** `D-20261126-master-1` (P1, 27/11 20h, cc Escobar e Stark): o portão 6 (Meta ligada ao AppsFlyer) já passou em 26/11; atualizar dados-5 e trafego-4. Turing e Escobar escreveram "hoje não passa" nas r1 e r2: desatualizado, sem multa (o registro estava numa lição do QG, não numa decisão que eles lessem).
- **Greco** `D-20261126-master-2` (estratégica 1, P3, 03/12, cc Stark, Turing, Disney): mapa de entrada do MinhaMoto na gringa (Portugal, EUA, Reino Unido), só pesquisa. Cardone foi o único que trouxe iniciativa pro norte de 25/11; os outros cinco não disseram nada. Lembrete registrado na memória de todos: toda iniciativa diz se aproxima a empresa da gringa (`CULTURA.md`).
- **Fogg** `D-20261126-cria-3` (já aberta pela Disney, P1, 27/11 19h): causa e id dos slots de 18h de 24 e 26/11. Eu cancelei a anterior em 24/11 com "reabre se falhar"; falhou, a falha é de processo meu e dele.
- **Ness** `D-20261126-dados-3` (já aberta pelo Turing): ids do Play por coleta no status, pra provar a janela de 7 dias.

**Conferência das correções de 24/11**
- **Fechadas:** `D-20261124-master-1` (Sun Tzu, escopo da fonte; aceita), `D-20261124-master-2` (Turing, contrato do resumo em %; aceita), `D-20261123-master-1` (Escobar, destino do anúncio; aceita), `D-20261124-mercado-4` e `cria-4` (Honda; aceitas, sem "não tem app"), `D-20261125-dados-1` (entregue "sem dado"). Greco corrigiu sozinho a leitura de mercado dele hoje.
- **Segue aberta e é minha, repetida:** o transporte do pacote e a **ponte de % do QG** (o arquivo `dados/resumo-pct.json` ainda não existe 3 dias depois da especificação aceita). Não alcanço o Léo nem o Davi desta sessão. **Pra Folha de sexta (27/11):** repetição da falha de transporte (21, 23, 24 e 26/11), −10 já anotada em 23/11; multa adicional é dos donos, que avaliam o Diretor-Geral.

## 1. Gargalo do funil
**App (assinantes pagos novos): a aquisição no topo ainda não começou, e o começo depende de 3 fatos de cima.** A única etapa com número é o alcance: o de 28 dias da conta foi de 10.001 pra 10.006 (+0,05% de 25 pra 26/11) e 98,9% dele é anúncio (9.892 de 10.001; feed 1,8%, story 1,3%, carrossel 1,1%); a mediana por post de feed é 13 pessoas, com 2 salvamentos e 1 compartilhamento nos 60 posts (`dados/insights-2026-11-26.json`, conferido por mim contra o arquivo: bate com Turing e Disney). O orgânico não carrega a meta. Etapas abaixo do topo (loja, cadastro, paywall, pago): **sem número, então sem culpado**. O que mudou hoje: o Léo decidiu começar pela landing → loja otimizando IC, o app 1.0.2 e o SDK estão no código, e a compra chega na Meta. O que ainda segura o primeiro pagante lido: (1) o sim do Léo no dia 1 (DECISÃO 1), (2) a 1.0.2 estar nas lojas e o dia (PERGUNTA 1), (3) a ponte de % do QG pra ler o RevenueCat. IC mede clique pra loja, não assinante: a régua é custo por assinante pago em % do teto do privado, e iOS fica separado de Android.
**Infoprodutos (Corretores): criativo cansado e queda na entrada da página.** Último público (UTMify, `09-numeros.md`, 23/11): vendas por dia −43%, gasto −32%, custo por venda +19%, ROAS de 1,88 pra 1,61; visualização de página por clique de ~92% pra ~75% (página aliviada em 23/11). Sem número novo hoje: a semana isolada, o reembolso e a meta semanal dependem da ponte. O remédio é criativo novo (6 estilos, o Léo aprova peça a peça no Estúdio). Recuperação de Pix cancelada: não é mais alavanca.

## 2. Quem supera algum diretor (tomada de cadeira)
Ninguém. A regra pede 4 semanas seguidas com prova e o piloto tem uma. Em observação, sem comparação ainda: **Sun Tzu** (mercado-4 entregue 12 h antes do prazo, aceita), **Ted Lasso** (coletas e lojas-2 no prazo), **Jobs** (3 aceitas, nenhuma devolvida, leu código antes de propor) e **Hemingway** (tem dados-3 devolvida com 2 linhas faltando e relatório de 30/11 por vir: não entra). Nenhum diretor está atrás de subagente com prova.

## 3. Fios parados há 3 reuniões (20, 22, 23, 24 e 26/11)
- **F-001** medição: 5 reuniões sem resposta do Davi; **andou por fora dele** (SDK no código de 25/11, compra na Meta). Falta A (1.0.2 nas lojas, que dia) e B (3 eventos).
- **F-004** vídeos A/B: 5 reuniões sem o Léo; virou DECISÃO 1.
- **F-005** 1★ de sync: 5 reuniões; a janela de 7 dias fecha por volta de 18h35 BRT de hoje (hipótese do Turing, prova em 27/11). Vira morte por relógio, sem pergunta.
- Andaram: F-002 (4 líderes provados), F-006 (25/11 fechou 4 de 4; 18h de 24 e 26/11 sem post provado, Fogg), F-007 fechado.

## 4. Demandas em cobrança 3
**Nenhuma** (`cobrancas` ≥ 1 só em `D-20261120-master-1`, já aceita; nenhuma atrasada). **Quem está devendo (bloqueadas por resposta):**
- **Davi:** `D-20261120-dados-2` (venceu 21/11), `D-20261122-produto-3`, `D-20261123-dados-2`, `D-20261124-produto-3`, `D-20261120-cria-3` (telas, 27/11 18h): tudo dentro do pacote v3.
- **Léo:** `D-20261123-cria-2` (venceu hoje 20h; é a DECISÃO 1), `D-20261123-trafego-1` (nomes; entra na DECISÃO 1), `D-20261124-dados-2` e `D-20261122-ted-1` (1★ e nota do Play; vão morrer por relógio), domínios das lojas (cinco demandas de pesquisa de concorrente; ver Perguntas).
- **QG:** a ponte de resumo em % (trava lojas-2, trafego-1, mkt-1, lojas-3, produto-5, mercado-3 e a leitura do Turing).
- **Eu:** o transporte do pacote e o relatório de 27/11. Executores e diretores: nada vencido por descuido. Fogg deve a causa do 18h (P1, 27/11 19h).

## 5. Iniciativas: o que aprovo e o que corto
| Iniciativa | Veredito | Por quê |
|---|---|---|
| Escobar: "Primeiro clique que vira assinante" (1 campanha Meta, landing → loja, IC, 7 dias, A1/B1) | **Aprovo como proposta; vai ao Léo (DECISÃO 1)** | É o primeiro caminho pra um custo por assinante lido. Régua: assinante pago, corte em % do teto, sem verba antes do OK. |
| Disney: "o clique barato não é o assinante" (dois níveis de leitura) | **Aprovo, fundida com a do Escobar**; **2 anúncios no dia 1, não 12** | Ela mesma recuou na r2: sem baseline, 12 slots dividem o sinal. Os 10 restantes só depois da 1ª leitura. |
| Turing: "Cobertura da landing até a compra" | **Aprovo, prioridade 1 dos dados** | Corta a decisão no escuro. Limites numéricos "a calibrar" até haver baseline; o corte "mais de 80% Android" é hipótese dele, não premissa. |
| Stark: "Funil visível" (3 eventos no SDK) | **Aprovo como proposta pro Davi (pergunta B)** | Sem ele "não cadastrou" e "viu e não pagou" são a mesma coisa. Nada é escrito sem o OK do Davi. |
| Greco: variante "a landing da SUA CG 160" | **Seguro: 2º teste, só depois da 1ª leitura de A1/B1** | Escobar e Disney têm razão: sem baseline, 2 variáveis na mesma verba não decidem nada. Texto da Disney (mercado-1) segue em rascunho, só "Biz 125", nunca "Biz". |
| Bezos: loja alinhada ao anúncio (3 primeiros prints) | **Mantenho, morre em 07/12 sem base** | Depende de A1/B1 e da tela da build. Nada na loja sem OK do Léo. |
| Cardone: garantia à vista de 30 dias no teste | **Aprovo; vai ao Léo (DECISÃO 2)** | Parecer de promessa já dado (24/11). |
| Cardone: Mapa Visual EUA e Portugal | **Aprovo a pesquisa** (zero gasto, nada no ar), veredito sim/não até 03/12 | Aproxima a empresa do norte de 25/11. Fonte da NAR é blog (confirmar); Kavoo fora do Brasil a checar. |
| Escobar: BM Operação antes de escalar | **Aprovo o plano; sim/não vai ao Léo (DECISÃO 3)** | Ponto único de falha (Matriz) já destruiu o Perfect Class. Escala é depois da 1ª leitura, então não bloqueia o dia 1. |
| Pedido de trazer agente da reserva ou criar novo | **Nego** | Ninguém trouxe tarefa real e semanal. |

## 6. Perguntas dos diretores pro Léo que valem a pena (3, juntando repetidas)
Cortadas, e por quê: **nota do Google Play e OK do 1★ ec124592** (Bezos, Turing, Stark, Disney, em 5 reuniões): n=7, o 1★ sai da janela hoje e o Léo responde no Console quando quiser; **domínios das lojas e das bibliotecas de anúncios** (Bezos, Greco, Escobar): cinco demandas de pesquisa de concorrente, P2/P3, não valem pergunta antes do 1º anúncio; ficam bloqueadas com a pergunta pronta; **"Honda e Biz"** (Greco): é minha, regra de redação; **A1/B1 e data do 1º anúncio** (Disney, Escobar, Turing): virou DECISÃO 1; **o pedido de avaliação no app e o botão de teste de aviso** (Stark): vão ao Davi, pacote v3.

**PERGUNTA 1 · A 1.0.2 já está nas duas lojas? Que dia?**
- **rec:** sim/não e a data, olhando App Store e Play (10 segundos).
- **custo:** nenhum.
- **ganho:** libera o relógio do vigia de 72 h, a primeira leitura do funil e a data certa do dia 1; era o item que o Davi não respondia há 5 reuniões (Stark, Turing, Escobar, Disney, Bezos).
- **prazo:** hoje (a primeira da lista; antes do bilhete de sexta).

**PERGUNTA 2 · A primeira tela da landing mostra "R$19,90" e a escolha da moto? O dia 1 roda em iOS e Android ou só iOS (o bug de sync do Android segue)? Qual endereço o Instagram recusou?**
- **rec:** respostas curtas; o anúncio tem que dizer o que a landing diz. Recomendo o dia 1 só em iOS enquanto o bug de sync do Android existir (Disney e Escobar).
- **custo:** nenhum.
- **ganho:** a Disney fecha o texto do anúncio sem inventar, o Escobar fecha o destino, e não se queima verba em Android com sincronização quebrada.
- **prazo:** 27/11, antes da ficha da Disney (28/11 21h).

**PERGUNTA 3 · Corretores: a garantia de 30 dias é reembolso total pela Kavoo? Como o cliente pede? A Kavoo manda o reembolso pra UTMify? O Acesso Essencial (R$27,90) listar os mesmos itens do Completo é erro da página?**
- **rec:** respostas curtas, só você vê isso no checkout.
- **custo:** nenhum.
- **ganho:** libera a palavra "reembolso" (hoje proibida), isola a garantia no teste e conserta, se for erro, o motivo de escolher o Completo.
- **prazo:** 29/11.

## DECISÕES PRO LÉO E O DAVI

**DECISÃO 1 · Dia 1 da campanha MinhaMoto: landing → loja, A1 e B1 como os 2 primeiros anúncios, e a data**
- **título:** Escobar prepara a proposta (1 campanha Meta, 1 conjunto aberto, minhamotopagina.online com UTMs, evento IC do pixel novo, 7 dias, nome `mm_meta_ic_lp_2611`) e A1/B1 são os 2 anúncios. Junta D-20261123-cria-2, D-20261126-trafego-3 e D-20261123-trafego-1 (nomes).
- **rec:** **Sim, nos dois, sem veredito de ângulo** (A1 e B1 diferem em mais de uma variável). Verba só depois que você aprovar a proposta, dentro do teto da semana 1 do privado; e a promessa do aviso só vai ao ar com o Davi confirmando o selo "Documento vencendo" e as telas da 1.0.2 (pergunta F do pacote). Data sugerida: assim que a 1.0.2 estiver nas lojas (pergunta 1) e o Escobar fechar a URL com UTMs (27/11).
- **custo:** 2 minutos pra ver A1 e B1; nenhuma verba agora.
- **ganho:** troca 7 rodadas de "zero número de campanha" por o primeiro custo por assinante pago lido (ou "sem sinal") até 07/12; fecha o F-004; a compra já chega na Meta.
- **prazo:** 27/11 (venceu hoje 20h na cria-2).
- **quem:** Léo (Davi só se quiser ver a tela).

**DECISÃO 2 · Corretores: V2 de cada estilo = gancho do piloto + faixa "Garantia de 30 dias · R$27,90"**
- **título:** isolar a garantia no teste dos 3 estilos.
- **rec:** **Sim**, só depois de você responder a pergunta 3 (termos da Kavoo); ninguém escreve "reembolso" antes disso. Parecer de promessa já dado por mim (`entregas/D-20261123-mkt-2.md`); sem renda prometida, sem Black Friday.
- **custo:** 1 gancho a menos por estilo (3 peças no total); nenhuma verba nova (o teste já está decidido de 23/11).
- **ganho:** leitura limpa de uma variável que custa quase nada e pode baixar o custo por venda (alvo do Cardone: −10% contra a versão sem garantia, com reembolso sem subir; alvo dele, não dado).
- **prazo:** 29/11.
- **quem:** Léo.

**DECISÃO 3 · BM Operação (blindagem) antes de escalar qualquer verba**
- **título:** você monta uma BM separada ("Operação": contas de anúncio novas, 1 conta de reserva, dois administradores com 2 fatores, pixel e página compartilhados pela Matriz) antes de escalar o MinhaMoto e antes de campanha nova dos Corretores. Plano em `entregas/D-20261125-trafego-2.md`.
- **rec:** **Sim**, em ordem: primeiro as 5 conferências do mapa (10 minutos, em Configurações da empresa), depois a BM. **Não toque na CA 01 nem nas campanhas ativas dos Corretores.** Os passos de menu da Meta estão marcados "confirmar no oficial" (o ambiente não abriu as páginas); aja só no que você vê na própria tela e me diga o que não bate.
- **custo:** algumas horas suas; meio de pagamento da conta de reserva é decisão sua. Zero verba.
- **ganho:** tira o ponto único de falha que derrubou o Perfect Class (pixel e anúncio na mesma BM); com a queda, a conta reserva sobe em horas e o pixel guarda o aprendizado. Não bloqueia o dia 1 (primeira leitura é com verba pequena); é pré-condição de escala.
- **prazo:** 07/12 (antes de escalar).
- **quem:** Léo.

## Pra Folha de sexta (27/11)
- **Shelby:** repetição do transporte do pacote do Davi e ponte de % do QG ainda inexistente (−10 já anotada em 23/11; avaliação dos donos). Mérito: corrigi sozinho 8 pontos de memória e playbook e fechei 5 demandas.
- **Disney:** mudou de posição com número (12 slots → 2), aceita 5 e devolveu 1; **elogio**.
- **Greco:** corrigiu a própria leitura de mercado com fonte; **elogio**.
- **Turing e Escobar:** "portão 6 não passa" desatualizado, sem multa (fato novo era do QG); **Turing** reconheceu hipótese como hipótese; **elogio**.
- **Stark e Jobs:** leram o código antes de perguntar ao Davi e ajudaram a cortar o pacote de 19 itens para 9 perguntas; **elogio**.
- **Fogg:** deve a causa do 18h (P1, 27/11 19h); se falhar, −5 (cobrança sem resposta).
- **Hemingway:** dados-3 devolvida (faltam 25 e 26/11); sem multa até 27/11 19h.
