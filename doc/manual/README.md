# Manual theme maintenance

The manual uses Material for MkDocs through ProperDocs. Styles and scripts live
in `docs/assets/`; template overrides live in `overrides/`.

## Stylesheets

`properdocs.yml` loads the stylesheets in this order:

1. `fonts.css`: self-hosted fonts.
2. `theme.css`: color ramp and Material palette variables.
3. `highlight-light.css` and `highlight-dark.css`: syntax colors.
4. `navigation.css`: header, tabs, sidebars, drawer and search.
5. `extra.css`: article layout, typography, examples and footer.
6. `page-toc.css`: mobile page TOC.

Keep `page-toc.css` after `extra.css` to override shared disclosure styles.

## External links

`external-links.js` adds Material's bundled Octicons external-link symbol to
article text links outside this manual. It runs on `document$`, like the navigation
adapter, and skips links already marked. The template and accessible description
live in `overrides/main.html`; icon size and spacing live in `extra.css`.

The boundary uses the current origin and the configured `site_url` path, with
mike's canonical version suffix removed so all manual versions stay internal.
Other projects on the same host are external. Email links, image links, code
blocks and navigation controls are excluded. Link targets and existing styles
stay unchanged. Without JavaScript, links keep their normal behavior.

## Navigation

Match Material's breakpoints: `60em` for the right TOC and `76.25em` for the
primary sidebar; use `59.9375em` and `76.1875em` for maximum-width queries.

- Place the version selector between the tabs and theme toggle, following the
  [RFCP syllabus](https://robotframework.org/robotframework-RFCP-syllabus/docs/overview).
  Its host must be the first `.md-header__topic` for Material's mike integration.
- Select the bundled Octicons theme icons in `properdocs.yml`. Material handles
  system preference and saved choices.
- Reinitialize page controls through `document$` after instant navigation.
  Keep labels and the native mobile TOC usable without JavaScript.
- Contain focus only in the open drawer, restore changed `inert` states, and use
  `preventScroll` when focusing drawer panes.
- Focus the destination heading or fragment after instant navigation, preserving
  scroll position. Do not force focus on initial load. After a mobile TOC jump,
  focus the heading before collapsing the TOC.
- Keep `search.highlight` disabled; highlight result previews only. Support Tab
  and arrows through results. Escape returns focus to the search opener or input;
  Tab at either end closes search. Clearing collapsed desktop search must not
  open results.
- Hide closed search controls and results with `visibility`; opacity and size
  alone leave them accessible.

## Rendered log examples

HTML log tables in `execution/basics.md` and `extend/libraries.md` need both
Material wrappers (`md-typeset__scrollwrap` and `md-typeset__table`), a region name,
and `tabindex="0"` on the scroll wrapper. Leave a blank line after HTML blocks.

## Example page bundles

Keep example HTML, images, and source files beside their page's `index.md`.
Screenshots with interactive HTML examples use Markdown image links to open
the examples. Preserve the source's display widths with image attributes such as
`{ width="500" }`; the theme scales images down on smaller screens. Keep log/report
companion links relative to the same bundle.

The Libdoc and execution artifact examples come from the
[User Guide source at `7c1c9fb04`](https://github.com/robotframework/robotframework/tree/7c1c9fb04/doc/userguide/src).
They are snapshots illustrating the accompanying screenshots; their generated
HTML does not need to be regenerated during ordinary documentation builds.

## Upgrading Material

Last compatibility review: Material **9.8.1**. See the
[header layout decision](https://github.com/pekkaklarck/manual/issues/30).

Compare `partials/header.html` and `partials/javascripts/outdated.html`
with the installed templates. Preserve the
outdated banner's URL base. Check DOM assumptions in `navigation.js` and selectors
and offsets in `navigation.css`.

Run `properdocs build` with API generation enabled. Use a mike preview with
`versions.json` to check version controls and the outdated banner.
Update the reviewed version above after completing these checks.

## Verification

Check both palettes at mobile, tablet and desktop widths, including long articles
and nested API pages:

- Header controls, version menu, long titles and resizing across breakpoints.
- Keyboard order, visible focus, drawer exits and search navigation.
- Current-page markers, TOC jumps and focus after instant navigation.
- Example scrolling and code/line-number alignment at larger text sizes.
- With NVDA or VoiceOver: landmarks, control names, roles, expanded states and
  reading order. Hidden controls must be unavailable; Skip to content must reach
  the article. Material places the desktop right TOC before the article in the DOM.

Lighthouse and browser checks do not replace screen reader testing.
