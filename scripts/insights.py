#!/usr/bin/env python3
"""Coleta métricas IG/FB pela Graph API e salva em dados/insights-<data>.json.
Roda no GitHub Actions (workflow insights.yml) com META_TOKEN. Tolerante a falha:
coleta o que conseguir e registra os erros no próprio JSON."""
import json, os, urllib.request, urllib.parse, datetime

V = 'v27.0'
IG = os.environ.get('IG_ID', '17841478100957290')
PAGE = os.environ.get('PAGE_ID', '1319425834577827')
TOKEN = os.environ['META_TOKEN']

def get(path, **params):
    params['access_token'] = TOKEN
    url = f'https://graph.facebook.com/{V}/{path}?' + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)

out = {'coletado_em': datetime.datetime.utcnow().isoformat() + 'Z', 'erros': {}}

def tenta(nome, fn):
    try:
        out[nome] = fn()
    except Exception as e:
        out['erros'][nome] = str(e)[:300]

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
            m['insights_erro'] = str(e)[:150]
        if m.get('caption'):
            m['caption'] = m['caption'][:120]
    return midias

tenta('ig_midias', ig_midias)
tenta('fb_pagina', lambda: get(PAGE, fields='fan_count,followers_count,name'))
tenta('fb_impressoes', lambda: get(f'{PAGE}/insights', metric='page_impressions,page_post_engagements', period='week'))

hoje = datetime.date.today().isoformat()
os.makedirs('dados', exist_ok=True)
with open(f'dados/insights-{hoje}.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print('salvo dados/insights-%s.json | erros: %s' % (hoje, list(out['erros']) or 'nenhum'))
