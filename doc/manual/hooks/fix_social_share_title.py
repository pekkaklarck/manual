"""Set the social preview title (`og:title`) on the front page to a custom value.

https://github.com/squidfunk/mkdocs-material/discussions/7597
"""


def on_page_context(context, page, config, nav):
    if page.is_homepage:
        for meta in page.meta['meta']:
            if (meta.get('property') == 'og:title'
                    or meta.get('name') == 'twitter:title'):
                meta['content'] = 'Robot Framework Manual'
