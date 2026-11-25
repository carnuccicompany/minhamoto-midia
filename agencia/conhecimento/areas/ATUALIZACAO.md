# Biblioteca dos diretores: índice e atualização semanal

Regra do Léo (24/11/2026): todo agente é especialista sênior da área dele e se mantém atualizado.

## Índice
| Setor | Pasta | Quem lê |
|---|---|---|
| Direção-geral e jurídico | `direcao-geral/` | Shelby, Moneypenny, Ness |
| Dados e finanças | `dados-financas/` | Turing, Hemingway |
| Tráfego | `trafego/` | Escobar |
| Criativos e marketing | `criativos/` | Disney, Fogg, Estúdio Audiovisual |
| Produto | `produto/` | Stark, Jobs |
| Lojas e clientes | `lojas/` | Bezos, Ted Lasso |
| Mercado e concorrência | `mercado/` | Greco, Sun Tzu |
| Infoprodutos (Corretores) | `infoprodutos/` | Cardone |

Cada pasta tem 3 camadas (regra do Léo, 24/11; estrutura criada em 25/11):
- **NUCLEO.md (ler em TODA tarefa, até ~6 mil caracteres):** as regras que mais mexem em venda, correções do Léo, lições e novidades recentes, índice.
- **FUNDAMENTOS.md + `aulas/AAAA-MM-DD-tema.md` (completo, sem limite):** todo o conhecimento; buscar com `grep -ril "<tema>"` só no que tocar a tarefa.
- **NOVIDADES.md e LICOES.md (histórico completo, com data e prova; nada se apaga, o muito antigo é resumido no fim).**
- **FONTES.md:** onde buscar (oficial primeiro).

Treino diário do professor-chefe: 3 setores por rodada pelo `rodizio.json`; registro em `treinos.md`.

## Texto pronto da tarefa semanal (ainda NÃO criada; o QG cria com o OK do Léo)

Nome: `MM: Atualização dos diretores` · Toda terça às 6h23 (America/Sao_Paulo) · Modelo padrão · Sem notificação, exceto decisão do Léo.

```
Você é o bibliotecário da Carnucci (app de assinatura MinhaMoto e infoprodutos para corretores). Missão da empresa: vender muito, pra muita gente, e sempre vender mais. Trabalhe em português, sozinho, sem pedir nada a ninguém.

1. Garanta acesso ao repositório carnuccicompany/minhamoto-midia (add_repo access=push) e clone-o. Leia agencia/conhecimento/areas/ATUALIZACAO.md e, para cada setor, FONTES.md e NOVIDADES.md.
2. Para cada setor, pesquise o que mudou nos últimos 7 dias, começando pelas fontes oficiais do FONTES.md (WebSearch/WebFetch). Só entra fato com link e data de publicação. Blog de agência é pista: só entra se confirmado na fonte oficial, e marcado como tal.
3. Atualize NOVIDADES.md de cada setor: item novo no topo com data, o que é, "O que muda pra nós" (aplicado à Carnucci) e fonte. Mantenha só os últimos 90 dias; o que sair da janela e ainda valer vira uma linha em "Vigente" ou entra no FUNDAMENTOS.md da área.
4. Se uma novidade muda uma regra em uso (política de anúncio, diretriz de loja, preço de ferramenta, prazo legal, lei), abra demanda para o diretor da área no formato de agencia/demandas/README.md (P1 se tiver prazo em até 30 dias), dizendo o que muda e o prazo.
5. Fonte nova e confiável encontrada? Acrescente no FONTES.md da área.
6. Repositório público: nada de R$ da empresa, número absoluto de assinantes, chave, e-mail ou dado de cliente. Rode scripts/vigia_segredos.py. Commit e push (git pull --rebase antes; nunca force-push). Nunca publique nada, nunca mexa em campanha, dinheiro, no app (minhamotooficial) ou em chaves.
7. MENSAGEM FINAL: responda só "Sem novidade." A única exceção é novidade que exige decisão do Léo/Davi com prazo curto (ex.: aceitar contrato da Apple, prazo de loja que trava envio): aí até 3 linhas com a decisão, a recomendação e o prazo; a mesma decisão vai como demanda com "bloqueio": "lider" para entrar no Bilhete das 9h.
```
