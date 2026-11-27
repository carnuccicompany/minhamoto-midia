# Aula 27/11/2026 · Páginas de produto personalizadas (iOS) e fichas personalizadas (Play) pra tráfego pago

Para: Jeff Bezos (Lojas) e Ayrton Senna (ASO), com cópia útil pra Pablo Escobar (Tráfego) e Disney (Criativos).
Por que importa agora: em 26/11 o Léo decidiu que o MinhaMoto começa com **anúncio → landing → loja** (campanha otimizando clique pra loja; venda lida no AppsFlyer pelo OneLink da landing). A loja virou a última etapa antes do assinante. Quem lê uma promessa no anúncio e cai numa página genérica desiste. A página personalizada é o jeito oficial de a loja **continuar a promessa do anúncio**.
Legenda das fontes: **[OF]** oficial lido direto (27/11/2026) · **[OF*]** oficial citado por terceiro (conferir antes de virar regra dura) · **[ESP]** especialista ou fornecedor (vende ferramenta; caso de cliente é vitrine, não média).

## 1. O que é
- **Apple · Custom Product Pages (CPP):** versões extras da página do app na App Store, cada uma com URL própria. Quem chega pelo link vê a versão personalizada; quem chega pela busca vê a padrão (a não ser que a CPP tenha palavras-chave, ver §2) [OF] (https://developer.apple.com/app-store/custom-product-pages).
- **Google Play · fichas personalizadas (custom store listings, CSL):** versões extras da ficha, mostradas por país, por segmento (usuário inativo, quem nunca comprou, palavra de busca, tráfego de anúncio) ou por **URL única** com `&listing=` [OF] (https://support.google.com/googleplay/android-developer/answer/9156429).
- **Não é teste A/B.** Página personalizada mostra uma versão pra um público que chega por um caminho; o teste com divisão de tráfego é o Product Page Optimization (Apple, até 3 variações de ícone, prints e vídeo) e o experimento de página do Play (1 experimento de gráficos por vez) [OF] (FUNDAMENTOS §2; https://support.google.com/googleplay/android-developer/answer/12053285). Comparar CPP contra a padrão compara públicos diferentes, não só páginas.

## 2. Limites (o que pode, quanto, como passa na revisão)
| | **Apple CPP** | **Play CSL** |
|---|---|---|
| Quantas | até **70** por app (iPhone e iPad) [OF]; eram 35 até out/2025 [ESP] (AppTweak, 01/02/2026) | até **50** [OF] |
| O que muda | prints, vídeos de prévia, texto promocional, palavras-chave e deep link [OF]. Nome, ícone, subtítulo e descrição ficam os da padrão [ESP] (AppTweak) | nome do app, ícone, descrições e gráficos (prints por aparelho) [OF]. Contato, política de privacidade e categoria são os mesmos [OF] |
| Como a pessoa chega | URL própria (a Apple diz que soma "um parâmetro de ID da página" à URL padrão; o nome usado no mercado é `ppid`) [OF]/[ESP]; Apple Ads (variações de anúncio); anúncios de rede via StoreKit (`customProductPageIdentifier`); editorial [OF] | `https://play.google.com/store/apps/details?id=<pacote>&listing=<parametro>` (minúsculas, números, `.`, `-`, `_`, `~`) [OF]; país; segmentos; Google Ads ("Ads Traffic") [OF] |
| Busca orgânica | desde jul/2025 a CPP pode aparecer na busca por palavras escolhidas do campo de palavras-chave; cada combinação de palavras vale pra uma página só; palavra do nome/subtítulo não entra [OF]/[ESP] (AppTweak) | "palavras de busca" é um dos segmentos [OF] |
| Revisão | toda CPP passa pela revisão da Apple, **independente de versão nova do app**; edição aprovada não muda a URL; precisa do app "Pronto para distribuição" e papel Admin, App Manager ou Marketing [OF] (https://developer.apple.com/help/app-store-connect/create-custom-product-pages/configure-multiple-product-page-versions) | precisa de ficha padrão publicada; cada CSL é revisada e aprovada antes de usar, inclusive como destino de anúncio [OF] |
| Deep link | opcional, por página; funciona do iOS 18 em diante; preferir universal link; **sem encurtador nem redirecionamento extra**; o link também passa pela revisão [OF] | não coberto na página de CSL |
| Métrica | App Analytics → Aquisição: impressões, downloads, conversão, retenção e receita média por pagante **por CPP**, comparando com a padrão; só aparece depois de **5 primeiros downloads** [OF] | relatório de desempenho da ficha, só depois de um mínimo de impressões; fichas de "tráfego de anúncio" só aparecem no AdMob e não batem com o total da campanha [OF] |
| Pega | idioma e país dos assets precisam bater com a campanha, senão o anúncio da Apple Ads não roda [OF] (https://ads.apple.com/app-store/best-practices/ad-variations); página desligada ou apagada manda pra padrão; apagar é definitivo [OF] | um país só pode estar em uma ficha; CSL não é traduzida sozinha; no Chrome o link pode abrir a versão web do Play [OF]/[ESP] (AppsFlyer) |

**Regras da loja valem igual na página personalizada:** prints mostram o app real e não enganam (Apple 2.3); imagens e vídeos promocionais dentro da App Store sem preço nem desconto (Apple 2.3.14, 16/10/2026, ver NOVIDADES).

## 3. Como ligar cada anúncio à sua página (o caminho técnico)
- **Pelo OneLink do AppsFlyer (o nosso caminho):** no link, em "Quando o app não está instalado", iOS → App Store com o ID da CPP; Android → Google Play com o parâmetro da CSL. Na URL: `af_ios_store_cpp=<ppid>` e `af_android_store_csl=<parametro>` [OF fornecedor] (https://support.appsflyer.com/hc/en-us/articles/4406217556625). O AppsFlyer guarda o valor no **clique**, não na impressão.
- **Meta:** o link da CPP vai no destino do anúncio; se o ID não bater com uma CPP, a pessoa cai na padrão [ESP] (Phiture, 27/09/2022, antigo: conferir no Gerenciador antes de usar).
- **TikTok:** CPP aceita no objetivo de promoção de app (instalação, cadastro, reengajamento), com menor custo, custo-alvo e maior valor; Smart+ também [OF] (https://ads.tiktok.com/help/article/about-ios-custom-product-pages?lang=en).
- **Apple Ads:** até 70 anúncios personalizados, cada um com sua CPP e deep link; casar a página com o tema das palavras do grupo; a Apple prefere mudar o criativo a mudar o público, porque 78% do volume de busca vem de aparelho com anúncio personalizado desligado (ano fiscal 2024) [OF].

## 4. Como o top 1% faz
1. **Uma página por intenção (ângulo/persona), não por criativo.** Granular demais dilui volume e não sai de "menos de 5 downloads" [ESP] (AppTweak).
2. **Print 1 repete a promessa do anúncio** com as mesmas palavras e a mesma tela; o resto dos prints sustenta essa promessa [ESP] (AppTweak; Phiture).
3. **Continuidade até dentro do app:** deep link leva pra tela que o anúncio mostrou (Apple: iOS 18+) [OF].
4. **ASO e tráfego no mesmo time:** quem faz o anúncio briefa a página; ângulo novo no anúncio = página revista [ESP] (AppTweak).
5. **Mede abaixo do download:** retenção e receita por pagante por CPP no App Analytics, não só conversão [OF].
6. **Testa páginas contra tráfego real** (SplitMetrics roda "até 4 páginas" por grupo e espalha a vencedora) [ESP] (SplitMetrics, 22/09/2026).

## 5. Números de referência (com cautela)
- **Média Apple:** quem manda gente pra CPP vê **+2,5 pontos percentuais** de conversão em média, "+156% sobre 1,6%" da página padrão [OF, sem data, lido 27/11/2026]. Cuidado: compara tráfego dirigido com tráfego geral; não é efeito puro da página.
- **Casos da Apple:** CBS Sports +20% de conversão; State of Survival +33% de conversão e −14% no custo por instalação [OF].
- **Apple Ads, variações com CPP contra o anúncio padrão (relatado pelo anunciante, sem data):** HelloFresh +9% conversão, −24% custo por instalação; Facetune +8% conversão, −15% custo por instalação; Norton 360 +30% ROAS [OF].
- **AppTweak:** CPP como variação de Apple Ads, apps +6,6% de conversão, jogos +8% (relatório, provável jul/2024) [ESP].
- **MobileAction, Apple Ads 2026:** variações com CPP em 2025, taxa de toque 1,72%, conversão toque→instalação 47,57% (55,87% em 2024) [ESP] (https://www.mobileaction.co/report/apple-ads-2026-benchmark-report/ad-variations-using-custom-product-pages/). É conversão de anúncio de busca, não serve de régua pra tráfego da Meta.
- **Meta:** +103% de instalações por mil impressões com CPP nos primeiros testes [ESP] (Phiture, 2022, antigo).
- **SplitMetrics:** BetterSleep +42,6% de taxa de toque e +40,5% de ROAS [ESP] (22/09/2026; o texto se contradiz, não usar como meta).
- Leitura honesta: casos de fornecedor são o melhor resultado, não a média. Ninguém publicou número de app pequeno, pago direto, no Brasil. A nossa régua vem do nosso App Analytics.

## 6. Erros comuns
1. Página por criativo (dezenas de páginas com poucos downloads; nada vira leitura).
2. Página que promete o que a versão publicada não entrega (Apple 2.3; caso da casa: "seu modelo", D-20261122-lojas-3).
3. Achar que CPP é teste A/B e declarar vencedor comparando públicos diferentes.
4. Assets em outro idioma/país que a campanha (anúncio não roda na Apple Ads).
5. Link com encurtador ou redirecionamento extra no deep link.
6. Preço, "grátis", desconto ou selo de promoção nos prints da página (Apple 2.3.14 e regra do Léo).
7. Play: usar a ficha de "tráfego de anúncio" e esperar que ela apareça na busca do Play (só AdMob); pôr o mesmo país em duas fichas.
8. Mudar o ângulo do anúncio e esquecer a página (a continuidade quebra em silêncio).
9. Ler a CPP só pela conversão da loja; a régua da casa é custo por **assinante pago**.

## 7. Como aplicamos aqui (regras práticas)
1. **Caminho:** anúncio → landing → OneLink → loja (decisão do Léo, 26/11). A CPP entra no OneLink (`af_ios_store_cpp`), sem mexer na campanha. **Uma página por ângulo de anúncio**, começando com no máximo 2 (os ângulos que forem ao ar), nunca uma por criativo.
2. **Android depois:** ficha personalizada do Play só quando houver campanha Android com verba (lição de 24/11, D-20261124-lojas-3 cancelada). Até lá o OneLink do Android vai pra ficha padrão.
3. **Continuidade de promessa:** o print 1 da CPP repete a promessa do anúncio em até 6 palavras, com tela real **da versão publicada** (não do `main`). Nada de "seu modelo" até o Davi confirmar a cobertura (D-20261122-lojas-3). A tabela anúncio × print da D-20261126-lojas-2 é o briefing de cada página.
4. **Texto da página:** sem "grátis", "teste", "X dias", "vitalício", "promoção" ou preço nos prints e vídeos (Apple 2.3.14 + Léo 24/11). Por cautela, também sem preço no texto promocional. "R$19,90" (nunca "por mês") fica no anúncio e na landing, onde o Léo liberou.
5. **Medição:** cada CPP com nome no padrão `MM-<ângulo>` e o mesmo ângulo no OneLink; ler no App Analytics (só depois de 5 primeiros downloads) e no AppsFlyer por clique; decidir por custo por assinante pago (RevenueCat confere o total). Base pequena se escreve "1 de 3", nunca "33%".
6. **Não é teste:** pra saber se a CPP vence a padrão, dividir o link da landing (metade CPP, metade padrão) ou testar os prints na página padrão pelo PPO. Sem essa divisão, a comparação é só indício.
7. **Deep link e palavras-chave orgânicas ficam pra segunda fase:** deep link só depois de o Davi confirmar o universal link e testar (iOS 18+); palavras-chave na CPP só com a ficha padrão estável.
8. **Nada vai à loja sem OK do Léo/Davi.** Quem cria e envia a CPP no App Store Connect é quem tem o acesso (Léo/Davi); o setor entrega o pacote pronto (prints, texto promocional, nome da página, ID no OneLink) e o parecer de regra (passa/corta).
