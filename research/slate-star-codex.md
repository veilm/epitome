# Slate Star Codex

## Canonical scope

The historical WordPress site at `https://slatestarcodex.com/` was inspected
through Chromium/CDP on 2026-08-10 while the Paul Graham crawl was active. The
homepage is still a rendered first-party archive with about 75,000 visible
characters and links to the archive, about/top-posts material, monthly indexes,
RSS, and the successor site.

`https://slatestarcodex.com/archives/` is the authoritative post inventory. Its
rendered page contains 1,906 links, including 1,558 distinct canonical post
URLs matching the site's dated `/YYYY/MM/DD/slug/` structure. The reviewed
source list in `sources/slate-star-codex.txt` contains those posts in the
archive's newest-to-oldest order plus four structural identities:

- homepage;
- about page;
- complete archives page; and
- curated top-posts page.

This yields 1,562 approved identities. Monthly/category/tag listings, RSS and
comments feeds, WordPress service endpoints, and the separate Astral Codex Ten
Substack are not duplicated into this scope. Comments embedded on individual
post pages remain part of each historical page and need explicit pilot review;
they are not equivalent to crawling the global comments feed.

## Validation plan

Before any page batch begins:

1. capture and locally replay the complete archives page;
2. validate a short ordinary post, an image-bearing post, a very long top post,
   and a comment-heavy/open-thread page;
3. measure whether server-rendered comments, pagination, MathJax/code, images,
   and outbound embeds survive script-free replay;
4. inventory external media without downloading YouTube or Twitter/X; and
5. require complete manifests, closed capture tabs, clean rendered-image
   audits, and zero production-origin requests during local replay.

The successor `astralcodexten.com` remains a separate source because its
Substack structure and free/paywalled/email variants require their own scope.
