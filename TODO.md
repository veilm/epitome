# Epitome source backlog

This is the working backlog for sources Epitome may preserve after the current
OpenAI crawl. Each source should eventually have both a faithful private archive
and a clean, model-readable rendition suitable for summaries. Investigation and
small validation samples come before any large crawl.

The continuously occupied capture lane, preparation handoff, adaptive alarm
policy, and explicitly low-risk queue are defined in `LOW_RISK_WORKFLOW.md`.

Prefer the easiest well-bounded static source whenever the current page crawl
finishes. Defer account-oriented or continuously changing sources such as
Twitter/X and YouTube until their identity, media, incremental-update, and
deletion-history workflows are explicitly designed.

- [x] Add a plan-first, one-command incremental refresh across configured
      first-party sources; separate newly listed URLs from reviewed historical
      backlog and capture only an explicitly requested delta.
- [x] Run the first all-source refresh and offline-audit its 25 new pages:
      OpenAI 16, Anthropic 2, Claude 6, and SemiAnalysis 1.

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
  - [ ] Inventory and preserve Jack Clark's **Import AI** newsletter at
        `importai.substack.com`, including its archive, post dates, attachments,
        outbound research links, and any email-only differences. Treat it as a
        first-party writer/newsletter scope related to—but distinct from—the
        official Anthropic company archive.
  - [ ] Preserve both Scott Alexander publication eras as separate, linked
        sources: the historical **Slate Star Codex** archive at
        `slatestarcodex.com` and its successor **Astral Codex Ten** at
        `astralcodexten.com`. Inventory canonical posts, archives, comments,
        media, cross-links, and redirects before approving either crawl.
    - [x] Build the reviewed 1,562-identity Slate Star Codex scope from its
          rendered canonical archive, keeping feeds/listing aliases and Astral
          Codex Ten separate pending representative capture validation.
    - [x] Validate the archive, ordinary-post, long-form, political-quiz, and
          comment-heavy open-thread variants through offline replay before any
          Slate Star Codex page batch begins.
    - [x] Capture and offline-audit the first 15 uncaptured identities; repair
          the 52 Gravatar avatars beyond the bounded asset budget.
    - [x] Complete the 30-page deduplicated batch across its original and
          optimized continuation runs; preserve comment text while excluding
          costly Gravatar completion downloads.
    - [x] Capture and offline-audit the next 45 identities with Gravatar
          completion excluded while retaining article images and comment text.
    - [x] Complete and offline-audit the 60-page optimized tranche, including
          a one-page retry after a transient lost CDP session.
    - [x] Capture and offline-audit the next 75 identities with Gravatar
          completion excluded and zero page failures.
    - [x] Capture and offline-audit the next 90 identities with Gravatar
          completion excluded and zero page failures.
    - [x] Complete and offline-audit the 105-page optimized tranche across its
          preserved 91-page run and focused 14-page streaming-asset recovery.
    - [x] Complete the 120-page optimized tranche across its preserved
          96-page run and focused 24-page CDP recovery.
    - [x] Complete and offline-audit the 135-page optimized tranche across its
          preserved 133-page run and focused two-page recovery.
    - [x] Capture and offline-audit the next 150 identities with zero page
          failures under the hardened policy.
    - [ ] Continue the active 165-page optimized batch.
  - [x] Inventory Dwarkesh Patel's 183-URL first-party publication scope and
        validate one long transcript/video post through offline replay.
  - [x] Inventory the representative post's Substack-hosted and YouTube video
        identities and stable import locations.
  - [x] Validate essay/voiceover and older audio-first Dwarkesh variants through
        offline replay, including inline transcript and external-player cases.
  - [x] Inventory the two validated Substack audio assets, source endpoints,
        caption-track lists, and embedded timed-transcript row counts in
        `inventories/dwarkesh-substack-audio.json`.
  - [x] Capture and offline-verify the selected first 15-page Dwarkesh batch;
        recover its expired SSRN paper as a stable local PDF resource.
  - [x] Capture and offline-verify the deduplicated 30-page Dwarkesh batch;
        repair 17 omitted article images and prioritize primary content in
        future asset-completion budgets.
  - [x] Capture and offline-verify the deduplicated 45-page Dwarkesh batch;
        prevent captured HLS playlists from leaking child requests to live Mux
        hosts.
  - [x] Capture and offline-verify the deduplicated 60-page Dwarkesh batch,
        including a successful retry of its one lost temporary CDP session.
  - [x] Complete and offline-verify the final 30-page Dwarkesh remainder; all
        183 approved page identities are archived.
  - [ ] Import Dwarkesh's inventoried audio and video through the external
        downloader and add future publication URLs incrementally.
  - [x] Inventory the 325-identity SemiAnalysis newsletter scope and separate it
        from the corporate/models site and authenticated institutional data.
  - [x] Validate current and historical paywalled SemiAnalysis pages plus a free
        legacy article; repair the sole missing primary image and verify all
        replays remain offline.
  - [x] Compare current SemiAnalysis subscriber emails with their public pages;
        free-account emails preserve the same preview/paywall boundary and are
        not a richer source for paid issues.
  - [x] Capture and offline-verify the first bounded 15-page SemiAnalysis batch;
        repair 43 omitted article/listing images and inventory four Substack
        videos.
  - [x] Capture and preservation-audit the deduplicated 30-page SemiAnalysis
        batch; repair 112 omitted article/listing images and inventory five new
        Substack videos.
  - [x] Capture and preservation-audit the deduplicated 45-page SemiAnalysis
        batch; repair 177 omitted article/listing images.
  - [x] Capture and preservation-audit the deduplicated 60-page SemiAnalysis
        batch; repair 11 omitted article images and inventory one new Substack
        video.
  - [x] Capture and preservation-audit the deduplicated 75-page SemiAnalysis
        increment; recover nine omitted primary figures and 22 listing images.
  - [x] Complete the selected final 97-page SemiAnalysis remainder; retry its
        one lost temporary CDP session and repair 59 article/listing images.
  - [x] Preserve SemiAnalysis posts, images, attachments, publication metadata,
        and links between installments across the approved 325-page scope.
  - [ ] Import the ten inventoried SemiAnalysis Substack videos through the
        external downloader and connect replay to their private media paths.
- [ ] **Individual writers and personal blogs**
  - [x] Inventory Peter Steinberger's canonical 116-URL core blog scope and
        validate one representative rendered article plus its official Markdown
        mirror.
  - [x] Capture and offline-verify the first varied 15-page Peter batch; restore
        the lost 2016 iWork image from its surviving canonical copy and render
        preserved tweet text without Twitter JavaScript.
  - [x] Capture and offline-verify the next 30 oldest Peter identities; recover
        three missing inline images from exact historical Wayback bodies and
        validate a locally playable titleless Vimeo embed.
  - [x] Capture and offline-verify the next 45 Peter identities; recover the
        historical Slack snooze screenshot and relocated emoji archive, and
        render the upstream-blocked Vimeo player as an explicit offline notice.
  - [x] Capture and offline-verify the final 25 Peter Steinberger core URLs;
        recover the full 3h28m Vimeo workshop and make multi-gigabyte media
        replay through bounded byte ranges.
  - [x] Inventory four pending YouTube videos across four Peter articles in
        `inventories/peter-steinberger-youtube.json`.
  - [ ] Import Peter's four YouTube videos; track the two unrecovered 2020 inline
        images, blocked Vimeo player, and four dead outbound citations, then
        preserve the deferred pagination and tag archives separately.
  - [x] Inventory Andrej Karpathy's canonical 26-page blog scope and validate
        article, image, and static Disqus-comment preservation.
  - [x] Capture and offline-verify all 26 canonical Karpathy blog URLs, including
        representative static Disqus threads.
  - [x] Inventory and preserve `karpathy.ai` as a separate first-party
        personal/educational property, including its course and books pages and
        first-party presentation PDF; do not conflate it with the completed
        `karpathy.github.io` blog scope.
  - [x] Inventory Karpathy's single first-party Bear Blog property: homepage,
        index, feed, and 13 dated posts.
  - [x] Inventory Karpathy's canonical Medium profile, About/feed resources, and
        eight authored posts; treat `medium.com/@karpathy` as an alias.
  - [x] Validate and capture the bounded Bear and Medium scopes separately,
        checking Medium bodies for mirrors of the completed Jekyll corpus.
    - [x] Validate Bear homepage, index, exact post dates, long-form layout,
          images, and production-network isolation through local replay.
    - [x] Capture and offline-audit all 16 reviewed Bear identities.
    - [x] Validate Medium profile and full article replay, production-network
          isolation, and body-level distinctness from the Jekyll archive.
    - [x] Capture and offline-audit all 11 reviewed Medium identities.
  - [ ] Recover archival copies of the five unavailable outbound research PDFs
        listed in `research/andrej-karpathy.md`.
  - [x] Preserve Paul Graham's static essay corpus from
        `paulgraham.com/articles.html`; the reviewed 232-identity index-plus-
        essay scope is tracked separately from the homepage, RSS, books, and
        historical language material.
    - [x] Validate the index and four varied essays, then complete and
          offline-audit the first 15-page bounded batch (20/232 total).
    - [x] Capture and offline-audit the next 30 essays (50/232 total).
    - [x] Capture and offline-audit the next 45 essays (95/232 total); classify
          the only failures as the reviewed obsolete Virtumundo layout spacer.
    - [x] Capture and offline-audit the next 60 essays (155/232 total); restore
          the retired Hacker News badge and historical traffic chart from exact
          Wayback bodies.
    - [x] Capture and offline-audit the next 60 essays (215/232 total); retain
          the reviewed legacy spacer/badge handling.
    - [x] Capture and offline-audit the final 17 essays (232/232 total).
  - [ ] Inventory Gwern.net in bounded families—major essays, blog entries, and
        first-party documents—before approving a crawl of its much larger link
        graph.
  - [ ] Inventory and preserve **Cyborgism Wiki** at `cyborgism.wiki` as an
        explicitly low-risk source; define its canonical page scope and
        validate a small varied pilot before bounded capture.
  - [ ] Inventory and preserve all of **Generative Ink** at `generative.ink` as
        an explicitly low-risk source; review its canonical pages, generated
        works, and first-party assets before bounded capture.
  - [ ] Inventory and preserve `https://alien.v01d.zone/` as an explicitly
        low-risk source; define its canonical page and asset scope and validate
        a small varied pilot before bounded capture.
  - [ ] Preserve Eliezer Yudkowsky's fiction page
        `https://www.yudkowsky.net/other/fiction/the-sword-of-good` and inventory
        the writing scope linked from `https://yudkowsky.tumblr.com/writing` as
        explicitly low-risk material, deduplicated against LessWrong.
  - [ ] Preserve Michael Burry's canonical Substack article
        `https://post.substack.com/p/the-ai-revolution-is-here-will-the`
        as an explicitly low-risk page; it is separate from Dwarkesh and Import
        AI.
  - [ ] Preserve Citrini Research's canonical article
        `https://www.citriniresearch.com/p/2028gic` as an explicitly low-risk
        page, with tracking parameters removed.
  - [ ] Inventory each person's canonical blog, essays, talks, and other
        first-party writing before defining capture scope.
- [ ] **One-off essay and forecast sites**
  - [x] Confirm AI 2027's canonical static site and its scenario, summary,
        supplements, about page, PDF, and AI 2040 navigation; prioritize this as
        the easiest next source after SemiAnalysis.
  - [x] Define the bounded 13-URL English AI 2027 inventory in
        `sources/ai-2027.txt`, excluding translations and legacy redirect aliases.
  - [x] Inventory the five-route December 2025 AI Futures Model web app as a
        distinct release between AI 2027 and AI 2040.
  - [x] Validate AI Futures Model application/data preservation through offline
        replay before beginning its bounded capture.
    - [x] Validate homepage model controls, eight forecast states, analysis
          plots, long-settle streaming behavior, and offline network isolation.
    - [x] Capture four canonical routes plus the historical `/results` alias;
          preserve the release and latest-update dates separately.
  - [x] Capture and offline-verify the long AI 2027 homepage pilot; localize SVG
        graph images and inventory its narrated audio plus YouTube companion.
  - [x] Capture and offline-verify all 13 identities in the bounded English
        AI 2027 scope, including the underlying 71-page PDF; correct the
        script-disabled percentage-height image layout in local replay.
  - [x] Inventory AI 2040's canonical Plan A scenario, PDF, about page,
        footnotes, supplements index, and seventeen supplements as a bounded
        22-identity scope in `sources/ai-2040.txt`.
  - [x] Capture and offline-verify the AI 2040 homepage pilot, preserve its
        first-party and substantive citation PDFs, and inventory the non-YouTube
        narration without downloading it.
  - [x] Capture and offline-verify the first varied ten-page AI 2040 batch,
        including the supplements index, long-form articles, the underlying PDF,
        and the Economic Growth Explorer's raw application/code/data.
  - [x] Capture and offline-verify the final deduplicated eleven AI 2040
        identities; retain raw visualization code/data while documenting that
        script-free replay exposes static or inert interactive states.
  - [x] *Situational Awareness* essay series.
    - [x] Inventory the introduction, eight installments, author page, and
          first-party PDF as an eleven-identity bounded scope.
    - [x] Validate the introduction and a long figure-heavy installment; retain
          all WordPress original/responsive assets and the actual 165-page PDF.
    - [x] Capture and offline-verify the final nine identities; restore the two
          unavailable outbound citation PDFs from exact historical copies.
  - [ ] Identify the canonical site and complete page/media set for each before
        capture.
- [ ] **near.blog and Near's link graph**
  - [ ] Preserve near.blog itself.
  - [ ] Inventory and prioritize the sites, essays, papers, videos, and other
        material Near links to.
  - [ ] Record provenance from each outbound item back to the Near page that
        referenced it; bound recursive discovery before crawling.
- [ ] **LessWrong**
  - [x] Distinguish the five Library core collections, 38 moderator-curated
        sequences, 266 community sequences, annual-review winners, and
        moderator-curated post stream from raw karma/popularity.
  - [x] Identify the user's received LessWrong emails as individual Curated
        post notifications and the supported curated RSS feed as the private-
        token-free incremental source.
  - [x] Build a rendered-browser inventory of collection order and stable post
        IDs; the hardened core/curated union contains 1,384 unique posts.
  - [x] Complete and offline-audit the seven-page structural/content pilot,
        including streamed Next.js materialization and comments.
  - [ ] Preserve the Sequences and their canonical ordering in bounded batches,
        beginning with the 50-post Highlights subset.
    - [x] Capture and offline-audit the first 15 ordered Highlights identities
          (14 new after pilot deduplication).
    - [x] Capture and offline-audit Highlights identities 16–30.
    - [x] Capture and offline-audit Highlights identities 31–45.
    - [x] Capture and offline-audit the final six Highlights identities; all 51
          rendered index identities (50 advertised readings plus intro) pass.
  - [ ] Preserve annual-review winners and new moderator-curated posts with
        original-publication and curation-date provenance.
  - [ ] Review standout community sequences explicitly rather than crawling
        all 266 or treating raw top-karma pages as editorial canon.
  - [ ] Define broader coverage for notable authors, comments, revisions, and
        linked media after the curated tiers pass replay validation.
    - [ ] Add the complete public post scope for Janus at
          `https://www.lesswrong.com/users/janus-1` as an explicitly low-risk
          author collection, deduplicated against existing LessWrong captures.
    - [ ] Prioritize the requested LessWrong posts and sequences listed in
          `sources/lesswrong-priority.txt`, deduplicating the already-inventoried
          `d3WgHDBAPYYScp5Em` sequence and all captured member posts.
    - [ ] Include the requested LessWrong wiki page *Highly Advanced
          Epistemology 101 for Beginners* and explicitly prioritize the
          already-inventoried `SqFbMbtxGybdS2gRs` sequence.
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
