#!/usr/bin/env python3
"""Amostras de vídeo da direção v2 (A = Nativo/Rua, B = Premium produto)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motor import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)))

def A1():
    v = Video('A1', 'A')
    v.cena(0, 2.9, bg_foto('3822836.jpg', 1.06, 1.2, (40, -20), escurece=0.55)(2.9))
    v.texto(0, 2.9, T_cap('POV: O MECÂNICO PERGUNTA QUANDO FOI A ÚLTIMA TROCA', ['MECÂNICO', 'ÚLTIMA', 'TROCA'], y=620, tam=104, inst=True))
    v.cena(2.9, 6.0, bg_foto('27704018.jpg', 1.18, 1.04, (0, 0), escurece=0.7)(3.1))
    v.texto(2.9, 6.0, T_cap('E VOCÊ: “UNS 3 MESES… OU 6? SEI LÁ.”', ['SEI', 'LÁ.”'], y=660, tam=112, ritmo=0.2))
    FB = lambda d: bg_foto('3822836.jpg', 1.25, 1.32, (0, 0), escurece=0.32, blur=16)(d)
    PH = dict(w=640, y=380, fundo='A', rot=(0, 0), tilt=(0, 0), esc=(0.86, 1.0), push=0.05)
    v.cena(6.0, 9.6, celular('tela-cadastro-moto.mp4', 100, 3.6, bgfn=FB(3.6), **PH))
    v.texto(6.0, 9.6, T_cap('NO MINHAMOTO NADA FICA NO “SEI LÁ”', ['MINHAMOTO', '“SEI', 'LÁ”'], y=190, tam=92, ritmo=0.17))
    v.cena(9.6, 12.8, celular('tela-saude-1.mp4', 10.5, 3.2, bgfn=FB(3.2), **PH))
    v.texto(9.6, 12.8, T_cap('O QUE VENCEU FICA EM VERMELHO', ['VENCEU', 'VERMELHO'], y=210, tam=96, ritmo=0.17))
    v.cena(12.8, 15.8, bg_grad('A'))
    v.texto(12.8, 15.8, T_cta('NUNCA MAIS<br>“SEI LÁ”', sub='Baixe o MinhaMoto', preco='por R$19,90', estilo='A'))
    return v

def A2():
    v = Video('A2', 'A')
    v.cena(0, 2.8, bg_foto('5195494.jpg', 1.04, 1.16, (0, 0), escurece=0.6)(2.8))
    v.texto(0, 2.8, T_cap('TUA MOTO TÁ EM DIA? PROVA.', ['PROVA.'], y=640, tam=132, inst=True))
    FB = lambda d: bg_foto('5195494.jpg', 1.2, 1.28, (0, 0), escurece=0.3, blur=16)(d)
    PH = dict(w=640, y=380, fundo='A', rot=(0, 0), tilt=(0, 0), esc=(0.86, 1.0), push=0.05)
    v.cena(2.8, 6.2, celular('tela-saude-1.mp4', 0, 3.4, bgfn=FB(3.4), **PH))
    v.texto(2.8, 6.2, T_cap('O APP MOSTRA A SAÚDE DA TUA MOTO', ['SAÚDE'], y=200, tam=96, ritmo=0.17))
    v.cena(6.2, 9.6, celular('tela-notificacoes.mp4', 67.6, 3.4, bgfn=FB(3.4), **PH))
    v.texto(6.2, 9.6, T_cap('E TE AVISA ANTES DE VENCER', ['AVISA'], y=210, tam=104, ritmo=0.17))
    v.cena(9.6, 13.0, celular('tela-manutencao.mp4', 43.5, 3.4, bgfn=FB(3.4), **PH))
    v.texto(9.6, 13.0, T_cap('QUANTOS KM FALTAM PRA PRÓXIMA REVISÃO', ['KM', 'FALTAM'], y=190, tam=90, ritmo=0.17))
    v.cena(13.0, 16.0, bg_grad('A'))
    v.texto(13.0, 16.0, T_cta('TUA MOTO EM DIA.<br>SEM CHUTE.', sub='Baixe agora o MinhaMoto', estilo='A'))
    return v

def B1():
    v = Video('B1', 'B')
    PH = dict(w=700, y=340)
    v.cena(0, 3.2, celular('tela-saude-1.mp4', 0, 3.2, rot=(-16, -6), tilt=(8, 3), esc=(0.97, 1.0), **PH))
    v.texto(0, 3.2, T_tit(['ESQUECEU A TROCA?', 'A MOTO NÃO ESQUECE.'], y=150, tam=104, largura=1000, hl_linhas=(1,), entra=-1))
    v.cena(3.2, 6.8, celular('tela-saude-1.mp4', 10.2, 3.6, rot=(12, 4), tilt=(4, 2), **PH))
    v.texto(3.2, 6.8, T_tit(['O QUE VENCEU', 'FICA EM VERMELHO'], y=170, tam=118, hl_linhas=(1,)))
    v.cena(6.8, 10.4, celular('tela-cadastro-moto.mp4', 100, 3.6, rot=(-12, -4), tilt=(4, 2), **PH))
    v.texto(6.8, 10.4, T_tit(['O QUE NUNCA FOI FEITO', 'ELE TE MOSTRA'], y=160, tam=104, largura=1000, hl_linhas=(1,)))
    v.cena(10.4, 13.6, celular('tela-notificacoes.mp4', 67.6, 3.2, rot=(10, 0), tilt=(4, 0), **PH))
    v.texto(10.4, 13.6, T_tit(['E TE AVISA', 'NA HORA CERTA'], y=170, tam=124, hl_linhas=(1,)))
    v.cena(13.6, 16.6, bg_grad('B'))
    v.texto(13.6, 16.6, T_cta('BAIXE O<br>MINHAMOTO', sub='O app que cuida da tua moto.', preco='por R$19,90', estilo='B'))
    return v

def B2():
    v = Video('B2', 'B')
    PH = dict(w=700, y=340)
    v.cena(0, 3.4, celular('tela-cadastro-moto.mp4', 2.4, 3.4, rot=(-16, -6), tilt=(8, 3), esc=(0.97, 1.0), **PH))
    v.texto(0, 3.4, T_tit(['30 SEGUNDOS', 'PRA SABER SE TUA MOTO', 'TÁ EM DIA'], y=110, tam=96, largura=1000, hl_linhas=(0,), entra=-1))
    v.cena(3.4, 7.0, celular('tela-cadastro-moto.mp4', 6, 3.6, speed=15, rot=(12, 4), tilt=(4, 2), **PH))
    v.texto(3.4, 7.0, T_tit(['RESPONDE', 'O QUE VOCÊ LEMBRA'], y=170, tam=118, hl_linhas=(1,)))
    v.cena(7.0, 10.6, celular('tela-cadastro-moto.mp4', 113, 3.6, rot=(-12, -4), tilt=(4, 2), **PH))
    v.texto(7.0, 10.6, T_tit(['E VÊ O PLANO', 'DA TUA MOTO'], y=170, tam=124, hl_linhas=(1,)))
    v.cena(10.6, 13.8, celular('tela-manutencao.mp4', 43.5, 3.2, rot=(10, 0), tilt=(4, 0), **PH))
    v.texto(10.6, 13.8, T_tit(['NO TEU MODELO.', 'NO TEU KM.'], y=170, tam=124, hl_linhas=(1,)))
    v.cena(13.8, 16.8, bg_grad('B'))
    v.texto(13.8, 16.8, T_cta('BAIXE O<br>MINHAMOTO', sub='Teu plano de revisão na palma da mão.', estilo='B'))
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
        ims = [Image.open(os.path.join(d, f)).resize((360, 640)) for f in fs]
        s = Image.new('RGB', (360*5, 640*2)); [s.paste(im, ((k % 5)*360, (k//5)*640)) for k, im in enumerate(ims)]
        s.save(f'/tmp/v2/prev_{vid}.jpg', quality=82); print('prev ok')
    else:
        os.makedirs(pasta, exist_ok=True)
        v.render(os.path.join(pasta, 'video.mp4')); print('render ok', pasta)
