# Research utilities and rules

Everything used to inspect or tune extraction belongs here or under `util/`;
one-off analysis code should not live only in shell history.

- `extract_page.js` selects and cleans the main browser DOM before conversion.
- `site_rules.json` contains small, reviewable site-specific adjustments.
- `list_sitemap_urls_cdp` inventories a sitemap through a disposable browser
  tab, supports bounded sitemap-index traversal and path-prefix filters, and
  closes the tab when finished.
- `list_sitemap_urls` performs bounded sitemap discovery.

Generated HTML, `cdp read` snapshots, reports, and captures belong under the
ignored `data/` and `output/` trees.
