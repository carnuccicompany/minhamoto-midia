"""Folha de miniaturas: python3 folha.py [saida] [pasta]"""
import glob, sys, os
from PIL import Image, ImageDraw, ImageFont
out = sys.argv[1] if len(sys.argv) > 1 else '/tmp/telas-reais/_folha.jpg'
pasta = sys.argv[2] if len(sys.argv) > 2 else '/tmp/telas-reais'
fs = sorted(glob.glob(pasta + '/[0-9]*.png'))
cols, w = 6, 300; h = int(w * 2556 / 1179); lab = 34
rows = (len(fs) + cols - 1) // cols
sh = Image.new('RGB', (cols * w + (cols + 1) * 16, rows * (h + lab + 16) + 16), (235, 235, 235)); d = ImageDraw.Draw(sh)
try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
except Exception: f = None
for i, p in enumerate(fs):
    x = 16 + (i % cols) * (w + 16); y = 16 + (i // cols) * (h + lab + 16)
    im = Image.open(p).convert('RGB').resize((w, h), Image.LANCZOS)
    d.text((x, y + 6), os.path.basename(p)[:-4], fill=(20, 20, 20), font=f); sh.paste(im, (x, y + lab))
sh.save(out, quality=88); print(out, sh.size, len(fs))
