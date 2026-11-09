# Manual theme maintenance

The manual uses Material for MkDocs through ProperDocs. Keep custom presentation
in `docs/assets/` and template changes in `overrides/`.

## Stylesheets

`properdocs.yml` loads the stylesheets in this order:

1. `fonts.css`: self-hosted fonts.
2. `theme.css`: color ramp and Material palette variables.
3. `highlight-light.css` and `highlight-dark.css`: syntax highlighting.
4. `navigation.css`: header, version selector, section tabs, sidebars and drawer.
5. `extra.css`: article layout, typography, links, examples and footer.
6. `page-toc.css`: the phone page TOC, including overrides of the shared
   `details` and `summary` styles.

Keep component rules together. Some selectors must override Material's
structural rules, especially its nested-list spacing inside `details`. Check
the rendered result before reducing specificity or changing stylesheet order.

## Navigation

The layout breakpoints match Material: the right TOC appears at `60em`, and the
primary navigation becomes a sidebar at `76.25em`. The corresponding maximum
width queries follow Material's `59.9375em` and `76.1875em` values.

`navigation.js` adds button semantics and Enter/Space support to the theme's
checkbox labels at every width. Focus containment and background isolation
apply only to an open drawer. The adapter preserves the theme's click behavior,
restores the `inert` states it changes, and subscribes to `document$` because
instant navigation replaces the article and sidebar while keeping the header.
Its delegated phone TOC click handler closes the disclosure after selection.

Drawer submenu headers retain Material's `5.6rem` minimum height. Titles wrap
and align to the bottom; longer titles expand the header below the back arrow.
Anchor offsets account for the section tabs sharing the header's single row.

The phone TOC uses a native `details` disclosure rendered by `page-toc.html`,
included from `main.html`. Its opening and heading links work without JavaScript.

## Rendered log examples

The log examples in `execution/basics.md` and `extend/libraries.md` use HTML
tables to retain per-cell log classes and HTML message content. The outer
`md-typeset__scrollwrap` provides local scrolling and keyboard focus, with an
accessible region name. The inner `md-typeset__table` supplies Material's table
layout. Keep the blank line after each HTML block so Markdown headings and prose
continue to parse correctly.

## Upgrading Material

The header override and navigation adapter were reviewed against Material
9.7.6. The custom header moves the drawer toggle before the logo, gives the
version selector its own host, and places the section tabs in the header row.
See the [layout decision](https://github.com/pekkaklarck/manual/issues/30).

When upgrading, compare `overrides/partials/header.html` with the installed
`material/templates/partials/header.html`, incorporate upstream changes, and
update the baseline comments. Check the DOM assumptions in `navigation.js` and
the theme-specific selectors and offsets in `navigation.css`.

Run `properdocs build` with API generation enabled, then preview the site and
check both palettes at phone, tablet and desktop widths:

- Header logo, title, section tabs, palette and search controls.
- Current-page and current-heading markers, plus anchor visibility after jumps.
- Keyboard focus visibility and order, Enter/Space, Back, Escape and drawer
  focus containment. Desktop navigation must allow focus to leave the sidebar.
- Long drawer titles, scrolling examples and phone TOC links.
- Instant navigation and resizing between drawer and sidebar layouts.
- Accessible names, reading order and focus behavior with a screen reader.

Use a mike preview with `versions.json` to check the version menu and page title
together; an ordinary local build has no version metadata.
