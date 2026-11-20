import * as THREE from 'three';
import { mergeGeometries, mergeVertices } from 'three/examples/jsm/utils/BufferGeometryUtils.js';
import { lerp, clamp, smooth, blob } from './util.js';

// Fartuzzi, a pantera negra. Corpo inteiro numa malha só com esqueleto (pele contínua, sem emendas de bolinhas),
// pelo aveludado com rosetas quase invisíveis (como pantera de verdade no sol) e olho verde.
// Anda solta pelo tapete de veludo: caminha, para, olha em volta, senta, muda de rumo. Nunca sai do tapete.

const V = (x, y, z) => new THREE.Vector3(x, y, z);

function ringFrame(T) {
  const up = Math.abs(T.y) > 0.92 ? V(0, 0, 1) : V(0, 1, 0);
  const side = new THREE.Vector3().crossVectors(T, up).normalize();
  const upv = new THREE.Vector3().crossVectors(side, T).normalize();
  return { side, upv };
}
// tubo de seção elíptica ao longo de uma curva; rad(t, a) -> [meia-largura, meia-altura, deslocY]; wts(t) -> [[osso, peso], ...]
function tube(pts, rad, wts, segL = 28, segR = 20, capA = true, capB = true) {
  const curve = new THREE.CatmullRomCurve3(pts, false, 'centripetal');
  const pos = [], nrm = [], uv = [], si = [], sw = [], idx = [];
  const push = (p, n, u, v, w) => { pos.push(p.x, p.y, p.z); nrm.push(n.x, n.y, n.z); uv.push(u, v); const ww = w.slice(0, 4); while (ww.length < 4) ww.push([0, 0]); const tot = ww.reduce((s, x) => s + x[1], 0) || 1; ww.forEach(([b, x]) => { si.push(b); sw.push(x / tot); }); };
  for (let i = 0; i <= segL; i++) {
    const t = i / segL, p = curve.getPointAt(t), T = curve.getTangentAt(t).normalize(), { side, upv } = ringFrame(T), w = wts(t);
    for (let j = 0; j <= segR; j++) {
      const a = j / segR * Math.PI * 2, [rw, rh, dy] = rad(t, a);
      const c = Math.cos(a), s = Math.sin(a);
      const q = p.clone().addScaledVector(side, c * rw).addScaledVector(upv, s * rh + (dy || 0));
      const n = side.clone().multiplyScalar(c / rw).addScaledVector(upv, s / rh).normalize();
      push(q, n, j / segR, t * 4, w);
    }
  }
  const R = segR + 1;
  for (let i = 0; i < segL; i++) for (let j = 0; j < segR; j++) { const a = i * R + j, b = a + R; idx.push(a, b, a + 1, b, b + 1, a + 1); }
  const cap = (t, flip) => {
    const p = curve.getPointAt(t), T = curve.getTangentAt(t).normalize(); const [rw, rh, dy] = rad(t, 0);
    const { upv } = ringFrame(T);
    const c = pos.length / 3; push(p.clone().addScaledVector(T, (flip ? -1 : 1) * Math.min(rw, rh) * 0.6).addScaledVector(upv, dy || 0), T.clone().multiplyScalar(flip ? -1 : 1), 0.5, t * 4, wts(t));
    const base = (t === 0 ? 0 : segL) * R;
    for (let j = 0; j < segR; j++) flip ? idx.push(c, base + j + 1, base + j) : idx.push(c, base + j, base + j + 1);
  };
  if (capA) cap(0, true); if (capB) cap(1, false);
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute('normal', new THREE.Float32BufferAttribute(nrm, 3));
  g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2)); g.setAttribute('skinIndex', new THREE.Uint16BufferAttribute(si, 4)); g.setAttribute('skinWeight', new THREE.Float32BufferAttribute(sw, 4));
  g.setIndex(idx); return g;
}
// esfera esculpida por uma função de deformação, presa a um osso
function blobGeo(center, r, deform, bone, wS = 28, hS = 20) {
  let g = new THREE.SphereGeometry(1, wS, hS); g.deleteAttribute('uv'); g.deleteAttribute('normal');
  g = mergeVertices(g);
  const p = g.attributes.position, v = new THREE.Vector3();
  for (let i = 0; i < p.count; i++) { v.fromBufferAttribute(p, i); const o = deform(v.clone()); p.setXYZ(i, center.x + o.x * r, center.y + o.y * r, center.z + o.z * r); }
  g.computeVertexNormals();
  const n = p.count, si = new Uint16Array(n * 4), sw = new Float32Array(n * 4), uv = new Float32Array(n * 2);
  for (let i = 0; i < n; i++) { si[i * 4] = bone; sw[i * 4] = 1; uv[i * 2] = p.getX(i) * 3; uv[i * 2 + 1] = p.getY(i) * 3; }
  g.setAttribute('skinIndex', new THREE.Uint16BufferAttribute(si, 4)); g.setAttribute('skinWeight', new THREE.Float32BufferAttribute(sw, 4)); g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2));
  return g;
}
const band = (t, a, b, w = 0.08) => smooth(clamp((t - a) / w + 0.5, 0, 1)) * (1 - smooth(clamp((t - b) / w + 0.5, 0, 1)));
const blend2 = (t, at, A, B, w = 0.12) => { const k = smooth(clamp((t - at) / w + 0.5, 0, 1)); return [[A, 1 - k], [B, k]]; };

export function buildPanther(scene) {
  // ---------- pelo ----------
  const furTex = (() => {
    const c = document.createElement('canvas'); c.width = c.height = 512; const g = c.getContext('2d');
    g.fillStyle = '#0d0d10'; g.fillRect(0, 0, 512, 512);
    for (let i = 0; i < 70; i++) { // rosetas fantasmas
      const x = Math.random() * 512, y = Math.random() * 512, r = 9 + Math.random() * 12;
      g.strokeStyle = 'rgba(0,0,0,.55)'; g.lineWidth = 3 + Math.random() * 2; g.beginPath(); g.ellipse(x, y, r, r * 0.8, Math.random() * 3, 0.3, 5.6); g.stroke();
      g.fillStyle = 'rgba(30,28,33,.35)'; g.beginPath(); g.ellipse(x, y, r * 0.55, r * 0.45, 0, 0, 7); g.fill();
    }
    for (let i = 0; i < 9000; i++) { g.fillStyle = `rgba(${Math.random() < .5 ? '42,44,50' : '0,0,0'},${Math.random() * .25})`; g.fillRect(Math.random() * 512, Math.random() * 512, 1, 3); }
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.anisotropy = 8; return t;
  })();
  const bumpTex = (() => {
    const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('2d');
    g.fillStyle = '#808080'; g.fillRect(0, 0, 256, 256);
    for (let i = 0; i < 9000; i++) { const v = 90 + Math.random() * 80 | 0; g.strokeStyle = `rgb(${v},${v},${v})`; g.lineWidth = 1; const x = Math.random() * 256, y = Math.random() * 256; g.beginPath(); g.moveTo(x, y); g.lineTo(x + (Math.random() - .5) * 1.5, y + 3 + Math.random() * 3); g.stroke(); }
    const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; return t;
  })();
  const fur = new THREE.MeshPhysicalMaterial({ color: 0xffffff, map: furTex, roughness: 0.48, metalness: 0, sheen: 1, sheenColor: new THREE.Color(0x46506a), sheenRoughness: 0.36, bumpMap: bumpTex, bumpScale: 0.35 });

  // ---------- esqueleto (pose de referência, em metros; frente = +z) ----------
  const bones = [], B = (name, parent, wx, wy, wz) => { const b = new THREE.Bone(); b.name = name; b.userData.w = V(wx, wy, wz); bones.push(b); if (parent) { parent.add(b); b.position.copy(b.userData.w).sub(parent.userData.w); } else b.position.copy(b.userData.w); return bones.length - 1; };
  const iHips = B('hips', null, 0, 0.6, -0.36), hips = bones[iHips];
  const iChest = B('chest', hips, 0, 0.62, 0.2), chest = bones[iChest];
  const iNeck = B('neck', chest, 0, 0.68, 0.42), neck = bones[iNeck];
  const iHead = B('head', neck, 0, 0.84, 0.62), head = bones[iHead];
  const legs = [];
  [-1, 1].forEach(s => {
    const u = B('fu' + s, chest, s * 0.115, 0.56, 0.27), l = B('fl' + s, bones[u], s * 0.12, 0.3, 0.22), p = B('fp' + s, bones[l], s * 0.12, 0.09, 0.27);
    legs.push({ front: true, s, u: bones[u], l: bones[l], p: bones[p], iu: u, il: l, ip: p });
  });
  [-1, 1].forEach(s => {
    const u = B('hu' + s, hips, s * 0.115, 0.58, -0.4), l = B('hl' + s, bones[u], s * 0.13, 0.35, -0.27), p = B('hp' + s, bones[l], s * 0.13, 0.15, -0.5);
    legs.push({ front: false, s, u: bones[u], l: bones[l], p: bones[p], iu: u, il: l, ip: p });
  });
  const tailCurve = new THREE.CatmullRomCurve3([V(0, 0.6, -0.66), V(0, 0.5, -0.9), V(0, 0.32, -1.14), V(0, 0.2, -1.36), V(0, 0.22, -1.52), V(0, 0.32, -1.6)]);
  const NT = 10, tailI = []; let tp = hips;
  for (let k = 0; k < NT; k++) { const w = tailCurve.getPointAt(k / NT); const i = B('t' + k, tp, w.x, w.y, w.z); tailI.push(i); tp = bones[i]; }
  const tail = tailI.map(i => bones[i]);

  // ---------- pele ----------
  const geos = [];
  // tronco: anca forte, cintura fina, peito fundo; costas um pouco achatadas
  geos.push(tube([V(0, 0.6, -0.7), V(0, 0.63, -0.46), V(0, 0.6, -0.12), V(0, 0.62, 0.18), V(0, 0.6, 0.42), V(0, 0.58, 0.52)],
    (t, a) => {
      const prof = [[0, 0.07, 0.08], [0.08, 0.15, 0.17], [0.22, 0.17, 0.2], [0.42, 0.135, 0.16], [0.55, 0.14, 0.18], [0.72, 0.17, 0.235], [0.88, 0.15, 0.2], [1, 0.07, 0.09]];
      let k = 0; while (k < prof.length - 2 && prof[k + 1][0] < t) k++; const [t0, w0, h0] = prof[k], [t1, w1, h1] = prof[k + 1]; const f = smooth(clamp((t - t0) / (t1 - t0), 0, 1));
      let w = lerp(w0, w1, f), h = lerp(h0, h1, f); const s = Math.sin(a);
      if (s > 0) h *= 0.9; else h *= 1 + 0.12 * band(t, 0.62, 0.9, 0.2);
      return [w, h, -0.03 * band(t, 0.6, 0.95, 0.2)];
    }, t => blend2(t, 0.5, iHips, iChest, 0.25), 40, 26));
  // pescoço grosso subindo pra cabeça
  geos.push(tube([V(0, 0.62, 0.3), V(0, 0.7, 0.46), V(0, 0.79, 0.57), V(0, 0.84, 0.64)],
    t => [lerp(0.13, 0.085, t), lerp(0.16, 0.095, t), 0], t => t < 0.5 ? blend2(t, 0.25, iChest, iNeck, 0.3) : blend2(t, 0.85, iNeck, iHead, 0.25), 18, 22, false, false));
  // cabeça: crânio largo e baixo, testa reta, bochechas, focinho curto
  geos.push(blobGeo(V(0, 0.85, 0.67), 0.13, v => {
    let { x, y, z } = v; const front = Math.max(0, z);
    x *= 1.0 - 0.22 * front + 0.12 * Math.max(0, -y) * (1 - front);
    y *= y > 0 ? 0.78 - 0.1 * front : 0.86;
    z *= 1.08;
    return V(x, y, z);
  }, iHead));
  geos.push(blobGeo(V(0, 0.81, 0.78), 0.075, v => V(v.x * 1.05 * (1 - 0.15 * Math.max(0, v.z)), v.y * (v.y > 0 ? 0.62 : 0.75), v.z * 0.95), iHead, 22, 16)); // focinho
  geos.push(blobGeo(V(0, 0.77, 0.74), 0.06, v => V(v.x * 0.95, v.y * 0.45, v.z * 0.9), iHead, 18, 12)); // queixo
  [-1, 1].forEach(s => {
    geos.push(blobGeo(V(s * 0.03, 0.795, 0.835), 0.034, v => V(v.x, v.y * 0.7, v.z * 0.7), iHead, 14, 10)); // almofada do bigode
    geos.push(blobGeo(V(s * 0.082, 0.955, 0.6), 0.045, v => V(v.x * 0.9 * (1 - 0.55 * Math.max(0, v.y)), v.y * 1.05, v.z * 0.32), iHead, 14, 10)); // orelha arredondada
    geos.push(blobGeo(V(s * 0.05, 0.89, 0.755), 0.03, v => V(v.x * 1.25, v.y * 0.32, v.z * 0.7), iHead, 12, 8)); // arcada sobre o olho
  });
  // patas da frente: braço musculoso, cotovelo, antebraço, pata larga
  legs.filter(l => l.front).forEach(L => {
    const s = L.s;
    geos.push(tube([V(s * 0.1, 0.66, 0.3), V(s * 0.12, 0.44, 0.25), V(s * 0.12, 0.3, 0.22), V(s * 0.12, 0.17, 0.25), V(s * 0.12, 0.09, 0.28), V(s * 0.12, 0.05, 0.3)],
      t => { const r = t < 0.4 ? lerp(0.1, 0.064, t / 0.4) : t < 0.75 ? lerp(0.06, 0.044, (t - 0.4) / 0.35) : lerp(0.044, 0.042, (t - 0.75) / 0.25); return [r * 0.92, r * 1.08, 0]; },
      t => t < 0.6 ? blend2(t, 0.42, L.iu, L.il, 0.14) : blend2(t, 0.86, L.il, L.ip, 0.12), 22, 16, true, false));
    geos.push(blobGeo(V(s * 0.12, 0.035, 0.33), 0.06, v => V(v.x * 1.0, v.y * (v.y < 0 ? 0.35 : 0.6), v.z * 1.25 + (v.z > 0 ? 0.08 : 0)), L.ip, 18, 12));
  });
  // patas de trás: coxa enorme que entra no corpo, joelho pra frente, jarrete pra trás
  legs.filter(l => !l.front).forEach(L => {
    const s = L.s;
    geos.push(tube([V(s * 0.08, 0.68, -0.42), V(s * 0.12, 0.5, -0.33), V(s * 0.13, 0.35, -0.27), V(s * 0.13, 0.24, -0.39), V(s * 0.13, 0.15, -0.5), V(s * 0.13, 0.08, -0.48), V(s * 0.13, 0.05, -0.45)],
      t => { const r = t < 0.33 ? lerp(0.15, 0.07, t / 0.33) : t < 0.66 ? lerp(0.06, 0.042, (t - 0.33) / 0.33) : lerp(0.042, 0.04, (t - 0.66) / 0.34); return [r * (t < 0.33 ? 0.72 : 0.9), r * 1.1, 0]; },
      t => t < 0.5 ? blend2(t, 0.33, L.iu, L.il, 0.14) : blend2(t, 0.68, L.il, L.ip, 0.12), 26, 16, true, false));
    geos.push(blobGeo(V(s * 0.13, 0.035, -0.4), 0.056, v => V(v.x * 0.95, v.y * (v.y < 0 ? 0.35 : 0.6), v.z * 1.3 + (v.z > 0 ? 0.07 : 0)), L.ip, 18, 12));
  });
  // cauda longa em J, afinando
  geos.push(tube(Array.from({ length: 12 }, (_, i) => tailCurve.getPointAt(i / 11)),
    t => { const r = lerp(0.05, 0.03, t) + 0.006 * smooth(clamp((t - 0.85) / 0.15, 0, 1)); return [r, r, 0]; },
    t => { const f = t * NT, k = Math.min(NT - 1, Math.floor(f)), k2 = Math.min(NT - 1, k + 1), w = f - k; return t < 0.04 ? [[iHips, 1 - t / 0.04], [tailI[0], t / 0.04]] : [[tailI[k], 1 - w], [tailI[k2], w]]; }, 40, 12, true, true));

  const geo = mergeGeometries(geos, false); geos.forEach(g => g.dispose());
  const root = new THREE.Group(); scene.add(root);
  root.add(hips);
  const sk = new THREE.SkinnedMesh(geo, fur); sk.frustumCulled = false; sk.castShadow = false; root.add(sk);
  root.updateMatrixWorld(true); sk.bind(new THREE.Skeleton(bones), sk.matrixWorld);
  // olhos verdes (acesos) e nariz brilhante, presos à cabeça
  const eyeM = new THREE.MeshStandardMaterial({ color: 0xa8e04a, emissive: 0x7cc23a, emissiveIntensity: 1.6, roughness: 0.12 });
  const pupilM = new THREE.MeshBasicMaterial({ color: 0x000000 });
  const noseM = new THREE.MeshStandardMaterial({ color: 0x040405, roughness: 0.15 });
  const hw = head.userData.w;
  const att = (g, m, wx, wy, wz) => { const o = new THREE.Mesh(g, m); o.position.set(wx - hw.x, wy - hw.y, wz - hw.z); head.add(o); return o; };
  [-1, 1].forEach(s => {
    const e = att(new THREE.SphereGeometry(0.019, 18, 12), eyeM, s * 0.05, 0.873, 0.775); e.scale.set(1.3, 0.62, 0.5); e.rotation.set(0, s * 0.35, s * 0.28);
    const p = att(new THREE.CircleGeometry(0.006, 14), pupilM, s * 0.052, 0.873, 0.785); p.scale.set(0.45, 1.5, 1); p.rotation.y = s * 0.4;
  });
  const nose = att(new THREE.SphereGeometry(0.022, 16, 12), noseM, 0, 0.83, 0.855); nose.scale.set(1.35, 0.72, 0.7);
  blob(root, 0, -0.1, 0.42, 1.05, 0.55);
  const hit = new THREE.Mesh(new THREE.BoxGeometry(0.45, 0.7, 1.7), new THREE.MeshBasicMaterial({ visible: false })); hit.position.set(0, -0.05, 0.3); hit.userData.pet = 'pantera'; hips.add(hit);
  root.traverse(o => { if (o.isMesh) { o.userData.pet = 'pantera'; o.userData.dyn = true; } });
  root.userData.dyn = true;
  root.scale.setScalar(1.28);

  // ---------- comportamento: solta no tapete ----------
  const RMIN = 4.3, RMAX = 4.98;
  const st = { pos: V(Math.cos(0.8) * 4.65, 0, Math.sin(0.8) * 4.65), heading: Math.atan2(-Math.sin(0.8), Math.cos(0.8)), speed: 0, state: 'walk', t: 0, target: null, dir: 1, phase: 0, look: 0, lookT: 0, stareAt: null, sit: 0, headY: 0, headX: 0, maxSpd: 0.4 };
  function pickTarget() {
    if (Math.random() < 0.15) st.dir *= -1; // às vezes dá meia-volta
    const a = Math.atan2(st.pos.z, st.pos.x) + st.dir * (0.35 + Math.random() * 0.9), r = RMIN + 0.05 + Math.random() * (RMAX - RMIN - 0.1);
    st.target = V(Math.cos(a) * r, 0, Math.sin(a) * r); st.state = 'walk'; st.maxSpd = 0.34 + Math.random() * 0.18;
  }
  pickTarget();
  const out = { root, head, st, name: 'Fartuzzi' };
  out.angle = () => Math.atan2(st.pos.z, st.pos.x);
  out.blockers = null; // main: posições de quem está andando, pra ela esperar a pessoa passar
  out.stare = (worldPos, secs, onStart) => { if (st.state === 'stare' || st.state === 'sit') return false; st.state = 'stare'; st.t = secs; st.stareAt = worldPos.clone(); onStart && onStart(); return true; };
  out.busy = () => st.state === 'stare';
  const tmp = V(0, 0, 0), fwd = V(0, 0, 0);
  const wrap = a => Math.atan2(Math.sin(a), Math.cos(a));
  out.update = (dt, now) => {
    dt = Math.min(dt, 0.1);
    let wantSpd = 0, wantHead = st.heading, steer = false;
    if (st.state === 'walk') {
      tmp.subVectors(st.target, st.pos); tmp.y = 0; const d = tmp.length();
      wantHead = Math.atan2(tmp.x, tmp.z); steer = true;
      const turn = Math.abs(wrap(wantHead - st.heading));
      wantSpd = st.maxSpd * (1 - Math.min(1, turn) * 0.65) * Math.min(1, d / 0.5 + 0.25);
      if (out.blockers) { fwd.set(Math.sin(st.heading), 0, Math.cos(st.heading)); for (const b of out.blockers()) { tmp.subVectors(b, st.pos); tmp.y = 0; if (tmp.length() < 1.7 && tmp.dot(fwd) > 0) { wantSpd = 0; break; } } }
      if (d < 0.3) { const r = Math.random(); if (r < 0.42) { st.state = 'pause'; st.t = 1.5 + Math.random() * 3.5; st.lookT = 0; } else if (r < 0.54) { st.state = 'sit'; st.t = 7 + Math.random() * 8; } else pickTarget(); }
    } else if (st.state === 'pause' || st.state === 'sit') {
      st.t -= dt; if (st.t <= 0) pickTarget();
    } else if (st.state === 'stare') {
      tmp.subVectors(st.stareAt, st.pos); wantHead = st.heading + clamp(wrap(Math.atan2(tmp.x, tmp.z) - st.heading), -0.5, 0.5) * 0.6; steer = true;
      st.t -= dt; if (st.t <= 0) { st.stareAt = null; pickTarget(); }
    }
    st.speed = lerp(st.speed, wantSpd, Math.min(1, dt * 2.2));
    if (steer) st.heading += clamp(wrap(wantHead - st.heading), -1.0 * dt, 1.0 * dt);
    st.pos.x += Math.sin(st.heading) * st.speed * dt; st.pos.z += Math.cos(st.heading) * st.speed * dt;
    const r = Math.hypot(st.pos.x, st.pos.z), rc = clamp(r, RMIN, RMAX); if (r !== rc) { st.pos.x *= rc / r; st.pos.z *= rc / r; }
    root.position.copy(st.pos); root.rotation.y = st.heading;
    // corpo
    const mv = clamp(st.speed / 0.4, 0, 1);
    st.phase += dt * (0.2 + st.speed * 2.1) * (mv > 0.02 ? 1 : 0);
    st.sit = lerp(st.sit, st.state === 'sit' ? 1 : 0, Math.min(1, dt * 1.6)); const S = smooth(st.sit);
    const OFF = [0, 0.5, 0.75, 0.25]; // frente esq, frente dir, trás esq, trás dir (passo lateral de felino)
    legs.forEach((L, i) => {
      const p = (st.phase + OFF[i]) * Math.PI * 2, sw = Math.sin(p) * mv, lift = Math.max(0, -Math.cos(p)) * mv;
      if (L.front) { L.u.rotation.x = -sw * 0.38 + S * 0.3; L.l.rotation.x = lift * 0.95 - S * 0.05; L.p.rotation.x = -lift * 0.6; }
      else { L.u.rotation.x = -sw * 0.34 - S * 1.05; L.l.rotation.x = -lift * 0.55 + S * 1.55; L.p.rotation.x = lift * 0.75 - S * 0.5; }
    });
    hips.position.y = hips.userData.w.y + Math.sin(st.phase * Math.PI * 4) * 0.008 * mv - S * 0.26;
    hips.rotation.x = -S * 0.55; chest.rotation.x = S * 0.28;
    hips.rotation.z = Math.sin(st.phase * Math.PI * 2) * 0.03 * mv; chest.rotation.z = -hips.rotation.z * 0.8;
    hips.rotation.y = Math.sin(st.phase * Math.PI * 2) * 0.04 * mv; chest.rotation.y = -hips.rotation.y;
    // cabeça
    let ty = Math.sin(now * 0.4) * 0.12, tx = 0.18 * mv;
    if (st.state === 'pause' || st.state === 'sit') { st.lookT -= dt; if (st.lookT <= 0) { st.look = (Math.random() - 0.5) * 1.6; st.lookT = 1.2 + Math.random() * 1.8; } ty = st.look; tx = -0.08 - S * 0.1; }
    if (st.state === 'stare' && st.stareAt) { head.getWorldPosition(tmp); ty = clamp(wrap(Math.atan2(st.stareAt.x - tmp.x, st.stareAt.z - tmp.z) - st.heading), -1.3, 1.3); tx = -0.12; }
    st.headY = lerp(st.headY, ty, Math.min(1, dt * 2.2)); st.headX = lerp(st.headX, tx, Math.min(1, dt * 2.2));
    neck.rotation.y = st.headY * 0.55; head.rotation.y = st.headY * 0.45; neck.rotation.x = st.headX; head.rotation.x = -st.headX * 0.4;
    eyeM.emissiveIntensity = st.state === 'stare' ? 2.6 : 1.6;
    // cauda
    tail.forEach((b, k) => { b.rotation.y = Math.sin(now * (mv > 0.1 ? 1.3 : 2.2) - k * 0.42) * (0.05 + k * 0.012) * (st.state === 'stare' ? 1.6 : 1); b.rotation.x = S * (k < 3 ? 0.35 : -0.05); });
  };
  return out;
}
