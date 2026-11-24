# P-001 · Tela "Plano da sua moto" logo após o cadastro da moto

De: Steve Jobs (produto:analista-do-paywall) · Pra: Davi (decide), Léo (ciência) · Conferência: Tony Stark · 24/11/2026
Status: **proposta, aguardando o Davi.** Nada mexe no app. Sem R$, sem número absoluto. Paywall, preço, planos e ordem dos planos intocados (lapidado com o Léo, 20/11).
Página pra aprovar/recusar: `agencia/produto/propostas/P-001-plano-da-moto-apos-cadastro.html`. Telas: `agencia/demandas/entregas/D-20261122-produto-1-mockup.html` (passo 2 é a tela nova).

## Por que (ligado a vender)
O número do produto é % instalação > pagante. No código lido (17/11) o plano da moto só aparece no fim do tour, depois de configuração e diagnóstico (D-20261122-produto-1, `tour-onboarding.tsx`, `esse-e-o-minhamoto.tsx`). Quem larga antes nunca vê o valor do app. **Hipótese, sem funil ainda:** mostrar o plano logo depois do cadastro encurta o tempo até o valor e leva mais gente ao paywall. Apoio de fonte oficial: a Apple pede onboarding "rápido" e "adiar configuração não essencial" ([HIG, Onboarding](https://developer.apple.com/design/human-interface-guidelines/onboarding), lido em 24/11). Contraponto honesto, da mesma página: a Apple prefere deixar a pessoa "experimentar o app antes de pedir avaliação ou compra". Por isso a tela nova não pede nada e não é paywall; só mostra o plano mais cedo.

## 1. Antes e depois (uma única mudança)
| # | Antes (código de 17/11) | Depois |
|---|---|---|
| 1 | Boas-vindas | igual |
| 2 | Cadastro da moto | igual |
| 3 | Configuração (km, respostas, cuidados, ritmo) | **NOVO: "Plano da sua {moto}"** |
| 4 | Diagnóstico (briefing de 4 telas) | Configuração (igual ao 3 de hoje) |
| 5 | Tour | Diagnóstico e tour (iguais) |
| 6 | "Esse é o MinhaMoto" | igual |
| 7 | Paywall pago direto | igual, intocado |

Tela nova, em texto: título "Plano da sua {moto}", destaque "Próxima revisão" com o item do manual e o km, mais 2 itens, nota "Sem pedir km agora", botão Continuar. Todo "X" é dado que o app já calcula para o briefing; nada inventado.

## 2. Critérios de aceite
1. Após cadastrar a moto e antes da configuração, abre a tela do plano daquela moto.
2. Usa só dados de plano que o app já tem; não pede km, permissão nem cadastro novo ali.
3. Moto sem plano disponível: a tela não aparece e o fluxo segue como hoje. Nenhum plano inventado.
4. Conta com Pro, ou que já passou do onboarding, não vê a tela.
5. "Continuar" leva à configuração atual sem perder o que foi escolhido.
6. Paywall, planos, preço, ordem e "Restaurar compra" idênticos.
7. Eventos `moto_cadastrada` e `plano_visto` (parâmetro `momento`: pos_cadastro ou fim_tour) disparam uma vez cada, com `variante` (atual ou novo).
8. Fora do ar até o OK do Davi e do Léo. Nada de teste grátis, "grátis" ou "X dias" em lugar nenhum da tela.

## 3. O que mede
- **Principal:** % instalação > pagante, **iOS e Android separados desde o dia 1** (a base de apps com teste grátis não serve de meta: RevenueCat mostra Android abaixo do iOS já na 1ª etapa, `agencia/conselho/rodadas/2026-11-23/produto-r1.md`).
- **Etapas (leitura por evento, não por ordem de tela):** instalação > onboarding concluído > moto cadastrada > plano visto > paywall visto > pagante. `plano_visto` pode chegar antes de `onboarding_complete`.
- **Fontes:** AppsFlyer (instalação, eventos) + RevenueCat `INITIAL_PURCHASE`. Hoje o código lido não tem SDK do AppsFlyer nem `logEvent`; sem evento não há teste (pacote do Davi, itens 1 e 2).
- **Guarda-corpo:** nota e reclamações nas lojas por versão (vigia D-20261123-produto-2). Se a tela aumentar queda de avaliação, para.
- **Condição de morte (Stark):** se, no período combinado, a % de pagante do novo não ficar acima do atual, volta ao atual. Só dá pra afirmar efeito com divisão 50/50 de usuários simultâneos; "antes e depois" por data mistura efeito da build estética de 23/11 e não prova nada.
- Sem baseline hoje. Duração e tamanho de amostra: Turing define quando houver % por plataforma.

## 4. Perguntas pro Davi (3, sim/não, não repetem o pacote)
O pacote do Davi (`D-20261123-master-pacote-davi`) já pergunta, e valem aqui: **item 5** (a tela "Esse é o MinhaMoto" continua na build de 23/11? é a P1 desta proposta), **item 6** (cobertura CG 160, Pop 110i, Biz, Bros 160; moto sem plano) e **item 1** (SDK e eventos). Respondidos esses, só faltam:
1. **Logo após o cadastro, o app já tem os dados pra montar o plano daquela moto (sem o km da configuração)?** Recomendo: sim, por ser o mesmo cálculo do briefing, mas só o Davi sabe. Se "não", a proposta vira "plano em km médio do modelo", e eu redesenho.
2. **Dá pra dividir 50/50 por flag remota, sem build nova?** Recomendo perguntar: se não, o teste só entra numa próxima build e a leitura espera.
3. **Posso preparar um rascunho de código num branch separado (sem merge) depois do seu OK na proposta?** Recomendo sim, só depois do OK; sem isso nada é escrito.

## 5. Limites
- Código lido é de 17/11 (1.0.1), não da build de 23/11. A proposta depende da resposta ao item 5 do pacote.
- Nenhuma % nossa existe ainda; todo ganho aqui é hipótese até a 1ª leitura (até 7 dias depois da versão com SDK).
- Google In-App Review e Material não consultados: a tela não pede permissão nem muda compra. Apple HIG consultado em 24/11 (link acima).
