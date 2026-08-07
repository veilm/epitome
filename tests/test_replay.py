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
    rewrite_css,
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
            self.assertIn('#consent-banner', html)
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
<iframe title="Example on Vimeo" class="opacity-0 player"
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

    def test_index_only_accepts_complete_bodies(self):
        with tempfile.TemporaryDirectory() as temp:
            index = self.make_capture(Path(temp))
            self.assertIsNotNone(index.resource("https://example.com/image.png"))
            image = next(Path(temp).rglob("image/response-body.bin"))
            image.write_bytes(b"cut")
            index = CaptureIndex.from_roots([Path(temp)])
            self.assertIsNone(index.resource("https://example.com/image.png"))

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
