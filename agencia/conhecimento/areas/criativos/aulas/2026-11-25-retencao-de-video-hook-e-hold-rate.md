# Aula 25/11/2026 · Retenção de vídeo de anúncio: taxa de gancho, retenção e iteração de ganchos

Para: Walt Disney (Criativos), Estúdio Audiovisual e Phileas Fogg; cópia útil pro Escobar (Tráfego) e Cardone (Infoprodutos).
Por que importa agora: o teste dos 3 estilos dos Corretores e os vídeos A1/B1 do MinhaMoto vão gerar números por criativo. Sem saber ler gancho × retenção × clique, a gente troca o vídeo inteiro quando bastava trocar os 3 primeiros segundos (ou o contrário).
Legenda: **[OF]** oficial · **[ESP]** especialista/fornecedor. Meta e TikTok **não publicam benchmark** de taxa de gancho nem de retenção: todo benchmark abaixo é de terceiro.

## 1. O que é: as métricas e as fórmulas
- **Taxa de gancho (hook rate / thumbstop):** quem passou dos primeiros segundos ÷ impressões.
  - Meta: reproduções de 3 s ÷ impressões. TikTok: visualizações de 2 s ÷ impressões [ESP] (Billo, atualizado 24/09/2026: https://billo.app/blog/hook-rate-to-hold-rate).
- **Retenção (hold rate):** ThruPlays (15 s ou vídeo inteiro) ÷ reproduções de 3 s [ESP] (Billo; Jetfuel, 20/08/2026: https://jetfuel.agency/creative-performance-metrics-for-dtc-video-ads-hold-rate-thumbstop-and-thruplay-benchmarks-2026/). Dividir por impressões dá número menor e incomparável.
- **Taxa de clique de quem ficou** (thumbstop click rate): cliques ÷ reproduções de 3 s [ESP] (Motion, central de ajuda 27/10/2025: https://help.motionapp.com/en/articles/8757194-tell-stories-and-build-hypotheses-with-metrics).
- **TikTok, métricas nativas [OF]** (Video play, atualizado nov/2025: https://ads.tiktok.com/help/article/video-play?lang=en): visualizações de 2 s e de 6 s, 25/50/75/100%, tempo médio por usuário (com replays) e **focused view** (6 s ou 15 s, ou interação positiva dentro da janela).
- **Meta [OF]:** ThruPlay = 15 s ou até o fim. A Meta está trocando "3-second viewers" por *media views/viewers* nos insights orgânicos da Graph API (anunciado 18/02/2026, descontinuação em jun/2026: https://developers.facebook.com/blog/post/2026/02/18/introducing-graph-api-v25-and-marketing-api-v25). No Gerenciador de Anúncios, conferir se "reproduções de 3 segundos" ainda aparece antes de montar o placar.

## 2. Números de referência (todos de terceiros)
| Métrica | Fraco | Saudável | Elite | Fonte |
|---|---|---|---|---|
| Gancho Meta, público frio | <25% (corte <15%) | 25–35% | 35–45%+ | Billo 1º sem/2026 (88.329 anúncios, média 25,4%); Ryze 04/06/2026 |
| Gancho Meta por posicionamento | — | Feed ~23% (18–28%) · Reels ~30% (24–36%) | — | AdSights via Jetfuel |
| Gancho TikTok | — | média ~31% | 40–45% | Tuff (11 contas) via Billo |
| Retenção (ThruPlay ÷ 3 s) | <18% | ~20–25% | — | AdSights via Jetfuel; Ryze |
| CTR vídeo de vendas Meta | — | ~1,9% | — | Billo 2026 |
| CTR anúncio de lead, imóveis (Meta) | — | 3,75% (conversão 9,5%) | — | WordStream/LocaliQ, abr/2024–jun/2025: https://wordstream.com/blog/facebook-ads-benchmarks-2025 |
| CTR tráfego, automotivo (reparo/serviço) | — | 0,80% | — | WordStream/LocaliQ |
- Referências oficiais de atenção:
  - Meta [OF]: mais de 75% das visualizações de Reels no Instagram são com **som ligado**; seguir os "creative essentials" (9:16, áudio, gancho e CTA na zona segura) deu 2× mais entrega no Reels (Meta for Developers, 07/11/2024: https://developers.facebook.com/blog/post/2024/11/07/unlock-the-power-of-reel-ads/). E o anúncio tem que **funcionar sem som** também (texto na tela) (https://business.meta.com/news/video-ad-best-practices/).
  - Meta/Nielsen (histórico, 2015–2016): 47% do valor de uma campanha de vídeo é entregue nos 3 primeiros segundos; lembrança mensurável a partir de 0,25 s; legendas aumentaram o tempo médio de visualização em 12% (TechCrunch 18/02/2016; Social Media Today 05/08/2018). Dado antigo: usar como direção.
  - TikTok [OF] (Creative best practices, jun/2025: https://ads.tiktok.com/help/article/creative-best-practices?lang=en): apresentar a proposta nos **3 primeiros segundos**, priorizar o gancho nos **6 primeiros**, som ou música, texto na tela, 9:16 na zona segura. Creative Codes (PDF oficial, dados 2020–2022): 90% do impacto em lembrança acontece nos primeiros 6 s; gancho de suspense +16% de tempo assistido; produto na tela +25% de lembrança; card de CTA +45%.
  - A meta "gancho em menos de 2 s" é de mercado (Motion), não oficial do TikTok.

## 3. Diagnóstico: a matriz
| Gancho | Retenção | Clique / conversão | O que está errado → o que trocar |
|---|---|---|---|
| Baixo | Alta | — | Corpo bom, abertura fraca → **iterar gancho** (1º frame, texto na tela, primeira fala) |
| Alto | Baixa | — | Abertura promete, corpo enrola → entregar a promessa mais cedo, cortar, mudar o ritmo depois dos 3 s |
| Baixo | Baixa | — | Ideia/ângulo errado → refazer o conceito (abaixo de ~15% de gancho, desligar) |
| Alto | Alta | CTR baixo | Falta CTA ou oferta clara → testar CTA e oferta no fim |
| Alto | Alta | CTR alto, conversão baixa | Página/oferta, ou gancho prometendo o que a página não entrega |
| Qualquer | Baixa | CTR alto | Pode estar ótimo: a pessoa clicou cedo |
Base: Motion [ESP] ("gancho bom + retenção fraca = o conteúdo depois do gancho precisa de trabalho; clique bom + conversão fraca = olhe página e oferta"), Billo e Ryze [ESP]. **A decisão final é sempre a venda (UTMify), não a retenção.**

## 4. Como o top 1% itera ganchos
- **Trava o corpo, a prova e o CTA; varia só a abertura.** Grava 5–6 aberturas na mesma sessão, mesma pessoa, mesmo cenário: chamada direta ao público, afirmação forte, pergunta, quebra de padrão, prova social. Cada gancho vira um anúncio; julga primeiro pela taxa de gancho, depois pela venda [ESP] (Kalungi, 17/07/2026: https://www.kalungi.com/blog/test-ad-hooks-not-full-ads).
- **Mesmo ângulo, outro formato de abertura** (POV, depoimento, preço na tela, quebra visual), **um elemento por vez**; 10–20 variações por ciclo nas contas grandes; renovar a cada 7–10 dias; fadiga = CPM subindo + CTR caindo [ESP] (Billo, 24/09/2026: https://billo.app/blog/ad-hooks-variations/).
- Atenção ao leilão (aula de Tráfego de 25/11): variação de gancho do mesmo vídeo pode ser agrupada pela Meta como o mesmo anúncio. Ganchos fortes de verdade mudam **imagem e fala** do 1º segundo, não só o texto.
- Áudio forte **e** texto no 1º frame: as duas coisas (som ligado na maioria das visualizações de Reels, mas parte assiste sem som).

## 5. Erros comuns
1. **Gancho isca:** taxa de gancho alta com venda fraca. A Billo mostra anúncios com o maior gancho que mal empataram, e outros com gancho menor que renderam várias vezes mais.
2. Julgar só pelo gancho (ler gancho → retenção → clique → venda, juntos).
3. Retenção com o denominador errado (impressões em vez de reproduções de 3 s).
4. Condenar retenção baixa quando o CTR é alto.
5. Mudar várias coisas ao mesmo tempo e não saber o que funcionou.
6. Usar benchmark de e-commerce americano como régua: a régua boa é a **mediana da própria conta** por formato.

## 6. Como aplicamos aqui (regras práticas)
1. **Placar por criativo** (Disney + Escobar): taxa de gancho (3 s ÷ impressões), retenção (ThruPlay ÷ 3 s), CTR de link, custo por venda (UTMify, por `utm_content`). Em %, nunca R$ no público.
2. **Pisos iniciais, até termos a mediana própria:** gancho ≥25% e retenção ≥20% em público frio. Abaixo de 15% de gancho com gasto mínimo atingido = ideia errada. Depois de 2 semanas de dado, troca o piso pela mediana da conta.
3. **Use a matriz antes de pedir vídeo novo.** Gancho baixo + retenção boa → só abertura nova (barato). Gancho alto + venda fraca → olhar promessa × página com o Cardone antes de culpar o vídeo.
4. **Corretores:** o que vende é a Ana Paula falando (aprendizados). O próximo pedido de gravação a ela (só com OK do Léo e autorização dela) inclui **5–6 aberturas diferentes** pro mesmo corpo, gravadas na mesma sessão; cada uma vira um criativo. Nada de voz ou rosto dela por IA.
5. **Ganchos válidos nos Corretores:** chamada direta ("Corretor, …"), fala real do cliente ("E agora, qual é o próximo passo?"), pergunta-quiz, quebra de padrão mostrando a página do Mapa. Sempre sem promessa de renda e equilibrando ganho e perda (DESIGN-CORRETORES §4b).
6. **MinhaMoto:** texto no 1º frame + celular entrando (entrada aprovada pelo Léo) + promessa entregue até o 3º segundo; nunca prometer mais do que a tela mostra ("o app avisa na Garagem"). Preço só "R$19,90", nunca "por mês"; asset da App Store sem preço.
7. **Toda peça sai com legenda queimada e áudio** (voz ou música sem direito autoral), 9:16 na zona segura x 140–940, y 150–1500.
8. **Ciclo:** vencedor ganha 3–5 ganchos novos na semana seguinte; perdedor por conceito sai; reposição antes da fadiga (CTR caindo + CPM subindo).
