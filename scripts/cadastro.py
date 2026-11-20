#!/usr/bin/env python3
"""Cadastro 100%: junta o que confere sozinho com agencia/cadastro/itens.json e grava agencia/cadastro/status.json."""
import json, os, re, datetime
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = lambda p: json.load(open(os.path.join(R, p), encoding='utf-8'))
base = J('agencia/cadastro/itens.json')
livro = J('agencia/merito/livro.json')
metas = J('agencia/merito/metas.json')
cats = []

def val(it):
    s = it.get('status')
    return 1.0 if s == 'feito' else float(it.get('parcial', 0.5)) if s == 'parcial' else 0.0

# itens manuais (+ meta automática)
for key in ['estrutura', 'decisoes', 'conexoes']:
    c = base['categorias'][key]; itens = []
    for it in c['itens']:
        it = dict(it)
        if it['id'] == 'meta':
            ok = metas.get('pct') is not None or not str(metas.get('status', '')).startswith('aguardando')
            it['status'] = 'feito' if ok else 'pendente'
        it['valor'] = val(it); itens.append(it)
    cats.append({'id': key, 'nome': c['nome'], 'peso': c['peso'], 'itens': itens})

# agentes ativos: memória e playbook existem (30%), modelo definido (20%), lapidado com o Léo (50%)
itens = []
for a in livro['agentes']:
    if a.get('status', 'ativo') != 'ativo': continue
    mem = a.get('memoria') or f"agencia/memoria/agentes/{a['id'].replace(':', '-')}.md"
    v = 0.0; falta = []
    if os.path.exists(os.path.join(R, mem)) and a.get('playbook') and os.path.exists(os.path.join(R, a['playbook'])): v += 0.3
    else: falta.append('memória/playbook')
    if a.get('modelo'): v += 0.2
    else: falta.append('modelo')
    if a.get('lapidado'): v += 0.5
    else: falta.append('lapidar com o Léo')
    itens.append({'id': a['id'], 'titulo': f"{a['nome']} — {a.get('cargo', '')} · {a.get('setor', '')}", 'valor': round(v, 2),
                  'status': 'feito' if v >= 1 else 'parcial' if v > 0 else 'pendente', 'falta': falta})
cats.append({'id': 'agentes', 'nome': 'Agentes com função, cargo e cobrança', 'peso': 30, 'itens': itens})

# base de conhecimento: fatos preenchidos e perguntas respondidas
itens = []
for f in sorted(os.listdir(os.path.join(R, 'agencia/conhecimento'))):
    if not re.match(r'\d\d-.*\.md$', f): continue
    t = open(os.path.join(R, 'agencia/conhecimento', f), encoding='utf-8').read()
    fatos = t.split('## Fatos', 1)[-1].split('## Perguntas', 1)[0].strip()
    feitas, total = t.count('- [x]'), t.count('- [x]') + t.count('- [ ]')
    v = (0.0 if fatos in ('', '(vazio)') else 0.4) + (0.6 * feitas / total if total else 0.6 if fatos not in ('', '(vazio)') else 0)
    titulo = t.splitlines()[0].lstrip('# ').strip()
    itens.append({'id': f[:-3], 'titulo': titulo, 'valor': round(v, 2), 'status': 'feito' if v >= 0.99 else 'parcial' if v > 0 else 'pendente', 'falta': [] if v >= 0.99 else [f'{total - feitas} perguntas pro Léo']})
cats.append({'id': 'conhecimento', 'nome': 'Base de conhecimento', 'peso': 20, 'itens': itens})

total = 0.0
for c in cats:
    c['pct'] = round(100 * sum(i['valor'] for i in c['itens']) / max(1, len(c['itens'])), 1)
    c['feitos'] = sum(1 for i in c['itens'] if i['valor'] >= 1); c['total'] = len(c['itens'])
    total += c['pct'] * c['peso'] / 100
pend = [{'categoria': c['nome'], 'titulo': i['titulo'], 'falta': i.get('falta') or ([i['depende']] if i.get('depende') else [])} for c in cats for i in c['itens'] if i['valor'] < 1]
out = {'atualizado': datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3))).strftime('%d/%m/%Y %H:%M'), 'pct': round(total, 1), 'categorias': cats, 'pendentes': len(pend), 'lista_pendentes': pend}
os.makedirs(os.path.join(R, 'agencia/cadastro'), exist_ok=True)
hp = os.path.join(R, 'agencia/cadastro/historico.json')
hist = json.load(open(hp, encoding='utf-8')) if os.path.exists(hp) else []
dia = out['atualizado'][:10]
hist = [h for h in hist if h['data'] != dia] + [{'data': dia, 'pct': out['pct']}]
json.dump(hist, open(hp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
out['historico'] = hist[-60:]
json.dump(out, open(os.path.join(R, 'agencia/cadastro/status.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f"Cadastro: {out['pct']}% · {out['pendentes']} pendências")
for c in cats: print(f"  {c['nome']}: {c['pct']}% ({c['feitos']}/{c['total']})")
