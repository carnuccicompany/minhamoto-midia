# minhamoto-midia

Imagens e fila de publicação dos posts orgânicos do MinhaMoto.

- `carrosseis/<ID>/NN.jpg`: cards de cada carrossel, na ordem.
- `fila/carrosseis.json`: ordem de publicação, com legenda do Instagram/Facebook e do TikTok.
- `fila/estado.json`: o que já foi publicado. Para pausar, coloque `"pausado": true`.
- `.github/workflows/publicar.yml`: publica o próximo da fila às 12h, 15h, 18h e 21h (Brasília).

Repositório público só com mídia que vai ao ar. Sem código do app, sem dados de usuários, sem credenciais.
