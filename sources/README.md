# Source inventories

These tracked URL lists define reviewed, bounded capture scopes. They are small
inputs to the general `util/capture_urls` runner; raw captures remain outside
Git.

Each list should contain one reviewed URL identity per line. Prefer canonical
URLs, but retain distinct first-party sitemap identities until capture manifests
prove that they are aliases. Before expanding a list,
verify the source's own index or sitemap, document exclusions and broken links
in `research/`, and deduplicate against existing archive roots at capture time.

Current reviewed lists:

- `dario-amodei.txt`: homepage plus five self-hosted writings;
- `andrej-karpathy-blog.txt`: homepage, About page, RSS feed, and 23 dated blog
  posts. Captured Disqus threads are rendered statically during replay;
- `peter-steinberger-blog.txt`: homepage, About page, all-posts index, RSS feed,
  and 112 article identities from the first-party sitemap. Pagination and tag
  archives are deferred to a later phase;
- `dwarkesh-podcast.txt`: homepage, public podcast feed, archive/about/podcast
  indexes, and 178 first-party Substack post identities.

Example:

```sh
util/capture_urls \
  --url-file sources/dario-amodei.txt \
  --output-root /mnt2/capsule/epitome/dario-amodei/crawls/RUN_TIMESTAMP \
  --existing-root /mnt2/capsule/epitome/dario-amodei \
  --max-urls 6 \
  --port 2103 \
  --delay-seconds 30
```
