# Placar de experimentos

> Criado em 23/11/2026. Tudo que a Carnucci testa (criativo, gancho, preço, página, oferta) fica registrado em `placar.json`, com uma variável por vez, pra saber o que ganhou e por quê. Sem isso, a empresa repete teste e esquece o que aprendeu.

## Formato de cada experimento (`placar.json`)
| Campo | O que é |
|---|---|
| `id` | EXP-AAAAMMDD-n |
| `produto` | `minhamoto` ou `corretores` |
| `tipo` | `criativo`, `gancho`, `preço`, `página` ou `oferta` |
| `hipotese` | o que a gente acha que vai acontecer e por quê |
| `variavel` | a ÚNICA coisa que muda no teste |
| `metrica` | o número que decide (ex.: CPA, % de visualização de página por clique, % do Completo nos pedidos) |
| `base` | o valor antes do teste, em % ou variação, com fonte |
| `inicio` / `fim` | datas |
| `status` | `planejado`, `rodando` ou `encerrado` |
| `resultado_pct` | resultado em % ou variação (**nunca R$ nem número absoluto**: absolutos ficam no repo privado carnucci-dados) |
| `vencedor` | qual variação ganhou (ou "inconclusivo") |
| `aprendizado` | o que vira regra (e vai pro DESIGN do produto, se for criativo) |
| `proximo_passo` | o que fazer com o resultado |
| `dono` | quem toca |

## Regras
- **Uma variável por vez.** Se mudou duas coisas, o resultado não ensina nada.
- **Só encerra com número e fonte** (UTMify, Meta, RevenueCat, AppsFlyer). O Turing é o fiscal.
- **Meta semanal: pelo menos 5 experimentos novos por semana**, somando MinhaMoto e Corretores *(decisão do Claude, a confirmar com o Léo)*.
- Aprendizado de criativo vira regra no `agencia/DESIGN-MINHAMOTO.md` ou no `agencia/DESIGN-CORRETORES.md`.

## Quem atualiza
- **Escobar (tráfego) e Turing (dados), na Mesa de Demandas:** abrem, acompanham e encerram os experimentos de anúncio e de funil com o número.
- **Shelby, no Fechamento da semana (sexta):** confere o placar, cobra os que estão sem número e conta se a meta de 5 novos por semana bateu.
