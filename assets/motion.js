/* Lightweight neural field: no WebGL dependency, bounded work, decorative only. */
(() => {
  const canvas = document.querySelector('.ai-network');
  const hero = document.querySelector('.hero');
  const context = canvas?.getContext('2d');
  if (!context || !hero) return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let width = 0, height = 0, frame = 0, visible = true, points = [], previous = 0;
  function resize() {
    width = hero.clientWidth; height = hero.clientHeight;
    const ratio = Math.min(devicePixelRatio || 1, 2);
    canvas.width = width * ratio; canvas.height = height * ratio;
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
    points = Array.from({length: width < 600 ? 24 : 48}, (_, i) => ({
      x: ((i * 137.508) % width), y: ((i * 83.17) % height),
      phase: i * 1.7
    }));
  }
  function draw(time) {
    frame = 0;
    if (reduced.matches || document.hidden || !visible) return;
    if (time - previous > 32) {
      previous = time;
      context.clearRect(0, 0, width, height);
      const positions = points.map(p => ({x:p.x + Math.sin(time / 6500 + p.phase) * 22, y:p.y + Math.cos(time / 8000 + p.phase) * 18}));
      for (let i = 0; i < positions.length; i++) {
        const a = positions[i];
        for (let j = i + 1; j < positions.length; j++) {
          const b = positions[j], distance = Math.hypot(a.x - b.x, a.y - b.y);
          if (distance < 160) {
            context.strokeStyle = `rgba(146,108,67,${(1 - distance / 160) * .22})`;
            context.beginPath(); context.moveTo(a.x, a.y); context.lineTo(b.x, b.y); context.stroke();
          }
        }
        context.fillStyle = 'rgba(146,108,67,.38)';
        context.beginPath(); context.arc(a.x, a.y, 1.8, 0, Math.PI * 2); context.fill();
      }
    }
    frame = requestAnimationFrame(draw);
  }
  function sync() {
    if (frame) cancelAnimationFrame(frame);
    frame = 0;
    context.clearRect(0, 0, width, height);
    if (!reduced.matches && !document.hidden && visible) frame = requestAnimationFrame(draw);
  }
  new ResizeObserver(() => {resize();sync();}).observe(hero);
  new IntersectionObserver(([entry]) => {visible = entry.isIntersecting;sync();}).observe(hero);
  reduced.addEventListener('change', sync);
  document.addEventListener('visibilitychange', sync);
  resize(); sync();
})();
