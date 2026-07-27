#!/usr/bin/env python3
"""
Surgical strip: ONLY removes Framer JS runtime and related external dependencies.
Does NOT touch ANY HTML structure, CSS, data attributes, or SSR markers.
Preserves EVERYTHING needed for layout and styling.
"""

import re, os

BASE = '/home/deca/Downloads/eko-luxury-rides'

def process_dir(d):
    fns = []
    if os.path.isdir(f'{BASE}/{d}'):
        for f in os.listdir(f'{BASE}/{d}'):
            p = f'{BASE}/{d}/{f}'
            if os.path.isfile(p): fns.append(f'{d}/{f}')
    return fns

ALL_FILES = (['index.html','about','apartments','contact',
              'privacy-policy','refund-policy','terms-and-condition']
             + process_dir('cars') + process_dir('blog'))

def strip(html):
    before = len(html)

    # 1. Modulepreload links to framer CDN
    html = re.sub(
        r'<link rel="modulepreload"[^>]*href="https://framerusercontent\.com[^>]*>',
        '', html)

    # 2. Modulepreload to framer.com (editor)
    html = re.sub(
        r'<link rel="modulepreload"[^>]*href="https://framer\.com[^>]*>',
        '', html)

    # 3. Editor bar detection script
    html = re.sub(
        r'<script>try\{if\(localStorage\.getItem\("__framer_force_showing_editorbar_since"\).*?</script>',
        '', html, flags=re.DOTALL)

    # 4. Main framer runtime bundle (the hydration culprit)
    html = re.sub(
        r'<script type="module" async data-framer-bundle="main" fetchpriority="low" src="https://framerusercontent\.com[^>]*>.*?</script>',
        '', html, flags=re.DOTALL)

    # 5. Any other external script from framerusercontent.com
    html = re.sub(
        r'<script[^>]*src="https://framerusercontent\.com[^>]*>.*?</script>',
        '', html, flags=re.DOTALL)

    # 6. Framer events analytics
    html = re.sub(
        r'<script async src="https://events\.framer\.com/script\?v=2"[^>]*>.*?</script>',
        '', html, flags=re.DOTALL)

    # 7. Framer handover data script
    html = re.sub(
        r'<script type="framer/handover"[^>]*>.*?</script>',
        '', html, flags=re.DOTALL)

    # 8. Framer URL parameter variant script
    html = re.sub(
        r'<script>!function\(\)\{var w="framer_variant".*?</script>',
        '', html, flags=re.DOTALL)

    # 9. NODE_ENV detection script
    html = re.sub(
        r'<script>typeof document<"u"&&\(window\.process=.*?</script>',
        '', html, flags=re.DOTALL)

    # 10. Framer appear-animation script (triggers runtime animation)
    html = re.sub(
        r'<script data-framer-appear-animation[^>]*>.*?</script>',
        '', html, flags=re.DOTALL)

    # 11. Framer badge container (the floating "Made in Framer" badge)
    html = re.sub(
        r'<div id="__framer-badge-container">.*?</div>\s*',
        '', html, flags=re.DOTALL)

    # 12. Buy this template button
    html = re.sub(
        r'<a[^>]*class="framer-bOtdl[^"]*"[^>]*href="https://designtocodes\.com[^>]*>.*?</a>',
        '', html, flags=re.DOTALL)

    # 13. __framer_handoverData div
    html = re.sub(
        r'<div id="__framer__handoverData"[^>]*>.*?</div>',
        '', html, flags=re.DOTALL)

    # 14. template-overlay div
    html = re.sub(
        r'<div id="template-overlay">.*?</div>',
        '', html, flags=re.DOTALL)

    # 15. Our old post-hydration fixContent scripts
    html = re.sub(
        r'<script>[\s\S]*?function fixContent[\s\S]*?</script>',
        '', html, flags=re.DOTALL)

    # 16. Empty script tags
    html = re.sub(r'<script>\s*</script>', '', html)

    # 17. SVG templates container (if empty after badge removal etc)
    # KEEP this - it contains all SVG icons used in the page

    # Clean up excessive blank lines
    html = re.sub(r'\n{3,}', '\n\n', html)

    return html

for fname in ALL_FILES:
    path = f'{BASE}/{fname}'
    if not os.path.exists(path):
        print(f"⚠️  {fname}: not found")
        continue
    with open(path) as f:
        html = f.read()
    before = len(html)
    html = strip(html)
    after = len(html)
    with open(path, 'w') as f:
        f.write(html)
    print(f"{'✅' if before != after else '  '} {fname}: {before:,} → {after:,} ({before-after:,} removed)")

print(f"\nDone! Processed {len(ALL_FILES)} files.")
