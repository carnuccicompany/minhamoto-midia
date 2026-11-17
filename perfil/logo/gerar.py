import asyncio, os
from playwright.async_api import async_playwright
import base64
SVG='data:image/svg+xml;base64,'+base64.b64encode(open('simbolo.svg','rb').read()).decode()
BG='''background:
 radial-gradient(30% 26% at 11% 5%, rgba(40,245,255,1) 0%, rgba(20,190,255,.75) 38%, rgba(0,80,255,0) 100%),
 radial-gradient(110% 80% at 50% 118%, rgba(2,20,140,.95) 0%, rgba(2,28,170,.6) 45%, rgba(0,60,255,0) 80%),
 linear-gradient(180deg,#0048ff 0%,#0043fb 40%,#0532d6 78%,#0424b2 100%);'''
def html(w,h,sym_w,radius=0,rim=False,cy=0.5):
    rimcss = "box-shadow: inset 0 0 0 %dpx rgba(120,190,255,.35), inset 0 %dpx %dpx rgba(255,255,255,.18);"%(w//180, w//90, w//30) if rim else ""
    return f'''<html><body style="margin:0;background:transparent">
<div style="position:relative;width:{w}px;height:{h}px;border-radius:{radius}px;overflow:hidden;{BG}{rimcss}">
<img src="{SVG}" style="position:absolute;width:{sym_w}px;left:{(w-sym_w)/2}px;top:{h*cy}px;transform:translateY(-50%);
 filter:drop-shadow(0 {w*0.012}px {w*0.02}px rgba(0,10,80,.55));">
</div></body></html>'''
VARS={
 'icone-pequeno-512.png': (512,512,int(512*0.74),int(512*0.2237),False),
 # nome: (w,h,largura do símbolo, raio, rim)
 'perfil-redes-1080.png': (1080,1080,int(1080*0.70),0,False),   # foto de perfil (corte em círculo): símbolo menor
 'icone-app-1080.png':    (1080,1080,int(1080*0.87),int(1080*0.2237),True),  # igual ao ícone da loja
 'perfil-quadrado-1080.png':(1080,1080,int(1080*0.82),0,False),  # quadrado cheio (onde não corta em círculo)
 'retangulo-1920x1080.png':(1920,1080,int(1080*0.95),0,False),
}
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome' if os.path.exists('/usr/bin/google-chrome') else None,args=['--no-sandbox','--force-color-profile=srgb'])
        for nome,(w,h,sw,r,rim) in VARS.items():
            pg=await b.new_page(viewport={'width':w,'height':h},device_scale_factor=2)
            await pg.set_content(html(w,h,sw,r,rim)); await pg.wait_for_timeout(300)
            await pg.screenshot(path='_tmp.png',omit_background=True,clip={'x':0,'y':0,'width':w,'height':h})
            from PIL import Image
            Image.open('_tmp.png').resize((w,h),Image.LANCZOS).save(nome)
            await pg.close()
        await b.close()
asyncio.run(main())
from PIL import Image, ImageDraw
# prévia: como fica no círculo do Insta/TikTok
im=Image.open('perfil-redes-1080.png').convert('RGBA').resize((360,360),Image.LANCZOS)
m=Image.new('L',(360,360),0); ImageDraw.Draw(m).ellipse([0,0,359,359],fill=255)
c=Image.new('RGBA',(360,360),(255,255,255,0)); c.paste(im,(0,0),m)
loja=Image.open('icone-app-1080.png').convert('RGBA').resize((360,360),Image.LANCZOS)
ret=Image.open('retangulo-1920x1080.png').convert('RGBA').resize((640,360),Image.LANCZOS)
s=Image.new('RGBA',(360*2+640+60,360),(30,30,30,255)); s.alpha_composite(c,(0,0)); s.alpha_composite(loja,(380,0)); s.alpha_composite(ret,(760,0))
s.convert('RGB').save('/tmp/previa-logo.jpg',quality=90)
os.remove('_tmp.png')
