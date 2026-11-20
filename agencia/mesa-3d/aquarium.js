import * as THREE from 'three';
import { mergeGeometries } from 'three/examples/jsm/utils/BufferGeometryUtils.js';
import { M, mat, mesh, box, tex, clamp, lerp } from './util.js';
import { AQ } from './env.js';

// Aquário gigante embaixo do piso de vidro: a gente anda por cima, o tubarão nada embaixo.
// Tudo que fica dentro d'água recebe o mesmo "banho" no shader: azul que aumenta com a profundidade + cáusticas animadas.
const U = { uT: { value: 0 } };
const GLSL_CAUSTIC = `
uniform float uT;
varying vec3 vWP;
float causticF(vec2 p, float t) {
  vec2 q = p * 1.9; float c = 0.0;
  for (int i = 0; i < 3; i++) { q += vec2(sin(q.y * 1.37 + t * 0.71), cos(q.x * 1.13 - t * 0.63)); c += 1.0 / (1.0 + 16.0 * abs(sin(q.x) + cos(q.y))); }
  return c;
}`;
const D = AQ.D;
// aplica água num MeshStandardMaterial (funciona com esqueleto e com instância)
function water(m, k = 1) {
  m.onBeforeCompile = sh => {
    sh.uniforms.uT = U.uT;
    sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nvarying vec3 vWP;')
      .replace('#include <project_vertex>', `#include <project_vertex>
        vec4 wpA = vec4(transformed, 1.0);
        #ifdef USE_INSTANCING
          wpA = instanceMatrix * wpA;
        #endif
        vWP = (modelMatrix * wpA).xyz;`);
    sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\n' + GLSL_CAUSTIC)
      .replace('#include <fog_fragment>', `#include <fog_fragment>
        float dep = clamp(-vWP.y / ${D.toFixed(2)}, 0.0, 1.0);
        vec3 deep = vec3(0.01, 0.10, 0.17), shallow = vec3(0.05, 0.36, 0.48);
        gl_FragColor.rgb = mix(gl_FragColor.rgb * vec3(0.62, 0.86, 0.95), mix(shallow, deep, dep), (0.18 + 0.5 * dep) * ${k.toFixed(2)});
        gl_FragColor.rgb += vec3(0.55, 0.85, 0.95) * causticF(vWP.xz, uT) * 0.13 * (1.0 - dep * 0.55) * ${k.toFixed(2)};`);
  };
  m.customProgramCacheKey = () => 'water' + k;
  return m;
}
// paredes e areia: sem luz da sala (barato), só cor + cáustica + luz azul vinda de baixo
function waterSurf(colorA, colorB, texMap, causticK) {
  return new THREE.ShaderMaterial({
    uniforms: { uT: U.uT, map: { value: texMap }, cA: { value: new THREE.Color(colorA) }, cB: { value: new THREE.Color(colorB) } },
    vertexShader: `varying vec3 vWP; varying vec2 vUv; void main() { vUv = uv; vec4 w = modelMatrix * vec4(position, 1.0); vWP = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }`,
    fragmentShader: GLSL_CAUSTIC + `
      uniform sampler2D map; uniform vec3 cA; uniform vec3 cB; varying vec2 vUv;
      void main() {
        float dep = clamp(-vWP.y / ${D.toFixed(2)}, 0.0, 1.0);
        vec3 base = mix(cA, cB, dep) * (0.75 + 0.5 * texture2D(map, vUv).r);
        float c = causticF(vWP.xz + vec2(0.0, vWP.y * 0.4), uT);
        vec3 col = base + vec3(0.45, 0.85, 1.0) * c * ${causticK.toFixed(2)};
        gl_FragColor = vec4(col, 1.0);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }`,
  });
}
const V = (x, y, z) => new THREE.Vector3(x, y, z);

// ---------- tubarão: malha única com esqueleto ----------
function buildShark() {
  const L = 1.75; // comprimento
  const bones = []; const root = new THREE.Bone(); bones.push(root);
  const NB = 7, bz = []; let parent = root;
  for (let i = 0; i < NB; i++) { const z = L * 0.42 - i * (L * 0.88 / (NB - 1)); bz.push(z); const b = new THREE.Bone(); b.position.z = i === 0 ? z : z - bz[i - 1]; parent.add(b); bones.push(b); parent = b; }
  const boneAt = z => { // pesos entre os 2 ossos mais próximos
    if (z >= bz[0]) return [[1, 1]];
    for (let i = 0; i < NB - 1; i++) if (z <= bz[i] && z >= bz[i + 1]) { const t = (bz[i] - z) / (bz[i] - bz[i + 1]); return [[i + 1, 1 - t], [i + 2, t]]; }
    return [[NB, 1]];
  };
  const pos = [], col = [], si = [], sw = [], idx = [];
  const C = new THREE.Color(), DORSO = new THREE.Color(0x56616c), BARRIGA = new THREE.Color(0xe7eaec), ESCURO = new THREE.Color(0x1b2026);
  const push = (x, y, z, c) => { pos.push(x, y, z); col.push(c.r, c.g, c.b); const w = boneAt(z); si.push(w[0][0], w[1] ? w[1][0] : 0, 0, 0); sw.push(w[0][1], w[1] ? w[1][1] : 0, 0, 0); return pos.length / 3 - 1; };
  // corpo: anéis de seção oval ao longo de z (nariz em +z)
  const SL = 44, SR = 22, z0 = L * 0.5, z1 = -L * 0.5;
  const prof = t => { // t 0 nariz → 1 cauda : [meia-largura, meia-altura, deslocamento y]
    const nose = clamp(t / 0.16, 0, 1), body = Math.pow(nose, 0.55) * (1 - Math.pow(clamp((t - 0.32) / 0.68, 0, 1), 1.25) * 0.93);
    return [0.155 * body + 0.004, 0.18 * body + 0.004, -0.02 * Math.sin(Math.PI * clamp(t, 0, 0.6) / 0.6) + 0.012 * (1 - nose)];
  };
  for (let i = 0; i <= SL; i++) {
    const t = i / SL, z = lerp(z0, z1, t), [rw, rh, dy] = prof(t);
    for (let j = 0; j <= SR; j++) {
      const a = j / SR * Math.PI * 2, s = Math.sin(a), c = Math.cos(a);
      const flat = s < 0 ? 0.82 : 1; // barriga mais reta
      const x = c * rw, y = s * rh * flat + dy;
      let k = clamp((s + 0.15) * 1.6, 0, 1); C.copy(BARRIGA).lerp(DORSO, k);
      // guelras: 5 fendas nas laterais
      if (t > 0.19 && t < 0.29 && Math.abs(c) > 0.55 && s > -0.55 && s < 0.45) { const gi = (t - 0.19) / 0.1 * 5; if (gi % 1 > 0.62) C.lerp(ESCURO, 0.75); }
      // boca: faixa escura embaixo do focinho
      if (t > 0.075 && t < 0.11 && s < -0.55 && Math.abs(c) < 0.75) C.lerp(ESCURO, 0.85);
      push(x, y, z, C.clone());
    }
  }
  const R = SR + 1;
  for (let i = 0; i < SL; i++) for (let j = 0; j < SR; j++) { const a = i * R + j, b = a + R; idx.push(a, b, a + 1, b, b + 1, a + 1); }
  { const c0 = push(0, prof(0)[2], z0 + 0.01, DORSO); for (let j = 0; j < SR; j++) idx.push(c0, j, j + 1); }
  const body = new THREE.BufferGeometry();
  body.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); body.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
  body.setAttribute('skinIndex', new THREE.Uint16BufferAttribute(si, 4)); body.setAttribute('skinWeight', new THREE.Float32BufferAttribute(sw, 4)); body.setIndex(idx); body.computeVertexNormals();
  // nadadeiras: formas extrudadas finas presas ao corpo
  const fin = (pts, thick, place, color) => {
    const sh = new THREE.Shape(pts.map(([a, b]) => new THREE.Vector2(a, b)));
    let g = new THREE.ExtrudeGeometry(sh, { depth: thick, bevelEnabled: true, bevelThickness: thick * 0.4, bevelSize: thick * 0.5, bevelSegments: 2, curveSegments: 8 });
    g.translate(0, 0, -thick / 2); place(g); g = g.toNonIndexed(); g.computeVertexNormals();
    const n = g.attributes.position.count, cc = new Float32Array(n * 3), s1 = new Uint16Array(n * 4), w1 = new Float32Array(n * 4);
    for (let i = 0; i < n; i++) { cc.set([color.r, color.g, color.b], i * 3); const w = boneAt(g.attributes.position.getZ(i)); s1[i * 4] = w[0][0]; w1[i * 4] = w[0][1]; if (w[1]) { s1[i * 4 + 1] = w[1][0]; w1[i * 4 + 1] = w[1][1]; } }
    g.deleteAttribute('uv'); g.setAttribute('color', new THREE.BufferAttribute(cc, 3)); g.setAttribute('skinIndex', new THREE.BufferAttribute(s1, 4)); g.setAttribute('skinWeight', new THREE.BufferAttribute(w1, 4));
    return g;
  };
  const fins = [];
  const DF = DORSO.clone().multiplyScalar(0.92);
  // dorsal (no plano yz)
  fins.push(fin([[0, 0], [0.34, 0], [0.12, 0.3], [0.04, 0.27]], 0.018, g => { g.rotateY(Math.PI / 2); g.translate(0, 0.15, 0.12); }, DF));
  // segunda dorsal e anal pequenas
  fins.push(fin([[0, 0], [0.09, 0], [0.03, 0.07]], 0.01, g => { g.rotateY(Math.PI / 2); g.translate(0, 0.07, -0.42); }, DF));
  fins.push(fin([[0, 0], [0.08, 0], [0.025, -0.06]], 0.01, g => { g.rotateY(Math.PI / 2); g.translate(0, -0.06, -0.44); }, DF));
  // cauda heterocerca (lobo de cima maior)
  fins.push(fin([[0, 0.02], [0.06, 0.06], [0.3, 0.34], [0.22, 0.32], [0.07, 0.02], [0.2, -0.2], [0.13, -0.19], [0.0, -0.03]], 0.014, g => { g.rotateY(Math.PI / 2); g.translate(0, 0.0, -L * 0.47); }, DF));
  // peitorais (inclinadas pra baixo e pra trás)
  [-1, 1].forEach(s => fins.push(fin([[0, 0.04], [0.13, 0.02], [0.36, -0.2], [0.31, -0.24], [0.04, -0.1]], 0.012, g => { g.rotateX(Math.PI / 2); if (s < 0) g.scale(-1, 1, 1); g.rotateZ(s * -0.45); g.translate(s * 0.1, -0.1, 0.24); }, DF)));
  // pélvicas
  [-1, 1].forEach(s => fins.push(fin([[0, 0.02], [0.06, 0.0], [0.1, -0.07], [0.02, -0.05]], 0.008, g => { g.rotateX(Math.PI / 2); if (s < 0) g.scale(-1, 1, 1); g.rotateZ(s * -0.6); g.translate(s * 0.05, -0.1, -0.2); }, DF)));
  const parts = [body, ...fins].map(g => { const n = g.attributes.position.count; ['position', 'normal', 'color', 'skinIndex', 'skinWeight'].forEach(k => { if (!g.attributes[k]) console.warn('falta', k); }); return g; });
  // padroniza índices (mergeGeometries exige todos indexados ou nenhum)
  const geo = mergeGeometries(parts.map(g => (g.index ? g.toNonIndexed() : g)), false);
  const m = water(new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.42, metalness: 0.0 }), 0.75);
  const sk = new THREE.SkinnedMesh(geo, m); sk.frustumCulled = false;
  sk.add(root); sk.updateMatrixWorld(true); sk.bind(new THREE.Skeleton(bones));
  // olhos
  [-1, 1].forEach(s => { const e = new THREE.Mesh(new THREE.SphereGeometry(0.014, 10, 8), water(new THREE.MeshStandardMaterial({ color: 0x050607, roughness: 0.1 }), 0.4)); e.position.set(s * 0.085, 0.045, L * 0.5 - 0.17 - bz[0]); e.userData.keep = true; bones[1].add(e); });
  const g = new THREE.Group(); g.add(sk);
  return { g, bones: bones.slice(1), L, mesh: sk };
}

export function buildAquarium(scene) {
  const W = AQ.x1 - AQ.x0, H = AQ.z1 - AQ.z0, cx = (AQ.x0 + AQ.x1) / 2, cz = (AQ.z0 + AQ.z1) / 2;
  const g = new THREE.Group(); g.position.set(cx, 0, cz); scene.add(g);
  const noise = (w, h, f) => tex(w, h, (c) => { c.fillStyle = '#808080'; c.fillRect(0, 0, w, h); f(c, w, h); });
  // paredes internas (mosaico azul-escuro) e fundo de areia com marcas de ondulação
  const tileT = noise(256, 256, (c, w, h) => { for (let x = 0; x < w; x += 32) for (let y = 0; y < h; y += 32) { const v = 100 + Math.random() * 50 | 0; c.fillStyle = `rgb(${v},${v},${v})`; c.fillRect(x + 1, y + 1, 30, 30); } });
  tileT.repeat.set(W / 0.5, D / 0.5); tileT.wrapS = tileT.wrapT = THREE.RepeatWrapping;
  const sandT = noise(512, 512, (c, w, h) => { for (let i = 0; i < 26000; i++) { const v = 90 + Math.random() * 90 | 0; c.fillStyle = `rgba(${v},${v},${v},.5)`; c.fillRect(Math.random() * w, Math.random() * h, 2, 2); } c.strokeStyle = 'rgba(255,255,255,.18)'; for (let y = 0; y < h; y += 14) { c.lineWidth = 3; c.beginPath(); for (let x = 0; x <= w; x += 16) c.lineTo(x, y + Math.sin(x * 0.05 + y) * 4); c.stroke(); } });
  sandT.wrapS = sandT.wrapT = THREE.RepeatWrapping; sandT.repeat.set(W / 1.6, H / 1.6);
  const wallM = waterSurf(0x0b3a52, 0x031a28, tileT, 0.09), sandM = waterSurf(0x9a8d6a, 0x2c4a52, sandT, 0.14);
  const wg = (w, h, x, y, z, ry) => { const q = new THREE.PlaneGeometry(w, h); q.rotateY(ry); q.translate(x, y, z); return q; };
  const walls = new THREE.Mesh(mergeGeometries([wg(W, D, 0, -D / 2, -H / 2, 0), wg(W, D, 0, -D / 2, H / 2, Math.PI), wg(H, D, -W / 2, -D / 2, 0, Math.PI / 2), wg(H, D, W / 2, -D / 2, 0, -Math.PI / 2)]), wallM); walls.userData.keep = true; g.add(walls);
  const sand = new THREE.Mesh(new THREE.PlaneGeometry(W, H, 40, 12), sandM); sand.rotation.x = -Math.PI / 2; sand.position.y = -D; sand.userData.keep = true;
  { const p = sand.geometry.attributes.position; for (let i = 0; i < p.count; i++) p.setZ(i, Math.sin(p.getX(i) * 1.7) * 0.04 + Math.cos(p.getY(i) * 2.3 + p.getX(i)) * 0.03 + 0.04); sand.geometry.computeVertexNormals(); }
  g.add(sand);
  // pedras (malha única) e corais simples
  const rockM = water(new THREE.MeshStandardMaterial({ color: 0x6b6258, roughness: 0.95 }), 0.8);
  const rocks = [];
  for (let i = 0; i < 14; i++) {
    let r = new THREE.IcosahedronGeometry(0.12 + Math.random() * 0.28, 3); const p = r.attributes.position, sd = Math.random() * 9;
    for (let k = 0; k < p.count; k++) { const x = p.getX(k), y = p.getY(k), z = p.getZ(k); const s = 0.8 + 0.25 * Math.sin(x * 9 + sd) * Math.cos(z * 7 + sd) + 0.12 * Math.sin(y * 15 + sd); p.setXYZ(k, x * s, y * s * 0.65, z * s); }
    const side = i % 2 ? -1 : 1, x = (Math.random() - 0.5) * (W - 0.6), z = side * (H / 2 - 0.2 - Math.random() * 0.35);
    r.translate(x, -D + 0.06, z); r.deleteAttribute('uv'); r.computeVertexNormals(); rocks.push(r);
  }
  const rockMesh = new THREE.Mesh(mergeGeometries(rocks), rockM); rockMesh.userData.keep = true; g.add(rockMesh);
  // plantas: fitas que balançam (no shader)
  const kelpM = new THREE.MeshStandardMaterial({ color: 0x2f6b3a, roughness: 0.7, side: THREE.DoubleSide });
  kelpM.onBeforeCompile = sh => { sh.uniforms.uT = U.uT;
    sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nuniform float uT;\nvarying vec3 vWP;').replace('#include <begin_vertex>', `#include <begin_vertex>
      float hh = uv.y; float ph = position.x * 3.0 + position.z * 2.0;
      transformed.x += sin(uT * 1.3 + ph + hh * 2.5) * 0.09 * hh * hh; transformed.z += cos(uT * 1.1 + ph * 0.7 + hh * 2.0) * 0.06 * hh * hh;`)
      .replace('#include <project_vertex>', '#include <project_vertex>\nvWP = (modelMatrix * vec4(transformed, 1.0)).xyz;');
    sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\n' + GLSL_CAUSTIC).replace('#include <fog_fragment>', `#include <fog_fragment>
      float dep = clamp(-vWP.y / ${D.toFixed(2)}, 0.0, 1.0); gl_FragColor.rgb = mix(gl_FragColor.rgb * vec3(0.6,0.9,0.9), vec3(0.02,0.14,0.2), 0.2 + 0.45 * dep);`); };
  kelpM.customProgramCacheKey = () => 'kelp';
  const kelps = [];
  for (let i = 0; i < 22; i++) {
    const h = 0.6 + Math.random() * 0.75, k = new THREE.PlaneGeometry(0.07 + Math.random() * 0.05, h, 1, 8); k.translate(0, h / 2, 0);
    k.rotateY(Math.random() * Math.PI); const side = i % 2 ? -1 : 1;
    k.translate((Math.random() - 0.5) * (W - 0.5), -D + 0.04, side * (H / 2 - 0.15 - Math.random() * 0.4)); kelps.push(k);
  }
  const kelp = new THREE.Mesh(mergeGeometries(kelps), kelpM); kelp.userData.keep = true; g.add(kelp);
  // cardume (instâncias)
  const fishG = (() => {
    const b = new THREE.SphereGeometry(1, 10, 6); b.scale(0.011, 0.024, 0.055); b.translate(0, 0, 0.01);
    const ts = new THREE.Shape([new THREE.Vector2(0, 0), new THREE.Vector2(-0.035, 0.028), new THREE.Vector2(-0.028, 0), new THREE.Vector2(-0.035, -0.028)]);
    const t = new THREE.ShapeGeometry(ts); t.rotateY(Math.PI / 2); t.translate(0, 0, -0.04);
    const t2 = t.clone(); t2.rotateY(Math.PI); t2.translate(0, 0, -0.08); // verso da cauda
    return mergeGeometries([b.toNonIndexed(), t.toNonIndexed(), t2.toNonIndexed()].map(g => { g.deleteAttribute('uv'); return g; }));
  })();
  const NF = 34, fish = new THREE.InstancedMesh(fishG, water(new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.3, metalness: 0.35, side: THREE.DoubleSide }), 0.55), NF);
  fish.frustumCulled = false; fish.userData.keep = true; g.add(fish);
  const fishData = Array.from({ length: NF }, (_, i) => ({ o: Math.random() * Math.PI * 2, r: (Math.random() - 0.5) * 0.35, y: -0.45 - Math.random() * 0.5, s: 0.85 + Math.random() * 0.3, c: i % 5 === 0 }));
  { const c1 = new THREE.Color(0xd9dee2), c2 = new THREE.Color(0xe8a93a); fishData.forEach((f, i) => fish.setColorAt(i, f.c ? c2 : c1)); }
  // bolhas
  const NBUB = 30, bubM = new THREE.MeshBasicMaterial({ color: 0xcff4ff, transparent: true, opacity: 0.45, depthWrite: false });
  const bub = new THREE.InstancedMesh(new THREE.SphereGeometry(0.018, 8, 6), bubM, NBUB); bub.frustumCulled = false; bub.userData.keep = true; g.add(bub);
  const cols = [[-W * 0.36, -H * 0.3], [W * 0.05, H * 0.32], [W * 0.38, -H * 0.25]];
  const bubData = Array.from({ length: NBUB }, (_, i) => ({ c: cols[i % 3], y: Math.random() * D, v: 0.25 + Math.random() * 0.2, w: Math.random() * 6 }));
  // luz azul subindo pela borda (some na sala clara, aparece bonito à noite)
  const glowT = tex(256, 256, (c, w, h) => { const gr = c.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, 'rgba(80,200,255,0)'); gr.addColorStop(1, 'rgba(80,200,255,1)'); c.fillStyle = gr; c.fillRect(0, 0, w, h); });
  const glowM = new THREE.MeshBasicMaterial({ map: glowT, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, opacity: 0.22, toneMapped: false });
  const glowMesh = new THREE.Mesh(mergeGeometries([wg(W, 0.5, 0, -0.25, -H / 2 + 0.01, 0), wg(W, 0.5, 0, -0.25, H / 2 - 0.01, Math.PI), wg(H, 0.5, -W / 2 + 0.01, -0.25, 0, Math.PI / 2), wg(H, 0.5, W / 2 - 0.01, -0.25, 0, -Math.PI / 2)]), glowM);
  glowMesh.renderOrder = 4; glowMesh.userData.keep = true; g.add(glowMesh);
  // vidro grosso do piso: placas com junta de aço escuro e moldura dourada
  const glassM = new THREE.MeshStandardMaterial({ color: 0xbfe6f2, roughness: 0.04, metalness: 0.1, transparent: true, opacity: 0.16, depthWrite: false, envMapIntensity: 1.6 });
  const glass = new THREE.Mesh(new THREE.PlaneGeometry(W, H), glassM); glass.rotation.x = -Math.PI / 2; glass.position.y = -0.006; glass.renderOrder = 5; glass.userData.keep = true; g.add(glass);
  const sheen = new THREE.Mesh(new THREE.PlaneGeometry(W, H), new THREE.MeshBasicMaterial({ color: 0x9fe3ff, transparent: true, opacity: 0.05, depthWrite: false, toneMapped: false, blending: THREE.AdditiveBlending }));
  sheen.rotation.x = -Math.PI / 2; sheen.position.y = -0.004; sheen.renderOrder = 6; sheen.userData.keep = true; g.add(sheen);
  const steel = mat(0x15171a, { metalness: 0.8, roughness: 0.35 });
  { const NP = 6, parts = []; for (let i = 1; i < NP; i++) { const q = new THREE.BoxGeometry(0.022, 0.016, H); q.translate(-W / 2 + W * i / NP, -0.004, 0); parts.push(q); } const q2 = new THREE.BoxGeometry(W, 0.016, 0.022); q2.translate(0, -0.004, 0); parts.push(q2); mesh(mergeGeometries(parts), steel, g, null, null, false); }
  const rim = 0.07;
  mesh(box(W + rim * 2, 0.02, rim), M.gold, g, [0, 0.002, -H / 2 - rim / 2], null, false); mesh(box(W + rim * 2, 0.02, rim), M.gold, g, [0, 0.002, H / 2 + rim / 2], null, false);
  mesh(box(rim, 0.02, H), M.gold, g, [-W / 2 - rim / 2, 0.002, 0], null, false); mesh(box(rim, 0.02, H), M.gold, g, [W / 2 + rim / 2, 0.002, 0], null, false);
  // fita de luz logo abaixo do vidro, nas bordas
  const ledM = new THREE.MeshBasicMaterial({ color: 0x8fe6ff, toneMapped: false });
  { const bx = (w, d, x, z) => { const q = new THREE.BoxGeometry(w, 0.012, d); q.translate(x, -0.05, z); return q; };
    const led = new THREE.Mesh(mergeGeometries([bx(W, 0.012, 0, -H / 2 + 0.02), bx(W, 0.012, 0, H / 2 - 0.02), bx(0.012, H, -W / 2 + 0.02, 0), bx(0.012, H, W / 2 - 0.02, 0)]), ledM); led.userData.keep = true; g.add(led); }

  // tubarão
  const sh = buildShark(); g.add(sh.g); sh.g.scale.setScalar(1.08); sh.g.rotation.order = 'YXZ';
  const hit = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.45, 1.9), new THREE.MeshBasicMaterial({ visible: false })); hit.userData.pet = 'tubarao'; hit.userData.keep = true; sh.g.add(hit);
  // percurso: estádio (duas retas + duas curvas) com subida/descida suave
  const RX = W / 2 - 1.15, RZ = H / 2 - 0.62;
  const perim = 2 * (2 * RX) + 2 * Math.PI * RZ;
  const path = (s) => { // s em metros ao longo do percurso → ponto (x,z) e direção
    s = ((s % perim) + perim) % perim;
    const L = 2 * RX, A = Math.PI * RZ;
    if (s < L) return [RX - s, -RZ, Math.PI * 1.5];
    s -= L; if (s < A) { const a = Math.PI * 1.5 - s / RZ; return [-RX + Math.cos(a) * RZ, Math.sin(a) * RZ, a - Math.PI / 2]; }
    s -= A; if (s < L) return [-RX + s, RZ, Math.PI / 2];
    s -= L; const a = Math.PI / 2 - s / RZ; return [RX + Math.cos(a) * RZ, Math.sin(a) * RZ, a - Math.PI / 2];
  };
  const st = { s: 0, v: 0.55, phase: 0, yaw: Math.PI * 1.5 };
  const m4 = new THREE.Object3D(), up = V(0, 1, 0);
  const out = { group: g, shark: sh, root: sh.g, head: sh.bones[0], name: 'Tubarão Carnucci' };
  out.update = (dt, now) => {
    U.uT.value = now;
    // tubarão
    st.v = 0.5 + Math.sin(now * 0.13) * 0.12; st.s += st.v * dt; st.phase += dt * (3.2 + st.v * 2.2);
    const [x, z] = path(st.s), [x2, z2] = path(st.s + 0.25);
    const yaw = Math.atan2(x2 - x, z2 - z); let dy = yaw - st.yaw; dy = Math.atan2(Math.sin(dy), Math.cos(dy)); st.yaw += dy * Math.min(1, dt * 4);
    const y = -0.82 + Math.sin(st.s * 0.21) * 0.22;
    sh.g.position.set(x, y, z); sh.g.rotation.set(Math.sin(st.s * 0.21 + 1.2) * -0.06, st.yaw, -dy * 2.2);
    sh.bones.forEach((b, i) => { const k = i / (sh.bones.length - 1); b.rotation.y = Math.sin(st.phase - i * 0.75) * (0.03 + 0.2 * k * k) - (i > 0 ? dy * 0.8 * k : 0); });
    // cardume: segue o percurso do outro lado, em bando
    fishData.forEach((f, i) => {
      const s = -st.s * 0.9 + perim * 0.5 + f.o * 0.4 + i * 0.05;
      const [fx, fz] = path(s), [fx2, fz2] = path(s - 0.1);
      const wob = Math.sin(now * 1.7 + f.o) * 0.12;
      m4.position.set(fx * 0.85 + f.r + wob * 0.3, f.y + Math.sin(now + f.o) * 0.05, fz * 0.7 + f.r * 0.6 + wob * 0.2);
      m4.rotation.set(0, Math.atan2(fx2 - fx, fz2 - fz) + Math.sin(now * 8 + f.o) * 0.15, 0); m4.scale.setScalar(f.s); m4.updateMatrix(); fish.setMatrixAt(i, m4.matrix);
    });
    fish.instanceMatrix.needsUpdate = true;
    // bolhas
    bubData.forEach((b, i) => { b.y += b.v * dt; if (b.y > D - 0.05) b.y = 0; m4.position.set(b.c[0] + Math.sin(now * 2 + b.w) * 0.03, -D + 0.05 + b.y, b.c[1] + Math.cos(now * 1.7 + b.w) * 0.03); m4.rotation.set(0, 0, 0); m4.scale.setScalar(0.6 + b.y / D); m4.updateMatrix(); bub.setMatrixAt(i, m4.matrix); });
    bub.instanceMatrix.needsUpdate = true;
  };
  return out;
}
