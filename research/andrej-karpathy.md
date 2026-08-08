# Andrej Karpathy blog reconnaissance

Checked on 2026-08-07 through Chromium/CDP. This note covers the canonical
first-party blog at `https://karpathy.github.io/`; it does not yet claim to be a
complete inventory of Karpathy's writing on Medium, X, GitHub, `karpathy.ai`, or
other publications.

## Canonical blog scope

The rendered homepage lists 23 dated posts from 2011 through 2026. Together
with the homepage, About page, and RSS feed, the bounded site scope is 26 URLs.
The reviewed input is tracked at `sources/andrej-karpathy-blog.txt`.

The homepage and RSS feed agree on the current recent posts, while the homepage
is the complete historical index. The 2018 “started posting on Medium instead”
entry is retained because it is itself a canonical dated page and provides
provenance to the separate Medium corpus. Links to `karpathy.ai`, GitHub gists,
Colab notebooks, papers, and videos are outbound dependencies to inventory
separately rather than silently folding into this blog scope.

## Capture considerations

The pages are static Jekyll HTML with ordinary first-party images and long code
blocks, so the generic browser capture should preserve the primary article
content without a site-specific parser. The representative `microgpt` post has
roughly 35,000 characters of article text and one substantive first-party image.

Posts also embed Disqus. Comments live in a cross-origin, script-driven iframe
and are not part of the article DOM. A representative `microgpt` capture retained
the complete Disqus thread payload: 35 comments with authors, timestamps,
scores, parent relationships, and message HTML. Epitome's replay layer now
converts captured `disqus-threadData` into a static offline discussion, without
executing Disqus scripts or contacting production servers.

The representative post passed capture and replay validation with zero capture
or asset failures, its primary image loaded locally, all 35 comments rendered,
and a replay reload made zero external requests. The tracked 26-URL blog scope
is therefore ready for a bounded crawl.
