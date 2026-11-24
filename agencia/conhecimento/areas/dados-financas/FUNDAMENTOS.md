# Dados e finanças: fundamentos do especialista sênior

Para: Alan Turing (Dados e Finanças) e Ernest Hemingway (relatório semanal). Leia a seção que toca a tarefa.
Atualizado em 24/11/2026. Antes de propor, leia `NOVIDADES.md`. Número absoluto nunca vai pro repositório público: aqui só % e variação; o absoluto fica no `carnucci-dados`.

## 1. Economia unitária de assinatura (MinhaMoto)
- **MRR:** receita recorrente mensal (anual entra dividido por 12). **ARR** = MRR × 12.
- **Churn:** % de assinantes que cancelam no mês. Separar voluntário (pediu pra sair) e involuntário (cartão recusado).
- **LTV** ≈ receita média por assinante por mês × margem ÷ churn mensal. Com pouco histórico, usar curva de retenção por coorte em vez da fórmula.
- **CAC:** gasto de mídia ÷ novos assinantes pagos do período (por canal).
- **Payback:** meses até a margem do assinante pagar o CAC. Regra prática: payback curto (poucos meses) permite escalar com caixa próprio.
- **Receita líquida:** a loja fica com a comissão (Apple/Google, em geral 15% no programa de pequenas empresas e após 1 ano de assinatura); impostos por cima.
- **Como aplicamos aqui:** o placar semanal mostra novos pagantes, churn, MRR e CAC por canal, em %, com o absoluto no privado.

## 2. Economia unitária de infoproduto (Corretores)
- **Faturamento por venda** = front (R$27,90) + taxa de aceite dos order bumps × valor dos bumps. O bump é o que segura a margem de ticket baixo.
- **Margem por venda** = faturamento − taxas do checkout − impostos − reembolso − custo de mídia por venda.
- **ROAS de equilíbrio** = 1 ÷ margem de contribuição antes da mídia. Abaixo dele, cada venda dá prejuízo.
- **Pix não pago:** ~85% dos pagamentos são Pix e ~1 em 5 Pix gerados não é pago. Recuperar é a venda mais barata que existe.
- **Reembolso** entra no placar (garantia de 30 dias na página).
- **Como aplicamos aqui:** o placar diário dos Corretores sai da UTMify (por anúncio) e da planilha Kavoo (por produto e meio de pagamento).

## 3. Tributos que mexem na conta
- **Anúncio na Meta no Brasil:** desde 2026 a Meta repassa tributos ao anunciante (o comunicado de 2025 fala em cerca de 12,15% sobre o valor do anúncio). Esse custo entra no CAC e no ROAS real. Confirmar na fatura.
- **Reforma tributária (CBS e IBS):** 2026 é ano de teste (alíquotas simbólicas destacadas na nota, sem cobrança efetiva na maior parte dos casos); a transição real começa em 2027 com a CBS. Acompanhar com o contador o efeito no regime da Carnucci.
- **Apple/Google:** recolhem e repassam tributos nas vendas das lojas conforme o país; o relatório financeiro da loja mostra o líquido.
- Não sou contador: decisão tributária é do contador da empresa; o diretor traz o impacto em %.

## 4. Pix como canal de venda
- Pix é o meio dominante no Brasil (pessoa para empresa chegou a 45% das transações em out/2026, segundo o Banco Central).
- Pix Automático (desde jun/2025) permite cobrança recorrente: candidato a pagamento de assinatura fora das lojas no futuro (só onde a regra da loja permitir; dentro do app, a compra é pela loja).
- MED (devolução por fraude) e contestação existem: venda por Pix pode voltar em caso de fraude comprovada.

## 5. Dados e medição
- **Uma fonte da verdade por número:** assinatura = RevenueCat; instalação/campanha = AppsFlyer; venda de infoproduto = Kavoo; atribuição de venda por anúncio = UTMify; mídia = Meta/TikTok.
- **Números não batem e tudo bem:** cada ferramenta conta com regra própria (janela, fuso, reembolso). Explicar a diferença, não forçar.
- **Leitura de variação:** amostra pequena engana. Com poucas vendas por dia, olhar 7 dias móveis e intervalo, não o dia isolado.
- **Coorte:** comparar clientes do mesmo mês de entrada; média geral esconde piora recente.
- **Número sem fonte não entra.** O Turing é o fiscal: entrega com número sem fonte volta.

## 6. Caixa e decisão
- Caixa vem antes de lucro contábil: anúncio paga hoje, loja repassa depois (Apple ~mensal, com atraso).
- Teto de verba e de custo por assinante ficam no privado e só o Léo muda.
- **Como aplicamos aqui:** toda proposta que gasta dinheiro mostra custo, retorno esperado e prazo de retorno.

## 7. O que um sênior faz toda semana
- Placar semanal: novos pagantes, churn, MRR, CAC, ROAS dos Corretores, % da meta.
- Autópsia quando a meta não bate: em qual etapa caiu, com número.
- Confere se todas as fontes coletaram (status.json) e explica falhas.
- Lê NOVIDADES (tributos, Pix, preços das plataformas).
