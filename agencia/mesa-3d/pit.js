import * as THREE from 'three';
import { M, mat, phys, mesh, box, rbox, cyl, sph, tex, goldGrad, marbleTex } from './util.js';
import { PIT, ROOM } from './env.js';

// Fosso de pôquer: rebaixado no chão, banco curvo de couro conhaque em volta, mesa de feltro verde no centro,
// degraus de mármore preto virados pra mesa dos diretores e um pendente dourado em cima.
export function buildPit(scene) {
  const g = new THREE.Group(); g.position.set(PIT.x, 0, PIT.z); scene.add(g);
  const R = PIT.R, D = PIT.D, ENTRY = Math.PI, GAP = 0.42; // entrada virada pra oeste (pra mesa)
  const bm = phys(0xffffff, { map: marbleTex('#0e0e0f', 'rgba(220,220,220,A)', 18, 512, [2, 1]), roughness: 0.14, clearcoat: 1 });
  // parede interna, chão do fosso e borda
  const wall = mesh(new THREE.CylinderGeometry(R, R, D, 72, 1, true), new THREE.MeshStandardMaterial({ color: 0x1a120c, roughness: 0.4, side: THREE.BackSide }), g, [0, -D / 2, 0], null, false);
  const carpetT = tex(1024, 1024, (c, w, h) => { c.fillStyle = '#0d0b0b'; c.fillRect(0, 0, w, h); for (let i = 0; i < 30000; i++) { c.fillStyle = `rgba(${Math.random() < .5 ? '255,255,255' : '0,0,0'},${Math.random() * .04})`; c.fillRect(Math.random() * w, Math.random() * h, 2, 2); }
    c.strokeStyle = 'rgba(212,178,106,.55)'; c.lineWidth = 6; c.beginPath(); c.arc(w / 2, h / 2, w * 0.3, 0, 7); c.stroke(); c.lineWidth = 2; c.beginPath(); c.arc(w / 2, h / 2, w * 0.33, 0, 7); c.stroke(); });
  mesh(new THREE.CircleGeometry(R, 72), mat(0xffffff, { map: carpetT, roughness: 0.95 }), g, [0, -D + 0.001, 0], [-Math.PI / 2, 0, 0], false);
  mesh(new THREE.RingGeometry(R, R + 0.16, 96), bm, g, [0, 0.009, 0], [-Math.PI / 2, 0, 0], false);
  mesh(new THREE.TorusGeometry(R + 0.16, 0.012, 6, 128), M.gold, g, [0, 0.012, 0], [Math.PI / 2, 0, 0], false);
  mesh(new THREE.TorusGeometry(R, 0.016, 6, 128), M.gold, g, [0, 0.008, 0], [Math.PI / 2, 0, 0], false);
  mesh(new THREE.TorusGeometry(R - 0.012, 0.01, 6, 128), new THREE.MeshBasicMaterial({ color: 0xffd9a0, toneMapped: false }), g, [0, -0.045, 0], [Math.PI / 2, 0, 0], false); // fita de luz sob a borda
  // degraus (2) na entrada
  const stepAt = (r0, r1, top) => { const rm = (r0 + r1) / 2, x = Math.cos(ENTRY) * rm, z = Math.sin(ENTRY) * rm; const st = mesh(box(r1 - r0, top + D, 1.1), bm, g, [x, (top - D) / 2, z], [0, -ENTRY, 0], false); mesh(box(0.02, 0.012, 1.1), M.gold, g, [Math.cos(ENTRY) * (r0 + 0.01), top + 0.002, Math.sin(ENTRY) * (r0 + 0.01)], [0, -ENTRY, 0], false); return st; };
  stepAt(R - 0.34, R, -0.17); stepAt(R - 0.68, R - 0.34, -0.34);
  // banco curvo (setor de anel extrudado) com encosto
  const sector = (r0, r1, a0, a1) => { const s = new THREE.Shape(); s.absarc(0, 0, r1, a0, a1, false); s.absarc(0, 0, r0, a1, a0, true); s.closePath(); return s; };
  const leather = phys(0x6b3a1c, { roughness: 0.4, clearcoat: 0.5, sheen: 0.3 });
  const A0 = ENTRY + GAP, A1 = ENTRY - GAP + Math.PI * 2;
  const ext = (shape, depth, bevel) => new THREE.ExtrudeGeometry(shape, { depth, bevelEnabled: true, bevelSize: bevel, bevelThickness: bevel, bevelSegments: 3, curveSegments: 72 });
  // a forma fica em XY e é deitada: x→x, y→-z. Por isso os ângulos são espelhados (−a).
  const seat = mesh(ext(sector(R - 0.6, R - 0.02, -A1, -A0), D - 0.08, 0.035), leather, g, [0, -D, 0], [-Math.PI / 2, 0, 0]);
  const backR = mesh(ext(sector(R - 0.2, R - 0.02, -A1, -A0), 0.33, 0.04), leather, g, [0, -0.08, 0], [-Math.PI / 2, 0, 0]);
  // mesa de pôquer
  const TR = 1.05, TY = -D + 0.76;
  const t = new THREE.Group(); g.add(t);
  mesh(cyl(0.22, 0.42, 0.06, 40), M.gold, t, [0, -D + 0.03, 0]); mesh(cyl(0.12, 0.16, 0.66, 32), M.black, t, [0, -D + 0.38, 0]);
  mesh(cyl(TR, TR, 0.08, 72), phys(0x1b130e, { roughness: 0.3, clearcoat: 1 }), t, [0, TY - 0.04, 0]);
  const feltT = tex(1024, 1024, (c, w, h) => {
    const gr = c.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, w / 2); gr.addColorStop(0, '#1f6b42'); gr.addColorStop(0.7, '#124a2c'); gr.addColorStop(1, '#0a2e1b'); c.fillStyle = gr; c.fillRect(0, 0, w, h);
    for (let i = 0; i < 50000; i++) { c.fillStyle = `rgba(${Math.random() < .5 ? '255,255,255' : '0,0,0'},${Math.random() * .035})`; c.fillRect(Math.random() * w, Math.random() * h, 1.5, 1.5); }
    c.strokeStyle = 'rgba(232,200,120,.75)'; c.lineWidth = 5; c.beginPath(); c.arc(w / 2, h / 2, w * 0.36, 0, 7); c.stroke();
    c.fillStyle = 'rgba(232,200,120,.55)'; c.font = '600 54px "Cormorant Garamond", Georgia, serif'; c.textAlign = 'center'; c.fillText('C A R N U C C I', w / 2, h / 2 - 150); c.font = '600 30px Inter, Arial'; c.fillText('HIGH STAKES · SÓ ENTRE OS NOSSOS', w / 2, h / 2 + 175);
  });
  mesh(new THREE.CircleGeometry(TR - 0.1, 72), mat(0xffffff, { map: feltT, roughness: 1 }), t, [0, TY + 0.002, 0], [-Math.PI / 2, 0, 0], false);
  mesh(new THREE.TorusGeometry(TR - 0.03, 0.07, 14, 96), phys(0x0c0a09, { roughness: 0.35, clearcoat: 0.6 }), t, [0, TY + 0.02, 0], [Math.PI / 2, 0, 0]);
  mesh(new THREE.TorusGeometry(TR - 0.1, 0.008, 6, 96), M.gold, t, [0, TY + 0.006, 0], [Math.PI / 2, 0, 0], false);
  // fichas, cartas comunitárias e o pote
  const chipC = [0xb01c1c, 0x111111, 0x1c3fb0, 0xf2efe8, 0xc9a45c];
  const stack = (x, z, n, c0) => { for (let i = 0; i < n; i++) mesh(cyl(0.022, 0.022, 0.008, 16), mat(chipC[(c0 + (i > n * 0.6 ? 1 : 0)) % chipC.length], { roughness: 0.4 }), t, [x, TY + 0.006 + i * 0.0085, z], null, false); };
  [[0, 0.08, 9, 4], [0.06, 0.05, 6, 0], [-0.05, 0.11, 7, 2], [0.03, 0.15, 5, 1]].forEach(([x, z, n, c0]) => stack(x, z, n, c0));
  const cardT = tex(128, 180, (c, w, h) => { c.fillStyle = '#f7f3ea'; c.fillRect(0, 0, w, h); c.strokeStyle = '#c9a45c'; c.lineWidth = 4; c.strokeRect(6, 6, w - 12, h - 12); c.fillStyle = Math.random() < .5 ? '#b01c1c' : '#111'; c.font = '700 56px Georgia'; c.textAlign = 'center'; c.fillText(['A', 'K', 'Q', 'J', '10'][Math.floor(Math.random() * 5)], w / 2, h / 2 + 18); });
  const backT = tex(128, 180, (c, w, h) => { c.fillStyle = '#0d0d0d'; c.fillRect(0, 0, w, h); c.strokeStyle = '#c9a45c'; c.lineWidth = 3; c.strokeRect(8, 8, w - 16, h - 16); for (let i = 0; i < 12; i++) { c.beginPath(); c.moveTo(8, 8 + i * 15); c.lineTo(w - 8, 20 + i * 15); c.stroke(); } });
  for (let i = 0; i < 5; i++) mesh(new THREE.PlaneGeometry(0.06, 0.085), mat(0xffffff, { map: cardT, roughness: 0.6 }), t, [-0.14 + i * 0.07, TY + 0.004, -0.12], [-Math.PI / 2, 0, 0], false);
  mesh(rbox(0.08, 0.04, 0.11, 0.008), mat(0xffffff, { map: backT, roughness: 0.6 }), t, [0.3, TY + 0.02, -0.2], null, false); // baralho
  // pendente dourado + lavagem de luz no feltro
  const pend = new THREE.Group(); pend.position.set(0, ROOM.H, 0); g.add(pend);
  mesh(cyl(0.006, 0.006, ROOM.H - 1.9, 6), M.black, pend, [0, -(ROOM.H - 2.55) / 2, 0], null, false);
  mesh(cyl(0.62, 0.7, 0.22, 48, 1, true), new THREE.MeshStandardMaterial({ color: 0x0c0c0c, roughness: 0.3, side: THREE.DoubleSide }), pend, [0, -(ROOM.H - 2.55) - 0.11, 0], null, false);
  mesh(new THREE.TorusGeometry(0.7, 0.012, 6, 64), M.gold, pend, [0, -(ROOM.H - 2.55) - 0.22, 0], [Math.PI / 2, 0, 0], false);
  mesh(new THREE.CircleGeometry(0.66, 48), new THREE.MeshBasicMaterial({ color: 0xfff1d6, toneMapped: false }), pend, [0, -(ROOM.H - 2.55) - 0.2, 0], [Math.PI / 2, 0, 0], false);
  const washT = tex(256, 256, (c, w, h) => { const gr = c.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, w / 2); gr.addColorStop(0, 'rgba(255,230,180,.5)'); gr.addColorStop(0.6, 'rgba(255,230,180,.18)'); gr.addColorStop(1, 'rgba(255,230,180,0)'); c.fillStyle = gr; c.fillRect(0, 0, w, h); });
  const wash = mesh(new THREE.CircleGeometry(1.3, 48), new THREE.MeshBasicMaterial({ map: washT, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false }), g, [0, TY + 0.01, 0], [-Math.PI / 2, 0, 0], false); wash.renderOrder = 2; wash.userData.keep = true;

  // ---------- lugares e caminhos (mundo) ----------
  const C = new THREE.Vector3(PIT.x, 0, PIT.z);
  const SEATS = [0, 0.95, -0.95, 1.9, -1.9];
  const at = (a, r, y) => new THREE.Vector3(C.x + Math.cos(a) * r, y, C.z + Math.sin(a) * r);
  const out = { group: g, C, SEATS, TY };
  out.seat = i => { const a = SEATS[i]; return { pos: at(a, R - 0.5, -D), look: C.clone().setY(-D) }; };
  out.pathIn = i => {
    const a = SEATS[i], pts = [at(ENTRY, R + 0.2, 0), at(ENTRY, R - 0.17, -0.17), at(ENTRY, R - 0.51, -0.34), at(ENTRY, R - 0.82, -D)];
    const RW = 1.28, da = Math.atan2(Math.sin(a - ENTRY), Math.cos(a - ENTRY)), n = Math.max(1, Math.ceil(Math.abs(da) / 0.3));
    for (let k = 1; k <= n; k++) pts.push(at(ENTRY + da * k / n, RW, -D));
    pts.push(at(a, R - 0.62, -D)); return pts;
  };
  g.traverse(o => { if (o.isMesh) o.userData.keep = o.userData.keep || false; });
  return out;
}
