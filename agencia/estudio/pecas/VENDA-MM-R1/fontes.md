# VENDA-MM-R1 · fontes dos números (rodada 2, 24/11/2026)

Régua: DESIGN-MINHAMOTO.md, regra 7 da revisão independente ("número em R$ só com fonte séria; nunca contradizer o que o app mostra em outra peça").

## Valores em R$ (só no V4)
Decisão do Léo (24/11): o V4 deixou de usar óleo/retífica. Agora o componente é a **pastilha de freio** que gasta até o metal e risca o disco. O número é o **preço da peça nova** em fonte séria (concessionária Honda). Os textos ficam na variável `V4_NUM`, no topo de `agencia/estudio/motores/venda_mm_r1.py`.

| Número na peça | Onde | Fonte (consultada em 24/11/2026) | O que a fonte diz |
|---|---|---|---|
| **R$ 224** (pastilha) | V4, gancho: "Pastilha de freio: R$ 224. Ele adiou." | [Winner Honda Store, pastilha dianteira](https://www.winnerhondastore.com.br/pecas/pastilha-freio-dianteira-original-honda-cg-160-titan-2025) | "Pastilha Freio Dianteira Original Honda Cg 160 Titan 2025" (ref. 06455KPPN02): R$ 224,27. A página diz "Produto Original de Fábrica". |
| **R$ 606,28** (disco) | V4, gancho: "Disco novo: R$ 606,28" | [Winner Honda Store, categoria Disco de Freios](https://www.winnerhondastore.com.br/pecas/freios/disco-de-freios) | "Disco Freio Dianteiro Honda Cg Titan Fan 160 2018 A 2026": R$ 606,28 (12x de R$ 58,95 com juros). **A página do disco não diz "original"** nem traz código Honda, por isso o rodapé não usa essa palavra pro disco. |

Rodapé na tela (texto exato): "Pastilha dianteira original Honda R$ 224,27 · Disco de freio dianteiro CG 160 Titan/Fan R$ 606,28 · Winner Honda Store (Limeira/SP) · nov/2026". A loja se apresenta como "a sua concessionária Honda desde 1984" (Limeira/SP), na página da pastilha. Não achei confirmação externa do vínculo com a Honda.

Outra concessionária, só como referência (não está na peça): Moto Clube Honda, pastilha dianteira original CG 160 (ref. 06455K67951), R$ 239,04 ou R$ 227,09 à vista ([link](https://loja.motoclubehonda.com.br/pastilha-de-freio-jogo-dianteiro-cg-160)).

O registro "Pastilhas dianteiras e fluido de freio · R$ 150,00" que aparece no fim do V4 é o Histórico da moto de exemplo do app. Não é citado como preço no texto da peça.

Fontes descartadas (rodada 1, consideradas fracas pela revisão independente): CPG Click Petróleo e Gás (óleo R$ 60) e WorkMoto (retífica R$ 1.800 a R$ 2.500).

**Causa e consequência (V4):** a pastilha gasta até a base metálica passa a raspar metal com metal e risca o disco. Aí o disco tem de ser trocado e o freio perde eficiência. Isso é tecnicamente correto. A tela "Sinais de problema" do app traz "Freio esponjoso ou curso longo do manete · Pare agora · Provável causa: ar no sistema, fluido velho ou pastilhas no fim", e é ela que aparece no V4.

## Dados técnicos (vêm das telas do app, que citam o manual do modelo)
| Afirmação | Onde | Fonte |
|---|---|---|
| Corrente: lubrificar a cada 1.000 km | V3 (recorte da tela 28), V6 (dica 2) | Tela `28-item-proximo`: "Documento do modelo: a cada 1.000 km"; `25-fontes`: Manual do Proprietário Honda CG 160 Fan/Titan 2022–2024. |
| Calibrar com o pneu frio; com garupa a pressão é maior (29 → 33 psi) | V6 (dicas 1 e 3) | Telas `10-lista-revisao` ("29 psi sozinho · 33 psi com garupa — sempre com o pneu frio") e `11-cuidados` ("Medir a pressão com pneus frios"). |
| Corrente: limpar, lubrificar, ajustar a folga | V3, V6 | Tela `11-cuidados` ("Corrente de transmissão"). |
| Moto parada também tem prazo (bateria, óleo, fluido de freio) | V5 | Tela `29-manutencao-tempo` (Tempo · 4 itens: bateria, óleo km + tempo, pneus, fluido de freio). |
| Vela: "Era para trocar aos 29.500 km · a cada 12.000 km" | V1 | Tela `21-item-atrasado`. |

## Causa técnica das historinhas
- V3: corrente seca e folgada que escapa (salta da coroa) é falha real e comum em moto de trabalho sem lubrificação/ajuste. A rodada 1 usava "vela vencida 300 km apagou a moto", que não é crível; foi trocada.
- V4: pastilha gasta até o metal risca o disco, que tem de ser trocado (ver acima).

## Fotos (banco Pexels do repo, `agencia/designer/assets/fotos/`, uso livre; nenhuma repetida entre peças)
V2 12900279 (gancho, fundo e o painel em km/h da mesma moto) · V3 15802617 (cub; 3 planos, a roda traseira como plano neutro) · V4 14534738 (bancada), 6664916 (moto de rua: painel digital com o km rodado e plano do guidão/tanque) · V5 10196163 · V6 30817486, 25857998 (pneu), 37131862 (corrente), 13060251. Sem pessoa em cena. Logos de fabricante ficaram fora do quadro ou ilegíveis.

**Fotos que faltam no banco** (pra provar o texto ao pé da letra; enquanto não houver, as cenas usam plano neutro que não desmente o texto):
- corrente seca, enferrujada ou folgada (barriga caída) de moto de trabalho (V3);
- disco de freio riscado/sulcado e pastilha gasta até a base (V4);
- calibrador encaixado no bico do pneu (V6);
- moto de trabalho (CG/Fan/Biz/Factor) parada, sem pessoa, sem marca legível. Todas as do banco têm piloto em cena.
