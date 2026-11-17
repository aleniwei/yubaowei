#!/usr/bin/env python3
"""Validate locally generated static website (Python standard library only)."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import sys

ROOT = Path(__file__).resolve().parent
SITE = ROOT / 'site'
DOMAIN = 'https://weiyubao.pages.dev'

class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        for key in ('href', 'src'):
            if key in data:
                self.refs.append((tag, key, data[key]))


def check():
    errors = []
    html_files = sorted(SITE.rglob('*.html'))
    if not (SITE / 'index.html').is_file():
        errors.append('site/index.html is missing')
    if len(html_files) != 9:
        errors.append(f'Expected 9 pages; found {len(html_files)}')
    for page in html_files:
        content = page.read_text(encoding='utf-8')
        if f'<link rel="canonical" href="{DOMAIN}' not in content:
            errors.append(f'Missing canonical domain in {page.relative_to(SITE)}')
        p = References()
        p.feed(content)
        for tag, attr, ref in p.refs:
            parsed = urlparse(ref)
            if parsed.scheme or parsed.netloc or not parsed.path or ref.startswith(('#', '//', 'mailto:', 'tel:')):
                continue
            if parsed.path.startswith('/'):
                candidate = SITE / unquote(parsed.path).lstrip('/')
            else:
                candidate = page.parent / unquote(parsed.path)
            candidate = candidate.resolve()
            if SITE.resolve() not in candidate.parents and candidate != SITE.resolve():
                errors.append(f'Link escapes site in {page.relative_to(SITE)}: {ref}')
            elif not (candidate.is_file() or (candidate.is_dir() and (candidate / 'index.html').is_file())):
                errors.append(f'Broken link in {page.relative_to(SITE)}: {ref}')
    for name in ('robots.txt','sitemap.xml','assets/site.css','assets/site.js'):
        if not (SITE / name).is_file(): errors.append(f'Missing {name}')
    if errors:
        print('FAILED:\n'+'\n'.join('- '+x for x in errors))
        return 1
    print(f'OK: {len(html_files)} HTML pages; internal links, assets and canonical domain checked.')
    return 0

if __name__ == '__main__':
    sys.exit(check())
