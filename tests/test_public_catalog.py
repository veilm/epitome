from pathlib import Path
import json
import tempfile
import unittest

from util.epitome_lib.public_catalog import (
    build_public_catalog,
    extract_page_metadata,
)


class PublicCatalogTest(unittest.TestCase):
    def test_extracts_title_and_json_ld_date(self):
        with tempfile.TemporaryDirectory() as temp:
            page = Path(temp) / "page.html"
            page.write_text(
                '<meta property="og:title" content="A &amp; B">'
                '<script type="application/ld+json">'
                '{"@type":"Article","datePublished":"2026-08-07T16:08:04-04:00"}'
                "</script>",
                encoding="utf-8",
            )
            metadata = extract_page_metadata(page, "https://example.com/post")
            self.assertEqual(metadata["title"], "A & B")
            self.assertEqual(metadata["published_at"], 1786133284)

    def test_extracts_visible_publication_date_but_not_listing_item_date(self):
        with tempfile.TemporaryDirectory() as temp:
            page = Path(temp) / "page.html"
            page.write_text(
                '<meta property="og:title" content="An article">'
                "<main><div>Oct 21, 2025</div></main>",
                encoding="utf-8",
            )
            article = extract_page_metadata(page, "https://example.com/news/article")
            listing = extract_page_metadata(page, "https://example.com/archive")
            self.assertEqual(article["published_at"], 1761004800)
            self.assertIsNone(listing["published_at"])

    def test_build_deduplicates_and_ignores_dependency_hosts(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            config = root / "sources.json"
            config.write_text(
                json.dumps(
                    {
                        "sources": [
                            {
                                "id": "example",
                                "name": "Example",
                                "archive_directory": "example",
                                "hosts": ["example.com"],
                                "undated_paths": ["/2025/03/04/post"],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            for name, captured, title in (("old", 10, "Old"), ("new", 20, "New")):
                capture = root / "archive" / "example" / "crawls" / name
                capture.mkdir(parents=True)
                (capture / "manifest.json").write_text(
                    json.dumps(
                        {
                            "complete": True,
                            "requested_url": "https://example.com/2025/03/04/post/",
                            "capture_started_at": captured,
                        }
                    ),
                    encoding="utf-8",
                )
                (capture / "page.html").write_text(
                    f'<meta property="og:title" content="{title}">', encoding="utf-8"
                )
            dependency = root / "archive" / "example" / "dependencies" / "bad"
            dependency.mkdir(parents=True)
            (dependency / "manifest.json").write_text(
                json.dumps(
                    {
                        "complete": True,
                        "requested_url": "https://other.test/asset",
                        "capture_started_at": 30,
                    }
                ),
                encoding="utf-8",
            )
            (dependency / "page.html").write_text("<title>Asset</title>", encoding="utf-8")
            output = root / "catalog.json"
            result = build_public_catalog(root / "archive", config, output)
            catalog = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(result["pages"], 1)
            self.assertEqual(catalog["pages"][0]["title"], "New")
            self.assertIsNone(catalog["pages"][0]["published_at"])
            self.assertNotIn("capture_path", catalog["pages"][0])
            self.assertEqual(
                catalog["sources"], [{"id": "example", "name": "Example"}]
            )


if __name__ == "__main__":
    unittest.main()
