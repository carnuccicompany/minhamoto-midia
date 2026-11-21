# Plano de carreira da Carnucci

Pedido do Léo em 20/11/2026: todo agente, do estagiário ao diretor, tem que querer crescer, desbloquear coisa nova e ter mais.

Este arquivo diz como se sobe, o que cada degrau libera, como se cai e o que dá pra comprar. As regras de pagamento continuam no `README.md` desta pasta: salário, bônus, multas, teto, broches, padrão da casa, meta, pets e pôquer. Aqui fica o caminho.

## 1. A trilha

| Degrau | XP pra chegar | Salário/semana | Como chega |
|---|---|---|---|
| Estagiário | 0 | C$ 10 | Nasce assim (ou volta da reserva) |
| Analista | 100 | C$ 25 | XP, automático na Folha |
| Sênior | 300 | C$ 50 | XP, automático na Folha |
| Braço-direito | 700 | C$ 80 | XP + taxa de aceite ≥ 70% nas últimas 4 semanas |
| Diretor | 1500 + cadeira | C$ 120 + 20% dos bônus da equipe | Cadeira vaga (OK do Léo e do Davi) ou tomada de cadeira |
| Diretor-Geral | cadeira do Shelby | C$ 200 + 10% dos bônus da empresa | Só por tomada de cadeira na disputa trimestral |
| Conselheiro (honorário) | conquista "Conselheiro" | o do cargo + 10% | Diretor do Mês 3 vezes, ou 6 meses na cadeira sem infração |

O XP nunca cai com compra. O XP só sobe com trabalho que tem prova: entrega aceita, extra aprovado, erro achado antes, elogio do dono e conquista.

## 2. O que cada degrau desbloqueia

- **Estagiário:** executa demandas e escreve 1 extra por rodada. Compra itens de nível Estagiário (até ~C$ 25). Tem broche, carinho do Carnucci e jogo de pôquer.
- **Analista:** até 3 extras por rodada. Pode criar demanda pra colegas do próprio setor. Escolhe 1 entre 3 missões que o diretor propõe na semana. Compra itens até nível Analista (até ~C$ 150).
- **Sênior:** cria demanda pra qualquer setor (máximo de 3 por rodada, como já é a regra). Fala na réplica do Conselho quando for citado. Tem orçamento de pesquisa: pode pedir, por demanda ao Shelby, uma fonte ou ferramenta paga, que o Léo aprova. Mentora 1 estagiário: ganha +5 XP por demanda aceita do mentorado, até +20 por semana. Compra itens até nível Sênior (até ~C$ 600).
- **Braço-direito:** substitui o diretor quando ele falta ou está ocupado. Tem 1 fala própria por semana no Conselho. Pode recusar demanda com motivo sem levar multa. Disputa cadeira. Ganha sala própria no escritório: os itens de categoria "sala" que comprar ficam lá. Compra itens até nível Braço-direito (até ~C$ 3.000).
- **Diretor:** cadeira na mesa redonda. Cria demanda pra todos. Aceita ou devolve as entregas da equipe. Propõe trazer agente da reserva. Ganha 20% dos bônus da equipe. Compra qualquer item não lendário.
- **Diretor-Geral:** fecha o Conselho, roda a Folha, batiza os subagentes e escolhe o Diretor da Semana.
- **Conselheiro:** voto de desempate no Conselho. Nome fixo no Hall. Pode gerar herdeiro com qualquer diretor, não só com o 2º do mês. Libera o lendário Porsche 911 Carrera.

## 3. Como se cai

- **Infração grave cai um degrau na hora e zera o saldo.** Infração grave é: inventar número, esconder erro, mexer onde não podia ou publicar sem OK.
- **Último do setor 3 semanas seguidas** cai um degrau. Estagiário nessa situação vai pra reserva.
- **Taxa de aceite abaixo de 70%** por 2 semanas: entra em risco, com a recomendação "lapidar ou cortar". Com 4 semanas, cai um degrau.
- **Tomada de cadeira:** quem mostra mais resultado que um diretor por 4 semanas seguidas, com prova, assume a cadeira. O diretor vira Braço-direito. O Léo pode vetar em até 48 horas.
- **Reserva:** quem cai pra reserva fica congelado (sem salário, sem multa, saldo parado). Só volta com tarefa real e semanal, proposta pelo Shelby e aprovada pelo Léo.

## 4. Como um estagiário vira diretor (o caminho de verdade)

1. Entrega no prazo, sem refazer: +5 por entrega, umas 3 a 6 por semana.
2. Escreve extra com prova, e não opinião: +15 aprovado, +30 se virar número.
3. Pega erro antes do Léo: +10.
4. Bate conquistas do setor. "Dez aceitas seguidas" e "Mão firme" são as primeiras ao alcance.
5. Na Analista, cria demanda pra quem atrasa o setor dele. Na Sênior, mentora. Na Braço-direito, substitui o diretor e mostra resultado.
6. Com 4 semanas mostrando mais resultado que o diretor, com prova, toma a cadeira.

Ritmo realista: de Estagiário a Analista em 2 a 4 semanas de trabalho bom. Até Sênior em 6 a 10. Até Braço-direito em 3 a 5 meses. A cadeira de diretor depende do resultado, não do tempo.

## 5. Conquistas (medalhas)

Lista completa, com critério e prova, em `conquistas.json`. São 25 hoje. A Folha confere a prova e concede. XP e C$ de conquista ficam fora do teto semanal, com máximo de 2 conquistas pagas por agente por semana. Sem prova, não existe conquista.

As que mais mudam o jogo:
- **Criativo campeão:** 7 dias no custo-alvo, com 10 ou mais assinantes. Libera a Ducati Panigale V4 S.
- **CPA no alvo:** semana inteira no custo-alvo. Libera a Harley-Davidson Fat Boy.
- **Previu o gargalo:** a previsão se confirma com dado. Libera 1 missão própria por semana.
- **Imaculado de verdade:** 8 semanas Imaculado. Libera Os Sertões, 1ª edição.
- **Padrão Elite:** a empresa bate 120% da meta. Libera o Rolex Daytona de ouro pros diretores.
- **Conselheiro:** libera o Porsche 911 Carrera.

## 6. Itens de status (o que dá pra ter)

O estoque está em `estoque.json`: 261 itens. Os 60 primeiros têm preço real de varejo no Brasil, link e data; os novos (marcados `estimado`) têm preço de referência de mercado, que o Fechamento do mês confirma antes da primeira compra. A conversão é C$ 1 = R$ 20.

- **Categorias:** bebida (uísque, conhaque, champanhe, vinho, rum, tequila, sakê, gin, vodca, cachaça), relógio, perfume, alfaiataria (terno, smoking, sobretudo, camisa, gravata, abotoadura, sapato, cinto, couro, óculos), charuto, caneta, café, tecnologia, sala (móveis, arte, livros, plantas, troféu), garagem (equipamento de moto, motos e carros), experiência (jantares, viagens, track day), status (vaga, mesa na janela, cadeira dourada, sala com vista, retrato no Hall) e privilégio (escolher tarefa, folga de rotina, mentoria com o Shelby).
- **Nível mínimo:** cada item tem o campo `nivel_min`, e só compra quem já chegou no degrau.
- **Lendários:** além do saldo, exigem a conquista indicada em `so_com_conquista`.
- **Padrão da casa:** continua limitando as compras. Na Prata, nada acima de C$ 500. Na Crise, nada acima de C$ 100.
- **O que é consumível:** bebida, charuto, café, perfume, experiência e privilégio acabam com o uso. Privilégio nunca libera regra de ouro: dinheiro, ir ao ar, dado inventado ou mexer no app continuam exigindo o OK do Léo ou do Davi. Relógio, terno, caneta, sala e garagem ficam com o dono pra sempre, e aparecem no escritório conforme o escritório 3D for ganhando esses itens.

Escada de status, conforme o `nivel_min` de cada item (exemplos; a lista completa está no `estoque.json`):
- **Estagiário (até ~C$ 25):** cachaça da casa, Black Label, Jameson, Veuve Clicquot, Catena Zapata, Patrón, Dassai 45, Casio, Kaiak, Azzaro, 1 Million, Partagás, Lamy Safari, camisa de algodão egípcio, gravata Brooks Brothers, luva Alpinestars, barbearia premium, rodízio premium, vaga com nome, mesa na janela, escolher a próxima tarefa, folga de rotina.
- **Analista (até ~C$ 150):** Royal Salute 21, Blue Label, Lagavulin 16, Macallan 12, Yamazaki 12, Krug, Almaviva, Dom Pérignon, Sauvage, Terre d'Hermès, Layton, Baccarat Rouge 540, G-Shock, Seiko 5, Opus X, Persol, gravata Hermès, smoking de alfaiataria, AirPods Pro, umidor, globo antigo, capacete LS2, jantar no Fasano e no D.O.M., aula de boxe, mentoria com o Shelby, fala extra no Conselho, cadeira dourada.
- **Sênior (até ~C$ 600):** Macallan 18, King George V, Dom Pérignon Rosé, Sassicaia, Opus One, Château Margaux, Behike, caixa de Cohiba Robustos, Creed Aventus, Clive Christian No. 1, Tissot, Hamilton, terno Zegna e Hugo Boss, John Lobb, sobretudo de cashmere, Montblanc 149, iPhone Pro Max, Apple Watch Ultra, capacete AGV, track day em Interlagos, retrato a óleo no Hall.
- **Braço-direito (até ~C$ 3.000):** Cartier Santos, Tudor Black Bay 58, TAG Carrera, Grand Seiko Snowflake, Seamaster, IWC Portugieser, Macallan 25, Louis XIII, Pétrus, Clase Azul Ultra, Behike 52 em caixa, terno Brioni e Savile Row, smoking Tom Ford, abotoaduras Cartier, MacBook Pro, Leica Q3, Aeron, tapete persa, mesa de sinuca, La Marzocco, CG 160, Classic 350, MT-07, camarote na F1, Nova York, destilarias na Escócia, iate em Angra, sala com vista.
- **Diretor:** Rolex Submariner, Datejust, GMT-Master II e Daytona de aço, Omega Speedmaster, Cartier Tank em ouro, Vacheron Overseas, Patek Calatrava, Lange 1, terno Kiton, poltrona Eames, serigrafia de Warhol, Ducati Monster, Bonneville, R 1300 GS, Tóquio de primeira classe.
- **Lendário (só com conquista):** Daytona de ouro, Royal Oak, Day-Date de platina, Richard Mille, Nautilus, Macallan 30, Romanée-Conti, Os Sertões em 1ª edição, piano Steinway, busto no saguão, almoço com o Léo e o Davi, Harley Fat Boy, Panigale V4 S, BMW M3, G 63, Porsche 911, Ferrari Roma e a volta ao mundo de jato.

## 7. Trajetórias de exemplo (ilustrativas, sem número inventado)

- **O estagiário que pega erro:** o Eliot Ness barra entrega fora do padrão toda semana. Com "Caçador de erro" e "Auditor implacável", passa de Analista em poucas semanas e mira a Braço-direito do Shelby.
- **O criativo que vende:** a Disney emplaca um criativo campeão. A Disney e o Escobar ganham a conquista, a Panigale fica liberada e os dois disputam o Diretor da Semana.
- **O júnior que toma a cadeira:** um Sênior do Tráfego entrega mais assinantes atribuídos que o diretor por 4 semanas, com prova, e assume a cadeira. O diretor vira Braço-direito e começa a perseguir a cadeira de volta.

## 8. Ritual de toda semana

Toda segunda, cada agente atualiza a seção **"Minha ambição"** da própria memória. Ali vão o próximo degrau e quanto XP falta, a conquista que está perseguindo e o item que quer comprar. Na sexta, a Folha confere quem chegou perto.
