
## Extra: token da Meta ficou no histórico do repositório público
- o quê: `git grep access_token=` acha 2 ocorrências no commit 35f294d (dados/insights-2026-11-23.json); HEAD está limpo desde 178b0ba.
- prova: `git grep -c "access_token=" 35f294d` = 2; `git grep -c "access_token=" HEAD` = 0.
- risco: qualquer pessoa pode ler o token no histórico até ele ser revogado (só o Léo faz). Sugestão: revogar/trocar o token e conferir que a trava do insights.py cobre o campo `paging` e `next`.
