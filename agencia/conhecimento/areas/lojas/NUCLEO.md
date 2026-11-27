# Lojas e clientes · NÚCLEO (ler em TODA tarefa)

Para: Jeff Bezos e Ted Lasso. Reescrito em 27/11/2026 pelo professor-chefe (treino do rodízio). Curto de propósito: o resto está na biblioteca (índice no fim). Antes de propor, busque o tema: `grep -ril "<tema>" agencia/conhecimento/areas/lojas/`.

## 1. Correções do Léo (nunca repetir)
- App MinhaMoto **sem teste grátis**: nada de "grátis", "teste" ou "X dias" em loja, anúncio, print ou resposta de avaliação (20/11).
- Preço: pode "R$19,90", nunca "por mês"; imagens e vídeos dentro da App Store **sem preço** (Apple 2.3.14) (24/11). Nunca "vitalício". Sem Black Friday (19/11).
- **Anúncio → landing → loja** (26/11): a loja é a última etapa; a promessa do anúncio tem que estar na página.
- Nada vai à loja, gasta dinheiro ou mexe no app sem OK do Léo/Davi. Resposta de 1 a 3★ só com OK do Léo; 4–5★ o Ted responde pelo guia. Avaliações rodam 1x/dia (25/11).
- Não perguntar de novo: Kavoo + UTMify; garantia de 30 dias; meta em degraus e custo máximo por assinante no privado (23/11). O que está em página pública não vira pergunta (22/11).
- Repositório público: nada de R$ da empresa, número absoluto de assinantes/avaliações, chave, e-mail ou nome de cliente. Vazamento de chave é prioridade máxima (23/11).

## 2. As regras que mais mexem em venda
1. **Promessa contínua:** o que o anúncio promete aparece no print 1 da página (padrão ou personalizada), com tela real da **versão publicada** (não do `main`).
2. **Só prometer o que todos recebem:** nada de "seu modelo" até o Davi confirmar a cobertura (troca: "Plano de revisão por km e tempo").
3. **3 primeiros prints com legenda de benefício** (até 6 palavras), testados pelo PPO (Apple) e pelo experimento de gráficos (Play); barra +10% relativo visita→download, com linha de base.
4. **Nota:** pedido de avaliação só depois de vitória ("Registrar serviço"), nunca depois de erro; 1★ respondido rápido (com OK do Léo). Nota só se prova com histórico guardado + nota oficial do Console.
5. **Régua é assinante pago**, não download. Base pequena: "1 de 3", nunca "33%".

## 3. Lições recentes da casa (detalhe e prova em LICOES.md)
- 27/11: pergunta ao Léo com prazo vai pelo QG no mesmo dia, com a data-limite (o 1★ ec124592 espera OK desde 20/11).
- 26/11: prova que depende de horário se agenda antes de sair da rodada.
- 24/11: coleta boa = `status` ok **e** idade ≤ 48 h (o script regrava o arquivo mesmo com erro).
- 24/11: a API do Play só mostra os últimos dias (provável ~7); guardar histórico.
- 24/11: ficha/página personalizada só quando o canal que manda tráfego existe.
- 23/11: fonte que não abriu = "a conferir" com link, nunca fato.

## 4. Novidades que mudam o trabalho (detalhe em NOVIDADES.md)
- **Prazo Apple 12/01/2027** (classificação etária, novos descritores): 46 dias em 27/11, **sem dono registrado**. Resposta provável "não" (o app não pede localização), mas quem responde é Léo/Davi.
- **30/09/2026 · Verificação de desenvolvedor Android no Brasil:** app não registrado pode sair do Play. Davi confere na Home do Play Console.
- **ECA Digital:** fiscalização da ANPD a partir de jan/2027; decidir se o app lê o sinal de idade da loja.
- 29/09 Play e 04/11 Apple: mensagem/oferta de retenção no cancelamento (proposta pro Stark; desconto só com OK do Léo).
- 16/10 Apple 2.3.14 (sem preço nos assets) e 2.5.19 (nada escondido na versão pública).
- Target SDK: o `main` já está em 36; confirmar a build publicada.

## 5. Regras da aula nova (CPP e fichas personalizadas)
1. **Uma página por ângulo de anúncio**, no máximo 2 no começo; nunca uma por criativo. Ligar pelo OneLink da landing (`af_ios_store_cpp=<ppid>`), sem mexer na campanha.
2. **Print 1 da página = promessa do anúncio** em até 6 palavras; prints e vídeos sem preço, "grátis", "teste", "X dias", "vitalício" ou "promoção"; por cautela, sem preço também no texto promocional.
3. **CPP não é teste A/B:** pra saber se vence, dividir o link da landing (metade CPP, metade padrão) ou usar o PPO. Ler no App Analytics (depois de 5 primeiros downloads) e decidir por custo por assinante.
4. **Android depois:** ficha personalizada do Play (`&listing=`) só com campanha Android com verba.
5. **Toda página passa pela revisão da Apple** (sem precisar de versão nova) e é enviada por Léo/Davi; o setor entrega o pacote pronto e o parecer de regra.

## 6. Índice da biblioteca
- `FUNDAMENTOS.md`: §1 funil da loja · §2 ASO · §3 avaliações e respostas · §4 regras da Apple · §5 regras do Google Play · §6 voz do cliente · §7 rotina sênior · índice de aulas.
- `aulas/2026-11-27-paginas-de-produto-personalizadas.md`: CPP (até 70) e fichas do Play (até 50), limites, revisão, OneLink, números, erros, regras da casa.
- `NOVIDADES.md` (com fonte e data) · `LICOES.md` (acertos e erros, com prova) · `FONTES.md` (oficial primeiro).
- Fora da pasta: `agencia/memoria/decisoes.md`, `agencia/DESIGN-MINHAMOTO.md`, `agencia/demandas/entregas/D-*lojas*`.
