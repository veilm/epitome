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
            pages_catalog = root / "pages.json"
            pages_catalog.write_text(
                json.dumps(
                    {
                        "sources": [
                            {
                                "id": "example",
                                "name": "Example source",
                                "logo_url": "https://example.com/favicon.png",
                            }
                        ],
                        "pages": [
                            {
                                "captured_at": 20,
                                "published_at": 1741046400,
                                "source": "example",
                                "title": "Example article",
                                "url": source_url,
                            },
                            {
                                "captured_at": 19,
                                "published_at": None,
                                "source": "example",
                                "title": "An undated page",
                                "url": "https://example.com/undated",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = build_summary_site(catalog, output, pages_catalog)
            self.assertEqual(result["complete"], 1)
            self.assertEqual(result["pages"], 2)
            index = (output / "index.html").read_text(encoding="utf-8")
            article_pages = list((output / "articles").glob("*.html"))
            self.assertIn("Example article", index)
            self.assertIn('class="feed"', index)
            self.assertIn('class="crystal crystal-facet"', index)
            self.assertIn('data-crystal="outline-color"', index)
            self.assertIn('src="https://example.com/favicon.png"', index)
            self.assertNotIn("A living archive of machine intelligence", index)
            self.assertNotIn('href="/">Catalog</a>', index)
            self.assertIn("Archived publications", index)
            self.assertIn('target="_blank"', index)
            self.assertIn('data-source-filter checked', index)
            self.assertIn('id="sort-order"', index)
            self.assertIn('id="summary-filter"', index)
            self.assertIn('class="summary-link"', index)
            self.assertEqual(len(article_pages), 1)
            article = article_pages[0].read_text(encoding="utf-8")
            self.assertIn("Original article", article)
            self.assertIn('class="infobox"', article)
            variants = (output / "logo-variants.html").read_text(encoding="utf-8")
            settings = (output / "settings.html").read_text(encoding="utf-8")
            self.assertEqual(variants, settings)
            self.assertIn("Site settings", settings)
            self.assertIn('id="theme-setting"', settings)
            self.assertIn('id="source-border-setting"', settings)
            self.assertIn('value="facet-outline-color"', settings)
            self.assertIn('value="facet-outline-ink"', settings)
            self.assertIn('value="prism-outline-color"', settings)
            self.assertIn('value="prism-outline-ink"', settings)
            self.assertIn('value="cathedral-adaptive"', settings)
            self.assertIn('value="cathedral-ink"', settings)
            self.assertIn('value="outline-color"', settings)
            self.assertIn('value="outline-ink"', settings)
            self.assertIn('value="outline-dusk"', settings)
            self.assertIn('value="cathedral"', settings)
            self.assertIn("Facet", variants)
            self.assertIn("Prism", variants)
            self.assertIn("Orbit", variants)
            stylesheet = (output / "style.css").read_text(encoding="utf-8")
            self.assertIn('html[data-theme="dark"]', stylesheet)
            self.assertIn('html[data-source-border="on"]', stylesheet)


if __name__ == "__main__":
    unittest.main()
