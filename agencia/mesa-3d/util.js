import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';
import { mergeGeometries } from 'three/examples/jsm/utils/BufferGeometryUtils.js';

export const GOLD = 0xd4b26a;
const MCACHE = new Map();
const LIGHT_KEYS = ['map', 'emissive', 'emissiveMap', 'emissiveIntensity', 'roughness', 'metalness', 'transparent', 'opacity', 'side', 'depthWrite', 'flatShading', 'toneMapped'];
export const mat = (color, o = {}) => {
  const p = { color, roughness: 0.6, metalness: 0 }; for (const k of LIGHT_KEYS) if (o[k] !== undefined) p[k] = o[k];
  const key = JSON.stringify(p, (k, v) => (v && v.isTexture ? v.uuid : v && v.isColor ? v.getHex() : v));
  if (MCACHE.has(key)) return MCACHE.get(key);
  const m = new THREE.MeshStandardMaterial(p); MCACHE.set(key, m); return m;
};
// "physical" virou standard (bem mais leve); brilho de verniz vira rugosidade menor
export const phys = (color, o = {}) => mat(color, Object.assign({}, o, { roughness: o.clearcoat ? Math.min(o.roughness ?? 0.5, 0.25) : (o.roughness ?? 0.5) }));
export function tex(w, h, draw, repeat) {
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
  if (repeat) { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(repeat[0], repeat[1]); }
  return t;
}
export function mesh(geo, m, parent, pos, rot, shadow = true) {
  const o = new THREE.Mesh(geo, m);
  if (pos) o.position.set(pos[0], pos[1], pos[2]);
  if (rot) o.rotation.set(rot[0], rot[1], rot[2]);
  o.castShadow = shadow; o.receiveShadow = true;
  if (parent) parent.add(o);
  return o;
}
export const box = (w, h, d) => new THREE.BoxGeometry(w, h, d);
export const rbox = (w, h, d, r = 0.03, s = 2) => new RoundedBoxGeometry(w, h, d, s, Math.min(r, w / 2, h / 2, d / 2));
export const cyl = (rt, rb, h, s = 14) => new THREE.CylinderGeometry(rt, rb, h, s);
export const sph = (r, a = 10, b = 7) => new THREE.SphereGeometry(r, Math.min(a, 12), Math.min(b, 9));
export const lerp = THREE.MathUtils.lerp;
export const clamp = THREE.MathUtils.clamp;
export const smooth = t => t * t * (3 - 2 * t);
export const ease = (cur, target, k, dt) => cur + (target - cur) * (1 - Math.exp(-k * dt));
export const angLerp = (a, b, k) => a + Math.atan2(Math.sin(b - a), Math.cos(b - a)) * k;

export const M = {
  gold: mat(GOLD, { metalness: 1, roughness: 0.25 }),
  goldDim: mat(0xb08a45, { metalness: 1, roughness: 0.38 }),
  brass: mat(0xc9a35a, { metalness: 1, roughness: 0.32 }),
  chrome: mat(0xd8d8d8, { metalness: 1, roughness: 0.15 }),
  alu: mat(0xc6c8cc, { metalness: 0.9, roughness: 0.32 }),
  black: mat(0x0d0d0f, { roughness: 0.35 }),
  blackGloss: phys(0x0a0a0b, { roughness: 0.15, clearcoat: 1, clearcoatRoughness: 0.1 }),
  white: mat(0xf4f2ee, { roughness: 0.45 }),
  porcelain: phys(0xf7f5f0, { roughness: 0.2, clearcoat: 0.6 }),
  leather: mat(0x141110, { roughness: 0.38 }),
  leatherDark: phys(0x0c0a09, { roughness: 0.5, clearcoat: 0.2 }),
  glass: new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.05, metalness: 0.1, transparent: true, opacity: 0.25, depthWrite: false }),
  amber: phys(0xb8651a, { roughness: 0.1, transparent: true, opacity: 0.88, emissive: 0x2a1000 }),
  water: phys(0xcfe8ff, { roughness: 0.05, transparent: true, opacity: 0.45 }),
  ice: phys(0xeaf6ff, { roughness: 0.08, transparent: true, opacity: 0.55 }),
  coffee: mat(0x2a160a, { roughness: 0.2 }),
  cigar: mat(0x6b4426, { roughness: 0.85 }),
  ember: mat(0xff6a1a, { emissive: 0xff4a00, emissiveIntensity: 2.2 }),
  cash: mat(0x8fae82, { roughness: 0.85 }),
  band: mat(0xe9dcb8, { roughness: 0.7 }),
  shirt: mat(0xf3f1ec, { roughness: 0.7 }),
  shoe: phys(0x0a0908, { roughness: 0.25, clearcoat: 0.8, clearcoatRoughness: 0.2 }),
  sock: mat(0x111111, { roughness: 0.9 }),
  sclera: mat(0xf2efe9, { roughness: 0.3 }),
  iris: phys(0x2a1a10, { roughness: 0.1, clearcoat: 1 }),
};

export function marbleTex(base, vein, n = 26, size = 1024, rep = [4, 4]) {
  return tex(size, size, (g, w, h) => {
    g.fillStyle = base; g.fillRect(0, 0, w, h);
    for (let i = 0; i < n; i++) {
      g.strokeStyle = vein.replace('A', (0.05 + Math.random() * 0.18).toFixed(2)); g.lineWidth = 0.6 + Math.random() * 2.2;
      g.beginPath(); let x = Math.random() * w, y = -20; g.moveTo(x, y);
      while (y < h + 20) { x += (Math.random() - .5) * 70; y += 18 + Math.random() * 40; g.lineTo(x, y); } g.stroke();
    }
  }, rep);
}

export function goldGrad(g, w, h) {
  const gr = g.createLinearGradient(0, 0, w, h);
  gr.addColorStop(0, '#f6e3ad'); gr.addColorStop(.45, '#d4b26a'); gr.addColorStop(.7, '#a8823f'); gr.addColorStop(1, '#f0d9a0');
  return gr;
}

// logo dourada a partir da máscara branca
export function goldLogo(LOGO, size, draw) {
  return new Promise(res => {
    const img = new Image();
    img.onload = () => {
      const c = document.createElement('canvas'); c.width = c.height = size; const g = c.getContext('2d');
      const t = document.createElement('canvas'); t.width = t.height = size; const tg = t.getContext('2d');
      const s = size * (draw ? draw.scale : 0.9), ar = img.height / img.width;
      tg.drawImage(img, (size - s) / 2, (size - s * ar) / 2, s, s * ar);
      tg.globalCompositeOperation = 'source-in'; tg.fillStyle = goldGrad(tg, size, size); tg.fillRect(0, 0, size, size);
      if (draw) draw.fn(g, size, t); else g.drawImage(t, 0, 0);
      const T = new THREE.CanvasTexture(c); T.colorSpace = THREE.SRGBColorSpace; T.anisotropy = 8; res(T);
    };
    img.src = LOGO;
  });
}

// junta as peças de cada grupo (mesmo material) numa malha só: muito menos desenhos por quadro
export function mergeChildren(root) {
  const visit = (node) => {
    node.children.slice().forEach(visit);
    const groups = new Map();
    node.children.forEach(c => {
      if (!c.isMesh || c.isInstancedMesh || c.isSkinnedMesh || c.userData.keep || c.renderOrder !== 0 || Array.isArray(c.material) || !c.visible || c.children.length) return;
      const g = c.geometry; if (!g || g.morphAttributes.position || !g.attributes.normal || !g.attributes.uv) return;
      const k = c.material.uuid + (g.index ? 'i' : 'n');
      if (!groups.has(k)) groups.set(k, []); groups.get(k).push(c);
    });
    groups.forEach(list => {
      if (list.length < 2) return;
      const geos = list.map(c => { c.updateMatrix(); const g = c.geometry.clone(); g.applyMatrix4(c.matrix); for (const n of Object.keys(g.attributes)) if (n !== 'position' && n !== 'normal' && n !== 'uv') g.deleteAttribute(n); return g; });
      const merged = mergeGeometries(geos, false); geos.forEach(g => g.dispose()); if (!merged) return;
      const m = new THREE.Mesh(merged, list[0].material); m.userData = Object.assign({}, list[0].userData);
      list.forEach(c => node.remove(c)); node.add(m);
    });
  };
  visit(root);
}
// sombra falsa (mancha suave no chão)
let blobMat = null;
export function blob(parent, x, z, rx, rz = rx, op = 0.35) {
  if (!blobMat) { const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d'); const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, 'rgba(0,0,0,1)'); gr.addColorStop(0.5, 'rgba(0,0,0,.55)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(0, 0, 128, 128); const t = new THREE.CanvasTexture(c); blobMat = new THREE.MeshBasicMaterial({ map: t, transparent: true, depthWrite: false, opacity: 0.35 }); }
  const m = new THREE.Mesh(new THREE.PlaneGeometry(rx * 2, rz * 2), op === 0.35 ? blobMat : Object.assign(blobMat.clone(), { opacity: op }));
  m.rotation.x = -Math.PI / 2; m.position.set(x, 0.011, z); m.renderOrder = 1; parent.add(m); return m;
}

// cenário parado vira 3 malhas (metal, brilhante, fosco) com cor por vértice
const SHARED = {
  metal: new THREE.MeshStandardMaterial({ vertexColors: true, metalness: 1, roughness: 0.3 }),
  gloss: new THREE.MeshStandardMaterial({ vertexColors: true, metalness: 0.05, roughness: 0.22 }),
  matte: new THREE.MeshStandardMaterial({ vertexColors: true, metalness: 0, roughness: 0.75 }),
};
const isEmissive = m => m.emissive && m.emissive.getHex() !== 0 && m.emissiveIntensity > 0;
export function bakeStatic(group) {
  group.updateMatrixWorld(true);
  const inv = new THREE.Matrix4().copy(group.matrixWorld).invert();
  const buckets = { metal: [], gloss: [], matte: [] }, remove = []; let ud = null;
  group.traverse(o => {
    if (!o.isMesh || o.isSkinnedMesh || o.isInstancedMesh || o.userData.keep || o.renderOrder !== 0 || o.children.length || !o.visible) return;
    for (let a = o.parent; a && a !== group; a = a.parent) { if (a.userData.dyn || !a.visible) return; }
    const m = o.material; if (Array.isArray(m) || !m.isMeshStandardMaterial || m.map || m.transparent || m.vertexColors || isEmissive(m)) return;
    let g = o.geometry.index ? o.geometry.toNonIndexed() : o.geometry.clone();
    for (const n of Object.keys(g.attributes)) if (n !== 'position' && n !== 'normal') g.deleteAttribute(n);
    g.applyMatrix4(new THREE.Matrix4().multiplyMatrices(inv, o.matrixWorld));
    const c = m.color, cnt = g.attributes.position.count, cols = new Float32Array(cnt * 3);
    for (let i = 0; i < cnt; i++) { cols[i * 3] = c.r; cols[i * 3 + 1] = c.g; cols[i * 3 + 2] = c.b; }
    g.setAttribute('color', new THREE.BufferAttribute(cols, 3));
    buckets[m.metalness >= 0.5 ? 'metal' : m.roughness < 0.32 ? 'gloss' : 'matte'].push(g); remove.push(o); if (!ud) ud = o.userData;
  });
  remove.forEach(o => o.parent.remove(o));
  for (const k in buckets) {
    if (!buckets[k].length) continue;
    const merged = mergeGeometries(buckets[k], false); buckets[k].forEach(g => g.dispose()); if (!merged) continue;
    const mm = new THREE.Mesh(merged, SHARED[k]); if (ud) mm.userData = Object.assign({}, ud); group.add(mm);
  }
}
// pessoa inteira vira 1 malha com esqueleto (cada articulação = 1 osso)
const SKIN_MAT = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.6, metalness: 0 });
export function bakeSkinned(root) {
  root.updateMatrixWorld(true);
  const inv = new THREE.Matrix4().copy(root.matrixWorld).invert();
  const bones = []; root.traverse(o => { if (o.isBone) bones.push(o); });
  const idx = new Map(bones.map((b, i) => [b, i]));
  const geos = [], remove = []; let ud = null;
  root.traverse(o => {
    if (!o.isMesh || o.isSkinnedMesh || o.children.length) return;
    let b = o.parent; while (b && !b.isBone) b = b.parent; if (!b) return;
    const m = o.material; if (Array.isArray(m) || m.map || m.transparent) return;
    let g = o.geometry.index ? o.geometry.toNonIndexed() : o.geometry.clone();
    for (const n of Object.keys(g.attributes)) if (n !== 'position' && n !== 'normal') g.deleteAttribute(n);
    g.applyMatrix4(new THREE.Matrix4().multiplyMatrices(inv, o.matrixWorld));
    const cnt = g.attributes.position.count, cols = new Float32Array(cnt * 3), si = new Uint16Array(cnt * 4), sw = new Float32Array(cnt * 4), bi = idx.get(b);
    const c = m.color.clone(); if (m.metalness >= 0.5) c.multiplyScalar(0.85);
    for (let i = 0; i < cnt; i++) { cols[i * 3] = c.r; cols[i * 3 + 1] = c.g; cols[i * 3 + 2] = c.b; si[i * 4] = bi; sw[i * 4] = 1; }
    g.setAttribute('color', new THREE.BufferAttribute(cols, 3)); g.setAttribute('skinIndex', new THREE.Uint16BufferAttribute(si, 4)); g.setAttribute('skinWeight', new THREE.Float32BufferAttribute(sw, 4));
    geos.push(g); remove.push(o); if (!ud) ud = o.userData;
  });
  remove.forEach(o => o.parent.remove(o));
  const merged = mergeGeometries(geos, false); geos.forEach(g => g.dispose());
  const sk = new THREE.SkinnedMesh(merged, SKIN_MAT); sk.frustumCulled = false; if (ud) sk.userData = Object.assign({}, ud);
  root.add(sk); root.updateMatrixWorld(true); sk.bind(new THREE.Skeleton(bones), sk.matrixWorld);
  return sk;
}
