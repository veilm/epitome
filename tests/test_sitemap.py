import unittest

from pathlib import Path
import runpy

from research.sitemap import locations, rendered_xml


CDP_LISTER = runpy.run_path(
    str(Path(__file__).resolve().parents[1] / "research/list_sitemap_urls_cdp"),
    run_name="epitome_sitemap_cdp_test",
)
included = CDP_LISTER["included"]


class SitemapTest(unittest.TestCase):
    def test_urlset(self):
        child, urls = locations(
            b'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            b"<url><loc>https://example.com/a</loc></url></urlset>"
        )
        self.assertEqual(child, [])
        self.assertEqual(urls, ["https://example.com/a"])

    def test_index(self):
        child, urls = locations(
            b'<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            b"<sitemap><loc>https://example.com/one.xml</loc></sitemap>"
            b"</sitemapindex>"
        )
        self.assertEqual(child, ["https://example.com/one.xml"])
        self.assertEqual(urls, [])

    def test_browser_lister_path_filters(self):
        self.assertTrue(included("https://example.com/news/a", ["/news/"], []))
        self.assertFalse(included("https://example.com/research/a", ["/news/"], []))
        self.assertFalse(
            included("https://example.com/news/drafts/a", ["/news/"], ["/news/drafts/"])
        )

    def test_chromium_xml_viewer_prefix(self):
        xml = rendered_xml(
            "This XML file does not appear to have any style information.\n\n"
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            "<url><loc>https://example.com/a</loc></url></urlset>"
        )
        self.assertEqual(locations(xml), ([], ["https://example.com/a"]))

    def test_plain_text_xml_declaration(self):
        xml = rendered_xml(
            '<?xml version="1.0"?><sitemapindex>'
            "<sitemap><loc>https://example.com/one.xml</loc></sitemap>"
            "</sitemapindex>"
        )
        self.assertEqual(locations(xml), (["https://example.com/one.xml"], []))


if __name__ == "__main__":
    unittest.main()
