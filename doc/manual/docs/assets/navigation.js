/* Keyboard access for Material's checkbox-driven navigation at every width.
 * Focus containment applies only while the drawer layout is active.
 * Enhance labels into native buttons while keeping Material's checkbox state.
 * Recheck this adapter when upgrading Material (baseline: 9.7.6).
 */
(() => {
  const drawerLayout = matchMedia('(max-width: 76.1875em)');
  const searchLayout = matchMedia('(min-width: 60em)');
  const inertStates = new Map();
  const focusable = 'a[href], button, input, select, textarea, summary, [tabindex]';
  let drawer, navigation, menu, pane, content;
  let wasOpen = false;

  function focusableControls(container) {
    return [...container.querySelectorAll(focusable)].filter(element =>
      element.tabIndex >= 0 && !element.matches(':disabled') &&
      !element.closest('[inert]') && element.getClientRects().length &&
      getComputedStyle(element).visibility === 'visible'
    );
  }

  // Restore only states owned by this adapter, including across page swaps.
  function setInert(element, inert) {
    if (!inertStates.has(element)) inertStates.set(element, element.inert);
    element.inert = inert;
  }

  function restoreInertStates() {
    for (const [element, inert] of inertStates) element.inert = inert;
    inertStates.clear();
  }

  // Only the current pane participates in keyboard and screen reader navigation.
  function syncPane(nav) {
    setInert(nav, false);
    const list = nav.querySelector(':scope > .md-nav__list');
    const items = [...(list?.children || [])];
    const openNav = items
      .map(item => item.querySelector(':scope > input:checked ~ nav'))
      .find(child => child && getComputedStyle(child).display !== 'none');
    const openItem = openNav?.parentElement;
    for (const child of nav.children) setInert(child, !!openNav && child !== list);
    for (const item of items) {
      setInert(item, !!openNav && item !== openItem);
      // Nested TOC groups stay inline; only toggled submenus are separate panes.
      const nestedPane = item.querySelector(':scope > input ~ nav');
      for (const child of item.children) {
        setInert(child, child === nestedPane || (!!openNav && item === openItem));
      }
    }
    return openNav ? syncPane(openNav) : nav;
  }

  function isolateDrawer() {
    // Leave the overlay clickable, and restore existing inert states on close.
    for (let ancestor = navigation; ancestor.parentElement !== document.body;
      ancestor = ancestor.parentElement) {
      for (const sibling of ancestor.parentElement.children) {
        if (sibling === ancestor || sibling.matches('script, style')) continue;
        setInert(sibling, true);
      }
    }
    const container = navigation.closest('.md-container');
    for (const sibling of document.body.children) {
      if (sibling === container || sibling.matches('input, script, style, .md-overlay')) continue;
      setInert(sibling, true);
    }
  }

  function syncControlSemantics() {
    for (const button of document.querySelectorAll('[data-rf-nav-control]')) {
      const input = document.getElementById(button.dataset.rfNavControl);
      button.setAttribute('aria-expanded', String(input.checked));
      const target = document.getElementById(button.getAttribute('aria-controls'));
      if (target?.hasAttribute('aria-expanded')) {
        target.setAttribute('aria-expanded', String(input.checked));
      }
    }
  }

  function sync() {
    restoreInertStates();
    if (!navigation) return;
    const open = drawerLayout.matches && drawer.checked;
    const previousPane = pane;
    syncControlSemantics();
    updateSearchClearButton();
    if (drawerLayout.matches) {
      pane = syncPane(navigation);
      setInert(navigation, !open);
      setInert(navigation.closest('.md-sidebar--primary'), !open);
      if (open) isolateDrawer();
    } else {
      pane = undefined;
    }
    if (open && (!wasOpen || pane !== previousPane)) {
      const input = previousPane?.parentElement.querySelector(':scope > input');
      const back = previousPane && pane.contains(previousPane) && input;
      const opener = back && pane.querySelector(`[data-rf-nav-control="${input.id}"]`);
      // The pane is still sliding into view. Scrolling to its focus target can
      // shift Material's overflow-hidden wrapper and leave the drawer blank.
      (opener || focusableControls(pane)[0])?.focus({ preventScroll: true });
    } else if (wasOpen && !open && drawerLayout.matches) {
      menu.focus();
    }
    wasOpen = open;
  }

  function markCurrentLocation() {
    // Distinguish the current page from its containing section for AT users.
    for (const link of navigation.querySelectorAll('a.md-nav__link--active')) {
      if (!link.closest('.md-nav--secondary')) link.setAttribute('aria-current', 'page');
    }
    // Name the drawer's TOC pane after its page; the other TOCs keep their label.
    const tocTitle = navigation.querySelector('.md-nav--secondary > .md-nav__title');
    const pageTitle = navigation.querySelector('a[aria-current="page"] .md-ellipsis')?.textContent.trim();
    if (tocTitle && pageTitle) {
      const backIcon = tocTitle.querySelector('.md-nav__icon');
      tocTitle.textContent = pageTitle;
      if (backIcon) tocTitle.prepend(backIcon);
    }
    for (const link of document.querySelectorAll('.md-tabs__link')) {
      if (link.closest('.md-tabs__item--active')) {
        const current = new URL(link.href).pathname === location.pathname;
        link.setAttribute('aria-current', current ? 'page' : 'location');
      } else link.removeAttribute('aria-current');
    }
  }

  function addCloseButton() {
    if (navigation.querySelector('.rf-nav-close')) return;
    const close = document.createElement('button');
    close.type = 'button';
    close.className = 'rf-nav-close md-icon';
    close.setAttribute('aria-label', 'Close navigation');
    close.textContent = '\u00d7';
    close.addEventListener('click', () => drawer.click());
    navigation.prepend(close);
  }

  function updateSearchClearButton() {
    const clear = document.querySelector('.md-search__form button[type="reset"]');
    if (!clear) return;
    const visible = searchLayout.matches || document.getElementById('__search').checked;
    clear.tabIndex = visible && document.querySelector('.md-search__input')?.value ? 0 : -1;
    if (!visible && document.activeElement === clear) {
      // Let native Tab finish before restoring focus if it is still hidden.
      setTimeout(() => {
        if (clear.tabIndex < 0 && document.activeElement === clear) {
          document.querySelector('.md-header__button[data-rf-nav-control="__search"]')?.focus({ preventScroll: true });
        }
      }, 0);
    }
  }

  function clearSearch() {
    const query = document.querySelector('.md-search__input');
    query.value = '';
    // Material reads query changes on keyup.
    query.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true }));
    updateSearchClearButton();
  }

  function leaveSearch(direction = 0) {
    const query = document.querySelector('.md-search__input');
    const origin = searchLayout.matches ? query :
      document.querySelector('.md-header__button[data-rf-nav-control="__search"]');
    // Material debounces focus updates. Let it observe restored input focus
    // before closing, so Escape from a result does not reopen the panel.
    if (searchLayout.matches && !direction && document.activeElement !== query) {
      query.focus({ preventScroll: true });
      setTimeout(() => {
        const search = document.getElementById('__search');
        if (document.activeElement === query && search.checked) search.click();
      }, 10);
      return;
    }
    if (searchLayout.matches) query.focus({ preventScroll: true });
    document.getElementById('__search').click();
    const controls = focusableControls(document.body).filter(element =>
      element === origin || !element.closest('.md-search')
    );
    const target = direction && controls[controls.indexOf(origin) + direction];
    (target || origin).focus({ preventScroll: !direction });
  }

  function focusContent(hash = location.hash) {
    let target;
    try {
      target = document.getElementById(decodeURIComponent(hash.slice(1)));
    } catch { /* Malformed fragments fall back to the page heading. */ }
    target ||= content.querySelector('h1') || content;
    if (!target.hasAttribute('tabindex') && target.tabIndex < 0) target.tabIndex = -1;
    target.focus({ preventScroll: true });
  }

  function replaceLabelWithButton(label) {
    const button = document.createElement('button');
    for (const { name, value } of label.attributes) {
      if (!['for', 'tabindex', 'role'].includes(name)) button.setAttribute(name, value);
    }
    button.type = 'button';
    button.dataset.rfNavControl = label.htmlFor;
    button.append(...label.childNodes);
    label.replaceWith(button);
    return button;
  }

  function setupControls() {
    // Only unenhanced labels match, including after instant navigation.
    const labels = document.querySelectorAll(
      '.md-header__button:is([for="__drawer"], [for="__search"]), ' +
      '.md-nav--primary label[for]:not([for="__drawer"])'
    );
    for (const label of labels) {
      const input = label.control;
      if (!input) continue;
      const button = replaceLabelWithButton(label);
      button.addEventListener('click', () => {
        input.click();
        if (input.id === '__search') document.querySelector('.md-search__input').focus();
      });
      let target;
      if (input === drawer) {
        target = navigation;
        button.setAttribute('aria-label', 'Open navigation');
      } else if (input.id === '__search') {
        target = document.querySelector('.md-search');
        button.setAttribute('aria-label', 'Search');
        target?.setAttribute('aria-label', 'Search');
      } else {
        target = input.parentElement.querySelector(':scope > nav');
        const back = button.classList.contains('md-nav__title');
        const title = target?.querySelector(':scope > .md-nav__title')?.textContent.trim();
        button.setAttribute('aria-label', back ? 'Back to previous menu' : `Show ${title}`);
      }
      if (target) {
        target.id ||= `rf-${input.id}`;
        button.setAttribute('aria-controls', target.id);
      }
    }
  }

  function setup() {
    restoreInertStates();
    drawer = document.getElementById('__drawer');
    navigation = document.querySelector('.md-nav--primary');
    if (!drawer || !navigation) return;
    const article = document.querySelector('.md-content__inner');
    const pageChanged = content && content !== article;
    content = article;
    navigation.id = 'rf-navigation';
    markCurrentLocation();
    addCloseButton();
    setupControls();
    menu = document.querySelector('.md-header__button[data-rf-nav-control="__drawer"]');
    document.querySelector('.md-progress')?.setAttribute('aria-label', 'Loading page');
    sync();
    if (pageChanged) focusContent();
  }

  // Material adds the version selector asynchronously and keeps it on page swaps.
  // Use its visible text as the name, with the action as a separate description.
  const versionHost = document.querySelector('.rf-header-version');
  if (versionHost) {
    const observer = new MutationObserver(nameVersionSelector);
    function nameVersionSelector() {
      const button = versionHost.querySelector('.md-version__current');
      if (!button) return;
      const label = button.getAttribute('aria-label');
      if (label) {
        button.setAttribute('aria-description', label);
        button.removeAttribute('aria-label');
      }
      observer.disconnect();
    }
    observer.observe(versionHost, { childList: true, subtree: true });
    nameVersionSelector();
  }

  document.addEventListener('keydown', event => {
    if (!navigation) return;
    const drawerOpen = drawerLayout.matches && drawer.checked;
    if (drawerOpen && event.key === 'Escape') {
      event.preventDefault();
      event.stopImmediatePropagation();
      drawer.click();
      return;
    }
    if (event.key === 'Escape' && document.getElementById('__search').checked) {
      event.preventDefault();
      event.stopImmediatePropagation();
      leaveSearch();
      return;
    }
    // Material reserves results for arrow keys; include them in Tab navigation.
    if (event.key === 'Tab' && document.getElementById('__search').checked) {
      const query = document.querySelector('.md-search__input');
      const clear = document.querySelector('.md-search__form button[type="reset"]');
      const targets = [query, ...(clear?.tabIndex === 0 ? [clear] : []),
        ...document.querySelectorAll(
          '.md-search-result__link, .md-search-result__more > summary'
        )].filter(element => element?.getClientRects().length &&
          (!element.closest('details:not([open])') || element.matches('summary')));
      const index = targets.indexOf(event.target);
      const target = index >= 0 ? targets[index + (event.shiftKey ? -1 : 1)] : undefined;
      if (target) {
        event.preventDefault();
        event.stopImmediatePropagation();
        target.focus();
        return;
      }
      if (index >= 0) {
        event.preventDefault();
        event.stopImmediatePropagation();
        leaveSearch(event.shiftKey ? -1 : 1);
        return;
      }
    }
    const control = event.target.closest(
      '.md-search__form button[type="reset"], ' +
      '.md-search-result__more > summary'
    );
    if (control && (event.key === 'Enter' || event.key === ' ')) {
      event.preventDefault();
      event.stopImmediatePropagation();
      if (!event.repeat) control.click();
      return;
    }
    if (drawerOpen && event.key === 'Tab') {
      const targets = focusableControls(pane);
      const next = targets.indexOf(document.activeElement) + (event.shiftKey ? -1 : 1);
      if (next < 0 || next >= targets.length) {
        event.preventDefault();
        targets[event.shiftKey ? targets.length - 1 : 0]?.focus();
      }
    }
  }, true);
  document.addEventListener('change', event => {
    if (event.target.matches('#__drawer, #__search, .md-nav__toggle')) sync();
  });
  document.addEventListener('input', event => {
    if (!event.target.matches('.md-search__input')) return;
    const search = document.getElementById('__search');
    if (document.activeElement === event.target && !search.checked) search.click();
    updateSearchClearButton();
  });
  // Clearing a collapsed search bar must not open the results via theme focus.
  document.addEventListener('reset', event => {
    if (!event.target.matches('.md-search__form')) return;
    if (!document.getElementById('__search').checked) {
      event.stopPropagation();
      if (document.activeElement.matches('button[type="reset"]')) {
        document.querySelector('.md-header__button.md-logo')?.focus({ preventScroll: true });
      }
    }
    clearSearch();
  }, true);
  // Delegate once: Material replaces the page TOC during instant navigation.
  document.addEventListener('click', event => {
    if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    const search = document.getElementById('__search');
    if (event.target.matches('.md-search__input') && !search.checked) search.click();
    const link = event.target.closest('.rf-page-toc a[href]');
    if (link) {
      focusContent(new URL(link.href).hash);
      link.closest('.rf-page-toc').open = false;
    }
  });
  drawerLayout.addEventListener('change', sync);
  // Material moves the TOC out of the drawer before the desktop breakpoint.
  searchLayout.addEventListener('change', sync);
  // Material replaces the sidebar on instant page loads, but keeps the header.
  if (typeof document$ !== 'undefined') document$.subscribe(setup);
  else setup();
})();
