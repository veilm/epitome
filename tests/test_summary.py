from pathlib import Path
import json
import tempfile
import unittest

from util.epitome_lib.summary import (
    error_summary,
    parse_front_matter,
    validate_summary,
    write_catalog,
)


class SummaryTest(unittest.TestCase):
    def test_parse_and_validate_summary(self):
        url = "https://example.com/article"
        text = f"""---
status: complete
confidence: 0.8
title: "An article"
source_url: "{url}"
---

This is a sufficiently long summary body. It contains enough prose to pass the
minimum validation because a complete result should never be an empty stub.

Source: [Original article]({url})
"""
        metadata, body = validate_summary(text, url)
        self.assertEqual(metadata["status"], "complete")
        self.assertEqual(metadata["confidence"], 0.8)
        self.assertIn("Original article", body)

    def test_invalid_source_url_is_rejected(self):
        text = """---
status: error
confidence: 1
title: "Broken"
source_url: "https://wrong.example/"
---

The input was empty.
"""
        with self.assertRaises(ValueError):
            validate_summary(text, "https://example.com/")

    def test_generated_error_summary_is_valid(self):
        url = "https://example.com/article"
        text = error_summary(url, "Article", "Codex timed out")
        metadata, body = validate_summary(text, url)
        self.assertEqual(metadata["status"], "error")
        self.assertIn("timed out", body)

    def test_catalog_replaces_an_article_and_keeps_markdown_external(self):
        with tempfile.TemporaryDirectory() as temp:
            catalog = Path(temp) / "catalog.json"
            first = {
                "source_url": "https://example.com/a",
                "content_path": "articles/a.md",
                "status": "complete",
            }
            write_catalog(catalog, first)
            write_catalog(catalog, {**first, "status": "error"})
            entries = json.loads(catalog.read_text(encoding="utf-8"))
            self.assertEqual(entries, [{**first, "status": "error"}])
            self.assertNotIn("content", entries[0])

    def test_input_front_matter_supports_json_values(self):
        metadata, body = parse_front_matter(
            """---
title: "Title"
authors: ["One", "Two"]
published_at: 123
---

Body
"""
        )
        self.assertEqual(metadata["authors"], ["One", "Two"])
        self.assertEqual(metadata["published_at"], 123)
        self.assertEqual(body, "Body")


if __name__ == "__main__":
    unittest.main()
