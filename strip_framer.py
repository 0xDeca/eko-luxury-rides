#!/usr/bin/env python3
"""
Strip Framer JS runtime from all HTML files.
Keeps all CSS, fonts, images, and HTML structure intact.
Removes:
- modulepreload links to framerusercontent.com CDN
- Framer hydration data attributes
- Framer badge container
- Buy this template button
- Framer-specific inline scripts
- Framer analytics/events script
"""

import re
import os

BASE = '/home/deca/Downloads/eko-luxury-rides'

# Files to process (all HTML pages)
FILES = ['index.html', 'about', 'apartments', 'contact',
         'privacy-policy', 'refund-policy', 'terms-and-condition']

# Car detail pages
CAR_FILES = [f'cars/{f}' for f in os.listdir(f'{BASE}/cars') 
             if os.path.isfile(f'{BASE}/cars/{f}')]

# Blog pages
BLOG_DIR = f'{BASE}/blog'
BLOG_FILES = [f'blog/{f}' for f in os.listdir(BLOG_DIR) 
              if os.path.isfile(f'{BLOG_DIR}/{f}')]

ALL_FILES = FILES + CAR_FILES + BLOG_FILES

def strip_framer(html):
    # 1. Remove Framer comment header
    html = re.sub(r'<!-- Made in Framer.*?-->', '', html)
    html = re.sub(r'<!-- Published.*?-->', '', html)

    # 2. Remove framer meta tags
    html = re.sub(r'<meta name="framer-search-index[^>]*>', '', html)
    html = re.sub(r'<meta name="framer-search-index-fallback[^>]*>', '', html)
    html = re.sub(r'<meta name="generator"[^>]*>', '', html)

    # 3. Remove framer favicon/icon links
    html = re.sub(r'<link href="https://framerusercontent\.com/images/[^"]*" rel="icon"[^>]*>', '', html)
    html = re.sub(r'<link rel="apple-touch-icon" href="https://framerusercontent\.com[^>]*>', '', html)

    # 4. Remove framer search index and OG images from framer (keep title/desc)
    html = re.sub(r'<meta property="og:image" content="https://framerusercontent\.com[^>]*>', '', html)
    html = re.sub(r'<meta name="twitter:image" content="https://framerusercontent\.com[^>]*>', '', html)

    # 5. Remove framer editor bar detection script
    html = re.sub(r'<script>try\{if\(localStorage\.getItem\("__framer_force_showing_editorbar_since"\).*?</script>', '', html)

    # 6. Remove framer modulepreload links
    html = re.sub(r'<link rel="modulepreload"[^>]*href="https://framerusercontent\.com[^>]*>', '', html)
    html = re.sub(r'<link rel="modulepreload"[^>]*href="https://fonts\.gstatic\.com[^>]*>', '', html)

    # 7. Remove framer CSS SSR minified style tag (keep font CSS)
    html = re.sub(r'<style data-framer-css-ssr-minified[^>]*>.*?</style>', '', html, flags=re.DOTALL)

    # 8. Remove framer breakpoint CSS
    html = re.sub(r'<style data-framer-breakpoint-css[^>]*>.*?</style>', '', html, flags=re.DOTALL)

    # 9. Remove framer events/analytics script
    html = re.sub(r'<script async src="https://events\.framer\.com/script\?v=2"[^>]*>.*?</script>', '', html, flags=re.DOTALL)

    # 10. Remove framer URL parameter preservation script
    html = re.sub(r'<script>!function\(\)\{var w="framer_variant".*?</script>', '', html, flags=re.DOTALL)

    # 11. Remove appear-animation script tag
    html = re.sub(r'<script data-framer-appear-animation[^>]*>.*?</script>', '', html, flags=re.DOTALL)

    # 12. Remove NODE_ENV script
    html = re.sub(r'<script>typeof document<"u"&&\(window\.process=.*?</script>', '', html, flags=re.DOTALL)

    # 13. Remove framer badge container entirely
    html = re.sub(r'<div id="__framer-badge-container">.*?</div>\s*', '', html, flags=re.DOTALL)

    # 14. Remove buy-this-template button
    html = re.sub(r'<a[^>]*class="framer-bOtdl[^"]*"[^>]*href="https://designtocodes\.com[^>]*>.*?</a>', '', html, flags=re.DOTALL)

    # 15. Remove data-framer-hydrate-v2 attribute (this triggers hydration!)
    html = re.sub(r' data-framer-hydrate-v2="[^"]*"', '', html)

    # 16. Remove other framer data attributes that trigger behavior
    for attr in ['data-framer-ssr-released-at', 'data-framer-page-optimized-at',
                 'data-framer-generated-page', 'data-framer-appear-id',
                 'data-framer-name', 'data-framer-component-type',
                 'data-framer-background-image-wrapper',
                 'data-framer-preserve-params', 'data-framer-appear-animation']:
        html = re.sub(f' {attr}="[^"]*"', '', html)

    # 17. Remove __framer_handoverData div
    html = re.sub(r'<div id="__framer__handoverData[^>]*>.*?</div>', '', html, flags=re.DOTALL)

    # 18. Remove template-overlay div
    html = re.sub(r'<div id="template-overlay">.*?</div>', '', html, flags=re.DOTALL)

    # 19. Remove empty framer data-framer-html-style
    html = re.sub(r'<style data-framer-html-style[^>]*>.*?</style>', '', html, flags=re.DOTALL)

    # 20. Remove the nested-link click handler script at the bottom
    html = re.sub(r'<script>\(\(\)=>\{function u\(\)\{.*?return u\}\)\(\)\)\(\)</script>', '', html, flags=re.DOTALL)

    # 21. Remove framer variant query param script at bottom
    html = re.sub(r'<script>!function\(\)\{var w="framer_variant";.*?</script>', '', html, flags=re.DOTALL)

    # 22. Remove svg template container if empty
    html = re.sub(r'<div id="svg-templates">.*?</div>', '', html, flags=re.DOTALL)

    # 23. Remove framer data-nested-link and data-reset attributes
    html = html.replace(' data-nested-link="true"', '')
    html = html.replace(' data-reset="button"', '')

    # 24. Remove our own fix script (no longer needed)
    html = re.sub(r'<script>\s*\(function\(\)\s*\{[^}]*fixContent[^}]*\}.*?</script>', '', html, flags=re.DOTALL)

    # 25. Remove the CSS !important style override we added
    html = re.sub(r'<style>\s*a\[href="cars"\].*?</style>', '', html, flags=re.DOTALL)

    # Clean up empty lines
    html = re.sub(r'\n\s*\n\s*\n', '\n\n', html)

    return html

for fname in ALL_FILES:
    path = f'{BASE}/{fname}'
    if not os.path.exists(path):
        print(f"⚠️  {fname}: not found, skipping")
        continue
    
    with open(path, 'r') as f:
        html = f.read()
    
    before = len(html)
    html = strip_framer(html)
    after = len(html)
    
    with open(path, 'w') as f:
        f.write(html)
    
    print(f"✅ {fname}: {before} → {after} bytes (removed {before-after})")

print(f"\nDone! Processed {len(ALL_FILES)} files.")
