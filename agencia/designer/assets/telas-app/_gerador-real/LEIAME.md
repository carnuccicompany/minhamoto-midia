# Telas REAIS do MinhaMoto: como reproduzir

São as rotas logadas `_authenticated.*`, as mesmas que o usuário vê depois do cadastro, renderizadas a partir do HEAD do repositório `minhamotooficial` (commit `05425c9` na captura de 23/11/2026). Os dados são 100% fictícios: a moto simulada "Minha Titan" (Honda CG 160 Titan 2022, 29.800 km, placa BRA2E19, dono Rafael Souza). Nenhum serviço real é chamado.

## Arquivos

| arquivo | o que é |
|---|---|
| `capturar.py` | captura com Playwright e composição (barra de status 9:41 + indicador de início) |
| `folhas.json` | pop-ups e folhas (roteiro de cliques), lido pelo `capturar.py` |
| `mock_supabase.py` | Supabase falso em memória (Auth, PostgREST, RPC, Storage) que responde ao host `https://mock-supabase.invalid` |
| `semente.ts` | gera `dados.json` (linhas de `dados_usuario`) e `local.json` (localStorage do aparelho) com as funções REAIS do app |
| `app-real.patch` | tudo o que mudou na cópia em relação ao HEAD |
| `folha.py` | gera `_folha.jpg` (miniaturas) |
| `sonda.py` | diagnóstico: abre rotas e lista requisições, console e erros |

## Passo a passo

```bash
# 1. cópia limpa (o repositório oficial nunca é tocado)
mkdir -p /tmp/app-real && cd /home/claude/minhamotooficial && git archive HEAD | tar -x -C /tmp/app-real
cd /tmp/app-real && rm -f .env                 # o .env real nem é lido
cp -al /tmp/app-previa/node_modules node_modules  # hardlinks: o cache .vite fica separado
git apply /tmp/telas-reais/_gerador/app-real.patch

# 2. vite da cópia (porta 5174; a 5173 é da prévia)
VITE_CONFIG_NATIVE_IGNORE_WARNING=true node_modules/.bin/vite dev --port 5174 --strictPort --host 127.0.0.1 &

# 3. captura (todas, ou só por prefixo: python3 capturar.py 02 21)
python3 /tmp/telas-reais/_gerador/capturar.py
python3 /tmp/telas-reais/_gerador/folha.py
```

A primeira carga do vite demora de 1 a 2 minutos (otimização de dependências), e o script espera esse tempo.

## O que o patch muda na cópia (e por quê)

1. **`.env` falso**: `VITE_SUPABASE_URL=https://mock-supabase.invalid` e uma chave inventada. O host `.invalid` nunca resolve, e o Playwright responde tudo pelo `mock_supabase.py`.
2. **`src/lib/estado-conta-cliente.ts`**: `lerLeituraEntrada()` devolve `{tipo:"livre"}` (conta sem pedido de exclusão). Na web, essa leitura é uma Server Function que consultaria o Supabase de produção.
3. **`src/routes/_authenticated.tsx`**: tira o envoltório `<AceiteLegalOficial>`. O aceite legal exige uma prova assinada (ES256) pelo servidor real, que não dá para simular sem a chave privada. As outras barreiras continuam ativas e passam com o mock: exclusão de conta, piloto, assinatura web (`ProAcessoWebOficial`) e moto principal.
4. **`src/lib/previa-fixtures.ts`**: o mesmo patch de marketing da prévia (`/tmp/telas-novas/_gerador/previa-fixtures.patch`). Só serve de fonte de dados para o `semente.ts`, que monta as linhas do banco. As rotas reais não usam a prévia.

Nenhum componente de tela foi alterado.

## O que é simulado fora do código (no navegador)

- **Sessão**: sessão Supabase fictícia gravada no localStorage (`sb-mock-supabase-auth-token`), com JWT sem assinatura válida, `session_id` e expiração em 30 dias. O usuário tem e-mail confirmado e Google vinculados.
- **Assinatura MinhaMoto Pro ativa**: a RPC `pro_producao_operacao_propria` responde `true`, e `/api/public/acesso-premium` responde `{"versao":1,"estado":"liberado","origem":"assinatura"}`.
- **Dados**: a tabela `dados_usuario` recebe as chaves `garagem`, `bike:`, `hist:`, `fuel:`, `docs:`, `docsinfo:` e `marcos:`. A média informada é de 30 km/dia.
- **Tutorial parado**: grava o mesmo estado que o botão "Parar revisão do tutorial" grava (`minhamoto-dicas:u:<uid>:<área>` com `parado:true`). Assim nenhuma dica fica por cima das telas.
- **Central de notificações**: 4 avisos já recebidos, com os textos do catálogo real (`notificacoes/textos.ts`), dos quais 2 não lidos.
- **Relógio fixo às 9:41 de hoje** (`clock.install`), coerente com a barra de status.
- **Rede**: tudo que não é `127.0.0.1:5174` é abortado. `/_serverFn` e outras rotas `/api` locais (métricas) também são abortadas. O Chrome roda com um proxy morto (`127.0.0.1:9`) e com o tráfego interno desligado.
- **Áreas seguras do iPhone 15** emuladas por CDP (`Emulation.setSafeAreaInsetsOverride`: 59 pt no topo e 34 pt embaixo). O app usa `viewport-fit=cover` e pinta essas áreas como no aparelho.

## Saída

- `/tmp/telas-reais/NN-nome.png`: 1179×2556, iPhone 393×852 @3x, pt-BR, America/Sao_Paulo.
- `/tmp/telas-reais/rolagem/NN-nome.png`: página inteira, sem a ilha de abas. Não é gerada para folhas e pop-ups.
- O script avisa (AVISOS) quando encontra um texto proibido na tela ("demonstração", "erro", "carregando"…) e mostra o trecho. Em 12-sinais o aviso é falso positivo: o trecho é "recarregando a bateria", conteúdo do manual.
