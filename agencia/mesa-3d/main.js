import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js';
import { DIRETORES, MASTER, FATURAMENTO, DECOR, HALL, ESTOQUE, GOSTOS, CAMBIO, ESTOQUE_DATA, SUBJEITO, SUBNOME, PETS_HUMOR, MERITO, CADASTRO, SOCIOS } from './data.js';
import { buildGauge } from './gauge.js';
import { buildAquarium } from './aquarium.js';
import { buildDecor, buildHall } from './decor.js';
import { buildStock } from './stock.js';
import { M, mat, mesh, box, sph, lerp, clamp, smooth, ease, angLerp, mergeChildren, blob, bakeStatic } from './util.js';
import { buildEnv, SPOTS, TABLE_R, TOP_Y, ROOM, PIT } from './env.js';
import { buildPit } from './pit.js';
import { buildPerson, blendPose, sitLegs, standLegs, faceTick } from './people.js';
import { macbook, glassOf, cigar, phone, newspaper, tableProps, chair, throne, plateTex, smokeTex } from './props.js';
import { buildPhoenix } from './phoenix.js';
import { buildPanther } from './panther.js';
import { buildRedPanda } from './pets.js';

const LOGO = window.__LOGO__;
const app = document.getElementById('app');
const isMobile = () => window.innerWidth < 760;

const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance', stencil: true });
let HD = false; const PR = () => HD ? Math.min(window.devicePixelRatio || 1, 2) : (isMobile() ? 1 : Math.min(window.devicePixelRatio || 1, 1.25));
renderer.setPixelRatio(PR());
renderer.setSize(app.clientWidth, app.clientHeight);
renderer.shadowMap.enabled = false;
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.outputColorSpace = THREE.SRGBColorSpace;
app.appendChild(renderer.domElement);
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(40, app.clientWidth / app.clientHeight, 0.1, 2500);
const HOME = { pos: new THREE.Vector3(10.5, 11.5, 17), tgt: new THREE.Vector3(-0.6, 0.6, 0.4) };
if (isMobile()) HOME.pos.set(8, 17, 21);
camera.position.copy(HOME.pos);
const controls = new OrbitControls(camera, renderer.domElement);
Object.assign(controls, { enableDamping: true, dampingFactor: 0.08, minDistance: 2.5, maxDistance: 30, maxPolarAngle: 1.45, screenSpacePanning: false, autoRotate: true, autoRotateSpeed: 0.25 });
controls.target.copy(HOME.tgt);
let camFly = null, rotOn = true, autoTimer = null, follow = null, viewMode = false;
controls.addEventListener('start', () => { controls.autoRotate = false; camFly = null; follow = null; document.getElementById('bFollow').classList.remove('on'); clearTimeout(autoTimer); });
controls.addEventListener('end', () => { clearTimeout(autoTimer); autoTimer = setTimeout(() => { if (!selected && !follow) controls.autoRotate = rotOn; }, 12000); });

const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture; scene.environmentIntensity = 0.3;
const env = buildEnv(scene, renderer, LOGO, FATURAMENTO);
const clock = new THREE.Clock();

// ---------- assentos ----------
const SEAT_R = 3.3, RING = 4.75;
const deg = d => d * Math.PI / 180;
const meritOf = d => Object.assign({}, d, { padrao: (MERITO.agentes[d.id] || {}).padrao || MERITO.padrao || 'ouro', broche: (MERITO.agentes[d.id] || {}).broche || 'nenhum' });
const east = [-60, -30, 0, 30, 60].map(deg), west = [120, 150, 180, 210, 240].map(deg);
const angles = [...east, ...west];
const seats = [];
const pickables = [];
const labelsEl = document.getElementById('labels');

function frameAt(a, r = SEAT_R) { const f = new THREE.Group(); f.position.set(Math.cos(a) * r, 0, Math.sin(a) * r); f.lookAt(0, 0, 0); scene.add(f); return f; }

// tronos do Léo e do Davi (sempre vazios)
const thrones = [];
[['Léo', deg(90)], ['Davi', deg(270)]].forEach(([nome, a]) => {
  const f = frameAt(a, SEAT_R + 0.12);
  const t = throne(plateTex(nome, 'Sócio · CEO')); f.add(t); blob(f, 0, -0.05, 0.6, 0.65, 0.4);
  t.traverse(o => { if (o.isMesh) { o.userData.thr = nome; pickables.push(o); } });
  macbook(f, 0, 0.7, 0, 'money').group.position.y = TOP_Y;
  const g = glassOf('whisky'); g.position.set(0.34, TOP_Y, 0.62); f.add(g);
  thrones.push({ nome, a, f });
  // SÓCIOS: quando SOCIOS (data.js) tiver o Léo ou o Davi, a pessoa senta no próprio trono
  const socio = (SOCIOS || []).find(x => x.nome && nome.toLowerCase().startsWith(x.nome.toLowerCase()));
  if (socio) { const P = buildPerson(Object.assign({ id: 'socio-' + nome, terno: 0x0d0d10, gravata: 0x111111, pele: 0xd9a77f, cabelo: 0x161210, estilo: 'curto', padrao: 'elite', broche: 'imaculado', idade: 30 }, socio)); f.add(P.root); sitLegs(P); }
});

function addTag(html, cls = '') { const el = document.createElement('button'); el.type = 'button'; el.className = 'tag ' + cls; el.innerHTML = html; labelsEl.appendChild(el); return el; }
function addBubble() { const el = document.createElement('div'); el.className = 'bubble'; labelsEl.appendChild(el); return el; }

DIRETORES.forEach((d, i) => {
  const a = angles[i];
  const frame = frameAt(a);
  const ch = chair(plateTex(d.nome, d.setor)); frame.add(ch); blob(frame, 0, -0.05, 0.5, 0.55, 0.4);
  const P = buildPerson(meritOf(d)); frame.add(P.root); sitLegs(P);
  const mb = macbook(frame, 0, 0.7, 0, d.tela); mb.group.position.y = TOP_Y;
  const slots = [[-0.38, 0.68], [0.42, 0.88], [-0.44, 0.92]];
  let si = 0;
  d.props.forEach(k => { if (k === 'whisky' || k === 'espresso') return; const it = tableProps[k](frame, ...slots[si++ % 3]); it.position.y = TOP_Y; });
  const drink = d.bebe === 'whisky' ? 'whisky' : d.bebe === 'cafe' ? 'cafe' : 'agua';
  const tg = glassOf(drink); tg.position.set(0.33, TOP_Y, 0.6); frame.add(tg);
  const hg = glassOf(drink); hg.visible = false; P.wr[1].add(hg); hg.position.set(0, -0.09, 0.035); hg.rotation.x = Math.PI / 2 - 0.1;
  const hand = {};
  if (d.props.includes('cigar')) { const c = cigar(); c.visible = false; P.wr[1].add(c); c.position.set(-0.03, -0.11, 0.02); c.rotation.set(0, 0, 0.3); hand.cigar = c; }
  if (d.comp === 'phone' || d.comp === 'twophones' || d.comp === 'talk') { const p = phone(d.comp === 'twophones'); p.visible = false; P.wr[1].add(p); p.position.set(0, -0.1, 0.02); p.rotation.set(Math.PI / 2, 0, 0); hand.phone = p; }
  if (d.comp === 'newspaper') { const n = newspaper(d.papel); n.visible = false; P.torso.add(n); n.position.set(0, 0.32, 0.42); n.rotation.x = -0.25; hand.paper = n; }
  ch.traverse(o => { if (o.isMesh) { o.userData.dirId = d.id; pickables.push(o); } }); P.root.traverse(o => o.isMesh && pickables.push(o));
  const s = { d, a, frame, chair: ch, P, mb, tg, hg, hand, drink, level: 0.4 + Math.random() * 0.6, state: 'sit', act: 'work', actT: 1 + Math.random() * 4, actK: 0, phase: 0, seed: Math.random() * 100,
    timers: { banheiro: 40 + Math.random() * 260, janela: 120 + Math.random() * 400 }, stats: { banheiro: 0, refil: 0 } };
  s.tag = addTag(`<b>${d.nome}</b><span>${d.setor}</span>`); s.tag.addEventListener('click', e => { e.stopPropagation(); select(s); });
  s.bubble = addBubble();
  seats.push(s);
});
seats.forEach((s, i) => { s.left = seats[(i + seats.length - 1) % seats.length]; s.right = seats[(i + 1) % seats.length]; });

// Consigliere (diretor-geral) — anda pela sala
const masterP = buildPerson(meritOf(MASTER));
const master = { d: MASTER, P: masterP, pos: new THREE.Vector3(5.2, 0, -4.6), heading: -2.2, state: 'idle', t: 4, phase: 0, path: null, leg: 0, target: null, bubble: addBubble() };
scene.add(masterP.root); blob(masterP.root, 0, 0, 0.32, 0.32); standLegs(masterP, 0, false); blendPose(masterP, 'armsCross', 'armsCross', 1);
masterP.root.traverse(o => { if (o.isMesh) { o.userData.dirId = 'master'; pickables.push(o); } });
master.tag = addTag(`<b>${MASTER.nome}</b><span>${MASTER.cargo}</span>`, 'master'); master.tag.addEventListener('click', e => { e.stopPropagation(); select(master); });

// objetos pessoais de cada diretor + Hall da Fama
const NOMES = Object.fromEntries([...DIRETORES, MASTER].map(d => [d.id, d.nome]));
const decor = buildDecor(scene, DECOR, NOMES);
const hall = buildHall(scene, LOGO, HALL, id => NOMES[id]);
const stock = buildStock(scene);
const ITEM = Object.fromEntries(ESTOQUE.map(e => [e.id, e]));
const cs = e => Math.round(e.reais / CAMBIO);
const brl = v => v ? 'R$ ' + v.toLocaleString('pt-BR') : 'grátis';
const phoenix = buildPhoenix(scene, window.__PARROT__);
const humor = id => PETS_HUMOR.humor[id] || 'ok';
const FALA_PET = {
  foda: ['Essa foi pra você, Marnevali.', 'Ela soltou fogo pra mim. Semana boa.', 'Marnevali feliz, empresa feliz.'],
  ok: ['Tô de olho no número, Marnevali.', 'Calma que vem coisa boa aí.'],
  fraco: ['Desculpa, Marnevali. Semana que vem eu viro esse número.', 'Não fica assim, vou compensar.'],
  panda: ['Vem cá, Carnucci.', 'Esse é o melhor funcionário da empresa.', 'Carinho pro chefe peludo.'],
  pandaMesa: ['Ô Carnucci, deita aqui do lado.', 'Esse panda não sai da mesa.', 'Carinho rapidinho e volto pro número.', 'Melhor colega de mesa que existe.'],
  pantera: ['Tô no gás, tô no gás.', 'Relaxa, o relatório sai hoje.', 'Já tô refazendo esse número.', 'Ela não tira o olho de mim.', 'Ninguém dorme no ponto com ela aqui.'],
};
const pick = a => a[Math.floor(Math.random() * a.length)];
let fenixT = 18, pandaT = 40, fenixIdx = 0;
const panda = buildRedPanda(scene);
{ const sa = [...angles, deg(90), deg(270)].sort((a, b) => a - b); const gaps = []; for (let i = 0; i < sa.length; i++) { const a = sa[i], b = i + 1 < sa.length ? sa[i + 1] : sa[0] + Math.PI * 2; gaps.push((a + b) / 2); } panda.setSeats(angles, gaps); }
panda.onPetIdle = a => { const s = seats.find(x => Math.abs(Math.atan2(Math.sin(x.a - a), Math.cos(x.a - a))) < 0.05 && x.state === 'sit'); if (s) say(s, pick(FALA_PET.pandaMesa)); };
const panther = buildPanther(scene);
const aquarium = buildAquarium(scene);
{ const _v = []; panther.blockers = () => { let k = 0; const out = []; seats.forEach(x => { if (x.state !== 'sit') { _v[k] = _v[k] || new THREE.Vector3(); out.push(x.P.root.getWorldPosition(_v[k++])); } }); _v[k] = _v[k] || new THREE.Vector3(); out.push(masterP.root.getWorldPosition(_v[k])); return out; }; }
let pantherT = 22;
// ---------- pôquer no fosso: 3 diretores descem, jogam uma mão amistosa e voltam ----------
const pit = buildPit(scene);
const POKER_FALA = { mesa: ['Paga pra ver.', 'Mesa.', 'Aumento.', 'Tô fora dessa.', 'Blefe seu, conheço essa cara.', 'All-in.', 'Vai, abre o jogo.'],
  win: ['Hoje é meu dia, rapaziada.', 'Obrigado pela doação, irmão.', 'Essa foi bonita, admite.'], lose: ['Revanche amanhã, parceiro.', 'Boa mão. Próxima é minha.', 'Leva, mas eu volto.'],
  saida: ['Bora trampar que a meta não bate sozinha.', 'Valeu a mão, irmão.', 'Amanhã tem mais.'] };
const poker = { t: 75, on: false, players: [], timer: 0, talkT: 0, toss: null, tossT: 0 };
function pokerTick(dt, now) {
  if (!poker.on) {
    poker.t -= dt; if (poker.t > 0) return;
    const free = seats.filter(s => s.state === 'sit' && selected !== s && s.act !== 'chat' && s.act !== 'listen');
    if (free.length < 3) { poker.t = 20; return; }
    const pl = []; while (pl.length < 3) { const c = pick(free); if (!pl.includes(c)) pl.push(c); }
    const idx = [0, 1, 2, 3, 4].sort(() => Math.random() - 0.5);
    pl.forEach((s, i) => { s.pokerSeat = idx[i]; goOut(s, 'poker', now); });
    poker.on = true; poker.players = pl; poker.timer = 0; poker.talkT = 4;
    return;
  }
  const seated = poker.players.filter(s => s.state === 'pokerSit');
  if (seated.length < poker.players.length) return;
  poker.timer += dt; poker.talkT -= dt;
  if (poker.talkT <= 0) { const s = pick(poker.players); say(s, pick(POKER_FALA.mesa), 3); poker.toss = s; poker.tossT = now; poker.talkT = 4 + Math.random() * 4; }
  if (poker.timer > 40) {
    const [w, ...rest] = [...poker.players].sort(() => Math.random() - 0.5), pot = 3 + Math.floor(Math.random() * 6);
    say(w, pick(POKER_FALA.win), 4); rest.forEach(s => say(s, pick(POKER_FALA.lose), 4));
    log(`<b>Pôquer no fosso:</b> ${first(w)} levou C$ ${pot} de ${rest.map(first).join(' e ')}. Saíram rindo, abraço na escada.`);
    poker.players.forEach((s, i) => setTimeout(() => { s.state = 'pokerOut'; s.ppath = pit.pathIn(s.pokerSeat).reverse(); s.pleg = 0; if (i === 0) say(s, pick(POKER_FALA.saida), 3); }, 2500 + i * 1200));
    poker.on = false; poker.t = 150 + Math.random() * 120; poker.players = []; poker.toss = null;
  }
}
function pantherTick(dt) {
  pantherT -= dt; if (pantherT > 0 || panther.busy()) return;
  // para atrás de quem está mais perto dela; quem está "fraco" com os pets leva encarada mais longa
  const a = panther.angle(); const sitting = seats.filter(s => s.state === 'sit');
  const near = sitting.map(s => ({ s, d: Math.abs(Math.atan2(Math.sin(s.a - a - 0.18), Math.cos(s.a - a - 0.18))) })).sort((x, y) => x.d - y.d)[0];
  if (!near || near.d > 0.16) { pantherT = 0.5; return; }
  const s = near.s, fraco = humor(s.d.id) === 'fraco';
  panther.stare(s.frame.getWorldPosition(new THREE.Vector3()).setY(1.2), fraco ? 6 : 3.5, () => {
    say(s, pick(FALA_PET.pantera));
    if (fraco || Math.random() < 0.35) log(`A <b>Fartuzzi</b> parou atrás do <b>${first(s)}</b> e ficou encarando até ver trabalho andar.`);
  });
  pantherT = 26 + Math.random() * 20;
}
function petTick(dt) {
  const sitting = seats.filter(s => s.state === 'sit');
  fenixT -= dt;
  if (fenixT <= 0 && phoenix.ready && sitting.length) {
    const s = sitting[fenixIdx++ % sitting.length], m = humor(s.d.id), pos = s.frame.getWorldPosition(new THREE.Vector3());
    if (phoenix.visit(pos, m, () => {
      say(s, pick(FALA_PET[m]));
      log(m === 'foda' ? `<b>Marnevali</b> soltou fogo pro <b>${first(s)}</b> · gorjeta: +10 XP e C$ 5` : m === 'fraco' ? `<b>Marnevali</b> passou acuada pelo <b>${first(s)}</b>` : `<b>Marnevali</b> passou de olho no <b>${first(s)}</b>`);
    })) fenixT = 32 + Math.random() * 18; else fenixT = 3;
  }
  pandaT -= dt;
  if (pandaT <= 0 && sitting.length) {
    const good = sitting.filter(s => humor(s.d.id) === 'foda'), okk = sitting.filter(s => humor(s.d.id) === 'ok');
    const pool = good.length ? good : okk;
    if (!pool.length) { pandaT = 30; return; }
    const s = pick(pool);
    if (panda.visit(s.frame.getWorldPosition(new THREE.Vector3()), () => { say(s, pick(FALA_PET.panda)); log(humor(s.d.id) === 'foda' ? `<b>Carnucci</b> subiu na mesa pra ganhar carinho do <b>${first(s)}</b> · gorjeta: +5 XP e C$ 3` : `<b>Carnucci</b> subiu na mesa do <b>${first(s)}</b>`); })) pandaT = 70 + Math.random() * 40; else pandaT = 10;
  }
}
panda.root.traverse(o => { if (o.isMesh) pickables.push(o); });
panther.root.traverse(o => { if (o.isMesh) pickables.push(o); });
const PETS = {
  fenix: { nome: 'Marnevali', tipo: 'Fênix · o pet da empresa', txt: 'A sala inteira ama ela e ninguém quer decepcionar a Marnevali. Ela passa voando por cada diretor: quando o trampo foi foda, solta fogo pro alto e o diretor ganha gorjeta (+10 XP e C$ 5). Quando o trampo foi fraco, passa acuadinha, de cabeça baixa. Renasce das cinzas, como a empresa que não para.' },
  panda: { nome: 'Carnucci', tipo: 'Panda-vermelho · o xodó da mesa', txt: 'A casa dele é a mesa dos diretores: passa o dia andando por cima dela e deitando do lado de alguém pra ganhar carinho. Desce de vez em quando, dá uma volta e sobe de novo. Quando um diretor manda bem, ele vai direto pra frente dele: é gorjeta de +5 XP e C$ 3. Com quem está devendo, ele não vai.' },
  pantera: { nome: 'Fartuzzi', tipo: 'Pantera negra · a vigia do tapete', txt: 'Anda solta pelo tapete de veludo em volta da mesa: caminha, para, olha em volta, senta, muda de rumo, sem nunca sair dele. De vez em quando para atrás de um diretor e fica encarando. Não morde ninguém: ela sobe a régua. Com quem está devendo, a encarada dura mais.' },
};
PETS.tubarao = { nome: 'Tubarão Carnucci', tipo: 'Tubarão · o dono do aquário', txt: 'Mora no aquário gigante embaixo do piso de vidro, entre a mesa e as janelas. Nada em volta o dia inteiro, sem pressa e sem parar: quem anda por cima vê ele passando debaixo dos pés. Lembra todo mundo que aqui dentro quem para, afunda.' };
const sharkTag = addTag('<b>Tubarão Carnucci</b><span>Tubarão</span>', 'pet'); sharkTag.addEventListener('click', e => { e.stopPropagation(); selectPet('tubarao'); });
const pandaTag = addTag('<b>Carnucci</b><span>Panda-vermelho</span>', 'pet'); pandaTag.addEventListener('click', e => { e.stopPropagation(); selectPet('panda'); });
const pantherTag = addTag('<b>Fartuzzi</b><span>Pantera negra</span>', 'pet'); pantherTag.addEventListener('click', e => { e.stopPropagation(); selectPet('pantera'); });
const fenixTag = addTag('<b>Marnevali</b><span>Fênix</span>', 'pet'); fenixTag.addEventListener('click', e => { e.stopPropagation(); selectPet('fenix'); });
function selectPet(k) {
  hideTeam(); const p = PETS[k]; selected = { pet: k }; controls.autoRotate = false;
  openPanel(`<button class="x" aria-label="Fechar">×</button><span class="kick">Mascote</span><h2>${p.nome}</h2><p class="nick">${p.tipo}</p><p class="what" style="margin-top:14px">${p.txt}</p><button class="povbtn" type="button" data-pov="pet:${k}">👁 Ver pelos olhos ${k === 'tubarao' ? 'dele' : 'dela'}</button>`);
  setOffset();
  if (k === 'fenix') { follow = 'phoenix'; document.getElementById('bFollow').classList.add('on'); }
  else if (k === 'tubarao') { const q = aquarium.root.getWorldPosition(new THREE.Vector3()); camFly = { pos: new THREE.Vector3(q.x + 1.2, 2.4, q.z + 3.0), tgt: new THREE.Vector3(q.x, 0, q.z) }; }
  else { const q = (k === 'pantera' ? panther.root : panda.root).position; camFly = { pos: q.clone().add(new THREE.Vector3(1.6, 1.3, 1.6)), tgt: q.clone().add(new THREE.Vector3(0, 0.3, 0)) }; selected.track = true; }
}

// ---------- caminhos ----------
function ringPath(fromPos, dest, startAngle) {
  const pts = [];
  const a0 = startAngle ?? Math.atan2(fromPos.z, fromPos.x);
  const a1 = Math.atan2(dest.z, dest.x);
  pts.push(new THREE.Vector3(Math.cos(a0) * RING, 0, Math.sin(a0) * RING));
  const da = Math.atan2(Math.sin(a1 - a0), Math.cos(a1 - a0));
  const n = Math.max(1, Math.ceil(Math.abs(da) / 0.22));
  for (let k = 1; k <= n; k++) { const aa = a0 + da * k / n; pts.push(new THREE.Vector3(Math.cos(aa) * RING, 0, Math.sin(aa) * RING)); }
  return pts;
}
function pathTo(s, dest) {
  const pts = [new THREE.Vector3(Math.cos(s.a) * (SEAT_R + 0.7), 0, Math.sin(s.a) * (SEAT_R + 0.7)), ...ringPath(null, dest, s.a)];
  if (dest === SPOTS.banheiro) pts.push(SPOTS.banheiroPorta.clone());
  pts.push(dest.clone());
  return pts;
}

const ticker = document.getElementById('ticker');
function log(msg) {
  const li = document.createElement('li'); li.innerHTML = `<i>${new Date().toLocaleTimeString('pt-BR', { timeZone: 'America/Sao_Paulo', hour: '2-digit', minute: '2-digit' })}</i>${msg}`; ticker.prepend(li);
  while (ticker.children.length > 5) ticker.lastChild.remove();
  requestAnimationFrame(() => li.classList.add('in'));
}
const first = s => s.d.nome.split(' ')[0];

function say(who, text, dur = 4.2) { who.bubble.textContent = text; who.bubble.classList.add('on'); who.sayT = dur; if (who.P) who.P.talk = 1; }
let nextChat = 6;
function startChat() {
  const free = seats.filter(s => s.state === 'sit' && s.act !== 'chat' && s.act !== 'listen');
  if (free.length < 2) return;
  const a = free[Math.floor(Math.random() * free.length)];
  const cand = [a.left, a.right].filter(x => x.state === 'sit' && x.act !== 'chat' && x.act !== 'listen');
  const others = free.filter(x => x !== a);
  const b = cand.length && Math.random() < 0.8 ? cand[Math.floor(Math.random() * cand.length)] : others[Math.floor(Math.random() * others.length)];
  if (!b) return;
  a.act = 'chat'; a.actT = 9; a.actK = 0; a.with = b; b.act = 'listen'; b.actT = 9; b.actK = 0; b.with = a;
  say(a, a.d.falas[Math.floor(Math.random() * a.d.falas.length)]);
  setTimeout(() => { if (b.act === 'listen' && b.state === 'sit') { b.act = 'chat'; say(b, b.d.falas[Math.floor(Math.random() * b.d.falas.length)]); } }, 4600);
}

const ACTS = {
  typing: [['work', 6], ['sip', 1.2], ['think', 1]],
  phone: [['phoneLook', 3], ['work', 3], ['sip', 1.5], ['phoneCall', 1.2]],
  sketch: [['work', 5], ['sip', 1.2], ['think', 1.5]],
  cigar: [['work', 3], ['smoke', 3], ['sip', 1.3], ['think', 1]],
  newspaper: [['read', 3], ['work', 2.5], ['smoke', 1.5], ['sip', 1]],
  tablet: [['work', 5], ['sip', 1.2], ['think', 1.2]],
  talk: [['work', 3], ['sip', 2], ['phoneLook', 1.5], ['think', 1]],
  twophones: [['phoneLook', 3], ['work', 3], ['sip', 1.4]],
  money: [['work', 4], ['smoke', 2], ['sip', 1.4], ['count', 2]],
};
function pickAct(s) { const list = ACTS[s.d.comp]; const tot = list.reduce((a, [, w]) => a + w, 0); let r = Math.random() * tot; for (const [k, w] of list) { r -= w; if (r <= 0) return k; } return 'work'; }
const DUR = { work: [6, 14], sip: [3, 3], smoke: [3.6, 3.6], phoneLook: [5, 10], phoneCall: [7, 10], read: [8, 14], think: [3, 5], count: [4, 7] };

function goOut(s, kind, now) {
  const dest = kind === 'poker' ? SPOTS.pokerTop : kind === 'refil' ? (s.drink === 'whisky' ? SPOTS.uisque : s.drink === 'cafe' ? SPOTS.cafe : SPOTS.agua) : kind === 'banheiro' ? SPOTS.banheiro : [SPOTS.janelaN1, SPOTS.janelaN2, SPOTS.janelaL][Math.floor(Math.random() * 3)];
  s.state = 'standup'; s.t0 = now; s.kind = kind; s.path = pathTo(s, dest); s.leg = 0; s.dir = 1; s.act = 'work';
  s.bubble.classList.remove('on');
  Object.values(s.hand).forEach(h => h.visible = false);
  if (kind === 'refil') { s.tg.visible = false; s.hg.visible = true; } else { s.hg.visible = false; s.tg.visible = true; }
  const txt = { banheiro: 'foi ao banheiro', refil: s.drink === 'whisky' ? 'foi na adega encher o copo' : s.drink === 'cafe' ? 'foi buscar mais um café' : 'foi encher o copo d’água', janela: 'foi olhar a vista', poker: 'desceu pro fosso do pôquer' }[kind];
  log(`<b>${first(s)}</b> ${txt}`);
}

const tmpV = new THREE.Vector3(), tmpW = new THREE.Vector3();
function walkStep(obj, P, frame, dt, speed = 1.2) {
  const target = obj.path[obj.leg];
  tmpV.subVectors(target, obj.wpos); tmpV.y = 0;
  const dist = tmpV.length(), spd = speed * dt;
  let arrived = false;
  if (dist < spd) { obj.wpos.copy(target); arrived = true; } else obj.wpos.addScaledVector(tmpV.normalize(), spd);
  obj.phase += dt * 6.8;
  standLegs(P, obj.phase, true);
  const sw = Math.sin(obj.phase) * 0.35;
  P.sh[0].rotation.set(-sw, 0, 0.07); P.sh[1].rotation.set(sw, 0, -0.07); P.el.forEach(e => e.rotation.x = -0.25); P.wr.forEach(w => w.rotation.x = 0);
  P.torso.rotation.x = 0.02; P.head.rotation.set(0, 0, 0);
  if (frame) { const local = frame.worldToLocal(tmpW.copy(obj.wpos)).clone(); P.root.position.copy(local); if (dist > 0.001) { const dl = frame.worldToLocal(tmpW.copy(obj.wpos).add(tmpV)).sub(local); obj.yaw = angLerp(obj.yaw ?? 0, Math.atan2(dl.x, dl.z), Math.min(1, dt * 8)); } P.root.rotation.y = obj.yaw; }
  else { P.root.position.copy(obj.wpos); if (dist > 0.001) obj.heading = angLerp(obj.heading, Math.atan2(tmpV.x, tmpV.z), Math.min(1, dt * 8)); P.root.rotation.y = obj.heading; }
  return arrived;
}

function updateSeat(s, dt, now) {
  const P = s.P;
  faceTick(P, dt, now);
  if (s.sayT > 0) { s.sayT -= dt; if (s.sayT <= 0) { s.bubble.classList.remove('on'); P.talk = 0; } }
  if (s.state === 'sit') {
    s.timers.banheiro -= dt; s.timers.janela -= dt;
    if (selected !== s && s.act !== 'chat' && s.act !== 'listen') {
      if (s.level < 0.15) return goOut(s, 'refil', now);
      if (s.timers.banheiro <= 0) { s.timers.banheiro = 1500 + Math.random() * 1200; s.stats.banheiro++; return goOut(s, 'banheiro', now); }
      if (s.timers.janela <= 0 && s.act === 'work') { s.timers.janela = 900 + Math.random() * 900; return goOut(s, 'janela', now); }
    }
    sitLegs(P); P.root.position.set(0, 0, 0); P.root.rotation.set(0, 0, 0);
    s.chair.position.z = ease(s.chair.position.z, 0, 6, dt);
    s.actT -= dt; s.actK += dt;
    if (s.actT <= 0) {
      s.with = null;
      Object.values(s.hand).forEach(h => h.visible = false);
      s.hg.visible = false; s.tg.visible = true;
      s.act = pickAct(s); const [a0, a1] = DUR[s.act]; s.actT = a0 + Math.random() * (a1 - a0); s.actK = 0;
      if (s.act === 'smoke' && !s.hand.cigar) s.act = 'think';
      if ((s.act === 'phoneLook' || s.act === 'phoneCall') && !s.hand.phone) s.act = 'work';
      if (s.act === 'read' && !s.hand.paper) s.act = 'work';
      if (s.act === 'sip') { s.tg.visible = false; s.hg.visible = true; s.level = Math.max(0, s.level - (0.18 + Math.random() * 0.1)); s.hg.userData.liquid.scale.y = Math.max(0.05, s.level); s.tg.userData.liquid.scale.y = Math.max(0.05, s.level); }
      if (s.act === 'smoke') s.hand.cigar.visible = true;
      if (s.act === 'phoneLook' || s.act === 'phoneCall') s.hand.phone.visible = true;
      if (s.act === 'phoneCall') say(s, ['Fechado, manda que eu vejo.', 'Pode subir hoje.', 'Me liga depois.'][Math.floor(Math.random() * 3)], 4);
      if (s.act === 'read') s.hand.paper.visible = true;
    }
    const k = smooth(clamp(s.actK / 0.6, 0, 1)), kOut = smooth(clamp(s.actT / 0.6, 0, 1)), kk = Math.min(k, kOut);
    let headYaw = 0, headPitch = 0.32, lean = 0.05;
    const tap = Math.sin(now * 16 + s.seed) * 0.03;
    switch (s.act) {
      case 'work': blendPose(P, 'rest', 'type', 1); P.wr[0].rotation.x += tap; P.wr[1].rotation.x -= tap; headPitch = 0.34 + Math.sin(now * 0.4 + s.seed) * 0.05; headYaw = Math.sin(now * 0.23 + s.seed) * 0.12; break;
      case 'sip': { const ph = clamp(s.actK / 3, 0, 1); const up = ph < 0.2 ? smooth(ph / 0.2) : ph > 0.8 ? smooth((1 - ph) / 0.2) : 1; blendPose(P, 'type', 'mouthR', up); headPitch = lerp(0.3, -0.12, up); lean = lerp(0.05, -0.04, up); break; }
      case 'smoke': { const ph = clamp(s.actK / 3.6, 0, 1); const up = ph < 0.25 ? smooth(ph / 0.25) : ph > 0.75 ? smooth((1 - ph) / 0.25) : 1; blendPose(P, 'rest', 'mouthR', up); headPitch = lerp(0.1, -0.15, up); lean = -0.05; if (ph > 0.75 && !s.puffed) { s.puffed = true; puff(s); } if (ph < 0.1) s.puffed = false; break; }
      case 'phoneLook': blendPose(P, 'type', 'phoneR', kk); headPitch = lerp(0.3, 0.5, kk); headYaw = 0.1; P.wr[1].rotation.z = Math.sin(now * 3) * 0.05; break;
      case 'phoneCall': blendPose(P, 'type', 'phoneEar', kk); headPitch = lerp(0.3, 0.0, kk); headYaw = lerp(0, 0.35, kk); lean = -0.06; break;
      case 'read': blendPose(P, 'type', 'read', kk); headPitch = lerp(0.3, 0.38, kk); lean = -0.08; break;
      case 'think': blendPose(P, 'type', 'rest', kk); headPitch = lerp(0.3, -0.1, kk); headYaw = Math.sin(now * 0.5 + s.seed) * 0.5 * kk; lean = lerp(0.05, -0.14, kk); break;
      case 'count': blendPose(P, 'rest', 'type', 1); P.sh[1].rotation.y = -0.4 + Math.sin(now * 5) * 0.12; headPitch = 0.45; headYaw = -0.35; break;
      case 'chat': case 'listen': {
        const other = s.with; let yaw = 0;
        if (other) { const lp = s.frame.worldToLocal(tmpW.copy(other.frame.position)); yaw = clamp(Math.atan2(lp.x, lp.z), -1.2, 1.2); }
        if (s.act === 'chat' && P.talk) { blendPose(P, 'rest', 'gesture', kk); P.wr[1].rotation.z = Math.sin(now * 4) * 0.2 * kk; } else blendPose(P, 'type', 'rest', kk);
        headYaw = yaw * kk; headPitch = lerp(0.3, 0.02, kk); lean = -0.03; break;
      }
    }
    P.head.rotation.y = ease(P.head.rotation.y, headYaw, 5, dt); P.head.rotation.x = ease(P.head.rotation.x, headPitch + P.slump * 0.16, 5, dt);
    P.torso.rotation.x = ease(P.torso.rotation.x, lean + P.slump * 0.12, 3, dt);
    return;
  }
  if (s.state === 'standup' || s.state === 'sitdown') {
    const k = Math.min(1, (now - s.t0) / 1.1); const e = smooth(s.state === 'standup' ? k : 1 - k);
    P.pelvis.position.set(0, lerp(0.56, 0.95, e), lerp(-0.04, 0, e)); P.pelvis.rotation.set(0, 0, 0);
    P.legs.forEach(l => l.rotation.set(lerp(-Math.PI / 2 + 0.06, 0, e), 0, 0));
    P.knees.forEach(kn => kn.rotation.set(lerp(Math.PI / 2 - 0.12, 0.02, e), 0, 0));
    P.torso.rotation.x = Math.sin(e * Math.PI) * 0.35;
    blendPose(P, 'type', 'stand', e);
    P.root.position.set(0, 0, -0.42 * e); P.root.rotation.y = 0;
    s.chair.position.z = -0.28 * e;
    if (k >= 1) {
      if (s.state === 'standup') { s.state = 'walk'; s.wpos = s.frame.localToWorld(new THREE.Vector3(0, 0, -0.42)); s.yaw = Math.PI; }
      else { s.state = 'sit'; s.act = 'work'; s.actT = 3; s.actK = 0; P.torso.rotation.x = 0; if (s.kind === 'refil') { s.hg.visible = false; s.tg.visible = true; } }
    }
    return;
  }
  if (s.state === 'walk') {
    if (walkStep(s, P, s.frame, dt)) {
      if (s.dir === 1 && s.leg === s.path.length - 1) { s.state = 'there'; s.t0 = now; s.thereFor = s.kind === 'banheiro' ? 9 + Math.random() * 6 : s.kind === 'refil' ? 5 : 10 + Math.random() * 10; }
      else if (s.dir === -1 && s.leg === 0) { s.state = 'turn'; s.t0 = now; }
      else s.leg += s.dir;
    }
    if (s.kind === 'refil') { P.sh[1].rotation.set(-0.7, 0, -0.1); P.el[1].rotation.x = -1.4; }
    return;
  }
  if (s.state === 'there' && s.kind === 'poker') { s.state = 'pokerIn'; s.ppath = pit.pathIn(s.pokerSeat); s.pleg = 0; return; }
  if (s.state === 'pokerIn' || s.state === 'pokerOut') {
    const tgt = s.ppath[s.pleg]; tmpV.subVectors(tgt, s.wpos); const d = tmpV.length(), spd = 0.95 * dt;
    if (d < spd) { s.wpos.copy(tgt); if (s.pleg < s.ppath.length - 1) s.pleg++; else if (s.state === 'pokerIn') { s.state = 'pokerSit'; s.actK = 0; } else { s.state = 'walk'; s.dir = -1; s.leg = s.path.length - 2; s.wpos.y = 0; } }
    else s.wpos.addScaledVector(tmpV.normalize(), spd);
    s.phase += dt * 6.8; standLegs(P, s.phase, true);
    const sw = Math.sin(s.phase) * 0.35; P.sh[0].rotation.set(-sw, 0, 0.07); P.sh[1].rotation.set(sw, 0, -0.07); P.el.forEach(e => e.rotation.x = -0.25); P.wr.forEach(w => w.rotation.x = 0); P.torso.rotation.x = 0.02; P.head.rotation.set(0, 0, 0);
    const local = s.frame.worldToLocal(tmpW.copy(s.wpos)).clone(); P.root.position.copy(local);
    if (d > 0.001) { const dl = s.frame.worldToLocal(tmpW.copy(s.wpos).add(tmpV)).sub(local); s.yaw = angLerp(s.yaw ?? 0, Math.atan2(dl.x, dl.z), Math.min(1, dt * 8)); } P.root.rotation.y = s.yaw;
    return;
  }
  if (s.state === 'pokerSit') {
    sitLegs(P); const st = pit.seat(s.pokerSeat);
    const local = s.frame.worldToLocal(tmpW.copy(st.pos)).clone(); P.root.position.lerp(local, Math.min(1, dt * 4));
    const lk = s.frame.worldToLocal(tmpW.copy(st.look)).sub(local); s.yaw = angLerp(s.yaw ?? 0, Math.atan2(lk.x, lk.z), Math.min(1, dt * 5)); P.root.rotation.y = s.yaw;
    s.actK += dt; const k = smooth(clamp(s.actK / 0.8, 0, 1));
    const toss = poker.toss === s ? Math.max(0, Math.sin((now - poker.tossT) * 6)) : 0;
    blendPose(P, 'rest', toss > 0 ? 'gesture' : 'read', k * (toss > 0 ? toss : 0.75));
    P.head.rotation.x = ease(P.head.rotation.x, 0.42 - toss * 0.3, 4, dt); P.head.rotation.y = ease(P.head.rotation.y, Math.sin(now * 0.3 + s.seed) * 0.35, 3, dt); P.torso.rotation.x = ease(P.torso.rotation.x, 0.12, 3, dt);
    if (s.sayT > 0) { s.sayT -= dt; if (s.sayT <= 0) { s.bubble.classList.remove('on'); P.talk = 0; } }
    faceTick(P, dt, now);
    return;
  }
  if (s.state === 'there') {
    standLegs(P, 0, false);
    const n = s.path.length;
    const look = s.kind === 'refil' ? (s.drink === 'whisky' ? new THREE.Vector3(-1, 0, 0) : new THREE.Vector3(0, 0, 1)) : s.kind === 'janela' ? (s.path[n - 1].x > 10 ? new THREE.Vector3(1, 0, 0) : new THREE.Vector3(0, 0, -1)) : s.path[n - 1].clone().sub(s.path[n - 2]);
    const a = s.frame.worldToLocal(s.wpos.clone()), b = s.frame.worldToLocal(s.wpos.clone().add(look));
    s.yaw = angLerp(s.yaw, Math.atan2(b.x - a.x, b.z - a.z), Math.min(1, dt * 4)); P.root.rotation.y = s.yaw;
    blendPose(P, 'stand', s.kind === 'refil' ? 'phoneR' : s.kind === 'janela' ? 'armsCross' : 'stand', 0.85);
    P.head.rotation.set(s.kind === 'refil' ? 0.4 : 0, Math.sin(now * 0.4) * 0.2, 0);
    if (s.kind === 'banheiro') P.root.visible = !!env.bathView;
    if (now - s.t0 > s.thereFor) {
      if (s.kind === 'refil') { s.level = 1; s.hg.userData.liquid.scale.y = 1; s.tg.userData.liquid.scale.y = 1; s.stats.refil++; }
      P.root.visible = true; s.state = 'walk'; s.dir = -1; s.leg = n - 2;
      if (s.kind === 'banheiro') log(`<b>${first(s)}</b> voltou do banheiro`);
    }
    return;
  }
  if (s.state === 'turn') {
    standLegs(P, 0, false); blendPose(P, 'stand', 'stand', 1);
    s.yaw = angLerp(s.yaw, 0, Math.min(1, dt * 6)); P.root.rotation.y = s.yaw;
    P.root.position.lerp(tmpW.set(0, 0, -0.42), Math.min(1, dt * 5));
    if (now - s.t0 > 0.8) { s.state = 'sitdown'; s.t0 = now; P.root.rotation.y = 0; }
  }
}

const puffs = [];
function puff(s) {
  const head = new THREE.Vector3(); s.P.mouth.getWorldPosition(head);
  for (let i = 0; i < 14; i++) { const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: smokeTex, transparent: true, depthWrite: false, opacity: 0.5 })); sp.position.copy(head); sp.userData = { v: new THREE.Vector3((Math.random() - .5) * .25, 0.25 + Math.random() * .25, (Math.random() - .5) * .25), t: 0, d: i * 0.05 }; sp.scale.setScalar(0.001); scene.add(sp); puffs.push(sp); }
}

function masterNext() {
  const r = Math.random();
  const sitting = seats.filter(x => x.state === 'sit');
  if (r < 0.6 && sitting.length) {
    const s = sitting[Math.floor(Math.random() * sitting.length)];
    const a = s.a + 0.16; master.visit = s;
    master.target = new THREE.Vector3(Math.cos(a) * (SEAT_R + 0.75), 0, Math.sin(a) * (SEAT_R + 0.75));
  } else if (r < 0.8) { master.visit = null; master.target = [SPOTS.janelaN1, SPOTS.janelaL][Math.floor(Math.random() * 2)].clone().add(new THREE.Vector3(-0.8, 0, 0.2)); }
  else { master.visit = null; const a = deg(90) + 0.25; master.target = new THREE.Vector3(Math.cos(a) * (SEAT_R + 1.1), 0, Math.sin(a) * (SEAT_R + 1.1)); }
  const pts = ringPath(master.pos, master.target); pts.push(master.target.clone());
  master.path = pts; master.leg = 0; master.state = 'walk'; master.wpos = master.pos;
}
function updateMaster(dt, now) {
  const P = master.P; faceTick(P, dt, now);
  if (master.sayT > 0) { master.sayT -= dt; if (master.sayT <= 0) { master.bubble.classList.remove('on'); P.talk = 0; } }
  if (master.state === 'walk') {
    if (walkStep(master, P, null, dt, 1.05)) {
      if (master.leg >= master.path.length - 1) {
        master.state = 'stay'; master.t = master.visit ? 9.5 : 12 + Math.random() * 8;
        const v = master.visit;
        if (v && v.state === 'sit') { say(master, MASTER.falas[Math.floor(Math.random() * MASTER.falas.length)]); v.act = 'listen'; v.actT = 9; v.actK = 0; v.with = { frame: { position: master.pos } }; setTimeout(() => { if (v.state === 'sit' && v.act === 'listen') { v.act = 'chat'; say(v, v.d.falas[Math.floor(Math.random() * v.d.falas.length)]); } }, 4500); log(`<b>${MASTER.nome.split(' ')[0]}</b> passou na mesa de <b>${first(v)}</b>`); }
      } else master.leg++;
    }
  } else {
    standLegs(P, 0, false);
    let want = master.heading;
    if (master.visit) { const v = master.visit.frame.position; want = Math.atan2(v.x - master.pos.x, v.z - master.pos.z); blendPose(P, 'stand', master.sayT > 0 ? 'gesture' : 'armsCross', 1); }
    else { want = master.pos.x > 10 ? Math.PI / 2 : master.pos.z < -7 ? Math.PI : Math.atan2(-master.pos.x, -master.pos.z); blendPose(P, 'stand', 'armsCross', 1); }
    master.heading = angLerp(master.heading, want, Math.min(1, dt * 3)); P.root.rotation.y = master.heading;
    P.head.rotation.y = Math.sin(now * 0.4) * 0.25;
    master.t -= dt; if (master.t <= 0) masterNext();
  }
}

const v3 = new THREE.Vector3();
function place(el, obj, dy, w, h) {
  obj.getWorldPosition(v3); v3.y += dy; const dist = v3.distanceTo(camera.position); v3.project(camera);
  const sx = (v3.x * .5 + .5) * w, sy = (-v3.y * .5 + .5) * h;
  const sc = clamp(1.25 - dist / 22, 0.55, 1);
  el.style.transform = `translate(${sx}px,${sy}px) translate(-50%,-100%) scale(${sc})`; el.style.transformOrigin = '50% 100%'; el.style.zIndex = String(10000 - Math.round(dist * 100));
  return v3.z < 1 && Math.abs(v3.x) < 1.15 && Math.abs(v3.y) < 1.15 ? 1 : 0;
}
function updateLabels() {
  const w = app.clientWidth, h = app.clientHeight;
  seats.forEach(s => {
    const hidden = !s.P.root.visible || !namesOn || selected === s;
    const o = place(s.tag, s.P.head, 0.3, w, h); s.tag.style.opacity = hidden ? 0 : o * (selected ? 0.35 : 1); s.tag.style.pointerEvents = hidden || !o ? 'none' : 'auto';
    const ob = place(s.bubble, s.P.head, !hidden && o ? 0.62 : 0.32, w, h); s.bubble.style.visibility = ob && s.P.root.visible ? 'visible' : 'hidden';
  });
  const o = place(master.tag, master.P.head, 0.3, w, h); const mh = !namesOn || selected === master; master.tag.style.opacity = mh ? 0 : o; master.tag.style.pointerEvents = !mh && o ? 'auto' : 'none';
  const ob = place(master.bubble, master.P.head, !mh ? 0.62 : 0.32, w, h); master.bubble.style.visibility = ob ? 'visible' : 'hidden';
  { const opp = place(pantherTag, panther.head, 0.32, w, h); pantherTag.style.opacity = namesOn ? opp : 0; pantherTag.style.pointerEvents = namesOn && opp ? 'auto' : 'none'; }
  { const os = place(sharkTag, aquarium.head, 0.55, w, h); sharkTag.style.opacity = namesOn && !pov ? os : 0; sharkTag.style.pointerEvents = namesOn && os && !pov ? 'auto' : 'none'; }
  const op = place(pandaTag, panda.head, 0.22, w, h); pandaTag.style.opacity = namesOn ? op : 0; pandaTag.style.pointerEvents = namesOn && op ? 'auto' : 'none';
  if (phoenix.ready) { const of = place(fenixTag, phoenix.root, 0.9, w, h); fenixTag.style.opacity = namesOn && follow !== 'phoenix' ? of : 0; fenixTag.style.pointerEvents = namesOn && of ? 'auto' : 'none'; } else fenixTag.style.opacity = 0;
}

let selected = null, namesOn = true;
const panel = document.getElementById('panel');
const ST = { on: 'Já rodando', part: 'Em parte', off: 'A criar' };
let holo = null;
const holoMat = new THREE.ShaderMaterial({ transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, uniforms: { t: { value: 0 }, c: { value: new THREE.Color(0xffcf73) } },
  vertexShader: 'varying vec3 vN; varying vec3 vV; varying float vY; void main(){ vec4 mv = modelViewMatrix * vec4(position, 1.0); vN = normalize(normalMatrix * normal); vV = normalize(-mv.xyz); vY = (modelMatrix * vec4(position, 1.0)).y; gl_Position = projectionMatrix * mv; }',
  fragmentShader: 'uniform float t; uniform vec3 c; varying vec3 vN; varying vec3 vV; varying float vY; void main(){ float f = pow(1.0 - abs(dot(vN, vV)), 2.0); float scan = 0.7 + 0.3 * sin(vY * 120.0 - t * 5.0); gl_FragColor = vec4(c * (0.10 + f * 1.25) * scan, 1.0); }' });
const holoDisc = new THREE.MeshBasicMaterial({ color: 0xf0cf86, transparent: true, opacity: 0.14, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide });
function showTeam(anchor, subs, back = 1, did = '') {
  hideTeam();
  const g = new THREE.Group(); anchor.add(g); const n = subs.length, tags = [];
  subs.forEach((name, k) => {
    const ang = (k - (n - 1) / 2) * (n > 4 ? 0.42 : 0.55);
    const f = new THREE.Group(); f.position.set(Math.sin(ang) * 1.55, 0.42, -back * (0.45 + Math.cos(ang) * 0.85)); f.rotation.y = -ang * 0.6 + (back < 0 ? Math.PI : 0); g.add(f);
    mesh(new THREE.RingGeometry(0.16, 0.19, 40), holoDisc, f, [0, 0.01, 0], [-Math.PI / 2, 0, 0], false);
    mesh(new THREE.CylinderGeometry(0.16, 0.05, 0.42, 24, 1, true), holoDisc, f, [0, -0.21, 0], null, false);
    const body = new THREE.Group(); f.add(body);
    [-0.06, 0.06].forEach(x => mesh(new THREE.CapsuleGeometry(0.035, 0.32, 4, 8), holoMat, body, [x, 0.2, 0], null, false));
    mesh(new THREE.CapsuleGeometry(0.09, 0.22, 4, 10), holoMat, body, [0, 0.55, 0], null, false).scale.set(1.25, 1, 0.75);
    mesh(sph(0.075, 14, 10), holoMat, body, [0, 0.85, 0], null, false);
    body.scale.set(1, 0.001, 1); body.userData.k = k;
    const t = document.createElement('div'); t.className = 'subtag'; t.innerHTML = `<b>${SUBNOME[did + '|' + name]?.nome || name}</b><span>${name}</span>`; labelsEl.appendChild(t);
    tags.push({ el: t, obj: body });
  });
  holo = { g, tags, t0: clock.elapsedTime };
}
function hideTeam() { if (!holo) return; holo.g.parent.remove(holo.g); holo.tags.forEach(t => t.el.remove()); holo = null; }
function setOffset() {
  const w = app.clientWidth, h = app.clientHeight;
  if (selected && !isMobile()) camera.setViewOffset(w, h, 190, 0, w, h);
  else if (selected && isMobile()) camera.setViewOffset(w, h, 0, h * 0.24, w, h);
  else camera.clearViewOffset();
}
function cardHTML(d, extra = '') {
  return `<button class="x" aria-label="Fechar">×</button>
    <span class="kick"><i class="st ${d.st}"></i>${d.setor} · ${ST[d.st]}</span>
    <h2>${d.nome}</h2>
    <p class="nick">“${d.apelido}” · ${d.cargo}</p>
    <p class="meta"><span>${d.bandeira} ${d.nacionalidade}</span><span>${d.cidade}</span><span>${d.idade} anos</span></p>
    <blockquote><small>Regra de ouro</small>${d.regra}</blockquote>
    <h4>O que faz</h4><p class="what">${d.faz}</p>
    <h4>Equipe · ${d.subs.length} subagentes</h4>
    <ol class="team">${d.subs.map((x, i) => `<li><i>${String(i + 1).padStart(2, '0')}</i><span>${SUBNOME[d.id + '|' + x] ? `<b>${SUBNOME[d.id + '|' + x].nome}</b> · ${x}` : x}${SUBJEITO[x] ? `<small>${SUBJEITO[x]}</small>` : ''}</span><em>Estagiário · C$ 0</em></li>`).join('')}</ol>
    <div class="merit"><div><b>C$ 0</b><span>Saldo</span></div><div><b>0 XP</b><span>Carreira</span></div><div><b>${d.id === 'master' ? 'Geral' : 'Diretor'}</b><span>Cargo</span></div></div>
    ${extra}
    ${d.id !== 'master' ? `<p class="trait"><b>Com os pets:</b> ${{ foda: 'a Marnevali solta fogo pra ele e o Carnucci sobe na mesa pra ganhar carinho', ok: 'a Marnevali passa de olho; o Carnucci às vezes visita', fraco: 'a Marnevali passa acuada e o Carnucci não vai até ele' }[humor(d.id)]}${PETS_HUMOR.atualizado ? '' : ' (o humor dos pets começa a valer com a primeira Folha de sexta)'}.</p>` : ''}
    ${GOSTOS[d.id] ? `<p class="trait"><b>Gosta de:</b> ${GOSTOS[d.id].map(k => ITEM[k].nome + (ITEM[k].reais ? ` (C$ ${cs(ITEM[k]).toLocaleString('pt-BR')})` : '')).join(' · ')}</p>` : ''}
    <p class="trait"><b>Jeito:</b> ${d.perfil}</p>
    <p class="trait"><b>Na mesa:</b> ${d.mesa}</p>`;
}
function openPanel(html) { document.body.classList.add('sel'); panel.innerHTML = html; panel.querySelector('.x').onclick = deselect; panel.classList.add('open'); panel.scrollTop = 0; }
function select(s) {
  if (selected === s) return deselect();
  selected = s; controls.autoRotate = false; follow = null;
  if (s === master) {
    openPanel(cardHTML(MASTER, '<p class="trait"><b>Acima dele:</b> Léo e Davi. <b>Abaixo:</b> os diretores e as equipes.</p><button class="povbtn" type="button" data-pov="dir:master">👁 Ver pelos olhos dele</button>'));
    showTeam(master.P.root, MASTER.subs, -1, 'master'); setOffset();
    const p = master.pos.clone(); const dir = new THREE.Vector3(Math.sin(master.heading), 0, Math.cos(master.heading));
    camFly = { pos: p.clone().addScaledVector(dir, 3.4).add(new THREE.Vector3(0, 2.0, 0)), tgt: p.clone().add(new THREE.Vector3(0, 1.2, 0)) };
    return;
  }
  const d = s.d; openPanel(cardHTML(d, `<p class="trait"><b>Hoje:</b> ${s.stats.banheiro} ida(s) ao banheiro, ${s.stats.refil} refil(s) do copo.</p><button class="povbtn" type="button" data-pov="dir:${d.id}">👁 Ver pelos olhos dele</button>`));
  showTeam(s.frame, d.subs, 1, d.id); setOffset();
  const back = new THREE.Vector3(Math.cos(s.a), 0, Math.sin(s.a)), side = new THREE.Vector3(-Math.sin(s.a), 0, Math.cos(s.a));
  const seatW = new THREE.Vector3(Math.cos(s.a) * SEAT_R, 0, Math.sin(s.a) * SEAT_R);
  const pos = seatW.clone().addScaledVector(back, isMobile() ? -4.6 : -3.7).addScaledVector(side, 0.3); pos.y = isMobile() ? 3.1 : 2.6;
  camFly = { pos, tgt: seatW.clone().addScaledVector(back, 0.5).setY(1.05) };
}
function selectThrone(nome) {
  hideTeam(); selected = { thr: nome }; controls.autoRotate = false;
  openPanel(`<button class="x" aria-label="Fechar">×</button><span class="kick">Sócio · CEO</span><h2>${nome}</h2><p class="nick">Cadeira do ${nome}</p>
    <blockquote>Quem decide.</blockquote><p class="what">Léo e Davi sentam um de frente pro outro, no meio dos diretores. O Diretor-Geral traz pra cá só o que precisa de decisão.</p>`);
  setOffset();
  const t = thrones.find(x => x.nome === nome); const back = new THREE.Vector3(Math.cos(t.a), 0, Math.sin(t.a));
  camFly = { pos: back.clone().multiplyScalar(SEAT_R + 3.2).setY(3.0), tgt: back.clone().multiplyScalar(SEAT_R).setY(1.1) };
}
function selectDecor(d) {
  hideTeam(); selected = { decor: d }; controls.autoRotate = false;
  const fmt = iso => iso.split('-').reverse().join('/');
  openPanel(`<button class="x" aria-label="Fechar">×</button><span class="kick">Conquista · Direito de decorar</span><h2>${d.nome}</h2><p class="nick">De ${NOMES[d.dono]} · desde ${fmt(d.desde)}</p><blockquote><small>Por quê</small>${d.porque}</blockquote><p class="what">Diretor que manda bem no mês ganha o direito de colocar no escritório algo que combina com ele. O Claude gera o item a partir da personalidade do diretor, sem precisar de aprovação.</p>`);
  setOffset(); camFly = { pos: new THREE.Vector3(d.pos[0] * 0.78, 2.2, d.pos[1] * 0.78), tgt: new THREE.Vector3(d.pos[0], 0.8, d.pos[1]) };
}
function selectHall() {
  hideTeam(); selected = { hall: true }; controls.autoRotate = false;
  openPanel(`<button class="x" aria-label="Fechar">×</button><span class="kick">Hall da Fama</span><h2>Diretor da Semana e do Mês</h2><p class="what" style="margin-top:12px">Toda sexta, o diretor que mais desenrolou na semana ganha o quadro dele aqui. No fim do mês, sai o Diretor do Mês. A escolha vem do placar do Sistema de Mérito, feita pelo Diretor-Geral.</p><p class="trait"><b>Agora:</b> ${HALL.semana ? NOMES[HALL.semana] : 'em disputa, primeira escolha na sexta 20/11'}.</p>`);
  setOffset(); camFly = { pos: new THREE.Vector3(-2.3, 2.6, 3.4), tgt: new THREE.Vector3(-2.3, 1.3, 7.45) };
}
function deselect() { if (viewMode) { viewMode = false; controls.maxPolarAngle = 1.45; controls.minDistance = 2.5; } document.body.classList.remove('sel'); selected = null; panel.classList.remove('open'); hideTeam(); setOffset(); camFly = { pos: HOME.pos.clone(), tgt: HOME.tgt.clone() }; setTimeout(() => { if (!selected && !follow) controls.autoRotate = rotOn; }, 1800); }

const ray = new THREE.Raycaster(), mouse = new THREE.Vector2(); let downAt = null;
renderer.domElement.addEventListener('pointerdown', e => { downAt = [e.clientX, e.clientY]; });
renderer.domElement.addEventListener('pointerup', e => {
  if (!downAt || Math.hypot(e.clientX - downAt[0], e.clientY - downAt[1]) > 6) return;
  const r = renderer.domElement.getBoundingClientRect(); mouse.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
  ray.setFromCamera(mouse, camera);
  const hit = ray.intersectObjects(pickables, false).find(h => { let o = h.object; while (o) { if (!o.visible) return false; o = o.parent; } return true; });
  if (!hit) return;
  if (hit.object.userData.thr) return selectThrone(hit.object.userData.thr);
  if (hit.object.userData.pet) { const k = hit.object.userData.pet; return selectPet(['pantera', 'tubarao', 'fenix'].includes(k) ? k : 'panda'); }
  if (hit.object.userData.decor) return selectDecor(hit.object.userData.decor);
  if (hit.object.userData.hall) return selectHall();
  if (hit.object.userData.stock) return openStock(hit.object.userData.stock);
  if (hit.object.userData.cadastro) return openCadastro();
  if (hit.object.userData.dirId === 'master') return select(master);
  const s = seats.find(x => x.d.id === hit.object.userData.dirId); if (s) select(s);
});

const $ = id => document.getElementById(id);
$('bRot').onclick = e => { rotOn = !rotOn; controls.autoRotate = rotOn && !selected && !follow; e.currentTarget.classList.toggle('on', rotOn); };
$('bNames').onclick = e => { namesOn = !namesOn; e.currentTarget.classList.toggle('on', namesOn); };
$('bHome').onclick = () => { if (viewMode) { viewMode = false; controls.maxPolarAngle = 1.45; controls.minDistance = 2.5; } follow = null; $('bFollow').classList.remove('on'); if (selected) deselect(); else camFly = { pos: HOME.pos.clone(), tgt: HOME.tgt.clone() }; };
$('bBath').onclick = e => { env.bathView = !env.bathView; env.setBathView(env.bathView); e.currentTarget.classList.toggle('on', env.bathView); if (env.bathView) { controls.autoRotate = false; camFly = { pos: new THREE.Vector3(14.5, 7.5, 12.5), tgt: new THREE.Vector3(10.3, 0.8, 6) }; } };
$('bFollow').onclick = e => { follow = follow ? null : 'phoenix'; e.currentTarget.classList.toggle('on', !!follow); controls.autoRotate = false; if (selected) { selected = null; panel.classList.remove('open'); hideTeam(); setOffset(); } };
$('bHD').onclick = e => { HD = !HD; e.currentTarget.classList.toggle('on', HD); renderer.setPixelRatio(PR()); renderer.setSize(app.clientWidth, app.clientHeight); };
$('bView').onclick = () => { follow = null; controls.autoRotate = false; controls.maxPolarAngle = 1.78; controls.minDistance = 1; viewMode = true; camFly = { pos: new THREE.Vector3(2.5, 1.55, -5.2), tgt: new THREE.Vector3(3.2, 2.15, -8.4) }; };
$('bTV').onclick = () => { follow = null; controls.autoRotate = false; camFly = { pos: new THREE.Vector3(-6.0, 2.3, -3.6), tgt: new THREE.Vector3(-11.8, 2.1, -3.6) }; };
const slider = $('hour'), hourLbl = $('hourLbl');
function hourText(h) { let hh = Math.floor(h), mm = Math.round((h - hh) * 60); if (mm === 60) { hh++; mm = 0; } return `${String(hh % 24).padStart(2, '0')}:${String(mm).padStart(2, '0')}`; }
slider.value = env.hourNow(); hourLbl.textContent = hourText(env.hourNow());
slider.oninput = () => { env.setHour(+slider.value); env.refreshSky(); hourLbl.textContent = hourText(+slider.value); $('bNow').classList.remove('on'); };
$('bNow').onclick = e => { env.setHour(null); env.refreshSky(); slider.value = env.hourNow(); e.currentTarget.classList.add('on'); };
const merit = $('merit');
$('bMerit').onclick = () => merit.classList.add('open');
const LUGAR = { adega: 'Adega', frigobar: 'Frigobar', armario: 'Armário dos Diretores' };
const quem = id => Object.entries(GOSTOS).filter(([, l]) => l.includes(id)).map(([d]) => NOMES[d].split(' ').slice(-1)[0]).join(', ') || '—';
$('stockDate').textContent = ESTOQUE_DATA; $('stockRate').textContent = CAMBIO;
$('stockList').innerHTML = ['adega', 'frigobar', 'armario'].map(l => `<h3 id="sec-${l}">${LUGAR[l]}</h3><div class="tablewrap"><table><thead><tr><th>Item</th><th>Preço real</th><th>C$</th><th>Quem gosta</th></tr></thead><tbody>${ESTOQUE.filter(e => e.onde === l).map(e => `<tr><td><b>${e.nome}</b><br><small>${e.tipo} · ${e.det}${e.url ? ` · <a href="${e.url}" target="_blank" rel="noopener">${e.fonte}</a>` : ` · ${e.fonte}`}</small></td><td class="n">${brl(e.reais)}</td><td class="n">${e.reais ? 'C$ ' + cs(e).toLocaleString('pt-BR') : '—'}</td><td>${quem(e.id)}</td></tr>`).join('')}</tbody></table></div>`).join('');
const gauge = buildGauge(scene, CADASTRO || { pct: 0, pendentes: 0, categorias: [], lista: [] });
function openCadastro() {
  const C = CADASTRO || { pct: 0, categorias: [], lista: [] }, cad = $('cad');
  const ring = (p, s = 46) => { const r = s / 2 - 5, c = 2 * Math.PI * r; return `<svg width="${s}" height="${s}" viewBox="0 0 ${s} ${s}"><circle cx="${s / 2}" cy="${s / 2}" r="${r}" fill="none" stroke="#2a241a" stroke-width="5"/><circle cx="${s / 2}" cy="${s / 2}" r="${r}" fill="none" stroke="${p >= 100 ? '#3ccf7a' : '#d8b46a'}" stroke-width="5" stroke-linecap="round" stroke-dasharray="${c * p / 100} ${c}" transform="rotate(-90 ${s / 2} ${s / 2})"/><text x="50%" y="54%" text-anchor="middle" dominant-baseline="middle" fill="#f2ead8" font-size="12" font-weight="700">${Math.round(p)}</text></svg>`; };
  $('cadPct').textContent = Math.round(C.pct) + '%'; $('cadUpd').textContent = C.atualizado || '';
  $('cadCats').innerHTML = C.categorias.map(c => `<div class="cc">${ring(c.pct)}<div><b>${c.nome}</b><span>${c.feitos}/${c.total} prontos</span></div></div>`).join('');
  $('cadList').innerHTML = C.lista.map(([cat, t, f]) => `<li><b>${t}</b><span>${cat}${f ? ' · falta: ' + f : ''}</span></li>`).join('');
  cad.classList.add('open');
}
{ const C = CADASTRO || { pct: 0, pendentes: 0 }, r = 12, c = 2 * Math.PI * r; $('cadChip').innerHTML = `<svg viewBox="0 0 30 30"><circle cx="15" cy="15" r="${r}" fill="none" stroke="#2a241a" stroke-width="3.5"/><circle cx="15" cy="15" r="${r}" fill="none" stroke="#d8b46a" stroke-width="3.5" stroke-linecap="round" stroke-dasharray="${c * C.pct / 100} ${c}" transform="rotate(-90 15 15)"/></svg><span>Cadastro <b>${Math.round(C.pct)}%</b> · ${C.pendentes} pendências</span>`; $('cadChip').onclick = openCadastro; }
$('cad').querySelector('.x').onclick = () => $('cad').classList.remove('open');
$('cad').addEventListener('click', e => { if (e.target.id === 'cad') e.currentTarget.classList.remove('open'); });
function openStock(lugar) {
  merit.classList.add('open'); merit.querySelector('.tabs button[data-t="t5"]').click();
  const el = lugar && $('sec-' + lugar); if (el) setTimeout(() => el.scrollIntoView({ block: 'start', behavior: 'smooth' }), 60);
}
$('bStock').onclick = () => openStock();
merit.querySelector('.x').onclick = () => merit.classList.remove('open');
merit.addEventListener('click', e => { if (e.target === merit) merit.classList.remove('open'); });
merit.querySelectorAll('.tabs button').forEach(b => b.onclick = () => { merit.querySelectorAll('.tabs button').forEach(x => x.classList.toggle('on', x === b)); merit.querySelectorAll('.tab').forEach(t => t.hidden = t.id !== b.dataset.t); });
document.addEventListener('keydown', e => { if (e.key === 'Escape' && !pov) { merit.classList.remove('open'); if (selected) deselect(); } });
(function fillPayroll() {
  const rows = [[MASTER.nome, 'Diretor-Geral', MASTER.setor, 'C$ 200']].concat(DIRETORES.map(d => [d.nome, 'Diretor', d.setor, 'C$ 120']));
  const sn = (id, x) => SUBNOME[id + '|' + x] ? `${SUBNOME[id + '|' + x].nome} <small>(${x})</small>` : x;
  DIRETORES.forEach(d => d.subs.forEach(x => rows.push([sn(d.id, x), 'Estagiário', d.setor, 'C$ 10'])));
  MASTER.subs.forEach(x => rows.push([sn('master', x), 'Estagiário', MASTER.setor, 'C$ 10']));
  $('payroll').innerHTML = rows.map(([n, c, s, sal]) => `<tr><td>${n}</td><td>${c}</td><td>${s}</td><td class="n">${sal}</td><td class="n">C$ 0</td><td class="n">0</td></tr>`).join('');
  $('headcount').textContent = rows.length;
})();


// ---------- POV: ver pelos olhos de um diretor ou de um bicho ----------
let pov = null, povYaw = 0, povPitch = 0, povDrag = null; const povQ = new THREE.Quaternion(), povSaved = {};
const povList = () => [master, ...seats].map(s => ({ id: 'dir:' + s.d.id, nome: s.d.nome, obj: s.P.head, off: new THREE.Vector3(0, 0.012, 0.16) }))
  .concat([
    { id: 'pet:fenix', nome: 'Marnevali', obj: phoenix.root, off: new THREE.Vector3(0, 0.25, 0.55), world: true, noRoll: true },
    { id: 'pet:panda', nome: 'Carnucci', obj: panda.head, off: new THREE.Vector3(0, 0.03, 0.15), noRoll: true },
    { id: 'pet:pantera', nome: 'Fartuzzi', obj: panther.head, off: new THREE.Vector3(0, 0.06, 0.2) },
    { id: 'pet:tubarao', nome: 'Tubarão Carnucci', obj: aquarium.head, off: new THREE.Vector3(0, 0.07, 0.42) },
  ]);
const _pv = new THREE.Vector3(), _pq = new THREE.Quaternion(), _flip = new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0, 1, 0), Math.PI), _e = new THREE.Euler(0, 0, 0, 'YXZ');
function enterPov(id) {
  const it = povList().find(x => x.id === id); if (!it) return;
  if (!pov) { povSaved.near = camera.near; povSaved.pos = camera.position.clone(); povSaved.tgt = controls.target.clone(); }
  pov = it; povYaw = 0; povPitch = 0; camFly = null; follow = null; controls.enabled = false; controls.autoRotate = false;
  camera.near = 0.02; camera.updateProjectionMatrix(); panel.classList.remove('open'); document.body.classList.remove('sel'); document.body.classList.add('pov');
  $('povName').textContent = it.nome; povStep(true);
}
function exitPov() {
  if (!pov) return; pov = null; document.body.classList.remove('pov'); controls.enabled = true; camera.near = povSaved.near || 0.1; camera.updateProjectionMatrix();
  camera.position.copy(povSaved.pos); controls.target.copy(povSaved.tgt); controls.update();
}
function povCycle(dir) { const L = povList(); const i = pov ? L.findIndex(x => x.id === pov.id) : -1; enterPov(L[(i + dir + L.length) % L.length].id); }
function povStep(snap) {
  const it = pov; it.obj.updateWorldMatrix(true, false);
  if (it.world) { _pv.copy(it.off).applyQuaternion(it.obj.getWorldQuaternion(_pq)).add(it.obj.getWorldPosition(new THREE.Vector3())); }
  else _pv.copy(it.off).applyMatrix4(it.obj.matrixWorld);
  it.obj.getWorldQuaternion(_pq);
  if (it.noRoll) { const f = new THREE.Vector3(0, 0, 1).applyQuaternion(_pq); _e.set(Math.asin(clamp(f.y, -0.6, 0.6)) * 0.5 + povPitch, Math.atan2(-f.x, -f.z) + Math.PI + povYaw, 0); _pq.setFromEuler(_e).multiply(_flip); }
  else { _pq.multiply(_flip); _e.set(povPitch, povYaw, 0); _pq.multiply(new THREE.Quaternion().setFromEuler(_e)); }
  if (snap) povQ.copy(_pq); else povQ.slerp(_pq, 0.25);
  camera.position.copy(_pv); camera.quaternion.copy(povQ);
}
document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-pov]'); if (b) { e.stopPropagation(); enterPov(b.dataset.pov); } });
renderer.domElement.addEventListener('pointerdown', e => { if (pov) povDrag = [e.clientX, e.clientY, povYaw, povPitch]; });
window.addEventListener('pointermove', e => { if (pov && povDrag) { povYaw = clamp(povDrag[2] - (e.clientX - povDrag[0]) * 0.005, -2.6, 2.6); povPitch = clamp(povDrag[3] - (e.clientY - povDrag[1]) * 0.005, -1.2, 1.2); } });
window.addEventListener('pointerup', () => { povDrag = null; });
document.addEventListener('keydown', e => { if (!pov) return; if (e.key === 'Escape') exitPov(); if (e.key === 'ArrowRight') povCycle(1); if (e.key === 'ArrowLeft') povCycle(-1); });
$('bPov').onclick = () => povCycle(1); $('povPrev').onclick = () => povCycle(-1); $('povNext').onclick = () => povCycle(1); $('povExit').onclick = exitPov;

// ---------- retrato do Diretor da Semana/Mês: foto do próprio boneco 3D ----------
function portraitOf(s) {
  const S = 384, rt = new THREE.WebGLRenderTarget(S, S, { samples: 4 }); rt.texture.colorSpace = THREE.SRGBColorSpace;
  const cam = new THREE.PerspectiveCamera(24, 1, 0.05, 10); cam.layers.set(1);
  const head = s.P.head; head.updateWorldMatrix(true, false);
  const h = new THREE.Vector3(0, -0.02, 0).applyMatrix4(head.matrixWorld), q = head.getWorldQuaternion(new THREE.Quaternion());
  const fwd = new THREE.Vector3(0, 0, 1).applyQuaternion(q).setY(0).normalize();
  cam.position.copy(h).addScaledVector(fwd, 0.85).add(new THREE.Vector3(0, 0.03, 0)).addScaledVector(new THREE.Vector3(-fwd.z, 0, fwd.x), 0.12); cam.lookAt(h.x, h.y - 0.03, h.z);
  const on = []; s.P.root.traverse(o => { if (o.isMesh || o.isSkinnedMesh) { o.layers.enable(1); on.push(o); } });
  const lights = []; scene.traverse(o => { if (o.isLight) { o.layers.enable(1); lights.push(o); } });
  const bg = scene.background, fog = scene.fog; scene.background = new THREE.Color(0x1a140e); scene.fog = null;
  renderer.setRenderTarget(rt); renderer.render(scene, cam); renderer.setRenderTarget(null);
  scene.background = bg; scene.fog = fog; on.forEach(o => o.layers.disable(1)); lights.forEach(o => o.layers.disable(1));
  const px = new Uint8Array(S * S * 4); renderer.readRenderTargetPixels(rt, 0, 0, S, S, px); rt.dispose();
  const c = document.createElement('canvas'); c.width = c.height = S; const g = c.getContext('2d'), id = g.createImageData(S, S);
  for (let y = 0; y < S; y++) id.data.set(px.subarray((S - 1 - y) * S * 4, (S - y) * S * 4), y * S * 4);
  g.putImageData(id, 0, 0); return c;
}
setTimeout(() => { try {
  const semana = HALL.semana && [master, ...seats].find(s => s.d.id === HALL.semana); if (semana) hall.setPortrait('semana', portraitOf(semana));
  const mes = HALL.mes && [master, ...seats].find(s => s.d.id === HALL.mes); if (mes) hall.setPortrait('mes', portraitOf(mes));
} catch (err) { console.warn('retrato', err); } }, 2200);

function clampTarget() { const t = controls.target; t.x = clamp(t.x, -11, 11); t.z = clamp(t.z, -8.5, 8.5); t.y = clamp(t.y, 0, 3); }
let frames = 0, lastClock = -9;
function loop() {
  const dt = Math.min(clock.getDelta(), 0.05) * (window.__speed || 1), now = clock.elapsedTime;
  if (camFly && !pov) { const k = 1 - Math.pow(0.03, dt); camera.position.lerp(camFly.pos, k); controls.target.lerp(camFly.tgt, k); if (camera.position.distanceTo(camFly.pos) < 0.02) camFly = null; }
  if (follow === 'phoenix' && phoenix.ready) { const p = phoenix.root.position; const back = new THREE.Vector3(0, 0, -1).applyQuaternion(phoenix.root.quaternion); controls.target.lerp(p, 1 - Math.pow(0.02, dt)); camera.position.lerp(p.clone().addScaledVector(back, 6.5).add(new THREE.Vector3(0, 2.2, 0)), 1 - Math.pow(0.1, dt)); }
  if (!pov) { controls.update(); if (!follow) clampTarget(); }
  env.updaters.forEach(f => f(dt, now)); env.updateWalls(camera);
  if (env.halo) env.halo.visible = camera.position.y < 4.6; // sem teto na visão de cima, o pendente só aparece de dentro da sala
  seats.forEach(s => updateSeat(s, dt, now)); updateMaster(dt, now);
  nextChat -= dt; if (nextChat <= 0) { startChat(); nextChat = 14 + Math.random() * 16; }
  const near = seats.some(s => s.wpos && (s.state === 'walk' || s.state === 'there') && s.kind === 'banheiro' && s.wpos.distanceTo(SPOTS.banheiroPorta) < 1.8);
  env.bathDoor.rotation.y = ease(env.bathDoor.rotation.y, near ? 1.4 : 0, 4, dt);
  frames++; if (frames % 12 === 0) seats[(frames / 12) % seats.length].mb.draw(now);
  gauge.update(dt); aquarium.update(dt, now); phoenix.update(dt, now); panda.update(dt, now); panther.update(dt, now); petTick(dt); pantherTick(dt); pokerTick(dt, now);
  if (selected && (selected.pet === 'panda' || selected.pet === 'pantera') && !camFly) { const q = selected.pet === 'panda' ? panda.root.position : panther.root.position; controls.target.lerp(q.clone().setY(q.y + 0.4), 1 - Math.pow(0.05, dt)); }
  for (let i = puffs.length - 1; i >= 0; i--) { const p = puffs[i]; p.userData.t += dt; const t = p.userData.t - p.userData.d; if (t < 0) continue; p.position.addScaledVector(p.userData.v, dt); const sc = 0.05 + t * 0.35; p.scale.set(sc, sc, sc); p.material.opacity = Math.max(0, 0.45 * (1 - t / 2.2)); if (t > 2.2) { scene.remove(p); p.material.dispose(); puffs.splice(i, 1); } }
  if (holo) {
    const w = app.clientWidth, h = app.clientHeight;
    holo.tags.forEach(t => { const k = clamp((now - holo.t0 - t.obj.userData.k * 0.12) / 0.6, 0, 1); const e = 1 - Math.pow(1 - k, 3); t.obj.scale.y = Math.max(0.001, e); t.obj.position.y = Math.sin(now * 1.6 + t.obj.userData.k) * 0.02; t.el.style.opacity = e * place(t.el, t.obj, 1.0 + (t.obj.userData.k % 3) * 0.34, w, h); });
    holoMat.uniforms.t.value = now;
  }
  scene.environmentIntensity = env.isNight ? 0.35 : 0.5;
  if (pov) povStep(false);
  renderer.render(scene, camera);
  updateLabels();
  if (now - lastClock > 1) { lastClock = now; const h = env.getHour(); const live = $('bNow').classList.contains('on'); $('clock').textContent = `${hourText(h)} em Brasília · ${env.isNight ? 'noite' : 'dia'}${live ? '' : ' (simulado)'}`; if (live) { slider.value = h; hourLbl.textContent = hourText(h); } }
  requestAnimationFrame(loop);
}
// cenário parado: assa em poucas malhas
thrones.forEach(t => t.f.children.forEach(c => { if (c.isGroup) { bakeStatic(c); c.userData.dyn = true; } }));
seats.forEach(s => { bakeStatic(s.chair); s.chair.userData.dyn = true; s.tg.userData.dyn = true; s.hg.userData.dyn = true; Object.values(s.hand).forEach(h => h.userData.dyn = true); });
env.southItems.concat(env.westItems).forEach(g => { if (g.isGroup) { bakeStatic(g); g.userData.dyn = true; } else g.userData.dyn = true; });
env.bathDoor.userData.dyn = true; bakeStatic(env.bathDoor);
decor.forEach(({ g }) => { bakeStatic(g); g.userData.dyn = true; }); bakeStatic(hall); hall.userData.dyn = true;
[stock.fr, stock.ar].forEach(g => { bakeStatic(g); g.userData.dyn = true; });
phoenix.root.userData.dyn = true; panda.root.userData.dyn = true; panther.root.userData.dyn = true; masterP.root.userData.dyn = true; seats.forEach(s => s.P.root.userData.dyn = true);
bakeStatic(scene);
mergeChildren(scene);
pickables.length = 0; scene.traverse(o => { if (o.isMesh && !o.isSkinnedMesh && (o.userData.hit || o.userData.thr || o.userData.pet || o.userData.decor || o.userData.hall || o.userData.stock || o.userData.cadastro) && !(o.userData.dirId && !o.userData.hit)) pickables.push(o); });
// hover: só raycast a cada 120 ms
masterNext();
loop();
log('Expediente rolando: o conselho trabalha 24h');
window.addEventListener('resize', () => { camera.aspect = app.clientWidth / app.clientHeight; setOffset(); camera.updateProjectionMatrix(); renderer.setPixelRatio(PR()); renderer.setSize(app.clientWidth, app.clientHeight); });
window.__mesa = { THREE, aquarium, pov: id => enterPov(id), povExit: () => exitPov(), panther, poker, pokerNow: () => { poker.t = 0; }, pit, petHumor: (id, m) => { PETS_HUMOR.humor[id] = m; }, petNow: () => { fenixT = 0; pandaT = 0; }, renderer, scene, panda, pet: k => selectPet(k), select: i => select(seats[i]), master: () => select(master), seats, camera, controls, env, goOut: (i, k) => goOut(seats[i], k, clock.elapsedTime), phoenix, setHour: h => { env.setHour(h); env.refreshSky(); }, view: () => $('bView').click(), fly: (p, t) => { camFly = { pos: new THREE.Vector3(...p), tgt: new THREE.Vector3(...t) }; controls.autoRotate = false; follow = null; }, bath: () => $('bBath').click(), snap: () => { if (camFly) { camera.position.copy(camFly.pos); controls.target.copy(camFly.tgt); camFly = null; } } };
