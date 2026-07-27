from pathlib import Path
import json
import tempfile
import unittest

from util.epitome_lib.replay import (
    CaptureIndex,
    decode_url,
    encode_url,
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

    def test_index_only_accepts_complete_bodies(self):
        with tempfile.TemporaryDirectory() as temp:
            index = self.make_capture(Path(temp))
            self.assertIsNotNone(index.resource("https://example.com/image.png"))
            image = next(Path(temp).rglob("image/response-body.bin"))
            image.write_bytes(b"cut")
            index = CaptureIndex.from_roots([Path(temp)])
            self.assertIsNone(index.resource("https://example.com/image.png"))


if __name__ == "__main__":
    unittest.main()
