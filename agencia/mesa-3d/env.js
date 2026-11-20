import * as THREE from 'three';
import { M, mat, phys, tex, mesh, box, rbox, cyl, sph, marbleTex, goldGrad, goldLogo, GOLD, lerp, clamp, smooth, blob } from './util.js';

export const ROOM = { x0: -12, x1: 12, z0: -9, z1: 9, H: 4.2 };
export const BATH = { x0: 8.6, x1: 12, z0: 3, z1: 9, door: [5.3, 6.5] };
export const TABLE_R = 2.75, TOP_Y = 0.76;

// pontos de destino das rotinas (x, z, direção pra onde olha)
export const SPOTS = {
  banheiroPorta: new THREE.Vector3(7.9, 0, 5.9),
  banheiro: new THREE.Vector3(10.3, 0, 6.4),
  uisque: new THREE.Vector3(-10.75, 0, 2.7),
  agua: new THREE.Vector3(-7.4, 0, 7.25),
  cafe: new THREE.Vector3(-10.8, 0, 7.25),
  janelaN1: new THREE.Vector3(3.6, 0, -8.15),
  janelaN2: new THREE.Vector3(-2.6, 0, -8.15),
  janelaL: new THREE.Vector3(11.1, 0, -3.8),
};

const OUT = m => { m = m.clone ? m.clone() : m; m.stencilWrite = true; m.stencilRef = 1; m.stencilFunc = THREE.EqualStencilFunc; m.stencilFail = m.stencilZFail = m.stencilZPass = THREE.KeepStencilOp; return m; };
const MASK = new THREE.MeshBasicMaterial({ colorWrite: false, depthWrite: false, side: THREE.DoubleSide, stencilWrite: true, stencilRef: 1, stencilFunc: THREE.AlwaysStencilFunc, stencilZPass: THREE.ReplaceStencilOp });
export function buildEnv(scene, renderer, LOGO, FAT) {
  const out = { solidWalls: [], bathWalls: [], updaters: [], southItems: [], westItems: [] };

  // ---------- céu ----------
  const skyU = { top: { value: new THREE.Color() }, hor: { value: new THREE.Color() }, sunDir: { value: new THREE.Vector3(0, 1, 0) }, sunCol: { value: new THREE.Color(1, .9, .7) }, sunAmt: { value: 1 } };
  const sky = new THREE.Mesh(new THREE.SphereGeometry(900, 24, 12), new THREE.ShaderMaterial({
    side: THREE.BackSide, depthWrite: false, uniforms: skyU,
    vertexShader: 'varying vec3 vP; void main(){ vP = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
    fragmentShader: `uniform vec3 top; uniform vec3 hor; uniform vec3 sunDir; uniform vec3 sunCol; uniform float sunAmt; varying vec3 vP;
      void main(){ float h = clamp(vP.y, -0.2, 1.0); vec3 c = mix(hor, top, pow(max(h,0.0), 0.55)); if (h < 0.0) c = mix(hor * 0.45, vec3(0.03, 0.032, 0.038), clamp(-h * 6.0, 0.0, 1.0));
      float d = max(dot(vP, normalize(sunDir)), 0.0); c += sunCol * (pow(d, 900.0) * 6.0 + pow(d, 12.0) * 0.35) * sunAmt; gl_FragColor = vec4(c, 1.0); }`
  }));
  sky.renderOrder = -10; OUT(sky.material); scene.add(sky);
  const starG = new THREE.BufferGeometry(); const sp = [];
  for (let i = 0; i < 500; i++) { const u = Math.random(), v = Math.random() * 0.9 + 0.08; const th = u * Math.PI * 2, ph = Math.acos(v); sp.push(Math.sin(ph) * Math.cos(th) * 850, Math.cos(ph) * 850, Math.sin(ph) * Math.sin(th) * 850); }
  starG.setAttribute('position', new THREE.Float32BufferAttribute(sp, 3));
  const stars = new THREE.Points(starG, OUT(new THREE.PointsMaterial({ color: 0xffffff, size: 1.6, sizeAttenuation: false, transparent: true, opacity: 0.8, depthWrite: false })));
  scene.add(stars);
  const moon = mesh(sph(14, 24, 16), OUT(new THREE.MeshBasicMaterial({ color: 0xf2f0e6 })), scene, [-300, 420, -600], null, false);

  // ---------- cidade ----------
  const GROUND = -115;
  const city = new THREE.Group(); scene.add(city);
  const streetTex = tex(512, 512, (g, w, h) => {
    g.fillStyle = '#1b1c1f'; g.fillRect(0, 0, w, h);
    g.fillStyle = '#2b2c30'; for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) g.fillRect(i * 128 + 16, j * 128 + 16, 96, 96);
    g.fillStyle = 'rgba(255,255,255,.25)'; for (let i = 0; i < 4; i++) for (let k = 0; k < 128; k += 16) { g.fillRect(i * 128 + 2, k + i * 0, 1, 8); g.fillRect(k, i * 128 + 2, 8, 1); }
  }, [60, 60]);
  const groundM = OUT(mat(0xffffff, { map: streetTex, roughness: 0.95 }));
  mesh(new THREE.PlaneGeometry(4000, 4000), groundM, city, [0, GROUND, 0], [-Math.PI / 2, 0, 0], false);
  // fachadas: vidro com caixilho, 8 colunas x 24 andares por ladrilho (≈12 m x 84 m)
  const facade = (seed) => {
    const day = document.createElement('canvas'), em = document.createElement('canvas'); day.width = em.width = 256; day.height = em.height = 512;
    const g = day.getContext('2d'), e = em.getContext('2d');
    const glass = [['#3d5368', '#7c93a8'], ['#2a3340', '#5a6878'], ['#5b6670', '#a9b4bd'], ['#1f2a36', '#46607a'], ['#6a6258', '#b8ad9c']][seed % 5];
    const frame = ['#1b1f24', '#2b2f35', '#d9d4ca', '#14181d', '#3a332c'][seed % 5];
    g.fillStyle = frame; g.fillRect(0, 0, 512, 1024); e.fillStyle = '#000'; e.fillRect(0, 0, 512, 1024);
    const cols = 8, rows = 24, cw = 256 / cols, rh = 512 / rows;
    // blocos de andares acesos (escritórios inteiros acendem juntos)
    const litRows = new Set(); for (let r = 0; r < rows; r++) if (Math.random() < 0.28) litRows.add(r);
    for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
      const x = c * cw + 2, y = r * rh + 2, w = cw - 4, h = rh - 4;
      const gr = g.createLinearGradient(x, y, x + w, y + h); gr.addColorStop(0, glass[1]); gr.addColorStop(0.55, glass[0]); gr.addColorStop(1, glass[0]);
      g.fillStyle = gr; g.fillRect(x, y, w, h);
      const lit = litRows.has(r) ? Math.random() < 0.8 : Math.random() < 0.06;
      if (lit) { const warm = Math.random() < 0.75; const k = 0.55 + Math.random() * 0.45; e.fillStyle = warm ? `rgba(255,${190 + Math.random() * 40},${120 + Math.random() * 50},${k})` : `rgba(190,215,255,${k})`; e.fillRect(x, y, w, h); }
    }
    for (let r = 0; r <= rows; r += 6) { g.fillStyle = frame; g.fillRect(0, r * rh - 1, 256, 3); }
    const T = new THREE.CanvasTexture(day), E = new THREE.CanvasTexture(em); T.colorSpace = E.colorSpace = THREE.SRGBColorSpace;
    T.anisotropy = E.anisotropy = 4; T.wrapS = T.wrapT = E.wrapS = E.wrapT = THREE.RepeatWrapping; return [T, E];
  };
  const faces = [0, 1, 3].map(facade);
  const cityMats = [];
  const bGeo = new THREE.BoxGeometry(1, 1, 1); bGeo.translate(0, 0.5, 0);
  // tira as faces de cima/baixo do mapeamento de janelas (topo liso)
  const roofM = OUT(mat(0x23262b, { roughness: 0.8 }));
  const rnd = (a, b) => a + Math.random() * (b - a);
  const towers = []; // [x, z, w, d, h, rot]
  for (let i = 0; i < 520; i++) {
    const ang = Math.random() * Math.PI * 2, r = 160 + Math.pow(Math.random(), 0.8) * 800;
    const x = Math.cos(ang) * r, z = Math.sin(ang) * r;
    // perto: mais baixo (vista por cima); faixa média: arranha-céus; longe: mistura
    const tall = r < 340 ? rnd(35, 100) : r < 720 ? (Math.random() < 0.17 ? rnd(170, 300) : rnd(60, 125)) : (Math.random() < 0.08 ? rnd(150, 240) : rnd(60, 120));
    let h = tall;
    if (h > 150 && towers.some(t => t[4] > 150 && Math.hypot(t[0] - x, t[1] - z) < 220)) h = rnd(60, 120); // nada de torres altas gêmeas lado a lado
    const w = h > 150 ? [20, 28, 36][Math.floor(Math.random() * 3)] : [18, 24, 30][Math.floor(Math.random() * 3)], d = h > 150 ? [22, 30, 40][Math.floor(Math.random() * 3)] : [18, 24, 30][Math.floor(Math.random() * 3)];
    towers.push([x, z, w, d, h, Math.random() < 0.15 ? 0.35 : Math.round(Math.random() * 3) * Math.PI / 2]);
  }
  // classes de altura (cada uma com sua escala de textura, janelas sempre do mesmo tamanho)
  const HCL = [50, 100, 160, 230, 300];
  HCL.forEach((hc, ci) => {
    faces.forEach(([T, E], fi) => {
      const mine = towers.filter((t, k) => k % 3 === fi && HCL.reduce((best, h, j) => Math.abs(h - t[4]) < Math.abs(HCL[best] - t[4]) ? j : best, 0) === ci);
      if (!mine.length) return;
      const t = T.clone(), e = E.clone(); t.needsUpdate = e.needsUpdate = true; t.repeat.set(2, hc / 84); e.repeat.set(2, hc / 84);
      const m = OUT(new THREE.MeshLambertMaterial({ map: t, emissive: 0xffffff, emissiveMap: e, emissiveIntensity: 1 }));
      cityMats.push(m);
      const im = new THREE.InstancedMesh(bGeo, [m, m, roofM, roofM, m, m], mine.length);
      const dd = new THREE.Object3D();
      mine.forEach(([x, z, w, d, h, rot], k) => { dd.position.set(x, GROUND, z); dd.rotation.y = rot; dd.scale.set(w, hc, d); dd.updateMatrix(); im.setMatrixAt(k, dd.matrix); });
      city.add(im);
      mine.forEach(tw => tw.hc = hc);
    });
  });
  // antenas e luzes vermelhas no topo das torres altas
  const tallOnes = towers.filter(t => t.hc >= 180);
  const spireM = OUT(mat(0x8a8f96, { metalness: 0.9, roughness: 0.3 }));
  const spire = new THREE.InstancedMesh(new THREE.CylinderGeometry(0.4, 1.2, 1, 8).translate(0, 0.5, 0), spireM, tallOnes.length);
  const capM = OUT(mat(0x2a2e34, { roughness: 0.6 }));
  const cap = new THREE.InstancedMesh(bGeo, capM, tallOnes.length);
  const cap2 = new THREE.InstancedMesh(bGeo, capM, tallOnes.length);
  const redPos = [];
  tallOnes.forEach(([x, z, w, d, , rot], k) => {
    const top = GROUND + tallOnes[k].hc, sh = 12 + Math.random() * 30;
    const o = new THREE.Object3D(); o.position.set(x, top, z); o.rotation.y = rot; o.scale.set(w * 0.55, 8, d * 0.55); o.updateMatrix(); cap.setMatrixAt(k, o.matrix);
    const hasSpire = k % 3 === 0;
    if (!hasSpire) { o.position.set(x, top + 8, z); o.scale.set(w * 0.3, 14 + (k % 4) * 6, d * 0.3); o.updateMatrix(); spire.setMatrixAt(k, new THREE.Matrix4().makeScale(0, 0, 0)); cap2.setMatrixAt(k, o.matrix); redPos.push(x, top + 22 + (k % 4) * 6, z); }
    else { o.position.set(x, top + 8, z); o.scale.set(1, sh, 1); o.updateMatrix(); spire.setMatrixAt(k, o.matrix); cap2.setMatrixAt(k, new THREE.Matrix4().makeScale(0, 0, 0)); redPos.push(x, top + 8 + sh, z); }
  });
  city.add(spire, cap, cap2);
  const redG = new THREE.BufferGeometry(); redG.setAttribute('position', new THREE.Float32BufferAttribute(redPos, 3));
  const redM = OUT(new THREE.PointsMaterial({ color: 0xff2a1a, size: 5, sizeAttenuation: false, transparent: true, depthWrite: false }));
  const reds = new THREE.Points(redG, redM); city.add(reds);
  out.updaters.push((dt, now) => { redM.opacity = (Math.sin(now * 3) > 0.2 ? 1 : 0.15) * (out.isNight ? 1 : 0.6); });
  // morros no horizonte
  const hillG = new THREE.CylinderGeometry(1300, 1300, 1, 64, 1, true); const hp = hillG.attributes.position;
  for (let i = 0; i < hp.count; i++) { if (hp.getY(i) > 0) { const a = Math.atan2(hp.getZ(i), hp.getX(i)); hp.setY(i, 40 + Math.abs(Math.sin(a * 3) * 70 + Math.sin(a * 7.3) * 35 + Math.sin(a * 17) * 12)); } else hp.setY(i, -10); }
  hillG.computeVertexNormals();
  const hillM = OUT(new THREE.MeshBasicMaterial({ color: 0x1a2030, side: THREE.BackSide, fog: true }));
  const hills = new THREE.Mesh(hillG, hillM); hills.position.y = GROUND; city.add(hills);
  // torre onde fica o escritório (vista de baixo pelas janelas)
  mesh(box(26, -GROUND, 20), OUT(phys(0x1a2230, { roughness: 0.1, metalness: 0.6 })), city, [0, GROUND / 2 - 0.5, 0], null, false);
  // luzes das ruas
  const lampG = new THREE.BufferGeometry(); const lp = [];
  for (let i = -30; i <= 30; i++) for (let j = -30; j <= 30; j++) if ((i + j) % 2 === 0 && Math.random() < .5) lp.push(i * 32 + 16, GROUND + 0.5, j * 32 + 16);
  lampG.setAttribute('position', new THREE.Float32BufferAttribute(lp, 3));
  const lamps = new THREE.Points(lampG, OUT(new THREE.PointsMaterial({ color: 0xffc070, size: 3, sizeAttenuation: false, transparent: true, depthWrite: false })));
  city.add(lamps); city.traverse(o => { o.renderOrder = 50; });

  // ---------- chão, paredes, vidro ----------
  const floorT = marbleTex('#ddd7cd', 'rgba(96,90,82,A)', 34, 1024, [5, 4]);
  const floor = mesh(new THREE.PlaneGeometry(24, 18), phys(0xffffff, { map: floorT, roughness: 0.22, clearcoat: 0.6, clearcoatRoughness: 0.25 }), scene, [0, 0, 0], [-Math.PI / 2, 0, 0], false);
  floor.receiveShadow = true;
  // sombra de contato assada (escurece cantos, pé dos móveis e o entorno da mesa) — 1 malha, sem luz extra
  {
    const W = 1536, H = 1152, sx = x => (x + 12) / 24 * W, sz = z => (z + 9) / 18 * H, k = W / 24;
    const t = tex(W, H, (c) => {
      c.fillStyle = '#fff'; c.fillRect(0, 0, W, H);
      const edge = (x0, y0, x1, y1, a) => { const g = c.createLinearGradient(x0, y0, x1, y1); g.addColorStop(0, `rgba(70,62,54,${a})`); g.addColorStop(1, 'rgba(70,62,54,0)'); return g; };
      const e = 1.3 * k;
      c.fillStyle = edge(0, 0, 0, e, .7); c.fillRect(0, 0, W, e);
      c.fillStyle = edge(0, H, 0, H - e, .7); c.fillRect(0, H - e, W, e);
      c.fillStyle = edge(0, 0, e, 0, .7); c.fillRect(0, 0, e, H);
      c.fillStyle = edge(W, 0, W - e, 0, .7); c.fillRect(W - e, 0, e, H);
      const blob = (x, z, r, a) => { const g = c.createRadialGradient(sx(x), sz(z), 0, sx(x), sz(z), r * k); g.addColorStop(0, `rgba(60,52,44,${a})`); g.addColorStop(1, 'rgba(60,52,44,0)'); c.fillStyle = g; c.fillRect(sx(x) - r * k, sz(z) - r * k, 2 * r * k, 2 * r * k); };
      const ring = (r0, r1, a) => { const g = c.createRadialGradient(sx(0), sz(0), r0 * k, sx(0), sz(0), r1 * k); g.addColorStop(0, 'rgba(60,52,44,0)'); g.addColorStop(.45, `rgba(60,52,44,${a})`); g.addColorStop(1, 'rgba(60,52,44,0)'); c.fillStyle = g; c.fillRect(0, 0, W, H); };
      ring(TABLE_R - 0.4, TABLE_R + 1.8, .5);
      const box2 = (x0, z0, x1, z1, a) => { c.save(); c.filter = `blur(${0.35 * k}px)`; c.fillStyle = `rgba(60,52,44,${a})`; c.fillRect(sx(x0), sz(z0), sx(x1) - sx(x0), sz(z1) - sz(z0)); c.restore(); };
      box2(-12, -7.6 - 1.2, -11.2, 5.0, .35);        // estantes, TV, adega, armário e frigobar (parede oeste)
      box2(-12, 6.3, -9.6, 8.2, .3);                 // bancada do café
      blob(8, -6.4, 2.2, .3); blob(-8.4, -3.6, 2.4, .25); // lounges
      blob(-2.3, 7.45, 0.9, .35);                    // Hall da Fama
    });
    const ao = mesh(new THREE.PlaneGeometry(24, 18), new THREE.MeshBasicMaterial({ map: t, transparent: true, blending: THREE.MultiplyBlending, premultipliedAlpha: true, depthWrite: false, toneMapped: false }), scene, [0, 0.004, 0], [-Math.PI / 2, 0, 0], false);
    ao.renderOrder = 1; ao.userData.keep = true;
  }
  const blackMarble = marbleTex('#0e0e0f', 'rgba(220,220,220,A)', 22, 1024, [4, 1]);
  const bmM = phys(0xffffff, { map: blackMarble, roughness: 0.15, clearcoat: 1, clearcoatRoughness: 0.15 });
  [[0, -8.45, 24, 1.1], [0, 8.45, 24, 1.1], [-11.45, 0, 1.1, 18], [11.45, 0, 1.1, 18]].forEach(([x, z, w, d]) => mesh(new THREE.PlaneGeometry(w, d), bmM, scene, [x, 0.003, z], [-Math.PI / 2, 0, 0], false));
  [[0, -7.88, 22.9, 0.03], [0, 7.88, 22.9, 0.03], [-10.88, 0, 0.03, 15.8], [10.88, 0, 0.03, 15.8]].forEach(([x, z, w, d]) => mesh(new THREE.PlaneGeometry(w, d), M.gold, scene, [x, 0.005, z], [-Math.PI / 2, 0, 0], false));
  // borda da laje (vista de fora)
  mesh(box(24.4, 0.4, 18.4), mat(0x1c1c1e, { roughness: 0.5 }), scene, [0, -0.215, 0], null, false);
  const wallT = tex(512, 512, (g, w, h) => {
    g.fillStyle = '#f2efe9'; g.fillRect(0, 0, w, h);
    g.fillStyle = 'rgba(0,0,0,.03)'; for (let x = 0; x < w; x += 128) g.fillRect(x, 0, 2, h);
    g.fillStyle = '#c9a45c'; g.fillRect(0, h - 26, w, 3);
    g.fillStyle = '#e4e0d8'; g.fillRect(0, h - 23, w, 23);
  }, [8, 1]);
  const wallM = mat(0xffffff, { map: wallT, roughness: 0.85 });
  function wall(x0, z0, x1, z1, keyName) {
    const len = Math.hypot(x1 - x0, z1 - z0);
    const t = wallT.clone(); t.needsUpdate = true; t.repeat.set(len / 3, 1);
    const w = mesh(box(len, ROOM.H, 0.16), mat(0xffffff, { map: t, roughness: 0.85 }), scene, [(x0 + x1) / 2, ROOM.H / 2, (z0 + z1) / 2], [0, -Math.atan2(z1 - z0, x1 - x0), 0], false);
    w.receiveShadow = true; w.userData.key = keyName; return w;
  }
  // parede sul (com porta de entrada em x 2.6..4.6) e parede oeste: paredes sólidas que somem quando a câmera está do lado de fora
  out.solidWalls.push({ side: 'S', mesh: wall(-12, 9, 2.6, 9, 'S') }, { side: 'S', mesh: wall(4.6, 9, 8.6, 9, 'S') }, { side: 'W', mesh: wall(-12, -9, -12, 9, 'W') });
  const lintel = mesh(box(2.0, 1.2, 0.16), wallM, scene, [3.6, 3.6, 9], null, false); out.solidWalls.push({ side: 'S', mesh: lintel });
  // vidro do chão ao teto (norte e leste)
  const glassM = new THREE.MeshPhysicalMaterial({ color: 0xdfe9f2, roughness: 0.02, transparent: true, opacity: 0.08, depthWrite: false, side: THREE.DoubleSide });
  const mull = mat(0x1a1a1c, { roughness: 0.4, metalness: 0.6 });
  mesh(new THREE.PlaneGeometry(24, ROOM.H), glassM, scene, [0, ROOM.H / 2, -9], null, false);
  mesh(new THREE.PlaneGeometry(12, ROOM.H), glassM, scene, [12, ROOM.H / 2, -3], [0, -Math.PI / 2, 0], false);
  // máscara: só aqui aparece a vista de fora
  [mesh(new THREE.PlaneGeometry(24, ROOM.H), MASK, scene, [0, ROOM.H / 2, -9.01], null, false), mesh(new THREE.PlaneGeometry(12, ROOM.H), MASK, scene, [12.01, ROOM.H / 2, -3], [0, -Math.PI / 2, 0], false)].forEach(m => { m.renderOrder = -100; m.castShadow = false; m.receiveShadow = false; });
  for (let x = -12; x <= 12.01; x += 2) mesh(box(0.07, ROOM.H, 0.09), mull, scene, [x, ROOM.H / 2, -9], null, false);
  for (let z = -9; z <= 3.01; z += 2) mesh(box(0.09, ROOM.H, 0.07), mull, scene, [12, ROOM.H / 2, z], null, false);
  [[0, -9, 24, 0], [12, -3, 12, 1]].forEach(([x, z, l, rotY]) => { [0.04, ROOM.H - 0.04].forEach(y => mesh(rotY ? box(0.1, 0.08, l) : box(l, 0.08, 0.1), mull, scene, [x, y, z], null, false)); });

  // porta de entrada (vidro com moldura dourada)
  const entry = new THREE.Group(); entry.position.set(3.6, 0, 9); scene.add(entry); out.southItems.push(entry);
  [-0.5, 0.5].forEach(s => { mesh(new THREE.PlaneGeometry(0.98, 2.98), glassM, entry, [s, 1.5, 0], null, false); mesh(box(0.04, 3, 0.06), M.gold, entry, [s * 2, 1.5, 0], null, false); mesh(box(0.03, 0.9, 0.05), M.gold, entry, [s * 0.12, 1.2, -0.05], null, false); });
  mesh(box(2.04, 0.05, 0.06), M.gold, entry, [0, 3.0, 0], null, false);

  // ---------- banheiro (paredes próprias + teto; "ver banheiro" tira) ----------
  const bathWallM = phys(0xffffff, { map: marbleTex('#0e0e0f', 'rgba(220,220,220,A)', 18, 1024, [1, 1]), roughness: 0.15, clearcoat: 1, transparent: true, opacity: 1 });
  const bw = (x, z, w, d, h = ROOM.H) => { const m = mesh(box(w, h, d), bathWallM, scene, [x, h / 2, z], null, false); m.userData.keep = true; return m; };
  const bWest1 = bw(8.6, (3 + 5.3) / 2, 0.16, 2.3), bWest2 = bw(8.6, (6.5 + 9) / 2, 0.16, 2.5), bTop = bw(8.6, 5.9, 0.16, 1.2, 1.2); bTop.position.y = 3.6;
  const bNorth = bw(10.3, 3, 3.4, 0.16), bSouth = bw(10.3, 9, 3.4, 0.16), bEast = bw(12, 6, 0.16, 6);
  const roof = mesh(box(3.6, 0.08, 6.2), phys(0x121212, { roughness: 0.3, clearcoat: 0.6, transparent: true }), scene, [10.3, ROOM.H, 6], null, false);
  [[10.3, 2.98, 3.5], [10.3, 9.02, 3.5]].forEach(([x, z, w]) => mesh(box(w, 0.06, 0.06), M.gold, scene, [x, ROOM.H + 0.05, z], null, false)); mesh(box(0.06, 0.06, 6.1), M.gold, scene, [8.55, ROOM.H + 0.05, 6], null, false);
  out.bathWalls = [bSouth, bEast, roof]; out.bathAll = [bWest1, bWest2, bTop, bNorth, bSouth, bEast, roof];
  // porta do banheiro
  const bDoor = new THREE.Group(); bDoor.position.set(8.62, 0, 5.3); scene.add(bDoor);
  mesh(box(0.05, 2.35, 1.18), mat(0x1a1410, { roughness: 0.45 }), bDoor, [0, 1.18, 0.59], null, false);
  mesh(cyl(0.012, 0.012, 0.22, 8), M.gold, bDoor, [-0.05, 1.05, 1.02], null, false);
  out.bathDoor = bDoor;
  const wcTex = tex(256, 96, (g, w, h) => { g.fillStyle = '#111'; g.fillRect(0, 0, w, h); g.strokeStyle = '#d4b26a'; g.lineWidth = 3; g.strokeRect(5, 5, w - 10, h - 10); g.fillStyle = '#e9cf91'; g.font = '600 40px Inter, Arial'; g.textAlign = 'center'; g.fillText('W C', w / 2, 62); });
  mesh(new THREE.PlaneGeometry(0.5, 0.19), new THREE.MeshBasicMaterial({ map: wcTex }), scene, [8.51, 2.6, 5.9], [0, -Math.PI / 2, 0], false);
  // interior
  const bFloor = mesh(new THREE.PlaneGeometry(3.4, 6), phys(0xffffff, { map: marbleTex('#141414', 'rgba(200,200,200,A)', 18, 512, [1, 2]), roughness: 0.2, clearcoat: 0.8 }), scene, [10.3, 0.004, 6], [-Math.PI / 2, 0, 0], false);
  const vanity = new THREE.Group(); vanity.position.set(10.3, 0, 3.35); scene.add(vanity);
  mesh(rbox(2.4, 0.12, 0.55, 0.02), phys(0x101010, { roughness: 0.15, clearcoat: 1 }), vanity, [0, 0.86, 0.1]);
  mesh(rbox(2.3, 0.5, 0.5, 0.02), mat(0x2a1d14, { roughness: 0.5 }), vanity, [0, 0.55, 0.1]);
  [-0.55, 0.55].forEach(x => { mesh(cyl(0.2, 0.17, 0.12, 32), M.porcelain, vanity, [x, 0.98, 0.12]); mesh(cyl(0.012, 0.012, 0.22, 8), M.gold, vanity, [x, 1.08, -0.08]); mesh(cyl(0.01, 0.01, 0.14, 8), M.gold, vanity, [x, 1.18, 0.0], [Math.PI / 2, 0, 0]); });
  const mirror = mesh(cyl(0.55, 0.55, 0.02, 48), phys(0xc8d0d8, { metalness: 1, roughness: 0.05 }), vanity, [0, 1.85, -0.12], [Math.PI / 2, 0, 0]);
  mesh(new THREE.TorusGeometry(0.56, 0.025, 10, 64), M.gold, vanity, [0, 1.85, -0.1]);
  const wc = new THREE.Group(); wc.position.set(11.35, 0, 8.2); wc.rotation.y = -Math.PI / 2; scene.add(wc);
  mesh(rbox(0.42, 0.42, 0.62, 0.15, 4), M.porcelain, wc, [0, 0.21, 0.08]);
  mesh(rbox(0.44, 0.55, 0.2, 0.05), M.porcelain, wc, [0, 0.55, -0.26]);
  mesh(rbox(0.4, 0.04, 0.5, 0.02), M.porcelain, wc, [0, 0.44, 0.1]);
  mesh(box(0.02, 1.9, 1.4), new THREE.MeshPhysicalMaterial({ color: 0xffffff, transparent: true, opacity: 0.25, roughness: 0.3 }), scene, [10.5, 0.95, 7.9], null, false);
  plantPot(scene, 11.5, 4.1, 0.6);
  const towel = mesh(rbox(0.5, 0.7, 0.06, 0.02), mat(0xece4d4, { roughness: 1 }), scene, [11.9, 1.2, 5.5], [0, -Math.PI / 2, 0]);

  // ---------- tapete e mesa ----------
  // tapete de veludo preto: pelo com brilho que muda com o ângulo (sheen), fio de ouro na borda
  const rugT = tex(2048, 2048, (g, w, h) => {
    const cx = w / 2, cy = h / 2, R = w / 2;
    const base = g.createRadialGradient(cx, cy, 0, cx, cy, R);
    base.addColorStop(0, '#141216'); base.addColorStop(0.55, '#0d0c0f'); base.addColorStop(0.93, '#09080a'); base.addColorStop(1, '#060507');
    g.fillStyle = base; g.beginPath(); g.arc(cx, cy, R, 0, 7); g.fill();
    // "escovado" do veludo: listras radiais finíssimas, como pelo penteado pra fora
    g.save(); g.beginPath(); g.arc(cx, cy, R - 70, 0, 7); g.clip();
    for (let i = 0; i < 2600; i++) { const a = Math.random() * 6.2832, r0 = Math.random() * R * 0.9, l = 30 + Math.random() * 160;
      g.strokeStyle = `rgba(${Math.random() < .5 ? '255,255,255' : '0,0,0'},${Math.random() * .045})`; g.lineWidth = 1 + Math.random() * 1.5;
      g.beginPath(); g.moveTo(cx + Math.cos(a) * r0, cy + Math.sin(a) * r0); g.lineTo(cx + Math.cos(a) * (r0 + l), cy + Math.sin(a) * (r0 + l)); g.stroke(); }
    // marcas suaves de quem pisou (veludo amassado)
    for (let i = 0; i < 26; i++) { const x = cx + (Math.random() - .5) * R * 1.5, y = cy + (Math.random() - .5) * R * 1.5, rr = 60 + Math.random() * 160;
      const gr = g.createRadialGradient(x, y, 0, x, y, rr); gr.addColorStop(0, `rgba(255,255,255,${.012 + Math.random() * .02})`); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(x - rr, y - rr, rr * 2, rr * 2); }
    g.restore();
    // pontinhos de fibra
    for (let i = 0; i < 26000; i++) { g.fillStyle = `rgba(255,255,255,${Math.random() * .03})`; g.fillRect(Math.random() * w, Math.random() * h, 1.5, 1.5); }
    // borda: debrum em cordão de ouro duplo + faixa de veludo mais escura
    g.lineWidth = 46; g.strokeStyle = '#050405'; g.beginPath(); g.arc(cx, cy, R - 23, 0, 7); g.stroke();
    const gold = (r, lw, a) => { g.lineWidth = lw; g.strokeStyle = `rgba(214,180,108,${a})`; g.beginPath(); g.arc(cx, cy, r, 0, 7); g.stroke(); };
    gold(R - 50, 10, .85); gold(R - 50, 3, 1); gold(R - 78, 3, .7);
    for (let i = 0; i < 360; i++) { const a = i / 360 * 6.2832; g.fillStyle = `rgba(240,210,140,${.35 + (i % 2) * .3})`; g.beginPath(); g.arc(cx + Math.cos(a) * (R - 50), cy + Math.sin(a) * (R - 50), 2.4, 0, 7); g.fill(); }
  });
  const rugBump = tex(1024, 1024, (g, w, h) => {
    g.fillStyle = '#808080'; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 60000; i++) { const v = 100 + Math.random() * 60 | 0; g.fillStyle = `rgb(${v},${v},${v})`; g.fillRect(Math.random() * w, Math.random() * h, 1.2, 1.2); }
    g.lineWidth = 22; g.strokeStyle = '#d0d0d0'; g.beginPath(); g.arc(w / 2, h / 2, w / 2 - 25, 0, 7); g.stroke();
  });
  rugBump.colorSpace = THREE.NoColorSpace;
  const velvet = new THREE.MeshPhysicalMaterial({ map: rugT, color: 0xffffff, roughness: 0.92, metalness: 0, sheen: 1, sheenColor: new THREE.Color(0x4a3f52), sheenRoughness: 0.42, bumpMap: rugBump, bumpScale: 0.6, transparent: true });
  const rug = mesh(new THREE.CircleGeometry(5.3, 128), velvet, scene, [0, 0.006, 0], [-Math.PI / 2, 0, 0], false); rug.userData.keep = true;
  // borda com volume (o tapete tem espessura)
  const rim = mesh(new THREE.TorusGeometry(5.29, 0.022, 8, 160), new THREE.MeshPhysicalMaterial({ color: 0x0a090b, roughness: 0.8, sheen: 1, sheenColor: new THREE.Color(0x5a4d63), sheenRoughness: 0.35 }), scene, [0, 0.012, 0], [Math.PI / 2, 0, 0], false); rim.scale.z = 0.6; rim.userData.keep = true;
  const table = new THREE.Group(); scene.add(table); blob(scene, 0, 0, 3.4, 3.4, 0.45);
  const woodT = tex(1024, 1024, (g, w, h) => {
    g.fillStyle = '#1b130e'; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 220; i++) { g.strokeStyle = `rgba(${Math.random() < .5 ? '0,0,0' : '90,60,40'},${Math.random() * .22})`; g.lineWidth = Math.random() * 2.5; g.beginPath(); const y = Math.random() * h; g.moveTo(0, y); g.bezierCurveTo(w * .3, y + Math.random() * 30 - 15, w * .7, y + Math.random() * 30 - 15, w, y + Math.random() * 20 - 10); g.stroke(); }
  });
  mesh(cyl(TABLE_R, TABLE_R, 0.06, 64), phys(0xffffff, { map: woodT, roughness: 0.28, clearcoat: 1, clearcoatRoughness: 0.12 }), table, [0, TOP_Y - 0.03, 0]);
  mesh(new THREE.TorusGeometry(TABLE_R, 0.03, 6, 96), M.gold, table, [0, TOP_Y - 0.03, 0], [Math.PI / 2, 0, 0]);
  mesh(new THREE.TorusGeometry(TABLE_R - 0.36, 0.006, 6, 160), M.gold, table, [0, TOP_Y + 0.001, 0], [Math.PI / 2, 0, 0], false);
  mesh(cyl(0.7, 1.05, TOP_Y - 0.12, 64), M.blackGloss, table, [0, (TOP_Y - 0.12) / 2 + 0.06, 0]);
  mesh(new THREE.TorusGeometry(0.71, 0.015, 8, 64), M.gold, table, [0, TOP_Y - 0.08, 0], [Math.PI / 2, 0, 0], false);
  mesh(cyl(1.15, 1.2, 0.06, 64), M.goldDim, table, [0, 0.03, 0]);
  // luz embutida sob o tampo (ilumina o tapete, sem feixe no meio)
  const under = mesh(new THREE.TorusGeometry(TABLE_R - 0.1, 0.012, 6, 160), new THREE.MeshBasicMaterial({ color: 0xffd9a0 }), table, [0, TOP_Y - 0.065, 0], [Math.PI / 2, 0, 0], false);
  goldLogo(LOGO, 1024, { scale: 0.5, fn: (g, size, t) => {
    g.fillStyle = '#0c0907'; g.beginPath(); g.arc(size / 2, size / 2, size * .36, 0, 7); g.fill();
    g.strokeStyle = '#d4b26a'; g.lineWidth = size * .008; g.beginPath(); g.arc(size / 2, size / 2, size * .36, 0, 7); g.stroke();
    g.shadowColor = 'rgba(240,210,140,.5)'; g.shadowBlur = size * .02; g.drawImage(t, 0, 0); g.shadowBlur = 0;
    g.strokeStyle = 'rgba(212,178,106,.55)'; g.lineWidth = size * .003; g.beginPath(); g.arc(size / 2, size / 2, size * .44, 0, 7); g.stroke();
  } }).then(t => mesh(new THREE.PlaneGeometry(0.95, 0.95), new THREE.MeshStandardMaterial({ map: t, transparent: true, roughness: 0.45, emissive: 0xffffff, emissiveMap: t, emissiveIntensity: 0.18 }), table, [0, TOP_Y + 0.002, 0], [-Math.PI / 2, 0, 0], false));

  // halo pendente sobre a mesa (luz de cima sem feixe)
  const halo = new THREE.Group(); halo.position.y = 3.25; scene.add(halo);
  out.halo = halo; halo.userData.dyn = true; // não entra no bake: some inteiro na visão de cima
  const haloM = mat(0xfff0d8, { emissive: 0xffe2b0, emissiveIntensity: 2 });
  mesh(new THREE.TorusGeometry(2.2, 0.03, 6, 96), haloM, halo, null, [Math.PI / 2, 0, 0], false);
  mesh(new THREE.TorusGeometry(2.24, 0.012, 4, 96), M.gold, halo, [0, 0.03, 0], [Math.PI / 2, 0, 0], false);
  for (let i = 0; i < 3; i++) { const a = i * Math.PI * 2 / 3; mesh(cyl(0.004, 0.004, ROOM.H - 3.25, 6), M.black, halo, [Math.cos(a) * 2.2, (ROOM.H - 3.25) / 2, Math.sin(a) * 2.2], null, false); }

  // ---------- lounge (oeste) com TV de faturamento ----------
  const lounge = new THREE.Group(); scene.add(lounge);
  const boucle = phys(0xe9e2d4, { roughness: 0.95, sheen: 1, sheenColor: new THREE.Color(0xffffff), sheenRoughness: 0.8 });
  blob(scene, -7.4, -3.6, 0.8, 2.0); blob(scene, -9.3, -3.6, 0.95, 0.95);
  const sofa = new THREE.Group(); sofa.position.set(-7.4, 0, -3.6); sofa.rotation.y = -Math.PI / 2; lounge.add(sofa);
  mesh(rbox(3.4, 0.42, 1.0, 0.12, 4), boucle, sofa, [0, 0.21, 0]);
  mesh(rbox(3.4, 0.5, 0.26, 0.12, 4), boucle, sofa, [0, 0.62, 0.38]);
  [-1.58, 1.58].forEach(x => mesh(rbox(0.24, 0.6, 1.0, 0.1, 4), boucle, sofa, [x, 0.3, 0]));
  [-1.05, 0, 1.05].forEach(x => mesh(rbox(1.0, 0.16, 0.8, 0.07, 4), boucle, sofa, [x, 0.5, -0.04]));
  [-1.2, 1.2].forEach(x => mesh(rbox(0.42, 0.42, 0.14, 0.06, 4), phys(0xb08a45, { roughness: 0.6, sheen: 0.6 }), sofa, [x, 0.72, 0.18], [-0.2, 0, x > 0 ? -0.2 : 0.2]));
  const cognac = phys(0x6b3a1c, { roughness: 0.38, clearcoat: 0.5, sheen: 0.3 });
  [[-9.9, -6.4, 0.6], [-9.9, -0.8, -0.6 + Math.PI]].forEach(([x, z, r]) => {
    const a = new THREE.Group(); a.position.set(x, 0, z); a.rotation.y = r; lounge.add(a);
    mesh(rbox(0.85, 0.36, 0.8, 0.1, 4), cognac, a, [0, 0.38, 0]); mesh(rbox(0.85, 0.55, 0.2, 0.1, 4), cognac, a, [0, 0.72, -0.32], [-0.15, 0, 0]);
    [-0.4, 0.4].forEach(s => mesh(rbox(0.12, 0.3, 0.75, 0.05, 4), cognac, a, [s, 0.55, 0]));
    [[-0.35, -0.3], [0.35, -0.3], [-0.35, 0.3], [0.35, 0.3]].forEach(([lx, lz]) => mesh(cyl(0.02, 0.015, 0.22, 8), M.gold, a, [lx, 0.11, lz]));
  });
  const ct = new THREE.Group(); ct.position.set(-9.3, 0, -3.6); lounge.add(ct);
  mesh(cyl(0.75, 0.75, 0.05, 64), phys(0xffffff, { map: marbleTex('#141414', 'rgba(230,230,230,A)', 14, 512, [1, 1]), roughness: 0.1, clearcoat: 1 }), ct, [0, 0.42, 0]);
  mesh(cyl(0.3, 0.42, 0.4, 32), M.gold, ct, [0, 0.2, 0]);
  [[0x1a1a1a, 0.06], [0xc9a45c, 0.05], [0xf0ece4, 0.045]].reduce((y, [c, h]) => { mesh(rbox(0.32, h, 0.24, 0.005), mat(c, { roughness: 0.6 }), ct, [0.25, y + h / 2, 0.15], [0, 0.3, 0]); return y + h; }, 0.445);
  mesh(sph(0.09, 16, 12), M.gold, ct, [-0.2, 0.53, -0.1]);
  const lrug = mesh(new THREE.PlaneGeometry(5, 7.6), mat(0xd8d0c2, { roughness: 1 }), lounge, [-9.4, 0.007, -3.6], [-Math.PI / 2, 0, 0], false);
  // luminária de arco
  const arcLamp = new THREE.Group(); arcLamp.position.set(-7.0, 0, -6.2); lounge.add(arcLamp);
  mesh(cyl(0.22, 0.24, 0.06, 32), phys(0x111111, { roughness: 0.2, clearcoat: 1 }), arcLamp, [0, 0.03, 0]);
  const arcC = new THREE.CatmullRomCurve3([new THREE.Vector3(0, 0.05, 0), new THREE.Vector3(0, 1.6, 0), new THREE.Vector3(-0.6, 2.35, 0.4), new THREE.Vector3(-1.5, 2.2, 1.0), new THREE.Vector3(-1.9, 1.85, 1.3)]);
  mesh(new THREE.TubeGeometry(arcC, 40, 0.018, 8), M.gold, arcLamp);
  mesh(new THREE.SphereGeometry(0.26, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2), M.gold, arcLamp, [-1.9, 1.85, 1.3]);

  // parede da TV: painel de mármore preto com moldura dourada
  const tvWall = new THREE.Group(); tvWall.position.set(-11.9, 0, -3.6); tvWall.rotation.y = Math.PI / 2; scene.add(tvWall);
  const bmT = marbleTex('#0d0d0e', 'rgba(230,230,230,A)', 26, 1024, [1, 1]);
  mesh(box(5.6, ROOM.H, 0.06), phys(0xffffff, { map: bmT, roughness: 0.12, clearcoat: 1 }), tvWall, [0, ROOM.H / 2, 0], null, false);
  [-2.8, 2.8].forEach(x => mesh(box(0.05, ROOM.H, 0.08), M.gold, tvWall, [x, ROOM.H / 2, 0.01], null, false));
  mesh(box(5.0, 0.12, 0.35), M.goldDim, tvWall, [0, 0.5, 0.2], null, false);
  mesh(box(5.0, 0.4, 0.4), phys(0x2a1a10, { roughness: 0.35, clearcoat: 0.6 }), tvWall, [0, 0.2, 0.2], null, false);
  // TV de faturamento na parede oeste
  const tvCanvas = document.createElement('canvas'); tvCanvas.width = 1280; tvCanvas.height = 720; tvCanvas.style.imageRendering = 'auto';
  const tvTex = new THREE.CanvasTexture(tvCanvas); tvTex.colorSpace = THREE.SRGBColorSpace; tvTex.anisotropy = 8;
  const tv = new THREE.Group(); tv.position.set(-11.88, 2.1, -3.6); tv.rotation.y = Math.PI / 2; scene.add(tv); out.westItems.push(tv);
  mesh(rbox(3.9, 2.25, 0.07, 0.02), M.black, tv, [0, 0, 0]);
  mesh(new THREE.PlaneGeometry(3.8, 2.14), new THREE.MeshBasicMaterial({ map: tvTex, toneMapped: false }), tv, [0, 0, 0.037], null, false);
  let fatShown = 0;
  function drawTV(now) {
    const g = tvCanvas.getContext('2d'), W = 1280, H = 720;
    g.fillStyle = '#07090b'; g.fillRect(0, 0, W, H);
    const grd = g.createRadialGradient(W * .2, 0, 0, W * .2, 0, W); grd.addColorStop(0, 'rgba(40,120,70,.18)'); grd.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = grd; g.fillRect(0, 0, W, H);
    g.fillStyle = '#d4b26a'; g.font = '600 22px Inter, Arial'; g.fillText('CARNUCCI · MINHAMOTO', 48, 56);
    g.fillStyle = '#8f8a80'; g.font = '500 20px Inter, Arial';
    const hora = new Date().toLocaleTimeString('pt-BR', { timeZone: 'America/Sao_Paulo', hour: '2-digit', minute: '2-digit', second: '2-digit' });
    const selo = 'UTMIFY · ATUALIZADO EM ' + FAT.atualizado; g.textAlign = 'right'; g.fillText(selo, W - 48, 56); g.textAlign = 'left';
    g.fillStyle = '#d4b26a'; g.beginPath(); g.arc(W - 48 - g.measureText(selo).width - 16, 49, 7, 0, 7); g.fill();
    fatShown = FAT.valor;
    g.fillStyle = '#9b958a'; g.font = '600 24px Inter, Arial'; g.fillText('FATURAMENTO TOTAL', 48, 130);
    g.fillStyle = '#f4efe4'; g.font = '700 108px Inter, Arial'; g.fillText('R$ ' + Math.round(fatShown).toLocaleString('pt-BR'), 44, 238);
    g.fillStyle = '#3ddc84'; g.font = '600 26px Inter, Arial'; g.fillText('▲ faturamento total na UTMify', 50, 284);
    // linha de crescimento (verde)
    const lx = 48, ly = 330, lw = 700, lh = 320;
    g.strokeStyle = 'rgba(255,255,255,.08)'; g.lineWidth = 1; for (let i = 0; i <= 4; i++) { g.beginPath(); g.moveTo(lx, ly + i * lh / 4); g.lineTo(lx + lw, ly + i * lh / 4); g.stroke(); }
    const pts = []; for (let i = 0; i <= 24; i++) { const t = i / 24; pts.push([lx + t * lw, ly + lh - (Math.pow(t, 1.6) * 0.9 + Math.sin(i * 1.7) * 0.025 + 0.04) * lh]); }
    const reveal = Math.min(1, now / 3);
    const gl = g.createLinearGradient(0, ly, 0, ly + lh); gl.addColorStop(0, 'rgba(61,220,132,.35)'); gl.addColorStop(1, 'rgba(61,220,132,0)');
    g.save(); g.beginPath(); g.rect(lx, ly - 10, lw * reveal, lh + 20); g.clip();
    g.beginPath(); pts.forEach(([x, y], i) => i ? g.lineTo(x, y) : g.moveTo(x, y)); g.lineTo(lx + lw, ly + lh); g.lineTo(lx, ly + lh); g.closePath(); g.fillStyle = gl; g.fill();
    g.beginPath(); pts.forEach(([x, y], i) => i ? g.lineTo(x, y) : g.moveTo(x, y)); g.strokeStyle = '#3ddc84'; g.lineWidth = 5; g.stroke(); g.restore();
    // barras entradas x saídas (verde/vermelho)
    const bx = 800, by = 330, bh = 170;
    g.fillStyle = '#9b958a'; g.font = '600 18px Inter, Arial'; g.fillText('ENTRADAS x SAÍDAS · SEMANAS', bx, by - 12);
    for (let i = 0; i < 8; i++) {
      const v = [.45, .5, .55, .52, .62, .7, .74, .82][i] * reveal, c = [.25, .28, .3, .26, .3, .32, .3, .34][i] * reveal;
      g.fillStyle = '#3ddc84'; g.fillRect(bx + i * 54, by + bh - v * bh, 20, v * bh);
      g.fillStyle = '#ff5a5f'; g.fillRect(bx + i * 54 + 22, by + bh - c * bh, 20, c * bh);
    }
    // pizza por loja
    const px = 920, py = 610, pr = 82; const split = [['App Store', .58, '#3ddc84'], ['Google Play', .42, '#ff5a5f']];
    let a0 = -Math.PI / 2;
    split.forEach(([n, f, c]) => { g.beginPath(); g.moveTo(px, py); g.arc(px, py, pr, a0, a0 + f * Math.PI * 2 * reveal); g.closePath(); g.fillStyle = c; g.fill(); a0 += f * Math.PI * 2; });
    g.fillStyle = '#07090b'; g.beginPath(); g.arc(px, py, pr * .55, 0, 7); g.fill();
    split.forEach(([n, f, c], i) => { g.fillStyle = c; g.fillRect(1030, 568 + i * 44, 16, 16); g.fillStyle = '#e8e2d6'; g.font = '500 20px Inter, Arial'; g.fillText(`${n}  ${Math.round(f * 100)}%`, 1056, 584 + i * 44); });
    g.fillStyle = '#5f5a52'; g.font = '400 15px Inter, Arial'; g.fillText(FAT.fonte, 48, H - 24);
    tvTex.needsUpdate = true;
  }
  let tvT = 0;
  out.updaters.push((dt, now) => { tvT -= dt; if (tvT <= 0) { tvT = now < 4 ? 0.15 : 1.0; drawTV(now); } });

  // estantes ao lado da TV
  [[-7.6]].forEach(([zc]) => {
    const sh = new THREE.Group(); sh.position.set(-11.75, 0, zc); sh.rotation.y = Math.PI / 2; scene.add(sh); out.westItems.push(sh);
    mesh(box(2.2, 3.4, 0.4), mat(0x121212, { roughness: 0.4 }), sh, [0, 1.7, 0]);
    for (let i = 0; i < 5; i++) {
      const y = 0.35 + i * 0.66; mesh(box(2.1, 0.03, 0.36), M.goldDim, sh, [0, y, 0.03]);
      mesh(box(2.0, 0.01, 0.01), new THREE.MeshBasicMaterial({ color: 0xffd9a0 }), sh, [0, y + 0.6, 0.19], null, false);
      let x = -0.95; while (x < 0.9) { const w = 0.03 + Math.random() * 0.04, hh = 0.32 + Math.random() * 0.18; if (Math.random() < 0.75) mesh(box(w, hh, 0.24), mat([0x1a1a1a, 0xe8e0d0, 0x6b3a1c, 0x2c3e50, 0xb08a45, 0x7a1c1c][Math.floor(Math.random() * 6)], { roughness: 0.7 }), sh, [x, y + 0.015 + hh / 2, 0.04], [0, 0, Math.random() < .1 ? 0.15 : 0], false); else { mesh(sph(0.07 + Math.random() * 0.04, 16, 12), Math.random() < .5 ? M.gold : M.porcelain, sh, [x + 0.08, y + 0.1, 0.04], null, false); x += 0.18; } x += w + 0.008; }
    }
  });

  // ---------- bar e café (sul) ----------
  const bar = new THREE.Group(); bar.position.set(-9, 0, 8.45); scene.add(bar); blob(bar, 0, -0.1, 2.8, 0.6);
  mesh(rbox(5, 1.02, 0.7, 0.03), mat(0x111111, { roughness: 0.4 }), bar, [0, 0.51, 0]);
  for (let i = -24; i <= 24; i++) mesh(cyl(0.035, 0.035, 0.95, 8), mat(0x1a1a1a, { roughness: 0.35 }), bar, [i * 0.1, 0.5, -0.36], null, false);
  mesh(rbox(5.1, 0.06, 0.78, 0.01), phys(0xffffff, { map: marbleTex('#f2f0ec', 'rgba(120,120,120,A)', 14, 512, [2, 1]), roughness: 0.12, clearcoat: 1 }), bar, [0, 1.05, 0]);
  mesh(box(5.0, 0.02, 0.02), new THREE.MeshBasicMaterial({ color: 0xffd9a0 }), bar, [0, 0.12, -0.36], null, false);
  // prateleira de garrafas iluminada atrás
  const shelfBack = new THREE.Group(); bar.add(shelfBack); out.southItems.push(shelfBack);
  mesh(box(5, 1.6, 0.3), mat(0x0e0e0e, { roughness: 0.5 }), shelfBack, [0, 2.2, 0.38]);
  mesh(box(4.8, 1.3, 0.02), new THREE.MeshBasicMaterial({ color: 0xffcf8a }), shelfBack, [0, 2.2, 0.225], null, false);
  for (let i = 0; i < 16; i++) { const c = [0x6b3a12, 0x2f4a22, 0x8a5a1a, 0x5a1a14, 0x1a1a1a, 0xb8651a][i % 6]; const x = -2.2 + i * 0.29; const gm = phys(c, { roughness: 0.08, transparent: true, opacity: 0.85, clearcoat: 1 }); mesh(cyl(0.05, 0.055, 0.26, 16), gm, shelfBack, [x, 1.75, 0.3]); mesh(cyl(0.016, 0.02, 0.09, 12), gm, shelfBack, [x, 1.93, 0.3]); }
  // máquina de espresso
  const esp = new THREE.Group(); esp.position.set(-1.8, 1.08, 0.05); bar.add(esp);
  mesh(rbox(0.55, 0.4, 0.42, 0.04), M.chrome, esp, [0, 0.2, 0]); mesh(rbox(0.5, 0.05, 0.3, 0.01), M.black, esp, [0, 0.42, 0]);
  [-0.12, 0.12].forEach(x => mesh(cyl(0.035, 0.035, 0.08, 16), M.black, esp, [x, 0.12, -0.23]));
  // decanters de uísque e jarra de água
  [-0.3, 0.05].forEach(x => { mesh(sph(0.1, 20, 14), M.glass, bar, [x, 1.2, -0.05]); mesh(cyl(0.085, 0.085, 0.06, 20), M.amber, bar, [x, 1.15, -0.05], null, false); mesh(sph(0.04, 12, 10), M.glass, bar, [x, 1.33, -0.05]); });
  mesh(cyl(0.08, 0.07, 0.28, 24), M.glass, bar, [1.6, 1.22, -0.05]); mesh(cyl(0.072, 0.065, 0.2, 24), M.water, bar, [1.6, 1.18, -0.05], null, false);
  for (let i = 0; i < 4; i++) mesh(cyl(0.035, 0.03, 0.1, 16), M.glass, bar, [1.9 + (i % 2) * 0.09, 1.13, -0.08 - Math.floor(i / 2) * 0.09], null, false);
  [-1, 0.3, 1.6].forEach(x => { const st = new THREE.Group(); st.position.set(x, 0, -0.75); bar.add(st); mesh(cyl(0.2, 0.2, 0.07, 24), M.leather, st, [0, 0.78, 0]); mesh(cyl(0.02, 0.02, 0.72, 8), M.gold, st, [0, 0.4, 0]); mesh(new THREE.TorusGeometry(0.15, 0.01, 6, 24), M.gold, st, [0, 0.3, 0], [Math.PI / 2, 0, 0]); mesh(cyl(0.18, 0.2, 0.02, 24), M.gold, st, [0, 0.01, 0]); });

  // ---------- quadros ----------
  const art = (kind, w, h, seed) => tex(Math.round(w * 300), Math.round(h * 300), (g, W, H) => {
    if (kind === 'ouro') {
      g.fillStyle = '#0c0c0c'; g.fillRect(0, 0, W, H);
      for (let i = 0; i < 9; i++) { g.strokeStyle = goldGrad(g, W, H); g.globalAlpha = .55 + Math.random() * .45; g.lineWidth = 6 + Math.random() * 40; g.lineCap = 'round'; g.beginPath(); g.moveTo(Math.random() * W, Math.random() * H); g.bezierCurveTo(Math.random() * W, Math.random() * H, Math.random() * W, Math.random() * H, Math.random() * W, Math.random() * H); g.stroke(); }
      g.globalAlpha = 1;
    } else if (kind === 'marmore') {
      g.fillStyle = '#f2efe8'; g.fillRect(0, 0, W, H);
      for (let i = 0; i < 40; i++) { g.strokeStyle = `rgba(20,20,20,${Math.random() * .5})`; g.lineWidth = Math.random() * 4; g.beginPath(); let x = Math.random() * W, y = 0; g.moveTo(x, y); while (y < H) { x += (Math.random() - .5) * 90; y += 30; g.lineTo(x, y); } g.stroke(); }
      g.fillStyle = goldGrad(g, W, H); g.fillRect(W * .62, 0, W * .04, H);
    } else if (kind === 'shanshui') {
      const gr = g.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, '#efe6d2'); gr.addColorStop(1, '#e3d6bb'); g.fillStyle = gr; g.fillRect(0, 0, W, H);
      const ridge = (base, amp, col, alpha, seed) => { g.fillStyle = col; g.globalAlpha = alpha; g.beginPath(); g.moveTo(0, H); for (let x = 0; x <= W; x += 6) { const y = base - Math.abs(Math.sin(x * 0.006 + seed) * amp + Math.sin(x * 0.021 + seed * 2) * amp * 0.35 + Math.sin(x * 0.05 + seed) * amp * 0.08); g.lineTo(x, y); } g.lineTo(W, H); g.closePath(); g.fill(); g.globalAlpha = 1; };
      ridge(H * 0.55, H * 0.42, '#9a958c', 0.35, 1.3); ridge(H * 0.68, H * 0.38, '#5d5a55', 0.55, 4.1);
      const mist = g.createLinearGradient(0, H * 0.55, 0, H * 0.8); mist.addColorStop(0, 'rgba(239,230,210,0)'); mist.addColorStop(0.5, 'rgba(239,230,210,.85)'); mist.addColorStop(1, 'rgba(239,230,210,0)'); g.fillStyle = mist; g.fillRect(0, H * 0.5, W, H * 0.35);
      ridge(H * 0.92, H * 0.3, '#1d1c1a', 0.85, 7.7);
      g.strokeStyle = 'rgba(30,30,30,.7)'; g.lineWidth = 2; for (let i = 0; i < 18; i++) { const x = W * (0.15 + Math.random() * 0.7), y = H * (0.6 + Math.random() * 0.25); g.beginPath(); g.moveTo(x, y); g.lineTo(x + 2, y - 26); g.stroke(); g.fillStyle = 'rgba(30,30,30,.6)'; g.beginPath(); g.arc(x + 2, y - 30, 8, 0, 7); g.fill(); }
      g.fillStyle = goldGrad(g, W, H); g.beginPath(); g.arc(W * 0.78, H * 0.2, H * 0.08, 0, 7); g.fill();
      g.fillStyle = '#a8231c'; g.fillRect(W * 0.06, H * 0.08, H * 0.06, H * 0.06);
      g.strokeStyle = 'rgba(40,40,40,.45)'; g.lineWidth = 3; g.beginPath(); g.moveTo(W * 0.1, H * 0.86); g.bezierCurveTo(W * 0.4, H * 0.8, W * 0.6, H * 0.9, W * 0.95, H * 0.84); g.stroke();
    } else if (kind === 'sol') {
      const gr = g.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, '#1a1410'); gr.addColorStop(1, '#3a2414'); g.fillStyle = gr; g.fillRect(0, 0, W, H);
      g.fillStyle = goldGrad(g, W, H); g.beginPath(); g.arc(W * .5, H * .55, Math.min(W, H) * .28, 0, 7); g.fill();
      g.fillStyle = '#0c0c0c'; g.fillRect(0, H * .7, W, H * .3);
      g.strokeStyle = 'rgba(212,178,106,.6)'; g.lineWidth = 3; g.beginPath(); g.moveTo(0, H * .7); g.lineTo(W, H * .7); g.stroke();
    } else {
      g.fillStyle = '#e9e4da'; g.fillRect(0, 0, W, H);
      [['#111', .2, .2, .35, .5], ['#c9a45c', .5, .35, .3, .45], ['#5a3a22', .3, .62, .4, .22]].forEach(([c, x, y, w2, h2]) => { g.fillStyle = c; g.fillRect(x * W, y * H, w2 * W, h2 * H); });
    }
  });
  function painting(x, y, z, rotY, w, h, kind) {
    const p = new THREE.Group(); p.position.set(x, y, z); p.rotation.y = rotY; scene.add(p);
    mesh(box(w + 0.12, h + 0.12, 0.06), M.gold, p, [0, 0, 0], null, false);
    mesh(box(w, h, 0.07), mat(0x111111), p, [0, 0, 0.002], null, false);
    mesh(new THREE.PlaneGeometry(w, h), mat(0xffffff, { map: art(kind, w, h), roughness: 0.75 }), p, [0, 0, 0.04], null, false);
    if (Math.abs(z - 8.9) < 0.2) out.southItems.push(p); if (x < -11.5) out.westItems.push(p);
    return p;
  }
  painting(-4.6, 2.1, 8.9, Math.PI, 2.6, 1.7, 'ouro');
  painting(-1.0, 2.1, 8.9, Math.PI, 1.5, 1.9, 'marmore');
  painting(6.6, 2.1, 8.9, Math.PI, 1.6, 2.0, 'sol');
  painting(-11.9, 2.15, 6.2, Math.PI / 2, 2.9, 1.7, 'shanshui');
  // brasão Carnucci acima da entrada (lado de dentro)
  goldLogo(LOGO, 512).then(t => out.southItems.push(mesh(new THREE.PlaneGeometry(0.9, 0.9), new THREE.MeshStandardMaterial({ map: t, transparent: true, metalness: 0.8, roughness: 0.3, emissive: 0x3a2a10, emissiveMap: t }), scene, [3.6, 3.6, 8.9], [0, Math.PI, 0], false)));

  // ---------- adega (Royal Salute e Blue Label, sem rótulos) ----------
  const adega = new THREE.Group(); adega.position.set(-11.6, 0, 2.7); adega.rotation.y = Math.PI / 2; scene.add(adega); out.westItems.push(adega);
  const cabM = phys(0x0c0b0a, { roughness: 0.25, clearcoat: 1 });
  mesh(box(1.9, 3.0, 0.04), cabM, adega, [0, 1.5, -0.3]); mesh(box(1.9, 0.08, 0.62), cabM, adega, [0, 0.04, 0]); mesh(box(1.9, 0.08, 0.62), cabM, adega, [0, 2.96, 0]);
  [-0.93, 0.93].forEach(x => mesh(box(0.04, 3.0, 0.62), cabM, adega, [x, 1.5, 0]));
  mesh(box(1.74, 2.7, 0.02), new THREE.MeshBasicMaterial({ color: 0x3a2a18 }), adega, [0, 1.55, -0.28], null, false);
  [-0.88, 0.88].forEach(x => mesh(box(0.03, 3.0, 0.66), M.gold, adega, [x, 1.5, 0], null, false));
  mesh(box(1.9, 0.03, 0.66), M.gold, adega, [0, 3.0, 0], null, false);
  const rs = [0x1e2f6b, 0x7a1222, 0x10402a]; // flagons de cerâmica (azul, vermelho, verde)
  for (let r = 0; r < 4; r++) {
    const y = 0.35 + r * 0.66;
    mesh(box(1.72, 0.02, 0.56), M.goldDim, adega, [0, y, 0], null, false);
    mesh(box(1.7, 0.01, 0.01), new THREE.MeshBasicMaterial({ color: 0xffd9a0 }), adega, [0, y + 0.6, 0.27], null, false);
    for (let i = 0; i < 5; i++) {
      const x = -0.68 + i * 0.34;
      if ((r + i) % 2 === 0) { // garrafa estilo flagon de cerâmica
        const c = rs[(r + i) % 3]; const fm = phys(c, { roughness: 0.18, clearcoat: 1 });
        const b = mesh(sph(0.1, 24, 18), fm, adega, [x, y + 0.13, 0.05]); b.scale.set(1, 1.1, 0.75);
        mesh(cyl(0.03, 0.045, 0.12, 16), fm, adega, [x, y + 0.29, 0.05]); mesh(cyl(0.034, 0.034, 0.04, 16), M.gold, adega, [x, y + 0.36, 0.05]);
        mesh(new THREE.TorusGeometry(0.075, 0.006, 6, 24), M.gold, adega, [x, y + 0.15, 0.05], [0, 0, 0], false);
      } else { // garrafa retangular azul escura
        const gm = phys(0x0e1a3a, { roughness: 0.05, transparent: true, opacity: 0.9, clearcoat: 1 });
        mesh(rbox(0.13, 0.27, 0.08, 0.015), gm, adega, [x, y + 0.155, 0.05]); mesh(cyl(0.02, 0.025, 0.08, 12), gm, adega, [x, y + 0.33, 0.05]);
        mesh(cyl(0.024, 0.024, 0.04, 12), M.gold, adega, [x, y + 0.385, 0.05]); mesh(box(0.131, 0.04, 0.081), M.gold, adega, [x, y + 0.1, 0.05], null, false);
      }
    }
  }
  mesh(new THREE.PlaneGeometry(1.76, 2.95), new THREE.MeshPhysicalMaterial({ color: 0xffffff, transparent: true, opacity: 0.12, roughness: 0.02, clearcoat: 1 }), adega, [0, 1.5, 0.315], null, false);
  mesh(box(0.025, 0.6, 0.03), M.gold, adega, [0.75, 1.6, 0.34], null, false);

  // ---------- segundo lounge: conversa perto da janela ----------
  const conv = new THREE.Group(); conv.position.set(8.0, 0, -6.4); scene.add(conv); blob(conv, 0, 0, 2.0, 1.4, 0.4);
  mesh(new THREE.CircleGeometry(2.2, 64), mat(0x2a2624, { roughness: 1 }), conv, [0, 0.007, 0], [-Math.PI / 2, 0, 0], false);
  mesh(new THREE.RingGeometry(2.05, 2.1, 64), M.gold, conv, [0, 0.008, 0], [-Math.PI / 2, 0, 0], false);
  const blackLeather = phys(0x121010, { roughness: 0.4, clearcoat: 0.4, sheen: 0.3 });
  [[-1.2, Math.PI / 2], [1.2, -Math.PI / 2]].forEach(([x, r]) => {
    const sf = new THREE.Group(); sf.position.set(x, 0, 0); sf.rotation.y = r; conv.add(sf);
    mesh(rbox(1.9, 0.4, 0.85, 0.1, 4), blackLeather, sf, [0, 0.2, 0]);
    mesh(rbox(1.9, 0.45, 0.22, 0.1, 4), blackLeather, sf, [0, 0.6, -0.33]);
    [-0.88, 0.88].forEach(ax => mesh(rbox(0.18, 0.55, 0.85, 0.08, 4), blackLeather, sf, [ax, 0.28, 0]));
    [-0.45, 0.45].forEach(cx => mesh(rbox(0.85, 0.14, 0.66, 0.06, 4), blackLeather, sf, [cx, 0.46, -0.02]));
    [-0.85, 0.85].forEach(lx => mesh(box(0.04, 0.06, 0.8), M.gold, sf, [lx, 0.03, 0]));
    mesh(rbox(0.38, 0.38, 0.12, 0.05, 4), phys(0xb08a45, { roughness: 0.6, sheen: 0.6 }), sf, [0.55, 0.68, -0.18], [-0.2, 0, -0.15]);
  });
  const ctab = new THREE.Group(); conv.add(ctab);
  mesh(rbox(1.0, 0.05, 0.6, 0.02), phys(0xffffff, { map: marbleTex('#f2f0ec', 'rgba(110,110,110,A)', 12, 512, [1, 1]), roughness: 0.1, clearcoat: 1 }), ctab, [0, 0.4, 0]);
  [[-0.45, -0.25], [0.45, -0.25], [-0.45, 0.25], [0.45, 0.25]].forEach(([x, z]) => mesh(box(0.03, 0.38, 0.03), M.gold, ctab, [x, 0.19, z]));
  mesh(sph(0.11, 20, 14), M.glass, ctab, [-0.25, 0.53, 0.05]); mesh(cyl(0.09, 0.09, 0.05, 20), M.amber, ctab, [-0.25, 0.48, 0.05], null, false);
  [[0.15, -0.1], [0.3, 0.12]].forEach(([x, z]) => { mesh(cyl(0.04, 0.036, 0.09, 20), M.glass, ctab, [x, 0.47, z], null, false); mesh(cyl(0.035, 0.032, 0.035, 20), M.amber, ctab, [x, 0.445, z], null, false); });
  mesh(rbox(0.26, 0.04, 0.2, 0.004), mat(0x1a1a1a), ctab, [0.2, 0.445, -0.15], [0, 0.3, 0]);

  // ---------- plantas ----------
  function plantPot(parent, x, z, s = 1) {
    const p = new THREE.Group(); p.position.set(x, 0, z); p.scale.setScalar(s); parent.add(p);
    mesh(new THREE.CylinderGeometry(0.34, 0.26, 0.7, 24, 1, true), mat(0xf2efe9, { roughness: 0.3, side: THREE.DoubleSide }), p, [0, 0.35, 0]);
    mesh(cyl(0.26, 0.26, 0.02, 20), mat(0xf2efe9, { roughness: 0.3 }), p, [0, 0.01, 0], null, false);
    mesh(new THREE.TorusGeometry(0.34, 0.018, 6, 32), mat(0xf2efe9, { roughness: 0.3 }), p, [0, 0.7, 0], [Math.PI / 2, 0, 0], false);
    mesh(cyl(0.325, 0.325, 0.03, 24), mat(0x3a2a1c, { roughness: 1 }), p, [0, 0.62, 0], null, false);
    const trunkC = new THREE.CatmullRomCurve3([new THREE.Vector3(0, 0.62, 0), new THREE.Vector3(0.05, 1.4, 0.02), new THREE.Vector3(-0.03, 2.0, 0.05), new THREE.Vector3(0.04, 2.4, 0)]);
    mesh(new THREE.TubeGeometry(trunkC, 20, 0.035, 8), mat(0x5a4632, { roughness: 0.9 }), p);
    const leafM = phys(0x2f4a2a, { roughness: 0.6, sheen: 0.4, side: THREE.DoubleSide });
    const leaf = new THREE.SphereGeometry(0.11, 5, 3); leaf.scale(1, 0.22, 0.55);
    blob(p, 0, 0, 0.55);
    for (let i = 0; i < 40; i++) {
      const a = Math.random() * Math.PI * 2, r = Math.random() * 0.55, y = 1.4 + Math.random() * 1.25;
      const l = mesh(leaf, leafM, p, [Math.cos(a) * r, y, Math.sin(a) * r], [Math.random() * 1.5 - .75, a, Math.random() - .5]);
      if (i % 3 === 0) l.material = phys(0x3d5c34, { roughness: 0.6, side: THREE.DoubleSide });
    }
    return p;
  }
  out.plantPot = plantPot;
  [[-11.2, -8.3], [11.2, -8.3], [-6.2, 8.4], [1.7, 8.4], [-4.6, -8.4], [11.2, 2.3]].forEach(([x, z]) => plantPot(scene, x, z, 0.85 + Math.random() * 0.35));
  // poltrona de leitura na janela

  // ---------- luzes (só 2: céu e sol/teto) ----------
  const hemi = new THREE.HemisphereLight(0xf4f1ea, 0x6a645a, 1.0); scene.add(hemi);
  const sun = new THREE.DirectionalLight(0xfff2df, 2); sun.position.set(4, 12, 6); scene.add(sun, sun.target);
  const interior = []; const interiorBase = [];
  // ---------- dia e noite (horário de Brasília) ----------
  const C = (h) => new THREE.Color(h);
  const P = {
    night: { top: C(0x03060f), hor: C(0x111833), sun: 0, hemi: 0.45, win: 0.55, inside: 0.85, exp: 0.9, fog: C(0x0d1228) },
    dusk: { top: C(0x1d2c5c), hor: C(0xff8a4c), sun: 1.2, hemi: 0.5, win: 0.6, inside: 0.8, exp: 0.88, fog: C(0x7a5a6a) },
    day: { top: C(0x2f6fd0), hor: C(0xd9e7f2), sun: 3.0, hemi: 0.7, win: 0.03, inside: 0.4, exp: 0.82, fog: C(0xc7dbeb) },
  };
  scene.fog = new THREE.Fog(0x0d1228, 250, 1500); scene.background = new THREE.Color(0x0b0a09);
  let hourOverride = null;
  out.setHour = h => { hourOverride = h; };
  out.hourNow = () => { const s = new Date().toLocaleString('en-US', { timeZone: 'America/Sao_Paulo', hour12: false, hour: '2-digit', minute: '2-digit' }); const [h, m] = s.split(':').map(Number); return (h % 24) + m / 60; };
  out.getHour = () => hourOverride ?? out.hourNow();
  const tmpC = new THREE.Color();
  function applySky(h) {
    const rise = 5.4, set = 18.9; const ph = (h - rise) / (set - rise);
    const elev = Math.sin(Math.PI * clamp(ph, -0.3, 1.3)) * (ph >= 0 && ph <= 1 ? 1 : 1);
    const el = ph < 0 || ph > 1 ? -Math.min(Math.abs(ph < 0 ? ph : ph - 1) * 3, 1) * 0.6 : elev;
    const az = Math.PI * clamp(ph, 0, 1);
    const dir = new THREE.Vector3(Math.cos(az), Math.max(el, -0.3), -0.45).normalize();
    // mistura: noite -> crepúsculo -> dia
    let a, b, k;
    if (el <= -0.12) { a = P.night; b = P.night; k = 0; }
    else if (el < 0.08) { a = P.night; b = P.dusk; k = smooth((el + 0.12) / 0.2); }
    else if (el < 0.35) { a = P.dusk; b = P.day; k = smooth((el - 0.08) / 0.27); }
    else { a = P.day; b = P.day; k = 0; }
    const mix = (x, y) => lerp(x, y, k);
    skyU.top.value.copy(a.top).lerp(b.top, k); skyU.hor.value.copy(a.hor).lerp(b.hor, k);
    skyU.sunDir.value.copy(dir); skyU.sunAmt.value = clamp(el * 4 + 0.4, 0, 1);
    scene.fog.color.copy(a.fog).lerp(b.fog, k);
    const sunK = clamp(el * 5, 0, 1);
    // de dia: sol entrando; de noite: luz de teto quente
    const ins0 = mix(a.inside, b.inside);
    sun.intensity = lerp(1.5 * ins0 + 0.6, mix(a.sun, b.sun) * 0.9, sunK);
    sun.color.set(sunK > 0.5 ? 0xfff2df : 0xffe2bd);
    if (sunK > 0.3) sun.position.copy(dir).multiplyScalar(40); else sun.position.set(3, 14, 5); sun.target.position.set(0, 0, 0);
    hemi.intensity = mix(a.hemi, b.hemi) + 0.5;
    hemi.color.copy(skyU.top.value).lerp(tmpC.set(0xffffff), 0.6);
    const win = mix(a.win, b.win); cityMats.forEach(m => m.emissiveIntensity = win);
    cityMats.forEach(m => m.color.setScalar(lerp(0.22, 1, clamp(el * 3 + 0.3, 0, 1))));
    groundM.color.setScalar(lerp(0.25, 1, clamp(el * 3 + 0.3, 0, 1)));
    hillM.color.copy(scene.fog.color).multiplyScalar(lerp(0.55, 0.8, clamp(el * 3, 0, 1)));
    lamps.material.opacity = clamp(win * 1.2, 0, 1);
    stars.material.opacity = clamp(1 - (el + 0.12) * 6, 0, 0.85);
    moon.visible = el < 0.05;
    const ins = mix(a.inside, b.inside);
    haloM.emissiveIntensity = 0.6 + ins * 1.6;
    renderer.toneMappingExposure = mix(a.exp, b.exp);
    out.isNight = el < 0;
  }
  let skyT = 0;
  out.updaters.push((dt) => { skyT -= dt; if (skyT <= 0) { skyT = hourOverride !== null ? 0 : 20; applySky(out.getHour()); } });
  out.refreshSky = () => { skyT = 0; };
  applySky(out.getHour());

  // paredes sólidas somem quando a câmera está do lado de fora (vista de maquete)
  out.updateWalls = (cam) => {
    const sV = cam.position.z < ROOM.z1 + 0.3, wV = cam.position.x > ROOM.x0 - 0.3;
    out.solidWalls.forEach(w => { w.mesh.visible = w.side === 'S' ? sV : wV; });
    out.southItems.forEach(o => o.visible = sV); out.westItems.forEach(o => o.visible = wV);
  };
  out.setBathView = on => {
    out.bathAll.forEach(m => { m.material = m.material.clone(); });
    [bSouth, bEast, roof, bNorth].forEach(m => { m.visible = !on; });
    [bWest1, bWest2, bTop].forEach(m => { m.material.opacity = on ? 0.25 : 1; m.material.depthWrite = !on; });
  };
  return out;
}
