"""Fixes to social share previews.

1. Set the social preview title (`og:title`) on the front page to a custom value.
   This can be done conveniently and safely with the `on_page_context` hook.
   https://github.com/squidfunk/mkdocs-material/discussions/7597

2. Avoid description in generated social cards being clipped. This requires
   monkey patching `SocialPlugin._render_card` which is somewhat unsafe.
   https://github.com/squidfunk/mkdocs-material/issues/7610
"""

from material.plugins.social.plugin import SocialPlugin


def on_page_context(context, page, config, nav):
    if page.is_homepage:
        for meta in page.meta['meta']:
            if (meta.get('property') == 'og:title'
                    or meta.get('name') == 'twitter:title'):
                meta['content'] = 'Robot Framework Manual'


def _render_card(self, site_name, title, description):
    """Monkey patched function.

    Original has been copied from here:
    https://github.com/squidfunk/mkdocs-material/blob/cc1508f1dc58ad56b71e769b9033acd3ff63f02a/material/plugins/social/plugin.py#L251

    The only thing that has been changed is increasing description width
    from 826 to 1026 in the "Render page description block".
    """
    # Render background and logo
    image = self._render_card_background((1200, 630), self.color["fill"])
    image.alpha_composite(
        self._resized_logo_promise.result(),
        (1200 - 228, 64 - 4)
    )

    # Render site name
    font = self._get_font("Bold", 36)
    image.alpha_composite(
        self._render_text((826, 48), font, site_name, 1, 20),
        (64 + 4, 64)
    )

    # Render page title
    font = self._get_font("Bold", 92)
    image.alpha_composite(
        self._render_text((826, 328), font, title, 3, 30),
        (64, 160)
    )

    # Render page description
    font = self._get_font("Regular", 28)
    image.alpha_composite(
        self._render_text((1026, 80), font, description, 2, 14),
        (64 + 4, 512)
    )

    # Return social card image
    return image


if not hasattr(SocialPlugin, '_render_card'):
    raise ValueError('SocialPlugin structure has changed and monkey patching '
                     'will not work anymore!')

SocialPlugin._render_card = _render_card
