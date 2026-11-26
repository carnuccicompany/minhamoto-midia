# Telas reais do MinhaMoto: visual novo (1.0.2)

- **Código do app:** `minhamotooficial` em `origin/HEAD` = `d4942b2a` (25/11/2026, "Código de amigo aberto a todos, rodapé das folhas sem retângulo e novidades da 1.0.2"). Inclui `87411f1b` (visual novo no app inteiro) e `a36f3e31` (folhas no padrão Apple/Spotify).
- **Captura:** 26/11/2026, relógio fixo às 9:41 (America/Sao_Paulo), pt-BR.
- **Formato:** PNG 1179×2556 (iPhone 393×852 @3x), barra de status 9:41 e indicador de início desenhados por cima. As páginas inteiras (`rolagem/`) não têm a ilha de abas.
- **Telas antigas** (`../01-…png`, `../rolagem/`, `../ios-1.0/`): visual anterior, **não usar mais**.

## Dados (100% fictícios)

Moto "Minha Titan": Honda CG 160 Titan 2022, 29.800 km, placa BRA2E19, dono Rafael Souza (rafael.souza@email.com), média de 30 km/dia, assinatura Pro ativa, conta antiga (sem tutorial) e tutorial parado. Histórico com 9 serviços (R$ 1.610,00), entre eles troca de óleo e filtro aos 27.100 km. 9 abastecimentos em dois postos. 4 avisos na central (2 não lidos). Vela de ignição vencida (passou 300 km), corrente e válvulas chegando.

Mudança na semente em relação a 23/11: bateria trocada aos 21.500 km (novo registro "Troca da bateria", R$ 260). Sem ela a Saúde mostrava "Avaliação parcial". Agora mostra "89% · Manutenção em dia · Atenção" (a atenção vem da vela vencida).

## Telas

| arquivo | o que mostra |
|---|---|
| 01-garagem | Garagem: Minha Titan (29.800 km), 825 km e R$ 45 no mês, alerta da vela, vaga livre |
| 02-saude | Saúde da moto: medidor 89%, "Manutenção em dia · Atenção", odômetro, dados da moto 82% |
| 02b-saude-sistemas | Saúde rolada: Sistemas da moto (Motor 67%, Freios e pneus 100%, Transmissão 80%, Elétrica 100%) e Cuidados (1 agora, 2 atenção, 7 em dia) |
| 03-manutencao | Manutenção: cena da estrada "Revisão da vez 30.000 km · faltam 200 km", emblema 25k, Por quilometragem |
| 04-uso-km | Uso da moto: 30 km/dia, 210 por semana, projeção dos itens pelo ritmo |
| 05-combustivel | Combustível: tanque 3D 100%, 37,4 km/L de média, 612 km para rodar, R$ 0,16/km |
| 06-historico | Histórico de manutenção: 9 registros, R$ 1.610, lavagem, corrente, troca de óleo |
| 07-documentos | Documentos da moto: CRLV, CNH, licenciamento, seguro, nota fiscal (sem arquivos) |
| 08-moto-especificacoes | Moto/ficha: CG 160 Titan, descrição técnica e ficha rápida |
| 09-resumo-mes | Resumo do mês: 825 km, 1 manutenção, R$ 45, comparação com outubro |
| 10-lista-revisao | Lista para revisão: óleo SAE 10W-30, filtro de ar, vela NGK, fluido DOT 4, pneus com calibragem (na rolagem) |
| 11-cuidados | Cuidados com a moto (manual): óleo, corrente, freios |
| 12-sinais-problema | Sinais de problema: luzes do painel e comportamentos (FI, medidor de combustível…) |
| 13-conheca-moto | Conheça sua moto: especificações por sistema |
| 14-carteirinha | Carteirinha da moto: km, placa, itens em atenção, situação geral |
| 15-notificacoes | Notificações: "O prazo passou", "Quer conferir a previsão?", odômetro, cuidado chegando |
| 16-perfil | Perfil: Rafael Souza, e-mail + Google |
| 21-item-atrasado | Folha da vela de ignição VENCIDA (era para trocar aos 29.500 km) |
| 22-registrar-servico | "Troquei agora" da vela: confirmar a troca (data, km 29.800) |
| 23-registrar-servico-itens | Mesmo formulário com produto (Vela NGK CPR8EA-9) e valor (R$ 45,00) preenchidos |
| 24-comparacao-postos | Combustível: comparação de postos e consumo a cada tanque cheio |
| 25-fontes | Fontes e confiabilidade (manual do fabricante) |
| 26-registrar-abastecimento | Registrar abastecimento (26/11, 09:40, 29.800 km, regra dos 70% do etanol) |
| 27-marco-30000 | Manutenção: lista do marco de 30.000 km com "Inspecionar 16" aberto |
| 28-item-proximo | Folha "Lubrificar e ajustar a corrente" (marco de 30.000 km) |
| 29-manutencao-tempo | Manutenção rolada até "Por tempo": óleo (km + tempo), pneus, fluido de freio, bateria |
| 30-item-ja-fiz-antes | Vela: "Já troquei antes" com produto e valor preenchidos |
| 31-sistema-motor | Folha do sistema Motor 67%: vela vencida, válvulas, óleo, filtro de ar |
| 32-chegando-a-hora | Cena da estrada com o balão "Chegando a hora · 2 itens" (corrente e válvulas) |
| 33-combustivel-resumo-mes | Combustível rolado: resumo do mês (R$ 134,33), previsão e projeção |

`rolagem/` tem a página inteira de 01 a 16 e 25 (a Manutenção inteira inclui "Por tempo").

## Observações e problemas

- Nenhuma tela com erro, carregando ou em branco. Nenhuma requisição externa (todas bloqueadas). Nenhum erro de JS na passada final.
- A ilha de abas de vidro (rodapé) fica por cima do conteúdo nas telas de viewport. É o visual real do app, mas corta o fim da tela. Para recortar sem ela, use `rolagem/`.
- As nuvens da cena da estrada se mexem, então mudam de lugar entre uma captura e outra (03, 27, 32). Em 03 uma nuvem fica atrás do texto "30.000 km · faltam 200 km". É assim no app.
- Motor fica em 67% por causa da vela vencida (é a história dos dados: o app avisa o que passou do ponto). Para mostrar tudo verde, seria preciso tirar a vela vencida da semente, e aí as telas 21, 22, 23, 30, 31 e as notificações perdem o sentido.
- "Dados da moto 82% · 19 de 23": faltam arquivos de CRLV/CNH/seguro e a foto da moto (não simulados).
- 01-garagem, 02 e 08 mostram o símbolo MM no lugar da foto da moto (sem foto, como no app).
- Em 12-sinais-problema o aviso automático de "carregando" é falso positivo (o texto é "recarregando a bateria", do manual).
- Animações: a captura usa "reduzir movimento" do sistema. Assim contagens e mostradores já aparecem no valor final, igual a depois que a animação termina.

## Como reproduzir (`_gerador/`)

```bash
# cópia limpa (o repositório oficial nunca é tocado)
mkdir -p /tmp/app-102 && git -C /home/claude/minhamotooficial archive origin/HEAD | tar -x -C /tmp/app-102
cd /tmp/app-102 && rm -f .env && git init -q && git apply <v1.0.2>/_gerador/app-real.patch
cp -a /tmp/app-previa/node_modules node_modules   # + appsflyer-capacitor-plugin@7.0.4 e @appsflyer-sdk/js-core-plugin@7.1.0 (npm pack)
VITE_CONFIG_NATIVE_IGNORE_WARNING=true node_modules/.bin/vite dev --port 5176 --strictPort --host 127.0.0.1 &
mkdir -p /tmp/telas-102/_gerador && cp <v1.0.2>/_gerador/* /tmp/telas-102/_gerador/
python3 /tmp/telas-102/_gerador/capturar.py          # ou prefixos: capturar.py 02 29
python3 /tmp/telas-102/_gerador/folha.py /tmp/telas-102/_folha.jpg /tmp/telas-102
```

- `app-real.patch`: `.env` falso (`https://mock-supabase.invalid`), `lerLeituraEntrada()` devolve conta livre, `_authenticated.tsx` sem o envoltório do aceite legal (exige prova assinada pelo servidor real). Nenhum componente de tela alterado.
- `titan-fixtures.ts`: a moto simulada (antes era um patch em `src/lib/previa-fixtures.ts`). Agora fica fora do app, porque a prévia da 1.0.2 mudou esse arquivo. Tem os campos novos de documentos (CNH e seguro em dia) e a bateria.
- `semente.ts` (bun): gera `dados.json` e `local.json` com as funções reais do app (textos das notificações, chaves da central e das dicas).
- `capturar.py`: roteiro das telas, com `folhas.json` para os cliques. É o mesmo do 23/11, mais "reduzir movimento", uma rolagem da página antes de cada foto (os blocos que aparecem ao entrar na tela ficam prontos) e o fechamento de folhas empilhadas.
- `explorar.py`: diagnóstico (lista botões, clica e mostra folhas).
