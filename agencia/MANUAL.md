# Manual de Conteúdo — MinhaMoto

Este é o cérebro compartilhado da agência. Todo agente lê este manual antes de trabalhar.
Nada aqui é sugestão: é regra. O que não estiver aqui, o agente decide com bom senso e anota a decisão.


> ## 🚨 FEEDBACK DO LÉO — 17/11 (lote piloto inteiro reprovado). Todo agente lê isto antes de qualquer coisa.
> - **"Não gostei de nada. Repensar tudo."** Os 10 carrosséis, 5 vídeos e 5 stories do lote piloto estão reprovados pelo dono.
> - **LOGO:** o símbolo MinhaMoto tem o **guidão/frente da moto pra DIREITA**. Use SÓ `agencia/designer/assets/icon.png` / `simbolo-branco.svg` (gerados do SVG oficial do app). Logo espelhada é erro gravíssimo — nunca mais.
> - **VÍDEO — o hook é tudo.** Nenhum vídeo prendeu. Se o gancho não segurar nos primeiros 1–2s, ninguém assiste. O hook tem que ser absurdo de bom (choque, curiosidade, dor real, contradição, número forte, POV que o motoboy se reconhece).
> - **Fontes feias.** A escolha tipográfica não ficou bonita. Repensar a tipografia (display forte, estilo nativo de TikTok/legenda, hierarquia que chama atenção).
> - **Vazio demais, sem imagem.** Peças só com texto sobre fundo liso não prestam. Precisa de imagem, movimento, elemento visual o tempo todo.
> - **Mockup do celular horrível.** App dentro do celular mal colocado, borrado, sem acabamento. A qualidade do app no mockup tem que ser PERFEITA — nítida, bem enquadrada, com sombra/profundidade bonitas, no nível (ou acima) dos vídeos que ele e o Davi já fizeram.
> - **Grifos/marca-texto não ficaram legais.** Não usar esse recurso como muleta.
> - **Até o story que o revisor aprovou (ST04, caixa de perguntas, todo azul) não passou com o Léo:** a ideia é boa, mas o grifado não ficou legal, a fonte não agradou, e o azul tá ok mas dá pra ficar muito mais foda (sombra, profundidade, acabamento). Lição: o Revisor estava permissivo demais — a régua é o gosto do Léo, não "sem erro técnico".
> - **TELAS DO APP = SÓ DO CÓDIGO MAIS NOVO.** Antes de qualquer carrossel, vídeo ou story: `git pull` no repo do app (carnuccicompany/minhamoto-midia não — o do app: carnuccicompany/minhamotooficial), ver se tem tela/estética/funcionalidade nova e usar as telas renderizadas desse código (`agencia/designer/assets/telas-app/`, regerar se o app mudou). Nunca gravação de tela antiga nem print velho. No repo do app: só ler e rodar local — nunca commit/push/deploy.
> - **YouTube = canal só de Shorts.**
> - O painel da agência ele aprovou ("muito foda") — manter e aprimorar.

## 1. O negócio

- **Produto:** MinhaMoto — app de assinatura pra motociclista cuidar da moto: revisões, histórico de manutenção, documentos, gastos, combustível, tudo num lugar só.
- **Lojas:** App Store (id 6815447825) e Google Play (`com.carnuccicompany.minhamoto`).
- **Objetivo das redes:** download do app. Tudo converge pra isso. Seguidor é meio, download é fim.
- **Público:** motociclista brasileiro do dia a dia — trabalha de moto, usa pra se locomover, faz a própria manutenção básica ou vive de oficina. Fala simples, odeia enrolação, respeita quem entende de moto.
- **Promessa central:** "O jeito de cuidar da sua moto mudou."

## 2. Tom de voz

- Português brasileiro informal, direto, de motociclista pra motociclista.
- Frases curtas. Uma ideia por frase.
- Fala com "você". Nunca "motociclistas devem..."
- Concreto sempre: "anota o km da troca" em vez de "mantenha registros".
- Zero juridiquês, zero clichê de marketing ("não perca!", "imperdível"), zero tom de professor.
- Pode usar gíria leve de moto (corrente, relação, baixa, ganha-pão — sem repetir a mesma expressão na sequência).
- Nunca inventar número, estatística ou dado técnico. Dado técnico errado mata a confiança do público. Na dúvida, reescrever sem o dado.

## 3. Linhas editoriais

| Linha | O que é | Template visual |
|---|---|---|
| **Dicas e hacks** | Problema real do dia a dia + 4-5 passos práticos | foto |
| **Educacional** | Explica um conceito (óleo, corrente, freio, documento) e termina provando no app | produto |
| **Marcas** | Curiosidades e comparativos de marcas/modelos | foto |
| **Curtos AIDA** | 4-5 cards de venda direta do app | produto |
| **Temas gerais** | Comportamento, economia, rotina do motociclista | foto ou editorial |

### Série do Davi (DV01–DV30) — já na fila, NÃO repetir o ângulo
Tutoriais de função do app, formato 9:16 (convertido pra 4:5 no IG/FB, original no TikTok), fundo pastel por série, gancho-pergunta → passos com tela → "Essa é uma das funções" → CTA preto "Assine por R$19,90/mês".
Temas cobertos: plano de revisão do modelo, histórico de serviços, cuidados feitos/pendentes, planejamento pela média de uso, combustível/consumo, comparação de postos, várias motos na garagem, documentos (cópias), especificações (óleo/pneu), cuidados por tempo (moto que roda pouco), primeira moto, moto usada, moto de alto valor, viagem, motoclube, moto de trabalho, ida à oficina, gastos do mês, quem faz a própria manutenção, estados da Saúde (verde/amarelo/vermelho), próximos marcos, bateria/itens por condição, completar histórico desconhecido.
→ A agência pode falar desses assuntos, mas com ângulo de VALOR (dica, erro comum, história, dado do mundo real) — não como tutorial de tela, que o Davi já fez.

Proporção alvo da fila: ~70% valor (dicas, educacional, marcas, temas) / ~30% venda (AIDA, produto).
Nunca dois carrosséis da mesma linha em sequência na fila.

## 4. Sistemas visuais

Formato: **1080×1350 (4:5)**, 5 a 7 cards, JPG q92. Fonte: **Inter** (400–900). Renderizador oficial: `agencia/designer/render2.py` (campo `"estilo"` no roteiro + `"layout"` em cada card: capa, texto, numero, item, phone, cta). Azul continua sendo a cor da marca.
Feedback do Léo (16/11) que originou esta versão: o fundo azul-claro pastel ficou "xoxo" e já existe demais no acervo; ele quer "tchan". Aprovou a sombra do celular e os prints reais. **Esses dois elementos ficam em todos os estilos.**

### Estilo DARK premium (`"estilo": "dark"`)
- Fundo quase preto (#05080f) com brilho azul nos cantos e grade sutil.
- Título branco, Inter 900, alinhado à esquerda, com destaque em azul elétrico #3d8bff (`*palavra*`).
- Kicker pequeno em caixa-alta azul acima do título ("CUSTO REAL", "O TRUQUE").
- Números grandes em contorno azul (cards `numero` e `item`).
- Celular com sombra profunda + halo azul; na capa ele entra inclinado e cortado embaixo.

### Estilo FOTO + tipografia gigante (`"estilo": "foto"`)
- Foto real do banco cobrindo o card, com degradê escuro de baixo pra cima.
- Título GIGANTE em caixa-alta, Inter 900, alinhado à esquerda no terço de baixo; destaque em azul #4b8dff.
- Kicker em etiqueta azul sólida ("OUVIU ISSO?", "ÉPOCA DE CHUVA"). Itens numerados "01, 02…" em azul acima do título.
- A foto tem que casar com o texto do card (consultar `assets/fotos-catalogo.md`).

### Estilo CLARO editorial (`"estilo": "claro"`)
- Fundo off-white quente (#f3f1ec), texto quase preto, régua preta no topo com marca/tema à esquerda e paginação "01/07" à direita.
- Destaque em **marca-texto azul sólido** (#1f5fff com texto branco) — é o "tchan" do estilo.
- Números gigantes azuis sólidos; pílula preta "ARRASTA →" na capa.
- Celular com sombra forte, levemente inclinado.

### Regras de composição (todos os estilos)
- Um foco por card. Quebra manual com `\n` quando a frase tem duas partes (evita palavra solta tipo "O" no fim da linha).
- Capa sempre com "Arrasta →". CTA final sempre com ícone do app + selos App Store/Google Play.
- Misturar estilos na fila: nunca dois carrosséis seguidos do mesmo estilo.
- O antigo "produto azul-claro" (render.py, Template B) foi **aposentado como padrão**: só eventual, quando o Léo pedir.

### Templates antigos (render.py — só para manutenção do acervo)
- A — "foto" (overlay escuro, texto central), B — "produto" (azul-claro + iPhone), C — "editorial". Não usar em produção nova sem pedido do Léo.

### Proibições (direção aprovada)
- Não repetir cabeçalho, logo ou chamada de navegação nos cards.
- Não recitar no texto a lista/números que já aparecem na tela do app.
- Não sugerir que é preciso atualizar km a cada corrida.
- Texto sobre foto: área visual limpa, contraste local, legível no tamanho do feed.

## 5. Legendas

**IG/FB (mesma legenda):**
```
{gancho forte, 1-2 linhas}

{valor: o resumo prático, 2-4 linhas}

📌 Salva pra não esquecer e manda pra quem {pessoa específica}.

📲 Baixe agora o MinhaMoto na App Store e no Google Play.

{8-12 hashtags do nicho}
```

**TikTok (diferente, mais curta):**
```
{gancho} 📌 Salva e manda pra quem {pessoa}. 📲 Baixe agora o MinhaMoto na App Store e no Google Play. {5 tags} #fyp #motostiktok
```

Regras:
- CTA **sempre imperativo**: "Baixe agora o MinhaMoto na App Store e no Google Play." Nunca variar essa frase.
- Gancho tem que parar o dedo: dor real, pergunta incômoda ou número específico.
- Hashtags: misturar grandes (#moto #motoboy #motociclista) com específicas do tema.

## 6. Publicação

- **4 carrosséis/dia**: 12h, 15h, 18h, 21h (Brasília). Robô publica IG + FB sozinho (`scripts/publicar.py`).
- **TikTok:** manual pelo Léo via notificação + página `tiktok.html`.
- Reels e stories: formato em definição com o Léo (não produzir ainda).
- Repetição: depois de ~300 posts publicados, uma ideia antiga pode voltar com estética nova. Antes disso, não.

## 6b. Vídeos (Reels/TikTok) — prioridade da operação

**Preço (regra do Léo, 16/11):** pode — e em parte dos vídeos é preferível — citar o preço no final, junto do CTA: "por R$19,90" (não precisa dizer "por mês"). Não precisa ser em todos. Nunca usar "vitalício" (oferta antiga). Vale também pro card de CTA dos carrosséis quando fizer sentido.
- **2 vídeos por dia**: **12h40** e **20h30** (BRT), longe dos carrosséis (12h/15h/18h/21h). O Analista revisa os horários com dados após ~2 semanas.
- Formato 1080×1920, 30 fps, H.264, 7–25 s, **sem música** (o Léo põe o som em alta na hora de postar no TikTok).
- Gancho em texto grande já no **primeiro frame** (0–2 s). Texto na tela o tempo todo (a maioria assiste sem som). Cortes rápidos (~2–3 s por cena).
- Final que emenda no começo (loop) quando possível.
- Zonas seguras: nada importante nos ~150 px de cima, ~380 px de baixo e ~160 px da direita.
- Tom de motoboy falando com motoboy; o app aparece como solução, não como anúncio.
- Formatos em rodízio: texto animado, tela do app em ação, POV/meme, lista rápida/ranking, quiz ou mito × verdade, e edição de material bruto que o Léo/Davi mandarem.
- Motor: `agencia/designer/video.py` (roteiros em `agencia/roteiros-video/`). Saída em `videos/VPnn/` + folha de frames em `revisao/`.
- Legenda IG/FB e TikTok no mesmo padrão do §5 (CTA intocável).

### Todo carrossel aprovado vira vídeo (regra fixa do Léo, 16/11)
Cada carrossel APROVADO pelo Léo gera também uma versão em vídeo 9:16 (motion dos próprios cards: texto entrando no ritmo, gancho do card 1 nos 2 primeiros segundos, transições entre cards, CTA final com "por R$19,90" quando fizer sentido). Esse vídeo entra na fila de vídeos com legenda própria. Vale também pros carrosséis antigos dele e do Davi que ele mandar pra converter.

### Canais de vídeo
- TikTok (manual, com aviso no celular), Instagram Reels e Facebook Reels (automático) e **YouTube Shorts (automático, canal orgânico extra)** — o mesmo vídeo sobe nos quatro, com título/descrição adaptados (Shorts: título curto com gancho + #shorts).

### Fase 2 (mais pra frente, já decidido)
- Teste de gancho com os vídeos/criativos vencedores (ver playbook do Analista).
- Responder comentários no Instagram e Facebook (precisa de permissão extra na Meta).

## 6c. Stories
- 1080×1920. Zonas seguras: 250 px de cima (barra do perfil) e 340 px de baixo (barra de resposta).
- Tipos em rodízio: enquete, você sabia, bastidor/tela do app, caixa de perguntas, CTA de download.
- Stickers (enquete, perguntas, link) são colocados pelo Léo no app: deixar quadro tracejado marcando o lugar e descrever o uso em `stories/pendentes.json`.
- Gerador: `agencia/designer/stories.py`.

## 7. Estoque

- **Mínimo de segurança: 14 dias de fila (56 carrosséis prontos).**
- Abaixo disso, o vigia alerta e a produção diária aumenta o ritmo até recompor.
- Nunca, em hipótese alguma, deixar a fila zerar.
