# Produto: novidades (últimos 90 dias)

Janela: 29/08/2026 a 27/11/2026. Pesquisado em 24/11/2026 e 27/11/2026 (treino do setor). Mais novo em cima.
Checado em 27/11/2026: Apple Developer News (último item 18/11, nada novo desde 24/11), App Review Guidelines (3.1.2 e 2.3.14 lidas), Apple HIG In-App Purchase (versão .md), página de assinaturas da Apple, Google Play (play-policies, política de assinaturas, blog Android Developers), RevenueCat blog (itens até 26/11), AppsFlyer (sem item datado relevante achado). Itens marcados "buraco da janela" são anteriores a 24/11 e faltavam aqui.

## 26/11/2026 · RevenueCat: preço na App Store x na web (regras de mudar preço)
- Artigo resume as regras das lojas pra mexer em preço de assinatura: na Apple, aumento acima de 50% **e** acima de US$5 por período (US$50/ano no anual) exige consentimento do assinante, e só 1 aumento a cada 12 meses (Áustria e Alemanha: consentimento sempre); no Google Play o aumento é opt-in por padrão, com 37 dias de aviso. Redução de preço passa todo mundo pro preço menor e não volta. Erro de cobrança responde por 15,2% (App Store) a 32,2% (Play) dos cancelamentos [ESP].
- **O que muda pra nós:** qualquer proposta futura de mudar o R$19,90 (decisão só do Léo/Davi) tem que dizer o efeito nos assinantes atuais: no Play quem não aceitar o aumento cai; uma redução não se desfaz. Reforça que preço não é teste barato.
- Fonte: https://www.revenuecat.com/blog/growth/app-store-vs-web-pricing

## 24/11/2026 · RevenueCat: paywall em várias telas (multi-step)
- Na base da RevenueCat, paywalls de várias telas convertem 5,2% das visualizações contra 2,7% dos de uma tela (mediana, apps diferentes, correlação e não teste); 77% dos apps que usam os dois tipos viram mais conversão no de várias telas. Métrica recomendada: receita por usuário **depois de reembolso**, não conversão bruta. A RevenueCat ainda não mostra conversão por etapa: precisa de evento próprio [ESP].
- **O que muda pra nós:** é candidata a teste do paywall do MinhaMoto só depois de existir `paywall_view` (D-20261126-produto-2) e com OK do Léo/Davi; uma variável, 50/50. Os exemplos do artigo são quase todos com teste grátis: copiar o formato, nunca a promessa.
- Fonte: https://www.revenuecat.com/blog/growth/multi-step-paywall

## 19/11/2026 · RevenueCat: onboarding mais curto aumentou conclusão e reduziu início de teste
- Teste com 24 mil usuários (app Everlove): menos telas = mais gente terminando o onboarding, mas menos gente começando o teste.
- **O que muda pra nós:** ao mexer no onboarding do MinhaMoto, a métrica principal é paywall visto → assinatura, não "terminou o onboarding".
- Fonte: https://www.revenuecat.com/blog/growth/everlove-onboarding-experiment (link exato conferido em 27/11)

## 17/11/2026 · RevenueCat: entregar valor antes do paywall
- Artigo defende definir o "valor" do app antes de decidir onde fica o paywall.
- **O que muda pra nós:** reforça a tese do plano da moto antes do paywall (proposta já aprovada como teste depois da 1ª leitura do funil).
- Fonte: https://www.revenuecat.com/blog/growth/app-value-paywall (link exato conferido em 27/11; o artigo lembra que tráfego pago pede sinal de conversão rápido)

## 04/11/2026 · Apple: mensagens de retenção para assinaturas
- Configuração no App Store Connect de mensagem mostrada no fluxo de cancelamento; API sob pedido.
- **O que muda pra nós:** proposta de mensagem de retenção do MinhaMoto (Stark redige, Léo aprova).
- Fonte: https://developer.apple.com/news/

## 02/11/2026 · Apple: novos descritores de classificação etária (prazo 12/01/2027)
- Declarar "localização compartilhada" e "namoro e relacionamentos"; Brasil com regras A16/A18.
- Fonte: https://developer.apple.com/news/

## 16/10/2026 · Apple: diretriz 2.3.14 (criativos da App Store sem preço) · buraco da janela
- Diretriz nova: criativos do topo da página e da busca não podem ter "preço específico ou com desconto", nem alegação que não dá pra verificar, nem referência a outro app pra enganar.
- **O que muda pra nós:** já é regra da casa (DESIGN-MINHAMOTO, 24/11). Vale também pra qualquer asset que o Produto proponha pra página da loja.
- Fonte: https://developer.apple.com/news/?id=92th7e5i e https://developer.apple.com/app-store/review/guidelines/

## 16/10/2026 · Apple: diretriz 2.5.19 proíbe recurso escondido ou não documentado
- **O que muda pra nós:** o botão de teste de aviso (`VITE_MM_AVISO_TESTE`) não pode ir pra versão pública.
- Fonte: https://developer.apple.com/news/

## 30/09/2026 · Google: verificação de desenvolvedor Android passa a valer no Brasil · buraco da janela
- Desde 30/09/2026, apps instalados em Android certificado no Brasil (e Indonésia, Singapura, Tailândia) precisam estar registrados por desenvolvedor verificado. Segundo o Google, 99% dos apps do Play foram registrados automaticamente; os que faltarem aparecem na página inicial do Play Console, sob risco de remoção global.
- **O que muda pra nós:** risco de conta/loja. Alguém com acesso (Léo/Davi) confere uma vez no Play Console se o MinhaMoto está registrado. Sem custo, 1 minuto.
- Fonte: https://developer.android.com/distribute/play-policies

## 29/09/2026 · Google Play: recursos novos de assinatura · buraco da janela
- Blog oficial: API de mensagem no app pra corrigir pagamento recusado e avisar mudança de preço (disponível), carência dinâmica por assinante, ofertas de retenção e troca de plano no fluxo de cancelamento do Play, ofertas de volta pra quem saiu, novas tentativas de cobrança automáticas. Vários em acesso antecipado.
- **O que muda pra nós:** no Android o erro de cobrança é a maior fatia de cancelamento (31% no Play pela RevenueCat 2026). Proposta pro Davi (sim/não): ligar carência e a mensagem de pagamento recusado no Android. Não mexe no paywall.
- Fonte: https://android-developers.googleblog.com/2026/09/unlocking-Google-play-subscription-growth.html

## 17/09/2026 · Apple: HIG de compra no app revisado · buraco da janela
- A página "Apple In-App Purchase" do HIG foi revisada (registro de mudanças: 17/09/2026). Lista o que a tela de assinatura tem que ter: nome, duração e o que a assinatura dá; valor cobrado localizado; jeito de entrar/restaurar; links de Termos e Privacidade no app e na loja; não mexer na folha de confirmação do sistema; cancelar tem que ser fácil.
- **O que muda pra nós:** virou o checklist da tela que cobra na aula de 27/11. A versão .md abre mesmo quando a página normal fica bloqueada.
- Fonte: https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase.md

## 16/09/2026 · Apple: assinaturas no iOS 27
- Pacotes de assinaturas (Bundles and Suites), compra multiusuário ligada por padrão, StoreKit 2 recomendado.
- Fonte: https://developer.apple.com/news/

## 31/08/2026 · Google Play: API 36 obrigatória para novas versões
- Conferir `targetSdk` antes de cada envio Android (prazo e extensão na página oficial).
- Fonte: https://developer.android.com/google/play/requirements/target-sdk
