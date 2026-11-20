import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

// Fênix: pássaro animado (batida de asa real) pintado de fogo e ouro, com rastro de chamas e sopro de fogo
export function buildPhoenix(scene, glbBase64) {
  const root = new THREE.Group(); scene.add(root);
  const out = { root, ready: false };
  const fireCols = new THREE.Color();

  // partículas de fogo (rastro + sopro)
  const N = 520;
  const pos = new Float32Array(N * 3), vel = new Float32Array(N * 3), age = new Float32Array(N), life = new Float32Array(N), size = new Float32Array(N);
  for (let i = 0; i < N; i++) { age[i] = 1; life[i] = 1; pos[i * 3 + 1] = -999; }
  const pg = new THREE.BufferGeometry();
  pg.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  pg.setAttribute('aAge', new THREE.BufferAttribute(age, 1));
  pg.setAttribute('aSize', new THREE.BufferAttribute(size, 1));
  const pm = new THREE.ShaderMaterial({
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
    uniforms: { scale: { value: 600 } },
    vertexShader: `attribute float aAge; attribute float aSize; varying float vAge; uniform float scale;
      void main(){ vAge = aAge; vec4 mv = modelViewMatrix * vec4(position,1.0); gl_PointSize = aSize * scale * (1.0 - aAge*0.5) / -mv.z; gl_Position = projectionMatrix * mv; }`,
    fragmentShader: `varying float vAge; void main(){ vec2 p = gl_PointCoord - 0.5; float d = length(p); if (d > 0.5) discard; float a = smoothstep(0.5, 0.0, d) * (1.0 - vAge);
      vec3 c = mix(vec3(1.0, 0.95, 0.7), vec3(1.0, 0.45, 0.05), smoothstep(0.0, 0.35, vAge)); c = mix(c, vec3(0.6, 0.08, 0.02), smoothstep(0.35, 1.0, vAge));
      gl_FragColor = vec4(c * a * 1.6, 1.0); }`
  });
  const fire = new THREE.Points(pg, pm); fire.frustumCulled = false; scene.add(fire);
  let cursor = 0;
  function emit(p, v, l, s) { const i = cursor; cursor = (cursor + 1) % N; pos.set([p.x, p.y, p.z], i * 3); vel.set([v.x, v.y, v.z], i * 3); age[i] = 0; life[i] = l; size[i] = s; }

  const light = { intensity: 0 }, breathLight = { intensity: 0, position: new THREE.Vector3() };

  // caminho de voo pela sala
  const pts = [[-8, 4.6, -5.5], [-2, 4.2, -7.0], [5, 5.0, -6.3], [9.0, 4.4, -2], [6.5, 5.3, 3.5], [2, 4.2, 6.2], [-4, 4.9, 5.3], [-9, 4.4, 2.5], [-6, 5.4, -1], [0, 4.5, 0.5], [6, 5.0, -1.5], [3, 4.3, -4], [-3, 5.2, -3]];
  const curve = new THREE.CatmullRomCurve3(pts.map(p => new THREE.Vector3(...p)), true, 'centripetal');
  const LEN = curve.getLength();
  let u = 0, roll = 0;
  let mixer = null, model = null;
  const wingL = new THREE.Vector3(), wingR = new THREE.Vector3(), tail = new THREE.Vector3(), beak = new THREE.Vector3();
  let breath = 0, nextBreath = 6;

  // fitas da cauda
  const ribTex = (() => { const c = document.createElement('canvas'); c.width = 32; c.height = 256; const g = c.getContext('2d'); const gr = g.createLinearGradient(0, 0, 0, 256); gr.addColorStop(0, 'rgba(255,240,180,1)'); gr.addColorStop(0.3, 'rgba(255,150,40,.9)'); gr.addColorStop(0.75, 'rgba(220,40,10,.5)'); gr.addColorStop(1, 'rgba(120,10,0,0)'); g.fillStyle = gr; g.fillRect(0, 0, 32, 256); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; })();
  const ribbons = [];

  const loader = new GLTFLoader();
  const bin = Uint8Array.from(atob(glbBase64), c => c.charCodeAt(0)).buffer;
  loader.parse(bin, '', gltf => {
    model = gltf.scene;
    model.traverse(o => {
      if (!o.isMesh) return;
      const m = new THREE.MeshStandardMaterial({ color: 0xff9a30, roughness: 0.35, metalness: 0.35, emissive: 0xff4a00, emissiveIntensity: 1.0, vertexColors: false });
      m.onBeforeCompile = sh => {
        sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nvarying vec3 vLoc;').replace('#include <begin_vertex>', '#include <begin_vertex>\nvLoc = position;').replace('#include <project_vertex>', '#include <project_vertex>\nvLoc = transformed;');
        sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nvarying vec3 vLoc;').replace('#include <emissivemap_fragment>', `#include <emissivemap_fragment>
          float kk = clamp(abs(vLoc.x) / 42.0 + max(-vLoc.z, 0.0) / 80.0, 0.0, 1.0);
          vec3 grad = mix(vec3(1.0, 0.5, 0.1), vec3(1.0, 0.18, 0.0), smoothstep(0.1, 0.5, kk)); grad = mix(grad, vec3(0.75, 0.05, 0.0), smoothstep(0.6, 1.0, kk));
          diffuseColor.rgb = mix(vec3(1.0, 0.45, 0.08), vec3(0.55, 0.04, 0.0), kk);
          totalEmissiveRadiance = grad * (0.42 + 0.35 * kk);`);
      };
      o.material = m; o.castShadow = false;
    });
    const S = 0.036; model.scale.setScalar(S);
    root.add(model);
    mixer = new THREE.AnimationMixer(model);
    const act = mixer.clipAction(gltf.animations[0]); act.timeScale = 0.75; act.play();
    for (let i = 0; i < 3; i++) {
      const g = new THREE.PlaneGeometry(0.17 - i * 0.015, 2.4 + i * 0.25, 1, 8);
      const r = new THREE.Mesh(g, new THREE.MeshBasicMaterial({ map: ribTex, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide }));
      r.userData = { base: g.attributes.position.array.slice(), i, keep: true }; ribbons.push(r); root.add(r);
    }
    out.ready = true;
  }, e => console.warn('fenix', e));

  const tmp = new THREE.Vector3(), fwd = new THREE.Vector3(), up = new THREE.Vector3(0, 1, 0), right = new THREE.Vector3();
  out.update = (dt, now) => {
    if (!out.ready) return;
    mixer.update(dt);
    u = (u + dt * 3.0 / LEN) % 1;
    const p = curve.getPointAt(u), p2 = curve.getPointAt((u + 0.004) % 1), p3 = curve.getPointAt((u + 0.012) % 1);
    root.position.copy(p);
    fwd.subVectors(p2, p).normalize();
    const turn = new THREE.Vector3().subVectors(p3, p2).normalize().cross(fwd).y;
    roll += (THREE.MathUtils.clamp(turn * 18, -0.8, 0.8) - roll) * Math.min(1, dt * 2.5);
    root.lookAt(tmp.copy(p).add(fwd));
    root.rotateZ(-roll);
    root.position.y += Math.sin(now * 2.2) * 0.08;
    // pontos de emissão (frame local: frente = +Z)
    const L = (x, y, z, v) => v.set(x, y, z).applyMatrix4(root.matrixWorld);
    root.updateMatrixWorld();
    const flap = Math.sin(now * 2.6);
    L(-1.33, flap * 0.5, -0.43, wingL); L(1.33, flap * 0.5, -0.43, wingR); L(0, 0.04, -2.1, tail); L(0, 0.15, 0.9, beak);
    for (let k = 0; k < 1; k++) {
      [wingL, wingR].forEach(w => emit(w, new THREE.Vector3((Math.random() - .5) * .4, Math.random() * .5, (Math.random() - .5) * .4), 0.6 + Math.random() * 0.5, 0.18 + Math.random() * 0.2));
      emit(tail, new THREE.Vector3((Math.random() - .5) * .5, Math.random() * .3, (Math.random() - .5) * .5), 0.9 + Math.random() * 0.6, 0.28 + Math.random() * 0.25);
    }
    // sopro de fogo
    nextBreath -= dt;
    if (nextBreath <= 0 && breath <= 0) { breath = 1.8; nextBreath = 9 + Math.random() * 7; out.onBreath && out.onBreath(); }
    if (breath > 0) {
      breath -= dt;
      for (let k = 0; k < 10; k++) {
        const dir = fwd.clone().add(new THREE.Vector3((Math.random() - .5) * .28, (Math.random() - .5) * .22 - 0.12, (Math.random() - .5) * .28)).normalize();
        emit(beak, dir.multiplyScalar(5 + Math.random() * 4), 0.45 + Math.random() * 0.4, 0.35 + Math.random() * 0.45);
      }
      breathLight.position.copy(beak).addScaledVector(fwd, 1.5); breathLight.intensity = 40 * Math.min(1, breath);
    } else breathLight.intensity *= 0.85;
    light.intensity = 16 + Math.sin(now * 17) * 3 + Math.sin(now * 7.3) * 2;
    // fitas da cauda ondulando
    ribbons.forEach(r => {
      const a = r.geometry.attributes.position.array, b = r.userData.base, i = r.userData.i;
      for (let v = 0; v < a.length; v += 3) { const y = b[v + 1]; const t = (y + 1.3) / 2.6; a[v] = b[v] + Math.sin(now * 5 + t * 6 + i) * 0.12 * (1 - t); a[v + 2] = b[v + 2] + Math.cos(now * 4 + t * 5 + i * 2) * 0.1 * (1 - t); }
      r.geometry.attributes.position.needsUpdate = true;
      r.position.set((i - 1) * 0.09, 0.04, -2.3 - i * 0.11); r.rotation.set(Math.PI / 2 + 0.15 + Math.sin(now * 3 + i) * 0.08, 0, (i - 2) * 0.12);
    });
    // atualiza partículas
    for (let i = 0; i < N; i++) {
      if (age[i] >= 1) continue;
      age[i] += dt / life[i];
      vel[i * 3] *= 0.97; vel[i * 3 + 1] = vel[i * 3 + 1] * 0.97 + dt * 1.2; vel[i * 3 + 2] *= 0.97;
      pos[i * 3] += vel[i * 3] * dt; pos[i * 3 + 1] += vel[i * 3 + 1] * dt; pos[i * 3 + 2] += vel[i * 3 + 2] * dt;
      if (age[i] >= 1) pos[i * 3 + 1] = -999;
    }
    pg.attributes.position.needsUpdate = true; pg.attributes.aAge.needsUpdate = true; pg.attributes.aSize.needsUpdate = true;
  };
  out.focusPos = () => root.position;
  return out;
}
