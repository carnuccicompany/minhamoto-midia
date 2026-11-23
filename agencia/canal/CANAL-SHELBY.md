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

## 2a. Estética (decidida pelo Léo em 23/11)

~~Revista do império: preto e ouro, ilustração de capa, carimbos, retratos estilizados dos diretores.~~ Recusada: "muito visual, desenho nada a ver".

**Relatório do conselho de uma holding aos sócios.** Carta de family office, extrato de private bank, board pack de banco. Sóbrio, caro, silencioso; o peso vem da tipografia, do espaço e do rigor.
- Papel marfim, tinta quase preta, um único acento escuro (verde-garrafa); ouro só em fios finos e no monograma. Escuro: carvão com texto marfim.
- Serifada clássica (EB Garamond) em pesos contidos, versaletes nos rótulos, algarismos tabulares.
- Cabeçalho de documento: monograma "C" em traço fino, "CARNUCCI — Relatório ao Conselho", edição nº, data, destinatários, "Estritamente confidencial".
- Seções em romano: I. Resoluções pendentes, II. Resultado da semana, III. Diretoria, IV. Ocorrências resolvidas pela diretoria, V. Próximos passos.
- Números em tabela (atual × anterior × variação ▲▼), no máximo sparkline fina. Ranking como tabela, sem retrato.
- Decisões viram **Resoluções do Conselho nº 2026-11-0XX** com linha de assinatura: Aprovar/Recusar põe o nome do sócio em manuscrito, com data e hora.
- Fecha com o parecer do Diretor-Geral e a assinatura dele.
- Proibido: ilustração, mascote, retrato, carimbo chamativo, cards coloridos, emoji.

## 2. A edição de sexta

Ordem fixa:

1. **Resoluções pendentes no topo**, com recomendação, custo, o que destrava e prazo.
2. **Resultado da semana vs. a anterior**, em %, com uma linha de "por quê" e "o que muda".
3. **Diretoria**: ranking em tabela, Diretor da Semana, advertências e menções da folha.
4. **O que o Shelby resolveu sozinho**: 1 linha por item, sem pedir nada.
5. **Próximos passos** da semana seguinte.

Abas fixas do link: **Semana** (edição atual), **Resoluções** (tudo que espera o Léo ou o Davi), **Mês**.

## 3. Respostas do Léo

O sócio assina Aprovar/Recusar no link e copia o texto gerado ("Resolução nº X — APROVADA por Léo em ...") pra conversa com o Claude (ou responde no chat). O Claude:
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
3. **Link:** (a) um só pro Léo e o Davi (b) um de cada, o do Davi só com produto e app
4. **O Davi recebe:** (a) a mesma edição (b) só as decisões dele + funil do app (c) nada, você repassa
5. ~~**Estética:** Dossiê ou Cartel~~ Decidido: relatório de holding (seção 2a). Nova pergunta: **acento:** (a) verde-garrafa (protótipo) (b) azul-marinho profundo
