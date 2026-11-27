# Produto · NÚCLEO (ler em TODA tarefa)

Para: Tony Stark e Steve Jobs. Reescrito em 27/11/2026 pelo professor-chefe, no 1º treino do setor. Curto de propósito: o resto está na biblioteca (índice no fim). Antes de propor, busque o tema: `grep -ril "<tema>" agencia/conhecimento/areas/produto/`. Antes de falar do app: `git log -1` no minhamotooficial (só leitura).

## 1. Correções do Léo (nunca repetir)
- **Sem teste grátis:** nada de "grátis", "teste" ou "X dias" em tela, loja, anúncio ou proposta (20/11).
- **Preço:** "R$19,90", nunca "por mês" em anúncio, post e vídeo; carrossel sem preço (26/11); criativo da App Store sem preço (24/11, Apple 2.3.14). Nunca "vitalício".
- **Paywall não se mexe** (preço, planos, ordem, texto) sem OK do Léo/Davi; código do app é só leitura.
- **Visual 1.0.2 é o único:** telas de 17/11 e `ios-1.0/` proibidas em mockup e proposta (26/11).
- **Tráfego (26/11):** landing → loja; régua = custo por assinante pago, nunca instalação ou clique.
- Sem Black Friday (19/11). Não perguntar de novo o que está em decisoes.md (23/11).
- Repositório público: nada de R$ da empresa, número absoluto, chave, e-mail ou dado de cliente (23/11).

## 2. As regras que mais mexem em venda
1. Toda proposta diz qual etapa mexe (instalação → cadastro → moto → plano → paywall → pagante → renovação), a linha de base e o evento que mede.
2. Proposta sai como página de decisão em sim/não pro Davi: 1 variável, teste 50/50 ao mesmo tempo, métrica antes (modelo P-001).
3. O valor que é da pessoa (plano da moto) vem antes de cobrar. A aposta é encurtar o caminho até ele (P-001).
4. Sem `paywall_view` e `onboarding_complete` nenhum teste fecha leitura: eventos primeiro (D-20261126-produto-2). Hoje só existe `af_complete_registration`.
5. Medir por plataforma (iOS e Android separados) e com receita depois de reembolso, não conversão bruta.

## 3. Lições recentes da casa (LICOES.md)
- 27/11: o paywall escreve "dias grátis" sozinho se a loja tiver oferta introdutória. Ninguém liga oferta na App Store Connect ou no Play.
- 26/11: código tratado como de 17/11 por 3 dias. `git log -1` no começo de toda rodada.
- 26/11: SDK do AppsFlyer no código desde 24/11; compra chega na Meta desde 26/11 (corrige a lição de 24/11).
- 26/11: pergunta copiada com corte mudou de sentido (devolvida). Copiar sem cortar.
- 24–25/11: afirmação sobre o app leva arquivo:linha, commit e versão; conferir a premissa no código; conferir cada item do `pronto_quando`.
- 24/11: aceite só depois de abrir o arquivo entregue, não o resumo.
- Página da Apple que não abre: tentar a versão `.md`.

## 4. Novidades que mudam a forma de trabalhar (detalhe em NOVIDADES.md)
- 26/11 RevenueCat: aumento de preço na Apple acima de 50% e de US$5 por período pede consentimento; no Play é opt-in com 37 dias de aviso; redução não volta.
- 24/11 RevenueCat: paywall em várias telas converte mais na mediana (correlação). Candidato a teste depois dos eventos.
- 04/11 Apple: mensagem de retenção no cancelamento (proposta do Stark, Léo aprova).
- 02/11 Apple: descritores de classificação etária, prazo 12/01/2027.
- 16/10 Apple: 2.5.19 (nada escondido: `VITE_MM_AVISO_TESTE` fora da loja) e 2.3.14 (criativo sem preço).
- 30/09 Google: verificação de desenvolvedor no Brasil. Conferir no Play Console se o app está registrado.
- 29/09 Google Play: carência dinâmica e mensagem de pagamento recusado. Proposta pro Davi no Android.

## 5. Paywall pago direto: regras da aula de 27/11
1. **Checklist da tela que cobra:** nome e duração do plano · o que libera · valor cobrado em destaque e localizado · renovação automática e como cancelar · restaurar compras · Termos e Privacidade · sair visível · zero "grátis/teste/dias/vitalício".
2. **Dentro da tela que cobra, duração e renovação ficam** ("mensal", "/mês"): Apple 3.1.2 e Google exigem. O "nunca por mês" é pra anúncio, post e vídeo (exceção levada ao Léo pra registrar).
3. **Valor cobrado é o preço mais destacado;** equivalente mensal e economia menores e abaixo.
4. **Pré-selecionado hoje: mensal** (Davi, 17/11). Anual em destaque é hipótese de teste com OK, nunca troca direta.
5. **10,7% é mediana de mercado de hard paywall** (RevenueCat 2026), não meta nossa. A régua nasce da 1ª leitura em %.

## 6. Índice da biblioteca
- `FUNDAMENTOS.md`: §1 funil · §2 onboarding · §3 paywall · §4 retenção e cancelamento · §5 experimentos · §6 medição · §7 qualidade e lojas · §8 rotina sênior · índice de aulas.
- `aulas/2026-11-27-paywall-pago-direto.md`: o que mostrar antes de cobrar, desenho da tela, exigências Apple/Google, números hard × freemium, erros, como aplicamos.
- `NOVIDADES.md` (90 dias, com fonte) · `LICOES.md` (acertos e erros com prova) · `FONTES.md` (oficial primeiro).
- Fora da pasta: `agencia/memoria/decisoes.md`, `conhecimento/02-produto.md`, `agencia/produto/propostas/`, `agencia/DESIGN-MINHAMOTO.md`.
