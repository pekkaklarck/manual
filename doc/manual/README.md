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
through `document$`. It enhances navigation labels into native buttons; the
original labels remain the fallback without JavaScript. Contain focus only in
an open drawer and restore the `inert` states the adapter changes. Keep
`preventScroll` when focusing sliding drawer panes to avoid scrolling them out
of view.

Search emphasizes matches in result previews only; keep `search.highlight`
disabled. Support both Tab and arrow keys through results, and keep clear
available inside the collapsed desktop search bar without opening results.
Hide closed search controls and results with `visibility`, since Material's
opacity and size changes alone leave them exposed to assistive technology.
Escape returns focus to the search opener on phones or the collapsed desktop
input; Tab at either end closes search and continues through the page.

After instant navigation, focus the destination heading (or fragment target)
without changing scroll position. Keep initial page loads free of forced focus.
Move focus to the heading before collapsing the phone TOC after a link is used.

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

## Lighthouse manual accessibility checks

Lighthouse lists these unscored checks even when its automated audits pass.
Use a versioned preview at phone, tablet and desktop widths in both palettes.
Include a long article, a deeply nested API page, search results and the footer.

| Check | What to verify in the manual |
| --- | --- |
| Keyboard focus | Tab to header controls, version links, navigation, page TOC, code copy buttons and footer links. Each focused control must have a visible indicator. |
| Purpose and state | Identify controls without hovering. Check disclosure arrows, current-page markers and expanded/collapsed announcements. |
| Tab order | Use Tab and Shift+Tab from the skip link through the page. Closed drawers, search panels and result groups must not receive focus. |
| DOM and visual order | Compare the screen reader's reading sequence with the visible groups. Material places the desktop right TOC before the article in the DOM; assess that navigation-first sequence and verify that Skip to content reaches the article. |
| Focus traps | Leave desktop navigation and search in both directions. The open drawer intentionally contains Tab; Back, Close and Escape must provide exits. |
| Focus after changes | Check drawer panes, search open/close, instant page changes and phone TOC jumps. Focus must reach the relevant control or heading without an unexpected scroll. Search result updates should leave focus in the query. |
| Landmarks | With a screen reader, navigate to the header, main content, navigation, search and footer. Confirm their names and that content can be reached efficiently. |
| Hidden content | With a screen reader, verify that closed drawers, inactive drawer panes, closed phone search and collapsed results are unavailable. Content below the viewport must remain available when it is part of the page. |
| Control labels | Listen to icon controls and submenu buttons. Their names must explain their action and identify their target where needed. |
| Control roles | Confirm that enhanced controls are announced as buttons, native disclosures as expandable controls, and links as links. Check that expanded states follow activation. |

Browser keyboard tests and accessibility-tree inspection help catch regressions,
but do not replace listening with a screen reader such as NVDA or VoiceOver.
