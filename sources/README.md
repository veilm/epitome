# Source inventories

These tracked URL lists define reviewed, bounded capture scopes. They are small
inputs to the general `util/capture_urls` runner; raw captures remain outside
Git.

Each list should contain one canonical URL per line. Before expanding a list,
verify the source's own index or sitemap, document exclusions and broken links
in `research/`, and deduplicate against existing archive roots at capture time.

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

