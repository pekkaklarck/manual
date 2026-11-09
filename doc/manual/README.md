# Manual theme maintenance

The manual uses Material for MkDocs through ProperDocs. Keep custom presentation
in `docs/assets/` and template changes in `overrides/`.

## Stylesheets

`properdocs.yml` loads the stylesheets in this order:

1. `fonts.css`: self-hosted fonts.
2. `theme.css`: color ramp and Material palette variables.
3. `highlight-light.css` and `highlight-dark.css`: syntax colors.
4. `navigation.css`: header, tabs, sidebars, drawer and search.
5. `extra.css`: article layout, typography, examples and footer.
6. `page-toc.css`: mobile page TOC.

Keep `page-toc.css` after `extra.css` to override shared disclosure styles. Check
rendered pages before changing selector specificity or stylesheet order.

## Navigation

Match Material's breakpoints: the right TOC appears at `60em` and the primary
sidebar at `76.25em`. Use `59.9375em` and `76.1875em` for their maximum-width
queries.

`navigation.js` provides keyboard access and accessible control names. Instant
navigation replaces the article and sidebar, so reinitialize page controls
through `document$`. Contain focus only in an open drawer and restore the `inert`
states the adapter changes. Keep `preventScroll` when focusing sliding drawer
panes to avoid scrolling them out of view.

Search emphasizes matches in result previews only; keep `search.highlight`
disabled. Support both Tab and arrow keys through results, and keep clear
available inside the collapsed desktop search bar without opening results.

The mobile TOC in `overrides/partials/page-toc.html` uses native `details` and
must work without JavaScript.

## Rendered log examples

Log examples in `execution/basics.md` and `extend/libraries.md` use HTML tables
to preserve cell classes and message markup. Keep both Material wrappers
(`md-typeset__scrollwrap` and `md-typeset__table`), the accessible region name,
and `tabindex="0"` on the scroll wrapper. Leave a blank line after HTML blocks
so Markdown continues to parse.

## Upgrading Material

The current baseline is Material **9.7.6**. See the
[header layout decision](https://github.com/pekkaklarck/manual/issues/30).

Compare our `partials/header.html` and `partials/javascripts/outdated.html`
overrides with Material's installed templates and update their baseline comments.
The latter supplies the URL base required by the version banner. Check DOM
assumptions in `navigation.js` and selectors and offsets in `navigation.css`.

Run `properdocs build` with API generation enabled. Preview both palettes at
mobile, tablet and desktop widths, checking:

- Header layout and controls, version menu and long drawer titles.
- Visible keyboard focus, Tab/Shift+Tab, arrows, Enter/Space, Escape and drawer
  Back. Contain focus in the open drawer; allow it to leave the desktop sidebar.
- Current-page/heading markers, TOC links and anchor visibility after jumps.
- Instant navigation, resizing across breakpoints and search result groups.
- Example scrolling and code/line-number alignment at larger text sizes.
- Control names, reading order and focus with a screen reader.

Use a mike preview with `versions.json` to check version controls, page titles
and the outdated banner; an ordinary local build has no version metadata.
