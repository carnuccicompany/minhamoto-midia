"""Corrige a legenda queimada do pronto AP DD 4: "CURSOS" → "CUSTOS" (ela fala "prazos, custos e todo o resto…").
Janela 25,000–25,700 s do arquivo; amarelo até 25,433 s, branco depois. Fonte Anton 68 (mesma métrica da legenda original)."""
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
_fill = np.load("/home/claude/corretores/cursos_fill.npy")
X0, Y0, X1, Y1 = 330, 1355, 560, 1447
_mask = cv2.dilate(_fill.astype(np.uint8) * 255, np.ones((19, 19), np.uint8))
_F = ImageFont.truetype("/home/claude/corretores/fontes/anton.ttf", 68)
def custos_dd4(img, tf):
    if not (24.99 <= tf <= 25.715): return img
    a = np.array(img)
    reg = np.ascontiguousarray(a[Y0:Y1, X0:X1])
    a[Y0:Y1, X0:X1] = cv2.inpaint(reg, _mask, 6, cv2.INPAINT_TELEA)
    im = Image.fromarray(a)
    cor = (255, 236, 0) if tf < 25.45 else (255, 255, 255)
    lay = Image.new("RGBA", (400, 160), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((20, 10), "CUSTOS", font=_F, fill=cor, stroke_width=7, stroke_fill=(0, 0, 0))
    lay = lay.crop(lay.getbbox()).resize((547 - 343, 1438 - 1364), Image.LANCZOS)   # mesma caixa da palavra original
    im = im.convert("RGBA"); im.alpha_composite(lay, (343, 1364))
    return im.convert("RGB")
