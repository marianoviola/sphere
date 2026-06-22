const canvas = document.querySelector("#sphere-field");
const ctx = canvas.getContext("2d", { alpha: false });

const TAU = Math.PI * 2;
const WHITE = [236, 244, 255];
const ACCENT = [120, 242, 255];

let width = 0;
let height = 0;
let pixelRatio = 1;
let spheres = [];
let stars = [];
let fragments = [];
let maxFragments = 20;
let pointer = { x: 0, y: 0, active: false };
let lastTime = performance.now();
let reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

function rgba(rgb, alpha) {
  return `rgba(${rgb[0]}, ${rgb[1]}, ${rgb[2]}, ${alpha})`;
}

function random(min, max) {
  return min + Math.random() * (max - min);
}

function mix(a, b, t) {
  return [
    a[0] + (b[0] - a[0]) * t,
    a[1] + (b[1] - a[1]) * t,
    a[2] + (b[2] - a[2]) * t,
  ];
}

function fitCanvas() {
  const rect = canvas.getBoundingClientRect();
  const w = Math.floor(rect.width);
  const h = Math.floor(rect.height);
  // Layout/fonts may not be settled on first run; bail until the element has a
  // real size. The ResizeObserver below calls back once it does.
  if (w < 1 || h < 1) return;
  pixelRatio = Math.min(window.devicePixelRatio || 1, 2);
  width = w;
  height = h;
  // Back the canvas with device pixels for the *measured* CSS size, then draw
  // in CSS units — crisp on HiDPI, never upscaled/grainy or stretched.
  canvas.width = Math.round(width * pixelRatio);
  canvas.height = Math.round(height * pixelRatio);
  ctx.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
  createField();
}

function createField() {
  const isSmall = width < 700;

  fragments = [];
  maxFragments = isSmall ? 10 : 20;

  // Depth starfield: x/y normalised to [-1, 1], z is depth toward the viewer.
  const starCount = isSmall ? 90 : 170;
  stars = Array.from({ length: starCount }, () => ({
    x: random(-1, 1),
    y: random(-1, 1),
    z: random(0.04, 1),
  }));

  // Wireframe globes drifting through a 2.5D space (Asteroids-style wrap).
  const count = isSmall ? 7 : 11;
  const minRadius = isSmall ? 30 : 44;
  const maxRadius = isSmall ? 64 : 120;
  spheres = Array.from({ length: count }, (_, index) => {
    const depth = random(0.34, 1);
    const drift = 0.018 * (isSmall ? 0.8 : 1);
    return {
      id: index,
      x: random(0, width),
      y: random(0, height),
      depth,
      baseRadius: random(minRadius, maxRadius),
      // Parallax: nearer globes (higher depth) drift faster.
      vx: random(-drift, drift) * (0.5 + depth),
      vy: random(-drift, drift) * (0.5 + depth),
      spin: random(0, TAU),
      spinSpeed: random(0.00012, 0.00032) * (random(0, 1) > 0.5 ? 1 : -1),
      tilt: random(-0.5, 0.5),
      glow: 0,
      emitTimer: random(900, 4200),
      sx: 0,
      sy: 0,
      r: 0,
    };
  });
}

// Irregular 3–6 vertex outline → reads as a shard, not a regular polygon.
function makeShardVerts() {
  const n = Math.floor(random(3, 6.99));
  const verts = [];
  for (let i = 0; i < n; i += 1) {
    verts.push({
      a: (i / n) * TAU + random(-0.28, 0.28),
      rr: random(0.52, 1),
    });
  }
  return verts;
}

function spawnFragment(sphere) {
  const isShard = Math.random() < 0.62;
  const angle = random(0, TAU);
  const dist = random(0, sphere.r * 0.55);
  const drift = random(0.004, 0.014);
  const heading = random(0, TAU);
  fragments.push({
    kind: isShard ? "shard" : "mote",
    parent: sphere,
    depth: sphere.depth,
    // Local position/velocity, relative to the parent globe's centre.
    lx: Math.cos(angle) * dist,
    ly: Math.sin(angle) * dist,
    lvx: Math.cos(heading) * drift,
    lvy: Math.sin(heading) * drift,
    spin: random(0, TAU),
    spinSpeed: random(0.0002, 0.0006) * (Math.random() > 0.5 ? 1 : -1),
    size: isShard ? random(5, 11) * sphere.depth : random(0.8, 1.7),
    verts: isShard ? makeShardVerts() : null,
    age: 0,
    life: isShard ? random(7000, 13000) : random(4500, 9000),
  });
}

// Fade in, hold, fade out across the fragment's lifetime.
function lifeEnvelope(frag) {
  const f = frag.age / frag.life;
  if (f < 0.18) return f / 0.18;
  if (f > 0.7) return Math.max(0, (1 - f) / 0.3);
  return 1;
}

function updateFragment(frag, delta) {
  const speed = reducedMotion ? 0.18 : 1;
  frag.age += delta;
  frag.lx += frag.lvx * delta * speed;
  frag.ly += frag.lvy * delta * speed;
  frag.spin += frag.spinSpeed * delta * speed;

  // Contained within the parent globe — bounce softly off its inner wall.
  const bound = frag.parent.r * 0.82 - frag.size;
  const d = Math.hypot(frag.lx, frag.ly);
  if (bound > 0 && d > bound) {
    const nx = frag.lx / d;
    const ny = frag.ly / d;
    frag.lx = nx * bound;
    frag.ly = ny * bound;
    const dot = frag.lvx * nx + frag.lvy * ny;
    frag.lvx -= 2 * dot * nx;
    frag.lvy -= 2 * dot * ny;
  }
}

// Faint links between fragments sharing a globe → an internal constellation.
function drawFragmentRelations() {
  for (let i = 0; i < fragments.length; i += 1) {
    for (let j = i + 1; j < fragments.length; j += 1) {
      const a = fragments[i];
      const b = fragments[j];
      if (a.parent !== b.parent) continue;
      const ea = lifeEnvelope(a);
      const eb = lifeEnvelope(b);
      if (ea <= 0 || eb <= 0) continue;
      const d = Math.hypot(b.lx - a.lx, b.ly - a.ly);
      const reach = a.parent.r * 0.9;
      if (d > reach) continue;
      const alpha = (1 - d / reach) * 0.16 * (0.4 + a.depth) * Math.min(ea, eb);
      ctx.beginPath();
      ctx.moveTo(a.parent.sx + a.lx, a.parent.sy + a.ly);
      ctx.lineTo(b.parent.sx + b.lx, b.parent.sy + b.ly);
      ctx.strokeStyle = rgba(WHITE, alpha);
      ctx.lineWidth = 0.5;
      ctx.stroke();
    }
  }
}

function drawFragment(frag) {
  const env = lifeEnvelope(frag);
  if (env <= 0) return;

  const ax = frag.parent.sx + frag.lx;
  const ay = frag.parent.sy + frag.ly;

  if (frag.kind === "mote") {
    const alpha = (0.1 + frag.depth * 0.3) * env;
    ctx.beginPath();
    ctx.arc(ax, ay, frag.size, 0, TAU);
    ctx.fillStyle = rgba(WHITE, alpha);
    ctx.fill();
    return;
  }

  const alpha = (0.16 + frag.depth * 0.4) * env;
  ctx.save();
  ctx.translate(ax, ay);
  ctx.beginPath();
  frag.verts.forEach((v, i) => {
    const px = Math.cos(v.a + frag.spin) * frag.size * v.rr;
    const py = Math.sin(v.a + frag.spin) * frag.size * v.rr;
    if (i === 0) ctx.moveTo(px, py);
    else ctx.lineTo(px, py);
  });
  ctx.closePath();
  ctx.strokeStyle = rgba(WHITE, alpha);
  ctx.lineWidth = 0.5 + frag.depth * 0.6;
  ctx.stroke();
  ctx.restore();
}

function updateStars(delta) {
  const speed = (reducedMotion ? 0.1 : 1) * 0.000016 * delta;
  for (const star of stars) {
    star.z -= speed;
    if (star.z <= 0.03) {
      star.z = 1;
      star.x = random(-1, 1);
      star.y = random(-1, 1);
    }
  }
}

function updateSphere(sphere, delta) {
  const speed = reducedMotion ? 0.14 : 1;
  sphere.spin += sphere.spinSpeed * delta * speed * (0.4 + sphere.depth);
  sphere.x += sphere.vx * delta * speed;
  sphere.y += sphere.vy * delta * speed;
  sphere.glow *= Math.pow(0.94, delta / 16.67);

  sphere.r = sphere.baseRadius * sphere.depth;
  sphere.sx = sphere.x;
  sphere.sy = sphere.y;

  // Toroidal wrap: leave one edge, re-enter from the opposite one.
  const margin = sphere.r + 4;
  if (sphere.x < -margin) sphere.x = width + margin;
  if (sphere.x > width + margin) sphere.x = -margin;
  if (sphere.y < -margin) sphere.y = height + margin;
  if (sphere.y > height + margin) sphere.y = -margin;

  if (pointer.active) {
    const dx = sphere.sx - pointer.x;
    const dy = sphere.sy - pointer.y;
    const distance = Math.hypot(dx, dy);
    const reach = sphere.r + 130;
    if (distance < reach && distance > 0.001) {
      const force = (1 - distance / reach) * 0.00012 * delta;
      sphere.vx += (dx / distance) * force;
      sphere.vy += (dy / distance) * force;
      sphere.glow = Math.min(1, sphere.glow + 0.05);
    }
  }

  // Keep the globe populated: refill fragments up to its capacity.
  sphere.emitTimer -= delta;
  if (sphere.emitTimer <= 0) {
    const capacity = 1 + Math.round(sphere.depth * 2.5);
    let count = 0;
    for (const frag of fragments) {
      if (frag.parent === sphere) count += 1;
    }
    if (count < capacity && fragments.length < maxFragments) spawnFragment(sphere);
    sphere.emitTimer = random(1200, 3200) * (reducedMotion ? 2.4 : 1);
  }
}

function drawStars() {
  ctx.fillStyle = "#000000";
  ctx.fillRect(0, 0, width, height);

  const cx = width / 2;
  const cy = height / 2;
  const spread = Math.max(width, height) * 0.62;

  for (const star of stars) {
    const k = 1 / star.z;
    const sx = cx + star.x * k * spread;
    const sy = cy + star.y * k * spread;
    if (sx < -4 || sx > width + 4 || sy < -4 || sy > height + 4) continue;
    const near = 1 - star.z;
    const size = Math.max(0.4, near * 1.7);
    const alpha = Math.min(0.7, 0.12 + near * 0.6);
    ctx.beginPath();
    ctx.arc(sx, sy, size, 0, TAU);
    ctx.fillStyle = rgba(WHITE, alpha);
    ctx.fill();
  }
}

function drawRelations() {
  for (let i = 0; i < spheres.length; i += 1) {
    for (let j = i + 1; j < spheres.length; j += 1) {
      const a = spheres[i];
      const b = spheres[j];
      const dx = b.sx - a.sx;
      const dy = b.sy - a.sy;
      const distance = Math.hypot(dx, dy);
      const reach = (a.r + b.r) * 1.9 + 90;
      if (distance > reach) continue;
      const closeness = 1 - distance / reach;
      const depth = Math.min(a.depth, b.depth);
      const alpha = closeness * 0.22 * (0.4 + depth);
      ctx.beginPath();
      ctx.moveTo(a.sx, a.sy);
      ctx.lineTo(b.sx, b.sy);
      ctx.strokeStyle = rgba(WHITE, alpha);
      ctx.lineWidth = 0.6;
      ctx.stroke();
    }
  }
}

function drawSphere(sphere) {
  const r = sphere.r;
  const glow = Math.min(1, sphere.glow);
  const color = glow > 0.02 ? mix(WHITE, ACCENT, glow) : WHITE;
  const alpha = 0.2 + sphere.depth * 0.5 + glow * 0.2;

  ctx.save();
  ctx.translate(sphere.sx, sphere.sy);
  ctx.lineWidth = 0.6 + sphere.depth * 0.7;

  // Silhouette.
  ctx.beginPath();
  ctx.arc(0, 0, r, 0, TAU);
  ctx.strokeStyle = rgba(color, alpha);
  ctx.stroke();

  // Equator ring (tilted) — reads as a globe rather than a flat disc.
  ctx.beginPath();
  ctx.ellipse(0, 0, r, r * 0.3, sphere.tilt, 0, TAU);
  ctx.strokeStyle = rgba(color, alpha * 0.5);
  ctx.stroke();

  // Two meridians whose width oscillates with spin → rotation illusion.
  const m1 = Math.abs(Math.cos(sphere.spin));
  ctx.beginPath();
  ctx.ellipse(0, 0, r * m1, r, sphere.tilt, 0, TAU);
  ctx.strokeStyle = rgba(color, alpha * 0.42);
  ctx.stroke();

  const m2 = Math.abs(Math.cos(sphere.spin + Math.PI / 2));
  ctx.beginPath();
  ctx.ellipse(0, 0, r * m2, r, sphere.tilt, 0, TAU);
  ctx.strokeStyle = rgba(color, alpha * 0.24);
  ctx.stroke();

  ctx.restore();
}

function animate(now) {
  const delta = Math.min(34, now - lastTime);
  lastTime = now;

  updateStars(delta);
  for (const sphere of spheres) {
    updateSphere(sphere, delta);
  }
  for (const frag of fragments) {
    updateFragment(frag, delta);
  }
  fragments = fragments.filter((frag) => frag.age < frag.life);

  drawStars();
  drawRelations();
  // Far globes first so nearer ones overlap them.
  const ordered = spheres.slice().sort((a, b) => a.depth - b.depth);
  for (const sphere of ordered) {
    drawSphere(sphere);
  }
  // Fragments live inside their globe, drawn over its wireframe.
  drawFragmentRelations();
  for (const frag of fragments) {
    drawFragment(frag);
  }

  requestAnimationFrame(animate);
}

function updatePointer(event) {
  const rect = canvas.getBoundingClientRect();
  pointer.x = event.clientX - rect.left;
  pointer.y = event.clientY - rect.top;
  pointer.active = true;
}

// Coalesce refit requests to one per frame.
let fitScheduled = false;
function scheduleFit() {
  if (fitScheduled) return;
  fitScheduled = true;
  requestAnimationFrame(() => {
    fitScheduled = false;
    fitCanvas();
  });
}

window.addEventListener("pointermove", updatePointer);
window.addEventListener("pointerleave", () => {
  pointer.active = false;
});

window.matchMedia("(prefers-reduced-motion: reduce)").addEventListener("change", (event) => {
  reducedMotion = event.matches;
});

// Re-fit whenever the canvas actually changes size — this corrects a wrong
// first measurement once layout/fonts settle, and handles rotation/resize —
// instead of relying on a single load-time read of getBoundingClientRect.
if (typeof ResizeObserver !== "undefined") {
  new ResizeObserver(scheduleFit).observe(canvas);
} else {
  window.addEventListener("resize", scheduleFit);
}

fitCanvas();
requestAnimationFrame(animate);
