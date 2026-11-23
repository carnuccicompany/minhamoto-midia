# Canal do Shelby — versão 1 (23/11)

Como o Léo e o Davi recebem as informações do Shelby e dos diretores. Rascunho pra refinar entre 23 e 24/11.

## Princípio: o dono não recebe o dia todo

O Léo é o dono. Problema pequeno se resolve entre o Shelby e os diretores e **não chega nele**. Só chega:
1. **decisão que só o Léo ou o Davi podem tomar;**
2. **resultado da semana e do mês:** melhorou ou piorou, por quê, o que muda;
3. **informação realmente relevante** (ex.: segurança, algo que custa dinheiro).

Chega em **momentos fixos**, nunca em fluxo contínuo. Sempre no **mesmo lugar** (um link fixo) e com a **mesma estética** (dossiê do império, preto e ouro, carimbos). Só o conteúdo muda.

**Regra de ouro dos números:** este repositório é público. Aqui só entram %, variação e status. Número absoluto (R$, assinantes, verba, custo por assinante) só no privado `carnucci-dados` e no link privado do briefing.

## 1. A agenda (só isso chega)

| Quando | O quê | Chega no celular? |
|---|---|---|
| Dia útil, 7h, **só se houver decisão nova** | Bilhete curto: as decisões em cartões sim/não com a recomendação do Shelby. Sem decisão, **nada chega** | Sim, só nesse caso |
| Segunda, 8h41 | **Plano da semana** (tarefa existente "MM: Plano da semana"): meta em %, 3 prioridades, experimentos | Não |
| Sexta, 19h17 | **Fechamento da semana** (tarefa existente "MM: Fechamento da semana"): a edição principal | Só se tiver decisão |
| Último dia útil do mês, 19h17 | **Fechamento do mês**: tendência do mês, Diretor do Mês, o que muda no mês seguinte | Só se tiver decisão |

Fora disso, o Shelby só fura a agenda por **alerta grave** (chave vazada, gasto fora do teto, app fora do ar). Nunca por "rodou ok".

## 2. A edição de sexta (revista do império)

Cada edição tem uma **ilustração de destaque** própria e visuais desenhados (gráficos, carimbos, cartões, retratos estilizados dos diretores em SVG, sem rosto real nem personagem de filme). Ordem fixa:

1. **Decisões pendentes no topo**, cartões sim/não com recomendação, custo e o que destrava.
2. **Resultado da semana vs. a anterior**, em %, com uma linha de "por quê" e "o que muda".
3. **Destaques e quem caiu**: ranking com retratos, Diretor da Semana, folha (multas e elogios).
4. **O que o Shelby resolveu sozinho**: 1 linha por item, sem pedir nada.
5. **Próximos passos** da semana seguinte.

Abas fixas do link: **Semana** (edição atual), **Decisões** (tudo que espera o Léo ou o Davi), **Mês**.

## 3. Respostas do Léo

O Léo marca sim/não no link e copia a resposta gerada pra conversa com o Claude (ou responde no chat). O Claude:
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
5. **Estética:** (a) Dossiê — preto e ouro, carimbos (protótipo) (b) Cartel — papel pardo, vermelho e fotos em halftone desenhadas
