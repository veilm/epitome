from pathlib import Path
import json
import tempfile
import unittest

from util.epitome_lib.capture import (
    redact_capture_headers,
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


if __name__ == "__main__":
    unittest.main()

