// Sala de comando: clicar num agente → conversar com ele no Claude, passar demanda ou deixar observação.
// Tudo vira uma sessão do Claude já com os repositórios da empresa; é lá que a demanda/observação é gravada.
import { AGENTES, DEMANDAS_ABERTAS } from './data.js';

const REPOS = 'carnuccicompany/minhamoto-midia,carnuccicompany/carnucci-dados';
const quem = () => { try { return localStorage.getItem('mm_quem') || 'Léo'; } catch (e) { return 'Léo'; } };
const setQuem = v => { try { localStorage.setItem('mm_quem', v); } catch (e) { /* sem armazenamento: fica só nesta visita */ } };
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

function contexto(id) {
  const a = AGENTES[id]; if (!a) return '';
  return `Você agora é ${a.nome}, ${a.cargo} de ${a.setor} da Carnucci (app de assinatura MinhaMoto e infoprodutos), conversando direto com o ${quem()} (dono, junto com o ${quem() === 'Léo' ? 'Davi' : 'Léo'}). Missão da empresa: vender muito, pra muita gente, e sempre vender mais.
Antes de responder, no repositório carnuccicompany/minhamoto-midia leia: agencia/merito/CULTURA.md, sua ficha em agencia/merito/livro.json (id "${id}"), seu playbook ${a.playbook} (a seção "Lapidado com o Léo" vale mais que o resto), sua memória ${a.memoria} e sua agenda (mesma pasta, ${id.replace(':', '_')}-agenda.md se existir), agencia/memoria/decisoes.md e as suas demandas em agencia/demandas/quadro.json. Números reais ficam no repositório privado carnuccicompany/carnucci-dados (resumo/, metas/, agentes/).
Fale no seu jeito, em português, curto e direto. Não invente número (cite o arquivo). Nada vai ao ar, nenhum dinheiro, campanha ou mudança no app sem OK do Léo ou do Davi; o app (minhamotooficial) é só leitura.
Quando o ${quem()} pedir algo: transforme em DEMANDA (arquivo JSON em agencia/demandas/itens/ no formato de agencia/demandas/README.md, "de": "${quem() === 'Léo' ? 'leo' : 'davi'}", "para": "${id}", prioridade e prazo combinados) ou em OBSERVAÇÃO (acrescente com data em ${a.memoria} na seção "Observações do dono"; se for decisão que vale pra empresa, também em agencia/memoria/decisoes.md). Depois rode python3 scripts/quadro_demandas.py, faça commit e push na main (git pull --rebase antes; nunca force-push; nada de número absoluto, R$ da empresa, chave ou dado de cliente no repositório público) e confirme o id da demanda.`;
}
function link(prompt) { const u = new URL('https://claude.ai/code'); u.searchParams.set('prompt', prompt); u.searchParams.set('repositories', REPOS); return u.toString(); }

function equipe(dir, alvo) {
  const a = AGENTES[dir]; if (!a || a.tipo !== 'diretor') return '';
  const time = Object.entries(AGENTES).filter(([k, x]) => x.status === 'ativo' && k !== dir && (x.chefe === dir || x.chefe === a.nome));
  if (!time.length) return '';
  const opt = (k, rot) => `<option value="${esc(k)}"${k === alvo ? ' selected' : ''}>${esc(rot)}</option>`;
  return `<label class="cmd-team">Falar com: <select class="cmd-sel">${opt(dir, a.nome + ' (diretor)')}${time.map(([k, x]) => opt(k, x.nome + ' · ' + x.cargo)).join('')}</select></label>`;
}
export function comandoHTML(id, dir = id) {
  const a = AGENTES[id];
  if (!a) return '';
  if (a.status !== 'ativo') return `<div class="cmd"><div class="cmd-k">Sala de comando</div><p class="cmd-off">${esc(a.nome)} está na <b>reserva</b>: não recebe demanda. Quem cuida da área agora está em ESTRUTURA-ENXUTA.md. Pra trazer de volta, peça ao Shelby.</p></div>`;
  const n = DEMANDAS_ABERTAS[id] || 0;
  return `<div class="cmd" data-id="${esc(id)}" data-dir="${esc(dir)}">
    <div class="cmd-k">Sala de comando <span class="cmd-q">falando como <button type="button" class="cmd-who">${esc(quem())}</button></span></div>
    ${equipe(dir, id)}
    <div class="cmd-st">${n ? `<b>${n}</b> demanda${n > 1 ? 's' : ''} aberta${n > 1 ? 's' : ''} com ele` : 'Nenhuma demanda aberta com ele'}</div>
    <div class="cmd-tabs"><button type="button" data-m="chat" class="on">💬 Conversar</button><button type="button" data-m="dem">📋 Passar demanda</button><button type="button" data-m="obs">📝 Observação</button></div>
    <div class="cmd-f" data-f="chat"><textarea rows="3" placeholder="O que você quer falar com ${esc(a.nome.split(' ')[0])}? (opcional)"></textarea></div>
    <div class="cmd-f" data-f="dem" hidden><input type="text" placeholder="Título da demanda" maxlength="120"><textarea rows="3" placeholder="O que você quer, por quê e quando está pronto"></textarea>
      <div class="cmd-pr"><label><input type="radio" name="pr-${esc(id)}" value="P1"> P1 · 24h</label><label><input type="radio" name="pr-${esc(id)}" value="P2" checked> P2 · 72h</label><label><input type="radio" name="pr-${esc(id)}" value="P3"> P3 · 7 dias</label></div></div>
    <div class="cmd-f" data-f="obs" hidden><textarea rows="3" placeholder="Observação, correção ou elogio pra ${esc(a.nome.split(' ')[0])} lembrar daqui pra frente"></textarea></div>
    <div class="cmd-go"><a class="cmd-open" target="_blank" rel="noopener" href="#">Abrir no Claude ↗</a><button type="button" class="cmd-copy">Copiar pedido</button></div>
    <p class="cmd-hint">Abre uma conversa nova no Claude já com ${esc(a.nome.split(' ')[0])} e os repositórios da empresa. Você revisa e envia; é lá que ele responde e grava a demanda.</p>
  </div>`;
}

export function bindComando(root) {
  const box = root.querySelector('.cmd[data-id]'); if (!box) return;
  const id = box.dataset.id;
  const sel = box.querySelector('.cmd-sel');
  if (sel) sel.onchange = () => { const host = box.parentElement; box.outerHTML = comandoHTML(sel.value, box.dataset.dir); bindComando(host); };
  let modo = 'chat';
  const montar = () => {
    const f = box.querySelector(`[data-f="${modo}"]`), txt = (f.querySelector('textarea')?.value || '').trim();
    let pedido;
    if (modo === 'chat') pedido = txt ? `Primeira mensagem do ${quem()}: ${txt}` : `O ${quem()} abriu uma conversa com você. Cumprimente em uma linha, diga em até 4 linhas como está o seu setor agora (com número e fonte, se houver) e pergunte o que ele precisa.`;
    else if (modo === 'dem') { const t = (f.querySelector('input[type=text]').value || '').trim(), pr = (f.querySelector('input[type=radio]:checked') || {}).value || 'P2'; pedido = `O ${quem()} está te passando uma DEMANDA agora. Título: "${t || 'sem título'}". Detalhes: ${txt || '(sem detalhes; pergunte o que faltar antes de criar)'}. Prioridade: ${pr}. Confirme que entendeu em 2 linhas, pergunte só o que faltar pra ficar verificável, crie a demanda e diga o id.`; }
    else pedido = `O ${quem()} está deixando uma OBSERVAÇÃO pra você guardar e seguir daqui pra frente: ${txt || '(vazia; pergunte qual é)'}. Grave na sua memória (seção "Observações do dono"), diga em 2 linhas como isso muda o seu trabalho e, se for regra pra empresa, registre também em agencia/memoria/decisoes.md.`;
    return contexto(id) + '\n\n' + pedido;
  };
  const atualizar = () => { box.querySelector('.cmd-open').href = link(montar()); };
  box.querySelectorAll('.cmd-tabs button').forEach(b => b.onclick = () => {
    modo = b.dataset.m; box.querySelectorAll('.cmd-tabs button').forEach(x => x.classList.toggle('on', x === b));
    box.querySelectorAll('.cmd-f').forEach(f => f.hidden = f.dataset.f !== modo); atualizar();
  });
  box.addEventListener('input', atualizar); box.addEventListener('change', atualizar);
  box.querySelector('.cmd-who').onclick = e => { setQuem(quem() === 'Léo' ? 'Davi' : 'Léo'); e.currentTarget.textContent = quem(); atualizar(); };
  box.querySelector('.cmd-copy').onclick = async e => {
    const b = e.currentTarget; try { await navigator.clipboard.writeText(montar()); b.textContent = 'Copiado ✓'; } catch (err) { b.textContent = 'Não deu pra copiar'; }
    setTimeout(() => { b.textContent = 'Copiar pedido'; }, 1800);
  };
  atualizar();
}
