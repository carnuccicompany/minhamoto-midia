# VENDA-MM-R1 · criativos de venda do MinhaMoto · rodada 2 (24/11/2026)

Refeito depois da revisão independente (`/home/claude/revisao/relatorio-venda-mm.md`) e das 14 regras novas do DESIGN-MINHAMOTO.md.
6 vídeos 9:16 · 1080x1920 · 30 fps · sem voz (texto + efeitos sonoros). Motor: `agencia/estudio/motores/venda_mm_r1.py`.

**O que vale pra todos**
- Telas só do iPhone (`telas-app/ios-1.0/`). A barra de abas aparece também na rolagem e o cabeçalho é igual em todas as telas.
- Folha (pop-up) abre como no iOS: o fundo escurece e o painel sobe.
- Destaque: o trecho real da tela sai do celular, ampliado. Depois **volta pra linha real** e só então some, sem texto fantasma. Isso tem trava automática.
- Texto branco com a palavra-chave em limão; vermelho só em alerta.
- CTA de 4 s que nunca fica parado: o brilho do ícone respira e o selo de preço pulsa uma vez. Traz "Baixe agora o MinhaMoto.", "por R$19,90" e os selos das lojas.

## Variedade (regra 2)
| # | Visual | Telas próprias (não aparecem em outra peça) | Recortes |
|---|---|---|---|
| V1 | navy + celular, gancho com o alerta gigante | 21 item atrasado (folha) | vela vencida, folha da vela, corrente "faltam 100", óleo/freio/pneus |
| V2 | foto de moto na serra (desfocada atrás do celular) + painel em km/h da mesma moto | 07 documentos, 27 marco 30.000 | troca de óleo no histórico, óleo SAE, CRLV/CNH, marco 30.000 |
| V3 | foto da cub na rua (sol), 3 planos | 28 corrente (folha) | folha da corrente, lembrete "29.900 km · a cada 1.000 km" |
| V4 | bancada de oficina + painel digital da moto de rua, depois navy | 12 sinais de problema | pastilhas em dia, "Freio esponjoso · pastilhas no fim", pastilhas no histórico |
| V5 | foto clara de moto na garagem (3 planos) | 29 manutenção · aba Tempo | card Tempo, bateria |
| V6 | 4 fotos (trail, pneu, corrente, scooter) com um tratamento de cor só + fundo azul vivo | 11 cuidados | pneu traseiro (calibragem), corrente (cuidados) |

Saúde aparece só em V1 e V4; Histórico em V2 e V4; Lista para revisão em V2 e V6. Nenhum recorte se repete entre peças.

| # | Formato | Duração | Público | Ângulo | Gancho (1º segundo) |
|---|---|---|---|---|---|
| V1 | Tela do app | 19,0 s | motoboy / entregador | controle | alerta vermelho "Troca vencida · Vela de ignição" gigante, com bipe, que voa e encaixa no app + "Moto parada é dia sem **ganhar**." |
| V2 | Tela do app | 30,8 s | hobby | orgulho da moto | moto na serra com push-in + "Moto bem cuidada tem **histórico**." · "A sua tem?" |
| V3 | Historinha da dor | 19,6 s | quem vai trabalhar de moto | medo de prejuízo | moto de trabalho com zoom forte + "Segunda-feira, 7h40 · A corrente **escapou** indo pro trabalho." |
| V4 | Historinha da dor | 31,9 s | motoboy | economia | "Pastilha de freio: R$ 224. Ele adiou." → "Disco novo: R$ 606,28" (mesma loja) |
| V5 | Nativo/POV | 23,1 s | hobby / fim de semana | medo de prejuízo | moto parada com zoom + "POV: domingo, rolê marcado… e a moto **não pega**." |
| V6 | Nativo/POV | 31,6 s | iniciante | controle | moto com capacete no banco, zoom + "3 erros de quem tem a **primeira moto**." |

---

## V1 · Controle (tela do app · motoboy) · 19,0 s
- **Gancho:**
  - 0–1,55 · o card vermelho real "Troca vencida · Vela de ignição · Passou 300 km" aparece gigante (bipe de alerta + grave) e voa até a linha dele na tela, enquanto o celular entra.
  - 0–2,5 · "Moto parada é dia sem **ganhar**."
- **Corpo:**
  - 2,5–5,4 · "O que vence primeiro aparece **primeiro**." · o card destaca e um toque em "Ver" abre a folha.
  - 5,4–8,6 · "E mostra quando **era pra trocar**." · folha da vela: "Era para trocar aos 29.500 km".
  - 8,6–11,8 · "Chegando a hora? O app **avisa antes**." · corrente, "faltam 100" (com notificação).
  - 11,8–15,0 · "Óleo, freio, pneus: tudo **no seu km**." · bloco "Tudo certo por aqui".
- **CTA (15,0–19,0):** "Moto de trabalho **sob controle**."

## V2 · Orgulho da moto (tela do app · hobby) · 30,8 s
- **Gancho (0–3,4):** foto de moto na estrada de serra (POV do guidão) com push-in · "Moto bem cuidada tem **histórico**." · "A sua tem?"
- **Corpo** (celular sobre a mesma foto desfocada):
  - 3,4–8,6 · "Cada serviço salvo, com **data, km e valor**." · Histórico → "Troca de óleo e filtro · 25/08/2026 · 27.100 km · R$ 120,00".
  - 8,6–13,6 · "O manual dela **na palma da mão**." · Lista → "Óleo do motor · SAE 10W-30 API SL+ JASO MA".
  - 13,6–18,6 · "CRLV, CNH e seguro **num lugar só**." · Documentos → CRLV digital + CNH.
  - 18,6–23,6 · "A próxima revisão **já está no radar**." · Marco → "30.000 km · Faltam 200 km".
  - 23,6–26,75 · painel da mesma moto (km/h), push-in · "Seu capricho, **registrado**."
- **CTA (26,75–30,75):** "Moto cuidada **se vê de longe**."
- Sem carteirinha e sem nenhum item vencido em destaque (é peça de orgulho).

## V3 · Corrente no caminho do trabalho (historinha · trabalho) · 19,6 s
- **Gancho (0–3,4):** moto de trabalho parada na calçada, sol da manhã, zoom forte de saída · kicker vermelho "Segunda-feira, 7h40" · "A corrente **escapou** indo pro trabalho."
- **Corpo:**
  - 3,4–6,8 · roda traseira da cub (plano neutro; o banco não tem foto de corrente seca) · "Seca, folgada… e **ninguém ajustou**."
  - 6,8–10,2 · a moto parada · "Atraso, guincho e **dia perdido**."
  - 10,2–12,6 · celular com a folha da corrente ("Alta prioridade · Lubrificar e ajustar a corrente") + notificação · "O MinhaMoto **teria avisado**."
  - 12,6–15,6 · recorte "Lubrificar quando a moto estiver com 29.900 km · a cada 1.000 km" · "Lubrificar e ajustar **no km certo**."
- **CTA (15,6–19,6):** "A moto avisa tarde. O MinhaMoto, **antes**."
- Causa técnica trocada: corrente seca e folgada escapa da coroa; isso acontece de verdade. A vela 300 km vencida saiu.

## V4 · Pastilha adiada risca o disco (historinha · motoboy · economia) · 31,9 s
- **Gancho (0–4,5):** bancada de ferramentas com zoom · "Pastilha de freio: **R$ 224**. Ele adiou." · em 1,5 s entra "Disco novo:" e "**R$ 606,28**" (vermelho, prejuízo). Rodapé: "Pastilha dianteira original Honda R$ 224,27 · Disco de freio dianteiro CG 160 Titan/Fan R$ 606,28 · Winner Honda Store (Limeira/SP) · nov/2026".
- **Corpo:**
  - 4,5–8,5 · painel digital da moto de rua, com o km rodado · "Rodando o dia todo, a pastilha ficou **pra depois**."
  - 8,5–12,5 · guidão e tanque da mesma moto (plano neutro) · "Gastou até o metal e **riscou o disco**."
  - 12,5–15,9 · bancada de oficina, com tremida + impacto · "Freio fraco, barulho… e **disco novo**."
  - 15,9–20,1 · Saúde → "Pastilhas / sapatas de freio · Em dia · faltam 10.800" · "O app mostra quando **trocar a pastilha**."
  - 20,1–24,1 · Sinais de problema → "Freio esponjoso ou curso longo do manete · Pare agora · … pastilhas no fim" · "E explica o sinal: **pastilha no fim**."
  - 24,1–27,9 · Histórico → "Pastilhas dianteiras e fluido de freio · 06/07/2026 · 25.600 km" · "Cada troca salva, com **data e km**."
- **CTA (27,9–31,9):** "Cuidar **custa menos** que consertar."
- O banco não tem foto de disco riscado: as cenas da causa usam planos neutros (painel e guidão da moto de rua, bancada), nunca peça perfeita sob texto de defeito.

## V5 · Moto parada também vence (POV · hobby) · 23,1 s
- **Gancho (0–4,0):** moto de passeio parada na garagem, clara, zoom de saída + 2 cliques de chave sem partida · "POV: domingo, rolê marcado… e a moto **não pega**."
- **Corpo:**
  - 4,0–8,0 · plano fechado na roda/garfo · "Bateria arriada. Ficou **parada** o mês todo."
  - 8,0–12,6 · plano no farol · "Parada, a moto também **tem prazo**." · "Bateria, óleo, fluido de freio."
  - 12,6–16,15 · celular, aba Tempo → card "Tempo · 4 itens · 1 em atenção" · "O MinhaMoto mostra o que vence **pelo tempo**."
  - 16,15–19,1 · linha da bateria ("Analisar") · "E o que já pede **atenção**."
- **CTA (19,1–23,1):** "Seu domingo de rolê, **sem surpresa**."

## V6 · Primeira moto (POV · iniciante) · 31,6 s
- **Gancho (0–3,8):** trail com capacete no banco, zoom de saída · "3 erros de quem tem a **primeira moto**."
- **Corpo** (selo limão 1-2-3, uma foto nítida por dica):
  - 3,8–8,2 · pneu de perto · 1 · "Calibrar com o pneu **quente** dá errado."
  - 8,2–12,8 · corrente · 2 · "Esquecer a corrente: ela pede óleo **a cada 1.000 km**."
  - 12,8–17,2 · scooter de banco inteiro · 3 · "Levar garupa na pressão de quem anda **sozinho**."
  - 17,2–22,6 · fundo azul vivo, Lista → "Pneu traseiro · 29 psi sozinho · 33 psi com garupa · sempre com o pneu frio" · "O MinhaMoto traz isso **do seu modelo**."
  - 22,6–27,55 · Cuidados → "Corrente de transmissão" (passo a passo) · "Com o passo a passo **do manual**."
- **CTA (27,55–31,55):** "Primeira moto, **zero achismo**."

---

## Texto principal dos anúncios (sugestão)
- **V1:** Moto de trabalho parada é dia sem ganhar. O MinhaMoto mostra o que venceu, o que tá chegando e o que tá em dia, no km da sua moto. 📲 Baixe agora o MinhaMoto na App Store e no Google Play.
- **V2:** Caderninho some, molha e fica pra trás. No MinhaMoto ficam cada serviço com data, km e valor, os documentos e a próxima revisão já planejada. 📲 Baixe agora o MinhaMoto na App Store e no Google Play.
- **V3:** Corrente seca e folgada escapa na hora errada. O MinhaMoto avisa quando lubrificar e ajustar, no km da sua moto. 📲 Baixe agora o MinhaMoto na App Store e no Google Play.
- **V4:** Pastilha de freio: R$ 224. Disco novo: R$ 606,28. Pastilha adiada gasta até o metal e risca o disco. O MinhaMoto mostra a hora de trocar a pastilha no km da sua moto e guarda cada troca. 📲 Baixe agora o MinhaMoto na App Store e no Google Play.
- **V5:** Moto parada também tem prazo: bateria, óleo, fluido de freio. O MinhaMoto mostra o que vence pelo tempo, pra moto não deixar você na mão no domingo. 📲 Baixe agora o MinhaMoto na App Store e no Google Play.
- **V6:** Primeira moto? O MinhaMoto traz a calibragem certa, o plano do manual e a hora de cada cuidado do seu modelo. 📲 Baixe agora o MinhaMoto na App Store e no Google Play.

## Áudio
- Decisão do Léo (24/11): entregar **só a versão sem música**, porque ele põe a trilha na hora de anunciar. Os efeitos são sutis: whoosh suave, clique curto, pop, notificação, bipe de alerta e grave. Ficam a -14 LUFS, com TP ≤ -2 dBTP.
- Se um dia precisar da versão com trilha, o motor já tem o comando: `python3 venda_mm_r1.py trilha V1 faixa.mp3`. Ele põe a música a -14 LUFS e os efeitos ~6 dB abaixo, sem renderizar o vídeo de novo.
