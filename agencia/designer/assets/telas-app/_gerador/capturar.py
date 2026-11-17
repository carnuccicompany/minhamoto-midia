import asyncio, sys, json, os
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont
URL='http://localhost:5173'
TOP, BOT = 59, 34     # safe areas iPhone 15 (pt)
W, H = 393, 852
OUT='/tmp/telas/out'; os.makedirs(OUT, exist_ok=True)
HIDE_JS = r'''
() => {
  const kill = (pred) => { for (const el of document.querySelectorAll('body *')) { try { if (pred(el)) el.style.setProperty('display','none','important'); } catch(e){} } };
  // botão DEV e painel
  let st=document.getElementById('__hide'); if(!st){st=document.createElement('style');st.id='__hide';document.head.appendChild(st);} st.textContent='[data-painel-previa],[aria-label="Cenário de demonstração"],[aria-label="Cenários fictícios"]{display:none!important}';
  // selo "Prévia visual · dados fictícios"
  for (const el of document.querySelectorAll('body *')) { const t=(el.innerText||'').trim().toUpperCase(); if (t==='PRÉVIA VISUAL · DADOS FICTÍCIOS' && el.children.length<=2) el.style.setProperty('display','none','important'); }
  // card "Baixe o aplicativo no seu celular" (só web) e "Testar onboarding (só na prévia)"
  for (const el of document.querySelectorAll('body *')) {
    const t=(el.innerText||'').trim();
    if (t.startsWith('Baixe o aplicativo no seu celular') && t.length<260 && el.offsetHeight<400) el.style.setProperty('display','none','important');
    if (t==='Cenários de teste da prévia' && el.children.length<=2) (el.closest('a,button')||el).style.setProperty('display','none','important');
    if (t==='Só prévia:' && el.tagName==='SPAN') el.parentElement.style.setProperty('display','none','important');
    if (t==='Testar onboarding (só na prévia)') { (el.closest('button,a')||el).style.setProperty('display','none','important'); }
  }
}
'''
async def cenario(pg, nome):
    await pg.evaluate("async (c)=>{const m=await import('/src/lib/previa-visual.ts'); m.restaurarPrevia(c);}", nome); await pg.wait_for_timeout(1200)
async def nav(pg, path):
    await pg.evaluate("(p)=>{history.pushState({__TSR_index:(history.state?.__TSR_index||0)+1},'',p); dispatchEvent(new PopStateEvent('popstate',{state:history.state}));}", path)
    await pg.wait_for_timeout(2200); await pg.evaluate('window.scrollTo(0,0)')
def compor(raw, dest, full=False):
    im = Image.open(raw).convert('RGB'); s=3
    if full:
        im.save(dest); return
    bg = im.getpixel((im.width//2, 2))
    can = Image.new('RGB', (W*s, H*s), bg); can.paste(im, (0, TOP*s))
    # faixa inferior com a cor do rodapé
    bb = im.getpixel((im.width//2, im.height-2)); ImageDraw.Draw(can).rectangle([0,(TOP+im.height//s)*s, W*s, H*s], fill=bb)
    d = ImageDraw.Draw(can)
    lum = sum(bg)/3; fg = (255,255,255) if lum<128 else (0,0,0)
    try: f = ImageFont.truetype('/home/claude/minhamoto-midia/agencia/direcao-v2/fontes/../fontes/sora-latin-800-normal.woff2', 51)
    except Exception: f = None
    try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 50)
    except Exception: f = ImageFont.load_default()
    d.text((96*1.0+40, 58), '9:41', fill=fg, font=f)
    # ilha dinâmica
    d.rounded_rectangle([W*s//2-188, 33, W*s//2+188, 33+111], radius=56, fill=(0,0,0))
    # ícones: sinal, wifi, bateria
    x = W*s-250; y=66
    for i,h in enumerate([14,20,27,34]): d.rounded_rectangle([x+i*16, y+34-h, x+i*16+10, y+34], radius=3, fill=fg)
    x2 = x+84; d.pieslice([x2, y-6, x2+50, y+44], 225, 315, fill=fg)
    d.pieslice([x2+12, y+8, x2+38, y+34], 225, 315, fill=bg); d.pieslice([x2+18, y+16, x2+32, y+30], 225, 315, fill=fg)
    xb = x2+70; d.rounded_rectangle([xb, y+4, xb+66, y+34], radius=9, outline=fg, width=4); d.rounded_rectangle([xb+6, y+10, xb+56, y+28], radius=5, fill=fg); d.rounded_rectangle([xb+69, y+14, xb+74, y+24], radius=2, fill=fg)
    # home indicator
    d.rounded_rectangle([W*s//2-200, H*s-25, W*s//2+200, H*s-10], radius=8, fill=fg)
    can.save(dest)
async def main(plano):
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--force-color-profile=srgb'])
        ctx=await b.new_context(viewport={'width':W,'height':H-TOP-BOT},device_scale_factor=3,is_mobile=True,has_touch=True,locale='pt-BR',timezone_id='America/Sao_Paulo',
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1')
        pg=await ctx.new_page(); erros=[]
        pg.on('pageerror', lambda e: erros.append(str(e)[:150]))
        await pg.goto(URL+'/preview-visual', wait_until='networkidle'); await pg.wait_for_timeout(2000)
        for passo in plano:
            acao = passo[0]
            try:
                if acao=='cenario': await cenario(pg, passo[1])
                elif acao=='url': await pg.goto(URL+passo[1], wait_until='networkidle'); await pg.wait_for_timeout(2200)
                elif acao=='nav': await nav(pg, passo[1])
                elif acao=='clique': await pg.get_by_text(passo[1], exact=passo[2] if len(passo)>2 else False).first.click(); await pg.wait_for_timeout(1500)
                elif acao=='rolar': await pg.mouse.wheel(0, passo[1]); await pg.wait_for_timeout(900)
                elif acao=='topo': await pg.evaluate('window.scrollTo(0,0)'); await pg.wait_for_timeout(500)
                elif acao=='chip': await pg.evaluate("(n)=>{for(const b of document.querySelectorAll('[role=radio]')) if(b.innerText.trim()===n){b.click();return}}", passo[1]); await pg.wait_for_timeout(1500)
                elif acao=='pular':
                    for _ in range(6):
                        pul = pg.get_by_role('button', name='Pular por enquanto')
                        if await pul.count() and await pul.first.is_visible(): await pul.first.click(); await pg.wait_for_timeout(700)
                        else: break
                elif acao=='fill': await pg.locator(passo[1]).first.fill(passo[2]); await pg.wait_for_timeout(400)
                elif acao=='js': await pg.evaluate(passo[1]); await pg.wait_for_timeout(1800)
                elif acao=='foto':
                    for _ in range(6):
                        pul = pg.get_by_role('button', name='Pular por enquanto')
                        if await pul.count() and await pul.first.is_visible(): await pul.first.click(); await pg.wait_for_timeout(700)
                        else: break
                    await pg.wait_for_timeout(500)
                    await pg.evaluate(HIDE_JS); await pg.wait_for_timeout(300)
                    raw=f'{OUT}/_raw.png'
                    full = len(passo)>2 and passo[2]=='full'
                    if full: await pg.evaluate("()=>{document.getElementById('__hide').textContent+='nav[aria-label=\"Seções da moto\"]{display:none!important}'}")
                    await pg.screenshot(path=raw, full_page=full)
                    await pg.evaluate("()=>{const s=document.getElementById('__hide'); if(s) s.textContent='';}")
                    compor(raw, f'{OUT}/{passo[1]}.png', full=full); print('ok', passo[1], pg.url)
            except Exception as e:
                print('FALHA', passo, str(e)[:200])
        print('erros js', erros[:5]); await b.close()
asyncio.run(main(json.loads(open(sys.argv[1]).read())))
