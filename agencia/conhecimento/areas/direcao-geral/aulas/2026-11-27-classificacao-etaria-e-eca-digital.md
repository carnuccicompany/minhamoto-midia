# Aula 27/11/2026 · Classificação etária e ECA Digital pra app de assinatura no Brasil

Para: Thomas Shelby (Direção-Geral e Jurídico) e Eliot Ness (auditoria), com cópia útil pra Bezos (Lojas), Stark e Jobs (Produto) e Escobar (Tráfego).
Por que importa agora: a Apple fecha o questionário novo em **12/01/2027**, o Google passa a mandar sinal de idade pra todo usuário até **11/12/2026** e a ANPD começa a **fiscalizar aferição de idade em janeiro de 2027**. Resposta errada no questionário trava envio de atualização ou derruba o app. Classificação alta demais corta download no Brasil. Os dois erros custam venda.
Legenda das fontes: **[OF]** oficial lido direto · **[OF*]** oficial citado por terceiro com o link oficial (conferir antes de virar regra dura) · **[ESP]** especialista ou escritório · **[CASA]** fato nosso, com prova no repositório.
O que já existia na biblioteca e aqui não se repete: FUNDAMENTOS §4 (resumo do ECA Digital, bloqueio de 18+ na Apple desde 24/02/2026) e NOVIDADES 02/11 (aviso dos descritores). Esta aula aprofunda: tabela do Brasil, o que cada loja exige, a régua do "acesso provável" e o processo.

## 1. O que é: três camadas que não se confundem
1. **Classificação etária da loja.** Cada loja pergunta o que o app tem e calcula a faixa. **Apple:** questionário próprio no App Store Connect, com faixa global (4+, 9+, 13+, 16+, 18+) e uma faixa do Brasil autodeclarada (AL, A6, A10, A12, A14, A16, A18) [OF]. **Google Play:** questionário da IARC; a autoridade de cada região (no Brasil, a ClassInd do Ministério da Justiça) dá a faixa a partir das respostas [OF].
2. **ECA Digital (Lei 15.211/2025, em vigor desde 17/03/2026).** Vale pra produto digital **direcionado** a menores ou de **"acesso provável"** por eles (art. 1º). Quem oferece conteúdo **impróprio ou proibido** pra menor tem que impedir o acesso com verificação de idade confiável a cada acesso, e a autodeclaração não vale (art. 9º, §1º). Lojas e sistemas operacionais aferem a idade e mandam um sinal por API (art. 12). App direcionado ou de acesso provável tem que **receber** esse sinal e manter mecanismo próprio (art. 14) [OF].
3. **APIs de sinal de idade.** Apple **Declared Age Range** (iOS, iPadOS, macOS) e Google **Play Age Signals** devolvem a faixa (padrão do Google: 0–12, 13–15, 16–17, 18+) quando o usuário ou o responsável aceita compartilhar [OF]. A obrigação de usar vem da lei e do risco do app, não da faixa da loja: "a classificação etária não substitui a verificação de idade exigida por lei" (Apple, Q&A em português) [OF].

## 2. A tabela do Brasil na Apple (o que empurra a faixa pra cima)
Fonte: App Store Connect Help, "Age ratings", seção Brasil [OF] (https://developer.apple.com/help/app-store-connect/reference/age-ratings).
| Faixa BR | Entra se o app tiver (exemplos) |
|---|---|
| **AL** | nada impróprio; pode ter controle parental e verificação de idade |
| A6 | conteúdo gerado por usuário; violência de desenho rara |
| A10 | palavrão raro; tema de saúde e bem-estar |
| **A12** | **publicidade dentro do app**; mensagens e chat; informação médica rara |
| A14 | terror frequente; álcool, tabaco ou drogas raros |
| **A16** | **acesso livre à web** (navegador embutido); rede social; **localização compartilhada** |
| **A18** | **namoro e relacionamentos**; **loot box**; jogo de azar frequente; nudez frequente |
- "Publicidade" na Apple é **anúncio pago mostrado dentro do app** (banner, vídeo, nativo) [OF]. SDK de atribuição (AppsFlyer) não é publicidade dentro do app.
- Faixa oficial do Ministério da Justiça (MJSP), quando existe, substitui a autodeclarada na loja do Brasil; dá pra pedir faixa menor ao MJSP se o recurso for feito pra família (ex.: localização entre pais e filhos) [OF] (https://developer.apple.com/news/?id=yxkh08us).
- App sem classificação não é publicado na App Store [OF].

## 3. Prazos, com data
| Data | O quê | Fonte |
|---|---|---|
| 31/01/2026 | Prazo das perguntas novas da Apple (controles, recursos, saúde, violência); quem não respondeu tem envio de atualização interrompido | [OF] https://developer.apple.com/news/?id=ks775ehf |
| 24/02/2026 | Apple bloqueia no Brasil o download de app 18+ por quem não foi confirmado adulto; loot box vira 18+ no Brasil | [OF] https://developer.apple.com/news/?id=f5zj08ey |
| 17/03/2026 | ECA Digital em vigor; Play Age Signals responde no Brasil | [OF] Planalto, art. 41-A; Android Developers |
| ago–nov/2026 | Período de adaptação da ANPD | [OF] https://www.gov.br/anpd/pt-br/assuntos/eca-digital |
| 16/11/2026 | Descritores "Localização compartilhada" e "Namoro e relacionamentos" no questionário da Apple; obrigatórios em toda atualização enviada | [OF] news yxkh08us |
| **11/12/2026** | Play Age Signals 0.0.6 responde pra todos os usuários ("até 11/12/2026") | [OF] release notes, 19/11/2026 |
| **12/01/2027** | Todos os apps da Apple com os dois descritores respondidos | [OF] news yxkh08us |
| **jan/2027** | ANPD começa a fiscalizar, com foco em aferição de idade | [OF] cronograma ANPD |
| sem data | Guia definitivo de aferição e guia de fornecedores da ANPD (em consolidação; página alterada em 24/11 sem versão nova) | [OF] |

## 4. Obrigatório x recomendado (pra um app adulto sem conteúdo impróprio)
**Obrigatório**
- Questionário da Apple completo e verdadeiro, com os 2 descritores novos até 12/01/2027 (antes, se sair atualização) [OF].
- Questionário da IARC no Play Console completo e verdadeiro; app sem classificação é removido; refazer quando recurso ou conteúdo mudar; deturpar o conteúdo pode levar a remoção ou suspensão; o anúncio não pode ser mais adulto que o app [OF] (https://support.google.com/googleplay/android-developer/answer/9898843?hl=en).
- No Brasil o Play bloqueia ou filtra app 18+ pra quem é identificado como menor; loot box pode exigir refazer o questionário [OF] (https://support.google.com/googleplay/android-developer/answer/6223646).
- ECA Digital, sempre: não fazer perfil de menor pra direcionar publicidade (art. 22) e não usar tela manipuladora em serviço acessível a menor (art. 18 e Q&A da ANPD) [OF].

**Só passa a ser obrigatório se o app mudar**
- Receber o sinal de idade (Declared Age Range / Play Age Signals) e ter mecanismo próprio: art. 14, só pra app direcionado ou de acesso provável [OF].
- Verificação de idade sem autodeclaração a cada acesso: art. 9º, só pra conteúdo impróprio ou proibido pra menor [OF]. Manutenção de moto não está na lista de proibidos do Q&A (álcool, armas, aposta, pornografia) [OF].

**Recomendado (é o que o top 1% faz)**
- Avaliação de "acesso provável" escrita em 1 página, com data e prova (seção 5).
- Faixa mínima de idade 18 nos anúncios e público-alvo 18+ declarado no Play Console [confirmar na tela de cada um].
- Política de privacidade com uma linha: "o app não é destinado a menores de 18 anos e não coleta dados de menores de propósito".

## 5. A régua do "acesso provável" (onde mora o risco jurídico)
- **Texto da lei (art. 1º, parágrafo único):** (I) probabilidade de uso por ser atrativo pra menor; (II) facilidade considerável de acesso e uso; **e** (III) risco relevante à privacidade, segurança ou desenvolvimento, sobretudo em serviço com interação social e compartilhamento amplo entre usuários [OF].
- **Proposta de guia da ANPD:** lê os três critérios como **cumulativos**; sinais são tema infantil, visual atrativo, publicidade mirada, semelhança com serviço usado por menores e dado de uso real. Aviso de idade, termos de uso e autodeclaração **não afastam sozinhos** o acesso provável. O Decreto 12.880/2026 presume acesso provável em rede social, jogo e IA generativa [ESP] (Data Privacy Brasil, 18/06/2026: https://dataprivacy.com.br/escopo-e-afericao-de-idade-entenda-as-propostas-de-guias-da-anpd/). O guia final pode mudar isso.
- **Prova vale, papel não:** no caso Discord a ANPD disse que informar a política de aferição "não converte informação prestada em prova de suficiência" (CD 35/2026, votos de 16 a 18/11/2026) [OF]. Por isso a avaliação tem que apontar fato verificável, não intenção.
- **Multa (art. 35):** advertência com prazo de até 30 dias; multa de até 10% do faturamento do grupo no Brasil, teto de R$ 50 milhões por infração; suspensão e proibição só pelo Judiciário [OF].

## 6. Como o top 1% faz (processo enxuto, 30 minutos por versão)
1. **Mapa recurso → descritor.** Uma tabela viva: cada recurso do app e a linha do questionário que ele toca (chat → A12; localização compartilhada → A16; navegador livre → A16; anúncio dentro do app → A12). Quem cria recurso novo atualiza a linha antes do envio.
2. **Responder pela versão que vai pra loja**, não pelo `main`: mesmo princípio que já vale pras telas (DESIGN-MINHAMOTO, 23/11).
3. **Print das respostas** (Apple e Play) guardado a cada envio; a faixa resultante anotada com a data. É a prova se a loja ou a ANPD perguntar.
4. **Não inflar a faixa "por segurança".** Marcar 18+ sem precisar ativa o bloqueio de download no Brasil pra quem não confirmou ser adulto (Apple, desde 24/02/2026; Play filtra menor) [OF]: perde instalação e não ganha proteção nenhuma.
5. **Avaliação de acesso provável** (1 página, revista a cada recurso social novo): público, tema, preço, canal de venda, interação entre usuários, dado coletado, faixa das lojas, idade nos anúncios. Conclusão e quem assinou.
6. **Sinal de idade só quando o risco existe.** A Apple diz que a obrigação "depende da região e da lei, não da classificação" e que a API "está disponível no mundo todo" [OF]; o Google diz que um app de clima "não deveria precisar" das mesmas proteções de um app de mídia [OF] (Android Developers Blog, 29/07/2026). Integrar sem necessidade é custo de produto e mais dado de idade pra proteger (art. 13 restringe o uso).
7. **Calendário com dono.** Prazos de loja e de lei no calendário do Diretor-Geral, com 30 dias de folga.

## 7. Onde o MinhaMoto está hoje [CASA, a confirmar pelo Davi]
Leitura só do código (commit d4942b2, 25/11/2026, versão 1.0.2), sem mexer em nada:
- **Não tem:** localização (nenhuma permissão de local no Android nem no iOS), chat, comunidade, anúncio dentro do app, namoro, loot box, conteúdo de saúde.
- **Tem:** navegador aberto só pra gerenciar a assinatura (link fixo, não é "acesso livre à web"); compartilhar convite e histórico pelo menu do celular (não é rede social); câmera e fotos pra documentos da moto, que ficam na conta da pessoa (não é conteúdo visto por outros usuários); SDK do AppsFlyer com rastreio pedido pelo ATT (não é publicidade dentro do app).
- **Faixa esperada:** AL no Brasil e 4+ global na Apple; Livre (L) na ClassInd pelo Play. **Faixa real:** sem dado aqui (o painel de cada loja não abre nesta sessão). Quem confirma: Léo ou Davi, com print.
- **Acesso provável:** baixo nos três critérios: tema adulto (moto exige CNH, que só sai aos 18), venda por assinatura paga na loja, anúncio mirado em adulto e nenhuma interação entre usuários. Não é parecer de advogado: é a avaliação da casa, pra ser escrita e assinada.

## 8. Erros comuns
1. Marcar "Publicidade" porque o app usa AppsFlyer ou Meta: o app vira A12 sem ter anúncio.
2. Subir pra 18+ "pra não ter problema" e perder o download de quem não confirmou idade no Brasil [OF].
3. Esquecer de refazer o questionário quando entra recurso novo (chat, ranking, localização): a Apple trava o envio, o Play pode remover por deturpação [OF].
4. Achar que aviso "proibido para menores" nos termos resolve: não afasta o acesso provável [ESP].
5. Integrar a API de idade e guardar a faixa junto do perfil de marketing (o art. 13 limita o uso do dado de verificação à própria verificação) [OF].
6. Anúncio com linguagem, personagem ou visual infantil: é sinal de atratividade (critério I) e o Play não aceita anúncio mais adulto ou mais infantil que o app [ESP][OF].
7. Responder pelo código do `main` com recurso que ainda não está na loja, ou o contrário.
8. Deixar o prazo de 12/01/2027 pra última semana, no meio das festas de fim de ano, sem folga pra uma rejeição e um reenvio (conferir se a Apple publica aviso de recesso da revisão em dezembro).

## 9. Como aplicamos aqui (checklist: quem, o quê, até quando)
Regra que manda em tudo: **o código do app é só leitura pros agentes; nada vai pro app, pro App Store Connect ou pro Play Console sem OK do Léo ou do Davi.** Os agentes preparam; quem clica é dono de conta.
| # | Quem | O quê | Até quando |
|---|---|---|---|
| 1 | Shelby (prepara) → Léo ou Davi (faz) | Print da classificação atual nas duas lojas (Apple: faixa global e do Brasil; Play: certificado IARC e ClassInd). Entra como 1 pergunta no pacote do Davi, sem notificação nova | plano da semana de 30/11/2026 |
| 2 | Davi | Na próxima atualização (ou até **05/01/2027**, folga de 1 semana), responder **"Não"** em Localização compartilhada e **"Não"** em Namoro e relacionamentos na Apple; conferir que "Publicidade" está "Não" | 05/01/2027 (prazo Apple 12/01/2027) |
| 3 | Davi | Play Console: questionário IARC conferido com o app 1.0.2; público-alvo declarado só 18+ [confirmar o nome da tela] | 11/12/2026 |
| 4 | Shelby | Avaliação de "acesso provável" do MinhaMoto em 1 página (seção 5 e 7), em `agencia/diretoria/` ou na pasta do jurídico, com prova de cada ponto | 18/12/2026 |
| 5 | Stark e Jobs | Mapa recurso → descritor (seção 6, item 1) na ficha do produto; toda proposta nova pro Davi diz se mexe na classificação | junto da próxima proposta |
| 6 | Escobar | Conjunto de anúncio do MinhaMoto e dos Corretores com idade mínima 18 [confirmar no Gerenciador se é controle fixo]; nenhum criativo com cara de público infantil | antes da 1ª verba (DECISÃO 1 de 26/11) |
| 7 | Shelby | Linha "não destinado a menores de 18" na política de privacidade do app, na próxima revisão dos termos (sobe pro Davi, que publica) | 12/01/2027 |
| 8 | Ness | Na auditoria de proposta de recurso: "isso mexe na classificação?" é pergunta obrigatória; se sim, volta com a linha do questionário | sempre |
| 9 | Shelby | Reler a página do ECA Digital da ANPD toda segunda até o guia definitivo sair; se o guia mudar a régua do acesso provável, refazer o item 4 | semanal |
- **Gatilhos que reabrem tudo:** chat, comunidade, ranking público, localização compartilhada, anúncio dentro do app, sorteio ou caixa de prêmio, conteúdo de saúde. Qualquer um deles: Shelby refaz a avaliação e o Davi refaz os questionários antes do envio.
- **Corretores (infoproduto na Kavoo):** não tem loja nem questionário. O que vale é não mirar anúncio em menor (art. 22) e seguir o CONAR quando houver influenciador (NOVIDADES, vigente).
