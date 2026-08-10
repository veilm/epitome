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

    def test_visible_date_fallback_preserves_document_order(self):
        with tempfile.TemporaryDirectory() as temp:
            page = Path(temp) / "page.html"
            page.write_text(
                '<meta property="og:title" content="An article">'
                '<main><p>October 27, 2025</p></main>'
                '<aside><time datetime="2026-08-01T00:00">Aug 1, 2026</time></aside>',
                encoding="utf-8",
            )
            metadata = extract_page_metadata(page, "https://example.com/news/article")
            self.assertEqual(metadata["published_at"], 1761523200)

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
                                "logo_url": "https://example.com/favicon.png",
                                "title_overrides": {
                                    "/2025/03/04/post": "Configured title"
                                },
                                "undated_paths": ["/2025/03/04/post"],
                                "exclude_paths": ["/feed"],
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
            excluded = root / "archive" / "example" / "crawls" / "feed"
            excluded.mkdir(parents=True)
            (excluded / "manifest.json").write_text(
                json.dumps(
                    {
                        "complete": True,
                        "requested_url": "https://example.com/feed",
                        "capture_started_at": 40,
                    }
                ),
                encoding="utf-8",
            )
            (excluded / "page.html").write_text("<title>Feed XML</title>", encoding="utf-8")
            output = root / "catalog.json"
            result = build_public_catalog(root / "archive", config, output)
            catalog = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(result["pages"], 1)
            self.assertEqual(catalog["pages"][0]["title"], "Configured title")
            self.assertIsNone(catalog["pages"][0]["published_at"])
            self.assertNotIn("capture_path", catalog["pages"][0])
            self.assertEqual(
                catalog["sources"],
                [
                    {
                        "id": "example",
                        "name": "Example",
                        "logo_url": "https://example.com/favicon.png",
                    }
                ],
            )

    def test_source_can_prefer_h1_over_generic_social_title(self):
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
                                "prefer_h1": True,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            capture = root / "archive" / "example" / "capture"
            capture.mkdir(parents=True)
            (capture / "manifest.json").write_text(
                json.dumps(
                    {
                        "complete": True,
                        "requested_url": "https://example.com/specific-article",
                        "capture_started_at": 10,
                    }
                ),
                encoding="utf-8",
            )
            (capture / "page.html").write_text(
                '<meta property="og:title" content="Generic site title">'
                "<h1>Specific article title</h1>",
                encoding="utf-8",
            )
            output = root / "catalog.json"
            build_public_catalog(root / "archive", config, output)
            catalog = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(catalog["pages"][0]["title"], "Specific article title")


if __name__ == "__main__":
    unittest.main()
