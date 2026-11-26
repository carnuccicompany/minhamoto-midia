"""Sonda: abre rotas e registra tudo (requisições, console, erros) + print rápido."""
import asyncio, json, os, sys, subprocess
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.dirname(__file__))
from mock_supabase import MockSupabase, init_script

URL = "http://127.0.0.1:5176"
W, H = 393, 852
TOP, BOT = 59, 34


def gerar_dados():
    subprocess.run(["bun", "/tmp/telas-102/_gerador/semente.ts"], cwd="/tmp/app-102", check=True)
    return json.load(open("/tmp/telas-102/_gerador/dados.json")), json.load(open("/tmp/telas-102/_gerador/local.json"))


async def preparar(p, extra_init=None):
    dados, local = gerar_dados()
    mock = MockSupabase(dados)
    b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox", "--force-color-profile=srgb", "--lang=pt-BR"],
                                env={**os.environ, "LANG": "pt_BR.UTF-8", "LANGUAGE": "pt_BR:pt"})
    ctx = await b.new_context(viewport={"width": W, "height": H - TOP - BOT}, device_scale_factor=3, is_mobile=True, has_touch=True,
                              locale="pt-BR", timezone_id="America/Sao_Paulo",
                              user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1")
    externos, locais = [], []

    async def roteador(route):
        url = route.request.url
        if url.startswith("https://mock-supabase.invalid/"):
            return await mock.handle(route)
        if url.startswith(URL) or url.startswith("data:") or url.startswith("blob:"):
            pth = url[len(URL):]
            if pth.startswith("/api/public/acesso-premium"):
                locais.append(("MOCK", pth))
                return await route.fulfill(status=200, content_type="application/json", body='{"versao":1,"estado":"liberado","origem":"assinatura"}')
            if pth.startswith("/_serverFn") or pth.startswith("/api/"):
                locais.append((route.request.method, pth[:160]))
            return await route.continue_()
        if url.startswith("https://fonts.googleapis.com/"):
            return await route.fulfill(status=200, content_type="text/css", body="/* sem rede */")
        externos.append(url[:160])
        return await route.abort()

    await ctx.route("**/*", roteador)
    await ctx.add_init_script(init_script(local))
    if extra_init:
        await ctx.add_init_script(extra_init)
    pg = await ctx.new_page()
    logs = []
    pg.on("console", lambda m: logs.append(f"{m.type}: {m.text[:200]}"))
    pg.on("pageerror", lambda e: logs.append(f"PAGEERROR: {str(e)[:200]}"))
    return b, ctx, pg, mock, externos, locais, logs


async def main(rotas):
    async with async_playwright() as p:
        b, ctx, pg, mock, externos, locais, logs = await preparar(p)
        for i, r in enumerate(rotas):
            if i == 0:
                await pg.goto(URL + r, wait_until="load", timeout=120000)
            else:
                await pg.evaluate("(p)=>{history.pushState({__TSR_index:(history.state?.__TSR_index||0)+1},'',p); dispatchEvent(new PopStateEvent('popstate',{state:history.state}));}", r)
            await pg.wait_for_timeout(6000)
            nome = r.strip("/").replace("/", "_") or "raiz"
            await pg.screenshot(path=f"/tmp/telas-work-102/sonda-{nome}.png")
            print("URL", pg.url)
            print("TEXTO", (await pg.evaluate("document.body.innerText"))[:600].replace("\n", " | "))
        print("EXTERNOS", externos[:30])
        print("LOCAIS", locais[:30])
        print("MOCK LOG", mock.log[:80])
        print("DESCONHECIDOS", mock.desconhecidos)
        print("LOGS", "\n".join(logs[-60:]))
        await b.close()

os.makedirs("/tmp/telas-work-102", exist_ok=True)
asyncio.run(main(sys.argv[1:] or ["/"]))
