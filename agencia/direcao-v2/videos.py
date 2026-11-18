#!/usr/bin/env python3
"""Amostras de vídeo da direção v2 (A = Nativo/Rua, B = Premium produto)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motor import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)))

# Régua: agencia/DESIGN-MINHAMOTO.md. Mesmo mockup e mesma entrada (meio de lado -> centro -> zoomzinho) em todas as cenas.
PH = dict(w=630, y=215, rot=(-12, 0), tilt=(5, 0), esc=(0.93, 1.0), push=0.035, entra=0.9)

def A1():
    v = Video('A1', 'A')
    v.cena(0, 2.8, bg_foto('3822836.jpg', 1.06, 1.18, (40, -20), escurece=0.55)(2.8))
    v.texto(0, 2.8, T_cap('Você lembra quando / trocou o óleo / pela última vez?', ['óleo'], y=640, tam=92, inst=True))
    v.cena(2.8, 5.6, bg_foto('27704018.jpg', 1.16, 1.04, (0, 0), escurece=0.62)(2.8))
    v.texto(2.8, 5.6, T_cap('Se a resposta é / “acho que…”, / o motor / paga a conta.', ['motor', 'conta.'], y=560, tam=88, ritmo=0.17))
    FB = lambda d: bg_foto('3822836.jpg', 1.25, 1.32, (0, 0), escurece=0.32, blur=16)(d)
    v.cena(5.6, 9.4, celular('rolagem/06-historico', 3.8, rola=(0, 1500), bgfn=FB(3.8), **PH))
    v.texto(5.6, 9.4, T_cap('Cada serviço salvo, / com data e km.', ['salvo,'], y=165, tam=64, ritmo=0.15))
    v.cena(9.4, 13.2, celular('rolagem/02-saude', 3.8, rola=(0, 1350), bgfn=FB(3.8), **PH))
    v.texto(9.4, 13.2, T_cap('A saúde da sua moto / em um só lugar.', ['saúde'], y=165, tam=64, ritmo=0.15))
    v.cena(13.2, 16.2, celular('15-notificacoes', 3.0, bgfn=FB(3.0), tap=dict(l='50%', tp='24%', t=1.3), **PH))
    v.texto(13.2, 16.2, T_cap('E o aviso chega / antes do prazo.', ['antes'], y=165, tam=64, ritmo=0.15))
    v.cena(16.2, 19.6, bg_grad('A'))
    v.texto(16.2, 19.6, T_cta('Sua moto.<br><span class=hl>Sob controle.</span>', sub='Baixe agora o MinhaMoto.', preco='por R$19,90', estilo='A'))
    return v

def A2():
    v = Video('A2', 'A')
    v.cena(0, 2.8, bg_foto('5195494.jpg', 1.04, 1.16, (0, 0), escurece=0.58)(2.8))
    v.texto(0, 2.8, T_cap('Manutenção esquecida / custa caro.', ['caro.'], y=680, tam=104, inst=True))
    FB = lambda d: bg_foto('5195494.jpg', 1.2, 1.28, (0, 0), escurece=0.3, blur=16)(d)
    v.cena(2.8, 6.6, celular('rolagem/02-saude', 3.8, rola=(0, 1350), bgfn=FB(3.8), **PH))
    v.texto(2.8, 6.6, T_cap('O que está em dia. / O que pede atenção.', ['em', 'dia.', 'atenção.'], y=165, tam=64, ritmo=0.14))
    v.cena(6.6, 10.4, celular('rolagem/09-resumo-mes', 3.8, rola=(0, 1100), bgfn=FB(3.8), **PH))
    v.texto(6.6, 10.4, T_cap('Cada gasto anotado. / Cada km contado.', ['gasto', 'km'], y=165, tam=64, ritmo=0.15))
    v.cena(10.4, 13.8, celular('rolagem/02-saude', 3.4, rola=(4300, 5350), bgfn=FB(3.4), **PH))
    v.texto(10.4, 13.8, T_cap('O próximo marco, / sempre à vista.', ['marco,'], y=165, tam=64, ritmo=0.15))
    v.cena(13.8, 17.2, bg_grad('A'))
    v.texto(13.8, 17.2, T_cta('Sua moto em dia,<br><span class=hl>sem esforço.</span>', sub='Baixe agora o MinhaMoto.', preco='por R$19,90', estilo='A'))
    return v

def B1():
    v = Video('B1', 'B')
    v.cena(0, 3.2, celular('02-saude', 3.2, **PH))
    v.texto(0, 3.2, T_tit(['Esqueceu a troca?', 'A moto não esquece.'], y=170, tam=72, hl_linhas=(1,), entra=-1))
    v.cena(3.2, 7.0, celular('rolagem/02-saude', 3.8, rola=(0, 3700), **PH))
    v.texto(3.2, 7.0, T_tit(['Tudo o que vence', 'aparece primeiro.'], y=170, tam=72, hl_linhas=(1,)))
    v.cena(7.0, 10.8, celular('rolagem/06-historico', 3.8, rola=(0, 1500), tap=dict(l='40%', tp='30%', t=0.9), **PH))
    v.texto(7.0, 10.8, T_tit(['O histórico completo,', 'sempre com você.'], y=170, tam=72, hl_linhas=(1,)))
    v.cena(10.8, 14.0, celular('15-notificacoes', 3.2, tap=dict(l='50%', tp='24%', t=1.2), **PH))
    v.texto(10.8, 14.0, T_tit(['E o aviso chega', 'na hora certa.'], y=170, tam=72, hl_linhas=(1,)))
    v.cena(14.0, 17.4, bg_grad('B'))
    v.texto(14.0, 17.4, T_cta('Controle total<br><span class=hl>da sua moto.</span>', sub='Na palma da mão.', preco='por R$19,90', estilo='B'))
    return v

def B2():
    v = Video('B2', 'B')
    v.cena(0, 3.4, celular('01-garagem', 3.4, **PH))
    v.texto(0, 3.4, T_tit(['Sua moto tá em dia?', 'Veja em 30 segundos'], y=170, tam=72, hl_linhas=(1,), entra=-1))
    v.cena(3.4, 7.2, celular('rolagem/02-saude', 3.8, rola=(1700, 2750), tap=dict(l='50%', tp='64%', t=2.75), **PH))
    v.texto(3.4, 7.2, T_tit(['Responda', 'o que você lembra'], y=170, tam=72, hl_linhas=(1,)))
    v.cena(7.2, 11.0, celular('rolagem/10-lista-revisao', 3.8, rola=(0, 1500), **PH))
    v.texto(7.2, 11.0, T_tit(['E veja o plano', 'da sua moto'], y=170, tam=72, hl_linhas=(1,)))
    v.cena(11.0, 14.2, celular('rolagem/02-saude', 3.2, rola=(4250, 5350), **PH))
    v.texto(11.0, 14.2, T_tit(['No seu modelo.', 'No seu km.'], y=170, tam=72, hl_linhas=(1,)))
    v.cena(14.2, 17.6, bg_grad('B'))
    v.texto(14.2, 17.6, T_cta('Baixe o<br><span class=hl>MinhaMoto</span>', sub='Seu plano de revisão na palma da mão.', preco='por R$19,90', estilo='B'))
    return v

VIDEOS = dict(A1=A1, A2=A2, B1=B1, B2=B2)

if __name__ == '__main__':
    vid = sys.argv[1]; modo = sys.argv[2] if len(sys.argv) > 2 else 'full'
    v = VIDEOS[vid]()
    pasta = os.path.join(OUT, vid[0], vid)
    if modo == 'prev':
        d = v.render(None, so_frames=[int(x*FPS) for x in [0.05, 1.5, 3.5, 5.0, 6.2, 8.5, 11, 13.0, 15, 16.0, 17.0, 19.0]])
        from PIL import Image
        fs = sorted(f for f in os.listdir(d) if f.endswith('.jpg'))
        from PIL import ImageDraw
        ims = []
        for f in fs:
            im = Image.open(os.path.join(d, f)).convert('RGB'); dr = ImageDraw.Draw(im)
            dr.line([(0, 150), (1080, 150)], fill=(255, 0, 0), width=4); dr.line([(0, 1500), (1080, 1500)], fill=(255, 0, 0), width=4)
            dr.line([(940, 0), (940, 1920)], fill=(255, 0, 0), width=4)
            ims.append(im.resize((360, 640)))
        s = Image.new('RGB', (360*6, 640*2)); [s.paste(im, ((k % 6)*360, (k//6)*640)) for k, im in enumerate(ims)]
        s.save(f'/tmp/v2/prev_{vid}.jpg', quality=82); print('prev ok')
    else:
        os.makedirs(pasta, exist_ok=True)
        v.render(os.path.join(pasta, 'video.mp4')); print('render ok', pasta)
