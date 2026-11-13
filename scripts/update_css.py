#!/usr/bin/env python3
"""Append new styles for cultural glyphs, About astrolabe, Bento switcher, and Hubs to theme.css."""
from pathlib import Path

theme_css = Path('assets/theme.css')
content = theme_css.read_text(encoding='utf-8')

new_styles = """
/* ==========================================================================
   DYNAMIC CULTURAL GLYPHS (Universal Card Watermarks)
   ========================================================================== */
.catalog-card .card-body::after,
.bento-card .card-body::after,
.vm::after, .why::after, .service::after, .contact-card::after, .do-row::after {
  content: "";
  position: absolute;
  pointer-events: none;
  z-index: 0;
  width: 136px;
  height: 168px;
  bottom: -22px;
  inset-inline-end: -12px;
  background-position: center;
  background-size: contain;
  background-repeat: no-repeat;
  opacity: 0.18;
  transform: rotate(-10deg) scale(0.95);
  transition: opacity 0.45s cubic-bezier(0.16, 1, 0.3, 1), transform 0.65s cubic-bezier(0.16, 1, 0.3, 1), filter 0.45s ease;
  background-image: url("./glyphs/arabic-zakaa.svg");
}

:is(.catalog-card, .bento-card):is([data-slug*="erp360"], :has(a[href*="erp360"])) .card-body::after { background-image: url("./glyphs/hiero-djed.svg"); }
:is(.catalog-card, .bento-card):is([data-slug*="worktracker"], :has(a[href*="worktracker"])) .card-body::after { background-image: url("./glyphs/hiero-wadjet.svg"); }
:is(.catalog-card, .bento-card):is([data-slug*="yourspace"], :has(a[href*="yourspace"])) .card-body::after { background-image: url("./glyphs/arabic-khatam.svg"); }
:is(.catalog-card, .bento-card):is([data-slug*="gathering"], :has(a[href*="gathering"])) .card-body::after { background-image: url("./glyphs/hiero-ankh.svg"); }
:is(.catalog-card, .bento-card):is([data-slug*="madinaty-ai"], :has(a[href*="madinaty-ai"])) .card-body::after { background-image: url("./glyphs/hiero-scarab.svg"); }
:is(.catalog-card, .bento-card):is([data-slug*="ai-software"], :has(a[href*="ai-software"])) .card-body::after { background-image: url("./glyphs/ai-neural.svg"); }
:is(.catalog-card, .bento-card):is([data-slug*="consulting"], :has(a[href*="consulting"])) .card-body::after { background-image: url("./glyphs/arabic-zakaa.svg"); }
:is(.catalog-card, .bento-card):is([data-slug*="websites-ecommerce"], :has(a[href*="websites-ecommerce"])) .card-body::after { background-image: url("./glyphs/ai-quantum.svg"); }
:is(.catalog-card, .bento-card):is([data-slug*="academy"], :has(a[href*="academy"])) .card-body::after { background-image: url("./glyphs/arabic-noon.svg"); }
:is(.catalog-card, .bento-card):is([data-slug*="autostop"], :has(a[href*="autostop"])) .card-body::after { background-image: url("./glyphs/ai-astrolabe.svg"); }
:is(.catalog-card, .bento-card):is([data-slug*="loqma"], :has(a[href*="loqma"])) .card-body::after { background-image: url("./glyphs/hiero-ankh.svg"); }
:is(.catalog-card, .bento-card):is([data-slug*="souk-el-kanto"], :has(a[href*="souk-el-kanto"])) .card-body::after { background-image: url("./glyphs/arabic-khatam.svg"); }
:is(.catalog-card, .bento-card):is([data-slug*="eduflow"], :has(a[href*="eduflow"])) .card-body::after { background-image: url("./glyphs/arabic-noon.svg"); }
:is(.catalog-card, .bento-card):is([data-slug*="masar"], :has(a[href*="masar"])) .card-body::after { background-image: url("./glyphs/ai-astrolabe.svg"); }

:is(.catalog-card, .bento-card, .vm, .why, .service):is(:hover, :focus-within) .card-body::after,
:is(.vm, .why, .service):hover::after {
  opacity: 0.38;
  transform: rotate(-3deg) scale(1.12);
  filter: drop-shadow(0 0 16px rgba(229, 178, 93, 0.45));
}

/* ==========================================================================
   ABOUT HERO: ALEXANDRIAN ASTROLABE OF COGNITION
   ========================================================================== */
.about-hero {
  position: relative;
  isolation: isolate;
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  align-items: center;
  min-height: 440px;
  padding-block: 56px 48px;
  gap: 40px;
  overflow: hidden;
}
.about-hero::before, .about-hero::after { display: none !important; }

.about-hero-copy {
  display: flex;
  flex-direction: column;
  gap: 16px;
  z-index: 2;
}
.about-hero-copy h1 { margin-bottom: 0; }
.about-hero-copy .lead { margin-top: 0; max-width: 620px; }

.about-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 8px;
}
.about-badge {
  font-family: var(--font-mono, monospace);
  font-size: 11px;
  letter-spacing: 0.08em;
  padding: 6px 12px;
  border-radius: 4px;
  background: rgba(229, 178, 93, 0.08);
  border: 1px solid rgba(229, 178, 93, 0.25);
  color: var(--copper);
}

.about-hero-stage {
  position: relative;
  width: 100%;
  aspect-ratio: 1;
  max-width: 380px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  perspective: 1000px;
}

.astrolabe-mechanism {
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transform-style: preserve-3d;
  transition: transform 0.25s cubic-bezier(0.25, 1, 0.5, 1);
}

.astrolabe-limb {
  position: absolute;
  inset: 12px;
  border-radius: 50%;
  border: 1.5px solid rgba(229, 178, 93, 0.4);
  box-shadow: 0 0 35px rgba(229, 178, 93, 0.15), inset 0 0 25px rgba(14, 165, 233, 0.08);
  background: radial-gradient(circle, transparent 62%, rgba(229, 178, 93, 0.05) 65%, transparent 68%);
  animation: astrolabe-limb-spin 90s linear infinite;
}
.astrolabe-limb::before {
  content: '';
  position: absolute;
  inset: -6px;
  border-radius: 50%;
  border: 1px dashed rgba(229, 178, 93, 0.25);
}
.astrolabe-limb::after {
  content: '';
  position: absolute;
  inset: 18px;
  border-radius: 50%;
  border: 1px solid rgba(14, 165, 233, 0.2);
}

.astrolabe-khatam {
  position: absolute;
  width: 58%;
  height: 58%;
  border: 1.5px solid rgba(229, 178, 93, 0.35);
  transform: rotate(0deg);
  animation: khatam-counter-spin 45s linear infinite;
}
.astrolabe-khatam::before {
  content: '';
  position: absolute;
  inset: -1.5px;
  border: 1.5px solid rgba(229, 178, 93, 0.35);
  transform: rotate(45deg);
  background: rgba(229, 178, 93, 0.03);
}

.astrolabe-cardinal {
  position: absolute;
  font-family: var(--font-arabic, sans-serif);
  font-size: 11px;
  font-weight: 600;
  color: var(--copper);
  background: rgba(12, 9, 7, 0.9);
  padding: 3px 8px;
  border: 1px solid rgba(229, 178, 93, 0.3);
  border-radius: 4px;
  letter-spacing: 0.05em;
  z-index: 5;
}
.astrolabe-cardinal.north { top: 0; transform: translateY(-50%); }
.astrolabe-cardinal.south { bottom: 0; transform: translateY(50%); }
.astrolabe-cardinal.east { inset-inline-end: 0; transform: translateX(50%); }
.astrolabe-cardinal.west { inset-inline-start: 0; transform: translateX(-50%); }

.astrolabe-core {
  position: relative;
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(229, 178, 93, 0.25) 0%, rgba(12, 9, 7, 0.95) 70%);
  border: 1.5px solid var(--copper);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 40px rgba(229, 178, 93, 0.4), inset 0 0 15px rgba(229, 178, 93, 0.3);
  z-index: 4;
}
.solar-pulse {
  position: absolute;
  inset: -15px;
  border-radius: 50%;
  border: 1px dashed rgba(229, 178, 93, 0.4);
  animation: solar-pulse-breathe 4s ease-in-out infinite alternate;
}
.core-glyph svg {
  width: 44px;
  height: 44px;
  animation: core-glyph-float 6s ease-in-out infinite alternate;
}

.hiero-orbit-marker {
  position: absolute;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(12, 9, 7, 0.92);
  border: 1px solid var(--copper);
  box-shadow: 0 0 14px rgba(229, 178, 93, 0.35);
  background-position: center;
  background-size: 65%;
  background-repeat: no-repeat;
  z-index: 6;
}
.hiero-orbit-marker.ankh {
  top: 18%;
  inset-inline-start: 14%;
  background-image: url("./glyphs/hiero-ankh.svg");
  animation: orbit-bob-1 5s ease-in-out infinite alternate;
}
.hiero-orbit-marker.wadjet {
  bottom: 20%;
  inset-inline-start: 16%;
  background-image: url("./glyphs/hiero-wadjet.svg");
  animation: orbit-bob-2 6s ease-in-out infinite alternate 1s;
}
.hiero-orbit-marker.djed {
  top: 25%;
  inset-inline-end: 14%;
  background-image: url("./glyphs/hiero-djed.svg");
  animation: orbit-bob-3 5.5s ease-in-out infinite alternate 0.5s;
}

@keyframes astrolabe-limb-spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes khatam-counter-spin { from { transform: rotate(0deg); } to { transform: rotate(-360deg); } }
@keyframes solar-pulse-breathe { 0% { transform: scale(0.92); opacity: 0.4; } 100% { transform: scale(1.12); opacity: 0.9; } }
@keyframes core-glyph-float { 0% { transform: translateY(-2px) scale(0.96); } 100% { transform: translateY(2px) scale(1.04); } }
@keyframes orbit-bob-1 { 0% { transform: translateY(0px) rotate(0deg); } 100% { transform: translateY(-8px) rotate(12deg); } }
@keyframes orbit-bob-2 { 0% { transform: translateY(0px) rotate(0deg); } 100% { transform: translateY(8px) rotate(-10deg); } }
@keyframes orbit-bob-3 { 0% { transform: translateY(0px) rotate(0deg); } 100% { transform: translateY(-6px) rotate(-8deg); } }

/* ==========================================================================
   HOMEPAGE INTERACTIVE BENTO SWITCHER
   ========================================================================== */
.bento-switcher-section {
  padding-block: 72px;
  border-top: 1px solid var(--line);
  position: relative;
}
.bento-header {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 40px;
}
.bento-nav-wrap {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
}
.bento-nav {
  display: inline-flex;
  gap: 8px;
  background: rgba(22, 18, 15, 0.8);
  border: 1px solid var(--line);
  padding: 6px;
  border-radius: 40px;
  backdrop-filter: blur(8px);
}
.bento-tab {
  background: transparent;
  border: none;
  color: var(--muted);
  font-family: var(--font-base, sans-serif);
  font-size: 13px;
  font-weight: 500;
  padding: 8px 18px;
  border-radius: 30px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.bento-tab:hover {
  color: var(--ink);
  background: rgba(229, 178, 93, 0.08);
}
.bento-tab.active {
  background: var(--copper);
  color: #0c0907;
  font-weight: 700;
  box-shadow: 0 2px 14px rgba(229, 178, 93, 0.35);
}
.bento-metrics-pill {
  font-family: var(--font-mono, monospace);
  font-size: 12px;
  color: var(--copper);
  background: rgba(229, 178, 93, 0.08);
  border: 1px solid rgba(229, 178, 93, 0.2);
  padding: 6px 14px;
  border-radius: 30px;
}

.bento-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 24px;
}
.bento-card {
  position: relative;
  border: 1px solid var(--line);
  border-radius: 14px;
  background: linear-gradient(150deg, #171310, #100d0a);
  overflow: hidden;
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.4s ease, box-shadow 0.4s ease, opacity 0.3s ease;
  display: flex;
  flex-direction: column;
}
.bento-card.is-hidden {
  display: none !important;
}
.bento-card:hover {
  transform: translateY(-6px);
  border-color: rgba(229, 178, 93, 0.5);
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.5), 0 0 24px rgba(229, 178, 93, 0.12);
}
.bento-card-media {
  width: 100%;
  height: 180px;
  background: #1a1512;
  border-bottom: 1px solid var(--line);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  padding: 16px;
}
.bento-card-media img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
.bento-card:hover .bento-card-media img {
  transform: scale(1.08);
}
.bento-card .card-body {
  padding: 24px;
  position: relative;
  display: flex;
  flex-direction: column;
  flex: 1;
}
.bento-badge {
  display: inline-block;
  align-self: flex-start;
  font-family: var(--font-mono, monospace);
  font-size: 10px;
  letter-spacing: 0.08em;
  padding: 4px 10px;
  border-radius: 4px;
  background: rgba(14, 165, 233, 0.1);
  border: 1px solid rgba(14, 165, 233, 0.3);
  color: #38bdf8;
  margin-bottom: 12px;
}
.bento-card h3 {
  font-size: 20px;
  margin-bottom: 10px;
}
.bento-card p {
  color: var(--muted);
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 18px;
  flex: 1;
}
.bento-card-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: auto;
  padding-top: 14px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

/* ==========================================================================
   REDESIGNED /PRODUCTS & /SERVICES COMMAND HUBS
   ========================================================================== */
.hub-intro {
  padding-block: 64px 44px;
  border-bottom: 1px solid var(--line);
  position: relative;
}
.hub-grid-2 {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 28px;
}
.spec-box {
  background: linear-gradient(150deg, #171310, #100d0a);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 28px;
  position: relative;
  overflow: hidden;
}
.spec-box h3 {
  font-size: 22px;
  margin-bottom: 12px;
  color: var(--ink);
}
.spec-list {
  list-style: none;
  padding: 0;
  margin: 18px 0 24px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.spec-list li {
  font-size: 14px;
  color: var(--muted);
  display: flex;
  align-items: flex-start;
  gap: 10px;
  line-height: 1.5;
}
.spec-list li::before {
  content: '✦';
  color: var(--copper);
  font-size: 11px;
  margin-top: 2px;
}

/* Feature Matrix Table */
.matrix-container {
  overflow-x: auto;
  border: 1px solid var(--line);
  border-radius: 12px;
  background: #14100d;
  margin-block: 36px;
}
.matrix-table {
  width: 100%;
  border-collapse: collapse;
  text-align: start;
  font-size: 14px;
}
.matrix-table th, .matrix-table td {
  padding: 16px 20px;
  border-bottom: 1px solid rgba(229, 178, 93, 0.1);
}
.matrix-table th {
  background: #1a1512;
  color: var(--copper);
  font-family: var(--font-mono, monospace);
  font-size: 12px;
  letter-spacing: 0.05em;
}
.matrix-table tr:hover td {
  background: rgba(229, 178, 93, 0.03);
}

/* 4-Phase Engineering Framework */
.phase-framework {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 20px;
  margin-block: 40px;
}
.phase-card {
  position: relative;
  background: linear-gradient(150deg, #16120e, #0e0b08);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease, border-color 0.3s ease;
}
.phase-card:hover {
  transform: translateY(-5px);
  border-color: var(--copper);
}
.phase-num {
  font-family: var(--font-mono, monospace);
  font-size: 26px;
  font-weight: 700;
  color: var(--copper);
  margin-bottom: 12px;
  opacity: 0.85;
}
.phase-card h4 {
  font-size: 17px;
  margin-bottom: 10px;
  color: var(--ink);
}
.phase-card p {
  font-size: 13px;
  color: var(--muted);
  line-height: 1.6;
}

@media (max-width: 900px) {
  .about-hero { grid-template-columns: 1fr; }
  .bento-grid { grid-template-columns: 1fr; }
  .hub-grid-2 { grid-template-columns: 1fr; }
  .phase-framework { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 600px) {
  .phase-framework { grid-template-columns: 1fr; }
  .bento-nav { width: 100%; justify-content: center; }
  .bento-tab { padding: 6px 12px; font-size: 12px; }
}
"""

if 'DYNAMIC CULTURAL GLYPHS' not in content:
    content += '\n' + new_styles
    theme_css.write_text(content, encoding='utf-8')
    print('Updated assets/theme.css successfully!')
else:
    print('Styles already present in assets/theme.css')
