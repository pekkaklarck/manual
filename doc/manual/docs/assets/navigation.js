/* Keyboard access for Material's checkbox-driven navigation at every width.
 * Focus containment applies only while the drawer layout is active.
 * Keep the theme's labels and click behavior, including instant navigation.
 * Recheck this adapter when upgrading Material (baseline: 9.7.6).
 */
(() => {
  const drawerLayout = matchMedia('(max-width: 76.1875em)');
  const initializedControls = new WeakSet();
  const inertStates = new Map();
  const focusable = 'a[href], button, input, select, textarea, summary, [tabindex]';
  let drawer, navigation, menu, pane;
  let wasOpen = false;

  function focusableControls(container) {
    return [...container.querySelectorAll(focusable)].filter(element =>
      element.tabIndex >= 0 && !element.matches(':disabled') &&
      !element.closest('[inert]') && element.getClientRects().length
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
    for (const label of document.querySelectorAll('[data-rf-nav-control]')) {
      const input = document.getElementById(label.htmlFor);
      label.tabIndex = 0;
      label.setAttribute('role', 'button');
      label.setAttribute('aria-expanded', String(input.checked));
    }
  }

  function sync() {
    restoreInertStates();
    if (!navigation) return;
    const open = drawerLayout.matches && drawer.checked;
    const previousPane = pane;
    syncControlSemantics();
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
      const opener = back && pane.querySelector(`label[for="${input.id}"]`);
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

  function setupControls() {
    const labels = [menu,
      ...document.querySelectorAll('.md-header__button[for="__search"]'),
      ...navigation.querySelectorAll('label[for]:not([for="__drawer"])')];
    for (const label of labels) {
      const input = document.getElementById(label.htmlFor);
      if (!input || initializedControls.has(label)) continue;
      initializedControls.add(label);
      label.dataset.rfNavControl = '';
      let target;
      if (input === drawer) {
        target = navigation;
        label.setAttribute('aria-label', 'Open navigation');
      } else if (input.id === '__search') {
        target = document.querySelector('.md-search');
        label.setAttribute('aria-label', 'Search');
      } else {
        target = input.parentElement.querySelector(':scope > nav');
        const back = label.classList.contains('md-nav__title');
        const title = target?.querySelector(':scope > .md-nav__title')?.textContent.trim();
        label.setAttribute('aria-label', back ? 'Back to previous menu' : `Show ${title}`);
      }
      if (target) {
        target.id ||= `rf-${input.id}`;
        label.setAttribute('aria-controls', target.id);
      }
    }
  }

  function setup() {
    restoreInertStates();
    drawer = document.getElementById('__drawer');
    navigation = document.querySelector('.md-nav--primary');
    menu = document.querySelector('.md-header__button[for="__drawer"]');
    if (!drawer || !navigation || !menu) return;
    navigation.id = 'rf-navigation';
    markCurrentLocation();
    addCloseButton();
    setupControls();
    sync();
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
    const control = event.target.closest('[data-rf-nav-control]');
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
  // Delegate once: Material replaces the page TOC during instant navigation.
  document.addEventListener('click', event => {
    const pageToc = event.target.closest('.rf-page-toc a[href]')?.closest('.rf-page-toc');
    if (pageToc) pageToc.open = false;
  });
  drawerLayout.addEventListener('change', sync);
  // Material moves the TOC out of the drawer before the desktop breakpoint.
  matchMedia('(min-width: 60em)').addEventListener('change', sync);
  // Material replaces the sidebar on instant page loads, but keeps the header.
  if (typeof document$ !== 'undefined') document$.subscribe(setup);
  else setup();
})();
