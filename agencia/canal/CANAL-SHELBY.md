# Canal do Shelby — versão 1 (23/11)

Como o Léo e o Davi recebem as informações do Shelby e dos diretores. Rascunho pra refinar entre 23 e 24/11.

## Princípio: o dono não recebe o dia todo

O Léo é o dono. Problema pequeno se resolve entre o Shelby e os diretores e **não chega nele**. Só chega:
1. **decisão que só o Léo ou o Davi podem tomar;**
2. **resultado da semana e do mês:** melhorou ou piorou, por quê, o que muda;
3. **informação realmente relevante** (ex.: segurança, algo que custa dinheiro).

Chega em **momentos fixos**, nunca em fluxo contínuo. Sempre no **mesmo lugar** (um link fixo) e com a **mesma estética** (ver seção 2a). Só o conteúdo muda.

**Regra de ouro dos números:** este repositório é público. Aqui só entram %, variação e status. Número absoluto (R$, assinantes, verba, custo por assinante) só no privado `carnucci-dados` e no link privado do briefing.

## 1. A agenda (só isso chega)

| Quando | O quê | Chega no celular? |
|---|---|---|
| Dia útil, 7h, **só se houver decisão nova** | Bilhete curto: as decisões em cartões sim/não com a recomendação do Shelby. Sem decisão, **nada chega** | Sim, só nesse caso |
| Segunda, 8h41 | **Plano da semana** (tarefa existente "MM: Plano da semana"): meta em %, 3 prioridades, experimentos | Não |
| Sexta, 19h17 | **Fechamento da semana** (tarefa existente "MM: Fechamento da semana"): a edição principal | Só se tiver decisão |
| Último dia útil do mês, 19h17 | **Fechamento do mês**: tendência do mês, Diretor do Mês, o que muda no mês seguinte | Só se tiver decisão |

Fora disso, o Shelby só fura a agenda por **alerta grave** (chave vazada, gasto fora do teto, app fora do ar). Nunca por "rodou ok".

## 2a. Estética (decidida pelo Léo em 23 e 24/11)

~~Revista do império: preto e ouro, ilustração de capa, carimbos, retratos estilizados dos diretores.~~ Recusada (23/11): "muito visual, desenho nada a ver".

~~v2: papel marfim, tinta preta, verde-garrafa, monograma "C".~~ Recusada em parte (24/11): estrutura e medições aprovadas; marrom/marfim "xoxo".

**Relatório do conselho de uma holding aos sócios (v3, 24/11).** Minimalista, premium, luxuoso, moderno, corporativo. O peso vem da tipografia, do espaço e do rigor.
- **Paleta:** preto (fundo ~#070708, papel ~#0E0F10), branco/marfim claro no texto, dourado champanhe (~#C9A55C) em fios, logo e rótulos, verde-água (~#3CBFAE) como acento e cor do positivo, vermelho discreto (~#CF5A4E) no negativo. Tema escuro é o padrão; o claro é papel branco limpo (nunca bege).
- **Logo real da Carnucci** (3 arcos) em dourado no topo, com fio dourado fino. Nunca o monograma genérico.
- Serifada clássica (EB Garamond) em pesos contidos, versaletes nos rótulos, algarismos tabulares. (O Léo gostou da fonte: manter.)
- Seções em romano: I. Resoluções pendentes, II. Resultado da semana, III. Diretoria, IV. Ocorrências resolvidas pela diretoria, V. Próximos passos.
- Números em tabela (atual × anterior × variação ▲▼), no máximo sparkline fina. Ranking como tabela, sem retrato.
- **Resoluções como missões** (gamificado, mas elegante): insígnia P1/P2/P3, contagem regressiva do prazo, "o que destrava", barra de impacto; placar no topo com "N resoluções pendentes", barra que enche a cada assinatura e sequência de dias decidindo; lacre que carimba ao fechar; "Mesa limpa" quando zera.
- **Assinaturas animadas:** Léo, Davi e Thomas Shelby aparecem sendo escritos (traço vetorial, ~1,6 s). Hoje são desenhadas a partir de fonte manuscrita. **Se o Léo e o Davi mandarem foto da assinatura real, a gente vetoriza e troca.**
- Fecha com o parecer do Diretor-Geral e a assinatura dele.
- Proibido: ilustração, mascote, retrato, cards coloridos, emoji.

## 2b. Dupla assinatura (regra do Léo, 24/11)

- **Um briefing só pros dois** (mesmo link, mesma edição) — respostas 3 (a) e 4 (a).
- Toda resolução precisa das **duas** assinaturas. Léo assina → "Assinada por Léo · aguardando Davi" (lacre "1 de 2", meia barra). Só com os dois aprovando vira **APROVADA**; os dois recusando, **RECUSADA**; um aprova e o outro recusa → **DIVERGÊNCIA — conversar**.
- **Onde fica gravado:** no banco de dados do próprio artifact (capacidade `db`, coleção `assinaturas`, um documento por resolução com `leo` e `davi` = decisão + hora). Os dois veem o mesmo estado em qualquer aparelho. Como o Léo e o Davi usam a mesma conta do Claude, a página não sabe quem está olhando: quem assina escolhe "Assinando como Léo/Davi" (botão no topo).
- **Limitação:** se o banco não responder (sem rede, conta deslogada), a página guarda as assinaturas só naquele aparelho e avisa; aí vale o texto copiado pro Claude.

## 2. A edição de sexta

Ordem fixa:

1. **Resoluções pendentes no topo**, com recomendação, custo, o que destrava e prazo.
2. **Resultado da semana vs. a anterior**, em %, com uma linha de "por quê" e "o que muda".
3. **Diretoria**: ranking em tabela, Diretor da Semana, advertências e menções da folha.
4. **O que o Shelby resolveu sozinho**: 1 linha por item, sem pedir nada.
5. **Próximos passos** da semana seguinte.

Abas fixas do link: **Semana** (edição atual), **Resoluções** (tudo que espera o Léo ou o Davi), **Mês**.

## 3. Respostas do Léo

Os dois sócios assinam Aprovar/Recusar no link (seção 2b) e um deles copia o texto gerado ("Resolução nº X — APROVADA — Léo aprovou em ...; Davi aprovou em ...") pra conversa com o Claude (ou responde no chat). O Claude também pode ler direto as assinaturas gravadas no banco do artifact. Só entram em decisoes.md as resoluções APROVADAS ou RECUSADAS pelos dois. O Claude:
- grava uma linha em `agencia/memoria/decisoes.md` (data, decisão, quem decidiu);
- fecha a demanda no `demandas/quadro.json` (status `decidida`);
- a decisão sai da aba Decisões e aparece como "decidido" na edição seguinte.

## 4. De onde vem cada bloco

| Bloco | Fonte pública (minhamoto-midia) | Fonte privada (carnucci-dados) |
|---|---|---|
| Decisões | `agencia/demandas/quadro.json` (bloqueadas pelo líder) e `conselho/rodadas/*/master.md` | — |
| Veredito, gargalo | `agencia/conselho/` | — |
| Ranking, Diretor da Semana/Mês | `agencia/merito/boletins/ultimo.json`, `merito/hall.json` | — |
| Folha | `agencia/merito/folhas/` | — |
| Resolvido sozinho | `agencia/coordenador/status.json`, ata do Conselho | — |
| Cadastro, experimentos | `agencia/cadastro/status.json`, `agencia/experimentos/placar.json` | — |
| Venda, assinantes, meta | — | `resumo/diario.json`, `resumo/meta_pct.json`, `resumo/funil.json` |
| Anúncios | — | `dados/meta_ads/`, `dados/utmify/` |

## 5. Onde mora

**Artifact privado com link fixo** ("Briefing do Shelby"), republicado no mesmo endereço a cada edição. Só o Léo vê até compartilhar com o Davi. O `painel.html` do GitHub Pages não serve: é público.

## 6. Quem escreve

- **MM: Fechamento da semana (sex 19h17):** monta a edição de sexta e republica o link. No último dia útil do mês, monta também a aba Mês.
- **MM: Plano da semana (seg 8h41):** atualiza a aba Semana com o plano.
- **MM: Reunião do Conselho (19h23):** grava cada decisão no formato de cartão (pergunta, recomendação, custo, destrava) e marca se é **nova**.
- **Nova tarefa "MM: Bilhete das decisões" (dia útil 6h47):** se houver decisão nova desde o último aviso, republica a aba Decisões e manda **um** aviso no celular. Se não houver, termina sem fazer nada.
- **Coordenador (:09/:39):** registra falha e auto-correção no `status.json`; não avisa o Léo.

## 7. Perguntas pro Léo (múltipla escolha)

1. **Bilhete de decisões:** (a) 7h, só quando houver decisão (b) junto do plano de segunda e do fechamento de sexta, nunca em outro dia (c) 12h
2. **Aviso no celular (só pra decisão):** (a) push do Claude (b) e-mail (c) os dois
3. ~~**Link:** (a) um só (b) um de cada~~ Decidido (24/11): **um link só pros dois**.
4. ~~**O Davi recebe:** ...~~ Decidido (24/11): **a mesma edição, com dupla assinatura** (seção 2b).
5. ~~**Estética / acento**~~ Decidido (24/11): preto, branco, dourado e verde-água (seção 2a).
