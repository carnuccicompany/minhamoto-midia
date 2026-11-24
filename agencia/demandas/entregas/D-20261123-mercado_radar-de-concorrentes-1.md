# D-20261123-mercado_radar-de-concorrentes-1: escolha da moto e plano por modelo (Stark, 24/11/2026)

Fonte: código do app (minhamotooficial, commit 05425c9, 17/11/2026, versão 1.0.1). A build de 23/11 não está no repositório; vale para o código lido.

**(1) É lista, não texto livre.** O cadastro é em 4 etapas de toque: marca (grade de 17 marcas), modelo (lista da marca, com busca), versão e ano (`src/components/garagem-home.tsx`, linhas 519-530, 735-790 e 880-900; catálogo em `src/data/bikes.ts`). Ninguém digita o nome da moto. Se o modelo não existe, aparece "Não encontrou sua moto? Solicite aqui" (e-mail ao suporte, texto do app: disponível em até 48 horas; `app-ui.tsx`, linha 446). Marca sem modelo mostra "Em breve".

**(2) Plano por modelo: 377 modelos documentados, 20 marcas no índice (Honda 54, Yamaha 42, Kawasaki 33, Suzuki 32, Triumph 27, BMW 26, Dafra 24, Shineray 23...).** Cada modelo vem de documento oficial do fabricante ("se o modelo não tem documento, ele não existe no app", `bikes.ts`). Destes, 263 arquivos trazem a tabela oficial de revisão (`cronogramaOficial`); os demais geram o cronograma pelos intervalos do documento. O plano é por km e tempo (marcos em `src/lib/revisao.ts`, tela Manutenção).

**Pode dizer no anúncio:** "escolha sua moto na lista (marca, modelo, versão e ano) e veja o plano de revisão do seu modelo". Faixa segura: "mais de 370 modelos".
**Não pode dizer:** "qualquer moto" ou "todas as motos"; "sem digitar" vale (é lista), mas existe pedido de modelo faltante. Não afirmar que os 377 têm tabela oficial (263 têm). Moto sem plano disponível: a tela do plano antes do paywall não aparece (Jobs, 22/11).
**Limite:** o catálogo pode ser carregado em parte pela rede (`catalogo?.indices`); o 377 é o do código embarcado. Se a build de 23/11 mudou, a pergunta 7 do pacote do Davi cobre.
