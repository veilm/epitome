# Epitome

Epitome researches and implements a faithful, archival clone of the public
OpenAI website, plus conversion of OpenAI blog posts to clean Markdown.

## Workflow

- Use auto commit behaviour: make one `msk_git ca` commit per logical change.
- Keep investigation notes, code, schemas, and small hand-written fixtures in
  Git.
- Do not commit downloaded pages, media, crawl databases, generated archives,
  or other captured site data.
- Keep exploratory crawls bounded. Do not start a large crawl without explicit
  user approval.
- Respect access controls and record provenance, timestamps, response metadata,
  redirects, and canonical URLs so captures can be reproduced and audited.

## Verification

- Run focused tests for any implemented crawler or converter.
- Before committing, inspect `git status` and confirm captured/generated data is
  ignored.

