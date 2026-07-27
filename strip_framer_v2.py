#!/usr/bin/env python3
"""
Strip Framer JS runtime from all HTML files without breaking CSS.
Version 2: Preserves ALL style tags and ALL data-attributes used by CSS.
Only removes:
- External Framer JS scripts and modulepreloads
- Framer badge and buy-template button
- Hydration/data attributes NOT referenced by CSS
"""

import re
import os

BASE = '/home/deca/Downloads/eko-luxury-rides'

def process_dir(dirname):
    files = []
    if os.path.isdir(f'{BASE}/{dirname}'):
        for f in os.listdir(f'{BASE}/{dirname}'):
            path = f'{BASE}/{dirname}/{f}'
            if os.path.isfile(path):
                files.append(f'{dirname}/{f}')
    return files

ALL_FILES = ['index.html', 'about', 'apartments', 'contact',
             'privacy-policy', 'refund-policy', 'terms-and-condition'] + \
            process_dir('cars') + process_dir('blog')

def strip_framer(html):
    before_len = len(html)

    # 1. Remove Framer comments
    html = re.sub(r'<!-- Made in Framer.*?-->', '', html)
    html = re.sub(r'<!-- Published.*?-->', '', html)

    # 2. Remove meta tags (only search-related, keep OG)
    html = re.sub(r'<meta name="framer-search-index[^>]*>', '', html)
    html = re.sub(r'<meta name="framer-search-index-fallback[^>]*>', '', html)
    html = re.sub(r'<meta name="generator"[^>]*>', '', html)

    # 3. Remove framer-specific favicon (keep if custom)
    html = re.sub(r'<link href="https://framerusercontent\.com/images/[^"]*" rel="icon"[^>]*>', '', html)
    html = re.sub(r'<link rel="apple-touch-icon" href="https://framerusercontent\.com[^>]*>', '', html)

    # 4. Remove OG images from framer CDN (keep OG title/desc)
    html = re.sub(r'<meta property="og:image" content="https://framerusercontent\.com[^>]*>', '', html)
    html = re.sub(r'<meta name="twitter:image" content="https://framerusercontent\.com[^>]*>', '', html)

    # 5. Remove framer editor bar detection script
    html = re.sub(r'<script>try\{if\(localStorage\.getItem\("__framer_force_showing_editorbar_since"\).*?</script>', '', html, flags=re.DOTALL)

    # 6. Remove modulepreload links to framer CDN (keep font preconnects)
    html = re.sub(r'<link rel="modulepreload"[^>]*href="https://framerusercontent\.com[^>]*>', '', html)
    # Also modulepreload for framer.com
    html = re.sub(r'<link rel="modulepreload"[^>]*href="https://framer\.com[^>]*>', '', html)

    # 7. Remove framer events/analytics
    html = re.sub(r'<script async src="https://events\.framer\.com/script\?v=2"[^>]*>.*?</script>', '', html, flags=re.DOTALL)

    # 8. Remove framer URL parameter preservation script
    html = re.sub(r'<script>!function\(\)\{var w="framer_variant".*?</script>', '', html, flags=re.DOTALL)

    # 9. Remove NODE_ENV detection script
    html = re.sub(r'<script>typeof document<"u"&&\(window\.process=.*?</script>', '', html, flags=re.DOTALL)

    # 10. Remove framer main bundle script
    html = re.sub(
        r'<script type="module" async data-framer-bundle="main" fetchpriority="low" src="https://framerusercontent\.com[^>]*>.*?</script>',
        '', html, flags=re.DOTALL
    )
    # Any external framer script
    html = re.sub(
        r'<script[^>]*src="https://framerusercontent\.com[^>]*>.*?</script>',
        '', html, flags=re.DOTALL
    )

    # 11. Remove handover data script
    html = re.sub(
        r'<script type="framer/handover"[^>]*>.*?</script>',
        '', html, flags=re.DOTALL
    )

    # 12. Remove framer badge container
    html = re.sub(r'<div id="__framer-badge-container">.*?</div>\s*', '', html, flags=re.DOTALL)

    # 13. Remove buy-this-template button
    html = re.sub(r'<a[^>]*class="framer-bOtdl[^"]*"[^>]*href="https://designtocodes\.com[^>]*>.*?</a>', '', html, flags=re.DOTALL)

    # 14. Remove SSR comment tokens (but NOT inside style tags)
    html = re.sub(r'<!--\$-->', '', html)
    html = re.sub(r'<!--/\$-->', '', html)

    # 15. Remove ssr-variant wrapper divs (keep content)
    # These are empty wrappers: <div class="ssr-variant hidden-...">
    # We need to be careful to only remove the opening tag and matching close
    html = re.sub(r'<div class="ssr-variant[^"]*"[^>]*>\s*', '', html)

    # 16. Remove only data attributes NOT used by CSS
    # CSS uses: data-border, data-framer-component-type, data-framer-stack-*, 
    # data-framer-cursor, data-framer-generated, data-framer-page-link-current,
    # data-nested-link, data-reset, data-selection, data-layout-template,
    # data-hide-scrollbars, data-is-present, data-lenis-prevent, data-text-fill,
    # data-width, data-framer-component-text-autosized
    #
    # SAFE to remove:
    for attr in ['data-framer-hydrate-v2',
                 'data-framer-appear-id',
                 'data-framer-appear-animation',
                 'data-framer-name',
                 'data-framer-generated-page',
                 'data-framer-page-optimized-at',
                 'data-framer-ssr-released-at',
                 'data-framer-preserve-params',
                 'data-framer-background-image-wrapper']:
        # Handle both boolean and key=value forms
        html = re.sub(f' {attr}(?:="[^"]*")?', '', html)

    # 17. Remove __framer_handoverData div
    html = re.sub(r'<div id="__framer__handoverData"[^>]*>.*?</div>', '', html, flags=re.DOTALL)

    # 18. Remove template-overlay div
    html = re.sub(r'<div id="template-overlay">.*?</div>', '', html, flags=re.DOTALL)

    # 19. Remove svg template container if empty
    html = re.sub(r'<div id="svg-templates">.*?</div>', '', html, flags=re.DOTALL)

    # 20. Clean up excessive whitespace
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
    
    print(f"✅ {fname}: {before:,} → {after:,} bytes (removed {before-after:,})")

print(f"\nDone! Processed {len(ALL_FILES)} files.")
