from pathlib import Path
import json
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import threading
import unittest

from util.epitome_lib.assets import (
    asset_priority,
    complete_body,
    complete_capture_assets,
    discover_html_assets,
    discover_vimeo_progressive_asset,
    discover_vimeo_video_asset,
)
from util.epitome_lib.capture import (
    archival_url_key,
    completed_capture_urls,
    redact_capture_headers,
    recommended_page_delay,
    summarize_crawl,
    summarize_network,
    url_slug,
    validate_url,
)


class _AssetHandler(BaseHTTPRequestHandler):
    body = b"complete media body"

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "video/mp4")
        self.send_header("Content-Length", str(len(self.body)))
        self.end_headers()
        self.wfile.write(self.body)

    def log_message(self, format, *args):
        pass


class CaptureHelpersTest(unittest.TestCase):
    def test_url_validation_and_slug(self):
        self.assertEqual(
            url_slug("https://openai.com/index/example/?x=1"),
            "openai.com-index-example",
        )
        self.assertEqual(validate_url("https://example.com/a"), "https://example.com/a")
        with self.assertRaises(ValueError):
            validate_url("file:///tmp/page.html")

    def test_completed_capture_urls_normalizes_and_requires_complete_html(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            complete = root / "complete"
            complete.mkdir()
            (complete / "page.html").write_text("<html></html>", encoding="utf-8")
            (complete / "manifest.json").write_text(
                json.dumps(
                    {
                        "complete": True,
                        "requested_url": "HTTPS://OPENAI.COM/index/example/",
                        "final_url": "https://openai.com/index/example/#section",
                    }
                ),
                encoding="utf-8",
            )
            incomplete = root / "incomplete"
            incomplete.mkdir()
            (incomplete / "page.html").write_text("<html></html>", encoding="utf-8")
            (incomplete / "manifest.json").write_text(
                json.dumps(
                    {
                        "complete": False,
                        "requested_url": "https://openai.com/index/retry/",
                    }
                ),
                encoding="utf-8",
            )
            self.assertEqual(
                completed_capture_urls([root]),
                {"https://openai.com/index/example"},
            )
            self.assertEqual(
                archival_url_key("https://openai.com/index/example/"),
                "https://openai.com/index/example",
            )

    def test_completed_capture_urls_follows_external_archive_symlink(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            external = root / "external"
            capture = external / "capture"
            capture.mkdir(parents=True)
            (capture / "page.html").write_text("<html></html>", encoding="utf-8")
            (capture / "manifest.json").write_text(
                json.dumps(
                    {
                        "complete": True,
                        "requested_url": "https://example.com/external/",
                    }
                ),
                encoding="utf-8",
            )
            local = root / "local"
            local.mkdir()
            (local / "captures").symlink_to(external, target_is_directory=True)
            self.assertEqual(
                completed_capture_urls([local]),
                {"https://example.com/external"},
            )

    def test_page_delay_scales_with_batch_size(self):
        self.assertEqual(recommended_page_delay(10), 10)
        self.assertEqual(recommended_page_delay(20), 15)
        self.assertEqual(recommended_page_delay(40), 20)
        self.assertEqual(recommended_page_delay(80), 30)
        self.assertEqual(recommended_page_delay(81), 45)

    def test_summary_and_header_redaction(self):
        with tempfile.TemporaryDirectory() as temp:
            network = Path(temp) / "network"
            item = network / "one"
            item.mkdir(parents=True)
            (item / "metadata.json").write_text(
                json.dumps(
                    {
                        "url": "https://example.com/data.json",
                        "status": "200",
                    }
                ),
                encoding="utf-8",
            )
            (item / "request-headers.json").write_text(
                json.dumps({"Cookie": "secret", "accept": "*/*"}),
                encoding="utf-8",
            )
            (item / "response-headers.json").write_text(
                json.dumps({"set-cookie": "secret", "content-type": "application/json"}),
                encoding="utf-8",
            )
            (item / "response-body.bin").write_bytes(b"{}")

            self.assertEqual(redact_capture_headers(network), 2)
            headers = json.loads((item / "request-headers.json").read_text())
            self.assertEqual(headers["Cookie"], "[redacted]")
            summary = summarize_network(network)
            self.assertEqual(summary["requests"], 1)
            self.assertEqual(summary["response_bytes"], 2)
            self.assertEqual(summary["hosts"], {"example.com": 1})

    def test_crawl_summary(self):
        with tempfile.TemporaryDirectory() as temp:
            crawl = Path(temp)
            page = crawl / "pages" / "000001-example"
            page.mkdir(parents=True)
            (page / "page.html").write_text("<html></html>", encoding="utf-8")
            (page / "read.json").write_text("{}", encoding="utf-8")
            (page / "manifest.json").write_text(
                json.dumps(
                    {
                        "requested_url": "https://example.com/article",
                        "complete": True,
                        "capture_started_at": 10,
                        "capture_finished_at": 15,
                        "redacted_header_values": 2,
                        "asset_completion": {
                            "attempted": 4,
                            "completed": 3,
                            "failed": 1,
                        },
                        "network_summary": {
                            "requests": 3,
                            "response_bodies": 2,
                            "response_bytes": 100,
                            "response_body_errors": 1,
                            "hosts": {"example.com": 3},
                            "statuses": {"200": 3},
                        },
                    }
                ),
                encoding="utf-8",
            )
            summary = summarize_crawl(crawl)
            self.assertEqual(summary["pages"], 1)
            self.assertEqual(summary["complete_pages"], 1)
            self.assertEqual(summary["requests"], 3)
            self.assertEqual(summary["response_bytes"], 100)
            self.assertEqual(summary["asset_attempts"], 4)
            self.assertEqual(summary["assets_completed"], 3)
            self.assertEqual(summary["asset_failures"], 1)
            self.assertEqual(summary["page_summaries"][0]["duration_seconds"], 5)

    def test_asset_discovery(self):
        urls = discover_html_assets(
            """
            <video poster="/poster.jpg"><source src="/movie.mp4"></video>
            <img src="/small.jpg" srcset="/medium.jpg 2x, /large.jpg 3x">
            <link rel="canonical" href="/article">
            <link rel="stylesheet" href="/site.css">
            <a href="/paper.pdf">Paper</a>
            """,
            "https://example.com/posts/one",
        )
        self.assertEqual(
            urls,
            {
                "https://example.com/poster.jpg",
                "https://example.com/movie.mp4",
                "https://example.com/small.jpg",
                "https://example.com/medium.jpg",
                "https://example.com/large.jpg",
                "https://example.com/site.css",
                "https://example.com/paper.pdf",
            },
        )

    def test_asset_discovery_encodes_spaces_in_urls(self):
        self.assertEqual(
            discover_html_assets(
                '<video src="/media/a video (1).mp4"></video>',
                "https://example.com/article/",
            ),
            {"https://example.com/media/a%20video%20(1).mp4"},
        )

    def test_asset_priority_favors_media_and_documents(self):
        urls = [
            "https://example.com/app.js",
            "https://example.com/image.jpg",
            "https://example.com/paper.pdf",
            "https://example.com/movie.mp4",
        ]
        self.assertEqual(
            sorted(urls, key=asset_priority),
            [
                "https://example.com/movie.mp4",
                "https://example.com/paper.pdf",
                "https://example.com/image.jpg",
                "https://example.com/app.js",
            ],
        )

    def test_vimeo_progressive_discovery_prefers_highest_resolution(self):
        html = (
            "<script>window.playerConfig = "
            + json.dumps(
                {
                    "request": {
                        "files": {
                            "progressive": [
                                {
                                    "height": 540,
                                    "width": 960,
                                    "url": "https://video.example/540.mp4",
                                },
                                {
                                    "height": 1080,
                                    "width": 1920,
                                    "url": "https://video.example/1080.mp4",
                                },
                            ]
                        }
                    }
                }
            )
            + ";</script>"
        )
        self.assertEqual(
            discover_vimeo_progressive_asset(html),
            "https://video.example/1080.mp4",
        )

    def test_vimeo_video_discovery_falls_back_to_hls(self):
        html = (
            "<script>window.playerConfig = "
            + json.dumps(
                {
                    "request": {
                        "files": {
                            "hls": {
                                "default_cdn": "archive",
                                "cdns": {
                                    "archive": {
                                        "avc_url": "https://video.example/master.m3u8"
                                    }
                                },
                            }
                        }
                    }
                }
            )
            + ";</script>"
        )
        self.assertEqual(
            discover_vimeo_video_asset(html),
            "https://video.example/master.m3u8",
        )

    def test_partial_response_is_complete_only_when_it_contains_full_entity(self):
        with tempfile.TemporaryDirectory() as temp:
            record = Path(temp)
            (record / "response-body.bin").write_bytes(b"12345")
            (record / "response-headers.json").write_text(
                json.dumps(
                    {
                        "content-length": "5",
                        "content-range": "bytes 0-4/5",
                    }
                ),
                encoding="utf-8",
            )
            self.assertTrue(complete_body(record, {"status": "206"}))
            (record / "response-headers.json").write_text(
                json.dumps(
                    {
                        "content-length": "5",
                        "content-range": "bytes 5-9/10",
                    }
                ),
                encoding="utf-8",
            )
            self.assertFalse(complete_body(record, {"status": "206"}))

    def test_asset_completion_downloads_a_missing_reference(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), _AssetHandler)
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        try:
            with tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                network = root / "network"
                network.mkdir()
                url = f"http://127.0.0.1:{server.server_port}/movie.mp4"
                page = root / "page.html"
                page.write_text(f'<video src="{url}"></video>', encoding="utf-8")
                report = complete_capture_assets(
                    page,
                    network,
                    url,
                    max_assets=1,
                    max_bytes=1024,
                    delay_seconds=0,
                )
                self.assertEqual(report["completed"], 1)
                self.assertEqual(report["downloaded_bytes"], len(_AssetHandler.body))
                bodies = list(network.glob("*/response-body.bin"))
                self.assertEqual(len(bodies), 1)
                self.assertEqual(bodies[0].read_bytes(), _AssetHandler.body)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


if __name__ == "__main__":
    unittest.main()
