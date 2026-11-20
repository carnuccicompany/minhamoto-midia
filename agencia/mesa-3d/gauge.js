import * as THREE from 'three';
import { M, mat, mesh, cyl } from './util.js';

// Anel do Cadastro 100%: pedestal dourado com um mostrador redondo que carrega até 100%
export function buildGauge(scene, C, pos = [-6.9, 3.4], look = [10.5, 17]) {
  const g = new THREE.Group(); g.position.set(pos[0], 0, pos[1]); g.rotation.y = Math.atan2(look[0] - pos[0], look[1] - pos[1]) * 0.8 + Math.atan2(-pos[0], -pos[1]) * 0.2; scene.add(g);
  // pedestal
  mesh(cyl(0.36, 0.42, 0.06, 40), M.black, g, [0, 0.03, 0]);
  mesh(cyl(0.3, 0.34, 0.03, 40), M.gold, g, [0, 0.075, 0]);
  mesh(cyl(0.04, 0.055, 1.1, 18), M.gold, g, [0, 0.62, 0]);
  const Y = 1.86, R = 0.72;
  // aro e fundo
  mesh(new THREE.TorusGeometry(R + 0.03, 0.028, 16, 96), M.gold, g, [0, Y, 0]);
  mesh(new THREE.TorusGeometry(R + 0.075, 0.008, 8, 96), M.goldDim, g, [0, Y, 0]);
  mesh(new THREE.CylinderGeometry(R + 0.02, R + 0.02, 0.05, 64), M.black, g, [0, Y, -0.03], [Math.PI / 2, 0, 0]);
  const cv = document.createElement('canvas'); cv.width = cv.height = 640; const tx = new THREE.CanvasTexture(cv); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 8;
  const face = mesh(new THREE.CircleGeometry(R, 72), new THREE.MeshBasicMaterial({ map: tx, toneMapped: false }), g, [0, Y, 0.0], null, false);
  const back = face.clone(); back.rotation.y = Math.PI; back.position.z = -0.058; g.add(back);
  // brilho atrás do mostrador
  const gc = document.createElement('canvas'); gc.width = gc.height = 128; const gg = gc.getContext('2d'); const rg = gg.createRadialGradient(64, 64, 20, 64, 64, 64); rg.addColorStop(0, 'rgba(255,214,140,.55)'); rg.addColorStop(1, 'rgba(255,214,140,0)'); gg.fillStyle = rg; gg.fillRect(0, 0, 128, 128);
  const glow = mesh(new THREE.PlaneGeometry(2.5, 2.5), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(gc), transparent: true, depthWrite: false, toneMapped: false, opacity: 0.5 }), g, [0, Y, -0.07], null, false);
  const pickM = new THREE.MeshBasicMaterial({ visible: false });
  const hit = mesh(new THREE.CylinderGeometry(0.85, 0.85, 2.7, 12), pickM, g, [0, 1.35, 0], null, false); hit.userData.cadastro = true; hit.userData.keep = true;
  [face, back, glow].forEach(o => o.userData.keep = true);

  const pct = Math.max(0, Math.min(100, C.pct || 0)), N = 72;
  function draw(shown, blink) {
    const c = cv.getContext('2d'), W = 640, h = W / 2;
    c.fillStyle = '#060608'; c.fillRect(0, 0, W, W);
    const bg = c.createRadialGradient(h, h * 0.8, 10, h, h, h); bg.addColorStop(0, '#16130d'); bg.addColorStop(1, '#050506'); c.fillStyle = bg; c.beginPath(); c.arc(h, h, h, 0, 7); c.fill();
    const lit = Math.round(shown / 100 * N);
    for (let i = 0; i < N; i++) {
      const a = i / N * Math.PI * 2 - Math.PI / 2, a2 = a + Math.PI * 2 / N * 0.62;
      c.beginPath(); c.arc(h, h, 296, a, a2); c.arc(h, h, 246, a2, a, true); c.closePath();
      if (i < lit) { const gr = c.createLinearGradient(0, 0, W, W); gr.addColorStop(0, '#fff1c8'); gr.addColorStop(0.5, '#e0bb6c'); gr.addColorStop(1, '#a37b38'); c.fillStyle = gr; c.shadowColor = 'rgba(255,200,110,.9)'; c.shadowBlur = 16; }
      else if (i === lit && shown < 100) { c.fillStyle = blink ? '#8a6c30' : '#2a2418'; c.shadowBlur = 0; }
      else { c.fillStyle = '#1c1b20'; c.shadowBlur = 0; }
      c.fill();
    }
    c.shadowBlur = 0;
    for (let i = 0; i < 60; i++) { const a = i / 60 * Math.PI * 2; c.strokeStyle = i % 5 ? '#2a2a30' : '#6a5630'; c.lineWidth = i % 5 ? 2 : 4; c.beginPath(); c.moveTo(h + Math.cos(a) * 304, h + Math.sin(a) * 304); c.lineTo(h + Math.cos(a) * 316, h + Math.sin(a) * 316); c.stroke(); }
    c.textAlign = 'center';
    c.fillStyle = '#c9a75e'; c.font = '600 24px Inter, Arial'; c.fillText('C A D A S T R O', h, 200);
    const tg = c.createLinearGradient(0, 230, 0, 380); tg.addColorStop(0, '#fff4d6'); tg.addColorStop(0.7, '#d8b46a'); tg.addColorStop(1, '#9c7a3a');
    c.fillStyle = tg; c.font = '800 150px Inter, Arial'; const num = String(Math.round(shown)), nw = c.measureText(num).width;
    c.fillText(num, h - 22, 372); c.font = '800 56px Inter, Arial'; c.textAlign = 'left'; c.fillText('%', h - 22 + nw / 2 + 6, 372);
    c.textAlign = 'center'; c.fillStyle = shown >= 100 ? '#3ccf7a' : '#8f8a80'; c.font = '600 24px Inter, Arial';
    c.fillText(shown >= 100 ? 'MOTOR MONTADO' : `${C.pendentes || 0} pendências`, h, 430);
    c.fillStyle = '#5a564e'; c.font = '500 18px Inter, Arial'; c.fillText('clique pra ver o que falta', h, 466);
    tx.needsUpdate = true;
  }
  let t = 0, acc = 0, blink = false; const t0 = performance.now();
  draw(0, false);
  return {
    group: g, hit,
    update(dt) {
      t = (performance.now() - t0) / 1000; acc += dt;
      if (t < 3.2) { if (acc > 0.05) { acc = 0; const e = 1 - Math.pow(1 - Math.min(1, t / 3), 3); draw(pct * e, false); } }
      else if (acc > 0.6) { acc = 0; blink = !blink; draw(pct, blink); }
      glow.material.opacity = 0.42 + Math.sin(t * 1.6) * 0.08;
    },
  };
}
