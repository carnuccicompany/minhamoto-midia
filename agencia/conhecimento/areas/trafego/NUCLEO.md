# Tráfego · NÚCLEO (ler em TODA tarefa)

Para: Pablo Escobar. Reescrito em 25/11/2026 pelo professor-chefe. Curto de propósito: o resto está na biblioteca (índice no fim). Antes de propor ou produzir, busque o tema: `grep -ril "<tema>" agencia/conhecimento/areas/trafego/`.

## 1. Correções do Léo (nunca repetir)
- App **sem teste grátis**: nada de "teste", "trial", "grátis", "X dias" em plano, funil ou anúncio (20/11).
- Campanhas dos **Corretores não se editam sem OK do Léo**; leitura sim (18/11). Nada sobe, nada gasta sem OK.
- **Destino do anúncio conferido** antes de verba: o link do Instagram @minhamotoapp está bloqueado (23/11).
- Não perguntar de novo: Kavoo + UTMify; custo máximo por assinante no privado; BM só de anúncios adiada (23/11).
- Sem Black Friday (19/11). Preço MinhaMoto "R$19,90", nunca "por mês"; asset da App Store sem preço (24/11).

## 2. As regras que mais mexem em venda
1. **Régua:** Corretores = custo por venda e ROAS contra a margem real (AOV líquido, não preço da frente). MinhaMoto = custo por **assinante pago**, nunca por instalação. Valores só no `carnucci-dados`.
2. **Verba zero no MinhaMoto até o SDK do AppsFlyer estar na build publicada** e o evento de compra chegar (a build de 23/11 saiu sem SDK).
3. **Criativo é a segmentação.** Público aberto + ideias realmente diferentes. A Meta agrupa criativos parecidos: teste = ângulo/formato/pessoa/cenário diferente.
4. **Conta dos conjuntos antes de montar teste:** verba semanal ÷ (CPA alvo × 50) = máximo de conjuntos (Meta: ~50 conversões/semana por conjunto; abaixo, CPA ~28% maior). Deu menos de 3? Teste de criativo dentro do conjunto que já vende.
5. **Regra de corte escrita antes de gastar**, em % do custo de outubro (3 estilos dos Corretores: dobra ≤100%, mantém 100–119%, corta >119%, pausa a 200% sem venda). Nada se decide antes de 4 dias, salvo corte por gasto.
6. **Leitura:** venda real pela UTMify (`utm_content` = CR-<ângulo>-<nn>); Meta pro diagnóstico (detalhamento Criativo → Mídia, gancho, CTR, CPM). Anúncio sem gasto não é perdedor provado.
7. **Escala:** +20 a 30% por degrau ou duplicar na campanha de escala; nunca desligar tudo pra ficar só com o vencedor.
8. **Reposição:** ≥5 criativos novos/semana nos Corretores enquanto houver teste (pedido à Disney antes da fadiga: CTR caindo + CPM subindo).
9. **Funil em queda:** diagnosticar na ordem CPM → CTR → clique→página → página→checkout → checkout→compra, com número em cada etapa.
10. **Padrão de UTM e nome:** `meta-ads`/`tiktok-ads`, `mm_<rede>_<evento>_<so>_<aamm>`; orgânico = `organico`.

## 3. Novidades que mudam a forma de trabalhar (detalhe em NOVIDADES.md)
- 12/11: Meta mede conversões também no aparelho (Pixel, padrão ligado) → compras na Meta podem subir sem venda nova; anotar quebra de série.
- ~16/11: escolha de posicionamento por conjunto some em Vendas/Leads/App → exclusões só na conta; criativo em 9:16 e 4:5.
- 05/11: novos termos da Meta **pausados**; aviso de aceite vai ao Léo antes.
- 04/11: conjunto de Vendas novo "só um tipo de aparelho" pode vazar pra outros (padrão ligado) → conferir no rascunho.
- 06/10: excluir quem já comprou nas campanhas de aquisição (proposta pro Léo).
- 01/10: WhatsApp cobra mensagem de atendimento/utilidade.

## 4. Lições recentes da casa (LICOES.md)
- 24/11: antes de criar demanda, `ls itens/ | grep <id>` (sobrescrita da trafego-1).
- 24/11: nº de vendas por variante quase não depende da taxa-base (~78 p/ 50% de diferença, ~200 p/ 30%).
- 23/11: aceite do próprio trabalho não vale.
- 22/11: conferir numerador e denominador de toda % ("1 de 3", não "40%").
- 20–24/11: quatro rodadas sem número de campanha; cada rodada traz um número ou o bloqueio exato.

## 5. Índice da biblioteca
- `FUNDAMENTOS.md` §1 conta que manda · §2 leilão · §3 estrutura · §4 sinal (pixel, CAPI, SDK) · §5 atribuição · §6 funil · §7 corte e escala · §8 TikTok · §9 políticas e risco · §10 rotina sênior.
- `aulas/2026-11-25-teste-de-criativo-meta-pos-andromeda.md` · ferramentas de teste, onde testar, volume, leitura, benchmarks (~5% de vencedores).
- `NOVIDADES.md` (histórico com fonte) · `LICOES.md` (acertos e erros da casa) · `FONTES.md` (oficial primeiro).
- Fora da pasta: `agencia/memoria/decisoes.md`, `conhecimento/09-numeros.md`, `estudio/produtos/corretores-aprendizados.md`.
