> 📱 **23/11 (noite) · VERSÕES DAS LOJAS.** iPhone = **1.0 build 33** (commit `7e17ed5`, aprovado 06/11). Android = **1.0.1** (no ar desde 17/11, ≈ main de 16/11). A 1.0.1 do iOS ainda não foi enviada (TestFlight build 40).
> - Telas desta pasta (raiz) = main 17/11 ≈ Android 1.0.1. Telas do iPhone 1.0 em `ios-1.0/`.
> - **Iguais nas duas versões (pode usar sem medo):** 03 manutenção, 04 uso, 05 combustível, 07 documentos, 09 resumo, 10 lista, 11 cuidados, 12 sinais, 13 conheça, 14 carteirinha, 16 perfil, 25 fontes, 22, 23, 26, 29, 30.
> - **Diferentes:** 01 garagem (card de transferência só no main), 02 saúde (89% main × 75% iPhone), 06 histórico (Exportar PDF só no main), 08 moto (botão Transferir só no main), 15 notificações (textos diferentes; a do iPhone tem erro de texto, não usar), 28 corrente (prioridade média × alta). Card de transferência, botão Transferir e Exportar PDF **não estão em nenhuma loja**: nunca mostrar.

> ✅ **23/11 (tarde) · TELAS REAIS.** Os PNGs desta pasta agora são capturas das **rotas reais do app logado** (`_authenticated.*`, componentes `GaragemHome`, `SaudeOficial`, `SinaisOficial`, `ManutencaoOficial` etc.), código `05425c9` (17/11), com Supabase/assinatura simulados em memória e moto fictícia Minha Titan. Nada de prévia. Como refazer: `_gerador-real/LEIAME.md` (patch numa cópia do app; nunca no repo do app; nenhuma rede externa).
> Telas: 01–16, 21–30 (sem 17–20, que eram cenários só da prévia). Rolagem: 01–16, 25, 27.
> ~~Telas da rota `/preview-visual`~~ → substituídas em 23/11. O texto abaixo é histórico do gerador antigo.

# Telas do app (geradas do código)

Telas do MinhaMoto renderizadas direto do código mais novo do app — **não** são gravações de tela.
Use sempre estas telas nos criativos. As gravações antigas do celular saíram do repositório.

- **Commit do app:** `05425c9` (minhamotooficial, main, 17/11/2026)
- **Gerado em:** 23/11/2026 pelo Estúdio (recaptura com o código de 17/11: inspeção vencida amarela, card "Receber moto por transferência" na Garagem, item "Assinatura" no Perfil; cenários 18/19 corrigidos; 03 e 21–23 recapturados)
- **Patch dos dados fictícios:** `_gerador/previa-fixtures.patch` (aplicar numa cópia do app, nunca no repo do app). Mexe em `previa-fixtures.ts`, `perfil-previa.tsx` e `central-previa.ts`.
- **Como:** modo "Prévia visual" do próprio app (`/preview-visual`, só roda em localhost). Ele bloqueia a rede e usa dados fictícios em memória. Nenhum login, Supabase ou RevenueCat foi usado.
- **Formato:** iPhone 15. Tela de 393×852 pt a 3x, ou seja 1179×2556 px. Barra de status limpa (9:41) e home indicator desenhados por cima. Os controles que só existem na prévia (botão DEV, selo "dados fictícios", chips de cenário, "Testar onboarding", "Só prévia", dicas do tutorial) foram escondidos.
- ~~**Dados (18/11):** moto simulada "Minha Titan" (Honda CG 160 Titan 2022, 29.800 km), histórico com 7 serviços, saúde 79%/95%, e as situações do app aparecendo: em dia (7 itens), precisa de atenção (corrente, bateria sem histórico), vencido (folga das válvulas), próximo marco 30.000 km (faltam 200). Dono fictício "Rafael Souza". Os dados foram trocados só numa cópia local do app (`src/lib/previa-fixtures.ts`), nunca no repositório do app. Nunca usar "Moto de demonstração".~~ → substituído em 23/11 (abaixo)
- **Dados (23/11):** Minha Titan (CG 160 Titan 2022, 29.800 km, placa fictícia BRA2E19), ~30 km/dia, 8 registros no histórico, 9 abastecimentos em 2 postos (37,4 km/L). Saúde 89% (avaliação parcial) e dados 95%. Vencido: vela de ignição (passou 300 km). Atenção: corrente (faltam 100 km), folga das válvulas (faltam 200 km), bateria (sem histórico). Em dia: óleo, pastilhas, pneus, kit relação, fluido de freio, filtro de ar. Próximo marco 30.000 km (faltam 200). Dono fictício Rafael Souza.
- **Barra de status:** desenhada em 4x e reduzida (`barra_status` em `_gerador/capturar.py`), sem ilha (a ilha é do mockup, igual em todas as cenas).
- **Não usar nos criativos:** `20-manutencao-atrasados` ("20 pendentes · 1.800 km acima do marco"). A `03` voltou a ser usável (23/11). Atenção: o app conta "itens que pedem atenção" diferente em cada tela (Garagem 4, Resumo 3): não citar esse número no texto da peça.

## Telas (1179×2556)

| Arquivo | O que mostra |
|---|---|
| 01-garagem.png | Garagem com 1 moto, resumo "pede atenção / gasto no mês" |
| 02-saude.png | Saúde da moto: anéis "Manutenção em dia" e "Dados", próximos cuidados |
| 03-manutencao.png | Manutenção: km atual 18.400, marco de 18.000 km, quilometragem × tempo |
| 04-uso-km.png | Uso da moto: km por dia/semana/mês |
| 05-combustivel.png | Combustível: consumo médio 28,1 km/L, autonomia, registrar abastecimento |
| 06-historico.png | Histórico de manutenção (troca de óleo, ajuste da corrente) |
| 07-documentos.png | Documentos da moto (CRLV, CNH, licenciamento…) |
| 08-moto-especificacoes.png | Ficha da moto (CG 160 Fan): especificações do manual |
| 09-resumo-mes.png | Resumo do mês |
| 10-lista-revisao.png | Lista para revisão: óleo, filtro, vela, pneus… com especificação |
| 11-cuidados.png | Cuidados com a moto |
| 12-sinais-problema.png | Sinais de problema (luzes do painel, barulhos) |
| 13-conheca-moto.png | Conheça sua moto: especificações por sistema |
| 14-carteirinha.png | Carteirinha da moto |
| 15-notificacoes.png | Notificações ("Você pediu, eu lembrei", previsão de troca) |
| 16-perfil.png | Perfil |
| 17-garagem-varias-motos.png | Garagem com 2 motos |
| 18-garagem-atencao.png | Garagem no cenário com itens atrasados (31.800 km) |
| 19-saude-atrasados.png | Saúde com "Troca vencida" do óleo (0% em dia, vermelho) |
| 20-manutencao-atrasados.png | Manutenção a 31.800 km, 1.800 km acima do marco |
| 21-item-atrasado.png | Detalhe do item atrasado: "Óleo do motor — Era para trocar aos 21.000 km" |
| 22-registrar-servico.png | Registrar serviço: data, produto "Óleo SAE 10W-30 + filtro", R$ 120,00, Salvar |
| 23-registrar-servico-itens.png | Registrar serviço com escolha de itens (Kit relação: "Troquei o conjunto") |
| 24-comparacao-postos.png | Comparação de postos: Posto Avenida 28,9 km/L × Posto Central 27,0 km/L |

## Rolagem (`rolagem/`)

Página inteira, 1179 px de largura e altura variável, **sem** barra de status e sem a barra de abas flutuante. Serve para animar rolagem nos vídeos: recorte uma janela de 1179×(2556−177−102) que desce pela imagem, depois cole por cima a barra de status e o topo da tela parada correspondente.

Arquivos: 01-garagem, 02-saude, 03-manutencao, 04-uso-km, 05-combustivel, 05-combustivel-postos (com comparação de postos), 06-historico, 07-documentos, 08-moto-especificacoes, 09-resumo-mes, 10-lista-revisao, 11-cuidados, 12-sinais-problema, 13-conheca-moto, 14-carteirinha, 15-notificacoes, 16-perfil, 19-saude-atrasados, 20-manutencao-atrasados.

## Regerar

`_gerador/capturar.py` + `_gerador/plano.json`. Para rodar:

1. Copie o app para uma pasta temporária e rode `bun install`. Se o mirror privado bloquear, troque no bun.lock as URLs do pkg.dev por registry.npmjs.org.
2. Suba o servidor: `bunx vite dev --port 5173 --host 127.0.0.1`.
3. Rode `python3 capturar.py plano.json`. Precisa de Playwright e do Chrome em /usr/bin/google-chrome.

Não faça commit no repositório do app.
