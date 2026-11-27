# Lojas: novidades (últimos 90 dias)

Janela: 29/08/2026 a 27/11/2026. Pesquisado em 27/11/2026 (antes: 24/11). Mais novo em cima.

## 27/11/2026 · Conferência de prazos de loja (professor-chefe)
- **Apple, classificação etária (novos descritores):** prazo **12/01/2027 = 46 dias** a partir de hoje; passa a menos de 45 dias amanhã (28/11). **Sem dono registrado:** nenhuma demanda nem linha em decisoes.md (grep em demandas/, memoria/, diretoria/). O código do app (minhamotooficial, só leitura) não pede localização no Android nem no iOS: a resposta provável a "localização compartilhada" e "namoro" é **não**, mas quem responde no App Store Connect é Léo/Davi.
- **Google Play, target SDK:** o `main` do app já declara `targetSdkVersion = 36` (minhamotooficial/android/variables.gradle, só leitura); falta o Davi confirmar que a build publicada saiu desse commit. Nenhum prazo novo de API alvo publicado (página de prazos lida hoje).
- **ECA Digital:** fiscalização da ANPD a partir de **janeiro/2027** (sem dia marcado), ver entrada de 09/10 abaixo.
- **Verificação de desenvolvedor Android (Brasil, 30/09/2026):** ver entrada abaixo; conferir na Home do Play Console.
- Fontes checadas hoje: https://developer.apple.com/news/ · https://developer.apple.com/news/?id=yxkh08us · https://developer.android.com/distribute/play-policies · https://developer.android.com/developer-verification · https://www.gov.br/anpd/pt-br/assuntos/eca-digital · App Review Guidelines (nenhuma revisão depois de 16/10/2026 encontrada). Bloqueadas no WebFetch hoje: support.google.com/googleplay/android-developer/answer/11926878 e developer.android.com/google/play/requirements/target-sdk (a conferir).

## 27/11/2026 · Google Play: políticas com prazo em 27/01/2027
- Na página de prazos: assinaturas com desconto por elegibilidade (ex.: plano estudante) precisam explicar critério, verificação e preço depois; apps que miram Android 17 (API 37+) usam o botão de localização ou declaram localização precisa; contatos amplos com política nova; geofencing sai dos serviços em primeiro plano.
- **O que muda pra nós:** nada hoje (o app não usa localização nem contatos e não tem plano por elegibilidade). Se algum dia houver plano com desconto por grupo, a tela precisa explicar a regra. Data da publicação de cada regra não aparece na página.
- Fonte: https://developer.android.com/distribute/play-policies

## 17/11/2026 · Apple: impostos e preços em alguns países
- Preços mudam em 03/12/2026 em Botswana, Colômbia, Egito, Ruanda e Turquia; imposto da Califórnia em 2027. Assinatura auto-renovável fica fora do ajuste automático.
- **O que muda pra nós:** nada. O Brasil não aparece, e o MinhaMoto é assinatura.
- Fonte: https://developer.apple.com/news/?id=4o5ie73a

## 09/10/2026 · ECA Digital: ANPD marca fiscalização pra janeiro/2027
- Etapa III a partir de jan/2027, com foco em verificação de idade; de novembro/2026 sai a norma de fiscalização e sanções atualizada. Lojas e sistemas operacionais dão sinal de idade por API; o app (art. 14) recebe a faixa etária da loja e bloqueia o que não serve pra idade. Multa até 10% do faturamento no Brasil, teto de R$ 50 milhões por infração.
- **O que muda pra nós:** risco de loja, não de venda. Léo/Davi decidirem até dezembro se o MinhaMoto lê o sinal de idade (Declared Age Range na Apple; equivalente no Play) e se a faixa etária declarada nas duas lojas está certa. Pauta pro Shelby (Jurídico).
- Fontes: https://www.gov.br/anpd/pt-br/assuntos/eca-digital (cronograma oficial, página alterada em 24/11/2026) · https://www.correiobraziliense.com.br/cbradar/lei-15-211-o-eca-digital-preve-multa-de-ate-10-do-faturamento-no-brasil-limitada-a-r-50-milhoes-por-infracao-e-a-anpd-marca-janeiro-de-2027-para-comecar-as-acoes-de-fiscalizacao-com-foco-na-veri/

## 30/09/2026 · Android: verificação de desenvolvedor começa no Brasil
- Desde 30/09/2026, apps instalados de lojas participantes no Brasil (e Indonésia, Singapura, Tailândia), em aparelho certificado Android 8+, precisam ser de desenvolvedor verificado e registrado. O Play registra 99% dos apps sozinho; o resto se registra no Play Console. A página de prazos diz que app não registrado corre risco de remoção global do Google Play. Expansão mundial em 2027.
- **O que muda pra nós:** o Davi confere na Home do Play Console se o MinhaMoto aparece como registrado. Leva 1 minuto e evita sumir da loja.
- Fontes: https://developer.android.com/developer-verification · https://developer.android.com/distribute/play-policies

## 29/09/2026 · Google Play: novos recursos de assinatura
- API de mensagens no app (avisar falha de pagamento e mudança de preço) disponível pra todos; em acesso antecipado: ofertas de retenção no fluxo de cancelamento do Play, troca pra plano mais barato, ofertas de reconquista na própria loja, carência dinâmica depois de pagamento recusado, pacotes entre desenvolvedores.
- **O que muda pra nós:** é o par Android da mensagem de retenção da Apple (04/11). Proposta pro Stark: mensagem de falha de pagamento pela API (sem desconto). Qualquer oferta com desconto mexe em preço: só com OK do Léo.
- Fonte: https://android-developers.googleblog.com/2026/09/unlocking-Google-play-subscription-growth.html

## 04/11/2026 · Apple: mensagens de retenção para assinaturas
- Dá pra configurar no App Store Connect uma mensagem mostrada quando o usuário vai cancelar a assinatura. API de mensagens de retenção sob pedido.
- **O que muda pra nós:** proposta pro Stark e pro Bezos: mensagem de retenção no cancelamento do MinhaMoto (ex.: lembrar a próxima revisão da moto).
- Fonte: https://developer.apple.com/news/

## 02/11/2026 · Apple: novos descritores na classificação etária
- A partir de 16/11/2026, declarar se o app tem "localização compartilhada" e "namoro e relacionamentos". Todos os apps precisam responder até 12/01/2027. O Brasil tem regras próprias (A16 e A18).
- **O que muda pra nós:** responder o questionário de classificação no App Store Connect antes de 12/01/2027. Se o app compartilha localização (posto, rota), marcar. Tarefa do Davi/Léo, com lembrete do Bezos.
- Fonte: https://developer.apple.com/news/ (item: https://developer.apple.com/news/?id=yxkh08us)

## 16/10/2026 · Apple atualiza as diretrizes de revisão
- Nova **2.3.14**: as imagens e vídeos promocionais (topo da página e resultado de busca) não podem ter preço específico nem preço com desconto, nem alegação que não dá pra verificar.
- Nova **2.5.19**: proíbe recurso escondido ou não documentado. App que se mostra diferente na revisão pode ser removido e a conta encerrada.
- Esclarecimentos em 1.2, 3.1.1(a) e 5.
- **O que muda pra nós:** nada de "R$ 19,90" ou "promoção" nos assets promocionais da App Store; preço continua permitido na tela de compra do app. Garante que o botão "Testar aviso em 1 minuto" não vai pra versão pública (2.5.19).
- Fontes: https://developer.apple.com/news/ · https://9to5mac.com/2026/10/16/apples-new-app-store-rules-crack-down-on-ai-nudification-and-bait-and-switch-apps/

## 05/10/2026 · Apple: novos assets na página da App Store
- Novo cabeçalho da página do produto, assets nos resultados de busca, ferramenta de prévia e biblioteca de assets no App Store Connect.
- **O que muda pra nós:** espaço novo pra destacar o MinhaMoto na busca. Respeitar a 2.3.14 (sem preço).
- Fonte: https://developer.apple.com/news/

## 16/09/2026 · Apple: assinaturas no iOS 27 (pacotes e compra por várias pessoas)
- "Bundles and Suites" permitem acesso a várias assinaturas com uma compra; compra multiusuário ligada por padrão; compra em volume para empresas e escolas desde 22/10. Apple recomenda StoreKit 2.
- **O que muda pra nós:** sem ação agora; registrar como ideia pra quando houver segundo app.
- Fonte: https://developer.apple.com/news/

## 31/08/2026 · Google Play: novas versões precisam mirar o Android 16 (API 36)
- Apps novos e atualizações precisam ter `targetSdk` 36; apps existentes precisam de API 35 pra continuar visíveis a novos usuários em versões novas do Android. Havia extensão até 01/11/2026 para quem pediu.
- **O que muda pra nós:** conferir o `targetSdkVersion` da build Android antes do envio (Davi). Confirmar o prazo na página oficial.
- Fontes: https://developer.android.com/google/play/requirements/target-sdk · https://support.google.com/googleplay/android-developer/answer/11926878

> Escopo da 2.3.14 (Léo, 24/11): vale SÓ para os assets promocionais dentro da App Store. Em anúncio (Meta/TikTok), post e vídeo segue a regra da casa: pode "R$19,90", nunca "por mês" (agencia/DESIGN-MINHAMOTO.md).
