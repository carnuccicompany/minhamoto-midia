import * as THREE from 'three';
import { M, mat, phys, mesh, box, rbox, cyl, sph, tex, lerp, clamp, smooth } from './util.js';

const pinTex = tex(256, 256, (g, w, h) => { g.fillStyle = '#fff'; g.fillRect(0, 0, w, h); g.fillStyle = 'rgba(0,0,0,.08)'; for (let x = 0; x < w; x += 24) g.fillRect(x, 0, 2, h); }, [5, 2]);
const fabricTex = tex(256, 256, (g, w, h) => { g.fillStyle = '#fff'; g.fillRect(0, 0, w, h); for (let i = 0; i < 9000; i++) { g.fillStyle = `rgba(0,0,0,${Math.random() * .06})`; g.fillRect(Math.random() * w, Math.random() * h, 1, 2); } }, [6, 6]);

// membro afunilado com articulação arredondada no topo
function limb(len, r0, r1, m, parent) {
  const g = new THREE.Group(); parent.add(g);
  mesh(cyl(r1, r0, len, 20), m, g, [0, -len / 2, 0]);
  mesh(sph(r0, 18, 12), m, g, [0, 0, 0]);
  return g;
}
function lathe(points, m, parent, pos, scaleZ = 1, scaleX = 1) {
  const geo = new THREE.LatheGeometry(points.map(([r, y]) => new THREE.Vector2(r, y)), 40);
  const o = mesh(geo, m, parent, pos); o.scale.set(scaleX, 1, scaleZ); return o;
}

// mão com dedos (palma pra baixo, dedos apontando pra -Y local do antebraço)
function hand(parent, skin, side) {
  const h = new THREE.Group(); parent.add(h);
  mesh(rbox(0.075, 0.085, 0.028, 0.012), skin, h, [0, -0.04, 0]);
  for (let i = 0; i < 4; i++) {
    const f = new THREE.Group(); f.position.set(-0.027 + i * 0.018, -0.082, 0); f.rotation.x = 0.25; h.add(f);
    const L = [0.034, 0.042, 0.039, 0.03][i];
    mesh(new THREE.CapsuleGeometry(0.0075, L, 4, 8), skin, f, [0, -L / 2, 0]);
  }
  const th = new THREE.Group(); th.position.set(side * 0.036, -0.03, 0.01); th.rotation.set(0.3, 0, side * 0.7); h.add(th);
  mesh(new THREE.CapsuleGeometry(0.009, 0.03, 4, 8), skin, th, [0, -0.02, 0]);
  return h;
}

export function buildPerson(d) {
  const W = !!d.mulher;
  const suit = phys(d.terno, { roughness: 0.66, map: d.risca ? pinTex : fabricTex, sheen: 0.35, sheenRoughness: 0.6, sheenColor: new THREE.Color(0xffffff).multiplyScalar(0.25) });
  const pants = suit;
  const skin = phys(d.pele, { roughness: 0.55, sheen: 0.25, sheenColor: new THREE.Color(0xff9a7a), sheenRoughness: 0.5 });
  const hairM = phys(d.cabelo, { roughness: 0.55, sheen: 0.6, sheenColor: new THREE.Color(0xffffff).multiplyScalar(0.25) });
  const shirtM = d.camisa ? mat(d.camisa, { roughness: 0.6 }) : M.shirt;
  const root = new THREE.Group();
  const pelvis = new THREE.Group(); root.add(pelvis);
  const P = { root, pelvis, legs: [], knees: [], feet: [], sh: [], el: [], wr: [], d };

  // pernas
  [-1, 1].forEach(s => {
    const hip = new THREE.Group(); hip.position.set(s * (W ? 0.088 : 0.098), 0, 0); pelvis.add(hip);
    limb(0.45, W ? 0.082 : 0.088, W ? 0.06 : 0.066, pants, hip);
    const knee = new THREE.Group(); knee.position.y = -0.45; hip.add(knee);
    limb(0.44, W ? 0.06 : 0.066, 0.046, pants, knee);
    const ankle = new THREE.Group(); ankle.position.y = -0.44; knee.add(ankle);
    mesh(cyl(0.042, 0.042, 0.05, 12), M.sock, ankle, [0, 0.01, 0]);
    const shoe = mesh(new THREE.CapsuleGeometry(0.046, 0.17, 6, 12), M.shoe, ankle, [0, -0.03, 0.07], [Math.PI / 2, 0, 0]); shoe.scale.set(W ? 0.85 : 1, 1, 0.62);
    if (W) mesh(cyl(0.012, 0.008, 0.06, 8), M.shoe, ankle, [0, -0.03, -0.04]);
    P.legs.push(hip); P.knees.push(knee); P.feet.push(ankle);
  });
  // quadril
  const hipM = mesh(sph(0.17, 24, 16), pants, pelvis, [0, 0.02, -0.01]); hipM.scale.set(W ? 1.08 : 1.0, 0.62, 0.78);

  // tronco (paletó) por perfil de torno
  const torso = new THREE.Group(); torso.position.y = 0.04; pelvis.add(torso); P.torso = torso;
  const prof = W ? [[0.16, 0], [0.15, 0.08], [0.135, 0.18], [0.155, 0.3], [0.17, 0.4], [0.165, 0.47], [0.13, 0.53], [0.06, 0.575]]
                 : [[0.165, 0], [0.165, 0.08], [0.16, 0.18], [0.178, 0.3], [0.196, 0.41], [0.198, 0.47], [0.158, 0.54], [0.065, 0.585]];
  lathe(prof, suit, torso, [0, 0, 0], 0.64, 1.0);
  const zf = (W ? 0.158 : 0.178) * 0.64; // frente do peito
  // camisa / blusa em V e gravata
  const vShape = new THREE.Shape(); vShape.moveTo(-0.055, 0.55); vShape.lineTo(0.055, 0.55); vShape.lineTo(0, W ? 0.33 : 0.26); vShape.closePath();
  const vMesh = mesh(new THREE.ShapeGeometry(vShape), W ? mat(0xebe5da, { roughness: 0.55 }) : shirtM, torso, [0, 0, zf + 0.012], [-0.12, 0, 0], false);
  if (d.gravata) {
    const tie = new THREE.Shape(); tie.moveTo(-0.014, 0.53); tie.lineTo(0.014, 0.53); tie.lineTo(0.022, 0.3); tie.lineTo(0, 0.27); tie.lineTo(-0.022, 0.3); tie.closePath();
    mesh(new THREE.ShapeGeometry(tie), phys(d.gravata, { roughness: 0.35, sheen: 0.6 }), torso, [0, 0, zf + 0.016], [-0.12, 0, 0], false);
    mesh(sph(0.018, 10, 8), phys(d.gravata, { roughness: 0.35 }), torso, [0, 0.535, zf + 0.0], null, false).scale.set(1.2, 0.9, 0.7);
  }
  if (d.colete) { const vest = new THREE.Shape(); vest.moveTo(-0.07, 0.42); vest.lineTo(0.07, 0.42); vest.lineTo(0.09, 0.12); vest.lineTo(0, 0.08); vest.lineTo(-0.09, 0.12); vest.closePath(); mesh(new THREE.ShapeGeometry(vest), mat(0x2a2a2e, { roughness: 0.6 }), torso, [0, 0, zf + 0.008], [-0.04, 0, 0], false); }
  // lapelas
  [-1, 1].forEach(s => {
    const lap = new THREE.Shape(); lap.moveTo(s * 0.055, 0.55); lap.lineTo(s * 0.1, 0.5); lap.lineTo(s * 0.075, 0.45); lap.lineTo(s * 0.03, 0.22); lap.lineTo(s * 0.0, W ? 0.33 : 0.26); lap.closePath();
    const lm = mesh(new THREE.ShapeGeometry(lap), suit, torso, [0, 0, zf + 0.02], [-0.12, 0, 0], false); lm.material = suit; lm.material.side = THREE.DoubleSide;
  });
  [0.2, 0.12].forEach(y => mesh(sph(0.009, 10, 8), M.black, torso, [0, y, (0.165) * 0.64 + 0.004], null, false));
  mesh(box(0.05, 0.022, 0.006), M.gold, torso, [0.09, 0.44, zf + 0.008], [0, 0.25, 0], false); // lenço de bolso
  // ombros
  [-1, 1].forEach(s => mesh(sph(0.062, 18, 12), suit, torso, [s * (W ? 0.16 : 0.182), 0.49, -0.005], null).scale.set(1.1, 0.62, 1.0));
  // pescoço e colarinho
  mesh(cyl(0.05, 0.056, 0.12, 16), skin, torso, [0, 0.62, 0.005]);
  if (!W) mesh(new THREE.TorusGeometry(0.056, 0.014, 8, 20, Math.PI * 1.4), shirtM, torso, [0, 0.585, 0.005], [Math.PI / 2, 0, Math.PI * 0.8], false);
  else mesh(new THREE.TorusGeometry(0.05, 0.005, 8, 24, Math.PI), M.gold, torso, [0, 0.57, 0.03], [0.35, 0, Math.PI], false);

  // braços
  [-1, 1].forEach(s => {
    const sh = new THREE.Group(); sh.position.set(s * (W ? 0.175 : 0.2), 0.49, -0.01); torso.add(sh);
    limb(0.29, W ? 0.048 : 0.054, W ? 0.04 : 0.045, suit, sh);
    const el = new THREE.Group(); el.position.y = -0.29; sh.add(el);
    limb(0.27, W ? 0.04 : 0.045, W ? 0.034 : 0.038, suit, el);
    mesh(cyl(0.036, 0.036, 0.03, 14), shirtM, el, [0, -0.265, 0], null, false);
    if (s === 1) mesh(cyl(0.03, 0.03, 0.016, 18), M.gold, el, [0, -0.25, 0.012], [Math.PI / 2, 0, 0], false);
    const wr = new THREE.Group(); wr.position.y = -0.28; el.add(wr);
    hand(wr, skin, -s);
    P.sh.push(sh); P.el.push(el); P.wr.push(wr);
  });

  // cabeça
  const head = new THREE.Group(); head.position.set(0, 0.79, 0.012); torso.add(head); P.head = head;
  const cran = mesh(sph(0.1, 32, 24), skin, head, [0, 0.03, -0.005]); cran.scale.set(W ? 0.88 : 0.92, 1.02, 1.03);
  const jaw = mesh(sph(0.088, 32, 24), skin, head, [0, -0.035, 0.012]); jaw.scale.set(W ? 0.84 : 0.92, 1.06, 0.98);
  mesh(sph(0.036, 16, 12), skin, head, [0, -0.1, 0.055]).scale.set(W ? 1.0 : 1.25, 0.8, 0.9); // queixo
  [-1, 1].forEach(s => mesh(sph(0.03, 14, 10), skin, head, [s * 0.05, -0.02, 0.06], null, false).scale.set(1, 0.8, 0.7)); // maçãs
  const nose = mesh(new THREE.ConeGeometry(0.018, 0.05, 12), skin, head, [0, -0.012, 0.098], [Math.PI / 2 - 0.35, 0, 0], false);
  mesh(sph(0.016, 12, 10), skin, head, [0, -0.034, 0.1], null, false).scale.set(1.4, 0.8, 0.9);
  // olhos (com pálpebra que pisca)
  const eyes = new THREE.Group(); head.add(eyes); P.eyes = [];
  [-1, 1].forEach(s => {
    const e = new THREE.Group(); e.position.set(s * 0.035, 0.008, 0.08); eyes.add(e);
    mesh(sph(0.0128, 16, 12), M.sclera, e, null, null, false);
    const iris = mesh(sph(0.0078, 12, 10), phys(d.olhosCor || 0x2a1a10, { roughness: 0.1, clearcoat: 1 }), e, [0, 0, 0.0105], null, false); iris.scale.set(1, 1, 0.5); iris.position.z = 0.0085;
    mesh(sph(0.004, 8, 6), M.black, e, [0, 0, 0.0122], null, false);
    const lid = mesh(new THREE.SphereGeometry(0.0139, 16, 10, 0, Math.PI * 2, 0, Math.PI * 0.5), skin, e, null, [-0.6, 0, 0], false);
    if (d.olhos === 'puxados') { e.scale.set(1.15, 0.72, 1); e.rotation.z = s * -0.12; }
    if (W) mesh(box(0.03, 0.003, 0.004), M.black, e, [s * 0.004, 0.013, 0.012], [0, 0, s * -0.25], false); // cílios
    P.eyes.push({ e, lid });
  });
  // sobrancelhas
  const browM = phys(d.estilo === 'grisalho' && d.barbaCor ? d.barbaCor : d.cabelo, { roughness: 0.9 });
  P.brows = [-1, 1].map(s => mesh(rbox(0.036, 0.008, 0.01, 0.003), browM, head, [s * 0.037, 0.035, 0.088], [0.1, 0, s * (W ? -0.14 : 0.06)], false));
  // boca
  const lipC = W ? 0x9a2a36 : new THREE.Color(d.pele).multiplyScalar(0.72).getHex();
  P.mouth = new THREE.Group(); P.mouth.position.set(0, -0.062, 0.085); head.add(P.mouth);
  mesh(new THREE.CapsuleGeometry(0.0065, 0.03, 4, 8), phys(lipC, { roughness: 0.35, clearcoat: W ? 0.6 : 0 }), P.mouth, [0, 0.004, 0], [0, 0, Math.PI / 2], false);
  P.lowerLip = mesh(new THREE.CapsuleGeometry(0.0072, 0.026, 4, 8), phys(lipC, { roughness: 0.35, clearcoat: W ? 0.6 : 0 }), P.mouth, [0, -0.007, -0.001], [0, 0, Math.PI / 2], false);
  // orelhas
  [-1, 1].forEach(s => mesh(sph(0.026, 14, 10), skin, head, [s * 0.088, 0.0, -0.005]).scale.set(0.35, 1, 0.65));
  if (W) [-1, 1].forEach(s => mesh(sph(0.009, 10, 8), M.gold, head, [s * 0.09, -0.03, 0.0], null, false));

  // cabelo
  const st = d.estilo, F = 0.95;
  const capR = 0.106;
  const cap = (th, rx = -0.3) => { const c = mesh(new THREE.SphereGeometry(capR, 32, 14, 0, Math.PI * 2, 0, Math.PI * th), hairM, head, [0, 0.036, -0.008]); c.scale.set(W ? 0.92 : 0.96, 1.06, 1.06); c.rotation.x = rx; return c; };
  const band = (t0, t1, f = F, r = capR) => { const b = mesh(new THREE.SphereGeometry(r, 32, 12, Math.PI / 2 + f, Math.PI * 2 - 2 * f, Math.PI * t0, Math.PI * (t1 - t0)), hairM, head, [0, 0.03, -0.008]); b.scale.set(W ? 0.92 : 0.97, 1.06, 1.06); return b; };
  if (st === 'raspado') { const c = cap(0.42); c.material = phys(d.cabelo, { roughness: 1, transparent: true, opacity: 0.6 }); }
  else {
    cap(st === 'grisalho' ? 0.36 : 0.42);
    band(0.25, st === 'chanel' ? 0.72 : st === 'longo' ? 0.66 : 0.58, st === 'chanel' || st === 'longo' ? 0.82 : F);
    if (st === 'penteado') { const top = mesh(sph(0.075, 20, 12), hairM, head, [0, 0.105, 0.02]); top.scale.set(1.3, 0.55, 1.5); top.rotation.x = -0.2; }
    if (st === 'liso') { const fr = mesh(sph(0.06, 16, 10), hairM, head, [0.02, 0.085, 0.07]); fr.scale.set(1.6, 0.5, 0.7); fr.rotation.z = -0.2; }
    if (st === 'curto' || st === 'grisalho') { const top = mesh(sph(0.07, 16, 10), hairM, head, [0, 0.1, 0.03]); top.scale.set(1.35, 0.45, 1.3); }
    if (st === 'longo') {
      const back = mesh(new THREE.CapsuleGeometry(0.085, 0.26, 6, 16), hairM, head, [0, -0.13, -0.065]); back.scale.set(1.25, 1, 0.5);
      [-1, 1].forEach(s => { const lk = mesh(new THREE.CapsuleGeometry(0.026, 0.22, 4, 10), hairM, head, [s * 0.092, -0.11, 0.025]); lk.rotation.z = s * 0.05; });
      const fr = mesh(sph(0.06, 16, 10), hairM, head, [-0.03, 0.095, 0.06]); fr.scale.set(1.5, 0.45, 0.8); fr.rotation.z = 0.35;
    }
    if (st === 'coque') { mesh(sph(0.052, 18, 14), hairM, head, [0, 0.1, -0.1]); const fr = mesh(sph(0.06, 16, 10), hairM, head, [0, 0.1, 0.05]); fr.scale.set(1.5, 0.4, 1.0); }
    if (st === 'chanel') { const fr = mesh(sph(0.07, 16, 10), hairM, head, [0.02, 0.09, 0.065]); fr.scale.set(1.5, 0.45, 0.6); fr.rotation.z = -0.25; }
  }
  if (d.barba) { const b = mesh(new THREE.SphereGeometry(0.093, 24, 12, Math.PI * 0.08, Math.PI * 0.84, Math.PI * 0.6, Math.PI * 0.33), phys(d.barbaCor || d.cabelo, { roughness: 0.95 }), head, [0, -0.03, 0.012]); b.scale.set(0.98, 1.08, 1.02); }
  if (d.oculos) { const gm = phys(0x1a1a1a, { roughness: 0.3, clearcoat: 1 }), lens = new THREE.MeshPhysicalMaterial({ color: 0xffffff, transparent: true, opacity: 0.18, roughness: 0.05 });
    [-1, 1].forEach(s => { mesh(new THREE.TorusGeometry(0.02, 0.0028, 8, 24), gm, head, [s * 0.036, 0.008, 0.094], null, false); mesh(new THREE.CircleGeometry(0.02, 20), lens, head, [s * 0.036, 0.008, 0.094], null, false); mesh(cyl(0.0022, 0.0022, 0.09, 6), gm, head, [s * 0.085, 0.012, 0.05], [Math.PI / 2, 0, 0], false); });
    mesh(cyl(0.0022, 0.0022, 0.03, 6), gm, head, [0, 0.012, 0.096], [0, 0, Math.PI / 2], false); }
  if (d.bigode) mesh(new THREE.CapsuleGeometry(0.008, 0.045, 4, 8), hairM, head, [0, -0.048, 0.093], [0, 0, Math.PI / 2], false);

  root.traverse(o => { if (o.isMesh) { o.castShadow = true; o.userData.dirId = d.id; } });
  P.blinkT = 2 + Math.random() * 3; P.talk = 0;
  return P;
}

// ---------- poses ----------
const POSE = {
  // ombro [x,y,z], cotovelo x, punho x (por lado: 0 = esquerda, 1 = direita)
  rest: { sh: [[-0.5, 0, 0.14], [-0.5, 0, -0.14]], el: [-1.05, -1.05], wr: [0.15, 0.15] },
  type: { sh: [[-0.62, 0.1, 0.12], [-0.62, -0.1, -0.12]], el: [-1.12, -1.12], wr: [0.35, 0.35] },
  mouthR: { sh: [[-0.5, 0, 0.14], [-1.15, -0.25, -0.35]], el: [-1.05, -2.2], wr: [0.15, -0.2] },
  phoneR: { sh: [[-0.5, 0, 0.14], [-0.85, -0.2, -0.18]], el: [-1.05, -1.75], wr: [0.15, 0.0] },
  phoneEar: { sh: [[-0.5, 0, 0.14], [-0.55, -0.1, -0.85]], el: [-1.05, -2.45], wr: [0.15, -0.3] },
  read: { sh: [[-0.95, 0.15, 0.25], [-0.95, -0.15, -0.25]], el: [-1.4, -1.4], wr: [0.0, 0.0] },
  gesture: { sh: [[-0.5, 0, 0.14], [-0.75, -0.3, -0.45]], el: [-1.05, -1.55], wr: [0.15, -0.4] },
  stand: { sh: [[0.05, 0, 0.07], [0.05, 0, -0.07]], el: [-0.2, -0.2], wr: [0, 0] },
  armsCross: { sh: [[-0.35, 0.5, 0.25], [-0.35, -0.5, -0.25]], el: [-1.9, -1.9], wr: [0, 0] },
};
export function blendPose(P, a, b, k) {
  const A = POSE[a], B = POSE[b];
  for (let s = 0; s < 2; s++) {
    P.sh[s].rotation.set(lerp(A.sh[s][0], B.sh[s][0], k), lerp(A.sh[s][1], B.sh[s][1], k), lerp(A.sh[s][2], B.sh[s][2], k));
    P.el[s].rotation.x = lerp(A.el[s], B.el[s], k);
    P.wr[s].rotation.x = lerp(A.wr[s], B.wr[s], k);
  }
}
export function sitLegs(P) {
  P.pelvis.position.set(0, 0.56, -0.04);
  P.legs.forEach((l, i) => l.rotation.set(-Math.PI / 2 + 0.06, 0, (i ? -1 : 1) * 0.04));
  P.knees.forEach(k => k.rotation.set(Math.PI / 2 - 0.12, 0, 0));
  P.feet.forEach(f => f.rotation.set(0.06, 0, 0));
}
export function standLegs(P, phase, moving) {
  const sw = moving ? Math.sin(phase) * 0.48 : 0;
  P.pelvis.position.set(0, 0.95 + (moving ? Math.abs(Math.cos(phase)) * 0.022 : 0), 0);
  P.pelvis.rotation.set(0, moving ? Math.sin(phase) * 0.06 : 0, moving ? Math.sin(phase) * 0.02 : 0);
  P.legs[0].rotation.set(sw, 0, 0); P.legs[1].rotation.set(-sw, 0, 0);
  P.knees[0].rotation.set(Math.max(0, -Math.cos(phase)) * (moving ? 0.9 : 0) + (moving ? 0.1 : 0.02), 0, 0);
  P.knees[1].rotation.set(Math.max(0, Math.cos(phase)) * (moving ? 0.9 : 0) + (moving ? 0.1 : 0.02), 0, 0);
  P.feet.forEach((f, i) => f.rotation.set(moving ? (i ? 1 : -1) * Math.sin(phase) * 0.25 : 0, 0, 0));
}
// vida: respirar, piscar, falar
export function faceTick(P, dt, now) {
  P.torso.scale.set(1, 1 + Math.sin(now * 1.6 + P.d.idade) * 0.006, 1);
  P.blinkT -= dt;
  let k = 1; if (P.blinkT < 0) { const t = -P.blinkT; k = t < 0.07 ? 1 - t / 0.07 : t < 0.15 ? (t - 0.07) / 0.08 : 1; if (t > 0.15) P.blinkT = 2.5 + Math.random() * 4; }
  P.eyes.forEach(({ lid }) => { lid.rotation.x = lerp(1.35, P.d.olhos === 'puxados' ? -0.35 : -0.6, k); });
  P.lowerLip.position.y = -0.007 - (P.talk > 0 ? Math.abs(Math.sin(now * 13)) * 0.006 * P.talk : 0);
}
