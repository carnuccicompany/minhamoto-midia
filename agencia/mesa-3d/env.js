import * as THREE from 'three';
import { M, mat, phys, tex, mesh, box, rbox, cyl, sph, marbleTex, goldGrad, goldLogo, GOLD, lerp, clamp, smooth, blob } from './util.js';

export const ROOM = { x0: -12, x1: 12, z0: -9, z1: 9, H: 4.2 };
export const BATH = { x0: 8.6, x1: 12, z0: 3, z1: 9, door: [5.3, 6.5] };
export const TABLE_R = 2.75, TOP_Y = 0.76;

// pontos de destino das rotinas (x, z, direção pra onde olha)
export const PIT = { x: 8.3, z: 0.7, R: 2.1, D: 0.5 };
export const SPOTS = {
  pokerTop: new THREE.Vector3(8.3 - 2.55, 0, 0.7),
  banheiroPorta: new THREE.Vector3(7.9, 0, 5.9),
  banheiro: new THREE.Vector3(10.3, 0, 6.4),
  uisque: new THREE.Vector3(-4.3, 0, 7.9),
  agua: new THREE.Vector3(-7.4, 0, 6.85),
  cafe: new THREE.Vector3(-10.4, 0, 6.85),
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
    const glass = [['#3a4652', '#8d9cab'], ['#2b3138', '#66727e'], ['#55606a', '#b3bcc4'], ['#232a31', '#56677a'], ['#5e5850', '#b9b0a2']][seed % 5];
    const frame = ['#1b1f24', '#2b2f35', '#d9d4ca', '#14181d', '#3a332c'][seed % 5];
    g.fillStyle = frame; g.fillRect(0, 0, 512, 1024); e.fillStyle = '#000'; e.fillRect(0, 0, 512, 1024);
    const cols = 8, rows = 24, cw = 256 / cols, rh = 512 / rows;
    const litRows = new Set(); for (let r = 0; r < rows; r++) if (Math.random() < 0.28) litRows.add(r);
    const sky = g.createLinearGradient(0, 0, 0, 512); sky.addColorStop(0, glass[1]); sky.addColorStop(1, glass[0]);
    for (let r = 0; r < rows; r++) {
      const y0 = r * rh, sp = Math.round(rh * 0.24);
      g.fillStyle = frame; g.fillRect(0, y0, 256, sp);                       // faixa de laje entre andares
      for (let c = 0; c < cols; c++) {
        const x = c * cw + 1, y = y0 + sp, w = cw - 2, h = rh - sp - 1;
        g.fillStyle = sky; g.fillRect(x, y, w, h);
        const v = (Math.random() - 0.5) * 0.12; g.fillStyle = v > 0 ? `rgba(255,255,255,${v})` : `rgba(0,0,0,${-v})`; g.fillRect(x, y, w, h);
        const gr = g.createLinearGradient(x, y, x + w, y + h); gr.addColorStop(0, 'rgba(255,255,255,.10)'); gr.addColorStop(0.5, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(x, y, w, h);
        const lit = litRows.has(r) ? Math.random() < 0.8 : Math.random() < 0.06;
        if (lit) { const warm = Math.random() < 0.75; const k = 0.55 + Math.random() * 0.45; e.fillStyle = warm ? `rgba(255,${190 + Math.random() * 40},${120 + Math.random() * 50},${k})` : `rgba(190,215,255,${k})`; e.fillRect(x, y, w, h); }
      }
    }
    const streak = g.createLinearGradient(0, 0, 256, 0); streak.addColorStop(0, 'rgba(255,255,255,0)'); streak.addColorStop(0.35, 'rgba(255,255,255,.08)'); streak.addColorStop(0.5, 'rgba(255,255,255,0)'); streak.addColorStop(0.8, 'rgba(255,255,255,.05)'); streak.addColorStop(1, 'rgba(255,255,255,0)');
    g.fillStyle = streak; g.fillRect(0, 0, 256, 512);
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
  const floorT = tex(2048, 2048, (g, w, h) => {
    g.fillStyle = '#ddd6ca'; g.fillRect(0, 0, w, h);
    const cl = g.createRadialGradient(w * .3, h * .3, 0, w * .5, h * .5, w * .8); cl.addColorStop(0, 'rgba(255,253,248,.55)'); cl.addColorStop(1, 'rgba(210,202,190,.25)'); g.fillStyle = cl; g.fillRect(0, 0, w, h);
    const vein = (blur, width, alpha, col, n) => { g.save(); g.filter = `blur(${blur}px)`; for (let i = 0; i < n; i++) { g.strokeStyle = col.replace('A', (alpha * (0.5 + Math.random())).toFixed(3)); g.lineWidth = width * (0.5 + Math.random()); g.beginPath(); let x = Math.random() * w, y = -40, ang = 0.9 + Math.random() * 0.6; g.moveTo(x, y); while (y < h + 40 && x > -60 && x < w + 60) { ang += (Math.random() - 0.5) * 0.5; x += Math.cos(ang) * 40; y += Math.sin(ang) * 40 + 14; g.lineTo(x, y); } g.stroke(); } g.restore(); };
    vein(18, 34, 0.05, 'rgba(120,112,100,A)', 10); vein(4, 6, 0.12, 'rgba(105,98,88,A)', 18); vein(0.6, 1.4, 0.22, 'rgba(90,84,76,A)', 30); vein(0.5, 1.2, 0.18, 'rgba(176,138,72,A)', 6);
    g.fillStyle = 'rgba(120,110,96,.28)'; for (let i = 1; i < 4; i++) { g.fillRect(i * w / 4 - 1, 0, 2, h); g.fillRect(0, i * h / 4 - 1, w, 2); }
    g.fillStyle = 'rgba(255,255,255,.35)'; for (let i = 1; i < 4; i++) { g.fillRect(i * w / 4 + 1, 0, 1, h); g.fillRect(0, i * h / 4 + 1, w, 1); }
  }, [5, 4]);
  // chão com o buraco do fosso de pôquer (plano em XY, depois deitado; o buraco fica em (PIT.x, -PIT.z) no plano)
  const holed = (W, H, cx, cy) => { const sh = new THREE.Shape(); sh.moveTo(-W / 2, -H / 2); sh.lineTo(W / 2, -H / 2); sh.lineTo(W / 2, H / 2); sh.lineTo(-W / 2, H / 2); sh.closePath();
    const hp = new THREE.Path(); hp.absarc(PIT.x - cx, -PIT.z - cy, PIT.R, 0, Math.PI * 2, true); sh.holes.push(hp);
    const g = new THREE.ShapeGeometry(sh, 64); const p = g.attributes.position, uv = g.attributes.uv; for (let i = 0; i < p.count; i++) uv.setXY(i, (p.getX(i) + W / 2) / W, (p.getY(i) + H / 2) / H); return g; };
  const floor = mesh(holed(24, 18, 0, 0), phys(0xffffff, { map: floorT, roughness: 0.22, clearcoat: 0.6, clearcoatRoughness: 0.25 }), scene, [0, 0, 0], [-Math.PI / 2, 0, 0], false); floor.userData.keep = true;
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
      const ring2 = (x, z, r0, r1, a) => { const g = c.createRadialGradient(sx(x), sz(z), r0 * k, sx(x), sz(z), r1 * k); g.addColorStop(0, `rgba(60,52,44,${a})`); g.addColorStop(1, 'rgba(60,52,44,0)'); c.fillStyle = g; c.fillRect(sx(x) - r1 * k, sz(z) - r1 * k, 2 * r1 * k, 2 * r1 * k); };
      const ring = (r0, r1, a) => { const g = c.createRadialGradient(sx(0), sz(0), r0 * k, sx(0), sz(0), r1 * k); g.addColorStop(0, 'rgba(60,52,44,0)'); g.addColorStop(.45, `rgba(60,52,44,${a})`); g.addColorStop(1, 'rgba(60,52,44,0)'); c.fillStyle = g; c.fillRect(0, 0, W, H); };
      ring(TABLE_R - 0.4, TABLE_R + 1.8, .5);
      const box2 = (x0, z0, x1, z1, a) => { c.save(); c.filter = `blur(${0.35 * k}px)`; c.fillStyle = `rgba(60,52,44,${a})`; c.fillRect(sx(x0), sz(z0), sx(x1) - sx(x0), sz(z1) - sz(z0)); c.restore(); };
      box2(-12, -7.6 - 1.2, -11.2, 5.0, .35);        // estantes, TV, adega, armário e frigobar (parede oeste)
      box2(-12, 6.3, -9.6, 8.2, .3);                 // bancada do café
      blob(8, -6.4, 2.2, .3); blob(-8.4, -3.6, 2.4, .25); // lounges
      blob(-2.3, 7.45, 0.9, .35);                    // Hall da Fama
      box2(-11.4, 8.4, 1.8, 9, .45);                 // parede da adega
      ring2(PIT.x, PIT.z, PIT.R, PIT.R + 0.9, .45);  // borda do fosso
    });
    const ao = mesh(holed(24, 18, 0, 0), new THREE.MeshBasicMaterial({ map: t, transparent: true, blending: THREE.MultiplyBlending, premultipliedAlpha: true, depthWrite: false, toneMapped: false }), scene, [0, 0.004, 0], [-Math.PI / 2, 0, 0], false);
    ao.renderOrder = 1; ao.userData.keep = true;
  }
  const blackMarble = marbleTex('#0e0e0f', 'rgba(220,220,220,A)', 22, 1024, [4, 1]);
  const bmM = phys(0xffffff, { map: blackMarble, roughness: 0.15, clearcoat: 1, clearcoatRoughness: 0.15 });
  [[0, -8.45, 24, 1.1], [0, 8.45, 24, 1.1], [-11.45, 0, 1.1, 18], [11.45, 0, 1.1, 18]].forEach(([x, z, w, d]) => mesh(new THREE.PlaneGeometry(w, d), bmM, scene, [x, 0.003, z], [-Math.PI / 2, 0, 0], false));
  [[0, -7.88, 22.9, 0.03], [0, 7.88, 22.9, 0.03], [-10.88, 0, 0.03, 15.8], [10.88, 0, 0.03, 15.8]].forEach(([x, z, w, d]) => mesh(new THREE.PlaneGeometry(w, d), M.gold, scene, [x, 0.005, z], [-Math.PI / 2, 0, 0], false));
  // borda da laje (vista de fora)
  mesh(box(24.4, 0.4, 18.4), mat(0x1c1c1e, { roughness: 0.5 }), scene, [0, -0.215, 0], null, false);
  const wallT = tex(1024, 1024, (g, w, h) => {
    g.fillStyle = '#efebe4'; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 26000; i++) { g.fillStyle = `rgba(${Math.random() < .5 ? '255,255,255' : '120,110,96'},${Math.random() * 0.035})`; g.fillRect(Math.random() * w, Math.random() * h, 2 + Math.random() * 6, 1 + Math.random() * 3); }
    const panel = (x, y, pw, ph) => { g.strokeStyle = 'rgba(255,255,255,.75)'; g.lineWidth = 3; g.strokeRect(x + 2, y + 2, pw, ph); g.strokeStyle = 'rgba(110,98,82,.28)'; g.lineWidth = 3; g.strokeRect(x, y, pw, ph); g.strokeStyle = 'rgba(176,140,74,.35)'; g.lineWidth = 1; g.strokeRect(x + 12, y + 12, pw - 24, ph - 24); };
    [0, 512].forEach(x => { panel(x + 54, 70, 404, 560); panel(x + 54, 690, 404, 200); });
    g.fillStyle = '#d9d3c9'; g.fillRect(0, h - 70, w, 70); g.fillStyle = '#c9a45c'; g.fillRect(0, h - 74, w, 4); g.fillStyle = 'rgba(0,0,0,.08)'; g.fillRect(0, h - 70, w, 3);
    g.fillStyle = 'rgba(255,255,255,.6)'; g.fillRect(0, 30, w, 3); g.fillStyle = 'rgba(110,98,82,.25)'; g.fillRect(0, 34, w, 3);
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
  const roofT = tex(512, 896, (g, w, h) => {
    g.fillStyle = '#e8e3da'; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 9000; i++) { g.fillStyle = `rgba(${Math.random() < .5 ? '255,255,255' : '110,100,88'},${Math.random() * 0.05})`; g.fillRect(Math.random() * w, Math.random() * h, 3, 2); }
    g.strokeStyle = '#c9a45c'; g.lineWidth = 6; g.strokeRect(14, 14, w - 28, h - 28); g.lineWidth = 2; g.strokeRect(34, 34, w - 68, h - 68);
    const sk = g.createLinearGradient(0, 0, w, h); sk.addColorStop(0, '#2e3a44'); sk.addColorStop(0.5, '#56646f'); sk.addColorStop(1, '#2a333b');
    g.fillStyle = sk; g.fillRect(140, 160, w - 280, h - 320); g.strokeStyle = '#1a1a1c'; g.lineWidth = 8; g.strokeRect(140, 160, w - 280, h - 320);
    g.lineWidth = 4; for (let y = 160 + (h - 320) / 4; y < h - 160; y += (h - 320) / 4) { g.beginPath(); g.moveTo(140, y); g.lineTo(w - 140, y); g.stroke(); }
    g.beginPath(); g.moveTo(w / 2, 160); g.lineTo(w / 2, h - 160); g.stroke();
    g.fillStyle = 'rgba(255,255,255,.18)'; g.beginPath(); g.moveTo(150, 170); g.lineTo(230, 170); g.lineTo(150, 330); g.fill();
  });
  const roof = mesh(box(3.6, 0.08, 6.2), phys(0xffffff, { map: roofT, roughness: 0.5, transparent: true }), scene, [10.3, ROOM.H, 6], null, false);
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
  mesh(cyl(TABLE_R, TABLE_R, 0.06, 64), new THREE.MeshStandardMaterial({ map: woodT, roughness: 0.62, envMapIntensity: 0.3 }), table, [0, TOP_Y - 0.03, 0]).userData.keep = true;
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
  // sofá em U enorme virado pra TV: encosto principal + dois braços longos, almofadas soltas, tapete grande de lã
  blob(scene, -7.0, -3.6, 0.9, 2.9); blob(scene, -8.6, -6.7, 1.6, 0.7); blob(scene, -8.6, -0.5, 1.6, 0.7);
  const sofaSeg = (cx, cz, len, rotY) => {
    const sg = new THREE.Group(); sg.position.set(cx, 0, cz); sg.rotation.y = rotY; lounge.add(sg);
    mesh(rbox(len, 0.4, 1.05, 0.12, 4), boucle, sg, [0, 0.2, 0]);
    mesh(rbox(len, 0.55, 0.28, 0.13, 4), boucle, sg, [0, 0.62, 0.39]);
    const n = Math.max(1, Math.round(len / 1.05));
    for (let i = 0; i < n; i++) { const x = -len / 2 + (i + 0.5) * len / n; mesh(rbox(len / n - 0.03, 0.17, 0.82, 0.08, 4), boucle, sg, [x, 0.48, -0.05]); mesh(rbox(len / n - 0.06, 0.42, 0.18, 0.09, 4), boucle, sg, [x, 0.74, 0.2], [-0.18, 0, 0]); }
    mesh(rbox(len, 0.06, 1.0, 0.03), M.goldDim, sg, [0, 0.03, 0]);
    return sg;
  };
  sofaSeg(-6.75, -3.6, 5.6, Math.PI / 2);          // encosto principal (costas pra mesa)
  sofaSeg(-8.75, -6.85, 3.0, Math.PI);                    // braço norte
  sofaSeg(-8.75, -0.35, 3.0, 0);              // braço sul
  [[-7.05, -6.25], [-7.05, -0.95]].forEach(([x, z]) => mesh(rbox(0.6, 0.55, 0.6, 0.12, 4), boucle, lounge, [x, 0.28, z])); // cantos
  [[-6.95, -5.2, 0.2], [-6.95, -2.0, -0.2], [-8.0, -6.6, 0.1], [-9.6, -0.6, -0.1]].forEach(([x, z, r]) => mesh(rbox(0.46, 0.46, 0.14, 0.06, 4), phys(0xb08a45, { roughness: 0.6, sheen: 0.6 }), lounge, [x, 0.74, z], [-0.15, Math.PI / 2 + r, 0]));
  // mesa de centro oval de mármore preto com base dourada
  const ct = new THREE.Group(); ct.position.set(-8.75, 0, -3.6); lounge.add(ct);
  const top = mesh(cyl(1.0, 1.0, 0.06, 64), phys(0xffffff, { map: marbleTex('#141414', 'rgba(230,230,230,A)', 14, 512, [1, 1]), roughness: 0.1, clearcoat: 1 }), ct, [0, 0.42, 0]); top.scale.set(0.85, 1, 1.6);
  const base = mesh(cyl(0.42, 0.55, 0.39, 40), M.gold, ct, [0, 0.2, 0]); base.scale.set(0.85, 1, 1.5);
  [[0x1a1a1a, 0.06], [0xc9a45c, 0.05], [0xf0ece4, 0.045]].reduce((y, [c, h]) => { mesh(rbox(0.32, h, 0.24, 0.005), mat(c, { roughness: 0.6 }), ct, [0.2, y + h / 2, 0.6], [0, 0.3, 0]); return y + h; }, 0.455);
  mesh(sph(0.09, 16, 12), M.gold, ct, [-0.15, 0.54, -0.5]);
  [-0.2, 0.1].forEach((z, i) => { mesh(cyl(0.04, 0.035, 0.09, 16), M.glass, ct, [0.25 - i * 0.1, 0.5, z]); });
  const lrugT = tex(1024, 1024, (c, w, h) => { c.fillStyle = '#d9d1c3'; c.fillRect(0, 0, w, h); for (let i = 0; i < 40000; i++) { c.fillStyle = `rgba(${Math.random() < .5 ? '255,255,255' : '90,80,66'},${Math.random() * .06})`; c.fillRect(Math.random() * w, Math.random() * h, 2, 2); } c.strokeStyle = 'rgba(176,138,69,.6)'; c.lineWidth = 10; c.strokeRect(40, 40, w - 80, h - 80); c.lineWidth = 3; c.strokeRect(64, 64, w - 128, h - 128); });
  const lrug = mesh(new THREE.PlaneGeometry(5.3, 7.7), mat(0xffffff, { map: lrugT, roughness: 1 }), lounge, [-8.75, 0.007, -3.6], [-Math.PI / 2, 0, 0], false);
  // luminária de arco
  const arcLamp = new THREE.Group(); arcLamp.position.set(-6.3, 0, -7.6); arcLamp.rotation.y = -0.6; lounge.add(arcLamp);
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
  const bar = new THREE.Group(); bar.position.set(-9, 0, 7.95); scene.add(bar); blob(bar, 0, -0.1, 2.8, 0.6);
  mesh(rbox(5, 1.02, 0.7, 0.03), mat(0x111111, { roughness: 0.4 }), bar, [0, 0.51, 0]);
  for (let i = -24; i <= 24; i++) mesh(cyl(0.035, 0.035, 0.95, 8), mat(0x1a1a1a, { roughness: 0.35 }), bar, [i * 0.1, 0.5, -0.36], null, false);
  mesh(rbox(5.1, 0.06, 0.78, 0.01), phys(0xffffff, { map: marbleTex('#f2f0ec', 'rgba(120,120,120,A)', 14, 512, [2, 1]), roughness: 0.12, clearcoat: 1 }), bar, [0, 1.05, 0]);
  mesh(box(5.0, 0.02, 0.02), new THREE.MeshBasicMaterial({ color: 0xffd9a0 }), bar, [0, 0.12, -0.36], null, false);
  // (as garrafas agora ficam na parede da adega, atrás do bar)
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
    } else if (kind === 'pantera') {
      // retrato da Fartuzzi: rosto saindo do escuro, olhos verdes, poeira de ouro
      const bg = g.createRadialGradient(W * .5, H * .42, 0, W * .5, H * .45, H * .75); bg.addColorStop(0, '#1d1a17'); bg.addColorStop(1, '#050505'); g.fillStyle = bg; g.fillRect(0, 0, W, H);
      for (let i = 0; i < 1400; i++) { g.fillStyle = `rgba(214,178,106,${Math.random() * .5})`; const r = Math.random() * 2.2; g.beginPath(); g.arc(Math.random() * W, H * (0.55 + Math.random() * .45), r, 0, 7); g.fill(); }
      const cx = W * .5, cy = H * .45, s = W * .36;
      g.save(); g.translate(cx, cy);
      const face = g.createRadialGradient(0, -s * .1, s * .1, 0, 0, s * 1.05); face.addColorStop(0, '#2a2a30'); face.addColorStop(.6, '#121216'); face.addColorStop(1, 'rgba(5,5,5,0)');
      g.fillStyle = face; g.beginPath(); g.moveTo(-s * .95, -s * .25); g.quadraticCurveTo(-s * 1.0, -s * .95, -s * .55, -s * .95); g.lineTo(-s * .38, -s * .62); g.quadraticCurveTo(0, -s * .8, s * .38, -s * .62); g.lineTo(s * .55, -s * .95); g.quadraticCurveTo(s * 1.0, -s * .95, s * .95, -s * .25);
      g.quadraticCurveTo(s * .9, s * .5, s * .3, s * .85); g.quadraticCurveTo(0, s * .98, -s * .3, s * .85); g.quadraticCurveTo(-s * .9, s * .5, -s * .95, -s * .25); g.fill();
      g.strokeStyle = 'rgba(120,130,160,.18)'; g.lineWidth = 2; for (let i = 0; i < 60; i++) { const a = Math.random() * 6.28, r0 = s * (.3 + Math.random() * .6); g.beginPath(); g.moveTo(Math.cos(a) * r0, Math.sin(a) * r0); g.lineTo(Math.cos(a) * (r0 + 14), Math.sin(a) * (r0 + 14)); g.stroke(); }
      [-1, 1].forEach(k => { const ex = k * s * .34, ey = -s * .18; const eg = g.createRadialGradient(ex, ey, 0, ex, ey, s * .2); eg.addColorStop(0, 'rgba(160,230,80,.55)'); eg.addColorStop(1, 'rgba(160,230,80,0)'); g.fillStyle = eg; g.fillRect(ex - s * .2, ey - s * .2, s * .4, s * .4);
        g.fillStyle = '#a8e04a'; g.beginPath(); g.ellipse(ex, ey, s * .13, s * .065, k * .25, 0, 7); g.fill(); g.fillStyle = '#0a0a0a'; g.beginPath(); g.ellipse(ex, ey, s * .025, s * .06, 0, 0, 7); g.fill(); g.fillStyle = 'rgba(255,255,255,.8)'; g.beginPath(); g.arc(ex - s * .03, ey - s * .02, s * .012, 0, 7); g.fill(); });
      g.fillStyle = '#070707'; g.beginPath(); g.moveTo(-s * .12, s * .25); g.quadraticCurveTo(0, s * .2, s * .12, s * .25); g.quadraticCurveTo(0, s * .38, -s * .12, s * .25); g.fill();
      g.strokeStyle = 'rgba(200,200,210,.25)'; g.lineWidth = 1.5; [-1, 1].forEach(k => { for (let i = 0; i < 5; i++) { g.beginPath(); g.moveTo(k * s * .18, s * .36 + i * 6); g.quadraticCurveTo(k * s * .6, s * .3 + i * 12, k * s * .95, s * .28 + i * 22); g.stroke(); } });
      g.restore();
      g.fillStyle = goldGrad(g, W, H); g.font = `600 ${Math.round(H * .03)}px "Cormorant Garamond", Georgia, serif`; g.textAlign = 'center'; g.fillText('F A R T U Z Z I', W * .5, H * .95);
    } else if (kind === 'kintsugi') {
      const bg = g.createLinearGradient(0, 0, W, H); bg.addColorStop(0, '#121212'); bg.addColorStop(1, '#1e1b18'); g.fillStyle = bg; g.fillRect(0, 0, W, H);
      for (let i = 0; i < 30000; i++) { g.fillStyle = `rgba(255,255,255,${Math.random() * .02})`; g.fillRect(Math.random() * W, Math.random() * H, 2, 2); }
      const crack = (x, y, a, len, wdt) => { g.strokeStyle = goldGrad(g, W, H); g.lineWidth = wdt; g.lineCap = 'round'; g.beginPath(); g.moveTo(x, y); for (let t = 0; t < len; t += 14) { a += (Math.random() - .5) * .6; x += Math.cos(a) * 14; y += Math.sin(a) * 14; g.lineTo(x, y); if (Math.random() < .05 && wdt > 2) crack(x, y, a + (Math.random() < .5 ? .9 : -.9), len * .4, wdt * .55); } g.stroke(); };
      for (let i = 0; i < 6; i++) crack(Math.random() * W, Math.random() < .5 ? 0 : H, Math.random() * 6.28, W * 1.2, 9);
      for (let i = 0; i < 18; i++) { g.fillStyle = goldGrad(g, W, H); g.globalAlpha = .5 + Math.random() * .5; const x = Math.random() * W, y = Math.random() * H, r = 6 + Math.random() * 30; g.beginPath(); for (let k = 0; k < 7; k++) { const a = k / 7 * 6.28; g.lineTo(x + Math.cos(a) * r * (0.6 + Math.random() * .5), y + Math.sin(a) * r * (0.6 + Math.random() * .5)); } g.fill(); }
      g.globalAlpha = 1;
    } else {
      g.fillStyle = '#e9e4da'; g.fillRect(0, 0, W, H);
      [['#111', .2, .2, .35, .5], ['#c9a45c', .5, .35, .3, .45], ['#5a3a22', .3, .62, .4, .22]].forEach(([c, x, y, w2, h2]) => { g.fillStyle = c; g.fillRect(x * W, y * H, w2 * W, h2 * H); });
    }
  });
  function painting(x, y, z, rotY, w, h, kind) {
    const p = new THREE.Group(); p.position.set(x, y, z); p.rotation.y = rotY; scene.add(p);
    const fw = 0.1, fd = 0.09;
    // moldura de galeria: preto laqueado com filete de ouro e passe-partout
    [[0, h / 2 + fw / 2, w + 2 * fw, fw], [0, -h / 2 - fw / 2, w + 2 * fw, fw], [-w / 2 - fw / 2, 0, fw, h], [w / 2 + fw / 2, 0, fw, h]].forEach(([fx, fy, bw, bh]) => mesh(rbox(bw, bh, fd, 0.02, 2), phys(0x0b0b0b, { roughness: 0.18, clearcoat: 1 }), p, [fx, fy, 0], null, false));
    [[0, h / 2 + 0.012, w + 0.04, 0.012], [0, -h / 2 - 0.012, w + 0.04, 0.012], [-w / 2 - 0.012, 0, 0.012, h + 0.04], [w / 2 + 0.012, 0, 0.012, h + 0.04]].forEach(([fx, fy, bw, bh]) => mesh(box(bw, bh, fd + 0.004), M.gold, p, [fx, fy, 0.002], null, false));
    mesh(box(w, h, 0.02), mat(0xece6da, { roughness: 0.9 }), p, [0, 0, -0.01], null, false);
    const m = 0.06;
    mesh(new THREE.PlaneGeometry(w - 2 * m, h - 2 * m), mat(0xffffff, { map: art(kind, w - 2 * m, h - 2 * m), roughness: 0.55 }), p, [0, 0, 0.003], null, false);
    // luz de quadro em latão com lavagem de luz quente (sem luz de verdade, só brilho)
    const arm = new THREE.Group(); arm.position.set(0, h / 2 + fw + 0.03, 0.02); p.add(arm);
    mesh(cyl(0.012, 0.012, 0.22, 10), M.gold, arm, [0, 0.02, 0.1], [Math.PI / 2 - 0.5, 0, 0], false);
    mesh(cyl(0.035, 0.035, w * 0.6, 20), M.gold, arm, [0, 0.07, 0.2], [0, 0, Math.PI / 2], false);
    mesh(box(w * 0.58, 0.008, 0.03), new THREE.MeshBasicMaterial({ color: 0xfff0cf, toneMapped: false }), arm, [0, 0.04, 0.2], null, false);
    const washT = tex(256, 256, (c, W2, H2) => { const gr = c.createLinearGradient(0, 0, 0, H2); gr.addColorStop(0, 'rgba(255,225,170,.22)'); gr.addColorStop(.5, 'rgba(255,225,170,.08)'); gr.addColorStop(1, 'rgba(255,225,170,0)'); c.fillStyle = gr; c.fillRect(0, 0, W2, H2); const sx = c.createLinearGradient(0, 0, W2, 0); sx.addColorStop(0, 'rgba(0,0,0,1)'); sx.addColorStop(.2, 'rgba(0,0,0,0)'); sx.addColorStop(.8, 'rgba(0,0,0,0)'); sx.addColorStop(1, 'rgba(0,0,0,1)'); c.globalCompositeOperation = 'destination-out'; c.fillStyle = sx; c.fillRect(0, 0, W2, H2); });
    const wash = mesh(new THREE.PlaneGeometry(w + 0.5, h * 0.9), new THREE.MeshBasicMaterial({ map: washT, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false }), p, [0, h * 0.12, 0.012], null, false); wash.renderOrder = 2; wash.userData.keep = true;
    if (Math.abs(z - 8.9) < 0.2) out.southItems.push(p); if (x < -11.5) out.westItems.push(p);
    return p;
  }
  painting(6.6, 2.15, 8.9, Math.PI, 1.6, 2.0, 'sol');
  painting(-11.9, 2.15, 6.2, Math.PI / 2, 2.9, 1.7, 'shanshui');
  painting(-11.9, 2.2, 2.7, Math.PI / 2, 1.7, 2.2, 'pantera');      // retrato da Fartuzzi, onde era a adega pequena
  painting(8.5, 2.2, 4.15, -Math.PI / 2, 1.6, 1.15, 'kintsugi');   // parede do banheiro, de frente pro fosso de pôquer
  // brasão Carnucci acima da entrada (lado de dentro)
  goldLogo(LOGO, 512).then(t => out.southItems.push(mesh(new THREE.PlaneGeometry(0.9, 0.9), new THREE.MeshStandardMaterial({ map: t, transparent: true, metalness: 0.8, roughness: 0.3, emissive: 0x3a2a10, emissiveMap: t }), scene, [3.6, 3.6, 8.9], [0, Math.PI, 0], false)));

  wineWall(scene, out);

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
    night: { top: C(0x03060f), hor: C(0x111833), sun: 0, hemi: 0.4, win: 0.55, inside: 0.85, exp: 0.82, fog: C(0x0d1228) },
    dusk: { top: C(0x1d2c5c), hor: C(0xff8a4c), sun: 1.2, hemi: 0.5, win: 0.6, inside: 0.8, exp: 0.88, fog: C(0x7a5a6a) },
    day: { top: C(0x2f6fd0), hor: C(0xd9e7f2), sun: 3.0, hemi: 0.7, win: 0.03, inside: 0.4, exp: 0.82, fog: C(0xc7dbeb) },
  };
  scene.fog = new THREE.Fog(0x0d1228, 110, 1150); scene.background = new THREE.Color(0x0b0a09);
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

// ---------- ADEGA: a parede sul inteira, do chão ao teto, atrás do bar ----------
function wineWall(scene, out) {
  const X0 = -11.4, X1 = 1.8, W = X1 - X0, H = ROOM.H, ZB = 8.88, D = 0.42, cx = (X0 + X1) / 2;
  const g = new THREE.Group(); scene.add(g); out.southItems.push(g);
  const walnut = phys(0x1a120c, { roughness: 0.35, clearcoat: 0.6 });
  mesh(box(W, H, 0.04), walnut, g, [cx, H / 2, ZB], null, false);
  // luz de fundo quente com faixas sob cada prateleira (1 malha, sem luz extra)
  const ROWS = 11, Y0 = 0.32, DY = 0.31;
  const glow = tex(2048, 512, (c, w, h) => {
    const gr = c.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, '#1c1108'); gr.addColorStop(0.5, '#3a2410'); gr.addColorStop(1, '#140c06'); c.fillStyle = gr; c.fillRect(0, 0, w, h);
    for (let r = 0; r <= ROWS; r++) { const y = h - (Y0 + r * DY) / H * h; const b = c.createLinearGradient(0, y - 22, 0, y + 4); b.addColorStop(0, 'rgba(255,214,150,0)'); b.addColorStop(0.85, 'rgba(255,190,110,.55)'); b.addColorStop(1, 'rgba(255,220,160,.9)'); c.fillStyle = b; c.fillRect(0, y - 22, w, 26); }
  });
  mesh(new THREE.PlaneGeometry(W - 0.1, H - 0.1), new THREE.MeshBasicMaterial({ map: glow, toneMapped: false }), g, [cx, H / 2, ZB - 0.025], [0, Math.PI, 0], false).name = 'wineGlow';
  // prateleiras e montantes (ouro escovado + preto)
  for (let r = 0; r <= ROWS; r++) mesh(box(W, 0.018, D), M.goldDim, g, [cx, Y0 + r * DY, ZB - D / 2], null, false);
  const nCols = 13;
  for (let i = 0; i <= nCols; i++) { const x = X0 + i * W / nCols; mesh(box(0.05, H, D + 0.02), M.black, g, [x, H / 2, ZB - D / 2], null, false); mesh(box(0.012, H, 0.012), M.gold, g, [x, H / 2, ZB - D - 0.005], null, false); }
  mesh(box(W, 0.06, D + 0.04), M.gold, g, [cx, H - 0.03, ZB - D / 2], null, false); mesh(box(W, 0.12, D + 0.04), M.black, g, [cx, 0.06, ZB - D / 2], null, false);
  // garrafas deitadas, gargalo pra frente (instanciadas: 2 draws pra mais de mil garrafas)
  const per = 11, n = nCols * per * ROWS;
  const body = new THREE.InstancedMesh(new THREE.CylinderGeometry(0.037, 0.037, 0.22, 7, 1, false).rotateX(Math.PI / 2), new THREE.MeshStandardMaterial({ roughness: 0.32, metalness: 0.0, envMapIntensity: 0.35 }), n);
  const neck = new THREE.InstancedMesh(new THREE.CylinderGeometry(0.013, 0.02, 0.09, 6, 1, true).rotateX(Math.PI / 2), new THREE.MeshStandardMaterial({ roughness: 0.35, metalness: 0.5, envMapIntensity: 0.5 }), n);
  const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), sc = new THREE.Vector3(1, 1, 1), col = new THREE.Color();
  const glassC = [0x0a1f0e, 0x1a0f05, 0x070707, 0x240806, 0x0e1a0a], foilC = [0x8a1c1c, 0xc9a45c, 0x111111, 0xd8d0c0, 0x5a1020];
  let k = 0;
  for (let r = 0; r < ROWS; r++) for (let c2 = 0; c2 < nCols; c2++) for (let j = 0; j < per; j++) {
    const x = X0 + c2 * W / nCols + 0.07 + j * ((W / nCols - 0.14) / (per - 1)), y = Y0 + r * DY + 0.05 + (j % 2) * 0.075, z = ZB - 0.17;
    const hidden = x < -6.4 && y < 1.1; // escondida atrás do balcão
    m4.compose(new THREE.Vector3(x, hidden ? -5 : y, z), q, sc); body.setMatrixAt(k, m4); body.setColorAt(k, col.setHex(glassC[(r * 7 + c2 * 3 + j) % glassC.length]));
    m4.compose(new THREE.Vector3(x, hidden ? -5 : y, z - 0.155), q, sc); neck.setMatrixAt(k, m4); neck.setColorAt(k, col.setHex(foilC[(r * 5 + c2 + j * 3) % foilC.length])); k++;
  }
  [body, neck].forEach(m => { m.instanceMatrix.needsUpdate = true; m.instanceColor.needsUpdate = true; m.frustumCulled = false; m.userData.keep = true; g.add(m); });
  // nicho dos destilados de luxo no meio (clique abre o estoque)
  const niche = new THREE.Group(); niche.position.set(-2.95, 0, 0); g.add(niche);
  const nW = W / nCols - 0.06;
  mesh(box(nW, 1.3, 0.05), new THREE.MeshBasicMaterial({ color: 0xffdfa8, toneMapped: false }), niche, [0, 1.95, ZB - 0.06], null, false);
  mesh(box(nW, 0.04, D), M.gold, niche, [0, 1.32, ZB - D / 2], null, false); mesh(box(nW, 0.04, D), M.gold, niche, [0, 2.62, ZB - D / 2], null, false);
  const amber = phys(0x7a3e10, { roughness: 0.05, clearcoat: 1 }), dark = phys(0x10241a, { roughness: 0.05, clearcoat: 1 }), blue = phys(0x10204a, { roughness: 0.05, clearcoat: 1 });
  [[-0.32, amber, 'dec'], [-0.1, blue, 'sq'], [0.12, amber, 'sq'], [0.33, dark, 'dec']].forEach(([x, m, kind]) => {
    if (kind === 'dec') { const b = mesh(sph(0.09, 20, 16), m, niche, [x, 1.46, ZB - 0.22]); b.scale.set(1, 1.15, 0.8); mesh(cyl(0.025, 0.04, 0.1, 14), m, niche, [x, 1.62, ZB - 0.22]); mesh(sph(0.035, 12, 10), M.gold, niche, [x, 1.7, ZB - 0.22]); }
    else { mesh(rbox(0.12, 0.26, 0.08, 0.015), m, niche, [x, 1.47, ZB - 0.22]); mesh(cyl(0.02, 0.025, 0.08, 12), m, niche, [x, 1.64, ZB - 0.22]); mesh(cyl(0.024, 0.024, 0.04, 12), M.gold, niche, [x, 1.7, ZB - 0.22]); }
    mesh(cyl(0.07, 0.08, 0.02, 20), M.gold, niche, [x, 1.345, ZB - 0.22]);
  });
  niche.traverse(o => { if (o.isMesh) o.userData.stock = 'adega'; });
  // portas de vidro com moldura dourada
  const glassM = new THREE.MeshPhysicalMaterial({ color: 0xffffff, transparent: true, opacity: 0.08, roughness: 0.02, depthWrite: false });
  // trilho de latão e escada de biblioteca
  mesh(cyl(0.018, 0.018, W, 10), M.gold, g, [cx, 3.55, ZB - D - 0.12], [0, 0, Math.PI / 2], false);
  const lad = new THREE.Group(); lad.position.set(-0.6, 0, ZB - D - 0.12); lad.rotation.x = 0.22; g.add(lad);
  [-0.22, 0.22].forEach(x => mesh(box(0.04, 3.7, 0.05), walnut, lad, [x, 1.8, -0.4], null, false));
  for (let i = 0; i < 11; i++) mesh(cyl(0.015, 0.015, 0.44, 8), M.gold, lad, [0, 0.25 + i * 0.32, -0.4], [0, 0, Math.PI / 2], false);
}
