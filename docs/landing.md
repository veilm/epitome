# Epitome landing page

`landing/index.html` is the standalone coming-soon page. It has no script, external
network dependency, or binary font asset in Git.

The wordmark was initially styled with `Georgia, 'Times New Roman', serif`.
On the Delirium workstation, Chrome DevTools Protocol's
`CSS.getPlatformFontsForNode` reported that the actual seven letters were
rendered by **Liberation Serif**: Georgia is not installed, and fontconfig
substitutes Liberation Serif. The page now requests Liberation Serif first,
with Georgia as a fallback on devices without it. This preserves the local
appearance without adding font binaries to Git. Other devices may show a
slightly different wordmark.

For a local comparison with other installed typefaces, open
`../design/type-study.html` on Delirium.

## Deployment

The page was launched on 2026-09-26 as the asset-only Cloudflare Worker
`epitome`, on the account's Workers Free plan. It serves `epitome.news` and
`www.epitome.news`. The dashboard upload contained only `landing/index.html`;
there is no Worker script, binding, paid plan, or Git integration. Cloudflare
creates the DNS and TLS setup for the Worker custom domains.

`wrangler.jsonc` records the equivalent asset-only configuration for a later
automated deployment. It selects `landing/` as the asset directory. At present,
committing changes to this repository does **not** update the live Worker. A
new landing page must be uploaded in the Cloudflare Workers dashboard until a
scoped automated deployment path is configured.

For the future reader, keep generated news data out of Git as required by
`GOLDEN.md`. A scheduled generator can publish a complete static output using
a scoped Cloudflare token and Wrangler. Cloudflare's default asset headers
make mutable HTML and JSON revalidate; a client that should change while open
must request the new data itself.
