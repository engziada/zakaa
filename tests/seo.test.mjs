import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

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
