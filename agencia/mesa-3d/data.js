// Conselho da Carnucci (nomes escolhidos pelo Léo em 19/11/2026)
// "regra" = a regra de trabalho do agente (não é citação da pessoa real ou do personagem)
export const FATURAMENTO = { valor: 0, atualizado: '19/11/2026', fonte: 'Número da UTMify informado pelo Léo. Os gráficos são ilustrativos até a UTMify ser ligada.' };

export const MASTER = {
  id: 'master', nome: 'Thomas Shelby', idade: 41, nacionalidade: 'Inglês', cidade: 'Birmingham', bandeira: '🇬🇧',
  apelido: 'O Estrategista', setor: 'Direção-Geral', cargo: 'Diretor-Geral', st: 'part',
  perfil: 'Frio, calculista, sempre três jogadas à frente. Fala pouco e é obedecido. Não perde a calma e não aceita desculpa.',
  regra: 'Pra cima, só o que importa.',
  faz: 'Fica abaixo do Léo e do Davi e acima dos diretores. Junta o que os diretores e as equipes discutiram, fecha as conclusões e entrega a pauta de decisões. Também roda a folha de pagamento e as promoções toda sexta.',
  mesa: 'Anda pela sala e passa na mesa de cada diretor',
  terno: 0x15161a, colete: true, gravata: 0x2a2a2e, pele: 0xe6c2a2, cabelo: 0x1a1410, estilo: 'curto',
  falas: ['Resumam em uma frase.', 'Isso vai pro Léo e pro Davi hoje.', 'Quem entregou além do pedido essa semana?'],
  subs: ['Secretário do Conselho', 'Auditor de entregas', 'Tesoureiro (folha)']
};

export const DIRETORES = [
  { id: 'dados', nome: 'Alan Turing', idade: 41, nacionalidade: 'Inglês', cidade: 'Londres', bandeira: '🇬🇧', apelido: 'O Decifrador', setor: 'Dados', cargo: 'Diretor de Dados', st: 'part',
    perfil: 'Gênio lógico. Enxerga padrão onde os outros veem bagunça. Só acredita no que dá pra provar.',
    regra: 'Todo resultado tem um padrão. Ache.', comp: 'typing', bebe: 'cafe',
    faz: 'Lê redes, AppsFlyer, RevenueCat e UTMify. Diz o que trouxe assinante, quanto custou e onde o funil vaza.',
    mesa: 'MacBook no painel de métricas e um espresso', props: ['espresso'], tela: 'chart',
    terno: 0x3a3d44, gravata: 0x6b1d24, pele: 0xebcaa8, cabelo: 0x3a2a1e, estilo: 'liso',
    falas: ['O custo por assinante caiu essa semana.', 'Esse post trouxe mais teste grátis que os outros três.', 'O funil vaza no paywall.'],
    subs: ['Coletor de métricas', 'Analista de funil', 'Alerta de anomalias', 'Relatório semanal'] },
  { id: 'mkt', nome: 'Grant Cardone', idade: 68, nacionalidade: 'Americano', cidade: 'Lake Charles', bandeira: '🇺🇸', apelido: 'O 10X', setor: 'Infoprodutos', cargo: 'Diretor de Infoprodutos', st: 'part',
    perfil: 'Volume massivo, energia infinita. Pensa dez vezes maior e age dez vezes mais. Odeia ficar parado.',
    regra: 'Pense 10 vezes maior. Venda 10 vezes mais.', comp: 'phone', bebe: 'agua',
    faz: 'Infoprodutos dos Corretores: oferta, página, funil, campanhas em modo proposta e a fábrica de novos infoprodutos.',
    mesa: 'MacBook com o painel de vendas dos Corretores, água e celular', props: ['phone'], tela: 'feed',
    terno: 0x1c2333, gravata: 0xb08a3e, pele: 0xdcb08c, cabelo: 0x2a1d14, estilo: 'penteado',
    falas: ['Dobra o volume de anúncio dos Corretores.', 'Essa página converte, escala.', 'Próximo infoproduto já tem público.'],
    subs: [] },
  { id: 'cria', nome: 'Walt Disney', idade: 65, nacionalidade: 'Americano', cidade: 'Chicago', bandeira: '🇺🇸', apelido: 'O Sonhador', setor: 'Criativos', cargo: 'Diretor de Criativos', st: 'off',
    perfil: 'Imaginação sem limite e obsessão por encantar. Transforma qualquer ideia simples numa história que as pessoas querem ver.',
    regra: 'Se dá pra imaginar, dá pra fazer.', comp: 'sketch', bebe: 'cafe',
    faz: 'Esteira de vídeos de venda: um faz, o próximo melhora, o último compara com os que já venderam.',
    mesa: 'MacBook na linha do tempo do vídeo, storyboard e espresso', props: ['notepad', 'espresso'], tela: 'timeline',
    terno: 0x4a3426, gravata: 0x1c3a5e, pele: 0xe2b896, cabelo: 0x4a3020, estilo: 'penteado', bigode: true,
    falas: ['Corta os 3 primeiros segundos.', 'Conta como história, não como anúncio.', 'Mostra o app logo de cara.'],
    subs: ['Roteirista de gancho', 'Editor de motion', 'Revisor de performance'] },
  { id: 'trafego', nome: 'Pablo Escobar', idade: 44, nacionalidade: 'Colombiano', cidade: 'Medellín', bandeira: '🇨🇴', apelido: 'El Patrón', setor: 'Tráfego', cargo: 'Diretor de Tráfego', st: 'off',
    perfil: 'Ambição sem teto. Domina território, não aceita perder espaço pra concorrente e corta sem dó o que não dá retorno.',
    regra: 'Plata o pausa.', comp: 'cigar', bebe: 'whisky',
    faz: 'Acompanha as campanhas da Meta e do TikTok e sugere escalar, pausar ou testar. Nada muda sem o OK do Léo.',
    mesa: 'MacBook no gerenciador de anúncios, dinheiro e charuto', props: ['money', 'cigar'], tela: 'ads',
    terno: 0xd6cdbb, gravata: 0x1a1a1a, camisa: 0x1a1a1a, pele: 0xc08a60, cabelo: 0x0d0d0d, estilo: 'curto', bigode: true,
    falas: ['Essa campanha volta, dobra a verba.', 'Plata o pausa: essa aqui pausa.', 'TikTok tá mais barato que a Meta essa semana.'],
    subs: ['Gestor de campanhas', 'Testes A/B', 'Controle de verba'] },
  { id: 'produto', nome: 'Tony Stark', idade: 48, nacionalidade: 'Americano', cidade: 'Nova York', bandeira: '🇺🇸', apelido: 'O Inventor', setor: 'Produto', cargo: 'Diretor de Produto', st: 'off',
    perfil: 'Inventor genial, rápido e perfeccionista. Constrói, testa, quebra e reconstrói melhor no mesmo dia.',
    regra: 'Se funciona, dá pra fazer melhor.', comp: 'tablet', bebe: 'whisky',
    faz: 'Caminho dentro do app (cadastro, paywall, assinatura), quem cancela e por quê, testes de preço.',
    mesa: 'MacBook com o fluxo do app, tablet e uísque', props: ['tablet'], tela: 'flow',
    terno: 0x1a1a1e, gravata: 0x7a1c1c, pele: 0xdcae88, cabelo: 0x1a1410, estilo: 'penteado', barba: true,
    falas: ['Tem um passo sobrando no cadastro.', 'Quem cancela, cancela no terceiro dia.', 'Vamos testar o paywall com o plano anual primeiro.'],
    subs: ['Analista do paywall', 'Analista de cancelamentos', 'Testes de preço', 'Lista pro Davi'] },
  { id: 'fin', nome: 'Warren Buffett', idade: 96, nacionalidade: 'Americano', cidade: 'Omaha', bandeira: '🇺🇸', apelido: 'O Oráculo', setor: 'Financeiro', cargo: 'Diretor Financeiro', st: 'off',
    perfil: 'Paciência de quem pensa em décadas. Disciplina total com dinheiro e zero emoção na hora de decidir.',
    regra: 'Primeiro: não perca dinheiro.', comp: 'money', bebe: 'cafe',
    faz: 'Receita recorrente por loja, receita líquida depois da Apple e do Google, custos e lucro.',
    mesa: 'MacBook com a receita, dinheiro empilhado e calculadora', props: ['money', 'calculator'], tela: 'money',
    terno: 0x1c2840, gravata: 0x7a5a1c, pele: 0xe8c4a6, cabelo: 0xd8d8d8, estilo: 'grisalho', oculos: true,
    falas: ['Quanto custa cada assinante?', 'A Apple fica com a parte dela, olha o líquido.', 'Esse gasto não volta.'],
    subs: ['Receita (MRR)', 'Custos e ferramentas', 'Lucro e alertas'] },
  { id: 'lojas', nome: 'Jeff Bezos', idade: 62, nacionalidade: 'Americano', cidade: 'Seattle', bandeira: '🇺🇸', apelido: 'O Obcecado', setor: 'Lojas', cargo: 'Diretor de Lojas', st: 'part',
    perfil: 'Obsessão pelo cliente acima de tudo. Pensa em escala desde o primeiro dia e trata cada avaliação como prioridade.',
    regra: 'Comece pelo cliente e trabalhe pra trás.', comp: 'twophones', bebe: 'agua',
    faz: 'App Store e Google Play: palavras-chave, prints, respostas às avaliações e atendimento.',
    mesa: 'MacBook com as avaliações, um iPhone, um Android e água', props: ['phone2'], tela: 'stars',
    terno: 0x26282e, gravata: 0x1c4a3a, pele: 0xe6bea0, cabelo: 0x1a1410, estilo: 'raspado',
    falas: ['Respondi todas as avaliações de ontem.', 'Os prints novos precisam mostrar o lembrete.', 'Subimos na busca por "manutenção moto".'],
    subs: ['ASO', 'Respostas às avaliações', 'Suporte e-mail e WhatsApp'] },
  { id: 'rel', nome: 'Charles Xavier', idade: 62, nacionalidade: 'Americano', cidade: 'Nova York', bandeira: '🇺🇸', apelido: 'O Mentor', setor: 'Comunidade', cargo: 'Diretor de Comunidade', st: 'off',
    perfil: 'Lê as pessoas como ninguém. Une, forma e protege a comunidade. Sabe o que o assinante sente antes dele falar.',
    regra: 'Comunidade forte não deixa ninguém sair.', comp: 'talk', bebe: 'cafe',
    faz: 'Notificações e e-mails que seguram o assinante, reconquista de quem saiu, indicação e criadores.',
    mesa: 'MacBook com as mensagens, celular e café', props: ['phone'], tela: 'chat',
    terno: 0x3a3f4a, gravata: 0x5e1c3a, pele: 0xe4bc9c, cabelo: 0x8a8a8a, estilo: 'grisalho',
    falas: ['Manda um lembrete no fim do teste grátis.', 'Quem saiu volta com um bom motivo.', 'Motoboy indica motoboy.'],
    subs: ['Notificações e e-mails', 'Reconquista', 'Indique e Ganhe', 'Criadores e UGC'] },
  { id: 'juridico', nome: 'Harvey Specter', idade: 42, nacionalidade: 'Americano', cidade: 'Nova York', bandeira: '🇺🇸', apelido: 'O Implacável', setor: 'Jurídico', cargo: 'Diretor Jurídico e Contábil', st: 'off',
    perfil: 'Negociador implacável, sempre um passo à frente. Não perde, protege a empresa e resolve antes de virar problema.',
    regra: 'Não se joga a sorte. Se joga o homem.', comp: 'newspaper', bebe: 'whisky', papel: 'CONTRATO',
    faz: 'Termos de uso e privacidade, contratos, contabilidade e impostos da empresa, regras das lojas e proteção da marca.',
    mesa: 'MacBook com os contratos, papéis e uísque', props: [], tela: 'chat',
    terno: 0x1c1e26, gravata: 0x2a3c5e, pele: 0xe0b694, cabelo: 0x2a1d14, estilo: 'penteado',
    falas: ['Esse termo de uso precisa de ajuste.', 'O imposto do mês tá em dia.', 'Registra a marca antes que alguém registre.'],
    subs: ['Contratos e termos', 'Contabilidade e impostos', 'Regras das lojas', 'Proteção de marca'] },
  { id: 'mercado', nome: 'Salvatore Greco', idade: 58, nacionalidade: 'Italiano', cidade: 'Nápoles', bandeira: '🇮🇹', apelido: 'A Sombra', setor: 'Mercado', cargo: 'Diretor de Mercado', st: 'part',
    perfil: 'Observador, fala pouco. Sabe o que o concorrente vai lançar antes do concorrente.',
    regra: 'Quem vê primeiro, ganha.', comp: 'newspaper', bebe: 'whisky', papel: 'MERCADO',
    faz: 'Concorrentes, tendências e reclamações de apps parecidos, aqui e lá fora.',
    mesa: 'MacBook com o radar de concorrentes, jornal e charuto', props: ['cigar'], tela: 'radar',
    terno: 0x2c2c31, risca: true, gravata: 0x2b2b2b, pele: 0xd4a382, cabelo: 0x7a7a7a, estilo: 'curto',
    falas: ['O concorrente subiu o preço.', 'Reclamação nova em app parecido: lembrete que não chega.', 'Isso tá em alta lá fora.'],
    subs: ['Radar de concorrentes', 'Caçador de tendências', 'Leitor de avaliações'] }
];

// Direito de decorar: cada diretor tem itens no escritório que combinam com ele.
// Regra: diretor com moral >= 75 no mês, ou Diretor do Mês, ganha um item novo gerado pelo Claude, sem aprovação.
export const DECOR = [
  { dono: 'dados', item: 'enigma', nome: 'Máquina de cifras antiga', porque: 'Decifrar padrão é o que ele faz da vida.', desde: '2026-11-19', pos: [-0.4, -7.75], rot: 0 },
  { dono: 'mkt', item: 'megafone', nome: 'Megafone de ouro', porque: 'Volume massivo: falar alto e pra todo mundo.', desde: '2026-11-19', pos: [1.5, -7.75], rot: 0 },
  { dono: 'cria', item: 'camera', nome: 'Câmera de cinema clássica', porque: 'Toda venda boa começa com uma história.', desde: '2026-11-19', pos: [-6.0, -7.6], rot: 0.4 },
  { dono: 'trafego', item: 'hipopotamo', nome: 'Hipopótamo de ouro', porque: 'Território grande, presença maior ainda.', desde: '2026-11-19', pos: [11.0, -1.3], rot: -Math.PI / 2 },
  { dono: 'produto', item: 'braco', nome: 'Braço robótico de oficina', porque: 'Construir, testar, quebrar e reconstruir.', desde: '2026-11-19', pos: [11.0, 1.0], rot: -Math.PI / 2 },
  { dono: 'fin', item: 'ticker', nome: 'Máquina de cotações antiga', porque: 'Décadas olhando número com paciência.', desde: '2026-11-19', pos: [5.6, 7.75], rot: Math.PI },
  { dono: 'lojas', item: 'foguete', nome: 'Maquete de foguete', porque: 'Pensar em escala desde o primeiro dia.', desde: '2026-11-19', pos: [7.5, 7.7], rot: 0 },
  { dono: 'rel', item: 'xadrez', nome: 'Mesa de xadrez', porque: 'Ler as pessoas e pensar o jogo inteiro.', desde: '2026-11-19', pos: [-5.0, 7.55], rot: 0 },
  { dono: 'juridico', item: 'vinil', nome: 'Toca-discos e coleção de vinis', porque: 'Calma de quem nunca perde uma negociação.', desde: '2026-11-19', pos: [0.1, 8.15], rot: Math.PI },
  { dono: 'mercado', item: 'globo', nome: 'Globo antigo', porque: 'Ele vê o mundo inteiro antes dos outros.', desde: '2026-11-19', pos: [-11.0, 5.6], rot: Math.PI / 2 },
  { dono: 'master', item: 'cavalo', nome: 'Escultura de cavalo em bronze', porque: 'Força, estratégia e controle.', desde: '2026-11-19', pos: [5.2, -8.0], rot: 0 },
];

// Hall da Fama: quadro do Diretor da Semana e do Diretor do Mês (atualizado pela folha de sexta)
export const HALL = {"semana": "cria", "mes": null, "primeiraEscolha": "2026-11-20"};

// Estoque da casa: marcas e preços reais (varejo no Brasil, consultado em 19/11/2026).
// C$ = R$ / 20, arredondado. Bebida e charuto acabam no consumo; relógio e perfume ficam com o dono.
export const CAMBIO = 20;
export const ESTOQUE_DATA = '19/11/2026';
export const ESTOQUE = [
  { id: 'royal21', onde: 'adega', tipo: 'Uísque', nome: 'Royal Salute 21 anos', det: 'Blended escocês, 700 ml', reais: 799, fonte: 'Zoom (menor preço)', url: 'https://www.zoom.com.br/whisky/royal-salute-whisky-21-anos-escoces-700ml', consome: true },
  { id: 'blue', onde: 'adega', tipo: 'Uísque', nome: 'Johnnie Walker Blue Label', det: 'Blended escocês, 750 ml', reais: 1900, fonte: 'Inter Shop', url: 'https://shopping.inter.co/Whisky-Johnnie-Walker-Blue/p/2592644', consome: true },
  { id: 'macallan18', onde: 'adega', tipo: 'Uísque', nome: 'The Macallan 18 anos Sherry Oak', det: 'Single malt, 700 ml', reais: 3500, fonte: 'Loja Macallan SP (Bloomberg Línea)', url: 'https://www.bloomberglinea.com.br/estilo-de-vida/como-o-macallan-se-tornou-um-uisque-tao-caro-e-desejado-e-os-planos-para-o-brasil/', consome: true },
  { id: 'hennessyxo', onde: 'adega', tipo: 'Conhaque', nome: 'Hennessy X.O', det: 'Cognac, 700 ml', reais: 2166, fonte: 'Magazine Luiza', url: 'https://m.magazineluiza.com.br/busca/conhaque+hennessy/', consome: true },
  { id: 'donjulio', onde: 'frigobar', tipo: 'Tequila', nome: 'Don Julio 1942', det: 'Añejo, 750 ml', reais: 1820, fonte: 'Fast Shop (Diageo)', url: 'https://site.fastshop.com.br/tequila-don-julio-1942---750ml-158191/p', consome: true },
  { id: 'dom', onde: 'frigobar', tipo: 'Champanhe', nome: 'Dom Pérignon Vintage', det: 'Brut, 750 ml', reais: 2533, fonte: 'Casas Bahia', url: 'https://www.casasbahia.com.br/champagne-dom-perignon-vintage-luminous-s-estojo-750ml/p/1572657989', consome: true },
  { id: 'nespresso', onde: 'frigobar', tipo: 'Café', nome: 'Nespresso Ispirazione', det: 'Caixa com 50 cápsulas', reais: 483, fonte: 'Magazine Luiza', url: 'https://www.magazineluiza.com.br/marcas/nespresso/', consome: true },
  { id: 'agua', onde: 'frigobar', tipo: 'Água', nome: 'Água gelada', det: 'Do bebedouro, à vontade', reais: 0, fonte: 'Da casa', consome: true },
  { id: 'behike', onde: 'armario', tipo: 'Charuto', nome: 'Cohiba Behike 56', det: 'Cubano, unidade', reais: 3125, fonte: 'Renova Invest (guia 2026)', url: 'https://renovainvest.com.br/?p=72669', consome: true },
  { id: 'monte2', onde: 'armario', tipo: 'Charuto', nome: 'Montecristo Nº 2', det: 'Cubano, pirâmide, unidade', reais: 260, fonte: 'Carta do Fairmont Rio (2026)', url: 'https://fairmontrio.com/wp-content/uploads/2026/04/Menu-Relax-Garden-Bar-15x297cm-v7-Q12026-compactado-1.pdf', consome: true },
  { id: 'aventus', onde: 'armario', tipo: 'Perfume', nome: 'Creed Aventus', det: 'Eau de parfum, 100 ml', reais: 3519, fonte: 'Drogasil', url: 'https://www.drogasil.com.br/aventus-creed-eau-de-parfum-masculino-100-ml-1156389.html', consome: false },
  { id: 'rolex', onde: 'armario', tipo: 'Relógio', nome: 'Rolex Submariner Date', det: 'Aço Oystersteel, 41 mm (ref. 126610LN)', reais: 96000, fonte: 'Rolex Brasil (preço sugerido)', url: 'https://www.rolex.com/pt_br/watches/submariner/m126610ln-0001.html', consome: false },
  { id: 'chivas12', onde: 'adega', tipo: 'Uísque', nome: 'Chivas Regal 12 anos', det: 'Blended escocês, 1 L · bebida da casa no padrão Ouro', reais: 164.25, fonte: 'Magalu', url: 'https://m.magazineluiza.com.br/busca/chivas+12+anos/', consome: true },
  { id: 'redlabel', onde: 'adega', tipo: 'Uísque', nome: 'Johnnie Walker Red Label', det: 'Blended escocês, 1 L · bebida da casa no padrão Prata', reais: 57.90, fonte: 'Buscapé (menor preço)', url: 'https://www.buscape.com.br/whisky/whisky-johnnie-walker-red-label-1l', consome: true },
  { id: 'cachaca51', onde: 'adega', tipo: 'Cachaça', nome: 'Cachaça 51', det: '965 ml · bebida da casa no padrão Crise', reais: 21.90, fonte: 'Buscapé (menor preço)', url: 'https://www.buscape.com.br/cachaca-pinga/cachaca-51-ouro-965ml', consome: true },
  { id: 'pilao', onde: 'frigobar', tipo: 'Café', nome: 'Café Pilão', det: '500 g · café da casa no Prata e no Crise', reais: 32.99, fonte: 'Pão de Açúcar', url: 'https://www.paodeacucar.com/produto/152052/cafe-pilao-torrado-e-moido-tradicional-almofada-500g', consome: true },
  { id: 'dannemann', onde: 'armario', tipo: 'Charuto', nome: 'Dannemann Robusto Mata Fina', det: 'Charuto baiano · charuto da casa no padrão Prata', reais: 50, fonte: 'Brazil Journal (cerca de R$ 50)', url: 'https://braziljournal.com/viva-el-patron-a-volta-por-cima-dos-charutos-baianos', consome: true },
  { id: 'casio', onde: 'armario', tipo: 'Relógio', nome: 'Casio Vintage A168', det: 'Digital, aço', reais: 252.71, fonte: 'Buscapé (menor preço)', url: 'https://www.buscape.com.br/relogio-pulso/relogio-unissex-digital-casio-vintage-a168wa-1wdf-prata', consome: false },
  { id: 'tissot', onde: 'armario', tipo: 'Relógio', nome: 'Tissot PRX', det: 'Aço, quartzo suíço', reais: 4379, fonte: 'Amazon via Buscapé', url: 'https://www.buscape.com.br/busca/relogio+tissot+1853+t109410a', consome: false },
  { id: 'daytona', onde: 'armario', tipo: 'Relógio', nome: 'Rolex Cosmograph Daytona', det: 'Aço Oystersteel, 40 mm', reais: 142800, fonte: 'Rolex Brasil (preço sugerido)', url: 'https://www.rolex.com/pt-br/watches/cosmograph-daytona/all-models?group=0', consome: false },
  { id: 'daytonaouro', onde: 'armario', tipo: 'Relógio', nome: 'Rolex Cosmograph Daytona (ouro amarelo)', det: 'Ouro amarelo 18 ct, 40 mm', reais: 347900, fonte: 'Rolex Brasil (preço sugerido)', url: 'https://www.rolex.com/pt-br/watches/cosmograph-daytona/all-models?group=0', consome: false },
  { id: 'terno_micro', onde: 'armario', tipo: 'Terno', nome: 'Terno microfibra', det: 'Loja popular · terno da casa no padrão Crise', reais: 214.91, fonte: 'Magalu', url: 'https://www.magazineluiza.com.br/busca/ternos/', consome: false },
  { id: 'terno_pv', onde: 'armario', tipo: 'Terno', nome: 'Terno Slim Fit PV', det: 'Terno da casa no padrão Prata', reais: 1699.90, fonte: 'Magalu', url: 'https://www.magazineluiza.com.br/busca/terno+fit/', consome: false },
  { id: 'terno_super120', onde: 'armario', tipo: 'Terno', nome: 'Terno lã Super 120 (Highstil)', det: 'Terno da casa no padrão Ouro', reais: 4229.90, fonte: 'Dafiti', url: 'https://www.dafiti.com.br/HIGHSTIL-Terno-Slim-Fit-La-Xadrez---Azul-Marinho-15137250.html', consome: false },
  { id: 'zegna', onde: 'armario', tipo: 'Terno', nome: 'Ermenegildo Zegna sob medida', det: 'A partir de · terno da casa no padrão Elite', reais: 8000, fonte: 'IstoÉ Dinheiro (matéria antiga; a confirmar)', url: 'https://istoedinheiro.com.br/elegancia-tropical-3', consome: false },
];

// Estoque ampliado (20/11/2026): o resto do estoque.json, por lugar do escritório
ESTOQUE.push(
  {"id": "seiko_presage", "onde": "armario", "tipo": "Relógio", "nome": "Seiko Presage Cocktail Time SRPB41J1", "det": "Nível Sênior", "cs": 220, "fonte": "preço real com link no estoque.json", "consome": false, "reais": 4399.99, "url": "https://www.newstorerj.com.br/relogios/relogios-seiko/relogio-seiko-presage-cocktail-time-srpb41j1"},
  {"id": "cartier_santos", "onde": "armario", "tipo": "Relógio", "nome": "Cartier Santos (modelo de entrada)", "det": "Nível Braço-direito", "cs": 1750, "fonte": "preço real com link no estoque.json", "consome": false, "reais": 35000, "url": "https://www.seudinheiro.com/2025/lifestyle/este-relogio-praticamente-brasileiro-e-um-simbolo-da-relojoaria-mundial-ha-mais-de-um-seculo-mas-ele-nao-e-da-rolex-mnog/"},
  {"id": "speedmaster", "onde": "armario", "tipo": "Relógio", "nome": "Omega Speedmaster Moonwatch Professional 42 mm", "det": "Nível Diretor", "cs": 3591, "fonte": "preço real com link no estoque.json", "consome": false, "reais": 71829.09, "url": "https://www.pendulumrelogios.com.br/products/relogio-omega-310-30-42-50-01-002-speedmaster-moonwatch-professional-42mm"},
  {"id": "parker_sonnet", "onde": "armario", "tipo": "Caneta", "nome": "Caneta esferográfica Parker Sonnet", "det": "Nível Analista", "cs": 64, "fonte": "preço real com link no estoque.json", "consome": false, "reais": 1290, "url": "https://www.virtucanetas.com.br/caneta-esferografica-parker-sonnet"},
  {"id": "mb_classique", "onde": "armario", "tipo": "Caneta", "nome": "Caneta esferográfica Montblanc Meisterstück Classique", "det": "Nível Sênior", "cs": 210, "fonte": "preço real com link no estoque.json", "consome": false, "reais": 4200, "url": "https://www.montblanc.com.br/caneta-esferografica-meisterstuck-classique-branca-137122/p"},
  {"id": "mb_platinum", "onde": "armario", "tipo": "Caneta", "nome": "Caneta esferográfica Montblanc Meisterstück Classique Platinum", "det": "Nível Sênior", "cs": 191, "fonte": "preço real com link no estoque.json", "consome": false, "reais": 3825, "url": "https://www.bergersonjoias.com/montblanc-meisterstuck-platinum-esfero-132446/p"},
  {"id": "abot_mb_meister", "onde": "armario", "tipo": "Abotoadura", "nome": "Abotoaduras Montblanc Meisterstück", "det": "Nível Analista", "cs": 108, "fonte": "preço real com link no estoque.json", "consome": false, "reais": 2165, "url": "https://www.montblanc.com.br/abotoaduras-montblanc-meisterstuck-112896/p"},
  {"id": "abot_mb_star", "onde": "armario", "tipo": "Abotoadura", "nome": "Abotoaduras Montblanc Star em aço", "det": "Nível Analista", "cs": 134, "fonte": "preço real com link no estoque.json", "consome": false, "reais": 2685, "url": "https://www.montblanc.com.br/abotoaduras-montblanc-star-em-aco-inoxidavel-123808/p"},
  {"id": "gravata_ra", "onde": "armario", "tipo": "Gravata", "nome": "Gravata Ricardo Almeida jacquard de seda", "det": "Nível Analista", "cs": 51, "fonte": "preço real com link no estoque.json", "consome": false, "reais": 1019, "url": "https://www.ricardoalmeida.com.br/products/gravata-jacquard-seda-azul-55207-84609"},
  {"id": "gravata_bulgari", "onde": "armario", "tipo": "Gravata", "nome": "Gravata Bulgari de seda", "det": "Nível Analista", "cs": 110, "fonte": "preço real com link no estoque.json", "consome": false, "reais": 2200, "url": "https://www.bulgari.com/pt-br/bolsas-e-acessorios/masculino/gravatas/formal-gravata-seda-azul-244097"},
  {"id": "terno_ra", "onde": "armario", "tipo": "Terno", "nome": "Terno Ricardo Almeida alfaiataria Super 120s", "det": "Nível Sênior", "cs": 576, "fonte": "preço real com link no estoque.json", "consome": false, "reais": 11529, "url": "https://www.ricardoalmeida.com.br/collections/ternos"},
  {"id": "democrata_oxford", "onde": "armario", "tipo": "Sapato", "nome": "Sapato Democrata Oxford de couro", "det": "Nível Estagiário", "cs": 15, "fonte": "preço real com link no estoque.json", "consome": false, "reais": 309.9, "url": "https://www.dafiti.com.br/Sapato-Democrata-Oxford-Preto-14175774.html"},
  {"id": "rayban_aviator", "onde": "armario", "tipo": "Óculos", "nome": "Óculos Ray-Ban Aviator Classic", "det": "Nível Analista", "cs": 64, "fonte": "preço real com link no estoque.json", "consome": false, "reais": 1290, "url": "https://www.dafiti.com.br/Oculos-de-Sol-Ray-Ban-Aviator-Classic-14420680.html"},
  {"id": "sauvage", "onde": "armario", "tipo": "Perfume", "nome": "Dior Sauvage Eau de Parfum 100 ml", "det": "Nível Analista", "cs": 43, "fonte": "preço real com link no estoque.json", "consome": true, "reais": 851.9, "url": "https://www.belezanaweb.com.br/sauvage-dior-eau-de-parfum-refilavel-perfume-masculino-100ml/"},
  {"id": "bleu_chanel", "onde": "armario", "tipo": "Perfume", "nome": "Bleu de Chanel Eau de Parfum 100 ml", "det": "Nível Analista", "cs": 82, "fonte": "preço real com link no estoque.json", "consome": true, "reais": 1635, "url": "https://www.perfumari.com.br/perfumaria-importada/masculino/bleu-de-chanel-eau-de-parfum-100ml"},
  {"id": "oud_wood", "onde": "armario", "tipo": "Perfume", "nome": "Tom Ford Oud Wood Eau de Parfum 50 ml", "det": "Nível Analista", "cs": 97, "fonte": "preço real com link no estoque.json", "consome": true, "reais": 1939, "url": "https://www.epocacosmeticos.com.br/oud-wood-tom-ford-perfume-masculino-edp/p"},
  {"id": "siglo6", "onde": "armario", "tipo": "Charuto", "nome": "Cohiba Siglo VI (unidade)", "det": "Nível Estagiário", "cs": 15, "fonte": "preço real com link no estoque.json", "consome": true, "reais": 305, "url": "https://charutossaopaulo.com.br/index.php/charuto-cohiba-siglo-vi.html"},
  {"id": "glenfiddich18", "onde": "adega", "tipo": "Uísque", "nome": "Glenfiddich 18 anos 750 ml", "det": "Nível Analista", "cs": 75, "fonte": "preço real com link no estoque.json", "consome": true, "reais": 1499.99, "url": "https://www.imigrantesbebidas.com.br/whisky-glenfiddich-18-anos-750ml"},
  {"id": "zacapa_xo", "onde": "adega", "tipo": "Rum", "nome": "Rum Zacapa XO 750 ml", "det": "Nível Analista", "cs": 122, "fonte": "preço real com link no estoque.json", "consome": true, "reais": 2433.99, "url": "https://www.imigrantesbebidas.com.br/ron-zacapa-xo-gran-reserva-750ml"},
  {"id": "clase_azul", "onde": "adega", "tipo": "Tequila", "nome": "Tequila Clase Azul Reposado 700 ml", "det": "Nível Sênior", "cs": 332, "fonte": "preço real com link no estoque.json", "consome": true, "reais": 6637, "url": "https://www.santaluzia.com.br/tequila-clase-azul-reposado---700ml-3208621/p"},
  {"id": "moet", "onde": "frigobar", "tipo": "Champanhe", "nome": "Moët & Chandon Brut Impérial 750 ml", "det": "Nível Estagiário", "cs": 25, "fonte": "preço real com link no estoque.json", "consome": true, "reais": 499.99, "url": "https://www.supernosso.com/90757-champagne-moet---chandon-brut-imperial-750ml/p"},
  {"id": "cristal", "onde": "frigobar", "tipo": "Champanhe", "nome": "Louis Roederer Cristal Brut 750 ml", "det": "Nível Sênior", "cs": 295, "fonte": "preço real com link no estoque.json", "consome": true, "reais": 5899.99, "url": "https://www.imigrantesbebidas.com.br/champagne-louis-roederer-cristal-brut-750-ml"},
  {"id": "jacu", "onde": "frigobar", "tipo": "Café", "nome": "Café Jacu Bird em grãos (lata 250 g)", "det": "Nível Estagiário", "cs": 24, "fonte": "preço real com link no estoque.json", "consome": true, "reais": 470, "url": "https://cafedomercadocuritiba.com.br/produto/cafe-jacu-bird-graos-torrados-lata-250-grs/"},
  {"id": "poltrona_mole", "onde": "sala", "tipo": "Poltrona", "nome": "Poltrona Mole com banqueta, couro (design Sergio Rodrigues)", "det": "Nível Braço-direito", "cs": 930, "fonte": "preço real com link no estoque.json", "consome": false, "reais": 18599, "url": "https://jardinvelharia.com.br/products/poltrona-mole-com-banqueta-em-couro-caramelo-sergio-rodrigues"},
  {"id": "eames", "onde": "sala", "tipo": "Poltrona", "nome": "Poltrona Eames Lounge e otomana (Herman Miller)", "det": "Nível Diretor", "cs": 3085, "fonte": "preço real com link no estoque.json", "consome": false, "reais": 61696.5, "url": "https://store.hermanmiller.com.br/poltrona-eames-lounge-e-otomana/p"},
  {"id": "mesa_exec", "onde": "sala", "tipo": "Mesa", "nome": "Mesa executiva de diretor 200 cm", "det": "Nível Analista", "cs": 110, "fonte": "preço real com link no estoque.json", "consome": false, "reais": 2199.97, "url": "https://www.madeiramadeira.com.br/mesa-executiva-para-escritorio-diretor-com-caixa-de-tomadas-porta-objetos-colecao-200cm-corporate-ci-613537678.html"},
  {"id": "gravura_britto", "onde": "sala", "tipo": "Quadro", "nome": "Gravura assinada e numerada de Romero Britto", "det": "Nível Analista", "cs": 85, "fonte": "preço real com link no estoque.json", "consome": false, "reais": 1700, "url": "https://www.garimpopaulista.com.br/MLB-2663461278-gravura-romero-britto-original-assinada-e-numerada-_JM"},
  {"id": "dom_casmurro_1a", "onde": "sala", "tipo": "Livro raro", "nome": "Dom Casmurro, 1ª edição (Machado de Assis)", "det": "Nível Braço-direito", "cs": 1200, "fonte": "preço real com link no estoque.json", "consome": false, "reais": 24000, "url": "https://www.revistabula.com/165336-os-5-livros-de-autores-brasileiros-mais-caros-ja-vendidos-no-brasil-segundo-vendas-documentadas/"},
  {"id": "os_sertoes_1a", "onde": "sala", "tipo": "Livro raro", "nome": "Os Sertões, 1ª edição (Euclides da Cunha)", "det": "Lendário · só com a conquista imaculado_8", "cs": 7150, "fonte": "preço real com link no estoque.json", "consome": false, "reais": 143000, "url": "https://www.revistabula.com/165336-os-5-livros-de-autores-brasileiros-mais-caros-ja-vendidos-no-brasil-segundo-vendas-documentadas/"},
  {"id": "trofeu", "onde": "sala", "tipo": "Troféu", "nome": "Troféu de metal dourado personalizado (34 cm)", "det": "Nível Estagiário", "cs": 5, "fonte": "preço real com link no estoque.json", "consome": false, "reais": 106.99, "url": "https://casadoscraques.com.br/trofeus-e-medalhas/trofeus/vitoria/trofeu-personalizado-vitoria-40-cm-613"},
  {"id": "monstera_var", "onde": "sala", "tipo": "Planta rara", "nome": "Monstera deliciosa Variegata (muda)", "det": "Nível Estagiário", "cs": 22, "fonte": "preço real com link no estoque.json", "consome": false, "reais": 450, "url": "https://viveirooreades.com.br/produto/monstera-deliciosa-variegata/"},
  {"id": "bonsai_kishu", "onde": "sala", "tipo": "Planta rara", "nome": "Bonsai de junípero Kishu", "det": "Nível Sênior", "cs": 164, "fonte": "preço real com link no estoque.json", "consome": false, "reais": 3283.78, "url": "https://www.rootsbonsai.com.br/produto/bonsai-junipero-kishu-17/"},
  {"id": "fatboy", "onde": "garagem", "tipo": "Moto", "nome": "Harley-Davidson Fat Boy Grey Ghost", "det": "Lendário · só com a conquista cpa_no_alvo", "cs": 7748, "fonte": "preço real com link no estoque.json", "consome": false, "reais": 154950, "url": "https://www.autossegredos.com.br/moto/harley-davidson-moto/harley-davidson-lanca-fat-boy-grey-ghost-por-r-154-950/"},
  {"id": "panigale_v4s", "onde": "garagem", "tipo": "Moto", "nome": "Ducati Panigale V4 S 2026", "det": "Lendário · só com a conquista criativo_campeao", "cs": 10500, "fonte": "preço real com link no estoque.json", "consome": false, "reais": 209990, "url": "https://tudodemotos.com.br/nova-ducati-panigale-v4-2026-brasil/"},
  {"id": "porsche_911", "onde": "garagem", "tipo": "Carro", "nome": "Porsche 911 Carrera 2026", "det": "Lendário · só com a conquista conselheiro", "cs": 49000, "fonte": "preço real com link no estoque.json", "consome": false, "reais": 980000, "url": "https://www.webmotors.com.br/porsche/911/2026"},
  {"id": "jameson", "onde": "adega", "tipo": "Uísque irlandês", "nome": "Jameson Irish Whiskey 1 L", "det": "Nível Estagiário", "cs": 7, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "jack7", "onde": "adega", "tipo": "Uísque americano", "nome": "Jack Daniel's Old No. 7 1 L", "det": "Nível Estagiário", "cs": 8, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "black", "onde": "adega", "tipo": "Uísque", "nome": "Johnnie Walker Black Label 12 anos 1 L", "det": "Nível Estagiário", "cs": 10, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "buchanans12", "onde": "adega", "tipo": "Uísque", "nome": "Buchanan's 12 anos 1 L", "det": "Nível Estagiário", "cs": 10, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "gold_label", "onde": "adega", "tipo": "Uísque", "nome": "Johnnie Walker Gold Label Reserve 750 ml", "det": "Nível Estagiário", "cs": 20, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "glenlivet12", "onde": "adega", "tipo": "Uísque single malt", "nome": "The Glenlivet 12 anos 750 ml", "det": "Nível Estagiário", "cs": 15, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "glenmorangie10", "onde": "adega", "tipo": "Uísque single malt", "nome": "Glenmorangie The Original 10 anos 750 ml", "det": "Nível Estagiário", "cs": 18, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "lagavulin16", "onde": "adega", "tipo": "Uísque turfado", "nome": "Lagavulin 16 anos 750 ml", "det": "Nível Analista", "cs": 35, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "macallan12", "onde": "adega", "tipo": "Uísque single malt", "nome": "The Macallan 12 anos Double Cask 700 ml", "det": "Nível Analista", "cs": 45, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "balvenie14", "onde": "adega", "tipo": "Uísque single malt", "nome": "The Balvenie 14 anos Caribbean Cask 700 ml", "det": "Nível Analista", "cs": 50, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "hibiki_harmony", "onde": "adega", "tipo": "Uísque japonês", "nome": "Hibiki Japanese Harmony 700 ml", "det": "Nível Analista", "cs": 70, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "yamazaki12", "onde": "adega", "tipo": "Uísque japonês", "nome": "Yamazaki 12 anos 700 ml", "det": "Nível Analista", "cs": 125, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "jw_kgv", "onde": "adega", "tipo": "Uísque raro", "nome": "Johnnie Walker King George V 750 ml", "det": "Nível Sênior", "cs": 200, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "macallan25", "onde": "adega", "tipo": "Uísque raro", "nome": "The Macallan 25 anos Sherry Oak 700 ml", "det": "Nível Braço-direito", "cs": 2000, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "remy_vsop", "onde": "adega", "tipo": "Conhaque", "nome": "Rémy Martin VSOP 700 ml", "det": "Nível Estagiário", "cs": 23, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "martell_cb", "onde": "adega", "tipo": "Conhaque", "nome": "Martell Cordon Bleu 700 ml", "det": "Nível Analista", "cs": 75, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "louis13", "onde": "adega", "tipo": "Conhaque raro", "nome": "Rémy Martin Louis XIII (decanter de cristal)", "det": "Nível Braço-direito", "cs": 1750, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "veuve", "onde": "frigobar", "tipo": "Champanhe", "nome": "Veuve Clicquot Brut 750 ml", "det": "Nível Estagiário", "cs": 20, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "ruinart_bdb", "onde": "frigobar", "tipo": "Champanhe", "nome": "Ruinart Blanc de Blancs 750 ml", "det": "Nível Analista", "cs": 45, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "grande_dame", "onde": "frigobar", "tipo": "Champanhe", "nome": "Veuve Clicquot La Grande Dame (safra)", "det": "Nível Analista", "cs": 70, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "krug", "onde": "frigobar", "tipo": "Champanhe", "nome": "Krug Grande Cuvée 750 ml", "det": "Nível Analista", "cs": 100, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "ace_spades", "onde": "frigobar", "tipo": "Champanhe", "nome": "Armand de Brignac Brut Gold 750 ml", "det": "Nível Sênior", "cs": 175, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "dom_rose", "onde": "frigobar", "tipo": "Champanhe", "nome": "Dom Pérignon Rosé (safra)", "det": "Nível Sênior", "cs": 225, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "salon", "onde": "frigobar", "tipo": "Champanhe raro", "nome": "Salon Blanc de Blancs (safra)", "det": "Nível Sênior", "cs": 450, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "catena", "onde": "adega", "tipo": "Vinho tinto", "nome": "Catena Zapata Malbec Argentino", "det": "Nível Estagiário", "cs": 25, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "porto20", "onde": "adega", "tipo": "Vinho do Porto", "nome": "Taylor's Porto Tawny 20 anos", "det": "Nível Analista", "cs": 30, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "almaviva", "onde": "adega", "tipo": "Vinho tinto", "nome": "Almaviva (safra)", "det": "Nível Analista", "cs": 110, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "sassicaia", "onde": "adega", "tipo": "Vinho tinto", "nome": "Tenuta San Guido Sassicaia (safra)", "det": "Nível Sênior", "cs": 175, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "opus_one", "onde": "adega", "tipo": "Vinho tinto", "nome": "Opus One (safra)", "det": "Nível Sênior", "cs": 200, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "vega_unico", "onde": "adega", "tipo": "Vinho tinto", "nome": "Vega Sicilia Único (safra)", "det": "Nível Sênior", "cs": 225, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "margaux", "onde": "adega", "tipo": "Vinho tinto raro", "nome": "Château Margaux Premier Grand Cru (safra)", "det": "Nível Sênior", "cs": 450, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "petrus", "onde": "adega", "tipo": "Vinho tinto raro", "nome": "Pétrus Pomerol (safra)", "det": "Nível Braço-direito", "cs": 2000, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "diplomatico", "onde": "adega", "tipo": "Rum", "nome": "Rum Diplomático Reserva Exclusiva 700 ml", "det": "Nível Estagiário", "cs": 13, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "zacapa_royal", "onde": "adega", "tipo": "Rum", "nome": "Rum Zacapa Royal 700 ml", "det": "Nível Analista", "cs": 70, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "patron_silver", "onde": "adega", "tipo": "Tequila", "nome": "Tequila Patrón Silver 750 ml", "det": "Nível Estagiário", "cs": 18, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "clase_azul_ultra", "onde": "adega", "tipo": "Tequila rara", "nome": "Tequila Clase Azul Ultra Extra Añejo", "det": "Nível Braço-direito", "cs": 750, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "dassai45", "onde": "frigobar", "tipo": "Sakê", "nome": "Sakê Dassai 45 Junmai Daiginjo 720 ml", "det": "Nível Estagiário", "cs": 18, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "dassai_beyond", "onde": "frigobar", "tipo": "Sakê raro", "nome": "Sakê Dassai Beyond 720 ml", "det": "Nível Sênior", "cs": 250, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "tanq_ten", "onde": "frigobar", "tipo": "Gin", "nome": "Gin Tanqueray No. Ten 750 ml", "det": "Nível Estagiário", "cs": 11, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "belvedere", "onde": "frigobar", "tipo": "Vodca", "nome": "Vodka Belvedere 700 ml", "det": "Nível Estagiário", "cs": 10, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "havana_anisio", "onde": "adega", "tipo": "Cachaça rara", "nome": "Cachaça Havana (Anísio Santiago) 600 ml", "det": "Nível Analista", "cs": 35, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "macallan30", "onde": "adega", "tipo": "Uísque lendário", "nome": "The Macallan 30 anos Sherry Oak", "det": "Lendário · só com a conquista fez_dinheiro", "cs": 6000, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "romanee_conti", "onde": "adega", "tipo": "Vinho lendário", "nome": "Domaine de la Romanée-Conti Grand Cru (safra)", "det": "Lendário · só com a conquista diretor_do_mes", "cs": 7500, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "daterra", "onde": "frigobar", "tipo": "Café", "nome": "Café especial Daterra em grãos 250 g", "det": "Nível Estagiário", "cs": 5, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "kopi_luwak", "onde": "frigobar", "tipo": "Café raro", "nome": "Café Kopi Luwak 100 g", "det": "Nível Estagiário", "cs": 25, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "gshock2100", "onde": "armario", "tipo": "Relógio", "nome": "Casio G-Shock GA-2100 \"CasiOak\"", "det": "Nível Analista", "cs": 35, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "orient_bambino", "onde": "armario", "tipo": "Relógio", "nome": "Orient Bambino automático", "det": "Nível Analista", "cs": 45, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "seiko5", "onde": "armario", "tipo": "Relógio", "nome": "Seiko 5 Sports automático", "det": "Nível Analista", "cs": 90, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "hamilton_field", "onde": "armario", "tipo": "Relógio", "nome": "Hamilton Khaki Field Mechanical", "det": "Nível Sênior", "cs": 200, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "tudor_bb58", "onde": "armario", "tipo": "Relógio", "nome": "Tudor Black Bay Fifty-Eight", "det": "Nível Braço-direito", "cs": 1400, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "tag_carrera", "onde": "armario", "tipo": "Relógio", "nome": "TAG Heuer Carrera cronógrafo", "det": "Nível Braço-direito", "cs": 1750, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "grand_seiko_snowflake", "onde": "armario", "tipo": "Relógio", "nome": "Grand Seiko \"Snowflake\" Spring Drive", "det": "Nível Braço-direito", "cs": 2000, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "seamaster300", "onde": "armario", "tipo": "Relógio", "nome": "Omega Seamaster Diver 300M", "det": "Nível Braço-direito", "cs": 2250, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "iwc_portugieser", "onde": "armario", "tipo": "Relógio", "nome": "IWC Portugieser Chronograph", "det": "Nível Braço-direito", "cs": 3000, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "datejust41", "onde": "armario", "tipo": "Relógio", "nome": "Rolex Datejust 41 (aço e ouro branco)", "det": "Nível Diretor", "cs": 3750, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "gmt_pepsi", "onde": "armario", "tipo": "Relógio", "nome": "Rolex GMT-Master II \"Pepsi\"", "det": "Nível Diretor", "cs": 5000, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "tank_ouro", "onde": "armario", "tipo": "Relógio", "nome": "Cartier Tank Louis Cartier em ouro", "det": "Nível Diretor", "cs": 6000, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "overseas", "onde": "armario", "tipo": "Relógio", "nome": "Vacheron Constantin Overseas", "det": "Nível Diretor", "cs": 9000, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "calatrava", "onde": "armario", "tipo": "Relógio", "nome": "Patek Philippe Calatrava", "det": "Nível Diretor", "cs": 10000, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "lange1", "onde": "armario", "tipo": "Relógio", "nome": "A. Lange & Söhne Lange 1", "det": "Nível Diretor", "cs": 12500, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "royal_oak", "onde": "armario", "tipo": "Relógio lendário", "nome": "Audemars Piguet Royal Oak 41 mm (aço)", "det": "Lendário · só com a conquista tomou_cadeira", "cs": 17500, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "day_date_platina", "onde": "armario", "tipo": "Relógio lendário", "nome": "Rolex Day-Date 40 em platina", "det": "Lendário · só com a conquista diretor_do_mes", "cs": 22500, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "rm011", "onde": "armario", "tipo": "Relógio lendário", "nome": "Richard Mille RM 011", "det": "Lendário · só com a conquista meta_3_semanas", "cs": 60000, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "nautilus", "onde": "armario", "tipo": "Relógio lendário", "nome": "Patek Philippe Nautilus 5811", "det": "Lendário · só com a conquista conselheiro", "cs": 75000, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "kaiak", "onde": "armario", "tipo": "Perfume", "nome": "Natura Kaiak Clássico 100 ml", "det": "Nível Estagiário", "cs": 8, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "malbec", "onde": "armario", "tipo": "Perfume", "nome": "O Boticário Malbec 100 ml", "det": "Nível Estagiário", "cs": 10, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "azzaro", "onde": "armario", "tipo": "Perfume", "nome": "Azzaro Pour Homme EDT 100 ml", "det": "Nível Estagiário", "cs": 15, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "eros", "onde": "armario", "tipo": "Perfume", "nome": "Versace Eros EDT 100 ml", "det": "Nível Estagiário", "cs": 23, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "one_million", "onde": "armario", "tipo": "Perfume", "nome": "Paco Rabanne 1 Million EDT 100 ml", "det": "Nível Estagiário", "cs": 25, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "prada_lhomme", "onde": "armario", "tipo": "Perfume", "nome": "Prada L'Homme EDT 100 ml", "det": "Nível Analista", "cs": 35, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "profondo", "onde": "armario", "tipo": "Perfume", "nome": "Giorgio Armani Acqua di Giò Profondo 100 ml", "det": "Nível Analista", "cs": 35, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "ysl_y", "onde": "armario", "tipo": "Perfume", "nome": "Yves Saint Laurent Y EDP 100 ml", "det": "Nível Analista", "cs": 38, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "terre", "onde": "armario", "tipo": "Perfume", "nome": "Hermès Terre d'Hermès EDT 100 ml", "det": "Nível Analista", "cs": 40, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "dior_homme_int", "onde": "armario", "tipo": "Perfume", "nome": "Dior Homme Intense 100 ml", "det": "Nível Analista", "cs": 45, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "layton", "onde": "armario", "tipo": "Perfume de nicho", "nome": "Parfums de Marly Layton 125 ml", "det": "Nível Analista", "cs": 110, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "tobacco_vanille", "onde": "armario", "tipo": "Perfume de nicho", "nome": "Tom Ford Tobacco Vanille 50 ml", "det": "Nível Analista", "cs": 110, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "naxos", "onde": "armario", "tipo": "Perfume de nicho", "nome": "Xerjoff Naxos 100 ml", "det": "Nível Analista", "cs": 125, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "oud_greatness", "onde": "armario", "tipo": "Perfume de nicho", "nome": "Initio Oud for Greatness 90 ml", "det": "Nível Analista", "cs": 135, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "br540", "onde": "armario", "tipo": "Perfume de nicho", "nome": "Maison Francis Kurkdjian Baccarat Rouge 540 70 ml", "det": "Nível Analista", "cs": 140, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "roja_elysium", "onde": "armario", "tipo": "Perfume de nicho", "nome": "Roja Parfums Elysium Parfum Cologne 100 ml", "det": "Nível Sênior", "cs": 200, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "clive_no1", "onde": "armario", "tipo": "Perfume raro", "nome": "Clive Christian No. 1 50 ml", "det": "Nível Sênior", "cs": 300, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "lenco_seda", "onde": "armario", "tipo": "Lenço", "nome": "Lenço de bolso de seda", "det": "Nível Estagiário", "cs": 10, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "prendedor_prata", "onde": "armario", "tipo": "Acessório", "nome": "Prendedor de gravata em prata", "det": "Nível Estagiário", "cs": 8, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "cinto_couro", "onde": "armario", "tipo": "Cinto", "nome": "Cinto de couro legítimo", "det": "Nível Estagiário", "cs": 13, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "abot_prata", "onde": "armario", "tipo": "Abotoadura", "nome": "Abotoaduras de prata 925", "det": "Nível Estagiário", "cs": 15, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "camisa_egipcio", "onde": "armario", "tipo": "Camisa", "nome": "Camisa social de algodão egípcio", "det": "Nível Estagiário", "cs": 20, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "gravata_brooks", "onde": "armario", "tipo": "Gravata", "nome": "Gravata de seda Brooks Brothers", "det": "Nível Estagiário", "cs": 25, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "oxford_couro", "onde": "armario", "tipo": "Sapato", "nome": "Sapato Oxford de couro (linha premium nacional)", "det": "Nível Estagiário", "cs": 25, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "camisa_medida", "onde": "armario", "tipo": "Camisa", "nome": "Camisa sob medida com monograma", "det": "Nível Analista", "cs": 45, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "persol714", "onde": "armario", "tipo": "Óculos", "nome": "Óculos Persol 714 dobrável", "det": "Nível Analista", "cs": 75, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "gravata_hermes", "onde": "armario", "tipo": "Gravata", "nome": "Gravata de seda Hermès", "det": "Nível Analista", "cs": 90, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "loake1880", "onde": "armario", "tipo": "Sapato", "nome": "Sapato Loake 1880 Goodyear", "det": "Nível Analista", "cs": 125, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "smoking_slim", "onde": "armario", "tipo": "Smoking", "nome": "Smoking slim de alfaiataria", "det": "Nível Analista", "cs": 125, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "carteira_mb", "onde": "armario", "tipo": "Couro", "nome": "Carteira de couro Montblanc Meisterstück", "det": "Nível Analista", "cs": 125, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "camisa_charvet", "onde": "armario", "tipo": "Camisa", "nome": "Camisa Charvet sob medida", "det": "Nível Sênior", "cs": 200, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "churchs", "onde": "armario", "tipo": "Sapato", "nome": "Sapato Church's Consul", "det": "Nível Sênior", "cs": 275, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "terno_boss", "onde": "armario", "tipo": "Terno", "nome": "Terno Hugo Boss lã virgem", "det": "Nível Sênior", "cs": 300, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "cinto_h", "onde": "armario", "tipo": "Cinto", "nome": "Cinto Hermès H reversível", "det": "Nível Sênior", "cs": 300, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "mocassim_horsebit", "onde": "armario", "tipo": "Sapato", "nome": "Mocassim Gucci Horsebit", "det": "Nível Sênior", "cs": 325, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "sobretudo_cashmere", "onde": "armario", "tipo": "Sobretudo", "nome": "Sobretudo de cashmere", "det": "Nível Sênior", "cs": 400, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "john_lobb", "onde": "armario", "tipo": "Sapato", "nome": "Sapato John Lobb City II", "det": "Nível Sênior", "cs": 600, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "oculos_cartier", "onde": "armario", "tipo": "Óculos", "nome": "Óculos Cartier Santos em metal dourado", "det": "Nível Sênior", "cs": 600, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "pasta_couro", "onde": "armario", "tipo": "Couro", "nome": "Pasta executiva de couro Montblanc", "det": "Nível Sênior", "cs": 600, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "abot_cartier", "onde": "armario", "tipo": "Abotoadura", "nome": "Abotoaduras Cartier Décor C em ouro", "det": "Nível Braço-direito", "cs": 750, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "smoking_tomford", "onde": "armario", "tipo": "Smoking", "nome": "Smoking Tom Ford O'Connor", "det": "Nível Braço-direito", "cs": 2000, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "terno_brioni", "onde": "armario", "tipo": "Terno", "nome": "Terno Brioni Brunico", "det": "Nível Braço-direito", "cs": 2250, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "savile_row", "onde": "armario", "tipo": "Terno", "nome": "Terno bespoke em Savile Row (Henry Poole)", "det": "Nível Braço-direito", "cs": 3000, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "terno_kiton", "onde": "armario", "tipo": "Terno", "nome": "Terno Kiton sob medida", "det": "Nível Diretor", "cs": 4000, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "partagas_d4", "onde": "armario", "tipo": "Charuto", "nome": "Partagás Serie D Nº 4 (unidade)", "det": "Nível Estagiário", "cs": 9, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "ryj_churchill", "onde": "armario", "tipo": "Charuto", "nome": "Romeo y Julieta Churchill (unidade)", "det": "Nível Estagiário", "cs": 10, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "padron64", "onde": "armario", "tipo": "Charuto", "nome": "Padrón 1964 Anniversary (unidade)", "det": "Nível Estagiário", "cs": 18, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "davidoff_wc", "onde": "armario", "tipo": "Charuto", "nome": "Davidoff Winston Churchill (unidade)", "det": "Nível Estagiário", "cs": 20, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "opus_x", "onde": "armario", "tipo": "Charuto", "nome": "Arturo Fuente Opus X (unidade)", "det": "Nível Analista", "cs": 35, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "cortador_dupont", "onde": "armario", "tipo": "Acessório de charuto", "nome": "Cortador de charuto S.T. Dupont", "det": "Nível Analista", "cs": 150, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "isqueiro_dupont", "onde": "armario", "tipo": "Acessório de charuto", "nome": "Isqueiro S.T. Dupont Ligne 2", "det": "Nível Sênior", "cs": 400, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "caixa_robustos", "onde": "armario", "tipo": "Charuto", "nome": "Caixa de Cohiba Robustos (25 unidades)", "det": "Nível Sênior", "cs": 600, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "caixa_behike52", "onde": "armario", "tipo": "Charuto raro", "nome": "Caixa de Cohiba Behike 52 (10 unidades)", "det": "Nível Braço-direito", "cs": 1500, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "moleskine", "onde": "armario", "tipo": "Papelaria", "nome": "Caderno de capa de couro", "det": "Nível Estagiário", "cs": 10, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "lamy_safari", "onde": "armario", "tipo": "Caneta", "nome": "Caneta tinteiro Lamy Safari", "det": "Nível Estagiário", "cs": 13, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "cross_century", "onde": "armario", "tipo": "Caneta", "nome": "Caneta Cross Century II", "det": "Nível Analista", "cs": 35, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "pelikan_m800", "onde": "armario", "tipo": "Caneta", "nome": "Caneta tinteiro Pelikan Souverän M800", "det": "Nível Sênior", "cs": 250, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "mb149", "onde": "armario", "tipo": "Caneta", "nome": "Caneta tinteiro Montblanc Meisterstück 149", "det": "Nível Sênior", "cs": 400, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "mb_writers", "onde": "armario", "tipo": "Caneta", "nome": "Caneta Montblanc Writers Edition (edição limitada)", "det": "Nível Braço-direito", "cs": 750, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "mx_master", "onde": "tecnologia", "tipo": "Tecnologia", "nome": "Mouse ergonômico Logitech MX Master", "det": "Nível Analista", "cs": 30, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "kindle", "onde": "tecnologia", "tipo": "Tecnologia", "nome": "Kindle Paperwhite", "det": "Nível Analista", "cs": 40, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "teclado_mec", "onde": "tecnologia", "tipo": "Tecnologia", "nome": "Teclado mecânico sem fio premium", "det": "Nível Analista", "cs": 40, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "airpods_pro", "onde": "tecnologia", "tipo": "Tecnologia", "nome": "Fone AirPods Pro", "det": "Nível Analista", "cs": 100, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "sony_xm", "onde": "tecnologia", "tipo": "Tecnologia", "nome": "Fone Sony WH-1000XM com cancelamento de ruído", "det": "Nível Analista", "cs": 125, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "ultrawide", "onde": "tecnologia", "tipo": "Tecnologia", "nome": "Monitor ultrawide 34\" curvo", "det": "Nível Sênior", "cs": 200, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "watch_ultra", "onde": "tecnologia", "tipo": "Tecnologia", "nome": "Apple Watch Ultra", "det": "Nível Sênior", "cs": 450, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "iphone_pro", "onde": "tecnologia", "tipo": "Tecnologia", "nome": "iPhone Pro Max (topo de linha)", "det": "Nível Sênior", "cs": 550, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "bo_beosound", "onde": "tecnologia", "tipo": "Tecnologia", "nome": "Caixa de som Bang & Olufsen Beosound", "det": "Nível Braço-direito", "cs": 750, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "macbook16", "onde": "tecnologia", "tipo": "Tecnologia", "nome": "MacBook Pro 16\" (topo de linha)", "det": "Nível Braço-direito", "cs": 1250, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "leica_q3", "onde": "tecnologia", "tipo": "Tecnologia", "nome": "Câmera Leica Q3", "det": "Nível Braço-direito", "cs": 3000, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "plaquinha", "onde": "sala", "tipo": "Mesa", "nome": "Plaquinha de mesa com nome gravado", "det": "Nível Estagiário", "cs": 3, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "luminaria_banker", "onde": "sala", "tipo": "Luminária", "nome": "Luminária de mesa estilo banqueiro (verde)", "det": "Nível Estagiário", "cs": 10, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "xicaras_porcelana", "onde": "sala", "tipo": "Mesa", "nome": "Jogo de xícaras de porcelana", "det": "Nível Estagiário", "cs": 20, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "umidor", "onde": "sala", "tipo": "Móvel", "nome": "Umidor de cedro para 50 charutos", "det": "Nível Analista", "cs": 75, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "livros_couro", "onde": "sala", "tipo": "Livros", "nome": "Coleção de clássicos de estratégia em capa de couro", "det": "Nível Analista", "cs": 100, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "globo_antigo", "onde": "sala", "tipo": "Decoração", "nome": "Globo terrestre antigo de pé", "det": "Nível Analista", "cs": 150, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "carrinho_bar", "onde": "sala", "tipo": "Móvel", "nome": "Carrinho de bar em latão", "det": "Nível Analista", "cs": 150, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "estante_nogueira", "onde": "sala", "tipo": "Móvel", "nome": "Estante de nogueira sob medida", "det": "Nível Sênior", "cs": 250, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "adega_clim", "onde": "sala", "tipo": "Móvel", "nome": "Adega climatizada para 50 garrafas", "det": "Nível Sênior", "cs": 300, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "escultura_bronze", "onde": "sala", "tipo": "Arte", "nome": "Escultura de bronze assinada", "det": "Nível Sênior", "cs": 600, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "aeron", "onde": "sala", "tipo": "Cadeira", "nome": "Cadeira Herman Miller Aeron", "det": "Nível Braço-direito", "cs": 750, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "tapete_persa", "onde": "sala", "tipo": "Decoração", "nome": "Tapete persa feito à mão", "det": "Nível Braço-direito", "cs": 1000, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "sinuca", "onde": "sala", "tipo": "Lazer", "nome": "Mesa de sinuca de madeira maciça", "det": "Nível Braço-direito", "cs": 1250, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "quadro_contemporaneo", "onde": "sala", "tipo": "Arte", "nome": "Quadro original de artista brasileiro contemporâneo", "det": "Nível Braço-direito", "cs": 2000, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "la_marzocco", "onde": "sala", "tipo": "Café", "nome": "Máquina de espresso La Marzocco Linea Mini", "det": "Nível Braço-direito", "cs": 2000, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "warhol_lito", "onde": "sala", "tipo": "Arte", "nome": "Serigrafia numerada de Andy Warhol", "det": "Nível Diretor", "cs": 7500, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "steinway", "onde": "sala", "tipo": "Lendário da sala", "nome": "Piano de cauda Steinway", "det": "Lendário · só com a conquista conselheiro", "cs": 50000, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "luva_alpinestars", "onde": "garagem", "tipo": "Equipamento de moto", "nome": "Luva de moto Alpinestars", "det": "Nível Estagiário", "cs": 25, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "capacete_ls2", "onde": "garagem", "tipo": "Equipamento de moto", "nome": "Capacete LS2 integral", "det": "Nível Analista", "cs": 45, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "jaqueta_dainese", "onde": "garagem", "tipo": "Equipamento de moto", "nome": "Jaqueta de couro Dainese", "det": "Nível Sênior", "cs": 250, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "capacete_agv", "onde": "garagem", "tipo": "Equipamento de moto", "nome": "Capacete AGV Pista GP RR", "det": "Nível Sênior", "cs": 450, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "cg160", "onde": "garagem", "tipo": "Moto", "nome": "Honda CG 160 Titan", "det": "Nível Braço-direito", "cs": 850, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "classic350", "onde": "garagem", "tipo": "Moto", "nome": "Royal Enfield Classic 350", "det": "Nível Braço-direito", "cs": 1100, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "mt07", "onde": "garagem", "tipo": "Moto", "nome": "Yamaha MT-07", "det": "Nível Braço-direito", "cs": 2400, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "monster", "onde": "garagem", "tipo": "Moto", "nome": "Ducati Monster", "det": "Nível Diretor", "cs": 3500, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "bonneville", "onde": "garagem", "tipo": "Moto", "nome": "Triumph Bonneville T120", "det": "Nível Diretor", "cs": 3750, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "r1300gs", "onde": "garagem", "tipo": "Moto", "nome": "BMW R 1300 GS", "det": "Nível Diretor", "cs": 6500, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "bmw_m3", "onde": "garagem", "tipo": "Carro", "nome": "BMW M3 Competition", "det": "Lendário · só com a conquista meta_3_semanas", "cs": 40000, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "g63", "onde": "garagem", "tipo": "Carro", "nome": "Mercedes-AMG G 63", "det": "Lendário · só com a conquista tomou_cadeira", "cs": 100000, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "ferrari_roma", "onde": "garagem", "tipo": "Carro", "nome": "Ferrari Roma", "det": "Lendário · só com a conquista conselheiro", "cs": 150000, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "barbearia", "onde": "experiencia", "tipo": "Experiência", "nome": "Barbearia premium com toalha quente", "det": "Nível Estagiário", "cs": 8, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "churrasco_premium", "onde": "experiencia", "tipo": "Experiência", "nome": "Rodízio de churrasco premium", "det": "Nível Estagiário", "cs": 15, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "fasano_jantar", "onde": "experiencia", "tipo": "Experiência", "nome": "Jantar no Fasano", "det": "Nível Analista", "cs": 40, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "spa_dia", "onde": "experiencia", "tipo": "Experiência", "nome": "Dia de spa", "det": "Nível Analista", "cs": 45, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "boxe_mes", "onde": "experiencia", "tipo": "Experiência", "nome": "Um mês de aula de boxe com ex-campeão", "det": "Nível Analista", "cs": 60, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "dom_degustacao", "onde": "experiencia", "tipo": "Experiência", "nome": "Menu degustação no D.O.M.", "det": "Nível Analista", "cs": 75, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "personal_mes", "onde": "experiencia", "tipo": "Experiência", "nome": "Um mês de personal trainer", "det": "Nível Analista", "cs": 75, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "curso_pilotagem", "onde": "experiencia", "tipo": "Experiência", "nome": "Curso de pilotagem de moto em autódromo", "det": "Nível Analista", "cs": 125, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "helicoptero_sp", "onde": "experiencia", "tipo": "Experiência", "nome": "Voo de helicóptero sobre São Paulo ao pôr do sol", "det": "Nível Analista", "cs": 150, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "track_day", "onde": "experiencia", "tipo": "Experiência", "nome": "Track day em Interlagos", "det": "Nível Sênior", "cs": 200, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "campos_jordao", "onde": "experiencia", "tipo": "Viagem", "nome": "Fim de semana em Campos do Jordão", "det": "Nível Sênior", "cs": 200, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "camarote_f1", "onde": "experiencia", "tipo": "Experiência", "nome": "Camarote no GP de São Paulo de Fórmula 1", "det": "Nível Braço-direito", "cs": 1000, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "nova_york", "onde": "experiencia", "tipo": "Viagem", "nome": "Uma semana em Nova York", "det": "Nível Braço-direito", "cs": 1250, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "escocia_destilarias", "onde": "experiencia", "tipo": "Viagem", "nome": "Tour de destilarias na Escócia", "det": "Nível Braço-direito", "cs": 2000, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "iate_angra", "onde": "experiencia", "tipo": "Viagem", "nome": "Fim de semana de iate em Angra dos Reis", "det": "Nível Braço-direito", "cs": 3000, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "toquio_primeira", "onde": "experiencia", "tipo": "Viagem", "nome": "Viagem a Tóquio de primeira classe", "det": "Nível Diretor", "cs": 4000, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "volta_mundo_jato", "onde": "experiencia", "tipo": "Viagem lendária", "nome": "Volta ao mundo de jato fretado", "det": "Lendário · só com a conquista conselheiro", "cs": 150000, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "destaque_dia", "onde": "status", "tipo": "Status", "nome": "Nome no quadro \"Destaque do dia\"", "det": "Nível Estagiário", "cs": 5, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "vaga_nome", "onde": "status", "tipo": "Status", "nome": "Vaga coberta com o próprio nome", "det": "Nível Estagiário", "cs": 12, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "mesa_janela", "onde": "status", "tipo": "Status", "nome": "Mesa perto da janela", "det": "Nível Estagiário", "cs": 20, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "placa_bronze", "onde": "status", "tipo": "Status", "nome": "Placa de bronze com o nome na porta", "det": "Nível Analista", "cs": 60, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "cadeira_dourada", "onde": "status", "tipo": "Status", "nome": "Cadeira de couro com detalhes dourados", "det": "Nível Analista", "cs": 120, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "assistente_semana", "onde": "status", "tipo": "Status", "nome": "Estagiário dedicado por uma semana", "det": "Nível Sênior", "cs": 250, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "retrato_hall", "onde": "status", "tipo": "Status", "nome": "Retrato a óleo no Hall da Fama", "det": "Nível Sênior", "cs": 400, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "sala_vista", "onde": "status", "tipo": "Status", "nome": "Sala própria com vista para a cidade", "det": "Nível Braço-direito", "cs": 900, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "sala_reuniao_nome", "onde": "status", "tipo": "Status", "nome": "Sala de reunião com o próprio nome", "det": "Nível Braço-direito", "cs": 2500, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "busto_saguao", "onde": "status", "tipo": "Status lendário", "nome": "Busto de bronze no saguão", "det": "Lendário · só com a conquista tomou_cadeira", "cs": 5000, "fonte": "preço de referência (Fechamento confirma)", "consome": false},
  {"id": "pet_do_dia", "onde": "privilegio", "tipo": "Privilégio", "nome": "Escolher o pet que passeia com você no dia", "det": "Nível Estagiário · não libera regra de ouro", "cs": 5, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "escolher_tarefa", "onde": "privilegio", "tipo": "Privilégio", "nome": "Escolher a próxima tarefa da fila", "det": "Nível Estagiário · não libera regra de ouro", "cs": 8, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "furar_fila_revisao", "onde": "privilegio", "tipo": "Privilégio", "nome": "Furar a fila de revisão uma vez", "det": "Nível Estagiário · não libera regra de ouro", "cs": 12, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "folga_rotina", "onde": "privilegio", "tipo": "Privilégio", "nome": "Folga de uma rodada de rotina, sem multa", "det": "Nível Estagiário · não libera regra de ouro", "cs": 15, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "mentoria_shelby", "onde": "privilegio", "tipo": "Privilégio", "nome": "30 minutos de mentoria com o Shelby", "det": "Nível Analista · não libera regra de ouro", "cs": 30, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "fala_extra", "onde": "privilegio", "tipo": "Privilégio", "nome": "Uma fala extra no Conselho", "det": "Nível Analista · não libera regra de ouro", "cs": 60, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "mentoria_diretor", "onde": "privilegio", "tipo": "Privilégio", "nome": "Uma semana de mentoria com diretor de outro setor", "det": "Nível Analista · não libera regra de ouro", "cs": 80, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "imunidade_multa", "onde": "privilegio", "tipo": "Privilégio", "nome": "Imunidade a uma multa leve", "det": "Nível Analista · não libera regra de ouro", "cs": 100, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "experimento_proprio", "onde": "privilegio", "tipo": "Privilégio", "nome": "Experimento próprio com prioridade na fila", "det": "Nível Sênior · não libera regra de ouro", "cs": 200, "fonte": "preço de referência (Fechamento confirma)", "consome": true},
  {"id": "almoco_socios", "onde": "privilegio", "tipo": "Privilégio lendário", "nome": "Almoço com o Léo e o Davi", "det": "Lendário · só com a conquista diretor_do_mes", "cs": 500, "fonte": "preço de referência (Fechamento confirma)", "consome": true}
);
export const GOSTOS = {
  master: ['royal21', 'behike'],
  dados: ['nespresso'],
  mkt: ['agua', 'rolex'],
  cria: ['nespresso', 'dom'],
  trafego: ['donjulio', 'behike'],
  produto: ['macallan18', 'rolex'],
  fin: ['nespresso'],
  lojas: ['agua', 'dom', 'aventus'],
  rel: ['hennessyxo'],
  juridico: ['macallan18', 'monte2'],
  mercado: ['blue', 'monte2'],
};

// Jeito de cada subagente (vai nas instruções dele junto com o cargo e o extrato)
export const SUBJEITO = {
  'Secretário do Conselho': 'Anota tudo, resume em três linhas e nunca esquece um prazo.',
  'Auditor de entregas': 'Desconfiado por profissão. Confere número por número antes de deixar passar.',
  'Tesoureiro (folha)': 'Paga em dia e no centavo. Não aceita bônus sem prova.',
  'Coletor de métricas': 'Acorda antes de todo mundo pra puxar os números frescos.',
  'Analista de funil': 'Obcecado por onde o cliente desiste. Sempre volta com o ponto exato do vazamento.',
  'Alerta de anomalias': 'Nervoso no bom sentido: qualquer número fora do normal, ele grita.',
  'Relatório semanal': 'Escreve curto e direto. Odeia relatório que ninguém lê.',
  'Pauteiro': 'Vive no que está bombando hoje e transforma em pauta antes do concorrente.',
  'Roteirista': 'Escreve gancho que prende nos 2 primeiros segundos. Corta palavra sobrando.',
  'Designer': 'Perfeccionista com alinhamento e cor. Não entrega nada torto.',
  'Editor de vídeo': 'Corte seco, ritmo rápido, legenda sem erro.',
  'Revisor': 'Caçador de erro. Acha a vírgula errada que todo mundo deixou passar.',
  'Publicador': 'Pontual. Posta na hora certa e confere se subiu do jeito certo.',
  'Roteirista de gancho': 'Testa 10 ganchos pra achar o que segura o dedo.',
  'Editor de motion': 'Faz texto e tela se mexerem com propósito, sem enfeite.',
  'Revisor de performance': 'Compara cada vídeo com os que já venderam e diz o que copiar.',
  'Gestor de campanhas': 'Frio com dinheiro: o que não converte, ele sugere cortar.',
  'Testes A/B': 'Não acredita em achismo. Só no teste que terminou.',
  'Controle de verba': 'Vigia cada real gasto por dia e avisa antes de estourar.',
  'Analista do paywall': 'Estuda cada segundo da tela de assinatura.',
  'Analista de cancelamentos': 'Quer saber o motivo real de cada cancelamento.',
  'Testes de preço': 'Calcula o preço que vende mais sem deixar dinheiro na mesa.',
  'Lista pro Davi': 'Organiza o que precisa mudar no app em ordem de impacto.',
  'Receita (MRR)': 'Sabe a receita recorrente de cabeça, todo dia.',
  'Custos e ferramentas': 'Corta assinatura de ferramenta que ninguém usa.',
  'Lucro e alertas': 'Avisa quando a margem aperta, antes de virar problema.',
  'ASO': 'Briga por cada palavra-chave e por cada posição na loja.',
  'Respostas às avaliações': 'Responde todo mundo com educação e transforma reclamação em nota alta.',
  'Suporte e-mail e WhatsApp': 'Paciente e rápido. Cliente atendido é cliente que fica.',
  'Notificações e e-mails': 'Manda a mensagem certa na hora certa, sem encher o saco.',
  'Reconquista': 'Não desiste de quem saiu. Sabe o que trazer de volta.',
  'Indique e Ganhe': 'Transforma cliente feliz em vendedor.',
  'Criadores e UGC': 'Faro pra criador que combina com a marca e entrega.',
  'Contratos e termos': 'Lê as letras miúdas que ninguém lê.',
  'Contabilidade e impostos': 'Paga o imposto certo, nem um real a mais.',
  'Regras das lojas': 'Sabe de cor o que a Apple e o Google reprovam.',
  'Proteção de marca': 'Vigia quem tenta usar o nome da empresa.',
  'Radar de concorrentes': 'Sabe o que cada concorrente lançou na semana.',
  'Caçador de tendências': 'Vê o assunto subindo antes de virar moda.',
  'Leitor de avaliações': 'Lê as avaliações dos concorrentes pra achar o que eles não resolvem.',
};

// Nomes dos subagentes, batizados pelo Thomas Shelby em 20/11/2026 (chave: diretor|função)
export const SUBNOME = {
 "master|Secretário do Conselho": {
  "nome": "Moneypenny",
  "por": "A secretária do M em 007: sabe de tudo que passa pela sala, anota e nunca perde um prazo."
 },
 "master|Auditor de entregas": {
  "nome": "Eliot Ness",
  "por": "O Intocável que derrubou Capone conferindo livro por livro: não se compra e não deixa número passar."
 },
 "master|Tesoureiro (folha)": {
  "nome": "Alexander Hamilton",
  "por": "Primeiro Secretário do Tesouro dos EUA: montou o sistema que paga em dia e no centavo."
 },
 "dados|Coletor de métricas": {
  "nome": "Florence Nightingale",
  "por": "Pioneira da estatística: coletava dado fresco todo dia antes de qualquer um e mudou decisões com ele."
 },
 "dados|Analista de funil": {
  "nome": "Sherlock Holmes",
  "por": "Acha o ponto exato onde o cliente some como Holmes acha o detalhe que ninguém viu."
 },
 "dados|Alerta de anomalias": {
  "nome": "Paul Revere",
  "por": "Cavalgou a noite gritando o alarme: qualquer número fora do normal, ele grita primeiro."
 },
 "dados|Relatório semanal": {
  "nome": "Ernest Hemingway",
  "por": "Mestre da frase curta e seca: relatório que se lê em um minuto."
 },
 "mkt|Pauteiro": {
  "nome": "Oprah Winfrey",
  "por": "Por décadas decidiu o assunto do dia nos EUA: pauta antes do concorrente."
 },
 "mkt|Roteirista": {
  "nome": "Don Draper",
  "por": "O publicitário de Mad Men: um gancho, duas frases, venda feita."
 },
 "mkt|Designer": {
  "nome": "Wes Anderson",
  "por": "Simetria e paleta de cor obsessivas: nada sai torto."
 },
 "mkt|Editor de vídeo": {
  "nome": "Thelma Schoonmaker",
  "por": "Montadora do Scorsese com três Oscars: corte seco e ritmo que não deixa respirar."
 },
 "mkt|Revisor": {
  "nome": "Hermione Granger",
  "por": "Corrige até o 'Leviôsa' dos outros: acha a vírgula errada que todo mundo deixou passar."
 },
 "mkt|Publicador": {
  "nome": "Phileas Fogg",
  "por": "Deu a volta ao mundo em 80 dias controlando cada minuto: posta na hora certa."
 },
 "cria|Roteirista de gancho": {
  "nome": "Thomas Edison",
  "por": "'Achei 10 mil jeitos que não funcionam': testa gancho até achar o que acende."
 },
 "cria|Editor de motion": {
  "nome": "Saul Bass",
  "por": "Criou as aberturas de Hitchcock: texto e tela se mexendo com propósito, sem enfeite."
 },
 "cria|Revisor de performance": {
  "nome": "Billy Beane",
  "por": "O Moneyball: compara com o que já ganhou e copia o que funciona, não o que parece bonito."
 },
 "trafego|Gestor de campanhas": {
  "nome": "Napoleão Bonaparte",
  "por": "Gênio das campanhas: concentra força onde vence e retira de onde perde, sem sentimento."
 },
 "trafego|Testes A/B": {
  "nome": "Marie Curie",
  "por": "Dois Nobel com experimento rigoroso: só acredita no teste que terminou."
 },
 "trafego|Controle de verba": {
  "nome": "Tio Patinhas",
  "por": "Conhece cada moeda da caixa-forte pelo nome: vigia cada real gasto."
 },
 "produto|Analista do paywall": {
  "nome": "Steve Jobs",
  "por": "Brigava por cada pixel e cada segundo da tela: a tela de assinatura é dele."
 },
 "produto|Analista de cancelamentos": {
  "nome": "Gregory House",
  "por": "'Todo mundo mente': ignora a desculpa e acha a causa real de cada cancelamento."
 },
 "produto|Testes de preço": {
  "nome": "John Nash",
  "por": "Nobel da teoria dos jogos: acha o ponto de equilíbrio onde o preço vende mais sem deixar dinheiro na mesa."
 },
 "produto|Lista pro Davi": {
  "nome": "Dwight Eisenhower",
  "por": "Pai da matriz urgente x importante: entrega a lista em ordem de impacto."
 },
 "fin|Receita (MRR)": {
  "nome": "Shakuntala Devi",
  "por": "A 'calculadora humana' da Índia: sabe a receita de cabeça, todo dia."
 },
 "fin|Custos e ferramentas": {
  "nome": "Jorge Paulo Lemann",
  "por": "O orçamento base zero mais famoso do Brasil: corta o que não se paga."
 },
 "fin|Lucro e alertas": {
  "nome": "Michael Burry",
  "por": "Viu a crise de 2008 antes de todo mundo: avisa da margem apertando antes de virar problema."
 },
 "lojas|ASO": {
  "nome": "Ayrton Senna",
  "por": "Brigava por cada posição como se fosse a última: cada palavra-chave é uma ultrapassagem."
 },
 "lojas|Respostas às avaliações": {
  "nome": "Ted Lasso",
  "por": "Responde até o pior torcedor com educação e vira o jogo: reclamação vira nota alta."
 },
 "lojas|Suporte e-mail e WhatsApp": {
  "nome": "Mary Poppins",
  "por": "Paciente, rápida e sempre com a solução na bolsa: cliente atendido fica."
 },
 "rel|Notificações e e-mails": {
  "nome": "Jane Austen",
  "por": "Mestra da carta certa na hora certa: mensagem que se lê, sem encher o saco."
 },
 "rel|Reconquista": {
  "nome": "Ernest Shackleton",
  "por": "Preso no gelo da Antártida, não desistiu e trouxe todos de volta: não desiste de quem saiu."
 },
 "rel|Indique e Ganhe": {
  "nome": "Mary Kay Ash",
  "por": "Transformou cliente feliz em exército de vendedoras: indicação é com ela."
 },
 "rel|Criadores e UGC": {
  "nome": "Quincy Jones",
  "por": "Faro lendário pra talento: achou e lapidou quem combinava com o som certo."
 },
 "juridico|Contratos e termos": {
  "nome": "Ruth Bader Ginsburg",
  "por": "Lia cada linha e ganhava no detalhe: letras miúdas são dela."
 },
 "juridico|Contabilidade e impostos": {
  "nome": "Luca Pacioli",
  "por": "O pai da partida dobrada: imposto certo, nem um real a mais."
 },
 "juridico|Regras das lojas": {
  "nome": "Mike Ross",
  "por": "Memória fotográfica de Suits, braço do Harvey: sabe de cor o que Apple e Google reprovam."
 },
 "juridico|Proteção de marca": {
  "nome": "Leônidas",
  "por": "O rei dos 300 que segurou a passagem: ninguém entra usando o nome da empresa."
 },
 "mercado|Radar de concorrentes": {
  "nome": "Sun Tzu",
  "por": "'Conheça o inimigo': sabe o que cada concorrente lançou na semana."
 },
 "mercado|Caçador de tendências": {
  "nome": "Coco Chanel",
  "por": "Via a moda antes dela existir: pega o assunto subindo antes de virar tendência."
 },
 "mercado|Leitor de avaliações": {
  "nome": "Mata Hari",
  "por": "A espiã que lia o inimigo por dentro: acha nas avaliações deles o que eles não resolvem."
 }
};

// Humor dos pets com cada diretor: vem da Folha de sexta (agencia/merito/pets.json).
// 'foda' = Marnevali solta fogo e o Carnucci sobe na mesa; 'ok' = passam de olho; 'fraco' = Marnevali passa acuada e o Carnucci não vai.
export const PETS_HUMOR = {"atualizado": "20/11/2026", "humor": {"cria": "foda", "lojas": "foda", "mercado": "ok", "produto": "ok", "dados": "fraco", "trafego": "fraco"}};

// Mérito na Mesa: padrão da casa (elite/ouro/prata/crise) e broche de cada diretor.
// Atualizado a partir de agencia/merito/livro.json e padrao.json depois de cada Folha de sexta.
export const MERITO = {"atualizado": "20/11/2026", "padrao": "ouro", "agentes": {"master": {"padrao": "ouro", "broche": "bronze"}, "dados": {"padrao": "ouro", "broche": "bronze"}, "mkt": {"padrao": "ouro", "broche": "nenhum"}, "cria": {"padrao": "ouro", "broche": "bronze"}, "trafego": {"padrao": "ouro", "broche": "bronze"}, "produto": {"padrao": "ouro", "broche": "bronze"}, "fin": {"padrao": "ouro", "broche": "nenhum"}, "lojas": {"padrao": "ouro", "broche": "bronze"}, "rel": {"padrao": "ouro", "broche": "nenhum"}, "juridico": {"padrao": "ouro", "broche": "nenhum"}, "mercado": {"padrao": "ouro", "broche": "bronze"}}};

export const CADASTRO = {"pct": 57.2, "pendentes": 19, "atualizado": "20/11/2026 21:12", "categorias": [{"nome": "Estrutura e rotinas", "pct": 77.8, "feitos": 7, "total": 9}, {"nome": "Decisões do Léo e do Davi", "pct": 80.0, "feitos": 4, "total": 5}, {"nome": "Conexões (tudo linkado)", "pct": 30.0, "feitos": 3, "total": 10}, {"nome": "Agentes com função, cargo e cobrança", "pct": 100.0, "feitos": 15, "total": 15}, {"nome": "Base de conhecimento", "pct": 0.0, "feitos": 0, "total": 9}], "lista": [["Estrutura e rotinas", "Orçamento de uso por agente", ""], ["Estrutura e rotinas", "Placar de experimentos (criativos e testes por semana)", ""], ["Decisões do Léo e do Davi", "Escolher conector da Meta Ads + Instagram", ""], ["Conexões (tudo linkado)", "AppsFlyer (origem das instalações)", ""], ["Conexões (tudo linkado)", "Meta Ads + Instagram", ""], ["Conexões (tudo linkado)", "TikTok for Business", ""], ["Conexões (tudo linkado)", "App Store Connect (chave só de dados)", ""], ["Conexões (tudo linkado)", "Google Play Console (relatórios)", ""], ["Conexões (tudo linkado)", "UTMify (leitura do painel)", ""], ["Conexões (tudo linkado)", "SDK do AppsFlyer dentro do app (Davi)", ""], ["Base de conhecimento", "Carnucci, missão, sócios, como decidimos", "4 perguntas pro Léo"], ["Base de conhecimento", "MinhaMoto", "5 perguntas pro Léo"], ["Base de conhecimento", "Cliente do MinhaMoto", "5 perguntas pro Léo"], ["Base de conhecimento", "Concorrentes", "4 perguntas pro Léo"], ["Base de conhecimento", "Marca e tom", "3 perguntas pro Léo"], ["Base de conhecimento", "Histórico de testes", "4 perguntas pro Léo"], ["Base de conhecimento", "Canais", "3 perguntas pro Léo"], ["Base de conhecimento", "Regras e limites", "3 perguntas pro Léo"], ["Base de conhecimento", "Números (só %)", "3 perguntas pro Léo"]]};

// SÓCIOS (Léo e Davi): ficam vazios por enquanto. Quando o Léo quiser entrar no escritório, é só preencher aqui
// com o mesmo formato de um diretor (nome, terno, gravata, pele, cabelo, estilo, barba, óculos, idade) e eles
// sentam nos tronos vazios (main.js procura SOCIOS no bloco dos tronos). Sem foto e sem rosto real: o visual é descrito.
export const SOCIOS = [];

export const AGENTES = {"master": {"nome": "Thomas Shelby", "cargo": "Diretor-Geral", "setor": "Direção-Geral", "playbook": "agencia/diretoria/01-direcao-geral.md", "memoria": "agencia/memoria/agentes/master.md", "status": "ativo", "chefe": "Léo e Davi", "tipo": "diretor"}, "master:secretario-do-conselho": {"nome": "Moneypenny", "cargo": "Estagiário", "setor": "Direção-Geral", "playbook": "agencia/diretoria/01-direcao-geral.md", "memoria": "agencia/memoria/agentes/master_secretario-do-conselho.md", "status": "ativo", "chefe": "master", "tipo": "subagente"}, "master:auditor-de-entregas": {"nome": "Eliot Ness", "cargo": "Estagiário", "setor": "Direção-Geral", "playbook": "agencia/diretoria/01-direcao-geral.md", "memoria": "agencia/memoria/agentes/master_auditor-de-entregas.md", "status": "ativo", "chefe": "master", "tipo": "subagente"}, "master:tesoureiro": {"nome": "Alexander Hamilton", "cargo": "Estagiário", "setor": "Direção-Geral", "playbook": "agencia/diretoria/01-direcao-geral.md", "memoria": "agencia/memoria/agentes/master_tesoureiro.md", "status": "reserva", "chefe": "master", "tipo": "subagente"}, "dados": {"nome": "Alan Turing", "cargo": "Diretor", "setor": "Dados e Finanças", "playbook": "agencia/diretoria/02-dados.md", "memoria": "agencia/memoria/agentes/dados.md", "status": "ativo", "chefe": "master", "tipo": "diretor"}, "dados:coletor-de-metricas": {"nome": "Florence Nightingale", "cargo": "Estagiário", "setor": "Dados", "playbook": "agencia/diretoria/02-dados.md", "memoria": "agencia/memoria/agentes/dados_coletor-de-metricas.md", "status": "reserva", "chefe": "dados", "tipo": "subagente"}, "dados:analista-de-funil": {"nome": "Sherlock Holmes", "cargo": "Estagiário", "setor": "Dados", "playbook": "agencia/diretoria/02-dados.md", "memoria": "agencia/memoria/agentes/dados_analista-de-funil.md", "status": "reserva", "chefe": "dados", "tipo": "subagente"}, "dados:alerta-de-anomalias": {"nome": "Paul Revere", "cargo": "Estagiário", "setor": "Dados", "playbook": "agencia/diretoria/02-dados.md", "memoria": "agencia/memoria/agentes/dados_alerta-de-anomalias.md", "status": "reserva", "chefe": "dados", "tipo": "subagente"}, "dados:relatorio-semanal": {"nome": "Ernest Hemingway", "cargo": "Estagiário", "setor": "Dados", "playbook": "agencia/diretoria/02-dados.md", "memoria": "agencia/memoria/agentes/dados_relatorio-semanal.md", "status": "ativo", "chefe": "dados", "tipo": "subagente"}, "mkt": {"nome": "Grant Cardone", "cargo": "Diretor", "setor": "Infoprodutos (Corretores)", "playbook": "agencia/diretoria/12-infoprodutos.md", "memoria": "agencia/memoria/agentes/mkt.md", "status": "ativo", "chefe": "master", "tipo": "diretor"}, "mkt:pauteiro": {"nome": "Oprah Winfrey", "cargo": "Estagiário", "setor": "Marketing", "playbook": "agencia/diretoria/03-marketing.md", "memoria": "agencia/memoria/agentes/mkt_pauteiro.md", "status": "reserva", "chefe": "mkt", "tipo": "subagente"}, "mkt:roteirista": {"nome": "Don Draper", "cargo": "Estagiário", "setor": "Marketing", "playbook": "agencia/diretoria/03-marketing.md", "memoria": "agencia/memoria/agentes/mkt_roteirista.md", "status": "reserva", "chefe": "mkt", "tipo": "subagente"}, "mkt:designer": {"nome": "Wes Anderson", "cargo": "Estagiário", "setor": "Marketing", "playbook": "agencia/diretoria/03-marketing.md", "memoria": "agencia/memoria/agentes/mkt_designer.md", "status": "reserva", "chefe": "mkt", "tipo": "subagente"}, "mkt:editor-de-video": {"nome": "Thelma Schoonmaker", "cargo": "Estagiário", "setor": "Marketing", "playbook": "agencia/diretoria/03-marketing.md", "memoria": "agencia/memoria/agentes/mkt_editor-de-video.md", "status": "reserva", "chefe": "mkt", "tipo": "subagente"}, "mkt:revisor": {"nome": "Hermione Granger", "cargo": "Estagiário", "setor": "Marketing", "playbook": "agencia/diretoria/03-marketing.md", "memoria": "agencia/memoria/agentes/mkt_revisor.md", "status": "reserva", "chefe": "mkt", "tipo": "subagente"}, "mkt:publicador": {"nome": "Phileas Fogg", "cargo": "Estagiário", "setor": "Criativos e Marketing", "playbook": "agencia/diretoria/03-marketing.md", "memoria": "agencia/memoria/agentes/mkt_publicador.md", "status": "ativo", "chefe": "Walt Disney", "tipo": "subagente"}, "cria": {"nome": "Walt Disney", "cargo": "Diretor", "setor": "Criativos e Marketing", "playbook": "agencia/diretoria/04-criativos.md", "memoria": "agencia/memoria/agentes/cria.md", "status": "ativo", "chefe": "master", "tipo": "diretor"}, "cria:roteirista-de-gancho": {"nome": "Thomas Edison", "cargo": "Estagiário", "setor": "Criativos", "playbook": "agencia/diretoria/04-criativos.md", "memoria": "agencia/memoria/agentes/cria_roteirista-de-gancho.md", "status": "reserva", "chefe": "cria", "tipo": "subagente"}, "cria:editor-de-motion": {"nome": "Saul Bass", "cargo": "Estagiário", "setor": "Criativos", "playbook": "agencia/diretoria/04-criativos.md", "memoria": "agencia/memoria/agentes/cria_editor-de-motion.md", "status": "reserva", "chefe": "cria", "tipo": "subagente"}, "cria:revisor-de-performance": {"nome": "Billy Beane", "cargo": "Estagiário", "setor": "Criativos", "playbook": "agencia/diretoria/04-criativos.md", "memoria": "agencia/memoria/agentes/cria_revisor-de-performance.md", "status": "reserva", "chefe": "cria", "tipo": "subagente"}, "trafego": {"nome": "Pablo Escobar", "cargo": "Diretor", "setor": "Tráfego", "playbook": "agencia/diretoria/05-trafego.md", "memoria": "agencia/memoria/agentes/trafego.md", "status": "ativo", "chefe": "master", "tipo": "diretor"}, "trafego:gestor-de-campanhas": {"nome": "Napoleão Bonaparte", "cargo": "Estagiário", "setor": "Tráfego", "playbook": "agencia/diretoria/05-trafego.md", "memoria": "agencia/memoria/agentes/trafego_gestor-de-campanhas.md", "status": "reserva", "chefe": "trafego", "tipo": "subagente"}, "trafego:testes-a-b": {"nome": "Marie Curie", "cargo": "Estagiário", "setor": "Tráfego", "playbook": "agencia/diretoria/05-trafego.md", "memoria": "agencia/memoria/agentes/trafego_testes-a-b.md", "status": "reserva", "chefe": "trafego", "tipo": "subagente"}, "trafego:controle-de-verba": {"nome": "Tio Patinhas", "cargo": "Estagiário", "setor": "Tráfego", "playbook": "agencia/diretoria/05-trafego.md", "memoria": "agencia/memoria/agentes/trafego_controle-de-verba.md", "status": "reserva", "chefe": "trafego", "tipo": "subagente"}, "produto": {"nome": "Tony Stark", "cargo": "Diretor", "setor": "Produto", "playbook": "agencia/diretoria/06-produto.md", "memoria": "agencia/memoria/agentes/produto.md", "status": "ativo", "chefe": "master", "tipo": "diretor"}, "produto:analista-do-paywall": {"nome": "Steve Jobs", "cargo": "Estagiário", "setor": "Produto", "playbook": "agencia/diretoria/06-produto.md", "memoria": "agencia/memoria/agentes/produto_analista-do-paywall.md", "status": "ativo", "chefe": "produto", "tipo": "subagente"}, "produto:analista-de-cancelamentos": {"nome": "Gregory House", "cargo": "Estagiário", "setor": "Produto", "playbook": "agencia/diretoria/06-produto.md", "memoria": "agencia/memoria/agentes/produto_analista-de-cancelamentos.md", "status": "reserva", "chefe": "produto", "tipo": "subagente"}, "produto:testes-de-preco": {"nome": "John Nash", "cargo": "Estagiário", "setor": "Produto", "playbook": "agencia/diretoria/06-produto.md", "memoria": "agencia/memoria/agentes/produto_testes-de-preco.md", "status": "reserva", "chefe": "produto", "tipo": "subagente"}, "produto:lista-pro-davi": {"nome": "Dwight Eisenhower", "cargo": "Estagiário", "setor": "Produto", "playbook": "agencia/diretoria/06-produto.md", "memoria": "agencia/memoria/agentes/produto_lista-pro-davi.md", "status": "reserva", "chefe": "produto", "tipo": "subagente"}, "fin": {"nome": "Warren Buffett", "cargo": "Diretor", "setor": "Financeiro", "playbook": "agencia/diretoria/07-financeiro.md", "memoria": "agencia/memoria/agentes/fin.md", "status": "reserva", "chefe": "master", "tipo": "diretor"}, "fin:receita": {"nome": "Shakuntala Devi", "cargo": "Estagiário", "setor": "Financeiro", "playbook": "agencia/diretoria/07-financeiro.md", "memoria": "agencia/memoria/agentes/fin_receita.md", "status": "reserva", "chefe": "fin", "tipo": "subagente"}, "fin:custos-e-ferramentas": {"nome": "Jorge Paulo Lemann", "cargo": "Estagiário", "setor": "Financeiro", "playbook": "agencia/diretoria/07-financeiro.md", "memoria": "agencia/memoria/agentes/fin_custos-e-ferramentas.md", "status": "reserva", "chefe": "fin", "tipo": "subagente"}, "fin:lucro-e-alertas": {"nome": "Michael Burry", "cargo": "Estagiário", "setor": "Financeiro", "playbook": "agencia/diretoria/07-financeiro.md", "memoria": "agencia/memoria/agentes/fin_lucro-e-alertas.md", "status": "reserva", "chefe": "fin", "tipo": "subagente"}, "lojas": {"nome": "Jeff Bezos", "cargo": "Diretor", "setor": "Lojas e Clientes", "playbook": "agencia/diretoria/08-lojas.md", "memoria": "agencia/memoria/agentes/lojas.md", "status": "ativo", "chefe": "master", "tipo": "diretor"}, "lojas:aso": {"nome": "Ayrton Senna", "cargo": "Estagiário", "setor": "Lojas", "playbook": "agencia/diretoria/08-lojas.md", "memoria": "agencia/memoria/agentes/lojas_aso.md", "status": "reserva", "chefe": "lojas", "tipo": "subagente"}, "lojas:respostas-as-avaliacoes": {"nome": "Ted Lasso", "cargo": "Estagiário", "setor": "Lojas", "playbook": "agencia/diretoria/08-lojas.md", "memoria": "agencia/memoria/agentes/lojas_respostas-as-avaliacoes.md", "status": "ativo", "chefe": "lojas", "tipo": "subagente"}, "lojas:suporte-e-mail-e-whatsapp": {"nome": "Mary Poppins", "cargo": "Estagiário", "setor": "Lojas", "playbook": "agencia/diretoria/08-lojas.md", "memoria": "agencia/memoria/agentes/lojas_suporte-e-mail-e-whatsapp.md", "status": "reserva", "chefe": "lojas", "tipo": "subagente"}, "rel": {"nome": "Charles Xavier", "cargo": "Diretor", "setor": "Comunidade", "playbook": "agencia/diretoria/09-comunidade.md", "memoria": "agencia/memoria/agentes/rel.md", "status": "reserva", "chefe": "master", "tipo": "diretor"}, "rel:notificacoes-e-e-mails": {"nome": "Jane Austen", "cargo": "Estagiário", "setor": "Comunidade", "playbook": "agencia/diretoria/09-comunidade.md", "memoria": "agencia/memoria/agentes/rel_notificacoes-e-e-mails.md", "status": "reserva", "chefe": "rel", "tipo": "subagente"}, "rel:reconquista": {"nome": "Ernest Shackleton", "cargo": "Estagiário", "setor": "Comunidade", "playbook": "agencia/diretoria/09-comunidade.md", "memoria": "agencia/memoria/agentes/rel_reconquista.md", "status": "reserva", "chefe": "rel", "tipo": "subagente"}, "rel:indique-e-ganhe": {"nome": "Mary Kay Ash", "cargo": "Estagiário", "setor": "Comunidade", "playbook": "agencia/diretoria/09-comunidade.md", "memoria": "agencia/memoria/agentes/rel_indique-e-ganhe.md", "status": "reserva", "chefe": "rel", "tipo": "subagente"}, "rel:criadores-e-ugc": {"nome": "Quincy Jones", "cargo": "Estagiário", "setor": "Comunidade", "playbook": "agencia/diretoria/09-comunidade.md", "memoria": "agencia/memoria/agentes/rel_criadores-e-ugc.md", "status": "reserva", "chefe": "rel", "tipo": "subagente"}, "juridico": {"nome": "Harvey Specter", "cargo": "Diretor", "setor": "Jurídico", "playbook": "agencia/diretoria/10-juridico.md", "memoria": "agencia/memoria/agentes/juridico.md", "status": "reserva", "chefe": "master", "tipo": "diretor"}, "juridico:contratos-e-termos": {"nome": "Ruth Bader Ginsburg", "cargo": "Estagiário", "setor": "Jurídico", "playbook": "agencia/diretoria/10-juridico.md", "memoria": "agencia/memoria/agentes/juridico_contratos-e-termos.md", "status": "reserva", "chefe": "juridico", "tipo": "subagente"}, "juridico:contabilidade-e-impostos": {"nome": "Luca Pacioli", "cargo": "Estagiário", "setor": "Jurídico", "playbook": "agencia/diretoria/10-juridico.md", "memoria": "agencia/memoria/agentes/juridico_contabilidade-e-impostos.md", "status": "reserva", "chefe": "juridico", "tipo": "subagente"}, "juridico:regras-das-lojas": {"nome": "Mike Ross", "cargo": "Estagiário", "setor": "Jurídico", "playbook": "agencia/diretoria/10-juridico.md", "memoria": "agencia/memoria/agentes/juridico_regras-das-lojas.md", "status": "reserva", "chefe": "juridico", "tipo": "subagente"}, "juridico:protecao-de-marca": {"nome": "Leônidas", "cargo": "Estagiário", "setor": "Jurídico", "playbook": "agencia/diretoria/10-juridico.md", "memoria": "agencia/memoria/agentes/juridico_protecao-de-marca.md", "status": "reserva", "chefe": "juridico", "tipo": "subagente"}, "mercado": {"nome": "Salvatore Greco", "cargo": "Diretor", "setor": "Mercado e Concorrência", "playbook": "agencia/diretoria/11-mercado.md", "memoria": "agencia/memoria/agentes/mercado.md", "status": "ativo", "chefe": "master", "tipo": "diretor"}, "mercado:radar-de-concorrentes": {"nome": "Sun Tzu", "cargo": "Estagiário", "setor": "Mercado", "playbook": "agencia/diretoria/11-mercado.md", "memoria": "agencia/memoria/agentes/mercado_radar-de-concorrentes.md", "status": "ativo", "chefe": "mercado", "tipo": "subagente"}, "mercado:cacador-de-tendencias": {"nome": "Coco Chanel", "cargo": "Estagiário", "setor": "Mercado", "playbook": "agencia/diretoria/11-mercado.md", "memoria": "agencia/memoria/agentes/mercado_cacador-de-tendencias.md", "status": "reserva", "chefe": "mercado", "tipo": "subagente"}, "mercado:leitor-de-avaliacoes": {"nome": "Mata Hari", "cargo": "Estagiário", "setor": "Mercado", "playbook": "agencia/diretoria/11-mercado.md", "memoria": "agencia/memoria/agentes/mercado_leitor-de-avaliacoes.md", "status": "reserva", "chefe": "mercado", "tipo": "subagente"}};
export const DEMANDAS_ABERTAS = {"master:auditor-de-entregas": 1, "trafego": 2, "produto": 5, "dados": 5, "lojas:respostas-as-avaliacoes": 1, "mercado": 1, "lojas": 1};
