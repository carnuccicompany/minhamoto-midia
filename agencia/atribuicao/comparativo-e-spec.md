# Atribuição de instalações e assinaturas — MinhaMoto

> Pesquisa de 16/11/2026. Preços mudam: confirmar na página do fornecedor antes de assinar.
> Funil: criativo (Meta Ads) ou post orgânico → página de vendas (minhamotopagina.online, hoje com UTMify) → App Store / Google Play → instalação → onboarding → paywall → assinatura (RevenueCat).
> Problema: a origem se perde entre a página de vendas e a assinatura. A UTMify não integra com o RevenueCat.

---

## 1. Comparativo

| | **AppsFlyer** | **Branch** | **Adjust** |
|---|---|---|---|
| Plano grátis / inicial | **Zero**: grátis, com pacote de 12.000 conversões grátis no 1º ano; depois, Growth a US$0,07 por conversão¹ | Basics com teste grátis; preços não são públicos (só por demo)² | **Base**: até 1.500 atribuições por mês por até 12 meses (até 18.000 por ano)³ |
| SDK pra Capacitor | **Plugin oficial** `appsflyer-capacitor-plugin` (marca AppsFlyer, ~9,6 mil downloads/semana, suporta Capacitor 3–6)⁴ | `capacitor-branch-deep-links`, documentado no Help Center da Branch⁵ | **Sem plugin oficial.** Só plugins de comunidade (`@joinflux/capacitor-adjust` etc.)⁶ |
| Integração com RevenueCat | Nativa. Envia `setAppsflyerID` + `collectDeviceIdentifiers`; o RevenueCat manda pro AppsFlyer, pelo servidor, conversões de trial, renovações e receita⁷ | Nativa. Usa `setIdentity` com o mesmo ID do RevenueCat; o RevenueCat manda START_TRIAL, PURCHASE (inicial, conversão, renovação) e cancelamentos⁸ | Nativa. Envia `setAdjustID` + `collectDeviceIdentifiers`; o RevenueCat manda eventos do ciclo de assinatura (tokens opacos)⁹ |
| Métodos no SDK Capacitor do RevenueCat (`@revenuecat/purchases-capacitor` 13.x) | `setAppsflyerID({appsflyerID})` ✅ | via `setAttributes({$branchId})` | `setAdjustID({adjustID})` ✅ |
| Página de vendas → app | OneLink + **Smart Script** (lê os parâmetros da URL da página e gera os links das lojas automaticamente)¹⁰ | Branch links; deferred deep link no iOS só via NativeLink (pacote Engagement)⁵ | Links Adjust; deep link e deferred deep link listados³ |
| Meta Ads / TikTok Ads | Parceiros integrados (padrão de mercado) | Parceiros integrados | Parceiros integrados |
| iOS (ATT, SKAdNetwork) e Android (Install Referrer) | Sim | Sim | SKAN sem custo extra pra todos os clientes³ |
| Dados pro dashboard próprio | Callback de conversão no app (media_source, campaign) + APIs/relatórios (confirmar o que entra no Zero) | APIs agregadas listadas no Basics² | "Raw data e Report Service API ilimitados" (sem dizer em qual plano)³ |

¹ Fonte: [Airbridge — Mobile Attribution Pricing](https://www.airbridge.io/tips/mobile-attribution-pricing-plans-contract-terms), artigo de 02/09/2026 com preços checados em 19/08/2026. **É conteúdo de um concorrente**: confirmar na [página de preços da AppsFlyer](https://appsflyer.com/pricing), que não mostra os números sem abrir o comparativo. A mesma fonte dá o Singular grátis até 15.000 conversões pagas, mas não achei SDK Capacitor oficial dele, por isso ficou fora.
² [branch.io/pricing](https://branch.io/pricing)
³ [adjust.com/pricing](https://adjust.com/pricing)
⁴ [npm appsflyer-capacitor-plugin](https://npmjs.com/package/appsflyer-capacitor-plugin) · [API](https://github.com/AppsFlyerSDK/appsflyer-capacitor-plugin/blob/main/docs/API.md)
⁵ [Branch — Capacitor SDK](https://help.branch.io/developer-hub/docs/capacitor)
⁶ [npm @joinflux/capacitor-adjust](https://npmjs.com/package/@joinflux/capacitor-adjust)
⁷ [RevenueCat — AppsFlyer](https://www.revenuecat.com/docs/integrations/attribution/appsflyer)
⁸ [RevenueCat — Branch](https://www.revenuecat.com/docs/integrations/attribution/branch)
⁹ [RevenueCat — Adjust](https://www.revenuecat.com/docs/integrations/attribution/adjust)
¹⁰ [AppsFlyer — OneLink Smart Script](https://support.appsflyer.com/hc/en-us/articles/360000677217)
SDK do RevenueCat: [@revenuecat/purchases-capacitor](https://socket.dev/npm/package/@revenuecat/purchases-capacitor)

**Atenção, AppsFlyer:** a página [Zero update 2026](https://www.appsflyer.com/pt/zero-update-2026/) diz que, desde 13/08/2026, o Zero de *deep linking* perdeu deep link avançado, exportação de dados brutos e domínio próprio. Configurações de Smart Script já existentes continuam funcionando, mas sem edição. **Antes de assinar, confirmar com a AppsFlyer se OneLink e Smart Script entram no plano escolhido.** Se não entrarem, o plano B é OneLink fixo por canal, montado à mão (seção 2.6).

### Recomendação: **AppsFlyer**

1. É a única das três com **plugin Capacitor oficial e mantido** (o app é Capacitor). A Adjust só tem plugin de comunidade, e a Branch documenta o dela mas sem versão nem manutenção clara.
2. O SDK Capacitor do RevenueCat já tem **`setAppsflyerID`**: a ligação com o pagamento é nativa e documentada dos dois lados.
3. **Custo inicial zero**: 12 mil conversões grátis no 1º ano cobrem com folga o volume atual. Conversão costuma ser instalação atribuída a mídia; orgânico não deveria contar (confirmar a definição no contrato).
4. **Smart Script** pega as UTMs que já chegam na página de vendas (Meta Ads, bio) e as leva até a instalação, sem reescrever a página.
5. É o maior parceiro do Meta e do TikTok no mercado, e o callback de conversão (`media_source`, `campaign`) dá o dado de origem dentro do próprio app, que é o que alimenta o dashboard.

**Custo esperado:** R$0 no 1º ano no volume atual. Depois, cerca de US$0,07 por instalação atribuída a mídia paga. Exemplo: 1.000 instalações pagas por mês ≈ US$70/mês. Confirmar com a AppsFlyer.

---

## 2. Especificação pro Davi (seguir com o Claude no repo `minhamotooficial`)

> Regras do repo continuam valendo: nada de commit, push ou deploy sem o ok do Davi. **Chave nunca vai pro código versionado nem pro chat**: use as variáveis de ambiente do Codemagic e os segredos do Supabase.

### 2.1 Contas e chaves (Léo ou Davi geram)
| O quê | Onde gerar | Onde guardar |
|---|---|---|
| Conta AppsFlyer + app iOS (id 6815447825) e Android (`com.carnuccicompany.minhamoto`) | appsflyer.com | — |
| **Dev key** do AppsFlyer | AppsFlyer → Configuration → App settings | Variável de ambiente do build (Codemagic) → injetada na config do app |
| Template OneLink | AppsFlyer → Engage → OneLink | Usado na página de vendas |
| Chave da integração (dev key ou S2S token) | AppsFlyer | **Painel do RevenueCat** → Integrations → AppsFlyer |
| Conectar Meta Ads e TikTok Ads | AppsFlyer → Integrated Partners | — |

### 2.2 Instalar o SDK
```bash
npm i appsflyer-capacitor-plugin
npx cap sync
```
- iOS: no `Info.plist`, `NSUserTrackingUsageDescription` (texto na 2.4). Adicionar `AdSupport` e `AppTrackingTransparency`.
- Android: o plugin traz o Install Referrer. Conferir a permissão `com.google.android.gms.permission.AD_ID`.

### 2.3 Inicializar (no boot do app, antes do RevenueCat comprar qualquer coisa)
```ts
import { AppsFlyer } from 'appsflyer-capacitor-plugin';
import { Purchases } from '@revenuecat/purchases-capacitor';

// 1) listeners ANTES do init
AppsFlyer.registerDeepLinkListener({ onDeepLinking: (d) => { /* opcional: abrir tela */ } });

await AppsFlyer.init({ devKey: import.meta.env.VITE_AF_DEV_KEY, appId: '6815447825' });

// 2) conversão: origem da instalação
AppsFlyer.registerConversionListener({
  onConversionDataSuccess: async (data) => {
    // só valores FINAIS: atributos reservados do RevenueCat só podem ser gravados 1 vez
    const organico = data.af_status === 'Organic';
    await Purchases.setMediaSource({ mediaSource: organico ? 'organic' : (data.media_source ?? 'desconhecido') });
    if (!organico && data.campaign) await Purchases.setCampaign({ campaign: data.campaign });
    // opcional: adset/ad via setAttributes({ $adGroup, $ad, $creative })
  },
  onConversionDataFail: (e) => console.warn('AF conversion', e),
});

// 3) ligar AppsFlyer ↔ RevenueCat (depois do Purchases.configure)
const uid = await AppsFlyer.getAppsFlyerUID();
if (uid) await Purchases.setAppsflyerID({ appsflyerID: uid });
await Purchases.collectDeviceIdentifiers();
```
- `setAppsflyerID` e `collectDeviceIdentifiers` têm que acontecer **antes da primeira compra**. Sem o ID do AppsFlyer, alguns eventos não chegam⁷.
- Se o app usa login, usar o **mesmo ID** como `appUserID` do RevenueCat e `AppsFlyer.setCustomerUserId(...)`.
- **Não** mandar evento de compra pelo app pro AppsFlyer: o RevenueCat já manda pelo servidor, e mandar dos dois lados duplica a receita⁷.
- A sequência de sessão do plugin (`registerSessionReadyListener` → `start()`) segue a doc do plugin⁴.

### 2.4 ATT (iPhone)
- **Quando:** no onboarding, logo depois da tela que mostra o valor do app e antes do paywall. Uma tela própria explica, depois vem o pop-up da Apple. Configurar o SDK pra esperar a resposta do ATT antes de mandar a instalação: no SDK nativo é `waitForATTUserAuthorization` (cerca de 60s); confirmar o nome da opção na doc do plugin Capacitor.
- **Texto do `NSUserTrackingUsageDescription`:**
  > "Usamos essa permissão só pra saber qual anúncio ou post trouxe você até o MinhaMoto e melhorar nossas campanhas. Seus dados da moto nunca são compartilhados."
- Depois da resposta, chamar `Purchases.collectDeviceIdentifiers()` de novo, pra mandar o IDFA se a pessoa aceitou.
- Quem recusa o rastreamento é atribuído por SKAdNetwork/AdAttributionKit (agregado, sem dado por pessoa). Esse limite vem da Apple e vale pra qualquer ferramenta.

### 2.5 Eventos no app (só funil, sem compra)
| Evento | Quando |
|---|---|
| `onboarding_complete` | fim do onboarding |
| `paywall_view` | paywall aparece |
| `att_answered` (param `status`) | resposta do ATT |
Trial, assinatura, renovação e cancelamento chegam pelo **RevenueCat → AppsFlyer** (lado servidor). Não duplicar.
```ts
await AppsFlyer.logEvent({ eventName: 'paywall_view', eventValues: {} });
```

### 2.6 Página de vendas (minhamotopagina.online)
- **Opção A (recomendada):** colar o **Smart Script V2** gerado no painel da AppsFlyer (dá pra instalar por GTM). Ele lê `utm_source`, `utm_campaign` etc. da URL e reescreve os botões App Store / Google Play como OneLink com `pid`/`c`. Os anúncios do Meta continuam mandando UTM normalmente.
- **Opção B (se o plano não incluir Smart Script):** um OneLink fixo por origem, ex.: `https://<sub>.onelink.me/<id>?pid=instagram_organico&c=bio`, e trocar os botões. Os links `l/*.html` do repo minhamoto-midia passam a redirecionar pro OneLink em vez de ir direto pra loja.
- A UTMify pode continuar pra métrica do site, mas a verdade de instalação e assinatura passa a ser AppsFlyer + RevenueCat.

### 2.7 Configurar o RevenueCat
Project settings → Integrations → **AppsFlyer**: chave (iOS/Android ou geral), nomes dos eventos e receita **líquida da comissão da loja**. Marcar "Key is a S2S token" se usar S2S. Pra eventos de sandbox, usar a chave de sandbox⁷.

### 2.8 Checklist de teste
1. AppsFlyer → **SDK Integration Test**: registrar o aparelho de teste pelo advertising ID.
2. Abrir um link de teste (`?pid=teste&c=teste_davi`) no aparelho, instalar pelo link e abrir o app.
3. Confirmar no painel do AppsFlyer a instalação **não orgânica** com `pid=teste`.
4. Fazer uma compra **sandbox** no app.
5. RevenueCat → Customer: conferir `$appsflyerId`, `$idfv`/`$gpsAdId`, `$ip`, `$mediaSource=teste` e `$campaign=teste_davi`.
6. RevenueCat → Customer History: evento entregue pro AppsFlyer com sucesso. AppsFlyer: evento de receita na campanha `teste_davi`.
7. Repetir sem link (instalação orgânica): `$mediaSource=organic`.
8. iOS: testar aceitando e recusando o ATT.

**Esforço estimado pro Davi:** 1 a 2 dias de dev (SDK, ATT, ligação com RevenueCat, eventos e testes) + o tempo de revisão das lojas. A página de vendas leva de 1 a 2 horas.

---

## 3. Plano do dashboard interno (PWA)

### Fontes
1. **Webhook do RevenueCat** → cada evento (TRIAL_STARTED, INITIAL_PURCHASE, RENEWAL, CANCELLATION, EXPIRATION, PRODUCT_CHANGE, REFUND…) chega com os **subscriber attributes** (`$mediaSource`, `$campaign`, `$ad`…). É o que liga **origem → assinatura → receita, por pessoa**, sem depender de API paga do AppsFlyer.
2. **RevenueCat Charts & Metrics API v2** (`/metrics/overview`, `/charts/{mrr|revenue|actives|trials|trial_conversion_rate…}`, com `start_date`/`end_date`/`resolution`; limite de 25 req/min; permissões `charts_metrics:*:read`)¹¹: números oficiais de MRR, receita, ativos e trials pra conferir os totais.
3. **Instalações por origem:** um evento `app_first_open` gravado pelo próprio app (com `media_source`/`campaign` do callback do AppsFlyer) numa tabela do Supabase de analytics. Opcional: API ou exportação do AppsFlyer, se o plano incluir.
4. **Custo de mídia** (pra CAC/ROAS): Marketing API do Meta (gasto por campanha/dia), quando tiver token de leitura de anúncios.

¹¹ [RevenueCat — Charts & Metrics API v2](https://www.revenuecat.com/docs/api-v2/charts-and-metrics)

### Métricas e cortes
- **Períodos:** hoje, ontem, 7d, 30d, mês, ou intervalo personalizado; visão diária, semanal ou mensal.
- **Cortes:** canal (Meta pago, Insta orgânico, TikTok, Face, busca na loja/orgânico, site), campanha, criativo, plataforma (iOS/Android).
- **Funil:** instalações → onboarding concluído → viu paywall → trial → pago (taxa de cada etapa).
- **Receita:** novos assinantes, conversão trial→pago, assinantes ativos, MRR, receita bruta e líquida, churn, reembolsos, mix de planos (mensal, trimestral, semestral, anual).
- **Unit economics:** custo por instalação, CAC, LTV e ROAS por campanha, assim que o custo do Meta entrar.

### Hospedagem segura (o repo minhamoto-midia é PÚBLICO)
**Recomendado: um projeto Supabase separado só pra analytics + PWA estático com login.**
- **Supabase "minhamoto-analytics"** (projeto novo, separado do banco do app, então não mexe no app):
  - Edge Function `rc-webhook`: recebe o webhook do RevenueCat, valida o header de autorização (segredo) e grava em `rc_events`.
  - Edge Function `rc-sync` agendada (pg_cron, diária): puxa a Charts API v2 pra `rc_metrics_daily`.
  - Tabela `installs`: o app grava o `app_first_open` via função com chave anônima e RLS só de insert.
  - **Auth** por e-mail (magic link) só pro Léo e o Davi. **RLS:** leitura só pra esses dois usuários.
  - Segredos (chave secreta v2 do RevenueCat, segredo do webhook, token do Meta) ficam **nos secrets do Supabase**, nunca no front.
- **PWA:** HTML/JS estático (manifest + service worker, "adicionar à tela inicial"). Pode ficar no GitHub Pages ou num repo privado: o código é público, mas **nenhum dado aparece sem login**, porque tudo vem do Supabase protegido por RLS.
- Por que não só GitHub Pages com JSON: os dados financeiros ficariam abertos pra qualquer um.
- Alternativa mais simples, sem cortes por campanha: só o painel do RevenueCat + o painel do AppsFlyer. Não dá a visão unificada que o Léo quer.

### LGPD
- Coletar só identificadores de publicidade com o consentimento exigido (ATT no iOS) e citar AppsFlyer/RevenueCat na política de privacidade (finalidade: medir campanhas).
- No dashboard, mostrar só agregados (contagens e receita por origem), sem e-mail ou nome.
- `$appsflyerSharingFilter` no RevenueCat permite bloquear o compartilhamento com parceiros específicos, se precisar⁷.
