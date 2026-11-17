#!/usr/bin/env python3
"""Amostras de vídeo da direção v2 (A = Nativo/Rua, B = Premium produto)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motor import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)))

def A1():
    v = Video('A1', 'A')
    v.cena(0, 2.9, bg_foto('3822836.jpg', 1.06, 1.2, (40, -20), escurece=0.55)(2.9))
    v.texto(0, 2.9, T_cap('POV: o mecânico / pergunta quando / foi a última troca', ['mecânico', 'última', 'troca'], y=660, tam=88, inst=True))
    v.cena(2.9, 6.0, bg_foto('27704018.jpg', 1.18, 1.04, (0, 0), escurece=0.7)(3.1))
    v.texto(2.9, 6.0, T_cap('E você: / “uns 3 meses… / ou 6? Sei lá.”', ['Sei', 'lá.”'], y=640, tam=104, ritmo=0.2))
    FB = lambda d: bg_foto('3822836.jpg', 1.25, 1.32, (0, 0), escurece=0.32, blur=16)(d)
    PH = dict(w=640, y=380, fundo='A', rot=(0, 0), tilt=(0, 0), esc=(0.86, 1.0), push=0.05)
    v.cena(6.0, 9.6, celular('22-registrar-servico', 3.6, bgfn=FB(3.6), **PH))
    v.texto(6.0, 9.6, T_cap('No MinhaMoto nada / fica no “sei lá”', ['MinhaMoto', '“sei', 'lá”'], y=180, tam=76, ritmo=0.17))
    v.cena(9.6, 12.8, celular('rolagem/19-saude-atrasados', 3.2, rola=(0, 3480), bgfn=FB(3.2), **PH))
    v.texto(9.6, 12.8, T_cap('O que venceu / fica em vermelho', ['venceu', 'vermelho'], y=180, tam=76, ritmo=0.17))
    v.cena(12.8, 15.8, bg_grad('A'))
    v.texto(12.8, 15.8, T_cta('Nunca mais<br><span class=hl>“sei lá”</span>', sub='Baixe o MinhaMoto', preco='por R$19,90', estilo='A'))
    return v

def A2():
    v = Video('A2', 'A')
    v.cena(0, 2.8, bg_foto('5195494.jpg', 1.04, 1.16, (0, 0), escurece=0.6)(2.8))
    v.texto(0, 2.8, T_cap('Sua moto / tá em dia? / Prove.', ['Prove.'], y=600, tam=124, inst=True))
    FB = lambda d: bg_foto('5195494.jpg', 1.2, 1.28, (0, 0), escurece=0.3, blur=16)(d)
    PH = dict(w=640, y=380, fundo='A', rot=(0, 0), tilt=(0, 0), esc=(0.86, 1.0), push=0.05)
    v.cena(2.8, 6.2, celular('02-saude', 3.4, bgfn=FB(3.4), **PH))
    v.texto(2.8, 6.2, T_cap('O app mostra a / saúde da sua moto', ['saúde'], y=180, tam=76, ritmo=0.17))
    v.cena(6.2, 9.6, celular('15-notificacoes', 3.4, bgfn=FB(3.4), **PH))
    v.texto(6.2, 9.6, T_cap('E te avisa / antes de vencer', ['avisa'], y=180, tam=76, ritmo=0.17))
    v.cena(9.6, 13.0, celular('rolagem/02-saude', 3.4, rola=(4300, 5250), bgfn=FB(3.4), **PH))
    v.texto(9.6, 13.0, T_cap('Quanto falta pra / próxima revisão', ['falta'], y=180, tam=76, ritmo=0.17))
    v.cena(13.0, 16.0, bg_grad('A'))
    v.texto(13.0, 16.0, T_cta('Em dia.<br><span class=hl>Sem chute.</span>', sub='Baixe agora o MinhaMoto', estilo='A'))
    return v

def B1():
    v = Video('B1', 'B')
    PH = dict(w=700, y=340)
    v.cena(0, 3.2, celular('21-item-atrasado', 3.2, rot=(-10, 0), tilt=(5, 0), esc=(0.94, 1.0), **PH))
    v.texto(0, 3.2, T_tit(['Esqueceu a troca?', 'A moto não esquece.'], y=180, tam=76, hl_linhas=(1,), entra=-1))
    v.cena(3.2, 6.8, celular('rolagem/19-saude-atrasados', 3.6, rola=(0, 3480), rot=(8, 0), tilt=(3, 0), **PH))
    v.texto(3.2, 6.8, T_tit(['O que venceu', 'fica em vermelho'], y=180, tam=76, hl_linhas=(1,)))
    v.cena(6.8, 10.4, celular('rolagem/19-saude-atrasados', 3.6, rola=(3480, 4600), rot=(-8, 0), tilt=(3, 0), **PH))
    v.texto(6.8, 10.4, T_tit(['O que nunca foi feito', 'ele te mostra'], y=180, tam=76, hl_linhas=(1,)))
    v.cena(10.4, 13.6, celular('15-notificacoes', 3.2, rot=(8, 0), tilt=(3, 0), **PH))
    v.texto(10.4, 13.6, T_tit(['E te avisa', 'na hora certa'], y=180, tam=76, hl_linhas=(1,)))
    v.cena(13.6, 16.6, bg_grad('B'))
    v.texto(13.6, 16.6, T_cta('Baixe o<br><span class=hl>MinhaMoto</span>', sub='O app que cuida da sua moto.', preco='por R$19,90', estilo='B'))
    return v

def B2():
    v = Video('B2', 'B')
    PH = dict(w=700, y=340)
    v.cena(0, 3.4, celular('01-garagem', 3.4, rot=(-10, 0), tilt=(5, 0), esc=(0.94, 1.0), **PH))
    v.texto(0, 3.4, T_tit(['Sua moto tá em dia?', 'Veja em 30 segundos'], y=180, tam=76, hl_linhas=(1,), entra=-1))
    v.cena(3.4, 7.0, celular('23-registrar-servico-itens', 3.6, rot=(8, 0), tilt=(3, 0), **PH))
    v.texto(3.4, 7.0, T_tit(['Responda', 'o que você lembra'], y=180, tam=76, hl_linhas=(1,)))
    v.cena(7.0, 10.6, celular('rolagem/10-lista-revisao', 3.6, rola=(0, 1500), rot=(-8, 0), tilt=(3, 0), **PH))
    v.texto(7.0, 10.6, T_tit(['E veja o plano', 'da sua moto'], y=180, tam=76, hl_linhas=(1,)))
    v.cena(10.6, 13.8, celular('03-manutencao', 3.2, rot=(8, 0), tilt=(3, 0), **PH))
    v.texto(10.6, 13.8, T_tit(['No seu modelo.', 'No seu km.'], y=180, tam=76, hl_linhas=(1,)))
    v.cena(13.8, 16.8, bg_grad('B'))
    v.texto(13.8, 16.8, T_cta('Baixe o<br><span class=hl>MinhaMoto</span>', sub='Seu plano de revisão na palma da mão.', estilo='B'))
    return v

VIDEOS = dict(A1=A1, A2=A2, B1=B1, B2=B2)

if __name__ == '__main__':
    vid = sys.argv[1]; modo = sys.argv[2] if len(sys.argv) > 2 else 'full'
    v = VIDEOS[vid]()
    pasta = os.path.join(OUT, vid[0], vid)
    if modo == 'prev':
        d = v.render(None, so_frames=[int(x*FPS) for x in [0.05, 1.5, 3.5, 5.5, 7.5, 9, 11, 12.5, 14, 15.8]])
        from PIL import Image
        fs = sorted(f for f in os.listdir(d) if f.endswith('.jpg'))
        from PIL import ImageDraw
        ims = []
        for f in fs:
            im = Image.open(os.path.join(d, f)).convert('RGB'); dr = ImageDraw.Draw(im)
            dr.line([(0, 150), (1080, 150)], fill=(255, 0, 0), width=4); dr.line([(0, 1500), (1080, 1500)], fill=(255, 0, 0), width=4)
            dr.line([(940, 0), (940, 1920)], fill=(255, 0, 0), width=4)
            ims.append(im.resize((360, 640)))
        s = Image.new('RGB', (360*5, 640*2)); [s.paste(im, ((k % 5)*360, (k//5)*640)) for k, im in enumerate(ims)]
        s.save(f'/tmp/v2/prev_{vid}.jpg', quality=82); print('prev ok')
    else:
        os.makedirs(pasta, exist_ok=True)
        v.render(os.path.join(pasta, 'video.mp4')); print('render ok', pasta)
