import librosa, numpy as np, glob, os
A="/mnt/user-data/uploads/Corretores/Criativos prontos/ESTUDIO 23-11/_trabalho/aud/"
def feat(f):
    y,sr=librosa.load(f,sr=16000)
    m=librosa.feature.mfcc(y=y,sr=sr,n_mfcc=20,hop_length=160)[1:]
    m=(m-m.mean(1,keepdims=True))/(m.std(1,keepdims=True)+1e-6)
    return m, len(y)/sr
B=sorted(glob.glob(A+"B_*.wav")); D=sorted(glob.glob(A+"DD*.wav"))
FD={os.path.basename(d):feat(d)[0] for d in D}
for b in B:
    fb,dur=feat(b)
    # usa o miolo do bruto (onde tem fala) - janela de 3s com mais energia
    best=[]
    L=fb.shape[1]; w=min(300,L)
    seg=fb[:, (L-w)//2:(L-w)//2+w]
    for dn,fd in FD.items():
        if fd.shape[1]<w: continue
        sc=[]
        for o in range(0,fd.shape[1]-w,2):
            x=fd[:,o:o+w]; sc.append((x*seg).mean())
        k=int(np.argmax(sc)); best.append((sc[k],dn,(k*2)/100))
    best.sort(reverse=True)
    print(os.path.basename(b), f"{dur:.1f}s", [(round(s,2),n,o) for s,n,o in best[:3]])
