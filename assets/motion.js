/* ==========================================================================
   ZAKAA — Astrolabe & Neural Vector Field Engine (assets/motion.js)
   (Islamic Astronomical Coordinates + Optical Refractions + 3D Neural Math)
   ========================================================================== */
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
    if (!art || !canvas) return;
    width = art.clientWidth;
    height = art.clientHeight;
    const ratio = Math.min(devicePixelRatio || 1, 1.75);
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    context.setTransform(ratio, 0, 0, ratio, 0, 0);

    // Toroidal Astrolabe Constellation
    const segments = width < 480 ? 80 : 150;
    const rings = 9;
    const count = segments * rings;
    particles = Array.from({length: count}, (_, i) => {
      const u = (i % segments) / segments * Math.PI * 2;
      const v = Math.floor(i / segments) / rings * Math.PI * 2 + u * 3;
      const tube = .09 + .025 * Math.sin(u * 3);
      const radius = .74 + tube * Math.cos(v);
      return {
        x: radius * Math.cos(u),
        y: tube * Math.sin(v),
        z: radius * Math.sin(u),
        isLapis: i % 8 === 0,
        size: i % 5 === 0 ? 1.6 : 0.9
      };
    });
  }

  /* Draw Astrolabe Coordinate Rings & Khatam Geometry */
  function drawAstrolabeCoords(cx, cy, radius, angle) {
    if (radius <= 0) return;
    context.save();
    context.translate(cx, cy);

    // Outer Graduated Astrolabe Circle
    context.strokeStyle = 'rgba(229, 178, 93, 0.22)';
    context.lineWidth = 1;
    context.beginPath();
    context.arc(0, 0, radius * 0.96, 0, Math.PI * 2);
    context.stroke();

    // Secondary Mid Dial (Dashed Almicantar)
    context.strokeStyle = 'rgba(14, 165, 233, 0.18)';
    context.setLineDash([4, 8]);
    context.beginPath();
    context.arc(0, 0, radius * 0.72, 0, Math.PI * 2);
    context.stroke();
    context.setLineDash([]);

    // 8-Point Sacred Khatam Star Geometry (Rotating slowly)
    context.save();
    context.rotate(angle * 0.8);
    context.strokeStyle = 'rgba(229, 178, 93, 0.16)';
    const starR = radius * 0.42;
    context.strokeRect(-starR, -starR, starR * 2, starR * 2);
    context.rotate(Math.PI / 4);
    context.strokeRect(-starR, -starR, starR * 2, starR * 2);
    context.restore();

    // Astrolabe 12-Hour Degree Ticks
    context.strokeStyle = 'rgba(229, 178, 93, 0.28)';
    const tickLen = 6;
    for (let i = 0; i < 24; i++) {
      const a = (i / 24) * Math.PI * 2;
      const x1 = Math.cos(a) * (radius * 0.96);
      const y1 = Math.sin(a) * (radius * 0.96);
      const x2 = Math.cos(a) * (radius * 0.96 - tickLen);
      const y2 = Math.sin(a) * (radius * 0.96 - tickLen);
      context.beginPath();
      context.moveTo(x1, y1);
      context.lineTo(x2, y2);
      context.stroke();
    }

    context.restore();
  }

  function paint() {
    if (!context) return;
    context.clearRect(0, 0, width, height);
    const scale = Math.min(width, height) * .59;
    const angle = clock * .000075 + pointer.x * .14;
    const tilt = .65 + pointer.y * .22;
    const cos = Math.cos(angle), sin = Math.sin(angle);
    const ct = Math.cos(tilt), st = Math.sin(tilt);
    const roll = -.38 + pointer.x * .16;
    const cr = Math.cos(roll), sr = Math.sin(roll);

    const cx = width / 2;
    const cy = height / 2;

    // Draw Astrolabe Underlay
    drawAstrolabeCoords(cx, cy, scale * 1.15, angle);

    // Project 3D Toroidal Constellation
    const projected = particles.map(p => {
      const x = p.x * cos - p.z * sin;
      const z = p.x * sin + p.z * cos;
      const y = p.y * ct - z * st;
      const depth = p.y * st + z * ct;
      const perspective = 2.8 / (2.8 - depth);
      return {
        x: cx + (x * cr - y * sr) * scale * perspective,
        y: cy + (x * sr + y * cr) * scale * perspective,
        depth,
        size: p.size * perspective,
        isLapis: p.isLapis
      };
    }).sort((a,b) => a.depth - b.depth);

    for (const p of projected) {
      const alpha = .22 + ((p.depth + 1) / 2) * .65;
      context.fillStyle = p.isLapis
        ? `rgba(14, 165, 233, ${alpha * 0.95})`
        : `rgba(229, 178, 93, ${alpha * 0.90})`;
      context.beginPath();
      context.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      context.fill();
    }
  }

  function draw(time) {
    frame = 0;
    if (stopped() || document.hidden || !visible) { lastTime = 0; return; }
    if (time - previous >= 16) {
      if (lastTime) clock += Math.min(time - lastTime, 64);
      lastTime = time;
      previous = time;
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

  pause?.addEventListener('click', () => { userPaused = !userPaused; sync(); });
  reduced.addEventListener('change', sync);
  document.addEventListener('visibilitychange', sync);
  new MutationObserver(updateLabel).observe(root, {attributes:true, attributeFilter:['lang']});
  
  if (context && art) {
    new ResizeObserver(() => { resize(); sync(); }).observe(art);
    new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; sync(); }).observe(art);
    if (matchMedia('(pointer: fine)').matches) {
      art.addEventListener('pointermove', e => {
        if (stopped()) return;
        const r = art.getBoundingClientRect();
        pointer.x = ((e.clientX - r.left) / r.width - .5) * 2;
        pointer.y = ((e.clientY - r.top) / r.height - .5) * 2;
        art.style.setProperty('--logo-x', `${pointer.x * 26}px`);
        art.style.setProperty('--logo-y', `${pointer.y * 26}px`);
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

  // About Hero Astrolabe 3D Parallax
  const aboutHero = document.querySelector('.about-hero');
  const astrolabe = document.querySelector('.astrolabe-mechanism');
  if (aboutHero && astrolabe && matchMedia('(pointer: fine)').matches) {
    aboutHero.addEventListener('pointermove', e => {
      if (stopped()) return;
      const r = aboutHero.getBoundingClientRect();
      const px = ((e.clientX - r.left) / r.width - 0.5) * 2;
      const py = ((e.clientY - r.top) / r.height - 0.5) * 2;
      astrolabe.style.transform = `perspective(900px) rotateY(${px * 22}deg) rotateX(${-py * 22}deg) scale(1.03)`;
    }, {passive:true});
    aboutHero.addEventListener('pointerleave', () => {
      astrolabe.style.transform = 'perspective(900px) rotateY(0deg) rotateX(0deg) scale(1)';
    });
  }

  const reveal = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      if (!stopped()) entry.target.classList.add('reveal-arrived');
      reveal.unobserve(entry.target);
    });
  }, {threshold:.12});
  document.querySelectorAll('.section-head, .service, .step, .proof-note, .contact-card, .catalog-card, .bento-card, .phase-card, .spec-box').forEach(el => reveal.observe(el));

  let scrollFrame = 0;
  const line = document.querySelector('.zakaa-scroll-line');
  const progress = () => {
    scrollFrame = 0;
    const max = Math.max(1, root.scrollHeight - innerHeight);
    line?.style.setProperty('--zakaa-progress', `${Math.min(100, scrollY / max * 100)}%`);
  };
  const schedule = () => { if (!scrollFrame) scrollFrame = requestAnimationFrame(progress); };
  addEventListener('scroll', schedule, {passive:true});
  addEventListener('resize', schedule, {passive:true});
  progress();
})();
