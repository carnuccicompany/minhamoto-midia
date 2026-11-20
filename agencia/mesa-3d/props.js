import * as THREE from 'three';
import { M, mat, phys, mesh, box, rbox, cyl, sph, tex, goldGrad } from './util.js';

export const smokeTex = tex(64, 64, (g) => { const gr = g.createRadialGradient(32, 32, 0, 32, 32, 32); gr.addColorStop(0, 'rgba(225,225,225,.55)'); gr.addColorStop(1, 'rgba(225,225,225,0)'); g.fillStyle = gr; g.fillRect(0, 0, 64, 64); });

export function screenCanvas(kind) {
  const c = document.createElement('canvas'); c.width = 512; c.height = 320; const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.generateMipmaps = false; t.minFilter = THREE.LinearFilter;
  const draw = (now) => {
    const g = c.getContext('2d'), w = 512, h = 320;
    g.fillStyle = '#0d1117'; g.fillRect(0, 0, w, h);
    g.fillStyle = '#161b22'; g.fillRect(0, 0, w, 26); [0xff5f57, 0xfebc2e, 0x28c840].forEach((cc, i) => { g.fillStyle = '#' + cc.toString(16); g.beginPath(); g.arc(14 + i * 16, 13, 5, 0, 7); g.fill(); });
    const sweep = (now * 0.4) % 1;
    if (kind === 'chart' || kind === 'money') {
      g.strokeStyle = '#21262d'; for (let i = 1; i < 6; i++) { g.beginPath(); g.moveTo(20, 30 + i * 46); g.lineTo(w - 20, 30 + i * 46); g.stroke(); }
      g.strokeStyle = kind === 'money' ? '#3ddc84' : '#58a6ff'; g.lineWidth = 4; g.beginPath();
      for (let i = 0; i <= 30; i++) { const x = 20 + i * 15.8, y = 270 - (i * 6 + Math.sin(i * 0.9 + now) * 12 + 20); i ? g.lineTo(x, y) : g.moveTo(x, y); } g.stroke();
      g.fillStyle = kind === 'money' ? '#3ddc84' : '#d4b26a'; g.font = '700 30px Inter, Arial'; g.fillText(kind === 'money' ? 'MRR' : 'Funil', 24, 64);
    } else if (kind === 'feed') {
      for (let i = 0; i < 9; i++) { g.fillStyle = ['#287af5', '#c6ff00', '#1f2937', '#d4b26a'][i % 4]; g.fillRect(24 + (i % 3) * 160, 40 + Math.floor(i / 3) * 92, 150, 84); }
    } else if (kind === 'timeline') {
      g.fillStyle = '#1f2937'; g.fillRect(20, 40, w - 40, 160); g.fillStyle = '#287af5'; g.fillRect(40, 60, 200, 120);
      for (let r = 0; r < 3; r++) for (let i = 0; i < 7; i++) { g.fillStyle = ['#d4b26a', '#58a6ff', '#3ddc84'][r]; g.fillRect(20 + i * 68, 220 + r * 30, 60, 22); }
      g.fillStyle = '#ff5a5f'; g.fillRect(20 + sweep * (w - 40), 210, 3, 100);
    } else if (kind === 'ads') {
      for (let i = 0; i < 6; i++) { const v = 0.3 + ((i * 37) % 60) / 100; g.fillStyle = i % 3 === 2 ? '#ff5a5f' : '#3ddc84'; g.fillRect(30 + i * 78, 290 - v * 220, 54, v * 220); }
    } else if (kind === 'radar') {
      g.strokeStyle = '#3ddc84'; g.lineWidth = 1.5; for (let r = 1; r <= 3; r++) { g.beginPath(); g.arc(256, 175, r * 45, 0, 7); g.stroke(); }
      g.beginPath(); g.moveTo(256, 175); g.lineTo(256 + Math.cos(now * 2) * 135, 175 + Math.sin(now * 2) * 135); g.stroke();
      g.fillStyle = '#ff5a5f'; [[310, 120], [200, 230], [330, 220]].forEach(([x, y]) => { g.beginPath(); g.arc(x, y, 6, 0, 7); g.fill(); });
    } else if (kind === 'flow') {
      g.fillStyle = '#287af5'; [[30, 60], [190, 60], [350, 60], [110, 190], [270, 190]].forEach(([x, y]) => g.fillRect(x, y, 130, 64));
      g.strokeStyle = '#c6ff00'; g.lineWidth = 4; g.beginPath(); g.moveTo(160, 92); g.lineTo(190, 92); g.moveTo(320, 92); g.lineTo(350, 92); g.moveTo(255, 124); g.lineTo(200, 190); g.stroke();
    } else if (kind === 'chat') {
      for (let i = 0; i < 6; i++) { g.fillStyle = i % 2 ? '#287af5' : '#30363d'; const ww = 160 + ((i * 53) % 140); g.fillRect(i % 2 ? w - 24 - ww : 24, 40 + i * 44, ww, 32); }
    } else if (kind === 'stars') {
      for (let r = 0; r < 4; r++) { for (let i = 0; i < 5; i++) { g.fillStyle = i < 5 - (r === 2 ? 1 : 0) ? '#febc2e' : '#30363d'; g.font = '28px Arial'; g.fillText('★', 30 + i * 30, 72 + r * 64); } g.fillStyle = '#30363d'; g.fillRect(200, 52 + r * 64, 280, 14); g.fillRect(200, 72 + r * 64, 200, 10); }
    }
    t.needsUpdate = true;
  };
  draw(0);
  return { tex: t, draw };
}

// MacBook (alumínio) — local: tela virada pra quem está em -Z do laptop
export function macbook(parent, x, z, rotY, kind) {
  const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = rotY; parent.add(g);
  mesh(rbox(0.31, 0.012, 0.215, 0.006), M.alu, g, [0, 0.006, 0]);
  mesh(box(0.27, 0.001, 0.1), M.black, g, [0, 0.0125, -0.025], null, false);
  mesh(box(0.1, 0.001, 0.065), mat(0x8e9095, { metalness: 0.8, roughness: 0.3 }), g, [0, 0.0125, -0.075 + 0.0], null, false);
  const hinge = new THREE.Group(); hinge.position.set(0, 0.012, 0.105); hinge.rotation.x = -0.32; g.add(hinge);
  mesh(rbox(0.31, 0.205, 0.006, 0.006), M.alu, hinge, [0, 0.1025, 0]);
  const scr = screenCanvas(kind);
  mesh(new THREE.PlaneGeometry(0.29, 0.18), new THREE.MeshBasicMaterial({ map: scr.tex, toneMapped: false }), hinge, [0, 0.105, -0.0035], [0, Math.PI, 0], false);
  return { group: g, draw: scr.draw };
}

export function glassOf(kind) {
  const g = new THREE.Group();
  if (kind === 'whisky') {
    mesh(cyl(0.04, 0.036, 0.09, 24), M.glass, g, [0, 0.045, 0], null, false);
    g.userData.liquid = mesh(cyl(0.035, 0.032, 0.04, 12), M.amber, g, [0, 0.025, 0], null, false); g.userData.liquid.userData.keep = true;
    mesh(box(0.03, 0.03, 0.03), M.ice, g, [0.005, 0.045, 0.004], [0.3, 0.5, 0.2], false);
  } else if (kind === 'agua') {
    mesh(cyl(0.035, 0.03, 0.12, 24), M.glass, g, [0, 0.06, 0], null, false);
    g.userData.liquid = mesh(cyl(0.031, 0.028, 0.08, 12), M.water, g, [0, 0.042, 0], null, false); g.userData.liquid.userData.keep = true;
  } else {
    mesh(cyl(0.032, 0.026, 0.055, 20), M.porcelain, g, [0, 0.028, 0]);
    g.userData.liquid = mesh(cyl(0.029, 0.029, 0.004, 12), M.coffee, g, [0, 0.052, 0], null, false); g.userData.liquid.userData.keep = true;
    mesh(new THREE.TorusGeometry(0.015, 0.005, 8, 16), M.porcelain, g, [0.037, 0.03, 0], [0, 0, Math.PI / 2]);
  }
  return g;
}
export function cigar() {
  const g = new THREE.Group();
  mesh(cyl(0.011, 0.011, 0.15, 12), M.cigar, g, [0, 0, 0], [0, 0, Math.PI / 2]);
  mesh(cyl(0.0115, 0.0115, 0.016, 12), M.gold, g, [0.045, 0, 0], [0, 0, Math.PI / 2], false);
  g.userData.tip = mesh(sph(0.0115, 10, 8), M.ember, g, [-0.076, 0, 0], null, false);
  return g;
}
export function phone(white) {
  const g = new THREE.Group();
  mesh(rbox(0.072, 0.008, 0.15, 0.004), white ? M.porcelain : M.black, g, [0, 0.004, 0]);
  const s = tex(128, 256, (c, w, h) => { c.fillStyle = '#0d1117'; c.fillRect(0, 0, w, h); for (let i = 0; i < 5; i++) { c.fillStyle = i % 2 ? '#287af5' : '#c6ff00'; c.fillRect(10, 20 + i * 44, w - 20 - (i % 2) * 40, 30); } });
  mesh(new THREE.PlaneGeometry(0.064, 0.14), new THREE.MeshBasicMaterial({ map: s, toneMapped: false }), g, [0, 0.0085, 0], [-Math.PI / 2, 0, 0], false);
  return g;
}

export const tableProps = {
  espresso(p, x, z) { const g = glassOf('cafe'); g.position.set(x, 0, z); p.add(g); mesh(cyl(0.06, 0.055, 0.01, 24), M.porcelain, g, [0, 0.005, 0]); g.children.slice(0, -1).forEach(o => { if (o.position.y < 0.01) return; o.position.y += 0.01; }); return g; },
  whisky(p, x, z) { const g = glassOf('whisky'); g.position.set(x, 0, z); p.add(g); return g; },
  agua(p, x, z) { const g = glassOf('agua'); g.position.set(x, 0, z); p.add(g); return g; },
  cigar(p, x, z) {
    const g = new THREE.Group(); g.position.set(x, 0, z); p.add(g);
    mesh(cyl(0.075, 0.065, 0.026, 32), phys(0x18181c, { roughness: 0.1, metalness: 0.4, clearcoat: 1 }), g, [0, 0.013, 0]);
    mesh(cyl(0.05, 0.05, 0.004, 24), mat(0x6e6a64, { roughness: 1 }), g, [0, 0.027, 0], null, false);
    const c = cigar(); c.position.set(0.03, 0.035, 0); c.rotation.z = -0.1; g.add(c); g.userData.cig = c; return g;
  },
  money(p, x, z) {
    const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = 0.3; p.add(g);
    const stack = (sx, sz, n, r) => { for (let i = 0; i < n; i++) { const b = mesh(box(0.165, 0.026, 0.075), M.cash, g, [sx, 0.013 + i * 0.027, sz], [0, r + (Math.random() - .5) * 0.06, 0]); mesh(box(0.028, 0.028, 0.077), M.band, b, [0, 0, 0], null, false); } };
    stack(0, 0, 5, 0); stack(0.17, 0.01, 3, 0.1); stack(0.08, 0.09, 2, -0.15); return g;
  },
  phone(p, x, z) { const g = phone(false); g.position.set(x, 0, z); g.rotation.y = 0.4; p.add(g); return g; },
  phone2(p, x, z) { const a = phone(false), b = phone(true); a.position.set(x - 0.05, 0, z); b.position.set(x + 0.06, 0, z + 0.03); a.rotation.y = 0.2; b.rotation.y = -0.2; p.add(a, b); return a; },
  tablet(p, x, z) {
    const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = 0.2; p.add(g);
    mesh(rbox(0.25, 0.008, 0.18, 0.008), M.black, g, [0, 0.004, 0]);
    const s = screenCanvas('flow'); mesh(new THREE.PlaneGeometry(0.23, 0.16), new THREE.MeshBasicMaterial({ map: s.tex, toneMapped: false }), g, [0, 0.0085, 0], [-Math.PI / 2, 0, Math.PI], false); return g;
  },
  notepad(p, x, z) {
    const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = -0.25; p.add(g);
    const t = tex(200, 280, (c, w, h) => { c.fillStyle = '#f1ead8'; c.fillRect(0, 0, w, h); c.strokeStyle = '#333'; c.lineWidth = 3; [[15, 20], [105, 20], [15, 110], [105, 110], [15, 200], [105, 200]].forEach(([x, y]) => c.strokeRect(x, y, 80, 70)); c.strokeStyle = '#c33'; c.beginPath(); c.moveTo(30, 60); c.lineTo(80, 40); c.stroke(); });
    mesh(rbox(0.2, 0.012, 0.28, 0.004), M.porcelain, g, [0, 0.006, 0]);
    mesh(new THREE.PlaneGeometry(0.19, 0.27), mat(0xffffff, { map: t, roughness: 0.9 }), g, [0, 0.0125, 0], [-Math.PI / 2, 0, Math.PI], false); return g;
  },
  newspaper(p, x, z) { const g = newspaper(); g.position.set(x, 0.004, z); g.rotation.set(-Math.PI / 2, 0, 0.4); p.add(g); return g; },
  calculator(p, x, z) {
    const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = 0.2; p.add(g);
    const t = tex(90, 140, (c, w, h) => { c.fillStyle = '#1a1a1a'; c.fillRect(0, 0, w, h); c.fillStyle = '#9fbf8a'; c.fillRect(8, 8, w - 16, 30); for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) { c.fillStyle = j === 3 ? '#c9a45c' : '#555'; c.fillRect(10 + j * 19, 48 + i * 22, 15, 16); } });
    mesh(rbox(0.09, 0.016, 0.14, 0.005), M.black, g, [0, 0.008, 0]);
    mesh(new THREE.PlaneGeometry(0.085, 0.135), mat(0xffffff, { map: t }), g, [0, 0.0165, 0], [-Math.PI / 2, 0, Math.PI], false); return g;
  },
};
export function newspaper(title = 'MERCADO') {
  const t = tex(300, 220, (c, w, h) => { c.fillStyle = title === 'CONTRATO' ? '#f4f1ea' : '#e4dfd2'; c.fillRect(0, 0, w, h); c.fillStyle = '#222'; c.font = '700 26px Georgia'; c.fillText(title, 14, 34); c.fillRect(14, 44, w - 28, 3); for (let i = 0; i < 14; i++) c.fillRect(14 + (i % 2) * 140, 60 + Math.floor(i / 2) * 22, 126, 6); });
  return new THREE.Mesh(new THREE.PlaneGeometry(0.34, 0.25), new THREE.MeshStandardMaterial({ map: t, roughness: 1, side: THREE.DoubleSide }));
}

// poltrona de diretor (local: pessoa olha pra +Z)
export function chair(plateTexture) {
  const c = new THREE.Group();
  mesh(rbox(0.58, 0.13, 0.56, 0.05, 3), M.leather, c, [0, 0.47, 0]);
  const back = new THREE.Group(); back.position.set(0, 0.55, -0.28); back.rotation.x = -0.1; c.add(back);
  mesh(rbox(0.6, 0.8, 0.11, 0.05, 3), M.leather, back, [0, 0.4, 0]);
  for (let i = 0; i < 4; i++) mesh(box(0.54, 0.006, 0.004), M.leatherDark, back, [0, 0.12 + i * 0.16, 0.056], null, false);
  mesh(rbox(0.62, 0.04, 0.13, 0.015), M.gold, back, [0, 0.81, 0]);
  if (plateTexture) {
    mesh(rbox(0.5, 0.15, 0.012, 0.004), M.gold, back, [0, 0.62, -0.06], null, false);
    mesh(new THREE.PlaneGeometry(0.48, 0.135), new THREE.MeshBasicMaterial({ map: plateTexture }), back, [0, 0.62, -0.067], [0, Math.PI, 0], false);
  }
  [-1, 1].forEach(s => { mesh(rbox(0.07, 0.05, 0.46, 0.02), M.leatherDark, c, [s * 0.33, 0.7, 0.02]); mesh(box(0.025, 0.2, 0.025), M.chrome, c, [s * 0.33, 0.58, 0.08]); });
  mesh(cyl(0.032, 0.032, 0.36, 12), M.chrome, c, [0, 0.24, 0]);
  for (let i = 0; i < 5; i++) { const a = i * Math.PI * 2 / 5; mesh(box(0.045, 0.03, 0.33), M.chrome, c, [Math.sin(a) * 0.16, 0.055, Math.cos(a) * 0.16], [0, a, 0]); mesh(sph(0.028, 8, 6), M.black, c, [Math.sin(a) * 0.31, 0.028, Math.cos(a) * 0.31]); }
  return c;
}
// trono do Léo e do Davi
export function throne(plateTexture) {
  const c = new THREE.Group();
  const cream = mat(0x0f0c0a, { roughness: 0.35 });
  mesh(rbox(0.82, 0.16, 0.72, 0.06, 4), cream, c, [0, 0.47, 0]);
  const back = new THREE.Group(); back.position.set(0, 0.55, -0.36); back.rotation.x = -0.08; c.add(back);
  mesh(rbox(0.86, 1.3, 0.14, 0.06, 4), cream, back, [0, 0.65, 0]);
  for (let i = 0; i < 6; i++) for (let j = 0; j < 4; j++) mesh(sph(0.012, 8, 6), M.gold, back, [-0.27 + j * 0.18, 0.15 + i * 0.2, 0.072], null, false);
  mesh(new THREE.TorusGeometry(0.44, 0.02, 10, 40, Math.PI), M.gold, back, [0, 1.28, 0], null, false);
  mesh(rbox(0.9, 0.05, 0.16, 0.02), M.gold, back, [0, 1.3, 0]);
  if (plateTexture) {
    mesh(rbox(0.6, 0.18, 0.014, 0.005), M.gold, back, [0, 1.05, -0.075], null, false);
    mesh(new THREE.PlaneGeometry(0.58, 0.16), new THREE.MeshBasicMaterial({ map: plateTexture }), back, [0, 1.05, -0.083], [0, Math.PI, 0], false);
  }
  [-1, 1].forEach(s => { mesh(rbox(0.12, 0.34, 0.7, 0.05, 4), cream, c, [s * 0.45, 0.62, 0]); mesh(rbox(0.13, 0.03, 0.72, 0.01), M.gold, c, [s * 0.45, 0.8, 0]); });
  mesh(rbox(0.86, 0.36, 0.74, 0.04), M.goldDim, c, [0, 0.2, 0]);
  return c;
}

export function plateTex(nome, linha2) {
  return tex(1024, 290, (g, w, h) => {
    g.fillStyle = goldGrad(g, w, h); g.fillRect(0, 0, w, h);
    g.strokeStyle = '#5e4218'; g.lineWidth = 8; g.strokeRect(16, 16, w - 32, h - 32); g.lineWidth = 2; g.strokeRect(30, 30, w - 60, h - 60);
    g.fillStyle = '#24160a'; g.textAlign = 'center';
    let fs = 104; g.font = `700 ${fs}px "Cormorant Garamond", Georgia, serif`;
    while (g.measureText(nome.toUpperCase()).width > w - 120) { fs -= 4; g.font = `700 ${fs}px "Cormorant Garamond", Georgia, serif`; }
    g.fillText(nome.toUpperCase(), w / 2, linha2 ? 152 : 180);
    if (linha2) { g.font = '600 44px Inter, Arial, sans-serif'; g.fillText(linha2.toUpperCase(), w / 2, 228); }
  });
}
