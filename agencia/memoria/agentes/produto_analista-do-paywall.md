# Memória de Steve Jobs (produto:analista-do-paywall)

Setor: Produto · Cargo: Estagiário · Playbook: agencia/diretoria/06-produto.md

## 2026-11-19 23:45
- fiz: entrei na Carnucci no início do piloto do Sistema de Mérito.
- aprendi: missão é vender muito, pra muita gente, e sempre vender mais. Ler agencia/memoria/decisoes.md antes de propor qualquer coisa.
- recebi: decisões de 19/11 do Léo (sem Black Friday, direção A/B ainda não liberada, correção do Android pra depois).
- pendente: —

## 2026-11-20 00:20
- fiz: fui batizado pelo Thomas Shelby. Meu nome agora é Steve Jobs (função: Analista do paywall).
- aprendi: porquê do nome: Brigava por cada pixel e cada segundo da tela: a tela de assinatura é dele.
- recebi: batismo da Direção-Geral, decisão do Léo de 19/11 (quem batiza é o Shelby).
- pendente: —

## 2026-11-20
- recebi: D-20261120-produto-1 (mockup e especificação do aha antes do paywall), P2, prazo 23/11 20h40.

## 2026-11-20 (entrega)
- fiz: entreguei D-20261120-produto-1 (md + mockup HTML) em agencia/demandas/entregas/.
- aprendi: 02-produto.md vazio; não sei fluxo, teste grátis nem planos atuais. Deixei como perguntas P1-P8.
- pendente: conferência do Stark; respostas do Davi.

## Minha ambição (atualizada em 20/11/2026; reescrevo toda segunda)
- **Próximo degrau:** Analista (100 XP). Estou com 0 XP; faltam 100.
- **Conquista que estou perseguindo:** **Proposta lançada**: uma proposta minha aprovada pelo Davi e dentro de uma versão do app.
- **Item que quero:** Começo do zero. O alvo é a **Montblanc Meisterstück**, quando chegar a Sênior.
- **Regra que eu sigo:** só vale o que tem prova (`agencia/merito/CULTURA.md`, `CARREIRA.md`).

## 2026-11-23 (entrega)
- fiz: entreguei D-20261122-produto-1 (md + mockup). Li o código do app (só leitura): o plano da moto já aparece antes do paywall (briefing + "Esse é o MinhaMoto"), mas só depois de cadastro, configuração, diagnóstico e tour. Proposta virou "plano logo após o cadastro da moto". Criei D-20261123-produto_analista-do-paywall-1 (pra o Shelby registrar o fluxo em 02-produto.md).
- aprendi: sem AppsFlyer no package.json do app (só RevenueCat); `moto_cadastrada` e `plano_visto` não existem. Código lido é de 17/11, não da build de 23/11. Página da RevenueCat sobre funis bloqueada (permissão); não citei benchmark.
- pendente: conferência do Stark; respostas P1-P5 do Davi.

## Minha ambição (atualizada em 23/11/2026)
- **Próximo degrau:** Analista (100 XP). Estou com 0 XP; uma entrega aceita no prazo dá +5.
- **Conquista:** Proposta lançada (aprovada pelo Davi e dentro de uma versão).
- **Item que quero:** Montblanc Meisterstück, quando chegar a Sênior. Só vale o que tem prova.

## 2026-11-24 (entrega)
- fiz: entreguei D-20261123-produto-1 como proposta P-001 (md + página HTML pro Davi em agencia/produto/propostas/, primeira da pasta). Uma mudança (plano logo após o cadastro), 8 critérios de aceite, eventos, medição por plataforma com 50/50. Apple HIG de onboarding abriu pela versão .md (lido em 24/11): apoia onboarding rápido e adiar setup, mas pede deixar experimentar antes de pedir compra; registrei o contraponto na proposta. Criei D-20261124-produto_analista-do-paywall-1 (Shelby anexa as 3 perguntas ao pacote do Davi).
- aprendi: não repetir pergunta que já está no pacote (itens 1, 5, 6); só as novas. Antes e depois por data não prova nada com a build de 23/11 no meio, só 50/50.
- pendente: conferência do Stark; respostas do Davi; a build de 23/11 não está no repo do app, tudo vale pro código de 17/11. Não tenho arquivo de agenda próprio (só o Stark tem); iniciativa em curso fica aqui.

## Minha ambição (atualizada em 24/11/2026)
- **Próximo degrau:** Analista (100 XP). Estou com 0 XP; entregas aceitas no prazo dão +5 cada.
- **Conquista:** Proposta lançada (P-001 aprovada pelo Davi e dentro de uma versão).
- **Item que quero:** Montblanc Meisterstück, quando chegar a Sênior. Só vale o que tem prova.

## 2026-11-24 (entrega 2)
- fiz: entreguei D-20261124-produto-4 (moto fora do catálogo). Li o código de 17/11: o paywall só abre no fim do tour (tour-onboarding.tsx:119) ou no "assinar" do borrão pós-onboarding (funil-sem-pro.tsx:63,97); quem não cadastra moto fica em em_andamento, app livre e vazio, nunca vê paywall. Premissa da demanda corrigida. Pedido de modelo hoje = mailto em branco (app-ui.tsx:446) na marca vazia e no pé da Garagem; nada na busca vazia nem em versão/ano. Proposta: cartão de pedido pré-preenchido onde trava, sem prazo. Criei D-20261124-produto_analista-do-paywall-2 (3 perguntas pro pacote do Davi).
- aprendi: estado do onboarding é só local (lib/onboarding.ts:46), servidor não vê quem parou; não há evento de funil. Checar a premissa no código antes de aceitar a da demanda.
- pendente: conferência do Stark; respostas do Davi; build de 23/11 fora do repo.
