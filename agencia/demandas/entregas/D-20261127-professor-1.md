# D-20261127-professor-1 (Stark, 27/11): proteger o paywall de 2 riscos de loja

De: Tony Stark (Produto) · Cópia: Bezos (Lojas), Shelby · Código lido: minhamotooficial, commit d4942b2 (25/11/2026), versionName 1.0.2 (android/app/build.gradle:49). `git log` rodado hoje. Nada foi alterado no app.
Ligação com venda: paywall que mostra "dias grátis" sem ninguém decidir quebra a decisão do Léo e vira anúncio, loja e tela dizendo coisas diferentes. Paywall que tira o período pra obedecer "nunca por mês" arrisca rejeição na loja e a primeira assinatura do tráfego pago. Nenhuma das duas mexe em preço, planos ou ordem.
Fonte "oficial": as páginas da Apple e do Google abaixo foram lidas pelo professor em 27/11 (aula 2026-11-27-paywall-pago-direto.md, §5). Hoje a minha leitura direta dessas duas páginas foi bloqueada pelo ambiente; o que está aqui sobre elas vem da aula e não foi relido por mim. O que eu mesmo conferi hoje é o código.

## O que eu conferi no código (premissa da demanda: confere)
1. **O paywall liga "dias grátis" sozinho.** `testeGratisComum(pacotes)` lê a oferta introdutória que a loja confirma em todos os planos (pro-producao-checkout.tsx:166-167; função em src/lib/funil-assinatura.ts, comentário na linha 105: "oferta introdutória gratuita do iOS", e Android lê `freeTrialDetails`, indicacoes-google.server.ts:121-122). O valor vai ao componente em pro-producao-checkout.tsx:510 e aparece em paywall-minhamoto.tsx:
   - :489 "{N} dias grátis"
   - :586 botão "Começar {N} dias grátis"
   - :501 palavra "depois" ao lado do preço
   - :597 "Nada é cobrado hoje. Renovação ..." (achado novo, além dos dois da demanda)
   Basta uma oferta introdutória ligada na App Store Connect ou no Play Console, sem mudar uma linha de código, e o app passa a mostrar teste grátis. Hoje isso só acontece se houver oferta ligada: não tenho como ver o console, só o Davi vê.
2. **O paywall já cumpre o que as lojas exigem.** Valor cobrado em destaque (`precoPrincipal="total"`, pro-producao-checkout.tsx:504; unidade "/mês", "/3 meses", "/6 meses", "/ano" em paywall-minhamoto.tsx:120), renovação automática por plano e "Cancele pela loja" (paywall-minhamoto.tsx:95-106), Restaurar compras, Termos e Privacidade (paywall-minhamoto.tsx:617-629). O plano pré-selecionado é o mensal (pro-producao-checkout.tsx:503).
3. **Risco 2 não é do código, é de regra.** Se alguém aplicar o "nunca por mês" (decisoes.md, 24/11, escopo "anúncio, post e vídeo") dentro da tela que cobra ou na descrição da assinatura na loja, o app perde a duração e a renovação que a Apple (3.1.2(c) e a página de assinaturas) e o Google (política de assinaturas) exigem. A decisão de 24/11 não diz onde vale; está escrito só pra mídia.

## Já resolvido antes? Conferido
decisoes.md e cadastro/itens.json não têm nada sobre oferta introdutória nas lojas nem sobre a exceção do "/mês" dentro da tela que cobra. Não é pergunta repetida. A decisão de 22/11 "sem teste grátis" é o que a pergunta 1 protege.

## PERGUNTA 1 · Davi (sim/não)
Você confere no App Store Connect e no Play Console que **nenhum produto de assinatura tem oferta introdutória (teste grátis ou preço de entrada) ligada**, e mantém assim? Nota: o app 1.0.2 mostra "dias grátis" sozinho se tiver (pro-producao-checkout.tsx:167, paywall-minhamoto.tsx:489 e 586).
**Recomendo: sim.** Custa uma conferência de dois minutos nas duas lojas e protege a decisão do Léo sem mexer em código. Se a resposta for "tem oferta ligada", é P1 pro Léo e a demanda volta pro Shelby.

## PERGUNTA 2 · Léo (sim/não, vai pra decisoes.md)
Registrar que **"nunca por mês" vale só pra anúncio, post e vídeo**, e que **dentro da tela que cobra e na descrição da assinatura na loja ficam a duração e a renovação**, como Apple e Google exigem ("/mês", "Renovação mensal automática")?
**Recomendo: sim.** Sem isso, qualquer agente que aplicar a regra à tela arrisca rejeição da versão. O que já roda no app não muda; é só marcar o limite da regra. Texto sugerido pra decisoes.md: "27/11 · Léo: 'por mês' continua proibido em anúncio, post e vídeo. Na tela de assinatura do app e na ficha da assinatura nas lojas, duração e renovação ficam, por exigência da Apple e do Google."

## Opcional, só se o Davi quiser (não é pergunta)
Trava no código: ignorar a oferta da loja no paywall (não passar `testeGratisDias`) como segunda camada. É decisão e trabalho do Davi; eu não escrevi nem proponho branch.

## Status
Bloqueada, bloqueio "lider". Fecha quando o Davi responder a 1 e o Léo a 2. O Shelby leva as duas no próximo pacote; até lá, ninguém propõe tirar o período da tela que cobra e ninguém liga oferta introdutória.
