# Archive storage

Large capture data is deliberately outside Git. Repository utilities accept
explicit output and existing-capture roots so each workstation can choose its
own storage without changing portable defaults.

## Delirium layout

The completed OpenAI raw archive lives on the external drive:

```text
/mnt2/capsule/epitome/openai/
├── captures/
└── crawls/
```

The ignored compatibility paths `data/captures` and `data/crawls` are absolute
symlinks to those directories. Replay commands and older notes can therefore
continue using their original paths. Completed-capture discovery follows these
directory symlinks, so default deduplication still sees the external archive.

Store future source corpora beside OpenAI rather than below its directory:

```text
/mnt2/capsule/epitome/anthropic/crawls/
/mnt2/capsule/epitome/darioamodei.com/crawls/
```

For example:

```sh
util/capture_urls --url-file data/anthropic-urls.txt \
  --output-root /mnt2/capsule/epitome/anthropic/crawls/RUN_TIMESTAMP \
  --existing-root /mnt2/capsule/epitome/anthropic \
  --max-urls 20
```

Use explicit source-specific output roots for external storage. Do not make the
portable utilities default to a path that exists only on Delirium.

## Moving or restoring the archive

Before changing a compatibility symlink, stop capture/replay processes that may
write through it. Copy first, compare file counts and apparent bytes, and run an
rsync metadata verification pass. Remove the source only after the comparison
reports no differences. Finally, exercise a known manifest and completed-URL
scan through the compatibility path.
