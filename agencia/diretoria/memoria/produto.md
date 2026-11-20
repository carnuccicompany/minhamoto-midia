# Memória do setor: produto

Pesquisas e aprendizados que valem guardar. Uma entrada por achado: data, achado, fonte (link), o que fazer com isso. Não repita pesquisa que já está aqui; atualize a entrada.

## Lista pro Davi (em ordem de impacto) · atualizada 20/11/2026
Obs.: nada aqui mexe em código; é proposta pro Davi decidir. Decisão de 19/11 vale: correção do Android só depois da build de 23/11.
1. **SDK AppsFlyer + eventos do funil na build de 23/11** (cadastro, moto escolhida, plano visto, paywall visto, teste iniciado, compra, cancelamento). Problema: sem isso não há assinante pago por origem nem custo por assinante (Conselho 19/11). Medir: % das assinaturas novas com fonte identificada. Pedidos abertos: D-20261120-dados-2, D-20261120-trafego-1.
2. **Pedido de avaliação no momento feliz** (depois de 'Registrar serviço' concluído; nunca após erro de sincronizar; 1 vez por usuário por versão). Problema: a loja tem 1 de 1★ em 9 avaliações, do Android (dados/avaliacoes/ultimas.json, 20/11). Medir: nº e nota média de avaliações novas por semana. A conferir antes: limites do Apple HIG e do Google In-App Review (não abriram em 20/11).
3. **Aha antes do paywall** (escolher moto > ver plano de revisão pronto em menos de 60 s > paywall). Problema: 55,4% dos cancelamentos de teste de 3 dias são no dia 0 (RevenueCat 2026, média de 115 mil apps). Medir: início de teste e teste→pago antes/depois. Desenho em D-20261120-produto-1; entra depois da build.
4. **Falha ao sincronizar no Android (v1.0.1)**: já decidido, o Davi corrige depois de 23/11. Evidência: avaliação 1★ de 19/11 no Google Play. Medir: nova avaliação de sincronização = 0.
5. **Teste da duração do teste grátis**: precisa do Léo e do Davi (preço e teste são deles). Referência de mercado: 17-32 dias convertem 42,5% vs 25,5% em menos de 4 dias (RevenueCat 2026). Só desenhar depois de saber o teste atual.
