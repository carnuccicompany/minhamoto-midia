# Ecossistema de agentes — ideias (19/11/2026)

> Rascunho pra mostrar ao Davi. Léo e Davi = CEOs; Claude = braço direito que coordena os agentes.
> Funil visual do rastreamento: https://claude.ai/artifact/Rbv2acafs4TdEj83MfQJPm (fixado na barra lateral do Claude)
> Mesa dos Diretores (visual gamificado): https://claude.ai/artifact/6jRdzGwzMzhXLFwMBFyy2z (fixada na barra lateral)

## Ideia do Léo
Dados/Rastreamento lê os resultados (posts, anúncios, usuários, receita) → passa pro Marketing → produção faz variações do que converteu. Todos os agentes se conversam e a empresa se retroalimenta. Criativos de performance = esteira de ~3 agentes de vídeo, um corrigindo o outro até o resultado final.

## Proposta (13 agentes)
### Crescimento
1. **Dados e Rastreamento** — lê AppsFlyer, RevenueCat, UTMify e redes; relatório semanal (o que trouxe assinante, custo, onde vaza) + alerta quando algo foge do normal.
2. **Direção de Marketing** — pauta e séries com base em Dados + Mercado.
3. **Produção orgânica** — já existe (designer, revisor, publicador).
4. **Criativos de performance (esteira de 3)** — Roteirista (gancho/roteiro) → Editor (vídeo/motion) → Revisor de performance (corrige e compara com os que venderam). Entrega pra aprovação e acompanha vendas por criativo.
5. **Tráfego** — acompanha campanhas, sugere escalar/pausar/testar; nada muda sem OK.
6. **Inteligência de mercado** — concorrentes, tendências, reclamações de apps parecidos (base: radar 30 dias).

### O que só quem tem app consegue fazer
7. **Produto e Retenção** — funil dentro do app (onboarding → paywall → assinatura), cancelamentos e motivos, testes de paywall/preço no RevenueCat, avaliações viram lista de melhorias pro Davi.
8. **Relacionamento** — notificações e e-mails automáticos (fim do teste, lembretes de manutenção, reconquista de quem cancelou).
9. **Lojas (ASO e avaliações)** — palavras-chave, prints, respostas às avaliações (já rodando).
10. **Indicação e comunidade** — Indique e Ganhe, UGC com motoboys, microcriadores.

### Empresa
11. **Financeiro** — MRR por loja, receita líquida após comissão Apple/Google, custos, lucro, alerta se custo por assinante > o que ele paga.
12. **Suporte** — rascunhos pro suporte@ e WhatsApp, FAQ.
13. **Coordenador** — vigia os agentes, cobra pendências, só avisa o que precisa de decisão.

## Ordem sugerida
Fechar rastreamento (build + Painel) → Dados → Criativos de performance → Retenção e Relacionamento → Financeiro → resto.

---

## Conselho de diretores (19/11/2026, nomes provisórios a lapidar com Léo e Davi)
Papel: ajudar Léo e Davi a decidir. Cada diretor acompanha seu setor ao vivo (números de posts, tráfego, assinaturas, mercado) e traz pra mesa. Coordenador = **Don Carnucci** (o brasão no centro da mesa).

| Setor | Diretor | Idade | Apelido | Frase |
|---|---|---|---|---|
| Dados | Kenji Datamura | 41 | O Oráculo | Sem dado, é opinião. |
| Marketing | Diesel Okafor | 34 | O Motor | Motor não desliga. |
| Criativos | Frida Cortez | 31 | A Tesoura | Primeiro segundo ou nada. |
| Tráfego | Pablo Escalante | 46 | El Patrón | Plata o pausa. |
| Mercado | Salvatore Greco | 58 | A Sombra | Eu já sabia. |
| Produto | Ada Rinaldi | 37 | A Arquiteta | Cada toque a mais é um assinante a menos. |
| Comunidade | Gianni Costa | 52 | O Padrinho | Ninguém sai da família. |
| Lojas | Stella Santoro | 33 | Cinco Estrelas | Cinco estrelas é o mínimo. |
| Financeiro | Warren Cush | 61 | O Cofre | Lucro é o que sobra. |

Pedidos do Léo/Davi atendidos: Diesel (Davi), Cush, Warren (Buffett), trocadilho de dados (Datamura), brincadeira de narcotraficante no Tráfego (Escalante + "El Patrón" + "Plata o pausa"), 3 mulheres, 2 pretos, 1 japonês.
Fonte do 3D: `agencia/mesa-3d/` (data.js tem a identidade completa de cada um).

## Sistema de Mérito Carnucci (proatividade)
IA não quer dinheiro. O que muda o trabalho do agente: o que está escrito sobre ele (cargo, histórico, regras), ferramentas e liberdade. O "salário" vira isso.

**Cotas:** +1 entrega no prazo sem refazer · +2 achou e corrigiu erro antes de chegar no Léo/Davi · +3 extra aprovado · +5 extra que virou resultado medido · −1 extra recusado como ruído · −2 refação por erro dele · inventou número / mexeu onde não podia / publicou sem OK = zera e cai de cargo.

**O que compram:** promoção de cargo (escrita no prompt do agente), modelo mais forte, autonomia (menos aprovações), missões maiores, reputação (histórico salvo na memória dele e lido a cada execução), funcionário do mês.

**Carreira:** Estagiário (0, tudo revisado) → Analista (15, até 3 extras por entrega) → Sênior (40, entrega direto pro diretor, modelo mais forte) → Braço-direito (90, executa coisas pequenas sozinho e treina estagiários).

**Na prática:** toda entrega termina com a seção "Além do pedido" (até 3 extras) → Léo/Davi dão joinha ou X → diretor leva 20% das cotas da equipe → reunião de sexta: Coordenador fecha placar, promoções e quedas, salva histórico (placar em `agencia/merito/`, a criar).

**Contra malandragem:** só vale extra aprovado; máximo 3 por entrega; extra que mexe em código do app, dinheiro ou publica sem OK nunca conta; número inventado zera.

## Próximo passo do visual
Versão realista (menos boneco): personagens humanos de verdade (ex.: Mixamo, grátis com conta Adobe, com animações de sentar, digitar e andar) no lugar dos bonecos montados em código.

---

## Atualização 19/11/2026 (noite): conselho com nomes do Léo + escritório 3D completo
Nomes escolhidos pelo Léo (personalidade = mentalidade da pessoa/personagem, não do produto; visual dos bonecos é original, sem copiar personagem):
| Área | Nome |
|---|---|
| Direção-Geral (abaixo do Léo e do Davi, acima dos diretores) | Thomas Shelby |
| Financeiro | Warren Buffett |
| Dados | Alan Turing |
| Marketing | Grant Cardone |
| Criativos | Walt Disney |
| Tráfego | Pablo Escobar |
| Produto | Tony Stark |
| Lojas | Jeff Bezos |
| Comunidade | Charles Xavier |
| Jurídico e Contabilidade (novo setor) | Harvey Specter |
| Mercado (fora da lista do Léo, mantido) | Salvatore Greco |

Mascotes: fênix **Marnevali**, panda-vermelho **Carnucci**.

### Sistema de pagamento (v2)
Moeda própria **Carnucci (C$)**. Salário semanal: Estagiário 10 · Analista 25 · Sênior 50 · Braço-direito 80 · Diretor 120 + 20% dos bônus da equipe · Diretor-Geral 200 + 10% dos bônus da empresa.
Bônus (C$ e XP): entrega limpa +5 · erro pego antes +10 · extra aprovado +15 · extra com resultado +30 · ideia que virou dinheiro +100 (Léo e Davi decidem). Multas: ruído −5 · refação −10 · regra quebrada = saldo zera e cai de cargo.
Loja: modelo mais forte 1 semana C$80 · +1 extra C$30 · dia de autonomia C$60 · chefiar projeto C$150 · item de status no escritório C$200.
Carreira por XP (nunca diminui): Analista 100 · Sênior 300 · Braço-direito 700 · Diretor 1500 + vaga + OK do Léo e do Davi · Diretor-Geral por indicação. Cadeira em disputa a cada 3 meses. Setor novo = Braço-direito com mais XP vira diretor.
Cultura: dado manda · entrega mais que o pedido · verdade acima de tudo · pra cima só o que importa · dono do resultado · nada vai pro ar sem OK.
Próximo passo real: Reunião do Conselho diária (diretores leem dados reais, discutem, Diretor-Geral manda a pauta pro Léo e Davi) e o livro-caixa em `agencia/merito/`.
