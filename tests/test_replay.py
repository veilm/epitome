from pathlib import Path
import json
import tempfile
import unittest

from util.epitome_lib.replay import (
    CaptureIndex,
    decode_url,
    encode_url,
    normalize_url,
    resource_path,
    resolve_byte_range,
    stable_resource_identity,
    rewrite_css,
    rewrite_hls_playlist,
    rewrite_html,
)


class ReplayTest(unittest.TestCase):
    def make_capture(self, root: Path) -> CaptureIndex:
        page = root / "capture"
        network = page / "network"
        page.mkdir()
        (page / "manifest.json").write_text(
            json.dumps(
                {
                    "capture_started_at": 100,
                    "requested_url": "https://example.com/article/",
                    "final_url": "https://example.com/article/",
                }
            ),
            encoding="utf-8",
        )
        (page / "page.html").write_text(
            """
            <!doctype html><html><head>
            <link rel="preconnect" href="https://example.com">
            <link rel="stylesheet" href="/style.css">
            <script src="/app.js">alert(1)</script>
            </head><body>
            <img src="/image.png">
            <a href="https://outside.example/story">Story</a>
            </body></html>
            """,
            encoding="utf-8",
        )
        for name, url, body, content_type in (
            ("css", "https://example.com/style.css", b"body{background:url('/image.png')}", "text/css"),
            ("image", "https://example.com/image.png", b"image", "image/png"),
        ):
            record = network / name
            record.mkdir(parents=True)
            (record / "metadata.json").write_text(
                json.dumps({"url": url, "status": "200"}),
                encoding="utf-8",
            )
            (record / "response-headers.json").write_text(
                json.dumps(
                    {
                        "content-length": str(len(body)),
                        "content-type": content_type,
                    }
                ),
                encoding="utf-8",
            )
            (record / "response-body.bin").write_bytes(body)
        return CaptureIndex.from_roots([root])

    def test_url_token_round_trip(self):
        url = "https://example.com/a?x=1&y=2"
        self.assertEqual(decode_url(encode_url(url)), url)

    def test_byte_ranges_cover_media_requests_without_loading_full_body(self):
        self.assertEqual(resolve_byte_range(1000, None), (200, 0, 999))
        self.assertEqual(resolve_byte_range(1000, "bytes=0-99"), (206, 0, 99))
        self.assertEqual(resolve_byte_range(1000, "bytes=900-"), (206, 900, 999))
        self.assertEqual(resolve_byte_range(1000, "bytes=-100"), (206, 900, 999))
        self.assertEqual(resolve_byte_range(1000, "bytes=1000-"), (416, 0, -1))
        self.assertEqual(
            resolve_byte_range(1000, "bytes=100-", max_open_ended=200),
            (206, 100, 299),
        )

    def test_normalize_url_encodes_spaces(self):
        self.assertEqual(
            normalize_url(
                "/media/a video (1).mp4",
                "https://example.com/article/",
            ),
            "https://example.com/media/a%20video%20(1).mp4",
        )

    def test_rewrite_removes_execution_and_localizes_fetches(self):
        with tempfile.TemporaryDirectory() as temp:
            index = self.make_capture(Path(temp))
            page = index.page("https://example.com/article/")
            html = rewrite_html(
                page.html_path.read_text(encoding="utf-8"),
                page.url,
                index,
            )
            self.assertNotIn("<script", html)
            self.assertNotIn("preconnect", html)
            self.assertIn('id="epitome-replay-style"', html)
            self.assertNotIn('id="epitome-disqus-comments"', html)
            self.assertIn('#consent-banner', html)
            self.assertIn('aspect-ratio:16/9', html)
            self.assertIn('.transition_wrap{display:none!important}', html)
            self.assertIn('main>section[style*="visibility: hidden"]', html)
            self.assertIn(
                resource_path("https://example.com/style.css"),
                html,
            )
            self.assertIn(
                resource_path("https://example.com/image.png"),
                html,
            )
            self.assertIn("/unavailable/", html)

    def test_css_urls_are_localized(self):
        result = rewrite_css(
            "a{background:url('../image.png')} @import '/more.css';",
            "https://example.com/css/site.css",
        )
        self.assertIn(resource_path("https://example.com/image.png"), result)
        self.assertIn(resource_path("https://example.com/more.css"), result)

    def test_hls_playlist_urls_are_localized(self):
        base = "https://media.example/path/master.m3u8?token=abc"
        playlist = """#EXTM3U
#EXT-X-KEY:METHOD=AES-128,URI="keys/key.bin?x=1"
#EXT-X-MAP:URI='init.mp4'
#EXT-X-STREAM-INF:BANDWIDTH=1000000
video/playlist.m3u8
#EXTINF:4.0,
https://chunks.example/segment-1.ts?token=abc
"""
        result = rewrite_hls_playlist(playlist, base)
        self.assertIn(
            f'URI="{resource_path("https://media.example/path/keys/key.bin?x=1")}"',
            result,
        )
        self.assertIn(
            f"URI='{resource_path('https://media.example/path/init.mp4')}'",
            result,
        )
        self.assertIn(
            resource_path("https://media.example/path/video/playlist.m3u8"),
            result,
        )
        self.assertIn(
            resource_path("https://chunks.example/segment-1.ts?token=abc"),
            result,
        )
        self.assertNotIn("https://chunks.example", result)

    def test_substack_comma_srcset_and_preloads_stay_offline(self):
        proxy = (
            "https://substackcdn.com/image/fetch/$s_!abc!,w_80,h_80,"
            "c_fill,f_auto/https%3A%2F%2Fexample.com%2Fimage.png"
        )
        second = proxy.replace("w_80,h_80", "w_160,h_160")
        source = f'''<html><head>
<link rel="preload" as="style" href="https://substackcdn.com/theme.css">
<link rel="preload" as="font" href="https://fonts.gstatic.com/font.woff2">
</head><body><img srcset="{proxy} 80w, {second} 160w"></body></html>'''
        index = CaptureIndex()
        index.resources[proxy] = object()
        index.resources[second] = object()
        html = rewrite_html(source, "https://example.com/article", index)
        self.assertNotIn("rel=\"preload\"", html)
        self.assertNotIn("https://substackcdn.com", html)
        self.assertNotIn("https://fonts.gstatic.com", html)
        self.assertIn(f"{resource_path(proxy)} 80w", html)
        self.assertIn(f"{resource_path(second)} 160w", html)

    def test_srcset_omits_uncaptured_variant_so_src_can_fallback(self):
        base = "https://example.com/base.png"
        missing = "https://example.com/missing-2x.png"
        source = f'<img src="{base}" srcset="{missing} 2x">'
        html = rewrite_html(source, "https://example.com/article", CaptureIndex())
        self.assertIn(resource_path(base), html)
        self.assertIn('srcset=""', html)
        self.assertNotIn(resource_path(missing), html)

    def test_missing_substack_proxy_falls_back_to_captured_original(self):
        original = "https://images.example/full.png"
        proxy = "https://cdn.example/proxy.png"
        source = (
            f'<article><img src="{proxy}" '
            f"data-attrs='{json.dumps({'src': original})}'></article>"
        )
        index = CaptureIndex()
        index.resources[original] = object()
        html = rewrite_html(source, "https://example.com/article", index)
        self.assertIn(resource_path(original), html)
        self.assertNotIn(resource_path(proxy), html)

    def test_lazy_images_and_vimeo_are_made_static(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            page = root / "capture"
            network = page / "network"
            network.mkdir(parents=True)
            player_url = "https://player.vimeo.com/video/123"
            video_url = "https://video.example/archive.mp4"
            (page / "manifest.json").write_text(
                json.dumps(
                    {
                        "capture_started_at": 100,
                        "requested_url": "https://example.com/article/",
                    }
                ),
                encoding="utf-8",
            )
            (page / "page.html").write_text(
                f"""<html><body><img loading="lazy" src="/image.png">
<iframe class="opacity-0 player"
src="{player_url}"></iframe></body></html>""",
                encoding="utf-8",
            )
            player_html = (
                "<script>window.playerConfig = "
                + json.dumps(
                    {
                        "request": {
                            "files": {
                                "progressive": [
                                    {
                                        "height": 1080,
                                        "width": 1920,
                                        "url": video_url,
                                    }
                                ]
                            }
                        }
                    }
                )
                + ";</script>"
            ).encode()
            for name, url, body, content_type in (
                ("player", player_url, player_html, "text/html"),
                ("video", video_url, b"video", "video/mp4"),
            ):
                record = network / name
                record.mkdir()
                (record / "metadata.json").write_text(
                    json.dumps({"url": url, "status": "200"}),
                    encoding="utf-8",
                )
                (record / "response-headers.json").write_text(
                    json.dumps(
                        {
                            "content-length": str(len(body)),
                            "content-type": content_type,
                        }
                    ),
                    encoding="utf-8",
                )
                (record / "response-body.bin").write_bytes(body)
            index = CaptureIndex.from_roots([root])
            html = rewrite_html(
                (page / "page.html").read_text(encoding="utf-8"),
                "https://example.com/article/",
                index,
            )
            self.assertIn('loading="eager"', html)
            self.assertIn("<video", html)
            self.assertIn("controls", html)
            self.assertIn(resource_path(video_url), html)
            self.assertNotIn("<iframe", html)
            self.assertNotIn("opacity-0", html)

    def test_disqus_thread_data_is_rendered_static(self):
        data = {
            "cursor": {"total": 2},
            "response": {
                "thread": {"clean_title": "Archived post"},
                "posts": [
                    {
                        "id": "100",
                        "parent": None,
                        "depth": 0,
                        "createdAt": "2026-01-01T12:00:00",
                        "points": 2,
                        "author": {"name": "Ada"},
                        "message": '<p>First <a href="https://example.com/x">link</a></p>',
                    },
                    {
                        "id": "101",
                        "parent": "100",
                        "depth": 1,
                        "createdAt": "2026-01-01T13:00:00",
                        "points": 1,
                        "author": {"username": "Grace"},
                        "message": "<p>Reply</p>",
                    },
                ],
            },
        }
        source = (
            '<html><body><script type="text/json" id="disqus-threadData">'
            + json.dumps(data)
            + "</script></body></html>"
        )
        html = rewrite_html(source, "https://disqus.com/embed/comments/", CaptureIndex())
        self.assertNotIn("<script", html)
        self.assertIn('id="epitome-disqus-comments"', html)
        self.assertIn("Archived post — 2 comments", html)
        self.assertIn("Ada", html)
        self.assertIn("Grace", html)
        self.assertIn("First", html)
        self.assertIn("Reply", html)
        self.assertIn('data-parent-id="100"', html)
        self.assertIn("/unavailable/", html)

    def test_twitter_iframe_uses_preserved_server_side_quote(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            index = self.make_capture(root)
            page = root / "capture"
            raw = page / "network" / "raw"
            raw.mkdir()
            tweet = (
                '<blockquote class="twitter-tweet"><p>Archived words</p>— Ada '
                '<a href="https://twitter.com/ada/status/12345">January 1</a>'
                "</blockquote>"
            ).encode()
            (raw / "metadata.json").write_text(
                json.dumps({"url": "https://example.com/article/", "status": "200"}),
                encoding="utf-8",
            )
            (raw / "response-headers.json").write_text(
                json.dumps({"content-length": str(len(tweet)), "content-type": "text/html"}),
                encoding="utf-8",
            )
            (raw / "response-body.bin").write_bytes(tweet)
            index = CaptureIndex.from_roots([root])
            html = rewrite_html(
                '<html><body><iframe title="X Post" data-tweet-id="12345" '
                'src="https://platform.twitter.com/embed/Tweet.html"></iframe></body></html>',
                "https://example.com/article/",
                index,
            )
            self.assertNotIn("<iframe", html)
            self.assertIn("Archived words", html)
            self.assertIn("twitter.com/ada/status/12345", html)

    def test_external_media_iframes_become_bounded_offline_placeholders(self):
        source = '''<html><body>
<iframe src="https://www.youtube-nocookie.com/embed/abcDEF_123"></iframe>
<iframe src="https://embed.podcasts.apple.com/us/podcast/example/id1?i=2"></iframe>
<iframe src="https://open.spotify.com/embed/episode/episode123"></iframe>
</body></html>'''
        html = rewrite_html(source, "https://example.com/article", CaptureIndex())
        self.assertNotIn("<iframe", html)
        self.assertEqual(html.count("epitome-media-placeholder"), 3)
        self.assertIn("YouTube video abcDEF_123", html)
        self.assertIn("Apple Podcasts episode", html)
        self.assertIn("Spotify episode123", html)
        self.assertNotIn("https://www.youtube-nocookie.com", html)

    def test_unpreservable_vimeo_iframe_becomes_offline_placeholder(self):
        player_url = "https://player.vimeo.com/video/123"
        html = rewrite_html(
            f'<html><body><iframe src="{player_url}"></iframe></body></html>',
            "https://example.com/article",
            CaptureIndex(),
        )
        self.assertNotIn("<iframe", html)
        self.assertIn("Vimeo video unavailable", html)
        self.assertIn("live player exposed no preservable media", html)
        self.assertNotIn(player_url, html)

    def test_index_only_accepts_complete_bodies(self):
        with tempfile.TemporaryDirectory() as temp:
            index = self.make_capture(Path(temp))
            self.assertIsNotNone(index.resource("https://example.com/image.png"))
            image = next(Path(temp).rglob("image/response-body.bin"))
            image.write_bytes(b"cut")
            index = CaptureIndex.from_roots([Path(temp)])
            self.assertIsNone(index.resource("https://example.com/image.png"))

    def test_resource_alias_resolves_only_when_original_is_missing(self):
        with tempfile.TemporaryDirectory() as temp:
            index = self.make_capture(Path(temp))
            original = "https://old.example/missing.png"
            replacement = "https://example.com/image.png"
            index.add_resource_aliases({original: replacement})
            self.assertEqual(index.resource(original), index.resource(replacement))

            # Captured originals remain authoritative if an alias is stale.
            index.add_resource_aliases({replacement: "https://example.com/other.png"})
            self.assertIsNotNone(index.resource(replacement))

    def test_resource_alias_cycles_fail_closed(self):
        index = CaptureIndex()
        index.add_resource_aliases(
            {
                "https://example.com/a": "https://example.com/b",
                "https://example.com/b": "https://example.com/a",
            }
        )
        self.assertIsNone(index.resource("https://example.com/a"))

    def test_expiring_ssrn_links_resolve_to_captured_stable_resource(self):
        stale = (
            "https://download.ssrn.com/paper.pdf?X-Amz-Date=old&abstractId=3722562"
        )
        fresh = (
            "https://download.ssrn.com/paper.pdf?X-Amz-Date=fresh&abstractId=3722562"
        )
        identity = "https://download.ssrn.com/paper.pdf?abstractId=3722562"
        self.assertEqual(stable_resource_identity(stale), identity)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            capture = root / "capture"
            network = capture / "network" / "pdf"
            network.mkdir(parents=True)
            (capture / "manifest.json").write_text(
                json.dumps(
                    {
                        "capture_started_at": 100,
                        "requested_url": "https://example.com/article",
                    }
                ),
                encoding="utf-8",
            )
            (capture / "page.html").write_text(
                f'<html><body><a href="{stale}">Paper</a></body></html>',
                encoding="utf-8",
            )
            body = b"%PDF captured"
            (network / "metadata.json").write_text(
                json.dumps({"url": fresh, "status": "200"}), encoding="utf-8"
            )
            (network / "response-headers.json").write_text(
                json.dumps(
                    {
                        "content-length": str(len(body)),
                        "content-type": "application/pdf",
                    }
                ),
                encoding="utf-8",
            )
            (network / "response-body.bin").write_bytes(body)
            index = CaptureIndex.from_roots([root])
            self.assertIsNotNone(index.resource(stale))
            html = rewrite_html(
                (capture / "page.html").read_text(encoding="utf-8"),
                "https://example.com/article",
                index,
            )
            self.assertIn(resource_path(stale), html)
            self.assertNotIn("/unavailable/", html)

    def test_index_ignores_replay_capture_recursion(self):
        with tempfile.TemporaryDirectory() as temp:
            page = Path(temp) / "capture"
            page.mkdir()
            (page / "manifest.json").write_text(
                json.dumps(
                    {
                        "capture_started_at": 100,
                        "requested_url": "http://127.0.0.1:8013/replay/example",
                    }
                ),
                encoding="utf-8",
            )
            (page / "page.html").write_text("<html></html>", encoding="utf-8")
            index = CaptureIndex.from_roots([Path(temp)])
            self.assertEqual(index.pages, {})


if __name__ == "__main__":
    unittest.main()
