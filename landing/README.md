# Epitome landing page

`index.html` is the standalone coming-soon page. It has no script, external
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
