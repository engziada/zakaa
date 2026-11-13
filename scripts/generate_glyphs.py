#!/usr/bin/env python3
"""Generate crisp, authentic vector glyphs combining Arabic Calligraphy, Egyptian Hieroglyphs, Astrolabe, and AI."""
from pathlib import Path

glyphs = {
  'arabic-zakaa': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 220">
  <g fill="none" stroke="#efad78" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">
    <polygon points="90,28 102,40 90,52 78,40" fill="#efad78" fill-opacity="0.35"/>
    <path d="M118 72 C115 62 104 60 92 68 C80 76 68 102 62 135 C58 158 64 178 88 182 C112 186 138 178 152 170" stroke-width="2.2"/>
    <path d="M104 64 C112 55 124 54 130 58" opacity="0.6"/>
    <path d="M48 150 C54 165 65 178 82 185" stroke-dasharray="3 3" opacity="0.5"/>
    <path d="M125 110 L138 98" stroke-width="1.8" opacity="0.7"/>
    <path d="M62 70 L72 82" opacity="0.5"/>
  </g>
</svg>''',

  'arabic-noon': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 220">
  <g fill="none" stroke="#efad78" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">
    <polygon points="90,75 98,83 90,91 82,83" fill="#efad78" fill-opacity="0.45"/>
    <circle cx="90" cy="83" r="16" stroke-dasharray="2 4" opacity="0.5"/>
    <path d="M142 98 C140 148 126 182 90 182 C54 182 40 148 38 108 C37 98 42 90 48 90 C54 90 56 100 58 112 C62 145 74 168 90 168 C106 168 120 145 124 102" stroke-width="2.2"/>
    <line x1="90" y1="30" x2="90" y2="60" stroke-width="1.8" stroke-linecap="round"/>
    <polygon points="90,20 86,30 94,30" fill="#efad78" opacity="0.7"/>
    <path d="M24 120 A70 70 0 0 0 156 120" stroke-dasharray="3 5" opacity="0.4"/>
  </g>
</svg>''',

  'arabic-khatam': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 220">
  <g fill="none" stroke="#efad78" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="90" cy="110" r="82" stroke-dasharray="2 4" opacity="0.4"/>
    <circle cx="90" cy="110" r="68" stroke="#efad78" opacity="0.6"/>
    <rect x="44" y="64" width="92" height="92" transform="rotate(0 90 110)" stroke-width="1.8"/>
    <rect x="44" y="64" width="92" height="92" transform="rotate(45 90 110)" stroke-width="1.8" fill="#efad78" fill-opacity="0.05"/>
    <circle cx="90" cy="110" r="24" stroke-width="1.2"/>
    <polygon points="90,92 95,105 108,110 95,115 90,128 85,115 72,110 85,105" fill="#efad78" fill-opacity="0.4"/>
    <line x1="90" y1="18" x2="90" y2="32" stroke-width="2"/>
    <line x1="90" y1="188" x2="90" y2="202" stroke-width="2"/>
    <line x1="8" y1="110" x2="22" y2="110" stroke-width="2"/>
    <line x1="158" y1="110" x2="172" y2="110" stroke-width="2"/>
  </g>
</svg>''',

  'hiero-ankh': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 220">
  <g fill="none" stroke="#efad78" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">
    <ellipse cx="90" cy="62" rx="32" ry="42" stroke-width="2.2"/>
    <ellipse cx="90" cy="62" rx="18" ry="26" stroke-width="1.4" fill="#efad78" fill-opacity="0.08"/>
    <circle cx="90" cy="62" r="6" fill="#efad78" fill-opacity="0.5"/>
    <path d="M38 116 L142 116" stroke-width="2.4"/>
    <path d="M38 122 L142 122" stroke-width="1.2" opacity="0.6"/>
    <rect x="34" y="113" width="6" height="12" rx="2" fill="#efad78" opacity="0.8"/>
    <rect x="140" y="113" width="6" height="12" rx="2" fill="#efad78" opacity="0.8"/>
    <path d="M84 122 L84 202" stroke-width="2"/>
    <path d="M96 122 L96 202" stroke-width="2"/>
    <line x1="90" y1="122" x2="90" y2="202" stroke-dasharray="3 3" opacity="0.5"/>
    <rect x="80" y="198" width="20" height="6" rx="1" fill="#efad78" opacity="0.8"/>
    <path d="M48 42 A55 55 0 0 1 132 42" stroke-dasharray="2 4" opacity="0.4"/>
  </g>
</svg>''',

  'hiero-wadjet': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 220">
  <g fill="none" stroke="#efad78" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">
    <path d="M36 68 C64 48 116 48 144 68" stroke-width="2.4"/>
    <path d="M144 68 C136 64 88 56 36 74" opacity="0.5"/>
    <path d="M34 94 C56 70 120 70 146 94 C120 118 56 118 34 94 Z" stroke-width="2" fill="#efad78" fill-opacity="0.06"/>
    <circle cx="90" cy="94" r="16" stroke-width="1.6"/>
    <circle cx="90" cy="94" r="7" fill="#efad78" fill-opacity="0.7"/>
    <path d="M68 108 L68 152 C68 156 64 160 60 160" stroke-width="2.2"/>
    <path d="M104 106 C114 124 128 136 126 150 C124 162 108 166 100 156 C94 148 102 140 108 144" stroke-width="2"/>
    <line x1="22" y1="94" x2="32" y2="94" stroke-width="1.8"/>
    <line x1="148" y1="94" x2="158" y2="94" stroke-width="1.8"/>
    <path d="M50 185 L130 185" stroke-dasharray="3 4" opacity="0.4"/>
  </g>
</svg>''',

  'hiero-djed': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 220">
  <g fill="none" stroke="#efad78" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">
    <rect x="44" y="42" width="92" height="10" rx="2" stroke-width="1.8" fill="#efad78" fill-opacity="0.15"/>
    <rect x="40" y="60" width="100" height="10" rx="2" stroke-width="1.8" fill="#efad78" fill-opacity="0.15"/>
    <rect x="36" y="78" width="108" height="10" rx="2" stroke-width="1.8" fill="#efad78" fill-opacity="0.15"/>
    <rect x="32" y="96" width="116" height="10" rx="2" stroke-width="1.8" fill="#efad78" fill-opacity="0.15"/>
    <path d="M78 42 L78 195 L64 205 L116 205 L102 195 L102 42 Z" stroke-width="2" fill="#efad78" fill-opacity="0.05"/>
    <line x1="90" y1="106" x2="90" y2="195" stroke-dasharray="3 3" stroke-width="1.4" opacity="0.6"/>
    <path d="M54 205 L126 205" stroke-width="3"/>
    <path d="M90 20 L90 34" stroke-width="2"/>
    <path d="M70 24 L78 36" opacity="0.6"/>
    <path d="M110 24 L102 36" opacity="0.6"/>
  </g>
</svg>''',

  'hiero-scarab': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 220">
  <g fill="none" stroke="#efad78" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="90" cy="35" r="16" stroke-width="2" fill="#efad78" fill-opacity="0.2"/>
    <circle cx="90" cy="35" r="26" stroke-dasharray="2 4" opacity="0.5"/>
    <path d="M78 62 L102 62 L98 52 L82 52 Z" stroke-width="1.6"/>
    <path d="M72 74 C72 64 108 64 108 74 L114 86 L66 86 Z" stroke-width="1.8" fill="#efad78" fill-opacity="0.1"/>
    <path d="M66 88 C45 92 40 135 68 160 C78 168 88 170 88 170 L88 88 Z" stroke-width="1.8"/>
    <path d="M114 88 C135 92 140 135 112 160 C102 168 92 170 92 170 L92 88 Z" stroke-width="1.8"/>
    <line x1="90" y1="88" x2="90" y2="170" stroke-width="2"/>
    <path d="M68 66 C50 62 42 48 38 42" stroke-width="1.6"/>
    <path d="M112 66 C130 62 138 48 142 42" stroke-width="1.6"/>
    <path d="M66 110 C46 112 36 122 30 138" stroke-width="1.6"/>
    <path d="M114 110 C134 112 144 122 150 138" stroke-width="1.6"/>
    <path d="M74 156 C60 172 52 188 56 198" stroke-width="1.6"/>
    <path d="M106 156 C120 172 128 188 124 198" stroke-width="1.6"/>
  </g>
</svg>''',

  'ai-neural': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 220">
  <g fill="none" stroke="#efad78" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="42" cy="65" r="8" stroke-width="1.6"/>
    <circle cx="42" cy="110" r="8" stroke-width="1.6"/>
    <circle cx="42" cy="155" r="8" stroke-width="1.6"/>
    <circle cx="90" cy="50" r="9" stroke-width="1.8" fill="#efad78" fill-opacity="0.15"/>
    <circle cx="90" cy="90" r="9" stroke-width="1.8" fill="#efad78" fill-opacity="0.25"/>
    <circle cx="90" cy="130" r="9" stroke-width="1.8" fill="#efad78" fill-opacity="0.15"/>
    <circle cx="90" cy="170" r="9" stroke-width="1.8" fill="#efad78" fill-opacity="0.15"/>
    <circle cx="138" cy="80" r="10" stroke-width="2" fill="#efad78" fill-opacity="0.35"/>
    <circle cx="138" cy="140" r="10" stroke-width="2" fill="#efad78" fill-opacity="0.35"/>
    <line x1="50" y1="65" x2="81" y2="50" opacity="0.5"/>
    <line x1="50" y1="65" x2="81" y2="90" opacity="0.8" stroke-width="1.6"/>
    <line x1="50" y1="110" x2="81" y2="50" opacity="0.4"/>
    <line x1="50" y1="110" x2="81" y2="90" opacity="0.9" stroke-width="2"/>
    <line x1="50" y1="110" x2="81" y2="130" opacity="0.7"/>
    <line x1="50" y1="155" x2="81" y2="130" opacity="0.8" stroke-width="1.6"/>
    <line x1="50" y1="155" x2="81" y2="170" opacity="0.5"/>
    <line x1="99" y1="50" x2="128" y2="80" opacity="0.6"/>
    <line x1="99" y1="90" x2="128" y2="80" opacity="0.9" stroke-width="2"/>
    <line x1="99" y1="90" x2="128" y2="140" opacity="0.8" stroke-width="1.6"/>
    <line x1="99" y1="130" x2="128" y2="80" opacity="0.5"/>
    <line x1="99" y1="130" x2="128" y2="140" opacity="0.9" stroke-width="2"/>
    <line x1="99" y1="170" x2="128" y2="140" opacity="0.6"/>
    <circle cx="138" cy="80" r="18" stroke-dasharray="2 4" opacity="0.4"/>
    <circle cx="138" cy="140" r="18" stroke-dasharray="2 4" opacity="0.4"/>
  </g>
</svg>''',

  'ai-astrolabe': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 220">
  <g fill="none" stroke="#efad78" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="90" cy="22" r="12" stroke-width="2"/>
    <rect x="84" y="32" width="12" height="14" fill="#efad78" fill-opacity="0.4"/>
    <circle cx="90" cy="120" r="72" stroke-width="2.2"/>
    <circle cx="90" cy="120" r="64" stroke-width="1.2" stroke-dasharray="3 3" opacity="0.6"/>
    <ellipse cx="90" cy="128" rx="40" ry="34" stroke-width="1.6" fill="#efad78" fill-opacity="0.06"/>
    <polygon points="90,56 94,68 86,68" fill="#efad78"/>
    <polygon points="130,94 120,98 122,90" fill="#efad78"/>
    <polygon points="50,94 60,98 58,90" fill="#efad78"/>
    <polygon points="120,150 110,146 114,140" fill="#efad78"/>
    <polygon points="60,150 70,146 66,140" fill="#efad78"/>
    <circle cx="90" cy="120" r="5" fill="#efad78"/>
    <path d="M28 120 A62 44 0 0 1 152 120" stroke-width="1.4" stroke-dasharray="2 3"/>
  </g>
</svg>''',

  'ai-quantum': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 220">
  <g fill="none" stroke="#efad78" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">
    <ellipse cx="90" cy="110" rx="74" ry="26" stroke-width="1.6"/>
    <g transform="rotate(60 90 110)">
      <ellipse cx="90" cy="110" rx="74" ry="26" stroke-width="1.6"/>
    </g>
    <g transform="rotate(120 90 110)">
      <ellipse cx="90" cy="110" rx="74" ry="26" stroke-width="1.6"/>
    </g>
    <circle cx="90" cy="110" r="14" stroke-width="2" fill="#efad78" fill-opacity="0.35"/>
    <circle cx="90" cy="110" r="6" fill="#efad78"/>
    <circle cx="164" cy="110" r="4.5" fill="#efad78"/>
    <circle cx="53" cy="46" r="4.5" fill="#efad78"/>
    <circle cx="53" cy="174" r="4.5" fill="#efad78"/>
    <polygon points="90,40 148,75 148,145 90,180 32,145 32,75" stroke-dasharray="3 4" opacity="0.35"/>
  </g>
</svg>'''
}

out_dir = Path('assets/glyphs')
out_dir.mkdir(parents=True, exist_ok=True)
for name, svg in glyphs.items():
  p = out_dir / f'{name}.svg'
  p.write_text(svg.strip() + '\n', encoding='utf-8')
print(f'Successfully wrote {len(glyphs)} cultural glyphs to assets/glyphs/')
