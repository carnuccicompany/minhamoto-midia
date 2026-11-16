# minhamoto-midia

Imagens e fila de publicação dos posts orgânicos do MinhaMoto.

- `carrosseis/<ID>/NN.jpg`: cards de cada carrossel, na ordem.
- `fila/carrosseis.json`: ordem de publicação, com legenda do Instagram/Facebook e do TikTok.
- `fila/estado.json`: o que já foi publicado. Para pausar, coloque `"pausado": true`.
- `.github/workflows/publicar.yml`: publica o próximo da fila às 12h, 15h, 18h e 21h (Brasília).

Repositório público só com mídia que vai ao ar. Sem código do app, sem dados de usuários, sem credenciais.


## Painel da agência
https://carnuccicompany.github.io/minhamoto-midia/painel.html — estoque da fila, posts de hoje/amanhã, itens aguardando aprovação (com comando `aprova ID` pra colar no chat), fila completa, agentes, rotinas e últimos relatórios. Lê os JSONs do repo em tempo real.

- O Analista, ao salvar um relatório em `dados/relatorios/AAAA-MM-DD.md`, acrescenta o nome do arquivo em `dados/relatorios/index.json` (lista JSON).
- O radar, ao salvar em `agencia/radar/AAAA-MM-DD.md`, acrescenta o nome em `agencia/radar/index.json`.
- Status de revisão no painel: campo `"revisao": {"status": "APROVADO|REPROVADO", "nota": 9}` em cada item dos `pendentes.json` (ou `revisao/relatorio.json`).
