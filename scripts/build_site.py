"""Generate static bilingual marketing pages: python scripts/build_site.py."""
from pathlib import Path
import re, json, html, urllib.parse

R = Path(__file__).resolve().parents[1]
esc = lambda s: html.escape(str(s), quote=True)

def t(en, ar, tag='span', cls=''):
    return f'<{tag} class="{cls}" data-en="{esc(en)}" data-ar="{esc(ar)}">{esc(en)}</{tag}>'

def link(url, en, ar, cls='text-link'):
    return f'<a class="{cls}" href="{url}">' + t(en, ar) + '</a>'

def item(slug, name, arname, group, visual, en, ar, points, status=None):
    return dict(slug=slug, name=name, arname=arname, group=group, visual=visual, en=en, ar=ar, points=points, status=status)

items = [
    item('erp360', 'ERP360', 'ERP360', 'products', 'erp', 'Sales, inventory and accounting in one connected operation.', 'المبيعات والمخزون والمحاسبة ضمن منظومة تشغيل واحدة.', [
        ('For retail, restaurants and service businesses.', 'لشركات التجزئة والمطاعم والأعمال الخدمية.'),
        ('Connect POS, purchasing, inventory movements, accounting and customer relationships.', 'ربط نقاط البيع والمشتريات وحركة المخزون والمحاسبة وعلاقات العملاء.'),
        ('Configure existing modules or scope new modules around your requirements.', 'تهيئة الوحدات الحالية أو تطوير وحدات إضافية وفق احتياجاتك.')
    ]),
    item('worktracker', 'WorkTracker', 'WorkTracker', 'products', 'work', 'Understand work patterns with workforce analytics and an administration dashboard.', 'فهم أنماط العمل من خلال تحليلات فرق العمل ولوحة الإدارة.', [
        ('A Windows activity agent connected to a central administration dashboard.', 'تطبيق لمتابعة النشاط على ويندوز مرتبط بلوحة إدارة مركزية.'),
        ('Explore application usage and work patterns; organize devices and access roles.', 'استعراض استخدام التطبيقات وأنماط العمل وتنظيم الأجهزة والصلاحيات.'),
        ('Agree visibility, access and deployment scope with your team before rollout.', 'تحديد نطاق الرؤية والصلاحيات والتشغيل مع فريقك قبل التطبيق.')
    ]),
    item('yourspace', 'YourSpace', 'YourSpace', 'products', 'space', 'Manage spaces, packages and subscriptions for institutes and service businesses.', 'إدارة المساحات والباقات والاشتراكات للمعاهد والأعمال الخدمية.', [
        ('Organize customers, spaces and service packages in one workspace.', 'تنظيم العملاء والمساحات وباقات الخدمات في مساحة عمل واحدة.'),
        ('Manage pricing rules, jobs and subscriptions.', 'إدارة قواعد التسعير والمهام والاشتراكات.'),
        ('Administration tools and Excel exports support everyday operations.', 'أدوات إدارة وتصدير إلى Excel لدعم التشغيل اليومي.')
    ]),
    item('gathering', 'Gathering', 'Gathering', 'products', 'event', 'Organize Arabic event journeys from registration to attendance and prize draws.', 'تنظيم تجربة الفعاليات بالعربية من التسجيل إلى الحضور وسحب الجوائز.', [
        ('Collect RSVPs and import guest lists from Excel.', 'جمع تأكيدات الحضور واستيراد قوائم الضيوف من Excel.'),
        ('Track attendance and event demographics.', 'متابعة الحضور والإحصاءات الخاصة بالفعالية.'),
        ('Manage event branding, prizes and draws.', 'إدارة هوية الفعالية والجوائز والسحوبات.')
    ]),
    item('madinaty-ai', 'Madinaty AI', 'مبادرة مدينتي AI', 'initiatives', 'community', 'A community initiative connecting residents, local businesses and services in residential communities.', 'مبادرة لخدمة المجتمعات العمرانية والسكنية تربط السكان بالأعمال والخدمات المحلية.', [
        ('A shared community experience for discovering places, services and local businesses.', 'تجربة مجتمعية موحدة لاكتشاف الأماكن والخدمات والأعمال المحلية.'),
        ('Life Portal, Kitchen Portal, Express Portal and the administration console sit within this ecosystem.', 'تندرج بوابات الحياة والمطابخ والتوصيل ولوحة الإدارة ضمن هذه المنظومة.'),
        ('Discuss how a connected community experience could serve your residential development.', 'ناقشنا في كيفية توظيف تجربة مجتمعية متكاملة لخدمة مجتمعك السكني.')
    ]),
    item('autostop', 'AutoStop', 'AutoStop', 'initiatives', 'ride', 'Community carpool coordination for residents sharing planned journeys.', 'تنسيق مشاركة الرحلات بين السكان أصحاب المسارات المتقاربة.', [
        ('Offer planned routes and seats in advance.', 'مشاركة المسارات والمقاعد المتاحة مسبقًا.'),
        ('Connect drivers and passengers within residential communities.', 'التنسيق بين السائقين والركاب في المجتمعات السكنية.'),
        ('Support shared community transit patterns.', 'دعم أنماط التنقل المشترك داخل المجتمع.')
    ]),
    item('loqma', 'Loqma · Home Kitchen', 'لقمة · Home Kitchen', 'initiatives', 'kitchen', 'A home-kitchen initiative connecting community life with home-cooked food.', 'مبادرة للمطابخ المنزلية تربط الحياة المجتمعية بالطعام المنزلي.', [
        ('Connect home kitchens with nearby residents.', 'ربط المطابخ المنزلية بسكان الحي القريبين.'),
        ('Support discovery, menus and direct coordination.', 'دعم استعراض القوائم والطلب والتنسيق المباشر.'),
        ('Encourage neighborhood community exchange.', 'تشجيع التبادل والترابط داخل المجتمعات السكنية.')
    ]),
    item('souk-el-kanto', 'Souk El-Kanto', 'سوق الكانتو', 'projects', 'shops', 'A modern platform for second-hand items, vintage fashion and unique finds.', 'منصة حديثة للمنتجات المستعملة والأزياء الكلاسيكية والقطع النادرة.', [
        ('Verified listings and clear item conditions.', 'عروض موثوقة ووصف واضح لحالة كل منتج.'),
        ('Search and discover across categories.', 'بحث وتصفح سلس في مختلف الأقسام.'),
        ('Support circular economy and sustainable reuse.', 'دعم الاقتصاد الدائري وإعادة استخدام المقتنيات.')
    ], status=('Beta', 'تجريبي')),
    item('masar', 'Masar EV', 'مسار للمركبات الكهربائية', 'projects', 'ev', 'A dedicated directory for electric-vehicle charging points and mobility services in Egypt.', 'دليل متكامل لنقاط شحن المركبات الكهربائية وخدمات التنقل في مصر.', [
        ('Find verified charging stations with socket types and operational status.', 'البحث عن محطات الشحن المعتمدة مع توضيح أنواع المقابس وحالة العمل.'),
        ('Filter by route, speed and network provider.', 'تصفية المحطات حسب المسار وسرعة الشحن ومقدم الخدمة.'),
        ('Contribute updates and new locations to support green mobility.', 'المساهمة في تحديث البيانات وإضافة مواقع جديدة لدعم النقل الأخضر.')
    ], status=('In development', 'قيد التطوير')),
    item('eduflow', 'EduFlow', 'EduFlow', 'projects', 'school', 'A modern school-management and student-journey platform built for bilingual schools in the MENA region.', 'نظام حديث لإدارة المدارس ومتابعة مسار الطلاب مصمم للمدارس ثنائية اللغة في المنطقة.', [
        ('Admissions, student records, attendance and academic gradebooks in one interface.', 'إدارة القبول وسجلات الطلاب والحضور والدرجات في واجهة واحدة.'),
        ('Parent and student web portals for transparent progress and communication.', 'بوابات أولياء الأمور والطلاب لمتابعة التحصيل الدراسي والتواصل المستمر.'),
        ('Automated timetable generation and Ministry-compliant reporting.', 'إنشاء الجداول الدراسية آليًا مع دعم تقارير المناهج والوزارة.')
    ], status=('In development', 'قيد التطوير')),
]

services = [
    item('ai-software', 'AI & Intelligent Software', 'الذكاء الاصطناعي والبرمجيات الذكية', 'services', 'intelligence', 'Custom AI models, process automation and intelligent software tailored to your workflows.', 'نماذج ذكاء اصطناعي مخصصة وأتمتة العمليات وبرمجيات ذكية تناسب طريقة عملك.', [
        ('Model integration: LLMs, document understanding, search and semantic recommendations.', 'دمج النماذج: النماذج اللغوية وفهم المستندات والبحث والتوصيات الذكية.'),
        ('Custom applications, customer-facing workflows and operational reporting.', 'تطبيقات مخصصة ومسارات خدمة العملاء وتقارير التشغيل.'),
        ('Start with one clear use case, agreed scope and measurable outcomes.', 'البداية بحالة استخدام واضحة ونطاق متفق عليه ونتائج قابلة للقياس.')
    ]),
    item('websites-ecommerce', 'Websites & E-commerce', 'تصميم المواقع والمتاجر الإلكترونية', 'services', 'shops', 'Business websites, online shops and digital storefronts designed around your brand.', 'مواقع الشركات والمتاجر الإلكترونية والواجهات التجارية المصممة حول هوية نشاطك.', [
        ('Corporate websites, service websites and campaign landing pages.', 'مواقع الشركات والخدمات وصفحات الحملات التعريفية.'),
        ('Product catalogues, shop interfaces and customer ordering journeys.', 'كتالوجات المنتجات وواجهات المتاجر ومسارات طلب العملاء.'),
        ('Responsive Arabic and English experiences, with integrations scoped to your needs.', 'تجارب متجاوبة بالعربية والإنجليزية مع تحديد التكاملات حسب احتياجك.')
    ]),
    item('consulting', 'Business Resilience Consulting', 'استشارات الأعمال والمرونة المؤسسية', 'services', 'resilience', 'Improve operations and prepare your organization for disruption.', 'تحسين العمليات وتجهيز مؤسستك للتعامل مع الاضطرابات.', [
        ('Business and operations improvement: review workflows and identify bottlenecks.', 'تحسين الأعمال والتشغيل عبر مراجعة خطوات العمل وتحديد نقاط التعطيل.'),
        ('Crisis management: response scenarios, responsibilities and communication.', 'إدارة الأزمات: سيناريوهات الاستجابة والمسؤوليات والتواصل.'),
        ('Business continuity: critical activities, recovery priorities and exercises.', 'استمرارية الأعمال: الأنشطة الحيوية وأولويات التعافي والتمارين.')
    ]),
]

academy_card = item('academy', 'Academy & Learning Experiences', 'الأكاديمية وتجارب التعلم', 'services', 'learning', 'AI and programming workshops for educators, youth and corporate teams in Cairo.', 'الذكاء الاصطناعي والبرمجة للمحاضرين والأطفال والشباب وفرق العمل في القاهرة.', [
    ('AI workshops for educators: lesson planning and practical AI tools.', 'ورش الذكاء الاصطناعي للمحاضرين: تخطيط الدروس والتدريس بالذكاء الاصطناعي.'),
    ('Youth & children: creative coding and computational thinking.', 'الأطفال والشباب: البرمجة الإبداعية والتفكير المنطقي.'),
    ('Executive training & corporate continuity simulations.', 'التدريب التنفيذي ومحاكاة استمرارية الأعمال للشركات.')
])

byid = {x['slug']: x for x in items + services + [academy_card]}
navs = [
    ('/', 'Home', 'الرئيسية'),
    ('/about', 'About us', 'من نحن'),
    ('/services', 'Services', 'الخدمات'),
    ('/products', 'Products', 'المنتجات'),
    ('/academy', 'Academy', 'الأكاديمية'),
    ('/initiatives', 'Initiatives', 'المبادرات'),
    ('/projects', 'Projects', 'المشاريع')
]

brand = '<a class="brand" href="/" aria-label="Zaka2 home"><span class="brand-art" aria-hidden="true"><svg class="wordmark wordmark-en" viewBox="190 598 680 260"><image href="/assets/brand-original.webp" width="1050" height="1050"/></svg><svg class="wordmark wordmark-ar" viewBox="190 178 680 422"><image href="/assets/brand-original.webp" width="1050" height="1050"/></svg></span></a>'
header = '<header class="header"><nav class="nav wrap" aria-label="Main navigation">' + brand + '<div class="navlinks" id="navlinks">' + ''.join(link(*n, cls='') for n in navs) + '</div><div class="nav-actions"><button class="theme-toggle" id="theme-toggle" type="button" aria-label="Switch theme">☾</button><button class="lang" id="lang-toggle" type="button">عربي</button>' + link('/#contact', 'Let’s talk ↗', 'لنتحدث ↗', 'nav-cta') + '<button class="menu" id="menu-toggle" type="button" aria-label="Open menu" aria-controls="navlinks" aria-expanded="false">☰</button></div></nav></header>'
contact = '<section class="contact-band" id="contact"><div class="wrap contact-inner"><div>' + t('LET’S START WITH YOUR NEXT STEP', 'لنبدأ بخطوتك القادمة', 'p', 'eyebrow') + t('What would you like to build?', 'ماذا تريد أن تبني؟', 'h2') + t('A product, a team capability or a stronger community. Tell us what you have in mind.', 'منتج أو مهارة لفريقك أو مجتمع أكثر ترابطًا. أخبرنا بما تفكر فيه.', 'p') + '</div><div class="contact-links">' + link('https://wa.me/201026655008', 'Talk on WhatsApp ↗', 'تواصل عبر واتساب ↗', 'btn') + '<a dir="ltr" href="tel:+201026655008">+20 102 665 5008</a><a href="mailto:Hello@Zakaa-AI.net">Hello@Zakaa-AI.net</a></div></div></section>'
footer = '<footer class="site-footer"><div class="wrap"><div class="footer-links">' + brand + link('/about', 'About Zaka2', 'عن ذكاء') + link('/services', 'Services', 'الخدمات') + link('/academy', 'Learning experiences', 'تجارب التعلم') + '<a href="mailto:Support@Zakaa-AI.net">Support@Zakaa-AI.net</a></div>' + '<p>© <span id="year"></span> Zaka2 · ' + t('Intelligence by design.', 'ذكاء يصنع الفرق.') + '</p></div></footer>'
chat = '<button class="assistant-link" id="zakaa-chat-toggle" type="button" aria-haspopup="dialog" aria-controls="zakaa-chat-panel" aria-expanded="false"><span>Ask Zaka2</span></button>'
pages = []

def page(slug, title, artitle, description, ardescription, body):
    head = (R / 'scripts/head-template.html').read_text(encoding='utf-8')
    head = re.sub(r'<title>.*?</title>', f'<title>{esc(title)} | Zaka2</title>', head)
    for attr in ['name="description" id="meta-description"', 'property="og:title"', 'name="twitter:title"', 'property="og:description"', 'name="twitter:description"', 'property="og:url"']:
        value = (title + ' | Zaka2') if 'title' in attr else ('https://zakaa-ai.net/' + slug if 'og:url' in attr else description)
        head = re.sub(r'<meta ' + re.escape(attr) + r' content="[^"]*">', f'<meta {attr} content="{esc(value)}">', head)
    head = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="https://zakaa-ai.net/{slug}">', head)
    schema = {
        '@context': 'https://schema.org',
        '@type': 'WebPage',
        'name': title,
        'description': description,
        'url': 'https://zakaa-ai.net/' + slug,
        'isPartOf': {'@type': 'WebSite', 'name': 'Zaka2', 'url': 'https://zakaa-ai.net/'},
        'publisher': {'@type': 'Organization', 'name': 'Zaka2 / ذكاء', 'url': 'https://zakaa-ai.net/', 'telephone': '+201026655008', 'logo': 'https://zakaa-ai.net/assets/brand-original.webp'}
    }
    text = head + '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False) + '</script></head><body class="catalog-site" data-title-en="' + esc(title) + '" data-title-ar="' + esc(artitle) + '" data-description-en="' + esc(description) + '" data-description-ar="' + esc(ardescription) + '"><a class="skip" href="#main">' + t('Skip to content', 'تجاوز إلى المحتوى') + '</a>' + header + '<main id="main">' + body + contact + '</main>' + footer + chat + '<script src="/assets/restored-copy.js" defer></script><script src="/assets/site.js" defer></script><script src="/assets/motion.js" defer></script><script src="/assets/theme-toggle.js" defer></script><script src="/assets/chat.js" defer></script></body></html>'
    (R / (slug + '.html' if slug else 'index.html')).write_text(text, encoding='utf-8')
    pages.append(slug)

def intro(label, arlabel, title, artitle, desc, ardesc):
    return '<section class="page-intro wrap">' + t(label, arlabel, 'p', 'eyebrow') + t(title, artitle, 'h1') + t(desc, ardesc, 'p', 'lead') + '</section>'

def card(x, compact=False):
    status = t(*x['status'], 'span', 'status') if x.get('status') else ''
    media = '' if compact else f'<img src="/assets/illustrations/{x["visual"]}.svg" alt="" width="640" height="400" loading="lazy">'
    return f'<article class="catalog-card" data-slug="{x["slug"]}">' + media + '<div class="card-body">' + status + t(x['name'], x['arname'], 'h3') + t(x['en'], x['ar'], 'p') + link('/' + x['slug'], 'Explore ' + x['name'] + ' ↗', 'اكتشف ' + x['arname'] + ' ↗') + '</div></article>'

def grid(xs, compact=False):
    return '<div class="catalog-grid">' + ''.join(card(x, compact) for x in xs) + '</div>'

def block(title, artitle, desc, ardesc, content):
    return '<section class="catalog-section wrap"><div class="section-heading">' + t(title, artitle, 'h2') + t(desc, ardesc, 'p') + '</div>' + content + '</section>'

def bento_card(x):
    status = t(*x['status'], 'span', 'status') if x.get('status') else ''
    badge_map = {
        'products': ('ENTERPRISE PRODUCT', 'منتج مؤسسي'),
        'services': ('ENGINEERING SERVICE', 'خدمة هندسية'),
        'initiatives': ('COMMUNITY INITIATIVE', 'مبادرة مجتمعية'),
        'projects': ('DEVELOPMENT PIPELINE', 'مشروع قيد التطوير')
    }
    b_en, b_ar = badge_map.get(x['group'], ('CAPABILITY', 'حل تقني'))
    badge = t(b_en, b_ar, 'span', 'bento-badge')
    media = f'<div class="bento-card-media"><img src="/assets/illustrations/{x["visual"]}.svg" alt="" width="640" height="400" loading="lazy"></div>'
    encoded_name = urllib.parse.quote(x['name'])
    return f'''<article class="bento-card" data-group="{x['group']}" data-slug="{x['slug']}">
      {media}
      <div class="card-body">
        {status}{badge}
        {t(x['name'], x['arname'], 'h3')}
        {t(x['en'], x['ar'], 'p')}
        <div class="bento-card-actions">
          {link('/' + x['slug'], 'Explore ' + x['name'] + ' ↗', 'اكتشف ' + x['arname'] + ' ↗')}
          <a class="text-link" href="https://wa.me/201026655008?text=Hello%20Zaka2,%20I%20would%20like%20to%20discuss%20{encoded_name}" target="_blank" rel="noopener">
            {t('Consult ↗', 'استشر ↗')}
          </a>
        </div>
      </div>
    </article>'''

# ==============================================================================
# HOMEPAGE GENERATION: HERO + INTERACTIVE BENTO SWITCHER
# ==============================================================================
hero = (R / 'scripts/hero-template.html').read_text(encoding='utf-8')

bento_section = f'''<section class="bento-switcher-section wrap" id="solutions">
  <div class="bento-header">
    <div class="section-heading">
      {t('THE INTELLIGENCE ECOSYSTEM', 'منظومة الحلول المتكاملة', 'p', 'eyebrow')}
      {t('One Unified Architecture.', 'منظومة ذكاء متصلة ومتكاملة.', 'h2')}
      {t('Filter seamlessly between operational software products, custom engineering services, and community initiatives.', 'تنقل بسلاسة بين منتجاتنا التشغيلية، وخدماتنا الهندسية المخصصة، ومبادراتنا المجتمعية.', 'p')}
    </div>
    <div class="bento-nav-wrap">
      <div class="bento-nav" role="tablist" aria-label="Solution Categories">
        <button class="bento-tab active" type="button" data-filter="all">
          <span aria-hidden="true">✦</span> {t('All Capabilities', 'جميع الحلول')}
        </button>
        <button class="bento-tab" type="button" data-filter="products">
          <span aria-hidden="true">❖</span> {t('Products', 'المنتجات')}
        </button>
        <button class="bento-tab" type="button" data-filter="services">
          <span aria-hidden="true">☥</span> {t('Services', 'الخدمات')}
        </button>
        <button class="bento-tab" type="button" data-filter="initiatives">
          <span aria-hidden="true">◉</span> {t('Initiatives', 'المبادرات')}
        </button>
      </div>
      <div class="bento-metrics-pill">
        {t('4 PRODUCTS · 4 SERVICES · 3 INITIATIVES', '٤ منتجات · ٤ خدمات · ٣ مبادرات')}
      </div>
    </div>
  </div>
  <div class="bento-grid">
    {''.join(bento_card(x) for x in ([x for x in items if x['group'] == 'products'] + services + [academy_card] + [x for x in items if x['group'] == 'initiatives']))}
  </div>
</section>'''

methodology_block = block(
    'Understand. Design. Deliver.', 'نفهم. نصمم. ننفذ.',
    'A clear engineering path from an idea to practical enterprise execution.', 'مسار هندسي واضح من الفكرة إلى التنفيذ العملي المستدام.',
    '<div class="steps">' + ''.join('<div>' + t(a, b, 'h3') + t(c, d, 'p') + '</div>' for a, b, c, d in [
        ('01 / Understand', '٠١ / نفهم', 'Your goals, people and operational workflows.', 'أهدافك وفريقك وخطوات العمل الحالية.'),
        ('02 / Design', '٠٢ / نصمم', 'Agree the cognitive scope and the right software architecture.', 'نتفق على النطاق المعرفي والمعمارية البرمجية المناسبة.'),
        ('03 / Deliver', '٠٣ / ننفذ', 'Build, test, deploy and iterate together.', 'نبني ونختبر وننشر ونحسّن معًا.')
    ]) + '</div>'
)

home_body = hero + bento_section + methodology_block
page('', 'AI, Software & Learning', 'الذكاء الاصطناعي والبرمجيات والتعلم', 'Zaka2: AI and software services, ERP360, WorkTracker, YourSpace, Gathering and programming training in Cairo.', 'ذكاء: خدمات الذكاء الاصطناعي والبرمجيات ومنتجات ERP360 وWorkTracker وYourSpace وGathering وتدريب البرمجة في القاهرة.', home_body)

# ==============================================================================
# ABOUT PAGE GENERATION: ALEXANDRIAN ASTROLABE CENTERPIECE
# ==============================================================================
about_hero = f'''<section class="page-intro about-hero wrap">
  <div class="about-hero-copy">
    {t('HERITAGE × COGNITION', 'أصالة الحضارة × عبقرية المستقبل', 'p', 'eyebrow')}
    {t('The Architecture of Intelligence.', 'هندسة الذكاء والريادة.', 'h1')}
    {t('Where 5,000 years of civilization meet modern neural computation. We build software shaped around people, purpose, and lasting operational excellence.', 'حيث تلتقي ٥٠٠٠ سنة من العراقة والعلوم بحوسبة الذكاء الاصطناعي. نبني برمجيات تصنع الفرق الحقيقي وتبسط الأعمال.', 'p', 'lead')}
    <div class="about-badges">
      {t('CAIRO // 30.0444° N, 31.2357° E', 'القاهرة // ٣٠.٠٤٤٤° ش، ٣١.٢٣٥٧° ق', 'span', 'about-badge')}
      {t('HERITAGE-ROOTED AI', 'ذكاء متجذر في الأصالة', 'span', 'about-badge')}
      {t('ENTERPRISE SYSTEMS', 'منظومات مؤسسية متكاملة', 'span', 'about-badge')}
    </div>
  </div>
  <div class="about-hero-stage" aria-label="Alexandrian Astrolabe of Cognition">
    <div class="astrolabe-mechanism">
      <div class="astrolabe-limb"></div>
      <div class="astrolabe-khatam"></div>
      <div class="astrolabe-cardinal north" data-en="NORTH // شَمَال" data-ar="شَمَال">شَمَال</div>
      <div class="astrolabe-cardinal east" data-en="EAST // مَشْرِق" data-ar="مَشْرِق">مَشْرِق</div>
      <div class="astrolabe-cardinal south" data-en="SOUTH // جَنُوب" data-ar="جَنُوب">جَنُوب</div>
      <div class="astrolabe-cardinal west" data-en="WEST // مَغْرِب" data-ar="مَغْرِب">مَغْرِب</div>
      <div class="astrolabe-core">
        <div class="solar-pulse"></div>
        <div class="core-glyph">
          <svg viewBox="0 0 100 100" fill="none" stroke="#E5B25D" stroke-width="1.8">
            <circle cx="50" cy="50" r="14" fill="#E5B25D" fill-opacity="0.3"/>
            <circle cx="50" cy="50" r="30" stroke-dasharray="3 3"/>
            <polygon points="50,26 56,44 74,50 56,56 50,74 44,56 26,50 44,44" fill="#E5B25D"/>
          </svg>
        </div>
      </div>
      <div class="hiero-orbit-marker ankh" title="Ankh ☥"></div>
      <div class="hiero-orbit-marker wadjet" title="Wadjet 𓂀"></div>
      <div class="hiero-orbit-marker djed" title="Djed 𓊽"></div>
    </div>
  </div>
</section>'''

page('about', 'About Zaka2', 'عن ذكاء', 'Our purpose, vision, mission and approach.', 'من نحن ورؤيتنا ورسالتنا ولماذا تختار ذكاء.', about_hero + (R / 'scripts/about-template.html').read_text(encoding='utf-8'))

# ==============================================================================
# REDESIGNED /PRODUCTS HUB: COMMAND CENTER & SPECIFICATION MATRIX
# ==============================================================================
products_hero = intro(
    'ENTERPRISE PRODUCT SUITE', 'منظومة المنتجات البرمجية',
    'Engineered for Scale. Designed for Simplicity.', 'برمجيات تشغيلية متقدمة مبنية لنمو أعمالك.',
    'Four dedicated software systems for retail operations, workforce performance, physical spaces, and Arabic event journeys.',
    'أربعة أنظمة متخصصة لإدارة العمليات والمبيعات، وتحليلات فرق العمل، وإدارة المساحات والاشتراكات، وتنظيم الفعاليات بالعربية.'
)

product_cards_bento = f'''<section class="catalog-section wrap">
  <div class="section-heading">
    {t('FLAGSHIP SOFTWARE ENGINES', 'الأنظمة البرمجية الرائدة', 'h2')}
    {t('Purpose-built platforms ready for custom configuration and enterprise deployment.', 'منصات مصممة ومختبرة بعناية، جاهزة للتهيئة والتطبيق المؤسسي المباشر.', 'p')}
  </div>
  <div class="hub-grid-2">
    <div class="spec-box" data-slug="erp360">
      <span class="bento-badge">{t('RETAIL & SERVICE ERP', 'إدارة العمليات والتجزئة')}</span>
      <h3>ERP360</h3>
      <p>{t('Sales, inventory and multi-branch accounting in one cohesive system. Connect POS, purchasing, and real-time inventory movements.', 'المبيعات والمخزون والمحاسبة متعددة الفروع ضمن منظومة واحدة مع ربط نقاط البيع والمشتريات وحركة المخزون الفورية.')}</p>
      <ul class="spec-list">
        <li>{t('Point of Sale (POS) with offline sync & barcode scanning', 'نقاط بيع متقدمة تعمل دون اتصال مع قراءة الباركود')}</li>
        <li>{t('Multi-warehouse inventory tracking & minimum stock alerts', 'متابعة حركة المخزون عبر عدة مستودعات وتنبيهات النواقص')}</li>
        <li>{t('Electronic invoicing, tax compliance, and automated profit reports', 'الفواتير الإلكترونية والضرائب وتقارير الأرباح التلقائية')}</li>
        <li>{t('Cloud SaaS or On-Premise Air-Gapped deployment', 'متاح كخدمة سحابية أو تثبيت محلي مؤمن على خوادمك')}</li>
      </ul>
      {link('/erp360', 'View ERP360 Technical Specs ↗', 'المواصفات الفنية لـ ERP360 ↗', 'btn')}
    </div>

    <div class="spec-box" data-slug="worktracker">
      <span class="bento-badge">{t('WORKFORCE ANALYTICS', 'تحليلات فرق العمل')}</span>
      <h3>WorkTracker</h3>
      <p>{t('Understand work patterns with privacy-conscious workforce telemetry and a central administrative dashboard.', 'فهم أنماط العمل من خلال تحليلات دقيقة تحافظ على الخصوصية ولوحة تحكم إدارية مركزية.')}</p>
      <ul class="spec-list">
        <li>{t('Lightweight Windows activity agent with low resource footprint', 'تطبيق خفيف على ويندوز لا يستهلك موارد الجهاز')}</li>
        <li>{t('Visual analytics on application utilization and active hours', 'رسوم بيانية توضح استخدام البرامج وساعات العمل الفعلية')}</li>
        <li>{t('Role-based access control and configurable visibility scopes', 'صلاحيات متعددة المستويات وتحديد نطاق الرؤية المتفق عليه')}</li>
        <li>{t('Daily summary exports to Excel and automated manager digests', 'تصدير الملخصات اليومية إلى Excel وإشعارات للإدارة')}</li>
      </ul>
      {link('/worktracker', 'View WorkTracker Technical Specs ↗', 'المواصفات الفنية لـ WorkTracker ↗', 'btn')}
    </div>

    <div class="spec-box" data-slug="yourspace">
      <span class="bento-badge">{t('SPACE & SUBSCRIPTIONS', 'إدارة المساحات والاشتراكات')}</span>
      <h3>YourSpace</h3>
      <p>{t('Manage spaces, memberships, pricing packages and recurring jobs for institutes and co-working environments.', 'إدارة الحجوزات والمساحات والباقات والاشتراكات المتكررة للمعاهد ومساحات العمل.')}</p>
      <ul class="spec-list">
        <li>{t('Unified calendar for room bookings, time slots, and equipment', 'تقويم موحد لحجوزات القاعات والمواعيد والمعدات')}</li>
        <li>{t('Flexible subscription engine with grace periods & renewals', 'نظام مرن للاشتراكات مع فترات السماح والتجديد الآلي')}</li>
        <li>{t('Customer profiles with transaction logs and attendance checks', 'سجلات مفصلة للعملاء وتاريخ العمليات وتسجيل الحضور')}</li>
        <li>{t('Custom invoice generation and financial overview', 'إصدار الفواتير المخصصة والملخص المالي للتشغيل')}</li>
      </ul>
      {link('/yourspace', 'View YourSpace Technical Specs ↗', 'المواصفات الفنية لـ YourSpace ↗', 'btn')}
    </div>

    <div class="spec-box" data-slug="gathering">
      <span class="bento-badge">{t('EVENT INTELLIGENCE', 'تنظيم الفعاليات الذكية')}</span>
      <h3>Gathering</h3>
      <p>{t('Organize Arabic event journeys from online RSVP to QR check-in, attendance analytics and live prize draws.', 'تنظيم تجربة الفعاليات بالعربية من التسجيل الإلكتروني ومسح QR إلى الإحصاءات وسحب الجوائز المباشر.')}</p>
      <ul class="spec-list">
        <li>{t('Branded Arabic registration pages with custom form fields', 'صفحات تسجيل بهوية الفعالية ونماذج مخصصة بالعربية')}</li>
        <li>{t('Instant QR code badges delivered via WhatsApp and Email', 'إصدار بطاقات QR فورية ترسل عبر واتساب والبريد')}</li>
        <li>{t('Fast check-in scanner via smartphone camera', 'مسح وتأكيد الحضور السريع عبر كاميرا الهاتف')}</li>
        <li>{t('Live animated digital raffle wheel for fair prize draws', 'سحب إلكتروني متحرك وتفاعلي للجوائز أمام الحضور')}</li>
      </ul>
      {link('/gathering', 'View Gathering Technical Specs ↗', 'المواصفات الفنية لـ Gathering ↗', 'btn')}
    </div>
  </div>
</section>'''

matrix_section = f'''<section class="catalog-section wrap">
  <div class="section-heading">
    {t('FEATURE & ARCHITECTURE MATRIX', 'مصفوفة الميزات والمعمارية', 'h2')}
    {t('Compare platform capabilities across hosting, privacy, localization and scalability.', 'مقارنة قدرات المنصات من حيث الاستضافة والخصوصية والتوطين وقابلية التوسع.', 'p')}
  </div>
  <div class="matrix-container">
    <table class="matrix-table">
      <thead>
        <tr>
          <th>{t('Capability', 'الميزة / المعيار')}</th>
          <th>ERP360</th>
          <th>WorkTracker</th>
          <th>YourSpace</th>
          <th>Gathering</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>{t('Native Arabic & RTL', 'واجهات عربية أصيلة')}</strong></td>
          <td>✓ {t('Complete', 'كاملة')}</td>
          <td>✓ {t('Complete', 'كاملة')}</td>
          <td>✓ {t('Complete', 'كاملة')}</td>
          <td>✓ {t('Complete', 'كاملة')}</td>
        </tr>
        <tr>
          <td><strong>{t('Deployment Models', 'نماذج التثبيت والاستضافة')}</strong></td>
          <td>{t('Cloud / On-Prem', 'سحابي أو محلي')}</td>
          <td>{t('Cloud / Local Server', 'سحابي أو خادم محلي')}</td>
          <td>{t('Cloud SaaS', 'سحابي')}</td>
          <td>{t('Cloud / On-Site', 'سحابي أو ميداني')}</td>
        </tr>
        <tr>
          <td><strong>{t('Excel & PDF Export', 'تصدير التقارير')}</strong></td>
          <td>✓ {t('Yes', 'نعم')}</td>
          <td>✓ {t('Yes', 'نعم')}</td>
          <td>✓ {t('Yes', 'نعم')}</td>
          <td>✓ {t('Yes', 'نعم')}</td>
        </tr>
        <tr>
          <td><strong>{t('Role-Based Access', 'صلاحيات متعددة')}</strong></td>
          <td>✓ {t('Granular', 'دقيقة')}</td>
          <td>✓ {t('Manager/Admin', 'إدارية')}</td>
          <td>✓ {t('Staff/Admin', 'فريق/إدارة')}</td>
          <td>✓ {t('Organizer/Staff', 'منظم/فريق')}</td>
        </tr>
        <tr>
          <td><strong>{t('API & Webhooks', 'الربط البرمجي API')}</strong></td>
          <td>✓ {t('REST API', 'متاح')}</td>
          <td>✓ {t('REST API', 'متاح')}</td>
          <td>✓ {t('REST API', 'متاح')}</td>
          <td>✓ {t('Webhooks', 'متاح')}</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>'''

products_body = products_hero + product_cards_bento + matrix_section
page('products', 'Our Products', 'منتجاتنا', 'Focused software for business operations, spaces and events.', 'برمجيات متخصصة لتشغيل الأعمال وإدارة المساحات والفعاليات.', products_body)

# ==============================================================================
# REDESIGNED /SERVICES HUB: 4-PHASE FRAMEWORK & SERVICE ARCHITECTURE
# ==============================================================================
services_hero = intro(
    'ENGINEERING & CONSULTING', 'الخدمات الهندسية والاستشارية',
    'From Strategic Vision to Shipped Intelligence.', 'من الرؤية الاستراتيجية إلى أنظمة ذكية تعمل على أرض الواقع.',
    'We architect custom AI engines, resilient cloud systems, and high-performance digital platforms tailored to your business realities.',
    'نصمم ونبني نماذج ذكاء اصطناعي مخصصة، وبنى تحتية سحابية مرنة، وتطبيقات رقمية تلائم طبيعة عملك واحتياجاتك الفعلية.'
)

framework_section = f'''<section class="catalog-section wrap">
  <div class="section-heading">
    {t('THE 4-PHASE ENGINEERING FRAMEWORK', 'منهجية العمل الهندسية في ٤ مراحل', 'h2')}
    {t('How we take your organization from ambiguous requirements to resilient production systems.', 'كيف ننتقل بأعمالك من الفكرة والاحتياج إلى منظومة برمجية مستقرة وعالية الكفاءة.', 'p')}
  </div>
  <div class="phase-framework">
    <div class="phase-card">
      <div class="phase-num">01</div>
      <h4>{t('Cognitive Discovery', 'فهم الاحتياجات ورسم المسار')}</h4>
      <p>{t('We map your existing operations, interview stakeholders, identify bottlenecks, and define clear measurable ROI criteria before writing code.', 'ندرس مسارات العمل الحالية، ونحدد نقاط التعطيل بدقة، ونضع معايير واضحة للعائد على الاستثمار قبل كتابة أي سطر برمجي.')}</p>
    </div>
    <div class="phase-card">
      <div class="phase-num">02</div>
      <h4>{t('Architectural Blueprint', 'التصميم الهندسي ونمذجة البيانات')}</h4>
      <p>{t('We design scalable schemas, interface wireframes, API contracts, and security boundaries with strict adherence to data sovereignty.', 'نصمم قواعد البيانات، ومسارات واجهات المستخدم، ونماذج الربط API، مع معايير أمان وسيادة بيانات صارمة.')}</p>
    </div>
    <div class="phase-card">
      <div class="phase-num">03</div>
      <h4>{t('Neural Weaving & Build', 'بناء الأنظمة ودمج الذكاء الاصطناعي')}</h4>
      <p>{t('We develop high-performance software with native Arabic RTL UX, integrating AI models as intrinsic functional engines rather than cosmetic add-ons.', 'نطور برمجيات عالية الأداء بتجربة عربية أصيلة، وندمج نماذج الذكاء الاصطناعي كعنصر وظيفي أصيل.')}</p>
    </div>
    <div class="phase-card">
      <div class="phase-num">04</div>
      <h4>{t('Resilient Deployment', 'النشر والتدريب والتشغيل')}</h4>
      <p>{t('We deploy with zero-downtime CI/CD pipelines, train your team hands-on, monitor telemetry, and provide continuous operational resilience.', 'نطلق النظام بسلاسة، وندرب فريقك عمليًا على الاستخدام، ونوفر المراقبة والتحسين المستمر للأداء.')}</p>
    </div>
  </div>
</section>'''

services_list_section = f'''<section class="catalog-section wrap">
  <div class="section-heading">
    {t('CORE ENGAGEMENT DOMAINS', 'مجالات الخدمات الرئيسية', 'h2')}
    {t('Select an individual engagement or combine several services into one cohesive delivery.', 'اختر مسار عمل محدد أو اجمع بين عدة خدمات لتحقيق أهدافك المؤسسية.', 'p')}
  </div>
  <div class="catalog-grid">
    {''.join(card(x) for x in (services + [academy_card]))}
  </div>
</section>'''

engagement_models_section = f'''<section class="catalog-section wrap">
  <div class="section-heading">
    {t('FLEXIBLE ENGAGEMENT MODELS', 'نماذج التعاقد والعمل', 'h2')}
    {t('Choose the structure that matches your organizational stage and internal team capacity.', 'اختر النموذج الذي يناسب مرحلة شركتك وقدرات فريقك الداخلي.', 'p')}
  </div>
  <div class="hub-grid-2">
    <div class="spec-box">
      <span class="bento-badge">{t('DEDICATED POD', 'فريق هندسي مخصص')}</span>
      <h3>{t('Dedicated Engineering Pod', 'فريق تطوير متكامل')}</h3>
      <p>{t('A dedicated squad of software engineers, AI architects and UI specialists working directly alongside your product leads.', 'فريق متخصص من مهندسي البرمجيات وخبراء الذكاء الاصطناعي وتصميم الواجهات يعمل كامتداد لفريقك الداخلي.')}</p>
      <ul class="spec-list">
        <li>{t('Agile 2-week delivery sprints with transparent backlog', 'سبرنتات عمل كل أسبوعين مع شفافية كاملة في المهام')}</li>
        <li>{t('Direct communication via Slack/Teams and weekly syncs', 'تواصل يومي مباشر واجتماعات مواءمة أسبوعية')}</li>
        <li>{t('Full IP ownership transferred to your company', 'ملكية فكرية كاملة لكل الأكواد والحلول المطورة')}</li>
      </ul>
    </div>
    <div class="spec-box">
      <span class="bento-badge">{t('TURNKEY SCOPE', 'تسليم مشاريع متكاملة')}</span>
      <h3>{t('Turnkey Product Delivery', 'تطوير وتسليم متكامل بالمفتاح')}</h3>
      <p>{t('Fixed-scope, milestone-based product development from initial architecture design to production launch and handover.', 'تطوير مشروع متكامل محدد النطاق والمعالم من التصميم حتى النشر والتسليم النهائي.')}</p>
      <ul class="spec-list">
        <li>{t('Clear milestone-based deliverables and acceptance criteria', 'مراحل تسليم ومعايير قبول واضحة ومتفق عليها')}</li>
        <li>{t('Post-launch warranty, documentation and team onboarding', 'فترة ضمان بعد الإطلاق، وتوثيق تقني، وتدريب كامل')}</li>
        <li>{t('Ideal for launching new digital platforms and enterprise apps', 'مثالي لإطلاق منتجات ومنصات رقمية جديدة بسرعة')}</li>
      </ul>
    </div>
  </div>
</section>'''

services_body = services_hero + framework_section + services_list_section + engagement_models_section
page('services', 'Services', 'الخدمات', 'AI, software, websites and business resilience consulting.', 'الذكاء الاصطناعي والبرمجيات والمواقع واستشارات المرونة المؤسسية.', services_body)

# ==============================================================================
# INITIATIVES & PROJECTS HUBS
# ==============================================================================
for slug, en, ar, desc, ardesc in [
    ('initiatives', 'Community initiatives', 'مبادرات خدمة المجتمع', 'Technology that connects people with everyday community needs.', 'تكنولوجيا تربط الناس باحتياجات المجتمع اليومية.'),
    ('projects', 'Projects in development', 'مشاريع قيد التطوير', 'Distinct platforms for commerce, mobility and education.', 'منصات مستقلة للتجارة والتنقل والتعليم.')
]:
    page(slug, en, ar, desc, ardesc, intro('EXPLORE', 'اكتشف', en, ar, desc, ardesc) + '<section class="catalog-section wrap">' + grid([x for x in items if x['group'] == slug]) + '</section>')

# ==============================================================================
# DETAIL PAGES FOR INDIVIDUAL PRODUCTS AND SERVICES
# ==============================================================================
for x in items + services:
    body = intro(x['group'].upper(), {'products': 'المنتجات', 'initiatives': 'المبادرات', 'projects': 'المشاريع', 'services': 'الخدمات'}[x['group']], x['name'], x['arname'], x['en'], x['ar'])
    body += f'<section class="catalog-section wrap detail-layout"><div class="detail-art"><img src="/assets/illustrations/{x["visual"]}.svg" alt="" width="640" height="400"><small>' + t('Illustration of the concept.', 'رسم توضيحي للفكرة.') + '</small></div><div>'
    if x.get('status'):
        body += t(*x['status'], 'p', 'status')
    body += t('A closer look', 'نظرة أقرب', 'h2') + '<ul class="feature-list">' + ''.join(t(a, b, 'li') for a, b in x['points']) + '</ul>' + link('https://wa.me/201026655008?text=' + urllib.parse.quote('Hello Zaka2, I would like to discuss ' + x['name']), 'Discuss ' + x['name'] + ' ↗', 'تواصل بشأن ' + x['arname'] + ' ↗', 'btn') + '</div></section>'
    if x['slug'] == 'madinaty-ai':
        body += block('For residential communities', 'للمجتمعات السكنية', 'A shared umbrella for resident services, local commerce and community management.', 'مظلة موحدة لخدمات السكان والتجارة المحلية وإدارة المجتمع.', link('https://madinatyai.com', 'Visit Madinaty AI ↗', 'زيارة مدينتي AI ↗', 'btn'))
    body += '<div class="wrap back-link">' + link('/' + x['group'], 'Explore more ↗', 'اكتشف المزيد ↗') + '</div>'
    page(x['slug'], x['name'], x['arname'], x['en'], x['ar'], body)

# ==============================================================================
# ACADEMY PAGE
# ==============================================================================
academy_rows = [
    ('AI workshops for educators', 'ورش الذكاء الاصطناعي للمحاضرين', 'Practical sessions on lesson planning, learning activities and responsible use of AI in teaching.', 'جلسات عملية لتخطيط الدروس والأنشطة التعليمية والاستخدام المسؤول للذكاء الاصطناعي في التدريس.'),
    ('Children & youth', 'الأطفال والشباب', 'AI literacy, programming and creative projects adapted to age and experience.', 'فهم الذكاء الاصطناعي والبرمجة والمشاريع الإبداعية بما يناسب العمر والخبرة.'),
    ('Professionals & executives', 'الموظفون والمدراء والتنفيذيون', 'AI for daily work, programming, leadership and decision-making; crisis and continuity exercises.', 'الذكاء الاصطناعي للعمل اليومي والبرمجة والقيادة واتخاذ القرار وتمارين الأزمات واستمرارية الأعمال.')
]

learning_rows = [
    ('Kids AI Academy', 'Kids AI Academy', 'Interactive educational sessions that help children learn by doing.', 'جلسات تعليمية تفاعلية تساعد الأطفال على التعلم بالممارسة.'),
    ('Little Explorer', 'Little Explorer', 'An Arabic geography-learning experience with an interactive 3D globe.', 'تجربة عربية لتعلم الجغرافيا عبر كرة أرضية تفاعلية ثلاثية الأبعاد.'),
    ('Family Games', 'ألعاب العائلة', 'Collaborative drawing, charades and trivia for shared learning and play.', 'الرسم الجماعي والتمثيل والأسئلة للتعلم واللعب المشترك.')
]

def simplecards(rows):
    return '<div class="catalog-grid">' + ''.join('<article class="catalog-card"><div class="card-body">' + t(a, b, 'h3') + t(c, d, 'p') + '</div></article>' for a, b, c, d in rows) + '</div>'

page('academy', 'Academy & Learning Experiences', 'الأكاديمية وتجارب التعلم', 'Programming and AI workshops for educators, children, youth, adults and corporate teams in Cairo.', 'ورش الذكاء الاصطناعي والبرمجة للمحاضرين والأطفال والشباب والكبار وفرق العمل في القاهرة.',
     intro('LEARN BY DOING', 'تعلّم بالممارسة', 'Skills for your next chapter.', 'مهارات لخطوتك القادمة.', 'Practical learning shaped around age, role and experience.', 'تعلم عملي يناسب العمر والدور والخبرة.') +
     block('Workshops & programmes', 'الورش والبرامج', 'Choose your audience; we shape the learning path.', 'حدد الفئة المستهدفة لنصمم مسار التعلم.', simplecards(academy_rows)) +
     block('Learning experiences', 'تجارب التعلم', 'Explore different ways to discover, create and learn.', 'طرق متنوعة للاكتشاف والإبداع والتعلم.', simplecards(learning_rows)))

# ==============================================================================
# SITEMAP & PROJECT DATA
# ==============================================================================
(R / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join('<url><loc>https://zakaa-ai.net/' + s + '</loc></url>' for s in pages) + '</urlset>\n', encoding='utf-8')
(R / 'assets/project-data.js').write_text('export const projects = ' + json.dumps([dict(id=i + 1, name=x['name'], group=x['group'], en=x['en'] + ' ' + ('Status: ' + x['status'][0] + '. ' if x.get('status') else '') + ' '.join(a for a, b in x['points']), ar=x['ar']) for i, x in enumerate(items + services)], ensure_ascii=False, indent=2) + ';\n', encoding='utf-8')

print('Generated', len(pages), 'pages successfully with Option C architecture!')
