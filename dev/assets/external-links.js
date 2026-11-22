/* Mark article links that leave this manual, including after instant navigation. */
(() => {
  const template = document.getElementById('rf-external-link');
  const site = new URL(template.dataset.siteUrl);
  const version = template.dataset.canonicalVersion;
  // mike appends the canonical version to site_url. All manual versions are internal.
  if (version && site.pathname.endsWith(`/${version}/`)) {
    site.pathname = new URL('../', site).pathname;
  }

  function setup() {
    for (const link of document.querySelectorAll('.md-content__inner a[href]')) {
      if (!['http:', 'https:'].includes(link.protocol)) continue;
      if (link.origin === location.origin &&
          (link.pathname === site.pathname.slice(0, -1) ||
           link.pathname.startsWith(site.pathname))) continue;
      if (link.matches('.headerlink, .md-button, .md-content__button, .md-annotation__index') ||
          link.closest('.highlight, pre, .tabbed-labels, .md-nav, .rf-page-toc') ||
          link.querySelector('img, svg, .rf-external-link') || !link.textContent.trim()) continue;

      link.append(template.content.firstElementChild.cloneNode(true));
      const description = link.getAttribute('aria-describedby');
      link.setAttribute('aria-describedby', [description, 'rf-external-site'].filter(Boolean).join(' '));
    }
  }

  if (typeof document$ !== 'undefined') document$.subscribe(setup);
  else setup();
})();
