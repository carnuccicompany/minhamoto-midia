import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { DIRETORES } from './data.js';

const LOGO = window.__LOGO__;
const GOLD = 0xd4b26a;
const app = document.getElementById('app');
const isMobile = () => window.innerWidth < 760;

// ---------- renderer / cena ----------
const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance', preserveDrawingBuffer: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75));
renderer.setSize(app.clientWidth, app.clientHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.15;
renderer.outputColorSpace = THREE.SRGBColorSpace;
app.appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x060607);
scene.fog = new THREE.Fog(0x07070a, 16, 30);

const camera = new THREE.PerspectiveCamera(42, app.clientWidth / app.clientHeight, 0.1, 80);
const HOME = { pos: new THREE.Vector3(0, 6.2, 9.6), tgt: new THREE.Vector3(0, 0.75, 0) };
camera.position.copy(HOME.pos);
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.copy(HOME.tgt);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 3.2;
controls.maxDistance = 13;
controls.maxPolarAngle = 1.42;
controls.enablePan = false;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.35;
let autoTimer = null;
controls.addEventListener('start', () => { controls.autoRotate = false; clearTimeout(autoTimer); camFly = null; });
controls.addEventListener('end', () => { clearTimeout(autoTimer); autoTimer = setTimeout(() => { if (!selected) controls.autoRotate = rotOn; }, 9000); });

// ---------- helpers ----------
const mat = (color, o = {}) => new THREE.MeshStandardMaterial(Object.assign({ color, roughness: 0.6, metalness: 0 }, o));
function tex(w, h, draw, repeat) {
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
  if (repeat) { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(repeat[0], repeat[1]); }
  return t;
}
function mesh(geo, m, parent, pos, rot, shadow = true) {
  const o = new THREE.Mesh(geo, m);
  if (pos) o.position.set(pos[0], pos[1], pos[2]);
  if (rot) o.rotation.set(rot[0], rot[1], rot[2]);
  o.castShadow = shadow; o.receiveShadow = true;
  if (parent) parent.add(o);
  return o;
}
const box = (w, h, d) => new THREE.BoxGeometry(w, h, d);
const cyl = (rt, rb, h, s = 24) => new THREE.CylinderGeometry(rt, rb, h, s);
const hex = n => '#' + n.toString(16).padStart(6, '0');

// materiais compartilhados
const M = {
  gold: mat(GOLD, { metalness: 1, roughness: 0.28 }),
  goldDim: mat(0xa8823f, { metalness: 1, roughness: 0.4 }),
  leather: mat(0x1a1210, { roughness: 0.42 }),
  leatherDark: mat(0x0f0b09, { roughness: 0.5 }),
  chrome: mat(0xcccccc, { metalness: 1, roughness: 0.2 }),
  black: mat(0x0d0d0f, { roughness: 0.35 }),
  shirt: mat(0xf2efe8, { roughness: 0.7 }),
  shoe: mat(0x0a0a0a, { roughness: 0.3, metalness: 0.2 }),
  eye: mat(0x0a0a0a),
  glass: new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: 0.05, metalness: 0, transparent: true, opacity: 0.28, clearcoat: 1 }),
  amber: mat(0xb8651a, { roughness: 0.15, transparent: true, opacity: 0.9, emissive: 0x3a1600 }),
  ice: new THREE.MeshPhysicalMaterial({ color: 0xeaf6ff, roughness: 0.1, transparent: true, opacity: 0.55 }),
  porcelain: mat(0xf4f1ea, { roughness: 0.3 }),
  coffee: mat(0x2a160a, { roughness: 0.2 }),
  cigar: mat(0x6b4426, { roughness: 0.8 }),
  ember: mat(0xff6a1a, { emissive: 0xff4a00, emissiveIntensity: 2.2 }),
  cash: mat(0x86a77a, { roughness: 0.85 }),
  band: mat(0xe9dcb8, { roughness: 0.7 }),
};

// ---------- texturas ----------
const woodFloor = tex(1024, 1024, (g, w, h) => {
  g.fillStyle = '#0c0c0d'; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 26; i++) {
    g.strokeStyle = `rgba(${150 + Math.random() * 60},${150 + Math.random() * 60},${150 + Math.random() * 60},${0.04 + Math.random() * 0.1})`; g.lineWidth = 0.6 + Math.random() * 2;
    g.beginPath(); let x = Math.random() * w, y = 0; g.moveTo(x, y);
    while (y < h) { x += (Math.random() - .5) * 60; y += 20 + Math.random() * 40; g.lineTo(x, y); } g.stroke();
  }
  g.strokeStyle = 'rgba(0,0,0,.8)'; g.lineWidth = 2; g.strokeRect(0, 0, w, h);
}, [6, 6]);
const pinTex = tex(256, 256, (g, w, h) => { g.fillStyle = '#ffffff'; g.fillRect(0, 0, w, h); g.fillStyle = 'rgba(0,0,0,.09)'; for (let x = 0; x < w; x += 32) g.fillRect(x, 0, 2, h); }, [4, 1]);
const tableWood = tex(1024, 1024, (g, w, h) => {
  const gr = g.createRadialGradient(w / 2, h / 2, 50, w / 2, h / 2, w / 2);
  gr.addColorStop(0, '#2a1d15'); gr.addColorStop(0.7, '#1a120c'); gr.addColorStop(1, '#100a07');
  g.fillStyle = gr; g.fillRect(0, 0, w, h);
  g.globalAlpha = 0.18; g.strokeStyle = '#000';
  for (let i = 0; i < 160; i++) { g.lineWidth = Math.random() * 2; g.beginPath(); const y = Math.random() * h; g.moveTo(0, y); g.bezierCurveTo(w * .3, y + Math.random() * 30 - 15, w * .7, y + Math.random() * 30 - 15, w, y + Math.random() * 20 - 10); g.stroke(); }
  g.globalAlpha = 1;
});
const panelWall = tex(512, 512, (g, w, h) => {
  g.fillStyle = '#121214'; g.fillRect(0, 0, w, h);
  for (let x = 0; x < w; x += 32) { g.fillStyle = x % 64 ? '#161619' : '#0f0f11'; g.fillRect(x, 0, 30, h); }
  g.fillStyle = 'rgba(212,178,106,.55)'; g.fillRect(0, h - 70, w, 3);
  g.fillStyle = '#0a0a0b'; g.fillRect(0, h - 67, w, 67);
}, [10, 1]);
const skyline = tex(4096, 1024, (g, w, h) => {
  const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, '#05070f'); gr.addColorStop(0.6, '#0e1530'); gr.addColorStop(1, '#2a1c2e');
  g.fillStyle = gr; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 300; i++) { g.fillStyle = `rgba(255,255,255,${Math.random() * .5})`; g.fillRect(Math.random() * w, Math.random() * h * .35, 2, 2); }
  let x = 0;
  while (x < w) {
    const bw = 60 + Math.random() * 180, bh = 180 + Math.random() * 640;
    g.fillStyle = `rgb(${10 + Math.random() * 10},${12 + Math.random() * 10},${22 + Math.random() * 14})`;
    g.fillRect(x, h - bh, bw, bh);
    for (let wy = h - bh + 12; wy < h - 8; wy += 11) for (let wx = x + 6; wx < x + bw - 6; wx += 8) {
      if (Math.random() < 0.3) { g.fillStyle = Math.random() < .8 ? `rgba(255,${200 + Math.random() * 40},${120 + Math.random() * 60},${.35 + Math.random() * .45})` : 'rgba(170,200,255,.6)'; g.fillRect(wx, wy, 3, 5); }
    }
    x += bw + Math.random() * 8;
  }
});

// brasão dourado + anel do Coordenador
function goldLogoCanvas(size, withRing) {
  const c = document.createElement('canvas'); c.width = c.height = size; const g = c.getContext('2d');
  return new Promise(res => {
    const img = new Image();
    img.onload = () => {
      const t = document.createElement('canvas'); t.width = t.height = size; const tg = t.getContext('2d');
      const s = size * (withRing ? 0.5 : 0.9), ar = img.height / img.width;
      tg.drawImage(img, (size - s) / 2, (size - s * ar) / 2, s, s * ar);
      tg.globalCompositeOperation = 'source-in';
      const gr = tg.createLinearGradient(0, 0, size, size);
      gr.addColorStop(0, '#f6e3ad'); gr.addColorStop(.45, '#d4b26a'); gr.addColorStop(.7, '#a8823f'); gr.addColorStop(1, '#f0d9a0');
      tg.fillStyle = gr; tg.fillRect(0, 0, size, size);
      if (withRing) {
        g.fillStyle = '#0d0907'; g.beginPath(); g.arc(size / 2, size / 2, size * .36, 0, 7); g.fill();
        g.strokeStyle = '#d4b26a'; g.lineWidth = size * .008; g.beginPath(); g.arc(size / 2, size / 2, size * .36, 0, 7); g.stroke();
        g.lineWidth = size * .003; g.beginPath(); g.arc(size / 2, size / 2, size * .345, 0, 7); g.stroke();
        g.shadowColor = 'rgba(240,210,140,.55)'; g.shadowBlur = size * .02;
        g.drawImage(t, 0, 0); g.shadowBlur = 0;
        const ring = (txt, r, fs, col, top) => {
          g.font = `600 ${fs}px Inter, Arial, sans-serif`; g.fillStyle = col;
          const chars = [...txt], sp = fs * 0.95 / r; const tot = sp * (chars.length - 1);
          chars.forEach((ch, i) => {
            const a = top ? -Math.PI / 2 - tot / 2 + i * sp : Math.PI / 2 + tot / 2 - i * sp;
            g.save(); g.translate(size / 2 + Math.cos(a) * r, size / 2 + Math.sin(a) * r); g.rotate(top ? a + Math.PI / 2 : a - Math.PI / 2);
            g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(ch, 0, 0); g.restore();
          });
        };
        ring('COORDENADOR', size * .41, size * .034, '#ecd295', true);
        ring('DON CARNUCCI', size * .41, size * .026, '#a39a8a', false);
        g.strokeStyle = 'rgba(212,178,106,.6)'; g.lineWidth = size * .003; g.beginPath(); g.arc(size / 2, size / 2, size * .455, 0, 7); g.stroke();
      } else g.drawImage(t, 0, 0);
      const T = new THREE.CanvasTexture(c); T.colorSpace = THREE.SRGBColorSpace; T.anisotropy = 8; res(T);
    };
    img.src = LOGO;
  });
}

function plateTex(d) {
  return tex(1024, 306, (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, w, h);
    gr.addColorStop(0, '#f3dda0'); gr.addColorStop(.5, '#c79f55'); gr.addColorStop(1, '#ebd090');
    g.fillStyle = gr; g.fillRect(0, 0, w, h);
    g.strokeStyle = '#5e4218'; g.lineWidth = 8; g.strokeRect(16, 16, w - 32, h - 32);
    g.lineWidth = 2; g.strokeRect(30, 30, w - 60, h - 60);
    g.fillStyle = '#24160a'; g.textAlign = 'center'; g.textBaseline = 'alphabetic';
    let fs = 104; g.font = `700 ${fs}px "Cormorant Garamond", Georgia, serif`;
    while (g.measureText(d.nome.toUpperCase()).width > w - 120) { fs -= 4; g.font = `700 ${fs}px "Cormorant Garamond", Georgia, serif`; }
    g.fillText(d.nome.toUpperCase(), w / 2, 160);
    g.font = '600 46px Inter, Arial, sans-serif'; g.fillText(d.setor.toUpperCase(), w / 2, 238);
  });
}

// ---------- sala ----------
const ROOM = 11;
mesh(new THREE.PlaneGeometry(ROOM * 2, ROOM * 2), mat(0xffffff, { map: woodFloor, roughness: 0.18, metalness: 0.15 }), scene, [0, 0, 0], [-Math.PI / 2, 0, 0], false);
// tapete
const rug = tex(1024, 1024, (g, w, h) => {
  g.fillStyle = '#141313'; g.beginPath(); g.arc(w / 2, h / 2, w / 2, 0, 7); g.fill();
  g.strokeStyle = 'rgba(212,178,106,.55)'; g.lineWidth = 8; g.beginPath(); g.arc(w / 2, h / 2, w / 2 - 30, 0, 7); g.stroke();
  g.lineWidth = 3; g.beginPath(); g.arc(w / 2, h / 2, w / 2 - 48, 0, 7); g.stroke();
  g.globalAlpha = .06; g.fillStyle = '#d4b26a';
  for (let i = 0; i < 36; i++) { g.save(); g.translate(w / 2, h / 2); g.rotate(i * Math.PI / 18); g.fillRect(-2, w / 2 - 120, 4, 60); g.restore(); }
});
const rugM = mesh(new THREE.CircleGeometry(4.6, 96), mat(0xffffff, { map: rug, transparent: true, roughness: 0.95 }), scene, [0, 0.005, 0], [-Math.PI / 2, 0, 0], false);

const wallM = mat(0xffffff, { map: panelWall, roughness: 0.75 });
function wall(x, z, ry, len) {
  const w = mesh(new THREE.PlaneGeometry(len, 4.4), wallM, scene, [x, 2.2, z], [0, ry, 0], false);
  mesh(box(len, 0.05, 0.06), M.goldDim, scene, [x, 3.4, z], [0, ry, 0], false).position.add(new THREE.Vector3(Math.sin(ry) * 0.03, 0, Math.cos(ry) * 0.03));
  return w;
}
// janela panorâmica (norte)
mesh(new THREE.PlaneGeometry(ROOM * 2, 4.4), new THREE.MeshBasicMaterial({ map: skyline, color: 0xb8b8c8 }), scene, [0, 2.2, -ROOM], [0, 0, 0], false);
for (let i = -4; i <= 4; i++) mesh(box(0.08, 4.4, 0.1), M.black, scene, [i * 2.6, 2.2, -ROOM + 0.05], null, false);
mesh(box(ROOM * 2, 0.12, 0.14), M.black, scene, [0, 0.06, -ROOM + 0.06], null, false);
wall(0, ROOM, Math.PI, ROOM * 2);
wall(-ROOM, 0, Math.PI / 2, ROOM * 2);
wall(ROOM, 0, -Math.PI / 2, ROOM * 2);

// brasão grande na parede sul
goldLogoCanvas(512, false).then(t => {
  const m = new THREE.MeshStandardMaterial({ map: t, transparent: true, metalness: 0.9, roughness: 0.3, emissive: 0x3a2a10, emissiveMap: t });
  mesh(new THREE.PlaneGeometry(2.2, 2.2), m, scene, [0, 2.3, ROOM - 0.02], [0, Math.PI, 0], false);
});

// porta do banheiro (leste)
const DOOR = new THREE.Vector3(ROOM - 0.02, 0, 3.4);
mesh(box(0.12, 2.5, 1.35), M.goldDim, scene, [ROOM - 0.05, 1.25, DOOR.z], null, false);
const doorPivot = new THREE.Group(); doorPivot.position.set(ROOM - 0.1, 0, DOOR.z - 0.6); scene.add(doorPivot);
mesh(box(0.06, 2.38, 1.18), mat(0x2a1a10, { roughness: 0.5 }), doorPivot, [0, 1.19, 0.59], null, false);
mesh(new THREE.SphereGeometry(0.035, 12, 8), M.gold, doorPivot, [-0.06, 1.05, 1.05], null, false);
mesh(new THREE.PlaneGeometry(1.1, 2.35), new THREE.MeshBasicMaterial({ color: 0x050505 }), scene, [ROOM - 0.005, 1.18, DOOR.z], [0, -Math.PI / 2, 0], false);
const wcTex = tex(256, 96, (g, w, h) => { g.fillStyle = '#120d09'; g.fillRect(0, 0, w, h); g.strokeStyle = '#d4b26a'; g.lineWidth = 3; g.strokeRect(5, 5, w - 10, h - 10); g.fillStyle = '#e9cf91'; g.font = '600 40px Inter, Arial'; g.textAlign = 'center'; g.fillText('W C', w / 2, 62); });
mesh(new THREE.PlaneGeometry(0.6, 0.22), new THREE.MeshBasicMaterial({ map: wcTex }), scene, [ROOM - 0.03, 2.75, DOOR.z], [0, -Math.PI / 2, 0], false);

// aparador com bebidas (oeste)
const bar = new THREE.Group(); bar.position.set(-ROOM + 0.45, 0, -2); bar.rotation.y = Math.PI / 2; scene.add(bar);
mesh(box(3, 0.9, 0.7), mat(0x0e0d0c, { roughness: 0.3 }), bar, [0, 0.45, 0]);
mesh(box(3.04, 0.04, 0.74), M.goldDim, bar, [0, 0.92, 0]);
[[-1.1, 0x6b3a12], [-0.8, 0x2f4a22], [-0.5, 0x8a5a1a], [-0.2, 0x5a1a14], [0.9, 0x8a5a1a], [1.15, 0x3a2a12]].forEach(([x, c]) => {
  mesh(cyl(0.06, 0.07, 0.3), new THREE.MeshPhysicalMaterial({ color: c, roughness: 0.1, transparent: true, opacity: 0.85, clearcoat: 1 }), bar, [x, 1.09, 0]);
  mesh(cyl(0.02, 0.025, 0.1), new THREE.MeshPhysicalMaterial({ color: c, roughness: 0.1, transparent: true, opacity: 0.85 }), bar, [x, 1.29, 0]);
});
mesh(new THREE.SphereGeometry(0.11, 20, 14), M.glass, bar, [0.35, 1.05, 0]);
// plantas
function plant(x, z) {
  const p = new THREE.Group(); p.position.set(x, 0, z); scene.add(p);
  mesh(cyl(0.28, 0.22, 0.6), M.black, p, [0, 0.3, 0]); mesh(cyl(0.29, 0.29, 0.04), M.goldDim, p, [0, 0.6, 0]);
  const leaf = mat(0x1d3a22, { roughness: 0.8 });
  for (let i = 0; i < 9; i++) mesh(new THREE.SphereGeometry(0.25 + Math.random() * 0.12, 10, 8), leaf, p, [Math.cos(i) * 0.22, 1 + Math.random() * 0.9, Math.sin(i * 1.7) * 0.22]);
}
plant(-ROOM + 0.8, -ROOM + 0.8); plant(ROOM - 0.8, -ROOM + 0.8); plant(-ROOM + 0.8, ROOM - 0.8); plant(ROOM - 0.8, ROOM - 0.8);

// ---------- leão (escultura dourada facetada) ----------
function lion() {
  const L = new THREE.Group();
  const gold = new THREE.MeshStandardMaterial({ color: 0xd8b56a, metalness: 1, roughness: 0.22, flatShading: true });
  const marble = mat(0x0b0b0c, { roughness: 0.15, metalness: 0.2, map: woodFloor });
  mesh(box(1.7, 0.95, 0.95), marble, L, [0, 0.475, 0]);
  mesh(box(1.76, 0.04, 1.01), M.gold, L, [0, 0.95, 0]);
  mesh(box(1.76, 0.04, 1.01), M.gold, L, [0, 0.02, 0]);
  const Y = 0.97, ico = (r, d = 1) => new THREE.IcosahedronGeometry(r, d);
  const part = (geo, p, sc, rot) => { const m = mesh(geo, gold, L, p, rot); if (sc) m.scale.set(...sc); return m; };
  part(ico(0.34), [-0.18, Y + 0.3, 0], [1.55, 0.78, 0.9]); // corpo deitado
  part(ico(0.3), [-0.55, Y + 0.24, 0], [1, 0.85, 1.15]); // quadril
  part(ico(0.3), [0.25, Y + 0.38, 0], [0.95, 1.1, 1]); // peito
  part(ico(0.36, 1), [0.42, Y + 0.68, 0], [0.8, 1.05, 1.05]); // juba
  part(ico(0.2), [0.6, Y + 0.68, 0], [1.05, 1, 0.92]); // cabeça
  part(ico(0.1), [0.77, Y + 0.6, 0], [1.2, 0.8, 1]); // focinho
  part(ico(0.06), [0.46, Y + 0.9, 0.12]); part(ico(0.06), [0.46, Y + 0.9, -0.12]); // orelhas
  [0.17, -0.17].forEach(z => {
    part(new THREE.CapsuleGeometry(0.075, 0.42, 3, 6), [0.5, Y + 0.09, z], null, [0, 0, Math.PI / 2]); // patas da frente
    part(ico(0.09), [0.78, Y + 0.07, z], [1.2, 0.7, 1]);
    part(ico(0.13), [-0.48, Y + 0.12, z * 1.35], [1.5, 0.75, 0.8]); // patas de trás
  });
  const tail = new THREE.CatmullRomCurve3([new THREE.Vector3(-0.78, Y + 0.18, 0), new THREE.Vector3(-0.9, Y + 0.06, 0.2), new THREE.Vector3(-0.7, Y + 0.04, 0.42), new THREE.Vector3(-0.4, Y + 0.05, 0.44)]);
  mesh(new THREE.TubeGeometry(tail, 20, 0.03, 6), gold, L);
  part(ico(0.06), [-0.38, Y + 0.06, 0.44]);
  L.traverse(o => { if (o.isMesh) o.castShadow = true; });
  return L;
}
const leao = lion(); leao.scale.setScalar(1.35); leao.position.set(-5.6, 0, -5.2); leao.rotation.y = -Math.atan2(5.2, 5.6); scene.add(leao);
const leaoLuz = new THREE.SpotLight(0xfff0d6, 60, 8, 0.4, 0.5, 1.3); leaoLuz.position.set(-3.6, 5, -3.6); leaoLuz.target = leao; scene.add(leaoLuz);

// ---------- mesa ----------
const TABLE_R = 2.35, TOP_Y = 0.76;
const table = new THREE.Group(); scene.add(table);
mesh(cyl(TABLE_R, TABLE_R, 0.07, 96), mat(0xffffff, { map: tableWood, roughness: 0.3, metalness: 0.05 }), table, [0, TOP_Y - 0.035, 0]);
mesh(new THREE.TorusGeometry(TABLE_R, 0.022, 10, 120), M.gold, table, [0, TOP_Y - 0.02, 0], [Math.PI / 2, 0, 0]);
mesh(new THREE.TorusGeometry(TABLE_R - 0.32, 0.006, 6, 120), M.gold, table, [0, TOP_Y + 0.001, 0], [Math.PI / 2, 0, 0], false);
mesh(cyl(0.55, 0.9, TOP_Y - 0.1, 48), mat(0x0e0c0b, { roughness: 0.3 }), table, [0, (TOP_Y - 0.1) / 2 + 0.05, 0]);
mesh(cyl(1.0, 1.05, 0.08, 48), M.goldDim, table, [0, 0.04, 0]);
goldLogoCanvas(1024, true).then(t => {
  mesh(new THREE.PlaneGeometry(0.95, 0.95), new THREE.MeshStandardMaterial({ map: t, transparent: true, metalness: 0, roughness: 0.55, emissive: 0xffffff, emissiveMap: t, emissiveIntensity: 0.22 }), table, [0, TOP_Y + 0.003, 0], [-Math.PI / 2, 0, 0], false);
});
// garrafa decanter no centro? não: o brasão é o centro. Um feixe de luz suave em cima dele
const beam = new THREE.Mesh(new THREE.CylinderGeometry(0.36, 0.5, 2.6, 48, 1, true), new THREE.MeshBasicMaterial({ color: 0xffd68a, transparent: true, opacity: 0.035, side: THREE.DoubleSide, depthWrite: false }));
beam.position.y = TOP_Y + 1.3; scene.add(beam);

// lustre
const chand = new THREE.Group(); chand.position.y = 4.9; scene.add(chand);
mesh(new THREE.TorusGeometry(1.6, 0.035, 12, 96), mat(0xffe2a8, { emissive: 0xffc870, emissiveIntensity: 1.5 }), chand, null, [Math.PI / 2, 0, 0], false);
mesh(new THREE.TorusGeometry(1.0, 0.025, 12, 80), mat(0xffe2a8, { emissive: 0xffc870, emissiveIntensity: 2 }), chand, [0, 0.25, 0], [Math.PI / 2, 0, 0], false);


// ---------- luz ----------
scene.add(new THREE.HemisphereLight(0xf2ece4, 0x111111, 0.45));
scene.add(new THREE.AmbientLight(0xffffff, 0.08));
const key = new THREE.SpotLight(0xfff0dc, 110, 14, 0.75, 0.55, 1.6);
key.position.set(0, 7.2, 0.4); key.target.position.set(0, 0.6, 0);
key.castShadow = true; key.shadow.mapSize.set(isMobile() ? 1024 : 2048, isMobile() ? 1024 : 2048); key.shadow.bias = -0.0004; key.shadow.normalBias = 0.02;
scene.add(key, key.target);
for (let i = 0; i < 4; i++) { const p = new THREE.PointLight(0xffe2bd, 6, 7, 1.8); const a = i * Math.PI / 2 + 0.6; p.position.set(Math.cos(a) * 1.6, 3.3, Math.sin(a) * 1.6); scene.add(p); }
const moon = new THREE.DirectionalLight(0x8aa6ff, 0.35); moon.position.set(0, 4, -12); scene.add(moon);
const wallWash = new THREE.PointLight(0xffd08a, 6, 6, 1.6); wallWash.position.set(0, 3, ROOM - 1.2); scene.add(wallWash);
const barLight = new THREE.PointLight(0xffb060, 3, 4, 1.6); barLight.position.set(-ROOM + 1.2, 1.8, -2); scene.add(barLight);

// ---------- pessoa ----------
function limb(len, r, m) { const g = new THREE.Group(); const c = mesh(new THREE.CapsuleGeometry(r, len - 2 * r, 6, 12), m, g, [0, -len / 2, 0]); return { g, c }; }
function person(d) {
  const suit = mat(d.terno, { roughness: 0.62, map: d.risca ? pinTex : null });
  const shirtM = d.camisa ? mat(d.camisa, { roughness: 0.6 }) : M.shirt;
  const skin = mat(d.pele, { roughness: 0.65 });
  const hair = mat(d.cabelo, { roughness: 0.85 });
  const root = new THREE.Group();
  const pelvis = new THREE.Group(); root.add(pelvis);
  const P = { root, pelvis, legs: [], knees: [], shoulders: [], elbows: [] };
  // pernas
  [-0.1, 0.1].forEach(x => {
    const hip = new THREE.Group(); hip.position.set(x, 0, 0); pelvis.add(hip);
    const th = limb(0.44, 0.085, suit); hip.add(th.g);
    const knee = new THREE.Group(); knee.position.y = -0.44; hip.add(knee);
    const sh = limb(0.44, 0.075, suit); knee.add(sh.g);
    mesh(box(0.11, 0.07, 0.27), M.shoe, knee, [0, -0.47, 0.06]);
    P.legs.push(hip); P.knees.push(knee);
  });
  // tronco
  mesh(box(0.36, 0.16, 0.24), suit, pelvis, [0, 0.04, 0]);
  const torso = mesh(new THREE.CapsuleGeometry(0.17, 0.32, 6, 16), suit, pelvis, [0, 0.36, -0.01]);
  torso.scale.set(1.35, 1, 0.78);
  if (d.gravata) {
    mesh(box(0.13, 0.24, 0.02), shirtM, pelvis, [0, 0.47, 0.128]);
    mesh(box(0.045, 0.22, 0.012), mat(d.gravata, { roughness: 0.4 }), pelvis, [0, 0.45, 0.142]);
    mesh(box(0.05, 0.035, 0.014), mat(d.gravata, { roughness: 0.4 }), pelvis, [0, 0.565, 0.143]);
    mesh(box(0.05, 0.03, 0.01), M.gold, pelvis, [-0.13, 0.5, 0.13]); // lenço de bolso
  } else {
    mesh(box(0.12, 0.2, 0.02), mat(0xe9e2d6, { roughness: 0.5 }), pelvis, [0, 0.49, 0.128]); // blusa
    mesh(new THREE.TorusGeometry(0.05, 0.006, 8, 24, Math.PI), M.gold, pelvis, [0, 0.6, 0.11], [0.2, 0, Math.PI]); // colar
  }
  [-1, 1].forEach(s => mesh(box(0.07, 0.26, 0.02), suit, pelvis, [s * 0.075, 0.45, 0.133], [0, 0, s * -0.32]));
  if (d.mulher) torso.scale.set(1.2, 1, 0.74);
  // braços
  [-1, 1].forEach(s => {
    const sh = new THREE.Group(); sh.position.set(s * (d.mulher ? 0.225 : 0.255), 0.6, -0.01); pelvis.add(sh);
    const up = limb(0.3, 0.065, suit); sh.add(up.g);
    const el = new THREE.Group(); el.position.y = -0.3; sh.add(el);
    const fo = limb(0.3, 0.058, suit); el.add(fo.g);
    mesh(cyl(0.05, 0.05, 0.04, 12), M.shirt, el, [0, -0.29, 0]);
    mesh(new THREE.SphereGeometry(0.052, 12, 10), skin, el, [0, -0.34, 0]);
    if (s === 1) mesh(cyl(0.035, 0.035, 0.012, 16), M.gold, el, [0.045, -0.26, 0], [0, 0, Math.PI / 2]); // relógio
    P.shoulders.push(sh); P.elbows.push(el);
  });
  // cabeça
  mesh(cyl(0.055, 0.06, 0.1, 12), skin, pelvis, [0, 0.69, 0]);
  const head = new THREE.Group(); head.position.set(0, 0.84, 0.01); pelvis.add(head); P.head = head;
  const hm = mesh(new THREE.SphereGeometry(0.125, 24, 18), skin, head); hm.scale.set(0.95, 1.12, 1);
  mesh(new THREE.SphereGeometry(0.018, 8, 6), skin, head, [0, -0.005, 0.125]); // nariz
  [-1, 1].forEach(s => {
    const eye = mesh(new THREE.SphereGeometry(0.012, 8, 6), M.eye, head, [s * 0.042, 0.025, 0.112]);
    if (d.olhos === 'puxados') { eye.scale.set(1.5, 0.45, 1); eye.rotation.z = s * -0.18; }
    mesh(new THREE.SphereGeometry(0.022, 8, 6), skin, head, [s * 0.12, 0, 0]);
    if (d.mulher) mesh(new THREE.SphereGeometry(0.011, 8, 6), M.gold, head, [s * 0.123, -0.035, 0.005]); // brinco
  });
  if (d.mulher) mesh(box(0.04, 0.009, 0.01), mat(0x8a1c2a, { roughness: 0.4 }), head, [0, -0.06, 0.112]); // batom
  // cabelo: calota no topo (inclinada pra trás) + faixa nas laterais e na nuca, rosto livre
  const st = d.estilo, F = 0.95; // meia-abertura do rosto (rad)
  const cap = (r, th, m, rx = -0.32) => { const c = mesh(new THREE.SphereGeometry(r, 28, 12, 0, Math.PI * 2, 0, Math.PI * th), m, head, [0, 0.008, -0.004]); c.scale.set(0.97, 1.12, 1.02); c.rotation.x = rx; return c; };
  const band = (r, t0, t1, m, f = F) => { const b = mesh(new THREE.SphereGeometry(r, 28, 12, Math.PI / 2 + f, Math.PI * 2 - 2 * f, Math.PI * t0, Math.PI * (t1 - t0)), m, head, [0, 0.004, -0.004]); b.scale.set(0.97, 1.12, 1.02); return b; };
  if (st === 'raspado') { cap(0.1265, 0.4, mat(0x0d0b0a, { roughness: 1, transparent: true, opacity: 0.55 })); }
  else {
    cap(0.132, st === 'grisalho' ? 0.34 : 0.4, hair);
    band(0.131, 0.25, st === 'chanel' ? 0.74 : st === 'longo' ? 0.7 : 0.6, hair, st === 'chanel' || st === 'longo' ? 0.85 : F);
  }
  if (st === 'liso') mesh(box(0.17, 0.035, 0.05), hair, head, [0, 0.105, 0.085], [0.5, 0, 0]); // franja
  if (st === 'longo') {
    const back = mesh(new THREE.CapsuleGeometry(0.105, 0.22, 6, 14), hair, head, [0, -0.15, -0.07]); back.scale.set(1.2, 1, 0.5);
    [-1, 1].forEach(s => { const lk = mesh(new THREE.CapsuleGeometry(0.03, 0.2, 4, 8), hair, head, [s * 0.112, -0.13, 0.03]); lk.rotation.z = s * 0.06; });
  }
  if (st === 'coque') mesh(new THREE.SphereGeometry(0.062, 16, 12), hair, head, [0, 0.09, -0.12]);
  if (st === 'chanel') mesh(box(0.2, 0.03, 0.05), hair, head, [0, 0.11, 0.08], [0.55, 0, 0.12]);
  // sobrancelhas
  [-1, 1].forEach(s => mesh(box(0.038, 0.009, 0.01), mat(d.barbaCor && st === 'grisalho' ? d.barbaCor : d.cabelo, { roughness: 1 }), head, [s * 0.044, 0.052, 0.114], [0, 0, s * (d.mulher ? -0.12 : 0.05)]));
  if (d.barba) { const b = mesh(new THREE.SphereGeometry(0.127, 18, 12, Math.PI * 0.05, Math.PI * 0.9, Math.PI * 0.62, Math.PI * 0.3), mat(d.barbaCor || d.cabelo, { roughness: 0.95 }), head, [0, 0.0, 0.01]); b.rotation.y = Math.PI * 0.5 - Math.PI * 0.5; b.scale.set(0.98, 1.1, 1.02); }
  if (d.bigode) mesh(box(0.07, 0.016, 0.02), hair, head, [0, -0.035, 0.118]);
  root.traverse(o => { if (o.isMesh) { o.castShadow = true; o.userData.dirId = d.id; } });
  return P;
}
function poseSit(P, t = 0) {
  P.pelvis.position.set(0, 0.55, -0.02);
  P.legs.forEach(l => l.rotation.set(-Math.PI / 2 + 0.05, 0, 0));
  P.knees.forEach(k => k.rotation.set(Math.PI / 2 - 0.05, 0, 0));
  P.shoulders.forEach((s, i) => { s.rotation.set(-0.45, 0, (i ? -1 : 1) * 0.12); });
  P.elbows.forEach(e => e.rotation.set(-1.0, 0, 0));
  P.pelvis.rotation.x = 0.04 + Math.sin(t * 0.8) * 0.012;
  P.head.rotation.y = Math.sin(t * 0.37) * 0.25;
  P.head.rotation.x = Math.sin(t * 0.23) * 0.06;
}
function poseStand(P, phase, moving) {
  const sw = moving ? Math.sin(phase) * 0.45 : 0;
  P.pelvis.position.set(0, 0.94 + (moving ? Math.abs(Math.cos(phase)) * 0.025 : 0), 0);
  P.legs[0].rotation.set(sw, 0, 0); P.legs[1].rotation.set(-sw, 0, 0);
  P.knees[0].rotation.set(Math.max(0, -sw) * 0.9, 0, 0); P.knees[1].rotation.set(Math.max(0, sw) * 0.9, 0, 0);
  P.shoulders[0].rotation.set(-sw * 0.7, 0, 0.08); P.shoulders[1].rotation.set(sw * 0.7, 0, -0.08);
  P.elbows.forEach(e => e.rotation.set(-0.25, 0, 0));
  P.pelvis.rotation.x = 0; P.head.rotation.set(0, 0, 0);
}

// ---------- cadeira ----------
function chair(d) {
  const c = new THREE.Group();
  mesh(box(0.58, 0.12, 0.56), M.leather, c, [0, 0.47, 0]);
  const back = mesh(box(0.62, 0.82, 0.12), M.leather, c, [0, 0.93, -0.3], [-0.06, 0, 0]);
  for (let i = 0; i < 3; i++) for (let j = 0; j < 5; j++) mesh(new THREE.SphereGeometry(0.012, 6, 4), M.goldDim, back, [-0.22 + j * 0.11, -0.3 + i * 0.16, 0.062], null, false);
  mesh(box(0.66, 0.04, 0.15), M.gold, back, [0, 0.43, 0]);
  mesh(box(0.6, 0.19, 0.012), M.gold, back, [0, 0.27, -0.066], null, false);
  const plate = mesh(new THREE.PlaneGeometry(0.57, 0.17), new THREE.MeshBasicMaterial({ map: plateTex(d) }), back, [0, 0.27, -0.073], [0, Math.PI, 0], false);
  [-1, 1].forEach(s => { mesh(box(0.08, 0.06, 0.5), M.leatherDark, c, [s * 0.33, 0.7, 0.0]); mesh(box(0.03, 0.2, 0.03), M.chrome, c, [s * 0.33, 0.58, 0.05]); });
  mesh(cyl(0.035, 0.035, 0.36, 12), M.chrome, c, [0, 0.24, 0]);
  for (let i = 0; i < 5; i++) { const a = i * Math.PI * 2 / 5; const leg = mesh(box(0.05, 0.035, 0.33), M.chrome, c, [Math.sin(a) * 0.16, 0.06, Math.cos(a) * 0.16], [0, a, 0]); mesh(new THREE.SphereGeometry(0.03, 8, 6), M.black, c, [Math.sin(a) * 0.31, 0.03, Math.cos(a) * 0.31]); }
  c.traverse(o => { if (o.isMesh) o.userData.dirId = d.id; });
  return c;
}

// ---------- objetos de mesa ----------
const smoke = [];
const smokeTex = tex(64, 64, (g, w) => { const gr = g.createRadialGradient(32, 32, 0, 32, 32, 32); gr.addColorStop(0, 'rgba(220,220,220,.5)'); gr.addColorStop(1, 'rgba(220,220,220,0)'); g.fillStyle = gr; g.fillRect(0, 0, 64, 64); });
function screenTex(kind) {
  return tex(256, 170, (g, w, h) => {
    g.fillStyle = '#0b1220'; g.fillRect(0, 0, w, h);
    if (kind === 'chart') {
      g.strokeStyle = '#2a3a5a'; for (let i = 1; i < 5; i++) { g.beginPath(); g.moveTo(10, i * 34); g.lineTo(w - 10, i * 34); g.stroke(); }
      g.strokeStyle = '#c6ff00'; g.lineWidth = 4; g.beginPath(); [150, 135, 140, 110, 100, 82, 70, 48, 30].forEach((y, i) => i ? g.lineTo(14 + i * 29, y) : g.moveTo(14, y)); g.stroke();
      g.fillStyle = '#287af5'; [40, 70, 55, 90, 110].forEach((v, i) => g.fillRect(140 + i * 22, h - 10 - v * .5, 14, v * .5));
    } else if (kind === 'flow') {
      g.fillStyle = '#287af5'; [[20, 30], [100, 30], [180, 30], [60, 105], [140, 105]].forEach(([x, y]) => g.fillRect(x, y, 56, 34));
      g.strokeStyle = '#c6ff00'; g.lineWidth = 3; g.beginPath(); g.moveTo(76, 47); g.lineTo(100, 47); g.moveTo(156, 47); g.lineTo(180, 47); g.moveTo(128, 64); g.lineTo(100, 105); g.stroke();
    } else { // phone
      g.fillStyle = '#16233d'; g.fillRect(0, 0, w, h);
      for (let i = 0; i < 4; i++) { g.fillStyle = i % 2 ? '#287af5' : '#c6ff00'; g.fillRect(16, 16 + i * 38, w - 32 - (i % 2) * 60, 26); }
    }
  });
}
const props = {
  laptop(p, x, z) {
    const g = new THREE.Group(); g.position.set(x, TOP_Y, z); g.rotation.y = Math.PI; p.add(g);
    mesh(box(0.36, 0.018, 0.25), M.chrome, g, [0, 0.009, 0]);
    mesh(box(0.3, 0.002, 0.1), M.black, g, [0, 0.019, -0.03], null, false);
    const hinge = new THREE.Group(); hinge.position.set(0, 0.018, 0.125); hinge.rotation.x = 0.3; g.add(hinge);
    mesh(box(0.36, 0.23, 0.012), M.chrome, hinge, [0, 0.115, 0]);
    mesh(new THREE.PlaneGeometry(0.33, 0.2), new THREE.MeshBasicMaterial({ map: screenTex('chart') }), hinge, [0, 0.115, -0.0065], [0, Math.PI, 0], false);
    const glow = new THREE.PointLight(0x6fa0ff, 0.6, 1.2, 2); glow.position.set(0, 0.15, -0.1); hinge.add(glow);
  },
  whisky(p, x, z) {
    const g = new THREE.Group(); g.position.set(x, TOP_Y, z); p.add(g);
    mesh(cyl(0.042, 0.038, 0.095, 24), M.glass, g, [0, 0.0475, 0], null, false);
    mesh(cyl(0.037, 0.034, 0.045, 24), M.amber, g, [0, 0.026, 0], null, false);
    mesh(box(0.032, 0.032, 0.032), M.ice, g, [0.006, 0.05, 0.004], [0.3, 0.5, 0.2], false);
    mesh(cyl(0.039, 0.039, 0.012, 24), M.glass, g, [0, 0.006, 0], null, false);
  },
  espresso(p, x, z) {
    const g = new THREE.Group(); g.position.set(x, TOP_Y, z); p.add(g);
    mesh(cyl(0.065, 0.06, 0.012, 24), M.porcelain, g, [0, 0.006, 0]);
    mesh(cyl(0.035, 0.028, 0.055, 20), M.porcelain, g, [0, 0.04, 0]);
    mesh(cyl(0.031, 0.031, 0.004, 20), M.coffee, g, [0, 0.066, 0], null, false);
    mesh(new THREE.TorusGeometry(0.016, 0.005, 8, 16), M.porcelain, g, [0.04, 0.042, 0], [0, 0, Math.PI / 2]);
  },
  cigar(p, x, z) {
    const g = new THREE.Group(); g.position.set(x, TOP_Y, z); p.add(g);
    mesh(cyl(0.075, 0.065, 0.028, 32), mat(0x1a1a1f, { roughness: 0.15, metalness: 0.3 }), g, [0, 0.014, 0]);
    mesh(cyl(0.05, 0.05, 0.004, 24), mat(0x6e6a64, { roughness: 1 }), g, [0, 0.029, 0], null, false);
    const c = mesh(cyl(0.012, 0.012, 0.16, 12), M.cigar, g, [0.035, 0.04, 0], [0, 0, Math.PI / 2 - 0.12]);
    mesh(cyl(0.0125, 0.0125, 0.018, 12), M.gold, c, [0, 0.03, 0], null, false);
    const tip = mesh(new THREE.SphereGeometry(0.0125, 10, 8), M.ember, g, [-0.044, 0.03, 0], null, false);
    const tipW = new THREE.Vector3(); tip.updateWorldMatrix(true, false);
    smoke.push({ tip, parts: Array.from({ length: 10 }, (_, i) => { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: smokeTex, transparent: true, depthWrite: false, opacity: 0 })); s.userData.t = i / 10; scene.add(s); return s; }) });
  },
  money(p, x, z) {
    const g = new THREE.Group(); g.position.set(x, TOP_Y, z); g.rotation.y = 0.25; p.add(g);
    const stack = (sx, sz, n, r) => { for (let i = 0; i < n; i++) { const b = mesh(box(0.165, 0.028, 0.075), M.cash, g, [sx, 0.014 + i * 0.029, sz], [0, r + (Math.random() - .5) * 0.08, 0]); mesh(box(0.03, 0.03, 0.077), M.band, b, [0, 0, 0], null, false); } };
    stack(0, 0, 4, 0); stack(0.17, 0.01, 3, 0.1); stack(0.08, 0.09, 2, -0.15); stack(0.08, 0.04, 1, 0.5);
  },
  phone(p, x, z, white) {
    const g = new THREE.Group(); g.position.set(x, TOP_Y, z); g.rotation.y = Math.PI + 0.3; p.add(g);
    mesh(box(0.075, 0.009, 0.155), white ? M.porcelain : M.black, g, [0, 0.0045, 0]);
    mesh(new THREE.PlaneGeometry(0.066, 0.145), new THREE.MeshBasicMaterial({ map: screenTex('phone') }), g, [0, 0.0095, 0], [-Math.PI / 2, 0, 0], false);
  },
  phone2(p, x, z) { props.phone(p, x - 0.06, z, false); props.phone(p, x + 0.07, z + 0.03, true); },
  tablet(p, x, z) {
    const g = new THREE.Group(); g.position.set(x, TOP_Y, z); g.rotation.y = Math.PI + 0.15; p.add(g);
    mesh(box(0.25, 0.008, 0.18), M.black, g, [0, 0.004, 0]);
    mesh(new THREE.PlaneGeometry(0.23, 0.16), new THREE.MeshBasicMaterial({ map: screenTex('flow') }), g, [0, 0.0085, 0], [-Math.PI / 2, 0, 0], false);
  },
  notepad(p, x, z) {
    const g = new THREE.Group(); g.position.set(x, TOP_Y, z); g.rotation.y = Math.PI + 0.2; p.add(g);
    const t = tex(200, 280, (c, w, h) => { c.fillStyle = '#f1ead8'; c.fillRect(0, 0, w, h); c.strokeStyle = '#333'; c.lineWidth = 3; [[15, 20], [105, 20], [15, 110], [105, 110], [15, 200], [105, 200]].forEach(([x, y]) => c.strokeRect(x, y, 80, 70)); c.strokeStyle = '#c33'; c.beginPath(); c.moveTo(30, 60); c.lineTo(80, 40); c.stroke(); });
    mesh(box(0.2, 0.012, 0.28), M.porcelain, g, [0, 0.006, 0]);
    mesh(new THREE.PlaneGeometry(0.19, 0.27), new THREE.MeshStandardMaterial({ map: t, roughness: 0.9 }), g, [0, 0.0125, 0], [-Math.PI / 2, 0, 0], false);
    mesh(cyl(0.006, 0.006, 0.14, 8), M.gold, g, [0.13, 0.008, 0], [Math.PI / 2, 0, 0.2]);
  },
  newspaper(p, x, z) {
    const g = new THREE.Group(); g.position.set(x, TOP_Y, z); g.rotation.y = Math.PI - 0.35; p.add(g);
    const t = tex(300, 220, (c, w, h) => { c.fillStyle = '#e4dfd2'; c.fillRect(0, 0, w, h); c.fillStyle = '#222'; c.font = '700 26px Georgia'; c.fillText('MERCADO', 14, 34); c.fillRect(14, 44, w - 28, 3); for (let i = 0; i < 14; i++) c.fillRect(14 + (i % 2) * 140, 60 + Math.floor(i / 2) * 22, 126, 6); });
    mesh(box(0.3, 0.008, 0.22), mat(0xe4dfd2), g, [0, 0.004, 0]);
    mesh(new THREE.PlaneGeometry(0.29, 0.21), new THREE.MeshStandardMaterial({ map: t, roughness: 1 }), g, [0, 0.0085, 0], [-Math.PI / 2, 0, 0], false);
  },
  calculator(p, x, z) {
    const g = new THREE.Group(); g.position.set(x, TOP_Y, z); g.rotation.y = Math.PI - 0.2; p.add(g);
    const t = tex(90, 140, (c, w, h) => { c.fillStyle = '#1a1a1a'; c.fillRect(0, 0, w, h); c.fillStyle = '#9fbf8a'; c.fillRect(8, 8, w - 16, 30); for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) { c.fillStyle = j === 3 ? '#c9a45c' : '#555'; c.fillRect(10 + j * 19, 48 + i * 22, 15, 16); } });
    mesh(box(0.09, 0.016, 0.14), M.black, g, [0, 0.008, 0]);
    mesh(new THREE.PlaneGeometry(0.085, 0.135), new THREE.MeshStandardMaterial({ map: t }), g, [0, 0.0165, 0], [-Math.PI / 2, 0, 0], false);
  },
};
// posições dos objetos na frente de cada diretor (local: diretor olha pra +Z)
const SLOTS = [[0, 0.78], [-0.3, 0.66], [0.3, 0.68]];

// ---------- monta a diretoria ----------
const N = DIRETORES.length, SEAT_R = 2.86;
const seats = [];
const pickables = [];
DIRETORES.forEach((d, i) => {
  const a = -Math.PI / 2 + i * 2 * Math.PI / N;
  const frame = new THREE.Group();
  frame.position.set(Math.cos(a) * SEAT_R, 0, Math.sin(a) * SEAT_R);
  frame.lookAt(0, 0, 0);
  scene.add(frame);
  const ch = chair(d); frame.add(ch);
  const P = person(d); frame.add(P.root); poseSit(P);
  d.props.forEach((k, j) => { const [x, z] = SLOTS[j]; props[k](frame, x, z); });
  ch.traverse(o => o.isMesh && pickables.push(o)); P.root.traverse(o => o.isMesh && pickables.push(o));
  seats.push({ d, a, frame, chair: ch, P, state: 'sit', path: null, t0: 0, phase: Math.random() * 10, seed: Math.random() * 100 });
});

// ---------- vida no escritório: levantar, ir ao banheiro, voltar ----------
const ticker = document.getElementById('ticker');
function log(msg) {
  const li = document.createElement('li'); li.textContent = msg; ticker.prepend(li);
  while (ticker.children.length > 4) ticker.lastChild.remove();
  requestAnimationFrame(() => li.classList.add('in'));
}
const WALK_R = 4.15;
const doorAng = Math.atan2(DOOR.z, DOOR.x - 1);
function toLocal(frame, v) { return frame.worldToLocal(v.clone()); }
function buildPath(s) {
  const pts = [];
  const out = new THREE.Vector3(Math.cos(s.a) * WALK_R, 0, Math.sin(s.a) * WALK_R);
  pts.push(new THREE.Vector3(Math.cos(s.a) * (SEAT_R + 0.55), 0, Math.sin(s.a) * (SEAT_R + 0.55)));
  pts.push(out);
  let a0 = s.a, a1 = doorAng; let da = Math.atan2(Math.sin(a1 - a0), Math.cos(a1 - a0));
  const steps = Math.max(1, Math.ceil(Math.abs(da) / 0.25));
  for (let k = 1; k <= steps; k++) { const aa = a0 + da * k / steps; pts.push(new THREE.Vector3(Math.cos(aa) * (WALK_R + 0.2), 0, Math.sin(aa) * (WALK_R + 0.2))); }
  pts.push(new THREE.Vector3(DOOR.x - 1.1, 0, DOOR.z));
  pts.push(new THREE.Vector3(DOOR.x + 0.4, 0, DOOR.z));
  return pts;
}
let nextOuting = 6;
let doorOpen = 0;
function startOuting(now) {
  const free = seats.filter(s => s.state === 'sit' && (!selected || selected.d.id !== s.d.id));
  if (!free.length) return;
  const s = free[Math.floor(Math.random() * free.length)];
  s.state = 'standup'; s.t0 = now; s.path = buildPath(s); s.leg = 0; s.dir = 1;
  const first = s.d.nome.split(' ')[0];
  log(`${first} levantou pra ir ao banheiro`);
}
const tmpV = new THREE.Vector3();
function updatePerson(s, now, dt) {
  const P = s.P;
  if (s.state === 'sit') { poseSit(P, now + s.seed); P.root.position.set(0, 0, 0); P.root.rotation.set(0, 0, 0); s.chair.position.z = THREE.MathUtils.lerp(s.chair.position.z, 0, 0.1); return; }
  if (s.state === 'standup' || s.state === 'sitdown') {
    const k = Math.min(1, (now - s.t0) / 0.9); const e = s.state === 'standup' ? k : 1 - k;
    poseSit(P, now); const sitY = 0.55;
    P.pelvis.position.y = THREE.MathUtils.lerp(sitY, 0.94, e);
    P.legs.forEach(l => l.rotation.x = THREE.MathUtils.lerp(-Math.PI / 2 + 0.05, 0, e));
    P.knees.forEach(kk => kk.rotation.x = THREE.MathUtils.lerp(Math.PI / 2 - 0.05, 0, e));
    P.root.position.set(0, 0, -0.35 * e);
    s.chair.position.z = -0.25 * e;
    if (k >= 1) {
      if (s.state === 'standup') { s.state = 'walk'; s.wpos = s.frame.localToWorld(new THREE.Vector3(0, 0, -0.35)); }
      else { s.state = 'sit'; log(`${s.d.nome.split(' ')[0]} voltou pra mesa`); }
    }
    return;
  }
  if (s.state === 'walk') {
    const target = s.path[s.leg];
    tmpV.subVectors(target, s.wpos); tmpV.y = 0;
    const dist = tmpV.length(), spd = 1.15 * dt;
    if (dist < spd) {
      s.wpos.copy(target);
      if (s.dir === 1 && s.leg === s.path.length - 1) { s.state = 'away'; s.t0 = now; P.root.visible = false; }
      else if (s.dir === -1 && s.leg === 0) { s.state = 'turn'; s.t0 = now; }
      else s.leg += s.dir;
    } else s.wpos.addScaledVector(tmpV.normalize(), spd);
    s.phase += dt * 7.5;
    poseStand(P, s.phase, true);
    const local = toLocal(s.frame, s.wpos);
    P.root.position.copy(local);
    const dirL = toLocal(s.frame, s.wpos.clone().add(tmpV)).sub(local);
    const want = Math.atan2(dirL.x, dirL.z);
    P.root.rotation.y += Math.atan2(Math.sin(want - P.root.rotation.y), Math.cos(want - P.root.rotation.y)) * Math.min(1, dt * 10);
    return;
  }
  if (s.state === 'away') {
    if (now - s.t0 > 7) { s.state = 'walk'; s.dir = -1; s.leg = s.path.length - 2; P.root.visible = true; log(`${s.d.nome.split(' ')[0]} saiu do banheiro`); }
    return;
  }
  if (s.state === 'turn') {
    poseStand(P, 0, false);
    P.root.rotation.y += Math.atan2(Math.sin(0 - P.root.rotation.y), Math.cos(0 - P.root.rotation.y)) * Math.min(1, dt * 6);
    const local = toLocal(s.frame, s.wpos); P.root.position.lerp(new THREE.Vector3(0, 0, -0.35), Math.min(1, dt * 4));
    if (now - s.t0 > 0.7) { s.state = 'sitdown'; s.t0 = now; P.root.rotation.y = 0; }
  }
}

// ---------- rótulos HTML ----------
const labels = document.getElementById('labels');
seats.forEach(s => {
  const el = document.createElement('button'); el.className = 'tag'; el.type = 'button';
  el.innerHTML = `<b>${s.d.nome}</b><span>${s.d.setor}</span>`;
  el.addEventListener('click', e => { e.stopPropagation(); select(s); });
  labels.appendChild(el); s.tag = el;
});
const headW = new THREE.Vector3();
function updateLabels() {
  const w = app.clientWidth, h = app.clientHeight;
  seats.forEach(s => {
    if (!s.P.root.visible || !namesOn || selected === s) { s.tag.style.opacity = 0; s.tag.style.pointerEvents = 'none'; return; }
    s.P.head.getWorldPosition(headW); headW.y += 0.32;
    const toCam = headW.clone().sub(camera.position);
    headW.project(camera);
    const sy = (-headW.y * .5 + .5) * h, sx = (headW.x * .5 + .5) * w;
    const vis = headW.z < 1 && Math.abs(headW.x) < 1.1 && Math.abs(headW.y) < 1.1 && !(sy < 150 && sx < 470) && true;
    s.tag.style.opacity = vis ? (selected && selected !== s ? 0.35 : 1) : 0;
    s.tag.style.pointerEvents = vis ? 'auto' : 'none';
    s.tag.style.transform = `translate(-50%,-100%) translate(${(headW.x * .5 + .5) * w}px,${(-headW.y * .5 + .5) * h}px)`;
    s.tag.style.zIndex = String(1000 - Math.round(toCam.length() * 10));
    s.tag.classList.toggle('sel', selected === s);
  });
}

// ---------- seleção / câmera ----------
let selected = null, camFly = null, rotOn = true, namesOn = true;
const panel = document.getElementById('panel');
const ST = { on: 'Já rodando', part: 'Em parte', off: 'A criar' };
// equipe em holograma atrás da cadeira
let holo = null;
const holoMat = new THREE.ShaderMaterial({
  transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
  uniforms: { t: { value: 0 }, c: { value: new THREE.Color(0xffcf73) } },
  vertexShader: 'varying vec3 vN; varying vec3 vV; varying float vY; void main(){ vec4 mv = modelViewMatrix * vec4(position, 1.0); vN = normalize(normalMatrix * normal); vV = normalize(-mv.xyz); vY = (modelMatrix * vec4(position, 1.0)).y; gl_Position = projectionMatrix * mv; }',
  fragmentShader: 'uniform float t; uniform vec3 c; varying vec3 vN; varying vec3 vV; varying float vY; void main(){ float f = pow(1.0 - abs(dot(vN, vV)), 2.0); float scan = 0.7 + 0.3 * sin(vY * 120.0 - t * 5.0); gl_FragColor = vec4(c * (0.10 + f * 1.25) * scan, 1.0); }'
});
const holoRing = new THREE.MeshBasicMaterial({ color: 0xf0cf86, transparent: true, opacity: 0.7, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide });
const holoDisc = new THREE.MeshBasicMaterial({ color: 0xf0cf86, transparent: true, opacity: 0.12, blending: THREE.AdditiveBlending, depthWrite: false });
function showTeam(s) {
  hideTeam();
  const g = new THREE.Group(); s.frame.add(g);
  const n = s.d.subs.length, tags = [];
  s.d.subs.forEach((name, k) => {
    const ang = (k - (n - 1) / 2) * (n > 4 ? 0.42 : 0.55);
    const f = new THREE.Group(); f.position.set(Math.sin(ang) * 1.55, 0.42, -0.45 - Math.cos(ang) * 0.85); f.rotation.y = -ang * 0.6; g.add(f);
    mesh(new THREE.RingGeometry(0.16, 0.19, 40), holoRing, f, [0, 0.01, 0], [-Math.PI / 2, 0, 0], false);
    mesh(new THREE.CircleGeometry(0.16, 40), holoDisc, f, [0, 0.008, 0], [-Math.PI / 2, 0, 0], false);
    mesh(new THREE.CylinderGeometry(0.16, 0.05, 0.42, 24, 1, true), holoDisc, f, [0, -0.21, 0], null, false);
    const body = new THREE.Group(); f.add(body);
    [-0.06, 0.06].forEach(x => mesh(new THREE.CapsuleGeometry(0.035, 0.32, 4, 8), holoMat, body, [x, 0.2, 0], null, false));
    mesh(new THREE.CapsuleGeometry(0.09, 0.22, 4, 10), holoMat, body, [0, 0.55, 0], null, false).scale.set(1.25, 1, 0.75);
    mesh(new THREE.SphereGeometry(0.075, 14, 10), holoMat, body, [0, 0.85, 0], null, false);
    body.scale.set(1, 0.001, 1); body.userData.k = k;
    const t = document.createElement('div'); t.className = 'subtag'; t.innerHTML = `<b>${name}</b><span>Estagiário · 0 cotas</span>`; labels.appendChild(t);
    tags.push({ el: t, obj: body });
  });
  holo = { g, tags, t0: clock.elapsedTime };
}
function hideTeam() { if (!holo) return; holo.g.parent.remove(holo.g); holo.tags.forEach(t => t.el.remove()); holo = null; }
function setOffset() {
  const w = app.clientWidth, h = app.clientHeight;
  if (selected && !isMobile()) camera.setViewOffset(w, h, 190, 0, w, h);
  else if (selected && isMobile()) camera.setViewOffset(w, h, 0, h * 0.22, w, h);
  else camera.clearViewOffset();
}
function select(s) {
  if (selected === s) return deselect();
  selected = s; controls.autoRotate = false;
  const d = s.d;
  panel.innerHTML = `
    <button class="x" aria-label="Fechar">×</button>
    <span class="kick"><i class="st ${d.st}"></i>${d.setor} · ${ST[d.st]}</span>
    <h2>${d.nome}</h2>
    <p class="nick">“${d.apelido}” · ${d.cargo} · ${d.idade} anos</p>
    <blockquote>${d.frase}</blockquote>
    <h4>O que faz</h4>
    <p class="what">${d.faz}</p>
    <h4>Equipe · ${d.subs.length} subagentes</h4>
    <ol class="team">${d.subs.map((x, i) => `<li><i>${String(i + 1).padStart(2, '0')}</i><span>${x}</span><em>Estagiário · 0</em></li>`).join('')}</ol>
    <div class="merit"><div><b>0</b><span>Cotas no mês</span></div><div><b>Diretor</b><span>Cargo</span></div><div><b>20%</b><span>das cotas da equipe</span></div></div>
    <p class="trait"><b>Jeito:</b> ${d.perfil}</p>
    <p class="trait"><b>Na mesa:</b> ${d.mesa}</p>`;
  panel.querySelector('.x').onclick = deselect;
  panel.classList.add('open');
  panel.scrollTop = 0;
  showTeam(s); setOffset();
  const back = new THREE.Vector3(Math.cos(s.a), 0, Math.sin(s.a));
  const side = new THREE.Vector3(-Math.sin(s.a), 0, Math.cos(s.a));
  const seatW = new THREE.Vector3(Math.cos(s.a) * SEAT_R, 0, Math.sin(s.a) * SEAT_R);
  const pos = seatW.clone().addScaledVector(back, isMobile() ? -4.4 : -3.5).addScaledVector(side, 0.3); pos.y = isMobile() ? 3.0 : 2.55;
  const tgt = seatW.clone().addScaledVector(back, 0.5); tgt.y = 1.05;
  camFly = { pos, tgt };
}
function deselect() { selected = null; panel.classList.remove('open'); hideTeam(); setOffset(); camFly = { pos: HOME.pos.clone(), tgt: HOME.tgt.clone() }; setTimeout(() => { if (!selected) controls.autoRotate = rotOn; }, 1600); }
const ray = new THREE.Raycaster(), mouse = new THREE.Vector2();
let downAt = null;
renderer.domElement.addEventListener('pointerdown', e => { downAt = [e.clientX, e.clientY]; });
renderer.domElement.addEventListener('pointerup', e => {
  if (!downAt || Math.hypot(e.clientX - downAt[0], e.clientY - downAt[1]) > 6) return;
  const r = renderer.domElement.getBoundingClientRect();
  mouse.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
  ray.setFromCamera(mouse, camera);
  const hit = ray.intersectObjects(pickables, false).find(h => h.object.visible);
  if (hit) { const s = seats.find(x => x.d.id === hit.object.userData.dirId); if (s) select(s); }
});
renderer.domElement.addEventListener('pointermove', e => {
  const r = renderer.domElement.getBoundingClientRect();
  mouse.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
  ray.setFromCamera(mouse, camera);
  renderer.domElement.style.cursor = ray.intersectObjects(pickables, false).length ? 'pointer' : 'grab';
});

// botões
document.getElementById('bRot').onclick = e => { rotOn = !rotOn; controls.autoRotate = rotOn && !selected; e.currentTarget.classList.toggle('on', rotOn); };
document.getElementById('bNames').onclick = e => { namesOn = !namesOn; e.currentTarget.classList.toggle('on', namesOn); };
document.getElementById('bHome').onclick = () => { if (selected) deselect(); else camFly = { pos: HOME.pos.clone(), tgt: HOME.tgt.clone() }; };
const merit = document.getElementById('merit');
document.getElementById('bMerit').onclick = () => merit.classList.add('open');
merit.querySelector('.x').onclick = () => merit.classList.remove('open');
merit.addEventListener('click', e => { if (e.target === merit) merit.classList.remove('open'); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') { merit.classList.remove('open'); if (selected) deselect(); } });

// ---------- loop ----------
const clock = new THREE.Clock();
const ember = new THREE.Vector3();
function loop() {
  const dt = Math.min(clock.getDelta(), 0.05), now = clock.elapsedTime;
  if (camFly) {
    camera.position.lerp(camFly.pos, 1 - Math.pow(0.02, dt)); controls.target.lerp(camFly.tgt, 1 - Math.pow(0.02, dt));
    if (camera.position.distanceTo(camFly.pos) < 0.02) camFly = null;
  }
  controls.update();
  if (now > nextOuting) { startOuting(now); nextOuting = now + 16 + Math.random() * 14; }
  let wantDoor = 0;
  seats.forEach(s => { updatePerson(s, now, dt); if ((s.state === 'walk' || s.state === 'away') && s.wpos && s.wpos.distanceTo(DOOR) < 2.2) wantDoor = 1; if (s.state === 'away' && now - s.t0 < 1 || s.state === 'away' && now - s.t0 > 6.2) wantDoor = 1; });
  doorOpen += (wantDoor - doorOpen) * Math.min(1, dt * 4);
  doorPivot.rotation.y = doorOpen * 1.35;
  smoke.forEach(sm => {
    sm.tip.getWorldPosition(ember);
    sm.parts.forEach(p => {
      p.userData.t += dt * 0.22; if (p.userData.t > 1) p.userData.t -= 1;
      const t = p.userData.t;
      p.position.set(ember.x + Math.sin(now * 1.3 + t * 9) * 0.03 * t, ember.y + t * 0.55, ember.z + Math.cos(now + t * 7) * 0.03 * t);
      const sc = 0.04 + t * 0.16; p.scale.set(sc, sc, sc);
      p.material.opacity = Math.sin(t * Math.PI) * 0.22;
    });
  });
  M.ember.emissiveIntensity = 1.8 + Math.sin(now * 3) * 0.5;
  if (holo) {
    const w = app.clientWidth, h = app.clientHeight, v = new THREE.Vector3();
    holo.tags.forEach(t => {
      const k = Math.min(1, Math.max(0, (now - holo.t0 - t.obj.userData.k * 0.12) / 0.6)); const e = 1 - Math.pow(1 - k, 3);
      t.obj.scale.y = Math.max(0.001, e); t.obj.position.y = Math.sin(now * 1.6 + t.obj.userData.k) * 0.02;
      t.obj.getWorldPosition(v); v.y += 1.02 + (t.obj.userData.k % 2) * 0.2; v.project(camera);
      t.el.style.opacity = e * (v.z < 1 ? 1 : 0);
      t.el.style.transform = `translate(-50%,-100%) translate(${(v.x * .5 + .5) * w}px,${(-v.y * .5 + .5) * h}px)`;
    });
    holoMat.uniforms.t.value = now;
  }
  renderer.render(scene, camera);
  updateLabels();
  requestAnimationFrame(loop);
}
loop();
document.body.classList.add('ready');

window.addEventListener('resize', () => {
  camera.aspect = app.clientWidth / app.clientHeight; setOffset(); camera.updateProjectionMatrix();
  renderer.setSize(app.clientWidth, app.clientHeight);
});
// para testes: window.__mesa.select(i)
window.__mesa = { select: i => select(seats[i]), outing: () => startOuting(clock.elapsedTime), seats, camera, controls };
