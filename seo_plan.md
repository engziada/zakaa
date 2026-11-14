# ZAKAA SEO Implementation Plan

## Purpose

Improve ZAKAA's organic visibility in English and Arabic, first for branded searches and relevant Egypt/Cairo searches, then for broader competitive topics. SEO work can improve discoverability, but cannot guarantee a first-place ranking.

Implementation is underway on branch `feature/seo-implementation`. Account setup and publication remain pending.

## Current baseline

- The live homepage, `robots.txt`, and `sitemap.xml` returned HTTP 200 during the initial review.
- `robots.txt` allows crawling and references `https://zakaa-ai.net/sitemap.xml`.
- The sitemap lists 20 public routes.
- Pages have canonical URLs, titles, descriptions, Open Graph metadata, and basic `WebPage` JSON-LD.
- Before this branch, Arabic and English content shared URLs. The language switch changed visible text, title, and description with JavaScript. Some pages had English source text even though the homepage initially declared Arabic.
- The site has not been checked against Google Search Console or Bing Webmaster Tools data. Current indexing and rankings are unknown.

## Implementation status

- **1. Crawlable language pages — partial:** The Arabic homepage remains at `/` to preserve the requested default landing page; `/en/` serves its English counterpart. AI/software, Academy, and ERP360 now have static Arabic HTML at `/ar/<page>` with reciprocal `hreflang` tags. The homepage retains its existing bilingual interactive layout; its metadata and first-fold copy are Arabic, but a full no-JavaScript content pass remains. Other pages still need reviewed Arabic copy and reciprocal routes.
- **2. Search-intent pages — partial:** Homepage, AI/software, Academy, and ERP360 metadata and content now target specific Egypt/Cairo business and training topics. Keyword demand and competitor research still need Search Console and keyword-tool data.
- **3. Trust and structured data — partial:** Priority pages use a shared `Organization` identity and page-specific `WebPage` data. No client results, testimonials, instructor credentials, course schedules, or address were added because these require verified owner-provided facts and permissions.
- **4. Indexing and measurement — pending external setup:** Search Console, Bing Webmaster Tools, and analytics ownership are not available in this repository. Verify ownership and submit the sitemap after deployment.
- **5. Local discovery — pending owner verification:** No Business Profile or directory records were changed. Confirm eligibility, business details, and account ownership first.

## Principles and constraints

- Keep all claims accurate. Do not invent clients, results, course credentials, locations, product features, testimonials, or business statistics.
- Prioritize useful pages for real search intent. Do not create near-duplicate doorway pages or repeat keywords unnaturally.
- Preserve current URLs where possible. If URL changes are needed, add and verify permanent redirects.
- Make the plan's language and geographic targeting explicit before writing new SEO copy.
- Measure rankings and organic traffic; do not treat structured data or metadata as a ranking guarantee.

## 1. Create crawlable Arabic and English pages

### Actions

1. Use one bilingual URL pattern. Keep existing English content URLs and add an `/ar/` counterpart for each translated page. Keep the requested Arabic homepage at `/` and serve its English counterpart at `/en/`, for example:
   - Arabic homepage: `/`
   - English homepage: `/en/`
   - English Academy: `/academy`
   - Arabic Academy: `/ar/academy`
2. Confirm route support in the Cloudflare Worker and asset routing. Ensure direct requests to every language URL return the correct page with HTTP 200, including clean routes without `.html`.
3. Give every language version its own static, crawlable HTML content:
   - Correct `<html lang>` and `dir` attributes.
   - Localized title, meta description, H1, body copy, navigation labels, image alt text, and relevant link text.
   - Correct canonical URL pointing to that language's own URL.
   - Reciprocal `hreflang="en"` and `hreflang="ar"` links; add `x-default` only if a real default destination is defined.
4. Ensure the initial HTML response already contains the correct language's text and metadata. Keep JavaScript language switching as a convenience, not as the only way to expose either language to crawlers.
5. Link each language switch to the equivalent page in the other language, not always to the homepage. Preserve the current page where a translated counterpart exists.
6. Update internal navigation, product/service cards, footer links, and cross-page links so they stay within the selected language.
7. Update `sitemap.xml` to list only canonical, indexable language URLs. Do not include redirects, duplicate URLs, or query-string variants.
8. For any retired or changed URL, add a one-hop permanent redirect to the closest equivalent page. Do not redirect every retired URL to the homepage.

### Acceptance criteria

- Each English and Arabic page loads directly and has matching language, direction, copy, title, description, canonical, and links.
- Each localized pair has reciprocal `hreflang` declarations and self-canonical URLs.
- Crawling the initial HTML without executing JavaScript reveals the correct localized content.
- No sitemap URL redirects, returns an error, or canonicalizes to a different URL.
- Language switching preserves the page topic and does not create duplicate or circular routes.

## 2. Target specific search intent with focused pages

### Actions

1. Establish a keyword and search-intent map before creating or rewriting pages:
   - Review Google Search Console data after access is available.
   - Research English and Arabic variants, local phrasing, and search intent using Google Keyword Planner or another approved source.
   - Review search results for Egypt/Cairo to see what page types and topics rank. Record the source, date, target language, country, and intent for each term.
2. Start with a manageable set of commercially relevant topics:
   - AI/software: AI automation and custom AI software services for businesses in Egypt.
   - Academy: AI courses and workshops in Cairo/Egypt, split by audience only when ZAKAA has distinct, substantive offerings.
   - ERP360: ERP software for retail, restaurants, and service businesses in Egypt, based only on supported product capabilities.
3. Map one primary intent to each existing page where possible. Create a new page only when it serves a distinct query and has enough unique information to help the reader.
4. For every target page, write:
   - A unique, descriptive title and meta description in that page's language.
   - One clear H1 matching the page's actual offering.
   - Useful details on audience, problems solved, capabilities, delivery, service area, and a relevant contact or next step.
   - Descriptive section headings, concise FAQs based on real customer questions, and links to related offerings.
5. Keep English and Arabic content natural and culturally appropriate. Do not rely on literal translation when search intent differs by language.
6. Add internal links from the homepage, service/product listings, academy, and relevant case studies. Use descriptive anchor text without over-optimizing it.
7. Review copy with the people responsible for AI services, ERP360, and training before publishing. Label concept previews accurately and distinguish available products from illustrative concepts.

### Acceptance criteria

- Each target page has one documented primary intent, a distinct title/H1, and substantive original content.
- No pages differ only by a city or keyword substitution.
- Product and training descriptions match what ZAKAA can currently provide.
- Each target page has useful internal links and a clear, relevant contact path.
- Keyword usage reads naturally in both languages.

## 3. Add trustworthy proof and accurate structured data

### Actions

1. Inventory approved evidence ZAKAA can publish:
   - Completed projects and client references with written permission.
   - Verifiable outcomes, including how each metric was calculated and the period measured.
   - Testimonials with attribution approved by the person or organization.
   - Current team, instructor, and company credentials.
2. Create case studies for suitable projects. Each should explain the client's context, problem, ZAKAA's contribution, solution, and verified outcome. Anonymize details only with client approval and do not imply an unidentified client is a named reference.
3. Expand academy information for actual courses or workshops: audience, prerequisites, learning outcomes, syllabus, duration, format, location or delivery method, instructor, schedule, and enrollment details. Publish only details that are confirmed and current.
4. Make company identity and contact information consistent across the site: preferred brand name, legal/business name where appropriate, phone, email, service area, and any public business address.
5. Review current JSON-LD on every indexable page:
   - Use a consistent `Organization` entity with a stable `@id`, canonical URL, logo, and verified contact details.
   - Add `sameAs` only for official social profiles.
   - Connect pages to the organization using `publisher` or `about` where relevant.
   - Add `Course` or event-related structured data only when the page describes a real, current course or event and all required facts are visible to users.
   - Do not add review/rating markup for self-serving testimonials or claim rich-result eligibility without validation.
6. Validate structured data with Google's Rich Results Test where applicable and Schema.org Validator. Fix errors and warnings that affect eligibility; keep visible page content consistent with the markup.

### Acceptance criteria

- Published proof is accurate, attributable or properly approved, and supported by records.
- Every page's structured data describes visible page content and uses the canonical URL.
- No fabricated or unsupported organization, course, event, review, rating, or outcome data appears.
- Structured data validates without critical errors.

## 4. Set up measurement and indexing workflows

### Actions

1. Verify the domain property `zakaa-ai.net` in Google Search Console. Use an account controlled by ZAKAA and retain at least two authorized owners/admins.
2. Add and verify the site in Bing Webmaster Tools. Consider importing verified Search Console data if available.
3. Submit the production sitemap in both tools after URL and language work is deployed.
4. Inspect the homepage and representative English/Arabic pages with URL Inspection:
   - Confirm crawl access, selected canonical, rendered content, and indexing eligibility.
   - Request indexing for important new or corrected pages when appropriate.
5. Review Search Console's indexing and sitemap reports weekly during rollout, then monthly. Resolve blocked pages, unexpected `noindex`, duplicate canonicals, redirect chains, and crawl errors.
6. Record a 28-day baseline for impressions, clicks, CTR, average position, landing pages, and queries. Segment by country, language URL, brand/non-brand intent, and target page where the tools allow it.
7. Review results monthly. Improve pages with impressions but weak CTR, pages ranking for the wrong intent, and pages with traffic but poor engagement or contact conversion.
8. Configure privacy-compliant analytics and conversion events for meaningful actions such as form submissions, qualified calls, WhatsApp clicks, and course inquiries. Do not count page views as leads.
9. Keep an SEO change log with deployment date, affected URLs, and observed outcomes so changes can be compared over time.

### Acceptance criteria

- Google Search Console and Bing Webmaster Tools show verified ownership and an accepted sitemap.
- Priority pages are crawlable, have the intended canonical, and are eligible for indexing.
- A baseline and recurring report exist; conversions are tracked without exposing personal data.
- Indexing and ranking claims are based on tool data, not assumptions.

## 5. Strengthen local discovery and business citations

### Actions

1. Confirm whether ZAKAA meets Google's current Business Profile eligibility rules. Create or claim a profile only for a real eligible business with accurate customer contact or service-area details.
2. Complete an eligible profile with the verified business name, category, phone, website, service area or address, hours, and description. Keep information current and consistent with the website.
3. If the business does not qualify for a public profile, do not create one to target a location. Use accurate service-area details on the site and pursue appropriate industry listings instead.
4. Identify reputable, relevant Egyptian business, technology, education, and partner directories. Add or correct listings only where ZAKAA has a legitimate presence. Avoid bulk low-quality directory submissions.
5. Use one agreed format for the business name, address (if public), and phone number across the website and approved listings. Audit and correct old or conflicting records.
6. Add location-specific content only where ZAKAA genuinely serves customers and can provide useful local details. Do not publish thin city pages.
7. Ask real clients and course participants for honest feedback through permitted channels. Do not offer incentives for positive reviews, filter out negative feedback, or publish reviews without permission.
8. Track profile views, direction requests where applicable, calls, website clicks, qualified inquiries, and referral traffic. Respond to reviews professionally and protect customer privacy.

### Acceptance criteria

- Any Business Profile is eligible, verified, accurate, and managed by ZAKAA.
- Business details are consistent across the site and selected legitimate listings.
- Location pages describe real service coverage and contain useful, unique information.
- Reviews and testimonials are authentic, permissioned, and handled under platform policies.

## Rollout order

1. Collect access and facts: Search Console, analytics, business details, service coverage, and approved case-study/course evidence.
2. Confirm bilingual URL strategy and routes.
3. Build localized crawlable pages, canonical and `hreflang` tags, redirects, internal links, and sitemap updates.
4. Research queries and improve the priority AI, Academy, and ERP360 pages.
5. Publish verified proof and appropriate structured data.
6. Set up webmaster tools, analytics, local listings where eligible, and recurring reporting.
7. Run the pre-release checks below, deploy, then monitor indexing and performance.

## Pre-release checks

- All canonical URLs return HTTP 200 and use HTTPS.
- `robots.txt` permits intended pages and references the current sitemap.
- Sitemap contains only canonical, indexable URLs and valid language variants.
- Each page has a unique title, description, H1, canonical, and correct language/direction.
- `hreflang` links are reciprocal and point to equivalent pages.
- No important content depends on JavaScript to appear in the initial HTML.
- No unintended `noindex`, duplicate pages, broken internal links, redirect loops, or redirect chains exist.
- Structured data matches visible content and passes validation.
- Pages work on mobile and have no critical accessibility or Core Web Vitals issues.
- Forms, phone links, email links, and inquiry tracking work.

## Dependencies and open decisions

- Access to Google Search Console, Bing Webmaster Tools, and analytics is required to assess real indexing, queries, and rankings.
- ZAKAA must confirm the preferred Arabic and English URL structure before any route changes.
- ZAKAA must confirm actual service areas, business-profile eligibility, current courses, product capabilities, and evidence it has permission to publish.
- Keyword priorities and content scope should be finalized from research and business goals before writing new landing pages.
