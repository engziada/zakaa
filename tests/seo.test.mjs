import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { runInNewContext } from 'node:vm';

const localizedPages = [
  ['index.html', 'https://zakaa-ai.net/en/', 'https://zakaa-ai.net/'],
  ['ar/ai-software.html', 'https://zakaa-ai.net/ai-software', 'https://zakaa-ai.net/ar/ai-software'],
  ['ar/academy.html', 'https://zakaa-ai.net/academy', 'https://zakaa-ai.net/ar/academy'],
  ['ar/erp360.html', 'https://zakaa-ai.net/erp360', 'https://zakaa-ai.net/ar/erp360'],
];

test('Arabic landing and priority pages are crawlable localized documents', async () => {
  for (const [file, englishUrl, arabicUrl] of localizedPages) {
    const html = await readFile(new URL(`../${file}`, import.meta.url), 'utf8');
    assert.match(html, /<html lang="ar" dir="rtl"/, file);
    assert.match(html, new RegExp(`<link rel="canonical" href="${arabicUrl.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}">`), file);
    assert.ok(html.includes(`<link rel="alternate" hreflang="en" href="${englishUrl}">`), file);
    assert.ok(html.includes(`<link rel="alternate" hreflang="ar" href="${arabicUrl}">`), file);
    assert.match(html, /<h1\b[^>]*>[\s\S]*[\u0600-\u06FF][\s\S]*<\/h1>/, file);
    assert.match(html, /<meta name="description"[^>]+content="[^"]+">/, file);

    const jsonLd = html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/);
    assert.ok(jsonLd, `${file}: JSON-LD missing`);
    const schema = JSON.parse(jsonLd[1]);
    assert.ok(schema['@graph'].some(item => item['@id'] === 'https://zakaa-ai.net/#organization'), file);
  }
});

test('sitemap lists localized priority pages and reciprocal language alternates', async () => {
  const sitemap = await readFile(new URL('../sitemap.xml', import.meta.url), 'utf8');
  for (const [, englishUrl, arabicUrl] of localizedPages) {
    assert.ok(sitemap.includes(`<loc>${englishUrl}</loc>`), englishUrl);
    assert.ok(sitemap.includes(`<loc>${arabicUrl}</loc>`), arabicUrl);
    assert.ok(sitemap.includes(`hreflang="en" href="${englishUrl}"`), englishUrl);
    assert.ok(sitemap.includes(`hreflang="ar" href="${arabicUrl}"`), arabicUrl);
  }
});

test('priority English pages link to their matching Arabic page', async () => {
  for (const [file, , arabicUrl] of localizedPages.slice(1)) {
    const html = await readFile(new URL(`../${file.replace(/^ar\//, '')}`, import.meta.url), 'utf8');
    assert.ok(html.includes(`<link rel="alternate" hreflang="ar" href="${arabicUrl}">`), file);
    assert.ok(html.includes(`href="${new URL(arabicUrl).pathname}" lang="ar" hreflang="ar"`), file);
  }
});

test('English homepage links back to the Arabic homepage', async () => {
  const html = await readFile(new URL('../en/index.html', import.meta.url), 'utf8');
  assert.match(html, /<html lang="en" dir="ltr"/);
  assert.ok(html.includes('<link rel="alternate" hreflang="ar" href="https://zakaa-ai.net/">'));
  assert.ok(html.includes('href="/" lang="ar" hreflang="ar"'));
});

test('homepage priority links keep their selected language', async () => {
  for (const [file, expectedPaths] of [
    ['index.html', ['/ar/ai-software', '/ar/erp360', '/ar/academy']],
    ['en/index.html', ['/ai-software', '/erp360', '/academy']],
  ]) {
    const html = await readFile(new URL(`../${file}`, import.meta.url), 'utf8');
    const anchors = [...html.matchAll(/<a\b([^>]*)>/g)].map(([, attrs]) => attrs.match(/\bhref="([^"]+)"/)?.[1]);
    for (const path of expectedPaths) assert.ok(anchors.includes(path), `${file}: ${path}`);
  }

  const script = await readFile(new URL('../assets/site.js', import.meta.url), 'utf8');
  assert.match(script, /querySelectorAll\('\.brand, \.navlinks a'\)/);
  assert.match(script, /querySelectorAll\('\.nav-cta'\)/);
});

test('all navigation links follow language across paired routes', async () => {
  const source = await readFile(new URL('../assets/site.js', import.meta.url), 'utf8');
  const run = selectedLanguage => {
    const makeElement = (href = '', className = '') => {
      let value = href;
      return {
        get href() { return value; },
        set href(next) { value = next; },
        getAttribute(name) { return name === 'href' ? value : null; },
        setAttribute(name, next) { if (name === 'href') value = next; },
        classList: {
          contains(name) { return className.split(' ').includes(name); },
          remove() {},
          toggle() { return false; },
        },
        addEventListener() {},
      };
    };
    const brand = makeElement('/');
    const home = makeElement('/');
    const academy = makeElement('/academy');
    const erp = makeElement('/erp360?view=inventory#details');
    const arabicAi = makeElement('/ar/ai-software');
    const language = makeElement('/ar/academy', 'lang');
    const cta = makeElement('/#contact');
    const anchors = [brand, home, academy, erp, arabicAi, language, cta];
    const menu = makeElement();
    const links = makeElement();
    const year = makeElement();
    const elements = { 'menu-toggle': menu, navlinks: links, 'lang-toggle': makeElement(), year };
    const document = {
      documentElement: { lang: 'en', dir: 'ltr', dataset: {} },
      body: { dataset: { titleEn: 'Title', titleAr: 'Title', descriptionEn: '', descriptionAr: '' } },
      getElementById(id) { return elements[id]; },
      querySelectorAll(selector) {
        if (selector === 'a[href]') return anchors;
        if (selector === '.brand, .navlinks a') return [brand, home];
        if (selector === '.nav-cta') return [cta];
        return [];
      },
      querySelector() { return null; },
      addEventListener() {},
    };
    const localStorage = {
      getItem(key) { return key === 'zakaa-lang' ? selectedLanguage : null; },
      setItem() {},
    };
    runInNewContext(source, { document, localStorage, window: { ZAKAA_RESTORED_COPY: {} } });
    return { brand, home, academy, erp, arabicAi, language, cta };
  };

  const arabic = run('ar');
  assert.equal(arabic.academy.href, '/ar/academy');
  assert.equal(arabic.erp.href, '/ar/erp360?view=inventory#details');
  assert.equal(arabic.arabicAi.href, '/ar/ai-software');
  assert.equal(arabic.language.href, '/ar/academy');
  assert.equal(arabic.brand.href, '/');
  assert.equal(arabic.home.href, '/');
  assert.equal(arabic.cta.href, '/#contact');

  const english = run('en');
  assert.equal(english.academy.href, '/academy');
  assert.equal(english.erp.href, '/erp360?view=inventory#details');
  assert.equal(english.arabicAi.href, '/ai-software');
  assert.equal(english.language.href, '/ar/academy');
  assert.equal(english.brand.href, '/en/');
  assert.equal(english.home.href, '/en/');
  assert.equal(english.cta.href, '/en/#contact');
});

test('Arabic priority pages share navigation and persist the selected theme', async () => {
  for (const file of ['ar/ai-software.html', 'ar/academy.html', 'ar/erp360.html']) {
    const html = await readFile(new URL(`../${file}`, import.meta.url), 'utf8');
    const header = html.match(/<header\b[\s\S]*?<\/header>/)?.[0];
    assert.ok(header, `${file}: header missing`);
    for (const href of ['/', '/about', '/services', '/products', '/ar/academy', '/initiatives', '/projects']) {
      assert.ok(header.includes(`href="${href}"`), `${file}: navigation link ${href} missing`);
    }
    assert.match(header, /id="theme-toggle"/, `${file}: theme control missing`);
    assert.match(html, /<meta name="color-scheme" content="dark light">/, `${file}: color-scheme missing`);
    assert.match(html, /src="\/assets\/theme-toggle\.js" defer/, `${file}: theme persistence missing`);
    assert.match(html, /localStorage\.setItem\("zakaa-lang","ar"\)/, `${file}: Arabic language preference missing`);
  }
});

test('English priority pages return to the English homepage', async () => {
  for (const file of ['ai-software.html', 'academy.html', 'erp360.html']) {
    const html = await readFile(new URL(`../${file}`, import.meta.url), 'utf8');
    const header = html.match(/<header\b[\s\S]*?<\/header>/)?.[0];
    assert.ok(header, `${file}: header missing`);
    assert.ok(header.includes('href="/en/"'), `${file}: English home link missing`);
    assert.ok(header.includes('href="/en/#contact"'), `${file}: English contact link missing`);
  }
});
