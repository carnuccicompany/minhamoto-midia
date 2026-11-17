# Direção criativa v2 — amostras pro Léo escolher (17/11)

Feita depois do feedback de 17/11 (lote piloto reprovado). Poucas peças, pra acertar a direção antes de escalar.
Logo sempre com o guidão pra DIREITA. Telas só do layout atual, geradas do código do app (`agencia/designer/assets/telas-app/`, prévia visual com dados fictícios, status bar 9:41). Nada de gravação de tela antiga nem filmagem antiga.

## Direção A — "Nativo / Rua"
- **Fonte:** Montserrat 900 em caixa-alta com contorno preto grosso e sombra (estilo legenda de TikTok), palavras-chave em amarelo #FFD400; apoio em Montserrat 800.
- **Cores / imagem:** foto real de moto/oficina em movimento (Ken Burns) no gancho; nas cenas de produto o celular fica sobre a mesma foto desfocada e escurecida. CTA em azul da marca com selo de preço amarelo.
- **Mockup / ritmo / hook:** celular frontal premium (bordas metálicas, ilha, reflexo, sombra em camadas) entrando com zoom; legenda palavra por palavra com "pop"; hooks de identificação (POV) e pergunta que dói ("Tua moto tá em dia? Prova.").

## Direção B — "Premium produto"
- **Fonte:** Anton (condensada, display) em caixa-alta, segunda linha em azul elétrico #3D8BFF; apoio em Poppins 600.
- **Cores / imagem:** fundo navy profundo com luz azul atrás do celular (sem foto); visual de anúncio de produto caro.
- **Mockup / ritmo / hook:** celular em leve 3D (rotação/inclinação que assenta), flutuando, com a tela do app dentro (parada ou rolando a página inteira de `telas-app/rolagem/`, com o cabeçalho fixo); títulos revelados linha a linha; hooks de perda/contradição ("Esqueceu a troca? A moto não esquece.").

## Arquivos
| Direção | Vídeos (9:16) | Carrossel (4:5) | Story (9:16) |
|---|---|---|---|
| A | A/A1/video.mp4 (POV mecânico, com "por R$19,90"), A/A2/video.mp4 (Tua moto tá em dia? Prova.) | A/carrossel/01–05.jpg | A/story/story.jpg (caixa de perguntas) |
| B | B/B1/video.mp4 (Esqueceu a troca?, com "por R$19,90"), B/B2/video.mp4 (30 segundos pra saber se tua moto tá em dia) | B/carrossel/01–05.jpg | B/story/story.jpg (ST04 refeito) |

Folhas de revisão: `X/Xn/frames.jpg` (vídeos) e `X/folha-carrossel-story.jpg`.
Banco de ganchos: `hooks.md` (44 ganchos + 8 fórmulas). Motores: `motor.py` (vídeo + mockup), `videos.py` (roteiros), `estaticos.py` (carrossel/story).

Próximo passo: o Léo escolhe A, B ou mistura → a direção escolhida vira padrão no MANUAL e nos motores da produção diária.
