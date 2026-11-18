# Direção criativa v2: os dois estilos ativos (atualizado 18/11)

> **Revisão 18/11** (feedback do Léo nas amostras): A e B seguem as duas, alternando na fila. Sem amarelo: azuis oficiais do app (#287AF5, #005FDE, #52A9FE, navy #051F43→#0F57A8, #010711) com toque de verde-limão #C6FF00 só em detalhe. Fonte Poppins. O mesmo mockup em todas as cenas (entra meio de lado, centraliza e dá zoom; rolagem suave; toques simulados), barra de status redesenhada em 4x, ilha só pelo mockup. Telas novas com a moto simulada CG 160 Titan 2022 "Minha Titan" (29.800 km): em dia, atenção, vencido e sem histórico. CTA: "Sua moto. Sob controle." (A1), "Sua moto em dia, sem esforço." (A2), "Controle total da sua moto." (B1), "Baixe o MinhaMoto / Seu plano de revisão na palma da mão." (B2), selo "por R$19,90" e lojas separadas embaixo. Copy premium. Régua: `agencia/DESIGN-MINHAMOTO.md`. Checagem automática: `python3 agencia/designer/revisar_video.py <arquivos>`.
> Histórico abaixo (17/11) mantido só como referência; onde conflitar, vale o de cima.

## Histórico (17/11)

Feita depois do feedback de 17/11 (lote piloto reprovado). **Revisão 17/11 tarde:** Léo reprovou a fonte em caixa-alta → tudo em frase normal com Plus Jakarta Sans (800/600/500), letter-spacing -0,035em; celulares retos e centralizados; margens laterais de 90px. Poucas peças, pra acertar a direção antes de escalar.
Logo sempre com o guidão pra DIREITA. Telas só do layout atual, geradas do código do app (`agencia/designer/assets/telas-app/`, prévia visual com dados fictícios, status bar 9:41). Nada de gravação de tela antiga nem filmagem antiga.

## Direção A — "Nativo / Rua"
- **Fonte:** Plus Jakarta Sans 800 em frase normal (sem caixa-alta), sombra suave pra ler sobre a foto, palavras-chave em amarelo #FFD400; apoio em Plus Jakarta Sans 600.
- **Cores / imagem:** foto real de moto/oficina em movimento (Ken Burns) no gancho; nas cenas de produto o celular fica sobre a mesma foto desfocada e escurecida. CTA em azul da marca com selo de preço amarelo.
- **Mockup / ritmo / hook:** celular frontal premium (bordas metálicas, ilha, reflexo, sombra em camadas) entrando com zoom; legenda palavra por palavra com "pop"; hooks de identificação (POV) e pergunta que dói ("Sua moto tá em dia? Prove.").

## Direção B — "Premium produto"
- **Fonte:** Plus Jakarta Sans 800 em frase normal, segunda linha em azul elétrico #3D8BFF; apoio em Plus Jakarta Sans 500.
- **Cores / imagem:** fundo navy profundo com luz azul atrás do celular (sem foto); visual de anúncio de produto caro.
- **Mockup / ritmo / hook:** celular reto e centralizado (só um leve giro na entrada, que assenta reto), flutuando, com a tela do app dentro (parada ou rolando a página inteira de `telas-app/rolagem/`, com o cabeçalho fixo); títulos revelados linha a linha; hooks de perda/contradição ("Esqueceu a troca? A moto não esquece.").

## Arquivos
| Direção | Vídeos (9:16) | Carrossel (4:5) / TikTok (9:16) | Story (9:16) |
|---|---|---|---|
| A | A/A1/video.mp4 (POV mecânico, com "por R$19,90"), A/A2/video.mp4 (Sua moto tá em dia? Prove.) | A/carrossel/01–05.jpg · A/carrossel-tiktok/01–05.jpg | A/story/story.jpg (caixa de perguntas) |
| B | B/B1/video.mp4 (Esqueceu a troca?, com "por R$19,90"), B/B2/video.mp4 (Sua moto tá em dia? Veja em 30 segundos) | B/carrossel/01–05.jpg · B/carrossel-tiktok/01–05.jpg | B/story/story.jpg (ST04 refeito) |

Folhas de revisão: `X/Xn/frames.jpg` (vídeos, 2 quadros/s) e `X/folha-carrossel-story.jpg` (linha 1: carrossel 4:5 + story; linha 2: carrossel TikTok 9:16).

**Formatos (MANUAL §5b):** TikTok sempre 9:16; carrossel 4:5 só no feed IG/FB. Tudo 9:16 (vídeos, carrossel-tiktok, stories) respeita a zona segura: texto entre x=140 e x=940 e entre y=150 e y=1500. `python3 videos.py <ID> prev` desenha as linhas da zona segura na prévia pra conferir.
Banco de ganchos: `hooks.md` (44 ganchos + 8 fórmulas). Motores: `motor.py` (vídeo + mockup), `videos.py` (roteiros), `estaticos.py` (carrossel/story).

Próximo passo: o Léo escolhe A, B ou mistura → a direção escolhida vira padrão no MANUAL e nos motores da produção diária.
