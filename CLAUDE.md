# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

The Robot Framework Manual: a MkDocs site (built with [ProperDocs](https://properdocs.org/), a wrapper around
MkDocs + Material) that is replacing the old RST User Guide and the Sphinx API docs. Content is Markdown under
`doc/manual/docs/`; configuration is `properdocs.yml` (the `mkdocs.yml` equivalent). There is no test suite or
linter; verifying a change means building the site and looking at it.

## Git rules

- Never commit unless explicitly asked in the current conversation. Leave changes in the working tree.
- When asked to commit, the author is the repository's configured git user (René), and the message contains
  no Claude attribution: no `Co-Authored-By`, no "Generated with Claude Code", no session trailer.

## Commands

```sh
python -m pip install -r requirements.txt      # Python 3.13+
properdocs serve                               # live preview at http://127.0.0.1:8000/manual/
DO_NOT_GENERATE_API_DOCS=True properdocs serve # skip the slow mkdocstrings API build (~10 s+)
properdocs build --strict                      # full build; fails on broken cross-refs
```

`properdocs` accepts the same subcommands as `mkdocs`. Set `DO_NOT_GENERATE_API_DOCS` whenever the change
does not touch `src/` or `doc/manual/docs/api/`.

## Architecture

### Generated pages

Three `generate.py` scripts run via the `gen-files` plugin at build time and create pages that do not exist
on disk (they are also excluded from the site via the `exclude` plugin):

- `doc/manual/docs/install/generate.py` — copies root `INSTALL.md` to `install/index.md`. **Edit
  `INSTALL.md`, never `install/index.md`.**
- `doc/manual/docs/api/generate.py` — walks `src/robot/**/*.py`, writes one `::: module` stub per public
  module and `api/nav.md`, which `literate-nav` turns into the API navigation (`nav: - API: api/` in
  `properdocs.yml`). Private modules (leading `_`) are skipped.
- `doc/manual/docs/libraries/generate.py` — runs Libdoc on the standard libraries listed in the script and
  emits `libraries/<Name>.html` + `.json`. Add a library to that list to publish it.

### `src/robot/`

A copy of the Robot Framework core source, kept here only so mkdocstrings and Libdoc can import it.
Docstrings are being converted from reStructuredText to Markdown page by page (see the warning in
`doc/manual/docs/api/index.md`); `robot.api.deco` and `robot.run` are the finished examples to imitate.

### Content conventions

- Pages converted from the RST User Guide keep `<a id="old-anchor"></a>` lines before headings so old
  deep links still resolve. Keep them when editing headings.
- Cross-page links are plain relative Markdown links with anchors (`suites.md#test-suite`); mkdocstrings
  cross-refs use `[robot.api][]` autorefs syntax.
- Robot code blocks use the `robotframework` fence language. Callouts use Material `!!! note` admonitions.
- `glossary.md` uses definition-list syntax; the `ezglossary` plugin auto-links terms across pages.
- Section navigation is hand-maintained in the `nav:` block of `properdocs.yml`; a new page needs an
  entry there.
- `doc/manual/overrides/main.html` only customises the mike "outdated version" banner.

### Design

The visual design follows robotframework.org. In order of authority:

1. `~/Source/robotframework/foundation-web/web-components/assets/css/themes/base.css` — the homepage
   design system (colour ramp `--robot-*`, type families, semantic tokens).
2. `~/Source/MarketSquare/robotframeworkguides/website/src/css/custom.css` — the Docusaurus Guides, already
   ported from the homepage; the closest reference for a long-form docs site.
3. This repo, three stylesheets loaded in this order:
   - `assets/fonts.css` — self-hosted fonts and `--rf-ff-*` type tokens (`theme.font: false` keeps Material
     from loading Roboto).
   - `assets/theme.css` — the `--rf-*` colour ramp and its mapping onto Material's `--md-*` variables. The ramp
     is declared once for light and once, reversed, under `[data-md-color-scheme="slate"]`, so a component rule
     is written **once** against a ramp step and is correct in both schemes. Never add a dark override to a
     `--rf-*` colour in a component rule — it would flip twice.
   - `assets/extra.css` — component rules (header, sidebars, headings, code plate, prose, footer, layout).
     Colours are `rgb(var(--rf-N) / alpha)`, never hex; the footer is the one fixed-dark exception.
   - Layout: no centred page grid (`.md-grid { max-width: none }`); article column caps at 1000px; page TOC
     hugs it.

Fonts are copied from the Guides' `static/fonts/`; keep the two in sync. IBM Plex Sans for body text is a
deliberate exception to the homepage's monospace running text, because the Manual is prose-heavy.

### Deployment

GitHub Actions deploy with `mike`: pushes to `main` publish the `dev` version; stable tags (`v7.1`,
not `v7.2rc1`) publish `<major>.<minor>` and move the `latest` alias. Site pages are pushed to the
`gh-pages` branch, so never commit build output.
