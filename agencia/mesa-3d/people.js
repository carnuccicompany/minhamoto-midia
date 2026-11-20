import * as THREE from 'three';
import { M, mat, phys, mesh, box, rbox, cyl, sph, tex, lerp, clamp, smooth, bakeSkinned } from './util.js';
import { makeFace, headGeo, hairGeo, beardGeo, noseGeo, torsoGeo, onChest, frontZ, zAt } from './head.js';

const pinTex = tex(256, 256, (g, w, h) => { g.fillStyle = '#fff'; g.fillRect(0, 0, w, h); g.fillStyle = 'rgba(0,0,0,.08)'; for (let x = 0; x < w; x += 24) g.fillRect(x, 0, 2, h); }, [5, 2]);
const fabricTex = tex(256, 256, (g, w, h) => { g.fillStyle = '#fff'; g.fillRect(0, 0, w, h); for (let i = 0; i < 9000; i++) { g.fillStyle = `rgba(0,0,0,${Math.random() * .06})`; g.fillRect(Math.random() * w, Math.random() * h, 1, 2); } }, [6, 6]);

// membro afunilado com articulação arredondada no topo
function limb(len, r0, r1, m, parent, bulge = 0.08, flat = 1) {
  // tubo de tecido com tampa redonda em cima e embaixo, afinando e com leve volume no meio (sem cara de cano)
  const g = new THREE.Group(); parent.add(g);
  const pts = [], N = 8;
  for (let i = 0; i <= 3; i++) { const a = Math.PI / 2 * (i / 3); pts.push(new THREE.Vector2(Math.sin(a) * r0, r0 * 0.3 * Math.cos(a))); }
  for (let i = 1; i < N; i++) { const t = i / N, r = r0 + (r1 - r0) * t + Math.sin(t * Math.PI) * bulge * r0 * (1 - t * 0.5); pts.push(new THREE.Vector2(r, -len * t)); }
  for (let i = 0; i <= 3; i++) { const a = Math.PI / 2 * (i / 3); pts.push(new THREE.Vector2(Math.cos(a) * r1, -len - r1 * 0.3 * Math.sin(a))); }
  const geo = new THREE.LatheGeometry(pts, 16); const o = mesh(geo, m, g, [0, 0, 0]); o.scale.z = flat;
  return g;
}
function lathe(points, m, parent, pos, scaleZ = 1, scaleX = 1) {
  const geo = new THREE.LatheGeometry(points.map(([r, y]) => new THREE.Vector2(r, y)), 26);
  const o = mesh(geo, m, parent, pos); o.scale.set(scaleX, 1, scaleZ); return o;
}

// mão com dedos (palma pra baixo, dedos apontando pra -Y local do antebraço)
function hand(parent, skin, side) {
  const h = new THREE.Group(); parent.add(h);
  // palma esculpida (mais larga nos nós dos dedos, fina no punho)
  const pg = new THREE.SphereGeometry(1, 18, 14), pp = pg.attributes.position;
  for (let i = 0; i < pp.count; i++) { const x = pp.getX(i), y = pp.getY(i), z = pp.getZ(i), t = (1 - y) / 2; pp.setXYZ(i, x * (0.03 + 0.008 * t), y * 0.05, z * (0.014 + 0.003 * (1 - Math.abs(x))) + (z > 0 ? 0.002 * t : 0)); }
  pg.computeVertexNormals(); mesh(pg, skin, h, [0, -0.05, 0], null, false);
  // dedos: duas falanges, levemente dobrados
  const L = [0.044, 0.05, 0.047, 0.038];
  [-0.021, -0.007, 0.007, 0.021].forEach((x, i) => {
    const r = 0.0074 - Math.abs(i - 1.5) * 0.0004, l1 = L[i] * 0.55, l2 = L[i] * 0.45;
    const f = new THREE.Group(); f.position.set(x * 1.05, -0.096, 0.002); f.rotation.set(0.22, 0, (i - 1.5) * -0.04); h.add(f);
    mesh(new THREE.CapsuleGeometry(r, l1, 3, 8), skin, f, [0, -l1 / 2, 0], null, false);
    const f2 = new THREE.Group(); f2.position.y = -l1; f2.rotation.x = 0.32; f.add(f2);
    mesh(new THREE.CapsuleGeometry(r * 0.92, l2, 3, 8), skin, f2, [0, -l2 / 2, 0], null, false);
    mesh(new THREE.SphereGeometry(r * 0.85, 8, 6), skin, f2, [0, -l2 - r * 0.2, -r * 0.35], null, false).scale.set(1, 0.5, 0.25); // unha
  });
  // polegar
  const th = new THREE.Group(); th.position.set(side * 0.03, -0.028, 0.008); th.rotation.set(0.35, 0, side * 0.75); h.add(th);
  mesh(new THREE.CapsuleGeometry(0.0095, 0.022, 3, 8), skin, th, [0, -0.012, 0], null, false);
  const th2 = new THREE.Group(); th2.position.y = -0.026; th2.rotation.x = 0.3; th.add(th2);
  mesh(new THREE.CapsuleGeometry(0.0085, 0.018, 3, 8), skin, th2, [0, -0.01, 0], null, false);
  return h;
}

// padrão da casa muda o terno e a cara: Elite (rico e descansado) → Crise (microfibra brilhosa, cansado)
const PAD = { elite: { sat: 1.1, val: 0.86, rough: 0.78, slump: 0 }, ouro: { sat: 1, val: 1, rough: 0.7, slump: 0 }, prata: { sat: 0.82, val: 1.06, rough: 0.6, slump: 0.45 }, crise: { sat: 0.55, val: 1.16, rough: 0.34, slump: 1 } };
const BROCHE = { imaculado: [0x0a0a0a, 0xf1d595], ouro: [0xd8ac48, 0xf6e2a0], prata: [0xc8ccd2, 0xffffff], bronze: [0xa8653a, 0xe0a070] };
function tone(hex, p) { const c = new THREE.Color(hex), hsl = {}; c.getHSL(hsl); c.setHSL(hsl.h, Math.min(1, hsl.s * p.sat), Math.min(0.95, hsl.l * p.val)); return c.getHex(); }
export function buildPerson(d) {
  const W = !!d.mulher;
  const pd = PAD[d.padrao] || PAD.ouro;
  const suit = mat(tone(d.terno, pd), { roughness: pd.rough, map: d.risca ? pinTex : null }); suit.userData.k = 2;
  const pants = suit;
  const skinHex = pd.slump > 0.9 ? new THREE.Color(d.pele).lerp(new THREE.Color(0xb8b0a4), 0.18).getHex() : d.pele;
  const skin = mat(skinHex, { roughness: 0.48 }); skin.userData.k = 1;
  const hairM = mat(d.cabelo, { roughness: 0.42 }); hairM.userData.k = 3;
  const shirtM = d.camisa ? mat(d.camisa, { roughness: 0.55 }) : M.shirt;
  const root = new THREE.Group();
  const pelvis = new THREE.Bone(); root.add(pelvis);
  const P = { root, pelvis, legs: [], knees: [], feet: [], sh: [], el: [], wr: [], d, slump: pd.slump };

  // pernas
  [-1, 1].forEach(s => {
    const hip = new THREE.Bone(); hip.position.set(s * (W ? 0.088 : 0.098), 0, 0); pelvis.add(hip);
    limb(0.45, W ? 0.088 : 0.096, W ? 0.064 : 0.07, pants, hip, 0.06);
    const knee = new THREE.Bone(); knee.position.y = -0.45; knee.userData.joint = true; hip.add(knee);
    limb(0.44, W ? 0.064 : 0.07, W ? 0.05 : 0.06, pants, knee, 0.02);
    const ankle = new THREE.Bone(); ankle.position.y = -0.44; ankle.userData.joint = true; knee.add(ankle);
    mesh(cyl(0.042, 0.042, 0.05, 12), M.sock, ankle, [0, 0.01, 0]);
    const shoe = mesh(new THREE.CapsuleGeometry(0.046, 0.17, 6, 14), M.shoe, ankle, [0, -0.03, 0.07], [Math.PI / 2, 0, 0]); shoe.scale.set(W ? 0.85 : 1, 1, 0.62);
    mesh(rbox(W ? 0.075 : 0.088, 0.014, 0.25, 0.006), mat(0x16100c, { roughness: 0.7 }), ankle, [0, -0.058, 0.07], null, false);
    if (W) mesh(cyl(0.012, 0.008, 0.06, 8), M.shoe, ankle, [0, -0.03, -0.04]);
    P.legs.push(hip); P.knees.push(knee); P.feet.push(ankle);
  });
  // quadril
  const hipM = mesh(new THREE.SphereGeometry(0.17, 12, 8), pants, pelvis, [0, 0.02, -0.01]); hipM.scale.set(W ? 1.08 : 1.0, 0.62, 0.78);

  // tronco: paletó com ombro de alfaiataria (superelipse), peças coladas na frente
  const torso = new THREE.Bone(); torso.position.y = 0.04; pelvis.add(torso); P.torso = torso;
  mesh(torsoGeo(W), suit, torso, [0, 0, 0]);
  const vTop = W ? 0.56 : 0.572, vBot = W ? 0.34 : 0.275;
  const vS = new THREE.Shape(); vS.moveTo(-0.062, vTop); vS.lineTo(0.062, vTop); vS.lineTo(0, vBot); vS.closePath();
  mesh(onChest(vS, W, () => 0.002), W ? mat(0xefe9df, { roughness: 0.55 }) : shirtM, torso, null, null, false);
  if (d.colete && !W) { const vest = new THREE.Shape(); vest.moveTo(-0.05, vTop - 0.04); vest.lineTo(0.05, vTop - 0.04); vest.lineTo(0.075, 0.13); vest.lineTo(0, 0.1); vest.lineTo(-0.075, 0.13); vest.closePath(); mesh(onChest(vest, W, () => 0.0032), mat(new THREE.Color(tone(d.terno, pd)).multiplyScalar(0.8).getHex(), { roughness: 0.62 }), torso, null, null, false); }
  if (d.gravata && !W) {
    const loose = pd.slump * 0.025, tw = pd.slump * 0.012;
    const tie = new THREE.Shape(); tie.moveTo(-0.012 + tw, vTop - 0.016 - loose); tie.lineTo(0.012 + tw, vTop - 0.016 - loose); tie.lineTo(0.024, 0.31); tie.lineTo(0, 0.282); tie.lineTo(-0.024, 0.31); tie.closePath();
    const tieM = phys(d.gravata, { roughness: 0.38 }); tieM.userData.k = 2;
    mesh(onChest(tie, W, (x, y) => 0.0052 + 0.004 * Math.max(0, (y - 0.3) / 0.27)), tieM, torso, null, null, false);
    const kn = mesh(new THREE.SphereGeometry(0.017, 14, 10), tieM, torso, [tw, vTop - 0.008 - loose, frontZ(W, 0, vTop - 0.008) + 0.006], null, false); kn.scale.set(1.1, 0.95, 0.7);
  }
  // lapelas (as duas, coladas no peito)
  [-1, 1].forEach(s => {
    const L = new THREE.Shape();
    L.moveTo(s * 0.062, vTop); L.lineTo(s * 0.088, vTop + 0.004); L.lineTo(s * 0.12, 0.515); L.lineTo(s * 0.097, 0.498); L.lineTo(s * 0.036, vBot + 0.03); L.lineTo(0, vBot - 0.012); L.closePath();
    mesh(onChest(L, W, (x, y) => 0.0072 + 0.003 * Math.min(1, Math.abs(x) / 0.1)), suit, torso, null, null, false);
  });
  // bolsos com aba e botões
  [-1, 1].forEach(s => { const fl = new THREE.Shape(); fl.moveTo(s * 0.06, 0.13); fl.lineTo(s * 0.135, 0.13); fl.lineTo(s * 0.137, 0.108); fl.lineTo(s * 0.062, 0.106); fl.closePath(); mesh(onChest(fl, W, () => 0.004, 2), suit, torso, null, null, false); });
  [0.21, 0.13].forEach(y => mesh(new THREE.SphereGeometry(0.0085, 10, 8), M.black, torso, [0, y, frontZ(W, 0, y) + 0.005], null, false).scale.set(1, 1, 0.5));
  const psq = mesh(box(0.042, 0.018, 0.006), d.gravata && !W ? mat(new THREE.Color(d.gravata).lerp(new THREE.Color(0xffffff), 0.35).getHex(), { roughness: 0.5 }) : M.gold, torso, [0.11, 0.445, frontZ(W, 0.11, 0.445) + 0.008], [0, 0.35, 0.08], false);
  const bc = BROCHE[d.broche];
  if (bc) { const bz = frontZ(W, -0.075, 0.47) + 0.0135;
    mesh(cyl(0.016, 0.016, 0.005, 22), mat(bc[0], { roughness: 0.25, metalness: d.broche === 'imaculado' ? 0.2 : 1 }), torso, [-0.075, 0.47, bz], [Math.PI / 2 - 0.2, 0, 0], false);
    mesh(new THREE.TorusGeometry(0.016, 0.0028, 6, 24), mat(bc[1], { roughness: 0.2, metalness: 1 }), torso, [-0.075, 0.47, bz + 0.002], [-0.2, 0, 0], false);
    if (d.broche === 'imaculado') mesh(sph(0.005, 8, 6), mat(0xf1d595, { roughness: 0.2, metalness: 1 }), torso, [-0.075, 0.47, bz + 0.004], null, false);
  }
  // cabeça do ombro (manga)
  
  // gola do paletó atrás do pescoço
  mesh(new THREE.TorusGeometry(W ? 0.062 : 0.068, 0.016, 8, 24, Math.PI), suit, torso, [0, 0.592, 0.0], [-Math.PI / 2 - 0.25, 0, 0], false);
  // pescoço e colarinho
  mesh(cyl(W ? 0.046 : 0.054, W ? 0.05 : 0.058, 0.1, 22), skin, torso, [0, 0.625, 0.004]);
  if (!W) { mesh(new THREE.CylinderGeometry(0.06, 0.064, 0.042, 28, 1, true, Math.PI * 0.16, Math.PI * 1.68), shirtM, torso, [0, 0.6, 0.004], [-0.12, 0, 0], false);
    [-1, 1].forEach(s => { const cp = new THREE.Shape(); cp.moveTo(s * 0.004, 0.6); cp.lineTo(s * 0.044, 0.585); cp.lineTo(s * 0.018, 0.545); cp.closePath(); mesh(onChest(cp, W, () => 0.0105, 2), shirtM, torso, null, null, false); }); }
  else mesh(new THREE.TorusGeometry(0.046, 0.004, 8, 24, Math.PI), M.gold, torso, [0, 0.585, 0.02], [0.45, 0, Math.PI], false);

  // braços
  [-1, 1].forEach(s => {
    const sh = new THREE.Bone(); sh.position.set(s * (W ? 0.165 : 0.188), 0.455, -0.008); torso.add(sh);
    limb(0.29, W ? 0.05 : 0.057, W ? 0.042 : 0.047, suit, sh, 0.1);
    const el = new THREE.Bone(); el.position.y = -0.29; el.userData.joint = true; sh.add(el);
    limb(0.27, W ? 0.043 : 0.048, W ? 0.037 : 0.042, suit, el, 0.05);
    mesh(cyl(0.036, 0.036, 0.03, 14), shirtM, el, [0, -0.265, 0], null, false);
    if (s === 1) mesh(cyl(0.03, 0.03, 0.016, 18), M.gold, el, [0, -0.25, 0.012], [Math.PI / 2, 0, 0], false);
    const wr = new THREE.Bone(); wr.position.y = -0.28; wr.userData.joint = true; el.add(wr);
    hand(wr, skin, -s);
    P.sh.push(sh); P.el.push(el); P.wr.push(wr);
  });

  // cabeça: uma esfera esculpida (mandíbula, maçãs, olhos fundos, arco da sobrancelha)
  const head = new THREE.Bone(); head.position.set(0, W ? 0.712 : 0.72, 0.016); torso.add(head); P.head = head;
  const F = makeFace(d);
  mesh(headGeo(F), skin, head, [0, 0, 0]);
  const Z = (x, y) => zAt(x, y, F);
  const darker = (hex, k) => new THREE.Color(hex).multiplyScalar(k).getHex();
  // nariz: ponte, ponta e asas
  mesh(noseGeo(F), skin, head, [0, 0, 0], null, false);
  // olhos encaixados, pálpebra que pisca e linha de cílios
  const eyes = new THREE.Group(); head.add(eyes); P.eyes = [];
  const lashM = mat(darker(d.cabelo, 0.55), { roughness: 0.8 }); lashM.userData.k = 3;
  const scl = mat(0xe9e3d9, { roughness: 0.32 });
  [-1, 1].forEach(s => {
    const ex = s * (W ? 0.029 : 0.031), ey = 0.011;
    const e = new THREE.Bone(); e.position.set(ex, ey, Z(ex, ey) - 0.0045); eyes.add(e);
    mesh(new THREE.SphereGeometry(0.0122, 14, 10), scl, e, null, null, false);
    const iris = mesh(new THREE.SphereGeometry(0.0072, 12, 8), phys(d.olhosCor || 0x2a1a10, { roughness: 0.12, clearcoat: 1 }), e, [0, 0, 0.0092], null, false); iris.scale.set(1, 1, 0.45);
    mesh(new THREE.SphereGeometry(0.0034, 8, 6), mat(0x050505, { roughness: 0.1 }), e, [0, 0, 0.0118], null, false).scale.set(1, 1, 0.3);
    const lid = new THREE.Bone(); e.add(lid); lid.rotation.x = -0.6;
    mesh(new THREE.SphereGeometry(0.0127, 14, 6, 0, Math.PI * 2, 0, Math.PI * 0.5), mat(darker(skinHex, 0.9), { roughness: 0.5 }), lid, null, null, false);
    mesh(new THREE.TorusGeometry(0.0127, W ? 0.0017 : 0.0013, 4, 16, Math.PI), lashM, lid, [0, 0, 0], [Math.PI / 2, 0, 0], false);
    if (d.olhos === 'puxados') { e.scale.set(1.12, 0.78, 1); e.rotation.z = s * -0.1; }
    P.eyes.push({ e, lid });
  });
  if (pd.slump > 0.3) [-1, 1].forEach(s => mesh(sph(0.013, 10, 8), mat(darker(skinHex, 0.78), { roughness: 0.6 }), head, [s * 0.031, -0.008, Z(s * 0.031, -0.008) - 0.004], null, false).scale.set(1.4, 0.5, 0.45));
  // sobrancelhas afinadas
  const browM = phys(d.estilo === 'grisalho' && d.barbaCor ? d.barbaCor : darker(d.cabelo, 0.9), { roughness: 0.9 }); browM.userData.k = 3;
  P.brows = [-1, 1].map(s => {
    const g = new THREE.Group(); head.add(g);
    const bx = s * 0.033, by = 0.039; g.position.set(bx, by, Z(bx, by) + 0.0036); g.rotation.set(-0.15, s * 0.3, s * (W ? -0.12 : 0.04));
    const e1 = mesh(new THREE.SphereGeometry(1, 16, 8), browM, g, [-s * 0.004, -0.0006, 0], null, false); e1.scale.set(0.0125, W ? 0.0026 : 0.0034, 0.0035);
    const e2 = mesh(new THREE.SphereGeometry(1, 16, 8), browM, g, [s * 0.0085, 0.0003, -0.0012], [0, 0, -s * (W ? 0.3 : 0.2)], false); e2.scale.set(0.009, W ? 0.0021 : 0.0028, 0.003);
    return g;
  });
  // boca
  const lipC = W ? 0x9a3a40 : new THREE.Color(d.pele).lerp(new THREE.Color(0x9a4c44), 0.32).multiplyScalar(0.92).getHex();
  P.mouth = new THREE.Bone(); P.mouth.position.set(0, -0.062, Z(0, -0.062) + 0.001); head.add(P.mouth);
  const lipM = phys(lipC, { roughness: 0.38, clearcoat: W ? 0.6 : 0 }); lipM.userData.k = 1;
  mesh(new THREE.SphereGeometry(1, 18, 10), lipM, P.mouth, [0, 0.0032, -0.001], null, false).scale.set(W ? 0.0155 : 0.017, 0.0036, 0.0055);
  mesh(new THREE.CapsuleGeometry(0.0011, 0.026, 3, 6), mat(darker(lipC, 0.45), { roughness: 0.6 }), P.mouth, [0, -0.0005, 0.0025], [0, 0, Math.PI / 2], false);
  P.lowerLip = new THREE.Bone(); P.lowerLip.position.set(0, -0.0065, -0.001); P.mouth.add(P.lowerLip);
  mesh(new THREE.SphereGeometry(1, 18, 10), lipM, P.lowerLip, [0, 0, -0.0012], null, false).scale.set(W ? 0.0135 : 0.0145, 0.0047, 0.006);
  // orelhas
  [-1, 1].forEach(s => { const ear = mesh(new THREE.SphereGeometry(0.025, 16, 12), skin, head, [s * 0.071, -0.006, -0.01], [0, s * 0.3, 0]); ear.scale.set(0.32, 1, 0.62);
    mesh(new THREE.SphereGeometry(0.012, 10, 8), mat(darker(skinHex, 0.8), { roughness: 0.6 }), head, [s * 0.0755, -0.006, -0.006], null, false).scale.set(0.3, 1, 0.6); });
  if (W) [-1, 1].forEach(s => mesh(sph(0.0075, 10, 8), M.gold, head, [s * 0.073, -0.036, -0.004], null, false));

  // cabelo: casca que segue a cabeça
  const st = d.estilo, seed = (d.idade || 3) * 1.37;
  mesh(hairGeo(st, F, seed), st === 'raspado' ? mat(new THREE.Color(d.cabelo).lerp(new THREE.Color(skinHex), 0.45).getHex(), { roughness: 0.9 }) : hairM, head, [0, 0, 0]);
  if (st === 'longo') {
    const back = mesh(new THREE.CapsuleGeometry(0.075, 0.2, 6, 16), hairM, head, [0, -0.16, -0.058]); back.scale.set(1.25, 1, 0.5);
    [-1, 1].forEach(s => { const lk = mesh(new THREE.CapsuleGeometry(0.022, 0.18, 4, 10), hairM, head, [s * 0.078, -0.13, 0.012]); lk.rotation.z = s * 0.06; });
  }
  if (st === 'coque') mesh(new THREE.SphereGeometry(0.046, 18, 14), hairM, head, [0, 0.075, -0.098]);
  if (d.barba) mesh(beardGeo(F, true, seed), phys(d.barbaCor || d.cabelo, { roughness: 0.95 }), head, [0, 0, 0]).material.userData.k = 3;
  if (d.oculos) { const gm = phys(0x1a1a1a, { roughness: 0.3, clearcoat: 1 }), lz = Z(0.031, 0.011) + 0.012;
    [-1, 1].forEach(s => { mesh(new THREE.TorusGeometry(0.019, 0.0024, 8, 24), gm, head, [s * 0.031, 0.011, lz], null, false); mesh(cyl(0.0019, 0.0019, 0.085, 6), gm, head, [s * 0.069, 0.014, lz - 0.042], [Math.PI / 2, 0, 0], false); });
    mesh(cyl(0.0019, 0.0019, 0.024, 6), gm, head, [0, 0.014, lz + 0.001], [0, 0, Math.PI / 2], false); }
  if (d.bigode) { const bg = mesh(new THREE.SphereGeometry(1, 18, 10), hairM, head, [0, -0.0465, Z(0, -0.0465) + 0.002], [0, 0, 0], false); bg.scale.set(0.017, 0.0032, 0.0042); }

  root.traverse(o => { if (o.isMesh) { o.castShadow = false; o.userData.dirId = d.id; } });
  P.skin = bakeSkinned(root);
  const hitM = new THREE.MeshBasicMaterial({ visible: false });
  P.hit = new THREE.Mesh(new THREE.BoxGeometry(0.7, 1.5, 0.8), hitM); P.hit.position.set(0, 0.75, 0); P.hit.userData.dirId = d.id; P.hit.userData.hit = true; root.add(P.hit);
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
  P.eyes.forEach(({ lid }) => { lid.rotation.x = lerp(1.35, (P.d.olhos === 'puxados' ? -0.35 : -0.6) + (P.slump || 0) * 0.45, k); });
  P.lowerLip.position.y = -0.007 - (P.talk > 0 ? Math.abs(Math.sin(now * 13)) * 0.006 * P.talk : 0);
}
