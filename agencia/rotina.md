# Rotina da Agência MinhaMoto

Como os 6 agentes trabalham juntos, sozinhos, todo dia.

## Ciclo diário de produção (sessão automática, de manhã)

```
1. VIGIA DE ESTOQUE
   Lê fila/carrosseis.json + estado.json → quantos dias de fila restam?
   ≥ 14 dias → produz a cota normal do dia (2 carrosséis novos)
   < 14 dias → produz 4/dia até recompor
   < 7 dias  → produz 6/dia + push URGENTE pro Léo

0. TODOS leem agencia/DESIGN-MINHAMOTO.md (régua do Léo) antes de começar.
2. PAUTEIRO     → briefings pela MATRIZ de ângulos (público × gancho × linha).
   ↳ REVISOR · Portão 1 (pauta)   → reprovou volta pro pauteiro.
3. ROTEIRISTA   → roteiros JSON a partir dos briefings aprovados (tom premium, telas indicadas).
   ↳ REVISOR · Portão 2 (roteiro) → reprovou volta pro roteirista.
4. DESIGNER     → renderiza (carrossel 4:5 + versão TikTok 9:16, vídeos, stories), confere card a card.
5. REVISOR · Portão 3 (peça)     → revisar_video.py + zoom + nota ≥9 em tudo. Aprovou → fila/preview. Reprovou → volta (máx. 2 rodadas).
6. PUBLICADOR   → confere saúde do sistema (workflow, slots de ontem, fila ordenada), commita e dá push no repo.
7. RELATO       → push notification pro Léo: "Produzidos X carrosséis (IDs), fila com Y dias. Z precisa de atenção."
```

O que o Léo recebe por dia: **uma notificação de resumo**. Só é acionado de novo se algo quebrar.

## Ciclo semanal (segunda de manhã)

```
ANALISTA → lê dados/insights-*.json da semana
         → escreve dados/relatorios/{data}.md
         → grava as diretrizes (DOBRAR/CORTAR/TESTAR) no topo do BANCO.md
         → push pro Léo com o placar em até 10 linhas
```

## Publicação (já roda sozinha, 24/7)

- GitHub Actions a cada 15 min → slots 12h/15h/18h/21h BRT → IG + FB automático.
- TikTok: notificação no celular + tiktok.html (Léo posta em ~30s).

## Papel do Léo (e do Davi)

- Ler o resumo diário. Silêncio = tudo certo.
- Lapidar: qualquer ajuste de estilo/tom vira edição no MANUAL.md — os agentes obedecem o manual, então lapidar o manual lapida todos de uma vez.
- Davi: mandar os carrosséis dele → entram na fila intercalados (Publicador cuida).
- Mandar parar: "pausa as postagens" → `"pausado": true` no estado.json.

## Regras de ouro da operação

1. **Nunca ficar sem post.** O vigia existe pra isso. Fila < 7 dias é emergência.
2. **Nada chega no feed sem passar pelo Revisor.** Nem com pressa, nem "só dessa vez".
3. **O MANUAL manda.** Conflito entre agente e manual → manual ganha. Conflito entre manual e Léo → Léo ganha (e o manual é atualizado na hora).
4. **Falha nunca é silenciosa.** Qualquer coisa fora do padrão → push pro Léo.
5. **Não mexer na estrutura de pastas do Léo** (6 FIGURES/MinhaMoto). Pastas novas ok, mexer no que existe não.

## O que ainda não entra na rotina (aguardando o Léo)
- Reels (2/dia) e stories — formato em discussão.
- Respostas a comentários/DMs — precisa de permissão extra na Meta.
- Dados de loja e RevenueCat no relatório — precisa de acesso na sessão do Analista.
