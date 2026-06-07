const canvas = document.querySelector("#sphere-field");
const ctx = canvas.getContext("2d", { alpha: false });

const palette = {
  base: [244, 250, 255],
  cyan: [120, 242, 255],
  green: [180, 255, 204],
  amber: [255, 212, 138],
  rose: [255, 157, 179],
};

let width = 0;
let height = 0;
let pixelRatio = 1;
let spheres = [];
let links = [];
let pointer = { x: 0, y: 0, active: false };
let lastTime = performance.now();
let reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

function rgba(rgb, alpha) {
  return `rgba(${rgb[0]}, ${rgb[1]}, ${rgb[2]}, ${alpha})`;
}

function random(min, max) {
  return min + Math.random() * (max - min);
}

function fitCanvas() {
  const rect = canvas.getBoundingClientRect();
  pixelRatio = Math.min(window.devicePixelRatio || 1, 2);
  width = Math.max(1, Math.floor(rect.width));
  height = Math.max(1, Math.floor(rect.height));
  canvas.width = Math.floor(width * pixelRatio);
  canvas.height = Math.floor(height * pixelRatio);
  ctx.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
  createField();
}

function createField() {
  const isSmall = width < 700;
  const count = isSmall ? 11 : 18;
  const minRadius = isSmall ? 28 : 38;
  const maxRadius = isSmall ? 78 : 128;
  spheres = Array.from({ length: count }, (_, index) => {
    const radius = random(minRadius, maxRadius);
    return {
      id: index,
      x: random(radius, width - radius),
      y: random(radius, height - radius),
      vx: random(-0.035, 0.035) * (isSmall ? 0.8 : 1),
      vy: random(-0.03, 0.03) * (isSmall ? 0.8 : 1),
      radius,
      targetRadius: radius * random(0.84, 1.18),
      phase: random(0, Math.PI * 2),
      pulse: 0,
      color: palette.base,
      operation: "",
    };
  });

  links = [];
}

function setPulse(sphere, color, operation) {
  sphere.pulse = Math.min(1, sphere.pulse + 0.075);
  sphere.color = color;
  sphere.operation = operation;
}

function updateSphere(sphere, delta) {
  const speed = reducedMotion ? 0.12 : 1;
  sphere.phase += delta * 0.00018 * speed;
  sphere.x += sphere.vx * delta * speed;
  sphere.y += sphere.vy * delta * speed;
  sphere.targetRadius += Math.sin(sphere.phase) * 0.012 * delta * speed;
  sphere.radius += (sphere.targetRadius - sphere.radius) * 0.003 * delta;
  sphere.pulse *= Math.pow(0.985, delta / 16.67);

  if (sphere.radius < 26) sphere.targetRadius = random(44, 92);
  if (sphere.radius > Math.min(width, height) * 0.28) sphere.targetRadius *= 0.82;

  if (sphere.x < sphere.radius || sphere.x > width - sphere.radius) {
    sphere.vx *= -1;
    sphere.x = Math.max(sphere.radius, Math.min(width - sphere.radius, sphere.x));
    setPulse(sphere, palette.cyan, "boundary");
  }

  if (sphere.y < sphere.radius || sphere.y > height - sphere.radius) {
    sphere.vy *= -1;
    sphere.y = Math.max(sphere.radius, Math.min(height - sphere.radius, sphere.y));
    setPulse(sphere, palette.green, "boundary");
  }

  if (pointer.active) {
    const dx = sphere.x - pointer.x;
    const dy = sphere.y - pointer.y;
    const distance = Math.hypot(dx, dy);
    const reach = sphere.radius + 120;
    if (distance < reach && distance > 0.001) {
      const force = (1 - distance / reach) * 0.00016 * delta;
      sphere.vx += (dx / distance) * force;
      sphere.vy += (dy / distance) * force;
      setPulse(sphere, palette.rose, "mutation");
    }
  }

  const velocity = Math.hypot(sphere.vx, sphere.vy);
  if (velocity > 0.07) {
    sphere.vx *= 0.98;
    sphere.vy *= 0.98;
  }
}

function resolveCollisions() {
  links = [];
  for (let i = 0; i < spheres.length; i += 1) {
    for (let j = i + 1; j < spheres.length; j += 1) {
      const a = spheres[i];
      const b = spheres[j];
      const dx = b.x - a.x;
      const dy = b.y - a.y;
      const distance = Math.hypot(dx, dy);
      const overlap = a.radius + b.radius - distance;
      const near = distance < (a.radius + b.radius) * 1.28;

      if (near) {
        links.push({ a, b, overlap: Math.max(0, overlap), distance });
      }

      if (overlap > 0 && distance > 0.001) {
        const nx = dx / distance;
        const ny = dy / distance;
        const push = overlap * 0.0015;
        a.vx -= nx * push;
        a.vy -= ny * push;
        b.vx += nx * push;
        b.vy += ny * push;
        a.targetRadius *= 0.9992;
        b.targetRadius *= 1.0006;
        setPulse(a, palette.amber, "intersection");
        setPulse(b, palette.amber, "union");
      }
    }
  }
}

function drawStars(time) {
  ctx.fillStyle = "#02050b";
  ctx.fillRect(0, 0, width, height);

  const spacing = width < 700 ? 58 : 72;
  ctx.save();
  ctx.globalAlpha = 0.26;
  ctx.strokeStyle = "rgba(244, 250, 255, 0.07)";
  ctx.lineWidth = 1;
  for (let x = ((time * 0.002) % spacing) - spacing; x < width + spacing; x += spacing) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x + height * 0.18, height);
    ctx.stroke();
  }
  for (let y = ((time * 0.0015) % spacing) - spacing; y < height + spacing; y += spacing) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(width, y + width * 0.08);
    ctx.stroke();
  }
  ctx.restore();
}

function drawLinks() {
  for (const link of links) {
    const alpha = link.overlap > 0 ? 0.42 : 0.12;
    const color = link.overlap > 0 ? palette.amber : palette.base;
    ctx.beginPath();
    ctx.moveTo(link.a.x, link.a.y);
    ctx.lineTo(link.b.x, link.b.y);
    ctx.strokeStyle = rgba(color, alpha);
    ctx.lineWidth = link.overlap > 0 ? 1.2 : 0.7;
    ctx.stroke();

    if (link.overlap > 0) {
      const mx = (link.a.x + link.b.x) / 2;
      const my = (link.a.y + link.b.y) / 2;
      const lens = Math.min(link.overlap * 0.28, 28);
      ctx.beginPath();
      ctx.ellipse(mx, my, lens * 1.8, lens, Math.atan2(link.b.y - link.a.y, link.b.x - link.a.x), 0, Math.PI * 2);
      ctx.strokeStyle = rgba(palette.amber, 0.55);
      ctx.lineWidth = 1;
      ctx.stroke();
    }
  }
}

function drawSphere(sphere, time) {
  const pulse = Math.min(1, sphere.pulse);
  const color = pulse > 0.02 ? sphere.color : palette.base;
  const alpha = 0.46 + pulse * 0.42;
  const wobble = Math.sin(time * 0.0012 + sphere.phase) * 1.8;
  const radius = sphere.radius + wobble;

  ctx.save();
  ctx.translate(sphere.x, sphere.y);

  ctx.beginPath();
  ctx.arc(0, 0, radius, 0, Math.PI * 2);
  ctx.strokeStyle = rgba(color, alpha);
  ctx.lineWidth = 1 + pulse * 0.9;
  ctx.stroke();

  ctx.beginPath();
  ctx.arc(0, 0, radius * 0.64, 0, Math.PI * 2);
  ctx.strokeStyle = rgba(color, 0.13 + pulse * 0.16);
  ctx.lineWidth = 0.8;
  ctx.stroke();

  ctx.beginPath();
  ctx.ellipse(0, 0, radius, radius * 0.36, sphere.phase * 0.32, 0, Math.PI * 2);
  ctx.strokeStyle = rgba(color, 0.15 + pulse * 0.24);
  ctx.lineWidth = 0.8;
  ctx.stroke();

  if (pulse > 0.18 && sphere.operation) {
    ctx.font = "500 10px Quicksand, sans-serif";
    ctx.fillStyle = rgba(color, Math.min(0.9, pulse + 0.15));
    ctx.textAlign = "center";
    ctx.fillText(sphere.operation, 0, -radius - 10);
  }

  ctx.restore();
}

function animate(now) {
  const delta = Math.min(34, now - lastTime);
  lastTime = now;

  for (const sphere of spheres) {
    updateSphere(sphere, delta);
  }
  resolveCollisions();

  drawStars(now);
  drawLinks();
  for (const sphere of spheres) {
    drawSphere(sphere, now);
  }

  requestAnimationFrame(animate);
}

function updatePointer(event) {
  const rect = canvas.getBoundingClientRect();
  pointer.x = event.clientX - rect.left;
  pointer.y = event.clientY - rect.top;
  pointer.active = true;
}

window.addEventListener("resize", fitCanvas);
window.addEventListener("pointermove", updatePointer);
window.addEventListener("pointerleave", () => {
  pointer.active = false;
});

window.matchMedia("(prefers-reduced-motion: reduce)").addEventListener("change", (event) => {
  reducedMotion = event.matches;
});

fitCanvas();
requestAnimationFrame(animate);
