"""Diagnóstico: abre rotas (com a mesma sessão da captura) e lista botões/links visíveis.
Uso: python3 explorar.py /rota [/rota2 ...]   ('!js' depois de uma rota roda código na página)"""
import asyncio, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from capturar import Sessao, nav, M, RAW
from playwright.async_api import async_playwright

JS = """() => [...document.querySelectorAll('button,a,[role=button],[role=tab]')].map(e => {
  const r = e.getBoundingClientRect();
  return [e.tagName, (e.getAttribute('aria-label')||'') , (e.innerText||'').replace(/\\s+/g,' ').slice(0,60), e.className.toString().slice(0,50), Math.round(r.y), r.width>0];
}).filter(x => x[5])"""

async def main(args):
    async with async_playwright() as p:
        s = Sessao(); pg = await s.abrir(p)
        for a in args:
            if a.startswith("!"):
                print(await pg.evaluate(a[1:])); await pg.wait_for_timeout(1500); continue
            if a.startswith("#"):
                
                try:
                    await pg.locator(a[1:]).first.click(timeout=8000); await pg.wait_for_timeout(1800)
                except Exception as e:
                    print("!! falhou", a, str(e)[:80]); continue
                print("== clique", a)
                for x in await pg.evaluate(JS.replace("document.querySelectorAll", "(document.querySelector('[role=dialog]')||document).querySelectorAll")): print("  ", x[:5])
                print("  TEXTO:", (await pg.evaluate("(document.querySelector('[role=dialog]')||document.body).innerText"))[:500].replace("\n"," | "))
                continue
            if a.startswith("~"):
                await pg.keyboard.press("Escape"); await pg.wait_for_timeout(800); continue
            if a.startswith("@"):
                await pg.screenshot(path=f"{RAW}/explorar-{a[1:]}.png"); continue
            await nav(pg, a.replace("M/", M + "/").replace("=M", M))
            print("==", a, pg.url)
            for x in await pg.evaluate(JS): print("  ", x[:5])
        await s.b.close()
asyncio.run(main(sys.argv[1:]))
