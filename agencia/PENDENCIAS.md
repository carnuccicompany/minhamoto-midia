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
