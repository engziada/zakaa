import { projects } from "./project-data.js";
/* Distinct vector diagrams describe purpose rather than pretend to be product screenshots. */
const PORTFOLIO_GROUPS = ['Solution', 'Tool / free service', 'Website sample'];
let portfolioFilter = 'All';
export function renderPortfolio(lang) {
  const target = document.getElementById('portfolio-content');
  const controls = document.getElementById('portfolio-controls');
  if (!target || !controls) return;
  const items = projects;
  const ar = lang === 'ar';
  const labels = ar
    ? {'All':'الكل','Solution':'حلول برمجية','Tool / free service':'أدوات وخدمات','Website sample':'نماذج مواقع'}
    : {'All':'All work','Solution':'Solutions','Tool / free service':'Tools & services','Website sample':'Website samples'};
  target.replaceChildren();
  // Preserve keyboard focus by keeping filter buttons when their category is unchanged.
  if (!controls.children.length) {
    for (const category of ['All', ...PORTFOLIO_GROUPS]) {
      const button = document.createElement('button');
      button.type = 'button'; button.className = 'portfolio-filter'; button.dataset.category = category;
      button.addEventListener('click', () => {portfolioFilter = category;renderPortfolio(document.documentElement.lang);});
      controls.append(button);
    }
  }
  for (const button of controls.children) {
    const category = button.dataset.category;
    const count = category === 'All' ? items.length : items.filter(x => x.group === category).length;
    button.textContent = `${labels[category]} (${count})`;
    button.setAttribute('aria-pressed', String(portfolioFilter === category));
  }
  for (const category of PORTFOLIO_GROUPS) {
    const entries = items.filter(x => x.group === category);
    const group = document.createElement('div'); group.className = 'portfolio-group';
    group.hidden = portfolioFilter !== 'All' && portfolioFilter !== category;
    const head = document.createElement('div'); head.className = 'portfolio-group-head';
    const h = document.createElement('h3'); h.textContent = labels[category];
    const count = document.createElement('span'); count.className = 'portfolio-count'; count.textContent = `${entries.length} ${ar ? 'مشاريع' : 'projects'}`;
    head.append(h, count); group.append(head);
    const grid = document.createElement('div'); grid.className = 'portfolio-grid';
    for (const entry of entries) {
      const card = document.createElement('article'); card.className = 'portfolio-card';
      const media = document.createElement('div'); media.className = 'portfolio-media';
      const image = document.createElement('img'); image.src = `./assets/illustrations/${entry.visual}.svg`;
      image.alt = ''; image.loading = 'lazy'; image.decoding = 'async'; image.width = 640; image.height = 400;
      media.append(image);
      const body = document.createElement('div'); body.className = 'portfolio-body';
      const kicker = document.createElement('span'); kicker.className = 'portfolio-kicker'; kicker.textContent = labels[category];
      const name = document.createElement('h4'); name.textContent = entry.name;
      const desc = document.createElement('p'); desc.textContent = ar ? entry.ar : entry.en;
      body.append(kicker, name);
      if (entry.status) {const status = document.createElement('span');status.className = 'project-status';status.textContent = entry.status[ar ? 'ar' : 'en'];body.append(status);}
      const actions = document.createElement('div'); actions.className = 'portfolio-actions';
      const link = document.createElement('a'); link.href = '#contact'; link.textContent = (ar ? 'لنتحدث عن هذا المشروع' : 'Discuss this project') + ' ↗';
      link.setAttribute('aria-label', `${link.textContent}: ${entry.name}`);
      actions.append(link);body.append(desc, actions);card.append(media, body);grid.append(card);
    }
    group.append(grid);target.append(group);
  }
}
