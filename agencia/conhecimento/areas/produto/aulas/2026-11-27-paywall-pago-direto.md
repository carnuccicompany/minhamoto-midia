# Aula 27/11/2026 · Paywall pago direto: o que o top 1% mostra antes de cobrar e como desenha a tela que cobra

Para: Tony Stark (Produto) e Steve Jobs (designer do paywall), com cópia útil pro Turing (Dados) e pro Bezos (Lojas).
Por que importa agora: o MinhaMoto não tem teste grátis; o caminho é onboarding → cadastro da moto → "Esse é o MinhaMoto" → paywall pago direto (Léo, 20/11). O tráfego pago começa pra landing → loja (Léo, 26/11) e o SDK do AppsFlyer já está no código de 25/11. Cada instalação paga cai nessa tela: o que vem antes dela e o que ela mostra decidem o custo por assinante.
Legenda das fontes: **[OF]** oficial lido direto · **[OF*]** oficial citado por terceiro com o link oficial (conferir antes de virar regra dura) · **[ESP]** especialista ou fornecedor (RevenueCat, Adapty, Superwall vendem ferramenta de paywall: dado bom, interesse próprio).

## 1. O que é
- **Paywall pago direto (hard paywall):** o app só entrega o uso de verdade depois da compra. Não tem versão grátis permanente (freemium) nem teste grátis. Quem não paga sai ou fica num app travado.
- **Soft paywall / freemium:** o app funciona de graça e a assinatura destrava mais. **Teste grátis** é uma terceira coisa (dias de uso antes da cobrança). Não existe no MinhaMoto e não entra em nada que a gente escreva.
- **Paywall de onboarding:** a tela que cobra aparece no fim do primeiro uso, antes de o usuário cair no app. É o nosso caso.
- Pro hard paywall a RevenueCat recomenda manter quando o app resolve um problema agudo, precisa de caixa pra tráfego pago e ainda não tem análise pra testar o que fica grátis. Freemium só como estratégia de produto, nunca como "trocar a tela" (um cliente do Phil Carter perdeu mais de 50% de assinantes ao migrar e voltou em duas semanas) [ESP] (RevenueCat, "Hard paywall vs freemium", 29/04/2026: https://www.revenuecat.com/blog/growth/hard-paywall-vs-freemium.md).

## 2. Números de referência (mediana de mercado, não é o nosso número)
| Métrica | Valor | Fonte e data |
|---|---|---|
| Download → pago em 35 dias, hard paywall | **10,7%** de mediana (12,1% no relatório de 2025) | [ESP] RevenueCat State of Subscription Apps 2026, 19/03/2026, 115 mil+ apps: https://www.revenuecat.com/blog/growth/subscription-app-trends-benchmarks-2026.md |
| Download → pago, freemium | **2,1%** (≈5× menos) | idem |
| Piso do hard paywall | 4,2% (o dobro da mediana do freemium) | [ESP] RevenueCat, 29/04/2026 (link da seção 1) |
| Receita por instalação no dia 60 | hard US$3,09 × freemium US$0,38 (≈8×) | [ESP] RevenueCat SOSA 2026 |
| Retenção no 1º ano do assinante anual | hard 27% × freemium 28% (empate) | [ESP] RevenueCat SOSA 2026 |
| LTV x conversão (Adapty) | hard paywall ≈21% mais LTV; soft converte ≈50% mais (outra métrica: visualização → compra) | [ESP] Adapty, 13/03/2026, 16 mil+ apps: https://adapty.io/blog/high-performing-paywall-2026/ |
| Compra no dia da instalação | 44,5% de todas as compras saem no dia 0 | [ESP] Adapty, 13/03/2026 |
| Paywall de onboarding sem teste | 0,82% de conversão × 0,76% no paywall dentro do app | [ESP] Adapty, 13/03/2026 |
| Receita por tipo de plano (mercado todo, 2025) | semanal 55,5% · anual 22,5% · mensal 11,7% (mensal caiu de 21,1% em 2023) | [ESP] Adapty State of In-App Subscriptions 2026: https://adapty.io/blog/mobile-app-monetization-2026/ |
| Retenção do anual no dia 380 | ≈20% (América do Norte 20,0%, Europa 21,3%) | [ESP] Adapty 2026 |
| Concentração | top 10% dos apps ficam com 94,5% da receita | [ESP] Adapty 2026 |
| Paywall em várias telas | 5,2% × 2,7% (uma tela), correlação entre apps diferentes | [ESP] RevenueCat, 24/11/2026: https://www.revenuecat.com/blog/growth/multi-step-paywall |
| Plano anual em destaque | +10 a 30% de LTV "é comum" | [ESP] Superwall (Ben Butz, sem data): https://api.superwall.me/blog/superwall-best-practices-winning-paywall-strategies-and-experiments-to |
| Erro de cobrança nos cancelamentos | Play 31% · App Store 14% | [ESP] RevenueCat SOSA 2026 |
| Download → pago por loja | Android 0,9% × iOS 2,6% (apps com teste; a diferença está na entrada) | [ESP] RevenueCat, android-paywall-gap, citado pela casa em 23/11, **não relido em 27/11**: https://www.revenuecat.com/blog/engineering/android-paywall-gap |

Como ler: os 10,7% são a mediana dos apps que cobram direto, com produto e preço diferentes. Não é meta nem promessa nossa. Serve de régua de sanidade **depois** da 1ª leitura do nosso funil (D-20261126-produto-3). A régua tinha sido retirada em 23/11 porque a página não abria (D-20261122-produto-2); em 27/11 ela foi lida no artigo da RevenueCat acima.

## 3. O que o top 1% mostra ANTES de cobrar
1. **Um valor que é da pessoa, não do app.** O mais forte é a projeção personalizada: Noom mostra o resultado com data a partir das respostas. Prévia do recurso principal (Wispr Flow mostra o resultado antes do setup) e aprender algo novo também contam [ESP] (RevenueCat, "6 ways to deliver value before the paywall", 17/11/2026: https://www.revenuecat.com/blog/growth/app-value-paywall). No MinhaMoto isso é o plano da própria moto com km e datas.
2. **Contexto curto antes da tela.** Rosie Hoggmascall testou 3 telas de contexto antes do paywall: a adesão foi de ~2% (paywall cedo) pra ~8% (paywall antes do onboarding) e ~15% (com o carrossel de 3 telas). Os números são de adesão a teste [ESP] (RevenueCat, 12/06/2025: https://www.revenuecat.com/blog/growth/how-top-apps-approach-paywalls.md).
3. **Anúncio, onboarding e paywall contam a mesma história.** Tráfego pago (Meta/TikTok) precisa de sinal de compra rápido; o fio entre criativo → primeira tela → paywall não pode quebrar [ESP] (RevenueCat, 17/11/2026).
4. **Pergunta que gera investimento.** Escolher a moto, ver a revisão da vez: tela que dá trabalho útil aumenta compra. Tela só de texto perde gente (FUNDAMENTOS §2; Everlove, 19/11/2026).
5. **Apple também pede:** "mostrar o valor da assinatura logo no primeiro uso... com uma chamada forte e um resumo claro dos termos" [OF] (HIG Apple In-App Purchase, revisado 17/09/2026: https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase.md). A mesma página sugere acesso grátis limitado; é sugestão de desenho, não regra de revisão.

## 4. Como o top 1% desenha a tela que cobra
- **Título de benefício**, não de recurso ("benefícios antes de recursos") [ESP] (Superwall).
- **1 a 3 opções, com um vencedor claro** [ESP] (Superwall). Rosie: começar pelo anual, uma escolha só, selo "Mais popular" (ganhou de destacar o mais barato nos testes dela) [ESP] (RevenueCat, 12/06/2025).
- **Valor cobrado em primeiro lugar.** O equivalente mensal ou a economia ficam menores e abaixo [OF] (Apple, Auto-renewable subscriptions: https://developer.apple.com/app-store/subscriptions/).
- **Transparência vende.** O "Honest Paywall" da Blinkist (linha do tempo clara, o que inclui) subiu conversão em 23% e cortou reclamações em 55% [ESP] (via RevenueCat, 12/06/2025). Mais clareza pode baixar a conversão bruta e subir a líquida: num caso os reembolsos caíram de ~6% pra ~1% [ESP] (RevenueCat, 24/11/2026).
- **Botão único e direto**, restaurar compras, termos e privacidade visíveis no rodapé, e a folha de confirmação do sistema sem mexer [OF] (HIG).
- **Teste com métrica certa:** receita por usuário depois de reembolso (LTV realizado por cliente), não "% de quem clicou" [ESP] (RevenueCat, 24/11/2026). Teste de preço sobe conversão em 28,3% das vezes e LTV em 45,5% [ESP] (Adapty, 13/03/2026).
- **Depois da compra:** reforçar o valor logo em seguida (Duolingo, Strava) [ESP] (RevenueCat, 12/06/2025).

## 5. O que as lojas EXIGEM na tela que cobra (risco de rejeição)
**Apple [OF]**
- 3.1.2(c): antes de pedir a assinatura, "descrever claramente o que o usuário recebe pelo preço" (https://developer.apple.com/app-store/review/guidelines/uk/, lido 27/11).
- Tela de assinatura precisa ter: **nome e duração** da assinatura e o que ela dá; **preço completo de renovação**, claro, em destaque e na moeda local; **jeito de entrar ou restaurar compras**; **links de Termos de Uso e Política de Privacidade** no app e na página da loja (https://developer.apple.com/app-store/subscriptions/).
- O valor cobrado é o elemento de preço mais destacado; equivalente mensal e economia ficam em posição e tamanho menores (idem).
- Folha de confirmação do sistema: não modificar nem imitar. Cancelar tem que ser fácil de achar (HIG, 17/09/2026).
- 3.1.2(a): período mínimo de 7 dias; a assinatura funciona em todos os aparelhos do usuário; não exigir tarefa extra pra liberar o que foi pago (postar, convidar). App que engana pra vender assinatura ("bait-and-switch") é removido e a conta pode cair.
- 2.5.19 (16/10/2026): nada escondido ou diferente do que foi revisado (o botão `VITE_MM_AVISO_TESTE` não vai pra versão de loja).
- 2.3.14 (16/10/2026): criativos da página da loja sem preço.

**Google Play [OF]** (Política de assinaturas: https://support.google.com/googleplay/android-developer/answer/9900533, lido 27/11)
- Mostrar custo, frequência da cobrança e que a renovação é automática; como gerenciar ou cancelar, com link pra Central de assinaturas do Play no app.
- Violação: anual mostrado principalmente como valor mensal; preço e termos mal traduzidos; o usuário ter que fazer algo a mais pra ver as condições.
- Violação: várias telas no fluxo que levam a tocar em "assinar" sem querer (multi-step precisa ser claro em cada tela).
- Violação: botão de fechar ausente ou pouco visível quando o usuário pode usar algo sem assinar. No paywall pago direto o "sair" tem que existir e ser visível mesmo assim.
- Nome de produto (SKU) que engana, como chamar de "Free Trial" uma cobrança recorrente.

## 6. Erros comuns
1. Copiar paywall de app com teste grátis ("Comece seus 7 dias", linha do tempo do teste) num app que cobra direto.
2. Destacar o equivalente mensal do anual acima do valor cobrado (Apple e Google rejeitam).
3. Tirar o período da tela que cobra pra "não dizer por mês": a loja exige duração e frequência. A regra do Léo vale pra anúncio, post e vídeo, não pra condição de compra.
4. Paywall antes de qualquer valor, ainda mais com tráfego pago: a pessoa compra no impulso e cancela ou pede reembolso.
5. Medir conversão bruta da tela e ignorar reembolso e renovação.
6. Mudar preço, ordem dos planos e texto ao mesmo tempo: ninguém sabe o que funcionou.
7. Comparar antes e depois por data com uma versão nova do app no meio (só 50/50 ao mesmo tempo prova).
8. Esquecer restaurar compras, termos ou privacidade numa tela nova.
9. Ligar oferta introdutória na loja "pra testar": no nosso código o paywall passa a mostrar "dias grátis" sozinho (seção 7, regra 4).

## 7. Como aplicamos aqui (regras práticas)
1. **Paywall não se mexe sem OK do Léo/Davi.** Preço, planos, ordem e texto ficam como estão (Léo, 20/11). Proposta de paywall sai como página de decisão em sim/não pro Davi, 1 variável por vez, teste 50/50 ao mesmo tempo, métrica definida antes (modelo: P-001).
2. **Antes de cobrar, o plano da moto.** O valor que é da pessoa (revisão da vez, km, datas da moto dela) vem antes do paywall. A aposta da casa é encurtar o caminho até ele (P-001), sem tocar no paywall. Moto fora do catálogo não chega ao paywall (D-20261124-produto-4): resolver isso conta como resolver o funil.
3. **Checklist da tela que cobra** (toda proposta passa por ele antes de ir ao Davi): nome e duração do plano · o que libera · valor cobrado em destaque e localizado · "renovação automática, cancele pela loja" · restaurar compras · Termos e Privacidade · botão de sair visível · nenhuma palavra "grátis/teste/dias" · nada de "vitalício". O paywall do código de 25/11 já tem isso: valor total em destaque (`precoPrincipal="total"` em pro-producao-checkout.tsx:504), renovação e cancelamento (paywall-minhamoto.tsx:95-106), restaurar, termos e privacidade (paywall-minhamoto.tsx:617-629).
4. **Nunca ligar oferta introdutória (teste ou preço de entrada) na App Store Connect ou no Play Console.** O paywall lê a oferta da loja e escreve "X dias grátis" e "Começar X dias grátis" sozinho (pro-producao-checkout.tsx:167 e 510; paywall-minhamoto.tsx:489 e 586). Isso fere a decisão do Léo sem ninguém mexer em código.
5. **Preço:** fora do app (anúncio, post, vídeo) "R$19,90" sem "por mês"; carrossel sem preço (26/11); criativo da App Store sem preço (2.3.14). **Dentro da tela que cobra**, a duração e a renovação ("mensal", "/mês") são exigência da Apple e do Google e ficam. Exceção levada ao Léo pelo professor-chefe em 27/11 pra registrar em decisoes.md; até lá, ninguém propõe tirar o período da tela que cobra.
6. **Plano pré-selecionado:** hoje é o mensal (Davi, 17/11; código de 25/11 passa `planoInicialId` do mensal). O mercado puxa pro anual em destaque (+10 a 30% de LTV [ESP]). É hipótese de teste pra depois da 1ª leitura do funil e do OK do Davi, nunca troca direta.
7. **O que medir:** `paywall_view` → compra por plataforma (iOS e Android separados), receita por instalação, reembolso e 1ª renovação. Sem `paywall_view` no código (só `af_complete_registration`), nenhum teste de paywall fecha leitura: evento primeiro (D-20261126-produto-2).
8. **Multi-step é candidato, não plano.** Só entra como teste quando houver evento por etapa e cada tela disser preço e renovação com clareza (regra do Google sobre tela que confunde).
9. **Android:** propor ao Davi carência e mensagem de pagamento recusado (Play, 29/09/2026). Recupera assinante sem mexer no paywall.
10. **Número de mercado não vira meta.** 10,7% é mediana de hard paywall com outros preços e categorias; nossa régua nasce da 1ª leitura em %, sem número absoluto no repositório.
