#!/usr/bin/env python3
"""Mesa de Demandas: aplica a cobrança em escada e gera agencia/demandas/quadro.json.
Uso: python3 scripts/quadro_demandas.py   (rodar da raiz do repositório)"""
import json, glob, os, datetime as dt

TZ = dt.timezone(dt.timedelta(hours=-3))
now = dt.datetime.now(TZ)
ABERTOS = {"aberta", "em_andamento", "devolvida"}
ITENS = "agencia/demandas/itens"

def parse(s):
    try:
        d = dt.datetime.fromisoformat(s)
        return d if d.tzinfo else d.replace(tzinfo=TZ)
    except Exception:
        return None

livro = json.load(open("agencia/merito/livro.json"))
nomes = {a["id"]: a.get("nome", a["id"]) for a in livro["agentes"]}
setor_dir = {}
for a in livro["agentes"]:
    if a.get("tipo") == "diretor":
        setor_dir[a.get("setor")] = a["id"]
diretor_de = {a["id"]: setor_dir.get(a.get("setor"), "master") for a in livro["agentes"]}

itens = []
for f in sorted(glob.glob(f"{ITENS}/*.json")):
    try:
        d = json.load(open(f))
    except Exception as e:
        print("ignorado (JSON inválido):", f, e); continue
    prazo = parse(d.get("prazo", ""))
    atrasada = bool(prazo and d.get("status") in ABERTOS and now > prazo)
    if atrasada:
        horas = (now - prazo).total_seconds() / 3600
        nivel = 1 if horas < 24 else 2 if horas < 48 else 3
        if nivel > d.get("cobrancas", 0):
            quem = {1: d["para"], 2: diretor_de.get(d["para"], "master"), 3: "master"}[nivel]
            d["cobrancas"] = nivel
            d.setdefault("historico", []).append({"quando": now.isoformat(timespec="minutes"), "quem": "mesa-de-demandas",
                "o_que": f"cobrança {nivel}: prazo vencido há {int(horas)} h; cobrado {nomes.get(quem, quem)}"})
            if nivel >= 2:
                cp = d.setdefault("copia", [])
                dirp = diretor_de.get(d["para"], "master")
                if dirp not in cp: cp.append(dirp)
            if nivel == 3 and "master" not in d["copia"]: d["copia"].append("master")
            d["atualizada_em"] = now.isoformat(timespec="minutes")
            json.dump(d, open(f, "w"), ensure_ascii=False, indent=1)
    d["_atrasada"] = atrasada
    d["_de_nome"] = nomes.get(d.get("de"), d.get("de"))
    d["_para_nome"] = nomes.get(d.get("para"), d.get("para"))
    itens.append(d)

ordem = {"P1": 0, "P2": 1, "P3": 2}
itens.sort(key=lambda d: (not d["_atrasada"], d.get("status") not in ABERTOS, ordem.get(d.get("prioridade"), 3), d.get("prazo", "")))
res = {
    "abertas": sum(d.get("status") in ABERTOS for d in itens),
    "atrasadas": sum(d["_atrasada"] for d in itens),
    "entregues": sum(d.get("status") == "entregue" for d in itens),
    "aceitas": sum(d.get("status") == "aceita" for d in itens),
    "bloqueadas_lider": sum(d.get("status") == "bloqueada" and d.get("bloqueio") == "lider" for d in itens),
}
json.dump({"atualizado": now.isoformat(timespec="minutes"), "resumo": res, "demandas": itens}, open("agencia/demandas/quadro.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False))
