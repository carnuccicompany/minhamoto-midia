# Telas do app (geradas do código)

Telas do MinhaMoto renderizadas direto do código mais novo do app — **não** são gravações de tela.
Use sempre estas telas nos criativos. As gravações antigas do celular saíram do repositório.

- **Commit do app:** `bb2ad21` (minhamotooficial, main, 11/11/2026 — "Isola checkout Apple Sandbox do Codigo de amigo")
- **Gerado em:** 17/11/2026
- **Como:** modo "Prévia visual" do próprio app (`/preview-visual`, só roda em localhost). Ele bloqueia a rede e usa dados fictícios em memória. Nenhum login, Supabase ou RevenueCat foi usado.
- **Formato:** iPhone 15. Tela de 393×852 pt a 3x, ou seja 1179×2556 px. Barra de status limpa (9:41) e home indicator desenhados por cima. Os controles que só existem na prévia (botão DEV, selo "dados fictícios", chips de cenário, "Testar onboarding", "Só prévia", dicas do tutorial) foram escondidos.
- **Dados:** moto fictícia "Moto de demonstração" (Honda CG 160 Fan 2022, 18.400 km). Também aparecem a "Segunda moto" (CB 300F Twister ABS 2024) e a conta "Conta de demonstração / usuario@exemplo.com", placa "EXEMPLO". Não há dado pessoal real.

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
