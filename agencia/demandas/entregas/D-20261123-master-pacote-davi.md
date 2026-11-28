# Pacote ao Davi (v3, reescrito pelo Shelby em 26/11/2026) · cobre D-20261122-produto-3, D-20261122-dados-1, D-20261124-produto-3 e as perguntas bloqueadas dele

Só o Davi responde, sim/não em cada item. Um pacote só, sem novo bilhete. **Mudou desde a v2 (23 a 26/11):** o Stark leu o código do app de 25/11 (89 commits, último d4942b2, `versionName` 1.0.2, SDK do AppsFlyer entrou em 24/11, commit 99c9a96; leitura só de commit, fonte: D-20261126-produto-1). Tudo abaixo marcado "código de 25/11" é **a confirmar pelo Davi**. Sem R$ e sem número absoluto.

## Já respondido pelo código de 25/11 (saiu da lista; o Davi só corrige se estiver errado)
- **SDK AppsFlyer:** existe no código (24/11). Era o item 1 da v2.
- **`appsflyerID` vai pro RevenueCat:** sim, `src/lib/revenuecat-compras-nativo.ts:53-59` e `:121`. Era o item 2.
- **Postbacks pra Meta:** o QG mapeou compra e cadastro no AppsFlyer em 26/11 (`trafego/LICOES.md`); não é pergunta ao Davi.
- **Só um evento de funil no código:** `af_complete_registration` (`src/lib/appsflyer.ts:17`). Não achei `onboarding_complete` nem `paywall_view` (vira a pergunta B).
- **Tela "Esse é o MinhaMoto" antes do paywall:** continua, commit 79d19d1. Era o item 5.

## Perguntas abertas (nesta ordem)
A. **A 1.0.2 já está nas duas lojas? Que dia?** (D-20261124-produto-3, P1). O repositório indica 1.0.2, mas não prova publicação. Sem o dia, a leitura do funil, o vigia de 72 h e o relógio do dia 1 da campanha ficam errados. **O Léo também responde isto olhando as lojas.**
B. **Dá pra incluir 3 eventos (`onboarding_complete`, `paywall_view`, moto cadastrada) numa 1.0.3, em cima do SDK que já existe?** Proposta do Jobs em D-20261126-produto-2. Recomendo: sim; sem eles não separo "não cadastrou" de "viu e não pagou".
C. O **modelo da moto** vira propriedade do usuário (sim/não)? Sem isso não existe % por modelo (Turing).
D. O build de loja define `VITE_MM_AVISO_TESTE` (botão "Testar aviso em 1 minuto", `verificacao-app.tsx:22`)? Se sim, sai da versão pública.
E. **O catálogo da 1.0.2 mantém CG 160, Pop 110i, Biz 125 e Bros 160 com tabela oficial?** E moto sem plano: o que o usuário vê? (Item 6 da v2.)
F. **Selo "Documento vencendo" e telas Histórico, Saúde e Notificações da 1.0.2** são iguais ao que A1/B1 mostram? Continua sem push de documento? Se mudou, descreve; a cena é refeita antes de ir ao ar. Mais: libera as 5 telas ou gravações 9:16 da 1.0.2 (sem dado de cliente), D-20261120-cria-3, 27/11 18h.
G. Já existe pedido de avaliação, só depois de "Registrar serviço"? A moto é escolhida em lista, há anúncio na tela, a conta guarda histórico entre aparelhos? O banco guarda a data de fim do onboarding e da 1ª moto por plataforma (só contagem por dia)? (Itens 7 a 9 da v2.)
H. **Plano da moto logo após o cadastro** (P-001, anexo: `agencia/produto/propostas/P-001-plano-da-moto-apos-cadastro.html`): **logo após o cadastro, o app já tem os dados pra montar o plano daquela moto (sem o km da configuração)?** Se não, a proposta vira "plano em km médio do modelo". Dá pra dividir 50/50 por flag remota, sem build nova? Posso preparar rascunho em branch separado, sem merge, depois do OK? (D-20261124-produto_analista-do-paywall-1; recomendo sim nos três.)
I. **Moto fora do catálogo:** o "em até 48 horas" é cumprido hoje? O cartão "Pedir este modelo" cabe dentro da lista sem mexer no servidor? A tela "Esse é o MinhaMoto" ainda completa com 6 itens genéricos? (D-20261124-produto_analista-do-paywall-2, itens 17 a 19 da v2.)

Se só der tempo de uma resposta: **A**. Depois B.
Quem usa depois: Stark confere cena por cena (cria-3), Turing monta a linha de base, Escobar fecha a data do dia 1.
Status: texto pronto; vai ao Davi pelo bilhete de decisões e pelo QG. Nada decidido por mim.
