# Lojas e clientes: lições da casa (histórico completo)

Cada acerto ou erro da casa vira lição: data · o que aconteceu · a regra · a prova. Correção do Léo vale mais que qualquer fonte e nunca se repete. Nada se apaga. Mais novo em cima.
Semente de 25/11/2026; treino completo em 27/11/2026 (professor-chefe): demandas e entregas do setor de 20 a 26/11, decisoes.md, DESIGN-MINHAMOTO.md e memórias do setor.

## Correções e decisões do Léo
- **26/11 · Anúncio → landing → loja.** O MinhaMoto começa com tráfego pra landing e dali pra loja; a loja vira a última etapa antes do assinante. Regra: a promessa do anúncio tem que aparecer nos 3 primeiros prints (e, com CPP, no print 1 da página do anúncio). Prova: decisoes.md 26/11; itens/D-20261126-lojas-2.json; aula 2026-11-27.
- **25/11 · Avaliações 1x/dia.** Agentes enxutos: a coleta e a resposta de avaliações rodam uma vez por dia, não a cada rodada. Prova: decisoes.md 25/11.
- **20–22/11 · App sem teste grátis.** Regra: nada de "grátis", "teste", "X dias". Prova: decisoes.md 22/11.
- **24/11 · Preço "R$19,90" sem "por mês"; App Store sem preço.** Prova: decisoes.md 24/11.
- **19/11 · Sem Black Friday.** Prova: decisoes.md 19/11.
- **23/11 · Perguntas já respondidas não voltam ao Léo.** Prova: decisoes.md 23/11.
- **23/11 · Vazamento de chave é prioridade máxima;** repositório público sem e-mail, telefone, R$ ou número absoluto. Prova: decisoes.md 23/11.

## Lições da equipe
- **27/11 (treino) · Pendência do Léo sem relógio fica parada.** O rascunho do 1★ ec124592 espera OK desde 20/11 (7 dias) e a memória do Ted diz "não reavisar". Regra: pergunta ao Léo que tem prazo (avaliação 1★ sem resposta, janela da API) vai pelo QG no mesmo dia, com a data-limite escrita; sem prazo, não reavisa. Prova: memoria/agentes/lojas_respostas-as-avaliacoes.md (20 a 26/11); decisoes.md 23/11 (regra do playbook do Shelby).
- **26/11 · Prova com horário se agenda antes de sair.** A hipótese "a API do Play guarda só 7 dias" vencia 26/11 21h35Z; a rodada terminou sem coleta depois desse horário e a prova ficou pendente. Regra: quando a prova depende de uma hora, deixar a coleta marcada pra depois dela (ou dizer quem dispara), não só anotar "fazer amanhã". Prova: entregas/D-20261126-lojas-1.md.
- **24/11 · Trabalho de loja pra canal sem verba é prematuro.** Ficha personalizada do Play cancelada pelo Shelby: Android fora da 1ª campanha e sem SDK, sem verba. Regra: ficha/página personalizada só quando o canal que manda tráfego pra ela existe. Prova: itens/D-20261124-lojas-3.json.
- **24/11 · Coleta "ok" pode estar quebrada.** `scripts/avaliacoes.py` regrava `ultimas.json` com hora nova mesmo quando uma loja dá erro (as avaliações dela somem do arquivo), e o workflow não tem horário automático. Regra: coleta boa = `status` da loja começa com `ok` E idade ≤ 48 h; aviso de 48 a 120 h (Bezos/Turing), push ao Léo só acima de 120 h. Prova: entregas/D-20261124-lojas-1.md.
- **24/11 · A API do Play mostra só os últimos dias (provável ~7).** 4 de 6 avaliações do Play já vistas sumiram sem avaliação nova (n 3 → 2 → 1). Regra: nota e "nota subiu" só se provam com histórico guardado por nós + nota oficial do Console; nunca com a média da API. Prova: entregas/D-20261123-lojas-1.md; entregas/D-20261126-lojas-1.md.
- **23/11 · Print de loja promete só o que a versão publicada entrega pra todos.** Legendas A1 e B1 ("seu modelo") cortadas: moto sem plano disponível não vê a tela. Troca segura: "Plano de revisão por km e tempo". Regra: nada de "seu modelo" até o Davi confirmar a cobertura. Prova: entregas/D-20261122-lojas-3.md.
- **23/11 · Tela de loja = versão publicada, não o `main`.** Telas renderizadas do `main` mostravam coisa que não existe no app instalado (CM01 r3); os rascunhos de print da D-20261123-lojas-3 saíram marcados "provisório" porque não foram conferidos contra a build. Regra: print de loja só de tela da versão das lojas (número da versão + commit), conferida. Prova: DESIGN-MINHAMOTO.md (23/11, CM01 r3); itens/D-20261123-lojas-3.json.
- **23–26/11 · Fonte bloqueada vira "a conferir", nunca fato (acerto).** O Bezos não afirmou a janela de 7 dias e o Shelby marcou "conferir na fonte" no parecer de regra. Regra: página oficial que não abriu = "a conferir" com o link; não copiar de memória. Prova: memoria/agentes/lojas.md (24/11); entregas/D-20261122-lojas-3.md.
- **22/11 · O que está em página pública não vira pergunta pro Léo.** Ronda do Shelby (D-20261122-master-3): ler título, subtítulo e prints nas páginas das lojas em vez de pedir. Regra: só sobe ao Léo o que nenhum agente consegue ler. Prova: memoria/agentes/lojas.md (22/11, ronda do Shelby).
- **20/11 · Pedido de avaliação só depois de vitória.** Aceito como requisito pelo Stark: dispara depois de "Registrar serviço" concluído, nunca depois de erro de sincronização, 1 vez por usuário por versão; falta o sim/não do Davi sobre o estado atual. Prova: itens/D-20261120-lojas-2.json.
- **20/11 · Extra sem número é ruído e dá multa.** Na Folha de 20/11 o extra do Ted veio como ruído e o diretor levou a multa por não filtrar. Regra: placar curto (até 15 linhas), só o que muda decisão; extra só com número. Prova: itens/D-20261120-lojas-1.json; memoria/agentes/lojas.md (Folha 20/11).
- **20–24/11 ·** Resposta a avaliação de 1 a 3★ só com OK do Léo; 4–5★ pelo guia.
- **20–24/11 ·** Asset promocional dentro da App Store sem preço nem promoção (Apple 2.3.14, 16/10).
- **20–24/11 ·** Base pequena se escreve "1 de 3", não "33%" (média do Play conferida: D-20261122-ted-1).
- **20–24/11 ·** Vigia de avaliações por versão nas 72 h depois de cada build.
