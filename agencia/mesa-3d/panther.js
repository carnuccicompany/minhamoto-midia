import * as THREE from 'three';
import { mesh, angLerp, lerp, clamp, blob, bakeSkinned } from './util.js';

// Pantera negra: ronda o tapete de veludo em círculo, devagar, sem nunca sair dele.
// De vez em quando para atrás de um diretor e encara. Ninguém relaxa com ela olhando.
export function buildPanther(scene, R = 5.0) {
  // tudo vira UMA malha com esqueleto (1 draw call); pelo com brilho de borda aveludado
  const fur = new THREE.MeshStandardMaterial({ color: 0x0d0d10, roughness: 0.42 }); fur.userData.k = 2;
  const furD = new THREE.MeshStandardMaterial({ color: 0x08080a, roughness: 0.55 }); furD.userData.k = 2;
  const noseM = new THREE.MeshStandardMaterial({ color: 0x050505, roughness: 0.18 });
  const eyeM = new THREE.MeshStandardMaterial({ color: 0xd9c84a, emissive: 0xc9b23a, emissiveIntensity: 1.6, roughness: 0.15, transparent: true });
  const pupilM = new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true });
  const S = (r, a = 16, b = 12) => new THREE.SphereGeometry(r, a, b);
  const C = (r, l, a = 5, b = 12) => new THREE.CapsuleGeometry(r, l, a, b);

  const root = new THREE.Group(); scene.add(root);
  const shadow = blob(root, 0, 0, 0.45, 0.95, 0.5);
  const body = new THREE.Bone(); body.position.y = 0.6; root.add(body);
  const lathe = (pts, m, parent, pos, segs = 28) => mesh(new THREE.LatheGeometry(pts.map(([r, y]) => new THREE.Vector2(r, y)), Math.min(segs, 20)), m, parent, pos);
  // tronco num perfil só (peito fundo, cintura fina, quadril forte) — silhueta contínua, nada de bolinhas
  const torso = lathe([[0, -0.66], [0.1, -0.63], [0.16, -0.55], [0.185, -0.42], [0.18, -0.28], [0.15, -0.12], [0.148, 0.0], [0.17, 0.16], [0.2, 0.3], [0.19, 0.42], [0.14, 0.52], [0.06, 0.58], [0, 0.6]], fur, body, [0, 0, 0], 32);
  torso.rotation.x = Math.PI / 2; torso.scale.set(0.82, 1, 1.12);
  const belly = lathe([[0, -0.4], [0.1, -0.32], [0.11, -0.05], [0.12, 0.2], [0.08, 0.36], [0, 0.4]], furD, body, [0, -0.07, 0], 20);
  belly.rotation.x = Math.PI / 2; belly.scale.set(0.9, 1, 0.8);
  const blades = [-1, 1].map(s => { const m = mesh(S(0.075, 16, 12), fur, body, [s * 0.1, 0.12, 0.3]); m.scale.set(0.75, 0.55, 1.2); return m; });
  [-1, 1].forEach(s => { const th = mesh(S(0.13, 20, 16), fur, body, [s * 0.1, -0.02, -0.4]); th.scale.set(0.62, 1.15, 1.05); }); // coxas traseiras
  // pescoço e cabeça
  const neck = new THREE.Bone(); neck.position.set(0, 0.04, 0.46); body.add(neck);
  const nk = lathe([[0.15, 0], [0.13, 0.1], [0.115, 0.2], [0.1, 0.27]], fur, neck, [0, 0, 0], 24); nk.rotation.x = 1.0;
  const head = new THREE.Bone(); head.position.set(0, 0.16, 0.2); head.scale.setScalar(1.18); neck.add(head);
  const skull = lathe([[0, -0.13], [0.07, -0.12], [0.12, -0.07], [0.135, 0.0], [0.12, 0.06], [0.09, 0.1], [0.07, 0.14], [0.05, 0.18], [0, 0.195]], fur, head, [0, 0, 0], 30);
  skull.rotation.x = Math.PI / 2; skull.scale.set(1.0, 1, 0.82);
  mesh(S(0.06, 16, 12), fur, head, [0, -0.045, 0.12]).scale.set(1.1, 0.72, 1.0);     // focinho
  [-1, 1].forEach(s => mesh(S(0.04, 16, 12), fur, head, [s * 0.036, -0.055, 0.155]).scale.set(1, 0.7, 0.75));
  mesh(S(0.024, 16, 12), noseM, head, [0, -0.025, 0.188]).scale.set(1.3, 0.72, 0.75);
  mesh(S(0.05, 18, 12), furD, head, [0, -0.095, 0.08]).scale.set(1.05, 0.48, 1.0);    // mandíbula
  mesh(S(0.055, 18, 12), fur, head, [0, 0.055, 0.05]).scale.set(1.55, 0.5, 1.25);     // testa pesada
  [-1, 1].forEach(s => mesh(S(0.05, 16, 12), fur, head, [s * 0.075, -0.02, 0.03]).scale.set(0.7, 0.9, 1.0)); // bochechas
  const eyes = [];
  [-1, 1].forEach(s => {
    const e = mesh(S(0.02, 18, 14), eyeM, head, [s * 0.052, 0.022, 0.118]); e.scale.set(1.3, 0.62, 0.55); e.rotation.z = s * 0.28;
    const p = mesh(new THREE.CircleGeometry(0.0062, 14), pupilM, head, [s * 0.052, 0.022, 0.1295]); p.scale.set(0.42, 1.45, 1); p.rotation.y = s * 0.3;
    eyes.push(e);
    mesh(S(0.03, 14, 10), fur, head, [s * 0.056, 0.046, 0.108]).scale.set(1.25, 0.32, 0.7); // pálpebra pesada: olhar de caça
    const ear = new THREE.Bone(); ear.position.set(s * 0.078, 0.098, -0.03); ear.rotation.set(-0.35, 0, s * -0.45); head.add(ear);
    mesh(S(0.034, 14, 10), fur, ear, [0, 0.02, 0]).scale.set(1, 1.1, 0.42);
    mesh(S(0.022, 12, 8), furD, ear, [0, 0.02, 0.008]).scale.set(1, 1, 0.3);
  });
  // patas afiladas (perfil de torno), com cotovelo e pata larga
  const legs = [];
  [[-0.105, 0.33, 1], [0.105, 0.33, 1], [-0.105, -0.42, 0], [0.105, -0.42, 0]].forEach(([x, z, front], i) => {
    const hip = new THREE.Bone(); hip.position.set(x, front ? -0.05 : -0.08, z); body.add(hip);
    lathe(front ? [[0.0, 0.06], [0.1, 0.04], [0.112, -0.04], [0.095, -0.14], [0.072, -0.24], [0.064, -0.29]] : [[0.0, 0.05], [0.1, 0.02], [0.098, -0.08], [0.075, -0.18], [0.06, -0.26]], fur, hip, [0, 0, 0], 20);
    const knee = new THREE.Bone(); knee.position.set(0, front ? -0.27 : -0.24, 0); hip.add(knee);
    mesh(S(front ? 0.064 : 0.06, 16, 12), fur, knee, [0, 0, 0]);
    lathe([[0.064, 0], [0.058, -0.07], [0.048, -0.16], [0.052, -0.2]], fur, knee, [0, 0, 0], 18);
    const paw = mesh(S(0.068, 18, 12), furD, knee, [0, -0.225, 0.03]); paw.scale.set(1, 0.5, 1.3);
    [-1, 0, 1].forEach(t => mesh(S(0.022, 10, 8), furD, knee, [t * 0.032, -0.235, 0.09]).scale.set(1, 0.7, 1)); // dedos
    legs.push({ hip, knee, front, ph: [0, Math.PI, Math.PI * 0.5, Math.PI * 1.5][i] });
  });
  // cauda longa em J
  const tail = new THREE.Bone(); tail.position.set(0, 0.08, -0.6); body.add(tail);
  const segs = []; let par = tail;
  for (let i = 0; i < 14; i++) {
    const g = new THREE.Bone(); g.position.z = i ? -0.075 : 0; g.rotation.x = i < 6 ? 0.16 : -0.1; par.add(g);
    mesh(C(0.04 - i * 0.0013, 0.06, 4, 10), fur, g, [0, 0, -0.035], [Math.PI / 2, 0, 0]);
    segs.push(g); par = g;
  }
  root.traverse(o => { if (o.isMesh) { o.userData.pet = 'pantera'; o.userData.dyn = true; } });
  const sk = bakeSkinned(root); sk.userData.pet = 'pantera';
  root.userData.dyn = true;

  const st = { a: Math.PI * 0.25, speed: 0.38, phase: 0, stop: 0, stopT: 14, stareAt: null, headY: 0, headX: 0 };
  const out = { root, head, st, R };
  // quem está perto da pantera agora (main usa pra decidir quem ela encara)
  out.angle = () => st.a;
  out.stare = (worldPos, secs, onStart) => { if (st.stop > 0) return false; st.stop = secs; st.stareAt = worldPos.clone(); onStart && onStart(); return true; };
  out.busy = () => st.stop > 0;
  const tmp = new THREE.Vector3();
  out.update = (dt, now) => {
    const moving = st.stop <= 0;
    if (moving) {
      st.a += (st.speed / R) * dt;               // anti-horário, sempre no círculo
      st.phase += dt * 4.2;
    } else st.stop -= dt;
    const x = Math.cos(st.a) * R, z = Math.sin(st.a) * R;
    root.position.set(x, 0, z);
    root.rotation.y = Math.atan2(-Math.sin(st.a), Math.cos(st.a)); // tangente do círculo
    // passada de felino: lenta, ombro rolando, cabeça baixa
    legs.forEach(l => {
      const p = st.phase + l.ph, sw = moving ? Math.sin(p) : 0;
      l.hip.rotation.x = lerp(l.hip.rotation.x, sw * (l.front ? 0.42 : 0.38), Math.min(1, dt * 10));
      const lift = moving ? Math.max(0, Math.cos(p)) : 0;
      l.knee.rotation.x = lerp(l.knee.rotation.x, (l.front ? -lift * 0.7 : lift * 0.8) + (l.front ? 0 : -0.25), Math.min(1, dt * 10)); if (!l.front) l.hip.rotation.x += 0.22;
    });
    blades.forEach((b, i) => { b.position.y = 0.13 + (moving ? Math.max(0, Math.sin(st.phase + (i ? Math.PI : 0))) * 0.035 : 0.01); });
    body.position.y = 0.6 + (moving ? Math.sin(st.phase * 2) * 0.008 : 0) - (moving ? 0.02 : 0.04);
    body.rotation.z = moving ? Math.sin(st.phase) * 0.025 : 0;
    // cabeça: baixa e varrendo enquanto anda; trava no alvo quando encara
    let ty = Math.sin(now * 0.35) * 0.25, tx = 0.12;
    if (!moving && st.stareAt) {
      head.getWorldPosition(tmp); const dx = st.stareAt.x - tmp.x, dz = st.stareAt.z - tmp.z;
      ty = clamp(angLerp(0, Math.atan2(dx, dz) - root.rotation.y, 1), -1.3, 1.3); tx = -0.05;
    }
    st.headY = lerp(st.headY, ty, Math.min(1, dt * 2.5)); st.headX = lerp(st.headX, tx, Math.min(1, dt * 2.5));
    neck.rotation.y = st.headY * 0.6; head.rotation.y = st.headY * 0.4; neck.rotation.x = st.headX;
    eyeM.emissiveIntensity = !moving ? 2.4 : 1.5;
    // cauda: balanço lento, ponta chicoteando quando parada
    segs.forEach((g, i) => { g.rotation.y = Math.sin(now * (moving ? 1.1 : 2.4) - i * 0.35) * (moving ? 0.07 : 0.12) * (i > 8 ? 1.6 : 1); });
  };
  return out;
}
