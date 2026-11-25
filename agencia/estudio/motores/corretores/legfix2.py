"""Correção genérica de palavra errada na legenda queimada de um pronto (ex.: "CURSOS" → "CUSTOS").
Acha sozinha a caixa da palavra (pixels amarelos num quadro de referência), os quadros em que a palavra está na tela
e se ela está amarela ou branca; apaga com inpaint e redesenha na mesma caixa (Anton, contorno preto)."""
import subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
W, H = 1080, 1920
_F = ImageFont.truetype("/home/claude/corretores/fontes/anton.ttf", 68)
def _frames(src, ta, tb):
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{ta:.3f}", "-i", src, "-t", f"{tb - ta:.3f}", "-vf", "fps=30",
                        "-pix_fmt", "rgb24", "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(p, np.uint8).reshape(-1, H, W, 3)
def prepara(src, t_ref, nova, faixa_y=(1340, 1470), xmax_palavra=None):
    ref = _frames(src, t_ref, t_ref + 0.04)[0].astype(int)
    yel = (ref[..., 0] > 190) & (ref[..., 1] > 180) & (ref[..., 2] < 110)
    yel[:faixa_y[0]] = False; yel[faixa_y[1]:] = False
    ys, xs = np.where(yel)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    if xmax_palavra: x1 = min(x1, xmax_palavra)
    bx = (x0 - 20, y0 - 16, x1 + 20, y1 + 16)
    fill = yel[bx[1]:bx[3], bx[0]:bx[2]]
    mask = cv2.dilate(fill.astype(np.uint8) * 255, np.ones((19, 19), np.uint8))
    est = {}
    fr = _frames(src, t_ref - 1.5, t_ref + 1.5)
    for i, f in enumerate(fr):
        s = f[bx[1]:bx[3], bx[0]:bx[2]].astype(int)
        ye = ((s[..., 0] > 190) & (s[..., 1] > 180) & (s[..., 2] < 110))[fill].mean()
        wh = ((s[..., 0] > 225) & (s[..., 1] > 225) & (s[..., 2] > 225))[fill].mean()
        k = round((t_ref - 1.5) * 30) + i
        if ye > 0.9: est[k] = "y"
        elif wh > 0.85: est[k] = "w"
    return dict(bx=bx, mask=mask, est=est, tinta=(x0 - 7, y0 - 7, x1 + 7, y1 + 7), nova=nova)
def aplica(cfg, img, tf):
    k = round(tf * 30)
    if k not in cfg["est"]: return img
    a = np.array(img); X0, Y0, X1, Y1 = cfg["bx"]
    reg = np.ascontiguousarray(a[Y0:Y1, X0:X1]); a[Y0:Y1, X0:X1] = cv2.inpaint(reg, cfg["mask"], 6, cv2.INPAINT_TELEA)
    im = Image.fromarray(a)
    cor = (255, 236, 0) if cfg["est"][k] == "y" else (255, 255, 255)
    lay = Image.new("RGBA", (500, 180), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((20, 10), cfg["nova"], font=_F, fill=cor, stroke_width=7, stroke_fill=(0, 0, 0))
    tx0, ty0, tx1, ty1 = cfg["tinta"]
    lay = lay.crop(lay.getbbox()).resize((tx1 - tx0, ty1 - ty0), Image.LANCZOS)
    im = im.convert("RGBA"); im.alpha_composite(lay, (tx0, ty0)); return im.convert("RGB")
