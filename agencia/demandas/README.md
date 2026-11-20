# Mesa de Demandas (decisão do Léo, 20/11/2026)

Os agentes **criam demandas uns pros outros, passam o trabalho adiante e se cobram**. Ninguém espera ordem do Léo pra se mexer: quem enxerga uma coisa que faz a empresa vender mais, pede pra quem sabe fazer, com prazo. Quem recebe, entrega. Quem pediu, confere. Quem atrasa, é cobrado.

## Uma demanda = um arquivo
`agencia/demandas/itens/<id>.json`. O id é `D-AAAAMMDD-<criador>-<n>` (troque `:` por `_`), assim duas IAs nunca criam o mesmo id.

```json
{
  "id": "D-20261120-trafego-1",
  "de": "trafego",
  "para": "cria:roteirista",
  "copia": ["cria"],
  "titulo": "3 ganchos novos pro criativo de troca de óleo",
  "por_que": "CTR do conjunto caiu 18% em 7 dias (fonte: dados/relatorios/...); sem gancho novo a meta da semana não fecha",
  "pronto_quando": "3 ganchos de até 8 palavras, cada um com a referência que inspirou, num arquivo em agencia/demandas/entregas/",
  "prioridade": "P1",
  "prazo": "2026-11-21T18:00:00-03:00",
  "status": "aberta",
  "criada_em": "2026-11-20T19:40:00-03:00",
  "fio": "F-003",
  "entrega": null,
  "cobrancas": 0,
  "historico": [{"quando": "2026-11-20T19:40:00-03:00", "quem": "trafego", "o_que": "criou"}]
}
```

**Status:** `aberta` → `em_andamento` → `entregue` → `aceita` (fecha) ou `devolvida` (volta pra quem fez, com o motivo). Também: `recusada` (não é comigo, com motivo e pra quem deveria ir), `bloqueada` (falta algo; diz o quê e de quem) e `cancelada` (quem pediu desistiu, com motivo).

## Regras
- **Quem pede pra quem:** qualquer agente pede pra qualquer agente. Se for de outro setor, põe o diretor do setor em `copia`. Diretor pede pros seus subagentes à vontade.
- **Toda demanda tem `por_que` ligado à meta** (vender mais, com número ou fonte) e **`pronto_quando` verificável**. Sem isso, quem recebe pode recusar.
- **Anti-spam:** cada agente cria no máximo 3 demandas por rodada. Demanda que não serve pra nada é recusada e conta como ruído (−5 na Folha pra quem criou).
- **Prazo pela prioridade:** P1 = 24 h, P2 = 72 h, P3 = 7 dias (pode ser menor se a meta pedir).
- **Entrega:** o arquivo vai em `agencia/demandas/entregas/<id>.<ext>` (ou o lugar certo do repositório) e o caminho fica em `entrega.arquivo`, com um resumo de 2 linhas.
- **Conferência:** quem pediu aceita ou devolve em até 24 h, dizendo exatamente o que falta. Devolver sem motivo concreto é puxa-saquismo ao contrário: ruído.
- **Nada vai pro ar, nada gasta dinheiro e nada mexe no app** por causa de uma demanda. Precisa do Léo ou do Davi? Status `bloqueada` com `"bloqueio": "lider"` e a pergunta pronta, respondível com sim/não.

## Cobrança em escada (automática, feita pela Mesa de Demandas)
1. **Venceu o prazo:** cobrança 1 no histórico, aviso pra quem recebeu.
2. **24 h depois, ainda parada:** cobrança 2, o diretor de quem recebeu entra em cópia e a demanda vai pra pauta do Conselho.
3. **48 h depois:** cobrança 3, vai pro Shelby; na Folha conta como "cobrança sem resposta" (−5 pra quem deveria ter entregue; se for subagente, o diretor também responde).
- `bloqueada` com motivo real não é cobrada; quem bloqueia (o "de quem") é cobrado no lugar.

## Mérito
- Entrega aceita no prazo: +5 XP e C$ 5 pra quem fez (vale como "entregou no prazo sem refazer").
- Entrega que virou número comprovado: +10 pra quem fez e +5 pra quem pediu (pediu certo).
- Devolvida por erro de quem fez: conta como refação (−10) e erro pro broche.
- Quem cria demandas boas, que destravam venda, aparece no boletim em "o que produziu".

## Quadro
A Mesa de Demandas gera `agencia/demandas/quadro.json` (todas as demandas, atrasadas no topo). Painel: https://carnuccicompany.github.io/minhamoto-midia/demandas.html
