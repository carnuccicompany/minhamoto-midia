import * as THREE from 'three';
import { mergeVertices } from 'three/examples/jsm/utils/BufferGeometryUtils.js';

// ---------- utilidades ----------
const sstep = (a, b, x) => { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); };
const mix = (a, b, t) => a + (b - a) * t;
// ruído de valor 3D barato e determinístico
function hash(x, y, z) { const s = Math.sin(x * 127.1 + y * 311.7 + z * 74.7) * 43758.5453; return s - Math.floor(s); }
export function noise3(x, y, z) {
  const xi = Math.floor(x), yi = Math.floor(y), zi = Math.floor(z), xf = x - xi, yf = y - yi, zf = z - zi;
  const u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf), w = zf * zf * (3 - 2 * zf);
  const c = (a, b, d) => hash(xi + a, yi + b, zi + d);
  return mix(mix(mix(c(0, 0, 0), c(1, 0, 0), u), mix(c(0, 1, 0), c(1, 1, 0), u), v), mix(mix(c(0, 0, 1), c(1, 0, 1), u), mix(c(0, 1, 1), c(1, 1, 1), u), v), w);
}
// subdivide triângulos (corte no meio) n vezes
export function subdivide(geo, n) {
  let g = geo.index ? geo.toNonIndexed() : geo.clone();
  for (let k = 0; k < n; k++) {
    const p = g.attributes.position.array, out = [];
    for (let i = 0; i < p.length; i += 9) {
      const a = [p[i], p[i + 1], p[i + 2]], b = [p[i + 3], p[i + 4], p[i + 5]], c = [p[i + 6], p[i + 7], p[i + 8]];
      const m = (u, v) => [(u[0] + v[0]) / 2, (u[1] + v[1]) / 2, (u[2] + v[2]) / 2];
      const ab = m(a, b), bc = m(b, c), ca = m(c, a);
      out.push(...a, ...ab, ...ca, ...ab, ...b, ...bc, ...ca, ...bc, ...c, ...ab, ...bc, ...ca);
    }
    g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(out, 3));
  }
  return g;
}

// ---------- cabeça: uma esfera só, esculpida (sem bolinhas coladas) ----------
// rosto de cada um: largura, mandíbula, queixo, maçãs, nariz e idade (rugas) variam por pessoa
export const face = W => (W && typeof W === 'object') ? W : { W: !!W, id: W ? 'w' : 'm', wide: 1, jawK: 1, chinK: 1, cheekK: 1, browK: 1, noseL: 1, noseW: 1, age: 35 };
export function makeFace(d) {
  let s = 0; for (const ch of String(d.id || d.nome || 'x')) s = (s * 31 + ch.charCodeAt(0)) % 100003;
  const r = () => { s = (s * 16807) % 2147483647; return (s % 10000) / 10000; };
  const W = !!d.mulher;
  return { W, id: (d.id || d.nome) + '', wide: 0.96 + r() * 0.08, jawK: (W ? 0.95 : 0.92) + r() * 0.18, chinK: 0.7 + r() * 0.7, cheekK: 0.7 + r() * 0.7, browK: W ? 0.6 : 0.8 + r() * 0.6, noseL: 0.9 + r() * 0.22, noseW: 0.88 + r() * 0.28, age: d.idade || 40 };
}
export function headDims(W) { const F = face(W), k = F.wide; return F.W ? { rx: 0.075 * k, ry: 0.108, rz: 0.096, jaw: 0.62 * F.jawK } : { rx: 0.081 * k, ry: 0.112, rz: 0.1, jaw: 0.72 * F.jawK }; }
// ponto da superfície da cabeça na direção u (unitário)
export function headPoint(u, W) {
  const F = face(W), D = headDims(F);
  let x = u.x * D.rx, y = u.y * D.ry, z = u.z * D.rz;
  const low = sstep(0.0, 1.0, -u.y);                       // metade de baixo
  x *= mix(1, D.jaw, Math.pow(low, 1.35));                 // mandíbula afinando até o queixo
  if (u.y < -0.2 && u.z > 0) z += 0.012 * F.chinK * sstep(0.55, 0.95, -u.y) * u.z;          // queixo pra frente
  if (u.z < 0) z *= mix(1.06, 0.78, sstep(-0.1, -0.85, u.y));                       // nuca arredondada, pescoço recolhido
  if (u.z > 0 && u.y > 0.25) z *= mix(1, 0.94, sstep(0.25, 0.9, u.y));              // testa
  x *= 1 - 0.035 * (1 - Math.abs(u.y));                                              // laterais achatadas
  const p = new THREE.Vector3(x, y, z);
  // olhos afundados
  for (const s of [-1, 1]) {
    const d = Math.hypot(x - s * 0.031, (y - 0.012) * 1.3); if (z > 0 && d < 0.03) p.z -= 0.0075 * Math.pow(1 - d / 0.03, 2);
    const c = Math.hypot(x - s * 0.047, (y + 0.02) * 1.2); if (z > 0 && c < 0.03) p.z += 0.004 * F.cheekK * Math.pow(1 - c / 0.03, 2); // maçã do rosto
  }
  if (z > 0 && Math.abs(x) < 0.058) p.z += 0.0045 * F.browK * sstep(0.022, 0.035, y) * (1 - sstep(0.042, 0.06, y)) * (1 - Math.abs(x) / 0.058); // arco da sobrancelha
  if (z > 0 && Math.abs(x) < 0.03 && y < -0.035 && y > -0.075) p.z += 0.003 * (1 - Math.abs(x) / 0.03); // boca levemente saltada
  return p;
}
const ZC = new Map();
export function zAt(x, y, W) { // profundidade da frente do rosto em (x,y)
  let best = 1e9, bz = 0;
  const key = face(W).id + x.toFixed(3) + y.toFixed(3); if (ZC.has(key)) return ZC.get(key);
  for (let a = -1; a <= 1; a += 0.02) for (let b = -1; b <= 1; b += 0.02) {
    const zz = 1 - a * a - b * b; if (zz <= 0) continue;
    const p = headPoint(new THREE.Vector3(a, b, Math.sqrt(zz)), W); const d = (p.x - x) ** 2 + (p.y - y) ** 2; if (d < best) { best = d; bz = p.z; }
  }
  ZC.set(key, bz); return bz;
}
export function headGeo(W) {
  const F = face(W), Wb = F.W, age = sstep(30, 70, F.age);
  const g = new THREE.SphereGeometry(1, 48, 36), pos = g.attributes.position, u = new THREE.Vector3();
  const tint = new Float32Array(pos.count * 3);
  for (let i = 0; i < pos.count; i++) {
    u.fromBufferAttribute(pos, i).normalize(); const p = headPoint(u, W); pos.setXYZ(i, p.x, p.y, p.z);
    // cor: bochecha mais quente, olheira sutil, embaixo do queixo mais escuro
    let r = 1, gg = 1, b = 1;
    for (const s of [-1, 1]) { const c = Math.hypot(p.x - s * 0.046, (p.y + 0.028) * 1.1); if (p.z > 0 && c < 0.035) { const k = (1 - c / 0.035) ** 2 * (Wb ? 0.9 : 0.55); r += 0.05 * k; gg -= 0.05 * k; b -= 0.05 * k; }
      const e = Math.hypot(p.x - s * 0.031, p.y - 0.004); if (p.z > 0 && e < 0.024) { const k = (1 - e / 0.024) ** 2; r -= 0.06 * k; gg -= 0.07 * k; b -= 0.05 * k; } }
    const under = sstep(-0.3, -0.85, u.y) * (u.z < 0.5 ? 1 : 0.4); r -= 0.08 * under; gg -= 0.09 * under; b -= 0.08 * under;
    if (p.z > 0) { // marcas de expressão: sulco nariz-boca, testa e pés de galinha crescem com a idade
      let w = 0;
      for (const s of [-1, 1]) {
        const yy = p.y, xx = s * p.x; // sulco: curva que desce da asa do nariz até o canto da boca
        if (yy < -0.02 && yy > -0.075) { const cx = 0.019 + (-0.02 - yy) * 0.28; const dd = Math.abs(xx - cx); w += (1 - sstep(0.0, 0.004, dd)) * (0.35 + 0.65 * age) * 0.9; }
        const ce = Math.hypot(xx - 0.06, p.y - 0.008); if (ce < 0.016 && xx > 0.052) w += age * 0.5 * (0.5 + 0.5 * Math.sin(Math.atan2(p.y - 0.008, xx - 0.06) * 7)) * (1 - ce / 0.016);
      }
      if (p.y > 0.05 && p.y < 0.085 && Math.abs(p.x) < 0.045) w += age * 0.55 * (0.5 + 0.5 * Math.cos((p.y - 0.05) / 0.012 * Math.PI * 2)) * (1 - Math.abs(p.x) / 0.045);
      const bag = Math.hypot(p.x - Math.sign(p.x) * 0.031, (p.y + 0.012) * 1.8); if (bag < 0.016) w += age * 0.45 * (1 - bag / 0.016);
      const dk = Math.min(0.22, w * 0.12); r -= dk * 0.9; gg -= dk * 1.05; b -= dk;
    }
    tint[i * 3] = r; tint[i * 3 + 1] = gg; tint[i * 3 + 2] = b;
  }
  g.setAttribute('tint', new THREE.BufferAttribute(tint, 3));
  g.computeVertexNormals(); return g;
}

// ---------- cabelo: casca que segue a cabeça, com linha de cabelo e volume por estilo ----------
const HL = { // linha do cabelo: altura (u.y) por ângulo |θ| (0 = testa, π = nuca)
  curto:    [[0, 0.62], [0.55, 0.6], [0.85, 0.46], [1.05, 0.28], [1.3, -0.1], [1.75, 0.05], [2.2, -0.35], [Math.PI, -0.5]],
  grisalho: [[0, 0.66], [0.55, 0.62], [0.85, 0.5], [1.05, 0.32], [1.3, -0.08], [1.75, 0.05], [2.2, -0.35], [Math.PI, -0.5]],
  penteado: [[0, 0.58], [0.55, 0.56], [0.85, 0.44], [1.05, 0.27], [1.3, -0.1], [1.75, 0.05], [2.2, -0.35], [Math.PI, -0.5]],
  liso:     [[0, 0.36], [0.75, 0.36], [1.05, 0.2], [1.3, -0.12], [1.75, 0.0], [2.2, -0.4], [Math.PI, -0.55]],
  raspado:  [[0, 0.5], [0.75, 0.42], [1.05, 0.25], [1.3, -0.05], [1.75, 0.05], [2.2, -0.35], [Math.PI, -0.5]],
  longo:    [[0, 0.42], [0.6, 0.38], [0.95, 0.1], [1.2, -0.75], [Math.PI, -0.95]],
  chanel:   [[0, 0.3], [0.6, 0.3], [0.95, 0.05], [1.2, -0.62], [Math.PI, -0.7]],
  coque:    [[0, 0.5], [0.75, 0.44], [1.05, 0.22], [1.3, -0.15], [1.75, -0.05], [2.2, -0.45], [Math.PI, -0.6]],
};
function lineAt(tab, th) { for (let i = 1; i < tab.length; i++) if (th <= tab[i][0]) { const [a, ya] = tab[i - 1], [b, yb] = tab[i]; const t = sstep(0, 1, (th - a) / (b - a)); return mix(ya, yb, t); } return tab[tab.length - 1][1]; }
function shellGeo(W, maskFn, thickFn, seed = 1, seg = [66, 48]) {
  const g0 = new THREE.SphereGeometry(1, seg[0], seg[1]).toNonIndexed(), pos = g0.attributes.position, u = new THREE.Vector3();
  const D = headDims(W), inv = new THREE.Vector3(1 / D.rx, 1 / D.ry, 1 / D.rz);
  const keep = new Float32Array(pos.count), P = new Float32Array(pos.count * 3), T = new Float32Array(pos.count), out = [], tint = [];
  for (let i = 0; i < pos.count; i++) {
    u.fromBufferAttribute(pos, i).normalize();
    const th = Math.abs(Math.atan2(u.x, u.z)), hp = headPoint(u, W);
    const m = maskFn(u, th, hp); keep[i] = m;
    const n = noise3(u.x * 6 + seed, u.y * 6, u.z * 6), fine = noise3(u.x * 22 + seed, u.y * 22, u.z * 22);
    let t = thickFn(u, th) * (0.88 + 0.24 * n) + 0.0009 * (fine - 0.5);
    t = mix(-0.005, t, sstep(0.15, 0.6, m));            // borda entra na pele: linha do cabelo lisa
    const nrm = u.clone().multiply(inv).normalize(), q = hp.addScaledVector(nrm, t + 0.0012);
    P[i * 3] = q.x; P[i * 3 + 1] = q.y; P[i * 3 + 2] = q.z; T[i] = 0.8 + 0.32 * fine + 0.12 * n;
  }
  for (let i = 0; i < pos.count; i += 3) {
    if (Math.max(keep[i], keep[i + 1], keep[i + 2]) < 0.06) continue;
    for (let k = 0; k < 3; k++) { out.push(P[(i + k) * 3], P[(i + k) * 3 + 1], P[(i + k) * 3 + 2]); const c = T[i + k]; tint.push(c, c, c); }
  }
  let g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(out, 3)); g.setAttribute('tint', new THREE.Float32BufferAttribute(tint, 3));
  g = mergeVertices(g, 1e-5); g.computeVertexNormals(); return g;
}
export function hairGeo(style, W, seed = 1) {
  const tab = HL[style] || HL.curto;
  const earCut = ['curto', 'grisalho', 'penteado', 'raspado', 'liso', 'coque'].includes(style);
  const mask = (u, th) => {
    let line = lineAt(tab, th);
    if (earCut && th > 1.32 && th < 1.95 && u.y < 0.12) line = Math.max(line, 0.12 - 0.25 * Math.max(0, 0.45 - Math.abs(th - 1.62)));
    return sstep(line - 0.02, line + 0.13, u.y);
  };
  const thick = (u) => {
    switch (style) {
      case 'raspado': return 0.0018;
      case 'curto': return 0.006 + 0.012 * Math.max(0, u.y) ** 1.5;
      case 'grisalho': return 0.005 + 0.01 * Math.max(0, u.y) ** 1.5;
      case 'penteado': return 0.006 + 0.016 * Math.max(0, u.y) ** 1.2 + 0.018 * sstep(0.2, 0.8, u.z) * sstep(0.4, 0.85, u.y);
      case 'liso': return 0.008 + 0.012 * Math.max(0, u.y) + 0.01 * sstep(0.3, 0.9, u.z) * sstep(0.2, 0.6, u.y) * (u.x < 0.2 ? 1 : 0.4);
      case 'longo': return 0.01 + 0.012 * Math.max(0, u.y) + 0.012 * sstep(0, -0.8, u.y) * (u.z < 0.3 ? 1 : 0.6);
      case 'chanel': return 0.011 + 0.01 * Math.max(0, u.y) + 0.016 * sstep(0, -0.6, u.y);
      case 'coque': return 0.005 + 0.006 * Math.max(0, u.y);
      default: return 0.008;
    }
  };
  return shellGeo(W, mask, thick, seed);
}
export function beardGeo(W, full = true, seed = 3) {
  const mask = (u, th, p) => {
    const jaw = sstep(-0.25, -0.45, u.y) * (1 - sstep(1.45, 1.75, th));
    const side = sstep(1.15, 1.32, th) * (1 - sstep(1.5, 1.62, th)) * sstep(0.15, -0.05, u.y); // costeleta
    const lips = Math.abs(p.x) < 0.024 && p.y < -0.048 && p.y > -0.078 ? 0 : 1;
    return Math.max(jaw, side) * lips * (full ? 1 : sstep(-0.55, -0.7, u.y) + 0.0);
  };
  return shellGeo(W, mask, () => (full ? 0.0045 : 0.003), seed, [48, 36]);
}

// ---------- tronco do paletó: anéis em superelipse (ombro quadrado de alfaiataria) ----------
const SECT_M = [ // y, meia-largura, meia-profundidade, deslocamento z, expoente
  [-0.13, 0.178, 0.112, -0.004, 2.4], [-0.06, 0.172, 0.108, -0.002, 2.35], [0.0, 0.165, 0.104, 0.0, 2.3], [0.1, 0.158, 0.099, 0.004, 2.3], [0.2, 0.156, 0.103, 0.01, 2.4], [0.3, 0.172, 0.112, 0.012, 2.5],
  [0.4, 0.192, 0.114, 0.006, 2.7], [0.455, 0.206, 0.106, -0.002, 3.1], [0.505, 0.192, 0.092, -0.008, 3.0], [0.545, 0.13, 0.074, -0.004, 2.6], [0.585, 0.072, 0.062, 0.004, 2.2], [0.6, 0.04, 0.04, 0.004, 2]];
const SECT_W = [
  [-0.12, 0.172, 0.108, -0.004, 2.4], [-0.06, 0.166, 0.104, -0.002, 2.35], [0.0, 0.16, 0.1, 0.0, 2.3], [0.1, 0.145, 0.094, 0.004, 2.3], [0.19, 0.132, 0.09, 0.008, 2.3], [0.3, 0.152, 0.116, 0.018, 2.4],
  [0.4, 0.168, 0.11, 0.01, 2.6], [0.45, 0.176, 0.098, 0.0, 2.9], [0.5, 0.165, 0.086, -0.006, 2.8], [0.54, 0.115, 0.07, -0.003, 2.5], [0.575, 0.065, 0.058, 0.004, 2.2], [0.59, 0.035, 0.035, 0.004, 2]];
export const sections = W => (W ? SECT_W : SECT_M);
function sectAt(W, y) { const S = sections(W); for (let i = 1; i < S.length; i++) if (y <= S[i][0]) { const a = S[i - 1], b = S[i], t = (y - a[0]) / (b[0] - a[0]); return a.map((v, k) => mix(v, b[k], t)); } return S[S.length - 1]; }
export function frontZ(W, x, y) { const [, hw, hd, zo, n] = sectAt(W, y); const r = Math.min(1, Math.abs(x) / hw); return zo + hd * Math.pow(Math.max(0, 1 - Math.pow(r, n)), 1 / n); }
export function torsoGeo(W) {
  const S = sections(W), N = 40, rows = [];
  // anéis intermediários pra suavizar
  const ys = []; for (let i = 0; i < S.length - 1; i++) for (let k = 0; k < 3; k++) ys.push(mix(S[i][0], S[i + 1][0], k / 3)); ys.push(S[S.length - 1][0]);
  const pos = [], idx = [];
  ys.forEach(y => { const [, hw, hd, zo, n] = sectAt(W, y); for (let j = 0; j <= N; j++) { const a = j / N * Math.PI * 2, c = Math.cos(a), s = Math.sin(a); const x = hw * Math.sign(s) * Math.pow(Math.abs(s), 2 / n), z = zo + hd * Math.sign(c) * Math.pow(Math.abs(c), 2 / n); pos.push(x, y, z); } });
  const R = N + 1;
  for (let i = 0; i < ys.length - 1; i++) for (let j = 0; j < N; j++) { const a = i * R + j, b = a + 1, c = a + R, d = c + 1; idx.push(a, c, b, b, c, d); }
  const top = pos.length / 3; pos.push(0, ys[ys.length - 1], 0.004); for (let j = 0; j < N; j++) idx.push((ys.length - 1) * R + j, top, (ys.length - 1) * R + j + 1);
  let g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setIndex(idx); g.computeVertexNormals();
  if (g.attributes.normal.getZ(Math.floor(ys.length / 2) * R) < 0) { for (let i = 0; i < idx.length; i += 3) { const t = idx[i + 1]; idx[i + 1] = idx[i + 2]; idx[i + 2] = t; } g.setIndex(idx); g.computeVertexNormals(); }
  return g;
}
// peça plana que gruda na frente do paletó (lapela, camisa, gravata, bolso)
function faceOut(g, axis, sign) { // garante que os triângulos olham pra fora
  const p = g.attributes.position.array, a = new THREE.Vector3(), b = new THREE.Vector3(), c = new THREE.Vector3();
  for (let i = 0; i < p.length; i += 9) {
    a.fromArray(p, i); b.fromArray(p, i + 3); c.fromArray(p, i + 6);
    const n = b.clone().sub(a).cross(c.clone().sub(a));
    if (n.getComponent(axis) * sign < 0) for (let k = 0; k < 3; k++) { const t = p[i + 3 + k]; p[i + 3 + k] = p[i + 6 + k]; p[i + 6 + k] = t; }
  }
}
export function onChest(shape, W, off, sub = 3) {
  const g = subdivide(new THREE.ShapeGeometry(shape), sub), p = g.attributes.position;
  faceOut(g, 2, 1);
  for (let i = 0; i < p.count; i++) { const x = p.getX(i), y = p.getY(i); p.setZ(i, frontZ(W, x, y) + off(x, y)); }
  g.computeVertexNormals(); return g;
}

// nariz numa peça só: ponte fina que alarga até a ponta e as asas, encaixado no rosto
export function noseGeo(W) {
  const F = face(W);
  const tab = []; for (let k = 0; k <= 40; k++) { const y = 0.02 - k * 0.002; tab.push(zAt(0, y, W)); }
  const zf = y => { const f = (0.02 - y) / 0.002, i = Math.max(0, Math.min(39, Math.floor(f))), t = Math.min(1, Math.max(0, f - i)); return mix(tab[i], tab[i + 1], t); };
  const g = new THREE.SphereGeometry(1, 24, 20), pos = g.attributes.position, tint = new Float32Array(pos.count * 3);
  const S = (F.W ? 0.88 : 1) * F.noseW, L = F.noseL;
  for (let i = 0; i < pos.count; i++) {
    const x = pos.getX(i), y = pos.getY(i), z = pos.getZ(i), t = (1 - y) / 2;
    const Y = 0.016 - 0.05 * L * t;
    let w = mix(0.0042, 0.0125, Math.pow(t, 1.6)) * S + 0.0042 * S * Math.exp(-Math.pow((t - 0.86) / 0.07, 2)) * Math.max(0, -z + 0.4);
    const d = z > 0 ? mix(0.003, 0.0175, Math.pow(t, 1.35)) * S * (t > 0.9 ? mix(1, 0.55, (t - 0.9) / 0.1) : 1) : 0.004;
    const X = x * w, Z = zf(Y) - 0.0025 + z * d;
    pos.setXYZ(i, X, Y, Z);
    const nost = (t > 0.88 && z > -0.2 && z < 0.55 && Math.abs(x) > 0.15) ? 0.62 : 1; const sh = 1 - 0.06 * Math.max(0, -z);
    tint[i * 3] = nost * sh * 0.985; tint[i * 3 + 1] = nost * sh * 0.97; tint[i * 3 + 2] = nost * sh * 0.97;
  }
  g.setAttribute('tint', new THREE.BufferAttribute(tint, 3)); g.computeVertexNormals(); return g;
}
