"""YouTube Shorts. Modo teste: confere se as credenciais funcionam (mostra o canal). Não envia nada.
Segredos: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN."""
import os, sys, json, requests
def token():
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": os.environ["YT_CLIENT_ID"].strip(), "client_secret": os.environ["YT_CLIENT_SECRET"].strip(),
        "refresh_token": os.environ["YT_REFRESH_TOKEN"].strip(), "grant_type": "refresh_token"}, timeout=30)
    if r.status_code != 200: print("ERRO token:", r.text[:300]); sys.exit(1)
    return r.json()["access_token"]
if __name__ == "__main__":
    tk = token(); h = {"Authorization": f"Bearer {tk}"}
    ti = requests.get("https://oauth2.googleapis.com/tokeninfo", params={"access_token": tk}, timeout=30).json()
    print("TOKEN OK · escopo:", ti.get("scope"), "· expira em", ti.get("expires_in"), "s")
    r = requests.get("https://www.googleapis.com/youtube/v3/channels", headers=h, params={"part": "snippet", "mine": "true"}, timeout=30)
    print("status", r.status_code)
    if r.ok:
        for c in r.json().get("items", []): print("CANAL:", c["id"], c["snippet"]["title"], c["snippet"].get("customUrl"))
    else: print(r.text[:400])
