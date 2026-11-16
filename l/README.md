# Links de download por rede — MinhaMoto

Cada rede tem seu próprio link. Quem abre no **iPhone** vai direto pra App Store, quem abre no **Android** vai pro Google Play, e quem abre no computador vê uma página com os dois botões. Cada link leva uma etiqueta de campanha, então as lojas mostram **quantos downloads vieram de cada rede**.

Os links não usam cookie nem analytics e não coletam dado pessoal.

## Os links

| Canal | Link | Onde usar | Etiqueta Apple (`ct`) | Etiqueta Google (UTM) |
|---|---|---|---|---|
| Instagram — bio | https://carnuccicompany.github.io/minhamoto-midia/l/ig.html | Link da bio do Instagram | `instagram-bio` | `instagram / bio` |
| Instagram — stories | https://carnuccicompany.github.io/minhamoto-midia/l/ig-story.html | Figurinha de link nos stories | `instagram-story` | `instagram / story` |
| TikTok — bio | https://carnuccicompany.github.io/minhamoto-midia/l/tt.html | Link da bio do TikTok | `tiktok-bio` | `tiktok / bio` |
| Facebook — página | https://carnuccicompany.github.io/minhamoto-midia/l/fb.html | Site da página + botão "Saiba mais" | `facebook-pagina` | `facebook / bio` |
| Site | https://carnuccicompany.github.io/minhamoto-midia/l/site.html | Botões de download do minhamotopagina.online | `site` | `site / site` |

Todos usam `utm_campaign=organico` no Google Play. Os links finais montados são:

- **Apple:** `https://apps.apple.com/app/apple-store/id6815447825?pt=129492564&ct=<canal>&mt=8` (formato do gerador oficial de link de campanha da App Store Connect; `pt` é o código de provedor da conta).
- **Google:** `https://play.google.com/store/apps/details?id=com.carnuccicompany.minhamoto&referrer=utm_source%3D<rede>%26utm_medium%3D<meio>%26utm_campaign%3Dorganico`

Pra criar um canal novo (um anúncio, um influenciador), copie uma das páginas e troque só a linha `window.CANAL={...}`.

## Onde ver os números

**App Store (iPhone)**
1. Entre na App Store Connect → **Apps** → MinhaMoto → aba **Análise**.
2. Menu da esquerda: **Aquisição → Campanhas**.
3. Aparece uma linha por etiqueta (`instagram-bio`, `tiktok-bio`…) com impressões, downloads e vendas.
   - A Apple só mostra uma campanha depois que **pelo menos 5 contas Apple diferentes** instalarem por ela.
   - Os dados vêm só de quem permitiu compartilhar análises com desenvolvedores, então o número é uma amostra, não o total.

**Google Play (Android)**
1. Entre no Play Console → MinhaMoto → **Aumentar número de usuários → Desempenho da página da loja → Análise de conversão**.
2. Filtre a origem do tráfego por **Anúncios e indicações**. Aí aparecem as dimensões **Origem UTM** e **Campanha UTM** (`instagram`, `tiktok`, `facebook`…), com visitantes e conversão de cada uma.

## Limitação: a maioria dos downloads não passa por link

Quem vê o vídeo no TikTok e depois **busca "MinhaMoto" na loja** não clica em link nenhum. Esse download entra como "Busca na App Store/Play" e não tem como saber de qual rede veio. Então os links mostram a origem de quem clicou, não de todo mundo que conheceu o app pelas redes.

O que dá pra fazer com isso:
- **Comparar canais entre si** (bio do Insta × bio do TikTok × stories).
- **Cruzar datas:** pico de "busca na loja" no dia em que um vídeo viralizou indica de onde veio o pico.
- Pra rastrear 100%, inclusive anúncio pago, só com uma ferramenta de atribuição dentro do app (AppsFlyer, Branch etc.). Isso exige mudança no código e custa caro, então só vale quando o investimento em anúncio for grande.
