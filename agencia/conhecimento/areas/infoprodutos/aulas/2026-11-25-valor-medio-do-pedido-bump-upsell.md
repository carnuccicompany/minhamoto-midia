# Aula 25/11/2026 · Valor médio do pedido em low ticket: order bump, upsell 1 clique, downsell e funil autoliquidável

Para: Grant Cardone (Infoprodutos), com cópia útil pro Escobar (Tráfego) e Turing (Dados).
Por que importa agora: nos Corretores o custo por venda subiu 19% de outubro pra novembro (09-numeros.md). Criativo novo baixa o custo; **valor médio do pedido (AOV) maior aumenta o quanto podemos pagar por venda**. Em ticket baixo, é aqui que mora o lucro.
Legenda: **[OF]** documentação oficial de plataforma/órgão · **[ESP]** especialista · **[VEND]** blog de quem vende checkout (conflito de interesse). Quase todo benchmark de aceite vem de vendedor de checkout: usar como direção, nunca como meta fechada.

## 1. O que é
- **Order bump:** caixinha de oferta extra dentro do checkout, aceita **antes** de pagar, com um clique. Barato, de impulso, ligado à mesma dor [VEND] (Hotmart, 15/06/2026: https://hotmart.com/pt-br/blog/order-bump-da-hotmart).
- **Upsell pós-compra (OTO):** oferta mostrada **depois** da compra aprovada, numa página própria; **downsell** = alternativa mais barata pra quem recusou [OF] (ClickFunnels, atualizado 09/11/2026: https://support.myclickfunnels.com/docs/adding-a-one-click-upsell-downsell-oto-page.md).
- **Upsell 1 clique e Pix (o ponto crítico pra nós):**
  - Kiwify [OF] (30/10/2026): upsell vale pra cartão e Pix, mas **o 1 clique é só no cartão**; quem pagou no Pix recebe **novo QR Code** ao aceitar (https://ajuda.kiwify.com.br/pt-br/article/como-configurar-upsell-de-1-clique-12ei26e/).
  - Hubla [OF] (20/02/2023) diz que o 1 clique funciona com cartão e Pix, sem detalhar se o Pix pede nova confirmação (https://updates.hub.la/log/upsell-de-1-clique). Greenn [OF] tem 1 clique desde fev/2026, sem dizer se vale pra Pix.
  - Banco Central lançou em 28/02/2025 a **Jornada sem Redirecionamento** do Pix (base do Pix por aproximação), que permite pagar sem sair da loja com biometria; gateways já vendem "Pix 1 clique" em cima disso (https://www.pagbrasil.com/payment-methods/1-click-pix/). Nenhuma plataforma de infoproduto foi confirmada usando isso no upsell.
  - **Kavoo:** sem documentação pública de upsell ou de Pix 1 clique. Precisa ser perguntado ao suporte.
- **Funil autoliquidável (SLO) / tripwire:** a venda da frente paga o anúncio; bump e upsell geram o lucro [ESP] (Social Media Examiner, 21/10/2020: https://socialmediaexaminer.com/how-to-use-self-liquidating-offers-in-facebook-ads/; Russell Brunson, podcast 22/11/2021). Front de US$1–49 no feed é o padrão do modelo.

## 2. A conta que manda
- **AOV = preço da frente + Σ (aceite de cada bump × preço do bump) + (aceite do upsell × preço do upsell).**
- **Autoliquida quando custo por venda ≤ AOV líquido** (depois de taxa do checkout, imposto e do repasse de tributos da Meta, ~+12,15% sobre o gasto no Brasil desde 01/01/2026; ver `trafego/FONTES.md`).
- ROAS de frente ≈ 1 quer dizer que o custo por venda é igual ao preço da frente; tudo o que bump e upsell somam acima disso é margem. Não existe benchmark público de "ROAS-meta" pra low ticket no Brasil: a meta sai da nossa margem real (privado).

## 3. Números de referência (direção, não meta)
| Item | Faixa | Fonte |
|---|---|---|
| Aceite de order bump | 30–40%, AOV +30% | SamCart 30/03/2026 [VEND] (https://www.samcart.com/blog/the-complete-guide-to-order-bumps) |
| Aceite de order bump | 37,8% (upsell pós-compra 14,6%) | Focus Digital, 1.847 negócios, jan–jul/2026, publ. 21/08/2026 [ESP] (https://focus-digital.co/average-upsell-conversion-rate-2026-report/) |
| Aceite de bump "saudável" | 20–40%; <15% = oferta fraca; >50% = deveria estar na oferta principal | Systeme.io [VEND] |
| Upsell 1 clique / com checkout novo / downsell | 10–25% / 2–5% / 5–15% de quem recusou | guia mantido pela Greenn [VEND, sem fonte externa] |
| Upsell pós-compra "saudável" | 3–8% | Hotmart [VEND] |
| Preço do bump vs. frente | 10–25% (acima de 30% derruba, Hotmart) · 20–40% (SamCart) · 20–50% (Systeme) | sem consenso |
| Nº de bumps | começar com 1; 3+ pode travar a escolha (Hotmart) · até 5 permitidos, "ticket +15–45%" (Cakto, 20/10/2026) [VEND] | sem estudo independente |
| Campos do checkout | média 11,3; 8 bastam; 17% abandonam por checkout longo/complicado | Baymard 26/06/2024 [ESP] (https://baymard.com/blog/checkout-flow-average-form-fields) |
| Etapa de oferta obrigatória | 66% ficaram muito frustrados com um passo de cross-sell obrigatório | Baymard [ESP] (https://baymard.com/checkout-usability/benchmark/step-type/cross-sell) |

## 4. Como o top 1% estrutura
1. **Bump = acelerador da mesma dor**, escrito como "isso te dá o resultado mais rápido"; descrição de 2–3 frases; preço "de/por" só se o "de" for verdade [VEND] (SamCart).
2. **Upsell numa página própria**, com benefício e prova; complementar ou acelerador, nunca "mais do mesmo"; urgência só se for real [ESP/VEND] (FunnelKit 09/09/2026; Shopify 12/11/2020).
3. **Sequência:** frente → bump(s) → upsell → downsell se recusar [OF] (ClickFunnels, Kiwify).
4. **Preço do bump se ajusta pelo aceite:** aceite muito alto (Hotmart fala em 70%) = bump barato demais ou que devia estar na oferta.
5. **Cada etapa é medida separado:** aceite por bump, aceite do upsell, reembolso por etapa. Upsell que gera reembolso não é receita.

## 5. Erros comuns
1. Bumps demais (paralisia) ou caros demais.
2. Bump **pré-marcado**: risco de CDC (venda não pedida) e de reembolso; nunca.
3. Oferta pós-compra que trava o acesso ao que foi comprado (frustração, reembolso).
4. Esquecer o CDC art. 49: arrependimento em 7 dias em compra pela internet, com devolução imediata (TJDFT, explicação oficial: https://www.tjdft.jus.br/institucional/imprensa/campanhas-e-produtos/direito-facil/edicao-semanal/direito-ao-arrependimento-de-compra). Upsell empurrado volta como reembolso.
5. Upsell no Pix com novo QR sem saber disso: a fricção derruba o aceite; medir antes de prometer receita.
6. **Canibalização:** a versão completa e os bumps disputam o mesmo bolso; testar um de cada vez.

## 6. Como aplicamos aqui (regras práticas)
1. **Número da semana do Cardone:** AOV dos Corretores (índice, outubro = 100), % de pedidos com o Pacote Completo, aceite de **cada** bump, reembolso por item. Fonte UTMify/Kavoo; absolutos só no `carnucci-dados`.
2. **Onde estamos (09-numeros.md, 23/11):** Completo em ~85% dos pedidos e ~0,5 bump por pedido. A ancoragem funciona e o bump já está dentro da faixa boa de mercado; o ganho fácil não é "mais aceite", é **uma oferta pós-compra que ainda não existe**.
3. **Antes de propor upsell, confirmar com a Kavoo** (pergunta pro Léo, que tem o acesso): existe upsell pós-compra? É 1 clique no cartão? E no Pix, gera novo QR? Com ~85% dos pagamentos em Pix, um upsell com novo QR deve aceitar bem menos (faixa 2–5% de "checkout novo").
4. **Testes candidatos (só com OK do Léo, um por vez):** (a) 4 bumps contra os 2 mais vendidos; (b) preço do bump mais vendido; (c) upsell pós-compra de um complementar com página própria; (d) bônus pequeno pra quem paga no cartão, se a Kavoo fizer upsell 1 clique só no cartão.
5. **Proibido:** bump pré-marcado, "de/por" falso, urgência falsa, promessa de renda. Garantia sempre "Garantia de 30 dias" sem a palavra "reembolso" até o Léo confirmar os termos da Kavoo (Shelby, 24/11).
6. **Checkout enxuto:** nome, e-mail, CPF se a Kavoo exigir e telefone (necessário pra recuperação de Pix, que está adiada pelo Léo). Campo a mais = venda a menos.
7. **Toda proposta de verba nos Corretores usa o AOV líquido**, não o preço da frente, pra calcular o custo por venda que dá pra pagar (com o Escobar; conta no privado).
