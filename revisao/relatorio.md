# Revisão do lote piloto da agência: AG01–AG10, VP01–VP05, ST01–ST05

Revisor independente, 16/11/2026. Base usada: MANUAL.md, playbook 04-revisor.md, acervo (A11, E04, E05, M01, B01, B05, B16, DV01/16/21 tiktok). `agencia/referencias/videos/` **não existe** no repo, então os vídeos foram comparados só com o acervo de carrosséis.
Régua: só aprova com **zero erros E nota ≥ 8/10**.

## Placar geral

| Tipo | Aprovados | Reprovados |
|---|---|---|
| Carrosséis (10) | 0 | 10 |
| Vídeos (5) | 0 | 5 |
| Stories (5) | 1 (ST04) | 4 |
| **Total (20)** | **1** | **19** |

## Os 3 problemas mais graves do lote

1. **Bug de renderização que se repete (render2.py, stories.py, video.py).** Em várias peças, a caixa de destaque de uma linha é desenhada por cima das letras da linha anterior. Isso corta as pernas de g, p, q, j e a cedilha do ç: AG03 card 06, AG06 cards 01/02/03/06/07, AG09 cards 04/05, ST02 (que também corta o "r" na borda da caixa) e VP01 em 05,2–07,4s. No estilo dark, os números/glifos vazados aparecem com o contorno quebrado e linhas internas visíveis: o "x" do "2x" (AG01 card 03) e o "4" (AG10 card 05). O erro está no renderizador, então vai se repetir em toda peça nova até alguém corrigir o código.
2. **Fotos estrangeiras, com marca de outras empresas e repetidas.** O AG08 inteiro ("Vida de motoboy") é banco do Sudeste Asiático. Tem jaqueta "maxim" (app de corrida russo) na capa, logo da Shell V-Power gigante com Ducati e preço em dólar no card 05, e baú da J&T Express com texto em vietnamita no card do CTA. O AG02 card 05 mostra o logo da Harley-Davidson. O AG05 card 06 tem placa indiana legível. Um pneu de trilha enlameado com placa estrangeira ilustra "pneu careca" (AG05) e "pneu murcho" (VP04). O mesmo modelo de barba aparece em AG02 (capa e CTA), VP03 e no acervo B16, e a mesma foto de roda está em AG02 e AG05.
3. **Prints do app com dados que se contradizem, e um frame preto.** No AG04, o card 01 mostra 24.400 km em 07/11/2026 e o card 04 mostra 18.400 km no mesmo dia, justo no post sobre "histórico que dá confiança". No VP02 acontece o mesmo (24.400 vs 18.400). No AG07, a capa diz "troca registrada 07/11, 18.400 km" e o card 05 diz "última troca 9 mai, 18.000 km, vence neste mês". No VP04, o **frame 318 (10,60s) aparece com o fundo preto**, só com o número "1".

Problemas que também se repetem no lote:
- **Tempo de leitura dos vídeos.** Usei a régua de 2 leituras a ~4 palavras/s, ou seja, nº de palavras ÷ 2 em segundos. Nenhum dos 5 vídeos passa.
- **Legendas dos vídeos fora do formato do §5.** No IG/FB está "📌 Salva e manda…" em vez de "📌 Salva pra não esquecer e manda…". No TikTok está "📌 Manda pra quem…" em vez de "📌 Salva e manda pra quem…".
- **Palavra solta no fim da linha do título** ("a", "o", "no", "COM A"), que o MANUAL §4 proíbe.
- **Ângulos que o acervo já usou.** AG01 repete B16 ("Quanto você gastou cuidando da moto?") e AG03 repete E05 ("Lubrificou a corrente? Ou trocou a relação?"). O MANUAL §6 só libera repetição depois de ~300 posts.

## Checagem de fatos (WebSearch)

| Afirmação | Resultado |
|---|---|
| AG06: CG é "a moto mais vendida do Brasil" | **Confirmado.** A CG 160 lidera, com 224.750 unidades no 1º semestre de 2025 (garagem360). |
| AG07/ST02/AG10: óleo vence por km e por tempo, o que chegar primeiro | **Confirmado** (AutoPapo, "10 mil km ou 12 meses, o que vencer primeiro"). A fonte fala de carro; em moto vale o manual. Sugiro falar "pelo manual". |
| VP05: 10W = frio, 30 = temperatura de trabalho | **Confirmado** (AutoPapo, "O que é o W na viscosidade do óleo"). |
| AG02: bater pino = combustível ruim ou carbonização | **Confirmado** (Vrum, mar/2026). |
| AG02: estouro no escape ao reduzir = entrada de ar ou mistura desregulada | **Confirmado em parte.** A Oficina Brasil cita mistura que enriquece na desaceleração, sistema PAIR, vedação dos coletores e mangueiras soltas. "Mistura desregulada" passa; o "Nenhum desses é normal" da legenda é forte demais. |
| AG03/AG05: lubrificar corrente depois de chuva/lavagem | **Confirmado.** AutoPapo/Motul: semanal ou a cada 500 km, e logo depois de chuva. "Cuidado de toda hora" (AG03 card 02) **é exagero.** |
| AG03 card 05: "dente da coroa pontudo" é sinal de troca | **Não confirmado** nas fontes encontradas. O manual Honda fala em "dentes excessivamente gastos"; O Mecânico e AutoPapo falam em desgaste e folga. **Pela régua, conta como erro.** Reescrever. |
| AG03 card 04: corrente, coroa e pinhão gastam juntos, troca é do kit | Confirmado por AutoPapo ("a troca do kit é fundamental"). |
| AG10: gasolina parada perde qualidade | Confirmado (Canaltech: "Combustível parado no tanque estraga?"). A frase do card é genérica e segura. |
| AG05 legenda: "Leva 5 minutos" | Não tem como verificar. Tirar. |
| ST05: link da bio "minhamotopagina.online" | Não verificado. Confirmar com o Léo se é o link certo. |

---

## CARROSSÉIS

### AG01 (Quanto sua moto te custa por mês) — REPROVADO
ERROS (corrigir obrigatoriamente):
1. [card 03] O "x" do "2x" vazado está com o contorno quebrado: aparecem triângulos e linhas internas onde os traços se cruzam. Evidência: `evidencias/AG01_card03_x_contorno_quebrado.jpg`.
2. [capa → card 06] A capa promete "Quanto sua moto te custa por mês?" e nenhum card mostra o custo do mês. Os prints mostram serviços avulsos (R$ 65, R$ 30) e consumo. O CTA "descubra quanto sua moto custa de verdade" fica sem prova.
3. [ângulo] Repete o B16 do acervo ("Quanto você gastou cuidando da moto?") e o DV19 do Davi (gastos registrados). O card 05 é tutorial da função combustível ("Anota o abastecimento e o app calcula…"), ângulo que o Davi já fez.
MELHORIAS:
1. [card 02] O kicker "O TRUQUE" não combina com o texto, que não é um truque. Trocar por "O PROBLEMA".
2. [card 05] O print mostra "Autonomia estimada --" (vazio) e "1 ciclo válido", o que passa a impressão de app sem dados. Usar um print com histórico cheio e um **total do mês** (ex.: "Novembro: R$ 412") pra cumprir a capa.
3. [cards 01 e 04] O mesmo print de histórico aparece duas vezes. Viúvas no corpo: "baixo." (capa) e "lugar só." (card 04).
4. [cards 02, 03, 06] O bloco de texto ocupa só a metade de cima e a de baixo fica vazia.
NOTA: 5/10

### AG02 (5 barulhos que você não pode ignorar) — REPROVADO
ERROS:
1. [card 04] O título quebra em "RONCO QUE / CRESCE COM A / VELOCIDADE": o artigo "A" fica solto no fim da linha (MANUAL §4). Usar "RONCO QUE CRESCE / COM A VELOCIDADE".
2. [card 05 — estouro no escape] A foto é guidão e velocímetro de **Harley-Davidson, com o logo legível** na mesa do guidão. Não mostra escape e põe marca de terceiro em destaque. Evidência: `AG02_card05_logo_HarleyDavidson_foto_nao_casa.jpg`.
3. [card 07 — CTA] O título "OUVIU UM DESSES?" cai sobre o rosto do modelo e a janela clara. O contraste local medido é de 2,3:1 no pior ponto. Evidência: `AG02_card07_titulo_sobre_rosto_contraste.jpg`.
MELHORIAS:
1. [card 06 — batendo pino] A foto mostra alguém despejando óleo, que não tem a ver com batida de pino. Trocar por foto de moto subindo ladeira ou de motor.
2. [cards 01 e 07] É o mesmo modelo do B16 e do VP03, e a foto do card 02 é a mesma do AG05 card 03. Variar o banco de fotos.
3. [card 02] "estraga o disco junto" repete "disco". Sugestão: "Metal no metal come o disco junto."
4. [legenda] "Nenhum desses é 'normal da moto'" é absoluto demais, porque estouro leve na desaceleração pode ser do sistema de emissões. Sugestão: "Nenhum desses dá pra ignorar."
5. O tema "barulho" já foi usado no A11. O ângulo é diferente, mas não postar perto dele.
NOTA: 6/10

### AG03 (Corrente: lubrificar, regular ou trocar) — REPROVADO
ERROS:
1. [card 06] A caixa azul de "Cada prazo na" corta a perna do "g" de "registrado". Evidência: `AG03_card06_descendente_g_cortado.jpg`.
2. [cards 01, 02, 03] Artigo solto no fim da linha do título: "trocar? Não é a / mesma coisa", "Lubrificar: o / cuidado de", "Regular: a / folga certa". O MANUAL §4 proíbe.
3. [card 05] "dente da coroa pontudo" não foi confirmado como sinal de troca nas fontes. Sugestão: "dente da coroa gasto, fino ou em gancho" (o manual Honda fala em "dentes excessivamente gastos").
4. [ângulo] Repete o E05 do acervo ("Lubrificou a corrente? Ou trocou a relação? São registros distintos").
MELHORIAS:
1. [card 02] "cuidado de toda hora" é exagero: a referência é semanal ou a cada ~500 km, e depois de chuva. Sugestão: "o cuidado de toda semana."
2. [card 03] "Nem esticada, nem frouxa" confunde, porque no jargão "corrente esticada" quer dizer corrente gasta. Sugestão: "Nem tensa demais, nem frouxa."
3. [card 06] O título usa "regular" e o CTA usa "ajustar". Padronizar.
4. [prints] Lubrificar, ajustar e trocar o kit aparecem todos em 07/11/2026 e 18.400 km, o que contradiz a ideia de que são momentos diferentes (e o AG01 mostra ajuste em 05/09). Usar datas e km diferentes.
5. [capa] Viúva no corpo: "cobra.".
NOTA: 6/10

### AG04 (Moto com histórico vende melhor) — REPROVADO
ERROS:
1. [card 01 × card 04] Os prints se contradizem. A capa mostra "Filtro de ar / Filtro de óleo — 07/11/2026 — **24.400 km**"; o card 04 mostra "Óleo do motor — 07/11/2026 — **18.400 km**". É a mesma moto, no mesmo dia, com 6.000 km de diferença, num post que vende confiança no histórico. Evidência: `AG04_cards01x04_km_contraditorio.jpg`.
2. [card 03] "“Quando trocou o / óleo?”" deixa o "o" solto no fim da linha. Usar "“Quando trocou / o óleo?”".
MELHORIAS:
1. [capa] "Adivinha qual o comprador escolhe." soa truncado. Sugestão: "Adivinha qual delas o comprador leva."
2. [card 05] O CTA "A venda de amanhã agradece" usa a mesma fórmula do AG07 ("O motor agradece"). Variar.
3. [card 03] No corpo, "contra a" e "puxa o" ficam soltos no fim da linha.
NOTA: 6,5/10

### AG05 (Chuva chegando: 5 checagens) — REPROVADO
ERROS:
1. [card 04] "Na chuva, ver e ser visto vale a sua vida." O sentido está errado ("vale a vida" = custa a vida). Usar "…pode salvar sua vida."
2. [card 06] O título "CAPA DE CHUVA NO / BAÚ" deixa "NO" no fim e "BAÚ" sozinho na linha. A foto não tem nem baú nem capa, e mostra **placa indiana "WB-01AT-887"** legível. Evidência: `AG05_card06_placa_estrangeira.jpg`.
3. [card 02] A foto de pneu de trilha enlameado, com placa estrangeira, ilustra "pneu careca no asfalto". Não combina com o texto.
MELHORIAS:
1. [card 03] É a mesma foto do AG02 card 02. [card 05] É a mesma moto do AG02 card 03.
2. [card 02] "aquaplanagem esperando acontecer" é decalque do inglês. Sugestão: "Na chuva, pneu careca é aquaplanagem na certa."
3. [legenda] Tirar "Leva 5 minutos" (sem base).
4. [card 07] "não te deixa na mão" repete a capa do AG02.
5. [capa] "5 checagens" inclui a capa de chuva, que não é checagem da moto. Trocar por "fluido/pastilha" ou "pressão do pneu".
NOTA: 6/10

### AG06 (Por que todo mundo tem uma CG) — REPROVADO
ERROS:
1. Caixas de destaque cortando letras da linha de cima: [card 01] perna do "q" de "Por que"; [card 02] cedilha de "Peça"; [card 03] perna do "q" de "que"; [card 06] cedilha de "atenção"; [card 07] perna do "j" de "Seja". Evidência: `AG06_cards01-02-03-06-07_descendentes_cortados.jpg`.
MELHORIAS:
1. Os 7 cards são só texto e a CG não aparece nenhuma vez. A linha Marcas pede o template foto (§3). Uma CG real na capa dá o impacto que o post precisa.
2. O fato "mais vendida do Brasil" está confirmado. Dá pra usar o número ("224 mil vendidas só no 1º semestre de 2025") e citar a Fenabrave.
3. Viúvas: "Brasil." (capa), "errado." (card 03), "dia." (card 05).
NOTA: 6/10

### AG07 (Passou do prazo do óleo) — REPROVADO
ERROS:
1. [capa × card 05] Os prints se contradizem. A capa mostra troca de óleo em **07/11/2026 com 18.400 km**; o card 05 mostra "Última realização **9 mai 2026, 18.000 km**", "Atenção — vence neste mês" e "próximo prazo 9 nov 2026", data que já passou quando o post for ao ar. Evidência: `AG07_cards01x05_dados_contraditorios.jpg`.
MELHORIAS:
1. [cards 02–04] São três cards seguidos só de texto, com a metade de baixo vazia. Pôr um visual de óleo velho × novo.
2. O "2" vazado e a fórmula "O motor agradece" já aparecem no AG01/AG04. "Moto parada também vence" repete o AG10.
3. [card 05] Mostrar o estado "Vencido" em vermelho dá mais força ao post do que "Atenção".
NOTA: 6,5/10

### AG08 (Só quem trabalha de moto entende) — REPROVADO
ERROS:
1. [card 05] Logo **Shell V-Power** gigante, macacão Dainese, Ducati e bomba com preço em dólar e "Litres". É marca de terceiro em destaque e nada a ver com o motoboy brasileiro. `AG08_card05_Shell_Ducati_dolar.jpg`
2. [card 07 — CTA] Baú da **J&T Express** com texto em vietnamita ("GIAO ĐÚNG GIỜ NHẬN CHU TOÀN"). A empresa opera no Brasil, então o post parece anúncio dela. `AG08_card07_JT_Express_vietnamita.jpg`
3. [card 01] Jaqueta **"maxim"** (app de corrida russo) na capa. `AG08_card01_logo_maxim.jpg`
4. [todos] As fotos são todas da Ásia: capacetes coco, placas, ruas. O post pede identificação ("vida de motoboy") e o público brasileiro não vai se reconhecer.
MELHORIAS:
1. [card 02] O topo da imagem corta o capacete.
2. [card 07] "Cuida como tal" soa traduzido. Sugestão: "Cuida dela como cuida do seu ganha-pão."
3. [legenda] Tem dois CTAs sociais ("Marca o parceiro" e "manda pra quem") e "trabalha de moto" aparece 3 vezes.
4. A copy dos cards é a melhor do lote ("Chuva não é desculpa. É só mais um dia."). Vale refazer com fotos de motoboy brasileiro (CG/Fan, baú, capa de chuva, iFood/Loggi sem logo).
NOTA: 4/10

### AG09 (Sua memória não é um sistema de manutenção) — REPROVADO
ERROS:
1. Caixas de destaque cortando letras: [card 04] pernas dos "p" de "app" e do "q" de "que"; [card 05] perna do "p" de "pilota". Evidência: `AG09_cards04-05_descendentes_cortados.jpg`.
MELHORIAS:
1. [cards 01–05] O kicker "REAL" não quer dizer nada. Usar "MEMÓRIA" ou "MANUTENÇÃO".
2. [cards 01 e 04] O print mostra "21 itens a confirmar" e "0/5", ou seja, pendência acumulada, que prova o contrário de "Esforço pra lembrar: zero". Usar um print com tudo em dia e o próximo cuidado destacado.
3. [card 04] "O app mostra o que vem pela frente" é o ângulo do Davi (próximos marcos).
NOTA: 6/10

### AG10 (Moto parada: checklist antes de ligar) — REPROVADO
ERROS:
1. [card 05] O "4" vazado está com o contorno quebrado (retângulos internos sobrepostos). Evidência: `AG10_card05_4_contorno_quebrado.jpg`.
MELHORIAS:
1. [cards 02–06] São cinco cards seguidos só de número e texto, com a metade de baixo vazia: no feed parece inacabado. A linha Dicas pede foto (§3): pneu, corrente, bateria, vareta de óleo.
2. [card 07] "Parada também tem prazo vencendo" repete o AG07 card 04.
3. [card 05] O dicionário registra "a manete". Se quiser evitar, usar "freio firme na mão e no pé".
NOTA: 6/10

---

## VÍDEOS

Dados técnicos: os 5 vídeos estão em 1080×1920, 30 fps constante, H.264 yuv420p. Durações: VP01 13,2s, VP02 17,4s, VP03 12,8s, VP04 15,3s, VP05 14,4s, todas dentro de 7–25s. Sem blocos de compressão visíveis nos frames em tamanho real. Extraí todos os frames (30/s), montei grades a 4 fps, detectei os cortes por diferença entre frames e conferi ±5 frames em volta de cada corte. Zona segura medida pela extensão do texto/elemento claro em cada frame.

### VP01 (Sua moto não quebra do nada) — REPROVADO
ERROS:
1. [05,20–07,40] "Quem ignora, / paga o / conserto.": a caixa branca de "conserto." corta as pernas do "p" e do "g" de "paga", e o "g" de "ignora" (texto branco) some dentro da caixa branca de "paga o". O "o" fica solto no fim da linha. `evidencias/VP01_05.60s_descendentes_g_p_cortados_paga_o.jpg`
2. Tempo de leitura: [02,20–05,20] "Ela avisa antes: barulho novo, freio mais mole, corrente batendo." tem 10 palavras e só fica completa de 3,73s a 5,20s (1,5s), quando precisaria de ~5s. [07,40–09,63] "Quem anota, paga só a manutenção." tem 6 palavras em 2,2s, quando precisaria de 3s. O gancho só fica completo de 0,53s a 2,2s. `VP01_02.2-05.2s_tempo_de_leitura.jpg`
3. Legendas: IG/FB está "📌 Salva e manda…" (o formato é "📌 Salva pra não esquecer e manda pra quem…"); TikTok está "📌 Manda pra quem…" (o formato é "📌 Salva e manda pra quem…").
MELHORIAS:
1. É um slide de texto sem nenhum motion design. O nível do acervo pede pelo menos ícones ou B-roll de moto em cada frase.
2. [05,20] e [07,40] Cortes secos de fundo escuro para azul chapado e de volta, com salto de luminância de 22 para 80, que incomodam no celular. Usar wipe ou máscara.
3. Ponto positivo: o loop fecha bem (termina na frase do gancho).
NOTA: 5/10

### VP02 (O app em ação) — REPROVADO
ERROS:
1. [04,60–07,20 × 07,20–09,80] Prints contraditórios: "Filtro de óleo 07/11/2026, 24.400 km" e depois "Óleo do motor 07/11/2026, 18.400 km".
2. Zona segura: o celular desce até y≈1700. O botão "Confirmar troca" (04,6–7,2s) e o texto da tela de combustível (12,4–14,8s, medido até y=1688) ficam dentro dos 380px de baixo, onde a legenda do TikTok/Reels cobre. `VP02_05.67s_e_14.70s_print_na_zona_insegura.jpg`
3. Tempo de leitura: cada cena dura ~2,6s com título, subtítulo e print. Exemplo: "Tudo vira histórico. Com o quanto você pagou em cada serviço." tem 11 palavras em 2,6s.
4. Legendas fora do formato do §5 (o mesmo problema do VP01).
MELHORIAS:
1. O formato promete "app em ação" e não tem ação: são prints parados com crossfade, sem toque, rolagem ou zoom no dado que importa.
2. [00,00–02,00] O gancho é genérico e quebra mal ("Onde você / anota / a manutenção / da sua moto?", com "anota" sozinho). Sugestão: "Caderninho, nota fiscal ou memória?"
3. [12,4–14,8] O print mostra "Autonomia estimada --" (vazio). [15,3–17,4] O final fica parado 2,1s e não volta pro começo.
NOTA: 4,5/10

### VP03 (POV: o mecânico pergunta) — REPROVADO
ERROS:
1. [00,00–03,40] O gancho "O MECÂNICO PERGUNTA: QUANDO FOI A ÚLTIMA TROCA DE ÓLEO?" tem 9 palavras em caixa-alta, texto médio (~54px), por 3,4s. Precisaria de ~4,5s pra 2 leituras e de letra maior no 1º frame.
2. Legendas fora do formato do §5.
MELHORIAS:
1. [00,00–03,40] A foto é o mesmo modelo do AG02 e do B16, olhando pra baixo. O POV não fecha: a cena não mostra mecânico nenhum perguntando. Pôr um mecânico olhando pra câmera, ou só texto sobre a oficina.
2. [05,80] e [07,20] Cortes secos de fundo escuro para azul chapado (Δ72 de luminância).
3. [10,40] O subtítulo "Baixe o MinhaMoto." entra antes do título "Seja o cliente que sabe.", em ordem invertida.
4. A piada "Uns 3 meses… ou 6? Sei lá." é a melhor ideia de roteiro do lote. Estender esse momento.
NOTA: 6/10

### VP04 (5 erros que encurtam a vida da moto) — REPROVADO
ERROS:
1. **[10,60s, frame 318] Frame com fundo preto**, só com o número "1", entre a cena 2 e a cena 1: um flash preto de 1 frame. `evidencias/VP04_10.53-10.77s_frame318_fundo_preto.jpg`
2. [02,20–04,33] "RODAR COM PNEU MURCHO" aparece sobre pneu de trilha enlameado (cheio, não murcho) com placa estrangeira. A foto não combina com o texto.
3. [00,00–02,20] O gancho quebra em "5 erros que / encurtam a / vida / da sua moto": "a" solto no fim e "vida" sozinha.
4. Tempo de leitura: cada item dura ~2,1s com título e subtítulo de 8–10 palavras, quando precisaria de ~4–5s.
5. Legendas: fora do formato do §5, e "manda pra quem precisa ver esse vídeo" não é pessoa específica.
MELHORIAS:
1. Todas as fotos são recicladas dos carrosséis do mesmo lote (pneu, moto Kawasaki, entregador borrado).
2. [02,20] "Gasta mais" fica vago: gasta o quê? Sugestão: "Gasta pneu e combustível e tira estabilidade."
3. O final fica parado 2,1s e não faz loop.
NOTA: 4/10

### VP05 (Quiz 10W-30) — REPROVADO
ERROS:
1. [05,73–08,33] A tela da explicação fica 2,6s sem nenhuma mudança visual, acima do limite de 2,5s do checklist. `VP05_05.73-08.33s_tela_parada_2.6s.jpg`
2. [09,00–11,80] "Regra de ouro: / use o que o / manual da sua / moto / indica.": "o" solto no fim da linha e "moto" e "indica." sozinhas.
3. Tempo de leitura: a explicação "10W: como o óleo se comporta no frio. 30: na temperatura de trabalho do motor." tem 14 palavras, em letra de ~40px, por ~3,7s.
4. Legendas: fora do formato do §5. A IG/FB pede "Responde nos comentários antes de ver a resposta" e na frase seguinte já dá a resposta.
MELHORIAS:
1. O conteúdo fica todo entre y 220 e 1100 e a metade de baixo da tela fica vazia o vídeo inteiro. Centralizar e aumentar as opções.
2. A contagem 4-3-2-1 não tem tensão. Pôr uma barra de tempo e destacar o erro antes do acerto.
3. O fato está correto (W = winter, 30 = viscosidade a quente).
NOTA: 5/10

---

## STORIES

Medidas: 1080×1920. Zonas seguras do §6c: 250px em cima e 340px embaixo (limite em y=1580).

### ST01 (Enquete) — REPROVADO
ERROS:
1. O título quebra em "quando foi a / última troca": "a" solto no fim da linha.
MELHORIAS:
1. O sticker fica bem posicionado (y≈1180–1475, fora das zonas) e o texto começa em y≈300. Está OK.
2. Opção de enquete mais forte: "Sei de cabeça" / "Vou ter que chutar".
NOTA: 7/10

### ST02 (Você sabia) — REPROVADO
ERROS:
1. A caixa azul corta a perna do "p" de "por km", corta o "r" de "por" na borda direita e encosta em "tempo." sem margem na borda esquerda, onde o "p" também some. A linha "e também por" tem um espaço inicial dentro da caixa. `evidencias/ST02_destaque_cortando_letras.jpg`
MELHORIAS:
1. O fato está confirmado. O "?" gigante no canto ficou bom.
NOTA: 4/10

### ST03 (Tela do app) — REPROVADO
ERROS:
1. O celular vai até a borda de baixo (y=1920), e as linhas "Tubo de dreno do filtro de ar" e "Facho do farol" ficam na faixa dos 340px que a barra de resposta cobre. O `como_usar` manda pôr o sticker de link "no rodapé", que é justamente onde está o print: o sticker vai cobrir o print. `evidencias/ST03_print_na_zona_insegura.jpg`
MELHORIAS:
1. O print mostra "21 itens a confirmar / 0/5", que dá impressão de bagunça. Usar um print com tudo em dia.
NOTA: 5/10

### ST04 (Caixa de perguntas) — APROVADO
ERROS: nenhum.
MELHORIAS:
1. No corpo, "revisão. A / gente" deixa o "A" solto. Quebrar antes: "revisão. / A gente responde…"
2. "A gente responde as melhores nos stories" → "…nos próximos stories."
3. O sticker está em y≈1180–1475, livre e centralizado. O contraste é alto.
NOTA: 8/10

### ST05 (CTA de download) — REPROVADO
ERROS:
1. O título quebra em "Sua moto no / controle.": "no" solto no fim da linha.
MELHORIAS:
1. "Sua moto" fica sobre o espelho e o guidão da foto (área poluída). Escurecer mais o topo ou descer o título.
2. Confirmar o link "minhamotopagina.online" antes de publicar.
3. O sticker de link está em y 1360–1510, dentro da área segura. OK.
NOTA: 6,5/10
