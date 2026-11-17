#!/usr/bin/env python3
"""Academic Portfolio B2. Build locally with Python 3 (stdlib only)."""
from __future__ import annotations
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'site'

def read_json(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))

PROFILE = read_json('config/site.json')
STORIES = read_json('content/research.json')
PUBLICATIONS = read_json('content/publications.json')
WRITING = read_json('content/writing.json')

def e(value):
    return html.escape(str(value if value is not None else ''), quote=True)

def safe_url(value):
    value = str(value or '').strip()
    p = urlparse(value)
    if p.scheme == 'https' and p.netloc:
        return e(value)
    if value and not p.scheme and not value.startswith(('/', '//', '#')) and '..' not in Path(value).parts:
        return e(value)
    return ''

def prefix(depth):
    return '../' * depth

def image_tag(path, alt, depth=0, css='', loading='lazy'):
    path = safe_url(path)
    if not path:
        return ''
    src = path if path.startswith('https://') else prefix(depth) + path
    return f'<img src="{src}" alt="{e(alt)}" loading="{loading}" class="{e(css)}">'

def layout(title, description, slug, body, depth=0):
    p = prefix(depth)
    nav = [('Home',''), ('Research Stories','research/'), ('Publications','publications/'), ('Writing','writing/'), ('CV','cv/'), ('Contact','contact/')]
    links = ''.join(f'<a href="{p}{path or "./"}" class="{"active" if slug == path else ""}" {"aria-current=\"page\"" if slug == path else ""}>{label}</a>' for label,path in nav)
    title_full = f'{title} · {PROFILE["display_name"]}'
    domain = PROFILE.get('domain','').rstrip('/')
    canonical = domain + ('/' + slug if slug else '/') if domain else ''
    # Story pages use their own canonical path, not the highlighted Research nav entry.
    if domain and depth == 2:
        canonical = domain + '/stories/' + next((s['slug'] for s in STORIES if s['short_title'] == title), '') + '/'
    social_image = domain + '/' + (next((s['image'] for s in STORIES if s['short_title'] == title), PROFILE.get('hero_image','assets/hero-embryo.webp')) if depth == 2 else PROFILE.get('hero_image','assets/hero-embryo.webp')) if domain else ''
    seo_tags = (f'<link rel="canonical" href="{e(canonical)}">\n'
                f'<meta property="og:url" content="{e(canonical)}">\n'
                f'<meta property="og:image" content="{e(social_image)}">\n'
                f'<meta name="twitter:card" content="summary_large_image">\n') if domain else ''
    externals = ''
    for label,key in [('ORCID','orcid_url'),('Google Scholar','scholar_url'),('researchmap','researchmap_url'),('GitHub','github_url')]:
        url = safe_url(PROFILE.get(key,''))
        if url: externals += f'<a href="{url}" target="_blank" rel="noopener noreferrer">{label} ↗</a>'
    return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{e(description)}"><meta name="theme-color" content="#173a42">
<meta property="og:title" content="{e(title_full)}"><meta property="og:description" content="{e(description)}"><meta property="og:type" content="website">
<title>{e(title_full)}</title>
{seo_tags}<link rel="icon" type="image/svg+xml" href="{p}assets/favicon.svg"><link rel="stylesheet" href="{p}assets/site.css">
</head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap header-inner">
<a class="brand" href="{p or "./"}"><span class="brand-mark" aria-hidden="true">◌</span><span>{e(PROFILE['short_name'])}<span class="brand-sub"> / Academic Portfolio</span></span></a>
<button class="menu-button" data-mobile-menu aria-expanded="false" aria-controls="main-nav">Menu ☰</button>
<nav class="nav" id="main-nav" aria-label="Main navigation" data-main-nav>{links}</nav>
</div></header>
<main id="main">{body}</main>
<footer class="site-footer"><div class="wrap footer-inner"><div class="footer-left"><b>{e(PROFILE['display_name'])}</b><div>© <span data-current-year>2026</span> · {e(PROFILE['affiliation'])} · {e(PROFILE['location'])}</div><div>{e(PROFILE['notice'])}</div></div><div class="footer-links">{externals}</div></div></footer>
<script defer src="{p}assets/site.js"></script>
</body></html>'''

def section_head(kicker, title, desc='', link=None, link_label='View all ↗'):
    return f'<div class="section-intro"><div><div class="overline">{e(kicker)}</div><h2>{e(title)}</h2><p>{e(desc)}</p></div>{f"<a class=\"text-link\" href=\"{link}\">{link_label}</a>" if link else ""}</div>'

def story_card(s, depth=0):
    p = prefix(depth)
    href = p + 'stories/' + e(s['slug']) + '/'
    img = image_tag(s['image'],s['image_alt'],depth,css='story-cover')
    return f'''<article class="story-card"><a href="{href}" class="story-image-link">{img}<span class="story-index">{e(s['number'])} / 03</span></a>
<div class="story-content"><div class="story-kicker">{e(s['tag'])}</div><h3><a href="{href}">{e(s['short_title'])}</a></h3><p>{e(s['summary'])}</p><a href="{href}" class="card-link">Read the story <span aria-hidden="true">↗</span></a></div></article>'''

def publication_html(pub):
    links=''
    doi=str(pub.get('doi','')).strip()
    if doi:
        doi = re.sub(r'^https?://(dx\.)?doi\.org/', '', doi, flags=re.I)
        links += f'<a href="https://doi.org/{e(doi)}" target="_blank" rel="noopener noreferrer">DOI ↗</a>'
    for label,key in [('Open access','url'),('PDF','pdf')]:
        u=safe_url(pub.get(key,''))
        if u: links+=f'<a href="{u}" target="_blank" rel="noopener noreferrer">{label} ↗</a>'
    return f'''<article class="pub-item" data-publication data-type="{e(pub.get('type','Research Article'))}"><div class="pub-year">{e(pub.get('year',''))}</div><div><span class="pub-type">{e(pub.get('type','Research Article'))}</span><h3 class="pub-title">{e(pub.get('title',''))}</h3><div class="pub-meta">{e(pub.get('authors',''))} · <i>{e(pub.get('journal',''))}</i></div>{f'<p class="note">{e(pub["summary"])}</p>' if pub.get('summary') else ''}<div class="pub-links">{links}</div></div></article>'''

def writing_html(w):
    url=safe_url(w.get('url',''))
    title=e(w.get('title',''))
    title_html=f'<a href="{url}" target="_blank" rel="noopener noreferrer">{title} ↗</a>' if url else title
    return f'''<article class="pub-item"><div class="pub-year">{e(w.get('year',''))}</div><div><span class="pub-type">{e(w.get('category','Essay'))}</span><h3 class="pub-title">{title_html}</h3><p class="note">{e(w.get('summary',''))}</p></div></article>'''

def empty_pubs():
    return '<div class="empty-state"><strong>Selected publications will appear here.</strong>The bibliography is intentionally blank until verified titles, authors and DOI records are supplied.</div>'

def page_hero(kicker,title,desc):
    return f'<section class="page-hero"><div class="wrap"><div class="overline">{e(kicker)}</div><h1>{e(title)}</h1><p>{e(desc)}</p></div></section>'

def home():
    cards=''.join(story_card(s) for s in STORIES)
    pubs=''.join(publication_html(x) for x in PUBLICATIONS[:3]) if PUBLICATIONS else empty_pubs()
    writing=''.join(writing_html(x) for x in WRITING[:3]) if WRITING else '''<div class="writing-grid"><div class="writing-card"><div class="category">Essays & commentary</div><h3>Reproductive ethics</h3><p>Testing, evidence, patient autonomy, and the societal implications of assisted reproduction.</p></div><div class="writing-card"><div class="category">Science writing</div><h3>Developmental biology</h3><p>Ideas and discoveries that illuminate the first days of mammalian development.</p></div><div class="writing-card"><div class="category">Reflections</div><h3>Science & society</h3><p>How research methods, institutions, and scientific culture shape what we know.</p></div></div>'''
    hero_img=image_tag(PROFILE.get('hero_image','assets/hero-embryo.webp'),'Conceptual illustration of an oocyte and early embryo development',0,'hero-photo','eager')
    portrait=image_tag(PROFILE.get('portrait',''),'Portrait of '+PROFILE['display_name'],0,'profile-portrait')
    return f'''<section class="b2-hero"><div class="wrap hero-grid"><div class="hero-copy"><div class="eyebrow">{e(PROFILE['eyebrow'])}</div><div class="hero-name">{e(PROFILE['display_name'])}, {e(PROFILE['degree'])}</div><h1>{e(PROFILE['headline'])}</h1><p class="lede">{e(PROFILE['introduction'])}</p><div class="actions"><a class="btn" href="research/">Explore research stories ↗</a><a class="btn secondary" href="publications/">Publications</a></div><div class="mini-line"><span>{e(PROFILE['role'])}</span><span class="dot"></span><span>{e(PROFILE['affiliation'])}</span><span class="dot"></span><span>{e(PROFILE['location'])}</span></div>{portrait}</div><div class="hero-visual">{hero_img}<div class="hero-art-label">{e(PROFILE.get('hero_caption','Concept illustration'))}</div></div></div></section>
<section class="section story-feature"><div class="wrap">{section_head('01 / Research Stories','A question-led view of research','Three connected lines of inquiry—from molecular traces to developmental timing and the ethics of reproductive choices.','research/','All research stories ↗')}<div class="story-grid">{cards}</div></div></section>
<section class="section quote-section"><div class="wrap split"><div><div class="overline">02 / Perspective</div><p class="lead-quote">{e(PROFILE.get('featured_quote',''))}</p><a class="text-link" href="cv/">Academic journey ↗</a></div><div class="subtle-panel"><h2>Connecting biological observations with meaningful questions.</h2><p class="split-copy">{e(PROFILE['research_statement'])}</p><div class="stats"><div class="stat"><b>01</b><span>Molecular signals</span></div><div class="stat"><b>02</b><span>Developmental time</span></div><div class="stat"><b>03</b><span>Evidence & ethics</span></div></div></div></div></section>
<section class="section light"><div class="wrap">{section_head('03 / Scholarship','Selected publications','Verified research papers, perspectives, and scholarly outputs.','publications/')}<div class="pub-list">{pubs}</div></div></section>
<section class="section"><div class="wrap">{section_head('04 / Essays','Writing & perspectives','A place for scientific essays, critical analysis, and reflection on the social context of research.','writing/','Browse writing ↗')}{writing}</div></section>
<section class="cta"><div class="wrap"><div class="cta-panel"><div><div class="overline" style="color:#b2d7c9">Academic collaboration</div><h2>Interested in the biology and ethics of early development?</h2><p>Scientific conversations and interdisciplinary exchanges are welcome.</p></div><a class="btn" href="contact/">Get in touch ↗</a></div></div></section>'''

def research_page():
    cards=''.join(story_card(s,1) for s in STORIES)
    return page_hero('Research / Stories','Research Stories','Science begins with questions. Explore three research narratives connecting early embryology, measurement, and interpretation.')+f'''<section class="page-body"><div class="wrap"><div class="research-intro"><div class="overline">A research portfolio</div><p>Rather than listing techniques in isolation, these stories explain the scientific questions behind my work, how they can be approached, and what remains unresolved.</p></div><div class="story-grid">{cards}</div><div class="disclaimer"><strong>About the images and text</strong><p>The cover images are conceptual illustrations, not microscopy or original experimental data. These narratives are editable drafts and do not claim clinical validation.</p></div></div></section>'''

def story_page(s):
    image=image_tag(s['image'],s['image_alt'],2,'story-hero-img')
    questions=''.join(f'<li>{e(q)}</li>' for q in s.get('open_questions',[]))
    methods=''.join(f'<span class="tag">{e(x)}</span>' for x in s.get('methods',[]))
    related=''.join(f'<li>{e(x)}</li>' for x in s.get('related_publications',[]))
    related_html=f'<ul>{related}</ul>' if related else '<p>Related verified publications will be linked here after the bibliography is added.</p>'
    other=''.join(story_card(x,2) for x in STORIES if x['slug']!=s['slug'])
    return f'''<section class="story-head"><div class="wrap"><a class="breadcrumb" href="../../research/">← All research stories</a><div class="overline">{e(s['tag'])} · {e(s['number'])} / 03</div><h1>{e(s['title'])}</h1><p class="story-standfirst">{e(s['summary'])}</p><div class="draft-label">{e(s.get('status','Narrative draft'))}</div></div></section>
<section class="story-media"><div class="wrap">{image}<p class="image-credit">Concept illustration. Not a microscopy image or original research data.</p></div></section>
<section class="page-body story-body"><div class="wrap story-columns"><aside class="story-sidebar"><div class="small-title">In this story</div><a href="#question">The question</a><a href="#background">Context</a><a href="#approach">Approach</a><a href="#significance">Why it matters</a><a href="#questions">Open questions</a></aside><article class="story-article"><section id="question"><div class="overline">The central question</div><h2>{e(s['question'])}</h2></section><section id="background"><div class="overline">01 / Context</div><h2>Why this question matters</h2><p>{e(s['background'])}</p></section><section id="approach"><div class="overline">02 / Approach</div><h2>How the question can be studied</h2><p>{e(s['approach'])}</p><div class="tag-row">{methods}</div></section><section id="significance"><div class="overline">03 / Interpretation</div><h2>What the work may contribute</h2><p>{e(s['significance'])}</p></section><section id="questions"><div class="overline">04 / Future directions</div><h2>Questions still open</h2><ul>{questions}</ul></section><section><div class="overline">Related scholarship</div><h2>Publications and resources</h2>{related_html}</section></article></div></section>
<section class="section light"><div class="wrap">{section_head('Continue exploring','Other research stories','Related questions in early development and reproductive science.')}<div class="story-grid other-stories">{other}</div></div></section>'''

def publication_page():
    groups=['All']+list(dict.fromkeys(p.get('type','Research Article') for p in PUBLICATIONS))
    buttons=''.join(f'<button class="filter {"active" if i==0 else ""}" type="button" data-pub-filter="{e(g)}" aria-pressed="{str(i==0).lower()}">{e(g)}</button>' for i,g in enumerate(groups))
    items=''.join(publication_html(x) for x in PUBLICATIONS) if PUBLICATIONS else empty_pubs()
    return page_hero('Scholarship / Output','Publications','A curated bibliography with verified titles, authorship, publication details and DOI links.')+f'<section class="page-body"><div class="wrap"><div class="section-intro"><div><div class="small-title">Full bibliography</div><p class="note">Filter by publication type; DOI and open-access links are provided when available.</p></div><span class="note" data-publication-count>{len(PUBLICATIONS)} items</span></div><div class="filters">{buttons}</div><div class="pub-list">{items}</div></div></section>'

def writing_page():
    topics='''<div class="writing-grid"><div class="writing-card"><div class="category">Research ethics</div><h3>Reproductive ethics</h3><p>Embryo testing, consent, clinical evidence, and reproductive autonomy.</p></div><div class="writing-card"><div class="category">Science essays</div><h3>Developmental biology</h3><p>Research stories and open questions in early development.</p></div><div class="writing-card"><div class="category">Conceptual work</div><h3>Science & society</h3><p>How scientific ideas interact with institutions and public life.</p></div></div>'''
    entries=''.join(writing_html(w) for w in WRITING) if WRITING else '<div class="empty-state"><strong>Essays will be added here.</strong>Only publicly available or approved writing will be listed as published.</div>'
    return page_hero('Ideas / Essays','Writing','Scientific essays, perspectives, and reflections across embryology, ethics and society.')+f'<section class="page-body"><div class="wrap"><div class="small-title">Themes</div>{topics}<div style="margin-top:55px"><div class="small-title">Articles & essays</div><div class="pub-list">{entries}</div></div></div></section>'

def cv_page():
    timeline=''.join(f'<article class="timeline-entry"><span class="when">{e(c["period"])}</span><h3>{e(c["position"])}</h3><p class="inst">{e(c["institution"])}</p><p>{e(c["description"])}</p></article>' for c in PROFILE.get('career',[]))
    pdf=safe_url(PROFILE.get('cv_pdf',''))
    cv_link=f'<a class="btn" href="{pdf if pdf.startswith("https://") else "../"+pdf}">View CV as PDF ↗</a>' if pdf else '<p class="note">A downloadable CV can be added later.</p>'
    return page_hero('Academic profile / Journey','Curriculum Vitae',f'{PROFILE["display_name"]}, {PROFILE["degree"]} · {PROFILE["role"]} at {PROFILE["affiliation"]}.')+f'<section class="page-body"><div class="wrap cv-grid"><div><div class="small-title">Experience & training</div><div class="timeline">{timeline}</div></div><aside class="side-panel"><h3>Research interests</h3><p>Preimplantation development; polar body biology; embryo morphokinetics; molecular assessment; reproductive ethics.</p><h3>Downloadable CV</h3>{cv_link}</aside></div></section>'

def contact_page():
    email=str(PROFILE.get('email','')).strip()
    email_html=f'<a class="email-link" href="mailto:{e(email)}">{e(email)} ↗</a>' if email and '@' in email else '<div class="empty-state"><strong>Contact details will be added soon.</strong>Enter your academic email in config/site.json before sharing the site publicly.</div>'
    social=''
    for label,key in [('ORCID','orcid_url'),('Google Scholar','scholar_url'),('researchmap','researchmap_url'),('GitHub','github_url')]:
        u=safe_url(PROFILE.get(key,''))
        if u:social+=f'<a href="{u}" target="_blank" rel="noopener noreferrer">{label} ↗</a>'
    return page_hero('Connect / Collaboration','Contact','For scientific collaboration, scholarly discussion, and professional inquiries.')+f'<section class="page-body"><div class="wrap contact-info"><div class="small-title">Academic contact</div>{email_html}<div style="margin-top:42px"><h2>Affiliation</h2><p>{e(PROFILE["affiliation"])}<br>{e(PROFILE["location"])}</p></div><div class="social-row">{social}</div><p class="fine-print">{e(PROFILE["notice"])}</p></div></section>'

if __name__=='__main__':
    for s in STORIES:
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',s['slug']):
            raise ValueError('Invalid story slug: '+s['slug'])
    if OUT.exists():shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shutil.copytree(ROOT/'assets',OUT/'assets',dirs_exist_ok=True)
    (OUT/'.nojekyll').write_text('',encoding='utf-8')
    pages=[('', 'Home','Academic research portfolio on preimplantation development and reproductive ethics.',home(),0),('research','Research Stories','Research stories on polar body biology, embryo development, and reproductive ethics.',research_page(),1),('publications','Publications','Verified scholarly bibliography and DOI links.',publication_page(),1),('writing','Writing','Essays and commentaries on science and society.',writing_page(),1),('cv','CV','Academic background and research experience.',cv_page(),1),('contact','Contact','Academic contact and collaboration.',contact_page(),1)]
    for s in STORIES:
        pages.append(('stories/'+s['slug'],s['short_title'],s['summary'],story_page(s),2))
    for path,title,desc,body,depth in pages:
        directory=OUT/path
        directory.mkdir(parents=True,exist_ok=True)
        slug='research/' if path=='research' else path+'/' if path and not path.startswith('stories/') else 'research/' if path.startswith('stories/') else ''
        (directory/'index.html').write_text(layout(title,desc,slug,body,depth),encoding='utf-8')
    if PROFILE.get('domain'):
        base=PROFILE['domain'].rstrip('/')
        urls=[base+'/' + (path+'/' if path else '') for path, *_ in pages]
        sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('  <url><loc>'+e(u)+'</loc></url>\n' for u in urls)+'</urlset>\n'
        (OUT/'sitemap.xml').write_text(sitemap,encoding='utf-8')
        (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+base+'/sitemap.xml\n',encoding='utf-8')
    print('Built',len(pages),'pages in',OUT)
