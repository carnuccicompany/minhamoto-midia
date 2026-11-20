import * as THREE from 'three';
import { M, mat, mesh, box, rbox, cyl, sph, tex, goldGrad } from './util.js';

// Estoque dos diretores: frigobar (bebidas geladas) e armário de vitrine (charutos, relógios, perfumes).
// Sem logos nem rótulos de marca: as marcas aparecem só no painel do Estoque.
const blackGloss = mat(0x0b0b0c, { roughness: 0.2 });
const walnut = mat(0x3a2416, { roughness: 0.42 });
const walnutDark = mat(0x24160c, { roughness: 0.5 });
const steel = mat(0xc9ccd1, { metalness: 1, roughness: 0.25 });
const glassM = new THREE.MeshPhysicalMaterial({ color: 0xffffff, transparent: true, opacity: 0.1, roughness: 0.02 });
const glow = new THREE.MeshBasicMaterial({ color: 0x4a3a26 });
const ledM = new THREE.MeshBasicMaterial({ color: 0xffd9a0 });

function plaque(g, text, y, z, w = 0.62) {
  const t = tex(768, 96, (c, W, H) => { c.fillStyle = goldGrad(c, W, H); c.fillRect(0, 0, W, H); c.fillStyle = '#24160a'; c.font = '700 46px "Cormorant Garamond", Georgia, serif'; c.textAlign = 'center'; c.fillText(text.toUpperCase(), W / 2, 63); });
  mesh(new THREE.PlaneGeometry(w, w * 0.125), new THREE.MeshBasicMaterial({ map: t }), g, [0, y, z], null, false);
}

function champagne(g, x, y, z) {
  const gm = mat(0x0f2a1a, { roughness: 0.12 });
  mesh(cyl(0.042, 0.042, 0.2, 16), gm, g, [x, y + 0.1, z]);
  mesh(cyl(0.016, 0.042, 0.08, 16), gm, g, [x, y + 0.24, z]);
  mesh(cyl(0.018, 0.018, 0.06, 12), M.gold, g, [x, y + 0.3, z]);
  mesh(cyl(0.0425, 0.0425, 0.05, 16), mat(0xe9dfc8, { roughness: 0.5 }), g, [x, y + 0.11, z], null, false);
}
function tequila(g, x, y, z) {
  const gm = new THREE.MeshPhysicalMaterial({ color: 0xc98a3a, transparent: true, opacity: 0.85, roughness: 0.05 });
  mesh(rbox(0.07, 0.24, 0.07, 0.01), gm, g, [x, y + 0.12, z]);
  mesh(cyl(0.012, 0.016, 0.05, 10), gm, g, [x, y + 0.265, z]);
  mesh(cyl(0.02, 0.02, 0.035, 12), walnut, g, [x, y + 0.3, z]);
}
function cupStack(g, x, y, z) {
  for (let i = 0; i < 3; i++) mesh(cyl(0.03, 0.025, 0.05, 14), mat(0xf5f1ea, { roughness: 0.3 }), g, [x + i * 0.07, y + 0.025, z]);
}

export function buildStock(scene) {
  // ---------- frigobar (ao lado da adega, parede oeste) ----------
  const fr = new THREE.Group(); fr.position.set(-11.55, 0, 4.3); fr.rotation.y = Math.PI / 2; scene.add(fr);
  mesh(box(0.66, 0.92, 0.03), blackGloss, fr, [0, 0.46, -0.285]);
  [-0.315, 0.315].forEach(x => mesh(box(0.03, 0.92, 0.6), blackGloss, fr, [x, 0.46, 0]));
  mesh(box(0.66, 0.1, 0.6), blackGloss, fr, [0, 0.05, 0]); mesh(box(0.66, 0.04, 0.6), blackGloss, fr, [0, 0.9, 0]);
  [-0.3, 0.3].forEach(x => mesh(box(0.03, 0.86, 0.025), blackGloss, fr, [x, 0.47, 0.3]));
  mesh(box(0.66, 0.04, 0.025), blackGloss, fr, [0, 0.89, 0.3]); mesh(box(0.66, 0.1, 0.025), blackGloss, fr, [0, 0.05, 0.3]);
  mesh(box(0.56, 0.78, 0.01), glow, fr, [0, 0.48, -0.27], null, false);
  [0.1, 0.5].forEach(y => { mesh(box(0.56, 0.01, 0.5), steel, fr, [0, y, 0]); mesh(box(0.54, 0.008, 0.008), ledM, fr, [0, y + 0.25, 0.24], null, false); });
  champagne(fr, -0.17, 0.11, 0); champagne(fr, -0.06, 0.11, 0);
  tequila(fr, 0.07, 0.11, 0); tequila(fr, 0.17, 0.11, 0);
  cupStack(fr, -0.2, 0.51, 0.05);
  for (let i = 0; i < 4; i++) mesh(cyl(0.028, 0.028, 0.16, 12), new THREE.MeshPhysicalMaterial({ color: 0xbfe3ff, transparent: true, opacity: 0.6, roughness: 0.05 }), fr, [0.06 + i * 0.065, 0.59, 0]);
  mesh(new THREE.PlaneGeometry(0.62, 0.86), glassM, fr, [0, 0.47, 0.305], null, false);
  mesh(box(0.66, 0.025, 0.62), M.gold, fr, [0, 0.93, 0], null, false);
  mesh(box(0.025, 0.5, 0.03), M.gold, fr, [0.27, 0.5, 0.32], null, false);
  // tampo de mármore com balde de gelo e taças
  mesh(cyl(0.11, 0.09, 0.2, 20), steel, fr, [-0.12, 1.04, 0]);
  champagne(fr, -0.12, 0.98, 0);
  [0.1, 0.2].forEach(x => { const gm = new THREE.MeshPhysicalMaterial({ color: 0xffffff, transparent: true, opacity: 0.35, roughness: 0.05 }); mesh(cyl(0.03, 0.006, 0.09, 14), gm, fr, [x, 1.05, 0.05]); mesh(cyl(0.004, 0.004, 0.08, 6), gm, fr, [x, 0.97, 0.05]); mesh(cyl(0.03, 0.03, 0.004, 14), gm, fr, [x, 0.935, 0.05]); });
  plaque(fr, 'Frigobar', 0.82, 0.31, 0.3);

  // ---------- armário dos diretores (vitrine) ----------
  const ar = new THREE.Group(); ar.position.set(-11.68, 0, 0.5); ar.rotation.y = Math.PI / 2; scene.add(ar);
  const W = 2.2, H = 3.2, D = 0.5;
  mesh(box(W, H, 0.04), walnutDark, ar, [0, H / 2, -D / 2]);
  [-W / 2, W / 2].forEach(x => mesh(box(0.05, H, D), walnut, ar, [x, H / 2, 0]));
  mesh(box(W, 0.06, D), walnut, ar, [0, H, 0]);
  mesh(box(W - 0.06, 1.0, D), walnut, ar, [0, 0.5, 0]); // base fechada
  [-0.53, 0.53].forEach(x => { mesh(box(1.02, 0.9, 0.02), walnutDark, ar, [x, 0.52, D / 2 + 0.005]); mesh(box(0.02, 0.3, 0.03), M.gold, ar, [x + (x < 0 ? 0.42 : -0.42), 0.6, D / 2 + 0.03], null, false); });
  mesh(box(W, 0.03, D + 0.02), M.gold, ar, [0, 1.01, 0], null, false);
  mesh(box(W + 0.02, 0.03, D + 0.02), M.gold, ar, [0, H + 0.03, 0], null, false);
  mesh(box(W - 0.1, H - 1.1, 0.01), glow, ar, [0, 2.07, -D / 2 + 0.025], null, false);
  const shelfY = [1.04, 1.76, 2.48];
  shelfY.forEach(y => { mesh(box(W - 0.1, 0.02, D - 0.06), mat(0xffffff, { roughness: 0.05 }), ar, [0, y, 0], null, false); mesh(box(W - 0.14, 0.008, 0.008), ledM, ar, [0, y + 0.68, D / 2 - 0.05], null, false); });
  // prateleira 1: umidor com charutos + caixas de charuto
  const y1 = shelfY[0] + 0.01;
  mesh(box(0.62, 0.16, 0.34), walnut, ar, [-0.6, y1 + 0.08, 0]);
  mesh(box(0.58, 0.01, 0.3), mat(0x6b4a2a, { roughness: 0.6 }), ar, [-0.6, y1 + 0.155, 0], null, false);
  for (let r = 0; r < 2; r++) for (let i = 0; i < 9; i++) mesh(cyl(0.012, 0.012, 0.26, 8), mat([0x5a3a20, 0x6e4626][(r + i) % 2], { roughness: 0.8 }), ar, [-0.84 + i * 0.06, y1 + 0.172 + r * 0.02, 0.02 - r * 0.05], [Math.PI / 2, 0, 0]);
  mesh(new THREE.PlaneGeometry(0.6, 0.32), glassM, ar, [-0.6, y1 + 0.3, -0.08], [-1.2, 0, 0], false);
  mesh(box(0.62, 0.02, 0.02), M.gold, ar, [-0.6, y1 + 0.16, 0.17], null, false);
  [[0.15, 0x3a1d10], [0.55, 0x20120a]].forEach(([x, c], k) => { for (let s = 0; s < 3 - k; s++) { mesh(box(0.34, 0.07, 0.24), mat(c, { roughness: 0.5 }), ar, [x, y1 + 0.035 + s * 0.075, 0], [0, (s % 2) * 0.06, 0]); mesh(box(0.345, 0.012, 0.245), M.gold, ar, [x, y1 + 0.05 + s * 0.075, 0], [0, (s % 2) * 0.06, 0], false); } });
  mesh(box(0.14, 0.04, 0.14), mat(0x1a1a1a, { roughness: 0.3 }), ar, [0.88, y1 + 0.02, 0.05]); // cinzeiro
  mesh(cyl(0.06, 0.06, 0.02, 20), M.gold, ar, [0.88, y1 + 0.05, 0.05]);
  // prateleira 2: relógios nos expositores
  const y2 = shelfY[1] + 0.01;
  for (let i = 0; i < 5; i++) {
    const x = -0.8 + i * 0.4;
    mesh(rbox(0.16, 0.12, 0.14, 0.02), mat(0x141414, { roughness: 0.6 }), ar, [x, y2 + 0.06, 0]);
    mesh(new THREE.TorusGeometry(0.045, 0.012, 8, 24), [steel, M.gold][i % 2], ar, [x, y2 + 0.15, 0.03]);
    mesh(cyl(0.036, 0.036, 0.008, 24), mat([0x0a0a0a, 0x0d2a1a, 0x0b1e3d][i % 3], { roughness: 0.15 }), ar, [x, y2 + 0.15, 0.035], [Math.PI / 2, 0, 0]);
    mesh(new THREE.TorusGeometry(0.038, 0.006, 6, 24), [M.gold, steel][i % 2], ar, [x, y2 + 0.15, 0.042], null, false);
  }
  // prateleira 3: perfumes e canetas
  const y3 = shelfY[2] + 0.01;
  for (let i = 0; i < 4; i++) {
    const x = -0.8 + i * 0.22;
    mesh(rbox(0.08, 0.16, 0.05, 0.008), new THREE.MeshPhysicalMaterial({ color: [0x111111, 0x2a3a2a, 0x1a1a24, 0x3a2a14][i], transparent: true, opacity: 0.9, roughness: 0.05 }), ar, [x, y3 + 0.08, 0]);
    mesh(cyl(0.022, 0.022, 0.05, 14), [steel, M.gold][i % 2], ar, [x, y3 + 0.185, 0]);
  }
  mesh(box(0.5, 0.05, 0.22), walnut, ar, [0.45, y3 + 0.025, 0]);
  for (let i = 0; i < 4; i++) { mesh(cyl(0.008, 0.008, 0.14, 10), blackGloss, ar, [0.3 + i * 0.1, y3 + 0.06, 0], [0, 0, Math.PI / 2]); mesh(cyl(0.0085, 0.0085, 0.03, 10), M.gold, ar, [0.24 + i * 0.1, y3 + 0.06, 0], [0, 0, Math.PI / 2], false); }
  mesh(sph(0.07, 16, 12), M.gold, ar, [0.9, y3 + 0.07, 0]);
  // portas de vidro
  [-W / 4, W / 4].forEach(x => { mesh(new THREE.PlaneGeometry(W / 2 - 0.04, H - 1.06), glassM, ar, [x, 2.07, D / 2], null, false); mesh(box(0.02, 0.4, 0.03), M.gold, ar, [x + (x < 0 ? W / 4 - 0.06 : -W / 4 + 0.06), 2.0, D / 2 + 0.02], null, false); });
  plaque(ar, 'Armário dos Diretores', 0.92, D / 2 + 0.02, 0.7);

  fr.traverse(o => { if (o.isMesh) o.userData.stock = 'frigobar'; });
  ar.traverse(o => { if (o.isMesh) o.userData.stock = 'armario'; });
  return { fr, ar };
}
