# D-20261122-mkt_publicador-2 · Plano de reposição da fila por linha

Autor: Walt Disney (cria) · 23/11/2026 · Base: tabela de dias por linha de `D-20261122-cria-1.md` (Fogg), conferida por mim contra `fila/carrosseis.json` e `fila/estado.json` (89 pendentes, ordem estrita do arquivo: `scripts/publicar.py` publica o primeiro não publicado, sem cota por linha). Nada foi publicado nem mexido na fila.

## Conta
- A fila sai na ordem do arquivo. Dia do post na posição p, a 4 por dia, com início em 23/11: dia = 23/11 + parte inteira de (p-1)/4. Posições pendentes por linha (recontadas): Curtos AIDA 4, 20, 32; Educacional 5, 15, 17, 26, 35, 45; Marcas até 72; Junto com a chave até 75; Dicas 1 até 86; Dicas 2 até 87; Tutorial até 88; Temas gerais até 89.
- "Secar" = o último pendente da linha sair. Meta pedida: nenhuma linha seca antes de 04/12. O post da posição 45 sai em 04/12; então toda linha precisa de pendente na posição 45 ou depois.
- Só duas linhas não cumprem ou cumprem no limite: **Curtos AIDA** (último na posição 32, seca em 30/11, 4 dias antes da meta) e **Educacional** (último na posição 45, seca em 04/12 exato, zero folga). As outras seis passam de 10/12.

## Plano (quantas peças novas, por linha, até quando)

| Linha | Pendentes hoje | Peças novas | Entrega na fila até | Posição sugerida no arquivo (dia a 4/dia) | Seca depois do plano |
|---|---|---|---|---|---|
| Curtos AIDA | 3 | **+5** | 1ª até 29/11; 2ª a 5ª até 03/12 | 40 (02/12), 50 (05/12), 60 (08/12), 70 (10/12), 80 (12/12) | 12/12 |
| Educacional | 6 | **+3** | até 03/12 | 55 (06/12), 65 (09/12), 75 (11/12) | 11/12 |
| Demais 6 linhas | 80 | 0 por ora | - | - | entre 10/12 e 15/12 |

Total de peças novas: **8** (mínimo para cumprir a meta de 04/12: 1 Curtos AIDA na posição 45 ou depois, mais 1 Educacional de folga, ou seja, 2 peças; recomendo as 8 porque 1 peça deixa Curtos AIDA sem nada por 3 dias de 30/11 a 02/12, e é a única linha de venda direta).

Se o ritmo real ficar em 2 por dia (como em 21 e 22/11): Curtos AIDA seca em 08/12 e Educacional em 15/12 sem reposição; a 1ª peça nova de Curtos AIDA tem que estar na fila até 06/12. O plano acima cobre os dois ritmos.

### De onde vêm as 5 de Curtos AIDA
Do Lote zero (`D-20261122-master-2.md`): os roteiros 1, 2, 3, 4 e 6 viram carrossel de venda (decisão do Shelby de 22/11: "5 viram carrossel Curtos AIDA"). O texto é meu, até 26/11 (3 dias antes da 1ª entrega). A arte e a montagem dos cards, hoje, só saem pela tarefa "MM: Produção diária de conteúdo", que está desativada desde 18/11 (`D-20261122-cria-1.md`, seção 2).

### De onde vêm as 3 de Educacional
Do pauteiro (fila de pautas do banco de ideias, seção "Do radar (24/11)" de `agencia/pautas/BANCO.md`): "Mito: app de manutenção é tudo igual" e "A conta do plano de frota que ninguém com uma moto só deveria pagar" já são de tema educacional e saem sem citar marca. A terceira escolho no banco depois da leitura dos insights. Texto meu, até 29/11.

## O que depende de aprovação do Léo
1. **Religar "MM: Produção diária de conteúdo" só pra essas 8 peças** (ou autorizar outra forma de montar os cards), sem tocar nas outras 80 e sem reativar pauteiro/roteirista (o Shelby negou por ora em 20/11; eu escrevo o texto). Sim/não. Sem isso, nada do plano sai da página.
2. A decisão A/B de vídeo (27/11) é outra coisa: este plano é só de carrossel. Mas a `PENDENCIAS.md` registra que religar a produção diária também espera a direção; por isso peço o sim restrito acima, separado do A/B.
3. Inserir as peças em posições intermediárias exige mudar a ordem de `fila/carrosseis.json`, que hoje é do Fogg. Proposta: ele insere conforme a coluna "posição sugerida", só de peça já aprovada pelo Shelby. Sem inserção, as peças entram no fim e saem só a partir de 15/12, o que não resolve nada.

## O que não está provado
- Quantas peças saem por dia: usei 4 (meta). O real é incerto (causa em `D-20261122-cria-1.md`).
- Se Curtos AIDA rende mais que as outras linhas: **não sei**. Não existe insight por post (`dados/relatorios/2026-11-23.md`: a Meta nega a permissão de insights ao token). Escolhi Curtos AIDA por ser a única de venda direta (27 das 89 peças são de produto/venda, 30%; só 3 dessas são AIDA), não por desempenho medido. Se o insight voltar e mostrar outra linha melhor, troco a divisão antes da 2ª entrega.
- Meta de resultado: reposição que vira assinante só se prova com atribuição por criativo (F-001). Hoje não prometo número.
