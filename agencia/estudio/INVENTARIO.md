# Inventário do acervo (Estúdio Audiovisual)

> Atualizado em 23/11/2026 pelo Estúdio. Atualizar sempre que o acervo mudar.
> Repositório público: sem números de assinantes ou receita (esses ficam em `carnucci-dados`).

## 1. MinhaMoto: o que existe

### Carrosséis orgânicos (4:5 + TikTok 9:16)
| Grupo | Qtde | Situação | Estética |
|---|---|---|---|
| Acervo Léo/Davi (A, B, DV, E, G, J, M, S) | 113 na fila (`fila/carrosseis.json`), todos com versão TikTok | 24 publicados (16 a 22/11, `fila/estado.json`), 89 na fila (~22 dias) | Foto com texto central (A/B), azul-claro pastel + iPhone (DV, E, J), navy com logo de marca (M) |
| Agência AG01–AG10 (lote piloto 16/11) | 10 | **Todos descartados** em 18/11 (`fila/descartados.json`) | Dark, foto e claro editorial (render2.py) |
| Direção v2: carrossel A e B (18/11) | 2 × 5 cards + TikTok | Corrigidos em 18/11; **direção ainda não liberada** pelo Léo (decisão 19/11) | A: foto escura + Poppins; B: navy com luz azul + celular |

Linhas na fila: Tutorial do Davi 30 · Dicas e hacks 1: 20 · Dicas e hacks 2: 20 · Marcas 11 · Educacional 10 · Junto com a chave 10 · Temas gerais 7 · Curtos AIDA 5. Venda direta (AIDA) quase acabando (3 restantes).

### Vídeos
| Grupo | Qtde | Situação |
|---|---|---|
| VP01–VP05 (lote piloto) | 5 | Reprovados 17/11 (hook fraco, fonte, mockup, tempo de leitura) |
| Direção v2: A1, A2, B1, B2 | 4 | A1/A2/B2 corrigidos 18/11; B2 tem a **copy aprovada**; entrada do celular e rolagem aprovadas; direção ainda não liberada |
| Referências antigas (curtos, motions de marca, "prontos") | removidas | App e oferta antigos: proibido usar |

### Stories
ST01–ST05 (lote piloto): reprovados, inclusive o ST04 que o revisor tinha aprovado. Stories A e B da direção v2: aprovados como ideia (só ajustar cor/fonte).

### Criativos de venda (anúncio)
Nenhum produzido ainda no padrão novo. Playbook em `agencia/diretoria/04-criativos.md`.

### Assets
- Logo `icon.png` / `simbolo-branco.svg` (guidão pra direita), selos das lojas, 145 fotos Pexels (`fotos-catalogo.md`).
- Telas do app (`telas-app/`, 24 + 20 páginas de rolagem): geradas em 18/11 de um commit de 11/11. **Desatualizadas**: o app mudou depois (inspeção vencida agora é amarela, card de transferência na Garagem etc.). Regeração em andamento em 23/11.
- Fontes: Poppins 500–800 em `direcao-v2/fontes/`.

### Ferramentas (testadas em 23/11)
`direcao-v2/estaticos.py` e `motor.py` renderizam (Playwright + Chrome + ffmpeg ok). `designer/revisar_video.py` roda (tesseract ok), mas só pega erro técnico: passou todas as amostras v2.

## 2. Desempenho
- Orgânico: **sem métrica por post**. O token da Meta não tem `instagram_manage_insights`; só curtidas (4 em 24 posts, 0 comentários). Não dá pra dizer o que performa.
- Vendas: RevenueCat conectado; AppsFlyer, lojas e Meta Ads sem chave. **Sem atribuição por criativo/canal**, então ainda não existe "o criativo que vende".
- Consequência: até o insight voltar, a régua é o gosto do Léo + boas práticas.

## 3. Reprovações: padrões que se repetem
1. **Tipografia:** caixa-alta, fonte "simplona" (Plus Jakarta, Inter, Montserrat/Anton), quebra de linha feia, palavra solta no fim da linha.
2. **Muleta visual no lugar de design:** grifo/marca-texto, número gigante vazado, fundo liso vazio, pastel "xoxo" repetido.
3. **Mockup e telas:** status bar bugada, ilha aparecendo e sumindo, sheet colado no topo, telas vazias (0%/6%, "moto de demonstração"), dados que se contradizem entre cards, telas antigas.
4. **Cor fora da marca:** amarelo, azuis inventados.
5. **Copy:** fraca ou informal demais, CTA fraco ("Nunca mais sei lá"), "tu", ângulo que o acervo já usou, dado não verificado.
6. **Foto:** banco estrangeiro, marca de terceiros (Shell, Harley, J&T), foto repetida, foto que não casa com o texto.
7. **Causa raiz:** revisor checava erro técnico, não o gosto do Léo ("tá certo" ≠ "tem tchan").

## 4. O que falta
- Carrossel-modelo aprovado sem comentário (em lapidação desde 23/11).
- Telas do app regeneradas do código de 17/11.
- Motion em cima do carrossel aprovado; motion de venda do app.
- Permissão de insights na Meta (Léo) pra medir o orgânico.
- Corretores: aguardando briefing.
