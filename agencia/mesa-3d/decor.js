import * as THREE from 'three';
import { M, mat, mesh, box, rbox, cyl, sph, tex, goldGrad, marbleTex } from './util.js';

const bronze = mat(0x7a5530, { metalness: 1, roughness: 0.35 });
const walnut = mat(0x3a2416, { roughness: 0.45 });
const blackM = mat(0x111112, { roughness: 0.25 });
const ivory = mat(0xf1ece2, { roughness: 0.35 });

function pedestal(g, h = 0.9, w = 0.55) {
  mesh(box(w, h, w), blackM, g, [0, h / 2, 0]);
  mesh(box(w + 0.04, 0.03, w + 0.04), M.gold, g, [0, h, 0]);
  mesh(box(w + 0.04, 0.03, w + 0.04), M.gold, g, [0, 0.015, 0]);
  return h;
}
function plaque(g, text, y, z) {
  const t = tex(512, 96, (c, w, h) => { c.fillStyle = goldGrad(c, w, h); c.fillRect(0, 0, w, h); c.fillStyle = '#24160a'; c.font = '700 44px "Cormorant Garamond", Georgia, serif'; c.textAlign = 'center'; c.fillText(text.toUpperCase(), w / 2, 62); });
  mesh(new THREE.PlaneGeometry(0.36, 0.068), new THREE.MeshBasicMaterial({ map: t }), g, [0, y, z], null, false);
}

const B = {
  enigma(g) {
    const y = pedestal(g, 0.9);
    mesh(box(0.42, 0.14, 0.34), walnut, g, [0, y + 0.07, 0]);
    const lid = mesh(box(0.42, 0.02, 0.3), walnut, g, [0, y + 0.22, -0.2], [-1.1, 0, 0]);
    mesh(box(0.38, 0.01, 0.12), blackM, g, [0, y + 0.145, 0.08]);
    for (let r = 0; r < 3; r++) for (let i = 0; i < 8; i++) mesh(cyl(0.012, 0.012, 0.012, 8), ivory, g, [-0.16 + i * 0.045 + (r % 2) * 0.02, y + 0.155, 0.04 + r * 0.035]);
    for (let i = 0; i < 3; i++) mesh(cyl(0.035, 0.035, 0.02, 16), M.gold, g, [-0.06 + i * 0.06, y + 0.16, -0.08], [0, 0, Math.PI / 2]);
    for (let i = 0; i < 8; i++) mesh(sph(0.01, 6, 4), mat(0xffd27a, { emissive: 0xffb040, emissiveIntensity: 0.8 }), g, [-0.16 + i * 0.045, y + 0.15, -0.01], null, false);
  },
  megafone(g) {
    const y = pedestal(g, 0.9);
    const m = new THREE.Group(); m.position.set(0, y + 0.18, 0); m.rotation.set(0, 0, 0.35); g.add(m);
    mesh(new THREE.CylinderGeometry(0.16, 0.035, 0.42, 24, 1, true), mat(0xd4b26a, { metalness: 1, roughness: 0.25, side: THREE.DoubleSide }), m, [0.08, 0, 0], [0, 0, -Math.PI / 2]);
    mesh(cyl(0.03, 0.03, 0.12, 12), blackM, m, [-0.18, 0, 0], [0, 0, Math.PI / 2]);
    mesh(box(0.03, 0.12, 0.03), blackM, m, [-0.17, -0.07, 0]);
    mesh(new THREE.TorusGeometry(0.16, 0.012, 6, 28), M.gold, m, [0.29, 0, 0], [0, Math.PI / 2, 0]);
  },
  camera(g) {
    [0, 1, 2].forEach(i => { const a = i * Math.PI * 2 / 3; const leg = mesh(cyl(0.012, 0.016, 1.3, 8), walnut, g, [Math.cos(a) * 0.22, 0.62, Math.sin(a) * 0.22]); leg.rotation.set(Math.sin(a) * 0.18, 0, -Math.cos(a) * 0.18); });
    mesh(box(0.34, 0.24, 0.2), blackM, g, [0, 1.38, 0]);
    mesh(cyl(0.05, 0.06, 0.16, 16), blackM, g, [0, 1.38, 0.17], [Math.PI / 2, 0, 0]);
    mesh(cyl(0.045, 0.045, 0.005, 16), mat(0x445566, { metalness: 0.5, roughness: 0.05 }), g, [0, 1.38, 0.255], [Math.PI / 2, 0, 0], false);
    [-0.09, 0.11].forEach(x => { mesh(cyl(0.11, 0.11, 0.03, 24), M.gold, g, [x, 1.6, -0.02], [0, 0, Math.PI / 2]); });
    const clap = new THREE.Group(); clap.position.set(0.35, 0.01, 0.2); clap.rotation.y = -0.5; g.add(clap);
    mesh(box(0.28, 0.01, 0.2), blackM, clap, [0, 0.005, 0]);
    for (let i = 0; i < 5; i++) mesh(box(0.028, 0.012, 0.04), ivory, clap, [-0.11 + i * 0.056, 0.012, -0.08], [0, 0, 0], false);
  },
  hipopotamo(g) {
    mesh(box(1.4, 0.18, 0.75), blackM, g, [0, 0.09, 0]); mesh(box(1.44, 0.025, 0.79), M.gold, g, [0, 0.18, 0]);
    const gold = mat(0xd8b56a, { metalness: 1, roughness: 0.22 });
    const body = mesh(new THREE.CapsuleGeometry(0.26, 0.5, 6, 16), gold, g, [0, 0.52, 0], [0, 0, Math.PI / 2]); body.scale.set(1, 1, 0.95);
    const head = mesh(new THREE.CapsuleGeometry(0.17, 0.2, 6, 14), gold, g, [0.58, 0.6, 0], [0, 0, Math.PI / 2 - 0.25]); head.scale.set(1.05, 1, 0.9);
    mesh(sph(0.17, 14, 10), gold, g, [0.78, 0.5, 0]).scale.set(0.8, 0.75, 1.1);
    [-1, 1].forEach(s => { mesh(sph(0.04, 8, 6), gold, g, [0.52, 0.78, s * 0.1]); mesh(sph(0.03, 8, 6), blackM, g, [0.66, 0.7, s * 0.11], null, false); });
    [[-0.3, -0.16], [-0.3, 0.16], [0.28, -0.16], [0.28, 0.16]].forEach(([x, z]) => mesh(cyl(0.085, 0.09, 0.24, 12), gold, g, [x, 0.3, z]));
  },
  braco(g) {
    mesh(cyl(0.22, 0.26, 0.12, 24), blackM, g, [0, 0.06, 0]);
    const j = (y, a, len, parent) => { const p = new THREE.Group(); p.position.y = y; p.rotation.z = a; parent.add(p); mesh(sph(0.075, 12, 8), M.gold, p); mesh(rbox(0.11, len, 0.11, 0.02), blackM, p, [0, len / 2, 0]); return p; };
    const a1 = j(0.14, 0.35, 0.6, g), a2 = j(0.6, -1.2, 0.5, a1), a3 = j(0.5, -0.6, 0.18, a2);
    [-1, 1].forEach(s => mesh(box(0.02, 0.1, 0.03), M.chrome, a3, [s * 0.035, 0.22, 0]));
    const ring = mesh(new THREE.TorusGeometry(0.28, 0.008, 6, 40), new THREE.MeshBasicMaterial({ color: 0x5ab0ff, transparent: true, opacity: 0.75 }), g, [0, 0.02, 0], [Math.PI / 2, 0, 0], false); ring.userData.keep = true;
  },
  ticker(g) {
    const y = pedestal(g, 0.85, 0.5);
    mesh(cyl(0.12, 0.14, 0.05, 20), M.brass, g, [0, y + 0.025, 0]);
    mesh(box(0.12, 0.1, 0.1), M.brass, g, [0, y + 0.1, 0]); mesh(cyl(0.03, 0.03, 0.14, 12), M.gold, g, [0, y + 0.12, 0], [0, 0, Math.PI / 2]);
    const dome = mesh(new THREE.SphereGeometry(0.14, 16, 10, 0, Math.PI * 2, 0, Math.PI / 2), M.glass, g, [0, y + 0.05, 0], null, false); dome.scale.y = 1.4;
    const tape = new THREE.CatmullRomCurve3([new THREE.Vector3(0.06, y + 0.12, 0), new THREE.Vector3(0.28, y - 0.05, 0.05), new THREE.Vector3(0.3, y - 0.4, 0.02), new THREE.Vector3(0.24, 0.1, 0.12), new THREE.Vector3(0.4, 0.02, 0.2)]);
    mesh(new THREE.TubeGeometry(tape, 24, 0.008, 4), ivory, g);
  },
  foguete(g) {
    mesh(cyl(0.3, 0.34, 0.06, 24), blackM, g, [0, 0.03, 0]);
    mesh(cyl(0.11, 0.11, 1.2, 20), ivory, g, [0, 0.75, 0]);
    mesh(new THREE.ConeGeometry(0.11, 0.32, 20), ivory, g, [0, 1.51, 0]);
    mesh(cyl(0.112, 0.112, 0.05, 20), M.gold, g, [0, 1.1, 0]); mesh(cyl(0.112, 0.112, 0.03, 20), M.gold, g, [0, 0.5, 0]);
    for (let i = 0; i < 4; i++) { const a = i * Math.PI / 2; const f = mesh(box(0.012, 0.26, 0.16), M.gold, g, [Math.cos(a) * 0.15, 0.28, Math.sin(a) * 0.15]); f.rotation.y = -a; }
    mesh(cyl(0.07, 0.09, 0.08, 16), blackM, g, [0, 0.12, 0]);
  },
  xadrez(g) {
    mesh(cyl(0.38, 0.38, 0.04, 28), walnut, g, [0, 0.72, 0]); mesh(cyl(0.05, 0.06, 0.7, 12), walnut, g, [0, 0.36, 0]); mesh(cyl(0.22, 0.24, 0.03, 20), walnut, g, [0, 0.015, 0]);
    const t = tex(256, 256, (c, w) => { for (let i = 0; i < 8; i++) for (let j = 0; j < 8; j++) { c.fillStyle = (i + j) % 2 ? '#1a1a1a' : '#e8e0d0'; c.fillRect(i * 32, j * 32, 32, 32); } });
    mesh(new THREE.PlaneGeometry(0.4, 0.4), mat(0xffffff, { map: t, roughness: 0.3 }), g, [0, 0.742, 0], [-Math.PI / 2, 0, 0], false);
    [[-0.15, -0.15, 0], [0.05, -0.1, 0], [-0.05, 0.12, 1], [0.15, 0.15, 1], [0.1, 0.05, 0], [-0.12, 0.02, 1]].forEach(([x, z, w]) => { mesh(cyl(0.012, 0.018, 0.04, 8), w ? ivory : blackM, g, [x, 0.762, z]); mesh(sph(0.013, 6, 4), w ? ivory : blackM, g, [x, 0.79, z]); });
    [-1, 1].forEach(s => { const c = new THREE.Group(); c.position.set(0, 0, s * 0.62); c.rotation.y = s > 0 ? Math.PI : 0; g.add(c); mesh(rbox(0.44, 0.08, 0.42, 0.03), M.leather, c, [0, 0.45, 0]); mesh(rbox(0.44, 0.45, 0.06, 0.03), M.leather, c, [0, 0.7, -0.2]); [[-0.18, -0.16], [0.18, -0.16], [-0.18, 0.16], [0.18, 0.16]].forEach(([x, z]) => mesh(cyl(0.014, 0.012, 0.42, 6), M.gold, c, [x, 0.21, z])); });
  },
  vinil(g) {
    mesh(rbox(1.1, 0.62, 0.42, 0.02), walnut, g, [0, 0.31, 0]); mesh(box(1.12, 0.02, 0.44), M.gold, g, [0, 0.63, 0]);
    for (let i = 0; i < 10; i++) mesh(box(0.012, 0.3, 0.3), mat([0x7a1c1c, 0x1c3a5e, 0xd4b26a, 0x1a1a1a, 0xe8e0d0][i % 5], { roughness: 0.6 }), g, [-0.45 + i * 0.035, 0.25, 0.04], null, false);
    mesh(cyl(0.16, 0.16, 0.02, 28), blackM, g, [0.24, 0.65, 0]); mesh(cyl(0.05, 0.05, 0.022, 16), mat(0xb02020), g, [0.24, 0.652, 0], null, false);
    mesh(box(0.02, 0.015, 0.2), M.chrome, g, [0.42, 0.67, -0.04], [0, 0.35, 0]);
  },
  globo(g) {
    [0, 1, 2, 3].forEach(i => { const a = i * Math.PI / 2 + 0.4; mesh(cyl(0.018, 0.018, 0.75, 8), walnut, g, [Math.cos(a) * 0.2, 0.37, Math.sin(a) * 0.2]); });
    mesh(new THREE.TorusGeometry(0.3, 0.02, 6, 32), walnut, g, [0, 0.74, 0], [Math.PI / 2, 0, 0]);
    const t = tex(512, 256, (c, w, h) => { c.fillStyle = '#c9b48a'; c.fillRect(0, 0, w, h); c.fillStyle = '#7a5f3a'; [[80, 70, 60, 40], [130, 150, 40, 60], [250, 60, 70, 45], [270, 130, 50, 70], [380, 80, 90, 50], [420, 180, 40, 25]].forEach(([x, y, rx, ry]) => { c.beginPath(); c.ellipse(x, y, rx, ry, 0.3, 0, 7); c.fill(); }); c.strokeStyle = 'rgba(60,40,20,.35)'; for (let i = 0; i < 12; i++) { c.beginPath(); c.moveTo(i * w / 12, 0); c.lineTo(i * w / 12, h); c.stroke(); } });
    const gl = mesh(new THREE.SphereGeometry(0.26, 24, 16), mat(0xffffff, { map: t, roughness: 0.4 }), g, [0, 0.9, 0], [0.41, 0, 0]);
    mesh(new THREE.TorusGeometry(0.28, 0.008, 4, 40, Math.PI), M.gold, g, [0, 0.9, 0], [0, 0, 0.41]);
  },
  cavalo(g) {
    mesh(box(1.1, 0.5, 0.45), blackM, g, [0, 0.25, 0]); mesh(box(1.14, 0.025, 0.49), M.gold, g, [0, 0.5, 0]);
    const y = 0.5;
    const body = mesh(new THREE.CapsuleGeometry(0.14, 0.42, 6, 14), bronze, g, [0, y + 0.5, 0], [0, 0, Math.PI / 2]); body.scale.set(1, 1, 0.85);
    const neck = mesh(new THREE.CapsuleGeometry(0.075, 0.26, 6, 10), bronze, g, [0.3, y + 0.68, 0], [0, 0, -0.6]);
    const head = mesh(new THREE.CapsuleGeometry(0.06, 0.18, 6, 10), bronze, g, [0.44, y + 0.82, 0], [0, 0, -1.8]);
    [-1, 1].forEach(s => mesh(new THREE.ConeGeometry(0.02, 0.06, 6), bronze, g, [0.37, y + 0.92, s * 0.03]));
    [[-0.22, -0.08, 0.15], [-0.22, 0.08, -0.1], [0.22, -0.08, -0.25], [0.22, 0.08, 0.05]].forEach(([x, z, r]) => mesh(cyl(0.028, 0.022, 0.42, 8), bronze, g, [x + Math.sin(r) * 0.1, y + 0.21, z], [0, 0, r]));
    const tail = mesh(new THREE.CapsuleGeometry(0.03, 0.22, 4, 8), bronze, g, [-0.38, y + 0.45, 0], [0, 0, -0.5]);
  },
};

export function buildDecor(scene, DECOR, NOMES) {
  const items = [];
  DECOR.forEach(d => {
    const g = new THREE.Group(); g.position.set(d.pos[0], 0, d.pos[1]); g.rotation.y = d.rot || 0; scene.add(g);
    (B[d.item] || B.globo)(g);
    const ped = ['enigma', 'megafone', 'ticker'].includes(d.item);
    plaque(g, NOMES[d.dono] || '', ped ? 0.45 : 0.1, ped ? 0.282 : 0.4);
    g.traverse(o => { if (o.isMesh) o.userData.decor = d; });
    items.push({ d, g });
  });
  return items;
}

// Hall da Fama: totem de mármore preto com os dois quadros (dos dois lados)
export function buildHall(scene, LOGO, HALL, nomeDe) {
  const g = new THREE.Group(); g.position.set(-2.3, 0, 7.45); scene.add(g);
  const bm = mat(0xffffff, { map: marbleTex('#0e0e0f', 'rgba(220,220,220,A)', 20, 512, [1, 1]), roughness: 0.15 });
  mesh(box(2.8, 2.5, 0.16), bm, g, [0, 1.25, 0]);
  mesh(box(2.86, 0.04, 0.2), M.gold, g, [0, 2.5, 0]); mesh(box(2.9, 0.08, 0.24), M.gold, g, [0, 0.04, 0]);
  const draw = (titulo, quem, sub) => tex(640, 800, (c, w, h) => {
    c.fillStyle = '#0c0a08'; c.fillRect(0, 0, w, h);
    c.strokeStyle = '#d4b26a'; c.lineWidth = 6; c.strokeRect(22, 22, w - 44, h - 44); c.lineWidth = 1.5; c.strokeRect(38, 38, w - 76, h - 76);
    c.fillStyle = '#d4b26a'; c.textAlign = 'center'; c.font = '600 30px Inter, Arial'; c.fillText(titulo, w / 2, 110);
    c.beginPath(); c.arc(w / 2, 330, 150, 0, 7); c.fillStyle = goldGrad(c, w, h); c.fill();
    c.beginPath(); c.arc(w / 2, 330, 138, 0, 7); c.fillStyle = '#14100c'; c.fill();
    c.fillStyle = goldGrad(c, w, h); c.font = '700 120px "Cormorant Garamond", Georgia, serif';
    const ini = quem ? quem.split(' ').map(x => x[0]).join('').slice(0, 2) : '?'; c.fillText(ini, w / 2, 372);
    c.fillStyle = '#f3ede2'; c.font = '700 54px "Cormorant Garamond", Georgia, serif'; c.fillText(quem || 'Em disputa', w / 2, 560);
    c.fillStyle = '#a39a8a'; c.font = '500 26px Inter, Arial'; c.fillText(sub, w / 2, 610);
    c.fillStyle = '#d4b26a'; c.font = '600 22px Inter, Arial'; c.fillText('CARNUCCI', w / 2, 720);
  });
  const fmt = iso => iso.split('-').reverse().slice(0, 2).join('/');
  const semana = HALL.semana ? nomeDe(HALL.semana) : null, mes = HALL.mes ? nomeDe(HALL.mes) : null;
  const tS = draw('DIRETOR DA SEMANA', semana, semana ? 'Mais desenrolou na semana' : `Primeira escolha na sexta, ${fmt(HALL.primeiraEscolha)}`);
  const tM = draw('DIRETOR DO MÊS', mes, mes ? 'Mais desenrolou no mês' : 'Primeira escolha no fim do mês');
  [1, -1].forEach(side => {
    [[-0.68, tS], [0.68, tM]].forEach(([x, t]) => {
      const fx = side * x;
      mesh(box(1.12, 1.4, 0.03), M.gold, g, [fx, 1.35, side * 0.095], null, false);
      mesh(new THREE.PlaneGeometry(1.04, 1.3), new THREE.MeshBasicMaterial({ map: t }), g, [fx, 1.35, side * 0.112], [0, side > 0 ? 0 : Math.PI, 0], false);
    });
  });
  g.traverse(o => { if (o.isMesh) o.userData.hall = true; });
  return g;
}
