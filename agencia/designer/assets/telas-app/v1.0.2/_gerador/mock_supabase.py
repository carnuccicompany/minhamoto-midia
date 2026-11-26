"""
Mock em memória do Supabase (Auth + PostgREST + Storage + RPC) para a captura
das telas reais do MinhaMoto. Nenhuma requisição sai da máquina: o app da
cópia (/tmp/app-102) aponta para https://mock-supabase.invalid (host que
nunca resolve) e o Playwright responde tudo aqui. Toda outra rede externa é
abortada pelo script de captura.

Dados 100% fictícios: moto simulada "Minha Titan" (dados.json, gerado a partir
de src/lib/previa-fixtures.ts com o patch de marketing).
"""
import base64, json, time, urllib.parse

HOST = "mock-supabase.invalid"
UID = "7f3c2a10-5b1e-4c8d-9a2f-3e6b8d4c1a90"
SESSAO_ID = "5d1b8e2a-4c3f-4a6e-9b7d-2f8e1c3a4b5d"
EMAIL = "rafael.souza@email.com"
NOME = "Rafael Souza"
STORAGE_KEY = "sb-mock-supabase-auth-token"


def _b64(d):
    return base64.urlsafe_b64encode(json.dumps(d, separators=(",", ":")).encode()).decode().rstrip("=")


def _agora():
    return int(time.time())


def access_token():
    agora = _agora()
    payload = {
        "iss": f"https://{HOST}/auth/v1", "sub": UID, "aud": "authenticated",
        "exp": agora + 30 * 86400, "iat": agora - 60, "email": EMAIL, "phone": "",
        "app_metadata": {"provider": "email", "providers": ["email"]},
        "user_metadata": {"minhamoto_nome": NOME, "email": EMAIL},
        "role": "authenticated", "aal": "aal1",
        "amr": [{"method": "password", "timestamp": agora - 3600}],
        "session_id": SESSAO_ID, "is_anonymous": False,
    }
    return _b64({"alg": "HS256", "typ": "JWT"}) + "." + _b64(payload) + ".bW9jay1zZW0tYXNzaW5hdHVyYQ"


def usuario():
    return {
        "id": UID, "aud": "authenticated", "role": "authenticated", "email": EMAIL,
        "email_confirmed_at": "2026-03-02T14:10:00Z", "phone": "",
        "confirmed_at": "2026-03-02T14:10:00Z", "last_sign_in_at": "2026-11-20T12:00:00Z",
        "app_metadata": {"provider": "email", "providers": ["email", "google"]},
        "user_metadata": {"minhamoto_nome": NOME, "email": EMAIL, "email_verified": True},
        # Conta com e-mail confirmado + Google vinculados (o Perfil mostra os métodos reais).
        "identities": [
            {"identity_id": "a1", "id": UID, "user_id": UID, "provider": "email",
             "identity_data": {"email": EMAIL, "email_verified": True, "sub": UID},
             "created_at": "2026-03-02T14:09:00Z", "updated_at": "2026-03-02T14:09:00Z"},
            {"identity_id": "a2", "id": "108234567890123456789", "user_id": UID, "provider": "google",
             "identity_data": {"email": EMAIL, "full_name": NOME, "sub": "108234567890123456789"},
             "created_at": "2026-05-10T18:00:00Z", "updated_at": "2026-05-10T18:00:00Z"},
        ],
        "created_at": "2026-03-02T14:09:00Z", "updated_at": "2026-11-20T12:00:00Z",
        "is_anonymous": False,
    }


def sessao():
    agora = _agora()
    return {
        "access_token": access_token(), "token_type": "bearer", "expires_in": 30 * 86400,
        "expires_at": agora + 30 * 86400, "refresh_token": "mock-refresh-token",
        "user": usuario(),
    }


class MockSupabase:
    def __init__(self, dados):
        self.tabelas = {
            "dados_usuario": [
                {"user_id": UID, "chave": k, "valor": v, "atualizado_em": "2026-11-20T12:00:00Z"}
                for k, v in dados.items()
            ],
            "perfis": [{"id": UID, "nome": NOME}],
            "exclusoes_conta": [],
            "legal_aceites_conta": [],
        }
        self.log = []          # (método, caminho) de tudo que chegou
        self.desconhecidos = []  # o que caiu no padrão (sem resposta específica)
        self.rpc = {
            # Assinatura MinhaMoto Pro ativa (autoridade da web).
            "pro_producao_operacao_propria": True,
            "acesso_premium_proprio": {"ativo": True, "premium": True, "plano": "pro"},
            "sessao_atual_recente": True,
            "transferencia_situacao": None,
            "transferencia_consultar": None,
            "exclusao_situacao": None,
            # Sem foto de perfil (avatar com iniciais).
            "foto_perfil_proprio": {"versao": 1, "fotoPath": None, "revisao": 0},
            # Programa de indicações não ativo nesta conta (painel some do Perfil).
            "indicacoes_cliente": None,
        }

    # ------------------------------------------------------------------ util
    @staticmethod
    def _json(route, corpo, status=200, headers=None):
        h = {"content-type": "application/json; charset=utf-8",
             "access-control-allow-origin": "*",
             "access-control-allow-headers": "*",
             "access-control-allow-methods": "GET,POST,PUT,PATCH,DELETE,OPTIONS",
             "access-control-expose-headers": "content-range,content-profile"}
        if headers:
            h.update(headers)
        return route.fulfill(status=status, headers=h, body="" if corpo is None and status == 204 else json.dumps(corpo))

    @staticmethod
    def _filtro(linhas, params):
        out = list(linhas)
        for col, vals in params.items():
            if col in ("select", "order", "limit", "offset", "on_conflict", "columns"):
                continue
            for v in vals:
                if v.startswith("eq."):
                    alvo = v[3:]
                    out = [l for l in out if str(l.get(col)) == alvo]
                elif v.startswith("in.("):
                    itens = [x.strip().strip('"') for x in v[4:-1].split(",")] if v[4:-1] else []
                    out = [l for l in out if str(l.get(col)) in itens]
                elif v.startswith("is.null"):
                    out = [l for l in out if l.get(col) is None]
                elif v.startswith("neq."):
                    out = [l for l in out if str(l.get(col)) != v[4:]]
        return out

    @staticmethod
    def _projetar(linhas, select):
        if not select or select.strip() == "*":
            return linhas
        cols = [c.strip() for c in select.split(",") if c.strip()]
        return [{c: l.get(c) for c in cols} for l in linhas]

    # --------------------------------------------------------------- handler
    async def handle(self, route):
        req = route.request
        u = urllib.parse.urlparse(req.url)
        caminho = u.path
        params = urllib.parse.parse_qs(u.query, keep_blank_values=True)
        metodo = req.method
        self.log.append((metodo, caminho + ("?" + u.query if u.query else "")))
        if metodo == "OPTIONS":
            return await self._json(route, None, 204)

        # ---------------- Auth
        if caminho.startswith("/auth/v1/"):
            sub = caminho[len("/auth/v1/"):]
            if sub == "user":
                return await self._json(route, usuario())
            if sub == "token":
                return await self._json(route, sessao())
            if sub == "logout":
                return await self._json(route, None, 204)
            if sub.startswith(".well-known/jwks"):
                return await self._json(route, {"keys": []})
            if sub == "settings":
                return await self._json(route, {"external": {"email": True}, "disable_signup": False})
            self.desconhecidos.append((metodo, caminho))
            return await self._json(route, {})

        # ---------------- RPC
        if caminho.startswith("/rest/v1/rpc/"):
            nome = caminho[len("/rest/v1/rpc/"):]
            if nome not in self.rpc:
                self.desconhecidos.append((metodo, caminho))
            return await self._json(route, self.rpc.get(nome))

        # ---------------- PostgREST
        if caminho.startswith("/rest/v1/"):
            tabela = caminho[len("/rest/v1/"):]
            linhas = self.tabelas.setdefault(tabela, [])
            if tabela not in ("dados_usuario", "perfis", "exclusoes_conta", "legal_aceites_conta", "metricas_desempenho"):
                self.desconhecidos.append((metodo, caminho))
            unico = "vnd.pgrst.object" in (req.headers.get("accept") or "")
            if metodo in ("GET", "HEAD"):
                res = self._projetar(self._filtro(linhas, params), (params.get("select") or ["*"])[0])
                if unico:
                    if len(res) == 1:
                        return await self._json(route, res[0])
                    return await self._json(route, {"code": "PGRST116", "message": "JSON object requested, multiple (or no) rows returned", "details": f"The result contains {len(res)} rows", "hint": None}, 406)
                return await self._json(route, res, headers={"content-range": f"0-{max(len(res)-1,0)}/{len(res)}"})
            corpo = req.post_data_json if req.post_data else None
            if metodo == "POST":
                novos = corpo if isinstance(corpo, list) else ([corpo] if corpo else [])
                if tabela == "dados_usuario":
                    for n in novos:
                        n = dict(n); n.setdefault("user_id", UID)
                        linhas[:] = [l for l in linhas if not (l["user_id"] == n["user_id"] and l["chave"] == n.get("chave"))]
                        linhas.append(n)
                elif tabela != "metricas_desempenho":
                    linhas.extend(novos)
                return await self._json(route, novos if "return=representation" in (req.headers.get("prefer") or "") else None, 201 if novos else 204)
            if metodo == "PATCH":
                alvo = self._filtro(linhas, params)
                for l in alvo:
                    l.update(corpo or {})
                return await self._json(route, alvo)
            if metodo == "DELETE":
                alvo = self._filtro(linhas, params)
                linhas[:] = [l for l in linhas if l not in alvo]
                return await self._json(route, alvo)

        # ---------------- Storage (sem fotos/arquivos)
        if caminho.startswith("/storage/v1/"):
            if "/object/list/" in caminho:
                return await self._json(route, [])
            if "/object/sign/" in caminho:
                return await self._json(route, {"error": "not_found", "message": "Object not found", "statusCode": "404"}, 400)
            self.desconhecidos.append((metodo, caminho))
            return await self._json(route, {})

        # ---------------- Functions / outros
        self.desconhecidos.append((metodo, caminho))
        return await self._json(route, {})


INIT_SESSAO_JS = """
(() => {
  try {
    if (location.port !== '5176') return;
    if (sessionStorage.getItem('__semeado')) return;   // só na 1ª carga da aba
    sessionStorage.setItem('__semeado', '1');
    localStorage.setItem('%(key)s', %(val)s);
    const extra = %(extra)s;
    for (const k in extra) localStorage.setItem(k, extra[k]);
  } catch (e) {}
})();
"""


def init_script(local=None):
    """Sessão fictícia (Auth persistido no aparelho) + chaves locais extras."""
    return INIT_SESSAO_JS % {"key": STORAGE_KEY, "val": json.dumps(json.dumps(sessao())),
                             "extra": json.dumps(local or {})}
