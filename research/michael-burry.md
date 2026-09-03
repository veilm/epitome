# Michael Burry article

## Public validation and bounded pilot

The canonical first-party page is
`https://post.substack.com/p/the-ai-revolution-is-here-will-the`. It rendered
as `The AI revolution is here. Will the economy survive the transition?` in a
real browser and exposed approximately 41,717 visible body characters, the
article headings, 35 images, and the ordinary public Substack subscribe/sign-in
frame. The page was inspected without logging in, bypassing a paywall, or
using any media downloader; the public preview boundary remains in force.

The one-page pilot is prepared in ignored
`data/michael-burry-article-pilot.txt` and runs with the standard public
settings: CDP port 2103 only, 15-second settle, 120-second page limit,
400-asset limit, two-second asset pacing, 90-second asset timeout, and
30-second inter-page delay. The exact YouTube/Twitter/X asset exclusions remain
in force. At the pilot boundary, require complete tab-closed manifests,
dependency/media and exclusion classification, both image audits, and local
loopback replay of the article and its image/media path before moving on.
