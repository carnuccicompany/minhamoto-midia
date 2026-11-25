# Playbook · criativo novo em cima de um vídeo que já vendeu (aprendido com o Léo em 25/11)

Escrito pro Claude do futuro. Antes de começar, leia também o `DESIGN-CORRETORES.md` (seções 0 e 0b) e a constituição no topo do `DESIGN-MINHAMOTO.md`.

## A ideia
Não inventar vídeo do zero. Pegar um pronto que já vende, usar o **body dele como está** (vídeo, legenda queimada, trilha e voz intactas) e trocar só a embalagem: **gancho em motion** na frente e **CTA com motion** no fim. A voz nunca é recortada de vários takes, nunca recebe EQ e nunca é "montada".

## Passo a passo
1. **Escolher o pronto** (Corretores: `Creative Lab/Ana Paula/PRONTOS/DD/`, HEVC 1080x1920, 30 fps). Trazer pro container com `device_stage_files` (só leitura; nada é salvo no PC do Léo).
2. **Mapear o pronto** antes de qualquer código:
   - folha 1 fps do vídeo inteiro → estrutura (gancho / body impresso / body iPad / preço / bumps / CTA);
   - tira da legenda a 4 fps (`crop` da faixa y≈1330–1470) → tempo de cada palavra;
   - energia do áudio em janelas de 10–50 ms → pausas reais.
3. **Escolher os cortes**: só em pausa real, depois de a palavra terminar e o som cair (nunca no meio da fala, nem no "você" do fim). Tirar o trecho em que ela fala o preço (por ora, sem preço em tudo).
4. **Conferir a legenda queimada do trecho**: os prontos DD têm "CURSOS" no lugar de "custos". Corrigir com `legfix2.py` (acha a palavra, apaga com inpaint e redesenha em Anton 68 com contorno, na mesma caixa).
5. **Alinhar o começo de cada trecho à grade de 30 fps** (o motor já usa o tempo real do quadro decodificado; correção de legenda depende disso).
6. **Gancho em motion** (padrão aprovado): Poppins caixa normal, cores do Mapa (navy, verde-água, coral), nada de fundo azul. Elementos com mola, partículas, empurrão de câmera, ícones Tabler em disco. Texto nunca junto com legenda. Toda tela de texto parada tempo suficiente pra ler.
7. **Body com elementos elegantes**: sempre centralizados na faixa logo acima da legenda do pronto (base y≈1335), cada um ligado ao que ela está falando ou ao que o Mapa mostra (contador +120, ícones dos temas, ilustrado/organizado/fácil, "?"→"✓", formas de aquisição). Cartão do tamanho do texto; rótulos sem encostar.
8. **CTA**: o "Clique em Saiba Mais" dela, do pronto + botão "Saiba mais" que recebe o toque de um dedo (só o símbolo, sem círculo), onda e partículas.
9. **Som**: voz como veio (só ganho igual entre trechos, -14 LUFS), efeitos sutis (pop, whoosh), sem trilha nova.
10. **Revisão antes de mostrar**: folha a 2–4 fps de tudo, tiras quadro a quadro em cada correção de legenda e em cada corte, energia do áudio em cada emenda, largura de todo texto.
11. **Mostrar ao Léo uma peça por vez**; cada feedback vira regra no DESIGN na hora; a peça aprovada vira referência da próxima.

## Ferramentas (agencia/estudio/motores/corretores/)
`v3.py` (motor: Seg, render, caixa, texto, disco, icone, particulas, cam), `legfix2.py` (correção de legenda queimada), `est2a_v6.py` (referência aprovada), `est8a_v5.py`, `icones/` (PNGs brancos Tabler + `dedo.png`). Fontes: Poppins e Anton em `fontes/`.
