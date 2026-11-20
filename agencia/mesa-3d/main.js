import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/examples/jsm/postprocessing/OutputPass.js';
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js';
import { DIRETORES, MASTER, FATURAMENTO } from './data.js';
import { M, mat, mesh, box, sph, lerp, clamp, smooth, ease, angLerp } from './util.js';
import { buildEnv, SPOTS, TABLE_R, TOP_Y, ROOM } from './env.js';
import { buildPerson, blendPose, sitLegs, standLegs, faceTick } from './people.js';
import { macbook, glassOf, cigar, phone, newspaper, tableProps, chair, throne, plateTex, smokeTex } from './props.js';
import { buildPhoenix } from './phoenix.js';
import { buildRedPanda } from './pets.js';

const LOGO = window.__LOGO__;
const app = document.getElementById('app');
const isMobile = () => window.innerWidth < 760;

const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance', preserveDrawingBuffer: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
renderer.setSize(app.clientWidth, app.clientHeight);
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
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
const rt = new THREE.WebGLRenderTarget(app.clientWidth, app.clientHeight, { type: THREE.HalfFloatType, stencilBuffer: true, samples: isMobile() ? 2 : 4 });
const composer = new EffectComposer(renderer, rt);
composer.setPixelRatio(renderer.getPixelRatio()); composer.setSize(app.clientWidth, app.clientHeight);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(app.clientWidth / 2, app.clientHeight / 2), 0.35, 0.4, 2.6);
composer.addPass(bloom); composer.addPass(new OutputPass());
const env = buildEnv(scene, renderer, LOGO, FATURAMENTO);
const clock = new THREE.Clock();

// ---------- assentos ----------
const SEAT_R = 3.3, RING = 4.75;
const deg = d => d * Math.PI / 180;
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
  const t = throne(plateTex(nome, 'Sócio · CEO')); f.add(t);
  t.traverse(o => { if (o.isMesh) { o.userData.thr = nome; pickables.push(o); } });
  macbook(f, 0, 0.7, 0, 'money').group.position.y = TOP_Y;
  const g = glassOf('whisky'); g.position.set(0.34, TOP_Y, 0.62); f.add(g);
  thrones.push({ nome, a, f });
});

function addTag(html, cls = '') { const el = document.createElement('button'); el.type = 'button'; el.className = 'tag ' + cls; el.innerHTML = html; labelsEl.appendChild(el); return el; }
function addBubble() { const el = document.createElement('div'); el.className = 'bubble'; labelsEl.appendChild(el); return el; }

DIRETORES.forEach((d, i) => {
  const a = angles[i];
  const frame = frameAt(a);
  const ch = chair(plateTex(d.nome, d.setor)); frame.add(ch);
  const P = buildPerson(d); frame.add(P.root); sitLegs(P);
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
const masterP = buildPerson(MASTER);
const master = { d: MASTER, P: masterP, pos: new THREE.Vector3(5.2, 0, -4.6), heading: -2.2, state: 'idle', t: 4, phase: 0, path: null, leg: 0, target: null, bubble: addBubble() };
scene.add(masterP.root); standLegs(masterP, 0, false); blendPose(masterP, 'armsCross', 'armsCross', 1);
masterP.root.traverse(o => { if (o.isMesh) { o.userData.dirId = 'master'; pickables.push(o); } });
master.tag = addTag(`<b>${MASTER.nome}</b><span>${MASTER.cargo}</span>`, 'master'); master.tag.addEventListener('click', e => { e.stopPropagation(); select(master); });

const phoenix = buildPhoenix(scene, window.__PARROT__);
phoenix.onBreath = () => log('<b>Marnevali</b> soltou fogo');
const panda = buildRedPanda(scene);
panda.root.traverse(o => { if (o.isMesh) pickables.push(o); });
const PETS = {
  fenix: { nome: 'Marnevali', tipo: 'Fênix · mascote da Carnucci', txt: 'Voa pela sala o dia inteiro e, de vez em quando, solta fogo. Renasce das cinzas, como a empresa que não para.' },
  panda: { nome: 'Carnucci', tipo: 'Panda-vermelho · mascote da Carnucci', txt: 'Anda pelo escritório, senta pra olhar o movimento e tira cochilos no tapete do lounge.' },
};
const pandaTag = addTag('<b>Carnucci</b><span>Panda-vermelho</span>', 'pet'); pandaTag.addEventListener('click', e => { e.stopPropagation(); selectPet('panda'); });
const fenixTag = addTag('<b>Marnevali</b><span>Fênix</span>', 'pet'); fenixTag.addEventListener('click', e => { e.stopPropagation(); selectPet('fenix'); });
function selectPet(k) {
  hideTeam(); const p = PETS[k]; selected = { pet: k }; controls.autoRotate = false;
  openPanel(`<button class="x" aria-label="Fechar">×</button><span class="kick">Mascote</span><h2>${p.nome}</h2><p class="nick">${p.tipo}</p><p class="what" style="margin-top:14px">${p.txt}</p>`);
  setOffset();
  if (k === 'fenix') { follow = 'phoenix'; document.getElementById('bFollow').classList.add('on'); }
  else { const q = panda.root.position; camFly = { pos: q.clone().add(new THREE.Vector3(1.6, 1.3, 1.6)), tgt: q.clone().add(new THREE.Vector3(0, 0.3, 0)) }; selected.track = true; }
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
  const dest = kind === 'refil' ? (s.drink === 'whisky' ? SPOTS.uisque : s.drink === 'cafe' ? SPOTS.cafe : SPOTS.agua) : kind === 'banheiro' ? SPOTS.banheiro : [SPOTS.janelaN1, SPOTS.janelaN2, SPOTS.janelaL][Math.floor(Math.random() * 3)];
  s.state = 'standup'; s.t0 = now; s.kind = kind; s.path = pathTo(s, dest); s.leg = 0; s.dir = 1; s.act = 'work';
  s.bubble.classList.remove('on');
  Object.values(s.hand).forEach(h => h.visible = false);
  if (kind === 'refil') { s.tg.visible = false; s.hg.visible = true; } else { s.hg.visible = false; s.tg.visible = true; }
  const txt = { banheiro: 'foi ao banheiro', refil: s.drink === 'whisky' ? 'foi na adega encher o copo' : s.drink === 'cafe' ? 'foi buscar mais um café' : 'foi encher o copo d’água', janela: 'foi olhar a vista' }[kind];
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
  if (frame) { const local = frame.worldToLocal(tmpW.copy(obj.wpos)); P.root.position.copy(local); if (dist > 0.001) { const dl = frame.worldToLocal(tmpW.copy(obj.wpos).add(tmpV)).sub(local); obj.yaw = angLerp(obj.yaw ?? 0, Math.atan2(dl.x, dl.z), Math.min(1, dt * 8)); } P.root.rotation.y = obj.yaw; }
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
    P.head.rotation.y = ease(P.head.rotation.y, headYaw, 5, dt); P.head.rotation.x = ease(P.head.rotation.x, headPitch, 5, dt);
    P.torso.rotation.x = ease(P.torso.rotation.x, lean, 3, dt);
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
function showTeam(anchor, subs, back = 1) {
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
    const t = document.createElement('div'); t.className = 'subtag'; t.innerHTML = `<b>${name}</b><span>Estagiário · C$ 0</span>`; labelsEl.appendChild(t);
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
    <ol class="team">${d.subs.map((x, i) => `<li><i>${String(i + 1).padStart(2, '0')}</i><span>${x}</span><em>Estagiário · C$ 0</em></li>`).join('')}</ol>
    <div class="merit"><div><b>C$ 0</b><span>Saldo</span></div><div><b>0 XP</b><span>Carreira</span></div><div><b>${d.id === 'master' ? 'Geral' : 'Diretor'}</b><span>Cargo</span></div></div>
    ${extra}
    <p class="trait"><b>Jeito:</b> ${d.perfil}</p>
    <p class="trait"><b>Na mesa:</b> ${d.mesa}</p>`;
}
function openPanel(html) { document.body.classList.add('sel'); panel.innerHTML = html; panel.querySelector('.x').onclick = deselect; panel.classList.add('open'); panel.scrollTop = 0; }
function select(s) {
  if (selected === s) return deselect();
  selected = s; controls.autoRotate = false; follow = null;
  if (s === master) {
    openPanel(cardHTML(MASTER, '<p class="trait"><b>Acima dele:</b> Léo e Davi. <b>Abaixo:</b> os 10 diretores e as equipes.</p>'));
    showTeam(master.P.root, MASTER.subs, -1); setOffset();
    const p = master.pos.clone(); const dir = new THREE.Vector3(Math.sin(master.heading), 0, Math.cos(master.heading));
    camFly = { pos: p.clone().addScaledVector(dir, 3.4).add(new THREE.Vector3(0, 2.0, 0)), tgt: p.clone().add(new THREE.Vector3(0, 1.2, 0)) };
    return;
  }
  const d = s.d; openPanel(cardHTML(d, `<p class="trait"><b>Hoje:</b> ${s.stats.banheiro} ida(s) ao banheiro, ${s.stats.refil} refil(s) do copo.</p>`));
  showTeam(s.frame, d.subs); setOffset();
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
  if (hit.object.userData.pet) return selectPet('panda');
  if (hit.object.userData.dirId === 'master') return select(master);
  const s = seats.find(x => x.d.id === hit.object.userData.dirId); if (s) select(s);
});

const $ = id => document.getElementById(id);
$('bRot').onclick = e => { rotOn = !rotOn; controls.autoRotate = rotOn && !selected && !follow; e.currentTarget.classList.toggle('on', rotOn); };
$('bNames').onclick = e => { namesOn = !namesOn; e.currentTarget.classList.toggle('on', namesOn); };
$('bHome').onclick = () => { if (viewMode) { viewMode = false; controls.maxPolarAngle = 1.45; controls.minDistance = 2.5; } follow = null; $('bFollow').classList.remove('on'); if (selected) deselect(); else camFly = { pos: HOME.pos.clone(), tgt: HOME.tgt.clone() }; };
$('bBath').onclick = e => { env.bathView = !env.bathView; env.setBathView(env.bathView); e.currentTarget.classList.toggle('on', env.bathView); if (env.bathView) { controls.autoRotate = false; camFly = { pos: new THREE.Vector3(14.5, 7.5, 12.5), tgt: new THREE.Vector3(10.3, 0.8, 6) }; } };
$('bFollow').onclick = e => { follow = follow ? null : 'phoenix'; e.currentTarget.classList.toggle('on', !!follow); controls.autoRotate = false; if (selected) { selected = null; panel.classList.remove('open'); hideTeam(); setOffset(); } };
$('bView').onclick = () => { follow = null; controls.autoRotate = false; controls.maxPolarAngle = 1.78; controls.minDistance = 1; viewMode = true; camFly = { pos: new THREE.Vector3(2.5, 1.55, -5.2), tgt: new THREE.Vector3(3.2, 2.15, -8.4) }; };
$('bTV').onclick = () => { follow = null; controls.autoRotate = false; camFly = { pos: new THREE.Vector3(-6.0, 2.3, -3.6), tgt: new THREE.Vector3(-11.8, 2.1, -3.6) }; };
const slider = $('hour'), hourLbl = $('hourLbl');
function hourText(h) { let hh = Math.floor(h), mm = Math.round((h - hh) * 60); if (mm === 60) { hh++; mm = 0; } return `${String(hh % 24).padStart(2, '0')}:${String(mm).padStart(2, '0')}`; }
slider.value = env.hourNow(); hourLbl.textContent = hourText(env.hourNow());
slider.oninput = () => { env.setHour(+slider.value); env.refreshSky(); hourLbl.textContent = hourText(+slider.value); $('bNow').classList.remove('on'); };
$('bNow').onclick = e => { env.setHour(null); env.refreshSky(); slider.value = env.hourNow(); e.currentTarget.classList.add('on'); };
const merit = $('merit');
$('bMerit').onclick = () => merit.classList.add('open');
merit.querySelector('.x').onclick = () => merit.classList.remove('open');
merit.addEventListener('click', e => { if (e.target === merit) merit.classList.remove('open'); });
merit.querySelectorAll('.tabs button').forEach(b => b.onclick = () => { merit.querySelectorAll('.tabs button').forEach(x => x.classList.toggle('on', x === b)); merit.querySelectorAll('.tab').forEach(t => t.hidden = t.id !== b.dataset.t); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') { merit.classList.remove('open'); if (selected) deselect(); } });
(function fillPayroll() {
  const rows = [[MASTER.nome, 'Diretor-Geral', MASTER.setor, 'C$ 200']].concat(DIRETORES.map(d => [d.nome, 'Diretor', d.setor, 'C$ 120']));
  DIRETORES.forEach(d => d.subs.forEach(x => rows.push([x, 'Estagiário', d.setor, 'C$ 10'])));
  MASTER.subs.forEach(x => rows.push([x, 'Estagiário', MASTER.setor, 'C$ 10']));
  $('payroll').innerHTML = rows.map(([n, c, s, sal]) => `<tr><td>${n}</td><td>${c}</td><td>${s}</td><td class="n">${sal}</td><td class="n">C$ 0</td><td class="n">0</td></tr>`).join('');
  $('headcount').textContent = rows.length;
})();

function clampTarget() { const t = controls.target; t.x = clamp(t.x, -11, 11); t.z = clamp(t.z, -8.5, 8.5); t.y = clamp(t.y, 0, 3); }
let frames = 0, lastClock = -9;
function loop() {
  const dt = Math.min(clock.getDelta(), 0.05), now = clock.elapsedTime;
  if (camFly) { const k = 1 - Math.pow(0.03, dt); camera.position.lerp(camFly.pos, k); controls.target.lerp(camFly.tgt, k); if (camera.position.distanceTo(camFly.pos) < 0.02) camFly = null; }
  if (follow === 'phoenix' && phoenix.ready) { const p = phoenix.root.position; const back = new THREE.Vector3(0, 0, -1).applyQuaternion(phoenix.root.quaternion); controls.target.lerp(p, 1 - Math.pow(0.02, dt)); camera.position.lerp(p.clone().addScaledVector(back, 6.5).add(new THREE.Vector3(0, 2.2, 0)), 1 - Math.pow(0.1, dt)); }
  controls.update(); if (!follow) clampTarget();
  env.updaters.forEach(f => f(dt, now)); env.updateWalls(camera);
  seats.forEach(s => updateSeat(s, dt, now)); updateMaster(dt, now);
  nextChat -= dt; if (nextChat <= 0) { startChat(); nextChat = 14 + Math.random() * 16; }
  const near = seats.some(s => s.wpos && (s.state === 'walk' || s.state === 'there') && s.kind === 'banheiro' && s.wpos.distanceTo(SPOTS.banheiroPorta) < 1.8);
  env.bathDoor.rotation.y = ease(env.bathDoor.rotation.y, near ? 1.4 : 0, 4, dt);
  frames++; seats[frames % seats.length].mb.draw(now);
  phoenix.update(dt, now); panda.update(dt, now);
  if (selected && selected.pet === 'panda' && !camFly) controls.target.lerp(panda.root.position.clone().setY(0.3), 1 - Math.pow(0.05, dt));
  for (let i = puffs.length - 1; i >= 0; i--) { const p = puffs[i]; p.userData.t += dt; const t = p.userData.t - p.userData.d; if (t < 0) continue; p.position.addScaledVector(p.userData.v, dt); const sc = 0.05 + t * 0.35; p.scale.set(sc, sc, sc); p.material.opacity = Math.max(0, 0.45 * (1 - t / 2.2)); if (t > 2.2) { scene.remove(p); p.material.dispose(); puffs.splice(i, 1); } }
  if (holo) {
    const w = app.clientWidth, h = app.clientHeight;
    holo.tags.forEach(t => { const k = clamp((now - holo.t0 - t.obj.userData.k * 0.12) / 0.6, 0, 1); const e = 1 - Math.pow(1 - k, 3); t.obj.scale.y = Math.max(0.001, e); t.obj.position.y = Math.sin(now * 1.6 + t.obj.userData.k) * 0.02; t.el.style.opacity = e * place(t.el, t.obj, 1.02 + (t.obj.userData.k % 2) * 0.2, w, h); });
    holoMat.uniforms.t.value = now;
  }
  scene.environmentIntensity = env.isNight ? 0.25 : 0.45; bloom.strength = env.isNight ? 0.55 : 0.3;
  composer.render();
  updateLabels();
  if (now - lastClock > 1) { lastClock = now; const h = env.getHour(); const live = $('bNow').classList.contains('on'); $('clock').textContent = `${hourText(h)} em Brasília · ${env.isNight ? 'noite' : 'dia'}${live ? '' : ' (simulado)'}`; if (live) { slider.value = h; hourLbl.textContent = hourText(h); } }
  requestAnimationFrame(loop);
}
masterNext();
loop();
log('Expediente rolando: o conselho trabalha 24h');
window.addEventListener('resize', () => { camera.aspect = app.clientWidth / app.clientHeight; setOffset(); camera.updateProjectionMatrix(); renderer.setSize(app.clientWidth, app.clientHeight); composer.setSize(app.clientWidth, app.clientHeight); });
window.__mesa = { scene, panda, pet: k => selectPet(k), select: i => select(seats[i]), master: () => select(master), seats, camera, controls, env, goOut: (i, k) => goOut(seats[i], k, clock.elapsedTime), phoenix, setHour: h => { env.setHour(h); env.refreshSky(); }, view: () => $('bView').click(), fly: (p, t) => { camFly = { pos: new THREE.Vector3(...p), tgt: new THREE.Vector3(...t) }; controls.autoRotate = false; follow = null; }, bath: () => $('bBath').click(), snap: () => { if (camFly) { camera.position.copy(camFly.pos); controls.target.copy(camFly.tgt); camFly = null; } } };
