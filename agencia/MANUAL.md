# Manual de Conteúdo — MinhaMoto

Este é o cérebro compartilhado da agência. Todo agente lê este manual antes de trabalhar.
Nada aqui é sugestão: é regra. O que não estiver aqui, o agente decide com bom senso e anota a decisão.

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

Proporção alvo da fila: ~70% valor (dicas, educacional, marcas, temas) / ~30% venda (AIDA, produto).
Nunca dois carrosséis da mesma linha em sequência na fila.

## 4. Sistemas visuais (aprovados pelo Léo — não inventar sistema novo)

Formato: **1080×1350 (4:5)**, 5 a 7 cards, JPG q92. Fonte: **Inter** (variável, pesos 400–900).

### Template A — "foto"
- Foto real (banco Pexels local em `agencia/designer/assets/fotos/`) cobrindo o card inteiro, escurecida (overlay escuro, mais forte atrás do texto).
- Texto branco, Inter extrabold, centralizado. Título grande (2 linhas no máx.) + apoio menor.
- Passos numerados: "2) Descreva a situação."
- A foto precisa conversar com o texto do card (card sobre oficina = foto de oficina).
- Um foco por card. Sem logo, sem cabeçalho repetido, sem moldura de gravação.

### Template B — "produto"
- Fundo azul-claro metálico em degradê suave (base `#dce8f5` → `#eef4fb`).
- Título editorial centralizado: parte em **navy `#16365c`**, parte em **azul `#2f6fe4`** (destaque só no que importa; na frase de apresentação, destacar só "MinhaMoto").
- Apoio em cinza-azulado `#5b6b80`.
- iPhone 15 (proporção real, base cortada intencionalmente quando o layout pedir) com **print real do app** (`agencia/designer/assets/prints/`). A captura prova o que o texto afirma.
- Rodapé da capa: "Deslize para entender →" em azul.
- Último card (CTA): título navy+azul, apoio citando **MinhaMoto** em azul, selos App Store + Google Play centralizados (`assets/selos-lojas.png`).

### Template C — "editorial"
- Só tipografia sobre fundo azul metálico (variações: petróleo, reflexos verde-água). Pra capas de impacto e cards de texto puro. Mesmas regras de hierarquia do B.

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

## 7. Estoque

- **Mínimo de segurança: 14 dias de fila (56 carrosséis prontos).**
- Abaixo disso, o vigia alerta e a produção diária aumenta o ritmo até recompor.
- Nunca, em hipótese alguma, deixar a fila zerar.
