# Robot Framework Design Port Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the Manual (Material for MkDocs) look like the Robot Framework Guides (Docusaurus), which are themselves a port of robotframework.org's design system.

**Architecture:** All work is CSS layered on top of Material for MkDocs; no template overrides and no theme fork. A new `theme.css` declares the robotframework.org colour ramp (`--rf-*`) once for light and once, reversed, for dark, and maps it onto Material's own `--md-*` variables so most of Material recolours itself. `extra.css` then restyles the handful of components whose look Material does not expose through variables (header, headings, code plate, sidebars, footer). Dark mode is `body[data-md-color-scheme="slate"]`, which Material stamps; the ramp flips there so every rule is written once.

**Tech Stack:** ProperDocs 1.6 (MkDocs fork) + Material for MkDocs, Pygments-generated highlight CSS, self-hosted fonts (already done in `assets/fonts.css`). Verification is a local build served with `python3 -m http.server` and inspected with the Playwright MCP browser at 1440 / 1024 / 390 px, light and dark.

**Spec:** There is no separate spec. The sources of truth, in order of authority:
1. `~/Source/robotframework/foundation-web/web-components/assets/css/themes/base.css` — the ramp and semantic tokens.
2. `~/Source/MarketSquare/robotframeworkguides/website/src/css/custom.css` — the same system applied to a docs site; every component rule below is a translation of a rule in this file.
3. Decisions made in conversation on 2026-09-17: header is **ground-coloured like the Guides** (not black like the homepage, not teal); body text is **IBM Plex Sans** on purpose; layout is left nav + right page TOC (`toc.integrate` already removed).

## Global Constraints

- **Never commit.** Leave every change in the working tree; the repository owner commits. (Project `CLAUDE.md`, "Git rules".)
- Build with `DO_NOT_GENERATE_API_DOCS=True .venv/bin/properdocs build -q -d <scratch>/site` — API generation is slow and irrelevant to CSS.
- Serve for inspection with `python3 -m http.server 8766 --bind 127.0.0.1` from the built dir, **outside the sandbox** (a sandboxed server accepts no connections). Kill it when done: `pkill -f "http.server 8766"`.
- Browser checks: Playwright MCP (`browser_navigate`, `browser_resize`, `browser_evaluate`, `browser_take_screenshot`). Screenshots must be saved under `.playwright-mcp/` in the repo (the only allowed root) and that directory deleted afterwards — it is not gitignored.
- Switch schemes in the browser with `document.body.setAttribute('data-md-color-scheme', 'slate')` / `'default'`.
- Colour values are space-separated RGB channels (`0 192 181`) so they can be used as `rgb(var(--rf-500) / 0.2)`. Never write a hex colour in a component rule; reach for a ramp step.
- **A `--rf-*` step must never get a dark-mode override in a component rule.** The ramp flips once under `slate`; a second override flips it twice.
- No `!important` unless a Material rule already carries one (documented per task).
- `assets/highlight-*.css` are generated — do not edit them; override their `.highlight { background }` from `extra.css` instead.
- Load order in `properdocs.yml` `extra_css`: `fonts.css`, `theme.css`, `highlight-light.css`, `highlight-dark.css`, `extra.css`. `extra.css` last so component rules win.

## File Structure

| File | Responsibility |
|---|---|
| `doc/manual/docs/assets/fonts.css` | (exists) `@font-face` + `--rf-ff-*` type tokens. Unchanged by this plan. |
| `doc/manual/docs/assets/theme.css` | **New.** The `--rf-*` colour ramp (light + reversed dark), semantic tokens, radii, and the `--md-*` variable mapping. Nothing but custom properties. |
| `doc/manual/docs/assets/extra.css` | (exists) Component rules: header/tabs, headings, links, code plate, sidebars, prose elements, footer, layout. Existing rules for definition lists, glossary refs and content width stay. |
| `properdocs.yml` | `extra_css` order; drop the `primary`/`accent` palette keys that `theme.css` supersedes. |
| `CLAUDE.md` | Design section: add `theme.css` to the file list and the "ramp flips once" rule. |

---

### Task 1: Colour ramp and Material variable mapping

**Files:**
- Create: `doc/manual/docs/assets/theme.css`
- Modify: `properdocs.yml` (`extra_css`, `theme.palette`)
- Modify: `doc/manual/docs/assets/extra.css:1-5` (remove the `--md-primary-fg-color` block)

**Interfaces:**
- Produces: custom properties every later task consumes — `--rf-0`…`--rf-1000`, `--rf-ground`, `--rf-text`, `--rf-accent-text`, `--rf-accent-indicator`, `--rf-surface-panel`, `--rf-surface-line`, `--rf-surface-card`, `--rf-r-sm`, `--rf-r-md`, `--rf-r-lg`.

- [ ] **Step 1: Write `theme.css`**

```css
/* Robot Framework colour system, ported from
   foundation-web/web-components/assets/css/themes/base.css via the Guides'
   custom.css. Nothing but custom properties lives here.

   THE RAMP encodes distance from the page ground, not absolute lightness:
   0 is the ground itself, 500 is the brand teal and never moves, 1000 is the
   far end. The `slate` block declares the ramp in reverse, so a rule written
   ONCE against a step is right under both schemes. Adding a dark override to
   a --rf-* colour in a component rule makes it flip twice — that is a bug.

   Values are RGB channels so a rule can write `rgb(var(--rf-500) / 0.2)`. */

:root {
  --rf-0: 255 255 255;
  --rf-50: 230 248 246;
  --rf-100: 204 230 227;
  --rf-200: 184 227 224;
  --rf-300: 92 214 207;
  --rf-400: 46 203 194;
  --rf-500: 0 192 181;
  --rf-600: 1 150 143;
  --rf-700: 31 102 98;
  --rf-800: 29 48 47;
  --rf-900: 18 26 28;
  --rf-950: 9 12 13;
  --rf-1000: 0 0 0;

  /* The page ground is a neutral, deliberately not a ramp step. */
  --rf-ground: 240 240 240;

  /* Semantic tokens. Step 700 rather than 500 carries text: the brand teal
     on the light ground measures 1.8:1, far under AA. */
  --rf-text: var(--rf-950);
  --rf-accent-text: var(--rf-700);
  --rf-accent-indicator: var(--rf-500);
  --rf-surface-panel: rgb(var(--rf-100));
  --rf-surface-line: rgb(var(--rf-200));
  --rf-surface-card: rgb(var(--rf-0));

  --rf-r-sm: 4px;
  --rf-r-md: 6px;
  --rf-r-lg: 8px;
}

[data-md-color-scheme="slate"] {
  --rf-0: 0 0 0;
  --rf-50: 9 12 13;
  --rf-100: 18 26 28;
  --rf-200: 29 48 47;
  --rf-300: 31 102 98;
  --rf-400: 1 150 143;
  --rf-500: 0 192 181;
  --rf-600: 46 203 194;
  --rf-700: 92 214 207;
  --rf-800: 184 227 224;
  --rf-900: 204 230 227;
  --rf-950: 230 248 246;
  --rf-1000: 255 255 255;

  --rf-ground: 34 34 34;

  /* Re-declared on purpose: a var() inside a custom property resolves on the
     element that DECLARES it, so the :root copies would keep light-ramp
     values after the ramp above is reversed. */
  --rf-text: var(--rf-950);
  --rf-accent-text: var(--rf-700);
  --rf-accent-indicator: var(--rf-500);
  --rf-surface-panel: rgb(var(--rf-100));
  --rf-surface-line: rgb(var(--rf-200));
  --rf-surface-card: rgb(var(--rf-100));
}

/* Material reads these. Declared on the same two selectors so each one
   resolves against its own ramp. */
:root,
[data-md-color-scheme="slate"] {
  --md-default-bg-color: rgb(var(--rf-ground));
  --md-default-fg-color: rgb(var(--rf-text));
  --md-default-fg-color--light: rgb(var(--rf-text) / 0.7);
  --md-default-fg-color--lighter: rgb(var(--rf-text) / 0.45);
  --md-default-fg-color--lightest: rgb(var(--rf-text) / 0.12);

  /* Header and tabs (Task 2 restyles them; these keep Material's own header
     rules coherent in the meantime). */
  --md-primary-fg-color: rgb(var(--rf-0));
  --md-primary-fg-color--light: rgb(var(--rf-50));
  --md-primary-fg-color--dark: rgb(var(--rf-100));
  --md-primary-bg-color: rgb(var(--rf-text));
  --md-primary-bg-color--light: rgb(var(--rf-text) / 0.7);

  /* Accent: hover states, focus rings, active toggles. */
  --md-accent-fg-color: rgb(var(--rf-600));
  --md-accent-fg-color--transparent: rgb(var(--rf-500) / 0.1);
  --md-accent-bg-color: rgb(var(--rf-0));

  --md-typeset-a-color: rgb(var(--rf-accent-text));

  /* Code surface: robot-100 on light, robot-50 on dark — the pair the source
     site uses. Written per scheme below because it is the one place a single
     ramp step cannot do the job. */
  --md-code-fg-color: rgb(var(--rf-text));
  --md-code-hl-color: rgb(var(--rf-500));
  --md-code-hl-color--light: rgb(var(--rf-500) / 0.12);

  --md-typeset-table-color: rgb(var(--rf-700) / 0.25);
  --md-typeset-table-color--light: rgb(var(--rf-500) / 0.08);
  --md-typeset-mark-color: rgb(var(--rf-500) / 0.3);
  --md-typeset-kbd-color: rgb(var(--rf-100));
  --md-typeset-kbd-accent-color: rgb(var(--rf-50));
  --md-typeset-kbd-border-color: rgb(var(--rf-700) / 0.25);

  --md-admonition-fg-color: rgb(var(--rf-text));
  --md-admonition-bg-color: rgb(var(--rf-100) / 0.5);

  /* Footer is a dark island (Task 6). Written here so the variables exist. */
  --md-footer-fg-color: rgb(230 248 246);
  --md-footer-fg-color--light: rgb(204 230 227);
  --md-footer-fg-color--lighter: rgb(184 227 224);
  --md-footer-bg-color: rgb(18 26 28);
  --md-footer-bg-color--dark: rgb(9 12 13);

  --md-shadow-z1: none;
  --md-shadow-z2: none;
  --md-shadow-z3: none;
}

:root {
  --md-code-bg-color: rgb(var(--rf-100));
  --md-code-bg-color--light: rgb(var(--rf-100) / 0.9);
  --md-code-bg-color--lighter: rgb(var(--rf-100) / 0.54);
}

[data-md-color-scheme="slate"] {
  --md-code-bg-color: rgb(var(--rf-50));
  --md-code-bg-color--light: rgb(var(--rf-50) / 0.9);
  --md-code-bg-color--lighter: rgb(var(--rf-50) / 0.54);
  color-scheme: dark;
}
```

- [ ] **Step 2: Register it and drop the superseded palette keys**

In `properdocs.yml`:

```yaml
extra_css:
  - assets/fonts.css    # Self-hosted fonts shared with robotframework.org, see the file for details.
  - assets/theme.css    # Colour ramp and Material variable mapping, see the file for details.
  - assets/highlight-light.css
  - assets/highlight-dark.css
  - assets/extra.css
```

In each of the three `palette:` entries, delete the line `primary: custom` (Material then applies no palette colour class, and `theme.css` owns every `--md-primary-*` value). Leave `scheme:` and `toggle:` as they are.

- [ ] **Step 3: Remove the old primary-colour block from `extra.css`**

Delete these five lines at the top of `doc/manual/docs/assets/extra.css`:

```css
:root {
  --md-primary-fg-color: #00c0b5;
  --md-primary-fg-color--light: #00c0b5;
  --md-primary-fg-color--dark: #00c0b5;
}
```

- [ ] **Step 4: Build and verify the variables resolve in both schemes**

Build, serve, open `http://127.0.0.1:8766/syntax/tests/` at 1440×900 and run:

```js
() => {
  const read = () => {
    const cs = getComputedStyle(document.body);
    return {
      bg: cs.getPropertyValue('--md-default-bg-color').trim(),
      link: getComputedStyle(document.querySelector('.md-content a')).color,
      rf700: cs.getPropertyValue('--rf-700').trim(),
      bodyBg: cs.backgroundColor,
    };
  };
  const light = read();
  document.body.setAttribute('data-md-color-scheme', 'slate');
  const dark = read();
  document.body.setAttribute('data-md-color-scheme', 'default');
  return { light, dark };
}
```

Expected:
- `light.rf700` = `31 102 98`, `light.link` = `rgb(31, 102, 98)`, `light.bodyBg` = `rgb(240, 240, 240)`
- `dark.rf700` = `92 214 207`, `dark.link` = `rgb(92, 214, 207)`, `dark.bodyBg` = `rgb(34, 34, 34)`

If `dark.link` is still the light teal, the `slate` re-declaration of `--rf-accent-text` is missing.

- [ ] **Step 5: Screenshot both schemes, then leave the change in the working tree**

Take `.playwright-mcp/t1-light.png` and `.playwright-mcp/t1-dark.png`. The page must be readable in both (grey ground, dark-teal links, no white-on-white). The header will look wrong (pale, with Material's default text colour) — Task 2 fixes it. Do not commit.

---

### Task 2: Header, tabs and search

**Files:**
- Modify: `doc/manual/docs/assets/extra.css` (remove the "Advertise search shortcut" block; add header rules)
- Modify: `doc/manual/docs/assets/fonts.css:60-70` (the `.md-tabs__link` rule moves into `extra.css` alongside the other header rules)

**Interfaces:**
- Consumes: `--rf-0`, `--rf-700`, `--rf-accent-text`, `--rf-text`, `--rf-ff-nav`, `--rf-ff-display` from Tasks 1 and `fonts.css`.

Target look (Guides, `.navbar`, `.navbar__title`, `.navbar__link`): header on the page ground colour, 1px bottom rule at `rgb(var(--rf-700) / 0.18)`, no shadow, title in OCR-A uppercase, nav links in JetBrains Mono 600, active tab in accent text colour.

- [ ] **Step 1: Delete the search-shortcut pseudo-element**

Remove the whole block starting `/* Advertise search shortcut */` through its closing `}` in `extra.css`. Its hard-coded white colours assume the teal header.

- [ ] **Step 2: Move the tabs font rule out of `fonts.css`**

Delete from `fonts.css`:

```css
.md-tabs__link {
  font-family: var(--rf-ff-nav);
  font-weight: 600;
}
```

(`fonts.css` keeps the `h1` / `.md-ellipsis` display-font rule — that is typography, not chrome.)

- [ ] **Step 3: Add the header rules to `extra.css`**

Append:

```css
/* ============================================================================
   HEADER — ground-coloured with a thin rule, as on the Guides. Material paints
   the header with --md-primary-fg-color (now the ground) and its text with
   --md-primary-bg-color (now ink); the rules here add the rule line and the
   type treatment Material has no variable for.
   ========================================================================== */
.md-header {
  border-bottom: 1px solid rgb(var(--rf-700) / 0.18);
  box-shadow: none;
}

/* Material re-adds a shadow once the page scrolls. */
.md-header[data-md-state="shadow"],
.md-header--shadow {
  box-shadow: none;
  transition: none;
}

.md-header__title .md-ellipsis {
  font-family: var(--rf-ff-display);
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: -0.05em;
}

.md-tabs {
  background: transparent;
  border-bottom: 1px solid rgb(var(--rf-700) / 0.18);
}

/* The header rule and the tabs rule would stack into a 2px line. */
.md-header + .md-tabs,
.md-header ~ .md-tabs {
  margin-top: -1px;
}

.md-tabs__link {
  font-family: var(--rf-ff-nav);
  font-weight: 600;
  opacity: 1;
  color: rgb(var(--rf-text) / 0.75);
}

.md-tabs__link:hover,
.md-tabs__link--active {
  color: rgb(var(--rf-accent-text));
}

/* Search box sits on the ground, so it needs an edge of its own. */
.md-search__form {
  background: rgb(var(--rf-0));
  border: 1px solid rgb(var(--rf-700) / 0.25);
  border-radius: var(--rf-r-sm);
  box-shadow: none;
}

.md-search__input,
.md-search__input::placeholder,
.md-search__form .md-search__icon {
  color: rgb(var(--rf-text) / 0.7);
}

/* Palette toggle and repo link inherit the header text colour. */
.md-header__button,
.md-header__source {
  color: rgb(var(--rf-text));
}
```

- [ ] **Step 4: Build and verify**

Open `/syntax/tests/` at 1440×900 and run:

```js
() => {
  const cs = s => getComputedStyle(document.querySelector(s));
  return {
    headerBg: cs('.md-header').backgroundColor,
    headerRule: cs('.md-header').borderBottomWidth + ' ' + cs('.md-header').borderBottomColor,
    titleFont: cs('.md-header__title .md-ellipsis').fontFamily.split(',')[0],
    tabFont: cs('.md-tabs__link').fontFamily.split(',')[0],
    activeTab: cs('.md-tabs__link--active').color,
    searchBg: cs('.md-search__form').backgroundColor,
    overflow: document.documentElement.scrollWidth <= innerWidth,
  };
}
```

Expected (light): `headerBg` = `rgb(255, 255, 255)`, `headerRule` starts with `1px`, `titleFont` = `"OCR-A"`, `tabFont` = `"JetBrains Mono"`, `activeTab` = `rgb(31, 102, 98)`, `searchBg` = `rgb(255, 255, 255)`, `overflow` = `true`.

Switch to `slate` and re-run: `headerBg` = `rgb(0, 0, 0)`, `activeTab` = `rgb(92, 214, 207)`.

- [ ] **Step 5: Check 390 px**

Resize to 390×844, screenshot `.playwright-mcp/t2-mobile.png`. The hamburger, title and search icon must be visible against the ground and `document.documentElement.scrollWidth <= innerWidth` must hold. Do not commit.

---

### Task 3: Headings and links

**Files:**
- Modify: `doc/manual/docs/assets/fonts.css:60-66` (delete the `h1` / `.md-ellipsis` rule; headings are handled in `extra.css` now)
- Modify: `doc/manual/docs/assets/extra.css` (replace the `h2 { font-weight: 500 }` rule)

**Interfaces:**
- Consumes: `--rf-ff-display`, `--rf-accent-text`, `--rf-800`, `--rf-500`, `--rf-text`.

Target (Guides `.markdown h1…h6`, `.markdown a`): all headings in OCR-A, weight 600, `letter-spacing: -0.1em`, `text-wrap: balance`; `h2`/`h3` in accent text colour, `h1` stays ink; links weight 600, underlined with the brand pivot, hover colour step 800.

- [ ] **Step 1: Remove the heading rule from `fonts.css`**

Delete:

```css
.md-typeset h1,
header .md-ellipsis {
  font-family: var(--rf-ff-display);
}
```

(The header title got its own rule in Task 2.)

- [ ] **Step 2: Replace the `h2` rule in `extra.css`**

Delete:

```css
.md-typeset h2 {
  /* Distinguish major page sections more clearly from body text and h3 headings. */
  font-weight: 500;
}
```

Append:

```css
/* ============================================================================
   HEADINGS — OCR-A with the source site's tracking. Sentence case: only the
   hero on robotframework.org is uppercase.
   ========================================================================== */
.md-typeset h1,
.md-typeset h2,
.md-typeset h3,
.md-typeset h4,
.md-typeset h5,
.md-typeset h6 {
  font-family: var(--rf-ff-display);
  font-weight: 600;
  letter-spacing: -0.1em;
  text-wrap: balance;
  color: rgb(var(--rf-text));
}

/* Section heads take the accent, as on the source site. h1 stays ink: a
   full-width teal page title reads as a banner rather than a heading. */
.md-typeset h2,
.md-typeset h3 {
  color: rgb(var(--rf-accent-text));
}

/* Material's permalink icon inherits the heading colour; keep it quiet. */
.md-typeset .headerlink {
  color: rgb(var(--rf-500) / 0.6);
}

/* ============================================================================
   LINKS
   ========================================================================== */
.md-typeset a {
  font-weight: 600;
  text-decoration: underline;
  text-decoration-color: rgb(var(--rf-500));
  text-underline-offset: 0.15em;
}

.md-typeset a:hover,
.md-typeset a:focus {
  color: rgb(var(--rf-800));
  text-decoration-color: currentColor;
}

/* Sidebar and TOC links are navigation, not prose: plain weight, no underline. */
.md-nav a,
.md-nav a:hover {
  font-weight: 400;
  text-decoration: none;
}
```

- [ ] **Step 3: Build and verify**

Open `/syntax/tests/` and run:

```js
() => {
  const cs = s => getComputedStyle(document.querySelector(s));
  return {
    h1: [cs('.md-typeset h1').fontFamily.split(',')[0], cs('.md-typeset h1').color, cs('.md-typeset h1').letterSpacing],
    h2: [cs('.md-typeset h2').fontFamily.split(',')[0], cs('.md-typeset h2').color],
    link: [cs('.md-content p a').fontWeight, cs('.md-content p a').textDecorationLine],
    navLink: [cs('.md-nav__link').fontWeight, cs('.md-nav__link').textDecorationLine],
  };
}
```

Expected (light): `h1` = `["\"OCR-A\"", "rgb(9, 12, 13)", "-3.2px"]` (−0.1em of 32px), `h2[1]` = `rgb(31, 102, 98)`, `link` = `["600", "underline"]`, `navLink` = `["400", "none"]`.

- [ ] **Step 4: Screenshot and eyeball the h3 list**

`.playwright-mcp/t3-light.png`. OCR-A at −0.1em is tight; if `h4`+ become hard to read at 16px, change the `letter-spacing` on `h4, h5, h6` only to `-0.05em` and note it in the plan. Do not commit.

---

### Task 4: Code plate and inline code

**Files:**
- Modify: `doc/manual/docs/assets/extra.css`

**Interfaces:**
- Consumes: `--rf-50`, `--rf-100`, `--rf-500`, `--rf-700`, `--rf-accent-text`, `--rf-accent-indicator`, `--rf-r-sm`, `--rf-r-md`, `--rf-ff-code`, `--rf-ff-display`.

Target (Guides `.theme-code-block`, `.markdown code`): a bordered plate, `1px solid rgb(var(--rf-700) / 0.25)`, radius `--rf-r-md`, surface robot-100 light / robot-50 dark; copy button outlined in OCR-A uppercase; highlighted lines tinted with a solid rail; inline code on a `rgb(var(--rf-500) / 0.13)` tint. Material renders fenced code as `.md-typeset .highlight > pre > code` with line numbers in `.linenodiv` when `linenums` is on, and the copy button as `.md-clipboard`.

- [ ] **Step 1: Append the plate rules**

```css
/* ============================================================================
   THE PLATE — shared editor chrome from the source site, dressing Material's
   own code-block markup. The generated highlight-*.css files set their own
   `.highlight { background }`; the surface rule below wins by load order.
   ========================================================================== */
.md-typeset .highlight {
  border: 1px solid rgb(var(--rf-700) / 0.25);
  border-radius: var(--rf-r-md);
  overflow: hidden;
  background: var(--md-code-bg-color);
}

.md-typeset .highlight pre,
.md-typeset .highlight > pre > code,
.md-typeset .highlighttable,
.md-typeset .highlighttable .linenos,
.md-typeset .highlighttable .code {
  background: var(--md-code-bg-color);
}

.md-typeset pre > code {
  font-family: var(--rf-ff-code);
  font-size: 0.83rem;
  line-height: 1.55;
}

/* Line-number gutter: a hair lighter than the code, separated by the same
   line the plate uses. */
.md-typeset .highlighttable .linenos {
  background: rgb(var(--rf-500) / 0.06);
  border-right: 1px solid rgb(var(--rf-700) / 0.18);
  color: rgb(var(--rf-text) / 0.45);
}

/* Copy button: OCR-A, outlined, quiet until hovered. */
.md-typeset .md-clipboard {
  font-family: var(--rf-ff-display);
  border: 1px solid rgb(var(--rf-500) / 0.35);
  border-radius: var(--rf-r-sm);
  color: rgb(var(--rf-text) / 0.65);
}

.md-typeset .md-clipboard:hover,
.md-typeset .md-clipboard:focus-visible {
  color: rgb(var(--rf-accent-text));
  border-color: rgb(var(--rf-accent-text));
}

/* Marked lines (`hl_lines`): the brand pivot with a solid rail. */
.md-typeset .highlight .hll {
  background: rgb(var(--rf-500) / 0.12);
  box-shadow: inset 2px 0 0 0 rgb(var(--rf-accent-indicator));
}

/* Inline code. */
.md-typeset code:not(pre code) {
  font-family: var(--rf-ff-code);
  background: rgb(var(--rf-500) / 0.13);
  border-radius: var(--rf-r-sm);
  padding: 0.1em 0.35em;
  font-size: 0.87em;
  color: inherit;
}

/* Code inside a link keeps the link colour. */
.md-typeset a code {
  color: inherit;
}
```

- [ ] **Step 2: Build and verify**

Open `/syntax/tests/` and run:

```js
() => {
  const cs = s => getComputedStyle(document.querySelector(s));
  const plate = cs('.md-typeset .highlight');
  return {
    border: plate.borderTopWidth + ' ' + plate.borderTopColor,
    radius: plate.borderTopLeftRadius,
    bg: cs('.md-typeset .highlight pre').backgroundColor,
    codeFont: cs('.md-typeset pre > code').fontFamily.split(',')[0],
    inline: cs('.md-typeset p code').backgroundColor,
    gutter: document.querySelector('.linenos') ? cs('.linenos').borderRightWidth : 'no gutter',
  };
}
```

Expected (light): `border` = `1px rgba(31, 102, 98, 0.25)`, `radius` = `6px`, `bg` = `rgb(204, 230, 227)`, `codeFont` = `"IBM Plex Mono"`, `inline` = `rgba(0, 192, 181, 0.13)`, `gutter` = `1px`.

Switch to `slate`: `bg` = `rgb(9, 12, 13)`.

- [ ] **Step 3: Check the highlight palettes still read on the new surfaces**

Screenshot `.playwright-mcp/t4-light.png` and `.playwright-mcp/t4-dark.png` scrolled to the first code block. The Pygments `default` style on robot-100 and `lightbulb` on robot-50 must stay legible (comments, strings, keywords all distinguishable). If a token colour disappears, regenerate the affected file with `python doc/manual/docs/assets/generate_highlight_css.py light <style>` (or `dark`) using a higher-contrast Pygments style and note the style name in the file header. Do not commit.

---

### Task 5: Sidebars, TOC, and prose elements

**Files:**
- Modify: `doc/manual/docs/assets/extra.css`

**Interfaces:**
- Consumes: `--rf-100`, `--rf-200`, `--rf-500`, `--rf-700`, `--rf-accent-text`, `--rf-accent-indicator`, `--rf-r-sm`, `--rf-r-md`, `--rf-ff-display`, `--rf-text`.

Target (Guides sidebar, `.markdown table`, `details`, `blockquote`, `.theme-admonition`): sidebar at 14px with a hairline under each top-level group, active item in accent text; right TOC same; tables with OCR-A headers in accent, row hover tint; admonitions with a 3px left rail; details with a rail that brightens when open; blockquotes with a rail and tint.

- [ ] **Step 1: Append the navigation rules**

```css
/* ============================================================================
   SIDEBARS — left nav and right TOC. 14px like the Guides, hairline between
   top-level groups, active item in the accent.
   ========================================================================== */
.md-sidebar .md-nav {
  font-size: 0.7rem;                /* 14px at Material's 20px root */
}

.md-nav__title {
  font-family: var(--rf-ff-display);
  font-weight: 600;
  letter-spacing: -0.05em;
  color: rgb(var(--rf-text));
}

.md-nav__link {
  color: rgb(var(--rf-text) / 0.8);
}

.md-nav__link:hover {
  color: rgb(var(--rf-accent-text));
}

.md-nav__link--active,
.md-nav__item--active > .md-nav__link {
  color: rgb(var(--rf-accent-text));
}

/* Hairline under each top-level group in the primary sidebar. */
.md-sidebar--primary .md-nav--primary > .md-nav__list > .md-nav__item {
  padding-bottom: 0.4rem;
  margin-bottom: 0.4rem;
  border-bottom: 1px solid rgb(var(--rf-700) / 0.18);
}

.md-sidebar--primary .md-nav--primary > .md-nav__list > .md-nav__item:last-child {
  border-bottom: 0;
}

/* Material draws the sidebar scrollbar track and a vertical rule via
   box-shadow on `.md-nav__list`; the rule is on the ramp now. */
.md-nav--secondary .md-nav__list {
  border-left: 1px solid rgb(var(--rf-700) / 0.18);
}
```

- [ ] **Step 2: Append the prose-element rules**

```css
/* ============================================================================
   PROSE ELEMENTS
   ========================================================================== */
.md-typeset table:not([class]) {
  font-size: 0.72rem;
  border: 0;
  border-radius: 0;
  box-shadow: none;
}

.md-typeset table:not([class]) th {
  font-family: var(--rf-ff-display);
  font-weight: 400;
  letter-spacing: 0.05em;
  color: rgb(var(--rf-accent-text));
  background: none;
  border-bottom: 1px solid rgb(var(--rf-300) / 0.4);
}

.md-typeset table:not([class]) td {
  border-top: 0;
  border-bottom: 1px solid rgb(var(--rf-700) / 0.25);
}

.md-typeset table:not([class]) tbody tr:hover {
  background: rgb(var(--rf-500) / 0.08);
  box-shadow: none;
}

/* Admonitions inherit the ramp so they sit on the page rather than on top.
   Material colours the rail per type via --md-admonition-icon and the type
   class; only the shape and surface change here. */
.md-typeset .admonition,
.md-typeset details {
  border-radius: var(--rf-r-md);
  border-width: 0 0 0 3px;
  box-shadow: none;
  background: rgb(var(--rf-100) / 0.5);
  font-size: 0.8rem;
}

.md-typeset .admonition-title,
.md-typeset summary {
  font-family: var(--rf-ff-display);
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  font-size: 0.7rem;
}

/* The `note` type — 207 of the Manual's 228 admonitions — takes the brand. */
.md-typeset .admonition.note,
.md-typeset details.note {
  border-color: rgb(var(--rf-accent-text));
}

.md-typeset .note > .admonition-title,
.md-typeset .note > summary {
  background: rgb(var(--rf-500) / 0.1);
}

.md-typeset .note > .admonition-title::before,
.md-typeset .note > summary::before {
  background-color: rgb(var(--rf-accent-text));
}

/* details / summary — a rail that brightens to the pivot when open. */
.md-typeset details[open] {
  border-left-color: rgb(var(--rf-accent-indicator));
}

.md-typeset blockquote {
  border-left: 3px solid rgb(var(--rf-accent-indicator));
  background: rgb(var(--rf-500) / 0.06);
  padding: 0.8rem 1.1rem;
  border-radius: 0 var(--rf-r-sm) var(--rf-r-sm) 0;
  color: inherit;
}

.md-typeset img {
  border-radius: var(--rf-r-md);
}
```

- [ ] **Step 3: Build and verify**

Open `/syntax/tests/` and run:

```js
() => {
  const cs = s => { const e = document.querySelector(s); return e ? getComputedStyle(e) : null; };
  return {
    navSize: cs('.md-sidebar .md-nav').fontSize,
    active: cs('.md-nav__link--active')?.color,
    adm: cs('.md-typeset .admonition') ? [cs('.md-typeset .admonition').borderLeftWidth, cs('.md-typeset .admonition').borderRadius] : 'no admonition on page',
    admTitleFont: cs('.md-typeset .admonition-title')?.fontFamily.split(',')[0],
  };
}
```

Expected (light): `navSize` = `14px`, `active` = `rgb(31, 102, 98)`, `adm` = `["3px", "6px"]`, `admTitleFont` = `"OCR-A"`.

Then open `/appendix/settings/` (it has tables) and check `getComputedStyle(document.querySelector('.md-typeset table th')).fontFamily` starts with `"OCR-A"`.

- [ ] **Step 4: Screenshot at 1440 and 390**

`.playwright-mcp/t5-desktop.png`, `.playwright-mcp/t5-mobile.png`. On mobile, open the drawer (`document.getElementById('__drawer').checked = true`) and confirm the group hairlines and active colour render there too. Do not commit.

---

### Task 6: Footer as a dark island

**Files:**
- Modify: `doc/manual/docs/assets/extra.css`

**Interfaces:**
- Consumes: the footer `--md-footer-*` values from Task 1 (already fixed dark values), `--rf-ff-nav`.

Target (Guides `.footer--dark`): the footer is dark in both schemes — ground robot-100-dark (`18 26 28`), text robot-950-dark, links robot-900-dark, hover/titles in the light teal. Task 1 already hard-set the `--md-footer-*` variables to those values, so Material paints most of it; the rules here only add the type and the previous/next links.

- [ ] **Step 1: Append the footer rules**

```css
/* ============================================================================
   FOOTER — a dark island on a light page, as on the source site. The colours
   are fixed dark values in theme.css (no flip: the island is dark under both
   schemes), so only the type treatment lives here.
   ========================================================================== */
.md-footer {
  border-top: 1px solid rgb(0 192 181 / 0.25);
}

.md-footer__title,
.md-footer__direction {
  font-family: var(--rf-ff-nav);
}

.md-footer__link:hover .md-footer__title {
  color: rgb(92 214 207);
}

.md-footer-meta {
  background: var(--md-footer-bg-color--dark);
}

.md-copyright a {
  color: rgb(92 214 207);
}
```

(These are the only hex-free literals allowed outside `theme.css`: the island's colours do not flip, so a ramp step would be wrong.)

- [ ] **Step 2: Build and verify**

Open `/syntax/tests/`, scroll to the bottom (`window.scrollTo(0, document.body.scrollHeight)`) and run:

```js
() => {
  const cs = s => getComputedStyle(document.querySelector(s));
  const light = [cs('.md-footer').backgroundColor, cs('.md-footer-meta').backgroundColor];
  document.body.setAttribute('data-md-color-scheme', 'slate');
  const dark = [cs('.md-footer').backgroundColor, cs('.md-footer-meta').backgroundColor];
  document.body.setAttribute('data-md-color-scheme', 'default');
  return { light, dark, same: light.join() === dark.join() };
}
```

Expected: `same` = `true`, `light[0]` = `rgb(18, 26, 28)`, `light[1]` = `rgb(9, 12, 13)`. Screenshot `.playwright-mcp/t6-footer.png`. Do not commit.

---

### Task 7: Layout width, cleanup, documentation

**Files:**
- Modify: `doc/manual/docs/assets/extra.css` (content width block)
- Modify: `CLAUDE.md` (Design section)

- [ ] **Step 1: Tighten the reading measure**

In `extra.css`, change the content block to

```css
.md-content__inner {
  /* ~90 characters per line at 16px Plex Sans; longer measures tire on
     these pages. Centred within whatever the two sidebars leave over. */
  max-width: 52rem;
  margin-inline: auto;
}
```

and keep the existing `@media screen and (max-width: 76.1875em)` gutter rule beneath it unchanged.

- [ ] **Step 2: Order `extra.css` by section**

Reorder the file so it reads top to bottom: layout → header → sidebars → headings → links → code plate → prose elements (definition lists and glossary rules join this section) → footer. Each section keeps the `/* ==== */` banner it was given. No rule changes in this step — only movement; the built CSS must be byte-identical in effect.

- [ ] **Step 3: Update `CLAUDE.md`**

In the Design section, replace item 3 with:

```markdown
3. This repo, three stylesheets loaded in this order:
   - `assets/fonts.css` — self-hosted fonts and `--rf-ff-*` type tokens (`theme.font: false` keeps Material
     from loading Roboto).
   - `assets/theme.css` — the `--rf-*` colour ramp and its mapping onto Material's `--md-*` variables. The ramp
     is declared once for light and once, reversed, under `[data-md-color-scheme="slate"]`, so a component rule
     is written **once** against a ramp step and is correct in both schemes. Never add a dark override to a
     `--rf-*` colour in a component rule — it would flip twice.
   - `assets/extra.css` — component rules (header, sidebars, headings, code plate, prose, footer, layout).
     Colours are `rgb(var(--rf-N) / alpha)`, never hex; the footer is the one fixed-dark exception.
```

- [ ] **Step 4: Full regression pass**

Build without `-q` and confirm no `WARNING` lines (the `INFO` anchor notices are pre-existing). Then, for each of `/`, `/syntax/tests/`, `/appendix/settings/`, `/glossary/`, `/libraries/`:

- 1440×900 light and dark: screenshot; `document.documentElement.scrollWidth <= innerWidth` is `true`.
- 1024×800 light: screenshot; the right TOC is gone, the left drawer is behind the hamburger, no overflow.
- 390×844 light: screenshot; `getComputedStyle(document.querySelector('.md-content__inner')).marginLeft` = `16px`; no overflow.

Compare `/syntax/tests/` light against the Guides page at `~/Source/MarketSquare/robotframeworkguides/website/build/docs/authoring/variables.html` (serve that directory on another port, force light with `document.documentElement.setAttribute('data-theme','light')`). Header, heading treatment, link style, code plate and sidebar should read as the same family.

- [ ] **Step 5: Hand-off**

Delete `.playwright-mcp/`, stop every `http.server`, and run `git status --short` — expected: `M properdocs.yml`, `M CLAUDE.md`, `M doc/manual/docs/assets/extra.css`, `M doc/manual/docs/assets/fonts.css`, `?? doc/manual/docs/assets/theme.css` (plus whatever was already pending). Report the list. **Do not commit.**

---

## Out of scope (deliberately)

- **Home page (`index.md`) hero** — the Guides have a dedicated landing layout; the Manual's home is a content page. Revisit once the content pages look right.
- **Syntax-highlighting palette** — Pygments styles stay; only their surface changes (Task 4). Matching the Guides' Prism theme token-for-token is a separate decision.
- **Tabs (`pymdownx.tabbed`) plate treatment** — the Manual's content uses no `=== "Tab"` blocks yet.
- **Social cards** — `plugins.social.cards_layout_options.background_color` is already the brand teal.
