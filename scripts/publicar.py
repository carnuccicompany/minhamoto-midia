"""Publica o próximo carrossel da fila no Instagram e no Facebook pela Graph API da Meta.

Variáveis de ambiente (segredos do repositório):
  META_TOKEN   token de página (longa duração) OU token de usuário do sistema (nunca expira) com
               instagram_content_publish, pages_manage_posts, pages_show_list, pages_read_engagement.
               Se for de usuário do sistema, o script troca sozinho pelo token da Página (sem gravar em lugar nenhum).
  IG_USER_ID   opcional (padrão: @minhamotoapp)
  FB_PAGE_ID   opcional (padrão: página MinhaMoto)
Opcional: GRAPH_VERSION (padrão v27.0), REDES (padrão "ig,fb"), SIMULAR=1 (não publica)
"""
import json, os, sys, time, urllib.parse, urllib.request
from datetime import datetime, timezone

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.environ.get("GITHUB_REPOSITORY", "carnuccicompany/minhamoto-midia")
BRANCH = os.environ.get("GITHUB_REF_NAME", "main")
RAW = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/"
V = os.environ.get("GRAPH_VERSION", "v27.0")
API = f"https://graph.facebook.com/{V}/"
TOKEN = os.environ.get("META_TOKEN", "")
IG = os.environ.get("IG_USER_ID") or "17841478100957290"
FB = os.environ.get("FB_PAGE_ID") or "1319425834577827"
REDES = [r.strip() for r in os.environ.get("REDES", "ig,fb").split(",") if r.strip()]
SIMULAR = os.environ.get("SIMULAR") == "1"
FORCAR = os.environ.get("FORCAR") == "1"  # execução manual: publica o próximo sem olhar horário
HORARIOS = [12, 15, 18, 21]  # horário de Brasília
JANELA_H = 2  # se o GitHub atrasar, ainda publica até 2h depois do horário


def chamar(metodo, caminho, dados=None):
    dados = dict(dados or {})
    dados["access_token"] = TOKEN
    corpo = urllib.parse.urlencode(dados).encode()
    url = API + caminho
    if metodo == "GET":
        req = urllib.request.Request(url + "?" + corpo.decode())
    else:
        req = urllib.request.Request(url, data=corpo, method=metodo)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        erro = e.read().decode(errors="replace")
        raise RuntimeError(f"{metodo} {caminho} -> {e.code}: {erro}") from None


def publicar_ig(post):
    filhos = []
    for c in post["cards"]:
        r = chamar("POST", f"{IG}/media", {"image_url": RAW + c, "is_carousel_item": "true"})
        filhos.append(r["id"])
    if len(filhos) == 1:
        raise RuntimeError("carrossel precisa de 2 ou mais imagens")
    cont = chamar("POST", f"{IG}/media", {"media_type": "CAROUSEL", "children": ",".join(filhos),
                                           "caption": post["legenda_ig_fb"]})["id"]
    for _ in range(30):
        st = chamar("GET", cont, {"fields": "status_code"}).get("status_code")
        if st == "FINISHED":
            break
        if st == "ERROR":
            raise RuntimeError("Instagram recusou o carrossel (status ERROR)")
        time.sleep(10)
    return chamar("POST", f"{IG}/media_publish", {"creation_id": cont})["id"]


def publicar_fb(post):
    ids = []
    for c in post["cards"]:
        r = chamar("POST", f"{FB}/photos", {"url": RAW + c, "published": "false"})
        ids.append(r["id"])
    dados = {"message": post["legenda_ig_fb"]}
    for n, i in enumerate(ids):
        dados[f"attached_media[{n}]"] = json.dumps({"media_fbid": i})
    return chamar("POST", f"{FB}/feed", dados)["id"]


def token_da_pagina():
    """Com token de usuário do sistema, pede à Meta o token da Página (não grava, não imprime)."""
    global TOKEN
    try:
        r = chamar("GET", FB, {"fields": "access_token"})
        if r.get("access_token"):
            TOKEN = r["access_token"]
    except Exception:
        pass  # já é token de página: segue com ele


def main():
    fila = json.load(open(os.path.join(RAIZ, "fila/carrosseis.json"), encoding="utf-8"))
    caminho_estado = os.path.join(RAIZ, "fila/estado.json")
    estado = json.load(open(caminho_estado, encoding="utf-8"))
    pub = estado.setdefault("publicados", {})
    from datetime import timedelta
    agora = datetime.now(timezone.utc) - timedelta(hours=3)
    slot = None
    for h in HORARIOS:
        inicio = agora.replace(hour=h, minute=0, second=0, microsecond=0)
        if inicio <= agora < inicio + timedelta(hours=JANELA_H):
            slot = inicio.strftime("%Y-%m-%d %H")
    if not FORCAR:
        if not slot:
            print("Fora de um horário de postagem. Nada a fazer.")
            return
        if slot in estado.get("horarios_feitos", []):
            print(f"Horário {slot} já publicado.")
            return
    if estado.get("pausado"):
        print("Fila pausada em fila/estado.json. Nada a fazer.")
        return
    proximo = next((p for p in fila if not all(r in pub.get(p["id"], {}) for r in REDES)), None)
    if not proximo:
        print("Fila vazia: todos os carrosséis já foram publicados.")
        return
    print(f"Próximo: {proximo['id']} · {proximo['titulo']} ({len(proximo['cards'])} cards)")
    if SIMULAR:
        print("SIMULAR=1: nada publicado.")
        return
    if not (TOKEN and IG and FB):
        print("Segredos META_TOKEN / IG_USER_ID / FB_PAGE_ID ainda não configurados.")
        return
    token_da_pagina()
    reg = pub.setdefault(proximo["id"], {})
    falhas = []
    for rede, fn in (("ig", publicar_ig), ("fb", publicar_fb)):
        if rede not in REDES or rede in reg:
            continue
        try:
            reg[rede] = {"id": fn(proximo), "em": datetime.now(timezone.utc).isoformat(timespec="seconds")}
            print(f"OK {rede}: {reg[rede]['id']}")
        except Exception as e:
            falhas.append(f"{rede}: {e}")
            print(f"FALHA {rede}: {e}", file=sys.stderr)
    if not reg:
        pub.pop(proximo["id"], None)
    elif slot:
        feitos = estado.setdefault("horarios_feitos", [])
        if slot not in feitos:
            feitos.append(slot)
        estado["horarios_feitos"] = feitos[-60:]
    json.dump(estado, open(caminho_estado, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if falhas:
        sys.exit(1)


if __name__ == "__main__":
    main()
