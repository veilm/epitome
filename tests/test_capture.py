from pathlib import Path
import json
import tempfile
import unittest

from util.epitome_lib.capture import (
    redact_capture_headers,
    summarize_crawl,
    summarize_network,
    url_slug,
    validate_url,
)


class CaptureHelpersTest(unittest.TestCase):
    def test_url_validation_and_slug(self):
        self.assertEqual(
            url_slug("https://openai.com/index/example/?x=1"),
            "openai.com-index-example",
        )
        self.assertEqual(validate_url("https://example.com/a"), "https://example.com/a")
        with self.assertRaises(ValueError):
            validate_url("file:///tmp/page.html")

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
            self.assertEqual(summary["page_summaries"][0]["duration_seconds"], 5)


if __name__ == "__main__":
    unittest.main()
