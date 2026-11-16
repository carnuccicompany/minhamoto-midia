#!/usr/bin/env python3
"""Stories 1080x1920 da agência MinhaMoto. Uso: python3 agencia/designer/stories.py
Gera stories/STnn.jpg, stories/pendentes.json e revisao/stories.jpg.
Zonas seguras: nada importante nos 250px de cima (barra do perfil) nem nos 340px de baixo (barra de resposta).
"""
import os, sys, json, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from video import CSS, fmt, A, REPO

EXTRA = """
.ph{position:absolute;border:4px dashed rgba(255,255,255,.55);border-radius:36px;display:flex;align-items:center;justify-content:center;
 color:rgba(255,255,255,.75);font-weight:800;font-size:34px;letter-spacing:3px;text-transform:uppercase;text-align:center}
.claro{background:#f3f1ec}
.claro .t{color:#0c0f14}
.claro .t .ac{background:#1f5fff;color:#fff;padding:0 .12em;border-radius:8px}
.claro .s{color:#3a3f48}
.claro .s .ac{color:#1f5fff}
.claro .k{background:#0c0f14}
"""

def phone(p, left, top, w):
    return (f"<div class='phone' style='left:{left}px;top:{top}px;width:{w}px'>"
            f"<img src='file://{os.path.join(A,'prints',p)}'></div>")

ST = [
 dict(id="ST01", tipo="Enquete", uso="Adicionar o sticker de ENQUETE no quadro tracejado. Opções: “Sei de cabeça” / “Nem faço ideia”. No dia seguinte, repostar o resultado.",
      html=lambda: "<div class='scene bg-dark' style='display:block'>"
      "<div class='box' style='top:330px'><div class='k' style='margin-bottom:40px'>Enquete</div>"
      f"<div class='t' style='font-size:104px'>{fmt('Você sabe quando foi a *última troca de óleo* da sua moto?')}</div>"
      f"<div class='s' style='font-size:46px;margin-top:36px'>{fmt('Sem olhar nota. Sem perguntar pro mecânico.')}</div></div>"
      "<div class='ph' style='left:140px;right:140px;top:1180px;height:300px'>Sticker de enquete aqui</div></div>"),
 dict(id="ST02", tipo="Você sabia", uso="Postar sozinho ou antes do ST03. Sem sticker; opcional: sticker de reação (emoji slider).",
      html=lambda: "<div class='scene claro' style='display:block'>"
      "<div class='box' style='top:330px'><div class='k' style='margin-bottom:40px'>Você sabia?</div>"
      f"<div class='t' style='font-size:112px'>{fmt('O óleo vence por km\n*e também por tempo.*')}</div>"
      f"<div class='s' style='font-size:50px;margin-top:40px'>{fmt('Moto parada também precisa de troca. O que chegar primeiro manda. Na dúvida, siga o *manual da sua moto.*')}</div></div>"
      f"<div class='t' style='position:absolute;right:70px;bottom:330px;font-size:420px;color:#1f5fff;letter-spacing:-14px'>?</div></div>"),
 dict(id="ST03", tipo="Bastidor / tela do app", uso="Pode ir com o sticker de LINK (link da bio) no rodapé, acima da barra de resposta.",
      html=lambda: "<div class='scene bg-dark' style='display:block'>"
      "<div class='box' style='top:290px'><div class='k' style='margin-bottom:34px'>Por dentro do app</div>"
      f"<div class='t' style='font-size:92px'>{fmt('É assim que o app mostra *o que vence* na sua moto.')}</div></div>"
      + phone('plano-atual.png', 250, 820, 580) + "</div>"),
 dict(id="ST04", tipo="Caixa de perguntas", uso="Adicionar o sticker de PERGUNTAS no quadro tracejado com o texto “Sua dúvida de manutenção”. Responder as melhores nos stories dos dias seguintes.",
      html=lambda: "<div class='scene bg-azul' style='display:block'>"
      "<div class='box' style='top:330px'><div class='k' style='margin-bottom:40px;background:#0c0f14'>Pergunta pra gente</div>"
      f"<div class='t' style='font-size:116px'>{fmt('Dúvida de manutenção? *Manda aqui.*')}</div>"
      f"<div class='s' style='font-size:50px;margin-top:40px;color:#e3ebff'>{fmt('Óleo, corrente, pneu, revisão. A gente responde as melhores nos stories.')}</div></div>"
      "<div class='ph' style='left:140px;right:140px;top:1180px;height:300px'>Sticker de perguntas aqui</div></div>"),
 dict(id="ST05", tipo="CTA de download", uso="Adicionar o sticker de LINK apontando pro link da bio (minhamotopagina.online), em cima do quadro tracejado.",
      html=lambda: "<div class='scene' style='display:block'>"
      f"<div class='photo' style=\"background-image:url('file://{os.path.join(A,'fotos','18596183.jpg')}')\"></div><div class='ov'></div>"
      f"<img src='file://{A}/icon.png' style='position:absolute;left:80px;top:300px;width:150px;border-radius:36px'>"
      "<div class='box' style='bottom:720px'>"
      f"<div class='t' style='font-size:118px'>{fmt('Sua moto *no controle.*')}</div>"
      f"<div class='s' style='font-size:50px;margin-top:30px'>{fmt('Manutenção, gastos e documentos num app só. *Baixe agora.*')}</div>"
      f"<div class='selos' style='margin-top:50px'><img src='file://{A}/selos-lojas.png'></div></div>"
      "<div class='ph' style='left:240px;right:240px;top:1360px;height:150px'>Sticker de link aqui</div></div>"),
]

def main():
    from playwright.sync_api import sync_playwright
    os.makedirs(os.path.join(REPO, 'stories'), exist_ok=True)
    with sync_playwright() as pw:
        args = ['--no-sandbox', '--force-color-profile=srgb']
        b = (pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=args)
             if os.path.exists('/usr/bin/google-chrome') else pw.chromium.launch(args=args))
        pg = b.new_page(viewport={'width': 1080, 'height': 1920})
        for s in ST:
            doc = (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}{EXTRA}</style></head><body>{s['html']()}"
                   "<script>document.fonts.ready.then(()=>document.body.dataset.ok=1)</script></body></html>")
            tmp = f"/tmp/{s['id']}.html"; open(tmp, 'w', encoding='utf-8').write(doc)
            pg.goto('file://' + tmp); pg.wait_for_selector('body[data-ok]'); pg.wait_for_timeout(200)
            pg.screenshot(path=os.path.join(REPO, 'stories', f"{s['id']}.jpg"), type='jpeg', quality=92)
        b.close()
    json.dump({'itens': [{'id': s['id'], 'tipo': s['tipo'], 'imagem': f"stories/{s['id']}.jpg", 'como_usar': s['uso']} for s in ST]},
              open(os.path.join(REPO, 'stories', 'pendentes.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    from PIL import Image
    w, h = 360, 640
    sheet = Image.new('RGB', (len(ST) * (w + 10) - 10, h), 'white')
    for i, s in enumerate(ST):
        sheet.paste(Image.open(os.path.join(REPO, 'stories', f"{s['id']}.jpg")).resize((w, h)), (i * (w + 10), 0))
    sheet.save(os.path.join(REPO, 'revisao', 'stories.jpg'), quality=85)
    print(len(ST), 'stories')

if __name__ == '__main__':
    main()
