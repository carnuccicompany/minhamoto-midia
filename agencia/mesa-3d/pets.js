import * as THREE from 'three';
import { phys, mat, mesh, sph, cyl, angLerp, smooth, clamp, lerp, blob } from './util.js';

// Panda-vermelho "Carnucci": anda pelo escritório, para, senta, olha em volta, deita no tapete do lounge
export function buildRedPanda(scene) {
  const fur = (c) => mat(c, { roughness: 0.85 });
  const rust = fur(0xb4441a), rustD = fur(0x8a2e10), dark = fur(0x24140d, 0.4), white = fur(0xf4eee4, 0.6), black = phys(0x080606, { roughness: 0.2, clearcoat: 1 });
  const root = new THREE.Group(); scene.add(root); blob(root, 0, 0, 0.35, 0.5);
  const body = new THREE.Group(); body.position.y = 0.3; root.add(body);
  const torso = mesh(new THREE.CapsuleGeometry(0.13, 0.3, 8, 18), rust, body, [0, 0, 0], [Math.PI / 2, 0, 0]); torso.scale.set(1, 1, 0.95);
  mesh(new THREE.CapsuleGeometry(0.1, 0.24, 6, 14), dark, body, [0, -0.055, 0.0], [Math.PI / 2, 0, 0]).scale.set(0.95, 1, 0.8); // barriga escura
  mesh(sph(0.135, 20, 14), rust, body, [0, 0.03, -0.17]).scale.set(1, 0.95, 1.05); // quadril
  // cabeça
  const head = new THREE.Group(); head.position.set(0, 0.1, 0.27); body.add(head);
  mesh(sph(0.11, 28, 20), rust, head, [0, 0, 0]).scale.set(1.12, 0.95, 0.98);
  mesh(sph(0.06, 20, 14), white, head, [0, -0.03, 0.08]).scale.set(1.05, 0.8, 1); // focinho
  mesh(sph(0.02, 12, 10), black, head, [0, -0.012, 0.135]).scale.set(1.3, 0.85, 0.9); // nariz
  [-1, 1].forEach(s => {
    mesh(sph(0.045, 16, 12), white, head, [s * 0.055, 0.035, 0.07]).scale.set(0.9, 0.75, 0.6); // sobrancelha branca
    mesh(sph(0.04, 14, 10), white, head, [s * 0.075, -0.03, 0.065]).scale.set(0.8, 0.9, 0.7); // bochecha
    mesh(sph(0.03, 12, 10), rustD, head, [s * 0.045, -0.005, 0.088]).scale.set(0.5, 1.2, 0.5); // "lágrima"
    mesh(sph(0.016, 14, 10), black, head, [s * 0.045, 0.012, 0.098]); // olho
    mesh(sph(0.004, 8, 6), phys(0xffffff, { roughness: 0.1 }), head, [s * 0.04, 0.018, 0.112], null, false); // brilho
    const ear = new THREE.Group(); ear.position.set(s * 0.075, 0.085, -0.01); ear.rotation.set(-0.2, 0, s * -0.35); head.add(ear);
    mesh(new THREE.ConeGeometry(0.042, 0.075, 14), white, ear, [0, 0.03, 0]).scale.set(1, 1, 0.45);
    mesh(new THREE.ConeGeometry(0.03, 0.06, 14), rustD, ear, [0, 0.026, 0.006]).scale.set(1, 1, 0.35);
  });
  // patas
  const legs = [];
  [[-0.08, 0.17], [0.08, 0.17], [-0.085, -0.17], [0.085, -0.17]].forEach(([x, z], i) => {
    const hip = new THREE.Group(); hip.position.set(x, -0.04, z); body.add(hip);
    mesh(new THREE.CapsuleGeometry(0.042, 0.17, 6, 12), dark, hip, [0, -0.12, 0]);
    mesh(sph(0.045, 12, 10), dark, hip, [0, -0.225, 0.02]).scale.set(1, 0.6, 1.3);
    legs.push(hip);
  });
  // cauda listrada e fofa
  const tail = new THREE.Group(); tail.position.set(0, 0.02, -0.3); body.add(tail);
  const segs = []; let parent = tail;
  for (let i = 0; i < 9; i++) {
    const g = new THREE.Group(); g.position.set(0, 0, i ? -0.06 : 0); g.rotation.x = 0.18; parent.add(g);
    const r = 0.07 - i * 0.003;
    mesh(sph(r, 16, 12), i % 2 ? rustD : fur(0xd1915a), g, [0, 0, -0.03]).scale.set(1, 1, 1.15);
    segs.push(g); parent = g;
  }
  root.traverse(o => { if (o.isMesh) o.userData.pet = 'panda'; });

  // passeio
  const spots = [[6.5, 6.2], [-3.4, 6.2], [-8.2, -1.5], [4.2, -6.6], [9.4, -0.2], [-2.0, -6.9], [0.6, 6.4], [-8.6, -5.8]];
  const RING = 5.35;
  const st = { pos: new THREE.Vector3(6.5, 0, 6.5), heading: 0, state: 'idle', t: 3, path: null, leg: 0, phase: 0, mode: 'stand' };
  root.position.copy(st.pos);
  function route(dest) {
    const a0 = Math.atan2(st.pos.z, st.pos.x), a1 = Math.atan2(dest.z, dest.x);
    const pts = [];
    const r0 = Math.hypot(st.pos.x, st.pos.z);
    if (r0 < RING + 0.5 || Math.hypot(dest.x, dest.z) < RING + 0.5 || true) {
      pts.push(new THREE.Vector3(Math.cos(a0) * RING, 0, Math.sin(a0) * RING));
      const da = Math.atan2(Math.sin(a1 - a0), Math.cos(a1 - a0)); const n = Math.max(1, Math.ceil(Math.abs(da) / 0.25));
      for (let k = 1; k <= n; k++) { const aa = a0 + da * k / n; pts.push(new THREE.Vector3(Math.cos(aa) * RING, 0, Math.sin(aa) * RING)); }
    }
    pts.push(dest); return pts;
  }
  const out = { root, head, st };
  const tmp = new THREE.Vector3();
  out.update = (dt, now, log) => {
    // cauda balançando sempre
    segs.forEach((g, i) => { g.rotation.y = Math.sin(now * 2.2 - i * 0.5) * 0.12; });
    head.rotation.y = lerp(head.rotation.y, st.state === 'walk' ? 0 : Math.sin(now * 0.7) * 0.6, Math.min(1, dt * 3));
    if (st.state === 'walk') {
      const target = st.path[st.leg]; tmp.subVectors(target, st.pos); tmp.y = 0;
      const d = tmp.length(), spd = 0.75 * dt;
      if (d < spd) { st.pos.copy(target); if (st.leg >= st.path.length - 1) { st.state = 'idle'; st.t = 5 + Math.random() * 10; st.mode = Math.random() < 0.45 ? 'sit' : Math.random() < 0.5 ? 'lie' : 'stand'; } else st.leg++; }
      else { st.pos.addScaledVector(tmp.normalize(), spd); st.heading = angLerp(st.heading, Math.atan2(tmp.x, tmp.z), Math.min(1, dt * 6)); }
      st.phase += dt * 9;
      legs.forEach((l, i) => { l.rotation.x = Math.sin(st.phase + (i === 0 || i === 3 ? 0 : Math.PI)) * 0.5; });
      body.position.y = 0.3 + Math.abs(Math.sin(st.phase)) * 0.015; body.rotation.x = 0;
    } else {
      st.t -= dt;
      const sitK = st.mode === 'sit' ? 1 : 0, lieK = st.mode === 'lie' ? 1 : 0;
      body.rotation.x = lerp(body.rotation.x, -0.55 * sitK, Math.min(1, dt * 3));
      body.position.y = lerp(body.position.y, 0.3 - 0.12 * lieK + 0.06 * sitK, Math.min(1, dt * 3));
      legs.forEach((l, i) => { l.rotation.x = lerp(l.rotation.x, lieK ? (i < 2 ? -1.3 : 1.3) : sitK && i >= 2 ? -1.1 : sitK ? 0.55 : 0, Math.min(1, dt * 3)); });
      if (st.t <= 0) { const sp = spots[Math.floor(Math.random() * spots.length)]; st.path = route(new THREE.Vector3(sp[0], 0, sp[1])); st.leg = 0; st.state = 'walk'; }
    }
    root.position.copy(st.pos); root.rotation.y = st.heading;
  };
  return out;
}
