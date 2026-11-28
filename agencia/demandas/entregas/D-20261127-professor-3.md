# D-20261127-professor-3: idade mínima 18 nos públicos dos anúncios (Pablo Escobar, 27/11/2026)

Só leitura e desenho. Não abri o Gerenciador, não mexi em campanha, conjunto ou público. Número absoluto e R$: nenhum.

**Resumo:** não consigo afirmar a idade mínima de nenhum conjunto: o repositório não registra e eu não tenho acesso de leitura ao Gerenciador. Isso é "sem dado", não "ok". Como os conjuntos duplicados entram no ar em **28/11 às 6h**, a conferência é de **antes das 6h**. Pergunta sim/não pro Léo no fim, com recomendação.

## 1. Por que importa (fonte)
- ECA Digital (Lei 15.211/2025), art. 22: proíbe perfilar menor pra direcionar publicidade. A ANPD começa a fiscalizar aferição de idade em jan/2027 (cronograma oficial: https://www.gov.br/anpd/pt-br/assuntos/eca-digital). Texto e prazos já lidos na aula `conhecimento/areas/direcao-geral/aulas/2026-11-27-classificacao-etaria-e-eca-digital.md` (item 6 do checklist é meu).
- Regra de anúncio da Meta: política de padrões de anúncios https://transparency.meta.com/policies/ad-standards/ [confirmar no oficial a página que fala de idade; a Meta não abriu pra mim nesta sessão, só busca com terceiros, que não uso como prova].

## 2. O que o repositório prova e o que não prova
| Campanha | Idade mínima configurada | Controle fixo? | Prova |
|---|---|---|---|
| MinhaMoto, 18 conjuntos duplicados (Pixel Novo, IC, início 28/11 6h) | **sem dado** | **sem dado** | LICOES 27/11 diz o que o Léo trocou (pixel, evento, complementos, recomendações) e não cita idade |
| MinhaMoto, proposta mm_meta_ic_lp_2611 (1 conjunto aberto, A1/B1) | **sem dado** (a proposta não define idade) | **sem dado** | D-20261126-dados-1 e cria-1 não têm campo de idade: **falha minha, corrijo abaixo** |
| MinhaMoto, 18 conjuntos antigos | pausados em 27/11 | n/a | LICOES 27/11 |
| Corretores (Meta, infoproduto Kavoo) | **sem dado** | **sem dado** | só o Léo edita; leitura não está ligada |
| TikTok (planejado, sem campanha) | n/a hoje | n/a | TikTok não é fixo em 18+ pra todos os formatos: [confirmar no oficial antes de criar] |

## 3. O ponto técnico que a pergunta tem que separar
Na Meta, **idade mínima 18 pode ser limite fixo ou só sugestão**, dependendo do tipo de público (Advantage+ audience trata a faixa de idade como sugestão em vários casos, e duplicar conjunto copia a configuração antiga e as recomendações). Por isso "está 18" não basta: tem que ser **o controle que a Meta não ultrapassa**. Fonte pra confirmar a regra exata: documentação de público da Marketing API https://developers.facebook.com/docs/marketing-api/audiences/ e a Central de Ajuda de público da Meta [confirmar no oficial; não abriu]. Até confirmar, trato como risco aberto, não como resolvido.

## 4. O que eu faria (só com OK, nada foi feito)
1. Em cada conjunto do MinhaMoto duplicado: conferir no passo de público se idade mínima = 18 e se o público é **por controle** (não "Advantage+ audience" com sugestão). Se for sugestão, trocar pra controle com mínimo 18.
2. Nenhum criativo com cara de público infantil (personagem, linguagem, cena de brinquedo/jogo). Os 2 de dia 1 (A1 CR-org-11 e B1 CR-org-12, `video-aviso.mp4`) são de moto e documento; a revisão visual por Disney/Shelby fica pro 1º dia.
3. Corretores: só conferir (leitura). Mudança é do Léo.
4. Guardar um print de cada tela com data. É a prova se a Meta ou a ANPD perguntar (a aula 27/11 §6 item 3 pede o mesmo).
5. Inclusão no meu D+0: **7º portão** "idade mínima 18 por controle conferida em cada conjunto" antes de a verba rodar. Hoje os 6 portões não tinham esse.

## 5. Erro meu, registrado
Minha proposta de 26/11 (URL, 12 slots, corte em %) não trazia idade mínima. Foi um buraco de checklist. Corrijo agora no 7º portão.

## 6. Pergunta pro Léo (sim/não), pelo QG, antes de 28/11 6h
"Léo, nos conjuntos do MinhaMoto que entram 28/11 às 6h (e nos dos Corretores), a idade mínima está em 18 como controle fixo (não só sugestão do Advantage+)? Se não, você aceita eu pedir pra trocar pra 18 fixo antes de ligar (você muda, eu só confiro)? Manda um print do passo de público de um conjunto de cada campanha."
**Recomendação: SIM.** Custa 5 minutos, não derruba entrega relevante (o público de moto é adulto) e fecha o risco do art. 22.
