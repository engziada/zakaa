(() => {
  const root = document.documentElement;
  const menu = document.getElementById('menu-toggle');
  const links = document.getElementById('navlinks');
  const language = document.getElementById('lang-toggle');
  function closeMenu() { links.classList.remove('open'); menu.setAttribute('aria-expanded','false'); }
  function setLanguage(lang) {
    root.lang = lang; root.dir = lang === 'ar' ? 'rtl' : 'ltr';
    document.querySelectorAll('[data-i18n],[data-i18n-html]').forEach(el => { const key=el.dataset.i18n||el.dataset.i18nHtml; const value=window.ZAKAA_RESTORED_COPY?.[lang]?.[key]; if(value!==undefined){if(el.dataset.i18nHtml)el.innerHTML=value;else el.textContent=value;} });
    document.querySelectorAll('[data-en][data-ar]').forEach(el => { el.textContent = el.dataset[lang]; });
    language.textContent = lang === 'ar' ? 'EN' : 'عربي';
    language.setAttribute('aria-label',lang === 'ar' ? 'Switch to English' : 'Switch to Arabic');
    menu.setAttribute('aria-label',lang === 'ar' ? 'القائمة الرئيسية' : 'Main menu');
    const suffix = lang === 'ar' ? 'Ar' : 'En';
    document.title = document.body.dataset['title'+suffix] + ' | Zaka2';
    const description = document.body.dataset['description'+suffix];
    document.querySelectorAll('meta[name="description"],meta[property="og:description"],meta[name="twitter:description"]').forEach(el => el.content = description);
    document.querySelectorAll('meta[property="og:title"],meta[name="twitter:title"]').forEach(el => el.content = document.title);
    const locale = document.querySelector('meta[property="og:locale"]'); if(locale) locale.content = lang === 'ar' ? 'ar_EG' : 'en_US';
    try { localStorage.setItem('zakaa-lang',lang); } catch {}
  }
  language.addEventListener('click',()=>setLanguage(root.lang === 'ar' ? 'en' : 'ar'));
  menu.addEventListener('click',()=>{ const open = links.classList.toggle('open'); menu.setAttribute('aria-expanded',String(open)); });
  document.addEventListener('keydown',e=>{ if(e.key==='Escape' && links.classList.contains('open')){closeMenu();menu.focus();} });
  links.addEventListener('click',e=>{if(e.target.closest('a'))closeMenu();});

  // Interactive Bento Capability Switcher
  const bentoTabs = document.querySelectorAll('.bento-tab');
  const bentoCards = document.querySelectorAll('.bento-card');
  if (bentoTabs.length && bentoCards.length) {
    bentoTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        bentoTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        const filter = tab.dataset.filter;
        bentoCards.forEach(card => {
          if (filter === 'all' || card.dataset.group === filter) {
            card.classList.remove('is-hidden');
          } else {
            card.classList.add('is-hidden');
          }
        });
      });
    });
  }

  let lang = navigator.language?.startsWith('ar') ? 'ar' : 'en';
  try { const saved=localStorage.getItem('zakaa-lang'); if(['en','ar'].includes(saved))lang=saved; } catch {}
  setLanguage(lang); document.getElementById('year').textContent=new Date().getFullYear();
})();
