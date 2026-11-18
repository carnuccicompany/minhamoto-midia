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
- [ ] SDK AppsFlyer + ligação com RevenueCat (etapas 4 e 5 do rastreamento)
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
- [ ] Ao terminar: funil visual explicando o rastreamento (o que cada peça faz) + Painel MinhaMoto
