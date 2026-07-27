from pathlib import Path
import json
import tempfile
import unittest

from util.epitome_lib.summary_site import (
    build_summary_site,
    markdown_to_html,
)


class SummarySiteTest(unittest.TestCase):
    def test_markdown_is_rendered_without_raw_html(self):
        html = markdown_to_html(
            "# Heading\n\n<script>alert(1)</script>\n\n"
            "[Source](https://example.com/) and **bold**."
        )
        self.assertIn("<h1>Heading</h1>", html)
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)
        self.assertIn('<a href="https://example.com/">Source</a>', html)
        self.assertIn("<strong>bold</strong>", html)

    def test_build_site_from_external_markdown_catalog(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            summaries = root / "summaries"
            articles = summaries / "articles"
            articles.mkdir(parents=True)
            source_url = "https://example.com/article"
            summary = articles / "article.md"
            summary.write_text(
                f"""---
status: complete
confidence: 0.9
title: "Example article"
source_url: "{source_url}"
---

This is a complete and sufficiently long article summary for the generated
site. It contains more than one hundred characters and links to the
[original article]({source_url}).
""",
                encoding="utf-8",
            )
            catalog = summaries / "catalog.json"
            catalog.write_text(
                json.dumps(
                    [
                        {
                            "content_path": "articles/article.md",
                            "model": "gpt-5.6-terra",
                            "source_url": source_url,
                        }
                    ]
                ),
                encoding="utf-8",
            )
            output = root / "dist"
            result = build_summary_site(catalog, output)
            self.assertEqual(result["complete"], 1)
            index = (output / "index.html").read_text(encoding="utf-8")
            article_pages = list((output / "articles").glob("*.html"))
            self.assertIn("Example article", index)
            self.assertIn('class="summary-list"', index)
            self.assertIn('class="crystal"', index)
            self.assertIn("Summaries in Epitome", index)
            self.assertEqual(len(article_pages), 1)
            article = article_pages[0].read_text(encoding="utf-8")
            self.assertIn("Original OpenAI article", article)
            self.assertIn('class="infobox"', article)


if __name__ == "__main__":
    unittest.main()
