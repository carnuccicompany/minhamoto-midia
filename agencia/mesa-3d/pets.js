import * as THREE from 'three';
import { phys, mat, mesh, sph, cyl, angLerp, smooth, clamp, lerp, blob } from './util.js';
import { TOP_Y } from './env.js';

// Panda-vermelho "Carnucci": mora em cima da mesa dos diretores; desce de vez em quando e volta
export function buildRedPanda(scene) {
  const furBump = (() => { const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('2d'); g.fillStyle = '#808080'; g.fillRect(0, 0, 256, 256);
    for (let i = 0; i < 7000; i++) { const x = Math.random() * 256, y = Math.random() * 256, l = 3 + Math.random() * 7; g.strokeStyle = `rgba(${Math.random() < .5 ? '255,255,255' : '0,0,0'},${0.15 + Math.random() * 0.25})`; g.lineWidth = 1; g.beginPath(); g.moveTo(x, y); g.lineTo(x + (Math.random() - .5) * 2, y + l); g.stroke(); }
    const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(3, 3); return t; })();
  const FC = new Map();
  const fur = (c) => { if (FC.has(c)) return FC.get(c); const col = new THREE.Color(c); const m = new THREE.MeshPhysicalMaterial({ color: col, roughness: 0.9, sheen: 1, sheenRoughness: 0.55, sheenColor: col.clone().lerp(new THREE.Color(0xffffff), 0.35), bumpMap: furBump, bumpScale: 1.2 }); FC.set(c, m); return m; };
  const rust = fur(0xb4441a), rustD = fur(0x8a2e10), dark = fur(0x24140d, 0.4), white = fur(0xf4eee4, 0.6), black = phys(0x080606, { roughness: 0.2, clearcoat: 1 });
  const root = new THREE.Group(); scene.add(root); blob(root, 0, 0, 0.35, 0.5);
  const body = new THREE.Group(); body.position.y = 0.27; root.add(body);
  const torso = mesh(new THREE.CapsuleGeometry(0.13, 0.3, 8, 18), rust, body, [0, 0, 0], [Math.PI / 2, 0, 0]); torso.scale.set(1, 1, 0.95);
  mesh(new THREE.CapsuleGeometry(0.1, 0.24, 6, 14), dark, body, [0, -0.055, 0.0], [Math.PI / 2, 0, 0]).scale.set(0.95, 1, 0.8); // barriga escura
  mesh(sph(0.135, 20, 14), rust, body, [0, 0.03, -0.17]).scale.set(1, 0.95, 1.05); // quadril
  // cabeça
  const head = new THREE.Group(); head.position.set(0, 0.1, 0.27); body.add(head);
  mesh(sph(0.11, 28, 20), rust, head, [0, 0, 0]).scale.set(1.12, 0.95, 0.98);
  mesh(sph(0.06, 20, 14), white, head, [0, -0.03, 0.08]).scale.set(1.05, 0.8, 1); // focinho
  mesh(new THREE.SphereGeometry(0.015, 12, 10), black, head, [0, -0.014, 0.134]).scale.set(1.3, 0.85, 0.9); // nariz
  [-1, 1].forEach(s => {
    mesh(sph(0.045, 16, 12), white, head, [s * 0.055, 0.035, 0.07]).scale.set(0.9, 0.75, 0.6); // sobrancelha branca
    mesh(sph(0.04, 14, 10), white, head, [s * 0.075, -0.03, 0.065]).scale.set(0.8, 0.9, 0.7); // bochecha
    mesh(sph(0.03, 12, 10), rustD, head, [s * 0.045, -0.005, 0.088]).scale.set(0.5, 1.2, 0.5); // "lágrima"
    mesh(new THREE.SphereGeometry(0.013, 14, 10), black, head, [s * 0.045, 0.012, 0.099]); // olho
    mesh(sph(0.004, 8, 6), phys(0xffffff, { roughness: 0.1 }), head, [s * 0.04, 0.018, 0.112], null, false); // brilho
    const ear = new THREE.Group(); ear.position.set(s * 0.075, 0.085, -0.01); ear.rotation.set(-0.2, 0, s * -0.35); head.add(ear);
    mesh(new THREE.SphereGeometry(0.042, 16, 12), white, ear, [0, 0.03, 0]).scale.set(1, 1.1, 0.42);
    mesh(new THREE.SphereGeometry(0.03, 14, 10), rustD, ear, [0, 0.026, 0.008]).scale.set(1, 1, 0.3);
  });
  // patas
  const legs = [];
  [[-0.08, 0.17], [0.08, 0.17], [-0.085, -0.17], [0.085, -0.17]].forEach(([x, z], i) => {
    const hip = new THREE.Group(); hip.position.set(x, -0.04, z); body.add(hip);
    mesh(new THREE.SphereGeometry(0.075, 16, 12), i < 2 ? rust : rust, hip, [0, 0.0, 0]).scale.set(0.85, 1.1, 1);
    const lg = mesh(new THREE.CylinderGeometry(0.05, 0.04, 0.17, 14), dark, hip, [0, -0.1, 0]);
    mesh(new THREE.SphereGeometry(0.05, 14, 10), dark, hip, [0, -0.19, 0.02]).scale.set(1, 0.62, 1.35);
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

  // passeio: a casa dele é a MESA. Anda por cima, senta perto dos diretores, ganha carinho.
  // De vez em quando desce, dá uma volta rápida e sobe de novo.
  const spots = [[6.5, 6.2], [-3.4, 6.2], [-8.2, -1.5], [4.2, -6.6], [9.4, -0.2], [-2.0, -6.9], [0.6, 6.4], [-8.6, -5.8]];
  const RING = 5.85, TR = 1.75;              // anel do chão (fora do tapete da pantera) e anel de cima da mesa
  let seatsA = [0, Math.PI / 2, Math.PI, Math.PI * 1.5], gapsA = [Math.PI / 4];
  const at = (a, r, y = 0) => new THREE.Vector3(Math.cos(a) * r, y, Math.sin(a) * r);
  const st = { pos: at(0.4, TR, TOP_Y), heading: 0, state: 'tIdle', t: 6, path: null, leg: 0, phase: 0, mode: 'sit', floorT: 0, nearSeat: null };
  root.position.copy(st.pos);
  function route(dest) {
    const a0 = Math.atan2(st.pos.z, st.pos.x), a1 = Math.atan2(dest.z, dest.x);
    const pts = [at(a0, RING)];
    const da = Math.atan2(Math.sin(a1 - a0), Math.cos(a1 - a0)); const n = Math.max(1, Math.ceil(Math.abs(da) / 0.25));
    for (let k = 1; k <= n; k++) pts.push(at(a0 + da * k / n, RING));
    pts.push(dest); return pts;
  }
  function tableRoute(a1, r1) {
    const a0 = Math.atan2(st.pos.z, st.pos.x);
    const pts = [at(a0, TR, TOP_Y)];
    const da = Math.atan2(Math.sin(a1 - a0), Math.cos(a1 - a0)); const n = Math.max(1, Math.ceil(Math.abs(da) / 0.3));
    for (let k = 1; k <= n; k++) pts.push(at(a0 + da * k / n, TR, TOP_Y));
    pts.push(at(a1, r1, TOP_Y)); return pts;
  }
  const nearest = (list, a) => list.reduce((b, x) => Math.abs(Math.atan2(Math.sin(x - a), Math.cos(x - a))) < Math.abs(Math.atan2(Math.sin(b - a), Math.cos(b - a))) ? x : b, list[0]);
  const out = { root, head, st };
  out.setSeats = (seats, gaps) => { seatsA = seats; gapsA = gaps; };
  out.onTable = () => st.pos.y > 0.3;
  // coraçõezinhos quando ganha carinho
  const heartTex = (() => { const c = document.createElement('canvas'); c.width = c.height = 64; const g = c.getContext('2d'); g.fillStyle = '#ff4d6d'; g.beginPath(); g.moveTo(32, 54); g.bezierCurveTo(4, 36, 6, 12, 22, 12); g.bezierCurveTo(28, 12, 32, 17, 32, 22); g.bezierCurveTo(32, 17, 36, 12, 42, 12); g.bezierCurveTo(58, 12, 60, 36, 32, 54); g.fill(); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; })();
  const hearts = Array.from({ length: 8 }, () => { const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: heartTex, transparent: true, depthWrite: false })); sp.scale.setScalar(0.12); sp.visible = false; sp.userData = { age: 1, keep: true }; scene.add(sp); return sp; });
  let hk = 0, hT = 0;
  const hp = new THREE.Vector3();
  function heart() { const sp = hearts[hk++ % hearts.length]; head.getWorldPosition(hp); sp.position.copy(hp).add(new THREE.Vector3((Math.random() - .5) * .2, 0.15, (Math.random() - .5) * .2)); sp.userData.age = 0; sp.visible = true; }
  // visita: vai (por cima da mesa) até a frente de um diretor e ganha carinho
  let visit = null;
  out.onPetIdle = null; // main: carinho espontâneo de quem está do lado
  function goTableVisit() { st.path = tableRoute(visit.a + 0.1, 2.1); st.leg = 0; st.state = 'tWalk'; }
  function jump(to, next) { st.state = next; st.jt = 0; st.from = st.pos.clone(); st.to = to; }
  out.visit = (seatPos, onPet) => {
    if (visit || st.state === 'climb' || st.state === 'down' || st.state === 'table') return false;
    const a = Math.atan2(seatPos.z, seatPos.x);
    visit = { a, seat: seatPos.clone(), onPet };
    if (out.onTable()) goTableVisit();
    else { const g = nearest(gapsA, a); visit.climbA = g; st.path = route(at(g, 3.95)); st.leg = 0; st.state = 'walk'; }
    return true;
  };
  out.busy = () => !!visit;
  const tmp = new THREE.Vector3();
  function pose(dt, mode) {
    const sitK = mode === 'sit' ? 1 : 0, lieK = mode === 'lie' ? 1 : 0, petK = mode === 'pet' ? 1 : 0;
    body.rotation.x = lerp(body.rotation.x, -0.55 * (sitK || petK), Math.min(1, dt * 3));
    body.position.y = lerp(body.position.y, 0.27 - 0.12 * lieK + 0.06 * (sitK || petK), Math.min(1, dt * 3));
    legs.forEach((l, i) => { l.rotation.x = lerp(l.rotation.x, lieK ? (i < 2 ? -1.3 : 1.3) : (sitK || petK) && i >= 2 ? -1.1 : (sitK || petK) ? 0.55 : 0, Math.min(1, dt * 3)); });
  }
  function walkStep(dt, spd) {
    const target = st.path[st.leg]; tmp.subVectors(target, st.pos); tmp.y = 0;
    const d = tmp.length(), step = spd * dt;
    let arrived = false;
    if (d < step) { st.pos.x = target.x; st.pos.z = target.z; if (st.leg >= st.path.length - 1) arrived = true; else st.leg++; }
    else { st.pos.addScaledVector(tmp.normalize(), step); st.heading = angLerp(st.heading, Math.atan2(tmp.x, tmp.z), Math.min(1, dt * 6)); }
    st.phase += dt * 9;
    legs.forEach((l, i) => { l.rotation.x = Math.sin(st.phase + (i === 0 || i === 3 ? 0 : Math.PI)) * 0.5; });
    body.position.y = 0.27 + Math.abs(Math.sin(st.phase)) * 0.015; body.rotation.x = 0;
    return arrived;
  }
  function faceSeat(a) { tmp.copy(at(a, 3.3)).sub(st.pos); st.heading = Math.atan2(tmp.x, tmp.z); }
  function nextOnTable() {
    // 1 em cada 7 vezes desce pra dar uma volta; no resto fica na mesa, perto de alguém
    if (Math.random() < 0.14) { const g = gapsA[Math.floor(Math.random() * gapsA.length)]; st.goDown = g; st.path = tableRoute(g, 2.35); st.leg = 0; st.state = 'tWalk'; return; }
    const sa = seatsA[Math.floor(Math.random() * seatsA.length)];
    st.path = tableRoute(sa + (Math.random() - 0.5) * 0.2, Math.random() < 0.65 ? 2.08 : TR); st.leg = 0; st.state = 'tWalk';
  }
  out.update = (dt, now) => {
    segs.forEach((g, i) => { g.rotation.y = Math.sin(now * 2.2 - i * 0.5) * 0.12; });
    head.rotation.y = lerp(head.rotation.y, st.state === 'walk' || st.state === 'tWalk' ? 0 : Math.sin(now * 0.7) * 0.6, Math.min(1, dt * 3));
    switch (st.state) {
      case 'tWalk':
        if (walkStep(dt, 0.45)) {
          if (visit) { st.state = 'table'; st.t = 6.5; faceSeat(visit.a); visit.onPet && visit.onPet(); }
          else if (st.goDown != null) { const g = st.goDown; st.goDown = null; jump(at(g, 3.95), 'down'); }
          else { st.state = 'tIdle'; st.t = 8 + Math.random() * 14; const r = Math.hypot(st.pos.x, st.pos.z);
            st.nearSeat = r > 2.0 ? nearest(seatsA, Math.atan2(st.pos.z, st.pos.x)) : null;
            st.mode = st.nearSeat != null ? 'sit' : Math.random() < 0.5 ? 'lie' : 'sit'; if (st.nearSeat != null) faceSeat(st.nearSeat); }
        }
        break;
      case 'tIdle':
        st.t -= dt; pose(dt, st.mode);
        if (st.nearSeat != null) { hT -= dt; if (hT <= 0) { heart(); hT = 1.1 + Math.random() * 0.8; head.rotation.z = 0.12; if (Math.random() < 0.04 && out.onPetIdle) out.onPetIdle(st.nearSeat); } else head.rotation.z = lerp(head.rotation.z, 0, dt * 3); }
        if (st.t <= 0) { head.rotation.z = 0; nextOnTable(); }
        break;
      case 'table':
        st.t -= dt; hT -= dt; if (hT <= 0) { heart(); hT = 0.45; }
        pose(dt, 'pet'); head.rotation.z = Math.sin(now * 3) * 0.12;
        if (st.t <= 0) { head.rotation.z = 0; visit = null; st.state = 'tIdle'; st.t = 6 + Math.random() * 8; st.mode = 'lie'; st.nearSeat = null; }
        break;
      case 'climb': case 'down': {
        st.jt = Math.min(1, st.jt + dt / 0.75); const k = smooth(st.jt);
        st.pos.lerpVectors(st.from, st.to, k); st.pos.y = lerp(st.from.y, st.to.y, k) + Math.sin(Math.PI * st.jt) * 0.35;
        tmp.subVectors(st.to, st.from); st.heading = angLerp(st.heading, Math.atan2(tmp.x, tmp.z), Math.min(1, dt * 8));
        legs.forEach((l, i) => { l.rotation.x = lerp(l.rotation.x, i < 2 ? -0.8 : 0.8, Math.min(1, dt * 8)); });
        if (st.jt >= 1) {
          if (st.state === 'climb') { st.pos.y = TOP_Y; if (visit) goTableVisit(); else { st.state = 'tIdle'; st.t = 4; st.mode = 'sit'; st.nearSeat = null; } }
          else { st.pos.y = 0; const sp = spots[Math.floor(Math.random() * spots.length)]; st.path = route(new THREE.Vector3(sp[0], 0, sp[1])); st.leg = 0; st.state = 'walk'; st.floorT = 1; }
        }
        break;
      }
      case 'walk':
        if (walkStep(dt, 0.75)) {
          if (visit && visit.climbA != null) { const g = visit.climbA; visit.climbA = null; jump(at(g, 2.25, TOP_Y), 'climb'); }
          else if (st.floorT > 0) { st.floorT = 0; st.state = 'idle'; st.t = 4 + Math.random() * 5; st.mode = Math.random() < 0.5 ? 'sit' : 'stand'; }
          else { jump(at(st.climbA, 2.25, TOP_Y), 'climb'); }
        }
        break;
      default: // idle no chão: logo quer voltar pra mesa
        st.t -= dt; pose(dt, st.mode);
        if (st.t <= 0) { const g = gapsA[Math.floor(Math.random() * gapsA.length)]; st.climbA = g; st.path = route(at(g, 3.95)); st.leg = 0; st.state = 'walk'; }
    }
    root.position.copy(st.pos); root.rotation.y = st.heading;
    hearts.forEach(sp => { if (sp.userData.age >= 1) return; sp.userData.age += dt / 1.4; sp.position.y += dt * 0.35; sp.material.opacity = 1 - sp.userData.age; if (sp.userData.age >= 1) sp.visible = false; });
  };
  return out;
}
