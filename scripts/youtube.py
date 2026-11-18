"""MinhaMoto Publicador — envio de YouTube Shorts para o canal oficial @minhamotoapp.

Ferramenta interna da Carnucci Co. LTDA. Não tem usuários externos: autentica por OAuth 2.0
com a conta Google da própria empresa (escopo youtube.upload) e envia, uma vez por dia, os
Shorts já aprovados pela equipe que estão na fila fila/shorts.json.

Uso:
  python3 scripts/youtube.py teste    # confere credenciais e mostra o canal (não envia nada)
  python3 scripts/youtube.py enviar   # envia o próximo Short aprovado da fila

Segredos (variáveis de ambiente, guardadas nos GitHub Secrets — nunca no código):
  YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN

Fluxo do envio (videos.insert com upload resumable):
  1. troca o refresh token por um access token (oauth2.googleapis.com/token)
  2. lê o próximo item com status "aprovado" em fila/shorts.json
  3. abre a sessão de upload (POST uploadType=resumable) com título, descrição, tags e privacidade
  4. envia o arquivo MP4 em partes de 8 MB, retomando em caso de queda
  5. grava o id do vídeo, a URL e a data em fila/shorts.json (status "publicado")
"""
import datetime
import json
import os
import pathlib
import sys
import time

import requests

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FILA = RAIZ / "fila" / "shorts.json"
TOKEN_URL = "https://oauth2.googleapis.com/token"
UPLOAD_URL = "https://www.googleapis.com/upload/youtube/v3/videos"
API = "https://www.googleapis.com/youtube/v3"
PARTE = 8 * 1024 * 1024  # 8 MB (múltiplo de 256 KB, exigência da API)
CATEGORIA_AUTOS = "2"     # Autos & Vehicles


def diag():
    """Mostra só tamanho/formato dos segredos, nunca o valor."""
    for n, ini in (("YT_CLIENT_ID", "644425422292-"), ("YT_CLIENT_SECRET", "GOCSPX-"), ("YT_REFRESH_TOKEN", "1//")):
        v = os.environ.get(n, "").strip()
        print(f"[diag] {n}: {len(v)} caracteres; começa certo={v.startswith(ini)}")


def access_token():
    r = requests.post(TOKEN_URL, data={
        "client_id": os.environ["YT_CLIENT_ID"].strip(),
        "client_secret": os.environ["YT_CLIENT_SECRET"].strip(),
        "refresh_token": os.environ["YT_REFRESH_TOKEN"].strip(),
        "grant_type": "refresh_token",
    }, timeout=30)
    if r.status_code != 200:
        print("ERRO ao obter token:", r.text[:300])
        sys.exit(1)
    return r.json()["access_token"]


def teste():
    diag()
    tk = access_token()
    h = {"Authorization": f"Bearer {tk}"}
    ti = requests.get("https://oauth2.googleapis.com/tokeninfo", params={"access_token": tk}, timeout=30).json()
    print("TOKEN OK · escopo:", ti.get("scope"), "· expira em", ti.get("expires_in"), "s")
    r = requests.get(f"{API}/channels", headers=h, params={"part": "snippet", "mine": "true"}, timeout=30)
    print("status", r.status_code)
    if r.ok:
        for c in r.json().get("items", []):
            print("CANAL:", c["id"], c["snippet"]["title"], c["snippet"].get("customUrl"))
    else:
        print(r.text[:400])


def ler_fila():
    if not FILA.exists():
        return []
    return json.loads(FILA.read_text(encoding="utf-8"))


def salvar_fila(itens):
    FILA.write_text(json.dumps(itens, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def metadados(item):
    titulo = item["titulo"].strip()
    if "#shorts" not in titulo.lower():
        titulo = f"{titulo} #Shorts"
    return {
        "snippet": {
            "title": titulo[:100],
            "description": item.get("descricao", "").strip()[:5000],
            "tags": item.get("tags", ["MinhaMoto", "moto", "manutenção de moto", "Shorts"])[:30],
            "categoryId": CATEGORIA_AUTOS,
            "defaultLanguage": "pt-BR",
            "defaultAudioLanguage": "pt-BR",
        },
        "status": {
            "privacyStatus": item.get("privacidade", "public"),
            "selfDeclaredMadeForKids": False,
            "embeddable": True,
        },
    }


def abrir_sessao(tk, arquivo, meta):
    r = requests.post(
        UPLOAD_URL,
        params={"uploadType": "resumable", "part": "snippet,status"},
        headers={
            "Authorization": f"Bearer {tk}",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Upload-Content-Type": "video/mp4",
            "X-Upload-Content-Length": str(arquivo.stat().st_size),
        },
        data=json.dumps(meta),
        timeout=60,
    )
    if r.status_code != 200 or "Location" not in r.headers:
        print("ERRO ao abrir sessão de upload:", r.status_code, r.text[:400])
        sys.exit(1)
    return r.headers["Location"]


def enviar_arquivo(tk, sessao, arquivo):
    total = arquivo.stat().st_size
    enviado = 0
    tentativas = 0
    with arquivo.open("rb") as f:
        while enviado < total:
            f.seek(enviado)
            pedaco = f.read(PARTE)
            fim = enviado + len(pedaco) - 1
            try:
                r = requests.put(sessao, data=pedaco, timeout=300, headers={
                    "Authorization": f"Bearer {tk}",
                    "Content-Length": str(len(pedaco)),
                    "Content-Range": f"bytes {enviado}-{fim}/{total}",
                })
            except requests.RequestException as e:
                r = None
                print("queda de conexão:", e)
            if r is not None and r.status_code in (200, 201):
                return r.json()
            if r is not None and r.status_code == 308:  # parte recebida, continua
                faixa = r.headers.get("Range")
                enviado = int(faixa.split("-")[1]) + 1 if faixa else 0
                tentativas = 0
                print(f"enviado {enviado}/{total} bytes")
                continue
            tentativas += 1
            if tentativas > 5 or (r is not None and r.status_code < 500 and r.status_code != 308):
                print("ERRO no upload:", None if r is None else (r.status_code, r.text[:400]))
                sys.exit(1)
            time.sleep(2 ** tentativas)
            st = requests.put(sessao, timeout=60, headers={
                "Authorization": f"Bearer {tk}", "Content-Range": f"bytes */{total}"})
            if st.status_code == 308:
                faixa = st.headers.get("Range")
                enviado = int(faixa.split("-")[1]) + 1 if faixa else 0
            elif st.status_code in (200, 201):
                return st.json()
    sys.exit("upload terminou sem resposta final")


def enviar():
    itens = ler_fila()
    item = next((i for i in itens if i.get("status") == "aprovado"), None)
    if not item:
        print("Nenhum Short aprovado na fila. Nada a enviar.")
        return
    arquivo = RAIZ / item["arquivo"]
    if not arquivo.exists():
        sys.exit(f"arquivo não encontrado: {arquivo}")
    diag()
    tk = access_token()
    meta = metadados(item)
    print("Enviando:", meta["snippet"]["title"], "·", arquivo.name, f"({arquivo.stat().st_size} bytes)")
    sessao = abrir_sessao(tk, arquivo, meta)
    video = enviar_arquivo(tk, sessao, arquivo)
    vid = video["id"]
    item.update({
        "status": "publicado",
        "youtube_id": vid,
        "url": f"https://youtube.com/shorts/{vid}",
        "publicado_em": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "privacidade_final": video.get("status", {}).get("privacyStatus"),
    })
    salvar_fila(itens)
    print("PUBLICADO:", item["url"], "· privacidade:", item["privacidade_final"])


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "teste"
    {"teste": teste, "enviar": enviar}.get(modo, teste)()
