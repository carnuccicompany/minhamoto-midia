"""Gera versão 9:16 (1080x1920) dos carrosséis 4:5 pro TikTok.
O card inteiro fica visível na área segura (acima da legenda/botões); topo e base
são preenchidos com a cor da borda do próprio card (sem desfoque, sem corte)."""
import json, os, sys, numpy as np
from PIL import Image
W,H=1080,1920; TOP=150   # card 1080x1350 de y=150 a 1500; 420px livres embaixo pra legenda
def conv(src,dst):
    c=Image.open(src).convert('RGB')
    if c.size!=(1080,1350): c=c.resize((1080,1350),Image.LANCZOS)
    a=np.asarray(c).astype(np.float32)
    t=a[:6].mean(axis=(0,1)); b=a[-6:].mean(axis=(0,1))
    foto = a[:6].std(axis=(0,1)).mean()>12 or a[-6:].std(axis=(0,1)).mean()>12
    out=np.zeros((H,W,3),np.float32)
    if foto:   # card com foto: faixas escuras e a foto se dissolve nelas (degradê, sem desfoque)
        t=t*0.25; b=b*0.25
    out[:TOP]=t; out[TOP+1350:]=b
    out[TOP:TOP+1350]=a
    if foto:
        f=160; r=np.linspace(0,1,f)[:,None,None]**1.3
        out[TOP:TOP+f]=t*(1-r)+a[:f]*r
        out[TOP+1350-f:TOP+1350]=a[-f:]*r[::-1]+b*(1-r[::-1])
    Image.fromarray(out.clip(0,255).astype('uint8')).save(dst,quality=95)
if __name__=='__main__':
    f='fila/carrosseis.json'; d=json.load(open(f)); it=d if isinstance(d,list) else d['itens']
    n=0
    for x in it:
        if x.get('cards_tiktok'): continue
        outs=[]
        for c in x['cards']:
            dd=os.path.join(os.path.dirname(c),'tiktok'); os.makedirs(dd,exist_ok=True)
            o=os.path.join(dd,os.path.basename(c)); conv(c,o); outs.append(o)
        x['cards_tiktok']=outs; n+=1
    json.dump(d,open(f,'w'),ensure_ascii=False,indent=1)
    print('carrosseis convertidos:',n)
