import * as THREE from 'three';
import { M, mat, phys, mesh, box, rbox, cyl, sph, tex, lerp, clamp, smooth, bakeSkinned } from './util.js';

const pinTex = tex(256, 256, (g, w, h) => { g.fillStyle = '#fff'; g.fillRect(0, 0, w, h); g.fillStyle = 'rgba(0,0,0,.08)'; for (let x = 0; x < w; x += 24) g.fillRect(x, 0, 2, h); }, [5, 2]);
const fabricTex = tex(256, 256, (g, w, h) => { g.fillStyle = '#fff'; g.fillRect(0, 0, w, h); for (let i = 0; i < 9000; i++) { g.fillStyle = `rgba(0,0,0,${Math.random() * .06})`; g.fillRect(Math.random() * w, Math.random() * h, 1, 2); } }, [6, 6]);

// membro afunilado com articulação arredondada no topo
function limb(len, r0, r1, m, parent) {
  const g = new THREE.Group(); parent.add(g);
  mesh(cyl(r1, r0, len, 12), m, g, [0, -len / 2, 0]);
  mesh(new THREE.SphereGeometry(r0, 12, 8), m, g, [0, 0, 0]);
  return g;
}
function lathe(points, m, parent, pos, scaleZ = 1, scaleX = 1) {
  const geo = new THREE.LatheGeometry(points.map(([r, y]) => new THREE.Vector2(r, y)), 26);
  const o = mesh(geo, m, parent, pos); o.scale.set(scaleX, 1, scaleZ); return o;
}

// mão com dedos (palma pra baixo, dedos apontando pra -Y local do antebraço)
function hand(parent, skin, side) {
  const h = new THREE.Group(); parent.add(h);
  mesh(rbox(0.07, 0.13, 0.03, 0.013, 2), skin, h, [0, -0.06, 0]);
  const th = mesh(new THREE.CapsuleGeometry(0.0095, 0.032, 4, 8), skin, h, [side * 0.036, -0.045, 0.012]); th.rotation.set(0.3, 0, side * 0.7);
  [-0.024, -0.008, 0.008, 0.024].forEach((x, i) => { const f = mesh(new THREE.CapsuleGeometry(0.0072, 0.045 - Math.abs(i - 1.5) * 0.006, 2, 6), skin, h, [x, -0.14, 0.004], [0.18, 0, 0]); });
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
    limb(0.45, W ? 0.082 : 0.088, W ? 0.06 : 0.066, pants, hip);
    const knee = new THREE.Bone(); knee.position.y = -0.45; hip.add(knee);
    limb(0.44, W ? 0.06 : 0.066, 0.046, pants, knee);
    const ankle = new THREE.Bone(); ankle.position.y = -0.44; knee.add(ankle);
    mesh(cyl(0.042, 0.042, 0.05, 12), M.sock, ankle, [0, 0.01, 0]);
    const shoe = mesh(new THREE.CapsuleGeometry(0.046, 0.17, 6, 14), M.shoe, ankle, [0, -0.03, 0.07], [Math.PI / 2, 0, 0]); shoe.scale.set(W ? 0.85 : 1, 1, 0.62);
    mesh(rbox(W ? 0.075 : 0.088, 0.014, 0.25, 0.006), mat(0x16100c, { roughness: 0.7 }), ankle, [0, -0.058, 0.07], null, false);
    if (W) mesh(cyl(0.012, 0.008, 0.06, 8), M.shoe, ankle, [0, -0.03, -0.04]);
    P.legs.push(hip); P.knees.push(knee); P.feet.push(ankle);
  });
  // quadril
  const hipM = mesh(new THREE.SphereGeometry(0.17, 12, 8), pants, pelvis, [0, 0.02, -0.01]); hipM.scale.set(W ? 1.08 : 1.0, 0.62, 0.78);

  // tronco (paletó) por perfil de torno
  const torso = new THREE.Bone(); torso.position.y = 0.04; pelvis.add(torso); P.torso = torso;
  const prof = W ? [[0.16, 0], [0.15, 0.08], [0.135, 0.18], [0.155, 0.3], [0.17, 0.4], [0.165, 0.47], [0.13, 0.53], [0.06, 0.575]]
                 : [[0.165, 0], [0.165, 0.08], [0.16, 0.18], [0.178, 0.3], [0.196, 0.41], [0.198, 0.47], [0.158, 0.54], [0.065, 0.585]];
  lathe(prof, suit, torso, [0, 0, 0], 0.64, 1.0);
  const zf = (W ? 0.158 : 0.178) * 0.64; // frente do peito
  // camisa / blusa em V e gravata
  const vShape = new THREE.Shape(); vShape.moveTo(-0.055, 0.55); vShape.lineTo(0.055, 0.55); vShape.lineTo(0, W ? 0.33 : 0.26); vShape.closePath();
  const vMesh = mesh(new THREE.ShapeGeometry(vShape), W ? mat(0xebe5da, { roughness: 0.55 }) : shirtM, torso, [0, 0, zf + 0.012], [-0.12, 0, 0], false);
  if (d.gravata) {
    const tie = new THREE.Shape(); tie.moveTo(-0.014, 0.53); tie.lineTo(0.014, 0.53); tie.lineTo(0.022, 0.3); tie.lineTo(0, 0.27); tie.lineTo(-0.022, 0.3); tie.closePath();
    const loose = pd.slump * 0.03, tw = pd.slump * 0.14;
    mesh(new THREE.ShapeGeometry(tie), phys(d.gravata, { roughness: 0.35, sheen: 0.6 }), torso, [0, -loose, zf + 0.016], [-0.12, 0, tw], false);
    mesh(sph(0.018, 10, 8), phys(d.gravata, { roughness: 0.35 }), torso, [0, 0.535 - loose, zf + 0.0], null, false).scale.set(1.2, 0.9, 0.7);
  }
  if (d.colete) { const vest = new THREE.Shape(); vest.moveTo(-0.07, 0.42); vest.lineTo(0.07, 0.42); vest.lineTo(0.09, 0.12); vest.lineTo(0, 0.08); vest.lineTo(-0.09, 0.12); vest.closePath(); mesh(new THREE.ShapeGeometry(vest), mat(0x2a2a2e, { roughness: 0.6 }), torso, [0, 0, zf + 0.008], [-0.04, 0, 0], false); }
  // lapelas
  [-1, 1].forEach(s => {
    const lap = new THREE.Shape(); lap.moveTo(s * 0.055, 0.55); lap.lineTo(s * 0.1, 0.5); lap.lineTo(s * 0.075, 0.45); lap.lineTo(s * 0.03, 0.22); lap.lineTo(s * 0.0, W ? 0.33 : 0.26); lap.closePath();
    const lm = mesh(new THREE.ShapeGeometry(lap), suit, torso, [0, 0, zf + 0.02], [-0.12, 0, 0], false); lm.material = suit; lm.material.side = THREE.DoubleSide;
  });
  [0.2, 0.12].forEach(y => mesh(sph(0.009, 10, 8), M.black, torso, [0, y, (0.165) * 0.64 + 0.004], null, false));
  mesh(box(0.05, 0.022, 0.006), M.gold, torso, [0.09, 0.44, zf + 0.008], [0, 0.25, 0], false); // lenço de bolso
  const bc = BROCHE[d.broche];
  if (bc) { // broche do histórico de erro (lapela esquerda de quem olha = direita dele)
    mesh(cyl(0.019, 0.019, 0.006, 22), mat(bc[0], { roughness: 0.25, metalness: d.broche === 'imaculado' ? 0.2 : 1 }), torso, [-0.072, 0.47, zf + 0.026], [Math.PI / 2 - 0.12, 0, 0], false);
    mesh(new THREE.TorusGeometry(0.019, 0.003, 6, 24), mat(bc[1], { roughness: 0.2, metalness: 1 }), torso, [-0.072, 0.47, zf + 0.029], [-0.12, 0, 0], false);
    if (d.broche === 'imaculado') mesh(sph(0.006, 8, 6), mat(0xf1d595, { roughness: 0.2, metalness: 1 }), torso, [-0.072, 0.47, zf + 0.031], null, false);
  }
  // ombros
  [-1, 1].forEach(s => mesh(sph(0.062, 18, 12), suit, torso, [s * (W ? 0.16 : 0.182), 0.49, -0.005], null).scale.set(1.1, 0.62, 1.0));
  // pescoço e colarinho
  mesh(cyl(0.05, 0.056, 0.12, 22), skin, torso, [0, 0.62, 0.005]);
  mesh(sph(0.03, 12, 9), skin, torso, [0, 0.6, 0.04], null, false).scale.set(0.9, 1.4, 0.7); // pomo/garganta
  if (!W) { mesh(new THREE.TorusGeometry(0.056, 0.014, 10, 28, Math.PI * 1.4), shirtM, torso, [0, 0.585, 0.005], [Math.PI / 2, 0, Math.PI * 0.8], false);
    [-1, 1].forEach(s => { const cp = new THREE.Shape(); cp.moveTo(0, 0); cp.lineTo(s * 0.035, -0.012); cp.lineTo(s * 0.012, -0.05); cp.closePath(); mesh(new THREE.ShapeGeometry(cp), shirtM, torso, [s * 0.006, 0.585, zf + 0.03], [-0.35, 0, 0], false).material.side = THREE.DoubleSide; }); }
  else mesh(new THREE.TorusGeometry(0.05, 0.005, 8, 24, Math.PI), M.gold, torso, [0, 0.57, 0.03], [0.35, 0, Math.PI], false);

  // braços
  [-1, 1].forEach(s => {
    const sh = new THREE.Bone(); sh.position.set(s * (W ? 0.175 : 0.2), 0.49, -0.01); torso.add(sh);
    limb(0.29, W ? 0.048 : 0.054, W ? 0.04 : 0.045, suit, sh);
    const el = new THREE.Bone(); el.position.y = -0.29; sh.add(el);
    limb(0.27, W ? 0.04 : 0.045, W ? 0.034 : 0.038, suit, el);
    mesh(cyl(0.036, 0.036, 0.03, 14), shirtM, el, [0, -0.265, 0], null, false);
    if (s === 1) mesh(cyl(0.03, 0.03, 0.016, 18), M.gold, el, [0, -0.25, 0.012], [Math.PI / 2, 0, 0], false);
    const wr = new THREE.Bone(); wr.position.y = -0.28; el.add(wr);
    hand(wr, skin, -s);
    P.sh.push(sh); P.el.push(el); P.wr.push(wr);
  });

  // cabeça
  const head = new THREE.Bone(); head.position.set(0, 0.79, 0.012); torso.add(head); P.head = head;
  // maçãs do rosto e têmporas: tiram o aspecto de bola
  [-1, 1].forEach(s => mesh(new THREE.SphereGeometry(0.03, 16, 12), skin, head, [s * 0.05, -0.02, 0.06], null, false).scale.set(1.05, 0.7, 0.55));
  const cran = mesh(new THREE.SphereGeometry(0.1, 22, 16), skin, head, [0, 0.03, -0.005]); cran.scale.set(W ? 0.88 : 0.92, 1.02, 1.03);
  const jaw = mesh(new THREE.SphereGeometry(0.088, 22, 16), skin, head, [0, -0.035, 0.012]); jaw.scale.set(W ? 0.84 : 0.92, 1.06, 0.98);
  mesh(sph(0.036, 16, 12), skin, head, [0, -0.1, 0.055]).scale.set(W ? 1.0 : 1.25, 0.8, 0.9); // queixo
  const nose = mesh(new THREE.ConeGeometry(0.018, 0.05, 12), skin, head, [0, -0.012, 0.098], [Math.PI / 2 - 0.35, 0, 0], false);
  mesh(sph(0.016, 12, 10), skin, head, [0, -0.034, 0.1], null, false).scale.set(1.4, 0.8, 0.9);
  // olhos (com pálpebra que pisca)
  const eyes = new THREE.Group(); head.add(eyes); P.eyes = [];
  [-1, 1].forEach(s => {
    const e = new THREE.Bone(); e.position.set(s * 0.035, 0.008, 0.08); eyes.add(e);
    mesh(new THREE.SphereGeometry(0.0128, 8, 6), M.sclera, e, null, null, false);
    const iris = mesh(new THREE.SphereGeometry(0.0078, 6, 5), phys(d.olhosCor || 0x2a1a10, { roughness: 0.1, clearcoat: 1 }), e, [0, 0, 0.0105], null, false); iris.scale.set(1, 1, 0.5); iris.position.z = 0.0085;
    const lid = new THREE.Bone(); e.add(lid); lid.rotation.x = -0.6; mesh(new THREE.SphereGeometry(0.0139, 8, 4, 0, Math.PI * 2, 0, Math.PI * 0.5), skin, lid, null, null, false);
    if (d.olhos === 'puxados') { e.scale.set(1.15, 0.72, 1); e.rotation.z = s * -0.12; }
    P.eyes.push({ e, lid });
  });
  if (pd.slump > 0.3) [-1, 1].forEach(s => mesh(sph(0.014, 10, 8), mat(new THREE.Color(skinHex).multiplyScalar(0.72).getHex(), { roughness: 0.6 }), head, [s * 0.035, -0.006, 0.084], null, false).scale.set(1.3, 0.45, 0.4));
  // sobrancelhas
  const browM = phys(d.estilo === 'grisalho' && d.barbaCor ? d.barbaCor : d.cabelo, { roughness: 0.9 });
  P.brows = [-1, 1].map(s => mesh(rbox(0.038, 0.01, 0.012, 0.004), browM, head, [s * 0.037, 0.035, 0.088], [0.1, 0, s * (W ? -0.14 : 0.06)], false));
  // boca
  const lipC = W ? 0x9a2a36 : new THREE.Color(d.pele).multiplyScalar(0.72).getHex();
  P.mouth = new THREE.Bone(); P.mouth.position.set(0, -0.062, 0.085); head.add(P.mouth);
  mesh(new THREE.CapsuleGeometry(0.0065, 0.03, 4, 8), phys(lipC, { roughness: 0.35, clearcoat: W ? 0.6 : 0 }), P.mouth, [0, 0.004, 0], [0, 0, Math.PI / 2], false);
  P.lowerLip = new THREE.Bone(); P.lowerLip.position.set(0, -0.007, -0.001); P.mouth.add(P.lowerLip); mesh(new THREE.CapsuleGeometry(0.0072, 0.026, 4, 8), phys(lipC, { roughness: 0.35 }), P.lowerLip, null, [0, 0, Math.PI / 2], false);
  // orelhas
  [-1, 1].forEach(s => { mesh(new THREE.SphereGeometry(0.026, 16, 12), skin, head, [s * 0.088, 0.0, -0.005]).scale.set(0.35, 1, 0.65); mesh(sph(0.012, 10, 8), mat(new THREE.Color(skinHex).multiplyScalar(0.8).getHex(), { roughness: 0.6 }), head, [s * 0.093, 0.0, 0.0], null, false).scale.set(0.3, 1, 0.6); });
  if (W) [-1, 1].forEach(s => mesh(sph(0.009, 10, 8), M.gold, head, [s * 0.09, -0.03, 0.0], null, false));

  // cabelo
  const st = d.estilo, F = 0.95;
  const capR = 0.106;
  const cap = (th, rx = -0.3) => { const c = mesh(new THREE.SphereGeometry(capR, 20, 9, 0, Math.PI * 2, 0, Math.PI * th), hairM, head, [0, 0.036, -0.008]); c.scale.set(W ? 0.92 : 0.96, 1.06, 1.06); c.rotation.x = rx; return c; };
  const band = (t0, t1, f = F, r = capR) => { const b = mesh(new THREE.SphereGeometry(r, 20, 7, Math.PI / 2 + f, Math.PI * 2 - 2 * f, Math.PI * t0, Math.PI * (t1 - t0)), hairM, head, [0, 0.03, -0.008]); b.scale.set(W ? 0.92 : 0.97, 1.06, 1.06); return b; };
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
