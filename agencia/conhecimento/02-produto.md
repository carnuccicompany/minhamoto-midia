# MinhaMoto

_Status: pré-preenchido pelo Claude em 23/11/2026; inclui também o produto dos Corretores. Última atualização: 23/11/2026_

## Fatos

### MinhaMoto (app de assinatura)
- App pra motociclista cuidar da moto: **plano de revisão por modelo e km**, histórico de manutenção, saúde da moto (em dia, atenção, vencido, acompanhamento, sem histórico), combustível e consumo, documentos, gastos, várias motos na garagem, notificações de marcos. (ficha do produto, `agencia/estudio/produtos/minhamoto.md`)
- Lojas: App Store (id 6815447825) e Google Play (com.carnuccicompany.minhamoto). (Léo, 16/11)
- Preço de vitrine: "por R$19,90" (preço público da loja); descontos no trimestral, semestral e anual. Nunca "vitalício" (oferta antiga). (Léo, 16/11)
- **Não existe teste grátis.** Fluxo: onboarding → cadastro da moto → paywall pago direto. Ninguém escreve "grátis" ou "X dias". (Léo, 20/11)
- Paywall não se mexe agora (preço, ordem dos planos); só volta a ser proposto com dado de funil. (Léo, 20/11)
- Próxima build (semana de 23/11): estética nova + SDK do AppsFlyer. (Léo, 18/11)
- Falha de sincronização no Android: o Davi corrige depois da build de 23/11. (Léo, 19/11)
- Diferencial a explorar: plano por modelo, sem digitar a moto (concorrente Drivvo recebe reclamação de modelo digitado). [rascunho do Claude — confirmar que o app escolhe a moto numa lista]
- **Fluxo do app (código de 17/11, a confirmar com o Davi na build de 23/11):** boas-vindas, cadastro da moto (marca, modelo, versão), configuração (km, respostas, cuidados, ritmo), diagnóstico (briefing de 4 telas), tour, "Esse é o MinhaMoto" (itens reais do plano da moto, até 6) e paywall pago direto. O plano da moto já aparece antes do paywall, só que no fim do caminho. O código lido não tem SDK do AppsFlyer nem eventos de funil. Moto sem plano disponível: a tela do plano não aparece. (Jobs, leitura do código, D-20261122-produto-1; registrado pelo Shelby em 23/11)
- **Documentos e avisos (código de 17/11):** o app guarda o vencimento do licenciamento e mostra o selo "Documento vencendo" na Garagem aos 30 dias. Não achei push de documento nem aviso de CRLV ou CNH. Texto de anúncio pode dizer "o app avisa na Garagem", não "te notifica". (Stark, D-20261123-mercado-3)

### Corretores (infoproduto)
- **Mapa Visual Completo do Fechamento Imobiliário**: 125 mapas visuais sobre tudo que vem depois do "sim" do cliente (formas de aquisição, crédito, FGTS, documentação, contrato, cartório, vistoria e chaves). Material de consulta, não curso. Digital, acesso vitalício, garantia de 30 dias, venda pela Kavoo. (página de vendas, 23/11)
- Ofertas: Acesso Essencial (só o Mapa) e Pacote Completo (Mapa + 5 complementares: WhatsApp pronto, 10 quebras de objeção, guia da reunião pós-aceite, 2 planilhas). (página, 23/11)
- 4 order bumps nos dois checkouts: Dicionário Visual do Imóvel, 37 Mapas de Perfis de Compradores, Cálculos do Mercado Imobiliário na Prática, Carisma Aplicado à Venda de Imóveis. Todos validados e vendem. (Léo e checkout, 23/11)
- O Léo garante: o material é muito bom, preenche um gap real do mercado e entrega o que promete. (Léo, 23/11)

## Perguntas pro Léo
- [x] O que o app faz, em uma frase que um motoqueiro entende? → "Tudo da sua moto num lugar só" (Léo, 23/11).
- [x] Quais as 5 funções que mais seguram o assinante? → Ainda sem dado; a aposta é plano de revisão, lembretes, histórico e documentos (Léo, 23/11). Turing confirma quando o RevenueCat/AppsFlyer tiverem uso por função.
- [x] Planos e preços hoje? (teste grátis: NÃO existe, fato do Léo de 20/11/2026) (vitrine "por R$19,90", trimestral/semestral/anual com desconto)
- [x] O que vem nas próximas versões? → Depois da build desta semana (estética + AppsFlyer): foco máximo em VENDER (Léo, 23/11).
- [x] Qual a maior reclamação do produto hoje? → Ainda não sabemos (pouca avaliação) (Léo, 23/11).
