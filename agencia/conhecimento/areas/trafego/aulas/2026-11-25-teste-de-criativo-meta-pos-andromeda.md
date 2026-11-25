# Aula 25/11/2026 · Teste de criativo na Meta depois do Andromeda

Para: Pablo Escobar (Tráfego), com cópia útil pra Disney (Criativos) e Cardone (Infoprodutos).
Por que importa agora: o teste dos 3 estilos dos Corretores (EXP-20261123-1, Historinha × Quiz × Split-screen, 3 criativos cada) e a primeira verba do MinhaMoto dependem de saber testar sem queimar dinheiro e sem ler ruído como vencedor.
Legenda das fontes: **[OF]** oficial lido direto · **[OF*]** oficial citado por terceiro com o link oficial (conferir no navegador antes de virar regra dura) · **[ESP]** especialista ou fornecedor.

## 1. O que é (e o que mudou)
- O sistema de recuperação Andromeda (dez/2024) escolhe quais anúncios entram no leilão pra cada pessoa; o criativo virou a segmentação. A Meta divulgou +6% de recall e +8% de qualidade de anúncio em segmentos testados [OF] (Engineering at Meta, 02/12/2024: https://engineering.fb.com/2024/12/02/production-engineering/meta-andromeda-advantage-automation-next-gen-personalized-ads-retrieval-engine/).
- **Criativos parecidos contam como um só.** A Meta "agrupa anúncios que compartilham atributos visuais e temáticos" [OF*] ("Demystifying Creative Diversification", 16/12/2025: https://www.facebook.com/business/news/demystifying-creative-diversification). Testar 3 cores do mesmo vídeo não é teste: é um anúncio dividido em três.
- Testar hoje é responder "qual **ideia** (ângulo, formato, pessoa, cenário) vende", não "qual detalhe".

## 2. As duas ferramentas oficiais de teste
| | **Teste de criativo** (no nível do anúncio, "Set Up Test") | **Teste A/B** (Experiments) |
|---|---|---|
| Quantos | 2 a 5 anúncios (algumas contas já até 10 [ESP]); na API, 2 a 7 células, 1 anúncio por célula [OF] | até 5 versões na interface |
| Verba | fatia do orçamento do conjunto (a Meta sugere até ~20%) [ESP] | verba própria por versão |
| Duração | padrão 7 dias [ESP] | mínimo 7, máximo 30 dias [ESP citando Help Center] |
| Exige | estratégia de lance "maior volume" (não roda com custo-alvo, bid cap ou ROAS-alvo) [ESP] | — |
| Resultado | aponta "melhores" (`high_performer_ids`); os campos de vencedor e confiança voltam sempre nulos na API [OF] | dá % de confiança |
| Serve pra | comparar ideias diferentes dentro do conjunto que já roda | hipótese estratégica (conceito, público, posicionamento) com confiança |
- Fontes: Marketing API, Split Testing [OF] https://developers.facebook.com/docs/marketing-api/guides/split-testing (lido 25/11/2026) · Jon Loomer [ESP] https://www.jonloomer.com/meta-creative-testing/ · Mockingbird, 14/10/2026 [ESP] https://mockingbirdhouse.com (cita facebook.com/business/help/1738164643098669 e /1423851372208214).
- Detalhes que pegam gente boa: o teste de criativo **duplica** os anúncios (o original fica fora), cada pessoa vê só um, e **quando acaba a entrega volta ao normal**: o vencedor não ganha verba sozinho [ESP, Loomer].

## 3. Onde testar: campanha separada ou dentro da escala
- **Regra de volume oficial:** cerca de 50 conversões por semana por conjunto. Conjuntos abaixo disso tiveram CPA de compra ~28% maior. Fórmula da Meta: **orçamento semanal ÷ (CPA × 50) = nº máximo de conjuntos** [OF*] ("Peak Season 2026: You Don't Beat The Auction. You Brief It", Meta, 21/10/2026; resumo em ppc.land, 25/10/2026).
- **Campanha de teste separada em ABO** (1 conceito por conjunto, verba igual) → vencedor vai pra CBO/Advantage+ de escala [ESP] (TheOptimizer, 23/05/2026; Top Growth Marketing, 22/06/2026). Pró: verba mínima garantida e leitura limpa. Contra: fragmenta o sinal e o vencedor do ABO pode falhar na escala.
- **Teste dentro do conjunto ativo** (o que a Meta empurra) [ESP] (Loomer, pubcast 19/02/2026: https://pubcast.jonloomer.com/what-to-do-with-creative-testing-results/; RevenueCat, 19/06/2025: https://www.revenuecat.com/blog/growth/7-meta-ad-testing-frameworks-for-subscription-apps/). Pró: não perde aprendizado. Contra: anúncio novo pode ficar sem gasto.
- Abaixo de ~US$5 mil/mês, a RevenueCat recomenda **1 conjunto Advantage+ com ~5 criativos**, entrando 2–3 novos por semana; até US$500/mês, 1 campanha, 1 conjunto, 8–10 criativos (3–4 vencedores + 2–3 novos) [ESP] (RevenueCat, 08/10/2025).
- Volume oficial de anúncios: "anúncios demais podem piorar o desempenho"; limite de 50 anúncios por conjunto, pausados contam [OF*] (https://www.facebook.com/business/help/2720085414702598 e /652738434773716).

## 4. Como o top 1% decide (volume, verba, tempo)
- **Verba por criativo antes de julgar:** 2–3× o CPA alvo [ESP] (Top Growth Marketing, 22/06/2026). Menos de 4 dias costuma ser ruído; parar em ~50 compras por conjunto ou 7 dias, o que vier antes.
- **Ordem de leitura:** taxa de gancho (3 s ÷ impressões) → retenção (ThruPlay ÷ 3 s) → CTR → CPA/ROAS. Gancho e retenção dizem *por que*; CPA diz *se* (ver aula de Criativos de 25/11).
- **Não esperar significância em tudo:** "Don't wait for statistical significance, it's going to limit how fast you can move" (Cedric Yarish, via RevenueCat, 19/06/2025) [ESP]. Régua prática de CPA dele: teste a 80% da média é bom; até 160% talvez; 200%+ sai.
- **Concentração de gasto é normal:** a Meta dá ~80–95% da verba aos 3 melhores anúncios [ESP] (RevenueCat). Criativo com menos de metade do gasto que deveria ter depois de 2 dias, em Advantage+, provavelmente perdeu; troque os que não gastam a cada 2–3 dias [ESP] (RevenueCat, 08/10/2025).
- **Anúncio sem gasto não é criativo ruim provado:** a Meta previu pior desempenho **ou** juntou com outro parecido. Pra ter leitura, force verba igual com o teste de criativo [ESP] (Loomer, pubcast 20/05/2026). Limiares de "similaridade de 60%/40%" que circulam NÃO são da Meta (hipótese de agência).

## 5. Leitura nova no Gerenciador (out–nov/2026)
- **Detalhamento por criativo:** aba Anúncios → Detalhamento → Criativo → Mídia mostra gasto, CTR, compras, CPA e ROAS por imagem/vídeo (inclui mídia removida); textos em "Dynamic creative element". Não cobre carrossel/coleção. Liberação gradual desde ~27–28/10/2026 [OF*] (Social Samosa 28/10/2026, link oficial https://www.facebook.com/business/help/1822387965412520).
- **Coluna "Creative Diversity"** (Low/Medium/High por conjunto), em desenvolvimento, critérios não divulgados [OF*] (26/08/2026, via Common Thread 09/09/2026). Usar como alerta, nunca como prova.
- **Creative audience pairing:** escolher idade/gênero por criativo dentro do conjunto (19/10/2026) [OF*] (via adsuploader).

## 6. Números de referência
- **~5% dos anúncios viram vencedores** (gasto ≥10× a mediana da conta); ~4% nas contas pequenas, 8–9% nas grandes; cerca de metade dos anúncios recebe gasto zero ou quase zero [ESP] (Motion Creative Benchmarks 2026, 550 mil+ anúncios, via Foxwell Digital, 16/06/2026).
- **Criativos novos por semana** (média / top 25%), por gasto mensal: <US$10 mil: 2,8 / 4,8 · US$10–50 mil: 4,1 / 8,1 · US$50–200 mil: 6,7 / 16 [ESP] (Motion 2026).
- **Fadiga:** 2–4 semanas hoje (antes 6–8) [ESP] (Common Thread, 06/05/2026; correlação, não causa).
- **Custo por vencedor** = (verba de teste + produção) ÷ nº de vencedores; ≥60% da verba de teste em conceito novo [ESP] (RevenueCat, 12/09/2025). Caso real: 3 de 70 estáticos (~4%) se destacaram.

## 7. Erros comuns
1. Testar variações quase iguais (a Meta agrupa) [OF*].
2. Abrir muitos conjuntos abaixo de ~50 eventos/semana [OF*].
3. Decidir com menos de 4 dias ou gasto mínimo, ou o oposto: esperar significância em tudo.
4. Desligar tudo e escalar só o "vencedor" do teste de criativo (o tema venceu, não o arquivo) [ESP].
5. Ler anúncio sem gasto como perdedor provado; microgerenciar a entrega.
6. App: otimizar por instalação sem olhar instalação → assinatura; contar visualização como conversão.
7. Só produzir reposição quando a fadiga já chegou; iterar só em cima de vencedor até a taxa de acerto cair.
8. Confiar em métrica "em desenvolvimento" (Creative Diversity) e limiar de terceiro como se fosse regra.

## 8. Como aplicamos aqui (regras práticas)
1. **Teste = ideia diferente.** Nos Corretores, cada estilo é uma ideia; dentro do estilo, os 3 criativos têm que diferir em gancho, cena ou formato, nunca só em cor/legenda. A V2 "com faixa de garantia" é teste de oferta, não de criativo: ler à parte (D-20261123-mkt-2).
2. **Conta dos conjuntos antes de montar:** verba semanal ÷ (custo por venda alvo × 50). Se der menos de 3, não abrir 1 conjunto por estilo: usar o **teste de criativo** dentro do conjunto que já vende (1 anúncio-cabeça por estilo, 7 dias, maior volume) e ler o estilo vencedor. Conta feita com o número do privado; aqui só o resultado em nº de conjuntos.
3. **Gasto mínimo antes de cortar:** 200% do custo por venda alvo sem venda = pausa (regra proposta pelo Escobar em D-20261123-mkt-3, aceita); entre 2× e 3× só corta se gancho e CTR estiverem abaixo do piso. Nunca decidir antes de 4 dias, salvo corte por gasto.
4. **Leitura oficial pelo detalhamento Criativo → Mídia** + UTMify por `utm_content` (padrão CR-<ângulo>-<nn>). Se os dois discordarem, vale a venda da UTMify.
5. **Anúncio que não gasta em 2–3 dias:** checar se é parecido demais com outro; se for, sai e entra uma ideia nova. Se for diferente e ainda assim não gasta, o teste de criativo dá a leitura justa.
6. **Ritmo de reposição:** meta de ≥5 criativos novos por semana nos Corretores enquanto houver teste (top 25% da faixa de gasto), com ≥60% em ideia nova. Medir custo por vencedor por mês.
7. **Vencedor:** sobe pra campanha de escala por duplicação ou ganha +20 a 30% de verba por degrau; os outros anúncios do conjunto não se desligam todos de uma vez.
8. **MinhaMoto (quando a verba abrir):** 1 campanha, 1 conjunto Advantage+ de app, 5 a 8 criativos de ideias diferentes, otimizando pelo evento de compra assim que o SDK mandar; decisão por custo por assinante, nunca por instalação.
9. **Nada disso sobe sozinho:** toda estrutura nova é proposta com OK do Léo; nos Corretores ninguém edita campanha sem ele.
