#!/usr/bin/env python3
"""Vigia do insights diário (D-20261124-dados-4).
Uso: python3 scripts/vigia_insights.py [--agora 2026-11-25T09:30:00Z]
Imprime JSON {"linha": ..., "alerta": bool, ...} pro Coordenador copiar em status.json ("insights_diario").
Regra: o cron do insights.yml (02:41 UTC = 23h41 BRT) grava dados/insights-<data UTC>.json.
Se o arquivo da data UTC de hoje não existir até 09:00 UTC (06h BRT), vira alerta. Arquivo com 'erros' não vazio também é alerta.
Não imprime nenhum valor de métrica, só data, hora e nomes dos erros."""
import datetime, glob, json, os, re, sys
UTC = datetime.timezone.utc
BRT = datetime.timezone(datetime.timedelta(hours=-3))
agora = datetime.datetime.now(UTC)
if '--agora' in sys.argv:
    agora = datetime.datetime.fromisoformat(sys.argv[sys.argv.index('--agora') + 1].replace('Z', '+00:00'))
raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
arqs = sorted(f for f in glob.glob(os.path.join(raiz, 'dados', 'insights-*.json')) if re.search(r'insights-\d{4}-\d{2}-\d{2}\.json$', f))
hoje = agora.date().isoformat()
out = {'data_utc_hoje': hoje, 'alerta': False}
ultimo = arqs[-1] if arqs else None
if ultimo:
    d = json.load(open(ultimo, encoding='utf-8'))
    data = re.search(r'insights-(\d{4}-\d{2}-\d{2})', ultimo).group(1)
    col = datetime.datetime.fromisoformat(d.get('coletado_em', '').replace('Z', '+00:00')) if d.get('coletado_em') else None
    erros = d.get('erros') or {}
    out.update(ultimo_arquivo=f'dados/insights-{data}.json', coletado_em_brt=col.astimezone(BRT).isoformat(timespec='minutes') if col else None, erros=sorted(erros) if isinstance(erros, dict) else [str(erros)])
else:
    data = None; out.update(ultimo_arquivo=None, erros=[])
partes = []
if data != hoje:
    if agora.hour >= 9:
        out['alerta'] = True; partes.append(f'ALERTA: falta dados/insights-{hoje}.json (último: {data}); passou das 06h BRT')
    else:
        partes.append(f'aguardando o cron das 23h41 BRT (arquivo de {hoje} ainda não saiu; último: {data})')
else:
    partes.append(f'arquivo de hoje ({hoje}) existe')
if out['erros']:
    out['alerta'] = True; partes.append('ALERTA: erros na coleta: ' + ', '.join(out['erros']))
elif ultimo:
    partes.append('erros vazio')
if ultimo:
    partes.insert(0, f"último {os.path.basename(ultimo)} coletado {out['coletado_em_brt']} BRT")
out['linha'] = ' · '.join(partes)
print(json.dumps(out, ensure_ascii=False))
