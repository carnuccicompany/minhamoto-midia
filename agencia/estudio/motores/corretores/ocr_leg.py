import sys, subprocess, os, re, json, glob
from PIL import Image, ImageOps
import pytesseract
def ocr_video(path, fps=5):
    d = '/tmp/ocrfr_'+str(os.getpid()); subprocess.run(['rm','-rf',d]); os.makedirs(d)
    subprocess.run(['ffmpeg','-loglevel','error','-i',path,'-vf',f'fps={fps},crop=iw:ih*0.11:0:ih*0.665','-q:v','2',f'{d}/%05d.jpg'],check=True)
    out=[]; prev=None
    for i,f in enumerate(sorted(glob.glob(d+'/*.jpg'))):
        im=Image.open(f).convert('L'); im=im.resize((im.width*3,im.height*3))
        # legenda: branco/amarelo com contorno escuro -> threshold
        bw=im.point(lambda p:255 if p>200 else 0); bw=ImageOps.invert(bw)
        t=pytesseract.image_to_string(bw,lang='por',config='--psm 7').strip()
        t=re.sub(r'[^A-ZÁÉÍÓÚÂÊÔÃÕÇÀ0-9+%$,\.\?! ]','',t.upper()).strip()
        t=re.sub(r'\s+',' ',t)
        if len(t)<2: t=''
        if t!=prev:
            out.append([round(i/fps,1),t]); prev=t
    return out
res={}
for p in sys.argv[1:]:
    r=ocr_video(p); res[os.path.basename(p)]=r
    print('==',os.path.basename(p))
    print(' | '.join(f"{a}:{b}" for a,b in r if b))
json.dump(res,open('legendas_ocr.json','w'),ensure_ascii=False,indent=0)
