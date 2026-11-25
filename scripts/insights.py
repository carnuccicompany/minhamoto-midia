#!/usr/bin/env python3
"""Coleta métricas IG/FB pela Graph API e salva em dados/insights-<data>.json.
Roda no GitHub Actions (workflow insights.yml) com META_TOKEN. Tolerante a falha:
coleta o que conseguir e registra os erros no próprio JSON."""
import json, os, urllib.request, urllib.parse, datetime

V = 'v27.0'
IG = os.environ.get('IG_ID', '17841478100957290')
PAGE = os.environ.get('PAGE_ID', '1319425834577827')
TOKEN = os.environ['META_TOKEN']
try:  # token de usuário do sistema -> token da Página (não grava, não imprime)
    import urllib.request as _u, json as _j
    _r = _j.loads(_u.urlopen('https://graph.facebook.com/v21.0/' + (os.environ.get('FB_PAGE_ID') or '1319425834577827') + '?fields=access_token&access_token=' + TOKEN, timeout=60).read())
    TOKEN = _r.get('access_token') or TOKEN
except Exception:
    pass

def get(path, **params):
    params['access_token'] = TOKEN
    url = f'https://graph.facebook.com/{V}/{path}?' + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)

out = {'coletado_em': datetime.datetime.utcnow().isoformat() + 'Z', 'erros': {}}

def erro_txt(e, n=300):
    # Inclui a mensagem da Meta (corpo do HTTP 400) para saber a causa real
    # (permissão do token, métrica inválida etc.). O corpo não contém o token.
    txt = str(e)
    if hasattr(e, 'read'):
        try:
            txt += ' | ' + e.read().decode('utf-8', 'replace')
        except Exception:
            pass
    return txt[:n]

def tenta(nome, fn):
    try:
        out[nome] = fn()
    except Exception as e:
        out['erros'][nome] = erro_txt(e)

tenta('ig_conta', lambda: get(IG, fields='followers_count,media_count,username'))
tenta('ig_alcance_28d', lambda: get(f'{IG}/insights', metric='reach', period='days_28'))

def ig_midias():
    r = get(f'{IG}/media', fields='id,caption,timestamp,media_product_type,like_count,comments_count', limit='60')
    midias = r.get('data', [])
    for m in midias:
        try:
            ins = get(f"{m['id']}/insights", metric='reach,saved,shares,total_interactions')
            m['insights'] = {d['name']: d['values'][0]['value'] for d in ins.get('data', [])}
        except Exception as e:
            m['insights_erro'] = erro_txt(e, 400)
        if m.get('caption'):
            m['caption'] = m['caption'][:120]
    return midias

tenta('ig_midias', ig_midias)
tenta('fb_pagina', lambda: get(PAGE, fields='fan_count,followers_count,name'))
# page_impressions foi descontinuada pela Meta (blog dev 15/08/2025): usa page_media_view
tenta('fb_impressoes', lambda: get(f'{PAGE}/insights', metric='page_media_view,page_post_engagements', period='week'))

def ig_alcance_formato():
    # Meta: breakdown só com metric_type=total_value (doc oficial). 28 dias fechados, UTC.
    # Grava só total e por_formato (nunca a resposta crua). Aprovado pelo Shelby em 24/11
    # (D-20261123-dados_relatorio-semanal-1); só leitura, dentro de tenta().
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

def sem_paging(o):
    # NUNCA gravar 'paging': as URLs de paginação da Meta trazem o access_token
    # e este repositório é público (vazamento em 23/11/2026).
    if isinstance(o, dict):
        o.pop('paging', None)
        for v in o.values():
            sem_paging(v)
    elif isinstance(o, list):
        for v in o:
            sem_paging(v)
    return o

sem_paging(out)
texto = json.dumps(out, ensure_ascii=False)
assert 'access_token' not in texto and TOKEN not in texto, 'token no JSON: abortado'

hoje = datetime.date.today().isoformat()
os.makedirs('dados', exist_ok=True)
with open(f'dados/insights-{hoje}.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print('salvo dados/insights-%s.json | erros: %s' % (hoje, list(out['erros']) or 'nenhum'))
