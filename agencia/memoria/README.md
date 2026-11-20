# Memória da Carnucci

Todo agente lembra de tudo. Agente de IA não tem memória entre uma rodada e outra: a memória é o que está escrito aqui. O que não foi escrito, foi esquecido.

## O que cada agente lê ANTES de começar (sempre)
1. `agencia/memoria/decisoes.md` — tudo que o Léo e o Davi já decidiram.
2. `agencia/memoria/agentes/<id>.md` — a sua memória pessoal (troque `:` por `_` no nome do arquivo).
3. `agencia/diretoria/memoria/<setor>.md` — a memória do seu setor (pesquisas e aprendizados).
4. A ata mais recente do Conselho em `agencia/conselho/` (decisões, ordens, cobranças abertas).

## O que cada agente escreve DEPOIS de terminar (sempre)
No fim do arquivo da sua memória pessoal, uma entrada:
```
## AAAA-MM-DD HH:MM
- fiz: <o que fez, com link/arquivo>
- aprendi: <o que vale lembrar da próxima vez>
- recebi: <ordem, cobrança ou feedback de alguém, e de quem>
- pendente: <o que ficou pra próxima rodada>
```
Quando o arquivo passar de ~300 linhas, resuma as entradas antigas numa seção "Resumo até AAAA-MM-DD" no topo (sem perder decisão, feedback ou aprendizado) e apague o detalhe antigo.

## Quem escreve o quê
- `decisoes.md`: o Claude (sessão do chat com o Léo) registra toda decisão do Léo/Davi no mesmo dia; o Secretário do Conselho registra as decisões respondidas nas notificações quando o Léo responder no chat.
- Memória pessoal: o próprio agente. A Folha de sexta acrescenta o feedback da semana em cada memória (bônus, multa, promoção, motivo).
- Memória do setor: o diretor e os subagentes do setor.
- Atas: Reunião do Conselho.

## Regras
- Repositório público: nada de valores em R$ da empresa, segredo, e-mail ou dado de cliente.
- Nunca apague decisão. Se mudou, escreva a nova em cima e diga o que mudou.
- Memória é verdade: não escreva o que não aconteceu.
