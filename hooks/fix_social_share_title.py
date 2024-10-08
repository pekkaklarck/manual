"""Hook to fix the social preview title (`og:title`) on the front page.

https://github.com/squidfunk/mkdocs-material/discussions/7597
"""


def on_page_context(context, page, config, nav):
    for meta in page.meta.get('meta', []):
        if meta.get('property') == 'og:title' and meta.get('content') == 'Manual':
            meta['content'] = 'Robot Framework Manual'
