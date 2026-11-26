# Agenda de Tony Stark (produto)

## Metas pessoais
- Manter o 1º lugar no setor e o 2º na empresa com entrega que vira número, não com bug apontado.
- Levar ao Davi uma proposta escrita antes da build de 23/11 (era a cobrança do Shelby na Folha de 20/11) e ter o 1º funil do app com dado real até 7 dias depois da build.
- Subir o broche e ganhar o fogo da Marnevali: um extra com número por semana.

## Apostas
- O gargalo do assinante pago está no começo do app (tempo até ver o plano da moto), não no volume de posts. Hipótese, sem dado nosso ainda.
- Preço e duração do teste grátis são decisão do Léo e do Davi: eu levo o teste desenhado e o risco.

## Iniciativa em curso (atualizada 2026-11-22)
- "Plano da moto visível antes do paywall", refeita pro fluxo real (onboarding > cadastro da moto > paywall pago direto, SEM teste grátis; fonte: lapidado com o Léo 20/11 em 06-produto.md). Mede-se % instalação>pagante por etapa. Sem baseline até o SDK entrar; 1ª leitura até 7 dias após a build; teste 50/50 de 14 dias; se não subir, eu mato. Desenho refeito pelo Jobs em D-20261122-produto-1.
- Erro meu a não repetir: na rodada de 20/11 não li a seção lapidada e tratei teste grátis como incógnita. Ler 06-produto.md inteiro antes de cada rodada.

## Pendências (22/11)
- Pacote único de perguntas ao Davi via Shelby: D-20261122-produto-3 (dados-2, lojas-2, mercado-2, mercado-4, cria-3).
- Funil em 6 etapas com o Turing: D-20261122-produto-2.
- Perguntas ao Léo: plano visto antes do paywall?; confirmar que não há teste grátis; pedido de avaliação já existe?
- Apple HIG e Google In-App Review bloqueados de novo em 22/11.

## Pendências antigas
- Devo 5 respostas bloqueadas no Davi (D-20261120-dados-2, -trafego-1, -lojas-2, -mercado-2, -cria-3): pergunta pronta em cada uma.
- Perguntas pro Léo sobre onboarding/paywall/teste atuais (registradas em conhecimento/perguntas-pendentes.md).
- Conferir Apple HIG e Google In-App Review (não abriram em 20/11).
- Sem acesso ao carnucci-dados nesta sessão.

## Do Jobs (23/11): D-20261122-produto-1 entregue
- Fluxo real lido no código (17/11): plano já vem antes do paywall, no fim do tour. Proposta: tela do plano logo após o cadastro da moto. Perguntas P1-P5 ao Davi no fim da entrega; P1 (a build de 23/11 mantém o briefing?) se junta ao item 4 do pacote produto-3.

## Rodada 23/11
- Iniciativa mantida (plano da moto logo após o cadastro). Aceitei produto-1 do Jobs e produto-3 do Bezos; Turing já tinha aceita em produto-2. Criei D-20261123-produto-1 (Jobs: página de decisão pro Davi, 26/11) e D-20261123-produto-2 (Bezos: vigia pós-build, 26/11).
- RevenueCat (android-paywall-gap): download>pago mediana Android 0,9% x iOS 2,6%, diferença na 1ª etapa. Uso só pra separar plataformas desde o 1º dia; não é meta nossa (apps com teste).
- Risco que vi no checklist: VITE_MM_AVISO_TESTE ainda a remover antes da build. Conquista alvo: Pegou antes do cliente.
- Pendências: Davi (produto-3); 1ª leitura em % até 7 dias após a versão com SDK; Apple HIG segue bloqueado.
- Perguntas ao Léo: avaliação no app já existe?; briefing antes do paywall fica na build?; RevenueCat leitura pro Turing?

## Rodada 24/11
- Entregues: mercado-3 (reentrega) e cria-3. Criadas produto-1 (Shelby, pacote do Davi) e produto-2 (Disney, frase do aviso), prazo 27/11.
- Pendências: D-20261123-produto-1 (Jobs, página de decisão, 26/11) e D-20261123-mercado_radar-de-concorrentes-1 (modelo por lista e planos por modelo, 30/11, não toquei: ainda aberta). Build de 23/11 não está no repositório do app: tudo que digo vale pro código de 17/11 (1.0.1).

## 24/11 tarde
- Entregues mercado_radar-de-concorrentes-1 e cria-1 (aguardam aceite). Próximo: acompanhar Jobs (produto-1, 26/11) e reconferir as 3 telas e o catálogo quando a build de 23/11 entrar no repo.

## Rodada 24/11 (Conselho, r1)
- Iniciativa mantida: P-001 (plano da moto após o cadastro), aceita; falta o "sim" do Davi e o SDK. Sem baseline, não chuto %.
- Fato novo: repo do app com último commit em 17/11; a build de 23/11 e o SDK não aparecem. Criei produto-3 (Shelby, P1: a build saiu?), produto-4 (Jobs: moto fora do catálogo), produto-5 (Turing: tamanho do teste 50/50 em semanas).
- Aceitei D-20261124-produto-1 e D-20261123-produto_analista-do-paywall-1. Pendências: Davi (pacote de 12 itens); Jobs com as 3 perguntas da P-001 (27/11); Apple HIG segue bloqueado.
- Pesquisa: RevenueCat, "Paywall placement: deliver value before the paywall" (17/11/2026), https://www.revenuecat.com/blog/growth/app-value-paywall.

## 25/11
- Reentreguei D-20261124-mercado-1 (4 líderes, versões e anos, Biz 110i até 2024). Aguardo aceite do Mercado. Próximo: Jobs produto-1 (26/11); reconferir catálogo quando a build de 23/11 entrar no repo.

## Rodada 26/11 (Conselho, r1)
- Iniciativa trocada: "Funil visível" (3 eventos mínimos sobre o SDK já no código) vem antes da P-001; a P-001 espera a etapa que mais perde gente. Mato se o evento chegar e não houver diferença entre etapas.
- Fato novo do repo do app (leitura): 89 commits, último 25/11 (d4942b2), versão 1.0.2, SDK AppsFlyer mergeado em 24/11 (99c9a96), único evento af_complete_registration, UID vai pro RevenueCat. Não prova que a 1.0.2 está nas lojas. "Esse é o MinhaMoto" continua no fim do tour, antes do paywall (79d19d1); a P-001 não entrou.
- Criadas: D-20261126-produto-1 (Shelby, P1), -2 (Jobs, P2), -3 (Turing, P2). Aceitei D-20261124-produto-4.
- Pendências: Davi (pacote); Jobs (trafego-3, 27/11); Turing (produto-5, 01/12). Apple HIG, Google In-App Review e a página de novembro da RevenueCat bloqueados.
- Pesquisa: RevenueCat, hard paywall e jornada de ativação (08/09/2026), https://www.revenuecat.com/blog/growth/hard-paywall-activation-journey.
