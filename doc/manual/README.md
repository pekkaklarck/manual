# Manual theme maintenance

The manual uses Material for MkDocs through ProperDocs. Styles and scripts live
in `docs/assets/`; template overrides live in `overrides/`.

## Translation documentation

`docs/appendix/update_translations.py` fills the marked sections in virtual copies
of the translations appendix and `docs/syntax/data.md` during `properdocs build`
and `properdocs serve`. The checked-in Markdown files keep these regions empty.
ProperDocs runs the script through `gen-files` before rendering pages. It reads the
bundled language definitions directly, including missing values, list order,
duplicates, version notes, and deprecations. Markdown escaping keeps translation
punctuation literal. Existing language heading anchors are retained.
Language subsections use H4 so that the global H3 TOC limit lists only languages
in the appendix.

Language coverage follows the bundled source version. Older source versions can
have fewer languages and no deprecation metadata; the updater documents only what
that source supplies. Deprecation tables are included when the API is available
and the language defines deprecated terms.

Review generated tables and language links in the built site or a standalone
export against `src/robot/conf/languages.py`. The checked-in Markdown files contain
the templates, not the generated translation values.

To export populated Markdown without building the site, run this from the project
root. Output is written to the selected directory, preserving the source templates:

```console
python doc/manual/docs/appendix/update_translations.py --output-dir .cache/translations
```

The script also works from another directory when invoked by its absolute path.
Both pages must have exactly one ordered pair of `START GENERATED CONTENT` and
`END GENERATED CONTENT` Markdown comments. The updater validates both pages
before rendering and preserves content outside the markers. Standalone exports
skip unchanged files and refuse to write into the source docs folder.

Run the focused tests with the build dependencies installed:

```console
python -m unittest discover -s doc/manual/tests -v
```

## Stylesheets

`properdocs.yml` loads the stylesheets in this order:

1. `fonts.css`: self-hosted fonts.
2. `theme.css`: color ramp and Material palette variables.
3. `highlight-light.css` and `highlight-dark.css`: syntax colors.
4. `navigation.css`: header, tabs, sidebars, drawer and search.
5. `extra.css`: article layout, typography, examples and footer.
6. `page-toc.css`: mobile page TOC.

Keep `page-toc.css` after `extra.css` to override shared disclosure styles.

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
