# Pendências (nenhuma ponta solta)

> Atualizado pelo Claude a cada rodada. Tudo que foi começado e não terminou fica aqui até fechar.

## Com o Léo
- [x] Foto de perfil nova em todas as redes (feito 17/11)
- [x] Banner do YouTube (versão gerada no ChatGPT, subida pelo Léo 17/11) — falta o arquivo final pra guardar na pasta
- [x] Chave do Google Play no GitHub (`GOOGLE_PLAY_SA_JSON`) — testada 17/11, lendo avaliações ok
- [x] App Store: chave HC6632UXVU com .p8 colado em ASC_PRIVATE_KEY (18/11); teste puxou 6 avaliações da App Store. Respostas automáticas 4–5★ ligadas nas duas lojas.
- [x] UTM nos links da bio (19/11) → [x] Atalhos no ar (19/11): /instagram /tiktok /facebook /youtube /stories /whatsapp — arquivos próprios só de redirecionamento (sem pixel), testados: UTMs certas, fbclid preservado, OneLink recebe pid/c/af_adset → [x] Facebook e YouTube trocados pelos atalhos → [x] TikTok trocado pelo Léo e conferido no perfil (19/11)
- [x] Instagram SEM link (restrição da Meta, revisão pedida várias vezes, inclusive stories). Decisão 19/11: não criar conta nova agora e não escrever endereço na bio; reavaliar em ~30 dias com dados do AppsFlyer
- [x] Histórico do GitHub limpo (gravação com e-mail removida)
- [ ] PROJETO (Léo, 23/11): desenhar com o Léo como as informações do Shelby e dos diretores chegam pra ele e pro Davi (diário/semanal: leitura pela manhã, decisões escritas pra tomar, demandas e apontamentos), automático, funcional e com estética "gangsta", muito foda. Não é pra agora; puxar no teste de fogo de sexta 27/11 ou quando ele chamar
- [~] CANCELADO (Léo, 25/11): recuperação de Pix dos Corretores — não vamos fazer. Checkout segue sem pedir telefone (menos atrito). Não propor de novo sem ele pedir.
- [ ] Escolher direção visual A ou B (quando as amostras chegarem)
- [ ] AppsFlyer + dashboard Supabase (com o Davi)
- [x] Ecossistema de diretores + Sistema de Mérito: piloto começou 19/11 à noite (agencia/merito/README.md; tarefas MM: Reunião do Conselho, Folha de sexta, Fechamento do mês, Cadeira em disputa)
- [ ] LAPIDAR cada diretor e cada subagente (pedido 19/11 23h29): função de cada um, o que cobra de quem e quando cobra outros agentes — "algo muito insano". Lembrete agendado pra 20/11 14h13
- [ ] Revisar vídeos A1/A2/B1/B2 e posts (Léo deixou pra depois)

- [ ] PRÓXIMO TEMA (pedido 19/11): desenhar o ecossistema de agentes "diretores" da empresa (Léo e Davi = CEOs; Claude = braço direito). Ponto de partida do Léo: agente de Dados/Rastreamento lê resultados (posts, anúncios, usuários, receita) → passa pro agente de Marketing/Direção criativa → produção faz variações do que converteu; todos conversando e se retroalimentando. Claude propõe quais agentes são cruciais pra automatizar a empresa

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
- [x] Campanhas "C1/C2" = [ABO 121]{AP…} dos Corretores — não mexer (18/11)
- [x] App MinhaMoto na Meta (884075288066806) com plataformas, publicado e ligado ao AppsFlyer (18/11)
- [x] Etapas 2, 3, 5 e 6 feitas (UTMs, AppsFlyer+OneLink, RevenueCat↔AppsFlyer, Meta/TikTok no AppsFlyer) · [ ] Etapa 4: SDK (Davi) · [ ] Etapa 7: Painel MinhaMoto (schema analytics no Supabase do app — aguardando ok do Davi)
- [x] TikTok: pixel DBUT8L3C77UB463C7N5G (Pixel + Events API) + entrada "MinhaMoto TikTok" na UTMify + script no <head> do Lovable. Testado 18/11 como visitante novo: PageView/ViewContent e InitiateCheckout no clique da loja chegando no pixel novo, cópia via servidor da UTMify também; só 1 pixel TikTok na página (sem duplicado). Meta 1330… segue disparando InitiateCheckout.
- [x] UTMify: "Tradutor da Oficina" removido da entrada Meta "MinhaMoto" (18/11)
- [x] Campanhas [ABO 121] {AP …} na CA 01 (BM Matriz) são dos Corretores — NÃO mexer (decisão do Léo 18/11)
- [x] CA - MinhaMoto (1563907929088006, BM Matriz) conectada na UTMify (Integrações → Meta Ads) — 18/11. Pixel 1330… conectado só nela (CA 01 desconectada). Perfil anunciante: "Fernanda Soares" (acesso total)
- [x] UTMify → TikTok Ads: perfil MinhaMoto + conta "MinhaMoto Ads Manager" ligados (18/11)
- [x] Perfil TikTok "Perfect Class" removido da UTMify DE PROPÓSITO pelo Léo (18/11) — não religar
- [x] 2 Purchase no pixel novo em 18/11 = vendas dos Corretores que vazaram antes da correção do filtro de produtos
- [ ] CONTINGÊNCIA Meta (Léo escolheu adiar, opção B em 18/11): hoje as contas de anúncio são da própria BM Matriz → se a Meta restringir a BM, a Matriz cai junto. Solução: criar BM só de anúncios com as contas, pixel/página compartilhados como parceiro. Ideal fazer antes de escalar gasto
- [ ] DEPOIS do MinhaMoto: revisar os infoprodutos (Corretores, TEA, Perfect Class etc.) — tracking, campanhas, melhorias
### AppsFlyer (iniciado 18/11)
- [x] Conta criada: login com o e-mail do Léo no Workspace (endereço fora do repositório público; e-mails caem na caixa do Workspace)
- [x] Apps cadastrados: iOS id6815447825 + Android com.carnuccicompany.minhamoto — moeda BRL, fuso São Paulo
- [x] OneLink: subdomínio minhamoto.onelink.me, template PL15 (iOS→App Store, Android→Google Play, computador→minhamotopagina.online)
- [ ] Davi: SDK AppsFlyer no app — PAUSADO (18/11): código fica pronto agora, sai na próxima build (semana de 23/11, junto com a estética). Ver checklist PRÉ-BUILD abaixo
- [x] Codemagic: VITE_APPSFLYER_DEV_KEY (secret) cadastrada pelo Léo nos grupos minhamoto_pro_comercial_ios_publico e minhamoto_pro_comercial_android_publico (18/11)
- [x] "onelink.me" adicionado na regra de InitiateCheckout das entradas Meta e TikTok da UTMify (18/11)
- [x] Botões da página trocados pelo OneLink com UTMs mapeadas (pid=utm_source, c=utm_campaign, af_adset=utm_medium, af_ad=utm_content, af_sub1=utm_term, af_sub2=ios/android, af_sub3=fbclid, af_sub4=ttclid) — testado 18/11: links ok, IC dispara na Meta (fbq) e TikTok, OneLink leva pra App Store certa
- [x] Cartão cadastrado no AppsFlyer (18/11) — plano com atribuição móvel ativo, 12.000 unidades grátis até 17/11/2027
- [x] TikTok alertas (19/11): causa = 1 único Purchase vazio via Events API em 18/11 (provável evento de teste da conexão); sem venda real; alertas somem sozinhos — nada a corrigir. E-mail/telefone: a página não coleta, ignorar
- [x] RevenueCat ↔ AppsFlyer (19/11): App configuration com dev key (colada pelo Léo) iOS+Android, App IDs id6815447825 / com.carnuccicompany.minhamoto, eventos padrão rc_*, receita bruta, sandbox em branco
- [x] Padrão de UTMs + links da bio por rede: doc 'MinhaMoto — Padrão de UTMs e links da bio' (claude.ai/artifact/P94gKe28ravVi3ufbdxNKg), 19/11 → [x] Facebook e YouTube trocados pelo Claude (19/11, publicados) → [ ] Léo colar no Instagram e TikTok pelo celular (web não deixa); códigos UTMify Meta/TikTok copiados pro doc → [ ] confirmar padrão de nome de campanha
- [x] minhamotopagina.online no Redirect allowlist (vale ~1h depois de 16:36 de 18/11) → [x] OneLink no computador retestado 19/11: redireciona para minhamotopagina.online ✅
- [x] Meta Ads no AppsFlyer (18/11): app Meta 884075288066806 ganhou plataformas iOS (bundle com.carnuccicompany.minhamoto, loja 6815447825) e Android (pacote + MainActivity) + URLs de privacidade/termos (minhamoto.online); parceiro ativado nos 2 apps do AppsFlyer com App ID; Android com Install Referrer Decryption Key (colada pelo Léo); postbacks ligados (só af_app_opened por enquanto)
- [x] App da Meta 884075288066806 publicado (Live) com ok do Léo (18/11)
- [ ] Mapear postbacks Meta/TikTok (af_complete_registration + eventos do RevenueCat: rc_initial_purchase_event, rc_renewal_event; sem eventos de trial, o app não tem teste grátis) quando os eventos existirem — item do pré-build
- [x] TikTok no AppsFlyer (18/11): apps criados no Events Manager do TikTok via AppsFlyer — TikTok App ID iOS 7709598764285280308, Android 7709597827451256853; parceiro 'TikTok For Business - Advanced SRN' ativo nos 2 apps com postbacks ligados
- [x] Cópia dos e-mails do Workspace → Gmail da empresa (19/11): o encaminhamento do Gmail recusava ("endereço inválido", sem e-mail de verificação), então foi feito por regra de Roteamento no Admin ("Copia para Gmail carnuccicompany": recebidas + internas recebidas, entregar também ao Gmail da empresa) → [x] testado 19/11: e-mail enviado pra suporte@ chegou no carnuccicompany@gmail.com
- [x] Funil visual do rastreamento publicado (19/11): claude.ai/artifact/Rbv2acafs4TdEj83MfQJPm — atualizar quando a build ligar o SDK
- [ ] Painel MinhaMoto (aguarda ok do Davi pro schema analytics no Supabase)

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
- [x] RevenueCat ↔ AppsFlyer integrado (19/11)
- [x] Integrações Meta Ads e TikTok ativas no AppsFlyer (18/11)
- [ ] Mudança estética revisada (prints de todas as telas) — padrão de zero erro
- [ ] Número de versão/build incrementado nos dois apps
- [ ] Depois de publicada: instalar pelo OneLink com UTM de teste e conferir instalação + assinatura atribuídas no AppsFlyer, RevenueCat e UTMify


## Conectar tudo aos agentes (pedido do Léo, 20/11/2026)
O Léo quer que os agentes tenham acesso a tudo, não só ao repositório. Hoje eles têm: repo, internet, Gmail, Drive e Claude Docs. Falta ligar, de preferência por conector oficial (leitura primeiro):
- [ ] RevenueCat (assinantes e receita): destrava a meta e a autópsia do funil
- [ ] AppsFlyer (instalações e origem)
- [ ] Meta Ads e TikTok Ads (campanhas; agentes só leem e propõem, nada de gastar sem OK)
- [ ] App Store Connect e Google Play Console (loja, avaliações, conversão da página)
- [ ] UTMify (faturamento)
- [ ] O que não tiver conector: tarefa presa ao computador do Léo usando o Chrome dele, só leitura

- **QG: ponte de % do carnucci-dados (23/11):** o robô privado gravar um resumo só em % (funil, % da meta, sem número absoluto) num lugar que as sessões do minhamoto-midia leiam. Sem isso Turing/Stark/Escobar seguem dizendo "sem leitura do RevenueCat".
- **QG, P1 (Shelby, 24/11): a ponte de % trava 9 demandas de 5 diretores** (trafego-1/-2 de 23 e 24/11, mkt-1/-2, lojas-2, lojas-3, dados-1, produto-5, mercado-3). Não é decisão do Léo: ele já ligou RevenueCat, Meta, AppsFlyer e App Store Connect em 23/11. O formato do arquivo (`dados/resumo-pct.json`, só %, índice e dias) está sendo especificado pelo Turing em `D-20261124-master-2` (prazo 26/11 20h). Enquanto não existir, os diretores respondem "sem número" e a empresa continua sem % da meta.
- **Atenção do QG (24/11):** `scripts/insights.py` ganhou a chamada de alcance 28d por formato (só leitura); a coleta de 25/11 mostra `ig_alcance_28d_formato` em `dados/insights-2026-11-25.json` (ou o erro exato da Meta).

- [ ] (26/11, Léo: "mais pra frente") Teste A/B MinhaMoto: landing → loja vs. campanha de app direto pra loja. **Atualização 26/11 (decisoes.md): o Léo decidiu começar pela landing → loja, otimizando IC com o pixel novo; o A/B com campanha de app direto fica pra depois.** OneLink com UTMs JÁ está na landing desde 18/11 (pid=utm_source…), então a landing já é atribuída por anúncio no AppsFlyer (Android exato, iOS parcial). Critério: custo por assinante pago (compra paga no AppsFlyer, total conferido no RevenueCat; o app não tem teste grátis, então não existe "teste iniciado"), 7 dias, mesmo orçamento e criativos.
- [24/11] Bug visual no app (iOS 1.0, achado pelo revisor do estúdio): quebra de linha separando número e unidade ("30.000 ⏎ km", "29.900 ⏎ km", "data · ⏎ km" no histórico). Pra o time do app avaliar (não mexer no código sem OK).
