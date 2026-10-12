/* Projected 3D particle observatory, without a WebGL dependency. */
(() => {
  const canvas = document.querySelector('.ai-network');
  const art = document.querySelector('.hero-art');
  const context = canvas?.getContext('2d');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const pause = document.querySelector('.motion-toggle');
  const root = document.documentElement;
  let userPaused = false;
  let visible = true;
  let frame = 0;
  let width = 0;
  let height = 0;
  let previous = 0;
  let clock = 0;
  let lastTime = 0;
  let particles = [];
  const pointer = {x: 0, y: 0};
  const stopped = () => reduced.matches || userPaused;

  function updateLabel() {
    if (!pause) return;
    const ar = root.lang === 'ar';
    pause.textContent = stopped() ? (ar ? 'الحركة متوقفة' : 'Motion paused') : (ar ? 'إيقاف الحركة' : 'Pause motion');
    pause.setAttribute('aria-pressed', String(stopped()));
    pause.disabled = reduced.matches;
    pause.title = reduced.matches ? (ar ? 'حسب إعداد تقليل الحركة في جهازك' : 'Your device prefers reduced motion') : '';
  }

  function resize() {
    width = art.clientWidth;
    height = art.clientHeight;
    const ratio = Math.min(devicePixelRatio || 1, 1.75);
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
    // A deterministic toroidal cloud stays stable across resize and language changes.
    const segments = width < 480 ? 72 : 140;
    const rings = 9;
    const count = segments * rings;
    particles = Array.from({length: count}, (_, i) => {
      const u = (i % segments) / segments * Math.PI * 2;
      const v = Math.floor(i / segments) / rings * Math.PI * 2 + u * 3;
      const tube = .09 + .025 * Math.sin(u * 3);
      const radius = .74 + tube * Math.cos(v);
      return {x: radius * Math.cos(u), y: tube * Math.sin(v), z: radius * Math.sin(u), ice: i % 9 === 0, size: i % 5 === 0 ? 1.5 : .8};
    });
  }

  function paint() {
    context.clearRect(0, 0, width, height);
    const scale = Math.min(width, height) * .59;
    const angle = clock * .000075;
    const tilt = .65 + pointer.y * .08;
    const cos = Math.cos(angle), sin = Math.sin(angle);
    const ct = Math.cos(tilt), st = Math.sin(tilt);
    const roll = -.38 + pointer.x * .06;
    const cr = Math.cos(roll), sr = Math.sin(roll);
    const projected = particles.map(p => {
      const x = p.x * cos - p.z * sin;
      const z = p.x * sin + p.z * cos;
      const y = p.y * ct - z * st;
      const depth = p.y * st + z * ct;
      const perspective = 2.8 / (2.8 - depth);
      return {x: width / 2 + (x * cr - y * sr) * scale * perspective,
        y: height / 2 + (x * sr + y * cr) * scale * perspective,
        depth, size: p.size * perspective, ice: p.ice};
    }).sort((a,b) => a.depth - b.depth);
    for (const p of projected) {
      const alpha = .22 + ((p.depth + 1) / 2) * .62;
      context.fillStyle = p.ice ? `rgba(158,216,210,${alpha})` : `rgba(239,173,120,${alpha})`;
      context.beginPath();context.arc(p.x, p.y, p.size, 0, Math.PI * 2);context.fill();
    }
  }

  function draw(time) {
    frame = 0;
    if (stopped() || document.hidden || !visible) {lastTime = 0;return;}
    if (time - previous >= 32) {
      if (lastTime) clock += Math.min(time - lastTime, 64);
      lastTime = time; previous = time;
      paint();
    }
    frame = requestAnimationFrame(draw);
  }

  function sync() {
    if (frame) cancelAnimationFrame(frame);
    frame = 0; lastTime = 0;
    root.classList.toggle('motion-paused', stopped());
    updateLabel();
    if (!context || !art) return;
    paint();
    if (!stopped() && !document.hidden && visible) frame = requestAnimationFrame(draw);
  }

  pause?.addEventListener('click', () => {userPaused = !userPaused;sync();});
  reduced.addEventListener('change', sync);
  document.addEventListener('visibilitychange', sync);
  new MutationObserver(updateLabel).observe(root, {attributes:true, attributeFilter:['lang']});
  if (context && art) {
    new ResizeObserver(() => {resize();sync();}).observe(art);
    new IntersectionObserver(([entry]) => {visible = entry.isIntersecting;sync();}).observe(art);
    if (matchMedia('(pointer: fine)').matches) {
      art.addEventListener('pointermove', e => {
        if (stopped()) return;
        const r = art.getBoundingClientRect();
        pointer.x = (e.clientX - r.left) / r.width - .5;
        pointer.y = (e.clientY - r.top) / r.height - .5;
        art.style.setProperty('--logo-x', `${pointer.x * 10}px`);
        art.style.setProperty('--logo-y', `${pointer.y * 10}px`);
      }, {passive:true});
      art.addEventListener('pointerleave', () => {
        pointer.x = pointer.y = 0;
        art.style.setProperty('--logo-x', '0px');
        art.style.setProperty('--logo-y', '0px');
      });
    }
    resize();
  }
  sync();

  const reveal = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      if (!stopped()) entry.target.classList.add('reveal-arrived');
      reveal.unobserve(entry.target);
    });
  }, {threshold:.12});
  document.querySelectorAll('.section-head, .service, .step, .proof-note, .contact-card').forEach(el => reveal.observe(el));

  let scrollFrame = 0;
  const line = document.querySelector('.zakaa-scroll-line');
  const progress = () => {
    scrollFrame = 0;
    const max = Math.max(1, root.scrollHeight - innerHeight);
    line?.style.setProperty('--zakaa-progress', `${Math.min(100, scrollY / max * 100)}%`);
  };
  const schedule = () => {if (!scrollFrame) scrollFrame = requestAnimationFrame(progress);};
  addEventListener('scroll', schedule, {passive:true});
  addEventListener('resize', schedule, {passive:true});
  progress();
})();
