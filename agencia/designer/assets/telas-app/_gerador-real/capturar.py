"""
Captura das telas REAIS do MinhaMoto (rotas _authenticated.*), a partir da
cópia /tmp/app-real (HEAD do repositório + patch deste gerador).

- Rede: tudo que não é o vite local (127.0.0.1:5174) é abortado, exceto o host
  falso https://mock-supabase.invalid, respondido em memória por mock_supabase.py.
- Dados: semente.ts (moto simulada "Minha Titan"), relógio fixo às 9:41 de hoje.
- Saída: /tmp/telas-reais/<nome>.png (1179x2556, barra de status 9:41) e
  /tmp/telas-reais/rolagem/<nome>.png (página inteira).

Uso:  python3 capturar.py            (todas)
      python3 capturar.py 02-saude   (só as que começam com esses prefixos)
"""
import asyncio, datetime, json, os, subprocess, sys
from zoneinfo import ZoneInfo
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mock_supabase import MockSupabase, init_script

URL = "http://127.0.0.1:5174"
TOP, BOT = 59, 34          # áreas seguras do iPhone 15 (pt)
W, H = 393, 852
OUT = "/tmp/telas-reais"
RAW = "/tmp/telas-work-real"
GER = os.path.dirname(os.path.abspath(__file__))
M = "/moto/honda-cg-160__titan__2022"
os.makedirs(OUT + "/rolagem", exist_ok=True)
os.makedirs(RAW, exist_ok=True)

TZ = ZoneInfo("America/Sao_Paulo")
AGORA = datetime.datetime.now(TZ).replace(hour=9, minute=41, second=0, microsecond=0)
AGORA_MS = int(AGORA.timestamp() * 1000)


# ----------------------------------------------------------------- composição
def barra_status(fg, largura, alt=177, k=4):
    """Barra de status estilo iOS (mesmo desenho do gerador da prévia): 9:41, sinal, wi-fi,
    bateria, sem ilha. Agora transparente: vai POR CIMA da área segura que o próprio app pinta."""
    Wk, Hk = largura * k, alt * k
    im = Image.new("RGBA", (Wk, Hk), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    fg = tuple(fg) + (255,)
    f = None
    for cand in ["/home/claude/carnuccicompany/minhamoto-midia/agencia/designer/assets/fontes/inter-latin-600-normal.woff2",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        try:
            f = ImageFont.truetype(cand, 50 * k); break
        except Exception:
            pass
    cy = 88 * k
    tb = d.textbbox((0, 0), "9:41", font=f); th = tb[3] - tb[1]
    d.text((150 * k, cy - th // 2 - tb[1]), "9:41", fill=fg, font=f)
    x = largura * k - 300 * k; base = cy + 17 * k
    for i, h in enumerate([12, 18, 25, 33]):
        d.rounded_rectangle([x + i * 17 * k, base - h * k, x + i * 17 * k + 11 * k, base], radius=3 * k, fill=fg)
    cx = largura * k - 196 * k; cyw = cy + 16 * k
    for r in (40, 27):
        d.arc([cx - r * k, cyw - r * k, cx + r * k, cyw + r * k], 225, 315, fill=fg, width=8 * k)
    d.pieslice([cx - 14 * k, cyw - 14 * k, cx + 14 * k, cyw + 14 * k], 225, 315, fill=fg)
    xb = largura * k - 150 * k; y0 = cy - 17 * k; y1 = cy + 17 * k
    d.rounded_rectangle([xb, y0, xb + 72 * k, y1], radius=10 * k, outline=fg, width=4 * k)
    d.rounded_rectangle([xb + 7 * k, y0 + 7 * k, xb + 58 * k, y1 - 7 * k], radius=5 * k, fill=fg)
    d.rounded_rectangle([xb + 76 * k, cy - 6 * k, xb + 82 * k, cy + 6 * k], radius=3 * k, fill=fg)
    return im.resize((largura, alt), Image.LANCZOS)


def compor(raw, dest, full=False):
    """A tela já vem do tamanho do aparelho (393x852 @3x), com as áreas seguras
    emuladas (topo 59 pt, base 34 pt) — o app pinta o fundo delas como no iPhone.
    Aqui só desenhamos a barra de status e o indicador de início por cima."""
    can = Image.open(raw).convert("RGBA"); s = 3
    bg = can.getpixel((can.width // 2, 8))[:3]
    lum = sum(bg) / 3; fg = (255, 255, 255) if lum < 128 else (0, 0, 0)
    bar = barra_status(fg, W * s)
    can.alpha_composite(bar, (0, 0))
    if not full:
        bb = can.getpixel((can.width // 2, can.height - 4))[:3]
        fgb = (255, 255, 255) if sum(bb) / 3 < 128 else (0, 0, 0)
        hi = Image.new("RGBA", (W * s * 4, 25 * 4), (0, 0, 0, 0))
        ImageDraw.Draw(hi).rounded_rectangle([(W * s // 2 - 200) * 4, 0, (W * s // 2 + 200) * 4, 15 * 4], radius=8 * 4, fill=fgb + (255,))
        hi = hi.resize((W * s, 25), Image.LANCZOS); can.alpha_composite(hi, (0, H * s - 25))
    can.convert("RGB").save(dest)


# ------------------------------------------------------------------- roteiro
# Cada tela: (nome, rota, ações antes da foto, gerar rolagem?)
# ações: ("clique", texto[, exato]) | ("rolar", px) | ("seletor", css) | ("esperar", ms) | ("js", código)
TELAS = [
    ("01-garagem", "/", [], True),
    ("02-saude", M, [], True),
    ("03-manutencao", M + "/manutencao", [], True),
    ("04-uso-km", M + "/uso", [], True),
    ("05-combustivel", M + "/combustivel", [], True),
    ("06-historico", M + "/historico", [], True),
    ("07-documentos", M + "/documentos", [], True),
    ("08-moto-especificacoes", M + "/moto", [], True),
    ("09-resumo-mes", M + "/resumo", [], True),
    ("10-lista-revisao", M + "/lista", [], True),
    ("11-cuidados", M + "/cuidados", [], True),
    ("12-sinais-problema", M + "/sinais", [], True),
    ("13-conheca-moto", M + "/conheca", [], True),
    ("14-carteirinha", M + "/carteirinha", [], True),
    ("15-notificacoes", "/notificacoes", [], True),
    ("16-perfil", "/perfil", [], True),
    ("25-fontes", M + "/fontes", [], True),
]
FOLHAS = json.load(open(os.path.join(GER, "folhas.json"))) if os.path.exists(os.path.join(GER, "folhas.json")) else []

PROIBIDO = ["demonstração", "demonstracao", "exemplo", "conta de teste", "funciona só no app", "não foi possível",
            "nao foi possivel", "sem conexão", "offline", "tente novamente", "erro", "manutenção programada",
            "dados fictícios", "prévia", "carregando"]


def gerar_semente():
    env = {**os.environ, "AGORA_MS": str(AGORA_MS)}
    subprocess.run(["bun", os.path.join(GER, "semente.ts")], cwd="/tmp/app-real", check=True, env=env)
    return json.load(open(os.path.join(GER, "dados.json"))), json.load(open(os.path.join(GER, "local.json")))


async def estabilizar(pg, extra=0):
    """Espera fontes, rede local e o fim de carregamentos/esqueletos."""
    try:
        await pg.wait_for_load_state("networkidle", timeout=15000)
    except Exception:
        pass
    await pg.evaluate("document.fonts.ready.then(()=>true)")
    for _ in range(40):
        pendente = await pg.evaluate("""() => {
          const t = document.body.innerText || '';
          const sk = document.querySelectorAll('.animate-pulse,[aria-busy="true"],[data-carregando]').length;
          return sk + (/Carregando/i.test(t) ? 1 : 0);
        }""")
        if not pendente:
            break
        await pg.wait_for_timeout(250)
    await pg.wait_for_timeout(1500 + extra)


async def nav(pg, rota):
    await pg.evaluate("(p)=>{history.pushState({__TSR_index:(history.state?.__TSR_index||0)+1},'',p); dispatchEvent(new PopStateEvent('popstate',{state:history.state}));}", rota)
    await pg.wait_for_timeout(800)
    await estabilizar(pg)
    await pg.evaluate("window.scrollTo(0,0)")
    await pg.wait_for_timeout(400)


async def executar(pg, acoes):
    for a in acoes:
        t = a[0]
        if t == "clique":
            loc = pg.get_by_text(a[1], exact=a[2] if len(a) > 2 else False).first
            await loc.scroll_into_view_if_needed(); await loc.click(); await pg.wait_for_timeout(1400)
        elif t == "papel":
            loc = pg.get_by_role(a[1], name=a[2], exact=a[3] if len(a) > 3 else False).first
            await loc.scroll_into_view_if_needed(); await loc.click(); await pg.wait_for_timeout(1400)
        elif t == "seletor":
            loc = pg.locator(a[1]).first
            await loc.scroll_into_view_if_needed(); await loc.click(); await pg.wait_for_timeout(1400)
        elif t == "rolar":
            await pg.mouse.wheel(0, a[1]); await pg.wait_for_timeout(900)
        elif t == "rolarate":
            await pg.get_by_text(a[1], exact=False).first.evaluate("e=>e.scrollIntoView({block:'start'})")
            await pg.evaluate(f"window.scrollBy(0,{a[2] if len(a) > 2 else -90})"); await pg.wait_for_timeout(900)
        elif t == "preencher":
            loc = pg.locator(a[1]).first
            val = a[2].replace("@hoje", AGORA.strftime("%Y-%m-%d"))
            if val.startswith("@dias:"):   # data de N dias atrás (AAAA-MM-DD)
                val = (AGORA - datetime.timedelta(days=int(val[6:]))).strftime("%Y-%m-%d")
            await loc.fill(val); await pg.wait_for_timeout(400)
        elif t == "rotulo":
            loc = pg.get_by_label(a[1], exact=False).first
            await loc.fill(a[2]); await pg.wait_for_timeout(400)
        elif t == "esperar":
            await pg.wait_for_timeout(a[1])
        elif t == "js":
            await pg.evaluate(a[1]); await pg.wait_for_timeout(1200)
    # sem anel de foco (o app foca o "fechar" ao abrir folhas)
    await pg.evaluate("document.activeElement && document.activeElement.blur && document.activeElement.blur()")
    await estabilizar(pg, 300)


async def foto(pg, nome, full, avisos):
    texto = (await pg.evaluate("document.body.innerText")).lower()
    for p in PROIBIDO:
        if p in texto:
            i = texto.index(p)
            avisos.append(f"{nome}: contém '{p}' → …{texto[max(0, i-50):i+40]!r}…")
    raw = f"{RAW}/_raw.png"
    await pg.screenshot(path=raw, animations="disabled")
    compor(raw, f"{OUT}/{nome}.png")
    if full:
        await pg.evaluate("window.scrollTo(0,0)"); await pg.wait_for_timeout(600)
        await pg.add_style_tag(content='nav[aria-label="Seções da moto"]{display:none!important}')
        await pg.screenshot(path=raw, full_page=True, animations="disabled")
        compor(raw, f"{OUT}/rolagem/{nome}.png", full=True)
        await pg.evaluate("""()=>{for(const s of document.querySelectorAll('style')) if(s.textContent.includes('Seções da moto')&&s.textContent.length<90) s.remove();}""")
    print("ok", nome, pg.url, flush=True)


async def main(filtro):
    dados, local = gerar_semente()
    mock = MockSupabase(dados)
    externos, locais, erros = [], [], []
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome",
                                    args=["--no-sandbox", "--force-color-profile=srgb", "--lang=pt-BR",
                                          "--disable-background-networking", "--disable-component-update",
                                          "--disable-sync", "--disable-default-apps", "--no-pings", "--no-first-run"],
                                    # Proxy morto: qualquer tráfego interno do próprio Chrome morre na máquina.
                                    proxy={"server": "http://127.0.0.1:9", "bypass": "127.0.0.1,localhost"},
                                    env={**os.environ, "LANG": "pt_BR.UTF-8", "LANGUAGE": "pt_BR:pt"})
        ctx = await b.new_context(viewport={"width": W, "height": H}, device_scale_factor=3,
                                  is_mobile=True, has_touch=True, locale="pt-BR", timezone_id="America/Sao_Paulo",
                                  user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1")

        async def roteador(route):
            url = route.request.url
            if url.startswith("https://mock-supabase.invalid/"):
                return await mock.handle(route)
            if url.startswith(URL):
                pth = url[len(URL):]
                if pth.startswith("/api/public/acesso-premium"):
                    # Assinatura MinhaMoto Pro ativa (resposta no formato do servidor).
                    return await route.fulfill(status=200, content_type="application/json",
                                               body='{"versao":1,"estado":"liberado","origem":"assinatura"}')
                if pth.startswith("/_serverFn") or pth.startswith("/api/"):
                    locais.append((route.request.method, pth[:90]))
                    return await route.abort()      # métricas etc.: nada de servidor real
                return await route.continue_()
            if url.startswith("data:") or url.startswith("blob:"):
                return await route.continue_()
            if url.startswith("https://fonts.googleapis.com/"):
                # Oxanium só é usada na tela de manutenção do site (fora das rotas capturadas).
                return await route.fulfill(status=200, content_type="text/css", body="/* sem rede */")
            externos.append(url[:120])
            return await route.abort()

        await ctx.route("**/*", roteador)
        await ctx.add_init_script(init_script(local))
        await ctx.clock.install(time=AGORA)
        pg = await ctx.new_page()
        # Áreas seguras do iPhone 15 (o app usa viewport-fit=cover + env(safe-area-inset-*)).
        cdp = await ctx.new_cdp_session(pg)
        await cdp.send("Emulation.setSafeAreaInsetsOverride", {"insets": {"top": TOP, "bottom": BOT, "left": 0, "right": 0}})
        pg.on("pageerror", lambda e: erros.append(str(e)[:200]))
        await pg.goto(URL + "/", wait_until="load", timeout=180000)
        await pg.wait_for_timeout(4000)
        await estabilizar(pg, 1500)

        avisos = []
        for nome, rota, acoes, full in TELAS + [tuple(f) for f in FOLHAS]:
            if filtro and not any(nome.startswith(f) for f in filtro):
                continue
            try:
                await nav(pg, rota)
                await executar(pg, acoes)
                await foto(pg, nome, full, avisos)
            except Exception as e:
                print("FALHA", nome, str(e)[:300], flush=True)
            # fecha folhas/pop-ups antes da próxima tela
            if acoes:
                await pg.keyboard.press("Escape"); await pg.wait_for_timeout(500)
        print("AVISOS", avisos)
        print("EXTERNOS bloqueados", externos)
        print("LOCAIS abortados", sorted(set(locais)))
        print("MOCK sem resposta específica", sorted(set(mock.desconhecidos)))
        print("ERROS JS", erros[:10])
        await b.close()

asyncio.run(main(sys.argv[1:]))
