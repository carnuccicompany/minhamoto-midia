# Erros que não se repetem (designer lê antes de todo lote; revisor confere um por um)

Regra do Léo (26/11): erro de design é inadmissível. O revisor aponta uma vez, o erro entra aqui e nunca mais aparece.

1. Texto saindo do card ou encostando na borda / em outro texto. Título sempre medido e com o corpo ajustado pra caber (`cabe()`), apoio quebrado pela largura real da fonte (`quebra()`).
2. Linha quebrando diferente do planejado (palavra sozinha, título com uma linha a mais).
3. Coisa mal centralizada (centralizado tem que estar no centro exato do card; texto à esquerda alinha com a margem).
4. Tela do app fora do mockup do celular, card solto imitando o app, notificação montada. O app só aparece como tela REAL inteira dentro do celular.
5. Tela do app no visual antigo (antes da 1.0.2).
6. Ícone grande e forte demais (ícone é apoio, discreto).
7. Preço nos carrosséis.
8. Emenda visível de foto (corte seco entre foto e fundo): a transição é feita no canal alfa da imagem.
9. Na versão 9:16 (TikTok), texto ou "Deslize" fora da zona segura (de 300 a 1480 px de altura, 140 px de cada lado).
10. Metade do card vazia sem motivo.
11. Mesmo fundo azul em tudo (variar branco, preto e azul).
12. Prometer função que o app não tem (ex.: aviso de chuva).

### Adicionados em 26/11 (revisão do lote 2)
13. A mesma foto em duas peças do mesmo lote, ou duas fotos da mesma cena na mesma peça. Também evitar fotos do lote que está na fila ao mesmo tempo.
14. Logo ou marca legível (Kawasaki, Honda, MV, Triumph, Royal Enfield, Benelli/TNT, AGV, Alpinestars, posto Flying J, Shell, app Maxim) e placa legível, principalmente estrangeira. Borrar no motor (`BORRA` em lote2.py) ou trocar a foto.
15. Mockup diferente entre cards (Dynamic Island em uns e não em outros): algumas telas da 1.0.2 vêm com a ilha desenhada. Usar a página de `rolagem/` com o topo fixo, que sai sem ilha.
16. Barra de abas de vidro do app por cima do conteúdo no fim do celular, ou texto fantasma atrás do cabeçalho translúcido. Usar `rolagem/` (sem barra de abas) parada no trecho certo.
17. A tela não prova a frase: o texto promete algo que a tela não mostra, ou os dados da tela contradizem o texto (ex.: texto fala em 150 km/dia e a tela mostra 30 km/dia).
18. Foto que não prova o texto ou é do mundo errado: superesportiva ou custom cromada em peça de motoboy, bomba de gasolina no card do óleo, papel de escritório no card do manual, cenário estrangeiro.
19. Rosto de pessoa à mostra. Pessoa só de capacete, de costas ou sem rosto aparecendo.
20. Linha de apoio terminando em artigo, preposição ou conjunção ("o", "do", "pra", "e"), ou partindo expressão ("não / só", "filtro / sujo"). O motor (`quebra()`) já impede; expressão que não pode partir leva espaço inseparável.
21. Card final "Salve" com o kicker repetindo ou contradizendo o título, e com a metade de baixo vazia: o conjunto vai centralizado.
22. Legenda com imperativo de "tu" ("Faz", "Confere"); o certo é "Faça", "Confira". Mais de 5 hashtags.
23. Capa escura em peça de tema claro: a capa segue o tema da peça (`capa_clara`).
24. Mais de 2 cards de app num carrossel.
25. Motor medindo o texto com uma fonte diferente da que renderiza (a fonte renderizada é a Poppins).
