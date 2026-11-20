# Conectar tudo aos agentes (plano, 20/11/2026)

Objetivo do Léo: os agentes com acesso a tudo, o mais automatizado possível. Claude é o cérebro que interliga.

## Três caminhos, nesta ordem de preferência
1. **Conector oficial no claude.ai** (o Léo liga uma vez, todas as tarefas agendadas passam a usar).
2. **Robô de dados (GitHub Actions) puxando a API de cada serviço** todo dia e gravando num **repositório privado `carnucci-dados`** (número absoluto de assinante e receita nunca no repo público). As chaves ficam em GitHub Secrets, coladas pelo Léo; ninguém imprime nem lê chave.
3. **Tarefa presa ao notebook do Léo usando o Chrome dele**, só leitura, pro que não tem nem conector nem API.

## Serviço por serviço
| Serviço | Caminho | O que o Léo faz |
|---|---|---|
| TikTok Ads | Conector "TikTok for Business" (oficial) | Ligar no claude.ai |
| Meta Ads + Instagram | Conector agregador (Windsor.ai ou Supermetrics; serviços pagos de terceiros) **ou** robô com a Marketing API | Escolher um |
| RevenueCat | Robô: API v2 (Charts & Metrics: assinantes ativos, novos, trials, MRR). Existe também um servidor MCP oficial que usa token v2 | Criar chave v2 **só leitura** e colar no GitHub Secret |
| AppsFlyer | Robô: Pull API (instalações por fonte) | Colar o token da API no Secret |
| App Store Connect | Robô: API de vendas e analytics | Criar uma chave NOVA só pra dados (não mexer na "Codemagic MinhaMoto") |
| Google Play Console | Robô: Play Developer Reporting API com conta de serviço | Criar conta de serviço com acesso só a relatórios |
| UTMify | Não achei API de leitura (a chave dela é pra mandar vendas pra dentro) | Tarefa presa ao notebook lendo o painel, só leitura |

## Regras
- Começa tudo em **modo leitura**. Mexer em campanha, preço ou gastar dinheiro continua só com OK do Léo/Davi.
- Os agentes leem `carnucci-dados` (privado) e escrevem só % no repositório público.
