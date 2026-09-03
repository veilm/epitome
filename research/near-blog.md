# near.blog

## Public validation and N+1 pilot

The canonical first-party site is `https://near.blog/`. Its public WordPress
home rendered as `near.blog` with approximately 2,102 visible body characters,
35 links, no images, and no iframe, video, or audio element. Representative
public routes are stable server-rendered pages: `/links/` is a 24,397-character
271-link index; `/things/` is a 10,308-character list with 69 images; and
`/heavenbanning/` is a 499-character illustrated post. Additional plain-text
posts include `/llms-are-strangely-shaped-tools/` (3,015 characters) and
`/2024-ai-reflections/` (10,255 characters). `/Glyptodons/` is a small
image-bearing post with one observed missing image, which is retained as a
bounded known-missing-image check.

The prepared N+1 pilot is in ignored `data/near-blog-pilot.txt`. It covers the
home, link index, list page, short illustrated post, two text posts, and the
known-missing-image post. The separate `/this-anime-does-not-exist/` page is
deferred because validation found direct video elements and many historical
`nearcyan.com` image references; it requires a separately bounded media scope.
No account or paywall bypass is in scope. The standard public settings apply:
CDP port 2103 only, 15-second settle, 120-second page limit, 400-asset limit,
two-second asset pacing, 90-second asset timeout, and 30 seconds between
pages. Exact YouTube/Twitter/X asset exclusions remain in force. At the pilot
boundary, require substantive text, image and missing-image classification,
media/redirect classification, and local-only replay with no live-origin
fallback.
