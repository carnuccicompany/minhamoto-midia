#!/usr/bin/env python3
"""Vigia de segredos: procura chave/token nos arquivos do repositório PÚBLICO.
Uso: python3 scripts/vigia_segredos.py  → sai com código 1 e lista arquivo:linha (sem mostrar o valor) se achar algo.
Rodar antes de todo commit e em toda rodada do Coordenador."""
import os, re, subprocess, sys
PADROES = {
    'token da Meta (EAA...)': r'EAA[A-Za-z0-9]{30,}',
    'access_token em URL': r'access_token=[A-Za-z0-9_\-]{20,}',
    'chave do RevenueCat (sk_)': r'\bsk_[A-Za-z0-9]{20,}',
    'chave do Google (AIza)': r'AIza[0-9A-Za-z_\-]{30,}',
    'token do GitHub': r'gh[pousr]_[A-Za-z0-9]{30,}',
    'chave privada': r'-----BEGIN (?:EC |RSA )?PRIVATE KEY-----\s*[A-Za-z0-9+/]{40,}',
    'chave da OpenAI/Anthropic': r'\bsk-(?:ant-)?[A-Za-z0-9\-_]{30,}',
}
arquivos = subprocess.run(['git', 'ls-files'], capture_output=True, text=True).stdout.split()
achados = []
for f in arquivos:
    if f.endswith(('.png', '.jpg', '.jpeg', '.mp4', '.mov', '.webp', '.ttf', '.otf', '.woff', '.woff2', '.gif', '.pdf', '.zip')): continue
    try: texto = open(f, encoding='utf-8', errors='ignore').read()
    except Exception: continue
    for nome, pad in PADROES.items():
        for m in re.finditer(pad, texto):
            achados.append(f"{f}:{texto[:m.start()].count(chr(10)) + 1} · {nome}")
if achados:
    print('🚨 POSSÍVEL SEGREDO NO REPOSITÓRIO PÚBLICO:'); print('\n'.join(achados[:50])); sys.exit(1)
print('ok: nenhum segredo encontrado')
