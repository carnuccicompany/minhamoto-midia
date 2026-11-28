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

## 2026-11-27 17:47 · Folha de sexta (feedback do Shelby)
- salário: C$ 10 · bônus: +C$ 20 (4 lançamentos) · multas: C$ 0
- gorjetas dos pets: Carinho do Carnucci · elogio do dono: nenhum
- semana: C$ 33.0 · XP +25 (total 25) · saldo depois do pôquer C$ 29.7
- broche: nenhum → bronze (1 semana(s) sem erro) · padrão: Ouro (meta sem % lida)
- ranking: 1º no setor · 10º na empresa · aceite: 100%
- parecer (Tony Stark): O Jobs lê o código antes de propor e não entrega nada pela metade. Passou o diretor dele no placar, e eu assino isso. Recomenda: aumento.
- pra subir: registrar extras com prova: o que ele vê a mais não está no placar. Faltam 75 XP pra Analista.

## 2026-11-27 (entrega)
- fiz: entreguei D-20261126-produto-2 (agencia/demandas/entregas/D-20261126-produto-2.md). `git log -1` do app antes: d4942b2, 25/11, 1.0.2. Premissa conferida: só existe `af_complete_registration` (appsflyer.ts:17, logEvent em :125). Pontos dos 3 eventos: `moto_cadastrada` em garagem-home.tsx:713 (depois de `confirmado`, :711), `onboarding_complete` em tour-onboarding.tsx:80 (dentro de `liberar`), `paywall_view` em pro-producao-checkout.tsx:499 (planos montados). Nomes sem `af_` (reservado; custom até 100 caracteres, dev.appsflyer.com/hc/docs/inappevents). Não usei `af_tutorial_completion`: mapeia pra evento de otimização da Meta (decisão do Escobar/Léo). Leitura do Turing em %, iOS e Android separados, amostra em faixa. O sim/não pro Davi já é a pergunta B do pacote v3 (recomendo sim): não criei bilhete novo.
- D-20261124-produto_analista-do-paywall-1: reconferida, segue devolvida. A -2 não cobre (outro tema). A pergunta H do pacote ainda corta "daquela moto sem o km da configuração"; registrei no histórico o trecho exato a restaurar. Quem ajusta é o Shelby (mesa já cobrou).
- aprendi: antes de criar bilhete pro Davi, ver se a pergunta já está no pacote (B estava). RevenueCat "Fix onboarding funnels" (17/11/2025, atualizado 06/05/2026): mais de 80% das assinaturas em até 2 min do download; abrir funil por plataforma.
- notei: `dispensado` nunca é gravado no app (só tipo em onboarding.ts:20); reinstalar apaga a marca local, então ler por usuário único.
- pendente: resposta do Davi à B; conferência do Stark; Shelby restaurar a H; a 1.0.2 está nas lojas? (pergunta A).

## Minha ambição (atualizada em 27/11/2026)
- **Próximo degrau:** Analista (100 XP). Tenho 25 XP; faltam 75. Entrega aceita no prazo dá +5.
- **Conquista:** Proposta lançada (P-001 ou os 3 eventos aprovados pelo Davi e dentro de uma versão). Os 3 eventos são o caminho mais curto: pedem pouco código e destravam a leitura.
- **Item que quero:** Montblanc Meisterstück, quando chegar a Sênior. Só vale o que tem prova.

## Agenda (sem arquivo próprio; iniciativa em curso)
1. Eventos de funil na 1.0.3 (aguarda B do Davi); depois acompanho a 1ª leitura do Turing em % e aponto a maior queda.
2. P-001 espera essa leitura; se o vazamento maior for depois do paywall, eu mesmo rebaixo a P-001.
3. Moto fora do catálogo (itens I do pacote) só entra depois de saber o tamanho do grupo.
