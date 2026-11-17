"""Avaliações das lojas (App Store + Google Play).
Modo listar: busca as avaliações recentes e grava dados/avaliacoes/ultimas.json
(sem nome do autor). Não responde nada. Testa também se as chaves funcionam.
Segredos: GOOGLE_PLAY_SA_JSON, ASC_ISSUER_ID, ASC_KEY_ID, ASC_PRIVATE_KEY."""
import json, os, sys, time, datetime
import requests, jwt
from google.oauth2 import service_account
from google.auth.transport.requests import Request

PLAY_PKG = "com.carnuccicompany.minhamoto"
APPLE_APP_ID = "6815447825"
OUT = "dados/avaliacoes/ultimas.json"

def play():
    raw = os.environ.get("GOOGLE_PLAY_SA_JSON", "").strip().lstrip("\ufeff")
    if not raw.startswith("{"):
        import base64
        try: raw = base64.b64decode(raw).decode()
        except Exception: pass
    diag("GOOGLE_PLAY_SA_JSON", raw, "{", "}")
    info = json.loads(raw)
    cred = service_account.Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/androidpublisher"])
    cred.refresh(Request())
    url = f"https://androidpublisher.googleapis.com/androidpublisher/v3/applications/{PLAY_PKG}/reviews"
    r = requests.get(url, headers={"Authorization": f"Bearer {cred.token}"},
                     params={"maxResults": 100, "translationLanguage": "pt-BR"}, timeout=30)
    r.raise_for_status()
    out = []
    for rv in r.json().get("reviews", []):
        cs = [c for c in rv.get("comments", [])]
        u = next((c["userComment"] for c in cs if "userComment" in c), {})
        d = next((c["developerComment"] for c in cs if "developerComment" in c), None)
        out.append({"loja": "google_play", "id": rv["reviewId"], "nota": u.get("starRating"),
                    "texto": (u.get("text") or "").strip(),
                    "data": datetime.datetime.utcfromtimestamp(int(u.get("lastModified", {}).get("seconds", 0))).isoformat() + "Z",
                    "versao_app": u.get("appVersionName"), "aparelho": (u.get("deviceMetadata") or {}).get("productName"),
                    "respondida": bool(d), "resposta_atual": d.get("text") if d else None})
    return out

def diag(nome, v, ini, fim):
    # diagnóstico sem revelar o segredo: só tamanho e se começa/termina como esperado
    print(f"[diag] {nome}: {len(v)} caracteres; começa certo={v.startswith(ini)}; termina certo={v.endswith(fim)}")

def pem():
    import re, textwrap
    v = os.environ.get("ASC_PRIVATE_KEY", "").strip().lstrip("\ufeff").replace("\\n", "\n")
    diag("ASC_PRIVATE_KEY", v, "-----BEGIN PRIVATE KEY-----", "-----END PRIVATE KEY-----")
    body = re.sub(r"-----(BEGIN|END) [A-Z ]*PRIVATE KEY-----", "", v)
    body = re.sub(r"[^A-Za-z0-9+/=]", "", body)
    print(f"[diag] corpo base64 da chave: {len(body)} caracteres (esperado ~200)")
    return "-----BEGIN PRIVATE KEY-----\n" + "\n".join(textwrap.wrap(body, 64)) + "\n-----END PRIVATE KEY-----\n"

def apple_token():
    now = int(time.time())
    return jwt.encode({"iss": os.environ["ASC_ISSUER_ID"], "iat": now, "exp": now + 1200, "aud": "appstoreconnect-v1"},
                      pem(), algorithm="ES256",
                      headers={"kid": os.environ["ASC_KEY_ID"].strip(), "typ": "JWT"})

def apple():
    h = {"Authorization": f"Bearer {apple_token()}"}
    url = f"https://api.appstoreconnect.apple.com/v1/apps/{APPLE_APP_ID}/customerReviews"
    r = requests.get(url, headers=h, params={"sort": "-createdDate", "limit": 200, "include": "response"}, timeout=30)
    r.raise_for_status()
    j = r.json()
    resp = {i["id"]: i for i in j.get("included", []) if i["type"] == "customerReviewResponses"}
    out = []
    for rv in j.get("data", []):
        a = rv["attributes"]
        rel = (rv.get("relationships", {}).get("response", {}) or {}).get("data")
        rr = resp.get(rel["id"]) if rel else None
        out.append({"loja": "app_store", "id": rv["id"], "nota": a.get("rating"),
                    "titulo": a.get("title"), "texto": (a.get("body") or "").strip(),
                    "data": a.get("createdDate"), "pais": a.get("territory"),
                    "respondida": bool(rr), "resposta_atual": rr["attributes"].get("responseBody") if rr else None})
    return out

if __name__ == "__main__":
    res = {"coletado_em": datetime.datetime.utcnow().isoformat() + "Z", "status": {}, "avaliacoes": []}
    for nome, f in (("google_play", play), ("app_store", apple)):
        try:
            a = f(); res["avaliacoes"] += a; res["status"][nome] = f"ok ({len(a)} avaliações)"
        except Exception as e:
            msg = str(e)
            if hasattr(e, "response") and e.response is not None: msg += " | " + e.response.text[:300]
            res["status"][nome] = "ERRO: " + msg
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(res, open(OUT, "w"), ensure_ascii=False, indent=1)
    print(json.dumps(res["status"], ensure_ascii=False))
