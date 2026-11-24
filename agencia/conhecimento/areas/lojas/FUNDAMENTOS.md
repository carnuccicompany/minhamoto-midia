# Lojas e clientes: fundamentos do especialista sênior

Para: Jeff Bezos (Lojas e Clientes) e Ted Lasso (respostas às avaliações). Leia a seção que toca a tarefa.
Atualizado em 24/11/2026. Antes de propor, leia `NOVIDADES.md`.

## 1. O funil da loja
Impressão na loja → visita à página → download → abertura → cadastro → assinante.
- **Taxa de conversão da página** (visita → download) é o número do ASO. App Store Connect mostra em "App Analytics"; Google Play Console em "Aquisição de usuários".
- Origem da visita: busca, navegação (destaques, categorias), referência (link externo/anúncio). Cada origem converte diferente.
- **Como aplicamos aqui:** toda proposta de ASO diz qual etapa quer mexer e qual a linha de base (iOS já ligado no carnucci-dados; Play quando a permissão de relatórios propagar).

## 2. ASO (otimização da loja)
- **Palavras-chave:** iOS indexa nome (30 caracteres), subtítulo (30) e campo de palavras-chave (100, invisível). Play indexa título, descrição curta e descrição longa. Não repetir palavra entre campos no iOS.
- **Prints e vídeo:** os 3 primeiros prints decidem a maior parte. Legenda de benefício (o que a pessoa ganha) converte mais que tela crua. Mostrar o app real: print que promete o que o app não faz é motivo de rejeição.
- **Ícone:** reconhecível em tamanho pequeno, contraste, sem texto pequeno.
- **Testes:** Apple tem Product Page Optimization (até 3 variações de ícone, prints e vídeo) e Custom Product Pages (páginas para cada anúncio). Google Play tem experimentos de página (ícone, gráfico, prints; descrições em experimentos localizados).
- **Como aplicamos aqui:** teste dos 3 primeiros prints com legenda de benefício nas duas lojas. Página personalizada por ângulo de anúncio quando o tráfego pago do app começar.

## 3. Avaliações e respostas
- Nota e volume de avaliações pesam em conversão e em ranking. Uma nota abaixo de 4 derruba a conversão da página.
- **Pedir avaliação no momento certo:** depois de uma vitória do usuário (ex.: registrou o serviço), nunca depois de erro. iOS: `SKStoreReviewController`/`requestReview`, no máximo 3 vezes em 365 dias por usuário (o sistema decide se mostra). Android: In-App Review API, também com cota.
- **Responder:** 1–2★ com bug: reconhecer, dizer o que foi feito, convidar pro suporte por e-mail. Nunca discutir, nunca pedir dado pessoal em público. Resposta publicada pode fazer o usuário mudar a nota.
- **Como aplicamos aqui:** resposta de 1 a 3★ só com OK do Léo (regra). 4–5★ o Ted responde pelo guia.

## 4. Regras da Apple que mais pegam app de assinatura
- **3.1.1:** conteúdo digital e assinatura dentro do app usam compra dentro do app da Apple (no Brasil, sem link externo de pagamento fora dos programas específicos).
- **3.1.2:** assinatura precisa entregar valor contínuo; a tela de compra mostra preço, período, renovação automática e como cancelar; links de Termos e Privacidade.
- **2.3 (metadados precisos):** nome, prints e descrição batem com o app. Desde 16/10/2026, a nova 2.3.14 proíbe preço específico ou com desconto nos "creative assets" (imagens e vídeos promocionais de busca e topo da página). Ver NOVIDADES.
- **5.1 (privacidade):** política de privacidade, rótulos de privacidade corretos ("nutrition labels"), e o ATT se o app rastreia (o AppsFlyer exige declarar).
- **Faixa etária:** questionário de classificação; desde 2026 o Brasil tem regras próprias (ECA Digital) e a Apple bloqueia download de app 18+ para quem não confirmou ser adulto.

## 5. Regras do Google Play que mais pegam
- **Pagamentos:** compra dentro do app pelo Google Play Billing.
- **Segurança dos dados:** formulário precisa bater com o que o app e os SDKs coletam (AppsFlyer coleta ID de publicidade: declarar e ter a permissão `AD_ID`).
- **Nível de API alvo:** todo ano o Play exige um nível mínimo pra novas versões (em 2026: API 36 até 31/08). Ver NOVIDADES.
- **Classificação de conteúdo:** app sem questionário respondido fica irregular.

## 6. Voz do cliente
- Avaliação é pesquisa de graça: agrupar por tema (bug, pagamento, pedido de recurso, elogio) e por versão do app.
- Reclamação de bug ou cobrança vira demanda pro Stark com o relato; dúvida repetida vira resposta pronta e, se for o caso, ajuste de tela.
- **Como aplicamos aqui:** vigia de avaliações por versão nas 72h depois de cada build.

## 7. O que um sênior faz toda semana
- Lê avaliações novas por estrela e por versão; responde dentro da regra.
- Acompanha conversão da página por origem e por loja.
- Propõe 1 teste de ASO com hipótese e linha de base.
- Confere mudanças de diretriz da Apple e do Google (NOVIDADES).
