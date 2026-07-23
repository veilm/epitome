import unittest

from research.sitemap import locations


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


if __name__ == "__main__":
    unittest.main()
