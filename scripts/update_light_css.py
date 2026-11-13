#!/usr/bin/env python3
"""Append light theme adaptations for new UI elements to light.css."""
from pathlib import Path

light_css = Path('assets/light.css')
content = light_css.read_text(encoding='utf-8')

new_light_styles = """
/* Light theme overrides for new Bento Switcher, Hubs, and Astrolabe */
html[data-theme="light"] .bento-nav {
  background: #FFFFFF;
  border-color: var(--line);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
}
html[data-theme="light"] .bento-tab.active {
  background: var(--copper);
  color: #FFFFFF;
  box-shadow: 0 2px 12px rgba(201, 147, 59, 0.35);
}
html[data-theme="light"] .bento-card {
  background: #FFFFFF;
  border-color: var(--line);
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.04);
}
html[data-theme="light"] .bento-card:hover {
  border-color: var(--copper);
  box-shadow: 0 16px 36px rgba(201, 147, 59, 0.15);
}
html[data-theme="light"] .bento-card-media {
  background: #F8F5F0;
  border-bottom-color: var(--line);
}
html[data-theme="light"] .bento-badge {
  background: rgba(14, 165, 233, 0.1);
  color: #0284c7;
  border-color: rgba(14, 165, 233, 0.25);
}
html[data-theme="light"] .matrix-container {
  background: #FFFFFF;
  border-color: var(--line);
}
html[data-theme="light"] .matrix-table th {
  background: #F6F1EA;
  color: var(--ink);
}
html[data-theme="light"] .matrix-table td {
  border-bottom-color: var(--line);
}
html[data-theme="light"] .spec-box,
html[data-theme="light"] .phase-card {
  background: #FFFFFF;
  border-color: var(--line);
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.03);
}
html[data-theme="light"] .astrolabe-cardinal {
  background: #FFFFFF;
  color: var(--copper);
  border-color: var(--copper);
}
html[data-theme="light"] .astrolabe-core {
  background: radial-gradient(circle, #F7CB78, #FAF7F2);
  border-color: var(--copper);
}
html[data-theme="light"] .hiero-orbit-marker {
  background: #FFFFFF;
  border-color: var(--copper);
}
"""

if 'bento-nav' not in content:
    content += '\n' + new_light_styles
    light_css.write_text(content, encoding='utf-8')
    print('Updated assets/light.css successfully!')
else:
    print('Already present in assets/light.css')
