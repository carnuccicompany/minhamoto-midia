# Tráfego pago: fundamentos do especialista sênior

Para: Pablo Escobar (Tráfego). Leia a seção que toca a tarefa, não o arquivo inteiro.
Atualizado em 24/11/2026. Novidades da área ficam em `NOVIDADES.md` (sempre leia antes de propor).

## 1. A conta que manda: custo por resultado contra o que o resultado paga
- **Infoproduto (Corretores):** venda única de ticket baixo + order bumps. A régua é o ROAS de front (faturamento ÷ gasto) e o custo por venda, sempre contra a margem real (taxas do checkout, impostos e o acréscimo de tributos que a Meta cobra no Brasil; ver `dados-financas/FUNDAMENTOS.md`). ROAS bonito com margem negativa é prejuízo.
- **App de assinatura (MinhaMoto):** a régua é custo por assinante pago contra o LTV (o que ele paga até cancelar). Sem LTV medido, use payback: em quantos meses a assinatura devolve o custo de aquisição.
- **Como aplicamos aqui:** toda proposta de verba vem com a conta "custo alvo por venda/assinante" e a fonte do número (UTMify, RevenueCat, AppsFlyer). Valores em R$ só no `carnucci-dados`.

## 2. Como o leilão da Meta funciona hoje
- O leilão escolhe o anúncio pelo **valor total**: lance × taxa de ação estimada + qualidade. Criativo melhor reduz o custo sem mexer no lance.
- Desde 2025 o sistema de recuperação de anúncios da Meta (Andromeda) e os modelos de ranqueamento escolhem **qual criativo mostrar para quem**. Consequência prática: o criativo virou a segmentação. Público aberto (broad) + criativos diferentes entre si funciona melhor que muitos públicos fechados.
- **Diversidade de criativo** quer dizer conceito diferente (ângulo, formato, pessoa, cenário), não 10 variações da mesma cor de botão. Variações quase iguais são tratadas como o mesmo anúncio e dividem a mesma entrega.
- **Como aplicamos aqui:** cada teste dos Corretores sobe estilos diferentes (Historinha, Quiz, Split-screen etc.), não pequenas variações. O ângulo novo é o que abre público novo.

## 3. Estrutura de conta
- **Consolidar:** poucas campanhas, cada uma com volume suficiente pra sair do aprendizado. Campanha que não junta cerca de 50 eventos de otimização por semana fica presa no aprendizado (regra pública da Meta).
- **Advantage+ (vendas/app):** automação de público, posicionamento e criativo. Bom quando há sinal de conversão confiável. Ruim quando o pixel/evento está quebrado.
- **CBO vs ABO:** CBO (orçamento na campanha) para escalar; ABO (orçamento no conjunto) para testar criativo com verba garantida.
- **Não mexer toda hora:** edição significativa (orçamento grande, público, criativo, evento) reinicia o aprendizado. Ajuste de verba em degraus de 20 a 30%.
- **Como aplicamos aqui:** teste em ABO com regra de corte escrita antes; vencedor sobe pra campanha de escala. Nunca editar campanha dos Corretores sem OK do Léo.

## 4. Sinal de conversão (sem sinal, não existe otimização)
- **Pixel + API de Conversões (CAPI):** o pixel no navegador perde eventos (bloqueador, iOS). A CAPI manda o evento do servidor. O ideal é os dois, com deduplicação por `event_id`.
- **Qualidade de correspondência (EMQ):** quanto mais dados de correspondência (e-mail, telefone com hash), melhor a Meta liga a venda ao anúncio.
- **Evento de otimização:** otimizar pelo evento mais perto do dinheiro que tenha volume. Se a compra não chega a 50/semana, use uma "escada de evento" (ex.: início de checkout) e suba quando o volume deixar.
- **App:** atribuição de instalação e compra vem do MMP (AppsFlyer) + SKAdNetwork/AdAttributionKit no iOS. Compra dentro do app chega na Meta pelo SDK ou pela integração do RevenueCat com o AppsFlyer.
- **Como aplicamos aqui:** Corretores: conferir que Purchase chega pelo checkout (Kavoo) com valor. MinhaMoto: verba zero até o SDK do AppsFlyer estar na build e o evento de compra chegar (regra do Escobar).

## 5. Atribuição: por que os números nunca batem
- Meta conta por janela (padrão 7 dias clique / 1 dia visualização). UTMify conta por UTM/último clique. Checkout conta a venda. Cada um mede uma coisa.
- iOS: depois do ATT, boa parte das conversões é modelada. SKAdNetwork entrega com atraso e agregado.
- **Teste de incrementalidade** (conversion lift, geo-holdout) responde "quanto o anúncio realmente causou". Usar quando a verba justificar.
- **Como aplicamos aqui:** decisão diária pela UTMify (venda real por anúncio). Meta serve pra diagnóstico de funil (CTR, CPM, custo por clique, visualização da página).

## 6. Leitura de funil do anúncio (diagnóstico em ordem)
1. **CPM** alto: leilão disputado, público pequeno, criativo com baixa qualidade estimada.
2. **CTR (link)** baixo: gancho/criativo fraco. Primeiro segundo do vídeo decide.
3. **Clique → visualização da página** baixa: página lenta ou pesada (já aconteceu: caiu de ~92% pra ~75% em novembro).
4. **Página → início de checkout** baixa: promessa do anúncio não bate com a página, ou oferta fraca.
5. **Checkout → compra** baixa: preço, meio de pagamento (Pix não pago), confiança.
- **Como aplicamos aqui:** toda autópsia de queda passa por essa ordem, com número em cada etapa.

## 7. Regras de corte e escala (escreva antes de gastar)
- Corte: criativo que gastou X vezes o custo alvo sem venda, ou CTR abaixo do piso depois de N impressões. O X e o piso ficam no privado.
- Escala: vencedor estável por alguns dias no custo alvo ganha +20 a 30% de verba por vez, ou é duplicado na campanha de escala.
- Fadiga: frequência subindo + CTR caindo + custo subindo = trocar ângulo. Reposição semanal de criativo, não mensal (novembro mostrou o custo de esperar).

## 8. TikTok Ads
- **Smart+** é a automação de campanha (equivalente ao Advantage+). Para app, campanha de instalação/evento no app; para site, conversão no site com Pixel + Events API.
- Criativo nativo: vertical, gente falando, legenda, primeiros 2 segundos com gancho. Anúncio com cara de anúncio perde.
- Fase de aprendizado: o TikTok usa ~50 conversões como sinal principal pra sair do aprendizado (Help Center).
- **Como aplicamos aqui:** TikTok só depois do app medido (SDK) e do app de dados TikTok aprovado; começar com os vídeos que já venceram na Meta.

## 9. Políticas e risco de conta
- Promessa de resultado financeiro, antes/depois, "renda garantida", alegação sem prova: reprovação e risco de bloqueio. Imóveis/corretores podem cair em "práticas comerciais" se prometer ganho.
- Conta de anúncio cai em cascata (BM, perfil, página). A Perfect Class já perdeu uma BM. Contingência (BM e perfis de reserva) é proteção, não luxo.
- **Como aplicamos aqui:** todo texto de anúncio passa pelo check de promessa do Shelby. Nada de "grátis" no MinhaMoto (não há teste grátis).

## 10. O que um sênior faz toda semana
- Lê o placar por anúncio, corta o que queima, propõe escala do que vende.
- Pede criativo novo à Disney antes da fadiga, com o ângulo que o dado sugere.
- Confere se o rastreamento continua de pé (evento chegando, valor certo).
- Lê `NOVIDADES.md` e as fontes oficiais; mudança de política ou produto vira demanda.

---
## Índice da biblioteca completa (atualizado em 25/11/2026)
Camadas: `NUCLEO.md` (ler em toda tarefa) → este arquivo + `aulas/` (buscar o tema com grep) → `NOVIDADES.md` e `LICOES.md` (histórico com data e prova).

| Data | Aula | Tema |
|---|---|---|
| 2026-11-25 | `aulas/2026-11-25-teste-de-criativo-meta-pos-andromeda.md` | Teste de criativo na Meta depois do Andromeda |
