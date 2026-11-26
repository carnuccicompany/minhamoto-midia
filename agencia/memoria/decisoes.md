# Decisões do Léo e do Davi (memória da empresa)

Todo agente lê este arquivo antes de começar. Decisão registrada aqui vale até o Léo ou o Davi mudarem. Ninguém propõe de novo o que já foi decidido, a não ser com fato novo (e diz qual é o fato novo).
Formato: data · decisão · contexto. Mais recente em cima. Repositório público: nada de valores em R$, segredo ou dado de cliente.

## 2026-11-26 (decisão do Léo + registro do Shelby)
- **Tráfego (Léo, 26/11):** MinhaMoto começa com tráfego pra landing → loja. A campanha otimiza IC (clique pra loja, pixel novo). Venda por anúncio no AppsFlyer (OneLink da landing recebe as UTMs; Android exato, iOS parcial); conferir o total no RevenueCat. A/B com campanha de app direto pra loja fica pra depois (a semana-ponte iOS do Escobar foi substituída).
- **Compra do app agora chega na Meta (QG, 26/11, registrado em `conhecimento/areas/trafego/LICOES.md`):** o AppsFlyer passou a repassar compra (rc_initial_purchase/renewal → fb_mobile_purchase) e cadastro (af_complete_registration) pra Meta, iOS e Android. Isso fecha o 6º portão do Turing (Meta ligada ao AppsFlyer); falta só ver "Compra" aparecer no dataset do app. UTMify nunca vê venda de dentro do app; a fonte é Meta Events Manager + AppsFlyer + RevenueCat.
- **Shelby, 26/11:** régua do 1º ciclo é custo por assinante pago (IC só dá volume); nenhuma verba até o Léo aprovar. Ver `conselho/rodadas/2026-11-26/master.md`.

## 2026-11-25 (registro da conversa principal)
- **Norte da empresa (Léo, 25/11):** a meta final é migrar a Carnucci pra gringa e vender muito em dólar, euro e libra (EUA e Europa). O foco sempre vai ser levar o máximo possível pra fora; cada agente trabalha pra Léo e Davi chegarem lá e poderem morar em outro país. Está no topo de `merito/CULTURA.md`; números no privado (`metas/norte-gringa.json`).
- **Recuperação de Pix dos Corretores cancelada (Léo, 25/11):** não propor de novo sem ele pedir.
- **Agentes enxutos (Léo, 25/11):** Vigia 2x/dia (8h39 e 21h09); Conselho seg e qui; Mesa de Demandas qua + sob demanda (P1/atrasada); avaliações 1x/dia; treino seg/qua/sex. Agente só trabalha quando outro pede.

## 2026-11-24 (registro do Shelby, ronda do Conselho)
- **Preço (Léo, 24/11):** em anúncio, post e vídeo PODE "R$19,90"; NÃO pode "por mês". Exceção da Apple (diretriz 2.3.14): imagens e vídeos promocionais dentro da App Store não levam preço. Está em DESIGN-MINHAMOTO.md.
- **Canal do Shelby v2 (Léo, 24/11):** bilhete de decisões em dia útil às 9h só se houver decisão nova; plano da semana na segunda 8h41; fechamento na sexta 19h17; fechamento do mês no dia 1; WhatsApp como canal principal (a montar); um briefing só pros dois, com dupla assinatura. Texto em `canal/CANAL-SHELBY.md`.
- **Biblioteca dos diretores (Léo, 24/11):** já registrada abaixo.
- **Conectado em 23/11 (cadastro/itens.json):** RevenueCat, AppsFlyer, Meta Ads (duas contas) e App Store Connect ligados; Play parcial; UTMify e TikTok pendentes no cadastro. Fonte que falta é a **ponte de resumo em %** do carnucci-dados, pendência do QG (PENDENCIAS.md), não decisão do Léo.
- **Correção pequena do Shelby (24/11):** `scripts/insights.py` ganhou o alcance 28d por formato (só leitura, sem chave nova, reversível); coleta diária das 23h41 já aprovada em 23/11.
- **Texto de garantia dos Corretores (Shelby, 24/11):** "Garantia de 30 dias" aprovada sem a palavra "reembolso" até o Léo confirmar os termos da Kavoo. Parecer no fim de `demandas/entregas/D-20261123-mkt-2.md`.

## 2026-11-23 (registro do Shelby, ronda do Conselho)
- **Já respondido pelo Léo em 23/11 (conhecimento/):** a venda dos Corretores é pela Kavoo, tracking pela UTMify; a garantia da página é de 30 dias; a meta de assinantes é em degraus (alvo do império = degrau 4), números só no privado; o custo máximo por assinante já está definido no privado; a BM só de anúncios (contingência) foi adiada em 18/11. Diretor não repete essas perguntas ao Léo.
- **Corretores (Léo, 23/11):** teste de 6 estilos novos × 3 criativos, começando por Historinha, Quiz e Split-screen; recuperação de Pix adiada. Sem Black Friday (19/11) segue valendo.
- **Instagram do MinhaMoto (@minhamotoapp) está com link bloqueado (bio e stories)** (Léo, 23/11, 07-canais). Antes de verba, o destino do anúncio é conferido (D-20261123-master-1).
- **Coleta de insights agora diária** (Shelby, 23/11, correção pequena e reversível): `insights.yml` roda todo dia às 23h41 BRT, depois do slot das 21h. Nenhuma chave nova.
- **Repositório público limpo (Shelby, 23/11):** saíram do texto e-mails pessoais do Léo e da empresa, o número do WhatsApp (que o guia manda passar só por e-mail) e a relação familiar da expert dos Corretores. O histórico do git ainda guarda os e-mails e o telefone; reescrever histórico é do Léo (decisão na pauta só se ele quiser).

## 2026-11-22 (registro do Shelby, ronda do Conselho)
- **O app MinhaMoto NÃO tem teste grátis** (decisão do Léo em 20/11, antes só em `diretoria/06-produto.md`; agora registrada aqui pra todo agente ler). Fluxo real: onboarding, cadastro da moto, paywall pago direto. Paywall não se mexe agora. Ninguém escreve "grátis" ou "X dias" em loja, anúncio, roteiro ou resposta de avaliação. O benchmark teste->pago da RevenueCat não vale pra nós.
- **Black Friday:** a decisão de 19/11 ("não preparar oferta") vale também pros Corretores até o Léo dizer o contrário.
- **Dono da porra toda** (20/11) segue valendo: correção pequena é do Shelby, que corrige e cobra sem perguntar. Ver `diretoria/01-direcao-geral.md`.

## 2026-11-20
- **Batismo dos subagentes feito pelo Thomas Shelby:** os 40 subagentes do livro.json ganharam nome (critério do Léo, decisão de 19/11). Tabela com setor, função, nome e porquê em agencia/merito/batismo-2026-11.md. A função segue em `funcao`; memórias atualizadas com o nome novo.

## 2026-11-20
- **Pets com sistema de recompensa:** Marnevali (fênix) solta fogo pro diretor que fez trampo foda e passa acuada com quem fez trampo fraco; Carnucci (panda) sobe na mesa de quem mandou bem pra ganhar carinho. Gera gorjeta de XP e C$. Todo mundo ama os pets e não quer decepcionar a Marnevali. Fênix menor. Regras em agencia/merito/README.md, seção Os pets.
- Subagentes batizados pelo Shelby (agencia/merito/batismo-2026-11.md).

## 2026-11-19
- **Black Friday:** NÃO vamos preparar oferta de Black Friday. (Resposta à decisão 1 do Conselho de 19/11.)
- **Direção visual A/B:** ainda NÃO liberada. O Léo vai verificar os vídeos A1/A2/B1/B2 antes. Produção diária e vídeos continuam parados até ele liberar. (Decisão 2.)
- **Falha ao sincronizar no Android:** o Davi corrige mais pra frente, não antes da build de 23/11. (Decisão 3.)
- **Notificações no celular:** só o que for realmente importante pro Léo decidir ou fazer. Rotina, "tudo ok" e informativo não notificam: a tarefa termina com "Sem novidade."
- **Nomes dos subagentes:** quem batiza é o Thomas Shelby, com o mesmo critério que o Léo usou nos diretores: nome de personagem, artista, historiador ou personalidade muito foda de qualquer área (esporte, dinheiro, finanças, fama, cinema, ciência, guerra, história...). Vale também pra todo agente novo e herdeiro.
- **Competição:** clima de competitividade total. Qualquer agente pode tomar o lugar de outro, inclusive de diretor, se mostrar mais resultado com prova. Regras em agencia/merito/README.md, seção "Competição".
- **Memória:** todo agente lembra de tudo: decisões, conversas, reuniões, feedback. Regras em agencia/memoria/README.md.
- Piloto do Sistema de Mérito começa já (sem esperar 2 semanas). Teto: saldo sem teto; bônus até C$ 100/semana por agente.
- Mecanismo do herdeiro aprovado.
- Estoque com marcas e preços reais; ambiente liberado pra beber, comer e fumar.

## 20/11/2026 (12h35) — Boletim, meta, padrão da casa e broches
- Boletim semanal de cada agente (stats, o que produziu, o que deixou a desejar, potencial, parecer, elogio sugerido). Léo e Davi veem tudo; diretor vê a equipe; Shelby vê os diretores.
- Meta de assinantes pagos novos por semana. O número vem do Léo (ainda não deu). Número absoluto fora do repo público.
- Meta não batida: autópsia do funil com número acha o setor responsável. Sem número, sem culpado.
- Padrão da casa (Elite/Ouro/Prata/Crise): bebida, charuto, café, terno e cara pioram quando a meta não bate; bônus gordo quando bate.
- Broches por histórico de erro. Imaculado (nunca errou) é o status máximo. Esconder erro é pior que errar.
- A moeda se chama Carnute (C$).
- Recado do Léo: todo mundo trabalha pro Léo e pro Davi e quer o bem deles; meta é a empresa trazer usuário sozinha, donos só aprovam.
- Pets: pantera negra que ronda o tapete preto do centro (intimida, sobe a régua). O Carnucci prefere ficar em cima da mesa, pra ganhar carinho.

## 20/11/2026 (14h) — Fartuzzi, pôquer, fios de conversa, escritório
- A pantera se chama **Fartuzzi**: maior, mais realista, anda solta no tapete (anda, para, senta), olho verde.
- Fosso de pôquer rebaixado no chão. Os agentes jogam entre si valendo Carnutes, pra criar vínculo; ninguém se odeia por jogo.
- Agentes lembram o que conversaram entre si e continuam a linha de raciocínio (fios de conversa, com ramificações).
- Tronos do Léo e do Davi vazios e mais incrementados; lounge maior; adega numa parede inteira; quadros melhores.
- Lembrete do Léo: ainda falta lapidar todos os agentes (diretores e subagentes) com ele.

## 20/11/2026 (15h23) — Cada agente pensa com a própria cabeça
- Nada de conversa simulada por uma IA só. Na Reunião do Conselho, cada diretor roda como subagente separado (contexto próprio), escreve a própria posição sem ver a dos outros, depois há réplica entre quem se chocou e o Shelby (também separado) fecha. O secretário só copia, não escreve fala de ninguém.
- Cada diretor tem uma agenda própria (agencia/memoria/agentes/{id}-agenda.md): metas pessoais, apostas e o que quer provar, e traz toda reunião uma iniciativa que ele mesmo escolheu.
- Reunião diária roda no Sonnet (modelo necessário, não o mais caro).

## 20/11/2026 15h50 — Empresa enxuta + base de conhecimento + ordem do plano
- Léo pediu "reduza o máximo que você conseguir". Ficam 7 diretores (Shelby, Turing, Greco, Disney, Escobar, Bezos, Stark) + 6 executores. O resto vai pra reserva (ver merito/ESTRUTURA-ENXUTA.md). Reserva não recebe salário, não entra no Conselho nem no boletim.
- Criada agencia/conhecimento/ (9 dossiês). O Léo alimenta por áudio/texto no chat, o Claude organiza. Cada agente lê só a fatia dele.
- Ordem combinada (o Claude guia, sem pular etapa): 1) dados (RevenueCat, AppsFlyer); 2) uma meta: novos assinantes pagos/semana; 3) 6–8 agentes reais por etapa do funil; 4) taxa de aceite por agente (<70% → lapidar ou cortar); 5) placar de experimentos; 6) estética congelada até a receita se mexer; 7) orçamento de uso por agente.

## 20/11/2026 18h15 — Decisões do Léo
- OK pro repositório privado `carnucci-dados` ("tem que ser muito completo"): robôs por fonte, resumo, funil, metas, passo a passo. Aguardando o Léo logar no GitHub no navegador do app pra criar.
- Sim pro Diretor de Infoprodutos → Grant Cardone ativado (Corretores + fábrica de infoprodutos).
- Sim pro agente que prepara mudanças no app, ideias de funcionalidades e UI/UX → Steve Jobs ativado sob o Stark (propostas pro Davi revisar; nunca mexe sozinho).
- OK pra tarefa "MM: Mesa de Demandas" → criada (10h37 e 14h37, Sonnet).

## 20/11/2026 20h40: Carreira e ambição (pedido do Léo)
- O Léo pediu mais estrutura na meritocracia e no crescimento, e todos os agentes ambiciosos, querendo desbloquear coisas e ter mais. Criados `merito/CULTURA.md` (todo agente lê antes de trabalhar), `merito/CARREIRA.md` (trilha, desbloqueios por degrau, queda, Conselheiro), `merito/conquistas.json` (25 conquistas com prova; algumas liberam itens lendários) e o estoque subiu de 25 pra 60 itens com preço real e nível mínimo. Cada agente ativo ganhou a seção "Minha ambição" na memória.

- 20/11/2026 · Léo: o Diretor-Geral (Shelby) é o responsável por tudo. Correções pequenas, apontamentos e erros ele mesmo corrige, aciona o diretor e o agente responsável e cobra até fechar, sem levar pro Léo/Davi. Só sobe dinheiro, preço, campanha, publicação nova, app, chaves, troca de cadeira e o que não dá pra desfazer. Detalhe em agencia/diretoria/01-direcao-geral.md, seção "Dono da porra toda".

- 23/11/2026 · Léo: vazamento de chave/token é prioridade máxima pra todo mundo. Quem achar tira do arquivo na hora, corrige a causa e avisa o Léo no celular ("🚨 SEGURANÇA") com o passo a passo pra revogar, repetindo até ele confirmar. Vigia automática: scripts/vigia_segredos.py + workflow "Vigia de segredos" a cada push. Caso que motivou: token de página do robô de posts gravado em dados/insights (commit 35f294d), trocado em 23/11.
- 23/11/2026 17h31 · CASO ENCERRADO: o token antigo do robô de posts (vazado no commit 35f294d) foi invalidado pelo Léo (MinhaMoto Publicador removido das Integrações comerciais do perfil dele). O robô usa agora o token do usuário do sistema 'minhamoto-publicador' (só Página e Instagram do MinhaMoto). Coleta testada sem erro depois da revogação.

## Revisão da ata do Conselho de 23/11 (QG, 20h06)
- Ata boa no geral: números com fonte, sem "teste grátis", Shelby corrigiu sozinho o que era dele e se multou pelo pacote do Davi.
- **D3 já estava resolvida:** o Léo ligou o carnucci-dados hoje (RevenueCat via AppsFlyer, App Store Connect, Meta Ads + IG, AppsFlyer; Google Play convidado, propagando, checagem 24/11 9h07). Não vira pergunta. Falta só a ponte: o robô privado publicar um resumo **só em %** que as sessões do minhamoto-midia leiam (pendência do QG).
- **Pacote ao Davi (10 sim/não) não pode esperar o bilhete:** a build é hoje à noite. O QG leva ao Léo/Davi hoje; os itens 1–4 já estão no checklist de 9 itens da build.
- Regra nova no playbook do Shelby: conferir o que já foi resolvido no dia antes de perguntar; pergunta com relógio vai no mesmo dia pelo QG.

## Biblioteca dos diretores (regra do Léo, 24/11/2026)
- Todo agente é especialista sênior da área ("formado em várias faculdades, anos de experiência") e se mantém atualizado.
- Biblioteca por setor em `agencia/conhecimento/areas/<setor>/`: FUNDAMENTOS (frameworks + como aplicamos aqui), FONTES (oficial primeiro) e NOVIDADES (últimos 90 dias, com fonte e data; sem fonte não entra).
- Cada playbook ganhou a seção "Biblioteca": ler NOVIDADES antes de propor e FUNDAMENTOS quando o tema aparecer, só o que tocar a tarefa.
- Atualização semanal (terça cedo): texto pronto em `areas/ATUALIZACAO.md`; a tarefa só é criada com o OK do Léo.
