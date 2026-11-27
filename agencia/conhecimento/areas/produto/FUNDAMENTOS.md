# Produto: fundamentos do especialista sênior

Para: Tony Stark (Produto) e Steve Jobs (designer de produto e paywall). Leia a seção que toca a tarefa.
Atualizado em 24/11/2026. Antes de propor, leia `NOVIDADES.md`.

## 1. O funil de um app de assinatura
Instalação → abertura → cadastro → ativação (primeiro valor) → paywall visto → assinatura → renovação.
- **Ativação** é o momento em que a pessoa sente o valor. No MinhaMoto: ver o plano de manutenção da própria moto (com datas e km).
- Mede cada etapa em %, separado por **plataforma** (iOS converte bem mais que Android na mediana do mercado; a diferença está na entrada) e por **origem** (orgânico x pago).
- **Como aplicamos aqui:** toda proposta de produto diz qual etapa mexe, qual a linha de base e qual evento mede (`onboarding_complete`, `paywall_view`, moto cadastrada).

## 2. Onboarding
- Objetivo: levar ao primeiro valor rápido, pedindo só o necessário. Cada tela a mais perde gente, mas tela que gera investimento (escolher a moto, ver o plano) aumenta a conversão.
- Encurtar não é sempre melhor: teste publicado pela RevenueCat (19/11/2026) mostrou que onboarding mais curto subiu a conclusão e derrubou o início de teste. Medir a etapa seguinte, não só a conclusão.
- **Como aplicamos aqui:** o plano da moto antes do paywall ("Esse é o MinhaMoto") é a aposta; qualquer mudança é 1 variável por vez, com teste 50/50.

## 3. Paywall
- Elementos: título de benefício, prova (o que a pessoa já viu do próprio plano), planos com preço claro, plano recomendado pré-selecionado, renovação e cancelamento explicados, termos e privacidade.
- **Âncora:** mostrar o anual com o equivalente mensal; o plano que você quer vender aparece selecionado (hoje: mensal selecionado, decisão do Davi de 17/11).
- **Momento:** paywall depois de entregar valor converte melhor que paywall seco na abertura; "valor antes do paywall" é a tese que a RevenueCat defende (17/11/2026).
- Sem teste grátis no MinhaMoto: nunca escrever "grátis" em tela, loja ou anúncio.
- Exigências das lojas na tela que cobra, checklist e números hard × freemium: ver `aulas/2026-11-27-paywall-pago-direto.md`.

## 4. Retenção e cancelamento
- **Churn** mensal e retenção por coorte (mês de assinatura) são os números de produto que mais mexem no LTV.
- Cancelamento involuntário (cartão recusado) se recupera com período de carência e aviso de cobrança (Apple e Google têm grace period / billing retry).
- Cancelamento voluntário: entender o motivo (pesquisa de saída), mensagem de retenção (Apple liberou em 04/11/2026), oferta de recuperação com cuidado pra não treinar o usuário a cancelar.
- **Hábito:** app que avisa no momento certo (revisão chegando, documento vencendo) cria motivo de voltar. Aviso só do que o app realmente faz (hoje: selo na Garagem, sem push de documento).

## 5. Experimentos
- Uma hipótese, uma variável, métrica principal definida antes, tamanho de amostra calculado, duração mínima de 1 a 2 semanas (ciclo semanal de uso).
- Com volume pequeno, priorizar mudanças grandes (efeito grande aparece com pouca amostra) e medir etapa a etapa.
- **Como aplicamos aqui:** nada vai pro app sem OK do Léo/Davi (código do app é só leitura pros agentes).

## 6. Medição dentro do app
- **RevenueCat:** fonte da verdade de assinatura (status, renovação, receita). `appUserID` = id da conta.
- **AppsFlyer:** origem da instalação (campanha) e eventos; o `appsflyerID` vai pro RevenueCat pra ligar compra à campanha.
- **Eventos mínimos:** cadastro, onboarding concluído, moto cadastrada, paywall visto, compra (vem do RevenueCat).
- **Privacidade:** coletar o mínimo, declarar nos rótulos das lojas, ATT no iPhone quando rastreia, política atualizada (a de 24/11/2026 já cita o AppsFlyer).

## 7. Qualidade e lojas
- Bug que o cliente acha antes do time vira 1★. Vigia de avaliações por versão nas 72h depois da build.
- Recurso escondido ou de teste na versão pública viola a diretriz 2.5.19 da Apple (desde 16/10/2026).

## 8. O que um sênior faz toda semana
- Olha o funil por etapa e plataforma; acha a etapa que mais perde.
- Escreve 1 proposta com hipótese, mudança única e métrica.
- Lê avaliações novas e relatos de bug.
- Confere novidades da Apple, Google e RevenueCat (NOVIDADES).

---
## Índice da biblioteca completa (atualizado em 27/11/2026)
Camadas: `NUCLEO.md` (ler em toda tarefa) → este arquivo + `aulas/` (buscar o tema com grep) → `NOVIDADES.md` e `LICOES.md` (histórico com data e prova).

| Data | Aula | Tema |
|---|---|---|
| 27/11/2026 | `aulas/2026-11-27-paywall-pago-direto.md` | Paywall pago direto: o que mostrar antes de cobrar, desenho da tela que cobra, exigências da Apple (3.1.2, HIG) e do Google, números hard × freemium, regras da casa |
