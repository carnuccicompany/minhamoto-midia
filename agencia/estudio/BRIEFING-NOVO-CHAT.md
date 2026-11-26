# Briefing pra um chat novo do Estúdio (Léo / Davi) · 26/11

Este arquivo existe pra um chat novo pegar o trabalho de criativos do ponto onde o chat principal (o "ESTÚDIO AUDIOVISUAL") está, sem ninguém precisar repetir orientação. A memória da conta já é a mesma em todos os chats. O que fica aqui é o que a memória não guarda: arquivos, motores e o estado do trabalho.

## 1. Ler antes de qualquer coisa (nesta ordem)
1. `agencia/DESIGN-MINHAMOTO.md`: a régua do MinhaMoto. A ★ CONSTITUIÇÃO vale acima de tudo. Inclui o bloco "★ REFERÊNCIA DE MOTION APROVADA (25/11)", que é o K6, modelo de motion sem voz.
2. `agencia/DESIGN-CORRETORES.md`: a régua dos Corretores. Seções 0, 0b e tudo que tem data de 25/11.
3. `agencia/estudio/PLAYBOOK-CRIATIVO-SOBRE-PRONTO.md`: método de criativo feito em cima de um vídeo pronto da Ana Paula.

## 2. Jeito de trabalhar (regras do Léo, valem pros dois)
- Uma peça por vez. Mostrar parte por parte e só seguir com o OK dele. A peça aprovada vira referência da próxima.
- Todo feedback vira regra na hora, no DESIGN do produto. Vale a mais nova, e a antiga fica riscada.
- Revisão crítica antes de entregar: quadro a quadro, legenda, áudio e texto que vaza ou encosta.
- Nunca cortar no meio da fala. Áudio de gancho abafado passa pelo `voz.py` (`tratar`).
- Variar os elementos entre vídeos (conjuntos `elem.py` a `elem4.py`, mais o conjunto do K6).
- Criativo aprovado se chama `K<n> - <produto> - <nome>.mp4`. O último foi o **K6**, então o próximo é o **K7**. Se dois chats estiverem produzindo, combinar antes quem pega qual número.
- Arquivos e pastas do Léo no PC são só leitura. Peça aprovada só vai pro PC com o OK dele, e os Corretores vão pra `Criativos prontos/TESTES 2/`.
- Nunca publicar, agendar, subir anúncio ou gastar dinheiro sem OK. Nunca voz ou rosto da Ana Paula por IA. Nada de vídeo, PDF ou número de venda dela neste repo, que é público.
- Git: `git pull --rebase` antes de qualquer commit; nunca force-push, nunca stash; push só com "pode dar push".

## 3. Onde estão as coisas
- Motores dos Corretores: `agencia/estudio/motores/corretores/`.
  - `v3.py`: montagem e áudio.
  - `voz.py`: tratamento da voz.
  - `trilha.py`: trilha original.
  - `elem*.py`: conjuntos de elementos.
  - Scripts dos 6 aprovados: `est2a_v6.py` (K1), `est8a_v5.py` (K2), `historinha_v4.py` (K3), `perguntas_v4.py` (K4), `folheando_v1.py` (K5), `motion_v1.py` (K6).
- Brutos dos Corretores (no PC, pasta conectada `6 FIGURES/Corretores`):
  - prontos da Ana Paula em `Creative Lab/Ana Paula/PRONTOS/DD/` (DD 2, 4, 7 e 10; o body é o mesmo em todos, com deslocamentos anotados no DESIGN);
  - cortes de trabalho em `Criativos prontos/ESTUDIO 23-11/_trabalho/`;
  - PDF do Mapa em `Materiais/`.
- Carrosséis do MinhaMoto:
  - motores `agencia/estudio/motores/lote1_*.py`;
  - peças em `agencia/estudio/pecas/LOTE1/` (a pauta tem o histórico e a rodada 5);
  - telas reais do app em `agencia/designer/assets/telas-app/ios-1.0/`.

## 4. Estado em 26/11 de manhã
- **Corretores:** K1 a K6 aprovados e no PC. O Léo sobe hoje e testa amanhã. Avaliação dele: "ficaram bons, mas não ficou uau nem muito diferente um do outro", então o próximo lote precisa de ideia e visual mais diferenciados.
- **Carrosséis do MinhaMoto (lote 1, rodada 5):** prontos, esperando o veredito. Perguntas em aberto:
  - piloto de capacete no CM05 pode ficar?
  - ordem de publicação CM01 → CM02 → CM06 → CM04 → CM05?
  - em qual pasta salvar quando aprovar?
- **Motions do MinhaMoto:** ainda não começados. São dois tipos:
  - com narração: o Claude escreve o roteiro, o Léo gera o áudio no ElevenLabs e o Claude monta o motion;
  - sem voz: no modelo do K6, com trilha própria e variada.
- **Pendências do Léo:**
  - "pode dar push" (sem isso, chat novo e agentes não veem as regras novas);
  - venda R1;
  - iOS 1.0.1 pra revisão da Apple.

## 5. Divisão sugerida, quando forem dois chats
Cada chat cuida de um produto, pra não brigar pelos mesmos arquivos:
- **Chat principal:** carrosséis e motions do MinhaMoto.
- **Chat do Davi:** próximo lote dos Corretores (K7 em diante) ou motions do MinhaMoto com narração.

Os dois escrevem regra nova no DESIGN do produto e fazem `git pull --rebase` antes de cada commit.
