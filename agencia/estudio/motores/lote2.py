#!/usr/bin/env python3
"""LOTE 2 (26/11) · 10 carrosséis do MinhaMoto pra fábrica (CM07–CM16).
Régua: DESIGN-MINHAMOTO.md (constituição + regras de 26/11): app só como tela REAL da 1.0.2 dentro do celular, ícone
discreto, sem preço, foto real do mundo do público (estética das capas do acervo: foto grande + título forte), metade
motoboy / metade rolê, temas dica · humor · mito × verdade · app.
Uso: python3 lote2.py [CM07 CM08 ...]  (sem argumento = todos)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import lote1_base as B
from lote1_base import *

B.PECAS = os.path.join(REPO, 'agencia', 'estudio', 'pecas', 'LOTE2')
TELAS = 'v1.0.2/'
from fontTools.ttLib import TTFont as _TT
_FN = {}
def _larg(txt, peso, tam):
    """largura em px do texto na Plus Jakarta Sans (lida do woff2, sem chute)."""
    if peso not in _FN:
        f = _TT(os.path.join(REPO, 'agencia', 'direcao-v2', 'fontes', f'plus-jakarta-sans-latin-{peso}-normal.woff2'))
        _FN[peso] = (f.getBestCmap(), f['hmtx'], f['head'].unitsPerEm)
    cmap, hm, upm = _FN[peso]
    return sum(hm[cmap.get(ord(ch), cmap.get(32))][0] for ch in txt) * tam / upm

def cabe(linhas, tam, w, peso=800):
    """diminui o corpo do título até a linha mais larga caber na largura (letter-spacing -0.035em)."""
    import re as _re
    lim = lambda l: _larg(_re.sub(r'</?b>', '', l), peso, tam)
    while tam > 40 and max(lim(l) for l in linhas) > w * .95: tam -= 2
    return tam

def quebra(txt, tam, w, peso=500):
    """parte o texto em linhas que cabem na largura (margem de 4%), sem deixar palavra sozinha na última linha."""
    if isinstance(txt, list): return txt
    pal = txt.split(); linhas = []; cur = ''
    for p in pal:
        t = (cur + ' ' + p).strip()
        if _larg(t, peso, tam) <= w * .96: cur = t
        else: linhas.append(cur); cur = p
    linhas.append(cur)
    if len(linhas) > 1 and len(linhas[-1].split()) == 1:
        a = linhas[-2].split(); linhas[-2] = ' '.join(a[:-1]); linhas[-1] = a[-1] + ' ' + linhas[-1]
    return linhas
     # telas reais do visual novo (capturadas do código da 1.0.2)

def _f(fid, nome, **kw):
    kw.setdefault('satura', .8); kw.setdefault('frio', .06)
    return foto_prep(fid, nome='l2_' + nome, **kw)

def M(tt):   # margem e largura
    return (140, 800) if tt else (90, 900)

# ---------- moldes ----------
def capa(tt, fid, linhas, sub, pos='50% 50%', nome=None, azul_de=None, tam=None, crop=None):
    """Capa do acervo: foto em tela cheia, título grande centralizado no terço de baixo, apoio e 'Deslize'."""
    arq = _f(fid, (nome or fid) + ('_tt' if tt else ''), crop=crop, escurece=.95)
    c = foto_fundo(arq, pos=pos, degr='escuro', forca=.92, topo=.25)
    L, w = M(tt)
    tam = cabe(linhas, tam or (100 if not tt else 92), w)
    n = len(linhas)
    base = 1110 if not tt else 1500
    ys = base - alt_titulo(n, tam) - 110
    c += titulo(linhas, L, ys, tam, w=w, alinha='center', azul_de=azul_de if azul_de is not None else n - 1)
    c += apoio(quebra(sub, 42 if not tt else 40, w, 600), L, base - 76, 42 if not tt else 40, w=w, alinha='center', cor='#F4F7FC', peso='j600')
    c += desliza(0, base + 20 if not tt else base + 40, tt, alinha='center').replace("left:0px;right:auto", "left:0px;right:0;width:1080px")
    return c

def foto_texto(n, N, tt, fid, kick, linhas, apo, pos='50% 50%', nome=None, crop=None, azul_de=None, tam=None):
    """Card escuro: texto em cima, foto real na metade de baixo sumindo pro fundo."""
    L, w = M(tt)
    arq = _f(fid, (nome or fid) + '_b', crop=crop, escurece=.9)
    c = fundo('escuro', (50, 10))
    c += foto_base(arq, 620 if not tt else 980, pos=pos, altura=1350 if not tt else 1920)
    y = 140 if not tt else 300
    if kick: c += kicker(kick, L, y, 'escuro', w=w); y += 70
    tam = tam or (92 if not tt else 84)
    tam = cabe(linhas, tam, w)
    c += titulo(linhas, L, y, tam, w=w, azul_de=azul_de if azul_de is not None else len(linhas) - 1)
    c += apoio(quebra(apo, 40, w), L, y + alt_titulo(len(linhas), tam) + 30, 40, w=w, cor='#F4F7FC')
    return c + pag(n, N, tt)

def numero(n, N, tt, num, linhas, apo, fid, pos='50% 50%', nome=None, crop=None):
    """Item de lista: número grande azul + título + apoio; foto real embaixo."""
    L, w = M(tt)
    arq = _f(fid, (nome or fid) + '_n', crop=crop, escurece=.9)
    c = fundo('escuro', (50, 10))
    c += foto_base(arq, 640 if not tt else 1000, pos=pos, altura=1350 if not tt else 1920)
    y = 120 if not tt else 280
    c += (f"<div class=titB style='left:{L}px;right:auto;width:300px;top:{y}px;font-size:{200 if not tt else 190}px;"
          f"line-height:1;letter-spacing:-.05em;color:{AZUL_CLARO}'>{num}</div>")
    yt = y + (230 if not tt else 220)
    tam = 90 if not tt else 82
    tam = cabe(linhas, tam, w)
    c += titulo(linhas, L, yt, tam, w=w, azul_de=None)
    c += apoio(quebra(apo, 40, w), L, yt + alt_titulo(len(linhas), tam) + 28, 40, w=w, cor='#F4F7FC')
    return c + pag(n, N, tt)

def mito(n, N, tt, txt_mito, real, apo, fid, pos='50% 50%', nome=None, crop=None):
    """Mito × verdade (fundo claro): mito riscado em cinza, 'A real' em pílula azul, título grande, foto real embaixo."""
    L, w = M(tt)
    arq = _f(fid, (nome or fid) + '_m', crop=crop)
    c = fundo('claro', (50, 10))
    c += foto_base(arq, 860 if not tt else 1220, pos=pos, altura=1350 if not tt else 1920)
    y = 130 if not tt else 300
    c += pilula('Mito', NAVY_TXT, '#FFFFFF', L, y, tam=30)
    tm = 50 if not tt else 46
    c += (f"<div class=titB style='left:{L}px;right:auto;width:{w}px;top:{y + 78}px;font-size:{tm}px;line-height:1.15;"
          f"color:rgba(10,26,51,.45);text-decoration:line-through;text-decoration-thickness:4px'>{H.escape(txt_mito)}</div>")
    yr = y + 78 + (2 * round(tm * 1.15)) + 60
    c += pilula('A real', AZUL, '#FFFFFF', L, yr, tam=30)
    tam = 88 if not tt else 80
    tam = cabe(real, tam, w)
    c += titulo(real, L, yr + 78, tam, w=w, azul_de=len(real) - 1)
    c += apoio(quebra(apo, 38, w), L, yr + 78 + alt_titulo(len(real), tam) + 26, 38, w=w, cor='rgba(10,26,51,.72)')
    return '<!--claro-->' + c + pag(n, N, tt)

def humor(n, N, tt, kick, linhas, apo, fid, pos='50% 50%', nome=None, crop=None):
    """Humor/identificação: foto real em tela cheia, frase grande em cima com degradê escuro no topo."""
    L, w = M(tt)
    arq = _f(fid, (nome or fid) + '_h' + ('_tt' if tt else ''), crop=crop, escurece=.95)
    c = foto_fundo(arq, pos=pos, degr='escuro_topo', forca=.9, topo=.35)
    y = 130 if not tt else 300
    c += kicker(kick, L, y, 'escuro', w=w)
    tam = 92 if not tt else 84
    tam = cabe(linhas, tam, w)
    c += titulo(linhas, L, y + 70, tam, w=w, azul_de=len(linhas) - 1)
    c += apoio(quebra(apo, 40, w, 600), L, y + 70 + alt_titulo(len(linhas), tam) + 28, 40, w=w, cor='#F4F7FC', peso='j600')
    return c + pag(n, N, tt)

def app(n, N, tt, linhas, apo, tela, rola=None, tema='escuro'):
    """O app só como tela REAL inteira dentro do celular (visual 1.0.2)."""
    L, w = M(tt)
    c = fundo(tema, (50, 70))
    ty = 300 if tt else 100
    tam = 78 if not tt else 66
    tam = cabe(linhas, tam, w)
    c += titulo(linhas, L, ty, tam, w=w, azul_de=len(linhas) - 1)
    ya = ty + alt_titulo(len(linhas), tam) + 24
    c += apoio(quebra(apo, 40 if not tt else 36, w), L, ya, 40 if not tt else 36, w=w, cor='#F4F7FC' if tema == 'escuro' else None)
    nome = TELAS + tela + ('' if tela.endswith('.png') or rola is not None else '.png')
    if rola is not None: nome = TELAS + 'rolagem/' + tela
    c += fone(nome, 660 if tt else 600, 540, ya + (130 if tt else 100), rola=rola)
    return c + pag(n, N, tt)

def fim_app(tt, l1, l2, sub):
    return final_app(tt, 'escuro', l1, l2, sub, preco=False)  # final_app já é centralizado com largura cheia

def fim_salve(tt, linhas, sub, kick='Salve este post'):
    L, w = M(tt)
    return final_salva(tt, 'escuro', kick, linhas, len(linhas) - 1, sub, tam=cabe(linhas, 76 if tt else 84, w))

# ---------- as 10 peças ----------
def CM07(tt):   # dica · motoboy · final app
    N = 6
    return [capa(tt, '7362948', ['Rodando 150 km por dia,', 'em 20 dias são', '3.000 km.'], 'Seu óleo conta km, não dias.', pos='50% 40%'),
            foto_texto(2, N, tt, '29473917', 'O manual', ['A troca é por km', 'ou por tempo.'], ['O que chegar primeiro.', 'Pra quem trabalha, quase sempre é o km.']),
            numero(3, N, tt, '1 mês', ['Quem roda muito', 'perde a conta.'], 'Num mês puxado, a moto anda o que outra anda em meio ano.', '7200709', pos='50% 60%'),
            foto_texto(4, N, tt, '32076422', 'Sinal de alerta', ['Óleo escuro e', 'motor mais áspero?'], 'Passou da hora. Não espere a luz do óleo acender.', pos='50% 45%'),
            app(5, N, tt, ['O app faz a conta', 'pelo seu ritmo.'], 'Você informa o km, ele mostra quando o óleo vence.', 'manutencao'),
            fim_app(tt, 'Você roda.', 'O MinhaMoto conta.', 'Baixe agora e nunca mais perca a troca.')]

def CM08(tt):   # humor · rolê · final salve
    N = 7
    return [capa(tt, '32076454', ['Todo posto tem', 'esses 5 tipos', 'de motociclista.'], 'Você é qual?', pos='50% 50%'),
            humor(2, N, tt, 'Tipo nº 1', ['O que calibra', 'o pneu no olho.'], '“Tá bom, tá bom.” Nunca tá.', '25857998', pos='50% 60%'),
            humor(3, N, tt, 'Tipo nº 2', ['O que limpa a moto', 'mais que a casa.'], 'Brilha por fora. E o óleo? Ninguém sabe.', '6872570', pos='50% 50%'),
            humor(4, N, tt, 'Tipo nº 3', ['O que põe R$ 10', 'e sai rezando.'], 'Até o próximo posto, se Deus quiser.', '32076422', pos='50% 50%'),
            humor(5, N, tt, 'Tipo nº 4', ['O que pergunta', 'pro frentista', 'qual óleo usar.'], 'O manual tava debaixo do banco.', '29473917', pos='50% 50%'),
            humor(6, N, tt, 'Tipo nº 5', ['O que sabe o km', 'de cada troca.'], 'Esse aqui usa o MinhaMoto.', '31664515', pos='50% 55%'),
            fim_salve(tt, ['Marque o amigo', 'que é o tipo nº 1.'], 'Todo grupo tem um.')]

def CM09(tt):   # mito × verdade · misto · final salve
    N = 6
    return [capa(tt, '5803314', ['3 coisas que', 'todo mundo fala', 'e estão erradas.'], 'A nº 2 quase todo mundo faz.', pos='50% 50%'),
            mito(2, N, tt, 'Calibrar com o pneu quente dá na mesma.', ['Calibre sempre', 'com o pneu frio.'], 'Quente, a pressão sobe e o número engana.', '25857998', pos='50% 55%'),
            mito(3, N, tt, 'Corrente bem esticada é mais segura.', ['Esticada demais', 'come coroa e pinhão.'], 'A folga certa está no manual da sua moto.', '37131862-corrente', pos='50% 50%'),
            mito(4, N, tt, 'A luz do óleo apagou, então tá tudo bem.', ['Confira o nível', 'antes de rodar.'], 'Luz que acende e apaga é aviso, não alívio.', '6664916', pos='50% 50%'),
            app(5, N, tt, ['O certo da sua moto', 'tá no app.'], 'Calibragem, óleo e corrente do seu modelo.', 'lista-revisao'),
            fim_salve(tt, ['Mande pro amigo', 'que ainda acredita', 'na nº 2.'], 'Ele vai agradecer depois.')]

def CM10(tt):   # app (combustível) · motoboy · final app
    N = 6
    return [capa(tt, '32076422', ['Quanto a sua moto', 'bebeu este mês?'], 'Quem trabalha de moto precisa saber.', pos='50% 45%'),
            foto_texto(2, N, tt, '7363198', 'Todo dia', ['Gasolina pesa', 'no bolso de quem', 'roda o dia todo.'], 'E quase ninguém anota quanto gastou.', pos='50% 50%'),
            foto_texto(3, N, tt, '37131862-corrente', 'Fica a dica', ['Consumo caiu?', 'A moto tá pedindo', 'manutenção.'], 'Pneu murcho, corrente seca e filtro sujo fazem a moto beber mais.', pos='50% 50%'),
            app(4, N, tt, ['Registre cada', 'abastecimento.'], 'O app calcula seu consumo médio.', 'combustivel'),
            app(5, N, tt, ['Veja quanto gastou', 'no mês.'], 'E compare os postos que você usa.', 'combustivel-resumo'),
            fim_app(tt, 'Cada real conta.', 'O MinhaMoto conta pra você.', 'Baixe agora e controle seu gasto.')]

def CM11(tt):   # dica · rolê · final salve
    N = 7
    return [capa(tt, '35721171', ['Rolê no domingo?', '10 minutos antes', 'salvam a viagem.'], '5 checagens na garagem.', pos='50% 50%'),
            numero(2, N, tt, '1', ['Pneu'], 'Calibre com o pneu frio e confira se o sulco está acima da marca de desgaste.', '25857998', pos='50% 60%'),
            numero(3, N, tt, '2', ['Óleo'], 'Com a moto em pé, o nível tem que estar entre o mínimo e o máximo.', '29473917', pos='50% 50%'),
            numero(4, N, tt, '3', ['Corrente'], 'Folga certa e lubrificada. Seca, ela estica e gasta o kit.', '37131862-corrente', pos='50% 50%'),
            numero(5, N, tt, '4', ['Freios'], 'Manete e pedal firmes. Chiado de metal é pastilha no fim.', '19949302', pos='50% 45%'),
            numero(6, N, tt, '5', ['Luzes'], 'Farol, lanterna, setas e luz de freio funcionando.', '4686570', pos='50% 50%'),
            fim_salve(tt, ['Salve e confira', 'antes do próximo rolê.'], 'Mande pro parceiro de estrada.')]

def CM12(tt):   # humor · motoboy · final app
    N = 7
    return [capa(tt, '7363198', ['Coisas que só', 'quem trabalha de moto', 'entende.'], 'A nº 4 dói no bolso.', pos='50% 45%', tam=92),
            humor(2, N, tt, 'nº 1', ['A chuva começa', 'na hora que você sai.'], 'Nem um minuto antes.', '31408946', pos='50% 60%'),
            humor(3, N, tt, 'nº 2', ['A corrida é sempre', 'do outro lado', 'da cidade.'], 'E o cliente mora no último bloco.', '7200709', pos='50% 60%'),
            humor(4, N, tt, 'nº 3', ['A moto inventa', 'um barulho novo', 'toda segunda.'], 'E ele some quando chega na oficina.', '32645708', pos='50% 55%'),
            humor(5, N, tt, 'nº 4', ['Moto parada', 'é dia sem ganhar.'], 'Por isso manutenção não pode virar surpresa.', '36909490', pos='50% 55%'),
            app(6, N, tt, ['O app avisa', 'antes de quebrar.'], 'Você trabalha. Ele cuida das datas e dos km.', 'saude'),
            fim_app(tt, 'Moto parada', 'não paga conta.', 'Baixe agora o MinhaMoto.')]

def CM13(tt):   # mito · rolê · final app
    N = 6
    return [capa(tt, '30817486', ['Moto parada', 'não estraga?'], 'Estraga sim. E em silêncio.', pos='50% 55%'),
            foto_texto(2, N, tt, '30817487', 'Bateria', ['Parada, a bateria', 'descarrega sozinha.'], 'Algumas semanas sem rodar e ela pode não pegar.', pos='50% 55%'),
            foto_texto(3, N, tt, '29713609', 'Pneu', ['O pneu perde', 'pressão parado.'], 'E força sempre o mesmo ponto no chão.', pos='50% 50%'),
            foto_texto(4, N, tt, '29473917', 'Óleo e gasolina', ['Eles também', 'envelhecem.'], 'Por isso o manual tem prazo, não só km.', pos='50% 50%'),
            app(5, N, tt, ['Por tempo', 'também conta.'], 'O app lembra mesmo se a moto quase não rodar.', 'manutencao-tempo'),
            fim_app(tt, 'Rodando ou parada,', 'o MinhaMoto lembra.', 'Baixe agora e cuide da sua moto.')]

def CM14(tt):   # app (saúde) · misto · final app
    N = 6
    return [capa(tt, '31664515', ['Sua moto tá', 'quantos % em dia?'], 'Dá pra saber em 1 segundo.', pos='50% 50%'),
            foto_texto(2, N, tt, '3822784', 'Manutenção', ['Moto em dia', 'não é chute.'], 'É óleo, corrente, freio, pneu e vela, cada um no seu km.', pos='50% 40%'),
            app(3, N, tt, ['O app mostra', 'num número só.'], 'Saúde da moto: quanto da manutenção está em dia.', 'saude'),
            app(4, N, tt, ['E mostra o que', 'pede atenção.'], 'Sistema por sistema, do motor aos freios.', 'saude', rola='saude-sistemas'),
            app(5, N, tt, ['Fez o serviço?', 'Registre e pronto.'], 'Data, km e o que foi feito, tudo no histórico.', 'historico'),
            fim_app(tt, 'Moto em dia', 'agora tem número.', 'Baixe agora o MinhaMoto.')]

def CM15(tt):   # dica · motoboy · final salve
    N = 6
    return [capa(tt, '19949302', ['3 sinais de que', 'a pastilha de freio', 'acabou.'], 'O 3º é o mais perigoso.', pos='50% 50%', tam=94),
            numero(2, N, tt, '1', ['Chiado de metal', 'na freada.'], 'É o aviso de desgaste ou o metal raspando no disco.', '19949302', pos='30% 60%', nome='19949302b', crop=None),
            numero(3, N, tt, '2', ['Manete ou pedal', 'mais fundo.'], 'Você precisa apertar mais pra frear igual.', '14700339', pos='50% 50%'),
            numero(4, N, tt, '3', ['A moto demora', 'mais pra parar.'], 'No trânsito, esse metro a mais é o acidente.', '31408946', pos='50% 60%'),
            foto_texto(5, N, tt, '8550664', 'E tem mais', ['Pastilha no fim', 'risca o disco.'], 'Aí a troca barata vira troca de disco.', pos='50% 45%'),
            fim_salve(tt, ['Salve e confira', 'seu freio hoje.'], 'Mande pro parceiro que vive no corredor.')]

def CM16(tt):   # app (ficha) · rolê · final app
    N = 6
    return [capa(tt, '8354256', ['Você sabe a', 'calibragem certa', 'da sua moto?'], 'E o óleo? E a corrente?', pos='50% 60%'),
            foto_texto(2, N, tt, '7681334', 'O manual', ['Tá tudo no manual.', 'Que ninguém acha.'], 'Ou ficou na gaveta da concessionária.', pos='50% 50%'),
            app(3, N, tt, ['A ficha da sua moto', 'no bolso.'], 'Motor, potência e o que o manual diz.', 'moto'),
            app(4, N, tt, ['Óleo, pneu, corrente:', 'o certo do seu modelo.'], 'Sem procurar em fórum.', 'lista-revisao'),
            app(5, N, tt, ['Conheça cada', 'parte da moto.'], 'Do motor ao freio, explicado.', 'conheca-moto'),
            fim_app(tt, 'O manual inteiro', 'no seu celular.', 'Baixe agora o MinhaMoto.')]

PECAS2 = {k: v for k, v in globals().items() if k.startswith('CM') and callable(v)}

if __name__ == '__main__':
    ids = sys.argv[1:] or sorted(PECAS2)
    ok = True
    for k in ids:
        f = PECAS2[k]
        tem = lambda c: ('claro' if c.startswith('<!--claro-->') else 'escuro', c)
        r = render_lista(k, [tem(c) for c in f(False)], [tem(c) for c in f(True)])
        folha(k, k); print(k, 'ok' if r else 'FALHOU'); ok &= r
    sys.exit(0 if ok else 1)
