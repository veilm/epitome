from pathlib import Path
import json
import tempfile
import unittest

from util.epitome_lib.refresh import build_plan, clean_url, filter_urls, parse_sitemap


class RefreshTest(unittest.TestCase):
    def test_parse_sitemap_index_and_urlset(self):
        children, urls = parse_sitemap(
            'This XML file has no style.\n<sitemapindex xmlns="x">'
            '<sitemap><loc>https://example.com/posts.xml</loc></sitemap></sitemapindex>'
        )
        self.assertEqual(children, ["https://example.com/posts.xml"])
        self.assertEqual(urls, [])
        children, urls = parse_sitemap(
            '<urlset xmlns="x"><url><loc>https://example.com/p/a</loc></url></urlset>'
        )
        self.assertEqual(children, [])
        self.assertEqual(urls, ["https://example.com/p/a"])

    def test_filter_urls_scopes_normalizes_and_deduplicates(self):
        urls = filter_urls(
            ["https://WWW.Example.com/p/new?utm_source=x#part",
             "https://www.example.com/p/new/", "https://evil.test/p/new",
             "https://www.example.com/about", {"unexpected": "link"}],
            {"hosts": ["example.com"], "include_path_regex": r"^/p/"},
        )
        self.assertEqual(urls, ["https://www.example.com/p/new"])

    def test_build_plan_compares_requested_and_final_identities(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            page = root / "example" / "capture"
            page.mkdir(parents=True)
            (page / "page.html").write_text("ok", encoding="utf-8")
            (page / "manifest.json").write_text(json.dumps({
                "complete": True,
                "requested_url": "https://example.com/old",
                "final_url": "https://example.com/current",
            }), encoding="utf-8")
            plan = build_plan(
                {"sources": [{"id": "example", "archive_directory": "example",
                              "discovery": {"type": "links"}}]},
                root,
                lambda _: ["https://example.com/old/",
                           "https://example.com/current",
                           "https://example.com/new"],
                max_new=5,
            )
            record = plan["sources"][0]
            self.assertEqual(record["new_urls"], ["https://example.com/new"])
            self.assertEqual(record["status"], "ready")

    def test_inventory_separates_old_backlog_from_new_discovery(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            inventory = root / "known.txt"
            inventory.write_text("https://example.com/known\n", encoding="utf-8")
            plan = build_plan(
                {"sources": [{"id": "example", "archive_directory": "example",
                              "inventory": str(inventory),
                              "discovery": {"type": "links"}}]},
                root,
                lambda _: ["https://example.com/known", "https://example.com/new"],
            )
            record = plan["sources"][0]
            self.assertEqual(record["new_urls"], ["https://example.com/new"])
            self.assertEqual(record["known_uncaptured_urls"],
                             ["https://example.com/known"])

    def test_clean_url_can_retain_semantic_query(self):
        self.assertEqual(clean_url("https://example.com/p?a=1#x", drop_query=False),
                         "https://example.com/p?a=1")

    def test_filter_urls_can_canonicalize_host_aliases(self):
        self.assertEqual(
            filter_urls(
                ["https://www.example.com/post", "https://external.test/post"],
                {"hosts": ["example.com"], "canonical_host": "example.com"},
            ),
            ["https://example.com/post"],
        )


if __name__ == "__main__":
    unittest.main()
