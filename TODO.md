# Epitome source backlog

This is the working backlog for sources Epitome may preserve after the current
OpenAI crawl. Each source should eventually have both a faithful private archive
and a clean, model-readable rendition suitable for summaries. Investigation and
small validation samples come before any large crawl.

## Source backlog

- [ ] **Company careers and job listings**
  - [ ] Add OpenAI careers and individual job listings to the OpenAI archive
        scope.
  - [ ] Add Anthropic's careers index and individual Greenhouse job listings to
        the Anthropic archive scope.
  - [ ] Preserve title, team, location, description, requirements, compensation
        where published, stable external job ID, first/last-seen timestamps, and
        removal history. Job listings need incremental snapshots because their
        historical value is largely in openings that later disappear.
- [ ] **Anthropic — first next investigation**
  - [x] Inventory Anthropic's official blog, newsroom, research, policy, safety,
        product, and other company-post collections.
  - [x] Treat the company publications on `anthropic.com` and the separate
        product/technical blog on `claude.com` as related but distinct sources.
  - [ ] Complete the Dario Amodei inventory from the seeds and gaps documented
        in `research/dario-amodei.md`; neither his homepage nor the independent
        interview index is exhaustive.
  - [x] Capture and offline-verify Dario Amodei's bounded personal-site scope:
        the homepage and all five self-hosted writings.
  - [x] Identify feeds, sitemaps, media embeds, PDFs, and related official
        Anthropic properties before defining crawl boundaries.
  - [x] Complete and offline-verify the approved first 160 Anthropic page URLs.
  - [x] Inventory the 34 pending YouTube videos used by 22 captured articles in
        `inventories/anthropic-youtube.json`.
  - [ ] Import those videos through the external downloader and connect replay
        to the files recorded in the inventory.
  - [x] Fix script-disabled Claude.com Webflow rendering and validate a bounded
        five-page blog sample before beginning a larger crawl.
  - [x] Archive and offline-verify all 201 inventoried Claude.com blog URL
        identities across bounded, deduplicated batches.
  - [x] Inventory the 81 pending YouTube videos used by 58 captured Claude.com
        articles in `inventories/claude-youtube.json`.
  - [ ] Import those videos through the external downloader and connect replay
        to the files recorded in the inventory.
  - [ ] Build and validate archive, model-readable extraction, and summary flows.
- [ ] **Twitter/X**
  - [ ] Define curated Twitter lists and accounts to preserve.
  - [ ] Preserve posts, threads, quoted/replied-to context, media, timestamps,
        authorship, and outbound links where available.
  - [ ] Design incremental updates and deletion/change history without repeatedly
        downloading posts already captured.
- [ ] **YouTube**
  - [ ] Define channels and playlists, beginning with Theo's videos.
  - [ ] Preserve video/audio, titles, descriptions, dates, thumbnails, chapters,
        captions or transcripts, and important outbound links.
  - [ ] Produce model-readable transcripts and article-style summaries.
- [ ] **Substack and newsletters**
  - [x] Inventory Dwarkesh Patel's 183-URL first-party publication scope and
        validate one long transcript/video post through offline replay.
  - [x] Inventory the representative post's Substack-hosted and YouTube video
        identities and stable import locations.
  - [ ] Validate essay-only and older audio-first Dwarkesh variants; inventory
        podcast audio and caption files before starting a larger page batch.
  - [ ] SemiAnalysis.
  - [ ] Preserve posts, podcast/video embeds, images, attachments, publication
        metadata, and links between installments.
- [ ] **Individual writers and personal blogs**
  - [x] Inventory Peter Steinberger's canonical 116-URL core blog scope and
        validate one representative rendered article plus its official Markdown
        mirror.
  - [x] Capture and offline-verify the first varied 15-page Peter batch; restore
        the lost 2016 iWork image from its surviving canonical copy and render
        preserved tweet text without Twitter JavaScript.
  - [ ] Capture the remaining 100 Peter Steinberger core URLs in bounded batches,
        track the unrecovered 2020 SwiftUI image, then preserve the deferred
        pagination and tag archives separately.
  - [x] Inventory Andrej Karpathy's canonical 26-page blog scope and validate
        article, image, and static Disqus-comment preservation.
  - [x] Capture and offline-verify all 26 canonical Karpathy blog URLs, including
        representative static Disqus threads.
  - [ ] Recover archival copies of the five unavailable outbound research PDFs
        listed in `research/andrej-karpathy.md`.
  - [ ] Inventory each person's canonical blog, essays, talks, and other
        first-party writing before defining capture scope.
- [ ] **One-off essay and forecast sites**
  - [ ] AI 2027.
  - [ ] AI 2040.
  - [ ] *Situational Awareness* essay series.
  - [ ] Identify the canonical site and complete page/media set for each before
        capture.
- [ ] **near.blog and Near's link graph**
  - [ ] Preserve near.blog itself.
  - [ ] Inventory and prioritize the sites, essays, papers, videos, and other
        material Near links to.
  - [ ] Record provenance from each outbound item back to the Near page that
        referenced it; bound recursive discovery before crawling.
- [ ] **LessWrong**
  - [ ] Preserve the Sequences and their canonical ordering.
  - [ ] Preserve daily/top-ranked article collections and their ranking/date
        context.
  - [ ] Define broader coverage for notable posts, series, authors, comments,
        and linked media.
- [ ] **Nonfiction books**
  - [ ] Start a title and edition inventory, beginning with *The Elephant in the
        Brain*.
  - [ ] Determine lawful source material available for each book and preserve
        edition, author, publication, and pagination metadata.
  - [ ] Create model-readable text and summaries only from material we are
        permitted to process and retain.

## Checklist for every new source

- [ ] Locate canonical indexes, feeds, sitemaps, APIs, and stable identifiers.
- [ ] Document access constraints, provenance, update cadence, and crawl limits.
- [ ] Deduplicate against all prior captures and support incremental refreshes.
- [ ] Use bounded samples and source-appropriate delays before approving scale.
- [ ] Preserve substantive images, audio, video, documents, captions, and link
      context—not merely page text.
- [ ] Verify offline replay cannot silently fall back to the live source.
- [ ] Extract compact, model-readable content independently of visual replay.
- [ ] Add source-specific completeness checks and retry ledgers.
- [ ] Add summaries only after archive and extraction quality are validated.
