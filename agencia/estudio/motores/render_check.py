#!/usr/bin/env python3
"""Render das peças estáticas com TRAVA DE LAYOUT (criada em 23/11 depois do CM01 v0).
Igual ao render() do direcao-v2/estaticos.py, mas antes do print mede no navegador:
  - sobreposição entre blocos de texto (título, apoio, CTA) e entre texto e card/celular;
  - quebra de linha: cada linha do título/apoio tem que caber em UMA linha (nada de palavra caindo pra linha de baixo);
  - texto fora do quadro / fora da zona segura 9:16 (x 140–940, y 150–1500) nas peças 1080x1920.
Qualquer problema = levanta erro (a peça não sai).
"""
import os
from PIL import Image
import estaticos as E

JS = r"""
() => {
  const out = {problemas: [], blocos: []};
  const txt = [...document.querySelectorAll('.titB,.apoB,.capA,.apoA,.desliza,.pag')];
  const vis = [...document.querySelectorAll('#phone, .uicard')];
  const R = el => { const r = el.getBoundingClientRect(); return {x0:r.left, y0:r.top, x1:r.right, y1:r.bottom}; };
  const cruza = (a, b) => Math.min(a.x1, b.x1) - Math.max(a.x0, b.x0) > 2 && Math.min(a.y1, b.y1) - Math.max(a.y0, b.y0) > 2;
  const nome = el => (el.className || el.id) + ' "' + (el.innerText || '').slice(0, 40).replace(/\n/g, ' / ') + '"';
  // linhas visuais de cada bloco vs. linhas pedidas (<br>)
  for (const el of txt) {
    const pedidas = (el.innerHTML.match(/<br\s*\/?>/gi) || []).length + 1;
    const range = document.createRange(); range.selectNodeContents(el);
    // agrupa as caixas por linha: nova linha só quando o topo desce mais que 60% do corpo da fonte
    const fs = parseFloat(getComputedStyle(el).fontSize);
    const ts = [...range.getClientRects()].filter(r => r.width > 1 && r.height > fs * 0.5).map(r => r.top).sort((a, b) => a - b);
    let linhas = 0, ult = -1e9;
    for (const t of ts) { if (t - ult > fs * 0.6) { linhas++; ult = t; } }
    if (linhas > pedidas) out.problemas.push('quebra de linha extra em ' + nome(el) + ` (${linhas} linhas, pedido ${pedidas})`);
    const r = R(el);
    if (r.x0 < 0 || r.x1 > innerWidth || r.y0 < 0 || r.y1 > innerHeight) out.problemas.push('fora do quadro: ' + nome(el));
    if (innerHeight === 1920 && !el.classList.contains('pag')) {
      // mede a caixa real do texto (não a div inteira)
      const rr = [...range.getClientRects()].filter(q => q.width > 1);
      for (const q of rr) if (q.left < 138 || q.right > 942 || q.top < 148 || q.bottom > 1502) { out.problemas.push('fora da zona segura 9:16: ' + nome(el)); break; }
    }
  }
  for (let i = 0; i < txt.length; i++) for (let j = i + 1; j < txt.length; j++)
    if (cruza(R(txt[i]), R(txt[j]))) out.problemas.push('texto sobre texto: ' + nome(txt[i]) + ' x ' + nome(txt[j]));
  for (const t of txt) for (const v of vis) {
    const range = document.createRange(); range.selectNodeContents(t);
    for (const q of [...range.getClientRects()].filter(q => q.width > 1))
      if (cruza({x0:q.left, y0:q.top, x1:q.right, y1:q.bottom}, R(v))) { out.problemas.push('texto sobre imagem: ' + nome(t)); break; }
  }
  return out;
}
"""

def render(html_corpo, w, h, saida):
    from playwright.sync_api import sync_playwright
    doc = E.BASE % dict(fontes=E.CSS_FONTES, phone=E.CSS_PHONE, w=w, h=h, corpo=html_corpo, azc=E.AZUL_CLARO, az=E.AZUL, aze=E.AZUL_ESC, lim=E.LIMAO)
    tmp = '/tmp/estudio_render.html'; open(tmp, 'w').write(doc)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--force-color-profile=srgb', '--allow-file-access-from-files'])
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2)
        pg.goto('file://' + tmp); pg.wait_for_timeout(700); pg.evaluate('document.fonts.ready')
        res = pg.evaluate(JS)
        pg.screenshot(path='/tmp/estudio_render@2x.png'); b.close()
    os.makedirs(os.path.dirname(saida), exist_ok=True)
    Image.open('/tmp/estudio_render@2x.png').convert('RGB').resize((w, h), Image.LANCZOS).save(saida, quality=93)
    if res['problemas']:
        print('TRAVA', saida); [print('   -', x) for x in res['problemas']]
        return False
    print('ok', saida); return True
