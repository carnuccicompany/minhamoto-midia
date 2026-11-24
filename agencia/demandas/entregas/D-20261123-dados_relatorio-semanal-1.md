# D-20261123-dados_relatorio-semanal-1: chamada de alcance 28d por formato (media_product_type)

Alan Turing (dados), 24/11/2026. Só leitura. Nada gravado em `dados/`, `scripts/insights.py` intocado, nenhum token usado ou citado.
**Status: bloqueada (lider). Não consegui testar a chamada: esta sessão não tem `META_TOKEN` (e não deve ter). Não afirmo que ela "retornou por_formato". Entrego o que dá sem token: doc oficial conferida, proposta do Hemingway revisada com ajustes, patch pronto e um teste de 1 comando que não grava nada.**

## 1. O que a doc oficial da Meta confirma (lida em 24/11)
Fonte: https://developers.facebook.com/docs/instagram-platform/api-reference/instagram-user/insights
- `reach` aceita `metric_type=total_value` e `time_series`, com breakdown `media_product_type` e `follow_type`.
- Valores de `media_product_type`: **AD, FEED, REELS, STORY**.
- Breakdown **só vale com `metric_type=total_value`**. Com `time_series` a Meta ignora o breakdown. Por isso a chamada atual (`period=days_28`) nunca vai trazer origem.
- `since` e `until` são timestamps Unix, intervalo inclusivo. Sem eles a Meta olha só as últimas 24 h.
- `reach` é marcado "estimada". Se uma consulta pede uma métrica sem suporte a breakdown, a Meta devolve erro.
- **A página não declara limite máximo da janela `since`/`until`.** Então "28 dias cabe" é hipótese, e é exatamente o que o teste responde. Se vier erro de janela, o ajuste é 2 chamadas de 14 dias, ou 4 de 7, somando; o alcance único não soma sem repetição, então só vale como ordem de grandeza.

## 2. Revisão da proposta do Hemingway (D-20261123-dados-4, seção 4)
A ideia está certa. Ajustes que eu faria antes de aceitar:
1. `until = agora` pode pedir dia incompleto. Usar **hoje 00:00 UTC** e `since = until - 28 dias` (28 dias fechados, repetível e comparável dia a dia).
2. Gravar só números: `total` e `por_formato` (dict formato -> valor). Nunca a resposta crua. O `sem_paging()` e o `assert` do script já protegem o JSON, mantidos.
3. Chamar dentro de `tenta()`: se a Meta recusar, a mensagem exata cai em `erros` e o resto da coleta segue (é o que já acontece com as outras chamadas).
4. A forma da resposta (`breakdowns[0].results[].dimension_values[0]` e `.value`) é de memória; **a doc não mostrou o exemplo**. O código usa `.get()` para não quebrar, mas só o teste confirma.
5. Reaproveitar a mesma chamada com `breakdown=follow_type` (seguidor x não seguidor) só depois que a primeira funcionar, em outra `tenta()`. Uma coisa por vez.

Patch proposto (colar **antes** de `sem_paging(out)` em `scripts/insights.py`; **não aplicado**):
```python
def ig_alcance_formato():
    # Meta: breakdown só com metric_type=total_value (doc oficial). 28 dias fechados, UTC.
    fim = int(datetime.datetime.combine(datetime.date.today(), datetime.time.min,
                                        tzinfo=datetime.timezone.utc).timestamp())
    ini = fim - 28 * 86400
    r = get(f'{IG}/insights', metric='reach', period='day', metric_type='total_value',
            breakdown='media_product_type', since=str(ini), until=str(fim))
    tv = r['data'][0]['total_value']
    res = (tv.get('breakdowns') or [{}])[0].get('results', [])
    return {'janela_dias': 28, 'total': tv.get('value'),
            'por_formato': {x['dimension_values'][0]: x['value'] for x in res}}
tenta('ig_alcance_28d_formato', ig_alcance_formato)
```

## 3. Como testar sem gravar em `dados/` (1 comando, por quem tem o token)
Salvar fora do repositório como `teste_formato.py` e rodar com o token do ambiente (o mesmo `META_TOKEN` do secret; **não colar o token em lugar nenhum**):
```python
import os, json, datetime, urllib.request, urllib.parse
IG = '17841478100957290'; T = os.environ['META_TOKEN']
fim = int(datetime.datetime.combine(datetime.date.today(), datetime.time.min, tzinfo=datetime.timezone.utc).timestamp())
q = dict(metric='reach', period='day', metric_type='total_value', breakdown='media_product_type',
         since=str(fim-28*86400), until=str(fim), access_token=T)
try:
    r = json.load(urllib.request.urlopen(f'https://graph.facebook.com/v27.0/{IG}/insights?'+urllib.parse.urlencode(q), timeout=60))
    tv = r['data'][0]['total_value']; print(json.dumps({'total': tv.get('value'), 'breakdowns': tv.get('breakdowns')}, ensure_ascii=False))
except Exception as e:
    print('ERRO', getattr(e,'code',''), e.read().decode()[:400] if hasattr(e,'read') else e)
```
A saída não contém o token (só total e breakdown, ou o erro da Meta). Colar a saída em `D-20261123-dados_relatorio-semanal-1` e eu fecho a leitura em %.
Alternativa mais barata: aplicar o patch da seção 2 e deixar a coleta das 23h41 de hoje responder. Como a chamada fica dentro de `tenta()`, o pior caso é uma linha a mais em `erros`.

## 4. Dado novo de hoje: o teto subiu, a pergunta continua
Fonte: `dados/insights-2026-11-24.json` (coleta 24/11 12h56 UTC, `erros` vazio).
- Alcance da conta em 28 dias: 6,3 vezes os seguidores (era 6,3 ontem). Variação de ontem para hoje: -0,4%.
- Os 59 posts listados são **todos FEED** (nenhum REELS). A soma do alcance deles é no máximo **9,9%** do alcance da conta (ontem 9,6%). Somar alcance por post superestima o alcance único, então isso é teto: **pelo menos 90% do alcance da conta não vem de post de feed.**
- `ig_midias` só lista feed e reels da conta. **Story e anúncio não entram nessa lista.** Há campanha da MinhaMoto na conta de anúncios (`conhecimento/07-canais.md`), então AD é a primeira hipótese; STORY a segunda. É hipótese: o breakdown decide.
- Por que importa pra vender: se o grosso for AD, o alcance orgânico real é bem menor que o que o placar sugere e o custo por assinante precisa ser lido por anúncio, não pela conta. Se for STORY, o formato que mais alcança não tem insight por post na nossa coleta e falta puxar `/stories`.

## 5. Decisão do Turing
- **Aceito a proposta do Hemingway com os 5 ajustes da seção 2.** Script só muda depois do teste ou do OK abaixo.
- Quem fecha: Léo ou Davi (token). Resposta sim/não abaixo.

## Pergunta (sim/não, com recomendação)
Davi (ou Léo): posso aplicar o patch da seção 2 em `scripts/insights.py` para a coleta das 23h41 de hoje trazer `por_formato` (ou o erro exato da Meta)? É só leitura, dentro de `tenta()`, não grava token e não derruba a coleta. **Recomendo: sim.**
