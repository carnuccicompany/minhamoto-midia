# Design Corretores: a régua do Léo (INICIAL, a lapidar com o Léo)

> Mesmo formato do `agencia/DESIGN-MINHAMOTO.md`. **Todo agente e o Estúdio leem este arquivo antes de criar qualquer peça dos Corretores** (Mapa Visual Completo do Fechamento Imobiliário).
> Versão inicial de 23/11/2026, inferida do material que já rodou (criativos da Ana Paula, lotes TESTES 1, estáticos, copies e ângulos do Léo). **Nada aqui foi aprovado pelo Léo ainda:** cada feedback dele vira regra aqui, na hora, e a regra antiga fica ~~riscada~~ com "→ substituída em DD/MM". Vale sempre o mais recente.
> Formato de cada regra: **REGRA** · ❌ errado · ✅ certo · data.

> **Regras de equipe e jeito de trabalhar do Léo:** ver "★ CONSTITUIÇÃO DO ESTÚDIO" no topo do `DESIGN-MINHAMOTO.md` (vale pros dois produtos: não repetir erro já corrigido, toda alteração vira regra na hora e a equipe toda lê, pesquisa de mercado constante, autonomia e avisos).

## 0. ★ FEEDBACK DO LÉO 25/11 (vale acima de tudo neste arquivo)
Os 13 criativos de 24/11 foram reprovados. O que ele disse, virando regra:
- **Legenda/texto "quadrado" (caixa-alta em bloco, palavra amarela) PROIBIDO.** Ou legenda estilo iPhone, ou Poppins (caixa normal). Ele já tinha reclamado antes: erro repetido. · 25/11
- **Nunca texto de gancho e legenda ao mesmo tempo na tela** (o início com manchete em cima e legenda embaixo ficou ridículo). · 25/11
- **Cores: nada de fundo azul o vídeo inteiro.** Azul (+ limão/laranja) é do MinhaMoto. Corretores usam as cores do próprio Mapa Visual (capa e páginas do material). · 25/11
- **Preço no CTA: o selo verde-escuro "R$27,90" é feio e amador.** O card de preço tem que ter cara de motion profissional. · 25/11
- **NÃO gerar/emendar áudio de voz** (nada de voz recortada de vários takes, ~~EQ~~, gravação abafada). · 25/11 (EQ agora só pra igualar o gancho abafado ao body do mesmo pronto, ver 16h39)
- **ESTRUTURA A · só motion, sem voz nenhuma:** prender a pessoa com efeito sonoro, trilha, transição de texto, efeitos. · 25/11
- **ESTRUTURA B · motion + body real:** hook em motion → body = trecho de um criativo que JÁ deu certo (ex.: do s10 ao s20), usado como está (voz, legenda e música originais, intactos), com transição forte na entrada e na saída → CTA em motion. Legenda só nos trechos de motion, se precisar. · 25/11
- **Um de cada vez, parte por parte, com o Léo aprovando cada parte** (regra geral no topo do DESIGN-MINHAMOTO.md). Não fazer 13 de uma vez. Primeiro 1 piloto por estrutura, aprovação, depois escala. Crédito gasto em peça ruim é prejuízo. · 25/11
- **EST2-A (25/11):** a ideia do balão "Você saberia responder?" e das perguntas 1/3–3/3 aprovada, a execução não. As perguntas saem da tela quando ela diz "se não, dá uma olhada no material" (nada de pergunta em cima do tablet). · 25/11
- **EST8-A (25/11):** APROVADO o gancho com a voz dela do próprio pronto (já editada) sobre outra imagem, em preto e branco. Reprovada a forma de apresentar o material na animação. · 25/11
- **NUNCA transição/corte no meio da fala** (nem no fim da palavra: o "você" final tem que sair inteiro). Corte só depois da palavra terminar e o som cair. ❌ v3 no "material", ❌ v4 no "você". Regra também na memória. · 25/11
- **Corte da fala: nunca no meio da frase dela.** O gancho vai até a pausa natural do fim da frase, mesmo que fique 1 s mais longo. ❌ EST2-A v3 cortava no "material". · 25/11
- **Motion dinâmico, não só balão:** ícones, efeitos, partículas, empurrão de câmera; cada criativo com cara própria (o EST2-A não pode parecer o EST8 com balão). Balão de abertura com acabamento (o "Você saberia responder?" da v3 estava fraco). · 25/11
- **Legenda do pronto também se revisa:** o DD 4 tem "CURSOS" onde ela fala "custos" → corrigido no vídeo (palavra refeita na mesma fonte/caixa, Anton 68). Conferir a legenda queimada de todo trecho de pronto que entrar. · 25/11
- **Não diminuir o Mapa:** "As 3 respostas estão no Mapa" dá a entender que é pouca coisa → "Essas e muitas outras respostas estão no Mapa" (+120 mapas). · 25/11
- **Elementos de motion também no body e no CTA**, elegantes e leves (tag no canto com check, contador +120, botão "Saiba mais" com toque), sem chapar e sem cobrir título de página. · 25/11
- **Mais body:** os dois estavam curtos e corriam pro CTA. Body longo (≈ 25–30 s do pronto), depois o CTA. · 25/11
- **Preço: tirar de tudo** (volta só se a gente decidir ir por preço, aí em tudo de novo). Body escolhido sem o trecho em que ela fala o preço. · 25/11
- **Áudio do jeito que veio:** sem abafar, sem mexer na voz. · 25/11
- **Parâmetro de qualidade:** "parece que nunca fez motion na vida" → o nível é motion profissional de anúncio (referência: criativos que já rodam no nicho), não template. · 25/11
- **(16h39) Nome de arquivo normal:** nada de "EST5-A v3". Entregável sai com nome descritivo em português: "Corretores - Historinha cliente seguro.mp4", "Corretores - Perguntas fora do basico.mp4" etc. Código EST só dentro dos scripts, se precisar. · 25/11
- **(16h39) Áudio do gancho dos prontos vem abafado** (DD 4 e DD 10: a 1ª parte, até a pausa antes do "São +120", tem menos agudo e mais grave que o body). Tem que ficar padrão com o resto do vídeo: EQ só nesse trecho, casada por faixa de oitava com o body do MESMO pronto (`eqmatch.py`, resto ≤ ±1 dB), costura na pausa, e volume da fala igualado ao body (ganho +1,5 a +2 dB). Isso não é "mexer na voz": é deixar igual ao resto. Continua proibido emendar takes ou gerar voz. · 25/11
- **(17h16) "Ainda assim o áudio não tá bom":** só EQ não resolve. Medido: no gancho (e no CTA dela sentada) o ambiente/chiado entre as palavras fica só 14–19 dB abaixo da fala nos agudos, contra 31 dB no body; quando o EQ sobe a presença, sobe o chiado junto. A gravação original do gancho (HOOK1/HOOK5) é igual: o problema é da captação, não do pronto. Cadeia padrão agora (`voz.py` → `tratar`, tudo clássico, sem IA): corta ronco (passa-alta 100 Hz) → tira o chiado com o perfil das pausas do próprio trecho → EQ 1/3 de oitava casada com o body só nos trechos de fala → de-esser → compressão leve → expansor que abaixa até 10 dB do ambiente entre palavras → fala no mesmo nível do body. Vale pro gancho E pro CTA (`remux_voz.py` troca só o áudio, sem re-render). · 25/11
- **(16h39) Variar os elementos entre os vídeos:** cada criativo com um conjunto próprio de elementos (não repetir faixa de ícones + contador + "?"→✓ em todos). Conjuntos prontos: 1 = `elem.py` (faixa de ícones, contador em cartão, "?"→✓) · 2 = `elem2.py` (anel de contagem, pílulas-adesivo inclinadas, palavra que troca na pílula navy, "Dúvida" riscada → "Certeza", cartões navy que viram) · 3 = `elem3.py` (+120 grande com contorno, checklist em 2 colunas, marca-texto, chave "Na dúvida → Seguro", pílulas navy deslizando dos lados). · 25/11
- **Correção do "CURSOS" no DD 10 estava 1 quadro adiantada** (pegava 1 quadro de "PRAZOS" e deixava 1 de "CURSOS" no fim) → janela certa = quadros 757–778. Toda correção de legenda: conferir no vídeo FINAL, quadro a quadro, do quadro antes ao quadro depois da palavra. · 25/11
- **(17h29) APROVADOS: Historinha cliente seguro + Perguntas fora do básico (com o áudio tratado).** Placar: 4 aprovados (Você saberia responder, Antes e depois, Historinha, Perguntas). · 25/11
- **Folheando o Mapa (25/11, v1):** DD 2 (= HOOK2, "Corretor, você sabe olhar a renda do seu cliente…") com o gancho tratado sobre o Mapa impresso folheado (pagdet), mini-mapa no estilo do material montando as 3 perguntas; body do DD 2 9,5→40,3 s (CURSOS do DD 2 nos quadros 665–687 corrigido); conjunto 4 (`elem4.py`: fluxo numerado, blocos coloridos, ALERTA→SAÍDA, rota com pinos, pilha de páginas). DD 2 = DD 4 − 2,767 s no body. · 25/11
- **Só motion (25/11, v1) = estrutura A:** sem voz; trilha ORIGINAL sintetizada (`trilha.py`, 100 BPM, cortes no compasso de 2,4 s, subida + impacto na virada) — nada de música de terceiros. Páginas reais do PDF em alta (pasta local `paginas/`, nunca no repo). Conjunto 5: pílulas de manchete, notificações "Cliente", palavra por batida, carrossel de páginas com marca-texto. · 25/11
- **(18h31) Nome dos entregáveis aprovados: "K<n> - Corretores - <nome>.mp4"** (K = feito pelo Claude; numeração corrida: K1, K2… K33…). Os 6 de 25/11: K1 Você saberia responder · K2 Antes e depois · K3 Historinha cliente seguro · K4 Perguntas fora do básico · K5 Folheando o Mapa · K6 Só motion. O próximo é o **K7**. Peça aprovada vai pro PC em `Corretores/Criativos prontos/TESTES 2/` (lote de 25/11). · 25/11
- **(18h31) Folheando o Mapa e Só motion: revisados e dados como prontos** (sem erro de elemento/animação; intro da trilha do Só motion ganhou batida desde o 1º segundo porque estava 14 dB mais baixa que o resto). Avaliação do Léo sobre o lote: "ficaram bons, pode ser que vendam", mas não ficaram "uau" nem muito diferentes um do outro → próximo lote precisa de ideia/visual mais diferenciado. · 25/11
- **(18h48) K6 Só motion: "ficou muito top" — virou a REFERÊNCIA de motion** (aqui, no MinhaMoto e em vídeo no geral). O que copiar está detalhado no DESIGN-MINHAMOTO.md (bloco "Referência de motion aprovada"). · 25/11
- **(16h39) CTA da Ana Paula sentada ("Clique em Saiba Mais", DD 10 68,33→73,70 s) + botão com toque: aprovado pra usar em vários vídeos.** · 25/11

## 0b. PADRÃO APROVADO PELO LÉO (25/11) — base pros próximos criativos, sem ele ter que guiar
**Aprovado (manter):**
- Estrutura: gancho em motion com a voz dela + body longo de pronto que já vendeu (como está) + CTA dela do pronto. · 25/11
- Gancho do EST2-A: "digitando…" → balão "Você saberia responder?" com "responder?" em verde e selo "?" coral com mola; perguntas 1/3–3/3 com ícone por pergunta, partículas e empurrão de câmera; saem quando ela diz "se não"; card "Essas e muitas outras respostas estão no Mapa" + 3 checks + "+120 mapas". · 25/11
- Gancho do EST8-A: voz dela do pronto sobre cenas em preto e branco + "Antes" + chip da frase do corretor inseguro. · 25/11
- CTA: botão "Saiba mais" que recebe um toque, com onda e partículas. · 25/11
- Áudio: voz do jeito que veio (só ganho igual entre trechos) + efeitos sonoros sutis (pop, whoosh) — aprovados. · 25/11
- Fonte Poppins caixa normal, cores do Mapa (navy, verde-água, coral), sem preço. · 25/11
**Reprovado (não repetir):**
- Dedo do toque dentro de círculo branco → só o símbolo (mão branca com contorno navy, PNG, sem fundo). · 25/11
- Elementos do body todos iguais no canto superior direito, sem relação com a apostila → elementos centralizados, na faixa logo acima da legenda do pronto, e cada um ligado ao que ela está falando/mostrando (contador +120, ícones dos temas, "ilustrado/organizado/fácil", "?"→"✓" no "nunca mais tenha dúvida", ícones das formas de aquisição). · 25/11
- Rótulos encostando um no outro (conferir largura com 6 itens). · 25/11
- Texto saindo do cartão ("Nunca mais na dúvida" vazava): cartão sempre do tamanho do texto, nunca largura fixa. · 25/11

**EST2-A v6 = APROVADO e finalizado pelo Léo (25/11).** É a referência dos próximos. (v7 = mesma peça com 1 quadro de "CURSOS" corrigido: o recorte do pronto começava no meio de um quadro e a correção de legenda pulava o 1º quadro → agora o motor usa o tempo real do quadro.)
- **EST8-A (25/11):** hook aprovado ("a gente vai fazer variações disso"); a cortina Antes→Depois passava rápido demais pra ler → a cortina entra, FICA PARADA ~1,3 s com o texto e só então sai. Toda tela de texto tem que durar o suficiente pra ler. · 25/11
- **Legenda do DD 7 também tem "CURSOS"** (em vez de custos) → corrigida. Os prontos DD têm esse erro: conferir em todo trecho. · 25/11

## 1. Pra quem e o que
- **Fala com o corretor de imóveis**, nunca com o comprador. · 23/11 (inicial)
- O produto é o **Mapa Visual Completo do Fechamento Imobiliário** (125 páginas visuais, do aceite da proposta às chaves). Ofertas da página: Acesso Essencial R$27,90 e Pacote Completo R$37,90 (Mapa + 5 complementares), acesso vitalício, garantia de 30 dias. **Preço citado no criativo: só "R$27,90", sem parcelamento (decisão do Léo, 23/11, `conhecimento/05-marca.md` e seção 5 abaixo).** ~~"Pacote Completo R$37,90" como preço do criativo~~ → substituída em 23/11 pela decisão do Léo; corrigido pelo Shelby em 24/11 (a linha contradizia a seção de preço). · 23/11
- Tese de todo criativo: **o corretor não perde venda na visita, perde depois do "sim"**; quem domina o processo passa segurança, perde menos venda e ganha indicação. · 23/11 (inicial)

## 2. Copy
- **Um ângulo por criativo** (banco em `agencia/estudio/produtos/corretores.md` §4). · 23/11 (inicial)
- **Hook nos 3 primeiros segundos** chamando o corretor ("Corretor, …", "Ei, corretor: …") ou com a fala real do cliente ("E agora, qual é o próximo passo?", "Meu FGTS paga tudo?"). · 23/11 (inicial)
- Ordem: **hook → dor concreta (as perguntas do cliente) → o material resolve (mostrar) → o que vem no pacote → CTA**. · 23/11 (inicial)
- Body mais curto que os lotes antigos: as copies longas (80 a 105 s) estão no arquivo "COPYS LEO 1 - nao deu bom". ✅ Testar menos de 15 s, 15 a 30 s e 30 a 60 s. · 23/11 (inicial)
- **Sempre "você"**, nunca "tu" nem imperativo de tu. · 23/11 (regra da casa)
- Nada inventado: ❌ "9 em cada 10 corretores" como estatística (é percepção da Ana Paula); ❌ promessa de renda ou comissão garantida; ✅ "poucos corretores dominam", "uma dúvida mal respondida pode custar uma comissão". · 23/11 (inicial)
- CTA: "Clique em Saiba Mais e conheça o Mapa Visual Completo do Fechamento Imobiliário". · 23/11 (inicial)
- Palavras-chave que puxam identificação: financiamento, FGTS, Minha Casa Minha Vida, consórcio, ITBI, escritura, registro, matrícula, cartório, avaliação do banco, entrega das chaves. · 23/11 (inicial)

## 3. Visual
- **Mostrar o material sempre** (prova): página real no iPad, no impresso em espiral ou em mockup animado. As páginas do Mapa são o melhor ativo visual: títulos fortes, ilustração, cards numerados. · 23/11 (inicial)
- **Legenda palavra por palavra**, branca em caixa-alta, palavra falada em amarelo (padrão dos criativos que rodaram). · 23/11 (inicial)
- Paleta do material: azul-marinho, verde-água/teal, laranja-terracota, fundo creme. Estáticos que rodaram: verde-escuro + off-white + botão verde "Conheça o material". · 23/11 (inicial)
- 9:16 (1080×1920) para Reels, Stories e TikTok; 1:1 ou 4:5 para estático de feed. Zona segura 9:16: texto entre x 140–940 e y 150–1500. · 23/11 (regra da casa)
- Sem logo de banco, Caixa ou programa do governo desenhado como marca. · 23/11 (regra da casa)

## 4. A expert (Ana Paula Mello)
- Corretora e advogada de Direito Imobiliário, tom de colega experiente, calma, sem cara de guru. Aparece no hook e no CTA; o meio mostra o material. · 23/11 (inicial)
- Só usar rosto e voz dela nos cortes que ela gravou para isso; nunca recriar o rosto nem a voz dela por IA. · 23/11 (regra da casa)

## 4b. Decisões do Léo (23/11)
- **Preço no criativo: "R$27,90".** Sem parcelamento. · 23/11
- **Voz: só a da Ana Paula** (takes dos brutos e dos prontos; legenda pode ser refeita). Nunca voz ou rosto por IA. · 23/11
- **Duração:** 15 a 30 s nos criativos novos (a copy longa foi a pior entre as que venderam; UTMify). · 23/11
- **CTA:** "Clique em Saiba Mais" (padrão dos que venderam). · 23/11
- **Ângulos: não é só "perdeu a venda depois do sim" (Léo, 23/11).** A dor da perda é um ângulo entre vários. Equilibrar com ângulos de GANHO, um por criativo:
  - **Qualificação e destaque:** o corretor que domina o processo se destaca dos outros e vira referência.
  - **Vender mais rápido:** sabendo os próximos passos, o cliente trava menos.
  - **Responder qualquer pergunta do cliente** na hora, sem "vou ver com o pessoal".
  - **Confiança:** a dele e a do cliente.
  - **Economia e lucro:** a finalização depois do sim costuma ser um serviço cobrado nesse mercado; quem entende o processo depende menos de terceiros e fica com uma parte maior do ganho. (Cuidado na copy: não prometer que ele faz o trabalho técnico de correspondente/cartório; a promessa é entender e conduzir, pagando menos por fora.)
  · 23/11

## 4c. Questionário do Léo (24/11)
- **Próximos estilos (fazer HOJE também, 24/11):** (1) folheando o Mapa com a Ana Paula narrando; (2) antes × depois do corretor; (3) mistura de motion com vídeo real; (4) só motion (sem rosto, com a voz dela). · 24/11
- **Rodada de teste:** 6 criativos por produto. · 24/11
- **Entrega:** ~~salvar direto em ESTUDIO 23-11 no PC~~ → substituída em 24/11: só vai pro PC o que o Léo aprovou e mandou salvar; antes disso, mostrar no chat. Peça aprovada não vai pra pasta de documentos dele: vai pra outro lugar (perguntar onde na 1ª aprovação). Cortes de trabalho: liberados SÓ em `ESTUDIO 23-11\_trabalho\`. Os 3 pilotos já salvos ficam lá. · 24/11


## 4d. Revisão independente (24/11): regras novas pra não repetir
- **Áudio: nunca emendar trechos com silêncio zerado.** Entre takes, usar o som ambiente do próprio take + crossfade de 30 a 60 ms. ❌ buracos de 100–160 ms nas 10 peças de 24/11 (`pc.silencio()` do motor_novo). · 24/11
- **Gravação limpa do Dia 2 tem timbre mais escuro:** equalizar pra casar com os takes de câmera antes de emendar. · 24/11
- **Split-screen: a legenda nunca passa na divisória (y 900–1010).** Parece texto riscado. ❌ EST4-A/B/C. · 24/11
- **CTA: usar o 4de4 ("clique em Saiba Mais e tenha acesso vitalício…").** O 2de2 tem "e tem acesso" (concordância). E "Saiba Mais" nunca quebra entre dois grupos de legenda. · 24/11
- **Um ângulo só, também entre texto e voz:** o texto na tela (história, quiz) tem que contar a mesma coisa que ela está falando. ❌ EST5-A/B, EST2-C. · 24/11
- **Chips sem imperativo que soe "tu":** "Você responde na hora", "Você conduz…". · 24/11
- **Correspondente:** não opor "vou ver com o correspondente" × "conduz a própria venda" (sugere dispensar o correspondente). A promessa é entender o processo, não substituir ninguém. · 24/11
- **Primeiro frame forte:** rosto inteiro, de frente, com texto de gancho já na tela. ❌ EST9-A torta, EST2-B careta, EST8-A sem texto. · 24/11
- **Gancho nos 3 primeiros segundos chama o corretor ou traz a dor/ganho.** Contador sozinho não é gancho. ❌ EST10-A. · 24/11
- **Cena tem que mostrar o que o texto diz** (ex.: "o corretor travou" com corretor confiante ❌). Não repetir a mesma cena de banco (corretor olhando pro teto, casal no sofá) em muitas peças da mesma rodada. · 24/11
- **Páginas do Mapa inteiras na largura, sem cortar nas laterais; nada de páginas fantasmas sobrepostas.** · 24/11
- **Áudio final 48 kHz em todas.** · 24/11
- **Página impressa: zoom no máximo 1,0, as duas margens visíveis do primeiro ao último frame.** ❌ "Consórcio não é financiamento" e "Na planta" cortadas em 6 peças (rodada 2). · 24/11
- **EQ da Gravação Dia 2 se confere por faixa (graves/médios a no máximo 3 dB do take do CTA), não só pelo brilho geral.** · 24/11
- **Nada de frame congelado com a voz andando.** · 24/11
- **Bolha/chip a pelo menos 120 px do queixo.** · 24/11
- **Não usar o mesmo clipe com o mesmo texto em duas peças do mesmo lote.** · 24/11
- **Cena de assinatura de contrato = venda fechada:** nunca embaixo de texto de dúvida/insegurança. · 24/11
- **Still de página impressa tem que ser nítido (cards legíveis); se não houver frame nítido, usar a página do PDF no tablet.** · 24/11
- **Cena embaixo de chip/texto de dor mostra a dor (hesitação, dúvida); nunca cliente sorrindo.** · 24/11
- **Chips e listas também ficam dentro de x 140–940.** · 24/11
- **Texto de bolha com pelo menos 40 px.** · 24/11

## 5. Formatos que já existem (pra variar e não repetir)
- Ana Paula hook + body (impresso/iPad) + CTA (lotes AP DD/LC e Dia 2).
- Só material físico folheado + voz em off (lote TESTES 1).
- Estático 1:1 com pergunta-headline + página real + botão.
→ Formatos novos a testar: motion só com as páginas do Mapa, historinha da dor com banco de cenas, quiz "você sabe responder?", fala do cliente → resposta do material, split-screen corretor inseguro × corretor que domina, tela de WhatsApp com as mensagens prontas.

## 6. Placar de erros
| Data | Peça | Erro que o Léo pegou | Regra criada |
|---|---|---|---|
| — | — | (vazio: começa na primeira rodada de lapidação) | — |
