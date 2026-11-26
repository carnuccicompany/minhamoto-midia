# Pacote ao Davi (Shelby, 23/11/2026; itens 11 e 12 somados em 24/11 de manhã; 13 a 16 somados em 24/11 à noite; 17 a 19 somados em 26/11) · cobre D-20261122-produto-3, D-20261122-dados-1 e as perguntas bloqueadas dele

Só o Davi responde. Uma mensagem, sim/não em cada item. O que o código de 17/11 já respondeu (Jobs e Stark leram, só leitura) saiu da lista.

1. **SDK AppsFlyer na build de 23/11?** O Léo disse em 18/11 que entra. Confirma? E manda `onboarding_complete`, `paywall_view` e "moto cadastrada" (sim/não pra cada)? Se só der um, o SDK.
2. O `appsflyerID` vai pro RevenueCat (sim/não)? Sem isso a compra não volta pra campanha.
3. O modelo da moto vira propriedade do usuário (sim/não)? Sem isso não existe % por modelo.
4. O botão "Testar aviso em 1 minuto" (`VITE_MM_AVISO_TESTE`) está fora da versão pública? Se for, o cliente acha antes de nós.
5. A tela "Esse é o MinhaMoto" (plano antes do paywall) continua na build de 23/11?
6. O plano de revisão cobre CG 160, Pop 110i, Biz e Bros 160? E moto sem plano: o que o usuário vê?
7. A moto é escolhida numa lista, sem digitar o modelo? Tem anúncio na tela? A conta guarda o histórico entre aparelhos?
8. Já existe pedido de avaliação, e só depois de "Registrar serviço", nunca após erro de sincronização?
9. O banco do app guarda a data de fim do onboarding e do cadastro da 1ª moto, por plataforma? Se sim, passa só a contagem por dia, sem dado de cliente.
10. Libera 5 prints ou gravações 9:16 da versão nova, sem dado de cliente, até 27/11?
11. **A build de 23/11 mantém igual o selo "Documento vencendo" da Garagem** (licenciamento, 30 dias ou menos) **e continua sem notificação push de documento?** Hoje (código de 17/11, versão 1.0.1) o selo existe só dentro do app e o planejador não trata documento. Se "não", descreve o que mudou. (D-20261124-produto-1; fonte: entregas/D-20261123-mercado-3.md)
12. **A build de 23/11 mantém igual as telas Histórico, Saúde e Notificações** usadas nos vídeos A1 e B1? Se "não", descreve o que mudou, que a cena é refeita antes de ir ao ar. (D-20261124-produto-1; fonte: entregas/D-20261123-cria-3.md)

13. **Logo após o cadastro da moto, o app já tem os dados pra montar o plano daquela moto (sem o km da configuração)?** (P-001, seção 4; D-20261124-produto_analista-do-paywall-1). Recomendo: sim, é o mesmo cálculo do briefing. Se "não", a proposta vira "plano em km médio do modelo".
14. **Dá pra dividir 50/50 por flag remota, sem build nova?** (P-001). Se "não", o teste só entra numa build futura e a leitura espera.
15. **Posso preparar um rascunho de código num branch separado, sem merge, depois do seu OK na P-001?** (P-001). Recomendo: sim, só depois do OK; nada é escrito antes.
16. **A build de 23/11 já está nas lojas? Qual versão e que dia?** (D-20261124-produto-3, P1). Sem a data, o vigia de 72 h, a 1ª leitura do funil e a P-001 ficam com o relógio errado. É a pergunta que vai primeiro.

17. **O "em até 48 horas" para pedir modelo de moto que falta é cumprido hoje?** (D-20261124-produto_analista-do-paywall-2, de D-20261124-produto-4, pergunta 1.) Se "não", o texto sai do app de qualquer jeito, sem prazo. Recomendo: responder com o que acontece de fato; nada é prometido antes da resposta.
18. **Dá pra pôr o cartão "Pedir este modelo" dentro da lista (busca sem resultado) e levar marca e texto buscado no corpo do e-mail, sem mexer no servidor?** (mesma demanda, pergunta 2.) Recomendo: sim, é o mesmo cartão que já existe; só vale depois do OK do Davi e do Léo, nada vai ao ar antes.
19. **Na build de 23/11, a tela "Esse é o MinhaMoto" ainda completa o plano com 6 itens genéricos (óleo, vela, filtro de ar, pastilhas, corrente, fluido) quando o modelo tem poucos itens?** (mesma demanda, pergunta 3; `esse-e-o-minhamoto.tsx:35-60` no código de 17/11.) Se "sim", o Davi diz se aceita isso como "plano da moto". Liga com o item 6 (moto sem plano), mas pergunta outra coisa: aqui é o complemento genérico, lá é a cobertura por modelo.

Contexto dos itens 17 a 19 (Jobs, entregas/D-20261124-produto-4.md, código de 17/11): quem tem moto fora da lista **não chega ao paywall** (o paywall só abre depois da moto cadastrada), então esse grupo some antes da etapa "paywall visto". Não há dado do tamanho do grupo; só medir com os eventos do item 1.

Recomendação do Shelby nos itens 11 e 12: responder "sim, igual" é o caminho mais barato. Enquanto o Davi não responde, A1/B1 e as séries de IPVA só podem dizer "avisa na Garagem, dentro do app" e nunca "te avisa por notificação do CRLV/CNH" (08-regras.md: promessa que o app não cumpre vira reprovação e 1 estrela). O item 5 acima (tela "Esse é o MinhaMoto") é outro assunto, não duplica.

Quem deve o quê depois da resposta: Stark confere cena por cena (cria-3), Turing monta a linha de base, Escobar libera o D+0 de medição (verba continua zero até lá).
Status: texto pronto; vai ao Davi no bilhete de decisões. Nada decidido por mim.
