# Pendências (nenhuma ponta solta)

> Atualizado pelo Claude a cada rodada. Tudo que foi começado e não terminou fica aqui até fechar.

## Com o Léo
- [x] Foto de perfil nova em todas as redes (feito 17/11)
- [x] Banner do YouTube (versão gerada no ChatGPT, subida pelo Léo 17/11) — falta o arquivo final pra guardar na pasta
- [x] Chave do Google Play no GitHub (`GOOGLE_PLAY_SA_JSON`) — testada 17/11, lendo avaliações ok
- [x] App Store: chave HC6632UXVU com .p8 colado em ASC_PRIVATE_KEY (18/11); teste puxou 6 avaliações da App Store. Respostas automáticas 4–5★ ligadas nas duas lojas.
- [ ] Ok pra colocar UTM no link da bio de cada rede (página de vendas com ?utm_source=…)
- [x] Histórico do GitHub limpo (gravação com e-mail removida)
- [ ] Escolher direção visual A ou B (quando as amostras chegarem)
- [ ] AppsFlyer + dashboard Supabase (com o Davi)

## Com o Davi
- [ ] SDK AppsFlyer: implementar agora SEM build (prompt + adendo enviados ao Léo 18/11); mandar resumo de volta pro Claude revisar
- [ ] Pedido de avaliação dentro do app (atualização seguinte à de 16/11)
- [ ] Investigar 2 avaliações 1★ no Google Play: "não abre" / "baixei mas não funciona"

## Claude (em andamento / próximo)
- [~] Direção criativa v2 — amostras A/B (em segundo plano)
- [x] Respostas às avaliações no Google Play: guia aprovado, 5 primeiras publicadas, tarefa automática 9h/13h/17h/21h (4–5★ automático, 1–3★ rascunho pro Léo). App Store ligada em 18/11.
- [x] Auditoria da YouTube Data API enviada em 18/11 (projeto 644425422292, videos.insert 10/dia, ferramenta interna). Aguardando resposta por e-mail (Vigia do Gmail avisa). Script completo de envio pronto em scripts/youtube.py (modo enviar) — NÃO rodar antes da aprovação (vídeo enviado antes fica privado pra sempre). Depois: workflow agendado + fila/shorts.json + trocar YT_CLIENT_SECRET.
- [ ] Publicador de vídeos/stories + YouTube Shorts (após aprovar direção)
- [ ] Carrossel aprovado → vídeo automático
- [ ] Religar produção diária (após aprovar direção)
- [ ] Lembrar: pedido de avaliação dentro do app entra na atualização seguinte

## Rastreamento (iniciado 18/11) — checklist sem ponta solta
- [x] Diagnóstico: Pixel MinhaMoto antigo (4034047696896725) recebia 247 "Compras" do imobiliário via UTMify ("Produto: Qualquer"). Corrigido 18/11: Corretores = só produtos imobiliários; MinhaMoto = só produtos MinhaMoto. MedHub segue "Qualquer" (Léo: deixar pra lá).
- [x] Pixel NOVO "Pixel MinhaMoto Novo" (1330115822529036) na BM 01 - Matriz, ligado à CA - MinhaMoto (1563907929088006) — 18/11
- [x] Página no Lovable NÃO precisa mudar pro Meta (pixel vem do script da UTMify). Falta: pixel do TikTok (UTMify tikTokPixelIds vazio) e conferir no Gerenciador de Eventos os eventos chegando no 1330… (pode levar até 30 min)
- [x] UTMify: entrada "MinhaMoto" (6a8638795f6e933acd7b7166) aponta pro pixel novo + CAPI; IC por URL (apps.apple.com / play.google.com). Testado 18/11: visitante novo dispara PageView, ViewContent e InitiateCheckout no pixel novo. Visitante que já tinha visitado mantém o pixel antigo em cache (localStorage "lead") até a UTMify renovar — ok.
- [ ] Conferir campanhas C1/C2 (10 conjuntos otimizando em Compra do pixel antigo): são do imobiliário? Migrar pro Pixel Corretores
- [ ] App MinhaMoto na Meta (dataset de app 884075288066806) — usar na etapa 6 (eventos do app via AppsFlyer)
- [ ] Etapa 2: padrão de UTMs · Etapa 3: AppsFlyer (plano Growth, 12 mil conversões grátis 1º ano) + OneLink · Etapa 4: SDK (Davi) · Etapa 5: RevenueCat↔AppsFlyer · Etapa 6: postbacks Meta/TikTok · Etapa 7: Painel MinhaMoto (schema analytics no Supabase do app — aguardando ok do Davi)
- [x] TikTok: pixel DBUT8L3C77UB463C7N5G (Pixel + Events API) + entrada "MinhaMoto TikTok" na UTMify + script no <head> do Lovable. Testado 18/11 como visitante novo: PageView/ViewContent e InitiateCheckout no clique da loja chegando no pixel novo, cópia via servidor da UTMify também; só 1 pixel TikTok na página (sem duplicado). Meta 1330… segue disparando InitiateCheckout.
- [x] UTMify: "Tradutor da Oficina" removido da entrada Meta "MinhaMoto" (18/11)
- [x] Campanhas [ABO 121] {AP …} na CA 01 (BM Matriz) são dos Corretores — NÃO mexer (decisão do Léo 18/11)
- [x] CA - MinhaMoto (1563907929088006, BM Matriz) conectada na UTMify (Integrações → Meta Ads) — 18/11. Pixel 1330… conectado só nela (CA 01 desconectada). Perfil anunciante: "Fernanda Soares" (acesso total)
- [x] UTMify → TikTok Ads: perfil MinhaMoto + conta "MinhaMoto Ads Manager" ligados (18/11)
- [x] Perfil TikTok "Perfect Class" removido da UTMify DE PROPÓSITO pelo Léo (18/11) — não religar
- [ ] Pixel Meta novo recebeu 2 Purchase via API de Conversões (~13h de 18/11) — confirmar com o Léo se foram testes ou vendas reais
- [ ] CONTINGÊNCIA Meta (Léo escolheu adiar, opção B em 18/11): hoje as contas de anúncio são da própria BM Matriz → se a Meta restringir a BM, a Matriz cai junto. Solução: criar BM só de anúncios com as contas, pixel/página compartilhados como parceiro. Ideal fazer antes de escalar gasto
- [ ] DEPOIS do MinhaMoto: revisar os infoprodutos (Corretores, TEA, Perfect Class etc.) — tracking, campanhas, melhorias
### AppsFlyer (iniciado 18/11)
- [x] Conta criada: login leonardo@carnucci.com (alias do usuário carnucci@carnucci.com no Workspace; e-mails caem na caixa do Workspace)
- [x] Apps cadastrados: iOS id6815447825 + Android com.carnuccicompany.minhamoto — moeda BRL, fuso São Paulo
- [x] OneLink: subdomínio minhamoto.onelink.me, template PL15 (iOS→App Store, Android→Google Play, computador→minhamotopagina.online)
- [ ] Davi: SDK AppsFlyer no app — PAUSADO (18/11): código fica pronto agora, sai na próxima build (semana de 23/11, junto com a estética). Ver checklist PRÉ-BUILD abaixo
- [x] Codemagic: VITE_APPSFLYER_DEV_KEY (secret) cadastrada pelo Léo nos grupos minhamoto_pro_comercial_ios_publico e minhamoto_pro_comercial_android_publico (18/11)
- [x] "onelink.me" adicionado na regra de InitiateCheckout das entradas Meta e TikTok da UTMify (18/11)
- [x] Botões da página trocados pelo OneLink com UTMs mapeadas (pid=utm_source, c=utm_campaign, af_adset=utm_medium, af_ad=utm_content, af_sub1=utm_term, af_sub2=ios/android, af_sub3=fbclid, af_sub4=ttclid) — testado 18/11: links ok, IC dispara na Meta (fbq) e TikTok, OneLink leva pra App Store certa
- [x] Cartão cadastrado no AppsFlyer (18/11) — plano com atribuição móvel ativo, 12.000 unidades grátis até 17/11/2027
- [x] minhamotopagina.online no Redirect allowlist (vale ~1h depois de 16:36 de 18/11) → [ ] retestar OneLink no computador
- [x] Meta Ads no AppsFlyer (18/11): app Meta 884075288066806 ganhou plataformas iOS (bundle com.carnuccicompany.minhamoto, loja 6815447825) e Android (pacote + MainActivity) + URLs de privacidade/termos (minhamoto.online); parceiro ativado nos 2 apps do AppsFlyer com App ID; Android com Install Referrer Decryption Key (colada pelo Léo); postbacks ligados (só af_app_opened por enquanto)
- [x] App da Meta 884075288066806 publicado (Live) com ok do Léo (18/11)
- [ ] Mapear postbacks Meta/TikTok (af_complete_registration, af_start_trial, af_subscribe) quando os eventos existirem — item do pré-build
- [x] TikTok no AppsFlyer (18/11): apps criados no Events Manager do TikTok via AppsFlyer — TikTok App ID iOS 7709598764285280308, Android 7709597827451256853; parceiro 'TikTok For Business - Advanced SRN' ativo nos 2 apps com postbacks ligados
- [ ] Encaminhamento automático do Workspace (carnucci@carnucci.com) → carnuccicompany@gmail.com, pra Claude acompanhar e-mails (Léo autorizou a ideia; confirmar)
- [ ] Ao terminar: funil visual explicando o rastreamento (o que cada peça faz) + Painel MinhaMoto

## ✅ CHECKLIST PRÉ-BUILD (próxima versão — estética + AppsFlyer, prevista semana de 23/11)
Claude revisa item a item com o Léo ANTES de disparar a build. Nada sobe sem isso.
- [ ] Resumo do Claude Code do Davi revisado pelo Claude (SDK: init com dev key via env, appID 6815447825, setCustomerUserId = mesmo ID do Purchases.logIn, AppsFlyer ID → RevenueCat antes de qualquer compra, af_complete_registration no cadastro, permissão AD_ID no Android)
- [ ] .env fora do Git (.gitignore) e removido do repositório
- [ ] Teste em debug feito: instalação aparece no AppsFlyer (SDK Integration Tests)
- [ ] codemagic.yaml: workflows públicos (iOS e Android) usam os grupos minhamoto_pro_comercial_*_publico (onde está a VITE_APPSFLYER_DEV_KEY)
- [ ] codemagic.yaml: REMOVER VITE_MM_AVISO_TESTE: "1" (botão "Testar aviso em 1 minuto" não pode ir pra versão pública)
- [x] Android também sai pelo Codemagic (workflow com bundleRelease no codemagic.yaml) — confirmar só que usa o grupo android_publico
- [ ] Mapear postbacks de eventos na Meta e TikTok (AppsFlyer → Integrações de parceiros)
- [x] App da Meta publicado (Live)
- [ ] RevenueCat ↔ AppsFlyer integrado (dev key colada pelo Léo no RevenueCat)
- [ ] Integrações Meta Ads e TikTok ativas no AppsFlyer
- [ ] Mudança estética revisada (prints de todas as telas) — padrão de zero erro
- [ ] Número de versão/build incrementado nos dois apps
- [ ] Depois de publicada: instalar pelo OneLink com UTM de teste e conferir instalação + assinatura atribuídas no AppsFlyer, RevenueCat e UTMify
