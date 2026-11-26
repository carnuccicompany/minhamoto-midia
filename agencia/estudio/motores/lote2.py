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
B.IOS = 'v1.0.2'   # visual novo oficial (1.0.2); telas antigas são material proibido
TELAS = 'v1.0.2/'
ROLA_TEMPO = 1500   # rolagem/03-manutencao: lista "Por tempo" (conferir)
ROLA_SIST = 3330    # rolagem/02-saude: começa em "Cuidados" (os sistemas aparecem com 0% na semente, não mostrar)
from fontTools.ttLib import TTFont as _TT
_FN = {}
def _larg(txt, peso, tam, ls=0.0):
    """largura em px na POPPINS (a fonte que renderiza: j500/j600/j800), lida do woff2, com o letter-spacing (em)."""
    if peso not in _FN:
        f = _TT(os.path.join(REPO, 'agencia', 'direcao-v2', 'fontes', f'poppins-latin-{peso}-normal.woff2'))
        _FN[peso] = (f.getBestCmap(), f['hmtx'], f['head'].unitsPerEm)
    cmap, hm, upm = _FN[peso]
    return sum(hm[cmap.get(ord(ch), cmap.get(32))][0] for ch in txt) * tam / upm + ls * tam * len(txt)

def cabe(linhas, tam, w, peso=800):
    """diminui o corpo do título até a linha mais larga caber (letter-spacing -0.035em; margem 3%)."""
    import re as _re
    lim = lambda l: _larg(_re.sub(r'</?b>', '', l), peso, tam, -.035)
    while tam > 40 and max(lim(l) for l in linhas) > w * .97: tam -= 2
    return tam

FRACAS = set('o a os as um uma uns umas de do da dos das no na nos nas em ao aos à às pra pro pras pros por pelo pela e ou que com se não seu sua seus suas é mais'.split())
def quebra(txt, tam, w, peso=500):
    """parte o texto em linhas equilibradas que cabem na largura; linha nunca termina em artigo/preposição/conjunção
    (erro 20) e a última nunca fica com 1 palavra só."""
    if isinstance(txt, list): return [l for x in txt for l in quebra(x, tam, w, peso)]
    pal = [p for p in txt.split(' ') if p]; n = len(pal); lim = w * .96   # '\u00a0' (NB) segura duas palavras juntas
    L = lambda i, j: _larg(' '.join(pal[i:j]), peso, tam, -.005)
    if L(0, n) <= lim: return [txt]
    INF = float('inf'); best = [INF] * (n + 1); prv = [0] * (n + 1); best[0] = 0
    for j in range(1, n + 1):
        for i in range(j):
            lw = L(i, j)
            if lw > lim: continue
            if j < n and pal[j - 1].lower().strip(',.:;') in FRACAS: continue
            if j == n and j - i == 1 and n > 1: continue
            c = best[i] + (lim - lw) ** 2 + 1e5
            if c < best[j]: best[j] = c; prv[j] = i
    if best[n] == INF:   # sem solução com as regras: cai pro guloso
        out, cur = [], ''
        for p in pal:
            t = (cur + ' ' + p).strip(' ')
            if _larg(t, peso, tam) <= lim: cur = t
            else: out.append(cur); cur = p
        return out + [cur]
    out, j = [], n
    while j > 0: i = prv[j]; out.append(' '.join(pal[i:j])); j = i
    return out[::-1]
     # telas reais do visual novo (capturadas do código da 1.0.2)

# marcas e placas legíveis saem borradas; cortes fixos por foto (erro 14 da lista)
BORRA = {'6674515': [(880, 320, 1140, 480)], '33915710': [(1060, 700, 1360, 1020), (1040, 1000, 1360, 1700), (760, 340, 1010, 520)], '29713609': [(470, 770, 870, 990)], '10622201': [(60, 1450, 240, 1690), (620, 690, 780, 770)],
         '12680555': [(550, 770, 790, 890), (370, 1140, 710, 1240)]}
CORTA = {'25857998': (0, 560, 1350, 1800)}
def _f(fid, nome, **kw):
    kw.setdefault('satura', .8); kw.setdefault('frio', .06)
    if fid in BORRA: kw.setdefault('borrar', BORRA[fid])
    if fid in CORTA and not kw.get('crop'): kw['crop'] = CORTA[fid]
    return foto_prep(fid, nome='l2_' + nome, **kw)

def M(tt):   # margem e largura
    return (140, 800) if tt else (90, 900)

# ---------- moldes ----------
# tema: 'azul' (fundo azul do app), 'preto' (preto com destaque limão), 'claro' (branco com destaque azul)
PRETO_BG = ("<div class=fill style='background:#05070B'></div>"
            "<div class=fill style='background:radial-gradient(60% 40% at 50% 0%, rgba(198,255,0,.07), rgba(0,0,0,0) 70%)'></div>")
TEMA = 'azul'
def bg(tema, luz=(50, 10)):
    if tema == 'preto': return PRETO_BG
    if tema == 'claro' and luz[1] < 50:   # claro limpo: o brilho radial no topo parecia mancha
        return CSS_CLARO + "<div class=fill style='background:linear-gradient(180deg,#FFFFFF 0%,#F4F7FC 60%,#E9F0FA 100%)'></div>"
    return fundo('claro' if tema == 'claro' else 'escuro', luz)

def foto_sob(arq, yfim, tt, pos, tema, minimo):
    """foto real embaixo começando logo depois do texto (nada de meio card vazio); no claro a transição é curta pra não lavar a foto."""
    alt = 1350 if not tt else 1920
    top = max(minimo - 120, yfim - 30)
    top = min(top, alt - 420)
    return foto_base(arq, top, pos=pos, altura=alt, fade=.30 if tema == 'claro' else .40)

def fim_apoio(linhas, y, tam): return y + len(linhas) * round(tam * 1.34)
def marca(tema, c):
    """marca o card pro render (classe de cor) e troca o destaque pra limão no fundo preto."""
    if tema == 'preto':
        c = c.replace("<span class=b>", f"<span class=b style='color:{LIMAO}'>")
    return ('<!--claro-->' if tema == 'claro' else '') + c
def txt(tema): return '#F4F7FC' if tema != 'claro' else 'rgba(10,26,51,.75)'
def kt(tema): return 'claro' if tema == 'claro' else 'escuro'

def capa(tt, fid, linhas, sub, pos='50% 50%', nome=None, azul_de=None, tam=None, crop=None, acento=None):
    """Capa do acervo: foto em tela cheia, título grande centralizado no terço de baixo, apoio e 'Deslize'."""
    arq = _f(fid, (nome or fid) + ('_tt' if tt else ''), crop=crop, escurece=.95)
    c = foto_fundo(arq, pos=pos, degr='escuro', forca=.92, topo=.25)
    L, w = M(tt)
    tam = cabe(linhas, tam or (100 if not tt else 88), w)
    n = len(linhas)
    base = 1110 if not tt else 1380
    ys = base - alt_titulo(n, tam) - 110
    c += titulo(linhas, L, ys, tam, w=w, alinha='center', azul_de=azul_de if azul_de is not None else n - 1)
    ts = 42 if not tt else 40; ls = quebra(sub, ts, w, 600)
    c += apoio(ls, L, base - 76, ts, w=w, alinha='center', cor='#F4F7FC', peso='j600')
    c += desliza(0, base + 20 + (len(ls) - 1) * round(ts * 1.38), tt, alinha='center').replace("left:0px;right:auto", "left:0px;right:0;width:1080px")
    return marca('preto' if (acento == 'limao' or TEMA == 'preto') else 'azul', c)

def capa_clara(tt, fid, linhas, sub, pos='50% 50%', nome=None, tam=None):
    """Capa das peças de tema claro (erro 23): fundo claro, título grande em cima, foto real embaixo."""
    L, w = M(tt)
    arq = _f(fid, (nome or fid) + '_cc', escurece=1.0)
    y = 150 if not tt else 330
    tam = cabe(linhas, tam or (104 if not tt else 92), w)
    t = titulo(linhas, L, y, tam, w=w, azul_de=len(linhas) - 1)
    ys = y + alt_titulo(len(linhas), tam) + 30
    ts = 42 if not tt else 40; ls = quebra(sub, ts, w, 600)
    t += apoio(ls, L, ys, ts, w=w, cor=txt('claro'), peso='j600')
    yd = fim_apoio(ls, ys, ts) + 24
    t += desliza(L, yd, tt).replace("class=desliza style='", "class=desliza style='color:#0A1A33;text-shadow:none;")
    c = bg('claro') + foto_sob(arq, yd + 90, tt, pos, 'claro', 0) + t
    return marca('claro', c)

def foto_texto(n, N, tt, fid, kick, linhas, apo, pos='50% 50%', nome=None, crop=None, azul_de=None, tam=None, tema=None):
    tema = tema or TEMA
    """Texto em cima, foto real na metade de baixo sumindo pro fundo."""
    L, w = M(tt)
    arq = _f(fid, (nome or fid) + '_b', crop=crop, escurece=.9 if tema != 'claro' else 1.0)
    y = 140 if not tt else 300
    t = ''
    if kick: t += kicker(kick, L, y, kt(tema), w=w); y += 70
    tam = cabe(linhas, tam or (92 if not tt else 84), w)
    t += titulo(linhas, L, y, tam, w=w, azul_de=azul_de if azul_de is not None else len(linhas) - 1)
    la = quebra(apo, 40, w); ya = y + alt_titulo(len(linhas), tam) + 30
    t += apoio(la, L, ya, 40, w=w, cor=txt(tema))
    c = bg(tema) + foto_sob(arq, fim_apoio(la, ya, 40), tt, pos, tema, 560 if not tt else 900) + t
    return marca(tema, c + pag(n, N, tt))

def numero(n, N, tt, num, linhas, apo, fid, pos='50% 50%', nome=None, crop=None, tema=None):
    tema = tema or TEMA
    """Item de lista: número grande + título + apoio; foto real embaixo."""
    L, w = M(tt)
    arq = _f(fid, (nome or fid) + '_n', crop=crop, escurece=.9 if tema != 'claro' else 1.0)
    c = ''
    y = 120 if not tt else 280
    corn = LIMAO if tema == 'preto' else (AZUL if tema == 'claro' else AZUL_CLARO)
    c += (f"<div class=titB style='left:{L}px;right:auto;width:600px;text-align:left;top:{y}px;font-size:{200 if not tt else 190}px;"
          f"line-height:1;letter-spacing:-.05em;color:{corn}'>{num}</div>")
    yt = y + (230 if not tt else 220)
    tam = cabe(linhas, 90 if not tt else 82, w)
    c += titulo(linhas, L, yt, tam, w=w, azul_de=None)
    la = quebra(apo, 40, w); ya = yt + alt_titulo(len(linhas), tam) + 28
    c += apoio(la, L, ya, 40, w=w, cor=txt(tema))
    c = bg(tema) + foto_sob(arq, fim_apoio(la, ya, 40), tt, pos, tema, 540 if not tt else 880) + c
    return marca(tema, c + pag(n, N, tt))

def mito(n, N, tt, txt_mito, real, apo, fid, pos='50% 50%', nome=None, crop=None, tema='claro'):
    """Mito × verdade: mito riscado, 'A real' em pílula, título grande, foto real embaixo."""
    L, w = M(tt)
    arq = _f(fid, (nome or fid) + '_m', crop=crop)
    c = ''
    y = 130 if not tt else 300
    claro = tema == 'claro'
    c += pilula('Mito', NAVY_TXT if claro else '#FFFFFF', '#FFFFFF' if claro else NAVY_TXT, L, y, tam=30)
    tm = 50 if not tt else 46
    lm = quebra(txt_mito, tm, w, 800)
    c += (f"<div class=titB style='left:{L}px;right:auto;width:{w}px;text-align:left;top:{y + 78}px;font-size:{tm}px;line-height:1.15;"
          f"color:{'rgba(10,26,51,.42)' if claro else 'rgba(255,255,255,.45)'};text-decoration:line-through;text-decoration-thickness:4px'>{'<br>'.join(H.escape(x) for x in lm)}</div>")
    yr = y + 78 + len(lm) * round(tm * 1.15) + 60
    c += pilula('A real', AZUL if tema != 'preto' else LIMAO, '#FFFFFF' if tema != 'preto' else NAVY_TXT, L, yr, tam=30)
    tam = cabe(real, 88 if not tt else 80, w)
    c += titulo(real, L, yr + 78, tam, w=w, azul_de=len(real) - 1)
    la = quebra(apo, 38, w); ya = yr + 78 + alt_titulo(len(real), tam) + 26
    c += apoio(la, L, ya, 38, w=w, cor=txt(tema))
    c = bg(tema) + foto_sob(arq, fim_apoio(la, ya, 38), tt, pos, tema, 700 if not tt else 1000) + c
    return marca(tema, c + pag(n, N, tt))

def humor(n, N, tt, kick, linhas, apo, fid, pos='50% 50%', nome=None, crop=None, acento=None):
    """Humor/identificação: foto real em tela cheia, frase grande em cima com degradê escuro no topo."""
    L, w = M(tt)
    arq = _f(fid, (nome or fid) + '_h' + ('_tt' if tt else ''), crop=crop, escurece=.95)
    c = foto_fundo(arq, pos=pos, degr='escuro_topo', forca=.9, topo=.35)
    y = 130 if not tt else 300
    c += kicker(kick, L, y, 'escuro', w=w)
    tam = cabe(linhas, 92 if not tt else 84, w)
    c += titulo(linhas, L, y + 70, tam, w=w, azul_de=len(linhas) - 1)
    c += apoio(quebra(apo, 40, w, 600), L, y + 70 + alt_titulo(len(linhas), tam) + 28, 40, w=w, cor='#F4F7FC', peso='j600')
    return marca('preto' if (acento == 'limao' or TEMA == 'preto') else 'azul', c + pag(n, N, tt))

def app(n, N, tt, linhas, apo, tela, rola=None, tema=None):
    tema = tema or TEMA
    """O app só como tela REAL inteira dentro do celular (visual 1.0.2)."""
    L, w = M(tt)
    c = bg(tema, (50, 70))
    ty = 300 if tt else 100
    tam = cabe(linhas, 78 if not tt else 66, w)
    c += titulo(linhas, L, ty, tam, w=w, azul_de=len(linhas) - 1)
    ya = ty + alt_titulo(len(linhas), tam) + 24
    ta = 40 if not tt else 36
    la = quebra(apo, ta, w)
    c += apoio(la, L, ya, ta, w=w, cor=txt(tema))
    ya += (len(la) - 1) * round(ta * 1.38)
    nome = TELAS + ('rolagem/' if rola is not None else '') + tela + ('' if tela.endswith('.png') else '.png')
    c += fone(nome, 660 if tt else 600, 540, ya + (130 if tt else 100), rola=rola)
    return marca(tema, c + pag(n, N, tt))

def fim_app(tt, l1, l2, sub, tema=None):
    tema = tema or TEMA
    c = final_app(tt, 'claro' if tema == 'claro' else 'escuro', l1, l2, sub, preco=False)
    if tema == 'preto': c = PRETO_BG + c[len(fundo('escuro', (50, 30))):]
    return marca(tema, c)

def fim_salve(tt, linhas, sub, kick, tema=None):
    """Final 'salve/mande': conjunto centralizado na altura do card (erro 21: nada de metade de baixo vazia);
    kicker diz a AÇÃO (não repete o título)."""
    tema = tema or TEMA
    L, w = M(tt)
    te = 'claro' if tema == 'claro' else 'escuro'
    tam = cabe(linhas, 100 if not tt else 86, w)
    ts = 42 if not tt else 40; ls = quebra(sub, ts, w)
    alt = 150 + 72 + 66 + alt_titulo(len(linhas), tam) + 40 + len(ls) * round(ts * 1.34)
    top_z, fim_z = (0, 1130) if not tt else (300, 1340)
    T = top_z + (fim_z - top_z - alt) // 2
    cor = AZUL_CLARO if te == 'escuro' else AZUL
    if tema == 'preto': cor = LIMAO
    caixa = ("background:linear-gradient(160deg,#121a2a,#05080f);box-shadow:inset 0 0 0 2px rgba(255,255,255,.07),0 24px 50px rgba(0,0,0,.45)"
             if te == 'escuro' else "background:#fff;box-shadow:0 0 0 2px rgba(10,26,51,.06),0 24px 50px rgba(10,26,51,.14)")
    ics = ''.join(f"<div style='display:inline-flex;width:150px;height:150px;border-radius:42px;{caixa};align-items:center;justify-content:center;margin-right:28px'>"
                  f"{icone(n, 78, cor, 7)}</div>" for n in ('salvar', 'enviar'))
    c = bg(tema, (30, 30)) if tema != 'claro' else bg('claro')
    c += f"<div style='position:absolute;left:{L}px;top:{T}px'>{ics}</div>"
    y = T + 150 + 72
    c += kicker(kick, L, y, kt(tema), w=w)
    c += titulo(linhas, L, y + 66, tam, w=w, azul_de=len(linhas) - 1)
    c += apoio(ls, L, y + 66 + alt_titulo(len(linhas), tam) + 40, ts, w=w, cor=txt(tema))
    c += assinatura(1440 if tt else 1200, te, left=L)
    return marca(tema, c)

# ---------- as 10 peças ----------
def CM07(tt):
    global TEMA; TEMA = 'preto'   # dica · motoboy · final app
    N = 6
    return [capa(tt, '17024710', ['Rodando 150 km por dia,', 'em 20 dias são', '3.000 km.'], 'Seu óleo conta km, não dias.', pos='55% 50%'),
            foto_texto(2, N, tt, '6674515', 'O manual', ['A troca é por km', 'ou por tempo.'], 'O que chegar primeiro. Pra quem trabalha, quase sempre é o km.', pos='50% 50%'),
            foto_texto(3, N, tt, '36909490', 'Na prática', ['Quem roda muito', 'perde a conta.'], 'Num mês puxado, a moto anda o que outra anda em meio ano.', pos='50% 55%'),
            foto_texto(4, N, tt, '29181493', 'Sinal de alerta', ['Óleo escuro e', 'motor mais áspero?'], 'Passou da hora. Não espere a luz do óleo acender.', pos='50% 50%'),
            app(5, N, tt, ['O app faz a conta', 'pelo seu ritmo.'], 'Você diz quanto roda por dia e ele projeta cada troca.', '04-uso-km', rola=177),
            fim_app(tt, 'Você roda.', 'O MinhaMoto conta.', 'Baixe agora e nunca mais perca a troca.')]

def CM08(tt):
    global TEMA; TEMA = 'preto'   # humor · rolê · final salve
    N = 7
    return [capa(tt, '32645708', ['Todo posto tem', 'esses 5 tipos', 'de motociclista.'], 'Você é qual?', pos='50% 50%'),
            humor(2, N, tt, 'Tipo nº 1', ['O que calibra', 'o pneu no olho.'], '“Tá bom, tá bom.” Nunca tá.', '14700339', pos='50% 60%'),
            humor(3, N, tt, 'Tipo nº 2', ['O que limpa a moto', 'mais que a casa.'], 'Brilha por fora. E o óleo? Ninguém sabe.', '6872570', pos='50% 50%'),
            humor(4, N, tt, 'Tipo nº 3', ['O que põe R$ 10', 'e sai rezando.'], 'Até o próximo posto, se Deus quiser.', '35213780', pos='50% 60%'),
            humor(5, N, tt, 'Tipo nº 4', ['O que pergunta', 'pro frentista', 'qual óleo usar.'], 'O manual tava debaixo do banco.', '33915710', pos='50% 40%'),
            humor(6, N, tt, 'Tipo nº 5', ['O que sabe o km', 'de cada troca.'], 'Esse aqui usa o MinhaMoto.', '13060251', pos='50% 60%'),
            fim_salve(tt, ['Marque o amigo', 'que é o tipo nº 1.'], 'Todo grupo tem um.', 'Marque nos comentários')]

def CM09(tt):
    global TEMA; TEMA = 'claro'   # mito × verdade · misto · final salve
    N = 6
    return [capa_clara(tt, '30307405', ['3 coisas que', 'todo mundo fala', 'e estão erradas.'], 'A nº 2 quase todo mundo faz.', pos='50% 45%'),
            mito(2, N, tt, 'Calibrar com o pneu quente dá na mesma.', ['Calibre sempre', 'com o pneu frio.'], 'Quente, a pressão sobe e o número engana.', '25857998', pos='50% 50%'),
            mito(3, N, tt, 'Corrente bem esticada é mais segura.', ['Esticada demais', 'come coroa e pinhão.'], 'A folga certa está no manual da sua moto.', '29740729', pos='50% 50%'),
            mito(4, N, tt, 'A luz do óleo apagou, então tá tudo bem.', ['Confira o nível', 'antes de rodar.'], 'Luz que acende e apaga é aviso, não alívio.', '37143221', pos='50% 50%'),
            app(5, N, tt, ['Na dúvida,', 'o app explica.'], 'Barulho, luz ou freio estranho: o que significa e o que fazer.', '12-sinais-problema', rola=2990),
            fim_salve(tt, ['Mande pro amigo', 'que ainda acredita', 'na nº 2.'], 'Ele vai agradecer depois.', 'Mande pra quem precisa')]

def CM10(tt):
    global TEMA; TEMA = 'claro'   # app (combustível) · motoboy · final app
    N = 6
    return [capa_clara(tt, '34710439', ['Quanto a sua moto', 'bebeu este mês?'], 'Quem roda todo dia precisa saber.', pos='50% 30%'),
            foto_texto(2, N, tt, '37031328', 'Todo dia', ['Gasolina pesa', 'no bolso de quem', 'roda o dia todo.'], 'E quase ninguém anota quanto gastou.', pos='50% 30%'),
            foto_texto(3, N, tt, '13853130', 'Fica a dica', ['Rendimento caiu?', 'A moto tá pedindo', 'manutenção.'], 'Pneu murcho, corrente seca e filtro sujo fazem a moto beber mais.', pos='50% 55%'),
            app(4, N, tt, ['Registre cada', 'abastecimento.'], 'O app calcula seu consumo médio.', '05-combustivel', rola=177),
            app(5, N, tt, ['Veja quanto gastou', 'no mês.'], 'Gasto, abastecimentos e o preço por litro.', '05-combustivel', rola=2080),
            fim_app(tt, 'Cada real conta.', 'O MinhaMoto anota.', 'Baixe agora e controle seu gasto.')]

def CM11(tt):
    global TEMA; TEMA = 'preto'   # dica · rolê · final salve
    N = 7
    return [capa(tt, '10622201', ['Rolê no domingo?', '10 minutos antes', 'salvam a viagem.'], '5 checagens antes de sair.', pos='50% 40%'),
            numero(2, N, tt, '1', ['Pneu'], 'Calibre com o pneu frio e veja se o sulco está acima da marca de desgaste.', '29713609', pos='50% 70%'),
            numero(3, N, tt, '2', ['Óleo'], 'Com a moto em pé, o nível tem que ficar entre o mínimo e o máximo.', '8550669', pos='50% 50%'),
            numero(4, N, tt, '3', ['Corrente'], 'Folga certa e lubrificada. Seca, ela estica e gasta o kit.', '37131862-corrente', pos='70% 70%'),
            numero(5, N, tt, '4', ['Freios'], 'Manete e pedal firmes. Chiado de metal é pastilha no fim.', '12680555', pos='50% 85%'),
            numero(6, N, tt, '5', ['Luzes'], 'Farol, lanterna, setas e luz de freio funcionando.', '4686570', pos='50% 50%'),
            fim_salve(tt, ['Confira tudo', 'antes do próximo rolê.'], 'E mande pro parceiro de estrada.', 'Salve este post')]

def CM12(tt):
    global TEMA; TEMA = 'azul'   # humor · motoboy · final app
    N = 7
    return [capa(tt, '5195494', ['Coisas que só quem', 'trabalha de moto', 'entende.'], 'A nº 4 dói no bolso.', pos='50% 45%', tam=92),
            humor(2, N, tt, 'nº 1', ['A chuva começa', 'na hora que você sai.'], 'Nem um minuto antes.', '31408946', pos='50% 60%'),
            humor(3, N, tt, 'nº 2', ['A corrida é sempre', 'do outro lado', 'da cidade.'], 'E o cliente mora no último bloco.', '33967690', pos='50% 60%'),
            humor(4, N, tt, 'nº 3', ['A moto inventa', 'um barulho novo', 'toda segunda.'], 'E ele some quando chega na oficina.', '18596183', pos='50% 55%'),
            humor(5, N, tt, 'nº 4', ['Moto parada', 'é dia sem ganhar.'], 'Por isso manutenção não pode virar surpresa.', '11895391', pos='60% 60%'),
            app(6, N, tt, ['O app avisa', 'antes do problema.'], 'Prazo vencido ou troca chegando: aparece nas notificações.', '15-notificacoes'),
            fim_app(tt, 'Moto parada', 'não paga conta.', 'Baixe agora o MinhaMoto.')]

def CM13(tt):
    global TEMA; TEMA = 'claro'   # mito · rolê · final app
    N = 6
    return [capa_clara(tt, '30817486', ['Moto parada', 'não estraga?'], 'Estraga sim. E em silêncio.', pos='50% 55%'),
            foto_texto(2, N, tt, '32678623', 'Bateria', ['Parada, a bateria', 'descarrega sozinha.'], 'Algumas semanas sem rodar e ela pode não pegar.', pos='50% 55%'),
            foto_texto(3, N, tt, '7444212', 'Pneu', ['O pneu perde', 'pressão parado.'], 'E força sempre o mesmo ponto no chão.', pos='50% 70%'),
            foto_texto(4, N, tt, '13805323', 'Óleo e gasolina', ['Eles também', 'envelhecem.'], 'Por isso o manual tem prazo, não só km.', pos='50% 50%'),
            app(5, N, tt, ['Por tempo', 'também conta.'], 'O app lembra mesmo se a moto quase não rodar.', '03-manutencao', rola=2588),
            fim_app(tt, 'Rodando ou parada,', 'o MinhaMoto lembra.', 'Baixe agora e cuide da sua moto.')]

def CM14(tt):
    global TEMA; TEMA = 'azul'   # app (saúde) · misto · final app
    N = 5
    return [capa(tt, '20635067', ['Sua moto tá', 'quantos % em dia?'], 'Dá pra saber em 1 segundo.', pos='50% 60%'),
            foto_texto(2, N, tt, '9606748', 'Manutenção', ['Moto em dia', 'não é chute.'], 'É óleo, corrente, freio, pneu e vela, cada um no seu km.', pos='50% 50%'),
            app(3, N, tt, ['O app mostra', 'num número só.'], 'Saúde da moto: quanto da manutenção está em dia.', '02-saude', rola=177),
            app(4, N, tt, ['E mostra onde', 'pede atenção.'], 'Sistema por sistema: motor, freios, transmissão e elétrica.', '02-saude', rola=1920),
            fim_app(tt, 'Moto em dia', 'agora tem número.', 'Baixe agora o MinhaMoto.')]

def CM15(tt):
    global TEMA; TEMA = 'preto'   # dica · motoboy · final salve
    N = 6
    return [capa(tt, '28899351', ['3 sinais de que', 'a pastilha de freio', 'acabou.'], 'O 3º é o mais perigoso.', pos='50% 50%', tam=94),
            numero(2, N, tt, '1', ['Chiado de metal', 'na freada.'], 'É o aviso de desgaste ou o metal raspando no disco.', '10614293', pos='50% 50%'),
            numero(3, N, tt, '2', ['Manete ou pedal', 'mais fundo.'], 'Você precisa apertar mais para frear igual.', '33469801', pos='50% 35%'),
            numero(4, N, tt, '3', ['A moto demora', 'mais pra parar.'], 'No trânsito, esse metro a mais é o acidente.', '18550074', pos='50% 50%'),
            foto_texto(5, N, tt, '9607261', 'E tem mais', ['Pastilha no fim', 'risca o disco.'], 'Aí a troca barata vira troca de disco.', pos='50% 50%'),
            fim_salve(tt, ['Confira seu freio', 'ainda hoje.'], 'E mande pro parceiro que vive no corredor.', 'Salve este post')]

def CM16(tt):
    global TEMA; TEMA = 'claro'   # app (ficha) · rolê · final app
    N = 5
    return [capa_clara(tt, '12912716', ['Você sabe a', 'calibragem certa', 'da sua moto?'], 'Sozinho e com garupa muda.', pos='50% 55%'),
            foto_texto(2, N, tt, '35721171', 'Na estrada', ['Na hora de calibrar,', 'ninguém lembra', 'o número.'], 'E o manual ficou em casa.', pos='50% 60%'),
            app(3, N, tt, ['A ficha da sua moto', 'no bolso.'], 'Os dados do manual do seu modelo.', '08-moto-especificacoes', rola=177),
            app(4, N, tt, ['A calibragem certa,', 'sozinho ou com garupa.'], 'Dianteiro e traseiro, direto do manual.', '10-lista-revisao', rola=3060),
            fim_app(tt, 'O manual inteiro', 'no seu celular.', 'Baixe agora o MinhaMoto.')]

PECAS2 = {k: v for k, v in globals().items() if k.startswith('CM') and callable(v)}

if __name__ == '__main__':
    ids = sys.argv[1:] or sorted(PECAS2)
    ok = True
    for k in ids:
        f = PECAS2[k]
        tem = lambda c: ('claro' if c.startswith('<!--claro-->') else 'escuro', c.replace('<!--claro-->', ''))
        r = render_lista(k, [tem(c) for c in f(False)], [tem(c) for c in f(True)])
        folha(k, k); print(k, 'ok' if r else 'FALHOU'); ok &= r
    sys.exit(0 if ok else 1)
